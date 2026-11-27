"""Target selection + skill baseline — P0: personal starting path.

Reuses existing infrastructure:
- exam engine for diagnostic attempt persistence/scoring
- assessment_blueprint.select_questions for role-specific question selection
- skill_assessment for baseline mastery (skill_graph)
- role_engine.profiles for role/company definitions
- adaptive_learning.generate_learning_path for the preparation path
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid
from app.middleware.auth import get_current_user
from app.services.exam_engine import score_question
from app.services.assessment_blueprint import select_questions
from app.services.skill_assessment import (
    initialize_skill_graph,
    update_skill_score,
    get_skill_graph,
    SKILL_CATEGORIES,
)
from app.services.role_engine.profiles import get_profile, list_profiles
from app.services.adaptive_learning import generate_learning_path

router = APIRouter(prefix="/api/v1/target", tags=["target"])


class TargetSelectReq(BaseModel):
    company: Optional[str] = None
    role: str = "sde"
    language: str = "python"
    experience_level: str = "fresher"
    study_hours_per_week: int = 10
    target_date: Optional[str] = None


class DiagnosticAnswer(BaseModel):
    attempt_id: str
    question_id: str
    answer: Any


# ────────────────────────────────────────────────────────────
# Role / company metadata
# ────────────────────────────────────────────────────────────
@router.get("/roles")
async def list_roles():
    return {"roles": list_profiles()}


@router.get("/companies")
async def list_companies(role: Optional[str] = Query(None)):
    profile = get_profile(role or "sde")
    companies = [c.name for c in (profile.target_companies if profile else [])]
    return {"companies": companies}


# ────────────────────────────────────────────────────────────
# Target generation
# ────────────────────────────────────────────────────────────
@router.post("/select")
async def select_target(req: TargetSelectReq, user=Depends(get_current_user)):
    """Generate a personalized target path based on user's role/company."""
    profile = get_profile(req.role)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Role {req.role} not found")

    skills = get_skill_graph(user["id"]) if user else None

    target = {
        "company": req.company or "any",
        "role": req.role,
        "language": req.language,
        "experience_level": req.experience_level,
        "study_hours_per_week": req.study_hours_per_week,
        "target_date": req.target_date,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    return target


@router.get("/dashboard")
async def target_dashboard(user=Depends(get_current_user)):
    """Get target dashboard for the current user."""
    skills = get_skill_graph(user["id"]) if user else None
    return {
        "user_id": user["id"],
        "skills": skills,
        "targets": [],
    }