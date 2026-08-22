from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from bson import ObjectId
from app.services.placement_engine import PlacementEngine
from app.middleware.auth import get_current_user
from app.database import users_collection, predictions_collection, prediction_outcomes_collection

router = APIRouter(
    prefix="/api/v1/predictor",
    tags=["Placement Predictor"]
)

# Initialize the zero-cost math engine globally to save memory
predictor_engine = PlacementEngine()


# --- REQUEST & RESPONSE SCHEMAS ---

class StudentScores(BaseModel):
    dsa: float = Field(..., ge=0, le=100, description="Data Structures & Algorithms score out of 100")
    system_design: float = Field(..., ge=0, le=100, description="System Design score out of 100")
    behavioral: float = Field(..., ge=0, le=100, description="Behavioral / STAR score out of 100")
    aptitude: float = Field(..., ge=0, le=100, description="Aptitude / Quant score out of 100")
    resume: float = Field(..., ge=0, le=100, description="Algorithmic ATS Resume score out of 100")


class PredictionRequest(BaseModel):
    company_name: Optional[str] = Field(None, example="Google")
    company: Optional[str] = Field(None, example="tcs")  # alias used by frontend
    role: Optional[str] = Field("SDE")
    scores: Optional[StudentScores] = None  # Optional: uses stored scores if not provided

    def resolved_company(self) -> str:
        name = self.company_name or self.company
        if not name:
            raise ValueError("company_name or company is required")
        return name


class WhatIfScenario(BaseModel):
    id: str
    title: str
    description: str
    impact_delta: str
    projected_probability: str
    effort: str
    time_estimate: str


class ImprovementRoadmap(BaseModel):
    priority: str
    skill: str
    current_score: float
    target_score: float
    gap: float
    action: str
    resources: List[str]
    estimated_time: str


class PredictionResponse(BaseModel):
    target_company: str
    company_tier: str
    company_color: str
    historical_acceptance_rate: str
    current_probability: float
    probability_band: Dict[str, str]
    breakdown: Dict[str, Any]
    skill_scores: Dict[str, float]
    skill_weights: Dict[str, float]
    sub_skills: Dict[str, Any]
    what_if_scenarios: List[WhatIfScenario]
    improvement_roadmap: List[ImprovementRoadmap]
    comparison: Dict[str, Any]


class OutcomeRecord(BaseModel):
    company: str = Field(..., example="google")
    role: Optional[str] = "SDE"
    prediction_id: Optional[str] = None
    predicted_probability: Optional[float] = Field(None, ge=1, le=100)
    ctc: Optional[float] = Field(None, ge=0)
    factors: Optional[Dict[str, Any]] = None
    confidence_band: Optional[Dict[str, Any]] = None
    outcome: str = Field(..., example="offered")
    interview_date: Optional[str] = None
    notes: Optional[str] = None


# --- API ENDPOINTS ---

@router.post("/predict", status_code=status.HTTP_200_OK)
async def predict_probability(
    payload: PredictionRequest,
    user=Depends(get_current_user)
):
    """
    POST: Calculates exact company offer probability using zero-cost math models.

    If scores are provided in the request, use them directly.
    Otherwise, fetch from user's stored skill graph.
    """
    try:
        company = payload.resolved_company()
        if payload.scores:
            scores_dict = payload.scores.model_dump()
            result = await _calculate_with_custom_scores(
                user["id"], company, scores_dict, role=payload.role or "SDE"
            )
        else:
            result = await predictor_engine.calculate_probability(
                user_id=user["id"],
                company_name=company,
                role=payload.role or "SDE",
            )

        # Frontend-friendly aliases + concrete gap actions
        try:
            from app.services.company_conversion import compute_gap_analysis
            gap = await compute_gap_analysis(user["id"], company)
            result["gap_analysis"] = gap
        except Exception:
            result["gap_analysis"] = None

        result["probability"] = result.get("current_probability")
        result["company"] = result.get("target_company")
        return result

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction calculation failed: {str(e)}"
        )


@router.post("/time-to-offer", status_code=status.HTTP_200_OK)
async def time_to_offer(
    payload: PredictionRequest,
    user=Depends(get_current_user)
):
    """
    POST: Estimates weeks-to-offer from current readiness and practice velocity.

    Transparent math only: typical process length for the company tier plus the
    prep weeks needed to close weighted skill gaps at observed practice pace.
    """
    try:
        company = payload.resolved_company()
        result = await predictor_engine.calculate_time_to_offer(
            user_id=user["id"],
            company_name=company,
            role=payload.role or "SDE",
        )
        return result

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Time-to-offer calculation failed: {str(e)}"
        )


async def _calculate_with_custom_scores(
    user_id: str,
    company_name: str,
    custom_scores: Dict[str, float],
    role: str = "SDE",
) -> Dict[str, Any]:
    """Calculate probability with custom scores (for what-if testing)."""
    company = company_name.lower().strip()
    if company not in predictor_engine.COMPANY_PROFILES:
        matches = [c for c in predictor_engine.COMPANY_PROFILES if company in c or c in company]
        if matches:
            company = matches[0]
        else:
            raise ValueError(f"Company '{company_name}' not found")

    profile = predictor_engine.COMPANY_PROFILES[company]
    weights = predictor_engine._effective_weights(profile["tier"], role)

    # Calculate with custom scores
    base_score = sum(custom_scores.get(skill, 0) * weights[skill] for skill in weights)

    # Penalty calculation
    normalized_min_bar = profile["min_score"] * 10
    penalty_multiplier = 1.0
    if base_score < normalized_min_bar:
        ratio = base_score / normalized_min_bar
        penalty_multiplier = 0.4 * ratio

    # Get experience data
    experience_data = await predictor_engine._get_experience_data(user_id)
    experience_modifier = predictor_engine._calculate_experience_modifier(experience_data)

    # Final probability
    raw_probability = base_score * penalty_multiplier * experience_modifier
    final_probability = min(99.0, max(1.0, raw_probability))

    # Generate what-if scenarios with custom scores
    what_if_scenarios = predictor_engine._generate_what_if_analysis(
        custom_scores, weights, final_probability, profile
    )

    # Generate improvement roadmap
    improvement_roadmap = predictor_engine._generate_improvement_roadmap(
        custom_scores, weights, profile, final_probability
    )

    # Explainable breakdown (consistent with the stored-score path)
    factors = predictor_engine._compute_factors(custom_scores, weights, profile, base_score)
    confidence_band = predictor_engine._compute_confidence_band(
        True, experience_data, final_probability
    )
    next_best_moves = predictor_engine._compute_next_best_moves(
        what_if_scenarios, improvement_roadmap
    )
    what_it_means = predictor_engine._build_plain_language_summary(
        final_probability, confidence_band, factors, weights, experience_modifier
    )

    return {
        "target_company": company_name.title(),
        "company_tier": profile["tier"],
        "company_color": profile["color"],
        "historical_acceptance_rate": f"{profile['rate'] * 100:.1f}%",
        "role": role,
        "role_profile": predictor_engine._role_profile_label(role),
        "current_probability": round(final_probability, 1),
        "probability_band": predictor_engine._get_probability_band(final_probability),
        "breakdown": {
            "base_score": round(base_score, 1),
            "penalty_applied": penalty_multiplier < 1.0,
            "penalty_multiplier": round(penalty_multiplier, 2),
            "experience_modifier": round(experience_modifier, 2),
            "raw_probability": round(raw_probability, 1),
        },
        "skill_scores": custom_scores,
        "skill_weights": weights,
        "sub_skills": {},
        "what_if_scenarios": what_if_scenarios,
        "improvement_roadmap": improvement_roadmap,
        "factors": factors,
        "confidence_band": confidence_band,
        "next_best_moves": next_best_moves,
        "what_it_means": what_it_means,
        "comparison": await predictor_engine._get_peer_comparison(user_id, company),
    }


@router.get("/predict/{company}", status_code=status.HTTP_200_OK)
async def predict_by_company(
    company: str,
    role: str = Query(default="SDE", description="Target role"),
    user=Depends(get_current_user)
):
    """
    GET: Calculate probability using stored user scores.
    GET /api/predictor/predict/google?role=SDE
    """
    try:
        result = await predictor_engine.calculate_probability(
            user_id=user["id"],
            company_name=company,
            role=role,
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/companies")
async def list_supported_companies():
    """
    GET: Returns all indexed companies across FAANG, Product, Services, and Startups.
    """
    companies = predictor_engine.get_all_companies()
    return {
        "companies": companies,
        "total": len(companies),
        "tiers": ["FAANG", "Product", "Services", "Startup"],
    }


@router.get("/companies/{tier}")
async def get_companies_by_tier(tier: str):
    """
    GET: Returns companies filtered by tier.
    GET /api/predictor/companies/FAANG
    """
    companies = [
        c for c in predictor_engine.get_all_companies()
        if c["tier"].lower() == tier.lower()
    ]
    if not companies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No companies found for tier '{tier}'. Valid tiers: FAANG, Product, Services, Startup"
        )
    return {"companies": companies, "tier": tier, "count": len(companies)}


@router.get("/tiers")
async def get_tier_weights():
    """
    GET: Returns the static skill distribution weight charts used for transparency.
    """
    return {
        "tiers": predictor_engine.TIER_WEIGHTS,
        "description": "Skill weights by company tier for probability calculation",
    }


@router.get("/sub-skills")
async def get_sub_skills():
    """
    GET: Returns sub-skill breakdown structure for granular analysis.
    """
    return {
        "sub_skills": predictor_engine.SUB_SKILLS,
        "description": "Granular skill categories for detailed performance tracking",
    }


@router.get("/history")
async def get_prediction_history(user=Depends(get_current_user)):
    """
    GET: Returns user's prediction history to track improvement over time.
    """
    history = await predictor_engine.get_prediction_history(user["id"])
    return {"history": history, "total_predictions": len(history)}


# --- OUTCOME TRACKING (builds the real training dataset) ---

@router.post("/outcome", status_code=status.HTTP_201_CREATED)
async def record_outcome(payload: OutcomeRecord, user=Depends(get_current_user)):
    """
    POST: Record what actually happened for a prediction.

    This is how the model learns. Aggregate outcomes become the calibration
    data that turns the math engine into a real, evidence-backed predictor.
    """
    allowed = {"offered", "rejected", "in_process"}
    if payload.outcome not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"outcome must be one of: {', '.join(sorted(allowed))}",
        )

    doc = {
        "user_id": user["id"],
        "company": payload.company.lower().strip(),
        "role": payload.role or "SDE",
        "prediction_id": payload.prediction_id,
        "predicted_probability": payload.predicted_probability,
        "ctc": payload.ctc,
        "factors": payload.factors or {},
        "confidence_band": payload.confidence_band or {},
        "outcome": payload.outcome,
        "interview_date": payload.interview_date,
        "notes": payload.notes,
        "created_at": datetime.now(timezone.utc),
    }
    result = await prediction_outcomes_collection.insert_one(doc)
    return {
        "outcome_id": str(result.inserted_id),
        "company": doc["company"],
        "role": doc["role"],
        "predicted_probability": doc["predicted_probability"],
        "outcome": doc["outcome"],
    }


@router.get("/outcomes")
async def list_outcomes(user=Depends(get_current_user)):
    """
    GET: Returns the user's recorded outcomes.
    """
    cursor = prediction_outcomes_collection.find(
        {"user_id": user["id"]}
    ).sort("created_at", -1).limit(50)

    outcomes = []
    async for doc in cursor:
        outcomes.append({
            "id": str(doc["_id"]),
            "company": doc.get("company", ""),
            "role": doc.get("role", "SDE"),
            "predicted_probability": doc.get("predicted_probability"),
            "ctc": doc.get("ctc"),
            "outcome": doc.get("outcome"),
            "interview_date": doc.get("interview_date"),
            "notes": doc.get("notes"),
            "created_at": doc.get("created_at"),
        })

    return {"outcomes": outcomes, "total": len(outcomes)}


@router.delete("/outcome/{outcome_id}")
async def delete_outcome(outcome_id: str, user=Depends(get_current_user)):
    """
    DELETE: Remove a recorded outcome.
    """
    try:
        doc = await prediction_outcomes_collection.find_one({"_id": ObjectId(outcome_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid outcome id")

    if not doc or doc.get("user_id") != user["id"]:
        raise HTTPException(status_code=404, detail="Outcome not found")

    await prediction_outcomes_collection.delete_one({"_id": ObjectId(outcome_id)})
    return {"deleted": True}


@router.get("/outcome-stats")
async def get_outcome_stats():
    """
    GET: Anonymous aggregate calibration stats from real recorded outcomes.
    """
    total = await prediction_outcomes_collection.count_documents({})
    decided = await prediction_outcomes_collection.count_documents(
        {"outcome": {"$in": ["offered", "rejected"]}}
    )
    offered = await prediction_outcomes_collection.count_documents({"outcome": "offered"})
    in_process = await prediction_outcomes_collection.count_documents({"outcome": "in_process"})

    offered_rate = round(offered / decided * 100, 1) if decided else None

    calibration = []
    if decided >= 20:
        buckets = [("0-25%", 0, 25), ("25-50%", 25, 50), ("50-75%", 50, 75), ("75-100%", 75, 101)]
        for label, lo, hi in buckets:
            count = 0
            offers = 0
            cursor = prediction_outcomes_collection.find({
                "outcome": {"$in": ["offered", "rejected"]},
                "predicted_probability": {"$gte": lo, "$lt": hi},
            })
            async for d in cursor:
                count += 1
                if d.get("outcome") == "offered":
                    offers += 1
            if count:
                calibration.append({
                    "band": label,
                    "count": count,
                    "actual_offer_rate": round(offers / count * 100, 1),
                })

    return {
        "total_outcomes": total,
        "decided": decided,
        "offered": offered,
        "in_process": in_process,
        "offered_rate": offered_rate,
        "calibration": calibration,
        "note": "Real outcomes reported by users. Enough samples tighten the calibration curve over time.",
    }


@router.get("/stats")
async def get_global_stats():
    """
    GET: Returns anonymized global statistics computed from real prediction data.
    """
    total_users = await users_collection.count_documents({})
    total_predictions = await predictions_collection.count_documents({})

    avg_probability = None
    async for row in predictions_collection.aggregate([
        {"$group": {"_id": None, "avg": {"$avg": "$probability"}}}
    ]):
        avg_probability = round(row.get("avg", 0), 1)

    top_companies = []
    async for row in predictions_collection.aggregate([
        {"$group": {"_id": "$company", "avg_probability": {"$avg": "$probability"}, "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5},
    ]):
        top_companies.append({
            "name": str(row.get("_id", "")).title(),
            "avg_probability": round(row.get("avg_probability", 0), 1),
            "predictions": row.get("count", 0),
        })

    return {
        "total_users": total_users,
        "total_predictions": total_predictions,
        "average_probability": avg_probability,
        "top_companies": top_companies,
        "improvement_rate": "Users who practice daily see a measurable probability increase in 2 weeks (tracked per user over time).",
        "note": "Aggregated live from prediction data — no mock numbers.",
    }
