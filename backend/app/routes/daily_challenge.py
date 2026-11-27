"""Daily Challenge & Leagues — Retention engine with daily problems and competitive leagues.

Migrated from MongoDB collections:
- solved_problems → SolvedProblemRepository (solved_problems table)
- gamification → GamificationProfileRepository (gamification_profiles table)
- users → User model (users table)
- daily_challenges_users → DailyChallengeUserRepository (daily_challenges_users table)
- question_answers → QuestionAnswerRepository (question_answers table)
"""

import hashlib
import random
from datetime import datetime, timezone, timedelta, date as date_type
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, and_

from app.middleware.auth import get_current_user
from app.database import get_session
from app.services.cache import cache
from app.services.postgres_gamification import record_practice as pg_record_practice
from app.repositories.assessments import SolvedProblemRepository, QuestionAnswerRepository
from app.repositories.learning import DailyChallengeUserRepository
from app.repositories.identity import UserRepository
from app.models.identity import User
from app.models.gamification import GamificationProfile
from sqlalchemy import update

router = APIRouter(prefix="/api/v1/daily", tags=["daily-challenge"])

# Alias for router registry compatibility
challenge_router = router

# League configuration
LEAGUES = {
    "bronze": {"name": "Bronze", "min_xp": 0, "max_xp": 999, "emoji": "🥉", "color": "#CD7F32"},
    "silver": {"name": "Silver", "min_xp": 1000, "max_xp": 4999, "emoji": "🥈", "color": "#C0C0C0"},
    "gold": {"name": "Gold", "min_xp": 5000, "max_xp": 14999, "emoji": "🥇", "color": "#FFD700"},
    "platinum": {"name": "Platinum", "min_xp": 15000, "max_xp": 49999, "emoji": "💎", "color": "#E5E4E2"},
    "diamond": {"name": "Diamond", "min_xp": 50000, "max_xp": float("inf"), "emoji": "👑", "color": "#B9F2FF"},
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
    canonical store (Residency Rule): verified content first."""
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


async def _get_daily_leaderboard(session: AsyncSession, day_key: str):
    """Get today's daily challenge leaderboard from PostgreSQL."""
    cache_key = f"leaderboard:{day_key}"
    cached = await cache.get("daily_problem", cache_key)
    if cached is not None:
        return cached

    # Get solved problems for today ordered by time_taken (fastest first)
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    solved_repo = SolvedProblemRepository(session)
    results = await solved_repo.list_by_user(UUID("00000000-0000-0000-0000-000000000000"), limit=1000, offset=0)
    # Filter to today's date
    today_results = [
        r for b in results
        if b.created_at and today_start <= b.created_at < today_end
    ]
    today_results.sort(key=lambda x: (x.time_taken_seconds or 999999, - (x.score or 0)))
    leaderboard = []
    for r in today_results[:10]:
        leaderboard.append({
            "user_id": str(r.user_id),
            "time_taken": r.time_taken_seconds,
            "score": r.score,
        })

    await cache.set("daily_problem", cache_key, leaderboard, ttl=60)
    return leaderboard


@router.get("/challenge")
async def get_daily_challenge(user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    """Get today's daily challenge — weakness-based mission."""
    solved_repo = SolvedProblemRepository(session)
    gamification_repo = None  # Will use GamificationProfileRepository lazily
    uid = UUID(user["id"])

    today = datetime.now(timezone.utc).date().isoformat()

    # Check if user already completed today's challenge
    dcu_repo = DailyChallengeUserRepository(session)
    existing = await dcu_repo.get_by_user_and_date(UUID(uid), date_type.fromisoformat(today))

    if existing:
        return {
            "status": "already_completed",
            "score": existing.score,
            "completed_at": existing.completed_at.isoformat() if existing.completed_at else None,
        }

    # Load user skill graph for weakness-based selection
    # Use gamification profile for target_company
    gamification_repo = None  # Will load via UserRepository gamification relationship

    # Get user's gamification profile
    user_repo = UserRepository(session)
    db_user = await user_repo.get_by_id(uid)
    target_company = None
    skill_graph = {}
    if db_user:
        # Weak domains - use a default set since skill_graph is separate
        weak_domains = ["aptitude", "dsa", "coding"]

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
                "topics": q.get("topics", [q.get("topic", "general")]),
                "company": (q.get("companies") or [None])[0],
                "visible_test_cases": q.get("visible_test_cases", []),
                "constraints": q.get("constraints", []),
                "examples": q.get("examples", []),
                "hints": q.get("hints", []),
                "type": q.get("type", "coding"),
                "domain": "general",
            })

    return {
        "status": "new",
        "today": today,
        "mission_problems": mission_problems,
        "weak_domains": weak_domains[:3],
    }


@router.post("/submit")
async def submit_daily_challenge(
    problem_id: str,
    code: str,
    language: str,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Submit a daily challenge solution."""
    uid = user["id"]
    today = datetime.now(timezone.utc).date().isoformat()

    dcu_repo = DailyChallengeUserRepository(session)
    existing = await dcu_repo.get_by_user_and_date(UUID(uid), date_type.fromisoformat(today))
    if existing:
        raise HTTPException(status_code=400, detail="Daily challenge already completed today")

    # Simple scoring: if code submitted, mark as completed with score
    score = 8.0 if code and len(code.strip()) > 0 else 0.0

    # Record solved problem
    solved_repo = SolvedProblemRepository(session)
    await solved_repo.create({
        "user_id": uid,
        "problem_id": problem_id,
        "problem_type": "coding",
        "status": "solved",
        "score": int(score * 10),
        "language": language,
        "time_taken_seconds": 0,
        "attempts": 1,
    })

    # Record daily challenge completion
    await dcu_repo.create({
        "user_id": uid,
        "challenge_date": date_type.fromisoformat(today),
        "challenge_type": "coding",
        "status": "completed",
        "score": int(score * 10),
        "completed_at": datetime.now(timezone.utc),
    })

    # Gamification
    gamification_result = await pg_record_practice(session, uid, "daily_challenge", score, role=user.get("role") or user.get("target_role") or "sde")

    return {
        "status": "completed",
        "score": score,
        "xp_gained": gamification_result.get("xp_gained", 0),
        "level": gamification_result.get("level", 1),
        "badges": gamification_result.get("new_badges", []),
    }


@router.get("/leaderboard")
async def get_daily_leaderboard(user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    """Get today's daily challenge leaderboard."""
    config = get_daily_config()
    day_key = f"{config['category']}:{datetime.now(timezone.utc).date().isoformat()}"
    leaderboard = await _get_daily_leaderboard(session, day_key)
    return {
        "date": datetime.now(timezone.utc).date().isoformat(),
        "category": config["category"],
        "leaderboard": leaderboard,
    }


@router.get("/stats")
async def get_daily_stats(user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    """Get user's daily challenge statistics."""
    dcu_repo = DailyChallengeUserRepository(session)
    challenges = await dcu_repo.list_by_user(UUID(user["id"]), limit=100, offset=0)

    total = len(challenges)
    completed = len([c for c in challenges if c.status == "completed"])
    total_score = sum(c.score or 0 for c in completed)
    avg_score = round(total_score / len(completed), 1) if completed else 0

    return {
        "total_challenges": total,
        "completed_challenges": completed,
        "avg_score": avg_score,
        "total_score": total_score,
    }


@router.post("/{problem_id}/hint")
async def get_daily_hint(
    problem_id: str,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get a hint for the daily challenge problem."""
    from app.services import question_store
    q = question_store.get_question_for_serving(problem_id)
    if not q:
        raise HTTPException(status_code=404, detail="Problem not found")
    hints = q.get("hints", [])
    return {
        "problem_id": problem_id,
        "hints": hints[:2],  # Return first 2 hints
    }
