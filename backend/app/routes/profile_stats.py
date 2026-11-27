"""Profile stats — PostgreSQL-backed, no MongoDB."""

from datetime import datetime, timezone
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/profile", tags=["profile"])


@router.get("/stats")
async def get_stats(user=Depends(get_current_user)):
    return await get_profile_stats(user["id"])


@router.put("/integrations")
async def update_integration(payload: dict, user=Depends(get_current_user)):
    platform = payload.get("platform", "").lower()
    username = payload.get("username", "")
    if platform not in ("github", "leetcode"):
        raise HTTPException(status_code=400, detail="Supported platforms: github, leetcode")
    return await update_integrations(user["id"], platform, username)


@router.get("/readiness-score")
async def readiness_score(user=Depends(get_current_user)):
    uid = user["id"]
    # Get user profile from PostgreSQL instead of MongoDB
    from app.services.auth import get_user_profile
    user_profile = await get_user_profile(uid)
    
    # Get skill graph from PostgreSQL
    skill_graph = await get_skill_graph(uid)
    categories = skill_graph.get("categories", {}) if skill_graph else {}
    
    def _get_score(cat):
        c = categories.get(cat, {})
        return c.get("score", 0) if isinstance(c, dict) else (c or 0)
    
    dsa_score = _get_score("dsa")
    aptitude_score = _get_score("aptitude")
    behavioral_score = _get_score("behavioral")
    resume_score = _get_score("resume")
    interview_score = _get_score("system_design")
    
    # Get total interviews from PostgreSQL
    total_interviews = await get_total_interviews(uid)
    interview_comp = min(interview_score * 0.2 + (total_interviews / 10) * 20, 20)
    dsa_comp = dsa_score * 0.4
    aptitude_comp = aptitude_score * 0.2
    behavioral_comp = behavioral_score * 0.1
    
    # Get resume from PostgreSQL
    resume_doc = await get_resume(uid)
    resume_ats = resume_doc.get("ats_score", 0) if resume_doc else 0
    resume_comp = resume_ats * 0.1
    
    score = min(round(dsa_comp + aptitude_comp + interview_comp + behavioral_comp + resume_comp), 100)
    
    # Get gamification from PostgreSQL
    gam = await get_gamification(uid) or {}
    
    return {
        "score": score,
        "dsa_score": dsa_score,
        "aptitude_score": aptitude_score,
        "behavioral_score": behavioral_score,
        "resume_score": resume_comp,
        "interview_score": interview_comp,
        "gamification": {
            "overall_score": gam.get("overall_score", 0) if gam else 0,
            "level": gam.get("level", 1) if gam else 1,
            "diamonds": gam.get("diamonds", 0) if gam else 0,
            "streak": gam.get("streak", 0) if gam else 0,
        },
    }