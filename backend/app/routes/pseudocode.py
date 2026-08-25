"""
Pseudocode Dry-Run drills — serve static bank questions without answers,
grade individual checks instantly, and log completed drills into practice
stats. Zero AI cost.
"""
import random
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.middleware.auth import get_current_user
from app.services.gamification import record_practice
from app.data.pseudocode_bank import get_pseudocode_questions

router = APIRouter(prefix="/api/v1/pseudocode", tags=["pseudocode"])

_bank = get_pseudocode_questions()
_by_id = {q["id"]: q for q in _bank}


@router.get("/meta")
async def drill_meta():
    """Topic breakdown for the picker UI."""
    topics: dict = {}
    for q in _bank:
        t = q["sub_category"]
        topics[t] = topics.get(t, 0) + 1
    return {"total": len(_bank), "topics": topics}


@router.get("/questions")
async def get_drill(
    count: int = 10,
    topic: Optional[str] = None,
    user=Depends(get_current_user),
):
    """Serve a random set of tracing questions WITHOUT answers."""
    pool = _bank
    if topic:
        pool = [q for q in _bank if q["sub_category"].lower() == topic.lower()]
        if not pool:
            raise HTTPException(status_code=404, detail=f"Unknown topic: {topic}")

    n = max(1, min(count, len(pool)))
    picked = random.sample(pool, n)
    return {
        "questions": [
            {
                "id": q["id"],
                "sub_category": q["sub_category"],
                "question": q["question"],
                "options": q["options"],
            }
            for q in picked
        ],
        "total_available": len(pool),
    }


class CheckInput(BaseModel):
    question_id: str
    answer: str


@router.post("/check")
async def check_answer(req: CheckInput, user=Depends(get_current_user)):
    """Instant grading with explanation — this is practice, not an exam."""
    q = _by_id.get(req.question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Unknown question")

    is_correct = (
        req.answer.strip().lower() == q["correct_answer"].strip().lower()
    )
    return {
        "is_correct": is_correct,
        "correct_answer": q["correct_answer"],
        "explanation": q["explanation"],
    }


class CompleteInput(BaseModel):
    correct: int
    total: int


@router.post("/complete")
async def complete_drill(req: CompleteInput, user=Depends(get_current_user)):
    """Log a finished drill; feeds streaks/XP via record_practice."""
    if req.total <= 0:
        raise HTTPException(status_code=400, detail="Invalid total")
    pct = round(max(0, min(req.correct, req.total)) / req.total * 100, 1)

    xp_gained = 0
    try:
        result = await record_practice(user["id"], "aptitude", pct)
        if isinstance(result, dict):
            xp_gained = result.get("xp_gained", 0)
    except Exception:
        pass

    return {
        "accuracy": pct,
        "xp_gained": xp_gained,
        "message": (
            f"Dry run logged: {pct}% accuracy."
            if pct >= 60
            else f"{pct}% — trace slower and re-run the weak topics."
        ),
    }
