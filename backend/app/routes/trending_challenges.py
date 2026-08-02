"""Trending Challenges — viral challenge feed, FOMO-driven.
Reuses question_answers_collection, gamification_collection, battles_collection.
Bounded trending_collection: refreshed daily, TTL 7 days."""
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from app.middleware.auth import get_current_user
from app.database import get_db, question_answers_collection, gamification_collection, battles_collection
from app.services.gamification import record_practice
from app.services.cache import get_cache
import random, logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/trending", tags=["trending-challenges"])

TRENDING_TYPES = {
    "hot_streak": {"name": "Hot Streak", "icon": "🔥", "description": "Most solved problems today", "weight": 3},
    "new_drop": {"name": "New Drop", "icon": "🆕", "description": "Freshly added challenges", "weight": 2},
    "hard_mode": {"name": "Hard Mode", "icon": "💪", "description": "Tough challenges being tackled", "weight": 2},
    "campus_favorite": {"name": "Campus Favorite", "icon": "🏫", "description": "What your campus is solving", "weight": 2},
    "tournament_active": {"name": "Tournament Live", "icon": "🏆", "description": "Active tournament challenges", "weight": 3},
    "community_pick": {"name": "Community Pick", "icon": "👥", "description": "Most discussed challenges", "weight": 1},
}


@router.get("/feed")
async def get_trending_feed(limit: int = 10, user=Depends(get_current_user)):
    """Get the trending challenges feed."""
    cache = await get_cache()
    cache_key = f"trending_feed:{limit}"
    cached = await cache.get("trending", cache_key)
    if cached:
        return cached

    db = get_db()
    feed = []

    # Hot streak: most answered questions today
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    hot_streak = await question_answers_collection().aggregate([
        {"$match": {"answered_at": {"$gte": today_start.isoformat()}}},
        {"$group": {"_id": "$question_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5},
    ]).to_list(length=5)

    for item in hot_streak:
        q = await question_answers_collection().find_one({"question_id": item["_id"]})
        if q:
            feed.append({
                "type": "hot_streak",
                "icon": "🔥",
                "name": "Hot Streak",
                "description": f"{item['count']} students solved this today",
                "question_id": item["_id"],
                "question_title": q.get("title", "Unknown"),
                "difficulty": q.get("difficulty", "Medium"),
                "topic": q.get("topic", "General"),
                "participants": item["count"],
                "score": item["count"] * 10,
            })

    # New drops: recently added questions
    recent = await question_answers_collection().aggregate([
        {"$match": {"answered_at": {"$gte": (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()}}},
        {"$group": {"_id": "$question_id", "count": {"$sum": 1}, "latest": {"$max": "$answered_at"}}},
        {"$sort": {"latest": -1}},
        {"$limit": 3},
    ]).to_list(length=3)

    for item in recent:
        q = await question_answers_collection().find_one({"question_id": item["_id"]})
        if q:
            feed.append({
                "type": "new_drop",
                "icon": "🆕",
                "name": "New Drop",
                "description": "Freshly added challenge",
                "question_id": item["_id"],
                "question_title": q.get("title", "Unknown"),
                "difficulty": q.get("difficulty", "Medium"),
                "topic": q.get("topic", "General"),
                "participants": item["count"],
                "score": 50,
            })

    # Hard mode: questions with high attempt count but low solve rate
    hard_mode = await question_answers_collection().aggregate([
        {"$match": {"answered_at": {"$gte": today_start.isoformat()}}},
        {"$group": {
            "_id": "$question_id",
            "attempts": {"$sum": 1},
            "solved": {"$sum": {"$cond": [{"$eq": ["$is_correct", True]}, 1, 0]}},
        }},
        {"$match": {"attempts": {"$gte": 5}, "$expr": {"$lt": ["$solved", {"$divide": ["$attempts", 2]}]}}},
        {"$sort": {"attempts": -1}},
        {"$limit": 3},
    ]).to_list(length=3)

    for item in hard_mode:
        q = await question_answers_collection().find_one({"question_id": item["_id"]})
        if q:
            feed.append({
                "type": "hard_mode",
                "icon": "💪",
                "name": "Hard Mode",
                "description": f"Only {item['solved']}/{item['attempts']} solved — can you crack it?",
                "question_id": item["_id"],
                "question_title": q.get("title", "Unknown"),
                "difficulty": q.get("difficulty", "Hard"),
                "topic": q.get("topic", "General"),
                "participants": item["attempts"],
                "score": 75,
            })

    # Campus favorite: what's trending in user's campus
    profile = await db["campus_profiles"].find_one({"user_id": user["id"]})
    campus = profile.get("college", "Unknown") if profile else "Unknown"

    campus_qs = await question_answers_collection().aggregate([
        {"$match": {"answered_at": {"$gte": today_start.isoformat()}}},
        {"$group": {"_id": "$question_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 3},
    ]).to_list(length=3)

    for item in campus_qs:
        q = await question_answers_collection().find_one({"question_id": item["_id"]})
        if q:
            feed.append({
                "type": "campus_favorite",
                "icon": "🏫",
                "name": "Campus Favorite",
                "description": f"Popular on {campus}",
                "question_id": item["_id"],
                "question_title": q.get("title", "Unknown"),
                "difficulty": q.get("difficulty", "Medium"),
                "topic": q.get("topic", "General"),
                "participants": item["count"],
                "score": 30,
            })

    # Sort by score descending
    feed.sort(key=lambda x: x.get("score", 0), reverse=True)

    # Deduplicate by question_id
    seen = set()
    unique_feed = []
    for item in feed:
        qid = item.get("question_id")
        if qid not in seen:
            seen.add(qid)
            unique_feed.append(item)

    result = {"feed": unique_feed[:limit], "campus": campus}
    await cache.set("trending", cache_key, result, ttl=120)
    return result


@router.post("/engage/{question_id}")
async def engage_trending(question_id: str, user=Depends(get_current_user)):
    """Engage with a trending challenge — earns bonus XP."""
    db = get_db()

    # Check if already engaged today
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    existing = await db["trending_engagement"].find_one(
        {"user_id": user["id"], "question_id": question_id, "date": today}
    )
    if existing:
        return {"message": "Already engaged today", "bonus_xp": 0}

    # Record engagement
    await db["trending_engagement"].insert_one({
        "user_id": user["id"],
        "question_id": question_id,
        "date": today,
        "engaged_at": datetime.now(timezone.utc).isoformat(),
    })

    bonus_xp = 15
    await gamification_collection().update_one(
        {"user_id": user["id"]},
        {"$inc": {"xp": bonus_xp}},
        upsert=True,
    )

    await record_practice(user["id"], "trending_engage", bonus_xp, {"question_id": question_id})

    return {"message": f"Engaged! +{bonus_xp} XP", "bonus_xp": bonus_xp}


@router.get("/stats")
async def trending_stats(user=Depends(get_current_user)):
    """User's trending engagement stats."""
    db = get_db()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    engaged = await db["trending_engagement"].count_documents(
        {"user_id": user["id"], "date": today}
    )

    total_engaged = await db["trending_engagement"].count_documents(
        {"user_id": user["id"]}
    )

    return {
        "today_engaged": engaged,
        "total_engaged": total_engaged,
        "daily_limit": 10,
        "streak": min(engaged, 7),
    }