"""Student evidence views — read-only projections of canonical events.

Every endpoint here is a thin wrapper over services/evidence_aggregator.py
(the single aggregation layer). No new engines, no AI, no new collections.
"""
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.middleware.auth import get_current_user
from app.services import evidence_aggregator as agg

router = APIRouter(prefix="/api/v1/evidence", tags=["evidence"])


@router.get("/heatmap")
async def heatmap(user=Depends(get_current_user)):
    bundle = await agg.collect_student_evidence(user["id"])
    return agg.pattern_heatmap(bundle)


@router.get("/failures")
async def failures(pattern_id: Optional[str] = None, user=Depends(get_current_user)):
    bundle = await agg.collect_student_evidence(user["id"])
    return agg.failure_breakdown(bundle, pattern_id)


@router.get("/time-trend")
async def time_trend(pattern_id: Optional[str] = None, user=Depends(get_current_user)):
    bundle = await agg.collect_student_evidence(user["id"])
    return agg.solve_time_trend(bundle, pattern_id)


@router.get("/company-gap")
async def company_gap(role: str = Query("sde"), company: str = Query(...),
                      user=Depends(get_current_user)):
    return await agg.company_gap(user["id"], role, company)


@router.get("/records")
async def records(user=Depends(get_current_user)):
    bundle = await agg.collect_student_evidence(user["id"])
    return agg.personal_records(bundle)


@router.get("/retention")
async def retention(user=Depends(get_current_user)):
    bundle = await agg.collect_student_evidence(user["id"])
    return agg.retention_view(bundle)


@router.get("/reattempts")
async def reattempts(user=Depends(get_current_user)):
    bundle = await agg.collect_student_evidence(user["id"])
    return agg.reattempts_due(bundle)


@router.get("/pacing")
async def pacing(target_date: str = Query(..., description="ISO target date"),
                 remaining_missions: int = Query(..., ge=0),
                 user=Depends(get_current_user)):
    bundle = await agg.collect_student_evidence(user["id"])
    result = agg.pacing(bundle, target_date, remaining_missions)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/complexity")
async def complexity(question_id: Optional[str] = None, user=Depends(get_current_user)):
    bundle = await agg.collect_student_evidence(user["id"])
    return agg.complexity_signal(bundle, question_id)


@router.get("/report")
async def report(role: str = Query("sde"), company: Optional[str] = None,
                 user=Depends(get_current_user)):
    return await agg.prep_report(user["id"], role, company)


@router.get("/my-performance")
async def my_performance(role: str = Query("sde"), company: Optional[str] = None,
                         user=Depends(get_current_user)):
    """Flagship composite: heatmap + biggest weakness + why + improvement +
    target + next action — one call for the mobile screen."""
    bundle = await agg.collect_student_evidence(user["id"])
    heat = agg.pattern_heatmap(bundle)
    fails = agg.failure_breakdown(bundle)
    trend = agg.solve_time_trend(bundle)
    recs = agg.personal_records(bundle)
    gap = await agg.company_gap(user["id"], role, company) if company else None
    weak = heat["weakest_pattern"]
    weak_detail = next((p for p in heat["patterns"] if p["pattern_id"] == weak), None)
    return {
        "heatmap": heat["patterns"],
        "biggest_weakness": weak_detail,
        "why": fails["top_failure"],
        "failure_mix": fails["percentages"],
        "improvement": trend,
        "target": gap,
        "records": recs,
        "next": heat["next_action"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
