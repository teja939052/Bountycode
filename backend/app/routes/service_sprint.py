"""Service-company sprint API — curriculum spine + progressive hints."""

from typing import Any, Dict, List, Optional, Set

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.middleware.auth import get_current_user
from app.services.adaptive_learning import assess_user_skills
from app.services.lesson_assessment import progressive_hints
from app.services.service_company_sprint import daily_focus_plan, load_sprint, ordered_lessons
import json
import os

router = APIRouter(prefix="/api/v1/sprint", tags=["service-sprint"])

_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LESSONS_DIR = os.path.join(_APP_DIR, "data", "lessons")


class HintRequest(BaseModel):
    step_index: int = Field(..., ge=0)
    hints_used: int = Field(default=0, ge=0, le=10)


def _load_lesson(slug: str) -> Optional[Dict[str, Any]]:
    path = os.path.join(_LESSONS_DIR, f"{slug}.json")
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


@router.get("/curriculum")
async def get_curriculum(user=Depends(get_current_user)):
    data = load_sprint()
    return {
        "success": True,
        "curriculum": data,
        "ordered_lessons": ordered_lessons(),
    }


@router.get("/today")
async def get_today_plan(user=Depends(get_current_user)):
    """Today's focus tasks ordered by sprint daily_scrum policy."""
    assessment = await assess_user_skills(user["id"])
    skills = assessment.get("skills") or {}
    weak_domains: List[str] = []
    mastered: Set[str] = set()
    for domain, evidence in skills.items():
        score = float(evidence.get("score") or 0)
        attempts = int(evidence.get("total_attempts") or 0)
        if attempts > 0 and score < 70:
            weak_domains.append(domain)
        # Lesson mastery is tracked separately; domain score >= 80 is a soft signal.
        if attempts > 0 and score >= 80:
            # Not a lesson slug — only used as weak-domain filter above.
            pass

    overall = float(assessment.get("overall_accuracy") or assessment.get("overall_score") or 0)
    plan = daily_focus_plan(
        mastered=mastered,
        weak_domains=weak_domains[:3],
        reviews=[],
        mock_ready=overall >= 60,
    )
    return {"success": True, "data": plan, "skills_summary": {
        "weak_domains": weak_domains[:5],
        "overall": overall,
    }}


@router.post("/lessons/{slug}/hint")
async def get_step_hint(slug: str, body: HintRequest, user=Depends(get_current_user)):
    """Progressive hint for a lesson step. Never awards mastery."""
    lesson = _load_lesson(slug)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    steps = lesson.get("steps") or []
    if body.step_index < 0 or body.step_index >= len(steps):
        raise HTTPException(status_code=404, detail="Step not found")
    step = steps[body.step_index]
    result = progressive_hints(step, body.hints_used)
    return {
        "success": True,
        "slug": slug,
        "step_index": body.step_index,
        **result,
        "policy": "hints_never_award_mastery",
    }
