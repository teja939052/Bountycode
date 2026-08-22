from datetime import datetime, timezone
import asyncio
from app.database import users_collection
from app.config import get_settings
from bson import ObjectId
from app.services.email import send_email, limit_reached_email

settings = get_settings()


async def check_and_reset_monthly_usage(user: dict) -> dict:
    """Check if monthly reset is needed and reset counters if so."""
    now = datetime.now(timezone.utc)
    last_reset = user.get("monthly_reset_date")

    if last_reset is None:
        await users_collection.update_one(
            {"_id": ObjectId(user["id"])},
            {"$set": {"monthly_reset_date": now}},
        )
        user["monthly_reset_date"] = now
        return user

    if user.get("plan") in ("pro", "lifetime"):
        return user

    last_reset_utc = last_reset.replace(tzinfo=timezone.utc) if last_reset.tzinfo is None else last_reset
    months_diff = (now.year - last_reset_utc.year) * 12 + (now.month - last_reset_utc.month)

    if months_diff >= 1:
        await users_collection.update_one(
            {"_id": ObjectId(user["id"])},
            {
                "$set": {
                    "interviews_used": 0,
                    "resumes_used": 0,
                    "aptitude_used": 0,
                    "cover_letters_used": 0,
                    "company_mocks_used": 0,
                    "predictions_used": 0,
                    "question_bank_used": 0,
                    "streak_repairs_used": 0,
                    "monthly_reset_date": now,
                }
            },
        )
        user["interviews_used"] = 0
        user["resumes_used"] = 0
        user["aptitude_used"] = 0
        user["cover_letters_used"] = 0
        user["company_mocks_used"] = 0
        user["predictions_used"] = 0
        user["question_bank_used"] = 0
        user["streak_repairs_used"] = 0
        user["monthly_reset_date"] = now

    return user


def can_use_feature(user: dict, feature: str) -> tuple[bool, str]:
    """Check if user can use a feature based on their plan and usage."""
    if user.get("plan") in ("pro", "lifetime"):
        return True, ""

    limits = {
        "interview": settings.FREE_TIER_INTERVIEW_LIMIT,
        "resume": settings.FREE_TIER_RESUME_LIMIT,
        "aptitude": getattr(settings, "FREE_TIER_APTITUDE_LIMIT", 5),
        "cover_letter": getattr(settings, "FREE_TIER_COVER_LETTER_LIMIT", 3),
        "company_mock": getattr(settings, "FREE_TIER_COMPANY_MOCK_LIMIT", 1),
        "predictor": getattr(settings, "FREE_TIER_PREDICTOR_LIMIT", 3),
        "question_bank": getattr(settings, "FREE_TIER_QUESTION_BANK_LIMIT", 5),
        "interview_booking": getattr(settings, "FREE_TIER_INTERVIEW_BOOKING_LIMIT", 3),
        "streak_repair": getattr(settings, "FREE_TIER_STREAK_REPAIRS", 1),
    }

    used_keys = {
        "interview": "interviews_used",
        "resume": "resumes_used",
        "aptitude": "aptitude_used",
        "cover_letter": "cover_letters_used",
        "company_mock": "company_mocks_used",
        "predictor": "predictions_used",
        "question_bank": "question_bank_used",
        "interview_booking": "interview_bookings_used",
        "streak_repair": "streak_repairs_used",
    }

    limit = limits.get(feature, 0)
    used = user.get(used_keys.get(feature, ""), 0)

    if used >= limit:
        return False, f"Free tier limit reached for {feature}. Upgrade to Pro for unlimited."

    return True, ""


async def mark_feature_used(user_id: str, feature: str) -> None:
    """Increment the usage counter for a feature."""
    used_keys = {
        "interview": "interviews_used",
        "resume": "resumes_used",
        "aptitude": "aptitude_used",
        "cover_letter": "cover_letters_used",
        "company_mock": "company_mocks_used",
        "predictor": "predictions_used",
        "question_bank": "question_bank_used",
        "interview_booking": "interview_bookings_used",
        "streak_repair": "streak_repairs_used",
    }
    key = used_keys.get(feature)
    if not key:
        return
    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$inc": {key: 1}},
    )

    # Lifecycle upsell: the instant a free user hits their limit is the
    # highest-intent conversion moment. Email them once per 2-day cooldown so
    # we don't spam on repeated attempts (routes block further use anyway).
    _LIMITS = {
        "interview": settings.FREE_TIER_INTERVIEW_LIMIT,
        "resume": settings.FREE_TIER_RESUME_LIMIT,
        "aptitude": getattr(settings, "FREE_TIER_APTITUDE_LIMIT", 5),
        "cover_letter": getattr(settings, "FREE_TIER_COVER_LETTER_LIMIT", 3),
        "company_mock": getattr(settings, "FREE_TIER_COMPANY_MOCK_LIMIT", 1),
        "predictor": getattr(settings, "FREE_TIER_PREDICTOR_LIMIT", 3),
        "question_bank": getattr(settings, "FREE_TIER_QUESTION_BANK_LIMIT", 5),
        "interview_booking": getattr(settings, "FREE_TIER_INTERVIEW_BOOKING_LIMIT", 3),
        "streak_repair": getattr(settings, "FREE_TIER_STREAK_REPAIRS", 1),
    }
    limit = _LIMITS.get(feature)
    if not limit:
        return
    user = await users_collection.find_one(
        {"_id": ObjectId(user_id)},
        {"plan": 1, "email": 1, "name": 1, "last_limit_email": 1, key: 1},
    )
    if not user or user.get("plan") in ("pro", "lifetime", "trial"):
        return
    if user.get(key, 0) >= limit:
        last = user.get("last_limit_email")
        now = datetime.now(timezone.utc)
        if last is None or (now - last).total_seconds() > 2 * 86400:
            try:
                asyncio.create_task(
                    send_email(user.get("email"), *limit_reached_email(user.get("name", ""), feature))
                )
                await users_collection.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {"last_limit_email": now}},
                )
            except Exception:
                pass


def get_usage_stats(user: dict) -> dict:
    """Get usage statistics for a user."""
    is_premium = user.get("plan") in ("pro", "lifetime")

    return {
        "plan": user.get("plan", "free"),
        "interviews_used": user.get("interviews_used", 0),
        "interviews_limit": "unlimited" if is_premium else settings.FREE_TIER_INTERVIEW_LIMIT,
        "resumes_used": user.get("resumes_used", 0),
        "resumes_limit": "unlimited" if is_premium else settings.FREE_TIER_RESUME_LIMIT,
        "aptitude_used": user.get("aptitude_used", 0),
        "aptitude_limit": "unlimited" if is_premium else getattr(settings, "FREE_TIER_APTITUDE_LIMIT", 5),
        "cover_letters_used": user.get("cover_letters_used", 0),
        "cover_letters_limit": "unlimited" if is_premium else getattr(settings, "FREE_TIER_COVER_LETTER_LIMIT", 3),
        "company_mocks_used": user.get("company_mocks_used", 0),
        "company_mocks_limit": "unlimited" if is_premium else getattr(settings, "FREE_TIER_COMPANY_MOCK_LIMIT", 1),
        "predictions_used": user.get("predictions_used", 0),
        "predictions_limit": "unlimited" if is_premium else getattr(settings, "FREE_TIER_PREDICTOR_LIMIT", 3),
        "question_bank_used": user.get("question_bank_used", 0),
        "question_bank_limit": "unlimited" if is_premium else getattr(settings, "FREE_TIER_QUESTION_BANK_LIMIT", 5),
    }
