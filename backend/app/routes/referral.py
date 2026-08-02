from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.middleware.auth import get_current_user
from app.database import users_collection
from app.services.referral import (
    create_referral,
    get_referral_info,
    register_referred_user,
    get_referral_leaderboard,
    claim_referral_reward,
)

router = APIRouter(prefix="/api/v1/referral", tags=["referral"])


class RegisterReferralRequest(BaseModel):
    referrer_code: str


class RewardClaimRequest(BaseModel):
    referral_number: int


@router.get("/info")
async def referral_info(user=Depends(get_current_user)):
    return await get_referral_info(user["id"])


@router.post("/create")
async def create_referral_endpoint(user=Depends(get_current_user)):
    return await create_referral(user["id"])


@router.post("/register")
async def register_referral_endpoint(req: RegisterReferralRequest):
    if not req.referrer_code:
        raise HTTPException(status_code=400, detail="Referral code is required")
    user = await users_collection.find_one({"referral_code": req.referrer_code.upper()})
    if not user:
        raise HTTPException(status_code=404, detail="Referral code not found")
    return await register_referred_user(user["_id"], "pending_user")


@router.get("/leaderboard")
async def leaderboard(limit: int = 10):
    return await get_referral_leaderboard(limit)


@router.post("/claim-reward")
async def claim_reward(req: RewardClaimRequest, user=Depends(get_current_user)):
    return await claim_referral_reward(user["id"], req.referral_number)