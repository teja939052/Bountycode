"""Problem-based Spaced Repetition Engine — SM-2-inspired scheduling for review.

Schedules problem reviews based on difficulty and correctness:
- Easy + correct  → review in 7 days
- Medium + correct → review in 3 days
- Hard + correct  → review in 1 day
- Wrong answer    → review tonight (same day)
- Wrong on review → interval halves
- Correct on review → interval doubles (max 30 days)

Cards are stored in the `srs_cards` MongoDB collection. All scheduling
logic is pure math — testable without a database.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional


# ── Initial intervals by difficulty (days) ────────────────────────────
INITIAL_INTERVALS = {
    "easy": 7,
    "medium": 3,
    "hard": 1,
}

# ── Difficulty multipliers for wrong answers ──────────────────────────
WRONG_INTERVAL = 0.0  # Review tonight (same day)
HALF_INTERVAL_FACTOR = 0.5
DOUBLE_INTERVAL_FACTOR = 2.0
MAX_INTERVAL_DAYS = 30
MIN_EASE_FACTOR = 1.3
MAX_EASE_FACTOR = 3.0
DEFAULT_EASE_FACTOR = 2.5


@dataclass
class SRSCard:
    """A single spaced repetition card for a problem."""
    user_id: str
    problem_id: str
    difficulty: str  # easy, medium, hard
    last_attempt: Optional[datetime] = None
    accuracy: float = 0.0  # Running accuracy (0.0-1.0)
    next_review: Optional[datetime] = None
    interval_days: float = 0.0
    review_count: int = 0
    ease_factor: float = DEFAULT_EASE_FACTOR
    total_attempts: int = 0
    correct_attempts: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a MongoDB-ready dict."""
        return {
            "user_id": self.user_id,
            "problem_id": self.problem_id,
            "difficulty": self.difficulty,
            "last_attempt": self.last_attempt,
            "accuracy": self.accuracy,
            "next_review": self.next_review,
            "interval_days": self.interval_days,
            "review_count": self.review_count,
            "ease_factor": self.ease_factor,
            "total_attempts": self.total_attempts,
            "correct_attempts": self.correct_attempts,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SRSCard":
        """Create an SRSCard from a MongoDB document."""
        return cls(
            user_id=data.get("user_id", ""),
            problem_id=data.get("problem_id", ""),
            difficulty=data.get("difficulty", "medium"),
            last_attempt=data.get("last_attempt"),
            accuracy=data.get("accuracy", 0.0),
            next_review=data.get("next_review"),
            interval_days=data.get("interval_days", 0.0),
            review_count=data.get("review_count", 0),
            ease_factor=data.get("ease_factor", DEFAULT_EASE_FACTOR),
            total_attempts=data.get("total_attempts", 0),
            correct_attempts=data.get("correct_attempts", 0),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )


def calculate_next_schedule(
    is_correct: bool,
    difficulty: str,
    is_review: bool,
    current_interval: float,
    ease_factor: float,
) -> tuple[float, float]:
    """Calculate the next review interval and ease factor.

    Algorithm:
    - First attempt (not a review):
        - Correct → initial interval based on difficulty
        - Wrong → review tonight (interval = 0)
    - Review attempt:
        - Correct → interval doubles (capped at MAX_INTERVAL_DAYS)
        - Wrong → interval halves

    Ease factor adjusts based on performance:
    - Correct: ease_factor += 0.1 (capped at MAX_EASE_FACTOR)
    - Wrong: ease_factor -= 0.2 (floored at MIN_EASE_FACTOR)

    Args:
        is_correct: Whether the attempt was correct.
        difficulty: Problem difficulty (easy/medium/hard).
        is_review: Whether this is a review (not first attempt).
        current_interval: Current interval in days.
        ease_factor: Current ease factor.

    Returns:
        Tuple of (new_interval_days, new_ease_factor).
    """
    if not is_correct:
        # Wrong answer → review tonight (same day)
        new_ef = max(MIN_EASE_FACTOR, ease_factor - 0.2)
        return WRONG_INTERVAL, new_ef

    if not is_review:
        # First correct solve → set initial interval
        initial = INITIAL_INTERVALS.get(difficulty, 3)
        new_ef = min(MAX_EASE_FACTOR, ease_factor + 0.1)
        return initial, new_ef

    # Review + correct → double interval
    new_interval = current_interval * DOUBLE_INTERVAL_FACTOR
    new_interval = min(MAX_INTERVAL_DAYS, new_interval)
    new_ef = min(MAX_EASE_FACTOR, ease_factor + 0.1)
    return new_interval, new_ef


def create_card(
    user_id: str,
    problem_id: str,
    difficulty: str,
    is_correct: bool,
) -> SRSCard:
    """Create a new SRS card for a problem.

    Args:
        user_id: User ID.
        problem_id: Problem ID.
        difficulty: Problem difficulty.
        is_correct: Whether the first attempt was correct.

    Returns:
        New SRSCard with scheduling set.
    """
    now = datetime.now(timezone.utc)

    if is_correct:
        interval = INITIAL_INTERVALS.get(difficulty, 3)
        next_review = now + timedelta(days=interval)
    else:
        # Review tonight: set next_review to end of today
        interval = 0
        next_review = now.replace(hour=23, minute=59, second=59, microsecond=0)

    return SRSCard(
        user_id=user_id,
        problem_id=problem_id,
        difficulty=difficulty,
        last_attempt=now,
        accuracy=1.0 if is_correct else 0.0,
        next_review=next_review,
        interval_days=interval,
        review_count=0,
        ease_factor=DEFAULT_EASE_FACTOR,
        total_attempts=1,
        correct_attempts=1 if is_correct else 0,
        created_at=now,
        updated_at=now,
    )


def update_card(card: SRSCard, is_correct: bool) -> SRSCard:
    """Update an existing card after a review attempt.

    Pure function — modifies and returns the card. Caller persists to DB.

    Args:
        card: Existing SRSCard.
        is_correct: Whether this attempt was correct.

    Returns:
        Updated SRSCard with new schedule.
    """
    now = datetime.now(timezone.utc)
    is_review = card.review_count > 0 or card.interval_days > 0

    new_interval, new_ef = calculate_next_schedule(
        is_correct=is_correct,
        difficulty=card.difficulty,
        is_review=is_review,
        current_interval=card.interval_days,
        ease_factor=card.ease_factor,
    )

    card.total_attempts += 1
    if is_correct:
        card.correct_attempts += 1

    card.accuracy = card.correct_attempts / card.total_attempts if card.total_attempts > 0 else 0.0
    card.interval_days = new_interval
    card.ease_factor = new_ef
    card.last_attempt = now
    card.updated_at = now

    if new_interval > 0:
        card.next_review = now + timedelta(days=new_interval)
    else:
        # Review tonight
        card.next_review = now.replace(hour=23, minute=59, second=59, microsecond=0)

    if is_correct:
        card.review_count += 1

    return card


def get_due_cards(cards: List[SRSCard], limit: int = 20) -> List[SRSCard]:
    """Get cards that are due for review now.

    Args:
        cards: List of all user's SRSCards.
        limit: Maximum number of cards to return.

    Returns:
        Due cards sorted by next_review (most overdue first).
    """
    now = datetime.now(timezone.utc)
    due = [c for c in cards if c.next_review and c.next_review <= now]
    due.sort(key=lambda c: c.next_review or now)
    return due[:limit]


def compute_stats(cards: List[SRSCard]) -> Dict[str, Any]:
    """Compute review statistics from all cards.

    Args:
        cards: List of all user's SRSCards.

    Returns:
        Dict with due_count, overdue_count, mastered_count, etc.
    """
    now = datetime.now(timezone.utc)
    total = len(cards)
    due_now = sum(1 for c in cards if c.next_review and c.next_review <= now)
    overdue = sum(1 for c in cards if c.next_review and c.next_review < now - timedelta(days=1))
    mastered = sum(1 for c in cards if c.interval_days >= 21)
    learning = sum(1 for c in cards if c.review_count == 0)
    reviewed = sum(1 for c in cards if c.review_count > 0)

    avg_ease = sum(c.ease_factor for c in cards) / total if total > 0 else DEFAULT_EASE_FACTOR
    avg_interval = sum(c.interval_days for c in cards) / total if total > 0 else 0
    total_reviews = sum(c.review_count for c in cards)

    # Retention rate (correct attempts / total attempts across all cards)
    total_attempts = sum(c.total_attempts for c in cards)
    total_correct = sum(c.correct_attempts for c in cards)
    retention = total_correct / total_attempts if total_attempts > 0 else 1.0

    # By difficulty
    by_difficulty = {}
    for diff in ["easy", "medium", "hard"]:
        diff_cards = [c for c in cards if c.difficulty == diff]
        if diff_cards:
            diff_due = sum(1 for c in diff_cards if c.next_review and c.next_review <= now)
            diff_mastered = sum(1 for c in diff_cards if c.interval_days >= 21)
            by_difficulty[diff] = {
                "total": len(diff_cards),
                "due": diff_due,
                "mastered": diff_mastered,
            }

    return {
        "total_cards": total,
        "due_now": due_now,
        "overdue": overdue,
        "mastered": mastered,
        "learning": learning,
        "reviewed": reviewed,
        "avg_ease_factor": round(avg_ease, 2),
        "avg_interval_days": round(avg_interval, 1),
        "total_reviews": total_reviews,
        "retention_rate": round(retention * 100, 1),
        "by_difficulty": by_difficulty,
    }


def serialize_card(card: SRSCard) -> Dict[str, Any]:
    """Serialize an SRSCard for API response.

    Args:
        card: SRSCard to serialize.

    Returns:
        Dict suitable for JSON response.
    """
    now = datetime.now(timezone.utc)
    overdue_days = 0
    if card.next_review and card.next_review < now:
        overdue_days = (now - card.next_review).days

    return {
        "problem_id": card.problem_id,
        "difficulty": card.difficulty,
        "accuracy": round(card.accuracy * 100, 1),
        "next_review": card.next_review.isoformat() if card.next_review else None,
        "interval_days": card.interval_days,
        "review_count": card.review_count,
        "ease_factor": round(card.ease_factor, 2),
        "total_attempts": card.total_attempts,
        "correct_attempts": card.correct_attempts,
        "is_due": bool(card.next_review and card.next_review <= now),
        "overdue_days": overdue_days,
    }
