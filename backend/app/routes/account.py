from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.config import get_settings
from app.database import users_collection, usage_collection
from app.services.usage import check_and_reset_monthly_usage, get_usage_stats

router = APIRouter(prefix="/api/v1/account", tags=["account"])
settings = get_settings()


class AccountProfileResponse(BaseModel):
    user: Dict[str, Any]
    plan: Dict[str, Any]
    usage: Dict[str, Any]
    features: List[Dict[str, Any]]
    upgrade_recommended: bool
    upgrade_message: Optional[str] = None


@router.get("/profile", response_model=AccountProfileResponse)
async def account_profile(user=Depends(get_current_user)):
    """Unified account profile: plan, usage, feature access, and upgrade state."""
    user = await check_and_reset_monthly_usage(user)
    plan_key = user.get("plan", "free")
    tier = "pro" if plan_key in ("pro", "lifetime") else "free" if plan_key == "free" else plan_key

    usage = get_usage_stats(user)

    trial_end = user.get("trial_end")
    plan_expires = None
    is_trial = plan_key == "trial"
    if is_trial and trial_end:
        plan_expires = trial_end.isoformat() if isinstance(trial_end, datetime) else str(trial_end)

    plan_meta = {
        "free": {
            "key": "free",
            "name": "Free",
            "price": {"USD": 0, "INR": 0},
            "billing": "forever",
            "period": "",
            "desc": "Limited free access",
            "highlights": [
                "3 AI interviews per month",
                "3 resume reviews per month",
                "5 aptitude tests per month",
                "20 daily compiler runs",
                "5 daily AI questions",
                "Basic learning modules",
                "Community access",
            ],
        },
        "pro": {
            "key": "pro",
            "name": "Commander",
            "price": {"USD": 19.0, "INR": 99.0},
            "billing": "monthly",
            "period": "/month",
            "desc": "Cancel anytime. Instant access.",
            "highlights": [
                "Unlimited AI interviews with feedback",
                "Unlimited resume uploads, generation and ATS optimization",
                "Unlimited aptitude tests with detailed solutions",
                "Unlimited coding challenges with hints and solutions",
                "Unlimited system design practice with evaluation",
                "AI debugging, coaching and step-by-step traces",
                "AI cover letters and LinkedIn summaries",
                "Unlimited daily compiler runs",
                "Full learning modules (video + hints + solutions)",
                "All company tags visible",
                "Leaderboard access",
            ],
        },
        "lifetime": {
            "key": "lifetime",
            "name": "Admiral",
            "price": {"USD": 149.0, "INR": 1499.0},
            "billing": "one_time",
            "period": "one-time",
            "desc": "Pay once. Use forever.",
            "highlights": [
                "Everything in Pro",
                "One-time payment, never billed again",
                "Unlimited access forever",
                "All future updates included",
                "No recurring charges",
            ],
        },
        "trial": {
            "key": "trial",
            "name": "Pro Trial",
            "price": {"USD": 0, "INR": 0},
            "billing": "trial",
            "period": "7 days",
            "desc": "Free trial — no card required",
            "highlights": [
                "All Pro features unlocked during trial",
                "No payment information needed",
                "Cancels automatically",
            ],
        },
    }

    plan_info = plan_meta.get(plan_key, plan_meta["free"])

    features = [
        {
            "id": "interviews",
            "name": "AI Mock Interviews",
            "description": "Practice with AI-powered interview questions and feedback",
            "category": "interview",
            "available": tier in ("pro", "lifetime") or usage.get("interviews_limit") != "unlimited",
        },
        {
            "id": "resume",
            "name": "Resume Builder & ATS Optimizer",
            "description": "Upload, generate, and optimize resumes with AI",
            "category": "resume",
            "available": True,
        },
        {
            "id": "aptitude",
            "name": "Aptitude Tests",
            "description": "Quantitative, logical, and verbal aptitude practice",
            "category": "aptitude",
            "available": True,
        },
        {
            "id": "coding",
            "name": "Coding Challenges",
            "description": "LeetCode-style coding problems with test cases",
            "category": "coding",
            "available": True,
        },
        {
            "id": "compiler",
            "name": "Code Compiler",
            "description": "Run code in Python, Java, C++, and more",
            "category": "coding",
            "available": True,
        },
        {
            "id": "ai_feedback",
            "name": "AI Answer Feedback",
            "description": "Get detailed AI-powered feedback on your answers",
            "category": "ai",
            "available": tier in ("pro", "lifetime"),
        },
        {
            "id": "company_prep",
            "name": "Company-Specific Prep",
            "description": "53+ company blueprints with tailored questions and mocks",
            "category": "prep",
            "available": tier in ("pro", "lifetime"),
        },
        {
            "id": "system_design",
            "name": "System Design Practice",
            "description": "Practice system design interviews with AI evaluation",
            "category": "interview",
            "available": tier in ("pro", "lifetime"),
        },
        {
            "id": "cover_letter",
            "name": "Cover Letter & LinkedIn",
            "description": "AI-generated cover letters and LinkedIn summaries",
            "category": "career",
            "available": tier in ("pro", "lifetime"),
        },
        {
            "id": "learning_modules",
            "name": "Full Learning Modules",
            "description": "Video lessons, hints, solutions, and guided practice",
            "category": "learning",
            "available": tier in ("pro", "lifetime"),
        },
        {
            "id": "leaderboard",
            "name": "Leaderboard",
            "description": "Compete with other learners and track your rank",
            "category": "gamification",
            "available": tier in ("pro", "lifetime"),
        },
        {
            "id": "mentor",
            "name": "AI Mentor Chat",
            "description": "24/7 AI coding mentor for debugging and coaching",
            "category": "ai",
            "available": tier in ("pro", "lifetime"),
        },
    ]

    upgrade_recommended = plan_key == "free" or is_trial
    upgrade_message = None
    if upgrade_recommended:
        upgrade_message = (
            "Upgrade to Pro to unlock unlimited AI interviews, resume optimization, "
            "company-specific prep, and all learning modules. Starting at ₹99/month."
        )

    return {
        "user": {
            "id": user["id"],
            "name": user.get("name", ""),
            "email": user.get("email", ""),
            "plan": plan_key,
            "tier": tier,
            "is_admin": user.get("is_admin", False),
            "role": user.get("role", "sde"),
            "target_company": user.get("target_company", ""),
            "target_role": user.get("target_role", ""),
        },
        "plan": {
            **plan_info,
            "expires_at": plan_expires,
            "is_trial": is_trial,
            "days_remaining": _days_remaining(plan_expires) if plan_expires else None,
        },
        "usage": usage,
        "features": features,
        "upgrade_recommended": upgrade_recommended,
        "upgrade_message": upgrade_message,
    }


def _days_remaining(iso_str: str) -> Optional[float]:
    try:
        end = datetime.fromisoformat(iso_str)
        now = datetime.now(timezone.utc)
        if end.tzinfo is None:
            end = end.replace(tzinfo=timezone.utc)
        diff = (end - now).total_seconds() / 86400
        return max(0.0, round(diff, 1))
    except Exception:
        return None


@router.get("/features")
async def account_features(user=Depends(get_current_user)):
    """Feature catalog with tier requirements."""
    user = await check_and_reset_monthly_usage(user)
    plan_key = user.get("plan", "free")
    tier = "pro" if plan_key in ("pro", "lifetime") else "free" if plan_key == "free" else plan_key

    features = [
        {
            "id": "interviews",
            "name": "AI Mock Interviews",
            "category": "interview",
            "description": "Practice with AI interview questions and get detailed feedback",
            "free_access": True,
            "pro_required": False,
            "limits": {
                "free": "3 per month",
                "pro": "Unlimited",
                "lifetime": "Unlimited",
            },
        },
        {
            "id": "resume",
            "name": "Resume Builder & ATS Optimizer",
            "category": "resume",
            "description": "Upload, generate, and optimize resumes with AI-powered ATS scoring",
            "free_access": True,
            "pro_required": False,
            "limits": {
                "free": "3 per month",
                "pro": "Unlimited",
                "lifetime": "Unlimited",
            },
        },
        {
            "id": "aptitude",
            "name": "Aptitude Tests",
            "category": "aptitude",
            "description": "Quantitative, logical, and verbal aptitude practice tests",
            "free_access": True,
            "pro_required": False,
            "limits": {
                "free": "5 per month",
                "pro": "Unlimited",
                "lifetime": "Unlimited",
            },
        },
        {
            "id": "coding",
            "name": "Coding Challenges",
            "category": "coding",
            "description": "LeetCode-style problems with test cases and hidden judge",
            "free_access": True,
            "pro_required": False,
            "limits": {
                "free": "5 per day",
                "pro": "Unlimited",
                "lifetime": "Unlimited",
            },
        },
        {
            "id": "compiler",
            "name": "Code Compiler",
            "category": "coding",
            "description": "Run code in Python, Java, C++, JavaScript, and more",
            "free_access": True,
            "pro_required": False,
            "limits": {
                "free": "20 runs/day",
                "pro": "Unlimited",
                "lifetime": "Unlimited",
            },
        },
        {
            "id": "question_bank",
            "name": "Question Bank",
            "category": "practice",
            "description": "100+ curated problems with company filters and solutions",
            "free_access": True,
            "pro_required": False,
            "limits": {
                "free": "5 per day",
                "pro": "Unlimited",
                "lifetime": "Unlimited",
            },
        },
        {
            "id": "ai_feedback",
            "name": "AI Answer Feedback",
            "category": "ai",
            "description": "Get detailed AI-powered feedback on your answers with strengths, improvements, and better approaches",
            "free_access": False,
            "pro_required": True,
            "limits": {
                "free": "Locked",
                "pro": "Unlimited",
                "lifetime": "Unlimited",
            },
        },
        {
            "id": "company_prep",
            "name": "Company-Specific Prep",
            "category": "prep",
            "description": "53+ company blueprints with tailored questions, patterns, and mocks",
            "free_access": False,
            "pro_required": True,
            "limits": {
                "free": "Locked (TCS/Infosys/Wipro only)",
                "pro": "All 53+ companies",
                "lifetime": "All 53+ companies",
            },
        },
        {
            "id": "system_design",
            "name": "System Design Practice",
            "category": "interview",
            "description": "Practice system design interviews with AI evaluation and rubrics",
            "free_access": False,
            "pro_required": True,
            "limits": {
                "free": "Locked",
                "pro": "Unlimited",
                "lifetime": "Unlimited",
            },
        },
        {
            "id": "cover_letter",
            "name": "Cover Letter & LinkedIn",
            "category": "career",
            "description": "AI-generated cover letters and LinkedIn About sections",
            "free_access": False,
            "pro_required": True,
            "limits": {
                "free": "Locked",
                "pro": "Unlimited",
                "lifetime": "Unlimited",
            },
        },
        {
            "id": "learning_modules",
            "name": "Full Learning Modules",
            "category": "learning",
            "description": "Video lessons, hints, solutions, and guided practice for all skills",
            "free_access": False,
            "pro_required": True,
            "limits": {
                "free": "Basic only",
                "pro": "Full access",
                "lifetime": "Full access",
            },
        },
        {
            "id": "leaderboard",
            "name": "Leaderboard",
            "category": "gamification",
            "description": "Compete with other learners and track your rank",
            "free_access": False,
            "pro_required": True,
            "limits": {
                "free": "Locked",
                "pro": "Unlimited",
                "lifetime": "Unlimited",
            },
        },
        {
            "id": "mentor",
            "name": "AI Mentor Chat",
            "category": "ai",
            "description": "24/7 AI coding mentor for debugging, coaching, and step-by-step traces",
            "free_access": False,
            "pro_required": True,
            "limits": {
                "free": "Locked",
                "pro": "Unlimited",
                "lifetime": "Unlimited",
            },
        },
        {
            "id": "visualizations",
            "name": "Algorithm Visualizations",
            "category": "learning",
            "description": "50+ pre-built algorithm visualizations with AI-generated traces",
            "free_access": True,
            "pro_required": False,
            "limits": {
                "free": "50+ templates",
                "pro": "Unlimited AI traces",
                "lifetime": "Unlimited AI traces",
            },
        },
        {
            "id": "hints",
            "name": "Progressive Hints",
            "category": "learning",
            "description": "3-level hint system: nudge → approach → solution",
            "free_access": True,
            "pro_required": False,
            "limits": {
                "free": "Level 1-2 only",
                "pro": "All 3 levels",
                "lifetime": "All 3 levels",
            },
        },
    ]

    return {
        "plan": plan_key,
        "tier": tier,
        "features": features,
        "upgrade_url": "/pricing",
    }


@router.get("/plan")
async def account_plan(user=Depends(get_current_user)):
    """Current plan details with expiry and renewal info."""
    user = await check_and_reset_monthly_usage(user)
    plan_key = user.get("plan", "free")

    trial_end = user.get("trial_end")
    plan_expires = None
    is_trial = plan_key == "trial"
    if is_trial and trial_end:
        plan_expires = trial_end.isoformat() if isinstance(trial_end, datetime) else str(trial_end)

    plan_details = {
        "plan": plan_key,
        "tier": "pro" if plan_key in ("pro", "lifetime") else "free" if plan_key == "free" else plan_key,
        "is_trial": is_trial,
        "expires_at": plan_expires,
        "days_remaining": _days_remaining(plan_expires) if plan_expires else None,
        "billing": {
            "free": {"cycle": "forever", "amount": 0, "currency": "USD"},
            "pro": {"cycle": "monthly", "amount": 19, "currency": "USD"},
            "lifetime": {"cycle": "one_time", "amount": 149, "currency": "USD"},
            "trial": {"cycle": "trial", "amount": 0, "currency": "USD"},
        }.get(plan_key, {"cycle": "unknown", "amount": 0, "currency": "USD"}),
    }

    return plan_details
