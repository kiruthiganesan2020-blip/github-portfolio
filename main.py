from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from src.zomato_ai.bootstrap import bootstrap


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Zomato AI project entrypoint.")
    parser.add_argument(
        "--health",
        action="store_true",
        help="Run a Phase 0 readiness check and print config.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = bootstrap()

    if args.health:
        print(json.dumps(asdict(config), default=str, indent=2))
        print("status: ok")
        return

    print(
        "Phase 0 completed. Project scaffold is ready. "
        "Next: implement Phase 1 data ingestion."
    )


if __name__ == "__main__":
    main()

