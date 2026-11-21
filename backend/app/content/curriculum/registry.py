"""
Lesson registry — maps a lesson slug to its authored content dict.

The LessonService and lesson route are generic: they operate on whatever
lesson dict is looked up here by slug. Add a new foundation lesson by
authoring a content module and registering it below.
"""
from typing import Dict, Any, Optional, List

from app.content.curriculum.vertical_slice_variables import VERTICAL_SLICE
from app.content.curriculum.control_flow import CONTROL_FLOW_SLICE
from app.content.curriculum.quant_percentages import PERCENTAGES_LESSON
from app.content.curriculum.quant_ratio_proportion import RATIO_PROPORTION_LESSON
from app.content.curriculum.quant_averages import AVERAGES_LESSON
from app.content.curriculum.quant_time_work import TIME_WORK_LESSON
from app.content.curriculum.quant_number_systems import NUMBER_SYSTEMS_LESSON
from app.content.curriculum.logical_series import LOGICAL_SERIES_LESSON
from app.content.curriculum.logical_blood_relations import BLOOD_RELATIONS_LESSON
from app.content.curriculum.logical_coding_decoding import CODING_DECODING_LESSON
from app.content.curriculum.verbal_reading_comprehension import READING_COMPREHENSION_LESSON
from app.content.curriculum.cs_sql_basics import SQL_BASICS_LESSON
from app.content.curriculum.cs_oop_basics import OOP_BASICS_LESSON
from app.content.curriculum.cs_debugging import DEBUGGING_LESSON
from app.content.curriculum.dsa_arrays_strings import ARRAYS_STRINGS_LESSON
from app.content.curriculum.cs_git_testing import GIT_TESTING_LESSON
from app.content.curriculum.cs_http_api import HTTP_API_LESSON
from app.content.curriculum.python_loops import PYTHON_LOOPS_LESSON
from app.data.worlds_data import WORLD_REGISTRY

LESSON_REGISTRY: Dict[str, Dict[str, Any]] = {
    "variables_state": VERTICAL_SLICE,
    "control_flow": CONTROL_FLOW_SLICE,
    # Quant aptitude (service-company foundation)
    "quant_percentages": PERCENTAGES_LESSON,
    "quant_ratio_proportion": RATIO_PROPORTION_LESSON,
    "quant_averages": AVERAGES_LESSON,
    "quant_time_work": TIME_WORK_LESSON,
    "quant_number_systems": NUMBER_SYSTEMS_LESSON,
    # Logical reasoning
    "logical_series": LOGICAL_SERIES_LESSON,
    "logical_blood_relations": BLOOD_RELATIONS_LESSON,
    "logical_coding_decoding": CODING_DECODING_LESSON,
    # Verbal ability
    "verbal_reading_comprehension": READING_COMPREHENSION_LESSON,
    # Computer science / technical
    "cs_sql_basics": SQL_BASICS_LESSON,
    "cs_oop_basics": OOP_BASICS_LESSON,
    "cs_debugging": DEBUGGING_LESSON,
    "dsa_arrays_strings": ARRAYS_STRINGS_LESSON,
    "cs_git_testing": GIT_TESTING_LESSON,
    "cs_http_api": HTTP_API_LESSON,
    "python_loops": PYTHON_LOOPS_LESSON,
    # Sprint-compatible aliases (service_company_sprint.json references these slugs)
    "number_systems": NUMBER_SYSTEMS_LESSON,
    "ratio_proportion": RATIO_PROPORTION_LESSON,
    "averages": AVERAGES_LESSON,
    "time_work": TIME_WORK_LESSON,
    "number_series": LOGICAL_SERIES_LESSON,
    "coding_decoding": CODING_DECODING_LESSON,
    "blood_relations": BLOOD_RELATIONS_LESSON,
    "reading_comprehension": READING_COMPREHENSION_LESSON,
    "data_structures_intro": ARRAYS_STRINGS_LESSON,
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
