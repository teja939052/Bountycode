"""Seasonal Events — limited-time challenges with exclusive rewards."""
from datetime import datetime, timezone, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    users_collection,
    gamification_collection,
)
from app.services.gamification import record_practice
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/seasons", tags=["seasons"])

SEASONS = {
    "winter-2026": {
        "name": "Winter Frost Challenge",
        "emoji": "❄️",
        "start": "2026-12-01T00:00:00Z",
        "end": "2027-02-28T23:59:59Z",
        "description": "Brave the cold and earn exclusive winter rewards!",
        "daily_quests": [
            {"id": "solve_3", "name": "Frost Fighter", "desc": "Solve 3 problems", "xp": 30, "type": "problems_solved", "target": 3},
            {"id": "streak_5", "name": "Warm Streak", "desc": "Maintain a 5-day streak", "xp": 50, "type": "streak_days", "target": 5},
            {"id": "interview_1", "name": "Ice Interview", "desc": "Complete 1 interview", "xp": 40, "type": "interviews_completed", "target": 1},
        ],
        "bonus_rewards": {"badge": "Frost Warrior", "title": "Frost Warrior", "xp_multiplier": 1.5},
    },
    "spring-2027": {
        "name": "Spring Bloom Marathon",
        "emoji": "🌸",
        "start": "2027-03-01T00:00:00Z",
        "end": "2027-05-31T23:59:59Z",
        "description": "Bloom your skills this spring with exclusive challenges!",
        "daily_quests": [
            {"id": "solve_5", "name": "Bloom Seeker", "desc": "Solve 5 problems", "xp": 50, "type": "problems_solved", "target": 5},
            {"id": "streak_7", "name": "Spring Streak", "desc": "Maintain a 7-day streak", "xp": 70, "type": "streak_days", "target": 7},
            {"id": "company_3", "name": "Company Prep", "desc": "Prep for 3 companies", "xp": 60, "type": "companies_prepared", "target": 3},
        ],
        "bonus_rewards": {"badge": "Spring Bloom", "title": "Spring Bloom", "xp_multiplier": 1.5},
    },
    "summer-2027": {
        "name": "Summer Code Sprint",
        "emoji": "☀️",
        "start": "2027-06-01T00:00:00Z",
        "end": "2027-08-31T23:59:59Z",
        "description": "Sprint through the summer with epic coding challenges!",
        "daily_quests": [
            {"id": "solve_7", "name": "Sun Solver", "desc": "Solve 7 problems", "xp": 70, "type": "problems_solved", "target": 7},
            {"id": "streak_10", "name": "Hot Streak", "desc": "Maintain a 10-day streak", "xp": 100, "type": "streak_days", "target": 10},
            {"id": "boss_1", "name": "Boss Slayer", "desc": "Defeat 1 boss battle", "xp": 100, "type": "bosses_defeated", "target": 1},
        ],
        "bonus_rewards": {"badge": "Summer Champion", "title": "Summer Champion", "xp_multiplier": 2.0},
    },
    "fall-2027": {
        "name": "Autumn Harvest Quest",
        "emoji": "🍂",
        "start": "2027-09-01T00:00:00Z",
        "end": "2027-11-30T23:59:59Z",
        "description": "Harvest XP and rewards this autumn season!",
        "daily_quests": [
            {"id": "solve_10", "name": "Harvest Hunter", "desc": "Solve 10 problems", "xp": 100, "type": "problems_solved", "target": 10},
            {"id": "streak_14", "name": "Harvest Streak", "desc": "Maintain a 14-day streak", "xp": 150, "type": "streak_days", "target": 14},
            {"id": "guild_1", "name": "Guild Helper", "desc": "Contribute to your guild", "xp": 80, "type": "guild_xp", "target": 1},
        ],
        "bonus_rewards": {"badge": "Autumn Collector", "title": "Autumn Collector", "xp_multiplier": 1.5},
    },
}

ACTIVE_SEASON_KEY = "summer-2027"


def _get_active_season():
    now = datetime.now(timezone.utc)
    for key, season in SEASONS.items():
        start = datetime.fromisoformat(season["start"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(season["end"].replace("Z", "+00:00"))
        if start <= now <= end:
            return key, season
    return None, None


@router.get("/current")
async def get_current_season(user=Depends(get_current_user)):
    key, season = _get_active_season()
    if not season:
        return {"season": None, "message": "No active seasonal event"}

    user_gam = await gamification_collection.find_one({"user_id": user["id"]})
    progress = user_gam.get("season_progress", {}).get(key, {}) if user_gam else {}

    return {
        "season_key": key,
        "season": {
            "name": season["name"],
            "emoji": season["emoji"],
            "description": season["description"],
            "start": season["start"],
            "end": season["end"],
            "bonus_rewards": season["bonus_rewards"],
        },
        "daily_quests": season["daily_quests"],
        "progress": progress,
        "days_remaining": (datetime.fromisoformat(season["end"].replace("Z", "+00:00")) - datetime.now(timezone.utc)).days,
    }


@router.get("/all")
async def get_all_seasons(user=Depends(get_current_user)):
    results = []
    for key, season in SEASONS.items():
        start = datetime.fromisoformat(season["start"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(season["end"].replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        is_active = start <= now <= end
        results.append({
            "key": key,
            "name": season["name"],
            "emoji": season["emoji"],
            "description": season["description"],
            "start": season["start"],
            "end": season["end"],
            "is_active": is_active,
            "bonus_rewards": season["bonus_rewards"],
        })
    return {"seasons": results}


@router.post("/progress")
async def update_season_progress(req: dict, user=Depends(get_current_user)):
    key, season = _get_active_season()
    if not season:
        raise HTTPException(status_code=400, detail="No active seasonal event")

    quest_id = req.get("quest_id")
    xp_earned = req.get("xp", 0)

    if not quest_id:
        raise HTTPException(status_code=400, detail="quest_id is required")

    quest = next((q for q in season["daily_quests"] if q["id"] == quest_id), None)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")

    await gamification_collection.update_one(
        {"user_id": user["id"]},
        {"$set": {
            f"season_progress.{key}.{quest_id}": {
                "completed": True,
                "xp_earned": xp_earned,
                "completed_at": datetime.now(timezone.utc),
            }
        }},
        upsert=True,
    )

    multiplier = season["bonus_rewards"].get("xp_multiplier", 1.0)
    bonus_xp = int(xp_earned * multiplier)

    return {
        "quest_id": quest_id,
        "xp_earned": xp_earned,
        "bonus_xp": bonus_xp,
        "multiplier": multiplier,
        "total_xp": xp_earned + bonus_xp,
    }


@router.get("/leaderboard/{season_key}")
async def get_season_leaderboard(season_key: str, user=Depends(get_current_user)):
    if season_key not in SEASONS:
        raise HTTPException(status_code=404, detail="Season not found")

    users = await users_collection.find(
        {"season_progress": {"$exists": True}},
    ).sort("honor", -1).limit(50).to_list(50)

    leaderboard = []
    for i, u in enumerate(users):
        season_progress = u.get("season_progress", {}).get(season_key, {})
        total_xp = sum(
            v.get("xp_earned", 0) for v in season_progress.values() if isinstance(v, dict)
        )
        leaderboard.append({
            "rank": i + 1,
            "user_id": u["_id"],
            "name": u.get("name", "Unknown"),
            "total_xp": total_xp,
            "quests_completed": len(season_progress),
        })

    return {"season_key": season_key, "leaderboard": leaderboard}