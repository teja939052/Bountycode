"""TCS NQT routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session

router = APIRouter(prefix="/api/v1/tcs-nqt", tags=["tcs-nqt"])


@router.get("/questions")
async def list_tcs_nqt_questions(user=Depends(get_current_user)):
    """List TCS NQT questions."""
    return {"questions": []}


@router.post("/questions/{question_id}/submit")
async def submit_tcs_nqt_answer(
    question_id: str,
    answer: str,
    user=Depends(get_current_user),
):
    """Submit answer for TCS NQT question."""
    return {"question_id": question_id, "answer": answer, "status": "submitted"}