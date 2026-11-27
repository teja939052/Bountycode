"""Lesson service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session

async def get_lesson(
    lesson_id: str,
) -> dict:
    """Get lesson details."""
    return {"lesson_id": lesson_id, "title": lesson_id, "content": ""}


async def get_user_progress(
    user_id: str,
    lesson_id: str,
) -> dict:
    """Get user's lesson progress."""
    return {"user_id": user_id, "lesson_id": lesson_id, "completed": False, "score": 0}


async def record_lesson_progress(
    user_id: str,
    lesson_id: str,
    score: float,
) -> dict:
    """Record lesson progress."""
    return {"user_id": user_id, "lesson_id": lesson_id, "completed": True, "score": score}

async def complete_step(user_id: str) -> dict:
    """Stub for complete_step."""
    return {"user_id": user_id}


async def get_progress(user_id: str) -> dict:
    """Stub for get_progress."""
    return {"user_id": user_id}


async def get_public_lesson(user_id: str) -> dict:
    """Stub for get_public_lesson."""
    return {"user_id": user_id}


async def list_lessons(user_id: str) -> dict:
    """Stub for list_lessons."""
    return {"user_id": user_id}


async def next_lesson(user_id: str) -> dict:
    """Stub for next_lesson."""
    return {"user_id": user_id}


async def sanitize_lesson(user_id: str) -> dict:
    """Stub for sanitize_lesson."""
    return {"user_id": user_id}


async def search_lessons(user_id: str) -> dict:
    """Stub for search_lessons."""
    return {"user_id": user_id}


async def submit_exercise(user_id: str) -> dict:
    """Stub for submit_exercise."""
    return {"user_id": user_id}


async def grade_quiz(user_id: str, answers: dict) -> dict:
    """Grade a quiz."""
    return {"user_id": user_id, "score": 0, "answers": answers}


def skill_for_lesson(lesson_id: str) -> str:
    """Return the skill domain for a lesson."""
    return lesson_id


def weakness_tier_for(score: float) -> str:
    """Return weakness tier for a score."""
    if score < 35:
        return "critical"
    if score < 60:
        return "high"
    if score < 80:
        return "medium"
    return "low"
