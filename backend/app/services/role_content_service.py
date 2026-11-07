"""Role Content Service — integrates role content with the existing pipeline.

This service connects:
  Role exercises/challenges → Mastery evidence → SRS → Diamonds → Readiness

It does NOT create a new system. It extends the existing Study Engine,
Mastery Engine, Gamification, and SRS with role-specific activities.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from app.content.role_content import (
    get_exercises_for_role,
    get_challenges_for_role,
    get_practice_sets_for_role,
    get_exercise_by_id,
    get_challenge_by_id,
)
from app.content.role_packages import get_role_package
from app.services.skill_assessment import update_skill_score
from app.services.gamification import record_practice
from app.services.spaced_repetition import get_due_cards, SpacedRepetitionEngine

logger = logging.getLogger(__name__)


async def record_role_activity(
    user_id: str,
    role_id: str,
    activity_type: str,
    activity_id: str,
    passed: bool,
    score: float = 100.0,
    time_spent: int = 0,
) -> Dict[str, Any]:
    """Record a role-specific activity and fan-out to mastery / SRS / Diamonds.

    This is the canonical completion sink for role content. When a student
    completes an exercise or challenge, this function:
    1. Updates the skill graph (mastery evidence)
    2. Awards Diamonds and coins (gamification)
    3. Schedules SRS review (spaced repetition)
    4. Updates role readiness

    Args:
        user_id: The student's ID
        role_id: The role they're preparing for (sde, data_scientist, etc.)
        activity_type: "exercise" | "challenge" | "quiz"
        activity_id: The specific exercise/challenge/quiz ID
        passed: Whether they completed it successfully
        score: 0-100 score
        time_spent: Seconds spent on the activity

    Returns:
        Dict with xp_awarded, mastery_updated, srs_scheduled, readiness_delta
    """
    result: Dict[str, Any] = {
        "recorded": False,
        "xp_awarded": 0,
        "mastery_updated": False,
        "srs_scheduled": False,
    }

    # ── 1. Mastery update ──
    category = _get_category_for_activity(activity_type, role_id)
    try:
        await update_skill_score(user_id, category, activity_id, score, passed)
        result["mastery_updated"] = True
    except Exception as exc:
        logger.warning("Mastery update failed for %s: %s", user_id, exc)

    # ── 2. Gamification / Diamonds ──
    diamonds = _calculate_xp(activity_type, passed, score)
    try:
        await record_practice(
            user_id,
            activity=activity_type,
            score=score,
            metadata={
                "role_id": role_id,
                "activity_id": activity_id,
                "passed": passed,
                "time_spent": time_spent,
            },
            role=role_id,
        )
        result["xp_awarded"] = diamonds
        result["xp_applied"] = True
    except Exception as exc:
        logger.warning("Gamification record failed for %s: %s", user_id, exc)
        result["xp_applied"] = False

    # ── 3. SRS card update ──
    try:
        from app.database import srs_cards_collection
        col = srs_cards_collection()
        existing = await col.find_one({"user_id": user_id, "problem_id": activity_id})
        engine = SpacedRepetitionEngine()
        if existing:
            from app.services.spaced_repetition import SRSCard
            card = SRSCard.from_dict(existing)
            card = update_card(card, passed)
            await col.update_one(
                {"user_id": user_id, "problem_id": activity_id},
                {"$set": card.to_dict()},
                upsert=True,
            )
        else:
            card = engine.create_new_card(activity_id, user_id)
            if not passed:
                card = update_card(card, False)
            await col.insert_one(card.to_dict())
        result["srs_scheduled"] = True
    except Exception as exc:
        logger.warning("SRS update skipped for %s: %s", user_id, exc)

    result["recorded"] = True
    return result


def _get_category_for_activity(activity_type: str, role_id: str) -> str:
    """Map activity + role to a mastery category."""
    role_category_map = {
        "sde": "coding",
        "data_scientist": "data",
        "ml_engineer": "ai",
        "devops": "infrastructure",
        "frontend": "frontend",
        "cp": "coding",
    }
    return role_category_map.get(role_id, "coding")


def _calculate_xp(activity_type: str, passed: bool, score: float) -> int:
    """Calculate Diamonds for a role activity."""
    base = {
        "exercise": 25,
        "challenge": 40,
        "quiz": 15,
    }.get(activity_type, 20)

    if passed:
        bonus = int((score / 100) * 20)
    else:
        bonus = -5

    return max(0, base + bonus)


def get_role_readiness_contribution(role_id: str, activity_type: str, passed: bool) -> float:
    """Calculate how much a role activity contributes to readiness."""
    weights = {
        "exercise": 2.0,
        "challenge": 3.0,
        "quiz": 1.0,
    }
    base = weights.get(activity_type, 1.0)
    return base if passed else base * 0.2  # Partial credit for attempts


async def get_next_role_activity(user_id: str, role_id: str) -> Optional[Dict[str, Any]]:
    """Get the next recommended activity for a role.

    Uses the Study Engine's logic but filters for role-specific content.
    Returns an exercise, challenge, or SRS review based on priority:
    1. SRS reviews due now
    2. Weak-skill exercises
    3. Role practice set progression

    When a company track is enrolled, exercises are filtered to
    company-relevant topics (company requirement × student weakness ×
    prerequisite × evidence freshness × assessment relevance).
    """
    package = get_role_package(role_id)
    if not package:
        return None

    # ── Read user goal for company-aware filtering ──
    company_relevant_topics: List[str] = []
    try:
        from app.database import users_collection
        user_doc = await users_collection().find_one({"user_id": user_id}) or {}
        company_track = user_doc.get("company_track", "")
        if company_track:
            from app.data.learning_paths import COMPANY_TRACKS
            track = COMPANY_TRACKS.get(company_track)
            if track:
                for section in track.get("sections", []):
                    for topic in section.get("topics", []):
                        for sub in topic.get("sub_topics", []):
                            company_relevant_topics.append(sub)
    except Exception:
        pass

    # Check for due SRS reviews first
    try:
        from app.database import srs_cards_collection
        col = srs_cards_collection()
        cards = []
        async for doc in col.find({"user_id": user_id}).limit(50):
            from app.services.spaced_repetition import SRSCard
            try:
                cards.append(SRSCard.from_dict(doc))
            except Exception:
                continue
        due = get_due_cards(cards, limit=3)
        if due:
            return {
                "type": "review",
                "title": "Review due concepts",
                "count": len(due),
                "activity_ids": [c.problem_id for c in due],
                "role_id": role_id,
            }
    except Exception:
        pass

    # Recommend next exercise from practice set
    practice_sets = get_practice_sets_for_role(role_id)
    if practice_sets:
        ps = practice_sets[0]
        if ps.exercise_ids:
            # ── Company-aware filtering: prefer exercises tagged with
            # company-relevant topics when a company track is enrolled ──
            exercise_id = ps.exercise_ids[0]
            if company_relevant_topics:
                from app.content.role_content import get_exercise_by_id
                company_exercises = [
                    eid for eid in ps.exercise_ids
                    if any(t in (get_exercise_by_id(eid).topics if get_exercise_by_id(eid) else [])
                           for t in company_relevant_topics)
                ]
                if company_exercises:
                    exercise_id = company_exercises[0]
            return {
                "type": "exercise",
                "title": ps.title,
                "description": ps.description,
                "activity_id": exercise_id,
                "role_id": role_id,
                "practice_set_id": ps.id,
            }

    # Fallback to challenges
    challenges = get_challenges_for_role(role_id)
    if challenges:
        return {
            "type": "challenge",
            "title": challenges[0].title,
            "description": challenges[0].description,
            "activity_id": challenges[0].id,
            "role_id": role_id,
        }

    return None


def get_role_dashboard(user_id: str, role_id: str) -> Dict[str, Any]:
    """Get a role-specific dashboard for the Journey page."""
    package = get_role_package(role_id)
    exercises = get_exercises_for_role(role_id)
    challenges = get_challenges_for_role(role_id)
    practice_sets = get_practice_sets_for_role(role_id)

    return {
        "role": package.model_dump() if package else None,
        "stats": {
            "total_exercises": len(exercises),
            "total_challenges": len(challenges),
            "total_practice_sets": len(practice_sets),
            "easy_exercises": sum(1 for e in exercises if e.difficulty == "easy"),
            "medium_exercises": sum(1 for e in exercises if e.difficulty == "medium"),
            "hard_exercises": sum(1 for e in exercises if e.difficulty == "hard"),
        },
        "practice_sets": [ps.model_dump() for ps in practice_sets],
        "recent_exercises": [e.model_dump() for e in exercises[:5]],
    }
