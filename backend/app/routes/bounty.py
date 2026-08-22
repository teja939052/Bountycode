"""Bounty Card API routes."""
from fastapi import APIRouter, Depends, HTTPException, Query
from app.middleware.auth import get_current_user
from app.services.bounty import generate_bounty_card, generate_leaderboard, get_bounty_tier, BOUNTY_TIERS

router = APIRouter(prefix="/api/v1/bounty", tags=["Bounty Card"])


@router.get("/card")
async def my_bounty_card(user=Depends(get_current_user)):
    return await generate_bounty_card(user["id"])


@router.get("/card/{target_user_id}")
async def user_bounty_card(target_user_id: str):
    return await generate_bounty_card(target_user_id)


@router.get("/leaderboard")
async def bounty_leaderboard(limit: int = Query(20, ge=1, le=100)):
    return await generate_leaderboard(limit)


@router.get("/tiers")
async def bounty_tiers():
    return {"tiers": BOUNTY_TIERS}
