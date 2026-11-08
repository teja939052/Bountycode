"""Placement predictor API endpoints.

Deterministic, zero-AI-cost placement probability calculator backed by
PlacementEngine. Consumes real student state (skill graph, practice history,
OA outcomes, interview outcomes) to produce explainable company match
probabilities, improvement roadmaps, and peer comparisons.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.database import users_collection
from app.middleware.auth import get_current_user
from app.services.placement_engine import PlacementEngine
from bson import ObjectId

router = APIRouter(prefix="/api/v1/predictor", tags=["predictor"])
engine = PlacementEngine()


class PredictRequest(BaseModel):
    company: str
    role: str = "SDE"


class CompanyTier(BaseModel):
    tier: str
    companies: list


@router.post("/predict")
async def predict_offer(req: PredictRequest, user=Depends(get_current_user)):
    """Calculate placement probability for a target company and role.

    Consumes: user's skill graph, practice history, OA outcomes, interview
    outcomes, and experience data. Returns probability, per-skill breakdown,
    what-if scenarios, improvement roadmap, and next-best moves.
    """
    try:
        result = await engine.calculate_probability(
            user_id=user["id"],
            company_name=req.company,
            role=req.role,
        )
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Prediction calculation failed")


@router.get("/predict/{company}")
async def predict_offer_by_company(
    company: str,
    role: str = Query("SDE", description="Target role"),
    user=Depends(get_current_user),
):
    """Calculate placement probability via GET with company in path."""
    try:
        result = await engine.calculate_probability(
            user_id=user["id"],
            company_name=company,
            role=role,
        )
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Prediction calculation failed")


@router.get("/history")
async def get_prediction_history(user=Depends(get_current_user)):
    """Get user's prediction history to track improvement over time."""
    try:
        history = await engine.get_prediction_history(user_id=user["id"])
        return {"history": history, "total": len(history)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to load prediction history")


@router.get("/companies")
async def get_supported_companies():
    """Get list of all companies supported by the predictor."""
    try:
        companies = engine.get_all_companies()
        return {"companies": companies, "total": len(companies)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to load companies")


@router.get("/companies/{tier}")
async def get_companies_by_tier(tier: str):
    """Get companies filtered by tier (FAANG, Product, Services, Startup)."""
    try:
        all_companies = engine.get_all_companies()
        filtered = [c for c in all_companies if c["tier"].lower() == tier.lower()]
        return {"tier": tier, "companies": filtered, "total": len(filtered)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to load companies by tier")


@router.get("/tiers")
async def get_tier_weights():
    """Get tier weight configurations used in probability calculation."""
    try:
        tiers = {}
        for tier_name, weights in engine.TIER_WEIGHTS.items():
            tiers[tier_name] = {
                "weights": weights,
                "companies": [
                    c["id"]
                    for c in engine.get_all_companies()
                    if c["tier"] == tier_name
                ],
            }
        return {"tiers": tiers}
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to load tier weights")


@router.get("/sub-skills")
async def get_sub_skills():
    """Get granular sub-skill breakdown for each skill category."""
    try:
        return {"sub_skills": engine.SUB_SKILLS}
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to load sub-skills")
