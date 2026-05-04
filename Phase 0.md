# Phase 0 Implementation (Project Bootstrap)

Phase 0 establishes the minimum project foundation required before starting Phase 1 (data ingestion).
It also defines the product direction that a **basic web UI** will be the primary source of user input.

## What Was Implemented

- Basic Python project structure under `src/zomato_ai`
- Environment-driven configuration loader
- Standard logging setup
- Startup bootstrap flow that creates required directories
- Shared data models for future pipeline phases
- Entrypoint script (`main.py`) with a health check option
- Input strategy decision: preferences will be collected from a basic web UI (instead of CLI-first input)

## Input Source Decision (Phase 0)

- **Chosen input channel**: Basic web UI
- **Reason**: It provides a more user-friendly and demo-ready interface for capturing preferences such as location, budget, cuisine, and rating.
- **Impact on next phases**:
  - Phase 2 should implement a web form as the primary input interface.
  - API/backend logic should be designed to serve UI-driven requests cleanly.

## Files Added

- `requirements.txt`
- `.env.example`
- `main.py`
- `src/zomato_ai/__init__.py`
- `src/zomato_ai/config.py`
- `src/zomato_ai/logging_utils.py`
- `src/zomato_ai/models.py`
- `src/zomato_ai/bootstrap.py`

## Directories Auto-Created at Runtime

- `data/`
- `logs/`
- `artifacts/`

## How to Run

1. Install dependencies:
   - `pip install -r requirements.txt`
2. (Optional) Copy `.env.example` to `.env` and adjust values
3. Run health check:
   - `python main.py --health`

If successful, the command prints resolved config plus `status: ok`.

