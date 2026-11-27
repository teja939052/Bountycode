"""Resume routes — migrated from MongoDB `resumes` collection to PostgreSQL `resume_metadata` table.

Actual resume file bytes live in Supabase Storage; this layer owns metadata,
extracted text, ATS analysis results and optimization history.
"""

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from app.models.resume import GenerateResume, OptimizeRequest
from app.database import get_session
from app.middleware.auth import get_current_user
from app.models.identity import User
from app.services.ai_resume import analyze_resume, optimize_ats, generate_resume_content
from app.services.resume_parser import extract_text_from_pdf
from app.services.export import export_to_docx, export_to_pdf
from app.services.ats_semantic import semantic_score, section_scores, semantic_gaps
from app.services.ats_enhanced import calculate_ats_score as keyword_ats_score
from app.services.postgres_gamification import record_practice as pg_record_practice
from app.repositories.assessments import ResumeMetadataRepository
from app.config import get_settings
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/api/v1/resume", tags=["resume"])
settings = get_settings()


def validate_pdf_content(content: bytes) -> bool:
    return content[:5] == b"%PDF-"


class SemanticScoreRequest(BaseModel):
    resume_text: str
    job_description: str = ""


class RuleBasedATSRequest(BaseModel):
    resume_text: str
    job_description: str = ""


@router.post("/analyze-rulebased")
async def analyze_resume_rulebased(req: RuleBasedATSRequest, user=Depends(get_current_user)):
    """Deterministic, non-AI ATS analysis. Always works without API keys/credits.

    Uses ``RealATSScanner`` to simulate enterprise ATS parsing (Workday, Lever,
    Greenhouse, iCIMS...) and returns a grade, critical issues, keyword gaps, and
    line-by-line rewrite suggestions. This is the reliable fallback and the
    core of the exact resume analyzer."""
    from app.services.real_ats import RealATSScanner

    scanner = RealATSScanner()
    result = scanner.full_scan(req.resume_text or "", req.job_description or "")

    return {
        "ats_score": result.get("ats_score"),
        "grade": result.get("grade"),
        "would_pass_ats": result.get("would_pass_ats", False),
        "parsing_simulation": result.get("parsing_simulation"),
        "section_detection": result.get("section_detection"),
        "contact_detection": result.get("contact_detection"),
        "content_analysis": result.get("content_analysis"),
        "keyword_analysis": result.get("keyword_analysis"),
        "critical_issues": result.get("critical_issues", []),
        "recommendations": result.get("recommendations", []),
    }


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if user.get("plan") == "free" and user.get("resumes_used", 0) >= settings.FREE_TIER_RESUME_LIMIT:
        raise HTTPException(
            status_code=403,
            detail=f"Free tier limit reached ({settings.FREE_TIER_RESUME_LIMIT} resumes). Upgrade to Pro.",
        )

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")

    if not validate_pdf_content(content):
        raise HTTPException(status_code=400, detail="File is not a valid PDF")

    text = extract_text_from_pdf(content)
    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")

    analysis = await analyze_resume(text)

    resume_data = {
        "user_id": UUID(user["id"]),
        "file_name": file.filename,
        "original_text": text,
        "analysis": analysis,
        "ats_score": None,
        "optimized_text": None,
        "optimization_details": None,
        "source": "upload",
        "storage_path": "",  # file bytes not persisted to Supabase Storage in this flow
    }
    resume_repo = ResumeMetadataRepository(session)
    resume = await resume_repo.create(resume_data)

    # Increment resumes_used counter
    await session.execute(
        update(User)
        .where(User.id == UUID(user["id"]))
        .values(resumes_used=(User.resumes_used or 0) + 1)
    )

    # Gamification Law: record resume activity through the canonical pipeline.
    # A created resume carries no ATS score yet, so score 0 — the ats_master /
    # ats_95 badges fire later from /optimize where the real ATS score exists.
    await pg_record_practice(session, user["id"], "resume", 0, role=user.get("role") or user.get("target_role") or "sde")

    return {
        "resume_id": str(resume.id),
        "text": text,
        "analysis": analysis,
    }


@router.post("/generate")
async def generate_resume(
    req: GenerateResume,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if user.get("plan") == "free" and user.get("resumes_used", 0) >= settings.FREE_TIER_RESUME_LIMIT:
        raise HTTPException(
            status_code=403,
            detail=f"Free tier limit reached ({settings.FREE_TIER_RESUME_LIMIT} resumes). Upgrade to Pro.",
        )

    content = await generate_resume_content(
        req.name, req.email, req.target_role, req.experience, req.education, req.skills
    )

    resume_data = {
        "user_id": UUID(user["id"]),
        "file_name": f"{req.name or 'resume'}.pdf",
        "original_text": content,
        "analysis": None,
        "ats_score": None,
        "optimized_text": None,
        "optimization_details": None,
        "source": "generated",
        "storage_path": "",
    }
    resume_repo = ResumeMetadataRepository(session)
    resume = await resume_repo.create(resume_data)

    # Same canonical resume counter as upload (no ATS score yet).
    await session.execute(
        update(User)
        .where(User.id == UUID(user["id"]))
        .values(resumes_used=(User.resumes_used or 0) + 1)
    )

    await pg_record_practice(session, user["id"], "resume", 0, role=user.get("role") or user.get("target_role") or "sde")

    return {
        "resume_id": str(resume.id),
        "content": content,
    }


@router.post("/optimize")
async def optimize_resume(
    req: OptimizeRequest,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        resume_id = UUID(req.resume_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid resume ID")

    resume_repo = ResumeMetadataRepository(session)
    resume = await resume_repo.get_by_id(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    if str(resume.user_id) != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    optimization = await optimize_ats(resume.original_text or "", req.job_description)

    await resume_repo.update(
        resume_id,
        {
            "ats_score": optimization.get("ats_score", 0),
            "optimized_text": optimization.get("optimized_resume", ""),
            "optimization_details": optimization,
        },
    )

    # Real ATS score exists here — feeds ats_master (90+) / ats_95 (95+).
    await pg_record_practice(
        session,
        user["id"],
        "resume",
        optimization.get("ats_score", 0),
        role=user.get("role") or user.get("target_role") or "sde",
        metadata={"resume_id": req.resume_id, "action": "optimize_ats"},
    )

    return optimization


@router.get("/{resume_id}/export/docx")
async def download_docx(
    resume_id: str,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        resume_uuid = UUID(resume_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid resume ID")

    resume_repo = ResumeMetadataRepository(session)
    resume = await resume_repo.get_by_id(resume_uuid)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    if str(resume.user_id) != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    text = resume.optimized_text or resume.original_text or ""
    docx_bytes = export_to_docx(text)

    return StreamingResponse(
        iter([docx_bytes]),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=resume.docx"},
    )


@router.get("/{resume_id}/export/pdf")
async def download_pdf(
    resume_id: str,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        resume_uuid = UUID(resume_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid resume ID")

    resume_repo = ResumeMetadataRepository(session)
    resume = await resume_repo.get_by_id(resume_uuid)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    if str(resume.user_id) != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    text = resume.optimized_text or resume.original_text or ""
    pdf_bytes = export_to_pdf(text)

    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=resume.pdf"},
    )


@router.get("/history")
async def get_resume_history(
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    resume_repo = ResumeMetadataRepository(session)
    resumes = await resume_repo.list_by_user(UUID(user["id"]), limit=20, offset=0)

    return {
        "resumes": [
            {
                "id": str(r.id),
                "source": r.source or "upload",
                "ats_score": r.ats_score,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "file_name": r.file_name,
            }
            for r in resumes
        ]
    }
