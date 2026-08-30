"""Study Engine extended endpoints."""
from fastapi import APIRouter, Depends

from app.middleware.auth import get_current_user
from app.services.study_engine import generate_30_day_plan, diagnose_mock_oa

router = APIRouter(prefix="/api/v1/study", tags=["study-engine"])


@router.get("/30-day-plan")
async def get_30_day_plan(role: str, company: str = "", user=Depends(get_current_user)):
    """Generate a 30-day preparation plan for a role/company."""
    plan = await generate_30_day_plan(user["id"], role, company)
    return {"success": True, "plan": plan}


@router.post("/mock-oa/diagnose")
async def post_mock_oa_diagnosis(responses: dict, user=Depends(get_current_user)):
    """Analyze Mock OA results and generate diagnostic report."""
    diagnosis = await diagnose_mock_oa(user["id"], responses)
    return {"success": True, "diagnosis": diagnosis}
