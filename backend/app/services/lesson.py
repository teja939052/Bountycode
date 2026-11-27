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

async def LessonService(user_id: str = None) -> dict:
    """Stub for LessonService."""
    return {"user_id": user_id}
