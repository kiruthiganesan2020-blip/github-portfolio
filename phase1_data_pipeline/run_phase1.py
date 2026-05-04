from __future__ import annotations

import argparse
import logging
from pathlib import Path

from phase1_data_pipeline.pipeline import Phase1Config, run_phase1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Phase 1: Zomato data ingestion and preprocessing."
    )
    parser.add_argument(
        "--dataset-id",
        default="ManikaSaini/zomato-restaurant-recommendation",
        help="Hugging Face dataset ID.",
    )
    parser.add_argument(
        "--split",
        default="train",
        help="Dataset split to load (falls back automatically if missing).",
    )
    parser.add_argument(
        "--output-dir",
        default="phase1_data_pipeline/output",
        help="Directory to store raw and processed files.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Application log level.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(
        level=args.log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    config = Phase1Config(
        dataset_id=args.dataset_id,
        split=args.split,
        output_dir=Path(args.output_dir).resolve(),
    )
    run_phase1(config)


if __name__ == "__main__":
    main()

