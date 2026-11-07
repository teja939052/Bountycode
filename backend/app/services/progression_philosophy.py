"""Bountycode progression philosophy — the law above XP.

This module is the single written contract for how motivation works in
Bountycode. Other gamification modules must not contradict it.

## What we optimize for

1. **Placement readiness** — measurable skill evidence toward service-company
   and product-company hiring bars (aptitude, coding, reasoning, interviews).
2. **Habit without punishment** — streaks reward showing up; freezes and soft
   resets exist so one missed day does not erase a month of work.
3. **Truthful status** — ranks and badges only unlock from server-graded mastery,
   diagnostics, mocks and assessments — never from time-on-page or UI clicks.

## What we refuse

- Power-ups that reveal answers, skip bosses, or buy mastery.
- Random "critical hit" rewards disconnected from skill.
- Leaderboards that rank pure XP farming over competence.
- Fantasy prestige ("God of Code") that does not map to an interview stage.

## Currency roles (kept intentionally few)

- **Proof** — non-spendable mastery signal (lessons, assessments, mocks).
- **Bounty** — cosmetic / comfort only (themes, optional polish). Never unlocks
  learning content or readiness score.
- **Diamonds / XP** — legacy display continuum toward rank bands; must not outrank
  readiness on the Dashboard primary surface.

## Rank model

Ranks describe the learner's *placement stage*, optionally company-aware:

  Beginner → Builder → Practitioner → Contender → Offer-Ready → Alumnus

Company tracks (TCS, Infosys, Wipro, Accenture, …) override display titles so a
learner preparing for NQT sees NQT-stage language, not generic RPG names.

## Badge law

Badges mark irreversible real events:
- first diagnostic completed
- first lesson mastered (server-graded)
- 7 focused study days
- company mock completed above threshold
- skill raised from weak to proficient

Volume badges ("50 of X") are secondary and never required for rank.

## Dashboard law

Primary: today's plan + readiness + weak skills.
Secondary: streak, rank title, proof earned today.
Tertiary: cosmetics and optional challenges.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

# ---------------------------------------------------------------------------
# Placement ranks (default, company-agnostic)
# Level bands remain compatible with existing level math; labels change.
# ---------------------------------------------------------------------------
PLACEMENT_RANKS: List[Tuple[int, str, str, str]] = [
    # min_level, id, title, short_description
    (1, "beginner", "Beginner", "Building foundations"),
    (5, "starter", "Starter", "First skills under assessment"),
    (10, "builder", "Builder", "Core aptitude and coding habits"),
    (15, "practitioner", "Practitioner", "Consistent evidence across topics"),
    (25, "contender", "Contender", "Mock-ready for target companies"),
    (35, "finalist", "Finalist", "Strong mock and interview signals"),
    (45, "offer_ready", "Offer-Ready", "Readiness matches hiring bar"),
    (60, "mentor", "Mentor-Track", "Depth beyond the entry bar"),
    (80, "alumnus", "Placement Alumnus", "Sustained mastery record"),
    (100, "legend", "Campus Legend", "Top-tier evidence across domains"),
]


def rank_for_level(level: int) -> Dict[str, Any]:
    """Return the highest placement rank at or below level."""
    level = max(1, int(level or 1))
    chosen = PLACEMENT_RANKS[0]
    for row in PLACEMENT_RANKS:
        if row[0] <= level:
            chosen = row
        else:
            break
    return {
        "min_level": chosen[0],
        "id": chosen[1],
        "title": chosen[2],
        "description": chosen[3],
        "level": level,
    }


# ---------------------------------------------------------------------------
# Power-ups: only learning-support tools. Cheats are disabled.
# ---------------------------------------------------------------------------
ALLOWED_POWER_UPS = {
    "extra_time": {
        "name": "Extra Time",
        "emoji": "⏰",
        "description": "+5 minutes on a timed mock (does not change scoring rules)",
        "enabled": True,
        "cost": 10,
    },
    "retry": {
        "name": "Retry",
        "emoji": "🔄",
        "description": "One extra attempt after feedback — still graded honestly",
        "enabled": True,
        "cost": 25,
    },
    "focus_mode": {
        "name": "Focus Mode",
        "emoji": "🎯",
        "description": "Hide non-essential UI during a study block",
        "enabled": True,
        "cost": 5,
    },
    "auto_save": {
        "name": "Auto-Save",
        "emoji": "💾",
        "description": "Auto-save code while practising",
        "enabled": True,
        "cost": 12,
    },
    "night_mode": {
        "name": "Night Mode",
        "emoji": "🌙",
        "description": "Comfort theme — pure cosmetics",
        "enabled": True,
        "cost": 5,
    },
}

# Explicitly forbidden — must never grant mastery or reveal answers.
DISABLED_POWER_UPS = {
    "show_answer",
    "skip_boss",
    "hint_reveal",  # free hints belong in the lesson design, not a shop
    "shield",       # must not erase wrong-answer evidence
}


def is_power_up_allowed(power_up_id: str) -> bool:
    if power_up_id in DISABLED_POWER_UPS:
        return False
    cfg = ALLOWED_POWER_UPS.get(power_up_id)
    return bool(cfg and cfg.get("enabled"))


# ---------------------------------------------------------------------------
# Mastery badges (primary). Volume badges remain elsewhere as secondary.
# ---------------------------------------------------------------------------
MASTERY_BADGES: Dict[str, Dict[str, str]] = {
    "first_diagnostic": {
        "name": "Mapped",
        "description": "Completed the placement diagnostic",
        "icon": "🧭",
        "category": "mastery",
    },
    "first_lesson_mastered": {
        "name": "First Mastery",
        "description": "Passed a server-graded lesson assessment",
        "icon": "✅",
        "category": "mastery",
    },
    "skill_recovered": {
        "name": "Gap Closed",
        "description": "Raised a weak skill above the proficient bar",
        "icon": "📈",
        "category": "mastery",
    },
    "plan_streak_7": {
        "name": "Seven Focused Days",
        "description": "Completed the daily learning plan 7 days in a row",
        "icon": "📅",
        "category": "habit",
    },
    "company_mock_pass": {
        "name": "Mock Cleared",
        "description": "Scored at or above the pass bar on a company-style mock",
        "icon": "🏢",
        "category": "company",
    },
    "aptitude_core": {
        "name": "Aptitude Core",
        "description": "Mastered the core quant lessons used in NQT-style papers",
        "icon": "🧮",
        "category": "aptitude",
    },
    "reasoning_core": {
        "name": "Reasoning Core",
        "description": "Mastered coding-decoding, series, relations and syllogisms",
        "icon": "🧩",
        "category": "reasoning",
    },
    "coding_fundamentals": {
        "name": "Coding Fundamentals",
        "description": "Mastered variables through loops and string basics",
        "icon": "💻",
        "category": "coding",
    },
    "readiness_50": {
        "name": "Halfway Ready",
        "description": "Reached 50% evidence-based placement readiness",
        "icon": "⭐",
        "category": "readiness",
    },
    "readiness_80": {
        "name": "Interview Window",
        "description": "Reached 80% evidence-based placement readiness",
        "icon": "🎯",
        "category": "readiness",
    },
}


# Streak policy: protect habit, do not shame.
STREAK_POLICY = {
    "freeze_on_missed_day": True,
    "default_freezes": 2,
    "message_on_freeze": "Streak protected — one freeze used. Come back tomorrow.",
    "message_on_reset": "New streak started. Consistency beats perfection.",
    "never_gate_content": True,  # streaks never lock lessons
}


def dashboard_priority() -> List[str]:
    """Ordered surfaces the Dashboard must respect."""
    return [
        "today_plan",
        "readiness",
        "weak_skills",
        "company_mock",
        "streak_and_rank",
        "cosmetics",
    ]
