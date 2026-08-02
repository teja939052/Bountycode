"""
Learning Hub service — progress tracking, XP rewards, daily goals, quick practice.
"""
from datetime import datetime, timezone, timedelta
from app.database import learning_progress_collection, users_collection, get_client
from app.data.curriculum import get_random_lessons
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


async def get_user_progress(user_id: str):
    """Get complete learning progress for a user across all languages."""
    doc = await learning_progress_collection.find_one({"user_id": user_id})
    if not doc:
        return {
            "user_id": user_id,
            "languages": {},
            "total_xp": 0,
            "total_lessons_completed": 0,
            "daily_completed": [],
            "daily_date": None,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    return doc


async def get_language_progress(user_id: str, language_id: str):
    """Get progress for a specific language."""
    doc = await learning_progress_collection.find_one({"user_id": user_id})
    if not doc:
        return {"completed_lessons": [], "total_xp": 0}
    return doc.get("languages", {}).get(language_id, {
        "completed_lessons": [], "total_xp": 0,
    })


async def complete_lesson(user_id: str, language_id: str, lesson_id: str, xp: int):
    """Mark a lesson as completed and award XP."""
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    existing = await learning_progress_collection.find_one(
        {"user_id": user_id},
        {"languages": 1, "daily_completed": 1, "daily_date": 1, "daily_goal_bonus_date": 1, "total_xp": 1},
    )

    if not existing:
        existing = {
            "languages": {},
            "daily_completed": [],
            "daily_date": today,
            "daily_goal_bonus_date": None,
            "total_xp": 0,
        }

    # Reset the rolling daily tracker when the calendar day changes.
    if existing.get("daily_date") != today:
        await learning_progress_collection.update_one(
            {"user_id": user_id},
            {"$set": {"daily_completed": [], "daily_date": today}},
            upsert=True,
        )
        existing["daily_completed"] = []
        existing["daily_date"] = today
        existing["daily_goal_bonus_date"] = None

    lang_progress = existing.get("languages", {}).get(language_id, {"completed_lessons": [], "total_xp": 0})
    if lesson_id in lang_progress.get("completed_lessons", []):
        daily_completed = len(existing.get("daily_completed", []))
        return {
            "xp_gained": 0,
            "base_xp": 0,
            "bonus_xp": 0,
            "total_xp": existing.get("total_xp", 0),
            "daily_completed": daily_completed,
            "daily_goal": 3,
            "daily_goal_reached": daily_completed >= 3,
            "lessons_completed_today": daily_completed,
            "already_completed": True,
        }

    # ─── Transactional lesson completion ───
    # Wraps: lesson add + XP inc + daily goal bonus in a MongoDB transaction
    # for atomicity on replica-set deployments (Atlas free tier uses RS).
    try:
        client = get_client()
        async with client.start_session() as session:
            async with session.start_transaction():
                update_result = await learning_progress_collection.update_one(
                    {
                        "user_id": user_id,
                        f"languages.{language_id}.completed_lessons": {"$ne": lesson_id},
                    },
                    {
                        "$setOnInsert": {
                            "user_id": user_id,
                            "languages": {},
                            "total_xp": 0,
                            "total_lessons_completed": 0,
                            "daily_completed": [],
                            "daily_date": today,
                            "daily_goal_bonus_date": None,
                            "created_at": now.isoformat(),
                        },
                        "$addToSet": {
                            f"languages.{language_id}.completed_lessons": lesson_id,
                            "daily_completed": lesson_id,
                        },
                        "$inc": {
                            "total_xp": xp,
                            "total_lessons_completed": 1,
                            f"languages.{language_id}.total_xp": xp,
                        },
                        "$set": {
                            "updated_at": now.isoformat(),
                            "daily_date": today,
                        },
                    },
                    upsert=True,
                    session=session,
                )

                if update_result.matched_count == 0 and update_result.upserted_id is None:
                    await session.abort_transaction()
                    refreshed = await learning_progress_collection.find_one(
                        {"user_id": user_id},
                        {"daily_completed": 1, "daily_date": 1, "total_xp": 1},
                    )
                    daily_completed = len(refreshed.get("daily_completed", [])) if refreshed else 0
                    return {
                        "xp_gained": 0,
                        "base_xp": 0,
                        "bonus_xp": 0,
                        "total_xp": refreshed.get("total_xp", 0) if refreshed else 0,
                        "daily_completed": daily_completed,
                        "daily_goal": 3,
                        "daily_goal_reached": daily_completed >= 3,
                        "lessons_completed_today": daily_completed,
                        "already_completed": True,
                    }

                refreshed = await learning_progress_collection.find_one(
                    {"user_id": user_id},
                    {"daily_completed": 1, "daily_date": 1, "daily_goal_bonus_date": 1, "total_xp": 1},
                    session=session,
                )
                daily_completed = len(refreshed.get("daily_completed", [])) if refreshed else 0
                daily_goal = 3
                bonus_xp = 0

                if daily_completed >= daily_goal and refreshed and refreshed.get("daily_goal_bonus_date") != today:
                    bonus_result = await learning_progress_collection.update_one(
                        {
                            "user_id": user_id,
                            "$or": [
                                {"daily_goal_bonus_date": {"$ne": today}},
                                {"daily_goal_bonus_date": {"$exists": False}},
                            ],
                        },
                        {
                            "$inc": {
                                "total_xp": 30,
                                f"languages.{language_id}.total_xp": 30,
                            },
                            "$set": {
                                "daily_goal_bonus_date": today,
                                "updated_at": now.isoformat(),
                            },
                        },
                        session=session,
                    )
                    if bonus_result.modified_count:
                        bonus_xp = 30

                refreshed_total_xp = (refreshed.get("total_xp", 0) if refreshed else 0) + bonus_xp
    except Exception as exc:
        logger.warning(
            f"Learning transaction failed, falling back to atomic writes: {exc}"
        )
        # ── Fallback: same logic without transactions (standalone mongod) ──
        update_result = await learning_progress_collection.update_one(
            {
                "user_id": user_id,
                f"languages.{language_id}.completed_lessons": {"$ne": lesson_id},
            },
            {
                "$setOnInsert": {
                    "user_id": user_id,
                    "languages": {},
                    "total_xp": 0,
                    "total_lessons_completed": 0,
                    "daily_completed": [],
                    "daily_date": today,
                    "daily_goal_bonus_date": None,
                    "created_at": now.isoformat(),
                },
                "$addToSet": {
                    f"languages.{language_id}.completed_lessons": lesson_id,
                    "daily_completed": lesson_id,
                },
                "$inc": {
                    "total_xp": xp,
                    "total_lessons_completed": 1,
                    f"languages.{language_id}.total_xp": xp,
                },
                "$set": {
                    "updated_at": now.isoformat(),
                    "daily_date": today,
                },
            },
            upsert=True,
        )
        if update_result.matched_count == 0 and update_result.upserted_id is None:
            refreshed = await learning_progress_collection.find_one(
                {"user_id": user_id},
                {"daily_completed": 1, "daily_date": 1, "total_xp": 1},
            )
            daily_completed = len(refreshed.get("daily_completed", [])) if refreshed else 0
            return {
                "xp_gained": 0,
                "base_xp": 0,
                "bonus_xp": 0,
                "total_xp": refreshed.get("total_xp", 0) if refreshed else 0,
                "daily_completed": daily_completed,
                "daily_goal": 3,
                "daily_goal_reached": daily_completed >= 3,
                "lessons_completed_today": daily_completed,
                "already_completed": True,
            }
        refreshed = await learning_progress_collection.find_one(
            {"user_id": user_id},
            {"daily_completed": 1, "daily_date": 1, "daily_goal_bonus_date": 1, "total_xp": 1},
        )
        daily_completed = len(refreshed.get("daily_completed", [])) if refreshed else 0
        daily_goal = 3
        bonus_xp = 0
        if daily_completed >= daily_goal and refreshed and refreshed.get("daily_goal_bonus_date") != today:
            bonus_result = await learning_progress_collection.update_one(
                {
                    "user_id": user_id,
                    "$or": [
                        {"daily_goal_bonus_date": {"$ne": today}},
                        {"daily_goal_bonus_date": {"$exists": False}},
                    ],
                },
                {
                    "$inc": {
                        "total_xp": 30,
                        f"languages.{language_id}.total_xp": 30,
                    },
                    "$set": {
                        "daily_goal_bonus_date": today,
                        "updated_at": now.isoformat(),
                    },
                },
            )
            if bonus_result.modified_count:
                bonus_xp = 30
        refreshed_total_xp = (refreshed.get("total_xp", 0) if refreshed else 0) + bonus_xp

    return {
        "xp_gained": xp + bonus_xp,
        "base_xp": xp,
        "bonus_xp": bonus_xp,
        "total_xp": refreshed_total_xp,
        "daily_completed": daily_completed,
        "daily_goal": daily_goal,
        "daily_goal_reached": daily_completed >= daily_goal,
        "lessons_completed_today": daily_completed,
    }


async def is_lesson_unlocked(user_id: str, language_id: str, lesson_id: str, level_lessons: list):
    """Check if a lesson is unlocked. First lesson is always unlocked.
    Others require the previous lesson to be completed."""
    progress = await get_language_progress(user_id, language_id)
    completed = set(progress.get("completed_lessons", []))

    for i, lesson in enumerate(level_lessons):
        if lesson["id"] == lesson_id:
            if i == 0:
                return True
            prev_id = level_lessons[i - 1]["id"]
            return prev_id in completed
    return False


async def get_daily_goal(user_id: str):
    """Get today's learning goal status."""
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    doc = await learning_progress_collection.find_one({"user_id": user_id})

    if not doc:
        return {"goal": 3, "completed": 0, "bonus_xp": 0, "reached": False}

    if doc.get("daily_date") != today:
        return {"goal": 3, "completed": 0, "bonus_xp": 0, "reached": False}

    completed = len(doc.get("daily_completed", []))
    goal = 3
    return {
        "goal": goal,
        "completed": completed,
        "bonus_xp": 30 if completed >= goal else 0,
        "reached": completed >= goal,
    }


async def get_quick_practice(language_id: str, count: int = 6):
    """Get random lessons for quick practice mode."""
    return get_random_lessons(language_id, count)


async def get_leaderboard(limit: int = 20):
    """Get top learners by total XP."""
    cursor = learning_progress_collection.find(
        {"total_xp": {"$gt": 0}},
        {"user_id": 1, "total_xp": 1, "total_lessons_completed": 1}
    ).sort("total_xp", -1).limit(limit)

    results = []
    async for doc in cursor:
        user = await users_collection.find_one({"_id": ObjectId(doc["user_id"])})
        name = user.get("name", "Anonymous") if user else "Anonymous"
        results.append({
            "user_id": doc["user_id"],
            "name": name,
            "total_xp": doc.get("total_xp", 0),
            "lessons_completed": doc.get("total_lessons_completed", 0),
        })
    return results


async def get_streak(user_id: str):
    """Calculate learning streak (consecutive days with at least 1 lesson)."""
    doc = await learning_progress_collection.find_one({"user_id": user_id})
    if not doc:
        return {"streak": 0, "longest": 0}

    # Count consecutive days from today backwards
    now = datetime.now(timezone.utc)
    streak = 0
    current_date = now.date()

    daily_completed = doc.get("daily_completed", [])
    daily_date = doc.get("daily_date")

    # If completed at least 1 today, start counting
    if daily_date and daily_date == now.strftime("%Y-%m-%d") and len(daily_completed) > 0:
        streak = 1
        current_date -= timedelta(days=1)

    # For simplicity, just check if there's any activity pattern
    # In production you'd store daily activity logs
    return {"streak": streak, "longest": streak}
