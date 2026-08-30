"""Company journey API endpoints."""
from fastapi import APIRouter, Depends, HTTPException

from app.middleware.auth import get_current_user
from app.content.company_journeys import (
    get_company_journey,
    get_companies_for_role,
    get_all_companies,
    evaluate_stage,
)

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
