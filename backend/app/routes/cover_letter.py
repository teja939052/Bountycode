from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.database import users_collection, resumes_collection, cover_letters_collection
from app.middleware.auth import get_current_user
from app.services.ai import generate_cover_letter, generate_linkedin_about, generate_salary_negotiation_tips
from app.services.usage import check_and_reset_monthly_usage, can_use_feature
from app.config import get_settings
from bson import ObjectId

router = APIRouter(prefix="/api/tools", tags=["tools"])
settings = get_settings()


class CoverLetterRequest(BaseModel):
    resume_id: str
    job_description: str
    company_name: str = ""


class LinkedInRequest(BaseModel):
    resume_id: str
    target_role: str = ""


class SalaryNegotiationRequest(BaseModel):
    job_title: str
    offered_salary: str
    location: str
    years_experience: int = 0
    company_size: str = ""
    benefits: list = []


@router.post("/cover-letter")
async def create_cover_letter(req: CoverLetterRequest, user=Depends(get_current_user)):
    user = await check_and_reset_monthly_usage(user)

    if not can_use_feature(user, "cover_letter"):
        raise HTTPException(
            status_code=403,
            detail=f"Free tier limit reached ({getattr(settings, 'FREE_TIER_COVER_LETTER_LIMIT', 3)} cover letters/month). Upgrade to Pro for unlimited.",
        )

    try:
        resume = await resumes_collection.find_one({"_id": ObjectId(req.resume_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid resume ID")

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    if resume["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    resume_text = resume.get("original_text", "")

    cover_letter_text = await generate_cover_letter(resume_text, req.job_description, req.company_name)

    cover_letter_doc = {
        "user_id": user["id"],
        "resume_id": req.resume_id,
        "job_description": req.job_description,
        "company_name": req.company_name,
        "cover_letter_text": cover_letter_text,
        "created_at": datetime.now(timezone.utc),
    }

    result = await cover_letters_collection.insert_one(cover_letter_doc)

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$inc": {"cover_letters_used": 1}},
    )

    return {
        "cover_letter_id": str(result.inserted_id),
        "cover_letter": cover_letter_text,
    }


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


@router.post("/salary-negotiation")
async def get_salary_negotiation_tips(req: SalaryNegotiationRequest, user=Depends(get_current_user)):
    offer_details = {
        "job_title": req.job_title,
        "offered_salary": req.offered_salary,
        "location": req.location,
        "years_experience": req.years_experience,
        "company_size": req.company_size,
        "benefits": req.benefits,
    }

    tips = await generate_salary_negotiation_tips(offer_details)

    return tips


@router.get("/cover-letter/history")
async def get_cover_letter_history(user=Depends(get_current_user)):
    cursor = cover_letters_collection.find(
        {"user_id": user["id"]}
    ).sort("created_at", -1).limit(20)

    letters = []
    async for doc in cursor:
        letters.append({
            "id": str(doc["_id"]),
            "company_name": doc.get("company_name", ""),
            "created_at": doc.get("created_at"),
        })

    return {"cover_letters": letters}
