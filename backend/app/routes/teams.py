"""Team Competitions — college/company-based team rankings."""
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import users_collection, gamification_collection
from app.services.gamification import record_practice
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/teams", tags=["teams"])

TEAM_PRESETS = [
    {"name": "IIT Bombay", "emoji": "🏛️", "color": "#ef4444"},
    {"name": "IIT Delhi", "emoji": "🎓", "color": "#3b82f6"},
    {"name": "IIT Madras", "emoji": "⚙️", "color": "#10b981"},
    {"name": "IIT Kharagpur", "emoji": "🔧", "color": "#f59e0b"},
    {"name": "IIT Kanpur", "emoji": "🚀", "color": "#8b5cf6"},
    {"name": "IIT Roorkee", "emoji": "🏗️", "color": "#ec4899"},
    {"name": "BITS Pilani", "emoji": "💡", "color": "#14b8a6"},
    {"name": "NIT Trichy", "emoji": "🏅", "color": "#f97316"},
    {"name": "Google", "emoji": "🔍", "color": "#4285f4"},
    {"name": "Microsoft", "emoji": "🪟", "color": "#00a4ef"},
    {"name": "Amazon", "emoji": "📦", "color": "#ff9900"},
    {"name": "Meta", "emoji": "👤", "color": "#1877f2"},
]


@router.get("/presets")
async def get_team_presets(user=Depends(get_current_user)):
    return {"teams": TEAM_PRESETS}


@router.post("/create")
async def create_team(req: dict, user=Depends(get_current_user)):
    name = req.get("name", "").strip()
    college = req.get("college", "")
    team_type = req.get("type", "college")

    if not name:
        raise HTTPException(status_code=400, detail="Team name is required")

    team_doc = {
        "name": name,
        "emoji": req.get("emoji", "🏆"),
        "color": req.get("color", "#6366f1"),
        "type": team_type,
        "college": college,
        "owner_id": user["id"],
        "members": [
            {
                "user_id": user["id"],
                "role": "captain",
                "joined_at": datetime.now(timezone.utc),
                "xp_contributed": 0,
            }
        ],
        "total_xp": 0,
        "wins": 0,
        "losses": 0,
        "created_at": datetime.now(timezone.utc),
        "is_active": True,
    }
    result = await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$set": {
            "team_id": "team_" + user["id"][:8],
            "team_role": "captain",
        }},
        upsert=True,
    )

    return {
        "team_id": "team_" + user["id"][:8],
        "name": name,
        "owner_id": user["id"],
        "members": 1,
    }


@router.get("/my-team")
async def get_my_team(user=Depends(get_current_user)):
    team_id = user.get("team_id")
    if not team_id:
        return {"team": None, "role": None}

    team = await users_collection.find_one({"team_id": team_id})
    if not team:
        return {"team": None, "role": None}

    team["id"] = team["_id"]
    team["members_count"] = len(team.get("members", []))
    team["user_role"] = next(
        (m["role"] for m in team["members"] if m["user_id"] == user["id"]),
        None,
    )
    del team["_id"]
    return {"team": team, "role": team["user_role"]}


@router.post("/join")
async def join_team(req: dict, user=Depends(get_current_user)):
    team_id = req.get("team_id")
    if not team_id:
        raise HTTPException(status_code=400, detail="team_id is required")

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$set": {"team_id": team_id, "team_role": "member"}},
    )

    return {"joined": True, "team_id": team_id}


@router.post("/leave")
async def leave_team(user=Depends(get_current_user)):
    team_id = user.get("team_id")
    if not team_id:
        raise HTTPException(status_code=400, detail="Not in a team")

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$unset": {"team_id": "", "team_role": ""}},
    )

    return {"left": True}


@router.get("/leaderboard")
async def team_leaderboard(
    limit: int = Query(20, ge=1, le=50),
    user=Depends(get_current_user),
):
    users = await users_collection.find(
        {"team_id": {"$exists": True}},
    ).sort("honor", -1).limit(limit).to_list(limit)

    teams = {}
    for u in users:
        tid = u.get("team_id")
        if tid not in teams:
            teams[tid] = {
                "team_id": tid,
                "name": u.get("team_name", tid),
                "emoji": u.get("team_emoji", "🏆"),
                "total_xp": 0,
                "members": 0,
                "wins": 0,
                "losses": 0,
            }
        teams[tid]["total_xp"] += u.get("honor", 0)
        teams[tid]["members"] += 1

    leaderboard = sorted(teams.values(), key=lambda t: t["total_xp"], reverse=True)
    for i, team in enumerate(leaderboard):
        team["rank"] = i + 1

    return {"teams": leaderboard[:20]}


@router.post("/contribute-xp")
async def contribute_team_xp(req: dict, user=Depends(get_current_user)):
    team_id = user.get("team_id")
    if not team_id:
        raise HTTPException(status_code=400, detail="Not in a team")

    xp = req.get("xp", 0)
    if xp <= 0:
        raise HTTPException(status_code=400, detail="XP must be positive")

    await users_collection.update_one(
        {"team_id": team_id},
        {"$inc": {"total_xp": xp}},
    )

    return {"contributed": xp, "team_id": team_id}


@router.get("/college-leaderboard")
async def college_leaderboard(user=Depends(get_current_user)):
    users = await users_collection.find(
        {"college": {"$exists": True}},
    ).sort("honor", -1).limit(50).to_list(50)

    colleges = {}
    for u in users:
        college = u.get("college", "Unknown")
        if college not in colleges:
            colleges[college] = {
                "college": college,
                "total_xp": 0,
                "members": 0,
                "top_player": u.get("name", "Unknown"),
            }
        colleges[college]["total_xp"] += u.get("honor", 0)
        colleges[college]["members"] += 1

    leaderboard = sorted(colleges.values(), key=lambda c: c["total_xp"], reverse=True)
    for i, college in enumerate(leaderboard):
        college["rank"] = i + 1

    return {"colleges": leaderboard[:20]}