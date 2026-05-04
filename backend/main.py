import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from backend.services import get_recommendations_service
import uvicorn

# Configure production-ready logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Zomato AI Recommendation API",
    description="Production-ready API for personalized restaurant recommendations",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with specific frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserPreferences(BaseModel):
    location: str = Field(..., min_length=2, description="Target city or locality")
    budget: float = Field(..., gt=0, description="Maximum budget threshold")
    cuisine: str = Field(..., description="Preferred cuisine or 'Any'")
    min_rating: float = Field(..., ge=0.0, le=5.0, description="Minimum acceptable rating (0 to 5)")
    
    # Fix mutable default by using default_factory
    additional_preferences: List[str] = Field(default_factory=list, description="Optional special features")
    top_n: int = Field(default=5, gt=0, le=20, description="Number of recommendations to retrieve")

@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint for load balancers."""
    return {"status": "healthy"}

@app.post("/recommend", tags=["Recommendations"])
async def recommend(prefs: UserPreferences):
    """
    Generates AI-powered restaurant recommendations based on strict validation criteria.
    """
    try:
        logger.info(f"Generating recommendations for location: '{prefs.location}', budget: {prefs.budget}")
        
        # Execute the core business logic
        result = get_recommendations_service(
            location=prefs.location,
            budget=prefs.budget,
            cuisine=prefs.cuisine,
            min_rating=prefs.min_rating,
            additional_preferences=prefs.additional_preferences,
            top_n=prefs.top_n
        )
        
        logger.info(f"Successfully retrieved {len(result.get('recommendations', []))} recommendations.")
        return result

    except Exception as e:
        logger.error(f"Internal Server Error during recommendation generation: {str(e)}", exc_info=True)
        # Prevent leaking raw backend exceptions/stack traces to the client
        raise HTTPException(
            status_code=500, 
            detail="An unexpected error occurred while generating recommendations. Please try again later."
        )

if __name__ == "__main__":
    # Use string reference for proper hot-reloading
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
