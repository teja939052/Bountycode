"""Guilds/Clans system — team-based gamification for social engagement."""
from datetime import datetime, timezone, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    users_collection,
    gamification_collection,
    guilds_collection,
)
from app.services.gamification import record_practice
import random
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/guilds", tags=["guilds"])

GUILD_PRESETS = [
    {
        "name": "Code Ninjas",
        "emoji": "🥷",
        "color": "#ef4444",
        "description": "Stealthy coders who strike with precision.",
        "bonus": "10% XP boost on all coding challenges",
    },
    {
        "name": "Algo Knights",
        "emoji": "⚔️",
        "color": "#3b82f6",
        "description": "Knights of the algorithm, defending against bugs.",
        "bonus": "Extra hint reveals on boss battles",
    },
    {
        "name": "Debug Dragons",
        "emoji": "🐉",
        "color": "#f59e0b",
        "description": "Fearless debuggers who breathe fire on errors.",
        "bonus": "Double XP on daily challenges",
    },
    {
        "name": "Stack Sorcerers",
        "emoji": "🔮",
        "color": "#8b5cf6",
        "description": "Masters of the data structure arts.",
        "bonus": "Free power-up spins every week",
    },
    {
        "name": "Pixel Rangers",
        "emoji": "🏹",
        "color": "#10b981",
        "description": "Rangers who never miss their target.",
        "bonus": "1.5x streak multiplier",
    },
    {
        "name": "Binary Bandits",
        "emoji": "💰",
        "color": "#f97316",
        "description": "Bandits who loot XP from every challenge.",
        "bonus": "Steal 10% XP from rival guilds on boss wins",
    },
]

GUILD_RANKS = {
    "Recruit": {"min_xp": 0, "color": "#9ca3af"},
    "Member": {"min_xp": 100, "color": "#60a5fa"},
    "Veteran": {"min_xp": 500, "color": "#34d399"},
    "Officer": {"min_xp": 2000, "color": "#fbbf24"},
    "Leader": {"min_xp": 10000, "color": "#f43f5e"},
}


def _get_guild_rank(xp: int) -> str:
    rank = "Recruit"
    for r, data in sorted(GUILD_RANKS.items(), key=lambda x: x[1]["min_xp"]):
        if xp >= data["min_xp"]:
            rank = r
    return rank


@router.get("/presets")
async def get_guild_presets(user=Depends(get_current_user)):
    return {"guilds": GUILD_PRESETS}


@router.post("/create")
async def create_guild(req: dict, user=Depends(get_current_user)):
    name = req.get("name", "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="Guild name is required")
    if len(name) > 30:
        raise HTTPException(status_code=400, detail="Guild name must be 30 characters or less")

    existing = await guilds_collection.find_one({"name": name})
    if existing:
        raise HTTPException(status_code=400, detail="Guild name already taken")

    preset = None
    for p in GUILD_PRESETS:
        if p["name"].lower() == name.lower():
            preset = p
            break

    guild_doc = {
        "name": name,
        "emoji": preset["emoji"] if preset else "🏰",
        "color": preset["color"] if preset else "#6366f1",
        "description": req.get("description", ""),
        "bonus": preset["bonus"] if preset else "No bonus",
        "owner_id": user["id"],
        "members": [
            {
                "user_id": user["id"],
                "role": "leader",
                "joined_at": datetime.now(timezone.utc),
                "xp_contributed": 0,
            }
        ],
        "total_xp": 0,
        "created_at": datetime.now(timezone.utc),
        "is_active": True,
    }
    result = await guilds_collection.insert_one(guild_doc)
    guild_id = str(result.inserted_id)

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$set": {"guild_id": guild_id, "guild_role": "leader"}},
    )

    return {
        "guild_id": guild_id,
        "name": name,
        "owner_id": user["id"],
        "members": 1,
    }


@router.get("/my-guild")
async def get_my_guild(user=Depends(get_current_user)):
    guild_id = user.get("guild_id")
    if not guild_id:
        return {"guild": None, "role": None}

    guild = await guilds_collection.find_one({"_id": ObjectId(guild_id)})
    if not guild:
        return {"guild": None, "role": None}

    guild["id"] = str(guild["_id"])
    guild["members_count"] = len(guild.get("members", []))
    guild["user_role"] = next(
        (m["role"] for m in guild["members"] if m["user_id"] == user["id"]),
        None,
    )
    del guild["_id"]
    return {"guild": guild, "role": guild["user_role"]}


@router.post("/join")
async def join_guild(req: dict, user=Depends(get_current_user)):
    guild_id = req.get("guild_id")
    if not guild_id:
        raise HTTPException(status_code=400, detail="guild_id is required")

    guild = await guilds_collection.find_one({"_id": ObjectId(guild_id)})
    if not guild:
        raise HTTPException(status_code=404, detail="Guild not found")

    if len(guild.get("members", [])) >= 50:
        raise HTTPException(status_code=400, detail="Guild is full (max 50 members)")

    existing_member = any(m["user_id"] == user["id"] for m in guild.get("members", []))
    if existing_member:
        raise HTTPException(status_code=400, detail="Already a member of this guild")

    await guilds_collection.update_one(
        {"_id": ObjectId(guild_id)},
        {"$push": {
            "members": {
                "user_id": user["id"],
                "role": "recruit",
                "joined_at": datetime.now(timezone.utc),
                "xp_contributed": 0,
            }
        }},
    )

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$set": {"guild_id": guild_id, "guild_role": "recruit"}},
    )

    return {"joined": True, "guild_id": guild_id}


@router.post("/leave")
async def leave_guild(user=Depends(get_current_user)):
    guild_id = user.get("guild_id")
    if not guild_id:
        raise HTTPException(status_code=400, detail="Not in a guild")

    await guilds_collection.update_one(
        {"_id": ObjectId(guild_id)},
        {"$pull": {"members": {"user_id": user["id"]}}},
    )

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$unset": {"guild_id": "", "guild_role": ""}},
    )

    return {"left": True}


@router.post("/kick/{member_id}")
async def kick_member(member_id: str, user=Depends(get_current_user)):
    guild_id = user.get("guild_id")
    if not guild_id:
        raise HTTPException(status_code=400, detail="Not in a guild")

    guild = await guilds_collection.find_one({"_id": ObjectId(guild_id)})
    if not guild:
        raise HTTPException(status_code=404, detail="Guild not found")

    user_role = next(
        (m["role"] for m in guild["members"] if m["user_id"] == user["id"]),
        None,
    )
    if user_role not in ("leader", "officer"):
        raise HTTPException(status_code=403, detail="Only leaders and officers can kick members")

    await guilds_collection.update_one(
        {"_id": ObjectId(guild_id)},
        {"$pull": {"members": {"user_id": member_id}}},
    )

    await users_collection.update_one(
        {"_id": ObjectId(member_id)},
        {"$unset": {"guild_id": "", "guild_role": ""}},
    )

    return {"kicked": True, "member_id": member_id}


@router.get("/leaderboard")
async def guild_leaderboard(
    limit: int = Query(20, ge=1, le=50),
    user=Depends(get_current_user),
):
    guilds = await guilds_collection.find(
        {"is_active": True},
    ).sort("total_xp", -1).limit(limit).to_list(limit)

    result = []
    for i, guild in enumerate(guilds):
        guild["id"] = str(guild["_id"])
        guild["rank"] = i + 1
        guild["members_count"] = len(guild.get("members", []))
        guild["owner_name"] = guild.get("owner_id", "")
        del guild["_id"]
        del guild["owner_id"]
        del guild["members"]
        result.append(guild)

    return {"guilds": result, "user_guild_rank": None}


@router.get("/members/{guild_id}")
async def get_guild_members(guild_id: str, user=Depends(get_current_user)):
    guild = await guilds_collection.find_one({"_id": ObjectId(guild_id)})
    if not guild:
        raise HTTPException(status_code=404, detail="Guild not found")

    members = []
    for m in guild.get("members", []):
        member_user = await users_collection.find_one({"_id": ObjectId(m["user_id"])})
        members.append({
            "user_id": m["user_id"],
            "role": m["role"],
            "joined_at": m["joined_at"].isoformat() if isinstance(m["joined_at"], datetime) else str(m["joined_at"]),
            "xp_contributed": m.get("xp_contributed", 0),
            "name": member_user["name"] if member_user else "Unknown",
            "email": member_user["email"] if member_user else "",
            "level": member_user.get("level", 1) if member_user else 1,
        })

    return {"guild_id": guild_id, "members": members, "total": len(members)}


@router.post("/contribute-xp")
async def contribute_guild_xp(req: dict, user=Depends(get_current_user)):
    guild_id = user.get("guild_id")
    if not guild_id:
        raise HTTPException(status_code=400, detail="Not in a guild")

    xp = req.get("xp", 0)
    if xp <= 0:
        raise HTTPException(status_code=400, detail="XP must be positive")

    await guilds_collection.update_one(
        {"_id": ObjectId(guild_id)},
        {"$inc": {"total_xp": xp}},
    )

    await guilds_collection.update_one(
        {"_id": ObjectId(guild_id), "members.user_id": user["id"]},
        {"$inc": {"members.$.xp_contributed": xp}},
    )

    return {"contributed": xp, "guild_id": guild_id}


@router.get("/rank/{guild_id}")
async def get_guild_rank(guild_id: str, user=Depends(get_current_user)):
    guild = await guilds_collection.find_one({"_id": ObjectId(guild_id)})
    if not guild:
        raise HTTPException(status_code=404, detail="Guild not found")

    user_rank = None
    for i, m in enumerate(guild.get("members", [])):
        if m["user_id"] == user["id"]:
            user_rank = i + 1
            break

    return {
        "guild_id": guild_id,
        "guild_name": guild["name"],
        "user_rank": user_rank,
        "total_members": len(guild.get("members", [])),
        "user_xp": next(
            (m["xp_contributed"] for m in guild.get("members", []) if m["user_id"] == user["id"]),
            0,
        ),
    }