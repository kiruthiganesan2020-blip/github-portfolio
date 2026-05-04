import json
import os
import time
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd
from dotenv import load_dotenv

from phase3_retrieval_candidates.pipeline import (
    load_processed_data,
    apply_strict_filters,
    apply_relaxed_filters,
    score_candidates
)
from phase3_retrieval_candidates.schema import PreferenceInput
from phase4_llm_recommendation.pipeline import (
    build_recommendation_prompt,
    _call_google_ai_studio,
    _extract_json_object,
    _validate_and_enrich_recommendations,
    _fallback_recommendations
)

# Configure Production Logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

PROCESSED_CSV = Path("phase1_data_pipeline/output/processed_zomato.csv").resolve()

# Global Dataset Cache to avoid redundant I/O operations
_DATASET_CACHE: Optional[pd.DataFrame] = None

def get_cached_dataset() -> pd.DataFrame:
    """Loads and caches the Zomato dataset in memory."""
    global _DATASET_CACHE
    if _DATASET_CACHE is None:
        logger.info(f"Loading dataset into memory from {PROCESSED_CSV}")
        _DATASET_CACHE = load_processed_data(PROCESSED_CSV)
    return _DATASET_CACHE

def _call_llm_with_retries(prompt: str, model_name: str, max_retries: int = 2) -> str:
    """Wrapper to call LLM with exponential backoff retry logic and environment config validation."""
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY is missing. Cannot make LLM requests.")
        
    last_exception = None
    for attempt in range(max_retries + 1):
        try:
            logger.info(f"LLM Call Attempt {attempt + 1}/{max_retries + 1} using {model_name}...")
            # Underlying _call_google_ai_studio handles the actual API generation
            return _call_google_ai_studio(prompt, model_name=model_name)
        except Exception as e:
            last_exception = e
            logger.warning(f"LLM call failed on attempt {attempt + 1}: {e}")
            if attempt < max_retries:
                time.sleep(1.5 ** attempt)  # Exponential backoff
    
    logger.error("All LLM attempts failed.")
    raise last_exception

def get_recommendations_service(
    location: str,
    budget: float,
    cuisine: str,
    min_rating: float,
    additional_preferences: Optional[List[str]] = None,
    model_name: str = "models/gemini-3-flash-preview",
    top_n: int = 5
) -> Dict[str, Any]:
    """
    Core business logic for generating restaurant recommendations.
    Production-ready refactor with caching, retries, and optimized payloads.
    """
    # 1. Fix Mutable Defaults & Init Preferences safely
    pref = PreferenceInput(
        location=location,
        budget=budget,
        cuisine=cuisine,
        min_rating=min_rating,
        additional_preferences=additional_preferences if additional_preferences is not None else []
    )

    # 2. Retrieval (Phase 3)
    df = get_cached_dataset()
    strict = apply_strict_filters(df, pref)
    
    if strict.empty:
        filtered, strategy = apply_relaxed_filters(df, pref)
        logger.info(f"Strict filters returned 0 results. Fallback to relaxed strategy: {strategy}")
    else:
        filtered, strategy = strict, "strict"
        logger.info(f"Strict filters matched {len(filtered)} candidates.")
    
    candidates = score_candidates(filtered, pref)
    
    # 3. Payload Optimization: Slim down candidate payload to reduce context window and token cost
    top_candidates = []
    for c in candidates[:15]:
        c_dict = c.to_dict()
        top_candidates.append({
            "name": c_dict.get("name"),
            "rating": c_dict.get("rating"),
            "cost": c_dict.get("cost"),
            "cuisine": c_dict.get("cuisine"),
            "location": c_dict.get("location"),
            "highlights": c_dict.get("highlights", [])
        })

    # 4. LLM Recommendation (Phase 4)
    prompt = build_recommendation_prompt(
        user_preferences=pref.__dict__,
        candidates=top_candidates,
        top_n=top_n
    )

    safety_notes = []
    try:
        raw_text = _call_llm_with_retries(prompt, model_name=model_name, max_retries=2)
        parsed = _extract_json_object(raw_text)
        raw_recommendations = parsed.get("recommendations", [])
        
        recommendations = _validate_and_enrich_recommendations(
            raw_recommendations=raw_recommendations,
            candidates=top_candidates,
            top_n=top_n
        )
    except Exception as exc:
        logger.error(f"Failed to generate LLM recommendations. Using fallback. Error: {exc}")
        safety_notes.append(f"LLM call failed: {str(exc)}")
        recommendations = _fallback_recommendations(top_candidates, top_n)

    # Safety Check for empty valid results
    if not recommendations:
        logger.warning("LLM returned empty valid recommendations. Using fallback ranking.")
        safety_notes.append("No valid LLM recommendations after validation; used fallback ranking.")
        recommendations = _fallback_recommendations(top_candidates, top_n)

    return {
        "user_preferences": pref.__dict__,
        "strategy": strategy,
        "recommendations": [r.__dict__ for r in recommendations],
        "safety_notes": safety_notes
    }
