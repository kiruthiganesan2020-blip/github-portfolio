from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Optional

import pandas as pd
from datasets import load_dataset

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Phase1Config:
    dataset_id: str
    split: str
    output_dir: Path
    raw_file: str = "raw_zomato.csv"
    processed_file: str = "processed_zomato.csv"

    @property
    def raw_path(self) -> Path:
        return self.output_dir / self.raw_file

    @property
    def processed_path(self) -> Path:
        return self.output_dir / self.processed_file


CANONICAL_ALIASES: Dict[str, Iterable[str]] = {
    "name": (
        "name",
        "restaurant_name",
        "res_name",
        "restaurant",
        "restaurant title",
    ),
    "location": ("location", "city", "locality", "address"),
    "cuisine": ("cuisine", "cuisines", "food_type", "food type"),
    "cost": (
        "cost",
        "average_cost_for_two",
        "average cost for two",
        "price",
        "approx_cost(for two people)",
        "approx cost(for two people)",
    ),
    "rating": ("rating", "aggregate_rating", "aggregate rating", "user_rating"),
}


def _normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def _resolve_column(columns: Iterable[str], aliases: Iterable[str]) -> Optional[str]:
    normalized = {_normalize_key(c): c for c in columns}
    for alias in aliases:
        candidate = normalized.get(_normalize_key(alias))
        if candidate:
            return candidate
    return None


def _to_float(value: object) -> Optional[float]:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    match = re.search(r"-?\d+(\.\d+)?", text.replace(",", ""))
    if not match:
        return None
    try:
        return float(match.group(0))
    except ValueError:
        return None


def _clean_text(value: object) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def load_hf_dataset_as_dataframe(dataset_id: str, split: str) -> pd.DataFrame:
    """
    Load a Hugging Face dataset split into a pandas DataFrame.
    Falls back to the first available split when requested split is unavailable.
    """
    try:
        ds_split = load_dataset(dataset_id, split=split)
    except Exception:
        logger.warning("Split '%s' unavailable; trying auto split resolution.", split)
        dataset_dict = load_dataset(dataset_id)
        first_split = next(iter(dataset_dict.keys()))
        logger.info("Using fallback split '%s'.", first_split)
        ds_split = dataset_dict[first_split]

    return ds_split.to_pandas()


def preprocess_restaurant_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Normalize core schema and clean key fields for downstream use."""
    if raw_df.empty:
        raise ValueError("Raw dataset is empty.")

    selected = {}
    for canonical, aliases in CANONICAL_ALIASES.items():
        source_col = _resolve_column(raw_df.columns, aliases)
        if source_col:
            selected[canonical] = raw_df[source_col]
        else:
            logger.warning("Could not resolve source column for '%s'.", canonical)
            selected[canonical] = None

    df = pd.DataFrame(selected)

    # Text cleanup
    for col in ("name", "location", "cuisine"):
        df[col] = df[col].map(_clean_text)

    # Numeric parsing
    df["cost"] = df["cost"].map(_to_float)
    df["rating"] = df["rating"].map(_to_float)

    # Remove impossible values
    df.loc[(df["rating"].notna()) & ((df["rating"] < 0) | (df["rating"] > 5)), "rating"] = None
    df.loc[(df["cost"].notna()) & (df["cost"] < 0), "cost"] = None

    # Basic validity constraints
    df = df[df["name"] != ""]
    df = df[df["location"] != ""]
    df = df.drop_duplicates(subset=["name", "location"], keep="first")
    df = df.reset_index(drop=True)

    return df


def run_phase1(config: Phase1Config) -> None:
    """Execute ingestion and preprocessing, then persist outputs."""
    config.output_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Loading dataset: %s", config.dataset_id)
    raw_df = load_hf_dataset_as_dataframe(config.dataset_id, config.split)

    raw_df.to_csv(config.raw_path, index=False)
    logger.info("Saved raw data to %s (%d rows).", config.raw_path, len(raw_df))

    processed_df = preprocess_restaurant_data(raw_df)
    processed_df.to_csv(config.processed_path, index=False)
    logger.info(
        "Saved processed data to %s (%d rows).",
        config.processed_path,
        len(processed_df),
    )

