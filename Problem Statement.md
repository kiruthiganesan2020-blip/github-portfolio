# Problem Statement: AI-Powered Restaurant Recommendation System (Zomato Use Case)

Build an AI-powered restaurant recommendation system inspired by Zomato.  
The goal is to deliver personalized restaurant suggestions by combining structured restaurant data with a Large Language Model (LLM).

## Objective

Design and implement an application that can:

- Accept user preferences such as location, budget, cuisine, and minimum rating
- Use a real-world restaurant dataset
- Leverage an LLM to generate personalized, natural-language recommendations
- Present clear, useful, and easy-to-compare results

## System Workflow

### 1) Data Ingestion

- Load and preprocess the Zomato dataset from Hugging Face:  
  [https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation)
- Extract relevant fields such as:
  - Restaurant name
  - Location
  - Cuisine
  - Estimated cost
  - Rating

### 2) User Input Collection

Capture user preferences including:

- Location (for example: Delhi, Bangalore)
- Budget range (low, medium, high)
- Preferred cuisine (for example: Italian, Chinese)
- Minimum acceptable rating
- Additional preferences (for example: family-friendly, quick service)

### 3) Integration and Prompting Layer

- Filter and prepare restaurant records based on user input
- Convert filtered results into structured context for the LLM
- Create a prompt that enables the LLM to reason, compare, and rank options

### 4) Recommendation Engine

Use the LLM to:

- Rank the best-matching restaurants
- Explain why each option fits the user’s preferences
- Optionally provide a short summary of top choices

### 5) Output Presentation

Display top recommendations in a user-friendly format, including:

- Restaurant name
- Cuisine
- Rating
- Estimated cost
- AI-generated explanation
