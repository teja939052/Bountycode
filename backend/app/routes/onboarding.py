from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.middleware.auth import get_current_user
from app.database import users_collection
from bson import ObjectId

logger = __import__("logging").getLogger(__name__)

router = APIRouter(prefix="/api/v1/onboarding", tags=["onboarding"])

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
        "title": "Earn Your First XP",
        "description": "Complete the lesson and watch your progress climb. Gamification keeps you hooked.",
        "type": "action",
        "action": "Complete a lesson to earn XP",
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
        "description": "Free users get 3 lessons per month. Pro unlocks everything for $9/mo or lock in lifetime for $39.",
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
            "$set": {"onboarding_quest.last_active": datetime.now(timezone.utc)},
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

    return {
        "completed_steps": completed_steps,
        "overall_progress": overall_progress,
        "is_complete": is_complete,
    }