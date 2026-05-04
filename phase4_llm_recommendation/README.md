# Phase 4: LLM Recommendation and Reasoning Engine

This folder contains a standalone implementation of **Phase 4** from `Phased architecture.md`.

## Scope Implemented

- Prompt template builder using:
  - user preferences from Phase 3 context
  - candidate restaurant list from Phase 3
- Google AI Studio inference integration (Gemini models)
- Structured JSON response parsing
- Hallucination safeguard:
  - recommendations are accepted only if they exist in the candidate set
  - invalid/empty model outputs trigger deterministic fallback
- Final formatter that saves ranked results with concise reasoning

## Input Dependency

This phase expects the Phase 3 candidate context JSON:

- `phase3_retrieval_candidates/output/candidate_context.json`

## Environment

Set your Google AI Studio key in `.env`:

- `GOOGLE_API_KEY=your_key_here`

## Run

```bash
python -m phase4_llm_recommendation.run_phase4 \
  --candidate-context phase3_retrieval_candidates/output/candidate_context.json \
  --model gemini-1.5-flash \
  --top-n 5
```

Optional flags:

- `--output-dir` to override output location

## Output

Generated file:

- `phase4_llm_recommendation/output/llm_recommendations.json`

