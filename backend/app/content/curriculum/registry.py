"""
Lesson registry — maps a lesson slug to its authored content dict.

The LessonService and lesson route are generic: they operate on whatever
lesson dict is looked up here by slug. Add a new foundation lesson by
authoring a content module and registering it below.
"""
from typing import Dict, Any, Optional, List

from app.content.curriculum.vertical_slice_variables import VERTICAL_SLICE
from app.content.curriculum.control_flow import CONTROL_FLOW_SLICE

LESSON_REGISTRY: Dict[str, Dict[str, Any]] = {
    "variables_state": VERTICAL_SLICE,
    "control_flow": CONTROL_FLOW_SLICE,
}

LESSON_SLUGS: List[str] = list(LESSON_REGISTRY.keys())


def get_lesson_dict(slug: str) -> Optional[Dict[str, Any]]:
    """Return the lesson content dict for a slug, or None if unknown."""
    return LESSON_REGISTRY.get(slug)
