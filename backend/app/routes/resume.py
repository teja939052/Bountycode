from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from pydantic import BaseModel
from typing import Optional
from app.models.resume import GenerateResume, OptimizeRequest
from app.database import users_collection, resumes_collection
from app.middleware.auth import get_current_user
from app.services.ai import analyze_resume, optimize_ats, generate_resume_content
from app.services.resume_parser import extract_text_from_pdf
from app.services.export import export_to_docx, export_to_pdf
from app.services.ats_semantic import semantic_score, section_scores, semantic_gaps
from app.services.ats_enhanced import calculate_ats_score as keyword_ats_score
from app.config import get_settings
from bson import ObjectId
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/api/v1/resume", tags=["resume"])
settings = get_settings()


def validate_pdf_content(content: bytes) -> bool:
    return content[:5] == b"%PDF-"


class SemanticScoreRequest(BaseModel):
    resume_text: str
    job_description: str = ""


@router.post("/semantic-score")
async def semantic_ats_score(req: SemanticScoreRequest, user=Depends(get_current_user)):
    jd = req.job_description or ""
    resume_text = req.resume_text or ""
    overall = semantic_score(resume_text, jd)
    sections = section_scores(resume_text, jd)
    gaps = semantic_gaps(resume_text, jd)
    keyword = keyword_ats_score(resume_text, jd)
    return {
        "semantic": overall,
        "section_scores": sections,
        "semantic_gaps": gaps,
        "keyword_ats": keyword,
    }


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), user=Depends(get_current_user)):
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

    resume_doc = {
        "user_id": user["id"],
        "original_text": text,
        "analysis": analysis,
        "ats_score": None,
        "optimized_text": None,
        "optimization_details": None,
        "source": "upload",
        "created_at": datetime.now(timezone.utc),
    }
    result = await resumes_collection.insert_one(resume_doc)

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$inc": {"resumes_used": 1}},
    )

    return {
        "resume_id": str(result.inserted_id),
        "text": text,
        "analysis": analysis,
    }


@router.post("/generate")
async def generate_resume(req: GenerateResume, user=Depends(get_current_user)):
    if user.get("plan") == "free" and user.get("resumes_used", 0) >= settings.FREE_TIER_RESUME_LIMIT:
        raise HTTPException(
            status_code=403,
            detail=f"Free tier limit reached ({settings.FREE_TIER_RESUME_LIMIT} resumes). Upgrade to Pro.",
        )

    content = await generate_resume_content(
        req.name, req.email, req.target_role, req.experience, req.education, req.skills
    )

    resume_doc = {
        "user_id": user["id"],
        "original_text": content,
        "analysis": None,
        "ats_score": None,
        "optimized_text": None,
        "optimization_details": None,
        "source": "generated",
        "created_at": datetime.now(timezone.utc),
    }
    result = await resumes_collection.insert_one(resume_doc)

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$inc": {"resumes_used": 1}},
    )

    return {
        "resume_id": str(result.inserted_id),
        "content": content,
    }


@router.post("/optimize")
async def optimize_resume(req: OptimizeRequest, user=Depends(get_current_user)):
    try:
        resume = await resumes_collection.find_one({"_id": ObjectId(req.resume_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid resume ID")

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    if resume["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    optimization = await optimize_ats(resume["original_text"], req.job_description)

    await resumes_collection.update_one(
        {"_id": ObjectId(req.resume_id)},
        {"$set": {
            "ats_score": optimization.get("ats_score", 0),
            "optimized_text": optimization.get("optimized_resume", ""),
            "optimization_details": optimization,
        }},
    )

    return optimization


@router.get("/{resume_id}/export/docx")
async def download_docx(resume_id: str, user=Depends(get_current_user)):
    try:
        resume = await resumes_collection.find_one({"_id": ObjectId(resume_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid resume ID")

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    if resume["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    text = resume.get("optimized_text") or resume.get("original_text", "")
    docx_bytes = export_to_docx(text)

    return StreamingResponse(
        iter([docx_bytes]),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=resume.docx"},
    )


@router.get("/{resume_id}/export/pdf")
async def download_pdf(resume_id: str, user=Depends(get_current_user)):
    try:
        resume = await resumes_collection.find_one({"_id": ObjectId(resume_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid resume ID")

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    if resume["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    text = resume.get("optimized_text") or resume.get("original_text", "")
    pdf_bytes = export_to_pdf(text)

    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=resume.pdf"},
    )


@router.get("/history")
async def get_resume_history(user=Depends(get_current_user)):
    cursor = resumes_collection.find(
        {"user_id": user["id"]}
    ).sort("created_at", -1).limit(20)

    resumes = []
    async for doc in cursor:
        resumes.append({
            "id": str(doc["_id"]),
            "source": doc.get("source", "upload"),
            "ats_score": doc.get("ats_score"),
            "created_at": doc.get("created_at"),
        })

    return {"resumes": resumes}
