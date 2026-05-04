from __future__ import annotations

from typing import Optional


def matches_budget(cost: Optional[float], budget: float) -> bool:
    if cost is None:
        return True
    return cost <= budget

