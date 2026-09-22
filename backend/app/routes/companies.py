"""Company journey API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query

from app.middleware.auth import get_current_user
from app.content.company_journeys import (
    get_company_journey,
    get_companies_for_role,
    get_all_companies,
    evaluate_stage,
)
from app.services.company_roadmap import generate_roadmap

router = APIRouter(prefix="/api/v1/companies", tags=["companies"])


@router.get("/")
async def list_companies():
    """List all available company journeys."""
    return get_all_companies()


@router.get("/{role_id}")
async def list_role_companies(role_id: str):
    """List companies available for a role."""
    return {"companies": get_companies_for_role(role_id)}


@router.get("/{role_id}/{company_id}")
async def get_journey(role_id: str, company_id: str):
    """Get a company journey for a role."""
    journey = get_company_journey(role_id, company_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")
    return journey.model_dump()


@router.post("/{role_id}/{company_id}/stage/{stage_order}/evaluate")
async def evaluate_stage_performance(
    role_id: str,
    company_id: str,
    stage_order: int,
    responses: dict,
    user=Depends(get_current_user),
):
    """Evaluate a student's performance on a company stage."""
    journey = get_company_journey(role_id, company_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")

    stage = next((s for s in journey.stages if s.order == stage_order), None)
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")

    result = await evaluate_stage(user["id"], stage, responses)

    # If failed, create a repair mission
    if not result["passed"] and result["weaknesses"]:
        result["repair_mission"] = {
            "title": f"Repair: {', '.join(result['weaknesses'])}",
            "skills": result["weaknesses"],
            "recommended_exercises": result["weaknesses"],
        }

    return result


@router.get("/roadmap")
async def get_company_roadmap(
    company: str = Query(..., description="Target company"),
    role: str = Query("sde", description="Target role"),
    timeline_days: int = Query(30, description="Timeline in days"),
    daily_minutes: int = Query(60, description="Daily study minutes"),
    user=Depends(get_current_user),
):
    """Generate a personalized company-first roadmap."""
    from app.services.readiness_engine import compute_readiness

    readiness = await compute_readiness(user["id"], company=company)
    skill_graph = {
        "categories": readiness.get("category_scores") or readiness.get("categories") or {},
    }
    roadmap = generate_roadmap(
        target_company=company,
        skill_graph=skill_graph,
        timeline_days=timeline_days,
        daily_minutes=daily_minutes,
        target_role=role,
    )
    return {
        "company": company,
        "role": role,
        "timeline_days": timeline_days,
        "daily_minutes": daily_minutes,
        "overall_readiness": roadmap.overall_readiness,
        "domain_scores": roadmap.domain_scores,
        "missions": [
            {
                "title": m.title,
                "category": m.category,
                "topic": m.topic,
                "pattern": m.pattern,
                "minutes": m.minutes,
                "question_count": m.question_count,
                "difficulty": m.difficulty,
                "company_relevance": m.company_relevance,
                "reason": m.reason,
            }
            for m in roadmap.missions
        ],
        "milestones": roadmap.milestones,
        "next_focus": roadmap.next_focus,
    }
