from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.database import resumes_collection
from app.middleware.auth import get_current_user
from app.services.ai_cover_letter import generate_linkedin_about
from app.config import get_settings
from bson import ObjectId

router = APIRouter(prefix="/api/v1/tools", tags=["tools"])
settings = get_settings()


class LinkedInRequest(BaseModel):
    resume_id: str
    target_role: str = ""


@router.post("/linkedin-about")
async def create_linkedin_about(req: LinkedInRequest, user=Depends(get_current_user)):
    try:
        resume = await resumes_collection.find_one({"_id": ObjectId(req.resume_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid resume ID")

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    if resume["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    resume_text = resume.get("original_text", "")

    linkedin_about = await generate_linkedin_about(resume_text, req.target_role)

    return {
        "linkedin_about": linkedin_about,
    }
