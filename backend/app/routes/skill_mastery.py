"""Skill Mastery — track mastery per skill/topic on a 0-5 scale.

Provides GET /api/v1/mastery/graph for full skill graph,
GET /api/v1/mastery/weak for weak areas, and
POST /api/v1/mastery/record to update mastery after a solve.
All logic is pure deterministic math from solved_problems data.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    solved_problems_collection,
    submissions_collection,
    curated_questions_collection,
    skill_graph_collection,
)
from app.services.mastery_engine import (
    build_mastery_graph,
    find_weak_areas,
    record_solve,
    calculate_mastery_level,
    MASTERY_LEVELS,
    get_mastery_color,
)

router = APIRouter(prefix="/api/v1/mastery", tags=["skill-mastery"])


class RecordSolveRequest(BaseModel):
    """Request to record a problem solve and update mastery."""
    topic: str = Field(..., min_length=1, description="Skill topic (e.g., 'arrays', 'graphs')")
    sub_topic: str = Field(..., min_length=1, description="Sub-topic (e.g., 'two-pointers', 'bfs-dfs')")
    is_correct: bool = Field(..., description="Whether the solve was correct")


async def _get_user_skill_stats(uid: str):
    """Aggregate per-skill stats from solved_problems + submissions.

    Joins solved_problems with curated_questions to get topic/sub_topic,
    then counts attempts (from submissions) and correct solves (from solved_problems).
    """
    solved_col = solved_problems_collection()
    subs_col = submissions_collection()

    # Get correct solves grouped by topic/sub_topic
    solved_pipeline = [
        {"$match": {"user_id": uid}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question",
        }},
        {"$unwind": {"path": "$question", "preserveNullAndEmptyArrays": True}},
        {"$group": {
            "_id": {
                "topic": {"$ifNull": ["$question.topic", "other"]},
                "sub_topic": {"$ifNull": ["$question.sub_topic", "general"]},
            },
            "solved_count": {"$sum": 1},
            "first_solved": {"$min": "$solved_at"},
            "last_solved": {"$max": "$solved_at"},
        }},
    ]

    solved_by_skill = {}
    async for doc in solved_col.aggregate(solved_pipeline):
        key = (doc["_id"]["topic"], doc["_id"]["sub_topic"])
        solved_by_skill[key] = {
            "solved_count": doc["solved_count"],
            "first_attempted": doc.get("first_solved"),
            "last_practiced": doc.get("last_solved"),
        }

    # Get total attempts grouped by topic/sub_topic
    attempts_pipeline = [
        {"$match": {"user_id": uid}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question",
        }},
        {"$unwind": {"path": "$question", "preserveNullAndEmptyArrays": True}},
        {"$group": {
            "_id": {
                "topic": {"$ifNull": ["$question.topic", "other"]},
                "sub_topic": {"$ifNull": ["$question.sub_topic", "general"]},
            },
            "total_attempts": {"$sum": 1},
            "passed_attempts": {"$sum": {"$cond": [{"$eq": ["$status", "passed"]}, 1, 0]}},
        }},
    ]

    attempts_by_skill = {}
    async for doc in subs_col.aggregate(attempts_pipeline):
        key = (doc["_id"]["topic"], doc["_id"]["sub_topic"])
        attempts_by_skill[key] = {
            "total_attempts": doc["total_attempts"],
            "passed_attempts": doc["passed_attempts"],
        }

    # Merge into a unified stats list
    all_keys = set(solved_by_skill.keys()) | set(attempts_by_skill.keys())
    stats = []
    for topic, sub_topic in all_keys:
        solved = solved_by_skill.get(key := (topic, sub_topic), {})
        attempts = attempts_by_skill.get(key, {})

        problems_attempted = max(
            attempts.get("total_attempts", 0),
            solved.get("solved_count", 0),
        )
        problems_solved = solved.get("solved_count", 0)

        # Use submission-based accuracy if available, fallback to solved count
        if attempts.get("total_attempts", 0) > 0:
            accuracy = attempts["passed_attempts"] / attempts["total_attempts"]
        else:
            accuracy = 1.0 if problems_solved > 0 else 0.0

        stats.append({
            "topic": topic,
            "sub_topic": sub_topic,
            "problems_attempted": problems_attempted,
            "problems_solved": problems_solved,
            "accuracy": accuracy,
            "first_attempted": _to_iso(solved.get("first_attempted")),
            "last_practiced": _to_iso(solved.get("last_practiced")),
            "recent_accuracy": accuracy,
        })

    return stats


def _to_iso(dt) -> Optional[str]:
    """Convert a datetime to ISO string, handling None."""
    if dt is None:
        return None
    if isinstance(dt, str):
        return dt
    return dt.isoformat()


@router.get("/graph")
async def get_mastery_graph(user=Depends(get_current_user)):
    """Get the full skill mastery graph for the user.

    Returns every skill with its mastery level (0-5), problem counts,
    accuracy, and category summaries. Skills are derived from the user's
    solved_problems and submissions history.
    """
    uid = user["id"]
    stats = await _get_user_skill_stats(uid)

    if not stats:
        return {
            "overall_level": 0,
            "total_skills": 0,
            "mastered_count": 0,
            "strong_count": 0,
            "weak_count": 0,
            "untried_count": 0,
            "skills": {},
            "category_summary": {},
            "message": "No skill data yet. Solve some problems to build your skill graph!",
        }

    graph = build_mastery_graph(stats)

    # Enrich skill data with labels and colors
    enriched_skills = {}
    for key, mastery in graph.skills.items():
        enriched_skills[key] = {
            "topic": mastery.topic,
            "sub_topic": mastery.sub_topic,
            "level": mastery.level,
            "level_name": mastery.name,
            "color": get_mastery_color(mastery.level),
            "problems_attempted": mastery.problems_attempted,
            "problems_solved": mastery.problems_solved,
            "accuracy": round(mastery.accuracy * 100, 1),
            "first_attempted": mastery.first_attempted,
            "last_practiced": mastery.last_practiced,
        }

    return {
        "overall_level": graph.overall_level,
        "total_skills": graph.total_skills,
        "mastered_count": graph.mastered_count,
        "strong_count": graph.strong_count,
        "weak_count": graph.weak_count,
        "untried_count": graph.untried_count,
        "skills": enriched_skills,
        "category_summary": graph.category_summary,
    }


@router.get("/weak")
async def get_weak_areas(
    limit: int = 10,
    user=Depends(get_current_user),
):
    """Get the user's weakest skill areas.

    Returns skills with mastery level < 3, sorted by improvement potential.
    Skills with more attempts are listed first (higher investment = easier to improve).
    """
    uid = user["id"]
    stats = await _get_user_skill_stats(uid)

    if not stats:
        return {"weak_areas": [], "message": "No skill data yet."}

    weak = find_weak_areas(stats, top_n=limit)

    return {
        "weak_areas": weak,
        "count": len(weak),
    }


@router.post("/record")
async def record_problem_solve(req: RecordSolveRequest, user=Depends(get_current_user)):
    """Record a problem solve and update mastery for the skill.

    Call this after a user submits a problem. It updates the skill_graphs
    collection with the new mastery state for the given topic/sub_topic.

    Returns the updated mastery level and whether it increased.
    """
    uid = user["id"]
    skill_col = skill_graph_collection()

    # Get existing mastery stats for this user + skill
    existing = await skill_col.find_one({
        "user_id": uid,
        "topic": req.topic,
        "sub_topic": req.sub_topic,
    })

    existing_stats = None
    if existing:
        existing_stats = {
            "problems_attempted": existing.get("problems_attempted", 0),
            "problems_solved": existing.get("problems_solved", 0),
            "first_attempted": existing.get("first_attempted"),
            "last_practiced": existing.get("last_practiced"),
            "recent_history": existing.get("recent_history", []),
        }

    # Calculate new mastery
    updated = record_solve(
        topic=req.topic,
        sub_topic=req.sub_topic,
        is_correct=req.is_correct,
        existing_stats=existing_stats,
    )

    previous_level = existing.get("current_level", 0) if existing else 0
    new_level = updated["current_level"]
    level_increased = new_level > previous_level

    # Upsert into skill_graphs
    now = datetime.now(timezone.utc)
    await skill_col.update_one(
        {"user_id": uid, "topic": req.topic, "sub_topic": req.sub_topic},
        {"$set": {
            "user_id": uid,
            "topic": req.topic,
            "sub_topic": req.sub_topic,
            "problems_attempted": updated["problems_attempted"],
            "problems_solved": updated["problems_solved"],
            "first_attempted": updated["first_attempted"],
            "last_practiced": updated["last_practiced"],
            "recent_history": updated["recent_history"],
            "recent_accuracy": updated["recent_accuracy"],
            "current_level": new_level,
            "current_level_name": updated["current_level_name"],
            "updated_at": now,
        }},
        upsert=True,
    )

    return {
        "topic": req.topic,
        "sub_topic": req.sub_topic,
        "is_correct": req.is_correct,
        "previous_level": previous_level,
        "current_level": new_level,
        "level_name": updated["current_level_name"],
        "level_increased": level_increased,
        "problems_attempted": updated["problems_attempted"],
        "problems_solved": updated["problems_solved"],
        "accuracy": round(updated["recent_accuracy"] * 100, 1) if updated["recent_accuracy"] is not None else 0,
        "color": get_mastery_color(new_level),
    }
