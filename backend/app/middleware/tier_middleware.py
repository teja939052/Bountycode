from datetime import datetime, timezone
from fastapi import Request, HTTPException, Depends
from typing import Callable, Awaitable
from app.middleware.auth import get_current_user
from app.services.usage import check_and_reset_monthly_usage

TIER_LIMITS = {
    "free": {
        "interviews_per_month": 3,
        "resume_reviews_per_month": 3,
        "aptitude_tests_per_month": 5,
        "cover_letters_per_month": 3,
        "daily_compiler_runs": 20,
        "daily_ai_questions": 5,
        "daily_mystery_boxes": 1,
        "problems_per_day": 10,
        "ai_mistakes_per_day": 3,
        "mock_interviews_per_month": 1,
    },
    "pro": {
        "interviews_per_month": 999,
        "resume_reviews_per_month": 999,
        "aptitude_tests_per_month": 999,
        "cover_letters_per_month": 999,
        "daily_compiler_runs": 999,
        "daily_ai_questions": 999,
        "daily_mystery_boxes": 3,
        "problems_per_day": 999,
        "ai_mistakes_per_day": 999,
        "mock_interviews_per_month": 999,
    },
    "lifetime": {
        "interviews_per_month": 999,
        "resume_reviews_per_month": 999,
        "aptitude_tests_per_month": 999,
        "cover_letters_per_month": 999,
        "daily_compiler_runs": 999,
        "daily_ai_questions": 999,
        "daily_mystery_boxes": 5,
        "problems_per_day": 999,
        "ai_mistakes_per_day": 999,
        "mock_interviews_per_month": 999,
    },
}

FEATURE_TO_LIMIT_KEY = {
    "interview": "interviews_per_month",
    "interviews": "interviews_per_month",
    "resume": "resume_reviews_per_month",
    "resume_review": "resume_reviews_per_month",
    "resumes": "resume_reviews_per_month",
    "aptitude": "aptitude_tests_per_month",
    "aptitude_test": "aptitude_tests_per_month",
    "aptitude_tests": "aptitude_tests_per_month",
    "cover_letter": "cover_letters_per_month",
    "cover_letters": "cover_letters_per_month",
    "mock_interview": "mock_interviews_per_month",
    "mock_interviews": "mock_interviews_per_month",
    "compiler_run": "daily_compiler_runs",
    "compiler_runs": "daily_compiler_runs",
    "ai_question": "daily_ai_questions",
    "ai_questions": "daily_ai_questions",
    "mystery_box": "daily_mystery_boxes",
    "mystery_boxes": "daily_mystery_boxes",
    "problem": "problems_per_day",
    "problems": "problems_per_day",
    "ai_mistake": "ai_mistakes_per_day",
    "ai_mistakes": "ai_mistakes_per_day",
}

MONTHLY_FEATURES = {
    "interview", "interviews", "interviews_per_month",
    "resume", "resume_review", "resume_reviews", "resume_reviews_per_month",
    "aptitude", "aptitude_test", "aptitude_tests", "aptitude_tests_per_month",
    "cover_letter", "cover_letters", "cover_letters_per_month",
    "mock_interview", "mock_interviews", "mock_interviews_per_month",
}

DAILY_FEATURES = {
    "compiler_run", "compiler_runs", "daily_compiler_runs",
    "ai_question", "ai_questions", "daily_ai_questions",
    "mystery_box", "mystery_boxes", "daily_mystery_boxes",
    "problem", "problems", "problems_per_day",
    "ai_mistake", "ai_mistakes", "ai_mistakes_per_day",
}


def _get_tier(plan: str) -> str:
    if plan == "lifetime":
        return "lifetime"
    if plan == "pro":
        return "pro"
    return "free"


def _get_current_month_key():
    now = datetime.now(timezone.utc)
    return f"{now.year}-{now.month}"


def _get_daily_key():
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d")


async def _increment_daily_usage(user: dict, feature_key: str):
    """Increment daily usage counter for a user."""
    from app.database import users_collection
    from bson import ObjectId

    daily_usage = user.get("daily_usage", {})
    today = _get_daily_key()

    if today not in daily_usage:
        daily_usage[today] = {}

    if feature_key not in daily_usage[today]:
        daily_usage[today][feature_key] = 0

    daily_usage[today][feature_key] += 1

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$set": {"daily_usage": daily_usage}},
    )

    return daily_usage[today][feature_key]


async def _increment_monthly_usage(user: dict, feature_key: str):
    """Increment monthly usage counter for a user."""
    from app.database import users_collection
    from bson import ObjectId

    used_key = feature_key + "_used"

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$inc": {used_key: 1}},
    )

    user[used_key] = user.get(used_key, 0) + 1
    return user[used_key]


async def check_tier_limit(user: dict, feature: str) -> None:
    """Check if a user's tier and usage allow access to a feature.
    Raises HTTPException(403) when the limit is reached."""
    plan = user.get("plan", "free")
    tier = _get_tier(plan)
    limits = TIER_LIMITS[tier]

    limit_key = FEATURE_TO_LIMIT_KEY.get(feature)
    if limit_key is None:
        return

    limit = limits.get(limit_key, 0)

    if limit >= 999:
        return

    if limit_key in MONTHLY_FEATURES or feature in MONTHLY_FEATURES:
        used_key = feature.replace("_per_month", "") + "_used" if "_per_month" in limit_key else feature + "_used"
        if limit_key.startswith("daily_"):
            used_key = limit_key.replace("daily_", "") + "_used"
        used = user.get(used_key, 0)

        if used >= limit:
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "upgrade_required",
                    "feature": feature,
                    "current_usage": used,
                    "limit": limit,
                    "plan": plan,
                    "tier": tier,
                    "unit": "per_month",
                    "message": f"Your {plan} tier limit for {feature} has been reached ({used}/{limit}). Upgrade to Pro for unlimited access.",
                },
            )
    elif limit_key in DAILY_FEATURES or feature in DAILY_FEATURES:
        daily_usage = user.get("daily_usage", {})
        today = _get_daily_key()
        today_usage = daily_usage.get(today, {})
        used = today_usage.get(limit_key, 0)

        if used >= limit:
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "upgrade_required",
                    "feature": feature,
                    "current_usage": used,
                    "limit": limit,
                    "plan": plan,
                    "tier": tier,
                    "unit": "per_day",
                    "reset_at": f"{today} 23:59:59 UTC",
                    "message": f"Your daily limit for {feature} has been reached ({used}/{limit}). Come back tomorrow or upgrade to Pro for unlimited access.",
                },
            )


async def tier_gate(feature: str):
    """
    Dependency that gates a feature based on the user's tier and usage.
    Raises HTTPException(403) with structured error when limit is reached.

    Usage in route:
        @router.post("/interview/answer")
        async def submit_answer(
            user=Depends(tier_gate("interview")),
            ...
        ):
            ...
    """
    async def dependency(user=Depends(get_current_user)):
        await check_and_reset_monthly_usage(user)
        await check_tier_limit(user, feature)
        return user

    return dependency


async def tier_gate_middleware(request: Request, call_next):
    """
    Middleware that checks tier limits on protected routes.
    Attach tier info to request state for route handlers to use.
    """
    user = getattr(request.state, "user", None)
    if user is None:
        try:
            user = await get_current_user(request)
            request.state.user = user
        except HTTPException:
            pass

    if user:
        await check_and_reset_monthly_usage(user)
        tier = _get_tier(user.get("plan", "free"))
        limits = TIER_LIMITS[tier]
        request.state.tier = tier
        request.state.tier_limits = limits

    response = await call_next(request)
    return response