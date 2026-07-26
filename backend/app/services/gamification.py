from datetime import datetime, timezone, timedelta
from app.database import users_collection, gamification_collection
from bson import ObjectId
import math


# ─── Placement Tower: Level titles ───
TOWER_TITLES = {
    1: ("Hatchling", "🐣"),
    5: ("Novice", "🌱"),
    10: ("Apprentice", "🌿"),
    15: ("Student", "📚"),
    20: ("Learner", "📖"),
    25: ("Adept", "⚔️"),
    30: ("Problem Solver", "🧩"),
    35: ("Code Knight", "🗡️"),
    40: ("Code Warrior", "🚀"),
    45: ("Tactician", "🎯"),
    50: ("Interview Pro", "🏆"),
    55: ("Algorithm Adept", "🔬"),
    60: ("Data Structures Expert", "💡"),
    65: ("Architect", "🏗️"),
    70: ("Algorithm Master", "🔥"),
    75: ("System Sage", "🧙"),
    80: ("Code Sage", "⚡"),
    85: ("Byte Lord", "🌐"),
    90: ("Legendary Programmer", "🏅"),
    95: ("Code Overlord", "👁️"),
    100: ("God of Code", "👑"),
}

# ─── Wizard outfits ───
WIZARD_OUTFITS = {
    1:   {"name": "Novice Robe", "color": "#6b7280", "effect": "none"},
    10:  {"name": "Apprentice Robe", "color": "#22c55e", "effect": "glow"},
    25:  {"name": "Mage Robe", "color": "#3b82f6", "effect": "sparkle"},
    50:  {"name": "Archmage Robe", "color": "#a855f7", "effect": "fire_aura"},
    75:  {"name": "Code Sage Robe", "color": "#f59e0b", "effect": "lightning"},
    100: {"name": "God of Code", "color": "#4CC9F0", "effect": "rainbow_wings"},
}

# ─── Boss definitions ───
BOSS_BATTLES = {
    10:  {"name": "Sliding Window Dragon", "emoji": "🐉", "topic": "sliding_window", "difficulty": "hard", "required_score": 70},
    20:  {"name": "DP Wizard", "emoji": "🧙", "topic": "dynamic_programming", "difficulty": "hard", "required_score": 70},
    30:  {"name": "Graph Knight", "emoji": "🗡️", "topic": "graph", "difficulty": "hard", "required_score": 70},
    40:  {"name": "System Design King", "emoji": "🏰", "topic": "system_design", "difficulty": "hard", "required_score": 70},
    50:  {"name": "Interview Emperor", "emoji": "👑", "topic": "behavioral", "difficulty": "hard", "required_score": 70},
    60:  {"name": "Algorithm Overlord", "emoji": "🔥", "topic": "algorithm", "difficulty": "hard", "required_score": 70},
    70:  {"name": "Data Structure God", "emoji": "🌌", "topic": "data_structure", "difficulty": "hard", "required_score": 70},
    80:  {"name": "Code Lightning", "emoji": "⚡", "topic": "optimization", "difficulty": "hard", "required_score": 70},
    90:  {"name": "Placement Master", "emoji": "🎯", "topic": "all", "difficulty": "hard", "required_score": 70},
    100: {"name": "The Final Boss", "emoji": "🏆", "topic": "ultimate", "difficulty": "expert", "required_score": 80},
}

# ─── Power-up definitions ───
POWER_UPS = {
    "extra_time":   {"name": "Extra Time", "emoji": "⏰", "description": "+5 minutes on timed test", "rarity": "common", "cost": 10},
    "hint_reveal":  {"name": "Hint Reveal", "emoji": "💡", "description": "Show 1 hint for free", "rarity": "common", "cost": 15},
    "retry":        {"name": "Retry", "emoji": "🔄", "description": "One extra attempt per problem", "rarity": "uncommon", "cost": 25},
    "double_xp":    {"name": "Double XP", "emoji": "⚡", "description": "2x XP for 1 hour", "rarity": "rare", "cost": 50},
    "skip_boss":    {"name": "Skip Boss", "emoji": "🛡️", "description": "Skip one boss battle", "rarity": "rare", "cost": 75},
    "show_answer":  {"name": "Show Answer", "emoji": "🎯", "description": "Reveal answer (use wisely!)", "rarity": "legendary", "cost": 100},
}

# ─── Streak multiplier tiers ───
STREAK_MULTIPLIERS = [
    (0,   1.0, 0),
    (3,   1.2, 10),
    (7,   1.5, 50),
    (14,  2.0, 100),
    (30,  3.0, 300),
    (60,  4.0, 500),
    (100, 5.0, 1000),
]

# ─── Weekly challenge templates ───
WEEKLY_CHALLENGES = [
    {"id": "solve_10", "name": "Solve 10 problems", "target": 10, "metric": "problems_solved", "xp_reward": 100},
    {"id": "streak_7", "name": "Maintain 7-day streak", "target": 7, "metric": "streak", "xp_reward": 50},
    {"id": "aptitude_90", "name": "Score 90%+ on 3 aptitude tests", "target": 3, "metric": "aptitude_90plus", "xp_reward": 100},
    {"id": "interview_3", "name": "Complete 3 mock interviews", "target": 3, "metric": "interviews", "xp_reward": 75},
    {"id": "hard_3", "name": "Solve 3 hard problems", "target": 3, "metric": "hard_solved", "xp_reward": 150},
]

MONTHLY_CHALLENGES = [
    {"id": "level_30", "name": "Reach level 30", "target": 30, "metric": "level", "xp_reward": 500},
    {"id": "solve_50", "name": "Solve 50 problems", "target": 50, "metric": "problems_solved", "xp_reward": 300},
    {"id": "interview_5", "name": "Complete 5 mock interviews", "target": 5, "metric": "interviews", "xp_reward": 300},
    {"id": "streak_30", "name": "30-day streak", "target": 30, "metric": "streak", "xp_reward": 500},
]

# Badge definitions
BADGES = {
    # Interview badges
    "first_interview": {
        "name": "First Steps",
        "description": "Complete your first mock interview",
        "icon": "🎯",
        "category": "interview",
    },
    "interview_10": {
        "name": "Interview Pro",
        "description": "Complete 10 mock interviews",
        "icon": "🏆",
        "category": "interview",
    },
    "interview_50": {
        "name": "Interview Master",
        "description": "Complete 50 mock interviews",
        "icon": "👑",
        "category": "interview",
    },
    "perfect_score": {
        "name": "Perfect Score",
        "description": "Score 10/10 in any interview",
        "icon": "⭐",
        "category": "interview",
    },
    "high_score_streak": {
        "name": "On Fire",
        "description": "Score 8+ in 5 consecutive interviews",
        "icon": "🔥",
        "category": "interview",
    },

    # Resume badges
    "first_resume": {
        "name": "Resume Rookie",
        "description": "Create your first resume",
        "icon": "📄",
        "category": "resume",
    },
    "ats_master": {
        "name": "ATS Master",
        "description": "Achieve 90+ ATS score",
        "icon": "🤖",
        "category": "resume",
    },
    "resume_10": {
        "name": "Resume Builder",
        "description": "Create 10 resumes",
        "icon": "📝",
        "category": "resume",
    },

    # Aptitude badges
    "first_aptitude": {
        "name": "Aptitude Starter",
        "description": "Complete your first aptitude test",
        "icon": "🧮",
        "category": "aptitude",
    },
    "aptitude_perfect": {
        "name": "Aptitude Wizard",
        "description": "Score 100% on any aptitude test",
        "icon": "🧙",
        "category": "aptitude",
    },
    "aptitude_50": {
        "name": "Aptitude Champion",
        "description": "Complete 50 aptitude tests",
        "icon": "🏅",
        "category": "aptitude",
    },

    # Coding badges
    "first_coding": {
        "name": "Code Warrior",
        "description": "Complete your first coding challenge",
        "icon": "💻",
        "category": "coding",
    },
    "coding_10": {
        "name": "Coding Ninja",
        "description": "Complete 10 coding challenges",
        "icon": "🥷",
        "category": "coding",
    },
    "hard_problem": {
        "name": "Hard Problem Solver",
        "description": "Solve a hard difficulty problem",
        "icon": "💪",
        "category": "coding",
    },

    # Streak badges
    "streak_3": {
        "name": "Consistent",
        "description": "3-day practice streak",
        "icon": "📅",
        "category": "streak",
    },
    "streak_7": {
        "name": "Dedicated",
        "description": "7-day practice streak",
        "icon": "🗓️",
        "category": "streak",
    },
    "streak_30": {
        "name": "Unstoppable",
        "description": "30-day practice streak",
        "icon": "🚀",
        "category": "streak",
    },

    # Company badges
    "company_ready": {
        "name": "Company Ready",
        "description": "Score 80+ readiness for any company",
        "icon": "🎯",
        "category": "company",
    },

    # System design
    "first_system_design": {
        "name": "Architect",
        "description": "Complete your first system design",
        "icon": "🏗️",
        "category": "system_design",
    },
    "system_design_master": {
        "name": "System Design Master",
        "description": "Score 9+ on a system design question",
        "icon": "🏛️",
        "category": "system_design",
    },
}


async def initialize_gamification(user_id: str):
    """Initialize gamification profile for a new user."""
    profile = {
        "user_id": user_id,
        "xp": 0,
        "level": 1,
        "streak": 0,
        "longest_streak": 0,
        "last_practice_date": None,
        "badges": [],
        "achievements": [],
        "total_interviews": 0,
        "total_resumes": 0,
        "total_aptitude": 0,
        "total_coding": 0,
        "total_system_design": 0,
        # Tower fields
        "stars_total": 0,
        "stars_per_problem": {},
        "coins": 0,
        "power_ups": {
            "extra_time": 0, "hint_reveal": 0, "retry": 0,
            "double_xp": 0, "skip_boss": 0, "show_answer": 0,
        },
        "bosses_defeated": [],
        "wizard_outfit": "novice_robe",
        "first_solve_today": None,
        "weekly_challenges": [],
        "monthly_challenges": [],
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    await gamification_collection.insert_one(profile)
    return profile


async def record_practice(user_id: str, activity_type: str, score: float = 0, metadata: dict = None):
    """Record a practice activity and update gamification with tower mechanics."""
    now = datetime.now(timezone.utc)
    today = now.date()

    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)

    # Ensure tower fields exist (migration for existing users)
    tower_defaults = {
        "stars_total": 0, "coins": 0,
        "power_ups": {k: 0 for k in POWER_UPS},
        "bosses_defeated": [], "wizard_outfit": "novice robe",
        "first_solve_today": None,
        "weekly_challenges": [], "monthly_challenges": [],
        "streak_freezes": 1,
        "daily_goal_count": 0,
        "daily_goal_target": 5,
        "daily_goal_date": None,
    }
    missing = {k: v for k, v in tower_defaults.items() if k not in profile}
    if missing:
        await gamification_collection.update_one({"user_id": user_id}, {"$set": missing})
        profile.update(missing)

    # Update streak — with streak freeze support
    last_date = profile.get("last_practice_date")
    streak_freezes = profile.get("streak_freezes", 0)
    streak_frozen_today = False

    if last_date:
        last_date = last_date.date() if isinstance(last_date, datetime) else last_date
        days_diff = (today - last_date).days
        if days_diff == 1:
            new_streak = profile.get("streak", 0) + 1
        elif days_diff == 0:
            new_streak = profile.get("streak", 0)
        elif days_diff == 2 and streak_freezes > 0:
            # Streak freeze: missed 1 day, use freeze to preserve streak
            new_streak = profile.get("streak", 0) + 1
            streak_freezes -= 1
            streak_frozen_today = True
        else:
            new_streak = 1
    else:
        new_streak = 1

    longest_streak = max(profile.get("longest_streak", 0), new_streak)

    # First solve of day?
    first_solve = profile.get("first_solve_today")
    is_first_today = False
    if first_solve:
        first_date = first_solve.date() if isinstance(first_solve, datetime) else first_solve
        is_first_today = first_date != today
    else:
        is_first_today = True

    # Update daily goal
    daily_goal_date = profile.get("daily_goal_date")
    if daily_goal_date:
        dg_date = daily_goal_date.date() if isinstance(daily_goal_date, datetime) else daily_goal_date
        if dg_date != today:
            daily_goal_count = 1
        else:
            daily_goal_count = profile.get("daily_goal_count", 0) + 1
    else:
        daily_goal_count = 1

    # Calculate XP with multiplier
    base_xp = _calculate_xp(activity_type, score)
    xp_gained = get_xp_with_multiplier(base_xp, new_streak, is_first_today)

    # Calculate stars
    time_taken = metadata.get("time_taken") if metadata else None
    stars = calculate_stars(score, time_taken)

    # Coins earned
    coins_earned = 5 + (stars * 3)  # 8-14 coins per activity

    # Update counters
    counter_field = f"total_{activity_type}s"
    update_ops = {
        "$set": {
            "last_practice_date": now,
            "streak": new_streak,
            "longest_streak": longest_streak,
            "daily_goal_count": daily_goal_count,
            "daily_goal_date": today.isoformat(),
        },
        "$inc": {
            "xp": xp_gained,
            "coins": coins_earned,
            "stars_total": stars,
            counter_field: 1,
        },
        "$currentDate": {"updated_at": True},
    }

    # Update first_solve_today
    if is_first_today:
        update_ops["$set"]["first_solve_today"] = now

    # Deduct streak freeze if used
    if streak_frozen_today:
        update_ops["$set"]["streak_freezes"] = streak_freezes

    await gamification_collection.update_one({"user_id": user_id}, update_ops)

    # ─── Update challenge progress ───
    await _update_challenge_progress(user_id, activity_type, score, new_streak, new_level)

    # Check for new badges
    new_badges = await _check_badges(user_id, activity_type, score, new_streak)

    # Recalculate level
    profile = await gamification_collection.find_one({"user_id": user_id})
    old_level = profile.get("level", 1)
    new_level = _calculate_level(profile.get("xp", 0))
    level_up = new_level != old_level

    if level_up:
        await gamification_collection.update_one(
            {"user_id": user_id},
            {"$set": {"level": new_level}},
        )
        # Update wizard outfit
        outfit = get_wizard_outfit(new_level)
        await gamification_collection.update_one(
            {"user_id": user_id},
            {"$set": {"wizard_outfit": outfit["name"]}},
        )

    # Check if current level is a boss level
    boss_level = new_level if new_level % 10 == 0 and new_level <= 100 else None
    is_boss_defeated = boss_level in (profile.get("bosses_defeated") or [])

    # Auto-check boss eligibility after recording the activity
    boss_result = await check_boss_eligibility(user_id, score, activity_type)

    result = {
        "xp_gained": xp_gained,
        "coins_earned": coins_earned,
        "stars_earned": stars,
        "new_streak": new_streak,
        "new_badges": new_badges,
        "level": new_level,
        "level_up": level_up,
        "old_level": old_level,
        "is_first_today": is_first_today,
        "boss_level": boss_level if boss_level and not is_boss_defeated else None,
        "streak_multiplier": calculate_streak_multiplier(new_streak)[0],
        "streak_frozen": streak_frozen_today,
        "streak_freezes_remaining": streak_freezes,
        "daily_goal_count": daily_goal_count,
        "daily_goal_target": profile.get("daily_goal_target", 5),
    }

    if boss_result:
        result["boss_defeated"] = boss_result

    return result


def _calculate_xp(activity_type: str, score: float) -> int:
    """Calculate XP gained from an activity — Candy Crush style."""
    base_xp = {
        "interview": 30,
        "resume": 15,
        "aptitude": 15,
        "coding": 25,
        "system_design": 30,
        "cover_letter": 15,
        "question_bank": 20,
    }.get(activity_type, 10)

    # Difficulty bonus for coding/question_bank
    if activity_type in ("coding", "question_bank"):
        if score >= 9:
            base_xp = 50  # Hard problem
        elif score >= 7:
            base_xp = 25  # Medium
        else:
            base_xp = 10  # Easy

    # Perfect score bonus
    if score >= 10:
        base_xp += 20

    return base_xp


def _calculate_level(xp: int) -> int:
    """Calculate level from exponential curve: XP_needed(level) = 100 * level."""
    if xp <= 0:
        return 1
    # level = floor(sqrt(xp / 50))
    return max(1, min(100, int(math.sqrt(xp / 50)) + 1))


def xp_for_level(level: int) -> int:
    """Total XP needed to reach a level."""
    return ((level - 1) ** 2) * 50


def xp_for_next_level(level: int) -> int:
    """XP needed to go from current level to next."""
    return (level ** 2) * 50


def get_title_for_level(level: int) -> tuple:
    """Get title and emoji for a level."""
    title = "Hatchling"
    emoji = "🐣"
    for threshold, (t, e) in sorted(TOWER_TITLES.items()):
        if level >= threshold:
            title, emoji = t, e
    return title, emoji


def get_wizard_outfit(level: int) -> dict:
    """Get wizard outfit for a level."""
    outfit = WIZARD_OUTFITS[1]
    for threshold, o in sorted(WIZARD_OUTFITS.items()):
        if level >= threshold:
            outfit = o
    return outfit


def calculate_streak_multiplier(streak: int) -> tuple:
    """Returns (multiplier, bonus_xp) for a streak."""
    mult = 1.0
    bonus = 0
    for min_streak, m, b in STREAK_MULTIPLIERS:
        if streak >= min_streak:
            mult, bonus = m, b
    return mult, bonus


def calculate_stars(score: float, time_taken: int = None, is_optimal: bool = False) -> int:
    """Calculate 1-3 stars based on performance."""
    stars = 1
    if score >= 7:
        stars = 2
    if score >= 9 and (time_taken is None or time_taken < 300):
        stars = 3
    return stars


def get_xp_with_multiplier(base_xp: int, streak: int, is_first_today: bool = False) -> int:
    """Apply streak multiplier and first-solve-of-day bonus."""
    mult, bonus = calculate_streak_multiplier(streak)
    xp = int(base_xp * mult) + bonus
    if is_first_today:
        xp *= 2  # Double XP first solve
    return xp


async def _check_badges(user_id: str, activity_type: str, score: float, streak: int) -> list:
    """Check and award new badges."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    existing_badges = set(profile.get("badges", []))
    new_badges = []

    badge_checks = {
        "interview": [
            ("first_interview", lambda p: p.get("total_interviews", 0) >= 1),
            ("interview_10", lambda p: p.get("total_interviews", 0) >= 10),
            ("interview_50", lambda p: p.get("total_interviews", 0) >= 50),
            ("perfect_score", lambda p: score >= 10),
            ("high_score_streak", lambda p: score >= 8),
        ],
        "resume": [
            ("first_resume", lambda p: p.get("total_resumes", 0) >= 1),
            ("ats_master", lambda p: score >= 90),
            ("resume_10", lambda p: p.get("total_resumes", 0) >= 10),
        ],
        "aptitude": [
            ("first_aptitude", lambda p: p.get("total_aptitude", 0) >= 1),
            ("aptitude_perfect", lambda p: score >= 100),
            ("aptitude_50", lambda p: p.get("total_aptitude", 0) >= 50),
        ],
        "coding": [
            ("first_coding", lambda p: p.get("total_coding", 0) >= 1),
            ("coding_10", lambda p: p.get("total_coding", 0) >= 10),
            ("hard_problem", lambda p: score >= 8),
        ],
        "system_design": [
            ("first_system_design", lambda p: p.get("total_system_design", 0) >= 1),
            ("system_design_master", lambda p: score >= 9),
        ],
        "question_bank": [
            ("first_coding", lambda p: p.get("total_question_bank", 0) >= 1),
            ("hard_problem", lambda p: score >= 8),
        ],
    }

    # Check streak badges
    if streak >= 3:
        badge_checks.setdefault("streak", []).append(("streak_3", lambda p: True))
    if streak >= 7:
        badge_checks.setdefault("streak", []).append(("streak_7", lambda p: True))
    if streak >= 30:
        badge_checks.setdefault("streak", []).append(("streak_30", lambda p: True))

    for badge_id, check_fn in badge_checks.get(activity_type, []):
        if badge_id not in existing_badges and check_fn(profile):
            new_badges.append(badge_id)
            await gamification_collection.update_one(
                {"user_id": user_id},
                {"$push": {"badges": badge_id}},
            )

    return [BADGES[b] for b in new_badges if b in BADGES]


async def _update_challenge_progress(user_id: str, activity_type: str, score: float, streak: int, level: int):
    """Increment challenge progress counters based on activity."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return

    now = datetime.now(timezone.utc)
    week_num = now.isocalendar()[1]
    month_key = f"{now.year}-{now.month}"

    # Only update if challenges are for current period
    if profile.get("challenge_week") != week_num and profile.get("challenge_month") != month_key:
        return

    weekly = profile.get("weekly_challenges", [])
    monthly = profile.get("monthly_challenges", [])
    updated = False

    for ch in weekly:
        if ch.get("completed"):
            continue
        metric = ch.get("metric", "")
        if metric == "problems_solved" and activity_type in ("question_bank", "coding"):
            ch["progress"] = ch.get("progress", 0) + 1
            if ch["progress"] >= ch["target"]:
                ch["completed"] = True
            updated = True
        elif metric == "streak" and streak >= ch["target"]:
            ch["progress"] = streak
            ch["completed"] = True
            updated = True
        elif metric == "aptitude_90plus" and activity_type == "aptitude" and score >= 90:
            ch["progress"] = ch.get("progress", 0) + 1
            if ch["progress"] >= ch["target"]:
                ch["completed"] = True
            updated = True
        elif metric == "interviews" and activity_type == "interview":
            ch["progress"] = ch.get("progress", 0) + 1
            if ch["progress"] >= ch["target"]:
                ch["completed"] = True
            updated = True
        elif metric == "hard_solved" and activity_type in ("question_bank", "coding") and score >= 8:
            ch["progress"] = ch.get("progress", 0) + 1
            if ch["progress"] >= ch["target"]:
                ch["completed"] = True
            updated = True

    for ch in monthly:
        if ch.get("completed"):
            continue
        metric = ch.get("metric", "")
        if metric == "problems_solved" and activity_type in ("question_bank", "coding"):
            ch["progress"] = ch.get("progress", 0) + 1
            if ch["progress"] >= ch["target"]:
                ch["completed"] = True
            updated = True
        elif metric == "level" and level >= ch["target"]:
            ch["progress"] = level
            ch["completed"] = True
            updated = True
        elif metric == "interviews" and activity_type == "interview":
            ch["progress"] = ch.get("progress", 0) + 1
            if ch["progress"] >= ch["target"]:
                ch["completed"] = True
            updated = True
        elif metric == "streak" and streak >= ch["target"]:
            ch["progress"] = streak
            ch["completed"] = True
            updated = True

    if updated:
        update_ops = {}
        if weekly:
            update_ops["weekly_challenges"] = weekly
        if monthly:
            update_ops["monthly_challenges"] = monthly
        if update_ops:
            await gamification_collection.update_one({"user_id": user_id}, {"$set": update_ops})


async def ensure_tower_fields(user_id: str):
    """Add missing tower fields to existing users (migration)."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return await initialize_gamification(user_id)

    defaults = {
        "stars_total": 0,
        "stars_per_problem": {},
        "coins": 0,
        "power_ups": {k: 0 for k in POWER_UPS},
        "bosses_defeated": [],
        "wizard_outfit": "novice robe",
        "first_solve_today": None,
        "weekly_challenges": [],
        "monthly_challenges": [],
    }

    missing = {k: v for k, v in defaults.items() if k not in profile}
    if missing:
        await gamification_collection.update_one(
            {"user_id": user_id},
            {"$set": missing},
        )

    return profile


async def get_gamification_profile(user_id: str) -> dict:
    """Get the full gamification profile with tower data."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)

    level = _calculate_level(profile.get("xp", 0))
    title, emoji = get_title_for_level(level)
    outfit = get_wizard_outfit(level)
    mult, bonus = calculate_streak_multiplier(profile.get("streak", 0))

    # Current boss info
    boss_level = level if level % 10 == 0 and level <= 100 else None
    current_boss = None
    if boss_level and boss_level not in (profile.get("bosses_defeated") or []):
        current_boss = BOSS_BATTLES.get(boss_level)

    profile["id"] = str(profile.pop("_id"))
    profile["badges_details"] = [BADGES[b] for b in profile.get("badges", []) if b in BADGES]
    profile["level"] = level
    profile["xp_to_next_level"] = xp_for_next_level(level) - profile.get("xp", 0)
    profile["xp_for_current_level"] = xp_for_level(level)
    profile["title"] = title
    profile["title_emoji"] = emoji
    profile["wizard_outfit"] = outfit
    profile["streak_multiplier"] = mult
    profile["streak_bonus_xp"] = bonus
    profile["current_boss"] = current_boss
    profile["boss_level"] = boss_level
    profile["power_ups"] = profile.get("power_ups", POWER_UPS.fromkeys([k for k in POWER_UPS], 0))
    profile["coins"] = profile.get("coins", 0)
    profile["stars_total"] = profile.get("stars_total", 0)
    profile["streak_freezes"] = profile.get("streak_freezes", 0)

    # Daily goal
    now = datetime.now(timezone.utc)
    today = now.date()
    daily_goal_date = profile.get("daily_goal_date")
    if daily_goal_date:
        dg_date = daily_goal_date.date() if isinstance(daily_goal_date, datetime) else daily_goal_date
        daily_goal_count = profile.get("daily_goal_count", 0) if dg_date == today else 0
    else:
        daily_goal_count = 0

    profile["daily_goal_count"] = daily_goal_count
    profile["daily_goal_target"] = profile.get("daily_goal_target", 5)
    profile["daily_goal_completed"] = daily_goal_count >= profile.get("daily_goal_target", 5)

    return profile


# ─── Tower-specific functions ───

async def check_boss_eligibility(user_id: str, activity_score: float, activity_type: str) -> dict | None:
    """Check if the user qualifies to defeat their current boss after an activity.

    Boss levels are multiples of 10 (10, 20, ..., 100).
    A boss is auto-defeated when:
      - The user's current level is a boss level (level % 10 == 0)
      - The boss hasn't been defeated yet
      - The activity_score >= the boss's required_score

    Returns boss defeat info dict or None.
    """
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return None

    level = profile.get("level", 1)
    if level % 10 != 0 or level > 100:
        return None

    defeated_list = profile.get("bosses_defeated") or []
    if level in defeated_list:
        return None

    boss = BOSS_BATTLES.get(level)
    if not boss:
        return None

    if activity_score < boss["required_score"]:
        return None

    bonus_xp = level * 10
    bonus_coins = level * 5

    await gamification_collection.update_one(
        {"user_id": user_id},
        {
            "$push": {"bosses_defeated": level},
            "$inc": {"xp": bonus_xp, "coins": bonus_coins},
        },
    )

    return {
        "boss_defeated": True,
        "boss_level": level,
        "boss_name": boss["name"],
        "boss_emoji": boss["emoji"],
        "bonus_xp": bonus_xp,
        "bonus_coins": bonus_coins,
    }


async def use_power_up(user_id: str, power_up_id: str) -> dict:
    """Use a power-up if user has enough."""
    if power_up_id not in POWER_UPS:
        raise ValueError("Invalid power-up")

    profile = await gamification_collection.find_one({"user_id": user_id})
    pows = profile.get("power_ups", {})
    count = pows.get(power_up_id, 0)
    if count <= 0:
        return {"success": False, "message": "No power-ups left"}

    await gamification_collection.update_one(
        {"user_id": user_id},
        {"$inc": {f"power_ups.{power_up_id}": -1}},
    )
    return {"success": True, "power_up": POWER_UPS[power_up_id]}


async def buy_power_up(user_id: str, power_up_id: str) -> dict:
    """Buy a power-up with coins."""
    if power_up_id not in POWER_UPS:
        raise ValueError("Invalid power-up")

    up = POWER_UPS[power_up_id]
    profile = await gamification_collection.find_one({"user_id": user_id})
    coins = profile.get("coins", 0)
    if coins < up["cost"]:
        return {"success": False, "message": f"Need {up['cost']} coins, have {coins}"}

    await gamification_collection.update_one(
        {"user_id": user_id},
        {
            "$inc": {"coins": -up["cost"], f"power_ups.{power_up_id}": 1},
        },
    )
    return {"success": True, "power_up": up, "coins_remaining": coins - up["cost"]}


# ─── Streak Freeze ───

STREAK_FREEZE_COST = 50  # coins

async def buy_streak_freeze(user_id: str) -> dict:
    """Buy a streak freeze for coins."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    coins = profile.get("coins", 0)
    if coins < STREAK_FREEZE_COST:
        return {"success": False, "message": f"Need {STREAK_FREEZE_COST} coins, have {coins}"}

    await gamification_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"coins": -STREAK_FREEZE_COST, "streak_freezes": 1}},
    )
    return {"success": True, "cost": STREAK_FREEZE_COST, "coins_remaining": coins - STREAK_FREEZE_COST}


async def get_streak_freeze_status(user_id: str) -> dict:
    """Get streak freeze status."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    freezes = profile.get("streak_freezes", 0)
    streak = profile.get("streak", 0)

    # Check if streak is in danger (no practice today yet)
    now = datetime.now(timezone.utc)
    today = now.date()
    last_date = profile.get("last_practice_date")
    days_since = 0
    if last_date:
        ld = last_date.date() if isinstance(last_date, datetime) else last_date
        days_since = (today - ld).days

    return {
        "streak_freezes": freezes,
        "streak": streak,
        "days_since_practice": days_since,
        "streak_in_danger": days_since >= 1 and streak > 0,
        "can_freeze": freezes > 0 and days_since == 1 and streak > 0,
        "cost": STREAK_FREEZE_COST,
    }


# ─── Daily Goal ───

async def get_daily_goal(user_id: str) -> dict:
    """Get daily goal progress."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return {"count": 0, "target": 5, "completed": False, "xp_reward": 15}

    now = datetime.now(timezone.utc)
    today = now.date()
    daily_goal_date = profile.get("daily_goal_date")

    if daily_goal_date:
        dg_date = daily_goal_date.date() if isinstance(daily_goal_date, datetime) else daily_goal_date
        if dg_date != today:
            count = 0
        else:
            count = profile.get("daily_goal_count", 0)
    else:
        count = 0

    target = profile.get("daily_goal_target", 5)
    completed = count >= target

    return {
        "count": count,
        "target": target,
        "completed": completed,
        "xp_reward": 15 if not completed else 0,
    }


async def get_challenges(user_id: str) -> dict:
    """Get weekly and monthly challenges for a user."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)

    now = datetime.now(timezone.utc)
    week_num = now.isocalendar()[1]
    month_key = f"{now.year}-{now.month}"

    # Check if challenges need refresh
    stored_week = profile.get("challenge_week")
    stored_month = profile.get("challenge_month")

    weekly = profile.get("weekly_challenges", [])
    monthly = profile.get("monthly_challenges", [])

    if stored_week != week_num:
        # Generate new weekly challenges (pick 3 random)
        import random
        weekly = []
        available = WEEKLY_CHALLENGES.copy()
        for _ in range(min(3, len(available))):
            ch = random.choice(available)
            weekly.append({**ch, "progress": 0, "completed": False, "claimed": False})
            available.remove(ch)
        await gamification_collection.update_one(
            {"user_id": user_id},
            {"$set": {"weekly_challenges": weekly, "challenge_week": week_num}},
        )

    if stored_month != month_key:
        import random
        monthly = []
        available = MONTHLY_CHALLENGES.copy()
        for _ in range(min(3, len(available))):
            ch = random.choice(available)
            monthly.append({**ch, "progress": 0, "completed": False, "claimed": False})
            available.remove(ch)
        await gamification_collection.update_one(
            {"user_id": user_id},
            {"$set": {"monthly_challenges": monthly, "challenge_month": month_key}},
        )

    return {"weekly": weekly, "monthly": monthly}


async def claim_challenge_reward(user_id: str, challenge_type: str, challenge_id: str) -> dict:
    """Claim a completed challenge reward."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    field = f"{challenge_type}_challenges"
    challenges = profile.get(field, [])

    for ch in challenges:
        if ch["id"] == challenge_id and ch["completed"] and not ch["claimed"]:
            ch["claimed"] = True
            await gamification_collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {field: challenges},
                    "$inc": {"xp": ch["xp_reward"], "coins": ch["xp_reward"] // 5},
                },
            )
            return {"success": True, "xp_earned": ch["xp_reward"]}

    return {"success": False, "message": "Challenge not completed or already claimed"}


async def get_leaderboard(limit: int = 10) -> list:
    """Get the top users by XP."""
    cursor = gamification_collection.find().sort("xp", -1).limit(limit)

    leaderboard = []
    async for doc in cursor:
        leaderboard.append({
            "user_id": doc.get("user_id", ""),
            "xp": doc.get("xp", 0),
            "level": _calculate_level(doc.get("xp", 0)),
            "streak": doc.get("streak", 0),
            "badges_count": len(doc.get("badges", [])),
        })

    return leaderboard
