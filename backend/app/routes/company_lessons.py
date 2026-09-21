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

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/company-lessons", tags=["company-lessons"])

_LESSONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "data", "lessons")

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
    score: float = Field(..., ge=0, le=100)
    time_spent_seconds: int = Field(default=0, ge=0)


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
            if not data:
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
    if data is None:
        raise HTTPException(status_code=404, detail=f"Lesson not found: {slug}")
    return {"success": True, "data": data}


@router.post("/{slug}/complete", response_model=None)
async def complete_lesson(slug: str, req: CompleteRequest, user=Depends(get_current_user)):
    data = _load_lesson(slug)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Lesson not found: {slug}")
    xp_reward = int(data.get("xp_reward") or data.get("diamonds") or 50)
    mastery_threshold = float(data.get("mastery_threshold") or data.get("assessment", {}).get("mastery_threshold") or 0.7)
    passed = req.score >= (mastery_threshold * 100)
    reward = record_practice(
        user_id=user["id"],
        activity_type="company_lesson",
        payload={
            "lesson_slug": slug,
            "lesson_title": data.get("title") or slug,
            "domain": data.get("domain") or data.get("pattern") or "General",
            "score": req.score,
            "passed": passed,
            "time_spent_seconds": req.time_spent_seconds,
        },
        pedagogical_score=10 if passed else 5,
    )
    return {
        "success": True,
        "data": {
            "passed": passed,
            "xp_earned": reward.get("xp_earned") if isinstance(reward, dict) else xp_reward,
            "proof_earned": reward.get("proof_earned") if isinstance(reward, dict) else xp_reward,
            "mastery_threshold": mastery_threshold,
        },
    }
