from __future__ import annotations

import argparse
from pathlib import Path

from phase3_retrieval_candidates.pipeline import run_phase3
from phase3_retrieval_candidates.schema import PreferenceInput


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Phase 3: retrieval and candidate generation."
    )
    parser.add_argument(
        "--processed-csv",
        default="phase1_data_pipeline/output/processed_zomato.csv",
        help="Path to Phase 1 processed CSV.",
    )
    parser.add_argument("--location", required=True, help="Preferred location/city.")
    parser.add_argument("--budget", required=True, help="Budget: low | medium | high.")
    parser.add_argument("--cuisine", required=True, help="Preferred cuisine.")
    parser.add_argument(
        "--min-rating",
        type=float,
        default=3.5,
        help="Minimum acceptable rating (0-5).",
    )
    parser.add_argument(
        "--additional-preferences",
        default="",
        help="Comma separated extra preferences.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=15,
        help="Maximum candidates to keep in prompt context.",
    )
    parser.add_argument(
        "--output-dir",
        default="phase3_retrieval_candidates/output",
        help="Output folder for candidate context JSON.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    additional = [x.strip() for x in args.additional_preferences.split(",") if x.strip()]
    pref = PreferenceInput(
        location=args.location,
        budget=args.budget,
        cuisine=args.cuisine,
        min_rating=args.min_rating,
        additional_preferences=additional,
    )
    output_path = run_phase3(
        processed_csv_path=Path(args.processed_csv).resolve(),
        pref=pref,
        output_dir=Path(args.output_dir).resolve(),
        top_k=args.top_k,
    )
    print(f"Phase 3 completed. Candidate context saved at: {output_path}")


if __name__ == "__main__":
    main()

