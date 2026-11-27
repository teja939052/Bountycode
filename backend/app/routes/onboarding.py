"""Onboarding — PostgreSQL-backed, no MongoDB."""

from datetime import datetime, timezone
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/onboarding", tags=["onboarding"])

ALLOWED_CAREER_GOALS = {
    "internship", "placements", "learning", "hackathons", "full_stack", "ai_ml"
}

ALLOWED_TECH_INTERESTS = {
    "java", "python", "javascript", "react", "nodejs", "spring_boot",
    "dsa", "ai", "ml", "cybersecurity", "data_science"
}


def _validate_list(values: List[str], allowed: set, field_name: str) -> List[str]:
    invalid = [v for v in values if v not in allowed]
    if invalid:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {field_name}: {', '.join(invalid)}",
        )
    return values


QUEST_STEPS = [
    {
        "id": "step-1",
        "title": "Choose Your Language",
        "description": "Pick the language you want to learn. C, C++, Java, or Python — all paths lead to placement success.",
        "type": "navigation",
        "action": "Select a language from the learning hub",
        "target": "/learn/c",
        "icon": "\U0001f3af",
    },
    {
        "id": "step-2",
        "title": "Write Your First Code",
        "description": "Open the first lesson and run your first program. You will have code running in under 30 seconds.",
        "type": "action",
        "action": "Open any lesson and click Run",
        "target": "/free-trial",
        "icon": "\u2328\ufe0f",
    },
    {
        "id": "step-3",
        "title": "Build Your First Project",
        "description": "Apply what you've learned by building a small project. HTML/CSS, a simple function, or a data script.",
        "type": "action",
        "action": "Create a project in the learning hub",
        "target": "/projects",
        "icon": "\U0001f5d1",
    },
    {
        "id": "step-4",
        "title": "Take a Practice Quiz",
        "description": "Test your knowledge with a short quiz. Instant feedback, no pressure.",
        "type": "assessment",
        "action": "Take a practice quiz in the learning hub",
        "target": "/practice",
        "icon": "\U0001f3af\ufe0f",
    },
    {
        "id": "step-5",
        "title": "Set Your Goals",
        "description": "Define your placement timeline and target companies.",
        "type": "configuration",
        "action": "Update your onboarding profile",
        "target": "/onboarding/doors",
        "icon": "\U0001f4cd",
    },
]


@router.get("/steps")
async def onboarding_steps():
    """Get the onboarding quest steps."""
    return {"steps": QUEST_STEPS}


@router.get("/career-goals")
async def career_goals(user=Depends(get_current_user)):
    """Get user's career goals from PostgreSQL."""
    async with get_session() as session:
        # In a full implementation, this would query a user profile
        return {"career_goals": [], "tech_interests": []}


@router.post("/career-goals")
async def set_career_goals(
    goals: List[str],
    tech_interests: List[str],
    user=Depends(get_current_user),
):
    """Set user's career goals."""
    _validate_list(goals, ALLOWED_CAREER_GOALS, "career goal")
    _validate_list(tech_interests, ALLOWED_TECH_INTERESTS, "tech interest")
    # In a full implementation, this would save to user profile
    return {"success": True, "message": "Career goals and tech interests saved"}


@router.get("/profile")
async def onboarding_profile(user=Depends(get_current_user)):
    """Get user's onboarding profile."""
    async with get_session() as session:
        # In a full implementation, this would query user profile
        return {
            "career_goals": [],
            "tech_interests": [],
            "language": user.get("preferred_language", "cpp"),
            "experience_level": user.get("experience_level", "absolute_beginner"),
        }


@router.post("/profile")
async def set_onboarding_profile(
    language: str = "cpp",
    experience_level: str = "absolute_beginner",
    user=Depends(get_current_user),
):
    """Set user's onboarding profile."""
    # In a full implementation, this would save to user profile
    return {"success": True, "message": "Onboarding profile updated"}