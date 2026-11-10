"""Service-company OA mocks — ontology-weighted, server-graded.

GET  /api/v1/service-oa/companies
POST /api/v1/service-oa/mocks/start
POST /api/v1/service-oa/mocks/grade
GET  /api/v1/service-oa/bank/stats
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from app.middleware.auth import get_current_user
from app.services import service_oa_mocks as engine

router = APIRouter(prefix="/api/v1/service-oa", tags=["service-oa-mocks"])

# In-process session store (sufficient for single-node; swap for Redis later)
_SESSIONS: Dict[str, Dict[str, Any]] = {}


class StartMockBody(BaseModel):
    company: str = Field(..., description="tcs | infosys | wipro | cognizant | accenture")
    question_count: int = Field(25, ge=5, le=40)
    seed: Optional[int] = None
    sections: Optional[List[str]] = Field(
        None,
        description="Optional filter: numerical_ability, reasoning_ability, verbal_ability, programming_logic",
    )


class GradeMockBody(BaseModel):
    session_id: str
    answers: Dict[str, int] = Field(..., description="{question_id: option_index}")
    time_spent_sec: Optional[int] = Field(None, ge=0)


@router.get("/companies")
def list_companies(user=Depends(get_current_user)):
    return {"data": engine.list_companies()}


@router.get("/bank/stats")
def bank_stats(user=Depends(get_current_user)):
    bank = engine.load_problem_bank()
    by_section: Dict[str, int] = {}
    by_topic: Dict[str, int] = {}
    for p in bank:
        by_section[p.get("section") or "?"] = by_section.get(p.get("section") or "?", 0) + 1
        by_topic[p.get("topic") or "?"] = by_topic.get(p.get("topic") or "?", 0) + 1
    return {
        "data": {
            "total": len(bank),
            "by_section": by_section,
            "topics": sorted(by_topic.keys()),
            "topic_count": len(by_topic),
        }
    }


@router.post("/mocks/start")
def start_mock(body: StartMockBody, user=Depends(get_current_user)):
    try:
        mock = engine.generate_mock(
            body.company,
            question_count=body.question_count,
            seed=body.seed,
            sections=body.sections,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not build mock: {e}")

    session_id = mock["session_id"]
    _SESSIONS[session_id] = {
        "user_id": str(getattr(user, "id", None) or user.get("id") or user.get("sub") or ""),
        "company_id": mock["company_id"],
        "answer_key": mock.pop("_answer_key"),
        "explanations": mock.pop("_explanations"),
        "topics": mock.pop("_topics"),
        "sections": mock.pop("_sections"),
        "duration_sec": mock["duration_sec"],
    }
    return {"data": mock}


@router.post("/mocks/grade")
def grade_mock(body: GradeMockBody, user=Depends(get_current_user)):
    session = _SESSIONS.get(body.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Mock session not found or expired. Start a new mock.")

    result = engine.grade_mock(
        answer_key=session["answer_key"],
        explanations=session["explanations"],
        topics=session["topics"],
        sections=session["sections"],
        answers=body.answers or {},
        company_id=session["company_id"],
        duration_sec=session["duration_sec"],
        time_spent_sec=body.time_spent_sec,
    )
    # One-time grade — drop answers from memory
    _SESSIONS.pop(body.session_id, None)
    return {"data": result}


@router.get("/mocks/preview")
def preview_weights(
    company: str = Query("tcs"),
    user=Depends(get_current_user),
):
    """Show section quota without starting a session (for UI)."""
    try:
        cid = engine.resolve_company(company)
        quota = engine._section_quota(cid, 25)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "data": {
            "company_id": cid,
            "sample_quota_25": quota,
            "section_labels": engine.SECTION_LABELS,
        }
    }
