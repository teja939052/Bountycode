"""
Adaptive Learning Path routes — skill assessment, weak areas, daily plans, recommendations.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from app.middleware.auth import get_current_user
from app.services.adaptive_learning import (
    assess_user_skills,
    detect_weak_areas,
    generate_daily_plan,
    generate_personalized_recommendations,
    generate_learning_path,
    calculate_readiness_score,
    record_learning_activity,
    SKILL_DOMAINS,
)

router = APIRouter(prefix="/api/v1/adaptive", tags=["adaptive"])


@router.get("/skills")
async def get_skill_assessment(user=Depends(get_current_user)):
    """Get comprehensive skill assessment across all domains."""
    result = await assess_user_skills(user["id"])
    return {"success": True, "data": result}


@router.get("/weak-areas")
async def get_weak_areas(user=Depends(get_current_user)):
    """Detect weakest skill domains with recommendations."""
    weak = await detect_weak_areas(user["id"])
    return {"success": True, "data": weak, "count": len(weak)}


@router.get("/daily-plan")
async def get_daily_plan(force: bool = Query(False, description="Force refresh the daily plan"), user=Depends(get_current_user)):
    """Get personalized daily learning plan."""
    plan = await generate_daily_plan(user["id"], force_refresh=force)
    return {"success": True, "data": plan}


@router.get("/recommendations")
async def get_recommendations(user=Depends(get_current_user)):
    """Get AI-powered personalized recommendations."""
    recs = await generate_personalized_recommendations(user["id"])
    return {"success": True, "data": recs}


@router.get("/learning-path")
async def get_learning_path(company: str = Query(None, description="Target company for interview prep"), user=Depends(get_current_user)):
    """Generate a multi-week structured learning path."""
    path = await generate_learning_path(user["id"], target_company=company)
    return {"success": True, "data": path}


@router.get("/readiness")
async def get_readiness(company: str = Query(None, description="Company-specific readiness"), user=Depends(get_current_user)):
    """Calculate interview readiness score."""
    score = await calculate_readiness_score(user["id"], company=company)
    return {"success": True, "data": score}


@router.post("/activity")
async def record_activity(activity: dict, user=Depends(get_current_user)):
    """Record a learning activity and update skill scores."""
    required = ["domain_id", "type"]
    for field in required:
        if field not in activity:
            return {"success": False, "error": f"Missing required field: {field}"}
    result = await record_learning_activity(user["id"], activity)
    return {"success": True, "data": result}


@router.get("/domains")
async def list_domains(user=Depends(get_current_user)):
    """List all skill domains with metadata."""
    domains = []
    for did, info in SKILL_DOMAINS.items():
        domains.append({
            "id": did,
            "name": info["name"],
            "emoji": info["emoji"],
            "color": info["color"],
        })
    return {"success": True, "data": domains}
