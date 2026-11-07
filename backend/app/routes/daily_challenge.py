"""
Daily Challenge & Leagues — Retention engine with daily problems and competitive leagues.
"""
import hashlib
import random
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from app.middleware.auth import get_current_user
from app.database import (
    solved_problems_collection,
    question_answers_collection,
    gamification_collection,
    users_collection,
    daily_challenges_users_collection,
)
from app.services.cache import cache
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/daily", tags=["daily-challenge"])

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


def get_user_league(diamonds):
    """Determine user's league based on Diamonds."""
    for league_key, league_data in LEAGUES.items():
        if league_data["min_xp"] <= diamonds < league_data["max_xp"]:
            return {"key": league_key, **league_data}
    return {"key": "bronze", **LEAGUES["bronze"]}


def _get_featured_daily_problem(config: dict, day_key: str):
    """Pick a deterministic featured problem for the day from the in-memory
    canonical store (Residency Rule): verified content first. The day-seeded
    pick is stable all day, so no cache round-trip is needed."""
    from app.services import question_store
    pool = question_store.find({
        "topic": config["category"],
        "difficulty": config["difficulty"],
        "type": "coding",
    }).prefer_verified().to_list()
    if not pool:
        pool = question_store.find({"type": "coding"}).prefer_verified().to_list()
    if not pool:
        return None
    seed = int(hashlib.sha256(f"{day_key}:{config['category']}:{config['difficulty']}".encode("utf-8")).hexdigest(), 16)
    q = pool[seed % len(pool)]
    return question_store.get_question_for_serving(q.get("id"))


async def _get_daily_leaderboard(solved_col, day_key: str):
    cache_key = f"leaderboard:{day_key}"
    cached = await cache.get("daily_problem", cache_key)
    if cached is not None:
        return cached

    leaderboard_pipeline = [
        {"$match": {"daily_challenge_date": day_key}},
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
    await cache.set("daily_problem", cache_key, leaderboard, ttl=60)
    return leaderboard


@router.get("/challenge")
async def get_daily_challenge(user=Depends(get_current_user)):
    """Get today's daily challenge — weakness-based mission."""
    solved_col = solved_problems_collection()
    gam_col = gamification_collection()
    uid = user["id"]

    today = datetime.now(timezone.utc).date().isoformat()

    # Check if user already completed today's challenge
    existing = await solved_col.find_one({
        "user_id": uid,
        "daily_challenge_date": today,
    })

    # Load user skill graph for weakness-based selection
    skill_graph = {}
    target_company = None
    try:
        from app.database import skill_graph_collection
        sg_doc = await skill_graph_collection.find_one({"user_id": uid}) or {}
        skill_graph = sg_doc.get("categories", {})
    except Exception:
        skill_graph = {}

    try:
        gam_doc = await gam_col.find_one({"user_id": uid}) or {}
        target_company = gam_doc.get("target_company")
    except Exception:
        target_company = None

    # Determine weak domains for this user
    weak_domains = []
    if skill_graph:
        scored = []
        for domain, val in skill_graph.items():
            s = float(val.get("score", 0)) if isinstance(val, dict) else float(val)
            scored.append((domain, s))
        scored.sort(key=lambda x: x[1])
        weak_domains = [d for d, _ in scored[:3]] if scored else ["aptitude", "dsa", "coding"]

    # Build daily mission: 1 problem per weak domain
    from app.services import question_store
    mission_problems = []
    used_ids = set()
    for domain in weak_domains[:3]:
        pool = question_store.find({
            "topic": domain,
            "type": {"$in": ["coding", "aptitude"]},
        }).prefer_verified().to_list()
        pool.sort(key=lambda q: (0 if q.get("difficulty") == "easy" else 1, 0 if q.get("id") not in used_ids else 1))
        if pool:
            q = pool[0]
            used_ids.add(q.get("id"))
            mission_problems.append({
                "id": str(q.get("id", "")),
                "question_title": q.get("question_title"),
                "statement": q.get("statement", q.get("question", "")),
                "difficulty": q.get("difficulty"),
                "topics": q.get("topics", [q.get("topic", domain)]),
                "company": (q.get("companies") or [None])[0],
                "visible_test_cases": q.get("visible_test_cases", []),
                "constraints": q.get("constraints", []),
                "examples": q.get("examples", []),
                "hints": q.get("hints", []),
                "type": q.get("type", "coding"),
                "domain": domain,
            })

    # Fallback: if no weak-domain problems found, use generic pool
    if not mission_problems:
        pool = question_store.find({"type": "coding"}).prefer_verified().to_list()
        if pool:
            q = pool[0]
            mission_problems.append({
                "id": str(q.get("id", "")),
                "question_title": q.get("question_title"),
                "statement": q.get("statement", q.get("question", "")),
                "difficulty": q.get("difficulty"),
                "topics": q.get("topics", [q.get("topic", "General")]),
                "company": (q.get("companies") or [None])[0],
                "visible_test_cases": q.get("visible_test_cases", []),
                "constraints": q.get("constraints", []),
                "examples": q.get("examples", []),
                "hints": q.get("hints", []),
                "type": q.get("type", "coding"),
                "domain": "general",
            })

    # Get user's Diamonds/Proof for league
    gam_doc = await gam_col.find_one({"user_id": uid}) or {}
    diamonds = gam_doc.get("diamonds", 0)
    proof = gam_doc.get("proof", 0)
    league = get_user_league(diamonds)

    leaderboard = await _get_daily_leaderboard(solved_col, today)

    return {
        "date": today,
        "mission_type": "weakness_repair",
        "target_company": target_company,
        "problems": mission_problems,
        "problem_count": len(mission_problems),
        "estimated_minutes": sum(30 if p.get("type") == "coding" else 15 for p in mission_problems),
        "already_completed": existing is not None,
        "user_league": league,
        "user_proof": proof,
        "leaderboard": leaderboard,
        "streak_bonus": 50,
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

    engine = CodeExecutionEngine()
    from app.services import question_store
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

    # Get the problem from the in-memory canonical store
    # (Residency Rule, AGENTS.md): never MongoDB.
    question = question_store.get_question_for_serving(problem_id)
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

    # Calculate Diamonds
    base_xp = 50 if all_passed else 10
    streak_bonus = 0

    # Check streak
    gam_doc = await gam_col.find_one({"user_id": uid})
    if gam_doc:
        streak = gam_doc.get("streak", 0)
        if streak >= 3:
            streak_bonus = min(50, streak * 5)  # Max 50 bonus

    total_xp = base_xp + streak_bonus

    # Record gamification (score normalization lives in record_practice)
    await record_practice(uid, "daily_challenge", score, role=user.get("role") or user.get("target_role") or "sde")

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

    # Get user's Diamonds
    gam_doc = await gam_col.find_one({"user_id": uid})
    diamonds = gam_doc.get("diamonds", 0) if gam_doc else 0
    user_league = get_user_league(diamonds)

    # Get leaderboard for each league
    league_leaderboards = {}
    for league_key, league_data in LEAGUES.items():
        pipeline = [
            {"$match": {
                "diamonds": {"$gte": league_data["min_xp"], "$lt": league_data["max_xp"]}
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
                "diamonds": 1,
                "level": 1,
                "streak": 1,
            }},
            {"$sort": {"diamonds": -1}},
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
        if league_data["min_xp"] > diamonds:
            next_league = {
                "name": league_data["name"],
                "emoji": league_data["emoji"],
                "xp_needed": league_data["min_xp"] - diamonds,
            }
            break

    return {
        "current_league": user_league,
        "diamonds": diamonds,
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


# ============================================================
# 30 Days to Offer Challenge
# ============================================================
BEHAVIORAL_QUESTIONS_POOL = [
    {"title": "Tell me about a time you led a project", "category": "leadership", "difficulty": "medium"},
    {"title": "Describe a conflict you resolved within a team", "category": "conflict", "difficulty": "medium"},
    {"title": "Tell me about a failure and what you learned", "category": "failure", "difficulty": "medium"},
    {"title": "Describe a time you went above and beyond expectations", "category": "initiative", "difficulty": "hard"},
    {"title": "How do you handle tight deadlines?", "category": "time-management", "difficulty": "easy"},
    {"title": "Tell me about a time you had to learn a new technology quickly", "category": "learning", "difficulty": "medium"},
    {"title": "Describe a situation where you had to persuade someone", "category": "influence", "difficulty": "hard"},
    {"title": "Tell me about a time you made a mistake", "category": "honesty", "difficulty": "easy"},
    {"title": "How do you prioritize tasks when everything is urgent?", "category": "prioritization", "difficulty": "medium"},
    {"title": "Describe a time you worked with a difficult teammate", "category": "teamwork", "difficulty": "medium"},
    {"title": "Tell me about a time you received constructive criticism", "category": "growth", "difficulty": "easy"},
    {"title": "Describe a situation where you had to make a decision with incomplete information", "category": "decision-making", "difficulty": "hard"},
    {"title": "Tell me about a time you mentored someone", "category": "mentorship", "difficulty": "medium"},
    {"title": "Describe a project where you had to collaborate across teams", "category": "collaboration", "difficulty": "medium"},
    {"title": "How do you stay motivated when facing a challenging problem?", "category": "resilience", "difficulty": "easy"},
    {"title": "Tell me about a time you presented technical info to non-technical stakeholders", "category": "communication", "difficulty": "hard"},
    {"title": "Describe a time you improved a process or system", "category": "improvement", "difficulty": "medium"},
    {"title": "Tell me about a time you had to balance multiple responsibilities", "category": "multitasking", "difficulty": "medium"},
    {"title": "Describe a situation where you had to adapt to a significant change", "category": "adaptability", "difficulty": "medium"},
    {"title": "Tell me about a time you showed initiative", "category": "initiative", "difficulty": "medium"},
    {"title": "Describe a time you had to work under pressure", "category": "pressure", "difficulty": "easy"},
    {"title": "Tell me about a situation where you had to compromise", "category": "negotiation", "difficulty": "medium"},
    {"title": "Describe a time you went beyond your job description", "category": "ownership", "difficulty": "hard"},
    {"title": "Tell me about a time you had to give difficult feedback", "category": "feedback", "difficulty": "hard"},
    {"title": "Describe a time when you had to manage up (influence your manager)", "category": "leadership", "difficulty": "hard"},
]

MENTOR_PATHS = {
    "swe": {"prefix": "Code Master", "names": ["Arya", "Dev", "Echo", "Nova"]},
    "data-scientist": {"prefix": "Data Sage", "names": ["Luna", "Nova", "Neo", "Sage"]},
    "sde": {"prefix": "Build Blazer", "names": ["Rex", "Blitz", "Storm", "Orion"]},
    "general": {"prefix": "Career Guru", "names": ["Zen", "Ora", "Mentis", "Guide"]},
}

XP_MILESTONES = [
    (1, 7, 100),
    (8, 14, 150),
    (15, 21, 200),
    (22, 30, 250),
]


def get_daily_xp(day: int) -> int:
    for start, end, diamonds in Diamonds_MILESTONES:
        if start <= day <= end:
            return diamonds
    return 100


def generate_mentor_name(path: str) -> str:
    config = MENTOR_PATHS.get(path, MENTOR_PATHS["general"])
    name = random.choice(config["names"])
    return f"{config['prefix']} {name}"


challenge_router = APIRouter(prefix="/api/v1/daily-challenge", tags=["30-day-challenge"])


@challenge_router.post("/enroll")
async def enroll_in_challenge(
    path: str = "general",
    user=Depends(get_current_user),
):
    """Enroll in the 30 Days to Offer challenge."""
    from app.services.ai_behavioral import generate_mentor_message

    uid = user["id"]
    col = daily_challenges_users_collection()

    existing = await col.find_one({"user_id": uid})
    if existing and existing.get("enrolled"):
        raise HTTPException(status_code=400, detail="Already enrolled in the challenge")

    valid_paths = list(MENTOR_PATHS.keys())
    if path not in valid_paths:
        raise HTTPException(status_code=400, detail=f"Invalid path. Choose from: {', '.join(valid_paths)}")

    mentor_name = generate_mentor_name(path)
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

    doc = {
        "user_id": uid,
        "enrolled": True,
        "start_date": today,
        "current_day": 1,
        "last_completed_date": None,
        "streak_broken": False,
        "completed_days": [],
        "total_xp_earned": 0,
        "chosen_path": path,
        "mentor_name": mentor_name,
        "daily_quests": [],
    }

    if existing:
        await col.update_one({"_id": existing["_id"]}, {"$set": doc})
    else:
        await col.insert_one(doc)

    # Generate welcome mentor message
    try:
        message = await generate_mentor_message(mentor_name, 1, 0)
    except Exception:
        message = f"Welcome to the 30 Days to Offer challenge, {mentor_name} is here to guide you!"

    return {
        "enrolled": True,
        "mentor_name": mentor_name,
        "mentor_message": message,
        "path": path,
        "current_day": 1,
        "start_date": today.isoformat(),
    }


@challenge_router.get("/status")
async def get_challenge_status(user=Depends(get_current_user)):
    """Get user's challenge status."""
    uid = user["id"]
    col = daily_challenges_users_collection()

    doc = await col.find_one({"user_id": uid})
    if not doc or not doc.get("enrolled"):
        return {"enrolled": False}

    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    last_completed = doc.get("last_completed_date")
    today_completed = last_completed and last_completed.replace(hour=0, minute=0, second=0, microsecond=0) == today
    days_remaining = 30 - doc.get("current_day", 1) + (0 if today_completed else 1)
    streak = _calculate_streak(doc.get("completed_days", []))

    return {
        "enrolled": True,
        "current_day": doc.get("current_day", 1),
        "start_date": doc.get("start_date").isoformat() if doc.get("start_date") else None,
        "streak": streak,
        "today_completed": today_completed,
        "days_remaining": max(0, days_remaining),
        "mentor_name": doc.get("mentor_name", "Career Guru"),
        "chosen_path": doc.get("chosen_path", "general"),
        "total_xp_earned": doc.get("total_xp_earned", 0),
    }


def _calculate_streak(completed_days: list) -> int:
    if not completed_days:
        return 0
    sorted_days = sorted(set(completed_days))
    streak = 1
    max_streak = 1
    for i in range(1, len(sorted_days)):
        if sorted_days[i] == sorted_days[i - 1] + 1:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 1
    return max_streak


@challenge_router.get("/today")
async def get_today_quest(user=Depends(get_current_user)):
    """Get today's quests for the 30-day challenge."""
    from app.services.ai_behavioral import generate_mentor_message

    uid = user["id"]
    col = daily_challenges_users_collection()
    solved_col = solved_problems_collection()

    doc = await col.find_one({"user_id": uid})
    if not doc or not doc.get("enrolled"):
        raise HTTPException(status_code=400, detail="Not enrolled in the challenge")

    current_day = doc.get("current_day", 1)
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    last_completed = doc.get("last_completed_date")

    # If already completed today, show the completed quests
    if last_completed and last_completed.replace(hour=0, minute=0, second=0, microsecond=0) == today:
        # Return cached daily quests
        daily = next((d for d in doc.get("daily_quests", []) if d.get("day") == current_day), None)
        if daily:
            return {
                "day": current_day,
                "quests": daily["quests"],
                "total_today_xp": daily.get("total_xp", get_daily_xp(current_day)),
                "daily_bonus_xp": 10,
                "mentor_message": daily.get("mentor_message", "Day completed! Great work."),
                "already_completed": True,
            }

    # Check if we need to advance the day (next day)
    if last_completed:
        last_day = last_completed.replace(hour=0, minute=0, second=0, microsecond=0)
        day_diff = (today - last_day).days
        if day_diff > 0:
            if day_diff == 1:
                current_day = min(30, doc.get("current_day", 1) + 1)
            # if day_diff > 1, streak is broken — we stay on current_day (they need to catch up)
            # actually, we let them continue where they left off
            await col.update_one({"user_id": uid}, {"$set": {"current_day": current_day}})

    # Get unsolved DSA questions
    solved_ids = []
    async for sd in solved_col.find({"user_id": uid}, {"question_id": 1}):
        solved_ids.append(sd["question_id"])

    # 2 DSA problems — prefer unsolved, verified first (in-memory only,
    # Residency Rule): never MongoDB.
    from app.services import question_store
    dsa_questions = []
    solved_set = set(solved_ids)
    dsa_pool = question_store.find({"type": "coding"}).prefer_verified().to_list()
    unsolved = [q for q in dsa_pool if str(q.get("id")) not in solved_set] or dsa_pool
    candidates = random.sample(unsolved, min(4, len(unsolved))) if unsolved else []

    if len(candidates) < 2:
        # Fallback: allow any coding question (already the whole pool)
        candidates = random.sample(dsa_pool, min(4, len(dsa_pool))) if dsa_pool else []

    for c in candidates[:2]:
        diff = c.get("difficulty", "medium")
        dsa_questions.append({
            "type": "dsa",
            "title": c.get("question_title") or c.get("title") or "Coding Problem",
            "difficulty": diff,
            "points": 50 if diff == "hard" else (30 if diff == "medium" else 20),
            "question_id": str(c.get("id", "")),
            "completed": False,
        })

    # 1 Aptitude question (in-memory, verified first)
    apt_pool = question_store.find({"type": "aptitude"}).prefer_verified().to_list()
    aptitude_q = None
    if apt_pool:
        a = random.choice(apt_pool)
        aptitude_q = {
            "question_title": a.get("question_title") or a.get("title") or "Aptitude Problem",
            "difficulty": a.get("difficulty", "medium"),
            "question_id": str(a.get("id", "")),
        }
    if not aptitude_q:
        aptitude_q = {"question_title": "Quantitative Aptitude Problem", "difficulty": "medium", "question_id": ""}

    aptitude_entry = {
        "type": "aptitude",
        "title": aptitude_q.get("question_title", "Aptitude Problem"),
        "difficulty": aptitude_q.get("difficulty", "medium"),
        "points": 20,
        "question_id": aptitude_q.get("question_id", ""),
        "completed": False,
    }

    # 1 Behavioral question
    behavioral = random.choice(BEHAVIORAL_QUESTIONS_POOL)
    behavioral_entry = {
        "type": "behavioral",
        "title": behavioral["title"],
        "difficulty": behavioral["difficulty"],
        "points": 20,
        "category": behavioral["category"],
        "completed": False,
    }

    quests = dsa_questions + [aptitude_entry, behavioral_entry]
    total_xp = sum(q["points"] for q in quests)
    day_xp = get_daily_xp(current_day)

    # Generate mentor message
    yesterday_completed = 0
    yesterday_data = next((d for d in doc.get("daily_quests", []) if d.get("day") == current_day - 1), None)
    if yesterday_data:
        yesterday_completed = sum(1 for q in yesterday_data.get("quests", []) if q.get("completed"))
    mentor_name = doc.get("mentor_name", "Career Guru")

    try:
        mentor_message = await generate_mentor_message(mentor_name, current_day, yesterday_completed)
    except Exception:
        mentor_message = f"Day {current_day} — Let's make it count, {mentor_name} believes in you!"

    # Save today's quests
    daily_entry = {
        "day": current_day,
        "generated_at": datetime.now(timezone.utc),
        "quests": quests,
        "total_xp": total_xp,
        "mentor_message": mentor_message,
    }

    await col.update_one(
        {"user_id": uid},
        {"$push": {"daily_quests": daily_entry}},
    )

    return {
        "day": current_day,
        "quests": quests,
        "total_today_xp": total_xp,
        "daily_bonus_xp": 10,
        "mentor_message": mentor_message,
        "already_completed": False,
        "mentor_name": mentor_name,
    }


@challenge_router.post("/complete-day")
async def complete_day(
    quest_ids_completed: list,
    user=Depends(get_current_user),
):
    """Mark today as completed."""
    from app.services.gamification import record_practice

    uid = user["id"]
    col = daily_challenges_users_collection()

    doc = await col.find_one({"user_id": uid})
    if not doc or not doc.get("enrolled"):
        raise HTTPException(status_code=400, detail="Not enrolled in the challenge")

    current_day = doc.get("current_day", 1)
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    last_completed = doc.get("last_completed_date")

    # Check if already completed today
    if last_completed and last_completed.replace(hour=0, minute=0, second=0, microsecond=0) == today:
        raise HTTPException(status_code=400, detail="Today already completed")

    # Find today's quests
    daily_entry = next((d for d in doc.get("daily_quests", []) if d.get("day") == current_day), None)
    if not daily_entry:
        raise HTTPException(status_code=400, detail="No quests found for today. Try fetching today's quests first.")

    quests = daily_entry.get("quests", [])
    required_types = {"dsa": 0, "aptitude": 0, "behavioral": 0}
    for q in quests:
        q_type = q.get("type")
        if q_type in required_types:
            required_types[q_type] += 1

    completed_by_type = {"dsa": 0, "aptitude": 0, "behavioral": 0}
    completed_quests = []
    for q in quests:
        q_id = q.get("question_id") or q.get("title", "")
        if q_id in quest_ids_completed or q.get("title") in quest_ids_completed or q.get("type") in quest_ids_completed:
            q_type = q.get("type")
            if q_type in completed_by_type:
                completed_by_type[q_type] += 1
            completed_quests.append({**q, "completed": True, "completed_at": datetime.now(timezone.utc)})
        else:
            completed_quests.append({**q, "completed": False})

    # Validate completion
    errors = []
    if completed_by_type["dsa"] < required_types["dsa"]:
        errors.append("Complete all DSA problems")
    if completed_by_type["aptitude"] < required_types["aptitude"]:
        errors.append("Complete the aptitude question")
    if completed_by_type["behavioral"] < required_types["behavioral"]:
        errors.append("Complete the behavioral question")

    if errors:
        raise HTTPException(status_code=400, detail=". ".join(errors))

    # Calculate Diamonds
    base_xp = get_daily_xp(current_day)
    daily_bonus = 10
    total_xp_gained = base_xp + daily_bonus

    # Check for streak
    previous_completed = doc.get("completed_days", [])
    new_completed_days = list(set(previous_completed + [current_day]))
    streak_broken = False
    if previous_completed:
        last_day_num = max(previous_completed)
        if current_day != last_day_num + 1 and current_day != last_day_num:
            streak_broken = True

    # Update document
    updated_daily_quests = doc.get("daily_quests", [])
    for i, de in enumerate(updated_daily_quests):
        if de.get("day") == current_day:
            updated_daily_quests[i]["quests"] = completed_quests
            updated_daily_quests[i]["completed_at"] = datetime.now(timezone.utc)
            updated_daily_quests[i]["total_xp"] = total_xp_gained
            break

    next_day = min(30, current_day + 1)
    all_done = len(new_completed_days) >= 30
    extra_bonus = 0

    if all_done:
        extra_bonus += 500

    await col.update_one(
        {"user_id": uid},
        {
            "$set": {
                "current_day": next_day if not all_done else 30,
                "last_completed_date": datetime.now(timezone.utc),
                "streak_broken": streak_broken,
                "completed_days": new_completed_days,
                "daily_quests": updated_daily_quests,
                "total_xp_earned": doc.get("total_xp_earned", 0) + total_xp_gained + extra_bonus,
                "enrolled": not all_done,
            }
        },
    )

    # Record Diamonds via gamification (also crosses global streak milestones).
    # Score is 10.0: reaching this line means every required quest verified
    # complete (400 otherwise). Passing total_xp_gained here used to mint
    # perfect bonuses for any completion — same LAW violation as above.
    practice_result = await record_practice(uid, "daily_challenge_30day", 10.0, role=user.get("role") or user.get("target_role") or "sde")

    result = {
        "day_completed": current_day,
        "xp_gained": total_xp_gained,
        "daily_bonus": daily_bonus,
        "current_day": next_day if not all_done else 30,
        "total_xp": doc.get("total_xp_earned", 0) + total_xp_gained + extra_bonus,
        "all_30_done": all_done,
        "streak_broken": streak_broken,
    }

    if extra_bonus:
        result["completion_bonus"] = extra_bonus
        result["badge_earned"] = "Placement Ready"

    # Streak milestone chests granted inside record_practice (7/14/30/60/100 days)
    milestone_rewards = practice_result.get("milestone", {})
    if milestone_rewards:
        result["milestone"] = milestone_rewards
        result["new_streak"] = practice_result.get("new_streak", 0)

    return result


@challenge_router.get("/progress")
async def get_challenge_progress(user=Depends(get_current_user)):
    """Get full progress of the 30-day challenge."""
    uid = user["id"]
    col = daily_challenges_users_collection()

    doc = await col.find_one({"user_id": uid})
    if not doc or not doc.get("enrolled"):
        return {
            "enrolled": False,
            "completed_days": [],
            "total_xp": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "days_missed": 0,
            "completion_percentage": 0,
        }

    completed_days = doc.get("completed_days", [])
    sorted_days = sorted(set(completed_days))
    total_xp = doc.get("total_xp_earned", 0)

    # Calculate streaks
    current_streak = 0
    longest_streak = 0
    streak = 0
    for i in range(len(sorted_days)):
        if i == 0 or sorted_days[i] == sorted_days[i - 1] + 1:
            streak += 1
        else:
            streak = 1
        longest_streak = max(longest_streak, streak)

    # Current streak — from today going back
    today_num = doc.get("current_day", 1) - 1  # current_day is next
    if today_num in completed_days:
        current_streak = 1
        for d in range(today_num - 1, 0, -1):
            if d in completed_days:
                current_streak += 1
            else:
                break

    days_missed = max(0, today_num - len(completed_days))
    completion_pct = round(len(completed_days) / 30 * 100, 1)

    # Calendar grid data (which days are done)
    calendar = []
    for day in range(1, 31):
        status = "completed" if day in completed_days else "missed" if day < today_num else "current" if day == today_num + 1 else "future"
        calendar.append({"day": day, "status": status})

    return {
        "enrolled": True,
        "completed_days": sorted_days,
        "calendar": calendar,
        "total_xp": total_xp,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "days_missed": days_missed,
        "completion_percentage": completion_pct,
        "total_days_completed": len(completed_days),
        "current_day": doc.get("current_day", 1),
        "chosen_path": doc.get("chosen_path", "general"),
        "mentor_name": doc.get("mentor_name", "Career Guru"),
    }


@challenge_router.get("/leaderboard")
async def get_challenge_leaderboard(limit: int = 10, user=Depends(get_current_user)):
    """Leaderboard of challengers by total Diamonds."""
    uid = user["id"]
    col = daily_challenges_users_collection()
    users_col = users_collection()

    pipeline = [
        {"$match": {"enrolled": True}},
        {"$sort": {"total_xp_earned": -1}},
        {"$limit": limit},
        {"$lookup": {
            "from": "users",
            "localField": "user_id",
            "foreignField": "_id",
            "as": "user"
        }},
        {"$unwind": "$user"},
        {"$project": {
            "user_name": "$user.name",
            "total_xp_earned": 1,
            "current_day": 1,
            "completed_days": {"$size": {"$ifNull": ["$completed_days", []]}},
            "chosen_path": 1,
            "mentor_name": 1,
        }},
    ]

    leaderboard = []
    async for entry in col.aggregate(pipeline):
        leaderboard.append(entry)

    # Get user's rank
    user_rank = None
    user_entry = await col.find_one({"user_id": uid})
    if user_entry:
        higher_count = await col.count_documents({
            "enrolled": True,
            "total_xp_earned": {"$gt": user_entry.get("total_xp_earned", 0)},
        })
        user_rank = higher_count + 1

    return {
        "leaderboard": leaderboard,
        "user_rank": user_rank,
        "total_participants": await col.count_documents({"enrolled": True}),
    }
