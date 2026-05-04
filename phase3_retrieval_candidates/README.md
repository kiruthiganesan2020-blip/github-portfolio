# Phase 3: Retrieval and Candidate Generation

This folder contains a standalone implementation of **Phase 3** from `Phased architecture.md`.

## Scope Implemented

- Deterministic rule-based filtering using:
  - location
  - cuisine
  - budget
  - minimum rating
- Progressive fallback strategy if strict filters return no rows:
  - relax minimum rating
  - relax minimum rating + budget
  - location-only fallback
- Candidate pre-ranking with deterministic scoring
- Prompt-ready context builder for downstream LLM phase

## Input Dependency

This phase expects the Phase 1 processed dataset:

- `phase1_data_pipeline/output/processed_zomato.csv`

## Run

```bash
python -m phase3_retrieval_candidates.run_phase3 \
  --location Bangalore \
  --budget medium \
  --cuisine Italian \
  --min-rating 4.0
```

Optional flags:

- `--processed-csv` to override input file path
- `--top-k` to cap output candidate pool
- `--additional-preferences` for context completeness
- `--output-dir` to override output location

## Output

Generated file:

- `phase3_retrieval_candidates/output/candidate_context.json`

This JSON is prompt-ready and can be directly consumed in Phase 4 (LLM recommendation engine).

