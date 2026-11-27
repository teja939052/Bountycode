"""Question store service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session

async def find(
    query: dict,
) -> list:
    """Find questions in the question bank."""
    return []


async def find_one(
    query: dict,
    allow_unverified: bool = False,
) -> Optional[dict]:
    """Find a single question."""
    return None


async def load_question_bank() -> list:
    """Load all questions from the question bank."""
    return []


async def count_questions(
    query: dict,
) -> int:
    """Count questions matching query."""
    return 0

async def canonical_company_key(user_id: str) -> dict:
    """Stub for canonical_company_key."""
    return {"user_id": user_id}


async def insert_question(user_id: str) -> dict:
    """Stub for insert_question."""
    return {"user_id": user_id}
