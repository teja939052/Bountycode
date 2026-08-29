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
from app.services.spaced_repetition import (
    SpacedRepetitionEngine,
    SRSState,
    ReviewGrade,
    get_due_cards,
    serialize_state,
)

router = APIRouter(prefix="/api/v1/srs", tags=["spaced-repetition-problems"])


class ReviewRecordRequest(BaseModel):
    """Request to record a review result for a problem."""
    problem_id: str = Field(..., min_length=1, description="Problem ID from curated_questions")
    difficulty: str = Field("medium", description="Problem difficulty: easy, medium, hard")
    is_correct: bool = Field(..., description="Whether the attempt was correct")


def _doc_to_state(doc: dict) -> SRSState:
    """Convert a MongoDB document to SRSState."""
    return SRSState(
        concept_id=doc.get("problem_id", doc.get("concept_id", "")),
        user_id=doc.get("user_id", ""),
        interval=doc.get("interval_days", doc.get("interval", 0)),
        repetitions=doc.get("review_count", doc.get("repetitions", 0)),
        ease_factor=doc.get("ease_factor", 2.5),
        total_reviews=doc.get("total_reviews", doc.get("review_count", 0)),
        lapses=doc.get("lapses", 0),
    )


@router.get("/due")
async def get_due_problems(
    limit: int = 20,
    user=Depends(get_current_user),
):
    """Get problems due for review today."""
    uid = user["id"]
    cards_col = srs_cards_collection()

    cursor = cards_col.find({"user_id": uid})
    cards = []
    async for doc in cursor:
        try:
            cards.append(_doc_to_state(doc))
        except Exception:
            continue

    due = get_due_cards(cards, limit=limit)

    return {
        "cards": [serialize_state(c) for c in due],
        "count": len(due),
        "total_cards": len(cards),
    }


@router.get("/stats")
async def get_review_stats(user=Depends(get_current_user)):
    """Get review statistics for the user."""
    uid = user["id"]
    cards_col = srs_cards_collection()

    cursor = cards_col.find({"user_id": uid})
    cards = []
    async for doc in cursor:
        try:
            cards.append(_doc_to_state(doc))
        except Exception:
            continue

    engine = SpacedRepetitionEngine()
    stats = engine.get_stats(cards)

    return stats


@router.post("/record")
async def record_review(req: ReviewRecordRequest, user=Depends(get_current_user)):
    """Record a review attempt for a problem and update the SRS schedule."""
    uid = user["id"]
    cards_col = srs_cards_collection()

    if req.difficulty not in ("easy", "medium", "hard"):
        raise HTTPException(status_code=400, detail="Difficulty must be 'easy', 'medium', or 'hard'")

    existing_doc = await cards_col.find_one({
        "user_id": uid,
        "problem_id": req.problem_id,
    })

    engine = SpacedRepetitionEngine()

    if existing_doc:
        state = _doc_to_state(existing_doc)
        is_review = state.total_reviews > 0
        grade = ReviewGrade.GOOD if req.is_correct else ReviewGrade.AGAIN
        state = engine.review(state, grade)
    else:
        is_review = False
        state = engine.create_new_card(req.problem_id, uid)
        if not req.is_correct:
            grade = ReviewGrade.AGAIN
            state = engine.review(state, grade)

    from dataclasses import asdict
    card_dict = asdict(state)
    card_dict["problem_id"] = req.problem_id
    card_dict["user_id"] = uid
    card_dict["difficulty"] = req.difficulty

    await cards_col.update_one(
        {"user_id": uid, "problem_id": req.problem_id},
        {"$set": card_dict},
        upsert=True,
    )

    serialized = serialize_state(state)
    serialized["is_review"] = is_review
    serialized["new_card"] = not existing_doc

    return serialized


@router.get("/problem/{problem_id}")
async def get_card_status(problem_id: str, user=Depends(get_current_user)):
    """Get the SRS status for a specific problem."""
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

    state = _doc_to_state(doc)
    serialized = serialize_state(state)
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
