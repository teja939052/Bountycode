"""Campus Wars — weekly college challenges + daily quests + streaks + badge economy."""
from datetime import datetime, timezone, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from app.middleware.auth import get_current_user
from app.database import gamification_collection, users_collection
from app.services.gamification import record_practice
import secrets
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/campus-wars", tags=["campus-wars"])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Weekly Challenge Templates (rotate weekly)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WEEKLY_TEMPLATES = [
    {"id": "speed_demon", "title": "Speed Demon", "desc": "Solve 3 problems under 8 min each", "tier": 1, "rewards": [{"type": "coins", "amount": 100}]},
    {"id": "topic_master", "title": "Topic Master", "desc": "Master all problems in one topic (10 solves)", "tier": 5, "rewards": [{"type": "badge", "id": "topic_master"}, {"type": "coins", "amount": 250}]},
    {"id": "streak_champion", "title": "Streak Champion", "desc": "Maintain a 7-day practice streak", "tier": 3, "rewards": [{"type": "xp_boost_2x_24h"}, {"type": "coins", "amount": 150}]},
    {"id": "duel_master", "title": "Duel Master", "desc": "Win 5 college duels", "tier": 7, "rewards": [{"type": "title", "value": "College Duelist"}, {"type": "coins", "amount": 300}]},
    {"id": "boss_slayer", "title": "Boss Slayer", "desc": "Complete 3 boss battles", "tier": 10, "rewards": [{"type": "cosmetic", "value": "boss_frame"}, {"type": "title", "value": "Boss Slayer"}, {"type": "coins", "amount": 500}]},
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Badge tiers (cosmetic + progression)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BADGE_TIERS = {1: "Bronze", 2: "Silver", 3: "Gold"}
BADGE_CATEGORIES = ["speed", "accuracy", "completion", "streak", "duel", "boss", "college"]

COLLEGE_RANKS = {
    "Recruit": {"threshold": 0, "icon": "🌱"},
    "Cadet": {"threshold": 500, "icon": "⭐"},
    "Soldier": {"threshold": 2000, "icon": "⚡"},
    "Veteran": {"threshold": 8000, "icon": "🛡️"},
    "Champion": {"threshold": 25000, "icon": "👑"},
    "Legend": {"threshold": 100000, "icon": "🏆"},
}


def _week_key() -> str:
    """Get the current week key (Monday-based)."""
    today = datetime.now(timezone.utc).date()
    start = today - timedelta(days=today.weekday())
    return start.strftime("%Y-%m-%d")


@router.post("/duel")
async def start_duel(
    college: str = Body(..., embed=True),
    user=Depends(get_current_user),
):
    """Start a college-scoped 1v1 duel. Matches with someone from same college."""
    if not college:
        raise HTTPException(400, "College name required")
    duel_id = secrets.token_hex(6)
    logger.info(f"Duel started: {duel_id} [{college}] by {user.get('name', user['id'])}")

    return {
        "duel_id": duel_id,
        "college": college,
        "status": "waiting",
        "message": "Challenge posted! Share the duel ID with a classmate to compete.",
    }


@router.post("/duel/{duel_id}/join")
async def join_duel(duel_id: str, user=Depends(get_current_user)):
    """Join an existing college duel."""
    from app.services.code_executor import execute_code
    import random
    problems = [
        {"id": "two_sum", "title": "Two Sum", "difficulty": "easy",
         "description": "Given an array, return indices of two numbers adding to target."},
        {"id": "reverse_ll", "title": "Reverse Linked List", "difficulty": "medium",
         "description": "Reverse a singly linked list."},
        {"id": "binary_tree_inorder", "title": "Binary Tree Inorder", "difficulty": "easy",
         "description": "Return inorder traversal of a binary tree."},
        {"id": "valid_parentheses", "title": "Valid Parentheses", "difficulty": "easy",
         "description": "Determine if input has valid parentheses."},
    ]
    problem = random.choice(problems)
    return {
        "duel_id": duel_id,
        "status": "ready",
        "problem": problem,
        "deadline_seconds": 86400,
    }


@router.get("/leaderboard/{college}")
async def get_college_leaderboard(college: str, limit: int = 20):
    """Top performers from a specific college."""
    db_cursor = (
        gamification_collection()
        .find({"college": college, "xp": {"$exists": True}})
        .sort("xp", -1)
        .limit(min(max(limit, 1), 100))
    )
    entries = []
    async for doc in db_cursor:
        total_xp = doc.get("xp", 0)
        rank_name = "Recruit"
        for rank, data in sorted(COLLEGE_RANKS.items(), key=lambda x: x[1]["threshold"]):
            if total_xp >= data["threshold"]:
                rank_name = rank
        entries.append({
            "user_id": doc.get("user_id"),
            "name": doc.get("name", ""),
            "xp": total_xp,
            "rank": rank_name,
            "icon": COLLEGE_RANKS[rank_name]["icon"],
        })
    return {"college": college, "leaderboard": entries}


@router.post("/daily-quests")
async def claim_daily_quest(
    quest_id: str = Body(..., embed=True),
    user=Depends(get_current_user),
):
    """Claim a daily quest reward."""
    user_doc = await users_collection().find_one({"_id": user["_id"]})
    if not user_doc:
        raise HTTPException(404, "User not found")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    claimed_quests = user_doc.get("claimed_dailies", {}).get(today, [])

    if quest_id in claimed_quests:
        raise HTTPException(400, "Already claimed today")

    daily_quests = {
        "solve_3_problems": {"xp": 50, "coins": 20},
        "solve_1_coding": {"xp": 30, "coins": 15},
        "daily_interview": {"xp": 40, "coins": 25},
        "attend_lecture": {"xp": 20, "coins": 10},
        "join_duel": {"xp": 35, "coins": 15},
    }

    if quest_id not in daily_quests:
        raise HTTPException(400, "Invalid quest")

    reward = daily_quests[quest_id]
    await gamification_collection().update_one(
        {"user_id": user["id"]},
        {"$inc": {"xp": reward["xp"], "coins": reward["coins"]},
         "$push": {"claimed_dailies.$[day].completed": quest_id}},
        upsert=True,
    )

    await users_collection().update_one(
        {"_id": user["_id"]},
        {"$set": {f"claimed_dailies.{today}": list(set(claimed_quests + [quest_id]))}},
        upsert=True,
    )

    await record_practice(user["id"], "daily_quest", reward["xp"], {"quest": quest_id})

    return {
        "quest_id": quest_id,
        "xp_gained": reward["xp"],
        "coins_gained": reward["coins"],
        "remaining_quests": [q for q in daily_quests if q not in claimed_quests + [quest_id]],
    }


@router.get("/weekly-challenges")
async def get_weekly_challenges(user=Depends(get_current_user)):
    """Get current weekly challenges + user progress."""
    week = _week_key()
    user_doc = await users_collection().find_one({"_id": user["_id"]})
    progress = user_doc.get("weekly_progress", {}).get(week, {})
    claimed = progress.get("claimed_tiers", [])

    return {
        "week_key": week,
        "challenges": WEEKLY_TEMPLATES,
        "user_progress": progress,
        "claimed_tiers": claimed,
        "college": user_doc.get("college", ""),
    }


@router.post("/weekly-claim")
async def claim_weekly_reward(
    tier: int = Body(..., embed=True),
    user=Depends(get_current_user),
):
    """Claim weekly challenge tier reward."""
    week = _week_key()
    user_doc = await users_collection().find_one({"_id": user["_id"]})
    progress = user_doc.get("weekly_progress", {}).get(week, {})
    claimed = progress.get("claimed_tiers", [])

    if tier in claimed:
        raise HTTPException(400, "Already claimed")

    total_xp = progress.get("xp", 0)
    # Require min XP to claim tier
    if total_xp < tier * 100:
        raise HTTPException(400, f"Need {tier * 100} XP to claim T{ter}")

    rewards = []
    coins_gained = tier * 25
    for template in WEEKLY_TEMPLATES:
        if template["tier"] == tier:
            rewards.extend(template["rewards"])
            coins_gained += 50

    await gamification_collection().update_one(
        {"user_id": user["id"]},
        {"$inc": {"xp": 0, "coins": coins_gained}},
        upsert=True,
    )

    await users_collection().update_one(
        {"_id": user["_id"]},
        {"$set": {f"weekly_progress.{week}.claimed_tiers": claimed + [tier]}},
        upsert=True,
    )

    return {"tier": tier, "coins_gained": coins_gained, "rewards": rewards}


@router.get("/daily-quests")
async def get_daily_quests(user=Depends(get_current_user)):
    """Get available daily quests + claim status."""
    user_doc = await users_collection().find_one({"_id": user["_id"]})
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    claimed = user_doc.get("claimed_dailies", {}).get(today, [])

    quests = [
        {"id": "solve_3_problems", "title": "Problem Solver", "desc": "Solve 3 problems", "xp": 50, "coins": 20},
        {"id": "solve_1_coding", "title": "Coder", "desc": "Solve 1 coding challenge", "xp": 30, "coins": 15},
        {"id": "daily_interview", "title": "Interview Prep", "desc": "Complete 1 mock interview", "xp": 40, "coins": 25},
        {"id": "attend_lecture", "title": "Scholar", "desc": "Attend 1 learning session", "xp": 20, "coins": 10},
        {"id": "join_duel", "title": "Warrior", "desc": "Join a college duel", "xp": 35, "coins": 15},
    ]

    return {
        "date": today,
        "quests": quests,
        "claimed": claimed,
    }


@router.post("/streak")
async def get_streak_bonus(user=Depends(get_current_user)):
    """Get streak bonus (7-day streak = 2x XP for 24h)."""
    user_doc = await users_collection().find_one({"_id": user["_id"]})
    streak = user_doc.get("daily_streak", {}).get("current", 0)

    if streak >= 7:
        await gamification_collection().update_one(
            {"user_id": user["id"]},
            {"$set": {"xp_boost_until": (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()}},
            upsert=True,
        )
        await record_practice(user["id"], "streak_bonus", 100, {"streak": streak})
        return {"granted": True, "bonus": "2x XP (24h)", "streak": streak}

    return {"granted": False, "bonus": None, "streak": streak}


@router.get("/badges")
async def get_badges(user=Depends(get_current_user)):
    """Get user's badge collection."""
    user_doc = await users_collection().find_one({"_id": user["_id"]})
    earned = user_doc.get("badges", [])
    badge_defs = []
    for cat in BADGE_CATEGORIES:
        for tier in [1, 2, 3]:
            badge_id = f"{cat}_{tier}"
            badge_defs.append({
                "id": badge_id,
                "name": f"{BADGE_TIERS[tier]} {cat.title()}",
                "tier": tier,
                "rarity": BADGE_TIERS[tier],
                "earned": badge_id in earned,
            })
    return {"badges": badge_defs, "earned_count": len(earned)}


@router.get("/ranks")
async def get_ranks():
    """Get all college rank tiers."""
    return {"ranks": COLLEGE_RANKS}
