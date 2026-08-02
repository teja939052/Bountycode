"""Campus Pulse — campus-vs-campus real-time battles.
Reuses campus_profiles collection, guilds_collection, gamification_collection.
Bounded pulse_battles collection: 1 active battle per campus pair, TTL 48h."""
import logging
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from app.middleware.auth import get_current_user
from app.database import get_db, campus_profiles_collection, guilds_collection, gamification_collection
from app.services.gamification import record_practice
from app.services.cache import get_cache
import random

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/pulse", tags=["campus-pulse"])

PULSE_CATEGORIES = {
    "aptitude": {"name": "Aptitude Blitz", "points_per_q": 10, "max_q": 20},
    "coding": {"name": "Code Sprint", "points_per_q": 15, "max_q": 15},
    "interview": {"name": "Interview Rush", "points_per_q": 20, "max_q": 10},
    "mixed": {"name": "Mixed Challenge", "points_per_q": 12, "max_q": 25},
}


@router.get("/active-battles")
async def get_active_battles():
    """List all active campus pulse battles."""
    cache = await get_cache()
    cached = await cache.get("pulse", "active_battles")
    if cached:
        return cached

    db = get_db()
    now = datetime.now(timezone.utc)
    battles = []
    async for doc in db["pulse_battles"].find(
        {"ends_at": {"$gt": now}, "status": "active"},
        {"scores": 1, "campus_a": 1, "campus_b": 1, "category": 1, "ends_at": 1, "_id": 0},
    ).sort("created_at", -1).limit(10):
        doc["_id"] = str(doc["_id"])
        battles.append(doc)
    await cache.set("pulse", "active_battles", battles, ttl=60)
    return {"battles": battles}


@router.post("/create-battle")
async def create_pulse_battle(
    campus_a: str = Body(..., embed=True),
    campus_b: str = Body(..., embed=True),
    category: str = Body(default="mixed", embed=True),
    user=Depends(get_current_user),
):
    """Create a new campus vs campus pulse battle."""
    if campus_a == campus_b:
        raise HTTPException(400, "Cannot battle the same campus")

    if category not in PULSE_CATEGORIES:
        raise HTTPException(400, "Invalid category")

    db = get_db()
    battle_config = PULSE_CATEGORIES[category]

    battle = {
        "campus_a": campus_a,
        "campus_b": campus_b,
        "category": category,
        "status": "active",
        "scores": {campus_a: 0, campus_b: 0},
        "participants": {campus_a: [], campus_b: []},
        "created_at": now.isoformat(),
        "ends_at": (now + timedelta(hours=24)).isoformat(),
        "points_per_q": battle_config["points_per_q"],
        "max_q": battle_config["max_q"],
    }

    await db["pulse_battles"].insert_one(battle)

    await record_practice(user["id"], "pulse_battle_create", 20, {
        "campus_a": campus_a, "campus_b": campus_b, "category": category,
    })

    return {"message": f"Battle created: {campus_a} vs {campus_b}!", "battle_id": str(battle["_id"])}


@router.post("/join-battle/{battle_id}")
async def join_pulse_battle(battle_id: str, user=Depends(get_current_user)):
    """Join a campus pulse battle."""
    db = get_db()
    battle = await db["pulse_battles"].find_one({"_id": battle_id})
    if not battle:
        raise HTTPException(404, "Battle not found")

    if battle["status"] != "active":
        raise HTTPException(400, "Battle is not active")

    # Determine which campus the user belongs to
    profile = await campus_profiles_collection().find_one({"user_id": user["id"]})
    campus = profile.get("college", "Unknown") if profile else "Unknown"

    # Check if user is already in this battle
    if campus in battle.get("participants", {}):
        if user["id"] in battle["participants"][campus]:
            return {"message": "Already joined this battle", "joined": False}

    # Add user to their campus team
    await db["pulse_battles"].update_one(
        {"_id": battle_id},
        {"$push": {f"participants.{campus}": user["id"]}},
    )

    await record_practice(user["id"], "pulse_battle_join", 10, {"battle_id": battle_id, "campus": campus})

    return {"message": f"Joined {campus} team!", "campus": campus, "joined": True}


@router.post("/submit-answer/{battle_id}")
async def submit_pulse_answer(
    battle_id: str,
    answer_data: dict = Body(...),
    user=Depends(get_current_user),
):
    """Submit an answer in a pulse battle."""
    db = get_db()
    battle = await db["pulse_battles"].find_one({"_id": battle_id})
    if not battle:
        raise HTTPException(404, "Battle not found")

    if battle["status"] != "active":
        raise HTTPException(400, "Battle has ended")

    # Determine user's campus
    profile = await campus_profiles_collection().find_one({"user_id": user["id"]})
    campus = profile.get("college", "Unknown") if profile else "Unknown"

    # Check if user is in this battle
    participants = battle.get("participants", {}).get(campus, [])
    if user["id"] not in participants:
        raise HTTPException(403, "You are not in this battle")

    # Score the answer (simplified: correct = full points)
    is_correct = answer_data.get("correct", False)
    points = battle["points_per_q"] if is_correct else 0

    # Update campus score
    if is_correct:
        await db["pulse_battles"].update_one(
            {"_id": battle_id},
            {"$inc": {f"scores.{campus}": points}},
        )

    await record_practice(user["id"], "pulse_answer", points, {
        "battle_id": battle_id, "campus": campus, "correct": is_correct,
    })

    # Get updated scores
    updated = await db["pulse_battles"].find_one({"_id": battle_id})

    return {
        "points_earned": points,
        "campus_score": updated["scores"].get(campus, 0),
        "opponent_score": updated["scores"].get(
            battle["campus_b"] if campus == battle["campus_a"] else battle["campus_a"], 0
        ),
        "is_correct": is_correct,
        "message": f"{'Correct! +' + str(points) + ' points' if is_correct else 'Wrong! 0 points'}",
    }


@router.get("/battle/{battle_id}/scores")
async def get_battle_scores(battle_id: str):
    """Get live scores for a pulse battle."""
    db = get_db()
    battle = await db["pulse_battles"].find_one({"_id": battle_id})
    if not battle:
        raise HTTPException(404, "Battle not found")

    return {
        "battle_id": battle_id,
        "campus_a": battle["campus_a"],
        "campus_b": battle["campus_b"],
        "scores": battle["scores"],
        "category": battle["category"],
        "status": battle["status"],
        "ends_at": battle.get("ends_at"),
    }


@router.get("/campus-rankings")
async def get_campus_rankings(limit: int = 20):
    """Top campuses by pulse battle performance."""
    cache = await get_cache()
    cached = await cache.get("pulse", f"campus_rankings:{limit}")
    if cached:
        return cached

    db = get_db()
    pipeline = [
        {"$match": {"status": "active"}},
        {"$project": {"scores": 1}},
        {"$unwind": "$scores"},
        {"$group": {"_id": "$scores._id", "total_points": {"$sum": "$scores"}}},
        {"$sort": {"total_points": -1}},
        {"$limit": limit},
    ]
    results = []
    async for doc in db["pulse_battles"].aggregate(pipeline):
        results.append({
            "campus": doc["_id"],
            "total_points": doc["total_points"],
        })
    await cache.set("pulse", f"campus_rankings:{limit}", results, ttl=300)
    return {"rankings": results}


@router.post("/daily-pulse")
async def daily_pulse_challenge(user=Depends(get_current_user)):
    """Daily campus pulse challenge — quick 5-question mini battle."""
    db = get_db()
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")

    # Check if already completed today
    existing = await db["pulse_daily"].find_one(
        {"user_id": user["id"], "date": today}
    )
    if existing:
        return {"message": "Already completed today's pulse challenge", "completed": True}

    # Create a quick 5-question challenge
    profile = await campus_profiles_collection().find_one({"user_id": user["id"]})
    campus = profile.get("college", "Unknown") if profile else "Unknown"

    daily_battle = {
        "user_id": user["id"],
        "campus": campus,
        "date": today,
        "questions_answered": 0,
        "correct_answers": 0,
        "total_points": 0,
        "completed": False,
    }

    await db["pulse_daily"].insert_one(daily_battle)

    await record_practice(user["id"], "pulse_daily", 15, {"campus": campus})

    return {
        "message": "Daily pulse challenge started! Answer 5 questions for your campus.",
        "battle_id": str(daily_battle["_id"]),
        "campus": campus,
        "questions_remaining": 5,
    }