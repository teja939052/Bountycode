"""
Concept cards API — Interactive learning cards for DSA topics.
"""
from fastapi import APIRouter, HTTPException
from app.services.concepts import get_concept_card, get_available_concepts

router = APIRouter(prefix="/api/concepts", tags=["concepts"])


@router.get("")
async def list_concepts():
    """Get list of all available concept cards."""
    return {"concepts": get_available_concepts()}


@router.get("/{topic}")
async def get_concept(topic: str):
    """Get a concept card for a specific topic."""
    card = get_concept_card(topic)
    if not card:
        raise HTTPException(status_code=404, detail=f"Concept card not found for: {topic}")
    return card
