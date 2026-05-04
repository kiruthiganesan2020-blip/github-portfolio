from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List





@dataclass
class UserPreferenceRequest:
    location: str
    budget: float
    cuisine: str
    min_rating: float
    additional_preferences: List[str] = field(default_factory=list)

    def normalize(self) -> "UserPreferenceRequest":
        self.location = " ".join(self.location.strip().split())

        self.cuisine = " ".join(self.cuisine.strip().split())
        self.additional_preferences = [
            " ".join(p.strip().split())
            for p in self.additional_preferences
            if p and p.strip()
        ]
        return self

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

