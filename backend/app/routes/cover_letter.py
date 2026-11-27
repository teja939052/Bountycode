"""Cover letter routes — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.database import get_session
from app.middleware.auth import get_current_user
from app.services.ai_cover_letter import generate_linkedin_about
from app.config import get_settings
from app.models.career import ResumeMetadata
from sqlalchemy import select

router = APIRouter(prefix="/api/v1/tools", tags=["tools"])
settings = get_settings()


class LinkedInRequest(BaseModel):
    resume_id: str
    target_role: str = ""


@router.post("/linkedin-about")
async def create_linkedin_about(req: LinkedInRequest, user=Depends(get_current_user)):
    async with get_session() as session:
        result = await session.execute(
            select(ResumeMetadata).where(ResumeMetadata.id == req.resume_id)
        )
        resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    if resume.user_id != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    resume_text = resume.original_text

    linkedin_about = await generate_linkedin_about(resume_text, req.target_role)

    return {
        "linkedin_about": linkedin_about,
    }