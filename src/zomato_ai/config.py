from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class AppConfig:
    dataset_url: str
    data_dir: Path
    raw_data_file: str
    processed_data_file: str
    log_level: str

    @property
    def raw_data_path(self) -> Path:
        return self.data_dir / self.raw_data_file

    @property
    def processed_data_path(self) -> Path:
        return self.data_dir / self.processed_data_file


def load_config() -> AppConfig:
    """Load app configuration from environment variables."""
    load_dotenv()

    data_dir = Path(os.getenv("DATA_DIR", "data")).resolve()
    data_dir.mkdir(parents=True, exist_ok=True)

    return AppConfig(
        dataset_url=os.getenv(
            "DATASET_URL",
            "https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation",
        ),
        data_dir=data_dir,
        raw_data_file=os.getenv("RAW_DATA_FILE", "raw_zomato.csv"),
        processed_data_file=os.getenv("PROCESSED_DATA_FILE", "processed_zomato.csv"),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )

