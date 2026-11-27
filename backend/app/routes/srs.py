"""SRS routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session

router = APIRouter(prefix="/api/v1/srs", tags=["srs"])


@router.get("/cards")
async def list_review_cards(user=Depends(get_current_user)):
    """List review cards for user."""
    return {"cards": []}


@router.post("/cards/{card_id}/review")
async def review_card(
    card_id: str,
    score: int,
    user=Depends(get_current_user),
):
    """Record a review for a card."""
    return {"card_id": card_id, "score": score, "next_review": None}