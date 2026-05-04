from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CandidateContext:
    user_preferences: Dict[str, Any]
    filter_strategy_used: str
    candidate_count: int
    candidates: List[Dict[str, Any]]


@dataclass
class RecommendationItem:
    rank: int
    name: str
    reason: str
    rating: Optional[float] = None
    cost: Optional[float] = None
    cuisine: str = ""
    location: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RecommendationResult:
    model: str
    recommendation_count: int
    recommendations: List[RecommendationItem] = field(default_factory=list)
    safety_notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "recommendation_count": self.recommendation_count,
            "recommendations": [item.to_dict() for item in self.recommendations],
            "safety_notes": self.safety_notes,
        }

