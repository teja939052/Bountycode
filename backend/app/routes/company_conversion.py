"""
Conversion API: company mock tests, gap analysis, alumni experiences, drive alerts.
All zero-LLM — pure bank + math.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Dict, Optional

from app.middleware.auth import get_current_user
from app.services import company_conversion as conv
from app.services.usage import check_and_reset_monthly_usage
from app.services.placement_engine import PlacementEngine
from app.config import get_settings

router = APIRouter(prefix="/api/placement", tags=["placement-conversion"])
settings = get_settings()
engine = PlacementEngine()


class StartMockRequest(BaseModel):
    company: str = Field(..., min_length=2, examples=["tcs", "infosys"])


class MockAnswerRequest(BaseModel):
    test_id: str
    question_index: int = Field(..., ge=0)
    answer: str = Field(..., min_length=0)


class CompleteMockRequest(BaseModel):
    test_id: str
    answers: Optional[Dict[str, str]] = None  # index -> answer


class GapAnalysisRequest(BaseModel):
    company: str
    target_probability: float = Field(75.0, ge=10, le=99)


# ── Company mock tests ─────────────────────────────────────────────────────

@router.get("/mocks/companies")
async def list_mock_companies(user=Depends(get_current_user)):
    """List company-tagged mock papers with free/pro locks."""
    user = await check_and_reset_monthly_usage(user)
    companies = await conv.list_mock_companies(user)
    limit = getattr(settings, "FREE_TIER_COMPANY_MOCK_LIMIT", 1)
    return {
        "companies": companies,
        "free_companies": [c.title() for c in conv.free_companies()],
        "mocks_used": user.get("company_mocks_used", 0),
        "mocks_limit": "unlimited" if conv.is_premium(user) else limit,
        "is_premium": conv.is_premium(user),
    }


@router.post("/mocks/start")
async def start_mock(req: StartMockRequest, user=Depends(get_current_user)):
    """Start a timed company mock assembled from the curated question bank."""
    user = await check_and_reset_monthly_usage(user)
    try:
        result = await conv.start_company_mock(user, req.company)
        return result
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/mocks/answer")
async def answer_mock(req: MockAnswerRequest, user=Depends(get_current_user)):
    try:
        return await conv.submit_mock_answer(
            user["id"], req.test_id, req.question_index, req.answer
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/mocks/complete")
async def complete_mock(req: CompleteMockRequest, user=Depends(get_current_user)):
    """Grade mock (no LLM) + return concrete gap analysis for that company."""
    try:
        return await conv.complete_company_mock(
            user["id"], req.test_id, answers=req.answers
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/mocks/history")
async def mock_history(user=Depends(get_current_user)):
    history = await conv.get_mock_history(user["id"])
    return {"tests": history, "total": len(history)}


# ── Gap analysis + probability ─────────────────────────────────────────────

@router.post("/gap-analysis")
async def gap_analysis(req: GapAnalysisRequest, user=Depends(get_current_user)):
    """
    Concrete actions: 'Solve X more Infosys aptitude problems to move 60%→75%'.
    """
    user = await check_and_reset_monthly_usage(user)
    company = req.company.lower().strip()

    if not conv.is_premium(user) and company not in conv.free_companies():
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"Gap analysis for {company.title()} is Pro-only. Free: {', '.join(c.title() for c in conv.free_companies())}.",
        )

    try:
        return await conv.compute_gap_analysis(
            user["id"], company, target_probability=req.target_probability
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/probability/{company}")
async def company_probability(
    company: str,
    target: float = Query(75.0, ge=10, le=99),
    user=Depends(get_current_user),
):
    """
    Company-wise placement probability + concrete gap actions in one call.
    Free tier: TCS/Infosys/Wipro only, limited monthly predictions.
    """
    user = await check_and_reset_monthly_usage(user)
    company_l = company.lower().strip()

    if not conv.is_premium(user):
        if company_l not in conv.free_companies():
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=f"Probability for {company.title()} is Pro-only.",
            )
        used = user.get("predictions_used", 0)
        limit = getattr(settings, "FREE_TIER_PREDICTOR_LIMIT", 3)
        if used >= limit:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=f"Free tier: {limit} predictions/month. Upgrade for unlimited.",
            )

    try:
        prediction = await engine.calculate_probability(user["id"], company_l)
        gap = await conv.compute_gap_analysis(
            user["id"], company_l, target_probability=target
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    # Count free prediction
    if not conv.is_premium(user):
        from app.database import users_collection
        from bson import ObjectId
        await users_collection.update_one(
            {"_id": ObjectId(user["id"])},
            {"$inc": {"predictions_used": 1}},
        )

    return {
        **prediction,
        # Frontend-friendly aliases
        "probability": prediction["current_probability"],
        "company": prediction["target_company"],
        "gap_analysis": gap,
    }


# ── Dashboard insights ─────────────────────────────────────────────────────

@router.get("/dashboard-insights")
async def dashboard_insights(user=Depends(get_current_user)):
    """Weak areas, company probs, matched drives, top concrete action."""
    return await conv.get_dashboard_insights(user["id"])


# ── Alumni experiences ─────────────────────────────────────────────────────

@router.get("/alumni")
async def alumni_experiences(
    company: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=50),
    user=Depends(get_current_user),
):
    """Senior/alumni interview experiences tagged by company."""
    return await conv.list_alumni_experiences(
        company=company.lower() if company else None,
        role=role,
        limit=limit,
        user=user,
    )


# ── Placement drive alerts ─────────────────────────────────────────────────

@router.get("/drives")
async def placement_drives(
    limit: int = Query(10, ge=1, le=30),
    user=Depends(get_current_user),
):
    """
    Drives filtered to eligible + likely-to-clear companies.
    Free users see teasers for FAANG/product; full match ranking for services.
    """
    drives = await conv.match_placement_drives(user["id"], limit=limit)
    premium = conv.is_premium(user)
    free = set(conv.free_companies())

    if not premium:
        for d in drives:
            co = d["company"].lower()
            if co not in free and d.get("tier") in ("FAANG", "Product"):
                d["locked"] = True
                d["apply_url"] = None
                d["match_reasons"] = ["Upgrade to Pro to unlock FAANG/Product drive alerts"]
            else:
                d["locked"] = False
    else:
        for d in drives:
            d["locked"] = False

    return {
        "drives": drives,
        "total": len(drives),
        "is_premium": premium,
    }
