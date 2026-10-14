from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List, Dict, Any

from app.middleware.auth import get_current_user
from app.services.company_prep_service import (
    list_company_tracks,
    get_company_track,
    most_asked_topics,
    get_most_asked_questions,
    concept_deep_dive,
    start_oa_assessment,
    submit_oa_assessment,
)

router = APIRouter(prefix="/api/v1/company-prep", tags=["company-prep"])


@router.get("/tracks")
async def tracks(user=Depends(get_current_user)):
    return {"tracks": list_company_tracks()}


@router.get("/tracks/{track_id}")
async def track_detail(track_id: str, user=Depends(get_current_user)):
    track = get_company_track(track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track


@router.get("/{company}/most-asked")
async def company_most_asked(company: str, limit: int = Query(8), user=Depends(get_current_user)):
    return {"company": company, "topics": most_asked_topics(company, limit=limit)}


@router.get("/{company}/most-asked-questions")
async def company_most_asked_questions(
    company: str,
    frequency: str = Query("high", description="high, medium, or low"),
    limit: int = Query(20, ge=1, le=100),
    user=Depends(get_current_user),
):
    questions = get_most_asked_questions(company, frequency=frequency, limit=limit)
    return {
        "company": company,
        "frequency": frequency,
        "count": len(questions),
        "questions": questions,
    }


@router.get("/{company}/concept/{topic}")
async def company_concept(company: str, topic: str, user=Depends(get_current_user)):
    data = concept_deep_dive(company, topic)
    if not data:
        raise HTTPException(status_code=404, detail="Concept not found")
    return data


@router.post("/{company}/oa/start")
async def start_oa(company: str, topic: Optional[str] = Query(None), count: int = Query(10), user=Depends(get_current_user)):
    assessment = start_oa_assessment(company, topic=topic, count=count)
    return assessment


@router.post("/{company}/oa/submit")
async def submit_oa(company: str, payload: Dict[str, Any], user=Depends(get_current_user)):
    result = await submit_oa_assessment(
        user_id=user["id"],
        company=company,
        answers=payload.get("answers", {}),
        time_spent_seconds=int(payload.get("time_spent_seconds") or 0),
    )
    return result
