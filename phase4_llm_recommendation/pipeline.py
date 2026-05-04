from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

import google.generativeai as genai
from dotenv import load_dotenv

from phase4_llm_recommendation.prompting import build_recommendation_prompt
from phase4_llm_recommendation.schema import (
    CandidateContext,
    RecommendationItem,
    RecommendationResult,
)


def _normalize_name(name: str) -> str:
    return " ".join(str(name or "").strip().lower().split())


def load_candidate_context(path: Path) -> CandidateContext:
    if not path.exists():
        raise FileNotFoundError(f"Candidate context file not found: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    return CandidateContext(
        user_preferences=payload.get("user_preferences", {}),
        filter_strategy_used=str(payload.get("filter_strategy_used", "")),
        candidate_count=int(payload.get("candidate_count", 0)),
        candidates=payload.get("candidates", []),
    )


def _extract_json_object(text: str) -> Dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("Model response did not contain a valid JSON object.")
        return json.loads(cleaned[start : end + 1])


def _fallback_recommendations(
    candidates: List[Dict[str, Any]], top_n: int
) -> List[RecommendationItem]:
    items: List[RecommendationItem] = []
    for index, candidate in enumerate(candidates[:top_n], start=1):
        items.append(
            RecommendationItem(
                rank=index,
                name=str(candidate.get("name", "")),
                reason="Selected from deterministic candidate ranking as fallback.",
                rating=float(candidate["rating"]) if candidate.get("rating") is not None else None,
                cost=float(candidate["cost"]) if candidate.get("cost") is not None else None,
                cuisine=str(candidate.get("cuisine", "")),
                location=str(candidate.get("location", "")),
            )
        )
    return items


def _validate_and_enrich_recommendations(
    raw_recommendations: List[Dict[str, Any]],
    candidates: List[Dict[str, Any]],
    top_n: int,
) -> List[RecommendationItem]:
    by_name: Dict[str, Dict[str, Any]] = {
        _normalize_name(c.get("name", "")): c for c in candidates if c.get("name")
    }
    validated: List[RecommendationItem] = []
    seen = set()

    for rec in raw_recommendations:
        candidate_name = _normalize_name(rec.get("name", ""))
        if not candidate_name or candidate_name in seen or candidate_name not in by_name:
            continue
        source = by_name[candidate_name]
        reason = str(rec.get("reason", "")).strip()
        validated.append(
            RecommendationItem(
                rank=len(validated) + 1,
                name=str(source.get("name", "")),
                reason=reason if reason else "Good match based on requested preferences.",
                rating=float(source["rating"]) if source.get("rating") is not None else None,
                cost=float(source["cost"]) if source.get("cost") is not None else None,
                cuisine=str(source.get("cuisine", "")),
                location=str(source.get("location", "")),
            )
        )
        seen.add(candidate_name)
        if len(validated) >= min(top_n, len(candidates)):
            break
    return validated


def _call_google_ai_studio(prompt: str, model_name: str) -> str:
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY is missing. Add it to your .env file for Google AI Studio access."
        )

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name=model_name)
    response = model.generate_content(prompt)
    text = getattr(response, "text", "") or ""
    if not text.strip():
        raise ValueError("Google AI Studio returned an empty response.")
    return text


def run_phase4(
    candidate_context_path: Path,
    output_dir: Path,
    model_name: str = "gemini-1.5-flash",
    top_n: int = 5,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    context = load_candidate_context(candidate_context_path)

    prompt = build_recommendation_prompt(
        user_preferences=context.user_preferences,
        candidates=context.candidates,
        top_n=top_n,
    )

    safety_notes: List[str] = []
    recommendations: List[RecommendationItem]

    try:
        raw_text = _call_google_ai_studio(prompt, model_name=model_name)
        parsed = _extract_json_object(raw_text)
        raw_recommendations = parsed.get("recommendations", [])
        if not isinstance(raw_recommendations, list):
            raise ValueError("`recommendations` must be a list in model output.")
        recommendations = _validate_and_enrich_recommendations(
            raw_recommendations=raw_recommendations,
            candidates=context.candidates,
            top_n=top_n,
        )
    except Exception as exc:
        safety_notes.append(
            f"LLM call/parse failed; used deterministic fallback. reason={type(exc).__name__}"
        )
        recommendations = []

    if not recommendations:
        safety_notes.append("No valid LLM recommendations after validation; used fallback ranking.")
        recommendations = _fallback_recommendations(context.candidates, top_n=top_n)

    result = RecommendationResult(
        model=model_name,
        recommendation_count=len(recommendations),
        recommendations=recommendations,
        safety_notes=safety_notes,
    )

    output_payload = {
        "user_preferences": context.user_preferences,
        "filter_strategy_used": context.filter_strategy_used,
        "candidate_count": context.candidate_count,
        "phase4_result": result.to_dict(),
    }

    output_path = output_dir / "llm_recommendations.json"
    output_path.write_text(json.dumps(output_payload, indent=2), encoding="utf-8")
    return output_path

