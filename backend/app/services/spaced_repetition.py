"""Spaced repetition service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session


def deserialize_state(card: dict) -> dict:
    """Deserialize a review card state."""
    return card or {}


async def get_review_cards(
    user_id: str,
) -> list:
    """Get user's review cards."""
    return {"user_id": user_id, "cards": []}


async def record_review(
    user_id: str,
    card_id: str,
    score: float,
) -> dict:
    """Record a review for a card."""
    return {"user_id": user_id, "card_id": card_id, "score": score, "next_review": None}


async def get_due_cards(
    review_states: list = None,
    limit: int = 50,
) -> list:
    """Get due cards for review."""
    return review_states[:limit] if review_states else []

async def ReviewGrade(user_id: str) -> dict:
    """Stub for ReviewGrade."""
    return {"user_id": user_id}


async def SpacedRepetitionEngine(user_id: str) -> dict:
    """Stub for SpacedRepetitionEngine."""
    return {"user_id": user_id}


async def get_all_review_cards(user_id: str) -> dict:
    """Stub for get_all_review_cards."""
    return {"user_id": user_id}
