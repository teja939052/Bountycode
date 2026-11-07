from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.middleware.auth import get_current_user
from app.services.role_engine.profiles import door_roles

router = APIRouter(prefix="/api/v1/onboarding/diagnostic", tags=["onboarding-diagnostic"])

VALID_ROLES = {r["key"] for r in door_roles()}


class DiagnosticCompleteRequest(BaseModel):
    role: str = Field(..., description="Door-1 target role key")
    answers: Dict[str, Any] = Field(default_factory=dict, description="question_id -> answer")


@router.get("/start")
async def start_diagnostic(role: str, user=Depends(get_current_user)):
    """Return the role's real interactive mini-diagnostic (gradable MCQ steps)."""
    if role not in VALID_ROLES:
        raise HTTPException(status_code=400, detail="Unknown target role")

    from app.services.job_diagnostic import get_diagnostic_questions

    return get_diagnostic_questions(role)


@router.post("/complete")
async def complete_diagnostic(req: DiagnosticCompleteRequest, user=Depends(get_current_user)):
    """Grade answers, seed the skill graph, compute readiness, build the path,
    and return first 3 missions."""
    if req.role not in VALID_ROLES:
        raise HTTPException(status_code=400, detail="Unknown target role")

    from app.services.job_diagnostic import run_job_diagnostic

    result = await run_job_diagnostic(user["id"], req.role, req.answers)
    return result
