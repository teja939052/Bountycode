"""
Lesson registry — maps a lesson slug to its authored content dict.

The LessonService and lesson route are generic: they operate on whatever
lesson dict is looked up here by slug. Add a new foundation lesson by
authoring a content module and registering it below.
"""
from __future__ import annotations

import importlib.util
import pkgutil
from pathlib import Path
from typing import Dict, Any, Optional, List

from app.content.curriculum.content_normalizer import normalize_lesson
from app.content.curriculum.vertical_slice_variables import VERTICAL_SLICE
from app.content.curriculum.control_flow import CONTROL_FLOW_SLICE
from app.content.curriculum.concept_loops import LOOP_SLICE
from app.content.curriculum.concept_arrays import ARRAY_SLICE
from app.content.curriculum.concept_strings import STRING_SLICE
from app.content.curriculum.concept_functions import FUNCTION_SLICE
from app.content.curriculum.concept_sorting import SORTING_SLICE
from app.content.curriculum.concept_complexity import COMPLEXITY_SLICE
from app.content.curriculum.concept_trie import TRIE_SLICE
from app.content.curriculum.concept_backtracking import BACKTRACK_SLICE
from app.content.curriculum.concept_segment_tree import SEGMENT_SLICE
from app.content.curriculum.concept_fenwick import FENWICK_SLICE
from app.content.curriculum.concept_heap import HEAP_SLICE
from app.content.curriculum.concept_graph import GRAPH_SLICE
from app.content.curriculum.concept_dp import DP_SLICE
from app.content.curriculum.world1_chapter1 import (
    PROGRAM_IO_SLICE, ASSIGNMENT_SLICE, TYPES_SLICE, EXPRESSIONS_SLICE, TRACE_MINI_SLICE,
)
from app.content.curriculum.flagship.trace_variables import LESSON as TRACE_VARIABLES_LESSON
from app.content.curriculum.flagship.percentages import LESSON as PERCENTAGES_LESSON
from app.content.curriculum.flagship.blood_relations import LESSON as BLOOD_RELATIONS_LESSON
from app.content.curriculum.flagship.email_format import LESSON as EMAIL_FORMAT_LESSON
from app.content.curriculum.flagship.binary_search import LESSON as BINARY_SEARCH_LESSON
from app.content.curriculum.flagship.valid_parentheses import LESSON as VALID_PARENTHESES_LESSON
from app.content.curriculum.flagship.two_sum import LESSON as TWO_SUM_LESSON
from app.content.curriculum.flagship.reverse_linked_list import LESSON as REVERSE_LINKED_LIST_LESSON
from app.content.curriculum.flagship.world2_wrappers import (
    get_two_pointers_lesson,
    get_sliding_window_lesson,
    get_hash_map_lesson,
    get_binary_search_lesson,
    get_prefix_sum_lesson,
    get_dfs_lesson,
    get_bfs_lesson,
    get_graph_traversal_lesson,
    get_topological_sort_lesson,
    get_memoization_lesson,
    get_tabulation_lesson,
)
from app.content.curriculum.flagship.world_wrappers import (
    get_all_world_lessons,
    get_world_lesson,
)

# ─── Phase B: Concept Clarity ────────────────────────────────────────
# The 13 coding-basics concepts that gate placement coding rounds. Two are
# pre-existing (variables_state, control_flow); the eleven authored slices
# below complete the set. Every slice implements the full teaching loop as
# the live vertical-slice contract that LessonService consumes.
LESSON_REGISTRY: Dict[str, Dict[str, Any]] = {
    "variables_state": normalize_lesson(VERTICAL_SLICE),
    "control_flow": normalize_lesson(CONTROL_FLOW_SLICE),
    "loops": normalize_lesson(LOOP_SLICE),
    "arrays": normalize_lesson(ARRAY_SLICE),
    "strings": normalize_lesson(STRING_SLICE),
    "functions": normalize_lesson(FUNCTION_SLICE),
    "sorting": normalize_lesson(SORTING_SLICE),
    "complexity": normalize_lesson(COMPLEXITY_SLICE),
    "program_io": normalize_lesson(PROGRAM_IO_SLICE),
    "assignment_boxes": normalize_lesson(ASSIGNMENT_SLICE),
    "types_values": normalize_lesson(TYPES_SLICE),
    "expressions_order": normalize_lesson(EXPRESSIONS_SLICE),
    "trace_mini": normalize_lesson(TRACE_MINI_SLICE),
    "trace_variables": normalize_lesson(TRACE_VARIABLES_LESSON),
    "percentages": normalize_lesson(PERCENTAGES_LESSON),
    "blood_relations": normalize_lesson(BLOOD_RELATIONS_LESSON),
    "email_format": normalize_lesson(EMAIL_FORMAT_LESSON),
    "binary_search": normalize_lesson(BINARY_SEARCH_LESSON),
    "valid_parentheses": normalize_lesson(VALID_PARENTHESES_LESSON),
    "two_sum": normalize_lesson(TWO_SUM_LESSON),
    "reverse_linked_list": normalize_lesson(REVERSE_LINKED_LIST_LESSON),
    "two_pointers": normalize_lesson(get_two_pointers_lesson()),
    "sliding_window": normalize_lesson(get_sliding_window_lesson()),
    "hash_map": normalize_lesson(get_hash_map_lesson()),
    "binary_search": normalize_lesson(get_binary_search_lesson()),
    "prefix_sum": normalize_lesson(get_prefix_sum_lesson()),
    "depth_first_search": normalize_lesson(get_dfs_lesson()),
    "breadth_first_search": normalize_lesson(get_bfs_lesson()),
    "graph_traversal": normalize_lesson(get_graph_traversal_lesson()),
    "topological_sort": normalize_lesson(get_topological_sort_lesson()),
    "memoization": normalize_lesson(get_memoization_lesson()),
    "tabulation": normalize_lesson(get_tabulation_lesson()),
    "trie": normalize_lesson(TRIE_SLICE),
    "backtracking": normalize_lesson(BACKTRACK_SLICE),
    "segment_tree": normalize_lesson(SEGMENT_SLICE),
    "fenwick_tree": normalize_lesson(FENWICK_SLICE),
    "heap": normalize_lesson(HEAP_SLICE),
    "graph": normalize_lesson(GRAPH_SLICE),
    "dynamic_programming": normalize_lesson(DP_SLICE),
}

# ─── Auto-discover generated curriculum modules ──────────────────────
_CURRICULUM_DIR = Path(__file__).resolve().parent
for _mod_path in _CURRICULUM_DIR.glob("*.py"):
    if _mod_path.name in {"__init__.py", "content_normalizer.py", "registry.py"} or _mod_path.name.startswith("_"):
        continue
    _raw_slug = _mod_path.stem
    _slug = _raw_slug.removeprefix("world1_")
    if _slug in LESSON_REGISTRY:
        continue
    try:
        _spec = importlib.util.spec_from_file_location(_raw_slug, _mod_path)
        if _spec is None or _spec.loader is None:
            continue
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        _lesson = getattr(_mod, "LESSON", None)
        if isinstance(_lesson, dict) and _lesson:
            LESSON_REGISTRY[_slug] = normalize_lesson(_lesson)
    except Exception:
        pass

# ─── Phase C: All World Lessons ─────────────────────────────────────
# Every level across all 13 worlds, converted to the full teaching loop.
_WORLD_LESSONS: Dict[str, Dict[str, Any]] = {
    slug: normalize_lesson(lesson) for slug, lesson in get_all_world_lessons().items()
}
LESSON_REGISTRY.update(_WORLD_LESSONS)

_WORLD_ID_NORMALIZE = {
    "code_foundations": "coding_foundations",
    "aptitude_world": "aptitude_gauntlet",
    "communication_world": "interview_arena",
    "cs_world": "cs_core",
    "company_world": "company_quests",
    "placement_world": "placement_readiness",
}

for _lesson in LESSON_REGISTRY.values():
    _wp = _lesson.get("world_progression") or {}
    _wid = _wp.get("world_id")
    if _wid in _WORLD_ID_NORMALIZE:
        _wp["world_id"] = _WORLD_ID_NORMALIZE[_wid]
        _lesson["world_progression"] = _wp


def concept_clarity_lessons() -> List[Dict[str, Any]]:
    """Return the full Phase B concept-clarity set in recommended order."""
    return [
        LESSON_REGISTRY["variables_state"],
        LESSON_REGISTRY["control_flow"],
        LESSON_REGISTRY["loops"],
        LESSON_REGISTRY["arrays"],
        LESSON_REGISTRY["strings"],
        LESSON_REGISTRY["functions"],
        LESSON_REGISTRY["sorting"],
        LESSON_REGISTRY["complexity"],
        LESSON_REGISTRY["program_io"],
        LESSON_REGISTRY["assignment_boxes"],
        LESSON_REGISTRY["types_values"],
        LESSON_REGISTRY["expressions_order"],
        LESSON_REGISTRY["trace_mini"],
    ]


def get_lesson_dict(slug: str) -> Optional[Dict[str, Any]]:
    """Return the canonicalized lesson content dict for a slug, or None if unknown."""
    lesson = LESSON_REGISTRY.get(slug)
    if lesson is None:
        lesson = get_world_lesson(slug)
        if lesson is not None:
            return normalize_lesson(lesson)
    return lesson


LESSON_SLUGS: List[str] = sorted(LESSON_REGISTRY.keys())

