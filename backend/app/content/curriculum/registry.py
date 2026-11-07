"""
Lesson registry — maps a lesson slug to its authored content dict.

The LessonService and lesson route are generic: they operate on whatever
lesson dict is looked up here by slug. Add a new foundation lesson by
authoring a content module and registering it below.
"""
from typing import Dict, Any, Optional, List

from app.content.curriculum.vertical_slice_variables import VERTICAL_SLICE
from app.content.curriculum.control_flow import CONTROL_FLOW_SLICE
from app.data.worlds_data import WORLD_REGISTRY

LESSON_REGISTRY: Dict[str, Dict[str, Any]] = {
    "variables_state": VERTICAL_SLICE,
    "control_flow": CONTROL_FLOW_SLICE,
}


def _world1_for_slug(slug: str) -> Optional[Dict[str, Any]]:
    for world in WORLD_REGISTRY.values():
        for town in world.towns:
            for lvl in town.levels:
                if lvl.id == slug:
                    return lvl.model_dump()
    return None


def _world2_for_slug(slug: str) -> Optional[Dict[str, Any]]:
    return _world1_for_slug(slug)


def get_lesson_dict(slug: str) -> Optional[Dict[str, Any]]:
    """Return the lesson content dict for a slug, or None if unknown."""
    lesson = LESSON_REGISTRY.get(slug)
    if lesson is not None:
        return lesson
    lesson = _world1_for_slug(slug)
    if lesson is not None:
        return lesson
    return _world2_for_slug(slug)


LESSON_SLUGS: List[str] = list(LESSON_REGISTRY.keys()) + sorted(
    lvl.id for w in WORLD_REGISTRY.values() for t in w.towns for lvl in t.levels
)
