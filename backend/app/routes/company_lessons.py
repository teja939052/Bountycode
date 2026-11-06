"""
Company-prep lessons — simple step-based lessons for TCS NQT, Infosys, Wipro, etc.

Routes (all under /api/v1/company-lessons, auth required):
  GET  /api/v1/company-lessons               → list all available lessons
  GET  /api/v1/company-lessons/{slug}        → full lesson content
  POST /api/v1/company-lessons/{slug}/complete → record completion + rewards
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import os
import json
import logging

from app.middleware.auth import get_current_user
from app.services.gamification import record_practice
from app.services.learning_paths import complete_track_module

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/company-lessons", tags=["company-lessons"])

_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LESSONS_DIR = os.path.join(_APP_DIR, "data", "lessons")

# In-memory cache so we don't hit disk on every request.
_LESSON_CACHE: Dict[str, Dict[str, Any]] = {}


def _load_lesson(slug: str) -> Optional[Dict[str, Any]]:
    if slug in _LESSON_CACHE:
        return _LESSON_CACHE[slug]
    path = os.path.join(_LESSONS_DIR, f"{slug}.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        _LESSON_CACHE[slug] = data
        return data
    except Exception as exc:
        logger.warning("Failed to load lesson %s: %s", slug, exc)
        return None


class CompleteRequest(BaseModel):
    # The server grades these assessment choices against the authored answer
    # key. A browser-supplied score is never trusted for completion or XP.
    answers: Dict[str, int] = Field(default_factory=dict)
    time_spent_seconds: int = Field(default=0, ge=0)
    track_id: Optional[str] = None
    module_id: Optional[str] = None


@router.get("", response_model=None)
async def list_lessons(user=Depends(get_current_user)):
    """Return metadata for all available company-prep lessons."""
    lessons: List[Dict[str, Any]] = []
    if os.path.isdir(_LESSONS_DIR):
        for fname in sorted(os.listdir(_LESSONS_DIR)):
            if not fname.endswith(".json"):
                continue
            slug = fname[:-5]
            data = _load_lesson(slug)
            if not data or not data.get("steps") or not (data.get("assessment") or {}).get("questions"):
                # Legacy pattern snapshots without the step-based lesson schema
                # belong to the pattern curriculum, not this lesson player.
                continue
            lessons.append({
                "id": data.get("id") or slug,
                "slug": slug,
                "title": data.get("title") or slug,
                "domain": data.get("domain") or data.get("pattern") or "General",
                "difficulty": data.get("difficulty") or "medium",
                "duration_min": data.get("duration_min") or data.get("estimated_minutes") or 15,
                "step_count": len(data.get("steps") or []),
            })
    return {"success": True, "data": lessons}


@router.get("/{slug}", response_model=None)
async def get_lesson(slug: str, user=Depends(get_current_user)):
    data = _load_lesson(slug)
    if data is None or not data.get("steps") or not (data.get("assessment") or {}).get("questions"):
        raise HTTPException(status_code=404, detail=f"Step-based lesson not found: {slug}")

    # Do not send final-assessment answer keys to the browser. The server grades
    # them in /complete and only returns explanations after submission.
    public_data = {**data}
    assessment = {**(data.get("assessment") or {})}
    public_questions = []
    for question in assessment.get("questions", []):
        public_questions.append({
            key: value for key, value in question.items()
            if key not in {"correct_index", "correct_answer"}
        })
    assessment["questions"] = public_questions
    public_data["assessment"] = assessment
    return {"success": True, "data": public_data}


@router.post("/{slug}/complete", response_model=None)
async def complete_lesson(slug: str, req: CompleteRequest, user=Depends(get_current_user)):
    data = _load_lesson(slug)
    if data is None or not data.get("steps") or not (data.get("assessment") or {}).get("questions"):
        raise HTTPException(status_code=404, detail=f"Step-based lesson not found: {slug}")

    questions = (data.get("assessment") or {}).get("questions", [])
    if not questions:
        raise HTTPException(status_code=400, detail="This lesson has no final assessment.")
    if len(req.answers) != len(questions) or any(str(i) not in req.answers for i in range(len(questions))):
        raise HTTPException(status_code=422, detail="Answer every final-assessment question before submitting.")

    results = []
    correct = 0
    for index, question in enumerate(questions):
        try:
            selected = int(req.answers[str(index)])
        except (TypeError, ValueError):
            selected = -1
        expected = question.get("correct_index")
        is_correct = selected == expected
        correct += int(is_correct)
        results.append({
            "index": index,
            "correct": is_correct,
            "selected_index": selected,
            "correct_index": expected,
            "explanation": question.get("explanation", ""),
        })

    score = round((correct / len(questions)) * 100, 1)
    mastery_threshold = float(
        data.get("mastery_threshold")
        or (data.get("assessment") or {}).get("mastery_threshold")
        or 0.7
    )
    passed = score >= mastery_threshold * 100
    if not passed:
        return {
            "success": True,
            "data": {
                "passed": False,
                "score": score,
                "correct": correct,
                "total": len(questions),
                "results": results,
                "mastery_threshold": mastery_threshold * 100,
                "xp_earned": 0,
                "module_completed": False,
            },
        }

    if bool(req.track_id) != bool(req.module_id):
        raise HTTPException(status_code=400, detail="track_id and module_id must be supplied together.")

    if req.track_id and req.module_id:
        try:
            module_result = await complete_track_module(
                user_id=user["id"],
                track_id=req.track_id,
                module_id=req.module_id,
                score=score,
                role=user.get("role") or user.get("target_role") or "sde",
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        xp_earned = module_result.get("xp_earned", 0)
        module_completed = bool(module_result.get("passed") or module_result.get("already_completed"))
        reward = None
    else:
        reward = await record_practice(
            user_id=user["id"],
            activity_type="company_lesson",
            score=score / 10,
            metadata={
                "lesson_slug": slug,
                "lesson_title": data.get("title") or slug,
                "domain": data.get("domain") or data.get("pattern") or "General",
                "score_percent": score,
                "time_taken": req.time_spent_seconds,
                "passed": True,
            },
            role=user.get("role") or user.get("target_role") or "sde",
        )
        xp_earned = reward.get("xp_gained", 0) if isinstance(reward, dict) else 0
        module_completed = False
        module_result = None

    return {
        "success": True,
        "data": {
            "passed": True,
            "score": score,
            "correct": correct,
            "total": len(questions),
            "results": results,
            "mastery_threshold": mastery_threshold * 100,
            "xp_earned": xp_earned,
            "module_completed": module_completed,
            "module_result": module_result if req.track_id else None,
            "reward": reward,
        },
    }
