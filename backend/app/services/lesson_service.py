"""Lesson service — reusable exam-style learning infrastructure.

Reuses existing question_store, scoring, exam_engine, skill_assessment,
path_generator, and gamification infrastructure. No duplicate systems.

Content is loaded from backend/app/services/lessons/ modules.
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.database import get_collection
from app.services.scoring import score_question
from app.services.skill_assessment import update_skill_score, get_skill_graph
from app.services.path_generator import decide_next_action
from app.services.lessons import _LESSONS

logger = logging.getLogger(__name__)

COLLECTION = get_collection("lesson_progress")


def list_lessons(track: Optional[str] = None) -> List[dict]:
    """Return all lessons, optionally filtered by track."""
    lessons = list(_LESSONS.values())
    if track:
        lessons = [l for l in lessons if l["track"] == track]
    return lessons


def search_lessons(query: str, track: Optional[str] = None) -> List[dict]:
    """Search lessons by title, description, step title/content."""
    q = query.lower()
    results = []
    for lesson in _LESSONS.values():
        if track and lesson["track"] != track:
            continue
        haystack = f"{lesson['title']} {lesson.get('description', '')} "
        for step in lesson.get("steps", []):
            haystack += f" {step.get('title', '')} {step.get('content', '')} {step.get('instruction', '')} {step.get('question', '')}"
        if q in haystack.lower():
            results.append(lesson)
    return results


def get_lesson(lesson_id: str) -> Optional[dict]:
    """Return a single lesson by id."""
    return _LESSONS.get(lesson_id)


# ═════════════════════════════════════════════════════════════════════
# Progress tracking
# ═════════════════════════════════════════════════════════════════════

async def get_progress(user_id: str) -> dict:
    """Get the user's lesson progress."""
    doc = await COLLECTION.find_one({"user_id": user_id})
    if not doc:
        return {"completed": {}, "current_lesson": None, "xp_earned": 0}
    return {
        "completed": doc.get("completed", {}),
        "current_lesson": doc.get("current_lesson"),
        "xp_earned": doc.get("xp_earned", 0),
    }


async def complete_step(
    user_id: str, lesson_id: str, step_id: str, code: str
) -> dict:
    """Record completion of a lesson step and return next action."""
    lesson = get_lesson(lesson_id)
    if not lesson:
        raise ValueError(f"Lesson {lesson_id} not found")

    step = next((s for s in lesson["steps"] if s["id"] == step_id), None)
    if not step:
        raise ValueError(f"Step {step_id} not found")

    # Score the answer for exercise steps
    is_correct = True
    feedback = ""
    if step["type"] == "exercise":
        q = {
            "id": step_id,
            "question": step.get("instruction", ""),
            "question_type": "code",
            "correct_answer": step.get("solution", ""),
        }
        sr = score_question(q, code)
        is_correct = sr["is_correct"]
        if is_correct:
            feedback = "Correct!"
        else:
            feedback = (
                f"Not quite. Try: {step.get('solution', '')}"
            )
            hints = step.get("hints")
            if hints:
                feedback += f" Hint: {hints[0]}"

    # Get or create progress
    progress = await get_progress(user_id)
    completed = dict(progress.get("completed", {}))
    lesson_key = f"{lesson_id}:{step_id}"
    completed[lesson_key] = {
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "is_correct": is_correct,
        "code": code,
    }

    # Check if full lesson is complete
    lesson_steps = [s["id"] for s in lesson["steps"]]
    lesson_done = all(
        f"{lesson_id}:{sid}" in completed for sid in lesson_steps
    )

    xp_earned = progress.get("xp_earned", 0)
    completed_lessons = set(
        k.split(":")[0]
        for k in progress.get("completed", {})
        if not k.startswith("_")
    )
    if lesson_done and lesson_id not in completed_lessons:
        xp_earned += lesson.get("xpReward", 0)
        completed_lessons.add(lesson_id)

    # Update skill graph
    if is_correct and step["type"] == "exercise":
        try:
            await update_skill_score(
                user_id=user_id,
                category="dsa",
                skill=lesson["track"],
                score=1.0,
                is_correct=True,
            )
        except Exception:
            pass

    # Persist
    await COLLECTION.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "completed": completed,
                "current_lesson": lesson_id if not lesson_done else None,
                "xp_earned": xp_earned,
                "updated_at": datetime.now(timezone.utc),
            }
        },
        upsert=True,
    )

    # Next action via path generator
    skill_graph = await get_skill_graph(user_id)
    next_action = decide_next_action(
        pattern=lesson["track"],
        mastery=0.5,
        weakness_tier="weak",
    )

    return {
        "is_correct": is_correct,
        "feedback": feedback,
        "lesson_complete": lesson_done,
        "xp_earned": lesson.get("xpReward", 0) if lesson_done else 0,
        "next_action": next_action,
    }


async def submit_exercise(
    user_id: str, lesson_id: str, step_id: str, code: str
) -> dict:
    """Submit an exercise answer (alias for complete_step)."""
    return await complete_step(user_id, lesson_id, step_id, code)


async def next_lesson(user_id: str, current_lesson_id: str) -> Optional[dict]:
    """Return the next recommended lesson."""
    progress = await get_progress(user_id)
    completed = set(
        k.split(":")[0]
        for k, v in progress.get("completed", {}).items()
        if not k.startswith("_")
    )
    for lesson in _LESSONS.values():
        if lesson["id"] not in completed:
            prereqs = lesson.get("prerequisites", [])
            if all(p in completed for p in prereqs):
                return lesson
    return None