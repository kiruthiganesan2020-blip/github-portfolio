from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd

from phase3_retrieval_candidates.budgeting import matches_budget
from phase3_retrieval_candidates.schema import CandidateRecord, PreferenceInput


def _normalize_text(value: object) -> str:
    return " ".join(str(value or "").strip().lower().split())


def load_processed_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Processed dataset not found: {path}")
    return pd.read_csv(path)


def _cuisine_match(row_cuisine: str, target_cuisine: str) -> bool:
    return target_cuisine in row_cuisine


def _location_match(row_location: str, target_location: str) -> bool:
    return target_location in row_location


def apply_strict_filters(df: pd.DataFrame, pref: PreferenceInput) -> pd.DataFrame:
    target_location = _normalize_text(pref.location)
    target_cuisine = _normalize_text(pref.cuisine)

    work = df.copy()
    work["location_norm"] = work["location"].map(_normalize_text)
    work["cuisine_norm"] = work["cuisine"].map(_normalize_text)

    strict = work[
        work["location_norm"].map(lambda v: _location_match(v, target_location))
        & work["cuisine_norm"].map(lambda v: _cuisine_match(v, target_cuisine))
        & work["cost"].map(lambda c: matches_budget(c, pref.budget))
        & (
            work["rating"].isna()
            | (work["rating"].astype(float) >= float(pref.min_rating))
        )
    ]
    return strict.drop(columns=["location_norm", "cuisine_norm"])


def apply_relaxed_filters(df: pd.DataFrame, pref: PreferenceInput) -> Tuple[pd.DataFrame, str]:
    """
    Relax constraints progressively when strict filtering yields no candidates:
    1) keep location + cuisine + budget, remove min_rating
    2) keep location + cuisine, remove budget and min_rating
    3) keep location only
    """
    target_location = _normalize_text(pref.location)
    target_cuisine = _normalize_text(pref.cuisine)

    work = df.copy()
    work["location_norm"] = work["location"].map(_normalize_text)
    work["cuisine_norm"] = work["cuisine"].map(_normalize_text)

    step1 = work[
        work["location_norm"].map(lambda v: _location_match(v, target_location))
        & work["cuisine_norm"].map(lambda v: _cuisine_match(v, target_cuisine))
        & work["cost"].map(lambda c: matches_budget(c, pref.budget))
    ]
    if not step1.empty:
        return step1.drop(columns=["location_norm", "cuisine_norm"]), "relaxed:min_rating"

    step2 = work[
        work["location_norm"].map(lambda v: _location_match(v, target_location))
        & work["cuisine_norm"].map(lambda v: _cuisine_match(v, target_cuisine))
    ]
    if not step2.empty:
        return step2.drop(columns=["location_norm", "cuisine_norm"]), "relaxed:min_rating+budget"

    step3 = work[work["location_norm"].map(lambda v: _location_match(v, target_location))]
    return step3.drop(columns=["location_norm", "cuisine_norm"]), "relaxed:location_only"


def score_candidates(df: pd.DataFrame, pref: PreferenceInput) -> List[CandidateRecord]:
    target_location = _normalize_text(pref.location)
    target_cuisine = _normalize_text(pref.cuisine)
    scored: List[CandidateRecord] = []

    for _, row in df.iterrows():
        notes: List[str] = []
        score = 0.0

        location_norm = _normalize_text(row.get("location"))
        cuisine_norm = _normalize_text(row.get("cuisine"))
        rating = row.get("rating")
        cost = row.get("cost")

        if target_location in location_norm:
            score += 0.35
            notes.append("location_match")
        if target_cuisine in cuisine_norm:
            score += 0.35
            notes.append("cuisine_match")
        if matches_budget(cost, pref.budget):
            score += 0.15
            notes.append("budget_match")
        if pd.notna(rating):
            rating_value = float(rating)
            score += min(max(rating_value / 5.0, 0.0), 1.0) * 0.15
            if rating_value >= pref.min_rating:
                notes.append("rating_match")

        scored.append(
            CandidateRecord(
                name=str(row.get("name", "")),
                location=str(row.get("location", "")),
                cuisine=str(row.get("cuisine", "")),
                cost=float(cost) if pd.notna(cost) else None,
                rating=float(rating) if pd.notna(rating) else None,
                score=round(score, 4),
                match_notes=notes,
            )
        )

    scored.sort(
        key=lambda c: (
            c.score,
            c.rating if c.rating is not None else -1.0,
            -(c.cost if c.cost is not None else 10**9),
            c.name.lower(),
        ),
        reverse=True,
    )
    return scored


def build_prompt_context(
    pref: PreferenceInput,
    candidates: List[CandidateRecord],
    filter_strategy: str,
    top_k: int,
) -> Dict[str, object]:
    top_candidates = candidates[:top_k]
    return {
        "user_preferences": asdict(pref),
        "filter_strategy_used": filter_strategy,
        "candidate_count": len(top_candidates),
        "candidates": [c.to_dict() for c in top_candidates],
    }


def run_phase3(
    processed_csv_path: Path,
    pref: PreferenceInput,
    output_dir: Path,
    top_k: int = 15,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    df = load_processed_data(processed_csv_path)

    strict = apply_strict_filters(df, pref)
    if strict.empty:
        filtered, strategy = apply_relaxed_filters(df, pref)
    else:
        filtered, strategy = strict, "strict"

    candidates = score_candidates(filtered, pref)
    context = build_prompt_context(pref, candidates, strategy, top_k)

    output_path = output_dir / "candidate_context.json"
    output_path.write_text(json.dumps(context, indent=2), encoding="utf-8")
    return output_path

