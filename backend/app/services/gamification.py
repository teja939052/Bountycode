"""Gamification service module — simplified.

Constitution: ONE currency (diamonds), simplified economy.
- Diamonds: primary reward currency
- Streak: consecutive practice days
- Level: derived from diamonds
- Badges: achievement system
- Daily login: streak bonus

Only writer of diamonds/streak/level/badges.
"""
from datetime import datetime, timezone, timedelta
from app.database import users_collection, gamification_collection
import logging

logger = logging.getLogger(__name__)

BADGES = {
    "first_diamond": {"name": "First Diamond", "emoji": "💎", "description": "Earn your first diamond"},
    "streak_3": {"name": "3-Day Streak", "emoji": "🔥", "description": "Practice 3 days in a row"},
    "streak_7": {"name": "7-Day Streak", "emoji": "⚡", "description": "Practice 7 days in a row"},
    "streak_14": {"name": "14-Day Streak", "emoji": "🌟", "description": "Practice 14 days in a row"},
    "streak_30": {"name": "30-Day Streak", "emoji": "👑", "description": "Practice 30 days in a row"},
    "level_5": {"name": "Apprentice", "emoji": "📚", "description": "Reach level 5"},
    "level_10": {"name": "Scholar", "emoji": "🎓", "description": "Reach level 10"},
    "level_25": {"name": "Expert", "emoji": "🏆", "description": "Reach level 25"},
    "level_50": {"name": "Master", "emoji": "👑", "description": "Reach level 50"},
    "level_100": {"name": "Legend", "emoji": "🌟", "description": "Reach level 100"},
    "interview_1": {"name": "First Interview", "emoji": "🎤", "description": "Complete your first interview"},
    "resume_1": {"name": "First Resume", "emoji": "📄", "description": "Create your first resume"},
    "coding_10": {"name": "Coder", "emoji": "💻", "description": "Solve 10 coding problems"},
    "perfect_10": {"name": "Perfect Score", "emoji": "⭐", "description": "Score 10/10 on any activity"},
}

DIAMONDS_BY_ACTIVITY = {    "interview": 50,
    "resume": 25,
    "aptitude": 25,
    "coding": 40,
    "system_design": 50,
    "question_bank": 35,
    "daily_challenge": 30,
    "lesson_complete": 20,
    "module_complete": 100,
    "practice": 15,
}

STREAK_MULTIPLIERS = {
    0: 1.0,
    3: 1.2,
    7: 1.5,
    14: 2.0,
    30: 3.0,
    60: 4.0,
    100: 5.0,
}

DAILY_LOGIN_REWARDS = [
    {"day": 1, "diamonds": 5},
    {"day": 2, "diamonds": 10},
    {"day": 3, "diamonds": 15},
    {"day": 4, "diamonds": 20},
    {"day": 5, "diamonds": 25},
    {"day": 6, "diamonds": 30},
    {"day": 7, "diamonds": 50},
]


def _calculate_level(diamonds: int) -> int:
    """Calculate level from diamonds. Negative balances clamp to level 1."""
    diamonds = max(0, diamonds or 0)
    return max(1, min(100, int((diamonds / 50) ** 0.5) + 1))


def _calculate_xp(activity_type: str, score: float = 0) -> int:
    """Calculate base diamonds for an activity."""
    base = DIAMONDS_BY_ACTIVITY.get(activity_type, 10)
    if score >= 9:
        return base + 40  # Perfect score bonus
    elif score >= 8:
        return base + 20  # High score bonus
    return base


def _get_streak_multiplier(streak: int) -> float:
    """Get streak multiplier."""
    best = 1.0
    for days, mult in sorted(STREAK_MULTIPLIERS.items()):
        if streak >= days:
            best = mult
    return best


# Bump when the reward math changes. Every ledger row carries the version
# that produced it so profile.diamonds == sum(ledger) stays auditable.
REWARD_POLICY_VERSION = "v1"


async def _append_ledger_event(
    user_id: str,
    activity_type: str,
    diamonds_awarded: int,
    score: float = 0,
    activity_id: str = None,
    metadata: dict = None,
) -> None:
    """Append one immutable gamification_events row. Never updated, never deleted."""
    await gamification_collection.database["gamification_events"].insert_one({
        "user_id": user_id,
        "activity_type": activity_type,
        "activity_id": activity_id,
        "diamonds_awarded": diamonds_awarded,
        "score": score,
        "metadata": metadata or {},
        "reward_policy_version": REWARD_POLICY_VERSION,
        "created_at": datetime.now(timezone.utc),
    })


async def spend_xp(user_id: str, diamonds: int, item: str, metadata: dict = None) -> dict:
    """Spend diamonds. The ONLY debit path (shop, streak repair, etc.).

    Atomic: the decrement applies only when the balance covers it, so two
    concurrent spends can never drive the balance negative.
    """
    if diamonds <= 0:
        raise ValueError("spend_xp requires a positive diamond amount")

    result = await gamification_collection.update_one(
        {"user_id": user_id, "diamonds": {"$gte": diamonds}},
        {
            "$inc": {"diamonds": -diamonds},
            "$set": {"updated_at": datetime.now(timezone.utc)},
        },
    )
    if result.modified_count == 0:
        profile = await gamification_collection.find_one({"user_id": user_id})
        balance = (profile or {}).get("diamonds", 0)
        logger.warning("spend_xp declined: user=%s item=%s cost=%d balance=%d", user_id, item, diamonds, balance)
        return {"success": False, "balance": balance, "message": "Insufficient diamonds"}

    await _append_ledger_event(
        user_id, "spend", -diamonds, 0, activity_id=item, metadata={"item": item, **(metadata or {})},
    )
    profile = await gamification_collection.find_one({"user_id": user_id})
    return {"success": True, "balance": profile.get("diamonds", 0), "spent": diamonds, "item": item}


async def initialize_gamification(user_id: str):
    """Initialize gamification profile for a new user."""
    profile = {
        "user_id": user_id,
        "diamonds": 0,
        "level": 1,
        "streak": 0,
        "longest_streak": 0,
        "last_practice_date": None,
        "badges": [],
        "total_interviews": 0,
        "total_resumes": 0,
        "total_aptitude": 0,
        "total_coding": 0,
        "total_system_design": 0,
        "target_company": None,
        "daily_login_streak": 0,
        "last_daily_login_date": None,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    await gamification_collection.insert_one(profile)
    return profile


async def get_gamification_profile(user_id: str) -> dict:
    """Get gamification profile, initializing if needed."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)
    return profile


async def record_practice(user_id: str, activity_type: str, score: float = 0, metadata: dict = None, role: str = None, activity_id: str = None):
    """Record a practice activity and award diamonds.

    This is the ONLY writer of diamonds/streak/level/badges.
    """
    now = datetime.now(timezone.utc)
    today = now.date()

    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)

    # Update streak
    last_date = profile.get("last_practice_date")
    if last_date:
        last_date = last_date.date() if isinstance(last_date, datetime) else last_date
        days_diff = (today - last_date).days
        if days_diff == 1:
            new_streak = profile.get("streak", 0) + 1
        elif days_diff == 0:
            new_streak = profile.get("streak", 0)
        else:
            new_streak = 1
    else:
        new_streak = 1

    longest_streak = max(profile.get("longest_streak", 0), new_streak)

    # Calculate diamonds
    base_diamonds = _calculate_xp(activity_type, score)
    streak_mult = _get_streak_multiplier(new_streak)
    diamonds_earned = int(base_diamonds * streak_mult)

    # Update activity counters
    updates = {
        "$set": {
            "streak": new_streak,
            "longest_streak": longest_streak,
            "last_practice_date": now,
            "updated_at": now,
        },
        "$inc": {
            "diamonds": diamonds_earned,
        },
    }

    # Increment activity-specific counter
    counter_field = f"total_{activity_type}"
    updates["$inc"][counter_field] = 1

    # Check badges
    current_badges = profile.get("badges", [])
    new_badges = []

    # First diamond badge
    if profile.get("diamonds", 0) == 0 and diamonds_earned > 0:
        new_badges.append("first_diamond")

    # Streak badges
    if new_streak >= 3 and "streak_3" not in current_badges:
        new_badges.append("streak_3")
    if new_streak >= 7 and "streak_7" not in current_badges:
        new_badges.append("streak_7")
    if new_streak >= 14 and "streak_14" not in current_badges:
        new_badges.append("streak_14")
    if new_streak >= 30 and "streak_30" not in current_badges:
        new_badges.append("streak_30")

    # Level badges
    new_level = _calculate_level(profile.get("diamonds", 0) + diamonds_earned)
    if new_level >= 5 and "level_5" not in current_badges:
        new_badges.append("level_5")
    if new_level >= 10 and "level_10" not in current_badges:
        new_badges.append("level_10")
    if new_level >= 25 and "level_25" not in current_badges:
        new_badges.append("level_25")
    if new_level >= 50 and "level_50" not in current_badges:
        new_badges.append("level_50")
    if new_level >= 100 and "level_100" not in current_badges:
        new_badges.append("level_100")

    # Activity badges
    if activity_type == "interview" and profile.get("total_interviews", 0) == 0:
        new_badges.append("interview_1")
    if activity_type == "resume" and profile.get("total_resumes", 0) == 0:
        new_badges.append("resume_1")
    if activity_type == "coding" and profile.get("total_coding", 0) == 9:
        new_badges.append("coding_10")
    if score >= 10 and "perfect_10" not in current_badges:
        new_badges.append("perfect_10")

    if new_badges:
        updates["$addToSet"] = {"badges": {"$each": new_badges}}

    await gamification_collection.update_one({"user_id": user_id}, updates)

    # Record immutable event (ledger)
    await _append_ledger_event(
        user_id, activity_type, diamonds_earned, score,
        activity_id=activity_id,
        metadata={"streak": new_streak, "level": new_level, "badges_earned": new_badges},
    )

    return {
        "diamonds": diamonds_earned,
        "new_diamonds": profile.get("diamonds", 0) + diamonds_earned,
        "level": new_level,
        "streak": new_streak,
        "longest_streak": longest_streak,
        "badges": current_badges + new_badges,
        "new_badges": new_badges,
    }


async def get_leaderboard(limit: int = 50, timeframe: str = "all") -> list:
    """Get top users by diamonds."""
    cursor = gamification_collection.find({}).sort("diamonds", -1).limit(limit)
    results = []
    async for doc in cursor:
        user = await users_collection.find_one({"_id": doc.get("user_id")})
        results.append({
            "user_id": doc.get("user_id"),
            "name": user.get("name") if user else "Unknown",
            "diamonds": doc.get("diamonds", 0),
            "level": doc.get("level", 1),
            "streak": doc.get("streak", 0),
        })
    return results


async def get_badges() -> dict:
    """Get all available badges."""
    return BADGES


async def get_skills(user_id: str) -> dict:
    """Get skill graph for user."""
    profile = await get_gamification_profile(user_id)
    return {
        "level": profile.get("level", 1),
        "diamonds": profile.get("diamonds", 0),
        "streak": profile.get("streak", 0),
        "badges": profile.get("badges", []),
    }


async def get_tower(user_id: str) -> dict:
    """Get tower progression (simplified)."""
    profile = await get_gamification_profile(user_id)
    level = profile.get("level", 1)
    return {
        "level": level,
        "diamonds": profile.get("diamonds", 0),
        "title": f"Level {level}",
    }


async def get_tower_boss(level: int) -> dict:
    """Get boss battle info (simplified)."""
    return {
        "level": level,
        "name": f"Level {level} Challenge",
        "required_score": 70,
    }


async def use_power_up(user_id: str, power_up_id: str) -> dict:
    """Power-ups removed in simplified economy."""
    return {"success": False, "message": "Power-ups removed"}


async def buy_power_up(user_id: str, power_up_id: str) -> dict:
    """Power-ups removed in simplified economy."""
    return {"success": False, "message": "Power-ups removed"}


async def claim_daily_login(user_id: str) -> dict:
    """Claim daily login reward."""
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)

    last_login = profile.get("last_daily_login_date")
    if last_login == today:
        return {"claimed": False, "message": "Already claimed today", "streak": profile.get("daily_login_streak", 0)}

    yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    login_streak = profile.get("daily_login_streak", 0)
    if last_login == yesterday:
        login_streak += 1
    elif last_login != today:
        login_streak = 1

    reward = DAILY_LOGIN_REWARDS[min(login_streak, len(DAILY_LOGIN_REWARDS)) - 1]
    diamonds = reward["diamonds"]

    await gamification_collection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "last_daily_login_date": today,
                "daily_login_streak": login_streak,
            },
            "$inc": {"diamonds": diamonds},
        },
    )
    await _append_ledger_event(
        user_id, "daily_login", diamonds, 0,
        metadata={"login_streak": login_streak},
    )

    return {
        "claimed": True,
        "streak": login_streak,
        "diamonds": diamonds,
    }


async def get_daily_login_calendar(user_id: str, days: int = 7) -> dict:
    """Get daily login calendar."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)

    login_streak = profile.get("daily_login_streak", 0)
    last_login = profile.get("last_daily_login_date")
    calendar = []
    for reward in DAILY_LOGIN_REWARDS[:days]:
        claimed = False
        if last_login:
            try:
                datetime.fromisoformat(last_login)
                claimed = login_streak >= reward["day"]
            except Exception:
                claimed = False
        calendar.append({**reward, "claimed": claimed})

    next_reward = None
    for reward in DAILY_LOGIN_REWARDS:
        if not any(c["day"] == reward["day"] and c["claimed"] for c in calendar):
            next_reward = reward
            break

    return {
        "streak": login_streak,
        "calendar": calendar,
        "next_reward": next_reward,
    }


async def get_achievement_chains(user_id: str) -> dict:
    """Get achievement chains."""
    return {"chains": []}


async def get_streak_status(user_id: str) -> dict:
    """Get streak status."""
    profile = await get_gamification_profile(user_id)
    return {
        "streak": profile.get("streak", 0),
        "longest_streak": profile.get("longest_streak", 0),
        "last_practice_date": profile.get("last_practice_date"),
    }


async def get_forest_state(user_id: str) -> dict:
    """Lightweight forest-journey payload for a user."""
    profile = await get_gamification_profile(user_id)
    return {
        "level": profile.get("level", 1),
        "diamonds": profile.get("diamonds", 0),
        "streak": profile.get("streak", 0),
        "badges": profile.get("badges", []),
    }


async def get_daily_goal(user_id: str) -> dict:
    """Get daily goal (simplified)."""
    return {"goal": 5, "completed": 0}


async def get_daily_bonus(user_id: str) -> dict:
    """Get daily bonus (simplified)."""
    return {"available": True}


async def get_profile_title_progression(user_id: str) -> dict:
    """Get title progression."""
    profile = await get_gamification_profile(user_id)
    level = profile.get("level", 1)
    return {
        "level": level,
        "title": f"Level {level}",
    }


async def get_readiness(user_id: str) -> dict:
    """Get readiness score (simplified)."""
    profile = await get_gamification_profile(user_id)
    return {
        "readiness": min(100, profile.get("level", 1) * 10),
        "level": profile.get("level", 1),
    }


async def get_readiness_simulation(user_id: str, company: str = None) -> dict:
    """Get readiness simulation (simplified)."""
    return await get_readiness(user_id)


async def set_target_company(user_id: str, company: str) -> dict:
    """Set target company."""
    await gamification_collection.update_one(
        {"user_id": user_id},
        {"$set": {"target_company": company, "updated_at": datetime.now(timezone.utc)}},
    )
    return {"success": True, "company": company}


async def award_bonus_xp(user_id: str, diamonds: int, source: str, metadata: dict = None) -> dict:
    """Award bonus diamonds (goes through the ledger like every other credit)."""
    await gamification_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"diamonds": diamonds}, "$set": {"updated_at": datetime.now(timezone.utc)}},
    )
    await _append_ledger_event(
        user_id, "bonus", diamonds, 0,
        metadata={"source": source, **(metadata or {})},
    )
    return {"diamonds": diamonds}


async def streak_freeze(user_id: str) -> dict:
    """Streak freeze removed in simplified economy."""
    return {"success": False, "message": "Streak freeze removed"}


async def streak_repair(user_id: str) -> dict:
    """Streak repair removed in simplified economy."""
    return {"success": False, "message": "Streak repair removed"}


async def get_powerups(user_id: str) -> dict:
    """Power-ups removed in simplified economy."""
    return {"powerups": []}


async def get_tower_challenges(user_id: str) -> dict:
    """Tower challenges removed in simplified economy."""
    return {"challenges": []}


async def claim_tower_challenge(user_id: str, challenge_type: str, challenge_id: str) -> dict:
    """Tower challenges removed in simplified economy."""
    return {"success": False, "message": "Challenges removed"}


async def get_startup_state(user_id: str) -> dict:
    """Startup state for app initialization."""
    profile = await get_gamification_profile(user_id)
    return {
        "level": profile.get("level", 1),
        "diamonds": profile.get("diamonds", 0),
        "streak": profile.get("streak", 0),
        "daily_goal_completed": profile.get("daily_goal_completed", False),
    }


async def get_combo_state(user_id: str) -> dict:
    """Combo state removed in simplified economy."""
    return {"current_combo": 0, "multiplier": 1}


async def get_league_state(user_id: str) -> dict:
    """League state removed in simplified economy."""
    return {"league": "bronze", "rank": 0}


async def get_daily_bonus_history(user_id: str, limit: int = 30) -> list:
    """Daily bonus history removed in simplified economy."""
    return []


async def get_leaderboard_nearby(limit: int = 10) -> list:
    """Get nearby users in leaderboard (simplified)."""
    return await get_leaderboard(limit)
