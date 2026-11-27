"""
Skill Mastery Engine — deterministic mastery tracking per topic/sub_topic.

Tracks mastery on a 0-5 scale based on solved_problems history:

  0 = Unknown     — never attempted
  1 = Introduced  — attempted 1-2 unique questions
  2 = Practicing  — 3-5 unique questions, <50% accuracy
  3 = Competent   — 6-10 unique questions, 50-75% accuracy
  4 = Strong      — 11-20 unique questions, 75-90% accuracy
  5 = Mastered    — 20+ unique questions, >90% accuracy

Key integrity rules (Phase 6):
- Repeated attempts at ONE question do NOT create unlimited mastery evidence.
  Only unique validated question IDs count toward problem counts.
- Unseen transfer questions contribute meaningful evidence (harder questions
  weight more, transfer questions count double for mastery evidence).
- Invalid or untrusted questions (trust_status not in {verified, reviewed})
  do NOT contribute to mastery.
- Difficulty influences evidence: hard > medium > easy weighting.
- Prerequisite skills must be respected: a skill cannot be Mastered if its
  prerequisites are not at least Competent.
- Repeated failures trigger targeted remediation flags.
- Mastery is reproducible and explainable: every level change has an
  evidence trail (question_ids, difficulty weights, timestamps).

All functions are pure and testable without a database — they accept
pre-fetched data dicts and return structured results.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple
from datetime import datetime, timezone


# Mastery level thresholds
MASTERY_LEVELS = {
    0: {"name": "Unknown", "min_unique_questions": 0, "min_accuracy": 0.0},
    1: {"name": "Introduced", "min_unique_questions": 1, "min_accuracy": 0.0},
    2: {"name": "Practicing", "min_unique_questions": 3, "min_accuracy": 0.0},
    3: {"name": "Competent", "min_unique_questions": 6, "min_accuracy": 0.50},
    4: {"name": "Strong", "min_unique_questions": 11, "min_accuracy": 0.75},
    5: {"name": "Mastered", "min_unique_questions": 20, "min_accuracy": 0.90},
}

# Difficulty weights for mastery evidence
DIFFICULTY_WEIGHTS = {
    "easy": 1.0,
    "medium": 1.5,
    "hard": 2.0,
}

# Trust statuses that contribute to mastery evidence
MASTERED_TRUST_STATUSES = {"verified", "reviewed"}


@dataclass
class QuestionEvidence:
    """Evidence from a single question attempt contributing to mastery."""
    question_id: str
    question_type: str
    difficulty: str
    is_correct: bool
    trust_status: str
    timestamp: str
    difficulty_weight: float
    is_transfer: bool = False  # True if this was an unseen transfer assessment
    prerequisite_met: bool = True


@dataclass
class SkillMastery:
    """Mastery state for a single skill/topic."""
    topic: str
    sub_topic: str
    level: int  # 0-5
    name: str  # Human-readable level name
    unique_questions_attempted: int  # count of unique question IDs
    unique_questions_solved: int  # count of unique question IDs solved correctly
    total_attempts: int  # all attempts including repeats
    accuracy: float  # 0.0-1.0 based on unique questions
    weighted_evidence: float  # sum of difficulty weights for correct unique questions
    first_attempted: Optional[str] = None  # ISO date
    last_practiced: Optional[str] = None  # ISO date
    remediation_needed: bool = False  # True if repeated failures on same question
    evidence_trail: List[QuestionEvidence] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)
    prerequisite_skills: List[str] = field(default_factory=list)
    prerequisites_met: bool = True


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
    remediation_queue: List[Dict[str, Any]] = field(default_factory=list)


def _difficulty_weight(difficulty: str) -> float:
    """Return the evidence weight for a difficulty level."""
    return DIFFICULTY_WEIGHTS.get(str(difficulty or "").lower(), 1.0)


def _difficulty_bonus(difficulty: str) -> float:
    """Bonus multiplier for transfer (unseen) questions."""
    return DIFFICULTY_WEIGHTS.get(str(difficulty or "").lower(), 1.0)


def calculate_mastery_level(
    unique_questions_attempted: int,
    unique_questions_solved: int,
    weighted_evidence: float = 0.0,
) -> int:
    """
    Calculate mastery level from unique question count and accuracy.

    Uses unique question IDs (not total attempts) to prevent inflated
    mastery from repeated attempts at the same question.

    Decision tree:
    - Never attempted → 0
    - 1-2 unique questions → 1 (regardless of accuracy)
    - 3-5 unique questions + <50% accuracy → 2
    - 3-5 unique questions + >=50% accuracy → 3
    - 6-10 unique questions + <75% accuracy → 3
    - 6-10 unique questions + >=75% accuracy → 4
    - 11-20 unique questions + <90% accuracy → 4
    - 11-20 unique questions + >=90% accuracy → 5
    - 20+ unique questions + <90% accuracy → 4
    - 20+ unique questions + >=90% accuracy → 5
    """
    if unique_questions_attempted == 0:
        return 0
    if unique_questions_attempted <= 2:
        return 1
    accuracy = unique_questions_solved / unique_questions_attempted if unique_questions_attempted > 0 else 0.0
    if unique_questions_attempted <= 5:
        return 2 if accuracy < 0.50 else 3
    if unique_questions_attempted <= 10:
        return 3 if accuracy < 0.75 else 4
    if unique_questions_attempted <= 20:
        return 4 if accuracy < 0.90 else 5
    # 20+ unique questions
    return 4 if accuracy < 0.90 else 5


def calculate_mastery_from_stats(
    topic: str,
    sub_topic: str,
    unique_question_ids: Optional[List[str]] = None,
    solved_question_ids: Optional[List[str]] = None,
    total_attempts: int = 0,
    first_attempted: Optional[str] = None,
    last_practiced: Optional[str] = None,
    evidence_trail: Optional[List[QuestionEvidence]] = None,
    prerequisite_skills: Optional[List[str]] = None,
    prerequisites_met: bool = True,
) -> SkillMastery:
    """
    Calculate full mastery state from unique question evidence.

    Only unique question IDs count toward problem counts. Repeated attempts
    at the same question increment total_attempts but not unique counts.

    Args:
        topic: Skill topic name.
        sub_topic: Skill sub-topic name.
        unique_question_ids: List of unique question IDs attempted.
        solved_question_ids: List of unique question IDs solved correctly.
        total_attempts: Total number of attempts (including repeats).
        first_attempted: ISO date of first attempt.
        last_practiced: ISO date of most recent practice.
        evidence_trail: Per-question evidence records.
        prerequisite_skills: List of prerequisite skill IDs.
        prerequisites_met: Whether all prerequisites are satisfied.

    Returns:
        SkillMastery with level, name, and all metadata.
    """
    unique_question_ids = unique_question_ids or []
    solved_question_ids = solved_question_ids or []
    evidence_trail = evidence_trail or []

    unique_attempted = len(set(unique_question_ids))
    unique_solved = len(set(solved_question_ids))
    accuracy = unique_solved / unique_attempted if unique_attempted > 0 else 0.0

    # Weighted evidence: sum of difficulty weights for correctly solved unique questions.
    # Each unique question contributes at most once (deduplicated by question_id),
    # even if it appears multiple times in the evidence trail (e.g. repeated attempts).
    weighted_evidence = 0.0
    counted_question_ids: set[str] = set()
    for ev in evidence_trail:
        if ev.is_correct and ev.question_id in set(solved_question_ids):
            if ev.question_id in counted_question_ids:
                continue  # already counted this unique question
            counted_question_ids.add(ev.question_id)
            weight = ev.difficulty_weight
            if ev.is_transfer:
                weight *= 2.0  # transfer questions count double
            weighted_evidence += weight

    level = calculate_mastery_level(unique_attempted, unique_solved, weighted_evidence)
    level_info = MASTERY_LEVELS[level]

    # Remediation needed if: attempted >= 3 unique questions but accuracy < 0.5,
    # or any question has repeated failures (same question_id, multiple incorrect attempts)
    remediation_needed = False
    if unique_attempted >= 3 and accuracy < 0.50:
        remediation_needed = True
    # Check for repeated failures on same question
    failed_counts: Dict[str, int] = {}
    for ev in evidence_trail:
        if not ev.is_correct:
            failed_counts[ev.question_id] = failed_counts.get(ev.question_id, 0) + 1
    if any(count >= 2 for count in failed_counts.values()):
        remediation_needed = True

    return SkillMastery(
        topic=topic,
        sub_topic=sub_topic,
        level=level,
        name=level_info["name"],
        unique_questions_attempted=unique_attempted,
        unique_questions_solved=unique_solved,
        total_attempts=total_attempts,
        accuracy=round(accuracy, 4),
        weighted_evidence=round(weighted_evidence, 4),
        first_attempted=first_attempted,
        last_practiced=last_practiced,
        remediation_needed=remediation_needed,
        evidence_trail=evidence_trail,
        details={
            "level_threshold": level_info,
            "weighted_evidence": round(weighted_evidence, 4),
            "unique_attempted": unique_attempted,
            "unique_solved": unique_solved,
        },
        prerequisite_skills=prerequisite_skills or [],
        prerequisites_met=prerequisites_met,
    )


def record_solve(
    topic: str,
    sub_topic: str,
    question_id: str,
    question_type: str,
    difficulty: str,
    is_correct: bool,
    trust_status: str = "unverified",
    is_transfer: bool = False,
    existing_stats: Optional[Dict[str, Any]] = None,
    prerequisite_skills: Optional[List[str]] = None,
    prerequisites_met: bool = True,
    timestamp: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Record a problem solve and return updated mastery stats.

    Pure function — does NOT touch the database. Callers should
    upsert the returned stats into their collection.

    Integrity rules:
    - Only unique question IDs count toward unique_questions_attempted/solved.
    - Questions with trust_status not in {verified, reviewed} are recorded
      in total_attempts but NOT counted as unique evidence.
    - Repeated attempts at the same question increment total_attempts but
      do not create new mastery evidence.
    - Difficulty weights evidence: hard > medium > easy.
    - Transfer questions count double for weighted evidence.

    Args:
        topic: Skill topic name.
        sub_topic: Skill sub-topic name.
        question_id: Unique question identifier.
        question_type: Type of question (coding, aptitude, logical, etc.).
        difficulty: Question difficulty (easy, medium, hard).
        is_correct: Whether the solve was correct.
        trust_status: Trust status of the question (only verified/reviewed count as evidence).
        is_transfer: Whether this was an unseen transfer assessment question.
        existing_stats: Previous stats for this user+skill, or None if first time.
        prerequisite_skills: List of prerequisite skill IDs.
        prerequisites_met: Whether all prerequisites are satisfied.
        timestamp: ISO timestamp (defaults to now).

    Returns:
        Dict with updated stats to be stored by the caller.
    """
    now_iso = timestamp or datetime.now(timezone.utc).isoformat()
    diff_weight = _difficulty_weight(difficulty)

    # Determine if this question contributes as unique evidence
    is_trusted = str(trust_status).lower() in MASTERED_TRUST_STATUSES

    if existing_stats:
        questions_seen = list(existing_stats.get("questions_seen", []))
        solved_questions = list(existing_stats.get("solved_question_ids", []))
        evidence_trail = existing_stats.get("evidence_trail", [])
        if isinstance(evidence_trail, list):
            evidence_trail = [QuestionEvidence(**e) if isinstance(e, dict) else e for e in evidence_trail]
        else:
            evidence_trail = []

        # Check if this is a new unique question
        is_new_question = question_id not in questions_seen

        # Only trusted questions are added to the unique evidence set.
        # Untrusted questions increment total_attempts only.
        if is_new_question and is_trusted:
            questions_seen.append(question_id)
            if is_correct:
                solved_questions.append(question_id)
        # Untrusted questions: recorded in total_attempts only, not unique counts

        total_attempts = existing_stats.get("total_attempts", 0) + 1
        first_attempted = existing_stats.get("first_attempted", now_iso)
        last_practiced = now_iso

        # Track recent accuracy (last 5 attempts) using a sliding window
        recent_history = existing_stats.get("recent_history", [])
        recent_history.append(1 if is_correct else 0)
        if len(recent_history) > 5:
            recent_history = recent_history[-5:]
        recent_accuracy = sum(recent_history) / len(recent_history) if recent_history else None

        # Build evidence trail entry
        evidence = QuestionEvidence(
            question_id=question_id,
            question_type=question_type,
            difficulty=difficulty,
            is_correct=is_correct,
            trust_status=trust_status,
            timestamp=now_iso,
            difficulty_weight=diff_weight,
            is_transfer=is_transfer,
            prerequisite_met=prerequisites_met,
        )
        evidence_trail.append(evidence)

        # Detect repeated failures on same question
        failed_counts: Dict[str, int] = {}
        for ev in evidence_trail:
            if not ev.is_correct:
                failed_counts[ev.question_id] = failed_counts.get(ev.question_id, 0) + 1
        remediation_needed = any(count >= 2 for count in failed_counts.values())
        if not remediation_needed:
            # Also check overall accuracy on 3+ unique questions
            unique_ids = set(questions_seen)
            unique_solved_ids = set(solved_questions)
            acc = len(unique_solved_ids) / len(unique_ids) if unique_ids else 0.0
            if len(unique_ids) >= 3 and acc < 0.50:
                remediation_needed = True
        existing_remediation = existing_stats.get("remediation_needed", False)
        remediation_needed = remediation_needed or existing_remediation

    else:
        # First attempt: only trusted questions enter the unique evidence set
        questions_seen = [question_id] if is_trusted else []
        solved_questions = [question_id] if (is_correct and is_trusted) else []
        total_attempts = 1
        first_attempted = now_iso
        last_practiced = now_iso
        recent_history = [1 if is_correct else 0]
        recent_accuracy = 1.0 if is_correct else 0.0

        evidence = QuestionEvidence(
            question_id=question_id,
            question_type=question_type,
            difficulty=difficulty,
            is_correct=is_correct,
            trust_status=trust_status,
            timestamp=now_iso,
            difficulty_weight=diff_weight,
            is_transfer=is_transfer,
            prerequisite_met=prerequisites_met,
        )
        evidence_trail = [evidence]
        remediation_needed = False

    # Build unique ID lists for mastery calculation
    unique_question_ids = list(set(questions_seen))
    unique_solved_ids = list(set(solved_questions))

    mastery = calculate_mastery_from_stats(
        topic=topic,
        sub_topic=sub_topic,
        unique_question_ids=unique_question_ids,
        solved_question_ids=unique_solved_ids,
        total_attempts=total_attempts,
        first_attempted=first_attempted,
        last_practiced=last_practiced,
        evidence_trail=evidence_trail,
        prerequisite_skills=prerequisite_skills or [],
        prerequisites_met=prerequisites_met,
    )

    # Apply prerequisite gating: if prerequisites not met, cap level at 2 (Practicing)
    if not prerequisites_met and mastery.level > 2:
        mastery.level = 2
        mastery.name = MASTERY_LEVELS[2]["name"]
        mastery.details["prerequisite_gated"] = True
        mastery.details["original_level"] = calculate_mastery_level(
            mastery.unique_questions_attempted, mastery.unique_questions_solved
        )

    return {
        "topic": topic,
        "sub_topic": sub_topic,
        "unique_questions_attempted": mastery.unique_questions_attempted,
        "unique_questions_solved": mastery.unique_questions_solved,
        "total_attempts": total_attempts,
        "accuracy": mastery.accuracy,
        "weighted_evidence": mastery.weighted_evidence,
        "first_attempted": first_attempted,
        "last_practiced": last_practiced,
        "recent_history": recent_history,
        "recent_accuracy": recent_accuracy,
        "current_level": mastery.level,
        "current_level_name": mastery.name,
        "questions_seen": questions_seen,
        "solved_question_ids": solved_questions,
        "evidence_trail": [
            {
                "question_id": e.question_id,
                "question_type": e.question_type,
                "difficulty": e.difficulty,
                "is_correct": e.is_correct,
                "trust_status": e.trust_status,
                "timestamp": e.timestamp,
                "difficulty_weight": e.difficulty_weight,
                "is_transfer": e.is_transfer,
                "prerequisite_met": e.prerequisite_met,
            }
            for e in evidence_trail
        ],
        "remediation_needed": mastery.remediation_needed,
        "prerequisites_met": mastery.prerequisites_met,
        "prerequisite_skills": mastery.prerequisite_skills,
        "details": mastery.details,
    }


def build_mastery_graph(skills_data: List[Dict[str, Any]]) -> MasteryGraph:
    """
    Build a complete mastery graph from pre-fetched skill data.

    Each item in skills_data should contain:
        topic: str, sub_topic: str, unique_questions_attempted: int,
        unique_questions_solved: int, total_attempts: int,
        first_attempted: str|None, last_practiced: str|None,
        evidence_trail: list[dict]|None, prerequisite_skills: list[str]|None,
        prerequisites_met: bool

    Args:
        skills_data: List of per-skill stat dicts.

    Returns:
        MasteryGraph with all skills scored and summary statistics.
    """
    skills = {}
    total_level = 0
    remediation_queue = []

    for item in skills_data:
        topic = item.get("topic", "unknown")
        sub_topic = item.get("sub_topic", "unknown")
        key = f"{topic}:{sub_topic}"

        mastery = calculate_mastery_from_stats(
            topic=topic,
            sub_topic=sub_topic,
            unique_question_ids=item.get("unique_question_ids", []),
            solved_question_ids=item.get("solved_question_ids", []),
            total_attempts=item.get("total_attempts", 0),
            first_attempted=item.get("first_attempted"),
            last_practiced=item.get("last_practiced"),
            evidence_trail=[
                QuestionEvidence(**e) if isinstance(e, dict) else e
                for e in (item.get("evidence_trail") or [])
            ],
            prerequisite_skills=item.get("prerequisite_skills", []),
            prerequisites_met=item.get("prerequisites_met", True),
        )

        skills[key] = mastery
        total_level += mastery.level

        if mastery.remediation_needed:
            remediation_queue.append({
                "topic": topic,
                "sub_topic": sub_topic,
                "level": mastery.level,
                "level_name": mastery.name,
                "accuracy": mastery.accuracy,
                "unique_questions_attempted": mastery.unique_questions_attempted,
                "reason": "repeated_failures_or_low_accuracy",
            })

    total_skills = len(skills)
    overall = total_level / total_skills if total_skills > 0 else 0

    mastered_count = sum(1 for s in skills.values() if s.level == 5)
    strong_count = sum(1 for s in skills.values() if s.level >= 4)
    weak_count = sum(1 for s in skills.values() if s.level <= 1 and s.unique_questions_attempted > 0)
    untried_count = sum(1 for s in skills.values() if s.level == 0)

    # Category summary
    categories: Dict[str, Dict[str, Any]] = {}
    for key, mastery in skills.items():
        cat = mastery.topic
        if cat not in categories:
            categories[cat] = {
                "total": 0, "mastered": 0, "strong": 0, "weak": 0,
                "untried": 0, "total_level": 0, "avg_level": 0,
            }
        categories[cat]["total"] += 1
        categories[cat]["total_level"] += mastery.level
        if mastery.level == 5:
            categories[cat]["mastered"] += 1
        if mastery.level >= 4:
            categories[cat]["strong"] += 1
        if mastery.level <= 1 and mastery.unique_questions_attempted > 0:
            categories[cat]["weak"] += 1
        if mastery.level == 0:
            categories[cat]["untried"] += 1

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
        remediation_queue=sorted(remediation_queue, key=lambda x: x["accuracy"]),
    )


def find_weak_areas(skills_data: List[Dict[str, Any]], top_n: int = 10) -> List[Dict[str, Any]]:
    """
    Find the weakest skills that have the most room for improvement.

    Weak areas are skills with mastery level < 3, sorted by:
    1. Lowest accuracy first
    2. Most unique questions attempted (more invested = easier to improve)
    3. Lowest level first

    Args:
        skills_data: List of per-skill stat dicts.
        top_n: Maximum number of weak areas to return.

    Returns:
        List of weak area dicts sorted by improvement potential.
    """
    weak = []
    for item in skills_data:
        attempted = item.get("unique_questions_attempted", 0)
        solved = item.get("unique_questions_solved", 0)
        accuracy = solved / attempted if attempted > 0 else 0.0
        level = calculate_mastery_level(attempted, solved)

        if level < 3 and attempted > 0:
            weak.append({
                "topic": item.get("topic", "unknown"),
                "sub_topic": item.get("sub_topic", "unknown"),
                "level": level,
                "level_name": MASTERY_LEVELS[level]["name"],
                "unique_questions_attempted": attempted,
                "unique_questions_solved": solved,
                "total_attempts": item.get("total_attempts", 0),
                "accuracy": round(accuracy * 100, 1),
                "remediation_needed": item.get("remediation_needed", False),
                "prerequisites_met": item.get("prerequisites_met", True),
                "improvement_potential": (3 - level) * 10 + attempted * 0.5,
            })

    # Sort: lowest level first, then lowest accuracy, then most attempts
    weak.sort(key=lambda x: (x["level"], -x["accuracy"], -x["unique_questions_attempted"]))
    return weak[:top_n]


def check_prerequisites(
    skill_key: str,
    mastery_graph: MasteryGraph,
    prerequisite_map: Dict[str, List[str]],
) -> Tuple[bool, List[str]]:
    """
    Check whether all prerequisites for a skill are met.

    A prerequisite is met if the prerequisite skill's mastery level >= 3
    (Competent).

    Args:
        skill_key: The skill key (topic:sub_topic) to check.
        mastery_graph: The current mastery graph.
        prerequisite_map: Map of skill_key -> list of prerequisite skill keys.

    Returns:
        (all_met, unmet_prerequisites) tuple.
    """
    unmet = []
    for prereq_key in prerequisite_map.get(skill_key, []):
        prereq = mastery_graph.skills.get(prereq_key)
        if prereq is None or prereq.level < 3:
            unmet.append(prereq_key)
    return (len(unmet) == 0, unmet)


def get_mastery_label(level: int) -> str:
    """Get human-readable label for a mastery level."""
    return MASTERY_LEVELS.get(level, MASTERY_LEVELS[0])["name"]


def get_mastery_color(level: int) -> str:
    """Get a hex color for visual representation of a mastery level."""
    colors = {
        0: "#6b7280",  # gray
        1: "#ef4444",  # red
        2: "#f59e0b",  # amber
        3: "#3b82f6",  # blue
        4: "#22c55e",  # green
        5: "#a855f7",  # purple
    }
    return colors.get(level, colors[0])


def explain_mastery(skill_mastery: SkillMastery) -> Dict[str, Any]:
    """
    Produce a human-readable explanation of how a mastery level was derived.

    Returns evidence breakdown so the level is reproducible and explainable.
    """
    return {
        "topic": skill_mastery.topic,
        "sub_topic": skill_mastery.sub_topic,
        "level": skill_mastery.level,
        "level_name": skill_mastery.name,
        "basis": {
            "unique_questions_attempted": skill_mastery.unique_questions_attempted,
            "unique_questions_solved": skill_mastery.unique_questions_solved,
            "total_attempts": skill_mastery.total_attempts,
            "accuracy": skill_mastery.accuracy,
            "weighted_evidence": skill_mastery.weighted_evidence,
        },
        "threshold": MASTERY_LEVELS.get(skill_mastery.level, {}),
        "remediation_needed": skill_mastery.remediation_needed,
        "prerequisites_met": skill_mastery.prerequisites_met,
        "prerequisite_skills": skill_mastery.prerequisite_skills,
        "evidence_count": len(skill_mastery.evidence_trail),
        "reproducible": True,
    }
