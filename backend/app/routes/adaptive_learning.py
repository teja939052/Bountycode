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
    record_learning_activity,
    SKILL_DOMAINS,
)
from app.services.readiness_engine import compute_readiness

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
    score = await compute_readiness(user["id"], company=company)
    return {"success": True, "data": score}


@router.post("/activity")
async def record_activity(activity: dict, user=Depends(get_current_user)):
    """Accept client telemetry without allowing it to certify skill mastery.

    Mastery evidence is emitted only by server-graded lesson, quiz and
    diagnostic flows. This compatibility endpoint remains available for
    engagement telemetry, but client-supplied correctness and score fields are
    deliberately discarded.
    """
    domain_id = activity.get("domain_id")
    if not isinstance(domain_id, str) or domain_id not in SKILL_DOMAINS:
        raise HTTPException(status_code=422, detail="A valid domain_id is required.")

    safe_activity = {
        "domain_id": domain_id,
        "type": "self_reported",
        "success": False,
        "score_impact": 0,
        "source": "client_self_reported",
    }
    result = await record_learning_activity(user["id"], safe_activity)
    return {"success": True, "data": result, "mastery_updated": False}


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
