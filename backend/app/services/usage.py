"""Usage tracking service — PostgreSQL-backed, replaces MongoDB None operations."""

from datetime import datetime, timezone
from typing import Dict, Any, Optional

from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.repositories.identity import UserRepository
from app.config import get_settings
from app.services.email import send_email, limit_reached_email
from app.models.identity import User

settings = get_settings()


async def check_and_reset_monthly_usage(user_id: str) -> dict:
    """Check if monthly reset is needed and reset counters if so."""
    async with get_session() as session:
        repo = UserRepository(session)
        user = await repo.get_by_id(user_id)

        if not user:
            return user

        now = datetime.now(timezone.utc)
        last_reset = user.monthly_reset_date

        if last_reset is None:
            await repo.update(user_id, {
                "monthly_reset_date": now,
            })
            return {
                "id": str(user.id),
                "monthly_reset_date": now,
            }

        last_reset_utc = last_reset.replace(tzinfo=timezone.utc) if last_reset.tzinfo is None else last_reset
        months_diff = (now.year - last_reset_utc.year) * 12 + (now.month - last_reset_utc.month)

        if months_diff >= 1:
            await repo.update(user_id, {
                "interviews_used": 0,
                "resumes_used": 0,
                "aptitude_used": 0,
                "company_mocks_used": 0,
                "predictions_used": 0,
                "question_bank_used": 0,
                "streak_repairs_used": 0,
                "monthly_reset_date": now,
            })

        return {
            "id": str(user.id),
            "interviews_used": user.interviews_used,
            "resumes_used": user.resumes_used,
            "aptitude_used": user.aptitude_used,
            "company_mocks_used": user.company_mocks_used,
            "predictions_used": user.predictions_used,
            "question_bank_used": user.question_bank_used,
            "streak_repairs_used": user.streak_repairs_used,
            "monthly_reset_date": user.monthly_reset_date,
        }


async def can_use_feature(user_id: str, feature: str) -> tuple[bool, str]:
    """Check if user can use a feature based on their plan and usage."""
    async with get_session() as session:
        repo = UserRepository(session)
        user = await repo.get_by_id(user_id)

        if not user:
            return True, ""  # Unknown user, allow

        if user.plan in ("pro", "lifetime"):
            return True, ""

    limits = {
        "interview": settings.FREE_TIER_INTERVIEW_LIMIT,
        "resume": settings.FREE_TIER_RESUME_LIMIT,
        "aptitude": getattr(settings, "FREE_TIER_APTITUDE_LIMIT", 5),
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
        "company_mock": "company_mocks_used",
        "predictor": "predictions_used",
        "question_bank": "question_bank_used",
        "interview_booking": "interview_bookings_used",
        "streak_repair": "streak_repairs_used",
    }

    limit = limits.get(feature, 0)
    used = user.get(used_keys.get(feature, ""), 0) if hasattr(user, used_keys.get(feature, "")) else 0

    if used >= limit:
        return False, f"Free tier limit reached for {feature}. Upgrade to Pro for unlimited."

    return True, ""


async def mark_feature_used(user_id: str, feature: str) -> None:
    """Increment the usage counter for a feature."""
    async with get_session() as session:
        repo = UserRepository(session)
        user = await repo.get_by_id(user_id)

        if not user:
            return

        used_keys = {
            "interview": "interviews_used",
            "resume": "resumes_used",
            "aptitude": "aptitude_used",
            "company_mock": "company_mocks_used",
            "predictor": "predictions_used",
            "question_bank": "question_bank_used",
            "interview_booking": "interview_bookings_used",
            "streak_repair": "streak_repairs_used",
        }
        key = used_keys.get(feature)
        if not key:
            return

        # Update usage counter
        updates = {key: getattr(user, key, 0) + 1}
        await repo.update(user_id, updates)

        # Lifecycle upsell: the instant a free user hits their limit is the
        # highest-intent conversion moment. Email them once per 2-day cooldown so
        # we don't spam on repeated attempts (routes block further use anyway).
        _LIMITS = {
            "interview": settings.FREE_TIER_INTERVIEW_LIMIT,
            "resume": settings.FREE_TIER_RESUME_LIMIT,
            "aptitude": getattr(settings, "FREE_TIER_APTITUDE_LIMIT", 5),
            "company_mock": getattr(settings, "FREE_TIER_COMPANY_MOCK_LIMIT", 1),
            "predictor": getattr(settings, "FREE_TIER_PREDICTOR_LIMIT", 3),
            "question_bank": getattr(settings, "FREE_TIER_QUESTION_BANK_LIMIT", 5),
            "interview_booking": getattr(settings, "FREE_TIER_INTERVIEW_BOOKING_LIMIT", 3),
            "streak_repair": getattr(settings, "FREE_TIER_STREAK_REPAIRS", 1),
        }
        limit = _LIMITS.get(feature)
        if not limit:
            return

        # Re-fetch user after update
        user = await repo.get_by_id(user_id)
        if not user or user.plan in ("pro", "lifetime", "trial"):
            return

        if user.get(key, 0) >= limit:
            last = user.last_limit_email
            now = datetime.now(timezone.utc)
            if last is None or (now - last).total_seconds() > 2 * 86400:
                try:
                    asyncio.create_task(
                        send_email(user.email, *limit_reached_email(user.name, feature))
                    )
                    await repo.update(user_id, {"last_limit_email": now})
                except Exception:
                    pass


async def get_usage_stats(user_id: str) -> dict:
    """Get usage statistics for a user."""
    async with get_session() as session:
        repo = UserRepository(session)
        user = await repo.get_by_id(user_id)

        if not user:
            is_premium = False
            return {
                "plan": "free",
                "interviews_used": 0,
                "interviews_limit": settings.FREE_TIER_INTERVIEW_LIMIT,
                "resumes_used": 0,
                "resumes_limit": settings.FREE_TIER_RESUME_LIMIT,
                "aptitude_used": 0,
                "aptitude_limit": getattr(settings, "FREE_TIER_APTITUDE_LIMIT", 5),
                "company_mocks_used": 0,
                "company_mocks_limit": getattr(settings, "FREE_TIER_COMPANY_MOCK_LIMIT", 1),
                "predictions_used": 0,
                "predictions_limit": getattr(settings, "FREE_TIER_PREDICTOR_LIMIT", 3),
                "question_bank_used": 0,
                "question_bank_limit": getattr(settings, "FREE_TIER_QUESTION_BANK_LIMIT", 5),
            }

        is_premium = user.plan in ("pro", "lifetime")

        return {
            "plan": user.plan,
            "interviews_used": user.interviews_used,
            "interviews_limit": "unlimited" if is_premium else settings.FREE_TIER_INTERVIEW_LIMIT,
            "resumes_used": user.resumes_used,
            "resumes_limit": "unlimited" if is_premium else settings.FREE_TIER_RESUME_LIMIT,
            "aptitude_used": user.aptitude_used,
            "aptitude_limit": "unlimited" if is_premium else getattr(settings, "FREE_TIER_APTITUDE_LIMIT", 5),
            "company_mocks_used": user.company_mocks_used,
            "company_mocks_limit": "unlimited" if is_premium else getattr(settings, "FREE_TIER_COMPANY_MOCK_LIMIT", 1),
            "predictions_used": user.predictions_used,
            "predictions_limit": "unlimited" if is_premium else getattr(settings, "FREE_TIER_PREDICTOR_LIMIT", 3),
            "question_bank_used": user.question_bank_used,
            "question_bank_limit": "unlimited" if is_premium else getattr(settings, "FREE_TIER_QUESTION_BANK_LIMIT", 5),
        }