"""Problem of the Day — a single curated coding challenge per day.
Reads from the in-memory question store so it never depends on MongoDB
being pre-seeded. Selection is deterministic by UTC date.
Persistence now uses PostgreSQL tables:
- solved_problems → SolvedProblemRepository
- gamification_profiles → GamificationProfileRepository (via pg_record_practice)
"""
import hashlib
from datetime import datetime, timezone, date as date_type
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.middleware.auth import get_current_user
from app.database import get_session
from app.services.question_store import find, find_one
from app.services.code_executor import CodeExecutionEngine
from app.repositories.assessments import SolvedProblemRepository
from app.services.postgres_gamification import record_practice as pg_record_practice
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/v1/daily-problem", tags=["daily-problem"])

DAILY_CATEGORIES = [
    {"day": 0, "category": "Arrays", "topic": "Arrays", "difficulty": "medium", "focus": "Two Pointers & Sliding Window"},
    {"day": 1, "category": "Linked Lists", "topic": "Linked Lists", "difficulty": "medium", "focus": "Reversal & Cycle Detection"},
    {"day": 2, "category": "Trees", "topic": "Trees", "difficulty": "medium", "focus": "DFS & BFS Traversals"},
    {"day": 3, "category": "Dynamic Programming", "topic": "Dynamic Programming", "difficulty": "medium", "focus": "1D DP Patterns"},
    {"day": 4, "category": "Graphs", "topic": "Graphs", "difficulty": "medium", "focus": "BFS & DFS Applications"},
    {"day": 5, "category": "Strings", "topic": "Strings", "difficulty": "medium", "focus": "Pattern Matching"},
    {"day": 6, "category": "Stacks & Queues", "topic": "Stacks & Queues", "difficulty": "medium", "focus": "Monotonic Stack"},
]


def _today_key() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _today_config():
    today = datetime.now(timezone.utc)
    return DAILY_CATEGORIES[today.weekday() % len(DAILY_CATEGORIES)]


def _is_real_question(q: dict) -> bool:
    """Prefer real LeetCode / curated questions over auto-generated variants."""
    if q.get("trust_status") == "verified":
        return True
    title = str(q.get("question_title") or q.get("title") or q.get("question") or "")
    if "variant" in title.lower():
        return False
    source = str(q.get("source") or "")
    curated = str(q.get("curated_source") or "")
    sources = q.get("sources") or []
    if isinstance(sources, str):
        sources = [sources]
    combined_sources = source + " " + " ".join(str(s) for s in sources) + " " + curated
    if "LeetCode" in combined_sources or curated:
        return True
    if len(title) > 40:
        return True
    return False


def _pick_problem(config: dict, day_key: str):
    """Deterministically pick a coding problem for the given day.

    Preference order: independently verified content first, then curated/real
    LeetCode questions, then any usable coding question. Selection is seeded
    by the UTC date so every user sees the same problem on the same day.
    """
    seed = int(hashlib.sha256(f"{day_key}:{config['topic']}:{config['difficulty']}".encode()).hexdigest(), 16)
    for query in [
        {"type": "coding", "topic": config["topic"], "difficulty": config["difficulty"]},
        {"type": "coding", "topic": config["topic"]},
        {"type": "coding", "difficulty": config["difficulty"]},
        {"type": "coding"},
    ]:
        # Prefer verified content first (Content Trust pipeline), then fall
        # back to any real question that isn't an auto-generated variant.
        verified = find(query).prefer_verified().to_list()
        if verified:
            return verified[seed % len(verified)]
        all_qs = find(query).to_list()
        curated = [q for q in all_qs if _is_real_question(q)]
        if curated:
            return curated[seed % len(curated)]
    return None


@router.get("/today")
async def get_today_problem(user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    """Get today's Problem of the Day."""
    day_key = _today_key()
    config = _today_config()
    problem = _pick_problem(config, day_key)

    if not problem:
        raise HTTPException(status_code=404, detail="No problem available for today")

    # Verified questions use `title` for the title and `question` for the
    # statement. Legacy questions may use `question_title` + `description` or
    # `question` + `explanation`. Normalize so the frontend always gets the
    # right field regardless of the question's origin.
    title = problem.get("question_title") or problem.get("title") or ""
    statement = problem.get("statement") or problem.get("question") or problem.get("description") or ""

    solved_repo = SolvedProblemRepository(session)
    existing = await solved_repo.list_by_user(UUID(user["id"]), limit=1000, offset=0)
    already_completed = any(
        s.problem_id == problem.get("id") for s in existing
    )

    return {
        "date": day_key,
        "config": config,
        "problem": {
            "id": problem.get("id"),
            "question_title": title,
            "statement": statement,
            "difficulty": problem.get("difficulty", "medium"),
            "topics": [problem.get("topic", "")] if problem.get("topic") else [],
            "company": problem.get("company", []),
            "visible_test_cases": problem.get("visible_test_cases") or problem.get("testcases", []),
            "hidden_test_cases": problem.get("hidden_test_cases") or problem.get("hidden_testcases", []),
            "constraints": problem.get("constraints", []),
            "examples": problem.get("examples", []),
            "hints": problem.get("hints", []),
            "type": problem.get("type", "coding"),
        },
        "already_completed": already_completed,
        "xp_reward": 50,
        "user_league": {"key": "bronze", "name": "Bronze", "emoji": "🥉", "color": "#CD7F32", "min_xp": 0, "max_xp": 999},
        "leaderboard": [],
        "streak_bonus": 0,
    }


@router.post("/submit")
async def submit_daily_problem(
    problem_id: str,
    code: str,
    language: str = "python",
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Submit solution for today's Problem of the Day."""
    day_key = _today_key()
    solved_repo = SolvedProblemRepository(session)

    # Check if already completed today (by problem_id, user_id)
    existing_list = await solved_repo.list_by_user(UUID(user["id"]), limit=1000, offset=0)
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    already = any(
        s.problem_id == problem_id and s.created_at and s.created_at >= today_start
        for s in existing_list
    )
    if already:
        raise HTTPException(status_code=400, detail="Already completed today's problem")

    problem = find_one({"id": problem_id})
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    engine = CodeExecutionEngine()
    test_cases = problem.get("visible_test_cases", []) + problem.get("hidden_test_cases", [])

    passed = 0
    total = len(test_cases)
    for case in test_cases:
        result = await engine.execute_code(code, language, case.get("input", ""), timeout=5)
        if result.get("success"):
            actual = result.get("stdout", "").strip()
            expected = case.get("expected", "").strip()
            if actual == expected:
                passed += 1

    all_passed = total == 0 or passed == total
    xp_gained = 50 if all_passed else max(0, 25 - (total - passed) * 5)

    await solved_repo.create({
        "user_id": UUID(user["id"]),
        "problem_id": problem_id,
        "problem_type": "coding",
        "status": "solved",
        "score": int(xp_gained / 5),  # 0-10 score
        "language": language,
        "time_taken_seconds": 0,
        "attempts": 1,
    })

    # Canonical reward (LAW): 0-10 score from the pass rate.
    score_10 = round(passed / total * 10, 1) if total > 0 else 10.0
    result = await pg_record_practice(
        session,
        user["id"],
        "coding",
        score_10,
        {"problem_id": problem_id, "language": language,
         "skill_id": "coding.daily", "passed": passed, "total": total},
        role=user.get("role") or user.get("target_role") or "sde",
    )
    xp_gained = int((result or {}).get("xp_gained", 0))

    return {
        "all_passed": all_passed,
        "passed_count": passed,
        "total_cases": total,
        "xp_gained": xp_gained,
        "streak_bonus": 0,
        "time_taken": 0,
    }


@router.get("/history")
async def get_problem_history(user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    """Get past problems the user has attempted."""
    solved_repo = SolvedProblemRepository(session)
    problems = await solved_repo.list_by_user(UUID(user["id"]), limit=30, offset=0)

    return {
        "history": [
            {
                "id": str(p.id),
                "problem_id": p.problem_id,
                "problem_type": p.problem_type,
                "status": p.status,
                "score": p.score,
                "language": p.language,
                "time_taken_seconds": p.time_taken_seconds,
                "attempts": p.attempts,
                "created_at": p.created_at.isoformat() if p.created_at else None,
            }
            for p in problems
        ]
    }
