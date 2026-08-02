from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
from bson import ObjectId
from app.database import users_collection, referrals_collection, payments_collection
from app.config import get_settings

settings = get_settings()


async def create_referral(user_id: str) -> Dict[str, Any]:
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return {"error": "User not found"}

    referral_code = user_id[:8].upper()

    existing = await referrals_collection.find_one({"referrer_id": user_id})
    if existing:
        return {
            "referral_code": existing["referral_code"],
            "referral_link": f"{existing['referral_link']}",
            "total_referrals": existing.get("total_referrals", 0),
            "total_rewards": existing.get("total_rewards", 0),
        }

    now = datetime.now(timezone.utc)
    doc = {
        "referrer_id": user_id,
        "referrer_email": user.get("email", ""),
        "referral_code": referral_code,
        "referral_link": f"/signup?ref={referral_code}",
        "total_referrals": 0,
        "total_rewards": 0,
        "reward_type": settings.REFERRAL_REWARD_TYPE,
        "reward_value": settings.REFERRAL_REWARD_VALUE,
        "max_rewards": settings.REFERRAL_MAX_REWARDS_PER_USER,
        "created_at": now,
    }
    result = await referrals_collection.insert_one(doc)

    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"referral_code": referral_code}},
    )

    return {
        "referral_code": referral_code,
        "referral_link": f"/signup?ref={referral_code}",
        "total_referrals": 0,
        "total_rewards": 0,
    }


async def get_referral_info(user_id: str) -> Dict[str, Any]:
    ref = await referrals_collection.find_one({"referrer_id": user_id})
    if not ref:
        return await create_referral(user_id)

    return {
        "referral_code": ref["referral_code"],
        "referral_link": ref["referral_link"],
        "total_referrals": ref.get("total_referrals", 0),
        "total_rewards": ref.get("total_rewards", 0),
        "reward_type": ref.get("reward_type", settings.REFERRAL_REWARD_TYPE),
        "reward_value": ref.get("reward_value", settings.REFERRAL_REWARD_VALUE),
        "max_rewards": ref.get("max_rewards", settings.REFERRAL_MAX_REWARDS_PER_USER),
        "reward_details": ref.get("reward_details", []),
    }


async def register_referred_user(referrer_id: str, referred_user_id: str) -> Dict[str, Any]:
    referrer = await users_collection.find_one({"_id": ObjectId(referrer_id)})
    if not referrer:
        return {"error": "Referrer not found"}

    ref = await referrals_collection.find_one({"referrer_id": referrer_id})
    if not ref:
        await create_referral(referrer_id)
        ref = await referrals_collection.find_one({"referrer_id": referrer_id})

    total_referrals = ref.get("total_referrals", 0)
    max_rewards = ref.get("max_rewards", settings.REFERRAL_MAX_REWARDS_PER_USER)

    if total_referrals >= max_rewards:
        return {"error": "Maximum referral rewards already claimed"}

    now = datetime.now(timezone.utc)
    reward_detail = {
        "referred_user_id": referred_user_id,
        "referral_number": total_referrals + 1,
        "registered_at": now,
        "reward_claimed": False,
    }

    reward_details = ref.get("reward_details", [])
    reward_details.append(reward_detail)

    reward_amount = 0
    reward_type = ref.get("reward_type", settings.REFERRAL_REWARD_TYPE)
    reward_value = ref.get("reward_value", settings.REFERRAL_REWARD_VALUE)

    if reward_type == "days":
        reward_description = f"{reward_value} days free Pro access"
    elif reward_type == "percent":
        reward_description = f"{reward_value}% discount on next purchase"
        reward_amount = reward_value
    else:
        reward_description = f"Referral reward #{total_referrals + 1}"

    await referrals_collection.update_one(
        {"_id": ref["_id"]},
        {
            "$set": {
                "total_referrals": total_referrals + 1,
                "reward_details": reward_details,
            },
            "$inc": {"total_rewards": 1},
        },
    )

    await users_collection.update_one(
        {"_id": ObjectId(referred_user_id)},
        {"$set": {"referred_by": referrer_id}},
    )

    return {
        "success": True,
        "total_referrals": total_referrals + 1,
        "reward_description": reward_description,
        "reward_amount": reward_amount,
        "referral_number": total_referrals + 1,
    }


async def claim_referral_reward(referrer_id: str, referral_number: int) -> Dict[str, Any]:
    ref = await referrals_collection.find_one({"referrer_id": referrer_id})
    if not ref:
        return {"error": "No referrals found"}

    reward_details = ref.get("reward_details", [])
    if referral_number < 1 or referral_number > len(reward_details):
        return {"error": "Invalid referral number"}

    reward = reward_details[referral_number - 1]
    if reward.get("reward_claimed"):
        return {"error": "Reward already claimed"}

    user = await users_collection.find_one({"_id": ObjectId(referrer_id)})
    if not user:
        return {"error": "User not found"}

    reward_type = ref.get("reward_type", settings.REFERRAL_REWARD_TYPE)
    reward_value = ref.get("reward_value", settings.REFERRAL_REWARD_VALUE)

    now = datetime.now(timezone.utc)
    expires_at = now
    if reward_type == "days":
        expires_at = now + timedelta(days=reward_value)

    await referrals_collection.update_one(
        {"_id": ref["_id"], "reward_details._id": reward["_id"] if "_id" in reward else {"$exists": True}},
        {"$set": {f"reward_details.{referral_number - 1}.reward_claimed": True, f"reward_details.{referral_number - 1}.claimed_at": now}},
    )

    return {
        "success": True,
        "reward_type": reward_type,
        "reward_value": reward_value,
        "expires_at": expires_at.isoformat() if reward_type == "days" else None,
        "description": f"Referral reward #{referral_number} claimed",
    }


async def get_referral_leaderboard(limit: int = 10) -> list:
    cursor = referrals_collection.find({}).sort("total_referrals", -1).limit(limit)
    results = []
    async for ref in cursor:
        referrer = await users_collection.find_one({"_id": ObjectId(ref["referrer_id"])})
        results.append(
            {
                "referrer_id": ref["referrer_id"],
                "referrer_name": referrer.get("name", "Anonymous") if referrer else "Anonymous",
                "referrer_email": ref.get("referrer_email", ""),
                "referral_code": ref.get("referral_code", ""),
                "total_referrals": ref.get("total_referrals", 0),
                "total_rewards": ref.get("total_rewards", 0),
            }
        )
    return results