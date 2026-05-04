from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class UserPreferences:
    location: str
    budget: str
    cuisine: str
    min_rating: float
    additional_preferences: List[str] = field(default_factory=list)


@dataclass
class RestaurantRecord:
    name: str
    location: str
    cuisine: str
    cost: Optional[float]
    rating: Optional[float]

