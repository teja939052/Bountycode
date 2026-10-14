"""Identity fallbacks for lessons that ship without a canonical skill.

Two stable keys already exist on every lesson dict:

    srs_concept_tag   "programming_fundamentals:variables"   semantic, preferred
    slug              "variables_state"                      registry key only

Neither is a canonical skill id, so both are translated here before the
resolver runs. Kept as its own module so the tables stay reviewable alone.
"""
from typing import Any, Dict, Optional

#: lesson slug -> canonical skill id
SLUG_SKILL: Dict[str, str] = {
    "variables_state": "code.variables",
    "types_values": "code.variables",
    "assignment_boxes": "code.variables",
    "control_flow": "code.conditions",
    "expressions_order": "code.operators",
    "loops": "code.loops",
    "arrays": "code.arrays",
    "strings": "code.strings",
    "functions": "code.functions",
    "sorting": "code.sorting",
    "complexity": "code.complexity",
    "program_io": "code.input_output",
    "trace_mini": "code.prediction",
}

#: lesson srs_concept_tag -> canonical skill id (authoritative when present)
SRS_SKILL: Dict[str, str] = {
    "programming_fundamentals:variables": "code.variables",
    "programming_fundamentals:assignment": "code.variables",
    "programming_fundamentals:types": "code.variables",
    "programming_fundamentals:control_flow": "code.conditions",
    "programming_fundamentals:expressions": "code.operators",
    "programming_fundamentals:loops": "code.loops",
    "programming_fundamentals:arrays": "code.arrays",
    "programming_fundamentals:strings": "code.strings",
    "programming_fundamentals:functions": "code.functions",
    "programming_fundamentals:sorting": "code.sorting",
    "programming_fundamentals:complexity": "code.complexity",
    "programming_fundamentals:input_output": "code.input_output",
    "programming_fundamentals:chapter1_trace": "code.prediction",
}


def skill_for_slug(slug: Optional[str]) -> str:
    """Resolve a lesson slug to a canonical skill id, or '' if unknown."""
    if not slug:
        return ""
    key = slug.strip().lower()
    if key in SLUG_SKILL:
        return SLUG_SKILL[key]
    # routes/lesson.py backfill entries look like "world_id::concept"
    return SLUG_SKILL.get(key.split("::")[-1], "")


def skill_for_lesson(lesson: Dict[str, Any], slug: Optional[str] = None) -> str:
    """Best-effort canonical skill for a raw lesson dict.

    Preference: an already-canonical value > srs_concept_tag > slug.
    """
    raw = lesson.get("canonical_skill")
    if isinstance(raw, str) and "." in raw:
        return raw
    if isinstance(lesson.get("skills"), list) and lesson["skills"]:
        first = lesson["skills"][0]
        if isinstance(first, str) and "." in first:
            return first
    srs = lesson.get("srs_concept_tag")
    if isinstance(srs, str):
        if srs in SRS_SKILL:
            return SRS_SKILL[srs]
        # already dot-qualified and canonical: backend.rest, sd.tradeoffs, …
        if "." in srs:
            return srs
    return skill_for_slug(slug or lesson.get("slug", ""))
