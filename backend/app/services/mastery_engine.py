"""Skill Mastery Engine — deterministic mastery tracking per topic/sub_topic.

Tracks mastery on a 0-5 scale based on solved_problems history:
  0 = Unknown     — never attempted
  1 = Introduced  — attempted 1-2 problems
  2 = Practicing  — 3-5 problems, <50% accuracy
  3 = Competent   — 6-10 problems, 50-75% accuracy
  4 = Strong      — 11-20 problems, 75-90% accuracy
  5 = Mastered    — 20+ problems, >90% accuracy

All functions are pure and testable without a database — they accept
pre-fetched data dicts and return structured results.
"""
from app.services.role_engine.profiles import get_profile, SkillDef, SkillImportance

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# Mastery level thresholds
MASTERY_LEVELS = {
    0: {"name": "Unknown", "min_problems": 0, "max_problems": 0, "min_accuracy": 0.0},
    1: {"name": "Introduced", "min_problems": 1, "max_problems": 2, "min_accuracy": 0.0},
    2: {"name": "Practicing", "min_problems": 3, "max_problems": 5, "min_accuracy": 0.0},
    3: {"name": "Competent", "min_problems": 6, "max_problems": 10, "min_accuracy": 0.50},
    4: {"name": "Strong", "min_problems": 11, "max_problems": 20, "min_accuracy": 0.75},
    5: {"name": "Mastered", "min_problems": 21, "max_problems": 9999, "min_accuracy": 0.90},
}


@dataclass
class SkillMastery:
    """Mastery state for a single skill/topic."""
    topic: str
    sub_topic: str
    level: int  # 0-5
    name: str  # Human-readable level name
    problems_attempted: int
    problems_solved: int  # correct submissions
    accuracy: float  # 0.0-1.0
    first_attempted: Optional[str] = None  # ISO date
    last_practiced: Optional[str] = None  # ISO date
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MasteryGraph:
    """Complete mastery graph for a user."""
    overall_level: float  # Average of all skill levels
    total_skills: int
    mastered_count: int  # level == 5
    strong_count: int  # level >= 4
    weak_count: int  # level <= 1 and attempted
    untried_count: int  # level == 0
    skills: Dict[str, SkillMastery] = field(default_factory=dict)
    category_summary: Dict[str, Dict[str, Any]] = field(default_factory=dict)


def calculate_mastery_level(problems_attempted: int, accuracy: float) -> int:
    """Calculate mastery level from problem count and accuracy.

    Decision tree:
    - Never attempted → 0
    - 1-2 problems → 1 (regardless of accuracy)
    - 3-5 problems + <50% accuracy → 2
    - 3-5 problems + >=50% accuracy → 3
    - 6-10 problems + <75% accuracy → 3
    - 6-10 problems + >=75% accuracy → 4
    - 11-20 problems + <90% accuracy → 4
    - 11-20 problems + >=90% accuracy → 5
    - 20+ problems + <90% accuracy → 4
    - 20+ problems + >=90% accuracy → 5

    Args:
        problems_attempted: Total number of problems attempted in this skill.
        accuracy: Accuracy rate (0.0 to 1.0).

    Returns:
        Mastery level from 0 to 5.
    """
    if problems_attempted == 0:
        return 0
    if problems_attempted <= 2:
        return 1
    if problems_attempted <= 5:
        return 2 if accuracy < 0.50 else 3
    if problems_attempted <= 10:
        return 3 if accuracy < 0.75 else 4
    if problems_attempted <= 20:
        return 4 if accuracy < 0.90 else 5
    # 20+ problems
    return 4 if accuracy < 0.90 else 5


def calculate_mastery_from_stats(
    problems_attempted: int,
    problems_solved: int,
    first_attempted: Optional[str] = None,
    last_practiced: Optional[str] = None,
    recent_accuracy: Optional[float] = None,
) -> SkillMastery:
    """Calculate full mastery state from raw stats.

    Args:
        problems_attempted: Total attempts.
        problems_solved: Correct solves.
        first_attempted: ISO date of first attempt.
        last_practiced: ISO date of most recent practice.
        recent_accuracy: Optional accuracy for recent attempts only.

    Returns:
        SkillMastery with level, name, and all metadata.
    """
    accuracy = problems_solved / problems_attempted if problems_attempted > 0 else 0.0
    level = calculate_mastery_level(problems_attempted, accuracy)
    level_info = MASTERY_LEVELS[level]

    return SkillMastery(
        topic="",
        sub_topic="",
        level=level,
        name=level_info["name"],
        problems_attempted=problems_attempted,
        problems_solved=problems_solved,
        accuracy=round(accuracy, 4),
        first_attempted=first_attempted,
        last_practiced=last_practiced,
        details={
            "recent_accuracy": round(recent_accuracy, 4) if recent_accuracy is not None else None,
            "level_threshold": level_info,
        },
    )


def build_mastery_graph(skills_data: List[Dict[str, Any]]) -> MasteryGraph:
    """Build a complete mastery graph from pre-fetched skill data.

    Each item in skills_data should contain:
        topic: str, sub_topic: str, problems_attempted: int,
        problems_solved: int, first_attempted: str|None,
        last_practiced: str|None, recent_accuracy: float|None

    Args:
        skills_data: List of per-skill stat dicts.

    Returns:
        MasteryGraph with all skills scored and summary statistics.
    """
    skills = {}
    total_level = 0

    for item in skills_data:
        topic = item.get("topic", "unknown")
        sub_topic = item.get("sub_topic", "unknown")
        key = f"{topic}:{sub_topic}"

        mastery = calculate_mastery_from_stats(
            problems_attempted=item.get("problems_attempted", 0),
            problems_solved=item.get("problems_solved", 0),
            first_attempted=item.get("first_attempted"),
            last_practiced=item.get("last_practiced"),
            recent_accuracy=item.get("recent_accuracy"),
        )
        mastery.topic = topic
        mastery.sub_topic = sub_topic

        skills[key] = mastery
        total_level += mastery.level

    total_skills = len(skills)
    overall = total_level / total_skills if total_skills > 0 else 0

    mastered_count = sum(1 for s in skills.values() if s.level == 5)
    strong_count = sum(1 for s in skills.values() if s.level >= 4)
    weak_count = sum(1 for s in skills.values() if s.level <= 1 and s.problems_attempted > 0)
    untried_count = sum(1 for s in skills.values() if s.level == 0)

    # Category summary
    categories: Dict[str, Dict[str, Any]] = {}
    for key, mastery in skills.items():
        cat = mastery.topic
        if cat not in categories:
            categories[cat] = {
                "total": 0, "mastered": 0, "strong": 0, "weak": 0,
                "total_level": 0, "avg_level": 0,
            }
        categories[cat]["total"] += 1
        categories[cat]["total_level"] += mastery.level
        if mastery.level == 5:
            categories[cat]["mastered"] += 1
        if mastery.level >= 4:
            categories[cat]["strong"] += 1
        if mastery.level <= 1 and mastery.problems_attempted > 0:
            categories[cat]["weak"] += 1

    for cat_data in categories.values():
        cat_data["avg_level"] = round(cat_data["total_level"] / cat_data["total"], 2) if cat_data["total"] > 0 else 0
        del cat_data["total_level"]

    return MasteryGraph(
        overall_level=round(overall, 2),
        total_skills=total_skills,
        mastered_count=mastered_count,
        strong_count=strong_count,
        weak_count=weak_count,
        untried_count=untried_count,
        skills=skills,
        category_summary=categories,
    )


def find_weak_areas(skills_data: List[Dict[str, Any]], top_n: int = 10) -> List[Dict[str, Any]]:
    """Find the weakest skills that have the most room for improvement.

    Weak areas are skills with mastery level < 3, sorted by:
    1. Number of attempts (more attempts = more invested, easier to improve)
    2. Lower accuracy first
    3. Lower level first

    Args:
        skills_data: List of per-skill stat dicts.
        top_n: Maximum number of weak areas to return.

    Returns:
        List of weak area dicts sorted by improvement potential.
    """
    weak = []
    for item in skills_data:
        attempted = item.get("problems_attempted", 0)
        solved = item.get("problems_solved", 0)
        accuracy = solved / attempted if attempted > 0 else 0.0
        level = calculate_mastery_level(attempted, accuracy)

        if level < 3 and attempted > 0:
            weak.append({
                "topic": item.get("topic", "unknown"),
                "sub_topic": item.get("sub_topic", "unknown"),
                "level": level,
                "level_name": MASTERY_LEVELS[level]["name"],
                "problems_attempted": attempted,
                "problems_solved": solved,
                "accuracy": round(accuracy * 100, 1),
                "improvement_potential": (3 - level) * 10 + attempted * 0.5,
            })

    # Sort: lowest level first, then most attempts first
    weak.sort(key=lambda x: (x["level"], -x["problems_attempted"]))
    return weak[:top_n]


def record_solve(
    topic: str,
    sub_topic: str,
    is_correct: bool,
    existing_stats: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Record a problem solve and return updated mastery stats.

    Pure function — does NOT touch the database. Callers should
    upsert the returned stats into their collection.

    Args:
        topic: The skill/topic category (e.g., "arrays", "graphs").
        sub_topic: The specific skill within the topic (e.g., "two-pointers").
        is_correct: Whether the solve was correct.
        existing_stats: Previous stats for this user+skill, or None if first time.

    Returns:
        Dict with updated stats to be stored by the caller.
    """
    now_iso = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat()

    if existing_stats:
        attempted = existing_stats.get("problems_attempted", 0) + 1
        solved = existing_stats.get("problems_solved", 0) + (1 if is_correct else 0)
        first_attempted = existing_stats.get("first_attempted", now_iso)
        last_practiced = now_iso

        # Track recent accuracy (last 5 attempts) using a sliding window
        recent_history = existing_stats.get("recent_history", [])
        recent_history.append(1 if is_correct else 0)
        if len(recent_history) > 5:
            recent_history = recent_history[-5:]
        recent_accuracy = sum(recent_history) / len(recent_history) if recent_history else None
    else:
        attempted = 1
        solved = 1 if is_correct else 0
        first_attempted = now_iso
        last_practiced = now_iso
        recent_history = [1 if is_correct else 0]
        recent_accuracy = 1.0 if is_correct else 0.0

    level = calculate_mastery_level(attempted, solved / attempted if attempted > 0 else 0)

    return {
        "topic": topic,
        "sub_topic": sub_topic,
        "problems_attempted": attempted,
        "problems_solved": solved,
        "first_attempted": first_attempted,
        "last_practiced": last_practiced,
        "recent_history": recent_history,
        "recent_accuracy": recent_accuracy,
        "current_level": level,
        "current_level_name": MASTERY_LEVELS[level]["name"],
    }


def get_mastery_label(level: int) -> str:
    """Get human-readable label for a mastery level.

    Args:
        level: Integer level 0-5.

    Returns:
        String label like 'Unknown', 'Introduced', etc.
    """
    return MASTERY_LEVELS.get(level, MASTERY_LEVELS[0])["name"]


def get_mastery_color(level: int) -> str:
    """Get a hex color for visual representation of a mastery level.

    Args:
        level: Integer level 0-5.

    Returns:
        Hex color string.
    """
    colors = {
        0: "#6b7280",  # gray
        1: "#ef4444",  # red
        2: "#f59e0b",  # amber
        3: "#3b82f6",  # blue
        4: "#22c55e",  # green
        5: "#a855f7",  # purple
    }
    return colors.get(level, colors[0])
