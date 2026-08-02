"""Tournament Bracket system — structured competitive tournaments."""
from datetime import datetime, timezone, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import users_collection, gamification_collection
from app.services.gamification import record_practice
import random
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/tournaments", tags=["tournaments"])

TOURNAMENT_PRESETS = [
    {
        "name": "Weekly Sprint",
        "emoji": "⚡",
        "format": "single_elimination",
        "max_participants": 16,
        "duration_hours": 24,
        "xp_reward": 200,
        "badge_reward": "Sprint Champion",
        "difficulty": "medium",
    },
    {
        "name": "Monthly Showdown",
        "emoji": "🏆",
        "format": "double_elimination",
        "max_participants": 32,
        "duration_hours": 72,
        "xp_reward": 500,
        "badge_reward": "Monthly Champion",
        "difficulty": "hard",
    },
    {
        "name": "Grand Championship",
        "emoji": "👑",
        "format": "round_robin",
        "max_participants": 8,
        "duration_hours": 168,
        "xp_reward": 1000,
        "badge_reward": "Grand Champion",
        "difficulty": "expert",
    },
]


@router.get("/presets")
async def get_tournament_presets(user=Depends(get_current_user)):
    return {"tournaments": TOURNAMENT_PRESETS}


@router.post("/create")
async def create_tournament(req: dict, user=Depends(get_current_user)):
    name = req.get("name", "").strip()
    preset_key = req.get("preset_key")

    if not name:
        raise HTTPException(status_code=400, detail="Tournament name is required")

    preset = None
    if preset_key:
        preset = next((t for t in TOURNAMENT_PRESETS if t["name"].lower() == preset_key.lower()), None)

    tournament_doc = {
        "name": name,
        "emoji": preset["emoji"] if preset else "🏟️",
        "format": preset["format"] if preset else "single_elimination",
        "max_participants": preset["max_participants"] if preset else 16,
        "duration_hours": preset["duration_hours"] if preset else 24,
        "xp_reward": preset["xp_reward"] if preset else 200,
        "badge_reward": preset["badge_reward"] if preset else "Tournament Champion",
        "difficulty": preset["difficulty"] if preset else "medium",
        "host_id": user["id"],
        "participants": [
            {
                "user_id": user["id"],
                "joined_at": datetime.now(timezone.utc),
                "bracket_position": 0,
                "wins": 0,
                "losses": 0,
            }
        ],
        "bracket": [],
        "status": "waiting",
        "created_at": datetime.now(timezone.utc),
        "starts_at": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    result = await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$push": {"tournaments_hosted": tournament_doc["name"]}},
        upsert=True,
    )

    return {
        "tournament_id": "tournament_" + user["id"][:8],
        "name": name,
        "host_id": user["id"],
        "participants": 1,
    }


@router.get("/active")
async def get_active_tournaments(user=Depends(get_current_user)):
    tournaments = [
        {
            "tournament_id": "tournament_weekly_sprint",
            "name": "Weekly Sprint",
            "emoji": "⚡",
            "format": "single_elimination",
            "status": "active",
            "participants": 8,
            "max_participants": 16,
            "xp_reward": 200,
            "badge_reward": "Sprint Champion",
            "round": "Quarterfinals",
            "starts_at": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
        },
        {
            "tournament_id": "tournament_monthly_showdown",
            "name": "Monthly Showdown",
            "emoji": "🏆",
            "format": "double_elimination",
            "status": "active",
            "participants": 16,
            "max_participants": 32,
            "xp_reward": 500,
            "badge_reward": "Monthly Champion",
            "round": "Round of 16",
            "starts_at": (datetime.now(timezone.utc) - timedelta(hours=12)).isoformat(),
        },
    ]
    return {"tournaments": tournaments}


@router.post("/join/{tournament_id}")
async def join_tournament(tournament_id: str, user=Depends(get_current_user)):
    tournament = await users_collection.find_one(
        {"tournaments_hosted": {"$regex": tournament_id}},
    )

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$push": {"tournaments_joined": tournament_id}},
        upsert=True,
    )

    return {"joined": True, "tournament_id": tournament_id}


@router.post("/submit/{tournament_id}")
async def submit_tournament_result(
    tournament_id: str,
    req: dict,
    user=Depends(get_current_user),
):
    opponent_id = req.get("opponent_id")
    result = req.get("result")

    if result not in ("win", "loss", "draw"):
        raise HTTPException(status_code=400, detail="Invalid result")

    xp_earned = 50 if result == "win" else 10
    if result == "draw":
        xp_earned = 25

    update_data = {"xp": xp_earned}
    if result == "win":
        update_data["tournament_wins"] = 1

    await gamification_collection.update_one(
        {"user_id": user["id"]},
        {"$inc": update_data},
        upsert=True,
    )

    await record_practice(user["id"], "tournament", xp_earned)

    return {
        "tournament_id": tournament_id,
        "result": result,
        "xp_earned": xp_earned,
        "opponent_id": opponent_id,
    }


@router.get("/leaderboard/{tournament_id}")
async def get_tournament_leaderboard(tournament_id: str, user=Depends(get_current_user)):
    users = await users_collection.find(
        {"tournaments_joined": {"$regex": tournament_id}},
    ).sort("honor", -1).limit(16).to_list(16)

    leaderboard = []
    for i, u in enumerate(users):
        leaderboard.append({
            "rank": i + 1,
            "user_id": u["_id"],
            "name": u.get("name", "Unknown"),
            "wins": u.get("tournament_wins", 0),
            "honor": u.get("honor", 0),
        })

    return {"tournament_id": tournament_id, "leaderboard": leaderboard}


@router.get("/history")
async def get_tournament_history(user=Depends(get_current_user)):
    tournaments_joined = user.get("tournaments_joined", [])
    tournaments_hosted = user.get("tournaments_hosted", [])

    return {
        "joined": tournaments_joined,
        "hosted": tournaments_hosted,
        "total_tournaments": len(set(tournaments_joined + tournaments_hosted)),
    }