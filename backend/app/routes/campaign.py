"""Campaign routes — company battlefield, pattern mastery, today recommendations.

Mounts under ``/api/v1/campaign``. All endpoints require authentication.

Reuses existing services:
- ``campaign_service`` for battlefield/recommendation logic
- ``study_engine`` for daily plan context
- ``question_store`` for question counts
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from app.middleware.auth import get_current_user
from app.services.campaign_service import (
    get_campaign_state,
    set_campaign_state,
    get_battlefield,
    get_today_recommendations,
    get_pattern_detail,
    record_mission_evidence,
)
from app.services.study_engine import get_today as study_get_today
from app.services.pattern_pack_service import get_pattern_pack, list_pattern_packs

router = APIRouter(prefix="/api/v1/campaign", tags=["campaign"])


# ---------------------------------------------------------------------------
# Request/Response models
# ---------------------------------------------------------------------------


class CampaignSelectRequest(BaseModel):
    company: str
    role: str = "Software Developer"
    assessment_date: str = ""


class MissionEvidenceRequest(BaseModel):
    pattern_id: str
    evidence: dict


# ---------------------------------------------------------------------------
# Campaign target
# ---------------------------------------------------------------------------


@router.get("/state")
async def get_state(user=Depends(get_current_user)):
    """Get the current campaign target."""
    return await get_campaign_state(user["id"])


@router.post("/select")
async def select_campaign(req: CampaignSelectRequest, user=Depends(get_current_user)):
    """Set or update the user's campaign target (company, role, date)."""
    if not req.company:
        raise HTTPException(status_code=400, detail="company is required")
    state = await set_campaign_state(
        user["id"],
        req.company,
        req.role or "Software Developer",
        req.assessment_date or "",
    )
    return {"success": True, "campaign": state}


# ---------------------------------------------------------------------------
# Battlefield
# ---------------------------------------------------------------------------


@router.get("/battlefield")
async def get_battlefield(company: str = Query(""), user=Depends(get_current_user)):
    """Return the full battlefield for the user's campaign company.

    Query params:
        company: target company slug (e.g. tcs, infosys). Falls back to
                 the user's saved target_company.
    """
    company = company or ""
    if not company:
        state = await get_campaign_state(user["id"])
        company = state.get("company", "") or "tcs"
    return await get_battlefield(user["id"], company)


# ---------------------------------------------------------------------------
# Today
# ---------------------------------------------------------------------------


@router.get("/today")
async def get_today(company: str = Query(""), user=Depends(get_current_user)):
    """Return the top 3 recommendations for today.

    This is the new canonical "what should I do now" endpoint. It replaces
    the generic study/today response with a company-battlefield-aware plan.
    """
    company = company or ""
    if not company:
        state = await get_campaign_state(user["id"])
        company = state.get("company", "") or "tcs"
    return await get_today_recommendations(user["id"], company)


# ---------------------------------------------------------------------------
# Pattern detail
# ---------------------------------------------------------------------------


@router.get("/patterns/{pattern_id}")
async def get_pattern(pattern_id: str, company: str = Query(""), user=Depends(get_current_user)):
    """Get full detail for a pattern: mastery, diagnosis, question count, mission slug."""
    company = company or ""
    if not company:
        state = await get_campaign_state(user["id"])
        company = state.get("company", "") or "tcs"
    return await get_pattern_detail(user["id"], pattern_id, company)


# ---------------------------------------------------------------------------
# Mission evidence
# ---------------------------------------------------------------------------


@router.post("/missions/evidence")
async def submit_evidence(req: MissionEvidenceRequest, user=Depends(get_current_user)):
    """Record mission completion evidence and update mastery/diamonds."""
    result = await record_mission_evidence(user["id"], req.pattern_id, req.evidence)
    return result


@router.get("/patterns/{pattern_id}/pack")
async def get_pattern_pack(pattern_id: str, company: str = Query(""), user=Depends(get_current_user)):
    """Return the authored Pattern Pack for a pattern.

    Falls back to an empty skeleton when no pack is authored yet.
    """
    pack = get_pattern_pack(pattern_id)
    return {"pattern_id": pattern_id, "pack": pack}


@router.get("/patterns/packs")
async def list_packs(user=Depends(get_current_user)):
    """List all authored pattern packs."""
    packs = list_pattern_packs()
    return {"count": len(packs), "packs": list(packs.keys())}


# ---------------------------------------------------------------------------
# Legacy compatibility: redirect old study/today queries through campaign
# ---------------------------------------------------------------------------


@router.get("/plan")
async def get_plan(company: str = Query(""), user=Depends(get_current_user)):
    """Return the full study plan in campaign shape (backward compat)."""
    company = company or ""
    if not company:
        state = await get_campaign_state(user["id"])
        company = state.get("company", "") or "tcs"
    try:
        plan = await study_get_today(user["id"], company=company)
    except Exception:
        plan = {}
    return plan


@router.get("/blueprint/{company}")
async def get_blueprint(company: str, user=Depends(get_current_user)):
    """Return the exam blueprint for a company."""
    from app.services.pattern_pack_service import get_company_blueprint
    blueprint = get_company_blueprint(company)
    if not blueprint:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    return blueprint
