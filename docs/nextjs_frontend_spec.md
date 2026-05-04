# Next.js Frontend Specification: Zomato AI

This document provides the requirements for building a modern, high-performance frontend for Zomato AI using Next.js (App Router), Tailwind CSS, and Framer Motion.

## 1. Backend Integration
The frontend must interact with the following FastAPI endpoint:
- **URL**: `http://localhost:8000/recommend`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "location": "string",
    "budget": "low | medium | high",
    "cuisine": "string",
    "min_rating": 4.0,
    "additional_preferences": ["string"],
    "model_name": "string",
    "top_n": 5
  }
  ```
- **Response Shape**:
  ```json
  {
    "user_preferences": {...},
    "strategy": "strict | relaxed",
    "recommendations": [
      {
        "rank": 1,
        "name": "string",
        "reason": "string",
        "rating": 4.5,
        "cost": 1500,
        "cuisine": "string",
        "location": "string"
      }
    ]
  }
  ```

## 2. Key Components to Implement

### A. Search/Preferences Form
- **Location Input**: Auto-suggesting or free text.
- **Budget Selection**: 3-stage toggle (Low, Mid, High).
- **Cuisine Input**: Pill-based input or dropdown.
- **Min Rating**: Stylish slider (0.0 to 5.0).
- **Additional Preferences**: Multi-select tags.

### B. Recommendation Results (The Cards)
- **Visuals**: Premium glassmorphism effect.
- **Rating Badge**: Highlighted with a star icon (green for high ratings).
- **Reasoning**: A "Why this?" section with a distinct italic font.
- **Metadata**: Clear icons for location (📍), cuisine (🍲), and cost (💰).

### C. Feedback Loop
- **Interactions**: Upvote/Downvote buttons on each card.
- **Toast Notifications**: Confirmation message when feedback is submitted.

## 3. Design Aesthetics
- **Color Palette**: Zomato Red (`#cb202d`), Dark Gray (`#1c1c1c`), and clean White.
- **Typography**: Inter or Roboto for a modern feel.
- **Animations**: 
  - Cards should fade in and slide up when results load.
  - Hover effects on cards (subtle scale up).

## 4. Technical Requirements
- **Next.js 14+** with App Router.
- **Tailwind CSS** for styling.
- **Lucide React** for icons.
- **Framer Motion** for micro-interactions.
- **Axios/Fetch** for API calls.
