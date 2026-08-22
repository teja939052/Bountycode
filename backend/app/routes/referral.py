from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import Optional
from app.middleware.auth import get_current_user
from app.database import users_collection, gamification_collection
from app.services.referral import (
    create_referral,
    get_referral_info,
    register_referred_user,
    get_referral_leaderboard,
    claim_referral_reward,
)
from app.services.gamification import record_practice
import secrets
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/referral", tags=["referral"])


class RegisterReferralRequest(BaseModel):
    referrer_code: str


class RewardClaimRequest(BaseModel):
    referral_number: int


class RegisterWithReferralRequest(BaseModel):
    referral_code: str


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


REFERRAL_REWARDS = {
    "referrer": {"xp": 100, "coins": 50, "badge": "referral_star"},
    "referee": {"xp": 50, "coins": 25, "badge": "newcomer"},
}
MAX_REFERRALS_PER_USER = 20


@router.post("/generate-code")
async def generate_referral_code(user=Depends(get_current_user)):
    user_doc = await users_collection.find_one({"_id": user["_id"]})
    if not user_doc:
        raise HTTPException(404, "User not found")

    code = user_doc.get("referral_code")
    if not code:
        code = "PP" + secrets.token_hex(4).upper()
        await users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"referral_code": code}},
        )

    return {
        "referral_code": code,
        "referral_url": f"https://placementpro.live/register?ref={code}",
        "total_referrals": user_doc.get("total_referrals", 0),
    }


@router.post("/register-with-referral")
async def register_with_referral(
    req: RegisterWithReferralRequest,
    user=Depends(get_current_user),
):
    if not req.referral_code or len(req.referral_code) < 4:
        raise HTTPException(400, "Invalid referral code")

    referrer = await users_collection.find_one({"referral_code": req.referral_code.upper()})
    if not referrer:
        raise HTTPException(404, "Referral code not found")

    if referrer["_id"] == user["_id"]:
        raise HTTPException(400, "Cannot refer yourself")

    existing = await users_collection.find_one({
        "referral_code": req.referral_code.upper(),
        "referrals": {"$elemMatch": {"referred_id": user["_id"]}},
    })
    if existing:
        return {"message": "Already claimed this referral", "rewards": {}}

    await users_collection.update_one(
        {"_id": referrer["_id"]},
        {"$push": {
            "referrals": {
                "referred_id": user["_id"],
                "referred_name": user.get("name", "Unknown"),
                "registered_at": datetime.now(timezone.utc),
                "claimed": True,
            }
        }, "$inc": {"total_referrals": 1}},
    )

    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"referred_by": referrer["_id"], "referral_code_used": req.referral_code.upper()}},
        upsert=True,
    )

    await gamification_collection.update_one(
        {"user_id": referrer["_id"]},
        {"$inc": {"xp": REFERRAL_REWARDS["referrer"]["xp"], "coins": REFERRAL_REWARDS["referrer"]["coins"]}},
        upsert=True,
    )
    await gamification_collection.update_one(
        {"user_id": user["id"]},
        {"$inc": {"xp": REFERRAL_REWARDS["referee"]["xp"], "coins": REFERRAL_REWARDS["referee"]["coins"]}},
        upsert=True,
    )

    await record_practice(referrer["_id"], "referral", REFERRAL_REWARDS["referrer"]["xp"], {"referral_code": req.referral_code})
    await record_practice(user["id"], "referral", REFERRAL_REWARDS["referee"]["xp"], {"referrer": referrer.get("name", "Unknown")})

    return {
        "message": "Referral accepted! Both you and your friend earned rewards.",
        "referrer_reward": REFERRAL_REWARDS["referrer"],
        "referee_reward": REFERRAL_REWARDS["referee"],
    }


@router.get("/my-referrals")
async def get_my_referrals(user=Depends(get_current_user)):
    user_doc = await users_collection.find_one({"_id": user["_id"]})
    if not user_doc:
        raise HTTPException(404, "User not found")

    referrals = user_doc.get("referrals", [])
    total = user_doc.get("total_referrals", 0)
    code = user_doc.get("referral_code", "")

    return {
        "referral_code": code,
        "total_referrals": total,
        "referrals": [
            {
                "name": r.get("referred_name", "Unknown"),
                "registered_at": r.get("registered_at"),
                "claimed": r.get("claimed", False),
            }
            for r in referrals
        ],
        "rewards_earned": {
            "xp": total * REFERRAL_REWARDS["referrer"]["xp"],
            "coins": total * REFERRAL_REWARDS["referrer"]["coins"],
        },
    }