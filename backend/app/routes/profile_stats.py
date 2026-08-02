from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.services.profile_stats import get_profile_stats, update_integrations
from app.database import users_collection, skill_graph_collection, gamification_collection, interviews_collection, resumes_collection, aptitude_collection

router = APIRouter(prefix="/api/v1/profile", tags=["profile"])


class IntegrationUpdate(BaseModel):
    platform: str
    username: str


@router.get("/stats")
async def get_stats(user=Depends(get_current_user)):
    return await get_profile_stats(user["id"])


@router.put("/integrations")
async def update_integration(payload: IntegrationUpdate, user=Depends(get_current_user)):
    platform = payload.platform.lower()
    if platform not in ("github", "leetcode"):
        raise HTTPException(status_code=400, detail="Supported platforms: github, leetcode")
    return await update_integrations(user["id"], platform, payload.username)


@router.get("/readiness-score")
async def readiness_score(user=Depends(get_current_user)):
    uid = user["id"]
    user_doc = await users_collection.find_one({"_id": ObjectId(uid)})

    skill_graph = await skill_graph_collection.find_one({"user_id": uid}) or {}
    categories = skill_graph.get("categories", {})

    def _get_score(cat):
        c = categories.get(cat, {})
        return c.get("score", 0) if isinstance(c, dict) else (c or 0)

    dsa_score = _get_score("dsa")
    aptitude_score = _get_score("aptitude")
    behavioral_score = _get_score("behavioral")
    resume_score = _get_score("resume")
    interview_score = _get_score("system_design")

    total_interviews = await interviews_collection.count_documents({"user_id": uid})
    interview_comp = min(interview_score * 0.2 + (total_interviews / 10) * 20, 20)
    dsa_comp = dsa_score * 0.4
    aptitude_comp = aptitude_score * 0.2
    behavioral_comp = behavioral_score * 0.1

    resume_doc = await resumes_collection.find_one({"user_id": uid}, sort=[("created_at", -1)])
    resume_ats = resume_doc.get("ats_score", 0) if resume_doc else 0
    resume_comp = resume_ats * 0.1

    score = min(round(dsa_comp + aptitude_comp + interview_comp + behavioral_comp + resume_comp), 100)

    gam = await gamification_collection.find_one({"user_id": uid}) or {}
    level = gam.get("level", 1)
    next_milestone = f"Reach level {((level // 5) + 1) * 5}" if level < 100 else "Max level reached"

    return {
        "score": score,
        "breakdown": {
            "dsa": round(dsa_comp, 1),
            "aptitude": round(aptitude_comp, 1),
            "interview": round(interview_comp, 1),
            "behavioral": round(behavioral_comp, 1),
            "resume": round(resume_comp, 1),
        },
        "next_milestone": next_milestone,
    }


@router.get("/company-matches")
async def company_matches(user=Depends(get_current_user)):
    uid = user["id"]
    user_doc = await users_collection.find_one({"_id": ObjectId(uid)})
    onboarding = user_doc.get("onboarding", {}) if user_doc else {}
    target_companies = onboarding.get("target_companies", [])

    skill_graph = await skill_graph_collection.find_one({"user_id": uid}) or {}
    categories = skill_graph.get("categories", {})

    def _get_score(cat):
        c = categories.get(cat, {})
        return c.get("score", 0) if isinstance(c, dict) else (c or 0)

    dsa = _get_score("dsa")
    sysd = _get_score("system_design")
    beh = _get_score("behavioral")
    apt = _get_score("aptitude")
    overall = (dsa + sysd + beh + apt) / 4

    company_data = {
        "Google": {"min_dsa": 7, "tags": ["algorithms", "system_design"], "priority": "dsa"},
        "Amazon": {"min_dsa": 6, "tags": ["leadership", "system_design"], "priority": "behavioral"},
        "Meta": {"min_dsa": 7, "tags": ["algorithms", "system_design"], "priority": "dsa"},
        "Apple": {"min_dsa": 6, "tags": ["algorithms", "system_design"], "priority": "dsa"},
        "Netflix": {"min_dsa": 6, "tags": ["system_design", "culture"], "priority": "system_design"},
        "TCS": {"min_aptitude": 5, "tags": ["aptitude", "verbal"], "priority": "aptitude"},
        "Infosys": {"min_aptitude": 5, "tags": ["aptitude", "logical"], "priority": "aptitude"},
        "Wipro": {"min_aptitude": 5, "tags": ["aptitude", "verbal"], "priority": "aptitude"},
        "Accenture": {"min_aptitude": 4, "tags": ["aptitude", "analytical"], "priority": "aptitude"},
        "Uber": {"min_dsa": 6, "tags": ["algorithms", "system_design"], "priority": "dsa"},
        "Flipkart": {"min_dsa": 6, "tags": ["algorithms", "system_design"], "priority": "dsa"},
        "Zoho": {"min_dsa": 5, "tags": ["algorithms", "aptitude"], "priority": "dsa"},
        "Goldman Sachs": {"min_dsa": 7, "tags": ["algorithms", "numerical"], "priority": "dsa"},
        "JPMorgan": {"min_dsa": 6, "tags": ["algorithms", "numerical"], "priority": "dsa"},
    }

    candidates = target_companies if target_companies else list(company_data.keys())[:6]
    matches = []

    for company in candidates:
        info = company_data.get(company, {"min_dsa": 5, "tags": ["general"], "priority": "dsa"})
        required = info.get("min_dsa", 5)
        match_pct = min(100, round((overall / max(required, 1)) * 60 + min(dsa, 10) * 4))
        missing = []
        if dsa < required:
            missing.append(f"DSA needs {required}/10 (current: {dsa})")
        if info["priority"] == "system_design" and sysd < 5:
            missing.append(f"System design needs improvement (current: {sysd})")
        if info["priority"] == "behavioral" and beh < 5:
            missing.append(f"Behavioral needs improvement (current: {beh})")
        if info["priority"] == "aptitude" and apt < 5:
            missing.append(f"Aptitude needs improvement (current: {apt})")
        recommended_focus = info["priority"]
        matches.append({
            "company": company,
            "match_percent": min(match_pct, 100),
            "missing_skills": missing,
            "recommended_focus": recommended_focus,
        })

    matches.sort(key=lambda m: m["match_percent"], reverse=True)
    return {"matches": matches[:5]}
