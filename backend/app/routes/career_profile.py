from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Dict, Optional, List
from app.middleware.auth import get_current_user
from app.services.career_profile import (
    get_profile,
    update_profile,
    parse_resume_to_profile,
    append_section_item,
    delete_section_item,
)
from app.services.resume_parser import extract_text_from_pdf
from app.config import get_settings

router = APIRouter(prefix="/api/v1/profile", tags=["career-profile"])
settings = get_settings()


# ── Schemas ──────────────────────────────────────────────────────────────────

class ProfileUpdatePayload(BaseModel):
    full_name: Optional[str] = None
    contact: Optional[Dict] = None
    summary: Optional[str] = None
    skills: Optional[List[str]] = None
    experience: Optional[List[Dict]] = None
    education: Optional[List[Dict]] = None
    projects: Optional[List[Dict]] = None
    certifications: Optional[List[Dict]] = None
    custom_sections: Optional[Dict] = None


class AppendItemPayload(BaseModel):
    item: Dict


class FromResumePayload(BaseModel):
    resume_text: str
    resume_id: Optional[str] = None


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.get("")
async def get_my_profile(user=Depends(get_current_user)):
    return await get_profile(user["id"])


@router.put("")
async def update_my_profile(payload: ProfileUpdatePayload, user=Depends(get_current_user)):
    data = payload.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(status_code=400, detail="No fields provided")
    return await update_profile(user["id"], data)


@router.post("/from-resume")
async def create_from_resume_text(payload: FromResumePayload, user=Depends(get_current_user)):
    try:
        return await parse_resume_to_profile(
            user_id=user["id"],
            resume_text=payload.resume_text,
            resume_id=payload.resume_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/upload-resume")
async def upload_resume_to_profile(file: UploadFile = File(...), user=Depends(get_current_user)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")
    if content[:5] != b"%PDF-":
        raise HTTPException(status_code=400, detail="File is not a valid PDF")

    try:
        return await parse_resume_to_profile(
            user_id=user["id"],
            pdf_bytes=content,
            source="resume_upload",
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/sections/{section}/items")
async def add_section_item(section: str, payload: AppendItemPayload, user=Depends(get_current_user)):
    try:
        return await append_section_item(user["id"], section, payload.item)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/sections/{section}/items/{index}")
async def remove_section_item(section: str, index: int, user=Depends(get_current_user)):
    try:
        return await delete_section_item(user["id"], section, index)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
