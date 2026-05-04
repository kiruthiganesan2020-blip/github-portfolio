from __future__ import annotations

import json
from typing import Any, Dict, List


def _compact_candidate(candidate: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": candidate.get("name"),
        "location": candidate.get("location"),
        "cuisine": candidate.get("cuisine"),
        "cost": candidate.get("cost"),
        "rating": candidate.get("rating"),
        "score": candidate.get("score"),
        "match_notes": candidate.get("match_notes", []),
    }


def build_recommendation_prompt(
    user_preferences: Dict[str, Any],
    candidates: List[Dict[str, Any]],
    top_n: int,
) -> str:
    compact_candidates = [_compact_candidate(c) for c in candidates]
    candidates_json = json.dumps(compact_candidates, indent=2, ensure_ascii=True)
    prefs_json = json.dumps(user_preferences, indent=2, ensure_ascii=True)

    return f"""
You are a restaurant recommendation assistant.
Your output must be valid JSON and nothing else.

Rules you must follow:
1. Only recommend restaurants from the provided candidate list.
2. Return exactly {top_n} items when enough candidates exist; otherwise return all candidates.
3. Keep reasons concise and specific to user preferences.
4. Do not invent missing values.

User preferences JSON:
{prefs_json}

Candidate restaurants JSON:
{candidates_json}

Return JSON in this exact shape:
{{
  "recommendations": [
    {{
      "rank": 1,
      "name": "Restaurant Name",
      "reason": "Short explanation for why this matches",
      "rating": 4.2,
      "cost": 1200.0,
      "cuisine": "Italian",
      "location": "Bangalore"
    }}
  ]
}}
""".strip()

