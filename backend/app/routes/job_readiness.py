"""Job Readiness Engine routes — the outcome loop API.

POST /api/v1/job-readiness/analyze-jd        — JD text → skill extraction + gap + curriculum
GET  /api/v1/job-readiness/role/{role_id}     — Competency graph for a role
GET  /api/v1/job-readiness/gaps               — Personalized gap analysis vs target role
GET  /api/v1/job-readiness/curriculum         — Ordered study plan from gaps
GET  /api/v1/job-readiness/company/{company}  — Company-specific readiness deep-dive
POST /api/v1/job-readiness/set-target         — Save job target to user profile
GET  /api/v1/job-readiness/target             — Get saved job target
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from bson import ObjectId

from app.middleware.auth import get_current_user
from app.database import users_collection, gamification_collection, skill_graph_collection
from app.services.job_readiness import (
    ROLE_PROFILES, COMPANY_DEEP_PROFILES,
    analyze_job_description, get_competency_graph,
    get_personalized_gaps, build_curriculum,
    analyze_jd_and_build_plan,
)
from app.services.readiness_engine import COMPANY_PROFILES, calculate_readiness, predict_readiness_date
from app.routes.readiness import (
    _gather_dsa_data, _gather_aptitude_data, _gather_cs_fundamentals_data,
    _gather_coding_data, _gather_interview_data, _gather_resume_data,
    _gather_project_data,
)

router = APIRouter(prefix="/api/v1/job-readiness", tags=["Job Readiness Engine"])


class AnalyzeJDRequest(BaseModel):
    jd_text: str = Field(..., min_length=20, max_length=10000, description="Job description text")


class SetTargetRequest(BaseModel):
    role_id: str = Field(..., description="Target role: sde, data_analyst, data_scientist, qa_engineer, devops, product_manager")
    company_id: Optional[str] = Field(None, description="Target company (optional)")
    jd_text: Optional[str] = Field(None, description="Job description (optional)")


# ─── Analyze Job Description ───
@router.post("/analyze-jd")
async def analyze_jd(req: AnalyzeJDRequest, user=Depends(get_current_user)):
    """Paste a job description → get skill extraction, matched role, gap analysis, and curriculum."""
    uid = user["id"]
    result = await analyze_jd_and_build_plan(uid, req.jd_text)
    return result


# ─── Role Competency Graph ───
@router.get("/roles")
async def list_roles():
    """List all available target roles."""
    return {
        "roles": [
            {
                "id": r["id"],
                "title": r["title"],
                "icon": r["icon"],
                "description": r["description"],
            }
            for r in ROLE_PROFILES.values()
        ]
    }


@router.get("/role/{role_id}")
async def get_role_graph(role_id: str):
    """Get competency graph for a role: skill nodes with weights and prerequisites."""
    graph = get_competency_graph(role_id)
    if "error" in graph:
        raise HTTPException(status_code=404, detail=graph["error"])
    return graph


# ─── Personalized Gap Analysis ───
@router.get("/gaps")
async def get_gaps(role: str = "sde", user=Depends(get_current_user)):
    """Compare your current skills against a target role. Returns gaps sorted by priority."""
    result = await get_personalized_gaps(user["id"], role)
    return result


# ─── Curriculum ───
@router.get("/curriculum")
async def get_curriculum(role: str = "sde", user=Depends(get_current_user)):
    """Get a personalized study plan based on your gaps for the target role."""
    gaps_data = await get_personalized_gaps(user["id"], role)
    mastery_doc = await skill_graph_collection.find_one({"user_id": user["id"]}) or {}
    mission_progress = {}
    for cat_id, cat_data in mastery_doc.get("categories", {}).items():
        for skill_id, skill_data in cat_data.get("skills", {}).items():
            mission_progress[skill_id] = {"overall": skill_data.get("score", 0)}

    curriculum = build_curriculum(gaps_data["gaps"], gaps_data["role"], mission_progress)
    total_minutes = sum(c["estimated_minutes"] for c in curriculum if not c["completed"])

    return {
        "role": gaps_data["role"],
        "readiness": gaps_data["overall_readiness"],
        "curriculum": curriculum,
        "stats": {
            "total_topics": len(curriculum),
            "completed": sum(1 for c in curriculum if c["completed"]),
            "remaining": sum(1 for c in curriculum if not c["completed"]),
            "estimated_weeks": max(1, round(total_minutes / 60 / 10)),
            "estimated_minutes": total_minutes,
        },
    }


# ─── Company Readiness Deep-Dive ───
@router.get("/company/{company_id}")
async def get_company_readiness(company_id: str, user=Depends(get_current_user)):
    """Company-specific readiness: your skill-by-skill readiness vs what this company needs."""
    company_id = company_id.lower().strip()
    profile = COMPANY_DEEP_PROFILES.get(company_id)
    if not profile:
        # Fall back to the basic readiness engine profiles
        basic_profile = COMPANY_PROFILES.get(company_id)
        if not basic_profile:
            raise HTTPException(status_code=404, detail=f"Unknown company: {company_id}")
        profile = {
            "id": company_id,
            "title": company_id.title(),
            "icon": "🏢",
            "tier": "mass" if basic_profile.get("min_solved", 0) < 100 else "mid",
            "color": "#666666",
            "min_readiness": 40,
            "skill_requirements": {
                "dsa": basic_profile.get("min_solved", 0) * 2,
                "aptitude": 40,
                "behavioral": 40,
                "resume": 40,
                "coding": 40,
                "system_design": 30,
            },
            "oa_format": "Varies by role",
            "interview_rounds": ["Online Assessment", "Technical Interview", "HR Interview"],
            "focus_areas": basic_profile.get("focus_topics", []),
            "leadership_principles": [],
        }

    uid = user["id"]
    dsa = await _gather_dsa_data(uid)
    apt = await _gather_aptitude_data(uid)
    cs = await _gather_cs_fundamentals_data(uid)
    coding = await _gather_coding_data(uid)
    interview = await _gather_interview_data(uid)
    resume = await _gather_resume_data(uid)
    projects = await _gather_project_data(uid)

    readiness_result = calculate_readiness(
        dsa_data=dsa, aptitude_data=apt, cs_data=cs,
        coding_data=coding, interview_data=interview,
        resume_data=resume, project_data=projects,
        company=company_id,
    )

    # Build skill-by-skill breakdown
    skill_breakdown = []
    for cat_id, required_score in profile.get("skill_requirements", {}).items():
        user_score = readiness_result.categories.get(cat_id)
        current = user_score.score if user_score else 0
        gap = max(0, required_score - current)
        skill_breakdown.append({
            "category": cat_id,
            "required": required_score,
            "current": round(current, 1),
            "gap": round(gap, 1),
            "met": current >= required_score,
        })

    skill_breakdown.sort(key=lambda s: s["gap"], reverse=True)

    prediction = predict_readiness_date(readiness_result.overall, company_id)

    return {
        "company": profile,
        "overall_readiness": readiness_result.overall,
        "company_readiness": readiness_result.company_score,
        "skill_breakdown": skill_breakdown,
        "recommendations": readiness_result.recommendations,
        "prediction": prediction,
    }


# ─── Company List ───
@router.get("/companies")
async def list_companies():
    """List all available companies for readiness analysis."""
    return {
        "companies": [
            {
                "id": c["id"],
                "title": c["title"],
                "icon": c["icon"],
                "tier": c["tier"],
                "color": c["color"],
                "min_readiness": c["min_readiness"],
            }
            for c in COMPANY_DEEP_PROFILES.values()
        ]
    }


# ─── Set / Get Job Target ───
@router.post("/set-target")
async def set_job_target(req: SetTargetRequest, user=Depends(get_current_user)):
    """Save your job target (role + company) to your profile."""
    if req.role_id not in ROLE_PROFILES:
        raise HTTPException(status_code=400, detail=f"Unknown role: {req.role_id}")

    update = {
        "$set": {
            "job_target": {
                "role_id": req.role_id,
                "company_id": req.company_id,
                "jd_text": req.jd_text,
                "set_at": datetime.now(timezone.utc),
            },
            "updated_at": datetime.now(timezone.utc),
        }
    }

    await users_collection().update_one({"_id": ObjectId(user["id"])}, update)

    return {
        "status": "saved",
        "target": {
            "role_id": req.role_id,
            "company_id": req.company_id,
            "role_title": ROLE_PROFILES[req.role_id]["title"],
        },
    }


@router.get("/target")
async def get_job_target(user=Depends(get_current_user)):
    """Get your saved job target."""
    uid = user["id"]
    user_doc = await users_collection().find_one({"_id": ObjectId(uid)})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    target = user_doc.get("job_target")
    if not target:
        return {"target": None, "message": "No job target set. Use POST /set-target to set one."}

    role = ROLE_PROFILES.get(target.get("role_id", ""), {})

    return {
        "target": {
            "role_id": target.get("role_id"),
            "company_id": target.get("company_id"),
            "role_title": role.get("title", "Unknown"),
            "role_icon": role.get("icon", "💼"),
            "set_at": target.get("set_at"),
        }
    }
