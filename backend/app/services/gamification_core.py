"""Gamification core — pure data + pure math helpers.

Extracted from app.services.gamification to keep that module focused on
orchestration (DB writes, profile/flow logic). This module is a LEAF: it
imports nothing from app.services.gamification, so it cannot create an import
cycle. All symbols defined here are re-exported by app.services.gamification,
so existing consumers (`from app.services.gamification import ...`) are
unchanged.

This split is behavioral no-op: the constants and helper logic below are copied
verbatim from the original gamification module. Do not change the math here.
"""

from __future__ import annotations

import math

# ─── Placement Tower: Level titles ───
# Default generic titles kept as fallback; company-aware titles are computed
# by get_title_for_level with company_id when available.
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

# Company-aware title overrides by level band.
# Used when the user has selected a target company.
COMPANY_TITLE_BANDS: Dict[str, Dict[str, List[tuple[int, str, str]]]] = {
    "tcs": {
        "1-10":  [(1, "TCS Aspirant", "🎯"), (5, "NQT Starter", "📝"), (10, "NQT Ready", "✅")],
        "11-20": [(11, "Aptitude Pro", "🧮"), (15, "TCS Trainee", "💻"), (20, "NQT Advanced", "🚀")],
        "21-30": [(21, "TCS Ready", "⭐"), (25, "TCS Contender", "🏆"), (30, "TCS Candidate", "🎖️")],
        "31-40": [(31, "TCS Finalist", "🌟"), (35, "TCS Select", "💼"), (40, "TCS Offer Ready", "🏢")],
        "41-100": [(41, "TCS Alumnus", "👑"), (50, "Service Prep Master", "👑"), (100, "Service Code Legend", "🏆")],
    },
    "infosys": {
        "1-10":  [(1, "Infosys Aspirant", "🎯"), (5, "Elevate Starter", "📝"), (10, "Elevate Ready", "✅")],
        "11-20": [(11, "Infosys Trainee", "💻"), (15, "Infosys Pro", "🚀"), (20, "Infosys Advanced", "⭐")],
        "21-30": [(21, "Infosys Ready", "🏆"), (25, "Infosys Contender", "🎖️"), (30, "Infosys Candidate", "🌟")],
        "31-40": [(31, "Infosys Finalist", "💼"), (35, "Infosys Select", "🏢"), (40, "Infosys Offer Ready", "👑")],
        "41-100": [(41, "Infosys Alumnus", "👑"), (50, "Service Prep Master", "👑"), (100, "Service Code Legend", "🏆")],
    },
    "wipro": {
        "1-10":  [(1, "Wipro Aspirant", "🎯"), (5, "NLTH Starter", "📝"), (10, "NLTH Ready", "✅")],
        "11-20": [(11, "Wipro Trainee", "💻"), (15, "Wipro Pro", "🚀"), (20, "Wipro Advanced", "⭐")],
        "21-30": [(21, "Wipro Ready", "🏆"), (25, "Wipro Contender", "🎖️"), (30, "Wipro Candidate", "🌟")],
        "31-40": [(31, "Wipro Finalist", "💼"), (35, "Wipro Select", "🏢"), (40, "Wipro Offer Ready", "👑")],
        "41-100": [(41, "Wipro Alumnus", "👑"), (50, "Service Prep Master", "👑"), (100, "Service Code Legend", "🏆")],
    },
    "cognizant": {
        "1-10":  [(1, "CTS Aspirant", "🎯"), (5, "GenC Starter", "📝"), (10, "GenC Ready", "✅")],
        "11-20": [(11, "CTS Trainee", "💻"), (15, "CTS Pro", "🚀"), (20, "CTS Advanced", "⭐")],
        "21-30": [(21, "CTS Ready", "🏆"), (25, "CTS Contender", "🎖️"), (30, "CTS Candidate", "🌟")],
        "31-40": [(31, "CTS Finalist", "💼"), (35, "CTS Select", "🏢"), (40, "CTS Offer Ready", "👑")],
        "41-100": [(41, "CTS Alumnus", "👑"), (50, "Service Prep Master", "👑"), (100, "Service Code Legend", "🏆")],
    },
    "accenture": {
        "1-10":  [(1, "Accenture Aspirant", "🎯"), (5, "Accenture Starter", "📝"), (10, "Accenture Ready", "✅")],
        "11-20": [(11, "Accenture Trainee", "💻"), (15, "Accenture Pro", "🚀"), (20, "Accenture Advanced", "⭐")],
        "21-30": [(21, "Accenture Ready", "🏆"), (25, "Accenture Contender", "🎖️"), (30, "Accenture Candidate", "🌟")],
        "31-40": [(31, "Accenture Finalist", "💼"), (35, "Accenture Select", "🏢"), (40, "Accenture Offer Ready", "👑")],
        "41-100": [(41, "Accenture Alumnus", "👑"), (50, "Service Prep Master", "👑"), (100, "Service Code Legend", "🏆")],
    },
    "google": {
        "1-10":  [(1, "Google Aspirant", "🎯"), (5, "Googler Starter", "📝"), (10, "Googler Ready", "✅")],
        "11-20": [(11, "Google Trainee", "💻"), (15, "Google Pro", "🚀"), (20, "L3 Ready", "⭐")],
        "21-30": [(21, "L3 Candidate", "🏆"), (25, "L3 Contender", "🎖️"), (30, "L3 Ready+", "🌟")],
        "31-40": [(31, "L4 Finalist", "💼"), (35, "L4 Select", "🏢"), (40, "L4 Offer Ready", "👑")],
        "41-100": [(41, "Googler Alumnus", "👑"), (50, "FAANG Ready", "👑"), (100, "Code Legend", "🏆")],
    },
    "amazon": {
        "1-10":  [(1, "Amazon Aspirant", "🎯"), (5, "Amazon Starter", "📝"), (10, "Amazon Ready", "✅")],
        "11-20": [(11, "Amazon Trainee", "💻"), (15, "Amazon Pro", "🚀"), (20, "SDE-1 Ready", "⭐")],
        "21-30": [(21, "SDE-1 Candidate", "🏆"), (25, "SDE-1 Contender", "🎖️"), (30, "SDE-1 Ready+", "🌟")],
        "31-40": [(31, "SDE-2 Finalist", "💼"), (35, "SDE-2 Select", "🏢"), (40, "SDE-2 Offer Ready", "👑")],
        "41-100": [(41, "Amazonian Alumnus", "👑"), (50, "LP Master", "👑"), (100, "Code Legend", "🏆")],
    },
    "microsoft": {
        "1-10":  [(1, "Microsoft Aspirant", "🎯"), (5, "Microsoft Starter", "📝"), (10, "Microsoft Ready", "✅")],
        "11-20": [(11, "Microsoft Trainee", "💻"), (15, "Microsoft Pro", "🚀"), (20, "SDE Ready", "⭐")],
        "21-30": [(21, "SDE Candidate", "🏆"), (25, "SDE Contender", "🎖️"), (30, "SDE Ready+", "🌟")],
        "31-40": [(31, "SDE Finalist", "💼"), (35, "SDE Select", "🏢"), (40, "SDE Offer Ready", "👑")],
        "41-100": [(41, "Microsoft Alumnus", "👑"), (50, "Growth Mindset Master", "👑"), (100, "Code Legend", "🏆")],
    },
    "meta": {
        "1-10":  [(1, "Meta Aspirant", "🎯"), (5, "Meta Starter", "📝"), (10, "Meta Ready", "✅")],
        "11-20": [(11, "Meta Trainee", "💻"), (15, "Meta Pro", "🚀"), (20, "E3 Ready", "⭐")],
        "21-30": [(21, "E3 Candidate", "🏆"), (25, "E3 Contender", "🎖️"), (30, "E3 Ready+", "🌟")],
        "31-40": [(31, "E4 Finalist", "💼"), (35, "E4 Select", "🏢"), (40, "E4 Offer Ready", "👑")],
        "41-100": [(41, "Meta Alumnus", "👑"), (50, "Move Fast Master", "👑"), (100, "Code Legend", "🏆")],
    },
    "uber": {
        "1-10":  [(1, "Uber Aspirant", "🎯"), (5, "Uber Starter", "📝"), (10, "Uber Ready", "✅")],
        "11-20": [(11, "Uber Trainee", "💻"), (15, "Uber Pro", "🚀"), (20, "Uber Advanced", "⭐")],
        "21-30": [(21, "Uber Candidate", "🏆"), (25, "Uber Contender", "🎖️"), (30, "Uber Ready+", "🌟")],
        "31-40": [(31, "Uber Finalist", "💼"), (35, "Uber Select", "🏢"), (40, "Uber Offer Ready", "👑")],
        "41-100": [(41, "Uber Alumnus", "👑"), (50, "Real-Time Systems Master", "👑"), (100, "Code Legend", "🏆")],
    },
    "apple": {
        "1-10":  [(1, "Apple Aspirant", "🎯"), (5, "Apple Starter", "📝"), (10, "Apple Ready", "✅")],
        "11-20": [(11, "Apple Trainee", "💻"), (15, "Apple Pro", "🚀"), (20, "ICT Ready", "⭐")],
        "21-30": [(21, "ICT Candidate", "🏆"), (25, "ICT Contender", "🎖️"), (30, "ICT Ready+", "🌟")],
        "31-40": [(31, "ICT Finalist", "💼"), (35, "ICT Select", "🏢"), (40, "ICT Offer Ready", "👑")],
        "41-100": [(41, "Apple Alumnus", "👑"), (50, "Low-Level Design Master", "👑"), (100, "Code Legend", "🏆")],
    },
}


def _band(level: int) -> str:
    if level <= 10:
        return "1-10"
    if level <= 20:
        return "11-20"
    if level <= 30:
        return "21-30"
    if level <= 40:
        return "31-40"
    return "41-100"


def get_title_for_level(level: int, company_id: Optional[str] = None) -> tuple[str, str]:
    """Return (title, emoji) for a level, optionally company-aware."""
    if company_id:
        bands = COMPANY_TITLE_BANDS.get(company_id.lower(), {})
        band_entries = bands.get(_band(level), [])
        if band_entries:
            # Pick the highest entry <= level
            best = band_entries[0]
            for entry in band_entries:
                if entry[0] <= level:
                    best = entry
            return best[1], best[2]
    return TOWER_TITLES.get(level, TOWER_TITLES.get(max(TOWER_TITLES.keys()), ("Champion", "👑")))


def get_company_title_progression(company_id: str) -> Dict[str, List[Dict[str, Any]]]:
    """Return full title progression for a company (for frontend rendering)."""
    bands = COMPANY_TITLE_BANDS.get(company_id.lower(), {})
    result = {}
    for band, entries in bands.items():
        result[band] = [{"level": lvl, "title": title, "emoji": emoji} for lvl, title, emoji in entries]
    return result


# ─── Proof/Bounty economy ────────────────────────────────────────────────
# Proof = non-spendable mastery currency (earned from learning activities).
# Bounty = spendable cosmetic currency (earned alongside Proof).
# This keeps cosmetic purchases from affecting learning outcomes.
PROOF_BY_ACTIVITY = {
    "mission_step": 10,            # per step in 10-step learning loop
    "mission_complete": 100,       # completing all 10 steps
    "practice_correct": 20,        # per correct practice answer
    "practice_wrong": 5,           # participation proof
    "mock_oa_complete": 200,       # completing a mock OA
    "mock_oa_section": 40,         # per section completed
    "pattern_mastered": 100,       # scoring 80%+ on pattern assessment
    "repair_complete": 50,         # completing a repair mission
    "retest_pass": 80,             # passing a retest after repair
    "streak_daily": 10,            # per day of streak
    "streak_weekly": 100,          # 7-day streak bonus
    "streak_monthly": 500,         # 30-day streak bonus
    "onboarding_complete": 50,     # completing onboarding quest
    "first_mission": 50,           # first mission ever completed
}

BOUNTY_BY_ACTIVITY = {
    "mission_step": 5,
    "mission_complete": 100,
    "practice_correct": 15,
    "practice_wrong": 2,
    "mock_oa_complete": 100,
    "mock_oa_section": 20,
    "pattern_mastered": 100,
    "repair_complete": 30,
    "retest_pass": 50,
    "streak_daily": 5,
    "streak_weekly": 50,
    "streak_monthly": 200,
    "onboarding_complete": 25,
    "first_mission": 25,
}


def calculate_proof(activity_key: str, count: int = 1) -> int:
    """Calculate Proof earned for an activity."""
    return PROOF_BY_ACTIVITY.get(activity_key, 0) * max(1, count)


def calculate_bounty(activity_key: str, count: int = 1) -> int:
    """Calculate Bounty earned for an activity."""
    return BOUNTY_BY_ACTIVITY.get(activity_key, 0) * max(1, count)


def proof_for_xp(xp: float) -> int:
    """Convert legacy XP to Proof (1 XP = 1 Proof)."""
    return int(xp)


def bounty_for_coins(coins: float) -> int:
    """Convert legacy Coins to Bounty (1 Coin = 1 Bounty)."""
    return int(coins)


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
    "double_xp":    {"name": "Double Diamonds", "emoji": "⚡", "description": "2x Diamonds for 1 hour", "rarity": "rare", "cost": 50},
    "skip_boss":    {"name": "Skip Boss", "emoji": "🛡️", "description": "Skip one boss battle", "rarity": "rare", "cost": 75},
    "show_answer":  {"name": "Show Answer", "emoji": "🎯", "description": "Reveal answer (use wisely!)", "rarity": "legendary", "cost": 100},
    "speed_boost":  {"name": "Speed Boost", "emoji": "🚀", "description": "30s bonus on timed tests", "rarity": "common", "cost": 8},
    "shield":       {"name": "Shield", "emoji": "🛡️", "description": "Block 1 wrong answer penalty", "rarity": "uncommon", "cost": 30},
    "x2_coins":     {"name": "Double Coins", "emoji": "🪙", "description": "2x coins for 1 hour", "rarity": "rare", "cost": 60},
    "auto_save":    {"name": "Auto-Save", "emoji": "💾", "description": "Auto-save code every 30s", "rarity": "common", "cost": 12},
    "night_mode":   {"name": "Night Mode", "emoji": "🌙", "description": "Dark theme for coding", "rarity": "common", "cost": 5},
    "focus_mode":   {"name": "Focus Mode", "emoji": "🎧", "description": "Hide distractions for 25 min", "rarity": "uncommon", "cost": 35},
}

# ─── Role-aware progression ───

ROLE_XP_MULTIPLIERS = {
    "sde": {"coding": 1.2, "system_design": 1.1, "aptitude": 1.0},
    "data_science": {"aptitude": 1.1, "coding": 1.0, "system_design": 1.0},
    "devops": {"system_design": 1.2, "coding": 1.1, "aptitude": 1.0},
    "frontend": {"coding": 1.2, "system_design": 1.0, "aptitude": 1.0},
    "backend": {"coding": 1.2, "system_design": 1.1, "aptitude": 1.0},
    "qa": {"aptitude": 1.2, "coding": 1.0, "system_design": 1.0},
    "mobile": {"coding": 1.2, "system_design": 1.0, "aptitude": 1.0},
}

ROLE_BADGE_PRIORITY = {
    "sde": ["coding_100", "system_design_master", "interview_50", "company_53"],
    "data_science": ["aptitude_100", "coding_50", "interview_50", "company_20"],
    "devops": ["system_design_master", "coding_50", "interview_50", "company_20"],
    "frontend": ["coding_100", "system_design_master", "interview_50", "company_20"],
    "backend": ["coding_100", "system_design_master", "interview_50", "company_53"],
    "qa": ["aptitude_100", "coding_50", "interview_50", "company_20"],
    "mobile": ["coding_100", "interview_50", "company_20", "system_design_master"],
}

ROLE_CHAMPION_TITLES = {
    "sde": "SDE Champion",
    "data_science": "Data Science Champion",
    "devops": "DevOps Champion",
    "frontend": "Frontend Champion",
    "backend": "Backend Champion",
    "qa": "QA Champion",
    "mobile": "Mobile Champion",
}


def get_role_xp_multiplier(role: str, activity_type: str) -> float:
    """Return Diamonds multiplier for a role + activity type."""
    role_multipliers = ROLE_XP_MULTIPLIERS.get(role, {})
    return float(role_multipliers.get(activity_type, 1.0))


def get_role_badge_priority(role: str) -> list[str]:
    """Return badge IDs prioritized for a role."""
    return list(ROLE_BADGE_PRIORITY.get(role, []))


def get_role_champion_title(role: str) -> str:
    """Return champion title for a role at max level."""
    return ROLE_CHAMPION_TITLES.get(role, "Champion")


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

# ─── Badge definitions ───
BADGES = {
    "first_interview": {"name": "First Steps", "description": "Complete your first mock interview", "icon": "🎯", "category": "interview", "rarity": "common"},
    "interview_10": {"name": "Interview Pro", "description": "Complete 10 mock interviews", "icon": "🏆", "category": "interview", "rarity": "uncommon"},
    "interview_50": {"name": "Interview Master", "description": "Complete 50 mock interviews", "icon": "👑", "category": "interview", "rarity": "rare"},
    "perfect_score": {"name": "Perfect Score", "description": "Score 10/10 in any interview", "icon": "⭐", "category": "interview", "rarity": "epic"},
    "high_score_streak": {"name": "On Fire", "description": "Score 8+ in an interview", "icon": "🔥", "category": "interview", "rarity": "rare"},
    "first_resume": {"name": "Resume Rookie", "description": "Create your first resume", "icon": "📄", "category": "resume", "rarity": "common"},
    "ats_master": {"name": "ATS Master", "description": "Achieve 90+ ATS score", "icon": "🤖", "category": "resume", "rarity": "uncommon"},
    "resume_10": {"name": "Resume Builder", "description": "Create 10 resumes", "icon": "📝", "category": "resume", "rarity": "uncommon"},
    "first_aptitude": {"name": "Aptitude Starter", "description": "Complete your first aptitude test", "icon": "🧮", "category": "aptitude", "rarity": "common"},
    "aptitude_perfect": {"name": "Aptitude Wizard", "description": "Score 100% on any aptitude test", "icon": "🧙", "category": "aptitude", "rarity": "rare"},
    "aptitude_50": {"name": "Aptitude Champion", "description": "Complete 50 aptitude tests", "icon": "🏅", "category": "aptitude", "rarity": "rare"},
    "first_coding": {"name": "Code Warrior", "description": "Complete your first coding challenge", "icon": "💻", "category": "coding", "rarity": "common"},
    "coding_10": {"name": "Coding Ninja", "description": "Complete 10 coding challenges", "icon": "🥷", "category": "coding", "rarity": "uncommon"},
    "hard_problem": {"name": "Hard Problem Solver", "description": "Score 95+ on a coding challenge", "icon": "💪", "category": "coding", "rarity": "uncommon"},
    "streak_3": {"name": "Consistent", "description": "3-day practice streak", "icon": "📅", "category": "streak", "rarity": "common"},
    "streak_7": {"name": "Dedicated", "description": "7-day practice streak", "icon": "🗓️", "category": "streak", "rarity": "uncommon"},
    "streak_30": {"name": "Unstoppable", "description": "30-day practice streak", "icon": "🚀", "category": "streak", "rarity": "rare"},
    "first_system_design": {"name": "Architect", "description": "Complete your first system design", "icon": "🏗️", "category": "system_design", "rarity": "common"},
    "system_design_master": {"name": "System Design Master", "description": "Score 9+ on a system design question", "icon": "🏛️", "category": "system_design", "rarity": "epic"},
    "coding_25": {"name": "Code Challenger", "description": "Complete 25 coding challenges", "icon": "💻", "category": "coding", "rarity": "uncommon"},
    "coding_50": {"name": "Code Expert", "description": "Complete 50 coding challenges", "icon": "👨‍💻", "category": "coding", "rarity": "rare"},
    "coding_100": {"name": "Code Legend", "description": "Complete 100 coding challenges", "icon": "👑", "category": "coding", "rarity": "epic"},
    "first_accepted": {"name": "First Accept", "description": "Get your first accepted solution", "icon": "✅", "category": "coding", "rarity": "common"},
    "question_10": {"name": "Question Novice", "description": "Answer 10 questions", "icon": "📝", "category": "question_bank", "rarity": "common"},
    "question_50": {"name": "Question Master", "description": "Answer 50 questions", "icon": "📚", "category": "question_bank", "rarity": "uncommon"},
    "question_100": {"name": "Question Guru", "description": "Answer 100 questions", "icon": "🧠", "category": "question_bank", "rarity": "rare"},
    "daily_3": {"name": "Daily Devotee", "description": "Complete 3 daily challenges", "icon": "📅", "category": "daily", "rarity": "common"},
    "daily_10": {"name": "Daily Devotee Pro", "description": "Complete 10 daily challenges", "icon": "🏅", "category": "daily", "rarity": "uncommon"},
    "daily_30": {"name": "Daily Champion", "description": "Complete 30 daily challenges", "icon": "🏆", "category": "daily", "rarity": "rare"},
    "tower_floor_1": {"name": "Floor 1 Clear", "description": "Reach level 10", "icon": "🏰", "category": "tower", "rarity": "common"},
    "tower_floor_5": {"name": "Floor 5 Clear", "description": "Reach level 50", "icon": "🏯", "category": "tower", "rarity": "rare"},
    "tower_floor_10": {"name": "Tower Conqueror", "description": "Reach level 100", "icon": "👑", "category": "tower", "rarity": "legendary"},
    "boss_1": {"name": "Boss Slayer", "description": "Defeat your first boss", "icon": "🐉", "category": "tower", "rarity": "uncommon"},
    "boss_5": {"name": "Boss Hunter", "description": "Defeat 5 bosses", "icon": "🎯", "category": "tower", "rarity": "rare"},
    "boss_10": {"name": "Boss Eliminator", "description": "Defeat 10 bosses", "icon": "💀", "category": "tower", "rarity": "legendary"},
    "powerup_10": {"name": "Power-Up Collector", "description": "Use 10 power-ups", "icon": "🎁", "category": "powerups", "rarity": "common"},
    "powerup_50": {"name": "Power-Up Master", "description": "Use 50 power-ups", "icon": "🎮", "category": "powerups", "rarity": "rare"},
    "streak_5": {"name": "Getting Warm", "description": "5-day practice streak", "icon": "🌡️", "category": "streak", "rarity": "common"},
    "streak_14": {"name": "Two Weeks", "description": "14-day practice streak", "icon": "📅", "category": "streak", "rarity": "uncommon"},
    "streak_60": {"name": "Month Master", "description": "60-day practice streak", "icon": "📆", "category": "streak", "rarity": "epic"},
    "streak_100": {"name": "Centurion", "description": "100-day practice streak", "icon": "💯", "category": "streak", "rarity": "legendary"},
    "perfect_3": {"name": "Triple Perfect", "description": "Get 3 perfect scores", "icon": "🌟", "category": "perfect", "rarity": "rare"},
    "perfect_10": {"name": "Perfect Ten", "description": "Get 10 perfect scores", "icon": "💫", "category": "perfect", "rarity": "epic"},
    "company_5": {"name": "Company Scout", "description": "Prep for 5 companies", "icon": "🏢", "category": "company", "rarity": "common"},
    "company_20": {"name": "Company Expert", "description": "Prep for 20 companies", "icon": "🏭", "category": "company", "rarity": "rare"},
    "company_53": {"name": "Company Master", "description": "Prep for all 53+ companies", "icon": "🌍", "category": "company", "rarity": "epic"},
    "resume_5": {"name": "Resume Writer", "description": "Create 5 resumes", "icon": "📄", "category": "resume", "rarity": "common"},
    "resume_25": {"name": "Resume Pro", "description": "Create 25 resumes", "icon": "📋", "category": "resume", "rarity": "rare"},
    "ats_95": {"name": "ATS Elite", "description": "Achieve 95+ ATS score", "icon": "🎯", "category": "resume", "rarity": "rare"},
    "aptitude_10": {"name": "Aptitude Regular", "description": "Complete 10 aptitude tests", "icon": "🧮", "category": "aptitude", "rarity": "common"},
    "aptitude_25": {"name": "Aptitude Expert", "description": "Complete 25 aptitude tests", "icon": "📊", "category": "aptitude", "rarity": "uncommon"},
    "aptitude_100": {"name": "Aptitude God", "description": "Complete 100 aptitude tests", "icon": "🧠", "category": "aptitude", "rarity": "legendary"},
    "lesson_5": {"name": "Lesson Learner", "description": "Complete 5 lessons", "icon": "📖", "category": "learning", "rarity": "common"},
    "lesson_20": {"name": "Lesson Master", "description": "Complete 20 lessons", "icon": "🎓", "category": "learning", "rarity": "uncommon"},
    "language_3": {"name": "Polyglot", "description": "Start 3 language paths", "icon": "🌐", "category": "learning", "rarity": "uncommon"},
    "lucky_streak": {"name": "Lucky Streak", "description": "Unlocked from daily bonus", "icon": "🍀", "category": "daily", "rarity": "legendary"},
    "first_exam_memory": {"name": "Memory Keeper", "description": "Submit your first exam memory", "icon": "🧠", "category": "exam_memory", "rarity": "common"},
    "exam_memory_5": {"name": "Memory Archiver", "description": "Submit 5 exam memories", "icon": "📚", "category": "exam_memory", "rarity": "uncommon"},
    "exam_memory_10": {"name": "Memory Vault", "description": "Submit 10 exam memories", "icon": "🏛️", "category": "exam_memory", "rarity": "rare"},
}


def normalize_badge_ids(badges) -> list:
    """Canonicalize a stored badges array to unique string IDs.

    LAW: badges are stored as string IDs, hydrated on read. Legacy object
    entries (id/name/icon dicts written by an older daily-bonus path) map
    to their id; anything without a usable id is dropped, never crashed on.
    Pure function — unit-tested.
    """
    out = []
    for b in badges or []:
        if isinstance(b, str) and b:
            bid = b
        elif isinstance(b, dict) and b.get("id"):
            bid = str(b["id"])
        else:
            continue
        if bid not in out:
            out.append(bid)
    return out

# ─── Canonical activity counters ───
# record_practice() writes ONE counter per activity through this map. The
# historical `f"total_{activity_type}s"` produced plural fields
# (total_aptitudes, total_codings) that NO reader consumed, while every
# reader — badge checks, models/gamification, tiers, placement_engine,
# daily_drill, company_conversion — reads the singular names below. Badges
# keyed on aptitude/coding/system_design could therefore never fire from
# engine writes. Keep both sides on these canonical fields.
ACTIVITY_COUNTER_FIELD = {
    "interview": "total_interviews",
    "resume": "total_resumes",
    "aptitude": "total_aptitude",
    "coding": "total_coding",
    "system_design": "total_system_design",
    "question_bank": "total_question_banks",
    "exam_memory": "total_exam_memorys",
    "lesson": "total_lessons",
    "daily_challenge": "total_daily_challenges",
    "daily_challenge_30day": "total_daily_challenge_30days",
    "learning_path": "total_learning_paths",
    "company_track": "total_company_tracks",
    "assignment": "total_assignments",
}

# ─── Declarative badge conditions ───
# CI invariant: every id in BADGES must appear in BADGE_CONDITIONS and vice
# versa (a badge with no condition can never be earned — a catalog lie).
# Two extra counters are incremented behind the scenes so the power-up and
# perfect-score families are earnable:
#   - total_powerups_used  (+1 per use_power_up success)
#   - total_perfect_scores (+1 per record_practice with score10 >= 10)
# Awarded outside the evaluator:
#   - lucky_streak (daily-bonus path, see claim_daily_bonus)
# Every condition is evaluated against the profile + current event. Each
# tuple below: (kind, key/value).
GAMIFICATION_COUNTER_FIELDS = set(ACTIVITY_COUNTER_FIELD.values()) | {
    "total_powerups_used",
    "total_perfect_scores",
}

BADGE_CONDITIONS = {
    "first_interview": ("counter", "total_interviews", 1),
    "interview_10": ("counter", "total_interviews", 10),
    "interview_50": ("counter", "total_interviews", 50),
    "perfect_score": ("score", "interview", 10),
    "high_score_streak": ("score", "interview", 8),
    "first_resume": ("counter", "total_resumes", 1),
    "ats_master": ("score", "resume", 90),
    "resume_10": ("counter", "total_resumes", 10),
    "resume_5": ("counter", "total_resumes", 5),
    "resume_25": ("counter", "total_resumes", 25),
    "ats_95": ("score", "resume", 95),
    "first_aptitude": ("counter", "total_aptitude", 1),
    "aptitude_perfect": ("score", "aptitude", 100),
    "aptitude_50": ("counter", "total_aptitude", 50),
    "aptitude_10": ("counter", "total_aptitude", 10),
    "aptitude_25": ("counter", "total_aptitude", 25),
    "aptitude_100": ("counter", "total_aptitude", 100),
    "first_coding": ("counter", "total_coding", 1),
    "coding_10": ("counter", "total_coding", 10),
    "hard_problem": ("score", "coding", 95),
    "coding_25": ("counter", "total_coding", 25),
    "coding_50": ("counter", "total_coding", 50),
    "coding_100": ("counter", "total_coding", 100),
    "first_accepted": ("score", "coding", 80),
    "question_10": ("counter", "total_question_banks", 10),
    "question_50": ("counter", "total_question_banks", 50),
    "question_100": ("counter", "total_question_banks", 100),
    "daily_3": ("counter", "total_daily_challenges", 3),
    "daily_10": ("counter", "total_daily_challenges", 10),
    "daily_30": ("counter", "total_daily_challenges", 30),
    "tower_floor_1": ("level", 10),
    "tower_floor_5": ("level", 50),
    "tower_floor_10": ("level", 100),
    "boss_1": ("bosses", 1),
    "boss_5": ("bosses", 5),
    "boss_10": ("bosses", 10),
    "powerup_10": ("counter", "total_powerups_used", 10),
    "powerup_50": ("counter", "total_powerups_used", 50),
    "streak_3": ("streak", 3),
    "streak_7": ("streak", 7),
    "streak_30": ("streak", 30),
    "streak_5": ("streak", 5),
    "streak_14": ("streak", 14),
    "streak_60": ("streak", 60),
    "streak_100": ("streak", 100),
    "perfect_3": ("counter", "total_perfect_scores", 3),
    "perfect_10": ("counter", "total_perfect_scores", 10),
    "company_5": ("counter", "total_company_tracks", 5),
    "company_20": ("counter", "total_company_tracks", 20),
    "company_53": ("counter", "total_company_tracks", 53),
    "lesson_5": ("counter", "total_lessons", 5),
    "lesson_20": ("counter", "total_lessons", 20),
    "language_3": ("counter", "total_learning_paths", 3),
    "lucky_streak": None,  # awarded by the daily-bonus path, not the evaluator
    "first_exam_memory": ("counter", "total_exam_memorys", 1),
    "exam_memory_5": ("counter", "total_exam_memorys", 5),
    "exam_memory_10": ("counter", "total_exam_memorys", 10),
    "first_system_design": ("counter", "total_system_design", 1),
    "system_design_master": ("score", "system_design", 9),
}


def badge_condition_met(
    condition,
    profile: dict,
    activity_type: str,
    score,
    streak: int,
) -> bool:
    """Pure evaluator for one badge condition tuple.

    condition is the value shape from BADGE_CONDITIONS:
      ("counter", field, min)         -> profile[field] >= min
      ("score", activity, min)        -> current activity matches AND score >= min
      ("streak", min)                 -> streak >= min
      ("level", min)                  -> profile level >= min
      ("bosses", min)                 -> len(bosses_defeated) >= min
      None                            -> never (externally awarded)
    """
    if condition is None:
        return False
    kind = condition[0]
    if kind == "counter":
        field = condition[1]
        if field not in GAMIFICATION_COUNTER_FIELDS:
            return False
        return float(profile.get(field, 0) or 0) >= float(condition[2])
    if kind == "score":
        if activity_type != condition[1]:
            return False
        try:
            return float(score or 0) >= float(condition[2])
        except (TypeError, ValueError):
            return False
    if kind == "streak":
        return int(streak or 0) >= int(condition[1])
    if kind == "level":
        return int(profile.get("level", 1) or 1) >= int(condition[1])
    if kind == "bosses":
        return len(profile.get("bosses_defeated") or []) >= int(condition[1])
    return False

# ─── Level / Diamonds math ───

def _calculate_xp(activity_type: str, score: float, role: str = "sde") -> int:
    """Calculate Diamonds gained from an activity — Candy Crush style."""
    base_xp = {
        "interview": 50,
        "resume": 25,
        "aptitude": 25,
        "coding": 40,
        "system_design": 50,
        "question_bank": 35,
        "daily_challenge": 60,
        "tower": 75,
        "boss_battle": 100,
        "practice": 20,
        "lesson": 15,
        "behavioral": 30,
        "exam_memory": 20,
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

    # Role multiplier
    role_mult = get_role_xp_multiplier(role, activity_type)
    base_xp = int(base_xp * role_mult)

    return base_xp


def _calculate_level(diamonds: int) -> int:
    """Calculate level from exponential curve: Diamonds_needed(level) = 100 * level."""
    if diamonds <= 0:
        return 1
    return max(1, min(100, int(math.sqrt(diamonds / 50)) + 1))


def xp_for_level(level: int) -> int:
    """Total Diamonds needed to reach a level."""
    return ((level - 1) ** 2) * 50


def xp_for_next_level(level: int) -> int:
    """Diamonds needed to go from current level to next."""
    return (level ** 2) * 50


def get_title_for_level(level: int) -> tuple:
    """Get title and emoji for a level."""
    title = "Hatchling"
    emoji = "🐣"
    for threshold, (t, e) in sorted(TOWER_TITLES.items()):
        if level >= threshold:
            title, emoji = t, e
    return title, emoji


# ─── Voyage ranks: the canonical status ladder ───
# Derived from the same `level` field as tower titles — no new currency,
# no stored state. Six tiers so rank-tier jumps stay rare enough for
# big-ceremony moments (proposal: ceremonies fire on tier change only).
# Bands align with boss levels (10/20/…/100) so tiers feel earned.
VOYAGE_RANKS = [
    {"tier": 0, "min_level": 1,  "rank": "Deckhand",     "emoji": "⚓"},
    {"tier": 1, "min_level": 10, "rank": "Lookout",      "emoji": "🔭"},
    {"tier": 2, "min_level": 25, "rank": "Navigator",    "emoji": "🧭"},
    {"tier": 3, "min_level": 45, "rank": "First Mate",   "emoji": "🗺️"},
    {"tier": 4, "min_level": 65, "rank": "Captain",      "emoji": "🏴‍☠️"},
    {"tier": 5, "min_level": 85, "rank": "Fleet Admiral","emoji": "👑"},
]


def voyage_rank_for_level(level: int) -> tuple:
    """Return (rank, emoji, tier_index) for a level. Pure; clamp to 1-100."""
    lvl = max(1, min(100, int(level or 1)))
    cur = VOYAGE_RANKS[0]
    for r in VOYAGE_RANKS:
        if lvl >= r["min_level"]:
            cur = r
    return cur["rank"], cur["emoji"], cur["tier"]


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


def compute_forest_state(level: int, diamonds: int, streak: int, badges: list, bosses_defeated: list) -> dict:
    """Derive the nature-themed gamification state from existing tower data.

    Purely additive/derived — nothing here mutates stored data:
      - Diamonds        -> sunlight
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
        "sunlight": diamonds,
        "waterings": streak or 0,
        "seeds": len(badges or []),
        "storms_cleared": len(defeated),
        "current_storm": current_storm,
        "zone_progress": round(zone_progress, 4),
    }


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
    diamonds = int(base_xp * mult) + bonus
    if is_first_today:
        diamonds *= 2  # Double Diamonds first solve
    return diamonds


LEVEL_COLORS = {
    1:  {"from": "#9CA3AF", "to": "#6B7280", "label": "Common", "color": "#9CA3AF"},
    10: {"from": "#22C55E", "to": "#16A34A", "label": "Uncommon", "color": "#22C55E"},
    30: {"from": "#3B82F6", "to": "#2563EB", "label": "Rare", "color": "#3B82F6"},
    50: {"from": "#A855F7", "to": "#6366F1", "label": "Epic", "color": "#A855F7"},
    70: {"from": "#EAB308", "to": "#F59E0B", "label": "Legendary", "color": "#EAB308"},
    90: {"from": "#EC4899", "to": "#A855F7", "label": "Mythic", "color": "#EC4899"},
}


def get_level_color(level: int) -> dict:
    """Return color metadata for a level."""
    level = max(1, min(100, level))
    color = LEVEL_COLORS[1]
    for threshold, c in sorted(LEVEL_COLORS.items()):
        if level >= threshold:
            color = c
    return color
