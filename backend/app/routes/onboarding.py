from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.middleware.auth import get_current_user
from app.database import users_collection
from bson import ObjectId

logger = __import__("logging").getLogger(__name__)

router = APIRouter(prefix="/api/v1/onboarding", tags=["onboarding"])

ALLOWED_CAREER_GOALS = {
    "internship", "placements", "learning", "hackathons", "full_stack", "ai_ml",
}

ALLOWED_TECH_INTERESTS = {
    "java", "python", "javascript", "react", "nodejs", "spring_boot",
    "dsa", "ai", "ml", "cybersecurity", "data_science",
}


def _validate_list(values: List[str], allowed: set, field_name: str) -> List[str]:
    invalid = [v for v in values if v not in allowed]
    if invalid:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {field_name}: {', '.join(invalid)}",
        )
    return values

QUEST_STEPS = [
    {
        "id": "step-1",
        "title": "Choose Your Language",
        "description": "Pick the language you want to learn. C, C++, Java, or Python — all paths lead to placement success.",
        "type": "navigation",
        "action": "Select a language from the learning hub",
        "target": "/learn/c",
        "icon": "\U0001f3af",
    },
    {
        "id": "step-2",
        "title": "Write Your First Code",
        "description": "Open the first lesson and run your first program. You will have code running in under 30 seconds.",
        "type": "action",
        "action": "Open any lesson and click Run",
        "target": "/free-trial",
        "icon": "\u2328\ufe0f",
    },
    {
        "id": "step-3",
        "title": "Earn Your First Diamonds",
        "description": "Complete the lesson and watch your progress climb. Gamification keeps you hooked.",
        "type": "action",
        "action": "Complete a lesson to earn Diamonds",
        "target": "/learn/c",
        "icon": "\u2b50",
    },
    {
        "id": "step-4",
        "title": "Track Your Streak",
        "description": "Keep learning daily to build your streak multiplier. Consistency beats intensity.",
        "type": "info",
        "action": "Check your streak in the dashboard",
        "target": "/dashboard",
        "icon": "\U0001f525",
    },
    {
        "id": "step-5",
        "title": "Go Pro for Unlimited Access",
        "description": "Free users get 3 lessons per month. Pro unlocks everything for ₹99/mo or ₹899/yr.",
        "type": "conversion",
        "action": "Upgrade to Pro",
        "target": "/pricing",
        "icon": "\U0001f680",
    },
]


class CompleteStepRequest(BaseModel):
    step_id: str
    completed: bool = True
    xp_earned: int = 10


@router.get("/quest")
async def get_quest(user=Depends(get_current_user)):
    return {
        "quest": {
            "id": "onboarding-quest",
            "title": "Welcome Aboard! Your First Steps",
            "description": "Get started in 5 minutes and see the platform shine",
            "steps": QUEST_STEPS,
        }
    }


@router.post("/complete")
async def complete_step(req: CompleteStepRequest, user=Depends(get_current_user)):
    step = next((s for s in QUEST_STEPS if s["id"] == req.step_id), None)
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {
            "$addToSet": {"onboarding_quest.completed_steps": req.step_id},
            "$set": {
                "onboarding_quest.last_active": datetime.now(timezone.utc),
                # Unlock the app once the user engages with the quest — the
                # OnboardingGuard reads this legacy flag.
                "onboarding.completed": True,
            },
        },
        upsert=True,
    )

    return {
        "step_id": req.step_id,
        "completed": req.completed,
        "xp_earned": req.xp_earned,
    }


@router.get("/status")
async def onboarding_status(user=Depends(get_current_user)):
    db_user = await users_collection.find_one({"_id": ObjectId(user["id"])})
    quest_data = db_user.get("onboarding_quest", {}) if db_user else {}
    completed_steps = quest_data.get("completed_steps", [])
    total_steps = len(QUEST_STEPS)
    overall_progress = int((len(completed_steps) / total_steps) * 100) if total_steps > 0 else 0
    is_complete = len(completed_steps) >= total_steps

    # Backfill for users who completed quest steps before the legacy flag was
    # synced — keeps the OnboardingGuard from trapping them in a redirect loop.
    legacy_completed = (db_user or {}).get("onboarding", {}).get("completed", False)
    if completed_steps and not legacy_completed:
        await users_collection.update_one(
            {"_id": ObjectId(user["id"])},
            {"$set": {"onboarding.completed": True}},
        )

    return {
        "completed_steps": completed_steps,
        "overall_progress": overall_progress,
        "is_complete": is_complete,
    }


class OnboardingPreferences(BaseModel):
    career_goals: List[str] = []
    tech_interests: List[str] = []


@router.get("/preferences")
async def get_preferences(user=Depends(get_current_user)):
    db_user = await users_collection.find_one({"_id": ObjectId(user["id"])})
    onboarding = db_user.get("onboarding", {}) if db_user else {}
    return {
        "career_goals": onboarding.get("career_goals", []),
        "tech_interests": onboarding.get("tech_interests", []),
        "completed": onboarding.get("completed", False),
    }


@router.post("/preferences")
async def save_preferences(req: OnboardingPreferences, user=Depends(get_current_user)):
    career_goals = _validate_list(req.career_goals, ALLOWED_CAREER_GOALS, "career_goals")
    tech_interests = _validate_list(req.tech_interests, ALLOWED_TECH_INTERESTS, "tech_interests")

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {
            "$set": {
                "onboarding.career_goals": career_goals,
                "onboarding.tech_interests": tech_interests,
                "onboarding.updated_at": datetime.now(timezone.utc),
            }
        },
        upsert=True,
    )
    return {
        "career_goals": career_goals,
        "tech_interests": tech_interests,
    }


@router.post("/restart")
async def restart_onboarding(user=Depends(get_current_user)):
    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {
            "$unset": {
                "onboarding": "",
            }
        },
    )
    return {"message": "Onboarding restarted"}