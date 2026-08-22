"""Adaptive Quest Engine — daily practice quests API.

Provides personalized daily quests based on the user's actual weak areas,
SRS review needs, target companies, and mastery levels. Rules-based, no AI.

Endpoints:
    GET  /api/v1/quests/daily     → today's generated quests
    GET  /api/v1/quests/active    → quests with live progress
    POST /api/v1/quests/record    → record a solve toward a quest
    GET  /api/v1/quests/history   → past completed quests (30 days)
    GET  /api/v1/quests/stats     → completion rate, XP, streaks
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

from app.middleware.auth import get_current_user
from app.database import (
    daily_quests_collection,
    skill_graph_collection,
    srs_cards_collection,
    solved_problems_collection,
    submissions_collection,
    users_collection,
    curated_questions_collection,
)
from app.services import question_store
from app.services.quest_engine import (
    generate_daily_quests,
    check_quest_progress,
    does_solve_match_quest,
    serialize_quest,
    compute_quest_stats,
    _today_str,
    _compute_recent_accuracy,
    QuestType,
)
from app.services.mastery_engine import build_mastery_graph, find_weak_areas
from app.services.cache import cache

router = APIRouter(prefix="/api/v1/quests", tags=["quests"])


class RecordSolveRequest(BaseModel):
    """Request to record a problem solve toward a quest."""
    question_id: str = Field(..., min_length=1, description="ID of the solved question")
    is_correct: bool = Field(True, description="Whether the solve was correct")


async def _get_user_target_companies(uid: str) -> list:
    """Fetch user's target companies from onboarding data.

    Args:
        uid: User ID.

    Returns:
        List of target company name strings.
    """
    user_doc = await users_collection.find_one({"_id": ObjectId(uid)})
    if not user_doc:
        return []
    onboarding = user_doc.get("onboarding", {})
    return onboarding.get("target_companies", [])


async def _get_due_srs_cards(uid: str) -> list:
    """Fetch SRS cards due for review right now.

    Args:
        uid: User ID.

    Returns:
        List of SRS card dicts.
    """
    now = datetime.now(timezone.utc)
    cards_col = srs_cards_collection()
    cursor = cards_col.find({
        "user_id": uid,
        "next_review": {"$lte": now},
    }).sort("next_review", 1).limit(20)
    return await cursor.to_list(20)


async def _get_skill_stats(uid: str) -> list:
    """Fetch per-skill stats from skill_graphs collection.

    Args:
        uid: User ID.

    Returns:
        List of skill stat dicts compatible with mastery_engine.
    """
    skill_col = skill_graph_collection()
    cursor = skill_col.find({"user_id": uid})
    docs = await cursor.to_list(500)

    stats = []
    for doc in docs:
        stats.append({
            "topic": doc.get("topic", "unknown"),
            "sub_topic": doc.get("sub_topic", "unknown"),
            "problems_attempted": doc.get("problems_attempted", 0),
            "problems_solved": doc.get("problems_solved", 0),
            "first_attempted": doc.get("first_attempted"),
            "last_practiced": doc.get("last_practiced"),
            "recent_accuracy": doc.get("recent_accuracy"),
        })
    return stats


async def _get_performance_data(uid: str) -> dict:
    """Fetch user's recent performance data for quest generation.

    Computes accuracy from solved_problems and submissions in the last 7 days.

    Args:
        uid: User ID.

    Returns:
        Dict with overall_accuracy, accuracy_per_topic, total_solved.
    """
    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)

    solved_col = solved_problems_collection()
    subs_col = submissions_collection()

    # Total solved
    total_solved = await solved_col.count_documents({"user_id": uid})

    # Last 7 days solves
    recent_solved_pipeline = [
        {"$match": {"user_id": uid, "solved_at": {"$gte": week_ago}}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question",
        }},
        {"$unwind": {"path": "$question", "preserveNullAndEmptyArrays": True}},
        {"$group": {
            "_id": "$question.topic",
            "count": {"$sum": 1},
        }},
    ]
    recent_topics: dict[str, int] = {}
    async for doc in solved_col.aggregate(recent_solved_pipeline):
        topic = doc["_id"] or "other"
        recent_topics[topic] = doc["count"]

    # Recent submissions for accuracy
    recent_subs_pipeline = [
        {"$match": {"user_id": uid, "submitted_at": {"$gte": week_ago}}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question",
        }},
        {"$unwind": {"path": "$question", "preserveNullAndEmptyArrays": True}},
        {"$group": {
            "_id": "$question.topic",
            "total": {"$sum": 1},
            "passed": {"$sum": {"$cond": [{"$eq": ["$status", "passed"]}, 1, 0]}},
        }},
    ]
    accuracy_per_topic: dict[str, float] = {}
    total_recent = 0
    total_passed = 0
    async for doc in subs_col.aggregate(recent_subs_pipeline):
        topic = doc["_id"] or "other"
        t = doc["total"]
        p = doc["passed"]
        total_recent += t
        total_passed += p
        accuracy_per_topic[topic] = p / t if t > 0 else 0.0

    overall_accuracy = total_passed / total_recent if total_recent > 0 else 0.5

    return {
        "overall_accuracy": round(overall_accuracy, 4),
        "accuracy_per_topic": accuracy_per_topic,
        "total_solved": total_solved,
        "recent_7day_solves": sum(recent_topics.values()),
    }


async def _get_today_solved_ids(uid: str) -> set:
    """Get problem IDs solved today by the user.

    Args:
        uid: User ID.

    Returns:
        Set of question ID strings.
    """
    now = datetime.now(timezone.utc)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)

    solved_col = solved_problems_collection()
    cursor = solved_col.find({
        "user_id": uid,
        "solved_at": {"$gte": start_of_day},
    }, {"question_id": 1})
    docs = await cursor.to_list(1000)
    return {str(d.get("question_id", "")) for d in docs}


async def _get_question_for_match(question_id: str) -> Optional[dict]:
    """Fetch question data for quest matching.

    Args:
        question_id: Question ID string.

    Returns:
        Question dict or None.
    """
    # Try in-memory store first (faster)
    q = question_store.find_one({"id": question_id})
    if q:
        return q

    # Fallback to MongoDB
    col = curated_questions_collection()
    doc = await col.find_one({"_id": ObjectId(question_id)}) if ObjectId.is_valid(question_id) else None
    if doc:
        doc["id"] = str(doc.pop("_id", ""))
        return doc
    return None


async def _get_or_generate_daily_quests(uid: str) -> dict:
    """Get today's quests from cache/DB, or generate fresh.

    Regenerates once per day. Uses MongoDB as cache.

    Args:
        uid: User ID.

    Returns:
        Daily quests document.
    """
    today = _today_str()
    quests_col = daily_quests_collection()

    # Check DB
    existing = await quests_col.find_one({"user_id": uid, "date": today})
    if existing:
        return existing

    # Generate fresh quests
    performance = await _get_performance_data(uid)
    skill_stats = await _get_skill_stats(uid)
    due_cards = await _get_due_srs_cards(uid)
    companies = await _get_user_target_companies(uid)
    solved_ids = await _get_today_solved_ids(uid)

    quests = generate_daily_quests(
        user_id=uid,
        performance_data=performance,
        skill_stats=skill_stats,
        due_srs_cards=due_cards,
        target_companies=companies,
        solved_problem_ids=solved_ids,
    )

    # Store in MongoDB
    now = datetime.now(timezone.utc)
    doc = {
        "user_id": uid,
        "date": today,
        "quests": quests,
        "created_at": now,
        "updated_at": now,
    }
    await quests_col.insert_one(doc)

    return doc


async def _count_matching_solves_today(
    uid: str,
    quest: dict,
) -> int:
    """Count how many solves today match a quest's criteria.

    Args:
        uid: User ID.
        quest: Quest dict.

    Returns:
        Count of matching solves.
    """
    today = _today_str()
    solved_col = solved_problems_collection()

    start_of_day = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    # Get today's solves with question data
    pipeline = [
        {"$match": {"user_id": uid, "solved_at": {"$gte": start_of_day}}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question",
        }},
        {"$unwind": {"path": "$question", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "question_id": 1,
            "topic": {"$ifNull": ["$question.topic", ""]},
            "sub_topic": {"$ifNull": ["$question.sub_topic", ""]},
            "companies": {"$ifNull": ["$question.companies", []]},
            "difficulty": {"$ifNull": ["$question.difficulty", "medium"]},
        }},
    ]

    count = 0
    async for doc in solved_col.aggregate(pipeline):
        q_data = {
            "id": str(doc.get("question_id", "")),
            "topic": doc.get("topic", ""),
            "sub_topic": doc.get("sub_topic", ""),
            "companies": doc.get("companies", []),
            "difficulty": doc.get("difficulty", "medium"),
        }
        if does_solve_match_quest(quest, q_data):
            count += 1

    return count


# ── API Endpoints ────────────────────────────────────────────────────


@router.get("/daily")
async def get_daily_quests(user=Depends(get_current_user)):
    """Get today's generated quests.

    Returns 3-5 personalized quests based on the user's weak areas,
    SRS reviews due, target companies, and mastery levels.
    Regenerates once per day (cached in daily_quests collection).
    """
    uid = user["id"]
    doc = await _get_or_generate_daily_quests(uid)

    quests = doc.get("quests", [])
    return {
        "date": doc.get("date", _today_str()),
        "quests": [serialize_quest(q) for q in quests],
        "generated_at": doc.get("created_at", datetime.now(timezone.utc)).isoformat()
            if isinstance(doc.get("created_at"), datetime)
            else str(doc.get("created_at", "")),
    }


@router.get("/active")
async def get_active_quests(user=Depends(get_current_user)):
    """Get today's quests with live progress counts.

    Recalculates progress for each quest based on solves today.
    """
    uid = user["id"]
    doc = await _get_or_generate_daily_quests(uid)
    quests = doc.get("quests", [])

    updated_quests = []
    for quest in quests:
        if quest.get("is_complete", False):
            updated_quests.append(serialize_quest(quest))
            continue

        matching = await _count_matching_solves_today(uid, quest)
        progress = check_quest_progress(quest, matching)

        # Update quest state
        quest["current_count"] = progress["current_count"]
        quest["is_complete"] = progress["is_complete"]
        if progress["is_complete"] and not quest.get("completed_at"):
            quest["completed_at"] = datetime.now(timezone.utc).isoformat()

        updated_quests.append(serialize_quest(quest))

    # Persist updated counts back to DB
    quests_col = daily_quests_collection()
    today = _today_str()
    await quests_col.update_one(
        {"user_id": uid, "date": today},
        {"$set": {"quests": quests, "updated_at": datetime.now(timezone.utc)}},
    )

    total_xp = sum(q.get("xp_reward", 0) for q in quests if q.get("is_complete"))
    completed_count = sum(1 for q in quests if q.get("is_complete"))

    return {
        "date": today,
        "quests": updated_quests,
        "completed_count": completed_count,
        "total_count": len(quests),
        "total_xp_earned": total_xp,
    }


@router.post("/record")
async def record_solve(
    req: RecordSolveRequest,
    user=Depends(get_current_user),
):
    """Record a problem solve that may count toward an active quest.

    Checks all active quests for the day and updates progress on any
    matching quest. Returns which quests were affected.
    """
    uid = user["id"]
    doc = await _get_or_generate_daily_quests(uid)
    quests = doc.get("quests", [])

    # Fetch question data for matching
    q_data = await _get_question_for_match(req.question_id)
    if not q_data:
        raise HTTPException(status_code=404, detail="Question not found")

    affected_quests = []
    quests_col = daily_quests_collection()
    today = _today_str()

    for quest in quests:
        if quest.get("is_complete", False):
            continue

        # For SRS quests, check by problem_id
        if quest.get("quest_type") == QuestType.SRS_REVIEW.value:
            due_ids = quest.get("metadata", {}).get("due_card_ids", [])
            if req.question_id not in due_ids:
                continue

        if not does_solve_match_quest(quest, q_data):
            continue

        # Recount progress
        matching = await _count_matching_solves_today(uid, quest)
        progress = check_quest_progress(quest, matching)

        was_complete = quest.get("is_complete", False)
        quest["current_count"] = progress["current_count"]
        quest["is_complete"] = progress["is_complete"]

        if progress["is_complete"] and not was_complete:
            quest["completed_at"] = datetime.now(timezone.utc).isoformat()

        affected_quests.append({
            "quest_id": quest.get("quest_id", ""),
            "quest_type": quest.get("quest_type", ""),
            "title": quest.get("title", ""),
            "progress": progress,
        })

    # Persist updates
    if affected_quests:
        await quests_col.update_one(
            {"user_id": uid, "date": today},
            {"$set": {"quests": quests, "updated_at": datetime.now(timezone.utc)}},
        )

    return {
        "question_id": req.question_id,
        "affected_quests": affected_quests,
        "total_affected": len(affected_quests),
    }


@router.get("/history")
async def get_quest_history(user=Depends(get_current_user)):
    """Get past quest documents for the last 30 days.

    Returns daily quest records with completion status and XP earned.
    """
    uid = user["id"]
    thirty_days_ago = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%d")

    quests_col = daily_quests_collection()
    cursor = quests_col.find({
        "user_id": uid,
        "date": {"$gte": thirty_days_ago},
    }).sort("date", -1)

    docs = await cursor.to_list(30)

    history = []
    for doc in docs:
        quests = doc.get("quests", [])
        total_xp = sum(q.get("xp_reward", 0) for q in quests if q.get("is_complete"))
        completed = sum(1 for q in quests if q.get("is_complete"))
        total = len(quests)

        history.append({
            "date": doc.get("date", ""),
            "total_quests": total,
            "completed_quests": completed,
            "total_xp_earned": total_xp,
            "completion_rate": round(completed / total * 100, 1) if total > 0 else 0,
            "quests": [serialize_quest(q) for q in quests],
        })

    return {
        "history": history,
        "days_returned": len(history),
    }


@router.get("/stats")
async def get_quest_stats(user=Depends(get_current_user)):
    """Get aggregate quest statistics.

    Includes completion rate, total XP earned, streak of daily completions,
    and quests-by-type breakdown.
    """
    uid = user["id"]
    thirty_days_ago = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%d")

    quests_col = daily_quests_collection()
    cursor = quests_col.find({
        "user_id": uid,
        "date": {"$gte": thirty_days_ago},
    })
    docs = await cursor.to_list(30)

    stats = compute_quest_stats(docs)

    return stats
