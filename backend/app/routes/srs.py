"""Problem-based Spaced Repetition — review scheduling for problem retention.

Provides GET /api/v1/srs/due for problems due today,
GET /api/v1/srs/stats for review statistics, and
POST /api/v1/srs/record to schedule a review after solving a problem.
Uses the srs_cards collection for scheduling state.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from app.middleware.auth import get_current_user
from app.database import (
    srs_cards_collection,
    solved_problems_collection,
)
from app.services.srs_engine import (
    create_card,
    update_card,
    get_due_cards,
    compute_stats,
    serialize_card,
    SRSCard,
)

router = APIRouter(prefix="/api/v1/srs", tags=["spaced-repetition-problems"])


class ReviewRecordRequest(BaseModel):
    """Request to record a review result for a problem."""
    problem_id: str = Field(..., min_length=1, description="Problem ID from curated_questions")
    difficulty: str = Field("medium", description="Problem difficulty: easy, medium, hard")
    is_correct: bool = Field(..., description="Whether the attempt was correct")


@router.get("/due")
async def get_due_problems(
    limit: int = 20,
    user=Depends(get_current_user),
):
    """Get problems due for review today.

    Returns the user's SRS cards that are scheduled for review now or are
    overdue, sorted by most overdue first. Each card includes the problem_id,
    difficulty, interval, and scheduling metadata.
    """
    uid = user["id"]
    cards_col = srs_cards_collection()

    cursor = cards_col.find({"user_id": uid})
    cards = []
    async for doc in cursor:
        cards.append(SRSCard.from_dict(doc))

    due = get_due_cards(cards, limit=limit)

    return {
        "cards": [serialize_card(c) for c in due],
        "count": len(due),
        "total_cards": len(cards),
    }


@router.get("/stats")
async def get_review_stats(user=Depends(get_current_user)):
    """Get review statistics for the user.

    Returns counts for due, overdue, mastered, and learning cards,
    plus average ease factor, retention rate, and per-difficulty breakdown.
    """
    uid = user["id"]
    cards_col = srs_cards_collection()

    cursor = cards_col.find({"user_id": uid})
    cards = []
    async for doc in cursor:
        cards.append(SRSCard.from_dict(doc))

    stats = compute_stats(cards)

    return stats


@router.post("/record")
async def record_review(req: ReviewRecordRequest, user=Depends(get_current_user)):
    """Record a review attempt for a problem and update the SRS schedule.

    Creates a new card if this is the first time, or updates the existing
    card's schedule based on the SM-2-inspired algorithm:
    - Correct → interval doubles (or sets initial interval)
    - Wrong → interval resets to tonight
    - Ease factor adjusts based on performance

    Returns the updated card with the next review date.
    """
    uid = user["id"]
    cards_col = srs_cards_collection()

    # Validate difficulty
    if req.difficulty not in ("easy", "medium", "hard"):
        raise HTTPException(status_code=400, detail="Difficulty must be 'easy', 'medium', or 'hard'")

    # Find existing card
    existing_doc = await cards_col.find_one({
        "user_id": uid,
        "problem_id": req.problem_id,
    })

    if existing_doc:
        card = SRSCard.from_dict(existing_doc)
        is_review = card.review_count > 0 or card.total_attempts > 0
        card = update_card(card, req.correct)
    else:
        is_review = False
        card = create_card(
            user_id=uid,
            problem_id=req.problem_id,
            difficulty=req.difficulty,
            is_correct=req.correct,
        )

    # Persist to database
    card_dict = card.to_dict()
    await cards_col.update_one(
        {"user_id": uid, "problem_id": req.problem_id},
        {"$set": card_dict},
        upsert=True,
    )

    serialized = serialize_card(card)
    serialized["is_review"] = is_review
    serialized["new_card"] = not existing_doc

    return serialized


@router.get("/problem/{problem_id}")
async def get_card_status(problem_id: str, user=Depends(get_current_user)):
    """Get the SRS status for a specific problem.

    Returns the card's scheduling state, or null values if no card exists yet.
    """
    uid = user["id"]
    cards_col = srs_cards_collection()

    doc = await cards_col.find_one({
        "user_id": uid,
        "problem_id": problem_id,
    })

    if not doc:
        return {
            "problem_id": problem_id,
            "has_card": False,
            "is_due": True,
            "interval_days": 0,
            "review_count": 0,
        }

    card = SRSCard.from_dict(doc)
    serialized = serialize_card(card)
    serialized["has_card"] = True

    return serialized


@router.delete("/problem/{problem_id}")
async def remove_card(problem_id: str, user=Depends(get_current_user)):
    """Remove an SRS card for a problem (reset its review schedule)."""
    uid = user["id"]
    cards_col = srs_cards_collection()

    result = await cards_col.delete_one({
        "user_id": uid,
        "problem_id": problem_id,
    })

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="No SRS card found for this problem")

    return {"message": "Card removed", "problem_id": problem_id}
