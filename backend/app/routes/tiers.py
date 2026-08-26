from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from app.middleware.auth import get_current_user, require_plan, _admin_emails
from app.config import get_settings
from app.database import users_collection
from bson import ObjectId
from app.services.usage import check_and_reset_monthly_usage, get_usage_stats

router = APIRouter(prefix="/api/v1/tiers", tags=["tiers"])
settings = get_settings()

TIER_LIMITS = {
    "free": {
        "interviews_per_month": 3,
        "resume_reviews_per_month": 3,
        "aptitude_tests_per_month": 5,
        "cover_letters_per_month": 3,
        "daily_compiler_runs": 20,
        "daily_ai_questions": 5,
        "problems_per_day": 10,
        "ai_mistakes_per_day": 3,
        "mock_interviews_per_month": 1,
        "learning_modules": "basic",
        "company_tags_visible": 1,
        "leaderboard_access": False,
        "community_access": True,
    },
    "pro": {
        "interviews_per_month": 999,
        "resume_reviews_per_month": 999,
        "aptitude_tests_per_month": 999,
        "cover_letters_per_month": 999,
        "daily_compiler_runs": 999,
        "daily_ai_questions": 999,
        "problems_per_day": 999,
        "ai_mistakes_per_day": 999,
        "mock_interviews_per_month": 999,
        "learning_modules": "full",
        "company_tags_visible": 53,
        "leaderboard_access": True,
        "community_access": True,
    },
    "lifetime": {
        "interviews_per_month": 999,
        "resume_reviews_per_month": 999,
        "aptitude_tests_per_month": 999,
        "cover_letters_per_month": 999,
        "daily_compiler_runs": 999,
        "daily_ai_questions": 999,
        "problems_per_day": 999,
        "ai_mistakes_per_day": 999,
        "mock_interviews_per_month": 999,
        "learning_modules": "full",
        "company_tags_visible": 53,
        "leaderboard_access": True,
        "community_access": True,
    },
}


class AccessCheckRequest(BaseModel):
    feature: str


class TierStatusResponse(BaseModel):
    plan: str
    tier: str
    limits: dict
    usage: dict
    locked_features: list
    remaining: dict


def _get_current_month_key():
    now = datetime.now(timezone.utc)
    return f"{now.year}-{now.month}"


def _get_daily_key():
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d")


def _get_tier_for_plan(plan: str) -> str:
    if plan == "lifetime":
        return "lifetime"
    if plan == "pro":
        return "pro"
    return "free"


def _get_remaining(user: dict, feature: str) -> dict:
    tier = _get_tier_for_plan(user.get("plan", "free"))
    limits = TIER_LIMITS[tier]

    monthly_features = [
        "interviews_per_month",
        "resume_reviews_per_month",
        "aptitude_tests_per_month",
        "cover_letters_per_month",
        "mock_interviews_per_month",
    ]
    daily_features = [
        "daily_compiler_runs",
        "daily_ai_questions",
        "problems_per_day",
        "ai_mistakes_per_day",
    ]

    result = {}

    if feature in monthly_features:
        limit_key = feature
        used_key = feature.replace("_per_month", "") + "_used"
        limit = limits.get(limit_key, 0)
        used = user.get(used_key, 0)
        result["limit"] = limit if limit < 999 else -1
        result["used"] = used
        result["remaining"] = max(0, limit - used) if limit < 999 else -1
        result["unit"] = "per_month"
    elif feature in daily_features:
        limit_key = feature
        daily_used_key = feature.replace("daily_", "daily_") + "_count"
        limit = limits.get(limit_key, 0)
        daily_usage = user.get("daily_usage", {})
        today = _get_daily_key()
        used = daily_usage.get(today, {}).get(feature, 0)
        result["limit"] = limit if limit < 999 else -1
        result["used"] = used
        result["remaining"] = max(0, limit - used) if limit < 999 else -1
        result["unit"] = "per_day"
    else:
        result["limit"] = 0
        result["used"] = 0
        result["remaining"] = 0
        result["unit"] = "unknown"

    return result


@router.get("/status", response_model=TierStatusResponse)
async def tier_status(user=Depends(get_current_user)):
    user = await check_and_reset_monthly_usage(user)
    tier = _get_tier_for_plan(user.get("plan", "free"))
    limits = TIER_LIMITS[tier]
    usage = get_usage_stats(user)

    locked_features = []
    for feature_key, limit_val in limits.items():
        if feature_key in ("learning_modules", "leaderboard_access", "community_access"):
            continue
        remaining_info = _get_remaining(user, feature_key)
        if remaining_info["remaining"] == 0 and limit_val < 999:
            locked_features.append(feature_key)

    if tier == "free":
        locked_features.append("learning_modules")
        locked_features.append("leaderboard_access")

    return {
        "plan": user.get("plan", "free"),
        "tier": tier,
        "limits": limits,
        "usage": usage,
        "locked_features": locked_features,
        "remaining": {
            "interviews_per_month": _get_remaining(user, "interviews_per_month"),
            "resume_reviews_per_month": _get_remaining(user, "resume_reviews_per_month"),
            "aptitude_tests_per_month": _get_remaining(user, "aptitude_tests_per_month"),
            "cover_letters_per_month": _get_remaining(user, "cover_letters_per_month"),
            "daily_compiler_runs": _get_remaining(user, "daily_compiler_runs"),
            "daily_ai_questions": _get_remaining(user, "daily_ai_questions"),
            "problems_per_day": _get_remaining(user, "problems_per_day"),
            "ai_mistakes_per_day": _get_remaining(user, "ai_mistakes_per_day"),
        },
    }


@router.get("/features")
async def tier_features(user=Depends(get_current_user)):
    user = await check_and_reset_monthly_usage(user)
    tier = _get_tier_for_plan(user.get("plan", "free"))
    limits = TIER_LIMITS[tier]

    features = {}
    for feature_key, limit_val in limits.items():
        if feature_key.startswith("_"):
            continue
        remaining_info = _get_remaining(user, feature_key)
        features[feature_key] = {
            "available": remaining_info["remaining"] != 0 or limit_val >= 999,
            "tier": tier,
            "limit": limit_val,
            "remaining": remaining_info["remaining"],
            "used": remaining_info["used"],
            "unit": remaining_info["unit"],
        }

    features["learning_modules"] = {
        "available": tier in ("pro", "lifetime"),
        "tier": tier,
        "level": limits["learning_modules"],
        "locked_for_tier": tier == "free",
    }
    features["leaderboard_access"] = {
        "available": tier in ("pro", "lifetime"),
        "tier": tier,
        "locked_for_tier": tier == "free",
    }
    features["community_access"] = {
        "available": True,
        "tier": tier,
    }

    return {
        "plan": user.get("plan", "free"),
        "tier": tier,
        "features": features,
    }


@router.post("/check-access")
async def check_access(req: AccessCheckRequest, user=Depends(get_current_user)):
    user = await check_and_reset_monthly_usage(user)
    tier = _get_tier_for_plan(user.get("plan", "free"))
    limits = TIER_LIMITS[tier]

    monthly_features = {
        "interviews": "interviews_per_month",
        "resume_reviews": "resume_reviews_per_month",
        "aptitude_tests": "aptitude_tests_per_month",
        "cover_letters": "cover_letters_per_month",
        "mock_interviews": "mock_interviews_per_month",
    }
    daily_features = {
        "compiler_runs": "daily_compiler_runs",
        "ai_questions": "daily_ai_questions",
        "problems": "problems_per_day",
        "ai_mistakes": "ai_mistakes_per_day",
    }
    special_features = {
        "learning_modules": "learning_modules",
        "leaderboard": "leaderboard_access",
        "company_tags": "company_tags_visible",
    }

    feature = req.feature
    remaining_info = None
    allowed = False

    if feature in monthly_features:
        limit_key = monthly_features[feature]
        limit = limits.get(limit_key, 0)
        used_key = feature + "_used"
        used = user.get(used_key, 0)
        remaining_info = {
            "limit": limit if limit < 999 else -1,
            "used": used,
            "remaining": max(0, limit - used) if limit < 999 else -1,
            "unit": "per_month",
        }
        allowed = limit >= 999 or used < limit
    elif feature in daily_features:
        limit_key = daily_features[feature]
        limit = limits.get(limit_key, 0)
        daily_usage = user.get("daily_usage", {})
        today = _get_daily_key()
        used = daily_usage.get(today, {}).get(limit_key, 0)
        remaining_info = {
            "limit": limit if limit < 999 else -1,
            "used": used,
            "remaining": max(0, limit - used) if limit < 999 else -1,
            "unit": "per_day",
        }
        allowed = limit >= 999 or used < limit
    elif feature in special_features:
        special_key = special_features[feature]
        if special_key == "learning_modules":
            allowed = tier in ("pro", "lifetime")
            level = limits.get("learning_modules", "basic")
            remaining_info = {
                "tier": tier,
                "level": level,
                "locked_for_tier": tier == "free",
            }
        elif special_key == "leaderboard_access":
            allowed = tier in ("pro", "lifetime")
            remaining_info = {
                "tier": tier,
                "locked_for_tier": tier == "free",
            }
        elif special_key == "company_tags_visible":
            allowed = tier in ("pro", "lifetime")
            remaining_info = {
                "tier": tier,
                "visible": limits.get("company_tags_visible", 0),
                "locked_for_tier": tier == "free",
            }
    else:
        allowed = True
        remaining_info = {"message": "Feature not gated"}

    return {
        "feature": feature,
        "allowed": allowed,
        "tier": tier,
        "remaining": remaining_info,
    }


@router.get("/pricing")
async def tier_pricing():
    return {
        "plans": {
            "pro": {
                "name": "Pro",
                "price": {"USD": 19.0, "INR": 99.0},
                "billing": "monthly",
                "features": TIER_LIMITS["pro"],
                "highlights": [
                    "Unlimited AI interviews",
                    "Unlimited resume reviews",
                    "Unlimited aptitude tests",
                    "Unlimited cover letters",
                    "Unlimited daily compiler runs",
                    "Full learning modules (video + hints + solutions)",
                    "All company tags visible",
                    "Leaderboard access",
                ],
            },
            "lifetime": {
                "name": "Lifetime",
                "price": {"USD": 49.0, "INR": 499.0},
                "billing": "one_time",
                "features": TIER_LIMITS["lifetime"],
                "highlights": [
                    "Everything in Pro",
                    "One-time payment, never billed again",
                    "Unlimited access forever",
                    "All future updates included",
                    "No recurring charges",
                ],
            },
        },
        "free": {
            "name": "Free",
            "price": {"USD": 0, "INR": 0},
            "billing": "forever",
            "features": TIER_LIMITS["free"],
            "highlights": [
                "3 AI interviews per month",
                "3 resume reviews per month",
                "5 aptitude tests per month",
                "3 cover letters per month",
                "20 daily compiler runs",
                "5 daily AI questions",
                "Basic learning modules",
                "Community access",
            ],
        },
    }


@router.post("/reset-usage")
async def reset_usage(user=Depends(get_current_user)):
    if user.get("plan") not in ("pro", "lifetime"):
        if user.get("email", "").lower() not in _admin_emails():
            raise HTTPException(status_code=403, detail="Admin access required")

    now = datetime.now(timezone.utc)
    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {
            "$set": {
                "interviews_used": 0,
                "resumes_used": 0,
                "aptitude_used": 0,
                "cover_letters_used": 0,
                "monthly_reset_date": now,
                "daily_usage": {},
            }
        },
    )
    return {
        "message": "Usage counters reset successfully",
        "reset_at": now.isoformat(),
    }


@router.get("/usage")
async def tier_usage(user=Depends(get_current_user)):
    user = await check_and_reset_monthly_usage(user)
    tier = _get_tier_for_plan(user.get("plan", "free"))
    limits = TIER_LIMITS[tier]
    now = datetime.now(timezone.utc)
    month_key = _get_current_month_key()
    today = _get_daily_key()

    daily_usage = user.get("daily_usage", {})
    today_usage = daily_usage.get(today, {})

    all_time_usage = user.get("all_time_usage", {})

    usage_breakdown = {
        "tier": tier,
        "plan": user.get("plan", "free"),
        "current_month": month_key,
        "current_day": today,
        "monthly": {
            "interviews": {
                "used": user.get("interviews_used", 0),
                "limit": limits["interviews_per_month"],
                "remaining": max(0, limits["interviews_per_month"] - user.get("interviews_used", 0))
                if limits["interviews_per_month"] < 999
                else -1,
                "unit": "per_month",
            },
            "resume_reviews": {
                "used": user.get("resumes_used", 0),
                "limit": limits["resume_reviews_per_month"],
                "remaining": max(0, limits["resume_reviews_per_month"] - user.get("resumes_used", 0))
                if limits["resume_reviews_per_month"] < 999
                else -1,
                "unit": "per_month",
            },
            "aptitude_tests": {
                "used": user.get("aptitude_used", 0),
                "limit": limits["aptitude_tests_per_month"],
                "remaining": max(0, limits["aptitude_tests_per_month"] - user.get("aptitude_used", 0))
                if limits["aptitude_tests_per_month"] < 999
                else -1,
                "unit": "per_month",
            },
            "cover_letters": {
                "used": user.get("cover_letters_used", 0),
                "limit": limits["cover_letters_per_month"],
                "remaining": max(0, limits["cover_letters_per_month"] - user.get("cover_letters_used", 0))
                if limits["cover_letters_per_month"] < 999
                else -1,
                "unit": "per_month",
            },
            "mock_interviews": {
                "used": user.get("mock_interviews_used", 0),
                "limit": limits["mock_interviews_per_month"],
                "remaining": max(0, limits["mock_interviews_per_month"] - user.get("mock_interviews_used", 0))
                if limits["mock_interviews_per_month"] < 999
                else -1,
                "unit": "per_month",
            },
        },
        "daily": {
            "compiler_runs": {
                "used": today_usage.get("daily_compiler_runs", 0),
                "limit": limits["daily_compiler_runs"],
                "remaining": max(0, limits["daily_compiler_runs"] - today_usage.get("daily_compiler_runs", 0))
                if limits["daily_compiler_runs"] < 999
                else -1,
                "unit": "per_day",
            },
            "ai_questions": {
                "used": today_usage.get("daily_ai_questions", 0),
                "limit": limits["daily_ai_questions"],
                "remaining": max(0, limits["daily_ai_questions"] - today_usage.get("daily_ai_questions", 0))
                if limits["daily_ai_questions"] < 999
                else -1,
                "unit": "per_day",
            },
            "problems": {
                "used": today_usage.get("daily_problems", 0),
                "limit": limits["problems_per_day"],
                "remaining": max(0, limits["problems_per_day"] - today_usage.get("daily_problems", 0))
                if limits["problems_per_day"] < 999
                else -1,
                "unit": "per_day",
            },
            "ai_mistakes": {
                "used": today_usage.get("daily_ai_mistakes", 0),
                "limit": limits["ai_mistakes_per_day"],
                "remaining": max(0, limits["ai_mistakes_per_day"] - today_usage.get("daily_ai_mistakes", 0))
                if limits["ai_mistakes_per_day"] < 999
                else -1,
                "unit": "per_day",
            },
        },
        "all_time": {
            "total_interviews": all_time_usage.get("total_interviews", 0),
            "total_resumes": all_time_usage.get("total_resumes", 0),
            "total_aptitude": all_time_usage.get("total_aptitude", 0),
            "total_cover_letters": all_time_usage.get("total_cover_letters", 0),
            "total_problems_solved": all_time_usage.get("total_problems_solved", 0),
            "total_compiler_runs": all_time_usage.get("total_compiler_runs", 0),
        },
    }

    return usage_breakdown