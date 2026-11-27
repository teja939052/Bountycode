"""Tier limits and plan enforcement — PostgreSQL-backed, no MongoDB."""

from datetime import datetime, timezone
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.middleware.auth import get_current_user, require_plan
from app.config import get_settings
from app.services.usage import check_and_reset_monthly_usage, get_usage_stats
from app.repositories.identity import UserRepository

router = APIRouter(prefix="/api/v1/tiers", tags=["tiers"])
settings = get_settings()

TIER_LIMITS = {
    "free": {
        "interviews_per_month": 3,
        "resume_reviews_per_month": 3,
        "aptitude_tests_per_month": 5,
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
        "daily_compiler_runs": 999,
        "daily_ai_questions": 999,
        "problems_per_day": 999,
        "ai_mistakes_per_day": 999,
        "mock_interviews_per_month": 999,
        "learning_modules": "full",
        "company_tags_visible": 999,
        "leaderboard_access": True,
        "community_access": True,
    },
}


@router.get("/limits")
async def get_tier_limits(user=Depends(get_current_user)):
    """Get tier limits for the user's current plan."""
    async with get_session() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_by_id(user["id"])
    
    plan = user.plan if user else "free"
    limits = TIER_LIMITS.get(plan, TIER_LIMITS["free"])
    
    # Get current usage from the usage service
    usage = await get_usage_stats(user["id"])
    
    # Calculate remaining usage
    remaining = {}
    for key, limit in limits.items():
        usage_key = key.replace("_per_month", "").replace("_per_day", " per day").replace("_per_week", " per week")
        used = usage.get(key, 0)
        remaining[key] = max(0, limit - used) if isinstance(limit, int) else "unlimited"
    
    return {
        "plan": plan,
        "limits": limits,
        "usage": usage,
        "remaining": remaining,
    }


@router.post("/check-usage")
async def check_usage(request: dict, user=Depends(get_current_user)):
    """Check if user can use a feature based on their plan and usage."""
    feature = request.get("feature")
    amount = request.get("amount", 1)
    
    async with get_session() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_by_id(user["id"])
    
    if not user or user.plan in ("pro", "lifetime"):
        return {"allowed": True, "reason": ""}
    
    # Check usage limits
    allowed, reason = check_and_reset_monthly_usage(user["id"], feature)
    
    return {"allowed": allowed, "reason": reason}