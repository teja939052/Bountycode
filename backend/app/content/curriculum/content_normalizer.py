"""Normalize authored lesson content into the canonical 9-step teaching loop.

Different legacy content modules use different schemas:
  - flagship lessons: discovery, prediction, guided_build, transfer_challenge, ...
  - concept slices:   discovery, prediction, guided_build, transfer_challenge, ...
  - mission templates: steps dict keyed by step name

This module maps any supported schema into the canonical
  discover → understand → manipulate → predict → build → break_step → debug → retrieval → transfer
loop expected by `UnifiedLessonPlayer` and `DomainAdapter._step_content`.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


# ═══════════════════════════════════════════════════════════════
# Public API
# ═══════════════════════════════════════════════════════════════

def normalize_lesson(lesson: Dict[str, Any]) -> Dict[str, Any]:
    """Return a lesson dict whose top-level `steps` follows the canonical contract.

    If the lesson already has canonical `steps`, it is returned unchanged.
    Otherwise legacy keys are mapped into canonical steps.
    """
    # Ensure domain is set
    if not lesson.get("domain"):
        lesson = dict(lesson, domain=_infer_domain(lesson))

    steps = lesson.get("steps")
    if isinstance(steps, dict) and steps:
        return lesson

    legacy = _detect_legacy_schema(lesson)
    if legacy is None:
        # Unknown schema — keep minimal contract to avoid silent fallback
        return dict(lesson, steps={})

    normalized = dict(lesson)
    normalized["steps"] = _map_legacy_to_canonical(lesson, legacy)
    return normalized


def _infer_domain(lesson: Dict[str, Any]) -> str:
    """Infer domain from module_id or lesson_id if not explicitly set."""
    domain = lesson.get("domain")
    if domain:
        return domain
    module_id = lesson.get("module_id", "")
    lesson_id = lesson.get("lesson_id", "")
    source = f"{module_id} {lesson_id}".lower()
    if any(k in source for k in ["aptitude", "quantitative", "logical", "blood", "percentage"]):
        return "aptitude"
    if any(k in source for k in ["communication", "verbal", "email", "language"]):
        return "verbal"
    if any(k in source for k in ["coding", "programming", "variables", "loops", "arrays", "strings", "functions", "sorting", "complexity", "control_flow", "trace", "input_output", "types", "expressions", "booleans", "decisions", "scope", "compose", "capstone"]):
        return "coding"
    if any(k in source for k in ["cs_core", "dbms", "os_", "tcp", "networking", "software_engineering", "encapsulation", "indexing", "normalization", "memory_management", "inheritance", "polymorphism", "osi_model"]):
        return "cs_core"
    if any(k in source for k in ["sql", "joins"]):
        return "sql"
    if any(k in source for k in ["behavioral", "star", "interview"]):
        return "behavioral"
    if any(k in source for k in ["system_design", "design"]):
        return "system_design"
    if any(k in source for k in ["reasoning", "syllogism", "series", "seating", "puzzles", "directions", "data_sufficiency", "coding_decoding"]):
        return "reasoning"
    return "coding"


def canonical_steps() -> List[str]:
    return [
        "discover",
        "understand",
        "manipulate",
        "predict",
        "build",
        "break_step",
        "debug",
        "retrieval",
        "transfer",
    ]


# ═══════════════════════════════════════════════════════════════
# Schema detection
# ═══════════════════════════════════════════════════════════════

_LEGACY_KEYS: Dict[str, List[str]] = {
    "flagship": ["discovery", "prediction", "guided_build", "transfer_challenge", "assessment", "break", "explain"],
    "concept_slice": ["discovery", "prediction", "guided_build", "transfer_challenge", "assessment", "break", "explain"],
    "mission_template": ["steps"],
}


def _detect_legacy_schema(lesson: Dict[str, Any]) -> Optional[str]:
    keys = list(lesson.keys())
    for schema, markers in _LEGACY_KEYS.items():
        if schema == "mission_template":
            if "steps" in lesson and isinstance(lesson.get("steps"), dict):
                return None  # already canonical/mission-template form
            continue
        if any(m in keys for m in markers):
            return schema
    return None


# ═══════════════════════════════════════════════════════════════
# Legacy → canonical mapping
# ═══════════════════════════════════════════════════════════════

def _map_legacy_to_canonical(lesson: Dict[str, Any], legacy: str) -> Dict[str, Any]:
    if legacy in ("flagship", "concept_slice"):
        return _map_flagship_slice(lesson)
    return {step: {} for step in canonical_steps()}


def _map_flagship_slice(lesson: Dict[str, Any]) -> Dict[str, Any]:
    steps: Dict[str, Any] = {step: {} for step in canonical_steps()}

    discovery = lesson.get("discovery", {})
    discovery_steps = discovery.get("steps", [])
    steps["discover"] = _discovery_to_step(discovery_steps[0] if discovery_steps else {}, "discover")
    steps["understand"] = _discovery_summary_to_understand(discovery)
    steps["manipulate"] = _discovery_to_step(discovery_steps[1] if len(discovery_steps) > 1 else {}, "manipulate")

    prediction = lesson.get("prediction", {})
    steps["predict"] = _prediction_to_predict(prediction)

    guided_build = lesson.get("guided_build", {})
    steps["build"] = _guided_build_to_build(guided_build)

    transfer_challenge = lesson.get("transfer_challenge", {})
    steps["transfer"] = _transfer_challenge_to_transfer(transfer_challenge)

    break_block = lesson.get("break", {})
    steps["break_step"] = _break_to_break_step(break_block)

    explain = lesson.get("explain", {})
    steps["retrieval"] = _explain_to_retrieval(explain)

    assessment = lesson.get("assessment", {})
    steps["debug"] = _assessment_debug_to_debug(assessment)

    return steps


# ═══════════════════════════════════════════════════════════════
# Mappers
# ═══════════════════════════════════════════════════════════════

def _discovery_to_step(step_block: Dict[str, Any], fallback_name: str) -> Dict[str, Any]:
    if not step_block:
        return {"prompt": fallback_name, "interaction": {"type": "read"}}
    interaction = step_block.get("interaction", {})
    return {
        "prompt": step_block.get("narration", fallback_name),
        "action": step_block.get("action", fallback_name),
        "interaction": interaction,
        "title": step_block.get("title", fallback_name),
    }


def _discovery_summary_to_understand(discovery: Dict[str, Any]) -> Dict[str, Any]:
    conclusion = discovery.get("conclusion", "")
    if conclusion:
        return {
            "prompt": "Understand the concept before you apply it.",
            "explanation": conclusion,
            "title": discovery.get("title", "Understand"),
        }
    return {"prompt": "Understand the concept before you apply it.", "title": "Understand"}


def _prediction_to_predict(prediction: Dict[str, Any]) -> Dict[str, Any]:
    options = prediction.get("options", [])
    correct = next((o for o in options if o.get("correct")), None)
    return {
        "prompt": prediction.get("question", "Predict the outcome before running."),
        "question": prediction.get("question", ""),
        "code": prediction.get("code", ""),
        "options": options,
        "correct_option_id": correct.get("id") if correct else None,
        "explanation": prediction.get("explanation", ""),
        "title": prediction.get("title", "Predict"),
    }


def _guided_build_to_build(guided_build: Dict[str, Any]) -> Dict[str, Any]:
    steps = guided_build.get("steps", [])
    primary = steps[0] if steps else {}
    return {
        "prompt": primary.get("description", "Build something with what you learned."),
        "title": guided_build.get("title", "Build"),
        "starter_code": primary.get("starter_code", ""),
        "function_name": primary.get("function_name", ""),
        "signature": primary.get("signature", ""),
        "test_cases": primary.get("test_cases", []),
        "hidden_test_cases": primary.get("hidden_test_cases", []),
        "scaffolded_hints": primary.get("scaffolded_hints", []),
        "diamonds": primary.get("diamonds", 0),
        "time_limit_minutes": primary.get("time_limit_minutes"),
        "steps": steps,
    }


def _transfer_challenge_to_transfer(transfer_challenge: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "prompt": transfer_challenge.get("description", "Transfer your skill to a new problem."),
        "title": transfer_challenge.get("title", "Transfer"),
        "function_name": transfer_challenge.get("function_name", ""),
        "signature": transfer_challenge.get("signature", ""),
        "description_full": transfer_challenge.get("description_full", ""),
        "test_cases": transfer_challenge.get("test_cases", []),
        "hidden_test_cases": transfer_challenge.get("hidden_test_cases", []),
        "scaffolded_hints": transfer_challenge.get("scaffolded_hints", []),
        "diamonds": transfer_challenge.get("diamonds", 0),
        "time_limit_minutes": transfer_challenge.get("time_limit_minutes"),
    }


def _break_to_break_step(break_block: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "prompt": break_block.get("story", "Find the broken assumption."),
        "title": break_block.get("title", "Break"),
        "buggy_code": break_block.get("buggy_code", ""),
        "expected_output": break_block.get("expected_output", ""),
        "actual_output": break_block.get("actual_output", ""),
        "diagnosis": break_block.get("diagnosis", {}),
        "fix": break_block.get("fix", ""),
        "fixed_code": break_block.get("fixed_code", ""),
        "explanation": break_block.get("explanation", ""),
    }


def _explain_to_retrieval(explain: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "prompt": explain.get("prompt", "Retrieve and explain the key idea."),
        "title": explain.get("title", "Retrieve"),
        "answer_format": explain.get("answer_format", "short_answer"),
        "keywords": explain.get("keywords", []),
        "min_words": explain.get("min_words", 0),
        "model_answer": explain.get("model_answer", ""),
        "intention": explain.get("intention", ""),
    }


def _assessment_debug_to_debug(assessment: Dict[str, Any]) -> Dict[str, Any]:
    questions = assessment.get("questions", [])
    debug_q = next((q for q in questions if q.get("type") == "debug"), None)
    if debug_q is None and questions:
        debug_q = questions[0]
    if debug_q is None:
        return {"prompt": "Debug and fix the issue.", "title": "Debug"}
    return {
        "prompt": debug_q.get("question", "Debug and fix the issue."),
        "title": assessment.get("title", "Debug"),
        "code": debug_q.get("code", ""),
        "error": debug_q.get("error", ""),
        "question": debug_q.get("question", ""),
        "fix": debug_q.get("fix", ""),
        "explanation": debug_q.get("explanation", ""),
    }
