"""Master registry — all 12 BountyCode worlds.

This is the single source of truth for the game's content. The Study Engine
and Journey State both pull from here.

To add a new world: create its content file, import it here, and add it to
ALL_WORLDS. No engineering changes needed — the engine reads this registry.
"""
from __future__ import annotations

from typing import Dict

from app.content.lesson_definitions import WorldDefinition, LessonDefinition
from app.content.world1_foundations import WORLD_1_FOUNDATIONS
from app.content.world2_problem_solver import WORLD_2_PROBLEM_SOLVER
from app.content.worlds_3_to_6 import WORLD_3_BUILD_SYSTEMS, WORLD_4_WORK_WITH_DATA, WORLD_5_SOFTWARE_ENGINEERING, WORLD_6_UNDER_PRESSURE
from app.content.worlds_7_to_9 import WORLD_7_HIRING_ARENA, WORLD_8_COMPANY_MISSIONS, WORLD_9_AI_ENGINEERING
from app.content.worlds_10_to_12 import WORLD_10_PRODUCTION, WORLD_11_PROJECTS, WORLD_12_CREATIVE

# ─── World registry ────────────────────────────────────────────────
# Order matters — worlds are presented to students in this order.

ALL_WORLDS: Dict[str, WorldDefinition] = {
    WORLD_1_FOUNDATIONS.id: WORLD_1_FOUNDATIONS,
    WORLD_2_PROBLEM_SOLVER.id: WORLD_2_PROBLEM_SOLVER,
    WORLD_3_BUILD_SYSTEMS.id: WORLD_3_BUILD_SYSTEMS,
    WORLD_4_WORK_WITH_DATA.id: WORLD_4_WORK_WITH_DATA,
    WORLD_5_SOFTWARE_ENGINEERING.id: WORLD_5_SOFTWARE_ENGINEERING,
    WORLD_6_UNDER_PRESSURE.id: WORLD_6_UNDER_PRESSURE,
    WORLD_7_HIRING_ARENA.id: WORLD_7_HIRING_ARENA,
    WORLD_8_COMPANY_MISSIONS.id: WORLD_8_COMPANY_MISSIONS,
    WORLD_9_AI_ENGINEERING.id: WORLD_9_AI_ENGINEERING,
    WORLD_10_PRODUCTION.id: WORLD_10_PRODUCTION,
    WORLD_11_PROJECTS.id: WORLD_11_PROJECTS,
    WORLD_12_CREATIVE.id: WORLD_12_CREATIVE,
}


def get_world(world_id: str) -> WorldDefinition | None:
    """Return a world by id, or None if not found."""
    return ALL_WORLDS.get(world_id)


def all_lessons() -> list[LessonDefinition]:
    """Flat list of every lesson across all worlds."""
    lessons: list[LessonDefinition] = []
    for world in ALL_WORLDS.values():
        for town in world.towns:
            lessons.extend(town.lessons)
    return lessons


def get_lesson(world_id: str, lesson_id: str) -> LessonDefinition | None:
    """Return a specific lesson by world + lesson id."""
    world = ALL_WORLDS.get(world_id)
    if not world:
        return None
    for town in world.towns:
        for lesson in town.lessons:
            if lesson.id == lesson_id:
                return lesson
    return None


def get_lesson_by_id(lesson_id: str) -> LessonDefinition | None:
    """Return a lesson by id across all worlds."""
    for world in ALL_WORLDS.values():
        for town in world.towns:
            for lesson in town.lessons:
                if lesson.id == lesson_id:
                    return lesson
    return None


def total_lesson_count() -> int:
    """Total lessons across all worlds."""
    return sum(
        len(town.lessons)
        for world in ALL_WORLDS.values()
        for town in world.towns
    )


def world_count() -> int:
    return len(ALL_WORLDS)
