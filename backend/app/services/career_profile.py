"""Career profile service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session
from app.models.career import CareerProfile
from sqlalchemy import select

router = APIRouter(prefix="/api/v1/career-profile", tags=["career-profile"])


@router.get("/")
async def get_career_profile(user=Depends(get_current_user)):
    """Get user's career profile."""
    async with get_session() as session:
        result = await session.execute(
            select(CareerProfile).where(CareerProfile.user_id == user["id"])
        )
        profile = result.scalar_one_or_none()
    if not profile:
        return {"user_id": user["id"], "profile": None}
    return {
        "user_id": user["id"],
        "profile": {
            "target_role": profile.target_role,
            "target_companies": profile.target_companies or [],
            "skills": profile.skills or [],
        },
    }


@router.post("/update")
async def update_career_profile(
    target_role: str,
    target_companies: List[str],
    user=Depends(get_current_user),
):
    """Update career profile."""
    async with get_session() as session:
        result = await session.execute(
            select(CareerProfile).where(CareerProfile.user_id == user["id"])
        )
        profile = result.scalar_one_or_none()
        if not profile:
            profile = CareerProfile(
                user_id=user["id"],
                target_role=target_role,
                target_companies=target_companies,
            )
            session.add(profile)
        else:
            profile.target_role = target_role
            profile.target_companies = target_companies
        await session.commit()
    return {"user_id": user["id"], "status": "updated"}

async def append_section_item(user_id: str) -> dict:
    """Stub for append_section_item."""
    return {"user_id": user_id}


async def delete_section_item(user_id: str) -> dict:
    """Stub for delete_section_item."""
    return {"user_id": user_id}


async def get_profile(user_id: str) -> dict:
    """Stub for get_profile."""
    return {"user_id": user_id}


async def parse_resume_to_profile(user_id: str) -> dict:
    """Stub for parse_resume_to_profile."""
    return {"user_id": user_id}


async def update_profile(user_id: str) -> dict:
    """Stub for update_profile."""
    return {"user_id": user_id}
