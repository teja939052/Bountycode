from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any

from app.middleware.auth import get_current_user
from app.services.company_conversion import (
    list_mock_companies,
    start_company_mock,
    submit_mock_answer,
    complete_company_mock,
    get_mock_history,
)

router = APIRouter(prefix="/api/v1/company-mocks", tags=["company-mocks"])


@router.get("/companies")
async def list_companies(user=Depends(get_current_user)):
    """List available company mock tests with free/pro gating."""
    companies = await list_mock_companies(user)
    return {"companies": companies}


@router.get("/{company_id}/config")
async def get_company_config(company_id: str, user=Depends(get_current_user)):
    """Get mock test configuration for a company."""
    from app.services.company_conversion import MOCK_BLUEPRINTS
    company_key = company_id.lower().strip().replace("-", "_")
    if company_key not in MOCK_BLUEPRINTS:
        raise HTTPException(status_code=404, detail="Company not found.")
    bp = MOCK_BLUEPRINTS[company_key]
    return {
        "company_id": company_key,
        "name": bp["name"],
        "duration_minutes": bp["duration_minutes"],
        "passing_score": bp["passing_score"],
        "tier": bp["tier"],
        "sections": bp["sections"],
        "pro_only": bool(bp.get("pro_only", False)),
    }


@router.post("/{company_id}/start")
async def start_company_mock_route(
    company_id: str,
    payload: Dict[str, Any],
    user=Depends(get_current_user),
):
    """Start a company mock test with real questions from the verified bank."""
    try:
        result = await start_company_mock(user, company_id)
        return {
            "session_id": result["test_id"],
            "questions": result.get("questions", []),
            "config": {
                "company": result.get("company"),
                "paper_name": result.get("paper_name"),
                "duration_minutes": result.get("duration_minutes"),
                "passing_score": result.get("passing_score"),
                "total_questions": result.get("total_questions"),
                "expires_at": result.get("expires_at"),
                "started_at": result.get("started_at"),
            },
        }
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/{session_id}/status")
async def get_mock_status(session_id: str, user=Depends(get_current_user)):
    """Get the status of an in-progress mock test."""
    from app.database import company_mock_tests_collection
    from bson import ObjectId
    try:
        oid = ObjectId(session_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Invalid session ID")
    test = await company_mock_tests_collection.find_one({"_id": oid, "user_id": user["id"]})
    if not test:
        return {"session_id": session_id, "status": "not_started", "current_round": None}
    return {
        "session_id": session_id,
        "status": test.get("status", "in_progress"),
        "current_round": None,
        "company": test.get("company"),
        "paper_name": test.get("paper_name"),
        "duration_minutes": test.get("duration_minutes"),
        "started_at": test.get("started_at"),
        "expires_at": test.get("expires_at"),
    }


@router.post("/{session_id}/answer")
async def submit_answer(
    session_id: str,
    payload: Dict[str, Any],
    user=Depends(get_current_user),
):
    """Submit an answer for a specific question in an in-progress mock."""
    question_index = payload.get("question_index")
    answer = payload.get("answer", "")
    if question_index is None:
        raise HTTPException(status_code=400, detail="question_index is required")
    try:
        result = await submit_mock_answer(user["id"], session_id, int(question_index), answer)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/{session_id}/complete")
async def complete_mock(session_id: str, user=Depends(get_current_user)):
    """Complete and grade the mock test."""
    try:
        result = await complete_company_mock(user["id"], session_id)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/{session_id}/results")
async def get_mock_results(session_id: str, user=Depends(get_current_user)):
    """Get results of a completed mock test."""
    try:
        result = await complete_company_mock(user["id"], session_id)
        return result
    except ValueError:
        return {"session_id": session_id, "results": []}


@router.get("/history")
async def mock_history(user=Depends(get_current_user), limit: int = Query(20, ge=1, le=50)):
    """Get user's mock test history."""
    history = await get_mock_history(user["id"], limit=limit)
    return {"history": history}
