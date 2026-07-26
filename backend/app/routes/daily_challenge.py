"""
Daily Challenge & Leagues — Retention engine with daily problems and competitive leagues.
"""
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    curated_questions_collection, solved_problems_collection,
    question_answers_collection, gamification_collection, users_collection
)
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/daily", tags=["daily-challenge"])

# League configuration
LEAGUES = {
    "bronze": {"name": "Bronze", "min_xp": 0, "max_xp": 999, "emoji": "🥉", "color": "#CD7F32"},
    "silver": {"name": "Silver", "min_xp": 1000, "max_xp": 4999, "emoji": "🥈", "color": "#C0C0C0"},
    "gold": {"name": "Gold", "min_xp": 5000, "max_xp": 14999, "emoji": "🥇", "color": "#FFD700"},
    "platinum": {"name": "Platinum", "min_xp": 15000, "max_xp": 49999, "emoji": "💎", "color": "#E5E4E2"},
    "diamond": {"name": "Diamond", "min_xp": 50000, "max_xp": float('inf'), "emoji": "👑", "color": "#B9F2FF"},
}

# Daily challenge categories (rotate daily)
DAILY_CATEGORIES = [
    {"day": 0, "category": "Arrays", "difficulty": "medium", "focus": "Two Pointers & Sliding Window"},
    {"day": 1, "category": "Linked Lists", "difficulty": "medium", "focus": "Reversal & Cycle Detection"},
    {"day": 2, "category": "Trees", "difficulty": "medium", "focus": "DFS & BFS Traversals"},
    {"day": 3, "category": "Dynamic Programming", "difficulty": "medium", "focus": "1D DP Patterns"},
    {"day": 4, "category": "Graphs", "difficulty": "medium", "focus": "BFS & DFS Applications"},
    {"day": 5, "category": "Strings", "difficulty": "medium", "focus": "Pattern Matching"},
    {"day": 6, "category": "Stacks & Queues", "difficulty": "medium", "focus": "Monotonic Stack"},
]


def get_daily_config():
    """Get today's daily challenge configuration."""
    today = datetime.now(timezone.utc)
    day_of_week = today.weekday()
    return DAILY_CATEGORIES[day_of_week % len(DAILY_CATEGORIES)]


def get_user_league(xp):
    """Determine user's league based on XP."""
    for league_key, league_data in LEAGUES.items():
        if league_data["min_xp"] <= xp < league_data["max_xp"]:
            return {"key": league_key, **league_data}
    return {"key": "bronze", **LEAGUES["bronze"]}


@router.get("/challenge")
async def get_daily_challenge(user=Depends(get_current_user)):
    """Get today's daily challenge problem."""
    collection = curated_questions_collection()
    solved_col = solved_problems_collection()
    gam_col = gamification_collection()
    config = get_daily_config()
    uid = user["id"]

    today = datetime.now(timezone.utc).date().isoformat()

    # Check if user already completed today's challenge
    existing = await solved_col.find_one({
        "user_id": uid,
        "daily_challenge_date": today,
    })

    # Get a problem for today's category
    query = {
        "topic": config["category"],
        "difficulty": config["difficulty"],
        "type": "coding",
    }

    # Get a problem the user hasn't solved
    solved_ids = []
    async for doc in solved_col.find({"user_id": uid}, {"question_id": 1}):
        solved_ids.append(doc["question_id"])

    if solved_ids:
        query["_id"] = {"$nin": [ObjectId(sid) for sid in solved_ids if ObjectId.is_valid(sid)]}

    pipeline = [
        {"$match": query},
        {"$sample": {"size": 1}},
        {"$project": {
            "question_title": 1,
            "statement": 1,
            "difficulty": 1,
            "topics": 1,
            "company": 1,
            "visible_test_cases": 1,
            "constraints": 1,
            "examples": 1,
            "hints": 1,
        }}
    ]

    problem = None
    async for doc in collection.aggregate(pipeline):
        doc["id"] = str(doc.pop("_id"))
        problem = doc

    if not problem:
        # Fallback: get any unsolved problem
        fallback_query = {"type": "coding"}
        if solved_ids:
            fallback_query["_id"] = {"$nin": [ObjectId(sid) for sid in solved_ids if ObjectId.is_valid(sid)]}
        cursor = collection.find(fallback_query).limit(1)
        async for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            problem = doc

    # Get user's XP for league
    gam_doc = await gam_col.find_one({"user_id": uid})
    xp = gam_doc.get("xp", 0) if gam_doc else 0
    league = get_user_league(xp)

    # Get today's leaderboard (who solved it)
    leaderboard_pipeline = [
        {"$match": {"daily_challenge_date": today}},
        {"$lookup": {
            "from": "users",
            "localField": "user_id",
            "foreignField": "_id",
            "as": "user"
        }},
        {"$unwind": "$user"},
        {"$project": {
            "user_name": "$user.name",
            "time_taken": 1,
            "score": 1,
        }},
        {"$sort": {"time_taken": 1}},
        {"$limit": 10}
    ]
    leaderboard = []
    async for doc in solved_col.aggregate(leaderboard_pipeline):
        leaderboard.append(doc)

    return {
        "date": today,
        "config": config,
        "problem": problem,
        "already_completed": existing is not None,
        "user_league": league,
        "leaderboard": leaderboard,
        "streak_bonus": 50,  # XP bonus for daily streak
    }


@router.post("/challenge/submit")
async def submit_daily_challenge(
    problem_id: str,
    code: str,
    language: str,
    user=Depends(get_current_user),
):
    """Submit solution for daily challenge."""
    from app.services.code_executor import CodeExecutionEngine
    from bson import ObjectId

    engine = CodeExecutionEngine()
    collection = curated_questions_collection()
    solved_col = solved_problems_collection()
    gam_col = gamification_collection()
    uid = user["id"]
    today = datetime.now(timezone.utc).date().isoformat()

    # Check if already completed
    existing = await solved_col.find_one({
        "user_id": uid,
        "daily_challenge_date": today,
    })
    if existing:
        raise HTTPException(status_code=400, detail="Already completed today's challenge")

    # Get the problem
    try:
        q_oid = ObjectId(problem_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid problem ID")

    question = await collection.find_one({"_id": q_oid})
    if not question:
        raise HTTPException(status_code=404, detail="Problem not found")

    # Execute against test cases
    visible_cases = question.get("visible_test_cases", [])
    hidden_cases = question.get("hidden_test_cases", [])
    all_cases = visible_cases + hidden_cases

    passed_count = 0
    total_cases = len(all_cases)

    for case in all_cases:
        result = await engine.execute_code(code, language, case.get("input", ""), timeout=5)
        if result["success"]:
            actual = result["stdout"].strip()
            expected = case.get("expected", "").strip()
            if actual == expected:
                passed_count += 1

    all_passed = passed_count == total_cases
    score = round(passed_count / total_cases * 100, 1) if total_cases > 0 else 0

    # Calculate time taken
    started_at = existing.get("started_at", datetime.now(timezone.utc)) if existing else datetime.now(timezone.utc)
    time_taken = (datetime.now(timezone.utc) - started_at).total_seconds()

    # Record solved
    await solved_col.insert_one({
        "user_id": uid,
        "question_id": problem_id,
        "code": code,
        "language": language,
        "score": score,
        "all_passed": all_passed,
        "time_taken": time_taken,
        "daily_challenge_date": today,
        "solved_at": datetime.now(timezone.utc),
    })

    # Calculate XP
    base_xp = 50 if all_passed else 10
    streak_bonus = 0

    # Check streak
    gam_doc = await gam_col.find_one({"user_id": uid})
    if gam_doc:
        streak = gam_doc.get("streak", 0)
        if streak >= 3:
            streak_bonus = min(50, streak * 5)  # Max 50 bonus

    total_xp = base_xp + streak_bonus

    # Record gamification
    await record_practice(uid, "daily_challenge", score)

    return {
        "score": score,
        "passed_count": passed_count,
        "total_cases": total_cases,
        "all_passed": all_passed,
        "time_taken": round(time_taken),
        "xp_gained": total_xp,
        "streak_bonus": streak_bonus,
        "message": "Daily Challenge Complete!" if all_passed else "Good attempt! Try again tomorrow.",
    }


@router.get("/leagues")
async def get_leagues(user=Depends(get_current_user)):
    """Get league standings and user's league position."""
    gam_col = gamification_collection()
    users_col = users_collection()
    uid = user["id"]

    # Get user's XP
    gam_doc = await gam_col.find_one({"user_id": uid})
    xp = gam_doc.get("xp", 0) if gam_doc else 0
    user_league = get_user_league(xp)

    # Get leaderboard for each league
    league_leaderboards = {}
    for league_key, league_data in LEAGUES.items():
        pipeline = [
            {"$match": {
                "xp": {"$gte": league_data["min_xp"], "$lt": league_data["max_xp"]}
            }},
            {"$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user"
            }},
            {"$unwind": "$user"},
            {"$project": {
                "user_name": "$user.name",
                "xp": 1,
                "level": 1,
                "streak": 1,
            }},
            {"$sort": {"xp": -1}},
            {"$limit": 10}
        ]
        leaders = []
        async for doc in gam_col.aggregate(pipeline):
            leaders.append(doc)

        league_leaderboards[league_key] = {
            "name": league_data["name"],
            "emoji": league_data["emoji"],
            "color": league_data["color"],
            "min_xp": league_data["min_xp"],
            "leaders": leaders,
        }

    # Calculate promotion/demotion info
    next_league = None
    for league_key, league_data in LEAGUES.items():
        if league_data["min_xp"] > xp:
            next_league = {
                "name": league_data["name"],
                "emoji": league_data["emoji"],
                "xp_needed": league_data["min_xp"] - xp,
            }
            break

    return {
        "current_league": user_league,
        "xp": xp,
        "next_league": next_league,
        "leagues": league_leaderboards,
    }


@router.get("/leaderboard")
async def get_leaderboard(timeframe: str = "daily", user=Depends(get_current_user)):
    """Get leaderboard for daily/weekly/monthly timeframe."""
    gam_col = gamification_collection()
    solved_col = solved_problems_collection()

    now = datetime.now(timezone.utc)

    if timeframe == "daily":
        start_date = now.date().isoformat()
        match_stage = {"daily_challenge_date": start_date}
    elif timeframe == "weekly":
        start_date = (now - timedelta(days=7)).isoformat()
        match_stage = {"daily_challenge_date": {"$gte": start_date}}
    else:  # monthly
        start_date = (now - timedelta(days=30)).isoformat()
        match_stage = {"daily_challenge_date": {"$gte": start_date}}

    pipeline = [
        {"$match": match_stage},
        {"$group": {
            "_id": "$user_id",
            "challenges_solved": {"$sum": 1},
            "avg_score": {"$avg": "$score"},
            "total_time": {"$sum": "$time_taken"},
        }},
        {"$lookup": {
            "from": "users",
            "localField": "_id",
            "foreignField": "_id",
            "as": "user"
        }},
        {"$unwind": "$user"},
        {"$project": {
            "user_name": "$user.name",
            "challenges_solved": 1,
            "avg_score": {"$round": ["$avg_score", 1]},
            "total_time": {"$round": ["$total_time", 0]},
        }},
        {"$sort": {"challenges_solved": -1, "avg_score": -1}},
        {"$limit": 50}
    ]

    leaderboard = []
    async for doc in solved_col.aggregate(pipeline):
        leaderboard.append(doc)

    return {
        "timeframe": timeframe,
        "leaderboard": leaderboard,
    }
