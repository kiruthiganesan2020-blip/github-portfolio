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

## Phase 7: Streamlit Deployment and Production Interface

### Goal
Deploy the AI-powered restaurant recommendation system as an interactive web application using Streamlit for real-time user interaction.

### Core Components
- **Streamlit Web Interface**: Interactive UI with input forms and result display
- **Session State Management**: Handle user preferences and conversation history
- **Real-time Processing**: Connect backend logic to frontend interface
- **Configuration Management**: Environment variables and API key handling
- **Error Handling and User Feedback**: Graceful error display and loading states

### Key Features
- **User Input Form**: Location, budget range, cuisine preferences, minimum rating
- **Dynamic Filters**: Real-time filtering based on user selections
- **Results Display**: Card-based layout with restaurant details and recommendations
- **Recommendation Explanations**: Show AI reasoning for each suggestion
- **Responsive Design**: Mobile-friendly interface
- **Loading Indicators**: Progress bars and spinners during processing

### Key Tasks
- Set up Streamlit application structure
- Create interactive input widgets (dropdowns, sliders, text inputs)
- Integrate all backend phases (1-6) into Streamlit workflow
- Implement session state for maintaining user context
- Add error handling and user-friendly error messages
- Style the interface for better user experience
- Configure deployment settings and environment variables

### Technical Implementation
- **Streamlit Components**: `st.sidebar()` for filters, `st.columns()` for layout
- **Caching**: Use `@st.cache_data` for dataset loading and `@st.cache_resource` for LLM client
- **File Structure**: Separate modules for each phase, imported into main app
- **Environment Management**: `.env` file for API keys and configuration
- **Deployment**: Streamlit Cloud or self-hosted option

### Deliverables
- Fully functional Streamlit web application
- Deployed application accessible via URL
- User documentation and usage instructions
- Configuration files for deployment

---

## End-to-End Data Flow

1. Load and clean restaurant dataset  
2. Capture and validate user preferences  
3. Filter and generate candidate restaurants  
4. Build prompt context and call LLM  
5. Rank and explain recommendations  
6. Display user-friendly results  
7. Deploy interactive Streamlit web interface  
8. Collect feedback and improve

---

## Recommended Tech Stack (Optional)

- **Language**: Python
- **Data Handling**: `pandas`
- **API/UI**: `FastAPI` + Streamlit/React (optional)
- **LLM Integration**: OpenAI-compatible client
- **Storage**: SQLite/JSON for milestone scope
- **Monitoring**: Basic logs + latency tracking
