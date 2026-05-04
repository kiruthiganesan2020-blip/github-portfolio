# Phase 2: User Preference Collection (Web UI)

This folder contains a standalone implementation of **Phase 2** from `Phased architecture.md`.

## Scope Implemented

- Basic web UI (Streamlit) as primary input source
- Structured user preference schema
- Validation for required fields and rating range
- Normalization of submitted values
- Snapshot persistence of submitted preferences to JSON

## Run

1. Install dependencies:
   - `pip install -r requirements.txt`
2. Start the app:
   - `streamlit run phase2_user_input/app.py`

## Output

Submitted payload snapshots are saved in:

- `phase2_user_input/output/`

Each submission is stored as a timestamped JSON file.

