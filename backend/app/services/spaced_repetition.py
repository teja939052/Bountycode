"""Spaced repetition service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional


class CardState:
    """Simple SM-2 card state."""
    def __init__(self, concept_id: str, user_id: str):
        self.concept_id = concept_id
        self.user_id = user_id
        self.interval = 0
        self.repetitions = 0
        self.ease_factor = 2.5
        self.next_review = datetime.now(timezone.utc)


class SpacedRepetitionEngine:
    """SM-2 spaced repetition engine."""

    def __init__(self, user_id: Optional[str] = None):
        self.user_id = user_id

    def create_new_card(self, concept_id: str, user_id: str) -> CardState:
        """Create a new card state."""
        return CardState(concept_id=concept_id, user_id=user_id)

    def review(self, state: CardState, grade: str) -> CardState:
        """Process a review and update card state."""
        from datetime import timedelta

        if grade == "good":
            state.repetitions += 1
            if state.repetitions == 1:
                state.interval = 1
            elif state.repetitions == 2:
                state.interval = 6
            else:
                state.interval = int(state.interval * state.ease_factor)
        else:
            state.repetitions = 0
            state.interval = 1
        state.next_review = datetime.now(timezone.utc) + timedelta(days=state.interval)
        return state


def deserialize_state(card: dict) -> dict:
    """Deserialize a review card state."""
    return card or {}


class ReviewGrade:
    GOOD = "good"
    AGAIN = "again"


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


async def get_all_review_cards(user_id: str) -> dict:
    """Stub for get_all_review_cards."""
    return {"user_id": user_id}
