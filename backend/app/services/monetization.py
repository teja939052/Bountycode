from datetime import datetime, timezone, timedelta
from app.database import users_collection, usage_collection
from bson import ObjectId


# Feature tiers and limits
FREE_TIER = {
    "name": "free",
    "price": 0,
    "features": {
        "resume_bullet_improve": {"daily": 3, "monthly": 30},
        "ats_checklist": {"daily": 5, "monthly": 50},
        "resume_tailor": {"daily": 1, "monthly": 10},
        "coding_challenge": {"daily": 3, "monthly": 30},
        "interview_practice": {"daily": 1, "monthly": 10},
        "behavioral_practice": {"daily": 2, "monthly": 20},
        "concept_explanation": {"daily": 3, "monthly": 30},
        "hint_level_1": {"daily": 5, "monthly": 50},
        "hint_level_2": {"daily": 2, "monthly": 20},
        "hint_level_3": {"daily": 0, "monthly": 0},  # Pro only
        "company_specific": {"daily": 1, "monthly": 10},  # Basic companies only
        "star_evaluation": {"daily": 2, "monthly": 20},
        "missing_bullet_generator": {"daily": 0, "monthly": 0},  # Pro only
    },
    "companies": ["tcs", "infosys", "wipro"],  # Basic companies only
}

PRO_TIER = {
    "name": "pro",
    "price": 9,
    "features": {
        "resume_bullet_improve": {"daily": -1, "monthly": -1},  # Unlimited
        "ats_checklist": {"daily": -1, "monthly": -1},
        "resume_tailor": {"daily": -1, "monthly": -1},
        "coding_challenge": {"daily": -1, "monthly": -1},
        "interview_practice": {"daily": -1, "monthly": -1},
        "behavioral_practice": {"daily": -1, "monthly": -1},
        "concept_explanation": {"daily": -1, "monthly": -1},
        "hint_level_1": {"daily": -1, "monthly": -1},
        "hint_level_2": {"daily": -1, "monthly": -1},
        "hint_level_3": {"daily": -1, "monthly": -1},
        "company_specific": {"daily": -1, "monthly": -1},
        "star_evaluation": {"daily": -1, "monthly": -1},
        "missing_bullet_generator": {"daily": -1, "monthly": -1},
    },
    "companies": "all",
}

LIFETIME_TIER = {
    "name": "lifetime",
    "price": 39,
    "features": PRO_TIER["features"],  # Same as Pro
    "companies": "all",
}


async def check_feature_access(user_id: str, feature: str) -> dict:
    """Check if user can access a feature based on their tier and usage."""
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return {"allowed": False, "reason": "User not found"}

    plan = user.get("plan", "free")

    # Get tier limits
    if plan == "lifetime":
        tier = LIFETIME_TIER
    elif plan == "pro":
        tier = PRO_TIER
    else:
        tier = FREE_TIER

    # Check if feature exists in tier
    feature_limits = tier["features"].get(feature)
    if not feature_limits:
        return {"allowed": False, "reason": "Feature not available"}

    # Unlimited access
    if feature_limits["daily"] == -1:
        return {"allowed": True, "remaining": -1, "plan": plan}

    # Get current usage
    today = datetime.now(timezone.utc).date()
    month_start = today.replace(day=1)

    usage = await usage_collection.find_one({
        "user_id": user_id,
        "feature": feature,
    })

    if not usage:
        # Create usage record
        await usage_collection.insert_one({
            "user_id": user_id,
            "feature": feature,
            "daily_count": 0,
            "monthly_count": 0,
            "last_reset_daily": today,
            "last_reset_monthly": month_start,
            "created_at": datetime.now(timezone.utc),
        })
        usage = {"daily_count": 0, "monthly_count": 0}

    # Check daily limit
    daily_count = usage.get("daily_count", 0)
    if daily_count >= feature_limits["daily"]:
        return {
            "allowed": False,
            "reason": "Daily limit reached",
            "remaining": 0,
            "resets_in": "tomorrow",
            "upgrade_message": f"Upgrade to Pro for unlimited {feature.replace('_', ' ')}",
        }

    # Check monthly limit
    monthly_count = usage.get("monthly_count", 0)
    if monthly_count >= feature_limits["monthly"]:
        return {
            "allowed": False,
            "reason": "Monthly limit reached",
            "remaining": 0,
            "resets_in": "next month",
            "upgrade_message": f"Upgrade to Pro for unlimited {feature.replace('_', ' ')}",
        }

    return {
        "allowed": True,
        "remaining_daily": feature_limits["daily"] - daily_count,
        "remaining_monthly": feature_limits["monthly"] - monthly_count,
        "plan": plan,
    }


async def record_feature_usage(user_id: str, feature: str) -> dict:
    """Record feature usage and check limits."""
    today = datetime.now(timezone.utc).date()
    month_start = today.replace(day=1)

    # Get or create usage record
    usage = await usage_collection.find_one({
        "user_id": user_id,
        "feature": feature,
    })

    if not usage:
        await usage_collection.insert_one({
            "user_id": user_id,
            "feature": feature,
            "daily_count": 1,
            "monthly_count": 1,
            "last_reset_daily": today,
            "last_reset_monthly": month_start,
            "created_at": datetime.now(timezone.utc),
        })
        return {"daily_count": 1, "monthly_count": 1}

    # Reset daily count if new day
    last_reset_daily = usage.get("last_reset_daily")
    if last_reset_daily and last_reset_daily < today:
        daily_count = 1
    else:
        daily_count = usage.get("daily_count", 0) + 1

    # Reset monthly count if new month
    last_reset_monthly = usage.get("last_reset_monthly")
    if last_reset_monthly and last_reset_monthly < month_start:
        monthly_count = 1
    else:
        monthly_count = usage.get("monthly_count", 0) + 1

    await usage_collection.update_one(
        {"_id": usage["_id"]},
        {"$set": {
            "daily_count": daily_count,
            "monthly_count": monthly_count,
            "last_reset_daily": today,
            "last_reset_monthly": month_start,
        }},
    )

    return {"daily_count": daily_count, "monthly_count": monthly_count}


async def get_usage_stats(user_id: str) -> dict:
    """Get comprehensive usage stats for a user."""
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return {}

    plan = user.get("plan", "free")

    # Get all usage records
    cursor = usage_collection.find({"user_id": user_id})
    usage_records = {}
    async for doc in cursor:
        feature = doc.get("feature", "")
        usage_records[feature] = {
            "daily": doc.get("daily_count", 0),
            "monthly": doc.get("monthly_count", 0),
        }

    # Build stats
    tier = PRO_TIER if plan in ["pro", "lifetime"] else FREE_TIER
    stats = {}
    for feature, limits in tier["features"].items():
        usage = usage_records.get(feature, {"daily": 0, "monthly": 0})
        stats[feature] = {
            "daily_used": usage["daily"],
            "monthly_used": usage["monthly"],
            "daily_limit": limits["daily"] if limits["daily"] != -1 else "unlimited",
            "monthly_limit": limits["monthly"] if limits["monthly"] != -1 else "unlimited",
        }

    return {
        "plan": plan,
        "features": stats,
    }
