"""Referral Gamification — bonus XP for referring friends."""
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import users_collection, gamification_collection
from app.services.gamification import record_practice
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/referrals", tags=["referrals"])

REFERRAL_REWARDS = {
    "per_referral": 50,
    "referral_bonus_xp": 100,
    "max_referrals_per_month": 10,
    "bonus_tier_1": {"min_referrals": 3, "bonus_xp": 200, "badge": "Social Butterfly"},
    "bonus_tier_2": {"min_referrals": 5, "bonus_xp": 500, "badge": "Community Leader"},
    "bonus_tier_3": {"min_referrals": 10, "bonus_xp": 1000, "badge": "Referral King"},
}


@router.get("/status")
async def get_referral_status(user=Depends(get_current_user)):
    user_gam = await gamification_collection.find_one({"user_id": user["id"]})
    referrals = user_gam.get("referrals", []) if user_gam else []
    referral_code = user.get("referral_code", "")

    if not referral_code:
        import random
        import string
        referral_code = "PP" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        await users_collection.update_one(
            {"_id": ObjectId(user["id"])},
            {"$set": {"referral_code": referral_code}},
        )

    total_referrals = len(referrals)
    total_xp_earned = sum(r.get("xp_earned", 0) for r in referrals)

    tier = "none"
    tier_bonus = 0
    if total_referrals >= 10:
        tier = "tier_3"
        tier_bonus = REFERRAL_REWARDS["bonus_tier_3"]["bonus_xp"]
    elif total_referrals >= 5:
        tier = "tier_2"
        tier_bonus = REFERRAL_REWARDS["bonus_tier_2"]["bonus_xp"]
    elif total_referrals >= 3:
        tier = "tier_1"
        tier_bonus = REFERRAL_REWARDS["bonus_tier_1"]["bonus_xp"]

    return {
        "referral_code": referral_code,
        "total_referrals": total_referrals,
        "total_xp_earned": total_xp_earned,
        "tier": tier,
        "tier_bonus": tier_bonus,
        "rewards": REFERRAL_REWARDS,
        "referrals": referrals,
    }


@router.post("/refer")
async def refer_friend(req: dict, user=Depends(get_current_user)):
    referred_user_id = req.get("referred_user_id")
    if not referred_user_id:
        raise HTTPException(status_code=400, detail="referred_user_id is required")

    # Check if already referred
    user_gam = await gamification_collection.find_one({"user_id": user["id"]})
    referrals = user_gam.get("referrals", []) if user_gam else []

    if any(r["user_id"] == referred_user_id for r in referrals):
        raise HTTPException(status_code=400, detail="Already referred this user")

    xp_reward = REFERRAL_REWARDS["referral_bonus_xp"]

    referral_record = {
        "user_id": referred_user_id,
        "referred_by": user["id"],
        "xp_earned": xp_reward,
        "referral_date": datetime.now(timezone.utc),
    }

    await gamification_collection.update_one(
        {"user_id": user["id"]},
        {"$push": {"referrals": referral_record}},
        upsert=True,
    )

    # Award XP to referrer
    await gamification_collection.update_one(
        {"user_id": user["id"]},
        {"$inc": {"xp": xp_reward}},
        upsert=True,
    )

    await record_practice(user["id"], "referral", xp_reward)

    return {
        "referral_code": user.get("referral_code", ""),
        "referred_user_id": referred_user_id,
        "xp_reward": xp_reward,
        "total_referrals": len(referrals) + 1,
    }


@router.post("/claim-bonus")
async def claim_referral_bonus(user=Depends(get_current_user)):
    user_gam = await gamification_collection.find_one({"user_id": user["id"]})
    referrals = user_gam.get("referrals", []) if user_gam else []
    total_referrals = len(referrals)

    tier = "none"
    bonus_xp = 0
    if total_referrals >= 10:
        tier = "tier_3"
        bonus_xp = REFERRAL_REWARDS["bonus_tier_3"]["bonus_xp"]
    elif total_referrals >= 5:
        tier = "tier_2"
        bonus_xp = REFERRAL_REWARDS["bonus_tier_2"]["bonus_xp"]
    elif total_referrals >= 3:
        tier = "tier_1"
        bonus_xp = REFERRAL_REWARDS["bonus_tier_1"]["bonus_xp"]

    if bonus_xp == 0:
        raise HTTPException(status_code=400, detail="No bonus available yet. Refer more friends!")

    # Check if bonus already claimed
    bonus_claimed = user_gam.get("referral_bonus_claimed", []) if user_gam else []
    if tier in bonus_claimed:
        raise HTTPException(status_code=400, detail="Bonus already claimed for this tier")

    await gamification_collection.update_one(
        {"user_id": user["id"]},
        {"$inc": {"xp": bonus_xp}, "$push": {"referral_bonus_claimed": tier}},
        upsert=True,
    )

    await record_practice(user["id"], "referral_bonus", bonus_xp)

    return {
        "tier": tier,
        "bonus_xp": bonus_xp,
        "badge": REFERRAL_REWARDS[f"bonus_{tier}"]["badge"],
    }