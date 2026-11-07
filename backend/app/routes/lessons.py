"""Lesson routes — interactive coding curriculum (reuses existing infra).

Answer keys never leave the server: every response passes through
``sanitize_lesson``. Static routes are declared before ``/{lesson_id}`` so
``/progress`` and ``/next`` are not swallowed by the dynamic route.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.middleware.auth import get_current_user
from app.services.lesson_service import (
    list_lessons,
    search_lessons,
    get_public_lesson,
    get_progress,
    complete_step,
    sanitize_lesson,
    submit_exercise,
    next_lesson,
)

router = APIRouter(prefix="/api/v1/lessons", tags=["lessons"])


class LessonStart(BaseModel):
    lesson_id: str


class ExerciseSubmit(BaseModel):
    lesson_id: str
    step_id: str
    code: str = ""
    answer: Optional[str] = None


@router.get("")
async def list_all_lessons(track: Optional[str] = None):
    """List all lessons, optionally filtered by track."""
    return {"lessons": [sanitize_lesson(l) for l in list_lessons(track=track)]}


@router.get("/search")
async def search_lessons_route(q: str, track: Optional[str] = None):
    """Search lessons by title, description, or step content."""
    return {
        "lessons": [sanitize_lesson(l) for l in search_lessons(q, track=track)],
        "query": q,
    }


@router.get("/progress")
async def get_lesson_progress(user=Depends(get_current_user)):
    """Get the user's lesson progress."""
    return await get_progress(user["id"])


@router.get("/next")
async def get_next_lesson(user=Depends(get_current_user)):
    """Get the next recommended lesson."""
    progress = await get_progress(user["id"])
    current = progress.get("current_lesson")
    lesson = await next_lesson(user["id"], current)
    if not lesson:
        return {"lesson": None, "message": "All lessons complete!"}
    return {"lesson": sanitize_lesson(lesson)}


@router.get("/{lesson_id}")
async def get_lesson_route(lesson_id: str):
    """Get a single lesson with its steps (answer keys stripped)."""
    lesson = get_public_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.post("/step")
async def complete_lesson_step(req: ExerciseSubmit, user=Depends(get_current_user)):
    """Grade and complete a lesson step."""
    try:
        return await complete_step(
            user_id=user["id"],
            lesson_id=req.lesson_id,
            step_id=req.step_id,
            code=req.code,
            answer=req.answer,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/exercise")
async def submit_lesson_exercise(req: ExerciseSubmit, user=Depends(get_current_user)):
    """Submit a lesson exercise answer."""
    try:
        return await submit_exercise(
            user_id=user["id"],
            lesson_id=req.lesson_id,
            step_id=req.step_id,
            code=req.code,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
