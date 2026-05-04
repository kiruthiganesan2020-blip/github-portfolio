from __future__ import annotations

from typing import List, Tuple

from phase2_user_input.schema import UserPreferenceRequest


def parse_additional_preferences(raw_text: str) -> List[str]:
    if not raw_text.strip():
        return []
    return [item.strip() for item in raw_text.split(",") if item.strip()]


def validate_preferences(payload: UserPreferenceRequest) -> Tuple[bool, List[str]]:
    errors: List[str] = []

    if not payload.location.strip():
        errors.append("Location is required.")

    if payload.budget < 200 or payload.budget > 5000:
        errors.append("Budget must be between 200 and 5000.")

    if not payload.cuisine.strip():
        errors.append("Cuisine is required.")

    if payload.min_rating < 0 or payload.min_rating > 5:
        errors.append("Minimum rating must be between 0 and 5.")

    return (len(errors) == 0, errors)

