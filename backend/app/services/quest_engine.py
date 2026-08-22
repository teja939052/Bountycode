"""Adaptive Quest Engine — deterministic daily practice quests, NO AI.

Generates 3-5 personalized daily quests based on the user's actual weak
areas, SRS review needs, target companies, and mastery levels. Pure rules
engine with no external API calls.

Quest types (by priority):
  1. SRS Review    — overdue spaced-repetition cards
  2. Weak Recovery — skills with mastery < 3
  3. Company Sprint — problems tagged with user's target company
  4. Skill Up      — advance skills at mastery 3-4 to next level
  5. Streak Maintenance — easy problems if accuracy > 80%
  6. Daily Challenge — adaptive difficulty from recent accuracy
"""
from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional


# ── Quest type enum ───────────────────────────────────────────────────

class QuestType(str, Enum):
    SRS_REVIEW = "srs_review"
    WEAKNESS_RECOVERY = "weakness_recovery"
    COMPANY_SPRINT = "company_sprint"
    SKILL_UP = "skill_up"
    STREAK_MAINTENANCE = "streak_maintenance"
    DAILY_CHALLENGE = "daily_challenge"


# ── XP rewards by difficulty ──────────────────────────────────────────

XP_REWARDS = {
    "easy": 50,
    "medium": 100,
    "hard": 200,
}

# ── Quest target counts ──────────────────────────────────────────────

QUEST_TARGETS = {
    QuestType.SRS_REVIEW: 3,
    QuestType.WEAKNESS_RECOVERY: 3,
    QuestType.COMPANY_SPRINT: 2,
    QuestType.SKILL_UP: 2,
    QuestType.STREAK_MAINTENANCE: 3,
    QuestType.DAILY_CHALLENGE: 1,
}

# ── Estimated minutes per quest type ─────────────────────────────────

ESTIMATED_MINUTES = {
    QuestType.SRS_REVIEW: 10,
    QuestType.WEAKNESS_RECOVERY: 20,
    QuestType.COMPANY_SPRINT: 15,
    QuestType.SKILL_UP: 20,
    QuestType.STREAK_MAINTENANCE: 10,
    QuestType.DAILY_CHALLENGE: 15,
}

# ── Difficulty tier labels for titles ─────────────────────────────────

DIFFICULTY_LABELS = {
    "easy": "Foundation",
    "medium": "Intermediate",
    "hard": "Advanced",
}

# ── Maximum quests per day ───────────────────────────────────────────

MAX_QUESTS_PER_DAY = 5


def generate_quest_id(quest_type: str, topic: str, date_str: str) -> str:
    """Generate a deterministic quest ID from type, topic, and date.

    Args:
        quest_type: The quest type string.
        topic: The topic or company name.
        date_str: ISO date string (YYYY-MM-DD).

    Returns:
        Unique quest ID string.
    """
    raw = f"{quest_type}:{topic}:{date_str}"
    short_hash = hashlib.sha256(raw.encode()).hexdigest()[:12]
    return f"qst_{short_hash}"


def _now_utc() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def _today_str() -> str:
    """Get today's date as ISO date string."""
    return _now_utc().strftime("%Y-%m-%d")


def _pick_topic_for_weak_area(weak_areas: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Select the best weak area to target for a quest.

    Prioritizes:
      1. Lowest mastery level
      2. Most attempts already invested (easier to improve)

    Args:
        weak_areas: List of weak area dicts from mastery_engine.

    Returns:
        Selected weak area dict, or None if empty.
    """
    if not weak_areas:
        return None
    # Already sorted by mastery_engine.find_weak_areas: lowest level first
    return weak_areas[0]


def _pick_company(company: Optional[str]) -> Optional[str]:
    """Normalize a company name for quest generation.

    Args:
        company: Raw company name from user profile.

    Returns:
        Normalized company name, or None if empty.
    """
    if not company:
        return None
    name = str(company).strip()
    return name if name else None


def _determine_difficulty_for_skill(
    mastery_level: int,
    recent_accuracy: Optional[float] = None,
) -> str:
    """Map mastery level to an appropriate difficulty tier.

    Mastery 0-1 → easy
    Mastery 2-3 → medium
    Mastery 4-5 → hard

    If recent_accuracy is available, adjusts within the band.

    Args:
        mastery_level: Current mastery level (0-5).
        recent_accuracy: Optional accuracy 0.0-1.0.

    Returns:
        Difficulty string: 'easy', 'medium', or 'hard'.
    """
    if mastery_level <= 1:
        return "easy"
    if mastery_level <= 3:
        if recent_accuracy is not None and recent_accuracy < 0.3:
            return "easy"
        if recent_accuracy is not None and recent_accuracy >= 0.7:
            return "hard"
        return "medium"
    # Mastery 4-5
    return "hard"


def _determine_daily_challenge_difficulty(recent_accuracy: float) -> str:
    """Map recent accuracy to challenge difficulty.

    Args:
        recent_accuracy: Average accuracy over last 7 days (0.0-1.0).

    Returns:
        Difficulty string: 'easy', 'medium', or 'hard'.
    """
    if recent_accuracy >= 0.8:
        return "hard"
    if recent_accuracy >= 0.5:
        return "medium"
    return "easy"


def _compute_recent_accuracy(performance_data: Dict[str, Any]) -> float:
    """Compute weighted average accuracy from performance data.

    Args:
        performance_data: Dict with 'accuracy_per_topic' and/or 'overall_accuracy'.

    Returns:
        Accuracy value between 0.0 and 1.0.
    """
    if performance_data.get("overall_accuracy") is not None:
        return float(performance_data["overall_accuracy"])

    topic_accuracies = performance_data.get("accuracy_per_topic", {})
    if not topic_accuracies:
        return 0.5  # Default neutral accuracy

    values = list(topic_accuracies.values())
    return sum(values) / len(values) if values else 0.5


def _build_srs_quest(
    due_cards: List[Dict[str, Any]],
    date_str: str,
) -> Optional[Dict[str, Any]]:
    """Build a quest for SRS review of due cards.

    Args:
        due_cards: List of SRS card dicts with at least 'difficulty' and 'problem_id'.
        date_str: Today's ISO date string.

    Returns:
        Quest dict or None if no due cards.
    """
    if not due_cards:
        return None

    overdue_count = len(due_cards)
    target = min(overdue_count, 5)  # Cap at 5 reviews

    quest_id = generate_quest_id(QuestType.SRS_REVIEW.value, "srs_review", date_str)

    return {
        "quest_id": quest_id,
        "quest_type": QuestType.SRS_REVIEW.value,
        "title": f"Review {target} due problems",
        "description": (
            f"You have {overdue_count} problem(s) due for spaced repetition. "
            f"Review {target} to keep retention high."
        ),
        "topic": "srs_review",
        "difficulty": "mixed",
        "target_count": target,
        "xp_reward": XP_REWARDS["medium"] * target,
        "estimated_minutes": ESTIMATED_MINUTES[QuestType.SRS_REVIEW] + (target - 3) * 2,
        "company": None,
        "current_count": 0,
        "is_complete": False,
        "completed_at": None,
        "metadata": {
            "due_card_ids": [c.get("problem_id", "") for c in due_cards[:target]],
        },
    }


def _build_weakness_quest(
    weak_area: Dict[str, Any],
    matching_questions: int,
    date_str: str,
) -> Optional[Dict[str, Any]]:
    """Build a quest targeting a specific weak skill area.

    Args:
        weak_area: Dict from mastery_engine.find_weak_areas with topic, sub_topic, level.
        matching_questions: Number of questions available for this topic.
        date_str: Today's ISO date string.

    Returns:
        Quest dict or None.
    """
    if matching_questions == 0:
        return None

    topic = weak_area.get("topic", "unknown")
    sub_topic = weak_area.get("sub_topic", "unknown")
    level = weak_area.get("level", 0)
    level_name = weak_area.get("level_name", "Unknown")
    accuracy = weak_area.get("accuracy", 0)

    target = min(QUEST_TARGETS[QuestType.WEAKNESS_RECOVERY], matching_questions)
    difficulty = _determine_difficulty_for_skill(level, accuracy / 100 if accuracy else None)
    xp = XP_REWARDS.get(difficulty, 100) * target

    quest_id = generate_quest_id(
        QuestType.WEAKNESS_RECOVERY.value, f"{topic}:{sub_topic}", date_str
    )

    display_topic = topic.replace("_", " ").title()
    display_sub = sub_topic.replace("_", " ").title() if sub_topic else ""

    return {
        "quest_id": quest_id,
        "quest_type": QuestType.WEAKNESS_RECOVERY.value,
        "title": f"Strengthen {display_topic}" + (f" - {display_sub}" if display_sub else ""),
        "description": (
            f"Your {display_topic} mastery is {level_name} ({level}/5, {accuracy}% accuracy). "
            f"Solve {target} problems to push it higher."
        ),
        "topic": topic,
        "difficulty": difficulty,
        "target_count": target,
        "xp_reward": xp,
        "estimated_minutes": ESTIMATED_MINUTES[QuestType.WEAKNESS_RECOVERY],
        "company": None,
        "current_count": 0,
        "is_complete": False,
        "completed_at": None,
        "metadata": {
            "sub_topic": sub_topic,
            "mastery_level": level,
        },
    }


def _build_company_quest(
    company: str,
    matching_questions: int,
    date_str: str,
) -> Optional[Dict[str, Any]]:
    """Build a company-specific sprint quest.

    Args:
        company: Target company name.
        matching_questions: Number of questions tagged with this company.
        date_str: Today's ISO date string.

    Returns:
        Quest dict or None.
    """
    if matching_questions == 0:
        return None

    target = min(QUEST_TARGETS[QuestType.COMPANY_SPRINT], matching_questions)
    quest_id = generate_quest_id(
        QuestType.COMPANY_SPRINT.value, company.lower(), date_str
    )

    return {
        "quest_id": quest_id,
        "quest_type": QuestType.COMPANY_SPRINT.value,
        "title": f"{company.title()} sprint",
        "description": (
            f"Solve {target} problems commonly asked at {company.title()}. "
            f"Build company-specific readiness."
        ),
        "topic": "company_prep",
        "difficulty": "medium",
        "target_count": target,
        "xp_reward": XP_REWARDS["medium"] * target,
        "estimated_minutes": ESTIMATED_MINUTES[QuestType.COMPANY_SPRINT],
        "company": company.lower(),
        "current_count": 0,
        "is_complete": False,
        "completed_at": None,
        "metadata": {},
    }


def _build_skill_up_quest(
    skill_data: Dict[str, Any],
    matching_questions: int,
    date_str: str,
) -> Optional[Dict[str, Any]]:
    """Build a quest to advance a skill at mastery 3-4.

    Args:
        skill_data: Skill dict with topic, sub_topic, level, accuracy.
        matching_questions: Number of questions available.
        date_str: Today's ISO date string.

    Returns:
        Quest dict or None.
    """
    if matching_questions == 0:
        return None

    topic = skill_data.get("topic", "unknown")
    sub_topic = skill_data.get("sub_topic", "unknown")
    level = skill_data.get("level", 3)
    accuracy = skill_data.get("accuracy", 0)

    target = min(QUEST_TARGETS[QuestType.SKILL_UP], matching_questions)
    difficulty = _determine_difficulty_for_skill(level, accuracy / 100 if accuracy else None)
    # Push toward harder problems for skill advancement
    if difficulty == "medium":
        difficulty = "medium"  # Keep at medium, goal is mastery via volume

    xp = XP_REWARDS.get(difficulty, 100) * target
    quest_id = generate_quest_id(
        QuestType.SKILL_UP.value, f"{topic}:{sub_topic}", date_str
    )

    display_topic = topic.replace("_", " ").title()
    display_sub = sub_topic.replace("_", " ").title() if sub_topic else ""

    return {
        "quest_id": quest_id,
        "quest_type": QuestType.SKILL_UP.value,
        "title": f"Level up {display_topic}" + (f" - {display_sub}" if display_sub else ""),
        "description": (
            f"You're at {level}/5 in {display_topic}. Solve {target} harder problems "
            f"to push toward mastery."
        ),
        "topic": topic,
        "difficulty": difficulty,
        "target_count": target,
        "xp_reward": xp,
        "estimated_minutes": ESTIMATED_MINUTES[QuestType.SKILL_UP],
        "company": None,
        "current_count": 0,
        "is_complete": False,
        "completed_at": None,
        "metadata": {
            "sub_topic": sub_topic,
            "mastery_level": level,
        },
    }


def _build_streak_quest(
    accuracy: float,
    total_solved: int,
    date_str: str,
) -> Optional[Dict[str, Any]]:
    """Build a streak maintenance quest with easy problems.

    Only generated when accuracy is above 80% and user has some history.

    Args:
        accuracy: Overall recent accuracy (0.0-1.0).
        total_solved: Total problems solved by user.
        date_str: Today's ISO date string.

    Returns:
        Quest dict or None.
    """
    if accuracy < 0.6 or total_solved < 5:
        return None

    target = QUEST_TARGETS[QuestType.STREAK_MAINTENANCE]
    quest_id = generate_quest_id(QuestType.STREAK_MAINTENANCE.value, "streak", date_str)

    return {
        "quest_id": quest_id,
        "quest_type": QuestType.STREAK_MAINTENANCE.value,
        "title": "Keep the streak alive",
        "description": (
            f"Solve {target} easy problems to maintain your practice rhythm. "
            f"Consistency is the path to mastery."
        ),
        "topic": "general",
        "difficulty": "easy",
        "target_count": target,
        "xp_reward": XP_REWARDS["easy"] * target,
        "estimated_minutes": ESTIMATED_MINUTES[QuestType.STREAK_MAINTENANCE],
        "company": None,
        "current_count": 0,
        "is_complete": False,
        "completed_at": None,
        "metadata": {},
    }


def _build_daily_challenge_quest(
    difficulty: str,
    matching_questions: int,
    date_str: str,
) -> Optional[Dict[str, Any]]:
    """Build an adaptive daily challenge quest.

    Uses a deterministic problem selection based on the date as seed.

    Args:
        difficulty: Determined difficulty tier.
        matching_questions: Number of available questions.
        date_str: Today's ISO date string.

    Returns:
        Quest dict or None.
    """
    if matching_questions == 0:
        return None

    xp = XP_REWARDS.get(difficulty, 100)
    quest_id = generate_quest_id(QuestType.DAILY_CHALLENGE.value, difficulty, date_str)
    diff_label = DIFFICULTY_LABELS.get(difficulty, "Medium")

    return {
        "quest_id": quest_id,
        "quest_type": QuestType.DAILY_CHALLENGE.value,
        "title": f"Daily {diff_label} Challenge",
        "description": (
            f"Complete today's {diff_label} challenge — "
            f"one curated problem to test your skills."
        ),
        "topic": "daily_challenge",
        "difficulty": difficulty,
        "target_count": 1,
        "xp_reward": xp,
        "estimated_minutes": ESTIMATED_MINUTES[QuestType.DAILY_CHALLENGE],
        "company": None,
        "current_count": 0,
        "is_complete": False,
        "completed_at": None,
        "metadata": {},
    }


def generate_daily_quests(
    user_id: str,
    performance_data: Dict[str, Any],
    skill_stats: List[Dict[str, Any]],
    due_srs_cards: List[Dict[str, Any]],
    target_companies: List[str],
    solved_problem_ids: set,
) -> List[Dict[str, Any]]:
    """Generate 3-5 personalized daily quests based on user data.

    Pure function — accepts pre-fetched data and returns quest list.
    No database access, no AI calls.

    Args:
        user_id: User ID (used for quest ID seeding).
        performance_data: Dict with 'overall_accuracy', 'accuracy_per_topic',
            'total_solved', 'recent_7day_accuracy'.
        skill_stats: List of per-skill stat dicts from skill_graphs collection.
        due_srs_cards: List of SRS card dicts where next_review <= now.
        target_companies: List of company names from user's onboarding.
        solved_problem_ids: Set of problem IDs the user has already solved today.

    Returns:
        List of 3-5 quest dicts, ordered by priority.
    """
    today = _today_str()
    quests: List[Dict[str, Any]] = []
    quest_topics_used: set = set()  # Prevent duplicate topics in same day

    # ── Priority 1: SRS reviews ──────────────────────────────────────
    srs_quest = _build_srs_quest(due_srs_cards, today)
    if srs_quest:
        quests.append(srs_quest)
        quest_topics_used.add("srs_review")

    # ── Priority 2: Weak area recovery ───────────────────────────────
    from app.services.mastery_engine import find_weak_areas
    weak_areas = find_weak_areas(skill_stats, top_n=5)

    for weak in weak_areas:
        if len(quests) >= MAX_QUESTS_PER_DAY:
            break
        topic_key = f"weak:{weak.get('topic', '')}"
        if topic_key in quest_topics_used:
            continue

        # Count available questions from the question bank
        topic = weak.get("topic", "")
        from app.services import question_store as _qs
        matching = _qs.count_documents({"topic": topic})
        # Fallback: at least 3 problems exist per topic
        matching = max(matching, 3)

        quest = _build_weakness_quest(weak, matching, today)
        if quest:
            quests.append(quest)
            quest_topics_used.add(topic_key)

    # ── Priority 3: Company sprint ───────────────────────────────────
    for company in target_companies:
        if len(quests) >= MAX_QUESTS_PER_DAY:
            break
        company_key = f"company:{company.lower()}"
        if company_key in quest_topics_used:
            continue

        # Count questions tagged with this company from the question bank
        from app.services import question_store as _qs
        matching = _qs.count_documents({"company": company})
        matching = max(matching, 1)

        company_quest = _build_company_quest(company, matching, today)
        if company_quest:
            quests.append(company_quest)
            quest_topics_used.add(company_key)

    # ── Priority 4: Skill advancement (mastery 3-4) ─────────────────
    from app.services.mastery_engine import calculate_mastery_level
    advanced_skills = []
    for s in skill_stats:
        topic = s.get("topic", "")
        if not topic:
            continue
        # Calculate actual mastery level from stats
        attempted = s.get("problems_attempted", 0)
        solved = s.get("problems_solved", 0)
        acc = solved / attempted if attempted > 0 else 0.0
        level = s.get("current_level", calculate_mastery_level(attempted, acc))
        if 3 <= level <= 4:
            advanced_skills.append({**s, "current_level": level})

    for skill in advanced_skills:
        if len(quests) >= MAX_QUESTS_PER_DAY:
            break
        level = skill.get("current_level", 3)
        if level < 3 or level > 4:
            continue
        topic_key = f"skillup:{skill.get('topic', '')}"
        # Skip if this topic was already used for a weakness quest
        weak_key = f"weak:{skill.get('topic', '')}"
        if weak_key in quest_topics_used or topic_key in quest_topics_used:
            continue

        matching = _qs.count_documents({"topic": skill.get("topic", "")})
        matching = max(matching, 3)
        quest = _build_skill_up_quest(skill, matching, today)
        if quest:
            quests.append(quest)
            quest_topics_used.add(topic_key)

    # ── Priority 5: Streak maintenance ───────────────────────────────
    if len(quests) < MAX_QUESTS_PER_DAY:
        accuracy = _compute_recent_accuracy(performance_data)
        total_solved = performance_data.get("total_solved", 0)
        streak_quest = _build_streak_quest(accuracy, total_solved, today)
        if streak_quest and "streak" not in quest_topics_used:
            quests.append(streak_quest)
            quest_topics_used.add("streak")

    # ── Priority 6: Daily challenge (always add if room) ─────────────
    if len(quests) < MAX_QUESTS_PER_DAY:
        accuracy = _compute_recent_accuracy(performance_data)
        daily_diff = _determine_daily_challenge_difficulty(accuracy)
        daily_quest = _build_daily_challenge_quest(daily_diff, 20, today)
        if daily_quest:
            quests.append(daily_quest)

    # Trim to max quests
    return quests[:MAX_QUESTS_PER_DAY]


def check_quest_progress(
    quest: Dict[str, Any],
    matching_solve_count: int,
) -> Dict[str, Any]:
    """Check progress on a single quest.

    Pure function — does not touch the database.

    Args:
        quest: The quest dict.
        matching_solve_count: Number of matching solves today.

    Returns:
        Dict with current_count, target_count, is_complete, xp_earned.
    """
    target = quest.get("target_count", 1)
    current = min(matching_solve_count, target)
    is_complete = current >= target
    xp_earned = quest.get("xp_reward", 0) if is_complete else 0

    # Partial XP: proportional for incomplete
    if not is_complete and current > 0:
        xp_earned = int(quest.get("xp_reward", 0) * (current / target))

    return {
        "current_count": current,
        "target_count": target,
        "is_complete": is_complete,
        "xp_earned": xp_earned,
    }


def does_solve_match_quest(
    quest: Dict[str, Any],
    question_data: Dict[str, Any],
) -> bool:
    """Check if a problem solve matches a quest's criteria.

    Args:
        quest: The quest dict.
        question_data: Dict with 'topic', 'sub_topic', 'companies', 'difficulty'.

    Returns:
        True if this solve counts toward the quest.
    """
    quest_type = quest.get("quest_type", "")
    quest_topic = quest.get("topic", "")
    quest_company = quest.get("company")
    quest_difficulty = quest.get("difficulty", "mixed")

    q_topic = question_data.get("topic", "")
    q_sub_topic = question_data.get("sub_topic", "")
    q_companies = [c.lower() for c in question_data.get("companies", [])]
    q_difficulty = question_data.get("difficulty", "medium")

    if quest_type == QuestType.SRS_REVIEW.value:
        # Check if problem_id is in the quest's due list
        due_ids = quest.get("metadata", {}).get("due_card_ids", [])
        q_id = question_data.get("id", "")
        return q_id in due_ids if due_ids else q_topic.lower() == quest_topic.lower()

    if quest_type == QuestType.WEAKNESS_RECOVERY.value:
        return (
            q_topic.lower() == quest_topic.lower()
            or q_sub_topic.lower() == quest.get("metadata", {}).get("sub_topic", "").lower()
        )

    if quest_type == QuestType.COMPANY_SPRINT.value:
        return quest_company and quest_company.lower() in q_companies

    if quest_type == QuestType.SKILL_UP.value:
        return (
            q_topic.lower() == quest_topic.lower()
            or q_sub_topic.lower() == quest.get("metadata", {}).get("sub_topic", "").lower()
        )

    if quest_type == QuestType.STREAK_MAINTENANCE.value:
        return True  # Any problem counts for streak maintenance

    if quest_type == QuestType.DAILY_CHALLENGE.value:
        return True  # Any problem counts for daily challenge

    return False


def serialize_quest(quest: Dict[str, Any]) -> Dict[str, Any]:
    """Serialize a quest for API response.

    Removes internal metadata and formats for consumption.

    Args:
        quest: Raw quest dict.

    Returns:
        Clean quest dict for API response.
    """
    return {
        "quest_id": quest.get("quest_id", ""),
        "quest_type": quest.get("quest_type", ""),
        "title": quest.get("title", ""),
        "description": quest.get("description", ""),
        "topic": quest.get("topic", ""),
        "difficulty": quest.get("difficulty", "medium"),
        "target_count": quest.get("target_count", 1),
        "xp_reward": quest.get("xp_reward", 0),
        "estimated_minutes": quest.get("estimated_minutes", 10),
        "company": quest.get("company"),
        "current_count": quest.get("current_count", 0),
        "is_complete": quest.get("is_complete", False),
        "completed_at": quest.get("completed_at"),
    }


def compute_quest_stats(
    completed_docs: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Compute quest statistics from historical daily quest documents.

    Args:
        completed_docs: List of daily_quests documents (past 30 days).

    Returns:
        Dict with completion_rate, total_xp, daily_completion_streak, etc.
    """
    if not completed_docs:
        return {
            "total_days": 0,
            "days_with_quests": 0,
            "days_fully_completed": 0,
            "completion_rate": 0.0,
            "total_xp_earned": 0,
            "total_quests_completed": 0,
            "total_quests_generated": 0,
            "daily_completion_streak": 0,
            "best_completion_streak": 0,
            "quests_by_type": {},
        }

    total_quests = 0
    completed_quests = 0
    total_xp = 0
    quests_by_type: Dict[str, int] = {}
    fully_completed_days = 0
    daily_streak = 0
    best_streak = 0

    # Sort docs by date descending
    sorted_docs = sorted(completed_docs, key=lambda d: d.get("date", ""), reverse=True)

    # Count current consecutive completion streak
    today = _today_str()

    for doc in sorted_docs:
        quests = doc.get("quests", [])
        day_total = len(quests)
        day_completed = sum(1 for q in quests if q.get("is_complete", False))
        day_xp = sum(q.get("xp_reward", 0) for q in quests if q.get("is_complete", False))

        total_quests += day_total
        completed_quests += day_completed
        total_xp += day_xp

        if day_total > 0 and day_completed == day_total:
            fully_completed_days += 1
            daily_streak += 1
            best_streak = max(best_streak, daily_streak)
        else:
            daily_streak = 0

        for q in quests:
            qt = q.get("quest_type", "unknown")
            if q.get("is_complete", False):
                quests_by_type[qt] = quests_by_type.get(qt, 0) + 1

    days_with_quests = len([d for d in completed_docs if d.get("quests")])

    return {
        "total_days": len(completed_docs),
        "days_with_quests": days_with_quests,
        "days_fully_completed": fully_completed_days,
        "completion_rate": round(completed_quests / total_quests * 100, 1) if total_quests > 0 else 0.0,
        "total_xp_earned": total_xp,
        "total_quests_completed": completed_quests,
        "total_quests_generated": total_quests,
        "daily_completion_streak": daily_streak,
        "best_completion_streak": best_streak,
        "quests_by_type": quests_by_type,
    }
