"""Service-company sprint curriculum engine.

Source of truth: app/data/service_company_sprint.json

Used by Academy plan and Study "today" surfaces so learners follow one
ordered path: diagnose → foundations → quant → reasoning → verbal →
coding OA → CS floor → mocks — not a random pile of lessons.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Any, Dict, List, Optional, Set

_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SPRINT_PATH = os.path.join(_APP_DIR, "data", "service_company_sprint.json")

# Domain tags for adaptive weak-skill → lesson routing (keep in sync with skill_graph).
LESSON_DOMAIN: Dict[str, str] = {
    # programming
    "variables_basics": "programming_fundamentals",
    "conditions_basics": "programming_fundamentals",
    "loops_basics": "programming_fundamentals",
    "loops_code_lab": "programming_fundamentals",
    "functions_basics": "programming_fundamentals",
    "arrays_basics": "programming_fundamentals",
    "strings_basics": "programming_fundamentals",
    # quant
    "number_systems": "quantitative_aptitude",
    "number_system": "quantitative_aptitude",
    "percentages": "quantitative_aptitude",
    "successive_percentage_change": "quantitative_aptitude",
    "profit_loss": "quantitative_aptitude",
    "ratio_proportion": "quantitative_aptitude",
    "averages": "quantitative_aptitude",
    "time_work": "quantitative_aptitude",
    "time_distance": "quantitative_aptitude",
    "hcf_lcm": "quantitative_aptitude",
    "simple_compound_interest": "quantitative_aptitude",
    "pipes_cisterns": "quantitative_aptitude",
    "mixture_alligation": "quantitative_aptitude",
    "probability_basics": "quantitative_aptitude",
    "data_interpretation": "quantitative_aptitude",
    "arithmetic_algebra": "quantitative_aptitude",
    # reasoning
    "number_series": "logical_reasoning",
    "coding_decoding": "logical_reasoning",
    "blood_relations": "logical_reasoning",
    "direction_sense": "logical_reasoning",
    "syllogisms": "logical_reasoning",
    "analogies_odd_one_out": "logical_reasoning",
    "seating_arrangement": "logical_reasoning",
    "logical_puzzles": "logical_reasoning",
    "puzzles_basics": "logical_reasoning",
    "pattern_matching_basics": "logical_reasoning",
    "clocks_calendars": "logical_reasoning",
    # verbal
    "reading_comprehension": "verbal_ability",
    "error_spotting": "verbal_ability",
    "sentence_correction": "verbal_ability",
    "sentence_completion": "verbal_ability",
    "para_jumbles": "verbal_ability",
    "vocabulary_cloze": "verbal_ability",
    "grammar_transformations": "verbal_ability",
    # dsa / logic
    "pseudocode_trace": "arrays_hashing",
    "data_structures_intro": "arrays_hashing",
    "searching_basics": "arrays_hashing",
    "sorting_basics": "arrays_hashing",
    "hashing_basics": "arrays_hashing",
    "algorithms_basics": "arrays_hashing",
    "recursion_basics": "arrays_hashing",
    "searching_sorting": "arrays_hashing",
    # cs interview
    "dbms_basics": "cs_interview",
    "oops_basics": "cs_interview",
}

DOMAIN_ENTRY_LESSON = {
    "programming_fundamentals": "variables_basics",
    "arrays_hashing": "pseudocode_trace",
    "quantitative_aptitude": "percentages",
    "logical_reasoning": "number_series",
    "verbal_ability": "reading_comprehension",
    "cs_interview": "dbms_basics",
    "sql": "dbms_basics",
    "computer_science": "oops_basics",
}

LESSON_PATH = "/learn/lesson"  # canonical player route


@lru_cache(maxsize=1)
def load_sprint() -> Dict[str, Any]:
    with open(_SPRINT_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


def ordered_lessons() -> List[str]:
    """Flat ordered list of all curriculum lesson slugs."""
    data = load_sprint()
    out: List[str] = []
    for sprint in data.get("sprints") or []:
        for slug in sprint.get("lessons") or []:
            if slug not in out:
                out.append(slug)
    return out


def next_curriculum_lessons(
    mastered: Optional[Set[str]] = None,
    *,
    limit: int = 3,
) -> List[Dict[str, Any]]:
    """Return the next unmastered lessons in sprint order."""
    mastered = mastered or set()
    data = load_sprint()
    picks: List[Dict[str, Any]] = []
    for sprint in data.get("sprints") or []:
        for slug in sprint.get("lessons") or []:
            if slug in mastered:
                continue
            picks.append(
                {
                    "slug": slug,
                    "type": "next_mission",
                    "kind": "lesson",
                    "title": slug.replace("_", " ").title(),
                    "sprint_id": sprint.get("id"),
                    "sprint_name": sprint.get("name"),
                    "domain": LESSON_DOMAIN.get(slug, "programming_fundamentals"),
                    "to": f"{LESSON_PATH}/{slug}",
                    "estimated_minutes": 20,
                    "reason": f"Next step in {sprint.get('name')}: {sprint.get('goal')}",
                }
            )
            if len(picks) >= limit:
                return picks
    return picks


def daily_focus_plan(
    *,
    mastered: Optional[Set[str]] = None,
    weak_domains: Optional[List[str]] = None,
    reviews: Optional[List[Dict[str, Any]]] = None,
    mock_ready: bool = False,
) -> Dict[str, Any]:
    """Build today's ordered tasks using sprint daily_scrum policy."""
    data = load_sprint()
    policy = data.get("daily_scrum") or {}
    max_tasks = int(policy.get("max_focus_tasks") or 3)
    tasks: List[Dict[str, Any]] = []

    for domain in weak_domains or []:
        slug = DOMAIN_ENTRY_LESSON.get(domain)
        if not slug:
            continue
        tasks.append(
            {
                "slug": slug,
                "type": "practice",
                "kind": "weak_area",
                "title": f"Strengthen {domain.replace('_', ' ')}",
                "domain": domain,
                "to": f"{LESSON_PATH}/{slug}",
                "estimated_minutes": 15,
                "reason": "Recommended because this skill needs more evidence.",
            }
        )
        if len(tasks) >= max_tasks:
            break

    if len(tasks) < max_tasks:
        for lesson in next_curriculum_lessons(mastered, limit=max_tasks):
            if any(t.get("slug") == lesson["slug"] for t in tasks):
                continue
            tasks.append(lesson)
            if len(tasks) >= max_tasks:
                break

    for card in (reviews or [])[:2]:
        if len(tasks) >= max_tasks + 2:
            break
        tasks.append(
            {
                "type": "review",
                "kind": "srs",
                "title": card.get("title") or card.get("question") or "Review a concept",
                "estimated_minutes": 5,
                "reason": "Due for spaced repetition so you keep what you learned.",
                "to": "/academy",
            }
        )

    if mock_ready:
        tasks.append(
            {
                "type": "company_mission",
                "title": "Service-company mock",
                "estimated_minutes": 30,
                "reason": "Measure readiness under exam conditions.",
                "to": "/service-oa",
            }
        )

    return {
        "curriculum_id": data.get("id"),
        "title": data.get("title"),
        "mastery_threshold": data.get("mastery_threshold", 0.7),
        "hint_policy": (policy.get("hint_policy") or {}),
        "lesson_flow": policy.get("lesson_flow") or [],
        "tasks": tasks[: max_tasks + 2],
        "next": tasks[0] if tasks else None,
        "sprints": [
            {
                "id": s.get("id"),
                "name": s.get("name"),
                "goal": s.get("goal"),
                "lesson_count": len(s.get("lessons") or []),
            }
            for s in (data.get("sprints") or [])
        ],
        "ordered_lesson_count": len(ordered_lessons()),
    }


def lesson_for_domain(domain: str) -> Optional[str]:
    return DOMAIN_ENTRY_LESSON.get(domain)
