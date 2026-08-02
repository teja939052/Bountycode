from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.middleware.auth import get_current_user
from app.services.ai_feedback import sentence_level_feedback

router = APIRouter(prefix="/api/v1/feedback", tags=["ai-feedback"])


class SentenceFeedbackRequest(BaseModel):
    answer: str
    topic: Optional[str] = ""
    ideal: Optional[str] = ""


@router.post("/sentence-level")
async def sentence_feedback(req: SentenceFeedbackRequest, user=Depends(get_current_user)):
    if not req.answer or not req.answer.strip():
        raise HTTPException(status_code=400, detail="Answer is required")

    result = await sentence_level_feedback(
        answer=req.answer,
        topic=req.topic or "",
        ideal=req.ideal or "",
    )
    return result
