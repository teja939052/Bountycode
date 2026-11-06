"""
Company-prep lessons — simple step-based lessons for TCS NQT, Infosys, Wipro, etc.

Routes (all under /api/v1/company-lessons, auth required):
  GET  /api/v1/company-lessons               → list all available lessons
  GET  /api/v1/company-lessons/{slug}        → full lesson content
  POST /api/v1/company-lessons/{slug}/complete → record completion + rewards
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import os
import json
import logging

from app.middleware.auth import get_current_user
from app.services.gamification import record_practice
from app.services.learning_paths import record_track_topic_mastery
from app.services.adaptive_learning import record_learning_activity

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/company-lessons", tags=["company-lessons"])

_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LESSONS_DIR = os.path.join(_APP_DIR, "data", "lessons")

# In-memory cache so we don't hit disk on every request.
_LESSON_CACHE: Dict[str, Dict[str, Any]] = {}

# A guided lesson can only certify a module whose authored topic overlaps the
# skill it teaches. Query-string IDs from the browser are not proof of coverage.
LESSON_MODULE_TOPICS = {
    "arrays_basics": {"arrays", "array", "basic_arrays"},
    "blood_relations": {"blood_relation", "blood_relations"},
    "flowchart_basics": {"flowchart", "flowcharts", "flowchart_basics", "pseudocode"},
    "reading_comprehension": {"reading_comprehension", "reading"},
    "successive_percentage_change": {"percentages", "successive_percentage_change"},
    "profit_loss": {"profit_loss"},
    "ratio_proportion": {"ratio_proportion", "ratio"},
    "averages": {"averages", "average"},
    "time_work": {"time_work", "advanced_time_work"},
    "time_distance": {"time_distance", "speed_time_distance"},
    "probability_basics": {"probability", "advanced_probability"},
    "permutations_combinations": {"permutations", "permutation", "permutations_combinations"},
    "number_series": {"series", "number_series"},
    "coding_decoding": {"coding_decoding"},
    "sentence_correction": {"sentence_correction", "grammar", "error_spotting"},
    "para_jumbles": {"para_jumbles", "sentence_rearrangement"},
    "loops_basics": {"loops", "conditions"},
    "strings_basics": {"strings"},
    "recursion_basics": {"recursion"},
    "sorting_basics": {"sorting"},
    "searching_basics": {"searching"},
    "hashing_basics": {"hashing", "hashmaps"},
    "sql_select_basics": {"sql", "basic_sql", "select"},
    "sql_joins": {"joins"},
    "oops_basics": {"oop"},
    "dbms_basics": {"normalization"},
    "os_basics": {"operating_systems", "os"},
    "computer_networks_basics": {"computer_networks", "networking"},
    "number_systems": {"number_system", "number_systems", "number_theory"},
    "hcf_lcm": {"hcf_lcm", "hcf", "lcm"},
    "simple_compound_interest": {"simple_compound_interest", "simple_interest", "compound_interest", "interest"},
    "mixture_alligation": {"mixture_alligation", "mixtures", "alligation", "advanced_mixtures"},
    "syllogisms": {"syllogisms"},
    "direction_sense": {"direction_sense", "directions"},
    "logical_puzzles": {"puzzles", "arrangements", "seating_arrangement", "venn_diagrams", "number_analogies", "odd_one_out", "word_relationships", "critical_reasoning"},
    "clocks_calendars": {"clocks", "calendars", "clock_calendar"},
    "linked_lists": {"linked_list", "linked_lists"},
    "trees_basics": {"trees", "binary_trees", "bst"},
    "stacks_queues": {"stack", "stacks", "queue", "queues", "stacks_queues"},
    "dynamic_programming": {"dynamic_programming", "dynamic_programming_basics", "dp", "basic_dp"},
    "exception_handling": {"exception_handling", "exceptions"},
    "file_io": {"file_io", "files"},
    "time_complexity": {"time_complexity", "complexity_analysis", "big_o"},
    "sql_subqueries": {"subqueries", "exists", "not_exists", "in", "any_all"},
    "sql_group_by": {"group_by", "having", "aggregation"},
    "matrix_operations": {"matrices", "matrix", "matrix_operations"},
    "pipes_cisterns": {"pipes_cisterns"},
    "analogies_odd_one_out": {"number_analogies", "odd_one_out", "word_relationships", "word_analogy"},
    "grammar_transformations": {"active_passive_voice", "direct_indirect_speech"},
    "error_spotting": {"error_spotting"},
    "vocabulary_cloze": {"cloze_test", "fill_in_blanks", "synonyms_antonyms", "vocabulary", "one_word_substitution"},
    "programming_languages": {"java_python_basics", "c_java_python_basics"},
    "collections_framework": {"collections"},
    "pattern_printing": {"pattern_printing"},
    "pattern_matching_basics": {"pattern_matching", "basic_pattern_matching", "pattern_recognition"},
    "sql_indexes_triggers": {"indexing", "triggers"},
    "algorithms_basics": {"basic_algorithms", "mathematical", "math"},
    "arithmetic_algebra": {"arithmetic", "algebra", "math"},
    "geometry_basics": {"geometry"},
    "data_structures_intro": {"basic_ds"},
    "essay_writing": {"technology_topics", "current_affairs", "opinion_essays", "technology", "business", "social_issues", "essay"},
    "advanced_probability": {"advanced_probability"},
    "advanced_time_work": {"advanced_time_work"},
}


LESSON_SKILL_DOMAINS = {
    "successive_percentage_change": "quantitative_aptitude",
    "profit_loss": "quantitative_aptitude",
    "ratio_proportion": "quantitative_aptitude",
    "averages": "quantitative_aptitude",
    "time_work": "quantitative_aptitude",
    "time_distance": "quantitative_aptitude",
    "probability_basics": "quantitative_aptitude",
    "permutations_combinations": "quantitative_aptitude",
    "number_series": "logical_reasoning",
    "coding_decoding": "logical_reasoning",
    "blood_relations": "logical_reasoning",
    "flowchart_basics": "logical_reasoning",
    "reading_comprehension": "verbal_ability",
    "sentence_correction": "verbal_ability",
    "para_jumbles": "verbal_ability",
    "arrays_basics": "arrays_hashing",
    "loops_basics": "programming_fundamentals",
    "strings_basics": "programming_fundamentals",
    "recursion_basics": "programming_fundamentals",
    "sorting_basics": "programming_fundamentals",
    "searching_basics": "programming_fundamentals",
    "hashing_basics": "arrays_hashing",
    "sql_select_basics": "sql",
    "sql_joins": "sql",
    "oops_basics": "computer_science",
    "dbms_basics": "computer_science",
    "os_basics": "computer_science",
    "computer_networks_basics": "computer_science",
    "number_systems": "quantitative_aptitude",
    "hcf_lcm": "quantitative_aptitude",
    "simple_compound_interest": "quantitative_aptitude",
    "mixture_alligation": "quantitative_aptitude",
    "syllogisms": "logical_reasoning",
    "direction_sense": "logical_reasoning",
    "logical_puzzles": "logical_reasoning",
    "clocks_calendars": "quantitative_aptitude",
    "linked_lists": "arrays_hashing",
    "trees_basics": "trees",
    "stacks_queues": "stack",
    "dynamic_programming": "dp",
    "exception_handling": "programming_fundamentals",
    "file_io": "programming_fundamentals",
    "time_complexity": "programming_fundamentals",
    "sql_subqueries": "sql",
    "sql_group_by": "sql",
    "matrix_operations": "programming_fundamentals",
    "pipes_cisterns": "quantitative_aptitude",
    "analogies_odd_one_out": "logical_reasoning",
    "grammar_transformations": "verbal_ability",
    "error_spotting": "verbal_ability",
    "vocabulary_cloze": "verbal_ability",
    "programming_languages": "programming_fundamentals",
    "collections_framework": "programming_fundamentals",
    "pattern_printing": "programming_fundamentals",
    "pattern_matching_basics": "programming_fundamentals",
    "sql_indexes_triggers": "sql",
    "algorithms_basics": "programming_fundamentals",
    "arithmetic_algebra": "quantitative_aptitude",
    "geometry_basics": "quantitative_aptitude",
    "data_structures_intro": "arrays_hashing",
    "essay_writing": "verbal_ability",
    "advanced_probability": "quantitative_aptitude",
    "advanced_time_work": "quantitative_aptitude",
    "logical_puzzles": "logical_reasoning",
    "clocks_calendars": "quantitative_aptitude",
    "linked_lists": "linked_list",
    "trees_basics": "trees",
    "stacks_queues": "stack",
    "dynamic_programming": "dp",
    "sql_subqueries": "sql",
    "sql_group_by": "sql",
    "pipes_cisterns": "quantitative_aptitude",
    "analogies_odd_one_out": "logical_reasoning",
    "grammar_transformations": "verbal_ability",
    "vocabulary_cloze": "verbal_ability",
    "programming_languages": "programming_fundamentals",
    "collections_framework": "programming_fundamentals",
    "pattern_printing": "programming_fundamentals",
    "pattern_matching_basics": "programming_fundamentals",
    "sql_indexes_triggers": "sql",
    "algorithms_basics": "programming_fundamentals",
    "arithmetic_algebra": "quantitative_aptitude",
    "geometry_basics": "quantitative_aptitude",
    "data_structures_intro": "arrays_hashing",
    "essay_writing": "verbal_ability",
}


def _normalize_topic(value: Any) -> str:
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def _load_lesson(slug: str) -> Optional[Dict[str, Any]]:
    if slug in _LESSON_CACHE:
        return _LESSON_CACHE[slug]
    path = os.path.join(_LESSONS_DIR, f"{slug}.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        _LESSON_CACHE[slug] = data
        return data
    except Exception as exc:
        logger.warning("Failed to load lesson %s: %s", slug, exc)
        return None


class StepAnswerRequest(BaseModel):
    answer_index: int = Field(..., ge=0)


class CompleteRequest(BaseModel):
    # The server grades these assessment choices against the authored answer
    # key. A browser-supplied score is never trusted for completion or XP.
    answers: Dict[str, int] = Field(default_factory=dict)
    time_spent_seconds: int = Field(default=0, ge=0)
    track_id: Optional[str] = None
    module_id: Optional[str] = None
    topic_id: Optional[str] = None


@router.get("", response_model=None)
async def list_lessons(user=Depends(get_current_user)):
    """Return metadata for all available company-prep lessons."""
    lessons: List[Dict[str, Any]] = []
    if os.path.isdir(_LESSONS_DIR):
        for fname in sorted(os.listdir(_LESSONS_DIR)):
            if not fname.endswith(".json"):
                continue
            slug = fname[:-5]
            data = _load_lesson(slug)
            if not data or not data.get("steps") or not (data.get("assessment") or {}).get("questions"):
                # Legacy pattern snapshots without the step-based lesson schema
                # belong to the pattern curriculum, not this lesson player.
                continue
            lessons.append({
                "id": data.get("id") or slug,
                "slug": slug,
                "title": data.get("title") or slug,
                "domain": data.get("domain") or data.get("pattern") or "General",
                "difficulty": data.get("difficulty") or "medium",
                "duration_min": data.get("duration_min") or data.get("estimated_minutes") or 15,
                "step_count": len(data.get("steps") or []),
            })
    return {"success": True, "data": lessons}


@router.get("/{slug}", response_model=None)
async def get_lesson(slug: str, user=Depends(get_current_user)):
    data = _load_lesson(slug)
    if data is None or not data.get("steps") or not (data.get("assessment") or {}).get("questions"):
        raise HTTPException(status_code=404, detail=f"Step-based lesson not found: {slug}")

    # Do not send final-assessment answer keys to the browser. The server grades
    # them in /complete and only returns explanations after submission.
    public_data = {**data}
    # Never ship answer keys to the learner before they submit an attempt.
    public_data["steps"] = [
        {
            key: value for key, value in step.items()
            if key not in (
                {"correct_index", "correct_answer", "answer", "explanation"}
                if step.get("step_type") in {"interactive", "practice", "quiz"}
                else {"correct_index", "correct_answer", "answer"}
            )
        }
        for step in data.get("steps", [])
    ]
    assessment = {**(data.get("assessment") or {})}
    assessment["questions"] = [
        {
            key: value for key, value in question.items()
            if key not in {"correct_index", "correct_answer", "answer", "explanation"}
        }
        for question in assessment.get("questions", [])
    ]
    public_data["assessment"] = assessment
    return {"success": True, "data": public_data}


@router.post("/{slug}/steps/{step_index}/answer", response_model=None)
async def answer_lesson_step(
    slug: str,
    step_index: int,
    req: StepAnswerRequest,
    user=Depends(get_current_user),
):
    """Grade one interactive lesson step without exposing its answer key."""
    data = _load_lesson(slug)
    steps = (data or {}).get("steps") or []
    if not data or step_index < 0 or step_index >= len(steps):
        raise HTTPException(status_code=404, detail="Lesson step not found")

    step = steps[step_index]
    options = step.get("options") or []
    expected = step.get("correct_index")
    if step.get("step_type") not in {"interactive", "practice", "quiz"} or expected is None:
        raise HTTPException(status_code=400, detail="This lesson step is not answerable.")
    if req.answer_index >= len(options):
        raise HTTPException(status_code=422, detail="Selected answer is outside the available options.")

    correct = req.answer_index == int(expected)
    domain = str(data.get("domain") or data.get("pattern") or "general").lower()
    domain_id = LESSON_SKILL_DOMAINS.get(
        slug,
        {
            "quantitative aptitude": "quantitative_aptitude",
            "reasoning": "logical_reasoning",
            "programming logic": "programming_fundamentals",
            "programming fundamentals": "programming_fundamentals",
            "dsa": "arrays_hashing",
            "verbal ability": "verbal_ability",
            "sql": "sql",
        }.get(domain, domain.replace(" ", "_")),
    )

    # Record evidence, but do not mint XP for every retryable in-lesson choice.
    try:
        await record_learning_activity(
            user["id"],
            {
                "domain_id": domain_id,
                "type": "lesson_step",
                "success": correct,
                "score_impact": 1,
                "lesson_slug": slug,
                "step_index": step_index,
            },
        )
    except Exception as exc:
        logger.warning("Could not update adaptive evidence for %s step %s: %s", slug, step_index, exc)

    return {
        "success": True,
        "data": {
            "correct": correct,
            "selected_index": req.answer_index,
            "correct_index": int(expected),
            "explanation": step.get("explanation", ""),
            "attempt_recorded": True,
        },
    }


@router.post("/{slug}/complete", response_model=None)
async def complete_lesson(slug: str, req: CompleteRequest, user=Depends(get_current_user)):
    data = _load_lesson(slug)
    if data is None or not data.get("steps") or not (data.get("assessment") or {}).get("questions"):
        raise HTTPException(status_code=404, detail=f"Step-based lesson not found: {slug}")

    questions = (data.get("assessment") or {}).get("questions", [])
    if not questions:
        raise HTTPException(status_code=400, detail="This lesson has no final assessment.")
    if len(req.answers) != len(questions) or any(str(i) not in req.answers for i in range(len(questions))):
        raise HTTPException(status_code=422, detail="Answer every final-assessment question before submitting.")

    results = []
    correct = 0
    for index, question in enumerate(questions):
        try:
            selected = int(req.answers[str(index)])
        except (TypeError, ValueError):
            selected = -1
        expected = question.get("correct_index")
        is_correct = selected == expected
        correct += int(is_correct)
        results.append({
            "index": index,
            "correct": is_correct,
            "selected_index": selected,
            "correct_index": expected,
            "explanation": question.get("explanation", ""),
        })

    score = round((correct / len(questions)) * 100, 1)
    mastery_threshold = float(
        data.get("mastery_threshold")
        or (data.get("assessment") or {}).get("mastery_threshold")
        or 0.7
    )
    passed = score >= mastery_threshold * 100
    if not passed:
        return {
            "success": True,
            "data": {
                "passed": False,
                "score": score,
                "correct": correct,
                "total": len(questions),
                "results": results,
                "mastery_threshold": mastery_threshold * 100,
                "xp_earned": 0,
                "module_completed": False,
            },
        }

    if bool(req.track_id) != bool(req.module_id):
        raise HTTPException(status_code=400, detail="track_id and module_id must be supplied together.")

    if req.track_id and req.module_id:
        from app.data.learning_paths import COMPANY_TRACKS

        track = COMPANY_TRACKS.get(req.track_id)
        if not track:
            raise HTTPException(status_code=404, detail="Company track not found.")
        module = next(
            (
                module
                for section in track.get("sections", [])
                for module in section.get("modules", [])
                if module.get("id") == req.module_id
            ),
            None,
        )
        if not module:
            raise HTTPException(status_code=404, detail="Company module not found.")
        lesson_topics = {
            _normalize_topic(topic) for topic in LESSON_MODULE_TOPICS.get(slug, set())
        }
        module_topics = {
            _normalize_topic(topic) for topic in module.get("topics", [])
        }
        matching_topics = sorted(lesson_topics.intersection(module_topics))
        if not matching_topics:
            raise HTTPException(
                status_code=422,
                detail="This lesson does not assess the selected company module's topics.",
            )

        # One lesson demonstrates one mapped topic. A mixed module is only
        # complete after every required topic has passed its own assessment.
        requested_topic = _normalize_topic(req.topic_id) if req.topic_id else None
        if requested_topic and requested_topic not in matching_topics:
            raise HTTPException(
                status_code=422,
                detail="The selected topic does not match this lesson and company module.",
            )
        topic_id = requested_topic or matching_topics[0]
        try:
            module_result = await record_track_topic_mastery(
                user_id=user["id"],
                track_id=req.track_id,
                module_id=req.module_id,
                topic_id=topic_id,
                score=score,
                role=user.get("role") or user.get("target_role") or "sde",
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        xp_earned = module_result.get("xp_earned", 0)
        module_completed = bool(module_result.get("module_completed"))
        reward = None
    else:
        reward = await record_practice(
            user_id=user["id"],
            activity_type="company_lesson",
            score=score / 10,
            metadata={
                "lesson_slug": slug,
                "lesson_title": data.get("title") or slug,
                "domain": data.get("domain") or data.get("pattern") or "General",
                "score_percent": score,
                "time_taken": req.time_spent_seconds,
                "passed": True,
            },
            role=user.get("role") or user.get("target_role") or "sde",
        )
        xp_earned = reward.get("xp_gained", 0) if isinstance(reward, dict) else 0
        module_completed = False
        module_result = None

    return {
        "success": True,
        "data": {
            "passed": True,
            "score": score,
            "correct": correct,
            "total": len(questions),
            "results": results,
            "mastery_threshold": mastery_threshold * 100,
            "xp_earned": xp_earned,
            "module_completed": module_completed,
            "module_result": module_result if req.track_id else None,
            "reward": reward,
        },
    }
