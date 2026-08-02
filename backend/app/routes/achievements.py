"""Achievement Chains — multi-step progression system."""
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import users_collection, gamification_collection
from app.services.gamification import record_practice
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/achievements", tags=["achievements"])

ACHIEVEMENT_CHAINS = {
    "first_steps": {
        "name": "First Steps",
        "emoji": "👣",
        "description": "Complete your first steps on PlacementPro",
        "steps": [
            {"id": "complete_onboarding", "name": "Complete Onboarding", "xp": 20, "type": "onboarding_complete"},
            {"id": "solve_first_problem", "name": "Solve First Problem", "xp": 30, "type": "problems_solved", "target": 1},
            {"id": "first_interview", "name": "First Interview", "xp": 50, "type": "interviews_completed", "target": 1},
        ],
        "bonus": {"badge": "Trailblazer", "title": "Trailblazer", "xp_bonus": 100},
    },
    "coding_ninja": {
        "name": "Coding Ninja",
        "emoji": "🥷",
        "description": "Master the art of coding",
        "steps": [
            {"id": "solve_10_problems", "name": "Solve 10 Problems", "xp": 50, "type": "problems_solved", "target": 10},
            {"id": "solve_25_problems", "name": "Solve 25 Problems", "xp": 100, "type": "problems_solved", "target": 25},
            {"id": "solve_50_problems", "name": "Solve 50 Problems", "xp": 200, "type": "problems_solved", "target": 50},
            {"id": "solve_100_problems", "name": "Solve 100 Problems", "xp": 500, "type": "problems_solved", "target": 100},
        ],
        "bonus": {"badge": "Coding Ninja", "title": "Coding Ninja", "xp_bonus": 300},
    },
    "interview_master": {
        "name": "Interview Master",
        "emoji": "🎯",
        "description": "Conquer the interview process",
        "steps": [
            {"id": "complete_5_interviews", "name": "Complete 5 Interviews", "xp": 50, "type": "interviews_completed", "target": 5},
            {"id": "complete_15_interviews", "name": "Complete 15 Interviews", "xp": 100, "type": "interviews_completed", "target": 15},
            {"id": "complete_30_interviews", "name": "Complete 30 Interviews", "xp": 200, "type": "interviews_completed", "target": 30},
        ],
        "bonus": {"badge": "Interview Master", "title": "Interview Master", "xp_bonus": 400},
    },
    "streak_king": {
        "name": "Streak King",
        "emoji": "👑",
        "description": "Maintain the longest streak",
        "steps": [
            {"id": "streak_7", "name": "7-Day Streak", "xp": 30, "type": "streak_days", "target": 7},
            {"id": "streak_14", "name": "14-Day Streak", "xp": 60, "type": "streak_days", "target": 14},
            {"id": "streak_30", "name": "30-Day Streak", "xp": 150, "type": "streak_days", "target": 30},
            {"id": "streak_60", "name": "60-Day Streak", "xp": 300, "type": "streak_days", "target": 60},
        ],
        "bonus": {"badge": "Streak King", "title": "Streak King", "xp_bonus": 200},
    },
    "guild_leader": {
        "name": "Guild Leader",
        "emoji": "⚔️",
        "description": "Lead a guild to victory",
        "steps": [
            {"id": "create_guild", "name": "Create a Guild", "xp": 20, "type": "guild_created"},
            {"id": "guild_5_members", "name": "5 Members in Guild", "xp": 30, "type": "guild_members", "target": 5},
            {"id": "guild_20_members", "name": "20 Members in Guild", "xp": 50, "type": "guild_members", "target": 20},
            {"id": "guild_leaderboard_top3", "name": "Top 3 Guild", "xp": 100, "type": "guild_rank_top3"},
        ],
        "bonus": {"badge": "Guild Leader", "title": "Guild Leader", "xp_bonus": 250},
    },
    "seasonal_champion": {
        "name": "Seasonal Champion",
        "emoji": "🏆",
        "description": "Dominate a seasonal event",
        "steps": [
            {"id": "season_quest_1", "name": "Complete 1 Seasonal Quest", "xp": 20, "type": "seasonal_quests", "target": 1},
            {"id": "season_quest_5", "name": "Complete 5 Seasonal Quests", "xp": 50, "type": "seasonal_quests", "target": 5},
            {"id": "season_quest_10", "name": "Complete 10 Seasonal Quests", "xp": 100, "type": "seasonal_quests", "target": 10},
        ],
        "bonus": {"badge": "Seasonal Champion", "title": "Seasonal Champion", "xp_bonus": 350},
    },
}


@router.get("/chains")
async def get_achievement_chains(user=Depends(get_current_user)):
    user_gam = await gamification_collection.find_one({"user_id": user["id"]})
    completed_chains = user_gam.get("completed_chains", []) if user_gam else []

    chains = []
    for key, chain in ACHIEVEMENT_CHAINS.items():
        completed_steps = user_gam.get("achievement_progress", {}).get(key, {}) if user_gam else {}
        steps_completed = sum(1 for s in chain["steps"] if completed_steps.get(s["id"], {}).get("completed"))
        total_steps = len(chain["steps"])
        is_complete = steps_completed >= total_steps

        chains.append({
            "key": key,
            "name": chain["name"],
            "emoji": chain["emoji"],
            "description": chain["description"],
            "steps": chain["steps"],
            "steps_completed": steps_completed,
            "total_steps": total_steps,
            "is_complete": is_complete,
            "bonus": chain["bonus"],
        })

    return {"chains": chains, "completed_count": len(completed_chains)}


@router.post("/progress")
async def update_achievement_progress(req: dict, user=Depends(get_current_user)):
    step_id = req.get("step_id")
    chain_key = req.get("chain_key")
    xp_earned = req.get("xp", 0)

    if not step_id or not chain_key:
        raise HTTPException(status_code=400, detail="step_id and chain_key are required")

    chain = ACHIEVEMENT_CHAINS.get(chain_key)
    if not chain:
        raise HTTPException(status_code=404, detail="Chain not found")

    step = next((s for s in chain["steps"] if s["id"] == step_id), None)
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")

    await gamification_collection.update_one(
        {"user_id": user["id"]},
        {"$set": {
            f"achievement_progress.{chain_key}.{step_id}": {
                "completed": True,
                "xp_earned": xp_earned,
                "completed_at": datetime.now(timezone.utc),
            }
        }},
        upsert=True,
    )

    # Check if chain is complete
    user_gam = await gamification_collection.find_one({"user_id": user["id"]})
    chain_progress = user_gam.get("achievement_progress", {}).get(chain_key, {}) if user_gam else {}
    all_completed = all(
        chain_progress.get(s["id"], {}).get("completed") for s in chain["steps"]
    )

    bonus_xp = 0
    if all_completed:
        bonus_xp = chain["bonus"].get("xp_bonus", 0)
        await gamification_collection.update_one(
            {"user_id": user["id"]},
            {"$push": {"completed_chains": chain_key}},
            upsert=True,
        )

    return {
        "step_id": step_id,
        "chain_key": chain_key,
        "xp_earned": xp_earned,
        "bonus_xp": bonus_xp,
        "total_xp": xp_earned + bonus_xp,
        "chain_complete": all_completed,
    }


@router.get("/stats")
async def get_achievement_stats(user=Depends(get_current_user)):
    user_gam = await gamification_collection.find_one({"user_id": user["id"]})
    achievement_progress = user_gam.get("achievement_progress", {}) if user_gam else {}
    completed_chains = user_gam.get("completed_chains", []) if user_gam else []

    total_steps = sum(len(ACHIEVEMENT_CHAINS[k]["steps"]) for k in ACHIEVEMENT_CHAINS)
    completed_steps = sum(
        1 for chain_key, progress in achievement_progress.items()
        for step_id, step_data in progress.items()
        if step_data.get("completed")
    )

    return {
        "total_chains": len(ACHIEVEMENT_CHAINS),
        "completed_chains": len(completed_chains),
        "total_steps": total_steps,
        "completed_steps": completed_steps,
        "progress_percentage": round(completed_steps / total_steps * 100, 1) if total_steps > 0 else 0,
        "completed_chain_keys": completed_chains,
    }