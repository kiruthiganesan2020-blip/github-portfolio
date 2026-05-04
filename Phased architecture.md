# Phase-Wise Architecture: AI-Powered Restaurant Recommendation System

This architecture breaks the solution into practical phases so you can build, test, and improve the system step by step.

## Phase 1: Foundation and Data Pipeline

### Goal
Set up the project, ingest the Zomato dataset, and prepare clean structured data for downstream processing.

### Core Components
- **Data Source**: Hugging Face Zomato dataset
- **Ingestion Script**: Downloads and loads raw records
- **Preprocessing Module**: Cleans and standardizes fields
- **Storage Layer**: CSV/JSON/SQLite (based on project scope)

### Key Tasks
- Load dataset from source
- Normalize columns (`name`, `location`, `cuisine`, `cost`, `rating`)
- Handle missing or invalid values
- Create reusable filtered dataset for recommendation logic

### Deliverables
- Clean dataset ready for querying
- Reproducible ingestion + preprocessing pipeline

---

## Phase 2: User Preference Collection Layer

### Goal
Capture user intent in a structured way that can be used by both filtering logic and LLM prompts.

### Core Components
- **Input Interface**: Basic web UI (primary source of user preferences)
- **Validation Layer**: Ensures correct input types and ranges
- **Preference Schema**: Standard request object

### Input Schema (Example)
- `location`: string
- `budget`: `low | medium | high`
- `cuisine`: string
- `min_rating`: float
- `additional_preferences`: list of strings

### Key Tasks
- Build input form/API
- Validate and sanitize incoming values
- Convert input to normalized internal format

### Deliverables
- Stable user preference contract
- Input validation and error handling

---

## Phase 3: Retrieval and Candidate Generation

### Goal
Narrow down restaurants to a high-quality candidate set before sending context to the LLM.

### Core Components
- **Rule-Based Filter Engine**
- **Candidate Rank Pre-Processor** (basic sorting/scoring)
- **Context Builder** for prompt-ready structured output

### Key Tasks
- Filter by location, budget (rates between ₹200 to ₹5000), cuisine (including special cravings/features like Italian, Spicy, Japanese, and other varieties), and minimum rating (rating provided as 3-5 and the medium rating as 3.5 and 4.5)
- Add fallback strategies if strict filters return few results
- Select top candidate pool (for example top 10-20)
- Prepare concise candidate context for LLM input

### Deliverables
- Deterministic candidate generation module
- Prompt-ready candidate context object

---

## Phase 4: LLM Recommendation and Reasoning Engine

### Goal
Generate personalized, human-friendly recommendations with clear reasoning.

### Core Components
- **Prompt Template Engine**
- **LLM Inference Layer**
- **Recommendation Formatter**

### Prompt Responsibilities
- Provide user preferences
- Provide structured candidate restaurant list
- Ask model to rank restaurants
- Ask model to explain each recommendation briefly
- Enforce output format for consistency

### Key Tasks
- Create and test prompt templates
- Parse and validate LLM outputs
- Add safeguards for hallucinations (only recommend from candidate set)

### Deliverables
- Reliable LLM recommendation module
- Structured output with ranked results + explanations

---

## Phase 5: Response Presentation Layer

### Goal
Display recommendations in a simple, readable, and comparable format.

### Core Components
- **Result Renderer** (CLI table or UI cards)
- **Explanation Panel** (why each option was chosen)
- **Metadata Display** (rating, cuisine, estimated cost)

### Key Tasks
- Show top N recommendations
- Provide readable summaries per restaurant
- Include user-applied filters in the output for transparency

### Deliverables
- User-facing recommendation view
- Consistent response layout

---

## Phase 6: Quality, Evaluation, and Iteration

### Goal
Measure recommendation quality and improve model behavior over time.

### Core Components
- **Evaluation Framework**
- **Feedback Capture**
- **Prompt/Logic Tuning Loop**

### Suggested Metrics
- Filter accuracy (does output respect constraints?)
- Relevance score (manual or user feedback)
- Diversity of suggestions
- Response latency
- User satisfaction rating

### Key Tasks
- Create test cases across locations/cuisines/budgets
- Evaluate recommendation quality
- Tune filtering + prompt strategy

### Deliverables
- Evaluation report
- Improved recommendation quality across iterations

---

## Phase 7: Production Deployment with Render + Vercel

### Goal
Deploy the AI-powered restaurant recommendation system with separate backend and frontend deployments for optimal performance and scalability.

### Core Components
- **Next.js Frontend**: Modern React-based web interface with input forms and result display
- **FastAPI Backend**: Production-ready API service deployed on Render
- **CORS Configuration**: Secure cross-origin communication between services
- **Environment Management**: Separate environment variables for production deployments
- **Error Handling and User Feedback**: Graceful error display and loading states

### Key Features
- **User Input Form**: Location, budget range, cuisine preferences, minimum rating
- **Dynamic Filters**: Real-time filtering based on user selections
- **Results Display**: Enhanced card-based layout with gradient backgrounds and animations
- **Recommendation Explanations**: Show AI reasoning for each suggestion
- **Responsive Design**: Mobile-friendly interface with modern typography
- **Loading Indicators**: Progress bars and spinners during processing
- **Modern UI**: Premium design with Inter and Playfair Display fonts, gradient backgrounds

### Key Tasks
- Set up Next.js application structure with React components
- Create interactive input forms with modern UI/UX
- Integrate all backend phases (1-6) into Next.js workflow
- Implement React state management for user preferences
- Add error handling and user-friendly error messages
- Apply modern UI design with Tailwind CSS and Framer Motion animations
- Remove complex model tuning features (hardcode optimal model selection)
- Configure deployment settings for Render and Vercel

### Technical Implementation
- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS, Framer Motion
- **Backend**: FastAPI with Uvicorn server, deployed on Render
- **Caching**: Use React state and API response caching
- **File Structure**: Separate modules for each phase, imported into Next.js app
- **Environment Management**: Separate `.env` files for frontend and backend
- **Deployment**: Render for backend API, Vercel for frontend

### Deliverables
- Fully functional Next.js web application
- Deployed backend API on Render
- Deployed frontend on Vercel
- User documentation and usage instructions
- Configuration files for both deployment platforms

---

## End-to-End Data Flow

1. Load and clean restaurant dataset  
2. Capture and validate user preferences  
3. Filter and generate candidate restaurants  
4. Build prompt context and call LLM  
5. Rank and explain recommendations  
6. Display user-friendly results via Next.js frontend  
7. Deploy backend API on Render and frontend on Vercel  
8. Collect feedback and improve

---

## Recommended Tech Stack (Optional)

- **Backend Language**: Python
- **Frontend Language**: TypeScript/JavaScript
- **Data Handling**: `pandas`
- **Backend API**: `FastAPI` deployed on Render
- **Frontend UI**: `Next.js` deployed on Vercel
- **LLM Integration**: Google Generative AI (Gemini)
- **Styling**: Tailwind CSS + Framer Motion
- **Storage**: SQLite/JSON for milestone scope
- **Monitoring**: Basic logs + latency tracking
