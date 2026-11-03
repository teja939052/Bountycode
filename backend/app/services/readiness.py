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


def _interview_score(user_id: str) -> float:
    try:
        col = get_collection("interview_history")
        row = col.find_one({"user_id": user_id}, sort=[("created_at", -1)])
        if row:
            return float(row.get("score") or row.get("overall_score") or 0)
    except Exception:
        pass
    return 0.0


def compute_readiness(user_id: str) -> Dict[str, Any]:
    resume_score = _clamp(_resume_score(user_id))
    aptitude_scores = _last_exam_scores(user_id)
    aptitude_score = _clamp(sum(aptitude_scores.values()) / len(aptitude_scores)) if aptitude_scores else 0.0
    coding_score = aptitude_scores.get("coding", aptitude_score)
    interview_score = _clamp(_interview_score(user_id))
    readiness = round(
        WEIGHTS["resume"] * resume_score
        + WEIGHTS["aptitude"] * aptitude_score
        + WEIGHTS["coding"] * coding_score
        + WEIGHTS["interview"] * interview_score,
        2,
    )
    components = [
        {"component": "Resume", "score": round(resume_score, 2), "weight": WEIGHTS["resume"],
         "contribution": round(WEIGHTS["resume"] * resume_score, 2)},
        {"component": "Aptitude", "score": round(aptitude_score, 2), "weight": WEIGHTS["aptitude"],
         "contribution": round(WEIGHTS["aptitude"] * aptitude_score, 2)},
        {"component": "Coding", "score": round(coding_score, 2), "weight": WEIGHTS["coding"],
         "contribution": round(WEIGHTS["coding"] * coding_score, 2)},
        {"component": "Interview", "score": round(interview_score, 2), "weight": WEIGHTS["interview"],
         "contribution": round(WEIGHTS["interview"] * interview_score, 2)},
    ]
    components.sort(key=lambda c: c["contribution"], reverse=True)
    drivers: List[str] = []
    weakest = min(components, key=lambda c: c["score"])
    if weakest["score"] < 60:
        drivers.append("Strengthen " + weakest["component"] + " (score " + str(weakest["score"]) + ") — biggest readiness gap.")
    if resume_score < 50:
        drivers.append("Resume below 50 — run ATS optimization before applying.")
    if aptitude_score < 50:
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
