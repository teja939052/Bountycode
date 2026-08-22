"""
Rank / Honor System — Codewars-style Kyu/Dan ranking.
Tracks honor points from activities and calculates rank.
"""
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import users_collection

router = APIRouter(prefix="/api/v1/rank", tags=["rank"])

# ─── Rank Calculation ──────────────────────────────────────────────────

# 8 kyu (beginner) -> 1 kyu -> 1 dan -> 6 dan (master)
# Formula: kyu = 8 - floor(honor / 25), dan = 1 + floor((honor - 200) / 50)

HONOR_ACTIONS = {
    "solve_problem": 5,
    "solve_optimal": 3,
    "win_battle": 15,
    "create_scrim": 10,
    "daily_streak_7": 20,
    "daily_streak_30": 50,
    "daily_login": 1,
    "perfect_score": 10,
}

AVAILABLE_BADGES = [
    {"id": "first_problem", "name": "First Steps", "description": "Solve your first problem", "icon": "🌟", "honor_required": 0},
    {"id": "ten_problems", "name": "Problem Solver", "description": "Solve 10 problems", "icon": "📚", "honor_required": 50},
    {"id": "fifty_problems", "name": "Dedicated Coder", "description": "Solve 50 problems", "icon": "💪", "honor_required": 150},
    {"id": "first_battle", "name": "Warrior", "description": "Win your first battle", "icon": "⚔️", "honor_required": 15},
    {"id": "ten_battles", "name": "Battle Hardened", "description": "Win 10 battles", "icon": "🛡️", "honor_required": 150},
    {"id": "kyu_8", "name": "8th Kyu", "description": "Reach 8 kyu rank", "icon": "🥉", "honor_required": 0},
    {"id": "kyu_5", "name": "5th Kyu", "description": "Reach 5 kyu rank", "icon": "🥈", "honor_required": 75},
    {"id": "kyu_1", "name": "1st Kyu", "description": "Reach 1 kyu rank", "icon": "🥇", "honor_required": 175},
    {"id": "dan_1", "name": "1st Dan", "description": "Reach 1 dan rank", "icon": "🔴", "honor_required": 200},
    {"id": "dan_3", "name": "3rd Dan", "description": "Reach 3 dan rank", "icon": "💎", "honor_required": 300},
    {"id": "dan_6", "name": "Grandmaster", "description": "Reach 6 dan rank", "icon": "👑", "honor_required": 450},
    {"id": "streak_7", "name": "Weekly Streak", "description": "Maintain 7-day streak", "icon": "🔥", "honor_required": 20},
    {"id": "streak_30", "name": "Monthly Streak", "description": "Maintain 30-day streak", "icon": "💥", "honor_required": 50},
    {"id": "perfect_score", "name": "Perfectionist", "description": "Get a perfect score", "icon": "⭐", "honor_required": 10},
]


def calculate_rank(honor: int) -> dict:
    if honor < 200:
        rank_num = max(1, min(8, 8 - honor // 25))
        rank_type = "kyu"
        rank_title = f"{rank_num} kyu"
    else:
        rank_num = min(6, 1 + (honor - 200) // 50)
        rank_type = "dan"
        rank_title = f"{rank_num} dan"

    return {
        "rank_number": rank_num,
        "rank_type": rank_type,
        "rank_title": rank_title,
    }


def calculate_next_rank_honor(honor: int) -> dict:
    if honor < 200:
        current_tier = honor // 25
        next_honor = (current_tier + 1) * 25 if current_tier < 7 else 200
        honor_for_current = current_tier * 25
        honor_for_next = next_honor
        return {
            "current_tier_honor": honor_for_current,
            "next_rank_honor": honor_for_next,
            "honor_needed": next_honor - honor,
            "progress_percent": min(100, round((honor - honor_for_current) / max(1, next_honor - honor_for_current) * 100, 1)),
        }
    else:
        dan_tier = (honor - 200) // 50
        next_dan_honor = 200 + (dan_tier + 1) * 50 if dan_tier < 5 else 200 + 6 * 50
        honor_for_current = 200 + dan_tier * 50
        honor_for_next = next_dan_honor
        return {
            "current_tier_honor": honor_for_current,
            "next_rank_honor": honor_for_next,
            "honor_needed": max(0, next_dan_honor - honor),
            "progress_percent": min(100, round((honor - honor_for_current) / max(1, honor_for_next - honor_for_current) * 100, 1)),
        }


def get_earned_badges(honor: int) -> list:
    earned = []
    for badge in AVAILABLE_BADGES:
        if honor >= badge["honor_required"]:
            earned.append(badge)
    return earned


# ─── Helper to ensure user has honor field ─────────────────────────────

async def _ensure_honor_field(user_id: str):
    await users_collection().update_one(
        {"_id": ObjectId(user_id)},
        {"$setOnInsert": {"honor": 0}},
        upsert=True,
    )


# ─── Routes ────────────────────────────────────────────────────────────

@router.get("/profile")
async def get_rank_profile(user=Depends(get_current_user)):
    """Get user's rank info: rank title, honor, progress."""
    uid = user["id"]
    await _ensure_honor_field(uid)

    user_doc = await users_collection().find_one({"_id": ObjectId(uid)})
    honor = user_doc.get("honor", 0) if user_doc else 0

    rank_info = calculate_rank(honor)
    next_rank_info = calculate_next_rank_honor(honor)
    badges = get_earned_badges(honor)

    return {
        "honor": honor,
        **rank_info,
        **next_rank_info,
        "badges": badges,
        "badge_count": len(badges),
        "total_badges": len(AVAILABLE_BADGES),
    }


@router.post("/award-honor")
async def award_honor(
    action: str = Query(..., min_length=1, max_length=50),
    user=Depends(get_current_user),
):
    """Award honor points for server-verified actions. Amount is always
    derived server-side from HONOR_ACTIONS — client-supplied amounts are
    never honored."""
    uid = user["id"]

    if action not in HONOR_ACTIONS:
        raise HTTPException(status_code=400, detail=f"Unknown action: {action}")

    amount = HONOR_ACTIONS[action]
    await _ensure_honor_field(uid)

    await users_collection().update_one(
        {"_id": ObjectId(uid)},
        {"$inc": {"honor": amount}},
    )

    user_doc = await users_collection().find_one({"_id": ObjectId(uid)})
    new_honor = user_doc.get("honor", 0) if user_doc else amount
    rank_info = calculate_rank(new_honor)

    return {
        "honor_awarded": amount,
        "total_honor": new_honor,
        "action": action,
        **rank_info,
    }


@router.get("/leaderboard")
async def get_rank_leaderboard(
    page: int = Query(1, ge=1, le=100),
    limit: int = Query(20, ge=1, le=100),
):
    """Top users by honor points."""
    skip = (page - 1) * limit
    cursor = users_collection().find(
        {"honor": {"$exists": True}},
        {"name": 1, "honor": 1},
    ).sort("honor", -1).skip(skip).limit(limit)

    entries = []
    rank_num = skip + 1
    async for doc in cursor:
        honor = doc.get("honor", 0)
        rank_data = calculate_rank(honor)
        entries.append({
            "rank": rank_num,
            "user_id": str(doc["_id"]),
            "name": doc.get("name", "Unknown"),
            "honor": honor,
            **rank_data,
        })
        rank_num += 1

    total = await users_collection().count_documents({"honor": {"$exists": True}})

    return {
        "leaderboard": entries,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": max(1, (total + limit - 1) // limit),
    }


@router.get("/badges")
async def get_all_badges():
    """All available badges with unlock criteria."""
    return {"badges": AVAILABLE_BADGES, "total": len(AVAILABLE_BADGES)}
