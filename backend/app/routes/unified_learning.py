"""Unified Learning routes — Mimo-style learning flow API.

Flow:
  POST /api/v1/unified/start        — start a learning session for a topic
  POST /api/v1/unified/step        — get a specific step (intro/concept/exercise/quiz/next)
  POST /api/v1/unified/exercise    — submit exercise code
  POST /api/v1/unified/quiz        — submit quiz answers
  GET  /api/v1/unified/continue    — continue from last session
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

from app.middleware.auth import get_current_user
from app.services.unified_learning import UnifiedLearningService, QUIZ_QUESTIONS, MASTERY_THRESHOLD
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/unified", tags=["unified-learning"])


class StartRequest(BaseModel):
    topic: str = Field(default="arrays", min_length=1, max_length=128)


class StepRequest(BaseModel):
    step: str = Field(..., min_length=1, max_length=32)
    payload: Optional[Dict[str, Any]] = None


class ExerciseRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=120000)
    language: str = Field(default="python", min_length=2, max_length=32)
    function_name: str = Field(default="", max_length=64)


class QuizRequest(BaseModel):
    answers: Dict[str, Any] = Field(default_factory=dict)


class ContinueRequest(BaseModel):
    topic: Optional[str] = None
    company: Optional[str] = None
    role: Optional[str] = None


@router.post("/start")
async def start_learning(req: StartRequest, user=Depends(get_current_user)):
    service = UnifiedLearningService(user_id=user["id"], topic_slug=req.topic)
    intro = await service.get_learning_step("intro", {"topic": req.topic})
    return {
        "topic": req.topic,
        "flow": ["intro", "concept", "exercise", "quiz", "next"],
        "current_step": "intro",
        "data": intro,
    }


@router.post("/step")
async def get_step(req: StepRequest, user=Depends(get_current_user)):
    topic = (req.payload or {}).get("topic", "arrays")
    service = UnifiedLearningService(user_id=user["id"], topic_slug=topic)
    try:
        data = await service.get_learning_step(req.step, req.payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    next_step = _next_step(req.step)
    return {
        "topic": topic,
        "current_step": req.step,
        "next_step": next_step,
        "data": data,
    }


@router.post("/exercise")
async def submit_exercise(req: ExerciseRequest, user=Depends(get_current_user)):
    topic = req.function_name or "arrays"
    service = UnifiedLearningService(user_id=user["id"], topic_slug=topic)
    result = await service.submit_exercise(req.code, req.language, req.function_name)
    return result


@router.post("/quiz")
async def submit_quiz(req: QuizRequest, user=Depends(get_current_user)):
    topic = "arrays"
    service = UnifiedLearningService(user_id=user["id"], topic_slug=topic)
    result = await service.submit_quiz(req.answers)
    return result


@router.post("/continue")
async def continue_learning(req: ContinueRequest, user=Depends(get_current_user)):
    topic = req.topic or "arrays"
    service = UnifiedLearningService(user_id=user["id"], topic_slug=topic)
    intro = await service.get_learning_step("intro", {"topic": topic})
    mission = await service._next({
        "company": req.company,
        "role": req.role,
        "topic": topic,
    })
    try:
        await record_practice(user["id"], "practice", 5, {
            "action": "continue",
            "topic": topic,
            "company": req.company,
        })
    except Exception:
        pass
    return {
        "topic": topic,
        "flow": ["intro", "concept", "exercise", "quiz", "next"],
        "current_step": "intro",
        "data": intro,
        "next_mission": mission,
    }


def _next_step(current: str) -> Optional[str]:
    order = ["intro", "concept", "exercise", "quiz", "next"]
    try:
        idx = order.index(current)
        return order[idx + 1] if idx + 1 < len(order) else None
    except ValueError:
        return None
