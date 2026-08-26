"""Gamification service module.

This module contains the complete gamification system including:
- Level/XP/streak math and progression
- Tower titles, boss battles
- Power-ups, challenges, badges
- Daily bonuses, mystery boxes
- Practice recording and profile management

Intended modular split (follow-up refactor):
- gamification_core.py: _calculate_level, _calculate_xp, calculate_streak_multiplier
- gamification_config.py: TOWER_TITLES, BOSS_BATTLES, POWER_UPS, BADGES, etc.
- gamification_actions.py: record_practice, claim_daily_bonus, open_mystery_box
- gamification_challenges.py: weekly/monthly challenge logic
"""
from datetime import datetime, timezone, timedelta
from app.database import users_collection, gamification_collection, get_client
from bson import ObjectId
import math
import logging
from app.services.usage import can_use_feature, mark_feature_used

logger = logging.getLogger(__name__)

# Activity types that auto-record a milestone on the placement timeline.

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

# ─── Forest Journey: Nature zones (10 bands of 10 levels) ───
# Levels 1-100 map onto a single growing tree's journey through a forest.
# This is a display-only, additive layer on top of the existing tower; the
# stored XP/level/boss data is unchanged.
FOREST_ZONES = [
    {"index": 0, "name": "Seedling Grove",  "level_min": 1,  "level_max": 10,  "stage": "seedling",   "emoji": "🌱", "color": "#a7f3d0", "description": "You sprout. Tiny roots, big potential."},
    {"index": 1, "name": "Sapling Orchard", "level_min": 11, "level_max": 20,  "stage": "sapling",    "emoji": "🌿", "color": "#86efac", "description": "Flexible, fast-growing, reaching for the light."},
    {"index": 2, "name": "Young Forest",    "level_min": 21, "level_max": 30,  "stage": "young",      "emoji": "🌳", "color": "#4ade80", "description": "The grove thickens; branches learn to hold weight."},
    {"index": 3, "name": "Canopy Trail",    "level_min": 31, "level_max": 40,  "stage": "canopy",     "emoji": "🍃", "color": "#22c55e", "description": "You climb above the undergrowth toward the sun."},
    {"index": 4, "name": "Fruiting Tree",   "level_min": 41, "level_max": 50,  "stage": "fruiting",   "emoji": "🍎", "color": "#16a34a", "description": "Knowledge starts bearing fruit others can share."},
    {"index": 5, "name": "Ancient Woods",   "level_min": 51, "level_max": 60,  "stage": "ancient",    "emoji": "🌲", "color": "#15803d", "description": "Deep roots, deep rings, quiet resilience."},
    {"index": 6, "name": "Summit Grove",    "level_min": 61, "level_max": 70,  "stage": "summit",     "emoji": "⛰️", "color": "#166534", "description": "Rare air. Only the tallest trees stand here."},
    {"index": 7, "name": "Crown Canopy",    "level_min": 71, "level_max": 80,  "stage": "crown",      "emoji": "👑", "color": "#14532d", "description": "You crown the forest — the view is yours."},
    {"index": 8, "name": "Legend Tree",     "level_min": 81, "level_max": 90,  "stage": "legend",     "emoji": "🌟", "color": "#0f766e", "description": "Stories are told about trees like you."},
    {"index": 9, "name": "World Tree",      "level_min": 91, "level_max": 100, "stage": "world",      "emoji": "🌍", "color": "#065f46", "description": "Your roots hold up the sky. The forest is you."},
]

# ─── Seasonal Storms: boss battles reimagined as nature ───
# Each boss level (multiple of 10) maps to a seasonal storm alias. Display
# only — original boss mechanics and stored data are unchanged.
SEASONAL_STORMS = {
    10:  {"name": "Monsoon Gale",      "emoji": "🌧️", "element": "rain"},
    20:  {"name": "Autumn Blight",     "emoji": "🍂", "element": "decay"},
    30:  {"name": "Thunderhead",       "emoji": "⛈️", "element": "storm"},
    40:  {"name": "Storm Surge",       "emoji": "🌊", "element": "flood"},
    50:  {"name": "Wildfire Season",   "emoji": "🔥", "element": "fire"},
    60:  {"name": "Frost Front",       "emoji": "❄️", "element": "frost"},
    70:  {"name": "Dust Storm",        "emoji": "🌪️", "element": "wind"},
    80:  {"name": "Tropical Cyclone",  "emoji": "🌀", "element": "cyclone"},
    90:  {"name": "Supercell",         "emoji": "⚡", "element": "lightning"},
    100: {"name": "The Primal Storm",  "emoji": "🌌", "element": "primal"},
}

# ─── Power-up definitions ───
POWER_UPS = {
    "extra_time":   {"name": "Extra Time", "emoji": "⏰", "description": "+5 minutes on timed test", "rarity": "common", "cost": 10},
    "hint_reveal":  {"name": "Hint Reveal", "emoji": "💡", "description": "Show 1 hint for free", "rarity": "common", "cost": 15},
    "retry":        {"name": "Retry", "emoji": "🔄", "description": "One extra attempt per problem", "rarity": "uncommon", "cost": 25},
    "double_xp":    {"name": "Double XP", "emoji": "⚡", "description": "2x XP for 1 hour", "rarity": "rare", "cost": 50},
    "skip_boss":    {"name": "Skip Boss", "emoji": "🛡️", "description": "Skip one boss battle", "rarity": "rare", "cost": 75},
    "show_answer":  {"name": "Show Answer", "emoji": "🎯", "description": "Reveal answer (use wisely!)", "rarity": "legendary", "cost": 100},
    "speed_boost":  {"name": "Speed Boost", "emoji": "🚀", "description": "30s bonus on timed tests", "rarity": "common", "cost": 8},
    "shield":       {"name": "Shield", "emoji": "🛡️", "description": "Block 1 wrong answer penalty", "rarity": "uncommon", "cost": 30},
    "x2_coins":     {"name": "Double Coins", "emoji": "🪙", "description": "2x coins for 1 hour", "rarity": "rare", "cost": 60},
    "auto_save":    {"name": "Auto-Save", "emoji": "💾", "description": "Auto-save code every 30s", "rarity": "common", "cost": 12},
    "night_mode":   {"name": "Night Mode", "emoji": "🌙", "description": "Dark theme for coding", "rarity": "common", "cost": 5},
    "focus_mode":   {"name": "Focus Mode", "emoji": "🎧", "description": "Hide distractions for 25 min", "rarity": "uncommon", "cost": 35},
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
    {"id": "coding_5", "name": "Complete 5 coding challenges", "target": 5, "metric": "coding", "xp_reward": 120},
    {"id": "company_2", "name": "Prep for 2 companies", "target": 2, "metric": "company_prep", "xp_reward": 80},
    {"id": "resume_1", "name": "Build 1 resume", "target": 1, "metric": "resumes", "xp_reward": 60},
    {"id": "questions_10", "name": "Answer 10 questions", "target": 10, "metric": "question_bank", "xp_reward": 90},
    {"id": "streak_14", "name": "14-day streak", "target": 14, "metric": "streak", "xp_reward": 200},
]

MONTHLY_CHALLENGES = [
    {"id": "level_30", "name": "Reach level 30", "target": 30, "metric": "level", "xp_reward": 500},
    {"id": "solve_50", "name": "Solve 50 problems", "target": 50, "metric": "problems_solved", "xp_reward": 300},
    {"id": "interview_5", "name": "Complete 5 mock interviews", "target": 5, "metric": "interviews", "xp_reward": 300},
    {"id": "streak_30", "name": "30-day streak", "target": 30, "metric": "streak", "xp_reward": 500},
    {"id": "level_50", "name": "Reach level 50", "target": 50, "metric": "level", "xp_reward": 1000},
    {"id": "solve_100", "name": "Solve 100 problems", "target": 100, "metric": "problems_solved", "xp_reward": 800},
    {"id": "coding_20", "name": "Complete 20 coding challenges", "target": 20, "metric": "coding", "xp_reward": 600},
    {"id": "aptitude_20", "name": "Complete 20 aptitude tests", "target": 20, "metric": "aptitude", "xp_reward": 400},
    {"id": "hard_10", "name": "Solve 10 hard problems", "target": 10, "metric": "hard_solved", "xp_reward": 500},
    {"id": "perfect_5", "name": "Get 5 perfect scores", "target": 5, "metric": "perfect_scores", "xp_reward": 750},
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

    # Coding badges (expanded)
    "coding_25": {
        "name": "Code Challenger",
        "description": "Complete 25 coding challenges",
        "icon": "💻",
        "category": "coding",
    },
    "coding_50": {
        "name": "Code Expert",
        "description": "Complete 50 coding challenges",
        "icon": "👨‍💻",
        "category": "coding",
    },
    "coding_100": {
        "name": "Code Legend",
        "description": "Complete 100 coding challenges",
        "icon": "👑",
        "category": "coding",
    },
    "easy_10": {
        "name": "Easy Does It",
        "description": "Solve 10 easy problems",
        "icon": "🟢",
        "category": "coding",
    },
    "medium_10": {
        "name": "Medium Mover",
        "description": "Solve 10 medium problems",
        "icon": "🟡",
        "category": "coding",
    },
    "hard_5": {
        "name": "Hard Hacker",
        "description": "Solve 5 hard problems",
        "icon": "🔴",
        "category": "coding",
    },
    "speed_run": {
        "name": "Speed Runner",
        "description": "Solve a problem in under 5 minutes",
        "icon": "⚡",
        "category": "coding",
    },
    "first_accepted": {
        "name": "First Accept",
        "description": "Get your first accepted solution",
        "icon": "✅",
        "category": "coding",
    },
    "streak_5_coding": {
        "name": "Coding Streak",
        "description": "5-day coding streak",
        "icon": "🔥",
        "category": "coding",
    },

    # Question bank badges
    "question_10": {
        "name": "Question Novice",
        "description": "Answer 10 questions",
        "icon": "📝",
        "category": "question_bank",
    },
    "question_50": {
        "name": "Question Master",
        "description": "Answer 50 questions",
        "icon": "📚",
        "category": "question_bank",
    },
    "question_100": {
        "name": "Question Guru",
        "description": "Answer 100 questions",
        "icon": "🧠",
        "category": "question_bank",
    },

    # Daily challenge badges
    "daily_3": {
        "name": "Daily Devotee",
        "description": "Complete 3 daily challenges",
        "icon": "📅",
        "category": "daily",
    },
    "daily_10": {
        "name": "Daily Devotee Pro",
        "description": "Complete 10 daily challenges",
        "icon": "🏅",
        "category": "daily",
    },
    "daily_30": {
        "name": "Daily Champion",
        "description": "Complete 30 daily challenges",
        "icon": "🏆",
        "category": "daily",
    },

    # Tower badges
    "tower_floor_1": {
        "name": "Floor 1 Clear",
        "description": "Reach level 10",
        "icon": "🏰",
        "category": "tower",
    },
    "tower_floor_5": {
        "name": "Floor 5 Clear",
        "description": "Reach level 50",
        "icon": "🏯",
        "category": "tower",
    },
    "tower_floor_10": {
        "name": "Tower Conqueror",
        "description": "Reach level 100",
        "icon": "👑",
        "category": "tower",
    },
    "boss_1": {
        "name": "Boss Slayer",
        "description": "Defeat your first boss",
        "icon": "🐉",
        "category": "tower",
    },
    "boss_5": {
        "name": "Boss Hunter",
        "description": "Defeat 5 bosses",
        "icon": "🎯",
        "category": "tower",
    },
    "boss_10": {
        "name": "Boss Eliminator",
        "description": "Defeat 10 bosses",
        "icon": "💀",
        "category": "tower",
    },

    # Power-up badges
    "powerup_10": {
        "name": "Power-Up Collector",
        "description": "Use 10 power-ups",
        "icon": "🎁",
        "category": "powerups",
    },
    "powerup_50": {
        "name": "Power-Up Master",
        "description": "Use 50 power-ups",
        "icon": "🎮",
        "category": "powerups",
    },

    # Streak badges (expanded)
    "streak_5": {
        "name": "Getting Warm",
        "description": "5-day practice streak",
        "icon": "🌡️",
        "category": "streak",
    },
    "streak_14": {
        "name": "Two Weeks",
        "description": "14-day practice streak",
        "icon": "📅",
        "category": "streak",
    },
    "streak_60": {
        "name": "Month Master",
        "description": "60-day practice streak",
        "icon": "📆",
        "category": "streak",
    },
    "streak_100": {
        "name": "Centurion",
        "description": "100-day practice streak",
        "icon": "💯",
        "category": "streak",
    },

    # Perfect score badges
    "perfect_3": {
        "name": "Triple Perfect",
        "description": "Get 3 perfect scores",
        "icon": "🌟",
        "category": "perfect",
    },
    "perfect_10": {
        "name": "Perfect Ten",
        "description": "Get 10 perfect scores",
        "icon": "💫",
        "category": "perfect",
    },

    # Company prep badges
    "company_5": {
        "name": "Company Scout",
        "description": "Prep for 5 companies",
        "icon": "🏢",
        "category": "company",
    },
    "company_20": {
        "name": "Company Expert",
        "description": "Prep for 20 companies",
        "icon": "🏭",
        "category": "company",
    },
    "company_53": {
        "name": "Company Master",
        "description": "Prep for all 53+ companies",
        "icon": "🌍",
        "category": "company",
    },

    # Resume badges (expanded)
    "resume_5": {
        "name": "Resume Writer",
        "description": "Create 5 resumes",
        "icon": "📄",
        "category": "resume",
    },
    "resume_25": {
        "name": "Resume Pro",
        "description": "Create 25 resumes",
        "icon": "📋",
        "category": "resume",
    },
    "ats_95": {
        "name": "ATS Elite",
        "description": "Achieve 95+ ATS score",
        "icon": "🎯",
        "category": "resume",
    },

    # Aptitude badges (expanded)
    "aptitude_10": {
        "name": "Aptitude Regular",
        "description": "Complete 10 aptitude tests",
        "icon": "🧮",
        "category": "aptitude",
    },
    "aptitude_25": {
        "name": "Aptitude Expert",
        "description": "Complete 25 aptitude tests",
        "icon": "📊",
        "category": "aptitude",
    },
    "aptitude_100": {
        "name": "Aptitude God",
        "description": "Complete 100 aptitude tests",
        "icon": "🧠",
        "category": "aptitude",
    },

    # Behavioral badges
    "behavioral_5": {
        "name": "Behavioral Pro",
        "description": "Complete 5 behavioral interviews",
        "icon": "💬",
        "category": "behavioral",
    },
    "behavioral_20": {
        "name": "Behavioral Expert",
        "description": "Complete 20 behavioral interviews",
        "icon": "🎤",
        "category": "behavioral",
    },

    # Learning badges
    "lesson_5": {
        "name": "Lesson Learner",
        "description": "Complete 5 lessons",
        "icon": "📖",
        "category": "learning",
    },
    "lesson_20": {
        "name": "Lesson Master",
        "description": "Complete 20 lessons",
        "icon": "🎓",
        "category": "learning",
    },
    "language_3": {
        "name": "Polyglot",
        "description": "Start 3 language paths",
        "icon": "🌐",
        "category": "learning",
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
            "speed_boost": 0, "shield": 0, "x2_coins": 0,
            "auto_save": 0, "night_mode": 0, "focus_mode": 0,
        },
        "bosses_defeated": [],
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
        "bosses_defeated": [],
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

    # Capture the pre-activity streak for milestone-chest detection (the
    # profile object is re-read with the *new* streak after the writes below).
    old_streak = profile.get("streak", 0)

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
    coins_earned = 10 + (stars * 5)  # 15-25 coins per activity

    # Apply active Double XP power-up (time-limited, set via use_power_up)
    dxp_expires = profile.get("double_xp_expires")
    if dxp_expires:
        try:
            exp_dt = datetime.fromisoformat(str(dxp_expires))
            if exp_dt > now:
                xp_gained = int(xp_gained * 2)
                coins_earned = int(coins_earned * 2)
        except (ValueError, TypeError):
            pass

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

    # ─── Transactional multi-step write ───
    # Wraps: activity update + level recalc + challenge progress in a
    # MongoDB transaction for atomicity on replica-set deployments.
    try:
        client = get_client()
        async with await client.start_session() as session:
            async with session.start_transaction():
                # 1. Record activity (streak, XP, coins, counters)
                coll = gamification_collection()
                await coll.update_one({"user_id": user_id}, update_ops, session=session)

                # 2. Re-read profile within transaction for consistent level calc
                profile = await coll.find_one({"user_id": user_id}, session=session)
                old_level = profile.get("level", 1)
                new_level = _calculate_level(profile.get("xp", 0))
                level_up = new_level != old_level

                if level_up:
                    await coll.update_one(
                        {"user_id": user_id},
                        {"$set": {"level": new_level}},
                        session=session,
                    )
                # 3. Update challenge progress inside the same transaction
                await _update_challenge_progress_tx(
                    user_id, activity_type, score, new_streak, new_level, session
                )
    except Exception as exc:
        logger.warning(
            f"Gamification transaction failed, falling back to atomic writes: {exc}"
        )
        # ── Fallback: same logic without transactions (standalone mongod) ──
        await gamification_collection.update_one({"user_id": user_id}, update_ops)
        profile = await gamification_collection.find_one({"user_id": user_id})
        old_level = profile.get("level", 1)
        new_level = _calculate_level(profile.get("xp", 0))
        level_up = new_level != old_level

        if level_up:
            await gamification_collection.update_one(
                {"user_id": user_id},
                {"$set": {"level": new_level}},
            )
        await _update_challenge_progress(user_id, activity_type, score, new_streak, new_level)

    # Check for new badges
    new_badges = await _check_badges(user_id, activity_type, score, new_streak)

    # Check streak milestone chests (real inventory rewards at 7/14/30/60/100 days)
    milestone_rewards = await _check_streak_milestones(user_id, new_streak, old_streak)

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
        "milestone": milestone_rewards,
        "milestone_xp_bonus": sum(r["items"].get("coins", 0) for r in milestone_rewards.values()),
    }

    if boss_result:
        result["boss_defeated"] = boss_result

    return result


def _calculate_xp(activity_type: str, score: float) -> int:
    """Calculate XP gained from an activity — Candy Crush style."""
    base_xp = {
        "interview": 50,
        "resume": 25,
        "aptitude": 25,
        "coding": 40,
        "system_design": 50,
        "cover_letter": 20,
        "question_bank": 35,
        "daily_challenge": 60,
        "tower": 75,
        "boss_battle": 100,
        "practice": 20,
        "lesson": 15,
        "behavioral": 30,
    }.get(activity_type, 10)

    # Difficulty bonus for coding/question_bank
    if activity_type in ("coding", "question_bank"):
        if score >= 9:
            base_xp = 80  # Hard problem
        elif score >= 7:
            base_xp = 40  # Medium
        else:
            base_xp = 20  # Easy

    # Perfect score bonus
    if score >= 10:
        base_xp += 40

    # High score bonus
    if score >= 8:
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


# ─── Forest Journey helpers ───

def forest_zone_for_level(level: int) -> dict:
    """Return the nature zone a level belongs to (1-based bands of 10 levels)."""
    band = min(9, (max(1, level) - 1) // 10)
    return FOREST_ZONES[band]


def seasonal_storm_for_boss(level: int) -> dict | None:
    """Return the seasonal storm alias for a boss level, or None if not a boss."""
    return SEASONAL_STORMS.get(level)


def alias_boss_with_storm(boss: dict | None, level: int) -> dict | None:
    """Merge the seasonal-storm alias into a boss dict without mutating it."""
    if not boss:
        return None
    merged = dict(boss)
    storm = SEASONAL_STORMS.get(level)
    if storm:
        merged["storm"] = storm
        merged["storm_name"] = storm["name"]
        merged["storm_emoji"] = storm["emoji"]
    return merged


def compute_forest_state(level: int, xp: int, streak: int, badges: list, bosses_defeated: list) -> dict:
    """Derive the nature-themed gamification state from existing tower data.

    Purely additive/derived — nothing here mutates stored data:
      - XP        -> sunlight
      - streak    -> waterings
      - badges    -> seeds
      - bosses    -> storms cleared
      - level     -> growth rings (one ring per level)
    """
    zone = forest_zone_for_level(level)
    span = max(1, zone["level_max"] - zone["level_min"])
    zone_progress = min(1.0, (level - zone["level_min"]) / span)
    boss_level = level if level % 10 == 0 and level <= 100 else None
    defeated = list(bosses_defeated or [])
    current_storm = None
    if boss_level and boss_level not in defeated:
        current_storm = seasonal_storm_for_boss(boss_level)
    return {
        "current_zone": zone,
        "zone_index": zone["index"],
        "zones_total": len(FOREST_ZONES),
        "tree_stage": zone["stage"],
        "growth_rings": level,
        "sunlight": xp,
        "waterings": streak or 0,
        "seeds": len(badges or []),
        "storms_cleared": len(defeated),
        "current_storm": current_storm,
        "zone_progress": round(zone_progress, 4),
    }


async def get_forest_state(user_id: str) -> dict:
    """Lightweight forest-journey payload for a user."""
    profile = await get_gamification_profile(user_id)
    if "forest_state" in profile:
        return profile["forest_state"]
    return compute_forest_state(
        level=profile.get("level", 1),
        xp=profile.get("xp", 0),
        streak=profile.get("streak", 0),
        badges=profile.get("badges", []),
        bosses_defeated=profile.get("bosses_defeated", []),
    )


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


async def _update_challenge_progress_tx(
    user_id: str,
    activity_type: str,
    score: float,
    streak: int,
    level: int,
    session,
):
    """Transaction-aware version of _update_challenge_progress.

    Accepts a ``motor`` session object so it participates in the caller's
    transaction.  Reads and writes are routed through the session to ensure
    snapshot-level isolation.
    """
    coll = gamification_collection()
    profile = await coll.find_one({"user_id": user_id}, session=session)
    if not profile:
        return

    now = datetime.now(timezone.utc)
    week_num = now.isocalendar()[1]
    month_key = f"{now.year}-{now.month}"

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
            await coll.update_one(
                {"user_id": user_id}, {"$set": update_ops}, session=session
            )


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
    mult, bonus = calculate_streak_multiplier(profile.get("streak", 0))

    # Current boss info
    boss_level = level if level % 10 == 0 and level <= 100 else None
    current_boss = None
    if boss_level and boss_level not in (profile.get("bosses_defeated") or []):
        current_boss = alias_boss_with_storm(BOSS_BATTLES.get(boss_level), boss_level)

    profile["id"] = str(profile.pop("_id"))
    profile["badges_details"] = [BADGES[b] for b in profile.get("badges", []) if b in BADGES]
    profile["level"] = level
    profile["xp_to_next_level"] = xp_for_next_level(level) - profile.get("xp", 0)
    profile["xp_for_current_level"] = xp_for_level(level)
    profile["title"] = title
    profile["title_emoji"] = emoji
    profile["streak_multiplier"] = mult
    profile["streak_bonus_xp"] = bonus
    profile["current_boss"] = current_boss
    profile["boss_level"] = boss_level
    profile["forest_state"] = compute_forest_state(
        level=level,
        xp=profile.get("xp", 0),
        streak=profile.get("streak", 0),
        badges=profile.get("badges", []),
        bosses_defeated=profile.get("bosses_defeated", []),
    )
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

    if power_up_id == "double_xp":
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        await gamification_collection.update_one(
            {"user_id": user_id},
            {
                "$inc": {f"power_ups.{power_up_id}": -1},
                "$set": {"double_xp_expires": expires_at.isoformat()},
            },
        )
        return {
            "success": True,
            "power_up": POWER_UPS[power_up_id],
            "double_xp_expires": expires_at.isoformat(),
            "double_xp_minutes": 60,
        }
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
STREAK_REPAIR_COST = 100  # coins — restores a broken streak (Duolingo "Streak Repair")

# Daily login bonus calendar (Duolingo-style escalating streak calendar).
# Bonus pays out as XP (10 → 50) + coins; coins only unlock at tier 3+.
DAILY_BONUS_TIERS = {
    0: {"coins": 0},
    1: {"coins": 0},
    2: {"coins": 5},
    3: {"coins": 10},
    4: {"coins": 15},
    5: {"coins": 25},
    6: {"coins": 40},
}

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


async def buy_streak_repair(user_id: str, user: dict = None) -> dict:
    """Restore a broken practice streak for coins (Duolingo-style Streak Repair).

    Free users get 1 Streak Repair/month; Pro/Lifetime = unlimited. If the user
    has a streak_freeze token, it is consumed instead of costing coins.
    """
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)

    # Tier gate: free users limited to FREE_TIER_STREAK_REPAIRS per month.
    if user is not None and user.get("plan") not in ("pro", "lifetime"):
        allowed, reason = can_use_feature(user, "streak_repair")
        if not allowed:
            return {"success": False, "upgrade_required": True, "message": reason}

    coins = profile.get("coins", 0)
    if coins < STREAK_REPAIR_COST:
        return {"success": False, "message": f"Need {STREAK_REPAIR_COST} coins, have {coins}"}

    now = datetime.now(timezone.utc)
    today = now.date()
    last_date = profile.get("last_practice_date")
    if last_date:
        ld = last_date.date() if isinstance(last_date, datetime) else last_date
        days_since = (today - ld).days
    else:
        days_since = 0

    # Only repair a streak broken today (missed exactly yesterday's check).
    if days_since != 1 or profile.get("streak", 0) <= 0:
        return {
            "success": False,
            "message": "Streak not eligible for repair (no streak broken today)",
        }

    streak_freezes = profile.get("streak_freezes", 0)

    # Determine cost source: use a streak_freeze token if available, else coins.
    if streak_freezes > 0:
        update = {
            "$inc": {"streak_freezes": -1},
            "$set": {
                "last_practice_date": now,
                "daily_goal_count": profile.get("daily_goal_count", 0) + 1,
                "daily_goal_date": today.isoformat(),
            },
        }
        message = "Streak repaired using a streak freeze"
        cost = 0
    else:
        update = {
            "$inc": {"coins": -STREAK_REPAIR_COST},
            "$set": {
                "last_practice_date": now,
                "daily_goal_count": profile.get("daily_goal_count", 0) + 1,
                "daily_goal_date": today.isoformat(),
            },
        }
        message = "Streak repaired"
        cost = STREAK_REPAIR_COST

    await gamification_collection.update_one({"user_id": user_id}, update)
    if user is not None and user.get("plan") not in ("pro", "lifetime"):
        await mark_feature_used(user["id"], "streak_repair")
    return {"success": True, "cost": cost, "message": message}


# ─── Streak Milestone Chests (real inventory rewards, not just XP) ───

# Research (Duolingo teardown): milestone celebrations must deliver *real*
# in-game value, not symbolic confetti. Each chest grants functional items.
STREAK_MILESTONE_REWARDS = {
    7:  {"title": "Firestarter", "items": {"streak_freezes": 1, "coins": 100}, "emoji": "🔥"},
    14: {"title": "Hot Streak",  "items": {"streak_freezes": 1, "coins": 250}, "emoji": "🌶️"},
    30: {"title": "Month Master", "items": {"streak_freezes": 2, "coins": 500, "double_xp": 1}, "emoji": "🌙"},
    60: {"title": "Unbreakable",  "items": {"streak_freezes": 3, "coins": 1000, "double_xp": 2}, "emoji": "💎"},
    100: {"title": "Centurion",   "items": {"streak_freezes": 5, "coins": 2000, "double_xp": 3, "skip_boss": 1}, "emoji": "🏯"},
}
STREAK_MILESTONE_DAYS = sorted(STREAK_MILESTONE_REWARDS.keys())


async def _check_streak_milestones(user_id: str, new_streak: int, old_streak: int) -> dict:
    """Grant real inventory rewards when a streak crosses a milestone day.

    Returns a dict describing the milestone chest opened (or empty). Mirrors
    Duolingo's "milestone = chest of real value" design: functional items
    (freezes, XP boosts, coins) the user can hold.
    """
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return {}

    claimed = set(profile.get("streak_milestones_claimed", []))
    result = {}
    crossed = [
        m for m in STREAK_MILESTONE_DAYS
        if old_streak < m <= new_streak and m not in claimed
    ]
    if not crossed:
        return result

    inc = {}
    for m in crossed:
        reward = STREAK_MILESTONE_REWARDS[m]
        result[m] = reward
        for k, v in reward["items"].items():
            if k == "coins":
                inc["coins"] = inc.get("coins", 0) + v
            elif k == "streak_freezes":
                inc["streak_freezes"] = inc.get("streak_freezes", 0) + v
            else:
                # power-up slot
                pu = profile.get("power_ups", {})
                inc[f"power_ups.{k}"] = inc.get(f"power_ups.{k}", 0) + v

    await gamification_collection.update_one(
        {"user_id": user_id},
        {
            "$push": {"streak_milestones_claimed": {"$each": crossed}},
            "$inc": inc,
        },
    )
    return result


async def apply_streak_freeze_on_login(user_id: str) -> dict:
    """Login-time streak protection.

    If the user opened the app after missing exactly one day and still has a
    streak freeze, auto-consume a freeze so opening the app protects the habit
    (recovery mechanic must exist at login — the moment a streak is most
    likely to die). Returns status for the login banner.
    """
    from app.services.gamification import ensure_tower_fields
    await ensure_tower_fields(user_id)
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return {"applied": False, "reason": "no_profile"}

    now = datetime.now(timezone.utc)
    today = now.date()
    last_date = profile.get("last_practice_date")
    if not last_date:
        return {"applied": False, "reason": "no_practice_yet"}
    last_day = last_date.date() if isinstance(last_date, datetime) else last_date
    days_since = (today - last_day).days
    streak = profile.get("streak", 0)
    freezes = profile.get("streak_freezes", 0)

    if days_since == 1 and streak > 0 and freezes > 0:
        await gamification_collection.update_one(
            {"user_id": user_id},
            {"$inc": {"streak_freezes": -1, "streak": 1},
             "$set": {"last_practice_date": now,
                      "streak_frozen_today": True}},
        )
        return {
            "applied": True,
            "streak": streak + 1,
            "freezes_remaining": freezes - 1,
            "message": "🔥 Streak protected! You keep your streak.",
        }
    return {"applied": False, "freezes_remaining": freezes, "days_since_practice": days_since}


# ─── Weekly Leagues (cohort-based promotion/relegation) ───

# Research (Duolingo): weekly reset cadence + promotion/relegation among
# beatable peers drives return visits. Ranks reset each week (Sunday UTC).
LEAGUE_TIERS = [
    {"key": "bronze",  "name": "Bronze",   "icon": "🥉", "min_xp": 0,   "color": "#CD7F32"},
    {"key": "silver",  "name": "Silver",   "icon": "🥈", "min_xp": 500, "color": "#C0C0C0"},
    {"key": "gold",    "name": "Gold",     "icon": "🥇", "min_xp": 1500,"color": "#FFD700"},
    {"key": "platinum","name": "Platinum", "icon": "💎", "min_xp": 4000,"color": "#E5E4E2"},
    {"key": "diamond", "name": "Diamond",  "icon": "♦️", "min_xp": 10000,"color": "#B9F2FF"},
]


def _league_week_id() -> str:
    """ISO week id (Sunday boundary) so leagues reset weekly."""
    now = datetime.now(timezone.utc)
    iso_year, iso_week, _ = now.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"


def _league_for_xp(xp: int):
    tier = LEAGUE_TIERS[0]
    for t in LEAGUE_TIERS:
        if xp >= t["min_xp"]:
            tier = t
    return tier


async def get_league_status(user_id: str) -> dict:
    """Compute the user's weekly league tier + rank within their cohort.

    Cohort: all users with season_xp this week (stored in season_xp_collection
    with season_id matching the weekly league id). Rank is by weekly XP.
    Mirrors Duolingo-style weekly reset + promotion/relegation.
    """
    from app.database import season_xp_collection
    week_id = _league_week_id()
    season_id = f"league-{week_id}"

    user_doc = await season_xp_collection.find_one(
        {"season_id": season_id, "user_id": user_id}
    )
    weekly_xp = user_doc.get("xp", 0) if user_doc else 0

    # Cohort rank: count users strictly above this user's XP (+1).
    rank = max(1, int(await season_xp_collection.count_documents(
        {"season_id": season_id, "xp": {"$gt": weekly_xp}}
    )) + 1)
    cohort_size = int(await season_xp_collection.count_documents({"season_id": season_id}))

    tier = _league_for_xp(weekly_xp)
    n = cohort_size or 1
    top_third = max(1, n // 3)
    bottom_third = max(1, n - top_third)
    promoted = 1 < n and rank <= top_third
    relegated = 1 < n and rank > bottom_third

    return {
        "week": week_id,
        "season_id": season_id,
        "weekly_xp": weekly_xp,
        "rank": rank,
        "of": cohort_size,
        "tier": tier,
        "promoted_next_week": promoted,
        "relegated_next_week": relegated,
        "tiers": LEAGUE_TIERS,
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


async def get_nearby_leaderboard(user_id: str, radius: int = 5, limit: int = 10) -> list:
    """Relative leaderboard: users near *your* XP rank (not absolute top).

    Returns `radius` users above and below the caller's rank, plus the caller.
    Per the gamification literature, relative ("tiered") leaderboards keep
    mid/low performers engaged far longer than a single global absolute board.
    """
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)
    my_xp = profile.get("xp", 0)

    above = gamification_collection.find({"xp": {"$gt": my_xp}}).sort("xp", 1).limit(radius)
    below = (
        gamification_collection.find({"xp": {"$lt": my_xp}})
        .sort("xp", -1)
        .limit(radius)
    )

    async def _compact(cursor):
        out = []
        async for doc in cursor:
            out.append(
                {
                    "user_id": doc.get("user_id", ""),
                    "xp": doc.get("xp", 0),
                    "level": _calculate_level(doc.get("xp", 0)),
                    "streak": doc.get("streak", 0),
                    "badges_count": len(doc.get("badges", [])),
                }
            )
        return out

    above_rows = await _compact(above)
    below_rows = await _compact(below)
    me = {
        "user_id": user_id,
        "xp": my_xp,
        "level": _calculate_level(my_xp),
        "streak": profile.get("streak", 0),
        "badges_count": len(profile.get("badges", [])),
        "is_me": True,
    }
    return below_rows + [me] + above_rows


async def get_streak_status(user_id: str) -> dict:
    """Lean payload for the streak-at-risk nudge (login-time notification).

    Reuses the same logic as get_streak_freeze_status but returns a minimal,
    notification-friendly shape without plan gating so it can be polled cheaply.
    """
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)

    now = datetime.now(timezone.utc)
    today = now.date()
    last_date = profile.get("last_practice_date")
    days_since = 0
    last_ok = False
    if last_date:
        ld = last_date.date() if isinstance(last_date, datetime) else last_date
        days_since = (today - ld).days
        last_ok = True

    streak = profile.get("streak", 0)
    streak_freezes = profile.get("streak_freezes", 0)
    return {
        "streak": streak,
        "days_since_practice": days_since,
        "streak_in_danger": last_ok and days_since >= 1 and streak > 0,
        "streak_freezes": streak_freezes,
        "can_self_repair": streak > 0 and (days_since == 1 or (days_since == 2 and streak_freezes > 0)),
        "daily_bonus_claimed_today": profile.get("last_daily_bonus_date") == today.isoformat(),
    }


async def get_daily_bonus_history(user_id: str, limit: int = 30) -> dict:
    """Return the user's daily login-bonus calendar history (most recent first)."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)
    history = profile.get("daily_bonus_history", []) or []
    history_sorted = sorted(history, key=lambda x: x.get("date", ""), reverse=True)
    login_streak = profile.get("daily_bonus_login_streak", 0)
    last_date = profile.get("last_daily_bonus_date")

    # 60-day calendar grid (most recent 60 days), each cell flagged claimed + xp.
    calendar = _daily_bonus_calendar_grid(history_sorted, login_streak)

    return {
        "login_streak": login_streak,
        "last_claimed": last_date,
        "history": [
            {**h, "count": h.get("xp", 0)} for h in history_sorted[:limit]
        ],
        "calendar": calendar,
    }


def _daily_bonus_calendar_grid(history: list, login_streak: int, days: int = 60) -> list:
    """Build a 60-day login-bonus calendar grid for heatmaps.

    Each entry: {date, claimed, xp, coins, badge}. Unclaimed prior days count
    as a broken-streak break; today is flagged separately for the frontend.
    """
    today = datetime.now(timezone.utc).date()
    by_date = {h.get("date"): h for h in history}
    grid = []
    for i in range(days - 1, -1, -1):
        d = today - timedelta(days=i)
        d_key = d.isoformat()
        h = by_date.get(d_key)
        entry = {
            "date": d_key,
            "claimed": h is not None,
            "xp": h.get("xp", 0) if h else 0,
            "coins": h.get("coins", 0) if h else 0,
            "badge": h.get("badge") if h else None,
        }
        if d_key == today.isoformat():
            entry["today"] = True
        grid.append(entry)
    return grid


async def claim_daily_bonus(user_id: str) -> dict:
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")

    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        profile = await initialize_gamification(user_id)

    last_bonus = profile.get("last_daily_bonus_date")
    if last_bonus and last_bonus == today:
        return {
            "claimed": False,
            "xp_bonus": 0,
            "streak_bonus": 0,
            "badge_unlocked": None,
            "message": "Already claimed today",
        }

    import random
    # Escalating daily bonus: the more days in a row you claim, the bigger the
    # payout. Mirrors Duolingo's streak-calendar reward curve (10 -> 50 + bonus).
    login_streak = profile.get("daily_bonus_login_streak", 0)
    xp_bonus = min(10 + (login_streak * 5), 50)
    streak_bonus = 0
    streak = profile.get("streak", 0)

    if streak >= 30:
        streak_bonus = 200
    elif streak >= 7:
        streak_bonus = 50

    bonus_tier = min(login_streak, 6)
    bonus_rewards = DAILY_BONUS_TIERS[bonus_tier]
    if random.random() < 0.1 or bonus_tier >= 5:
        badge_id = f"daily_bonus_{random.randint(1, 100)}"
        badge_unlocked = {
            "id": badge_id,
            "name": "Lucky Streak",
            "description": "Unlocked from daily bonus!",
            "icon": "🍀",
        }
        badges = profile.get("badges", [])
        badges.append({**badge_unlocked, "earned_at": now.isoformat()})
        await gamification_collection.update_one(
            {"user_id": user_id},
            {"$set": {"badges": badges}}
        )

    total_xp = xp_bonus + streak_bonus
    coin_reward = bonus_rewards.get("coins", 0)

    await gamification_collection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "last_daily_bonus_date": today,
                "daily_bonus_login_streak": login_streak + 1,
            },
            "$inc": {"xp": total_xp, "coins": coin_reward},
            "$push": {
                "daily_bonus_history": {
                    "date": today,
                    "xp": total_xp,
                    "coins": coin_reward,
                    "badge": badge_unlocked["id"] if badge_unlocked else None,
                }
            },
        }
    )

    return {
        "claimed": True,
        "xp_bonus": xp_bonus,
        "streak_bonus": streak_bonus,
        "coins_bonus": coin_reward,
        "login_streak": login_streak + 1,
        "bonus_tier": bonus_tier,
        "badge_unlocked": badge_unlocked,
    }
