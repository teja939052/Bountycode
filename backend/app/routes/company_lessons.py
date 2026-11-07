"""
Company-prep lessons — simple step-based lessons for TCS NQT, Infosys, Wipro, etc.

Routes (all under /api/v1/company-lessons, auth required):
  GET  /api/v1/company-lessons               → list all available lessons
  GET  /api/v1/company-lessons/{slug}        → full lesson content
  POST /api/v1/company-lessons/{slug}/complete → record completion + rewards
"""
import hashlib
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import os
import json
import logging

from app.middleware.auth import get_current_user
from app.database import learning_progress_collection
from app.services.gamification import record_practice
from app.services.learning_paths import record_track_topic_mastery
from app.services.adaptive_learning import record_learning_activity

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/company-lessons", tags=["company-lessons"])

_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LESSONS_DIR = os.path.join(_APP_DIR, "data", "lessons")

# In-memory cache so we don't hit disk on every request.
_LESSON_CACHE: Dict[str, Dict[str, Any]] = {}

# Only server-graded step types can satisfy the lesson evidence gate.
# code_lab is intentionally excluded: its current browser worker submits
# output text to this API, so the server cannot prove which code produced it.
ANSWERABLE_STEP_TYPES = frozenset({
    "interactive", "practice", "quiz", "predict_output", "fill_blank",
    "order_steps", "code_lab", "sql_lab", "debug_choice", "api_scenario",
})
STEP_EVIDENCE_TYPES = ANSWERABLE_STEP_TYPES - {"code_lab"}


def _step_fingerprint(step: Dict[str, Any]) -> str:
    """Bind a passed step to the exact authored content that was graded."""
    canonical = json.dumps(
        step, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _required_step_indices(data: Dict[str, Any]) -> List[int]:
    """Return authored, answerable steps that require persisted server evidence."""
    return [
        index
        for index, step in enumerate(data.get("steps") or [])
        if str(step.get("step_type") or "").strip().lower() in STEP_EVIDENCE_TYPES
    ]

# A guided lesson can only certify a module whose authored topic overlaps the
# skill it teaches. Query-string IDs from the browser are not proof of coverage.
LESSON_MODULE_TOPICS = {
    "input_output_basics": {"input_output", "input", "output", "input_output_basics", "type_conversion"},
    "operators_basics": {"operators", "operator", "expressions", "operator_precedence", "arithmetic_operators", "logical_operators"},
    "variables_basics": {"variables", "variables_basics", "data_types", "types", "assignment"},
    "conditions_basics": {"conditions", "conditional_logic", "boolean_logic", "branching"},
    "functions_basics": {"functions", "functions_basics", "parameters", "return_values"},
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
    "input_output_basics": "programming_fundamentals",
    "operators_basics": "programming_fundamentals",
    "variables_basics": "programming_fundamentals",
    "conditions_basics": "programming_fundamentals",
    "functions_basics": "programming_fundamentals",
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
    answer_index: Optional[int] = Field(default=None, ge=0)
    answer_text: Optional[str] = Field(default=None, min_length=1, max_length=8000)
    answer_order: Optional[List[int]] = Field(default=None, min_length=1, max_length=20)


class LessonProgressRequest(BaseModel):
    current_step: int = Field(..., ge=0, le=100)


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
                # Public catalog metadata helps learners choose a path without
                # exposing answers, SQL grading keys, or hidden assessment data.
                "learning_objectives": (data.get("learning_objectives") or [])[:3],
                "prerequisites": data.get("prerequisites") or [],
                "concept_count": len(data.get("concepts") or []),
                "worked_example_count": len(data.get("worked_examples") or data.get("examples") or []),
                "assessment_count": len((data.get("assessment") or {}).get("questions") or []),
                "company_count": len(data.get("company_applications") or data.get("company") or []),
                "revision_card_count": len(data.get("srs_cards") or data.get("srs") or []),
                "exercise_types": sorted({
                    str(step.get("step_type") or "").strip().lower()
                    for step in (data.get("steps") or [])
                    if str(step.get("step_type") or "").strip().lower() not in {"", "explain"}
                }),
                "quest_chapter": (data.get("quest") or {}).get("chapter"),
                "mission_preview": (data.get("quest") or {}).get("mission"),
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
    # Normalize legacy lesson authoring keys into the canonical player schema.
    # Existing lesson files use both old and new names for the same deep-dive data.
    public_data["worked_examples"] = data.get("worked_examples") or data.get("examples") or []
    public_data["company_applications"] = data.get("company_applications") or data.get("company") or []
    public_data["srs_cards"] = data.get("srs_cards") or data.get("srs") or []
    # Never ship answer keys to the learner before they submit an attempt.
    answer_key_fields = {
        "correct_index", "correct_answer", "answer", "correct_order",
        "expected_answer", "accepted_answers", "expected_output",
        "schema_ddl", "seed_inserts", "expected_query", "feedback_by_option",
    }
    public_data["steps"] = [
        {
            key: value for key, value in step.items()
            if key not in (
                answer_key_fields | {"explanation"}
                if str(step.get("step_type") or "").strip().lower() in ANSWERABLE_STEP_TYPES
                else answer_key_fields
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


@router.get("/{slug}/progress", response_model=None)
async def get_lesson_progress(slug: str, user=Depends(get_current_user)):
    """Return the learner's saved position without exposing lesson answer keys."""
    data = _load_lesson(slug)
    steps = (data or {}).get("steps") or []
    if not data or not steps:
        raise HTTPException(status_code=404, detail=f"Step-based lesson not found: {slug}")

    progress_doc = await learning_progress_collection.find_one({"user_id": user["id"]}) or {}
    saved = (progress_doc.get("lesson_progress") or {}).get(slug) or {}
    try:
        current_step = int(saved.get("current_step", 0))
    except (TypeError, ValueError):
        current_step = 0
    current_step = max(0, min(current_step, len(steps) - 1))

    return {
        "success": True,
        "data": {
            "lesson_slug": slug,
            "current_step": current_step,
            "step_count": len(steps),
            "updated_at": saved.get("updated_at"),
            "has_progress": bool(saved),
        },
    }


@router.put("/{slug}/progress", response_model=None)
async def save_lesson_progress(
    slug: str,
    req: LessonProgressRequest,
    user=Depends(get_current_user),
):
    """Persist a learner's last visited step so a lesson can be resumed."""
    data = _load_lesson(slug)
    steps = (data or {}).get("steps") or []
    if not data or not steps:
        raise HTTPException(status_code=404, detail=f"Step-based lesson not found: {slug}")
    if req.current_step >= len(steps):
        raise HTTPException(status_code=422, detail="The requested lesson step does not exist.")

    updated_at = datetime.now(timezone.utc).isoformat()
    await learning_progress_collection.update_one(
        {"user_id": user["id"]},
        {
            "$set": {
                f"lesson_progress.{slug}.current_step": req.current_step,
                f"lesson_progress.{slug}.updated_at": updated_at,
            }
        },
        upsert=True,
    )
    return {
        "success": True,
        "data": {
            "lesson_slug": slug,
            "current_step": req.current_step,
            "updated_at": updated_at,
        },
    }


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
    step_type = str(step.get("step_type") or "").strip().lower()
    selected_index = None
    correct_index = None
    correct_answer = None
    correct_order = None
    feedback = None
    student_results = None

    if step_type == "code_lab":
        if req.answer_text is None or req.answer_index is not None or req.answer_order is not None:
            raise HTTPException(status_code=422, detail="Run the code before checking its output.")
        expected_output = step.get("expected_output")
        if expected_output is None:
            raise HTTPException(status_code=500, detail="This code lab has no expected output.")
        normalize = lambda value: "\\n".join(line.rstrip() for line in str(value).replace("\\r\\n", "\\n").strip().splitlines())
        accepted_outputs = step.get("accepted_outputs") or [expected_output]
        if not isinstance(accepted_outputs, list):
            accepted_outputs = [accepted_outputs]
        correct = normalize(req.answer_text) in {normalize(value) for value in accepted_outputs}
        feedback = "Your program produced the expected output." if correct else "Your program ran, but the output does not match yet. Compare the loop condition, update and printed value."
    elif step_type == "sql_lab":
        if req.answer_text is None or req.answer_index is not None or req.answer_order is not None:
            raise HTTPException(status_code=422, detail="Write a SQL query before checking it.")
        schema_ddl = step.get("schema_ddl")
        seed_inserts = step.get("seed_inserts")
        expected_query = step.get("expected_query")
        if not all(isinstance(value, str) and value.strip() for value in (schema_ddl, seed_inserts, expected_query)):
            raise HTTPException(status_code=500, detail="This SQL lab is missing its grading data.")
        from app.services.sql_engine import SQLEngine
        validation = SQLEngine.verify_read_only_query(
            schema_ddl=schema_ddl,
            seed_inserts=seed_inserts,
            expected_query=expected_query,
            student_query=req.answer_text,
            enforce_order=bool(step.get("enforce_order", False)),
        )
        correct = validation.is_correct
        feedback = "Your query returned the required result." if correct else validation.error_message or "Your query needs another revision."
        student_results = validation.student_results
    elif step_type == "order_steps":
        options = step.get("options") or []
        expected = step.get("correct_order")
        if not isinstance(expected, list) or len(expected) != len(options) or sorted(expected) != list(range(len(options))):
            raise HTTPException(status_code=500, detail="This lesson has an invalid ordering key.")
        if req.answer_order is None or req.answer_index is not None or req.answer_text is not None:
            raise HTTPException(status_code=422, detail="Reorder every step before checking.")
        if len(req.answer_order) != len(options) or sorted(req.answer_order) != list(range(len(options))):
            raise HTTPException(status_code=422, detail="The submitted sequence must include every step exactly once.")
        correct_order = list(expected)
        correct = req.answer_order == expected
        correct_answer = " → ".join(str(options[index]) for index in expected)
    elif step_type in {"interactive", "practice", "quiz", "debug_choice", "api_scenario"}:
        options = step.get("options") or []
        expected = step.get("correct_index")
        if expected is None or req.answer_index is None or req.answer_text is not None:
            raise HTTPException(status_code=422, detail="Choose one of the available options.")
        if req.answer_index >= len(options):
            raise HTTPException(status_code=422, detail="Selected answer is outside the available options.")
        selected_index = req.answer_index
        correct_index = int(expected)
        correct_answer = str(options[correct_index])
        correct = selected_index == correct_index
        feedback_by_option = step.get("feedback_by_option") or {}
        feedback = feedback_by_option.get(str(selected_index))
    elif step_type in {"predict_output", "fill_blank"}:
        expected = step.get("expected_answer")
        if expected is None or req.answer_text is None or req.answer_index is not None:
            raise HTTPException(status_code=422, detail="Enter an answer before checking it.")
        submitted = " ".join(req.answer_text.strip().split())
        accepted = step.get("accepted_answers") or [expected]
        if not isinstance(accepted, list):
            accepted = [accepted]
        normalized_submitted = submitted if step.get("case_sensitive", True) else submitted.casefold()
        normalized_accepted = [
            " ".join(str(item).strip().split())
            if step.get("case_sensitive", True)
            else " ".join(str(item).strip().split()).casefold()
            for item in accepted
        ]
        correct = normalized_submitted in normalized_accepted
        correct_answer = str(expected)
    else:
        raise HTTPException(status_code=400, detail="This lesson step is not answerable.")

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

    # Persist server-graded evidence before reporting a step as completed.
    # Attempts are counted, but a prior pass is never erased by a later retry.
    evidence_recorded = step_type in STEP_EVIDENCE_TYPES
    if evidence_recorded:
        evidence_path = f"lesson_progress.{slug}.step_evidence.{step_index}"
        evidence_update: Dict[str, Any] = {
            "$inc": {f"{evidence_path}.attempts": 1},
        }
        if correct:
            evidence_update["$set"] = {
                f"{evidence_path}.passed": True,
                f"{evidence_path}.passed_at": datetime.now(timezone.utc).isoformat(),
                f"{evidence_path}.fingerprint": _step_fingerprint(step),
            }
        try:
            await learning_progress_collection.update_one(
                {"user_id": user["id"]},
                evidence_update,
                upsert=True,
            )
        except Exception as exc:
            logger.exception(
                "Could not persist lesson evidence for %s step %s: %s",
                slug, step_index, exc,
            )
            raise HTTPException(
                status_code=503,
                detail="Your answer was checked, but its learning evidence could not be saved. Please retry.",
            )

        # Adaptive telemetry is secondary to the persisted evidence record.
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
            "selected_index": selected_index,
            "correct_index": correct_index,
            "correct_answer": correct_answer,
            "correct_order": correct_order,
            "feedback": feedback,
            "student_results": student_results,
            "explanation": step.get("explanation", ""),
            "attempt_recorded": True,
            "evidence_recorded": evidence_recorded,
            "formative_only": step_type == "code_lab",
        },
    }


@router.post("/{slug}/complete", response_model=None)
async def complete_lesson(slug: str, req: CompleteRequest, user=Depends(get_current_user)):
    """Grade the final assessment and record evidence, including failed attempts."""
    data = _load_lesson(slug)
    if data is None or not data.get("steps") or not (data.get("assessment") or {}).get("questions"):
        raise HTTPException(status_code=404, detail=f"Step-based lesson not found: {slug}")

    questions = (data.get("assessment") or {}).get("questions", [])
    if not questions:
        raise HTTPException(status_code=400, detail="This lesson has no final assessment.")
    if len(req.answers) != len(questions) or any(str(i) not in req.answers for i in range(len(questions))):
        raise HTTPException(status_code=422, detail="Answer every final-assessment question before submitting.")
    if bool(req.track_id) != bool(req.module_id):
        raise HTTPException(status_code=400, detail="track_id and module_id must be supplied together.")

    required_indices = _required_step_indices(data)
    if required_indices:
        progress_doc = await learning_progress_collection.find_one(
            {"user_id": user["id"]}
        ) or {}
        saved_lesson = (progress_doc.get("lesson_progress") or {}).get(slug) or {}
        step_evidence = saved_lesson.get("step_evidence") or {}
        missing_steps = []
        for index in required_indices:
            step = data["steps"][index]
            evidence = step_evidence.get(str(index)) or step_evidence.get(index) or {}
            if (
                evidence.get("passed") is not True
                or evidence.get("fingerprint") != _step_fingerprint(step)
            ):
                missing_steps.append({
                    "step_index": index,
                    "step_number": step.get("step_number", index + 1),
                    "title": step.get("title") or f"Step {index + 1}",
                })
        if missing_steps:
            raise HTTPException(
                status_code=409,
                detail={
                    "message": "Complete the required interactive steps before submitting the final assessment.",
                    "missing_steps": missing_steps,
                },
            )

    # Validate the company mapping before recording any result. This prevents
    # a malformed target/module pair from creating misleading learner evidence.
    topic_id = None
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
        requested_topic = _normalize_topic(req.topic_id) if req.topic_id else None
        if requested_topic and requested_topic not in matching_topics:
            raise HTTPException(
                status_code=422,
                detail="The selected topic does not match this lesson and company module.",
            )
        topic_id = requested_topic or matching_topics[0]
    elif req.topic_id:
        raise HTTPException(status_code=400, detail="topic_id requires track_id and module_id.")

    results = []
    correct = 0
    for index, question in enumerate(questions):
        try:
            selected = int(req.answers[str(index)])
        except (TypeError, ValueError):
            selected = -1
        options = question.get("options") or []
        if selected < 0 or selected >= len(options):
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
        }.get(str(data.get("domain") or data.get("pattern") or "").lower(),
              "programming_fundamentals"),
    )
    # Record both passes and failures. Adaptive learning needs the denominator:
    # a learner who struggles should receive a different next lesson, not be
    # invisible to the recommendation engine.
    try:
        await record_learning_activity(
            user["id"],
            {
                "domain_id": domain_id,
                "type": "lesson_assessment",
                "success": passed,
                "score_impact": 1,
                "lesson_slug": slug,
                "score_percent": score,
                "correct_count": correct,
                "question_count": len(questions),
                "time_spent_seconds": req.time_spent_seconds,
                "topic_id": topic_id,
                "track_id": req.track_id,
                "module_id": req.module_id,
            },
        )
    except Exception as exc:
        logger.warning("Could not update adaptive evidence for lesson %s: %s", slug, exc)

    module_result = None
    module_completed = False
    reward = None
    xp_earned = 0
    reward_already_claimed = False

    if req.track_id and req.module_id and topic_id:
        try:
            # This service stores failed attempts too, but only records mastery
            # at >=70%; a mixed module completes only after every topic passes.
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
        module_completed = bool(module_result.get("module_completed"))
        xp_earned = int(module_result.get("xp_earned", 0) or 0)
    elif passed:
        # Standalone lessons do not have a company-module completion guard.
        # Claim the first-pass reward atomically in learner progress before
        # calling the canonical gamification writer; concurrent/replayed
        # completion requests must not mint Diamonds more than once.
        try:
            await learning_progress_collection.update_one(
                {"user_id": user["id"]},
                {"$setOnInsert": {"user_id": user["id"]}},
                upsert=True,
            )
            reward_claim_path = f"lesson_progress.{slug}.completion_reward_claimed"
            claim = await learning_progress_collection.update_one(
                {
                    "user_id": user["id"],
                    reward_claim_path: {"$ne": True},
                },
                {
                    "$set": {
                        reward_claim_path: True,
                        f"lesson_progress.{slug}.completion_reward_claimed_at": datetime.now(timezone.utc).isoformat(),
                        f"lesson_progress.{slug}.best_assessment_score": score,
                    }
                },
            )
        except Exception as exc:
            logger.exception("Could not claim standalone lesson reward for %s: %s", slug, exc)
            raise HTTPException(
                status_code=503,
                detail="Your assessment was graded, but its reward could not be safely claimed. Please retry.",
            )

        if getattr(claim, "modified_count", 0):
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
                activity_id=f"lesson:{slug}:first_mastery",
            )
            xp_earned = int(reward.get("xp_gained", 0) or 0) if isinstance(reward, dict) else 0
        else:
            reward_already_claimed = True

    return {
        "success": True,
        "data": {
            "passed": passed,
            "score": score,
            "correct": correct,
            "total": len(questions),
            "results": results,
            "mastery_threshold": mastery_threshold * 100,
            "xp_earned": xp_earned,
            "module_completed": module_completed,
            "module_result": module_result,
            "reward": reward,
            "reward_already_claimed": reward_already_claimed,
        },
    }
