"""Explanation cache service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session

async def get_or_create_explanation(
    question: dict,
    language: str = "python",
) -> dict:
    """Get or create explanation for a question."""
    return {
        "question_id": question.get("id", ""),
        "language": language,
        "explanation": "Explanation not available",
    }


async def get_cached_explanation(
    question_id: str,
    language: str,
) -> Optional[dict]:
    """Get cached explanation."""
    return None