import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.services.scoring import score_question

logger = logging.getLogger(__name__)
ALPHA = 0.4


def weakness_tier(mastery: float) -> str:
    if mastery < 0.40:
        return "critical"
    if mastery < 0.60:
        return "weak"
    if mastery < 0.85:
        return "on_track"
    return "strong"


def compute_ema(previous: Optional[float], exam_score: float, alpha: float = ALPHA) -> float:
    return round(alpha * exam_score + (1 - alpha) * previous, 6)


def first_mastery(exam_score: float) -> float:
    return round(exam_score, 6)


def diagnose_pattern(
    pattern: str,
    questions: List[dict],
    answers: Dict[str, Any],
    previous_mastery: Optional[float],
    exam_id: str,
    activity_id: Optional[str] = None,
) -> Dict[str, Any]:
    total = 0
    correct = 0
    for q in questions:
        if (q.get("topic") or q.get("pattern")) != pattern:
            continue
        total += 1
        ua = answers.get(q.get("id"))
        sr = score_question(q, ua)
        if sr["is_correct"]:
            correct += 1
    if total == 0:
        return {"pattern": pattern, "skipped": True}
    exam_score = correct / total
    if previous_mastery is None:
        new_mastery = first_mastery(exam_score)
    else:
        new_mastery = compute_ema(previous_mastery, exam_score)
    return {
        "pattern": pattern,
        "previous_mastery": previous_mastery,
        "exam_score": round(exam_score, 6),
        "new_mastery": new_mastery,
        "alpha": ALPHA,
        "questions_seen": total,
        "questions_correct": correct,
        "exam_id": exam_id,
        "activity_id": activity_id,
        "assessed_at": datetime.now(timezone.utc).isoformat(),
        "weakness_tier": weakness_tier(new_mastery),
    }


def diagnose_exam(
    questions: List[dict],
    answers: Dict[str, Any],
    previous_masteries: Dict[str, Optional[float]],
    exam_id: str,
    activity_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    patterns = set((q.get("topic") or q.get("pattern")) for q in questions if (q.get("topic") or q.get("pattern")))
    out = []
    for p in patterns:
        pm = previous_masteries.get(p)
        d = diagnose_pattern(p, questions, answers, pm, exam_id, activity_id)
        if not d.get("skipped"):
            out.append(d)
    return out
