# Phase 1: Data Ingestion and Preprocessing

This folder contains a standalone implementation of **Phase 1** from `Phased architecture.md`.

## Scope Implemented

- Load restaurant data from Hugging Face
- Handle split fallback if requested split is unavailable
- Normalize core fields:
  - `name`
  - `location`
  - `cuisine`
  - `cost`
  - `rating`
- Clean text and parse numeric values
- Remove invalid ratings/costs and duplicate rows
- Save both raw and processed datasets

## Run

```bash
python -m phase1_data_pipeline.run_phase1
```

Optional arguments:

```bash
python -m phase1_data_pipeline.run_phase1 \
  --dataset-id ManikaSaini/zomato-restaurant-recommendation \
  --split train \
  --output-dir phase1_data_pipeline/output \
  --log-level INFO
```

## Output

Generated in `phase1_data_pipeline/output`:

- `raw_zomato.csv`
- `processed_zomato.csv`

