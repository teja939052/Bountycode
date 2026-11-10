"""Composite placement readiness score with explainable drivers."""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.database import get_collection

logger = logging.getLogger(__name__)

WEIGHTS = {
    "resume": 0.25,
    "aptitude": 0.30,
    "coding": 0.30,
    "interview": 0.15,
}


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


def _last_exam_scores(user_id: str) -> Dict[str, float]:
    try:
        col = get_collection("exam_attempts")
        attempts = list(col.find({"user_id": user_id, "completed_at": {"$exists": True}}))
    except Exception:
        attempts = []
    by_topic: Dict[str, List[float]] = {}
    for a in attempts:
        topic = a.get("topic") or "general"
        score = a.get("score")
        if score is not None:
            by_topic.setdefault(topic, []).append(float(score))
    return {t: round(sum(v) / len(v), 2) for t, v in by_topic.items() if v}


def _resume_score(user_id: str) -> float:
    try:
        col = get_collection("resume_analysis")
        row = col.find_one({"user_id": user_id}, sort=[("created_at", -1)])
        if row:
            return float(row.get("score") or row.get("ats_score") or 0)
    except Exception:
        pass
    return 0.0


def _interview_score(user_id: str) -> tuple[float, bool]:
    """Returns (score, has_data). has_data is False when there is no
    interview evaluation record at all (e.g. pending AI evaluation).
    A genuine score of 0 returns (0.0, True)."""
    try:
        col = get_collection("interview_history")
        row = col.find_one({"user_id": user_id}, sort=[("created_at", -1)])
        if row:
            score = float(row.get("score") or row.get("overall_score") or 0)
            return score, True
    except Exception:
        pass
    return 0.0, False


def compute_readiness(user_id: str) -> Dict[str, Any]:
    resume_score = _clamp(_resume_score(user_id))
    resume_has_data = resume_score > 0
    aptitude_scores = _last_exam_scores(user_id)
    aptitude_score = _clamp(sum(aptitude_scores.values()) / len(aptitude_scores)) if aptitude_scores else 0.0
    aptitude_has_data = len(aptitude_scores) > 0
    coding_score = aptitude_scores.get("coding", aptitude_score)
    coding_has_data = coding_score > 0
    interview_score, interview_has_data = _interview_score(user_id)

    # Weighted average over dimensions that actually have data.
    # Missing data (e.g. pending AI evaluation) is excluded rather than
    # treated as a zero score, so a pending interview does not drag the
    # readiness down to 0.
    weights = {
        "resume": WEIGHTS["resume"],
        "aptitude": WEIGHTS["aptitude"],
        "coding": WEIGHTS["coding"],
        "interview": WEIGHTS["interview"],
    }
    total_weight = 0.0
    weighted_sum = 0.0
    components = []

    if resume_has_data:
        total_weight += weights["resume"]
        weighted_sum += weights["resume"] * resume_score
        components.append({
            "component": "Resume", "score": round(resume_score, 2),
            "weight": weights["resume"],
            "contribution": round(WEIGHTS["resume"] * resume_score, 2),
        })

    if aptitude_has_data:
        total_weight += weights["aptitude"]
        weighted_sum += weights["aptitude"] * aptitude_score
        components.append({
            "component": "Aptitude", "score": round(aptitude_score, 2),
            "weight": weights["aptitude"],
            "contribution": round(WEIGHTS["aptitude"] * aptitude_score, 2),
        })

    if coding_has_data:
        total_weight += weights["coding"]
        weighted_sum += weights["coding"] * coding_score
        components.append({
            "component": "Coding", "score": round(coding_score, 2),
            "weight": weights["coding"],
            "contribution": round(WEIGHTS["coding"] * coding_score, 2),
        })

    if interview_has_data:
        total_weight += weights["interview"]
        weighted_sum += weights["interview"] * interview_score
        components.append({
            "component": "Interview", "score": round(interview_score, 2),
            "weight": weights["interview"],
            "contribution": round(WEIGHTS["interview"] * interview_score, 2),
        })

    readiness = round(weighted_sum / total_weight, 2) if total_weight > 0 else 0.0
    components.sort(key=lambda c: c["contribution"], reverse=True)
    drivers: List[str] = []
    weakest = min(components, key=lambda c: c["score"]) if components else None
    if weakest and weakest["score"] < 60:
        drivers.append("Strengthen " + weakest["component"] + " (score " + str(weakest["score"]) + ") — biggest readiness gap.")
    if resume_has_data and resume_score < 50:
        drivers.append("Resume below 50 — run ATS optimization before applying.")
    if aptitude_has_data and aptitude_score < 50:
        drivers.append("Aptitude below 50 — take timed topic tests and repair weak patterns.")
    if not drivers:
        drivers.append("All dimensions balanced — maintain with weekly timed mocks.")
    return {
        "user_id": user_id,
        "readiness_score": readiness,
        "tier": "ready" if readiness >= 75 else ("developing" if readiness >= 50 else "at_risk"),
        "components": components,
        "drivers": drivers,
        "aptitude_by_topic": aptitude_scores,
        "weights": WEIGHTS,
    }
