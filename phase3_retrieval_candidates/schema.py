from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PreferenceInput:
    location: str
    budget: float
    cuisine: str
    min_rating: float
    additional_preferences: List[str] = field(default_factory=list)


@dataclass
class CandidateRecord:
    name: str
    location: str
    cuisine: str
    cost: Optional[float]
    rating: Optional[float]
    score: float
    match_notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

