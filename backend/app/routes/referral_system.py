"""Referral System — invite friends, earn XP and coins.
Reuses users_collection for referral tracking.
Bounded: 1 referral record per user pair (referral_code is unique)."""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Body
from app.middleware.auth import get_current_user
from app.database import users_collection, gamification_collection
from app.services.gamification import record_practice
import secrets
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/referral", tags=["referral"])

# ┃ Referral rewards config
REFERRAL_REWARDS = {
    "referrer": {"xp": 100, "coins": 50, "badge": "referral_star"},
    "referee": {"xp": 50, "coins": 25, "badge": "newcomer"},
}

MAX_REFERRALS_PER_USER = 20


@router.post("/generate-code")
async def generate_referral_code(user=Depends(get_current_user)):
    """Generate or return existing referral code."""
    user_doc = await users_collection().find_one({"_id": user["_id"]})
    if not user_doc:
        raise HTTPException(404, "User not found")

    code = user_doc.get("referral_code")
    if not code:
        code = "PP" + secrets.token_hex(4).upper()
        await users_collection().update_one(
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
    referral_code: str = Body(..., embed=True),
    user=Depends(get_current_user),
):
    """Register using a referral code. Both referrer and referee get rewards."""
    if not referral_code or len(referral_code) < 4:
        raise HTTPException(400, "Invalid referral code")

    # Find referrer
    referrer = await users_collection().find_one({"referral_code": referral_code.upper()})
    if not referrer:
        raise HTTPException(404, "Referral code not found")

    if referrer["_id"] == user["_id"]:
        raise HTTPException(400, "Cannot refer yourself")

    # Check if already referred
    existing = await users_collection().find_one({
        "referral_code": referral_code.upper(),
        "referrals": {"$elemMatch": {"referred_id": user["_id"]}},
    })
    if existing:
        return {"message": "Already claimed this referral", "rewards": {}}

    # Record the referral
    await users_collection().update_one(
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

    await users_collection().update_one(
        {"_id": user["_id"]},
        {"$set": {"referred_by": referrer["_id"], "referral_code_used": referral_code.upper()}},
        upsert=True,
    )

    # Award rewards
    await gamification_collection().update_one(
        {"user_id": referrer["_id"]},
        {"$inc": {"xp": REFERRAL_REWARDS["referrer"]["xp"], "coins": REFERRAL_REWARDS["referrer"]["coins"]}},
        upsert=True,
    )
    await gamification_collection().update_one(
        {"user_id": user["_id"]},
        {"$inc": {"xp": REFERRAL_REWARDS["referee"]["xp"], "coins": REFERRAL_REWARDS["referee"]["coins"]}},
        upsert=True,
    )

    await record_practice(referrer["_id"], "referral", REFERRAL_REWARDS["referrer"]["xp"], {"referral_code": referral_code})
    await record_practice(user["_id"], "referral", REFERRAL_REWARDS["referee"]["xp"], {"referrer": referrer.get("name", "Unknown")})

    return {
        "message": "Referral accepted! Both you and your friend earned rewards.",
        "referrer_reward": REFERRAL_REWARDS["referrer"],
        "referee_reward": REFERRAL_REWARDS["referee"],
    }


@router.get("/my-referrals")
async def get_my_referrals(user=Depends(get_current_user)):
    """Get all referrals made by current user."""
    user_doc = await users_collection().find_one({"_id": user["_id"]})
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


@router.get("/leaderboard")
async def get_referral_leaderboard(limit: int = 20):
    """Top referrers by total referrals."""
    cursor = (
        users_collection()
        .find({"total_referrals": {"$gt": 0}})
        .sort("total_referrals", -1)
        .limit(min(max(limit, 1), 100))
    )
    entries = []
    async for doc in cursor:
        entries.append({
            "user_id": doc.get("_id"),
            "name": doc.get("name", "Anonymous"),
            "total_referrals": doc.get("total_referrals", 0),
            "referral_code": doc.get("referral_code", ""),
        })
    return {"leaderboard": entries}
