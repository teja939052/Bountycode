"""Closed-loop repair mission system.

When a student fails an assessment (mock OA, AI interview, or company stage),
this system creates targeted repair missions to address weaknesses.

Flow:
  assessment failed
       ↓
  weaknesses identified
       ↓
  repair mission created
       ↓
  targeted practice (exercises + lessons)
       ↓
  re-assessment
       ↓
  pass → advance | fail → deeper repair
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RepairMission(BaseModel):
    """A targeted mission to repair weaknesses."""
    id: str
    user_id: str
    title: str
    weaknesses: List[str] = Field(default_factory=list)
    recommended_lessons: List[str] = Field(default_factory=list)
    recommended_exercises: List[str] = Field(default_factory=list)
    recommended_quizzes: List[str] = Field(default_factory=list)
    status: str = "pending"  # pending, in_progress, completed
    created_at: str = ""
    completed_at: str = ""
    misconception_tag: Optional[str] = None
    remediation_steps: List[str] = Field(default_factory=list)
    interactive_drill: Dict[str, Any] = Field(default_factory=dict)


async def create_repair_mission(
    user_id: str,
    weaknesses: List[str],
    source: str = "assessment",
) -> RepairMission:
    """Create a repair mission targeting specific weaknesses.

    Args:
        user_id: The student
        weaknesses: List of skill IDs that need repair
        source: What triggered the repair (interview, mock_oa, quiz, etc.)

    Returns:
        A RepairMission with recommended activities
    """
    from datetime import datetime, timezone

    # Find lessons that teach these weaknesses
    recommended_lessons = _find_lessons_for_skills(weaknesses)

    # Find exercises that practice these weaknesses
    recommended_exercises = _find_exercises_for_skills(weaknesses)

    # Find quizzes that test these weaknesses
    recommended_quizzes = _find_quizzes_for_skills(weaknesses)

    mission = RepairMission(
        id=f"repair:{user_id}:{int(datetime.now(timezone.utc).timestamp())}",
        user_id=user_id,
        title=f"Repair: {', '.join(weaknesses[:3])}",
        weaknesses=weaknesses,
        recommended_lessons=recommended_lessons,
        recommended_exercises=recommended_exercises,
        recommended_quizzes=recommended_quizzes,
        created_at=datetime.now(timezone.utc).isoformat(),
    )

    # Store the mission
    try:
        from app.database import repair_missions_collection
        await repair_missions_collection().insert_one(mission.model_dump())
    except Exception:
        pass  # best-effort storage

    return mission


def _find_lessons_for_skills(skills: List[str]) -> List[str]:
    """Find lessons that teach the given skills."""
    from app.data.worlds_data import WORLD_REGISTRY
    lesson_ids = []
    for world in WORLD_REGISTRY.values():
        for town in world.towns:
            for lesson in town.lessons:
                if any(s in lesson.concept or s in lesson.canonical_skill for s in skills):
                    lesson_ids.append(lesson.id)
    return lesson_ids[:5]


def _find_exercises_for_skills(skills: List[str]) -> List[str]:
    """Find exercises that practice the given skills."""
    from app.content.role_content import ALL_EXERCISES
    exercise_ids = []
    for role_exercises in ALL_EXERCISES.values():
        for ex in role_exercises:
            if any(s in ex.skills_tested for s in skills):
                exercise_ids.append(ex.id)
    return exercise_ids[:5]


def _find_quizzes_for_skills(skills: List[str]) -> List[str]:
    """Find quizzes that test the given skills."""
    from app.content.role_content import ALL_QUIZZES
    quiz_ids = []
    for role_quizzes in ALL_QUIZZES.values():
        for quiz in role_quizzes:
            quiz_ids.append(quiz.id)
    return quiz_ids[:3]


async def get_active_repair_missions(user_id: str) -> List[RepairMission]:
    """Get active repair missions for a student."""
    try:
        from app.database import repair_missions_collection
        col = repair_missions_collection()
        missions = []
        async for doc in col.find({"user_id": user_id, "status": {"$ne": "completed"}}).limit(5):
            missions.append(RepairMission(**doc))
        return missions
    except Exception:
        return []


async def complete_repair_mission(user_id: str, mission_id: str) -> Dict[str, Any]:
    """Mark a repair mission as completed."""
    from datetime import datetime, timezone
    try:
        from app.database import repair_missions_collection
        col = repair_missions_collection()
        await col.update_one(
            {"user_id": user_id, "id": mission_id},
            {"$set": {"status": "completed", "completed_at": datetime.now(timezone.utc).isoformat()}},
        )
        return {"completed": True, "mission_id": mission_id}
    except Exception:
        return {"completed": False}


async def get_repair_recommendations(user_id: str) -> Dict[str, Any]:
    """Get repair recommendations based on recent failures."""
    missions = await get_active_repair_missions(user_id)
    if not missions:
        return {"has_repairs": False, "missions": []}

    return {
        "has_repairs": True,
        "missions": [m.model_dump() for m in missions],
        "total_weaknesses": len(set(w for m in missions for w in m.weaknesses)),
        "next_recommended": missions[0].model_dump() if missions else None,
    }


async def create_repair_mission_from_misconception(
    user_id: str,
    misconception_tag: str,
    repair_title: str,
    remediation_steps: List[str],
    interactive_drill: Dict[str, Any],
    source_question_id: Optional[str] = None,
) -> Optional[RepairMission]:
    """Create a repair mission from a tagged MCQ misconception.

    Args:
        user_id: The student
        misconception_tag: The misconception class (e.g. "units_conversion_error")
        repair_title: Human-readable title for the repair mission
        remediation_steps: Step-by-step remediation guide
        interactive_drill: Diagnostic drill config for retest
        source_question_id: Optional originating question

    Returns:
        RepairMission if created, None if already exists or storage fails
    """
    from datetime import datetime, timezone

    try:
        from app.database import user_weaknesses_collection, repair_missions_collection

        # Record the weakness trigger
        await user_weaknesses_collection.update_one(
            {"user_id": user_id, "misconception_tag": misconception_tag},
            {
                "$inc": {"trigger_count": 1},
                "$set": {"last_triggered": datetime.now(timezone.utc).isoformat(), "status": "remediation_queued"},
                "$setOnInsert": {"user_id": user_id, "misconception_tag": misconception_tag},
            },
            upsert=True,
        )

        # Check if an active repair mission already exists for this tag
        existing = await repair_missions_collection.find_one(
            {"user_id": user_id, "misconception_tag": misconception_tag, "status": {"$ne": "completed"}}
        )
        if existing:
            return None

        mission = RepairMission(
            id=f"repair:{user_id}:{misconception_tag}:{int(datetime.now(timezone.utc).timestamp())}",
            user_id=user_id,
            title=repair_title,
            weaknesses=[misconception_tag],
            misconception_tag=misconception_tag,
            remediation_steps=remediation_steps,
            interactive_drill=interactive_drill,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        await repair_missions_collection.insert_one(mission.model_dump())
        return mission
    except Exception:
        return None
