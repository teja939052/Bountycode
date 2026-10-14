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

import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, model_validator

logger = logging.getLogger(__name__)


class RepairMission(BaseModel):
    """A targeted mission to repair weaknesses."""
    id: str
    user_id: str
    title: str
    weaknesses: List[str] = Field(default_factory=list)
    recommended_lessons: List[str] = Field(default_factory=list)
    recommended_exercises: List[str] = Field(default_factory=list)
    recommended_quizzes: List[str] = Field(default_factory=list)
    status: str = "pending"  # pending, in_progress, completed, verified_complete
    created_at: str = ""
    completed_at: str = ""
    misconception_tag: Optional[str] = None
    remediation_steps: List[str] = Field(default_factory=list)
    interactive_drill: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def _coerce_interactive_drill(cls, data: Any) -> Any:
        if isinstance(data, dict):
            drill = data.get("interactive_drill")
            if isinstance(drill, list):
                data = dict(data)
                data["interactive_drill"] = {}
        return data
    attempt_count: int = 0
    best_score: float = 0.0
    retest_history: List[dict] = Field(default_factory=list)


class RepairEvent(BaseModel):
    """Immutable evidence record for a repair action."""
    id: str
    user_id: str
    mission_id: Optional[str] = None
    event_type: str = ""  # mission_created, mission_completed, retest_passed, retest_failed
    skill: str = ""
    source: str = ""  # world, scrimba, mock_oa, interview, aptitude, repair_retest
    recommended_lessons: List[str] = Field(default_factory=list)
    recommended_exercises: List[str] = Field(default_factory=list)
    recommended_quizzes: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: str = ""


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

    weaknesses = [w for w in weaknesses if w]
    if not weaknesses:
        raise ValueError("weaknesses must not be empty")

    # Dedup: if an active mission already covers the primary weakness, reuse it.
    primary = weaknesses[0]
    try:
        from app.database import repair_missions_collection
        existing = await repair_missions_collection().find_one(
            {"user_id": user_id, "weaknesses": {"$in": [primary]}, "status": {"$ne": "completed"}}
        )
        if existing:
            return RepairMission(**existing)
    except Exception:
        pass

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
        logger.info("repair mission inserted for %s id=%s", user_id, mission.id)
    except Exception as exc:
        logger.warning("repair mission insert failed for %s: %s", user_id, exc)

    # Emit immutable repair event evidence
    try:
        await write_repair_event(
            user_id=user_id,
            mission_id=mission.id,
            event_type="mission_created",
            skill=primary,
            source=source,
            recommended_lessons=recommended_lessons,
            recommended_exercises=recommended_exercises,
            recommended_quizzes=recommended_quizzes,
            metadata={"weakness_count": len(weaknesses), "title": mission.title},
        )
    except Exception:
        pass

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
    except Exception as exc:
        logger.warning("get_active_repair_missions failed for %s: %s", user_id, exc)
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

        # Emit completion event
        try:
            mission = await col.find_one({"id": mission_id})
            if mission:
                await write_repair_event(
                    user_id=user_id,
                    mission_id=mission_id,
                    event_type="mission_completed",
                    skill=(mission.get("weaknesses") or [""])[0],
                    source="repair",
                    metadata={"title": mission.get("title", "")},
                )
        except Exception:
            pass

        return {"completed": True, "mission_id": mission_id}
    except Exception:
        return {"completed": False}


async def record_retest_attempt(
    user_id: str,
    mission_id: str,
    skill: str,
    score: float,
    passed: bool,
    source: str = "repair_retest",
) -> Dict[str, Any]:
    """Record a retest attempt for a repair mission.
    
    Mastery gate: mission only closes when retest passes (score >= 80).
    Tracks attempt_count, best_score, and retest_history.
    """
    from datetime import datetime, timezone
    try:
        from app.database import repair_missions_collection
        col = repair_missions_collection()
        mission = await col.find_one({"user_id": user_id, "id": mission_id})
        if not mission:
            return {"recorded": False, "reason": "mission_not_found"}

        attempt_count = int(mission.get("attempt_count", 0)) + 1
        best_score = max(float(mission.get("best_score", 0)), float(score))
        retest_history = list(mission.get("retest_history", []) or [])
        retest_history.append({
            "attempt": attempt_count,
            "score": float(score),
            "passed": bool(passed),
            "skill": skill,
            "source": source,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        # Mastery gate: only advance if passed
        if passed:
            await col.update_one(
                {"user_id": user_id, "id": mission_id},
                {"$set": {
                    "status": "verified_complete",
                    "completed_at": datetime.now(timezone.utc).isoformat(),
                    "attempt_count": attempt_count,
                    "best_score": best_score,
                    "retest_history": retest_history,
                }},
            )
        else:
            await col.update_one(
                {"user_id": user_id, "id": mission_id},
                {"$set": {
                    "status": "in_progress",
                    "attempt_count": attempt_count,
                    "best_score": best_score,
                    "retest_history": retest_history,
                }},
            )

        # Emit retest event
        try:
            await write_repair_event(
                user_id=user_id,
                mission_id=mission_id,
                event_type="retest_passed" if passed else "retest_failed",
                skill=skill,
                source=source,
                metadata={
                    "attempt": attempt_count,
                    "score": float(score),
                    "passed": passed,
                },
            )
        except Exception:
            pass

        return {
            "recorded": True,
            "passed": passed,
            "attempt_count": attempt_count,
            "best_score": best_score,
            "status": "verified_complete" if passed else "in_progress",
        }
    except Exception:
        return {"recorded": False}


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


async def write_repair_event(
    user_id: str,
    event_type: str,
    skill: str = "",
    source: str = "",
    mission_id: Optional[str] = None,
    recommended_lessons: Optional[List[str]] = None,
    recommended_exercises: Optional[List[str]] = None,
    recommended_quizzes: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Optional[RepairEvent]:
    """Write an immutable repair evidence event."""
    from datetime import datetime, timezone

    try:
        from app.database import repair_events_collection
        event = RepairEvent(
            id=f"revent:{user_id}:{int(datetime.now(timezone.utc).timestamp())}",
            user_id=user_id,
            mission_id=mission_id,
            event_type=event_type,
            skill=skill,
            source=source,
            recommended_lessons=recommended_lessons or [],
            recommended_exercises=recommended_exercises or [],
            recommended_quizzes=recommended_quizzes or [],
            metadata=metadata or {},
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        await repair_events_collection().insert_one(event.model_dump())
        return event
    except Exception:
        return None


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

        await repair_missions_collection().insert_one(mission.model_dump())

        try:
            await write_repair_event(
                user_id=user_id,
                mission_id=mission.id,
                event_type="mission_created",
                skill=misconception_tag,
                source="misconception",
                metadata={"repair_title": repair_title, "source_question_id": source_question_id},
            )
        except Exception:
            pass

        return mission
    except Exception:
        return None
