"""Study Goals — student-set learning goals with progress tracking and streaks.

Non-AI feature: goals track any metric (problems solved, XP earned, time studied,
tests attempted). Students build daily streaks and earn a completion bonus.
Free tier: max 3 active goals. Pro/Lifetime: unlimited.
"""
import uuid
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, Body
from app.middleware.auth import get_current_user
from app.database import gamification_collection
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/goals", tags=["goals"])

VALID_METRICS = {"problems", "xp", "time", "tests", "interviews", "lessons", "streak"}
FREE_TIER_GOALS = 3
COMPLETION_BONUS_XP = 50


def _is_pro(user) -> bool:
    return user.get("plan") in ("pro", "lifetime") or user.get("is_admin")


@router.get("/")
async def list_goals(user=Depends(get_current_user)):
    profile = await gamification_collection.find_one({"user_id": user["id"]})
    goals = (profile.get("goals") if profile else []) or []
    now = datetime.now(timezone.utc)
    enriched = []
    for g in goals:
        progress = g.get("progress", 0)
        target = g.get("target", 1)
        pct = round((progress / target) * 100) if target > 0 else 0
        deadline = g.get("deadline")
        enriched.append({
            "id": g["id"],
            "title": g["title"],
            "metric": g["metric"],
            "target": target,
            "progress": progress,
            "progress_pct": min(100, pct),
            "deadline": deadline,
            "streak": g.get("streak", 0),
            "completed": g.get("completed", False),
            "created_at": g.get("created_at"),
        })
    return {"goals": enriched}


@router.post("/create")
async def create_goal(goal: dict = Body(...), user=Depends(get_current_user)):
    title = (goal.get("title") or "").strip()[:120]
    if not title:
        raise HTTPException(400, "title is required")
    metric = goal.get("metric", "problems")
    if metric not in VALID_METRICS:
        raise HTTPException(400, f"metric must be one of: {', '.join(sorted(VALID_METRICS))}")
    try:
        target = int(goal.get("target"))
        if target <= 0:
            raise ValueError
    except (TypeError, ValueError):
        raise HTTPException(400, "target must be a positive integer")

    deadline = goal.get("deadline")
    if deadline:
        try:
            datetime.fromisoformat(deadline.replace("Z", "+00:00"))
        except ValueError:
            raise HTTPException(400, "deadline must be ISO date string")

    # Free-tier goal cap
    if not _is_pro(user):
        profile = await gamification_collection.find_one({"user_id": user["id"]})
        active = [g for g in (profile.get("goals") if profile else []) or [] if not g.get("completed")]
        if len(active) >= FREE_TIER_GOALS:
            raise HTTPException(402, f"Free tier limited to {FREE_TIER_GOALS} active goals. Upgrade for unlimited.")

    g = {
        "id": uuid.uuid4().hex[:10],
        "title": title,
        "metric": metric,
        "target": target,
        "progress": 0,
        "streak": 0,
        "deadline": deadline,
        "completed": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await gamification_collection.update_one(
        {"user_id": user["id"]},
        {"$push": {"goals": g}},
        upsert=True,
    )
    return {"goal": g, "created": True}


@router.post("/{goal_id}/track")
async def track_progress(goal_id: str, event: dict = Body(default=None), user=Depends(get_current_user)):
    """Increment a goal's progress. Body: {metric, amount}."""
    amount = 1
    if event:
        try:
            amount = max(0, int(event.get("amount", 1)))
        except (TypeError, ValueError):
            amount = 1

    profile = await gamification_collection.find_one({"user_id": user["id"]})
    if not profile:
        raise HTTPException(404, "Goal not found")
    goals = profile.get("goals") or []
    idx = next((i for i, g in enumerate(goals) if g.get("id") == goal_id), None)
    if idx is None:
        raise HTTPException(404, "Goal not found")
    if goals[idx].get("completed"):
        return {"goal_id": goal_id, "progress": goals[idx]["progress"], "completed": True, "message": "Already completed"}

    goals[idx]["progress"] = goals[idx].get("progress", 0) + amount
    # Streak: consecutive track events on different days
    today = datetime.now(timezone.utc).date().isoformat()
    if goals[idx].get("last_track_day") == today:
        goals[idx]["streak"] = goals[idx].get("streak", 0)
    else:
        goals[idx]["streak"] = goals[idx].get("streak", 0) + 1
        goals[idx]["last_track_day"] = today

    completed_now = goals[idx]["progress"] >= goals[idx]["target"]
    if completed_now and not goals[idx].get("completed"):
        goals[idx]["completed"] = True
        await record_practice(user["id"], "coding", COMPLETION_BONUS_XP, {"source": "goal_completion"})

    await gamification_collection.update_one(
        {"user_id": user["id"]},
        {"$set": {"goals": goals}},
    )
    return {
        "goal_id": goal_id,
        "progress": goals[idx]["progress"],
        "target": goals[idx]["target"],
        "completed": goals[idx].get("completed", False),
        "streak": goals[idx].get("streak", 0),
        "bonus_xp": COMPLETION_BONUS_XP if completed_now else 0,
    }


@router.delete("/{goal_id}")
async def delete_goal(goal_id: str, user=Depends(get_current_user)):
    profile = await gamification_collection.find_one({"user_id": user["id"]})
    if not profile:
        raise HTTPException(404, "Goal not found")
    goals = profile.get("goals") or []
    new_goals = [g for g in goals if g.get("id") != goal_id]
    if len(new_goals) == len(goals):
        raise HTTPException(404, "Goal not found")
    await gamification_collection.update_one({"user_id": user["id"]}, {"$set": {"goals": new_goals}})
    return {"deleted": True}
