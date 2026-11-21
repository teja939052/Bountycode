"""
Question Quality Service - Type-specific quality validation for BountyCode.

Separates content completeness from correctness. A question can be
structurally complete but have incorrect answers. Trust status and serving
eligibility are separate dimensions.

Design principles:
- Every question type has its own required/optional/inapplicable fields
- Completeness (structural) is distinct from correctness (answers match)
- A high score never automatically grants trust_status="verified"
- Trust transitions require explicit human review via transition_trust()
- All functions are pure and testable without a database

Architectural boundary:
    question quality  -> question_quality.py  (this file)
    trust status      -> question_store.py    (lifecycle state machine)
    serving eligibility -> question_store.py  (_is_servable gate)

These three systems are independent. A question can be structurally complete
but incorrect. It can be correct but not human-reviewed. And it can be
human-reviewed but unsuitable for a particular assessment.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple
from collections import Counter, defaultdict


# =============================================================================
# Type-specific question field definitions
# Each field spec: {field, required (bool), label, weight (int), inapplicable_types}
# ---------------------------------------------------------------------------

QUESTION_TYPE_SCHEMAS: Dict[str, List[Dict[str, Any]]] = {
    "coding": [
        {"field": "question", "required": True, "label": "Problem statement", "weight": 10},
        {"field": "solution", "required": True, "label": "Reference solution", "weight": 9},
        {"field": "test_cases", "required": True, "label": "Executable test cases", "weight": 10},
        {"field": "constraints", "required": False, "label": "Explicit constraints", "weight": 5},
        {"field": "examples", "required": False, "label": "Examples", "weight": 5},
        {"field": "edge_cases", "required": False, "label": "Edge cases", "weight": 6},
        {"field": "difficulty", "required": False, "label": "Difficulty", "weight": 5},
        {"field": "pattern", "required": False, "label": "Pattern", "weight": 4},
        {"field": "skill", "required": False, "label": "Skill tag", "weight": 6},
        {"field": "expected_thinking", "required": False, "label": "Expected thinking", "weight": 6},
        {"field": "hints", "required": False, "label": "Hints", "weight": 4},
        {"field": "complexity", "required": False, "label": "Time/space complexity", "weight": 5},
        {"field": "follow_up", "required": False, "label": "Follow-up question", "weight": 3},
        {"field": "interview_explanation", "required": False, "label": "Interview explanation", "weight": 3},
    ],
    "sql": [
        {"field": "question", "required": True, "label": "Problem statement", "weight": 10},
        {"field": "sql_schema", "required": True, "label": "SQL schema DDL", "weight": 10},
        {"field": "seed_inserts", "required": True, "label": "Seed data", "weight": 8},
        {"field": "expected_query", "required": True, "label": "Expected query", "weight": 9},
        {"field": "test_cases", "required": True, "label": "Executable test cases", "weight": 10},
        {"field": "difficulty", "required": False, "label": "Difficulty", "weight": 5},
        {"field": "pattern", "required": False, "label": "Pattern", "weight": 4},
        {"field": "skill", "required": False, "label": "Skill tag", "weight": 6},
        {"field": "explanation", "required": False, "label": "Explanation", "weight": 5},
        {"field": "hints", "required": False, "label": "Hints", "weight": 4},
        {"field": "constraints", "required": False, "label": "Explicit constraints", "weight": 4},
    ],
    "aptitude": [
        {"field": "question", "required": True, "label": "Problem statement", "weight": 10},
        {"field": "options", "required": True, "label": "Options", "weight": 10},
        {"field": "correct_answer", "required": True, "label": "Correct answer", "weight": 10},
        {"field": "explanation", "required": True, "label": "Step-by-step explanation", "weight": 10},
        {"field": "difficulty", "required": False, "label": "Difficulty", "weight": 5},
        {"field": "skill", "required": False, "label": "Skill tag", "weight": 6},
        {"field": "pattern", "required": False, "label": "Pattern", "weight": 4},
        {"field": "hints", "required": False, "label": "Hints", "weight": 4},
        {"field": "common_trap", "required": False, "label": "Common trap / distractor explanation", "weight": 5},
        {"field": "reasoning_steps", "required": False, "label": "Reasoning steps", "weight": 6},
    ],
    "logical": [
        {"field": "question", "required": True, "label": "Problem statement", "weight": 10},
        {"field": "options", "required": False, "label": "Options (optional)", "weight": 5},
        {"field": "correct_answer", "required": True, "label": "Correct answer", "weight": 10},
        {"field": "explanation", "required": True, "label": "Step-by-step explanation", "weight": 10},
        {"field": "difficulty", "required": False, "label": "Difficulty", "weight": 5},
        {"field": "skill", "required": False, "label": "Skill tag", "weight": 6},
        {"field": "pattern", "required": False, "label": "Pattern", "weight": 4},
        {"field": "hints", "required": False, "label": "Hints", "weight": 4},
        {"field": "common_trap", "required": False, "label": "Common trap", "weight": 5},
        {"field": "reasoning_steps", "required": False, "label": "Reasoning steps", "weight": 6},
    ],
    "verbal": [
        {"field": "question", "required": True, "label": "Question text", "weight": 10},
        {"field": "options", "required": False, "label": "Options (optional)", "weight": 5},
        {"field": "correct_answer", "required": True, "label": "Correct answer", "weight": 10},
        {"field": "explanation", "required": True, "label": "Explanation", "weight": 10},
        {"field": "difficulty", "required": False, "label": "Difficulty", "weight": 5},
        {"field": "skill", "required": False, "label": "Skill tag", "weight": 6},
        {"field": "pattern", "required": False, "label": "Pattern", "weight": 4},
        {"field": "hints", "required": False, "label": "Hints", "weight": 4},
        {"field": "passage", "required": False, "label": "Passage or sentence where needed", "weight": 5},
    ],
    "cs_fundamentals": [
        {"field": "question", "required": True, "label": "Problem statement", "weight": 10},
        {"field": "options", "required": False, "label": "Options (optional)", "weight": 5},
        {"field": "correct_answer", "required": True, "label": "Correct answer", "weight": 10},
        {"field": "explanation", "required": True, "label": "Explanation", "weight": 10},
        {"field": "difficulty", "required": False, "label": "Difficulty", "weight": 5},
        {"field": "skill", "required": False, "label": "Skill tag", "weight": 6},
        {"field": "pattern", "required": False, "label": "Pattern", "weight": 4},
        {"field": "hints", "required": False, "label": "Hints", "weight": 4},
        {"field": "common_trap", "required": False, "label": "Common trap", "weight": 5},
        {"field": "reasoning_steps", "required": False, "label": "Reasoning steps", "weight": 6},
    ],
    "debugging": [
        {"field": "question", "required": True, "label": "Problem statement", "weight": 10},
        {"field": "buggy_code", "required": True, "label": "Broken code", "weight": 10},
        {"field": "correct_code", "required": True, "label": "Corrected implementation", "weight": 10},
        {"field": "expected_behaviour", "required": True, "label": "Expected behaviour", "weight": 8},
        {"field": "logs_or_error", "required": True, "label": "Actual failure / error", "weight": 8},
        {"field": "root_cause", "required": True, "label": "Root cause", "weight": 10},
        {"field": "test_cases", "required": False, "label": "Regression tests", "weight": 6},
        {"field": "difficulty", "required": False, "label": "Difficulty", "weight": 5},
        {"field": "skill", "required": False, "label": "Skill tag", "weight": 6},
        {"field": "hints", "required": False, "label": "Hints", "weight": 4},
    ],
    "system_design": [
        {"field": "question", "required": True, "label": "Problem statement", "weight": 10},
        {"field": "rubric", "required": True, "label": "Evaluation rubric", "weight": 10},
        {"field": "requirements", "required": True, "label": "Requirements", "weight": 9},
        {"field": "constraints", "required": True, "label": "Constraints", "weight": 8},
        {"field": "architecture", "required": True, "label": "Architecture / components", "weight": 9},
        {"field": "trade_offs", "required": True, "label": "Trade-offs", "weight": 8},
        {"field": "reliability", "required": True, "label": "Reliability and scalability", "weight": 7},
        {"field": "difficulty", "required": False, "label": "Difficulty", "weight": 5},
        {"field": "skill", "required": False, "label": "Skill tag", "weight": 6},
        {"field": "pattern", "required": False, "label": "Pattern", "weight": 4},
        {"field": "hints", "required": False, "label": "Hints", "weight": 4},
    ],
    "interview": [
        {"field": "question", "required": True, "label": "Question text", "weight": 10},
        {"field": "rubric", "required": True, "label": "Evaluation rubric", "weight": 10},
        {"field": "competency", "required": True, "label": "Competency being tested", "weight": 8},
        {"field": "expected_thinking", "required": True, "label": "Expected thinking / response framework", "weight": 8},
        {"field": "difficulty", "required": False, "label": "Difficulty", "weight": 5},
        {"field": "skill", "required": False, "label": "Skill tag", "weight": 6},
        {"field": "pattern", "required": False, "label": "Pattern", "weight": 4},
        {"field": "hints", "required": False, "label": "Hints", "weight": 4},
    ],
    "behavioral": [
        {"field": "question", "required": True, "label": "Question text", "weight": 10},
        {"field": "rubric", "required": True, "label": "Evaluation rubric", "weight": 10},
        {"field": "competency", "required": True, "label": "Competency being tested", "weight": 8},
        {"field": "star_framework", "required": True, "label": "STAR or equivalent response framework", "weight": 8},
        {"field": "evaluation_criteria", "required": True, "label": "Evaluation criteria", "weight": 8},
        {"field": "difficulty", "required": False, "label": "Difficulty", "weight": 5},
        {"field": "skill", "required": False, "label": "Skill tag", "weight": 6},
        {"field": "pattern", "required": False, "label": "Pattern", "weight": 4},
        {"field": "hints", "required": False, "label": "Hints", "weight": 4},
    ],
}

# Question types that are served to learners
SERVABLE_TYPES = {
    "coding", "sql", "aptitude", "logical", "verbal",
    "cs_fundamentals", "cs", "debugging", "system_design",
    "interview", "behavioral",
}

# Question types that require executable validation (test cases / schema / code execution)
EXECUTABLE_TYPES = {"coding", "sql", "debugging"}

# Question types that use MCQ-style answer keys
MCQ_TYPES = {"aptitude", "logical", "verbal", "hr", "behavioral", "cs_fundamentals", "cs"}

# Question types that use rubric-based evaluation
RUBRIC_TYPES = {"interview", "system_design", "gd", "group_discussion"}

# Field inapplicability: fields that should NOT be scored for certain types
# (e.g., "test_cases" is inapplicable for verbal MCQs — they don't use them)
INAPPLICABLE_FIELDS: Dict[str, List[str]] = {
    "verbal": ["test_cases", "sql_schema", "seed_inserts", "expected_query",
               "buggy_code", "correct_code", "expected_behaviour", "logs_or_error",
               "root_cause", "rubric", "requirements", "architecture", "trade_offs",
               "reliability", "competency", "star_framework", "evaluation_criteria"],
    "logical": ["test_cases", "sql_schema", "seed_inserts", "expected_query",
                "buggy_code", "correct_code", "expected_behaviour", "logs_or_error",
                "root_cause", "rubric", "requirements", "architecture", "trade_offs",
                "reliability", "competency", "star_framework", "evaluation_criteria"],
    "cs_fundamentals": ["test_cases", "sql_schema", "seed_inserts", "expected_query",
                        "buggy_code", "correct_code", "expected_behaviour", "logs_or_error",
                        "root_cause", "rubric", "requirements", "architecture", "trade_offs",
                        "reliability", "competency", "star_framework", "evaluation_criteria"],
    "cs": ["test_cases", "sql_schema", "seed_inserts", "expected_query",
           "buggy_code", "correct_code", "expected_behaviour", "logs_or_error",
           "root_cause", "rubric", "requirements", "architecture", "trade_offs",
           "reliability", "competency", "star_framework", "evaluation_criteria"],
    "system_design": ["test_cases", "options", "correct_answer", "correct_index",
                      "buggy_code", "correct_code", "expected_behaviour", "logs_or_error",
                      "root_cause"],
    "interview": ["test_cases", "options", "correct_answer", "correct_index",
                  "buggy_code", "correct_code", "expected_behaviour", "logs_or_error",
                  "root_cause"],
    "behavioral": ["test_cases", "options", "correct_answer", "correct_index",
                   "buggy_code", "correct_code", "expected_behaviour", "logs_or_error",
                   "root_cause"],
    "coding": ["sql_schema", "seed_inserts", "expected_query", "rubric", "requirements",
               "architecture", "trade_offs", "reliability", "competency", "star_framework",
               "evaluation_criteria"],
    "sql": ["options", "correct_answer", "correct_index", "buggy_code", "correct_code",
            "expected_behaviour", "logs_or_error", "root_cause", "rubric", "requirements",
            "architecture", "trade_offs", "reliability", "competency", "star_framework",
            "evaluation_criteria"],
    "debugging": ["sql_schema", "seed_inserts", "expected_query", "rubric", "requirements",
                  "architecture", "trade_offs", "reliability", "competency", "star_framework",
                  "evaluation_criteria"],
    "aptitude": ["sql_schema", "seed_inserts", "expected_query",
                 "buggy_code", "correct_code", "expected_behaviour", "logs_or_error",
                 "root_cause", "rubric", "requirements", "architecture", "trade_offs",
                 "reliability", "competency", "star_framework", "evaluation_criteria"],
}


# =============================================================================
# Quality dimensions (independent, not combined into one score)
# =============================================================================

class QualityDimensions:
    """
    Independent quality dimensions for a question.

    Each dimension is scored 0-100 independently. A question can score
    100 on structural completeness but 0 on answer correctness. No single
    "overall score" is computed here — consumers combine dimensions with
    explicit weighting per use case.
    """

    def __init__(self, question_type: str):
        self.question_type = question_type
        self.structural_completeness: Optional[float] = None  # 0-100
        self.answer_correctness: Optional[float] = None       # 0-100 (None = not applicable / needs human review)
        self.explanation_correctness: Optional[float] = None  # 0-100
        self.executability: Optional[float] = None            # 0-100
        self.difficulty_accuracy: Optional[float] = None      # 0-100
        self.skill_alignment: Optional[float] = None          # 0-100
        self.placement_relevance: Optional[float] = None      # 0-100
        self.originality: Optional[float] = None              # 0-100
        self.assessment_usefulness: Optional[float] = None    # 0-100
        self.evidence: Dict[str, Any] = {}                    # raw evidence per dimension

    def to_dict(self) -> Dict[str, Any]:
        return {
            "question_type": self.question_type,
            "structural_completeness": self.structural_completeness,
            "answer_correctness": self.answer_correctness,
            "explanation_correctness": self.explanation_correctness,
            "executability": self.executability,
            "difficulty_accuracy": self.difficulty_accuracy,
            "skill_alignment": self.skill_alignment,
            "placement_relevance": self.placement_relevance,
            "originality": self.originality,
            "assessment_usefulness": self.assessment_usefulness,
            "evidence": self.evidence,
        }


# =============================================================================
# Field presence detection (shared helper)
# =============================================================================

def _field_present(q: dict, field: str) -> bool:
    """Check if a canonical field is present and non-empty on a question."""
    if field == "question":
        return bool(str(q.get("question") or q.get("question_title") or q.get("statement") or "").strip())
    if field == "options":
        opts = q.get("options")
        return bool(opts and (isinstance(opts, dict) and len(opts) > 0 or isinstance(opts, list) and len(opts) > 0))
    if field == "correct_answer":
        return bool(str(q.get("correct_answer") or q.get("correct_index") or "").strip())
    if field == "correct_index":
        return bool(str(q.get("correct_index") or "").strip())
    if field == "explanation":
        return bool(str(q.get("explanation") or "").strip())
    if field == "test_cases":
        tcs = q.get("test_cases") or q.get("testcases") or []
        return bool(tcs)
    if field == "sql_schema":
        return bool(q.get("sql_schema"))
    if field == "seed_inserts":
        return bool(q.get("seed_inserts"))
    if field == "expected_query":
        return bool(q.get("expected_query"))
    if field == "examples":
        return bool(q.get("examples"))
    if field == "edge_cases":
        return bool(q.get("edge_cases"))
    if field == "difficulty":
        return bool(str(q.get("difficulty") or "").strip())
    if field == "pattern":
        return bool(str(q.get("pattern") or "").strip())
    if field == "skill":
        return bool(str(q.get("skill") or q.get("skills") or q.get("topic") or q.get("sub_topic") or "").strip())
    if field == "placement_relevance":
        return bool(str(q.get("provenance") or q.get("companies") or q.get("role") or q.get("roles") or "").strip())
    if field == "expected_thinking":
        return bool(str(q.get("expected_thinking") or q.get("thinking") or "").strip())
    if field == "hints":
        h = q.get("hints")
        return bool(h and (isinstance(h, (list, tuple)) and len(h) > 0))
    if field == "solution":
        s = q.get("solution")
        if isinstance(s, dict):
            return bool(s.get("code") or s.get("explanation"))
        return bool(s)
    if field == "complexity":
        return bool(str(q.get("complexity") or q.get("expected_time_complexity") or q.get("expected_space_complexity") or "").strip())
    if field == "follow_up":
        return bool(str(q.get("follow_up") or "").strip())
    if field == "interview_explanation":
        return bool(str(q.get("interview_explanation") or q.get("explanation") or "").strip())
    if field == "common_trap":
        return bool(str(q.get("common_trap") or "").strip())
    if field == "reasoning_steps":
        return bool(q.get("reasoning_steps"))
    if field == "buggy_code":
        return bool(str(q.get("buggy_code") or "").strip())
    if field == "correct_code":
        return bool(str(q.get("correct_code") or "").strip())
    if field == "expected_behaviour":
        return bool(str(q.get("expected_behaviour") or q.get("expected_behavior") or "").strip())
    if field == "logs_or_error":
        return bool(str(q.get("logs_or_error") or q.get("logs") or "").strip())
    if field == "rubric":
        return bool(str(q.get("rubric") or q.get("evaluation_criteria") or "").strip())
    if field == "requirements":
        return bool(q.get("requirements"))
    if field == "architecture":
        return bool(q.get("architecture") or q.get("components") or q.get("components_list"))
    if field == "constraints":
        return bool(str(q.get("constraints") or "").strip())
    if field == "trade_offs":
        return bool(str(q.get("trade_offs") or "").strip())
    if field == "reliability":
        return bool(str(q.get("reliability") or q.get("scalability") or "").strip())
    if field == "competency":
        return bool(str(q.get("competency") or "").strip())
    if field == "star_framework":
        return bool(str(q.get("star_framework") or q.get("response_framework") or "").strip())
    if field == "evaluation_criteria":
        return bool(str(q.get("evaluation_criteria") or "").strip())
    if field == "passage":
        return bool(str(q.get("passage") or q.get("text") or "").strip())
    return False


def _field_weight(q: dict, field: str, field_specs: List[Dict[str, Any]]) -> int:
    """Get the weight for a field from the type-specific field map."""
    for f in field_specs:
        if f["field"] == field:
            return f.get("weight", 5)
    return 0


# =============================================================================
# Phase 1 — Structural completeness validation per type
# =============================================================================

def validate_structure(q: dict) -> Dict[str, Any]:
    """
    Validate structural completeness against the question type's schema.

    Returns a dict with:
      - score: 0-100 (weighted field presence, only applicable fields counted)
      - required_missing: list of required field labels that are absent
      - optional_missing: list of optional field labels that are absent
      - inapplicable: list of fields that don't apply to this type
      - per_field: per-field presence breakdown

    A question with all required fields present but missing optional fields
    can still score high; optional fields contribute partial weight.
    """
    qtype = str(q.get("type", "coding")).lower()
    field_specs = QUESTION_TYPE_SCHEMAS.get(qtype, QUESTION_TYPE_SCHEMAS["coding"])
    inapplicable = set(INAPPLICABLE_FIELDS.get(qtype, []))

    present = {}
    required_missing = []
    optional_missing = []
    per_field = []

    for f in field_specs:
        fname = f["field"]
        if fname in inapplicable:
            continue  # skip inapplicable fields entirely
        is_present = _field_present(q, fname)
        present[fname] = is_present
        per_field.append({
            "field": fname,
            "label": f["label"],
            "required": f["required"],
            "weight": f["weight"],
            "present": is_present,
        })
        if not is_present:
            if f["required"]:
                required_missing.append(f["label"])
            else:
                optional_missing.append(f["label"])

    # Weighted score counting only applicable fields
    total_weight = sum(f["weight"] for f in field_specs if f["field"] not in inapplicable)
    earned = sum(f["weight"] for f in field_specs
                 if f["field"] not in inapplicable and present.get(f["field"]))
    score = round((earned / total_weight) * 100) if total_weight > 0 else 0

    return {
        "question_type": qtype,
        "score": score,
        "required_missing": required_missing,
        "optional_missing": optional_missing,
        "inapplicable": sorted(inapplicable),
        "per_field": per_field,
        "all_required_present": len(required_missing) == 0,
    }


# =============================================================================
# Phase 2 — Answer correctness validation (where automatable)
# =============================================================================

def validate_answer_correctness(q: dict) -> Dict[str, Any]:
    """
    Validate answer correctness where automation is possible.

    For coding/SQL/debugging: runs the reference solution against test cases.
    For MCQ types: validates that correct_answer is within options range.
    For system_design/interview/behavioral: correctness is not automatable
      (returns None with evidence "requires_human_review").

    Returns:
      - score: 0-100 or None (None = not automatable, requires human review)
      - passed: int
      - total: int
      - details: list of per-check details
      - automatable: bool
    """
    qtype = str(q.get("type", "")).lower()

    # Coding / SQL / Debugging: execute reference solution against test cases
    if qtype in EXECUTABLE_TYPES:
        return _validate_code_correctness(q)

    # Rubric-based types: correctness not automatable (check BEFORE MCQ_TYPES
    # because behavioral is in both MCQ_TYPES and RUBRIC_TYPES conceptually,
    # but its correctness is human-evaluated, not auto-checkable)
    if qtype in RUBRIC_TYPES or qtype == "behavioral":
        return {
            "score": None,
            "passed": 0,
            "total": 0,
            "automatable": False,
            "details": [{
                "check": "answer_correctness",
                "pass": None,
                "detail": "Answer correctness not automatable for rubric-based type; requires human review",
            }],
        }

    # MCQ types: validate answer key is within options
    if qtype in MCQ_TYPES:
        return _validate_mcq_answer(q)

    return {
        "score": None,
        "passed": 0,
        "total": 0,
        "automatable": False,
        "details": [{
            "check": "answer_correctness",
            "pass": None,
            "detail": f"No automated correctness check defined for type '{qtype}'",
        }],
    }


def _validate_code_correctness(q: dict) -> Dict[str, Any]:
    """Validate coding/SQL/debugging correctness by running the reference solution."""
    from app.services.code_executor import CodeExecutionEngine

    engine = CodeExecutionEngine()
    details = []
    passed = 0
    total = 0

    # Extract reference solution code
    sol = q.get("solution")
    code = ""
    language = "python"
    if isinstance(sol, dict):
        code = str(sol.get("code", ""))
        language = str(sol.get("language", "python"))
    elif isinstance(sol, str):
        code = sol

    # Extract test cases
    test_cases = q.get("test_cases") or q.get("testcases") or []
    hidden = q.get("hidden_testcases") or q.get("hidden_test_cases") or []
    all_test_cases = list(test_cases) + list(hidden)

    if not code:
        details.append({
            "check": "solution_code_present",
            "pass": False,
            "detail": "No reference solution code found",
        })
        return {"score": 0, "passed": 0, "total": 1, "automatable": True, "details": details}

    if not all_test_cases:
        details.append({
            "check": "test_cases_present",
            "pass": False,
            "detail": "No test cases to validate against",
        })
        return {"score": 0, "passed": 0, "total": 1, "automatable": True, "details": details}

    # Run solution against each test case
    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    for i, tc in enumerate(all_test_cases):
        total += 1
        try:
            result = loop.run_until_complete(
                engine.execute_against_test_cases(
                    code, language, [tc], q.get("function_name", "")
                )
            )
            if result.get("all_passed"):
                passed += 1
                details.append({
                    "check": f"test_case_{i}",
                    "pass": True,
                    "detail": "Test case passed",
                })
            else:
                details.append({
                    "check": f"test_case_{i}",
                    "pass": False,
                    "detail": f"{result.get('passed_count', 0)}/{result.get('total_count', 1)} assertions passed",
                })
        except Exception as exc:
            details.append({
                "check": f"test_case_{i}",
                "pass": False,
                "detail": f"Execution error: {str(exc)[:200]}",
            })

    score = round((passed / total) * 100) if total > 0 else 0
    return {
        "score": score,
        "passed": passed,
        "total": total,
        "automatable": True,
        "details": details,
    }


def _validate_mcq_answer(q: dict) -> Dict[str, Any]:
    """Validate MCQ answer key is within valid options range."""
    details = []
    options = q.get("options")
    correct = str(q.get("correct_answer") or q.get("correct_index") or "").strip().upper()

    if not options:
        details.append({
            "check": "options_present",
            "pass": False,
            "detail": "No options defined",
        })
        return {"score": 0, "passed": 0, "total": 1, "automatable": True, "details": details}

    if isinstance(options, dict):
        valid_keys = set(options.keys())
        if correct in ("A", "B", "C", "D") and correct in valid_keys:
            details.append({
                "check": "answer_key_valid",
                "pass": True,
                "detail": f"Answer '{correct}' is a valid option key",
            })
            return {"score": 100, "passed": 1, "total": 1, "automatable": True, "details": details}
        else:
            details.append({
                "check": "answer_key_valid",
                "pass": False,
                "detail": f"Answer '{correct}' is not a valid option key (valid: {sorted(valid_keys)})",
            })
            return {"score": 0, "passed": 0, "total": 1, "automatable": True, "details": details}

    if isinstance(options, list):
        correct_idx = q.get("correct_index")
        correct_text = str(q.get("correct_answer") or "").strip()
        if isinstance(correct_idx, int) and 0 <= correct_idx < len(options):
            details.append({
                "check": "answer_index_valid",
                "pass": True,
                "detail": f"Answer index {correct_idx} is within range [0, {len(options)})",
            })
            return {"score": 100, "passed": 1, "total": 1, "automatable": True, "details": details}
        if correct_text and correct_text in [str(o).strip() for o in options]:
            details.append({
                "check": "answer_text_valid",
                "pass": True,
                "detail": "Answer text matches an option",
            })
            return {"score": 100, "passed": 1, "total": 1, "automatable": True, "details": details}
        details.append({
            "check": "answer_valid",
            "pass": False,
            "detail": "No valid answer index or matching answer text found",
        })
        return {"score": 0, "passed": 0, "total": 1, "automatable": True, "details": details}

    details.append({
        "check": "options_format",
        "pass": False,
        "detail": "Options format not recognized",
    })
    return {"score": 0, "passed": 0, "total": 1, "automatable": True, "details": details}


# =============================================================================
# Phase 2 — Executability validation
# =============================================================================

def validate_executability(q: dict) -> Dict[str, Any]:
    """
    Validate that a question can actually be executed/graded.

    Separate from structural completeness: a question can have all fields
    but still fail executability (e.g., MCQ with correct_answer='Z').
    """
    qtype = str(q.get("type", "")).lower()
    details = []
    checks_passed = 0
    checks_total = 0

    # Has question text
    checks_total += 1
    if _field_present(q, "question"):
        checks_passed += 1
        details.append({"check": "has_question_text", "pass": True, "detail": "Question text present"})
    else:
        details.append({"check": "has_question_text", "pass": False, "detail": "Missing question text"})

    # Type-specific executable checks
    if qtype in EXECUTABLE_TYPES:
        checks_total += 1
        tcs = q.get("test_cases") or q.get("testcases") or []
        if tcs:
            checks_passed += 1
            details.append({"check": "has_test_cases", "pass": True, "detail": f"{len(tcs)} test case(s)"})
        else:
            details.append({"check": "has_test_cases", "pass": False, "detail": "No test cases"})
        if qtype == "sql":
            checks_total += 1
            if q.get("sql_schema"):
                checks_passed += 1
                details.append({"check": "has_sql_schema", "pass": True, "detail": "SQL schema present"})
            else:
                details.append({"check": "has_sql_schema", "pass": False, "detail": "Missing SQL schema"})

    elif qtype in MCQ_TYPES:
        checks_total += 1
        options = q.get("options")
        correct = str(q.get("correct_answer") or q.get("correct_index") or "").strip().upper()
        if isinstance(options, dict) and len(options) >= 4 and correct in ("A", "B", "C", "D"):
            checks_passed += 1
            details.append({"check": "mcq_valid", "pass": True, "detail": "Valid MCQ with 4+ options and A-D answer"})
        elif isinstance(options, list) and len(options) >= 4:
            checks_passed += 1
            details.append({"check": "mcq_valid", "pass": True, "detail": "Valid list-style MCQ"})
        else:
            details.append({"check": "mcq_valid", "pass": False, "detail": "MCQ missing valid options or answer"})

    elif qtype in RUBRIC_TYPES:
        checks_total += 1
        if q.get("rubric") or q.get("evaluation_criteria") or q.get("worked_solution"):
            checks_passed += 1
            details.append({"check": "has_rubric", "pass": True, "detail": "Evaluation rubric present"})
        else:
            details.append({"check": "has_rubric", "pass": False, "detail": "Missing evaluation rubric"})

    score = round((checks_passed / checks_total) * 100) if checks_total > 0 else 0
    return {
        "score": score,
        "passed": checks_passed,
        "total": checks_total,
        "executable": score == 100,
        "details": details,
    }


# =============================================================================
# Phase 2 — Full quality assessment (all independent dimensions)
# =============================================================================

def assess_quality(q: dict) -> QualityDimensions:
    """
    Perform a full quality assessment across all independent dimensions.

    Returns a QualityDimensions object with separate scores for each
    dimension. No single combined score is produced.

    Usage:
        dims = assess_quality(q)
        # dims.structural_completeness  # 0-100 or None
        # dims.answer_correctness       # 0-100 or None (not automatable)
        # dims.to_dict()                # serializable dict
    """
    qtype = str(q.get("type", "coding")).lower()
    dims = QualityDimensions(question_type=qtype)

    # 1. Structural completeness
    struct = validate_structure(q)
    dims.structural_completeness = struct["score"]
    dims.evidence["structural"] = {
        "required_missing": struct["required_missing"],
        "optional_missing": struct["optional_missing"],
        "all_required_present": struct["all_required_present"],
    }

    # 2. Answer correctness
    correctness = validate_answer_correctness(q)
    if correctness["automatable"]:
        dims.answer_correctness = correctness["score"]
    else:
        dims.answer_correctness = None  # requires human review
    dims.evidence["answer_correctness"] = {
        "automatable": correctness["automatable"],
        "passed": correctness["passed"],
        "total": correctness["total"],
        "details": correctness["details"],
    }

    # 3. Explanation correctness (heuristic: explanation present and non-trivial)
    checks_total = 1
    checks_passed = 0
    if _field_present(q, "explanation") or qtype in RUBRIC_TYPES:
        checks_passed += 1
    if qtype in RUBRIC_TYPES:
        # For rubric types, rubric serves as explanation
        if q.get("rubric") or q.get("evaluation_criteria"):
            checks_passed += 1
        else:
            checks_total += 1  # rubric already counted above; adjust
    dims.explanation_correctness = round((checks_passed / checks_total) * 100) if checks_total > 0 else None

    # 4. Executability
    exec_result = validate_executability(q)
    dims.executability = exec_result["score"]
    dims.evidence["executability"] = {
        "executable": exec_result["executable"],
        "details": exec_result["details"],
    }

    # 5. Difficulty accuracy (heuristic: difficulty present and valid)
    diff = str(q.get("difficulty") or "").strip().lower()
    if diff in ("easy", "medium", "hard"):
        dims.difficulty_accuracy = 100
    elif diff:
        dims.difficulty_accuracy = 50  # present but unrecognized value
    else:
        dims.difficulty_accuracy = 0

    # 6. Skill alignment (heuristic: skill/topic present)
    if _field_present(q, "skill"):
        dims.skill_alignment = 100
    else:
        dims.skill_alignment = 0

    # 7. Placement relevance (heuristic: provenance/company/role present)
    if _field_present(q, "placement_relevance"):
        dims.placement_relevance = 100
    else:
        dims.placement_relevance = 0

    # 8. Originality (heuristic: not a duplicate — set by caller, default neutral)
    dims.originality = None  # set by dedupe/duplicate detection

    # 9. Assessment usefulness (derived from structural + correctness + executability)
    components = [dims.structural_completeness or 0,
                  dims.answer_correctness or 0,
                  dims.executability or 0]
    dims.assessment_usefulness = round(sum(components) / len(components)) if components else 0

    return dims


# =============================================================================
# Legacy scoring API (backward compatible)
# =============================================================================

def score_question(q: dict) -> Dict[str, Any]:
    """Score a question against its type-specific standard.

    Returns a dict with score, tier, per-field breakdown, and type-specific
    missing fields. Does NOT consider trust status - that's a separate
    dimension handled by question_store.transition_trust().
    """
    qtype = str(q.get("type", "coding")).lower()
    field_specs = QUESTION_TYPE_SCHEMAS.get(qtype, QUESTION_TYPE_SCHEMAS["coding"])

    result = _score_question_type(q, field_specs)
    result["question_type"] = qtype
    result["question_id"] = str(q.get("id", ""))

    # Tier classification based on score
    if result["score"] >= 90:
        result["quality_tier"] = "premium"
    elif result["score"] >= 60:
        result["quality_tier"] = "solid"
    else:
        result["quality_tier"] = "bronze"

    return result


def _score_question_type(q: dict, field_specs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Score a question against a specific type's schema."""
    present = {}
    for f in field_specs:
        fname = f["field"]
        present[fname] = _field_present(q, fname)

    total_weight = sum(f["weight"] for f in field_specs)
    earned = sum(f["weight"] for f in field_specs if present.get(f["field"]))

    score = round((earned / total_weight) * 100) if total_weight > 0 else 0

    return {
        "score": score,
        "total_fields": len(field_specs),
        "present_fields": sum(1 for v in present.values() if v),
        "missing": [f["label"] for f in field_specs if not present.get(f["field"])],
        "fields": [
            {"label": f["label"], "weight": f["weight"], "present": present.get(f["field"])}
            for f in field_specs
        ],
    }


def tier_for_score(score: int) -> str:
    """Classify a question's quality tier.

    - premium : 90+
    - solid   : 60-89
    - bronze  : < 60
    """
    if score >= 90:
        return "premium"
    if score >= 60:
        return "solid"
    return "bronze"


# =============================================================================
# Aggregation helpers
# =============================================================================

def score_all_servable(questions: List[dict]) -> Dict[str, Any]:
    """Score all servable questions and return aggregated quality metrics."""
    scores = {"premium": 0, "solid": 0, "bronze": 0}
    missing_fields_total = Counter()
    scored_questions = []

    for q in questions:
        result = score_question(q)
        tier = result["quality_tier"]
        scores[tier] += 1
        scored_questions.append({
            "id": q.get("id"),
            "type": q.get("type"),
            "topic": q.get("topic"),
            "score": result["score"],
            "tier": result["quality_tier"],
            "missing": result["missing"],
        })
        for f in result["fields"]:
            if not f["present"]:
                missing_fields_total[f["label"]] += 1

    return {
        "scores": scores,
        "total_servable": len(questions),
        "scored_questions": scored_questions,
        "missing_fields_total": dict(missing_fields_total),
    }


def get_servable_questions(questions: List[dict]) -> List[dict]:
    """Filter to only servable questions."""
    return [q for q in questions if _is_servable(q)]


def _is_servable(q: dict) -> bool:
    """Check if a question is servable (verified/reviewed + executable)."""
    trust = str(q.get("trust_status", "unverified")).lower()
    if trust not in ("verified", "reviewed"):
        return False
    return _is_executable(q)


def _is_executable(q: dict) -> bool:
    """Check if a question can actually be evaluated/graded."""
    qtype = str(q.get("type", "")).lower()

    # Coding/SQL/Debugging require test cases
    if qtype in ("coding", "sql", "debugging"):
        tcs = q.get("test_cases") or q.get("testcases") or []
        if not tcs:
            return False
        if qtype == "sql" and not q.get("sql_schema"):
            return False
        return True

    # MCQs require a valid correct_answer
    if qtype in ("aptitude", "logical", "verbal", "hr", "behavioral", "cs_fundamentals", "cs"):
        options = q.get("options")
        correct = str(q.get("correct_answer") or q.get("correct_index") or "").strip().upper()

        if isinstance(options, list) and len(options) >= 4:
            correct_idx = q.get("correct_index")
            if isinstance(correct_idx, int) and 0 <= correct_idx < len(options):
                return True
            if correct and correct in [str(o).strip() for o in options]:
                return True
            return False

        if isinstance(options, dict) and len(options) >= 4:
            return correct in ("A", "B", "C", "D")

        return False

    # Interview/system_design require rubric
    if qtype in ("interview", "system_design", "gd", "group_discussion"):
        return bool(q.get("rubric") or q.get("evaluation_criteria") or q.get("worked_solution"))

    # Default: require test cases or some form of answer key
    tcs = q.get("test_cases") or q.get("testcases") or []
    return len(tcs) > 0 or bool(q.get("correct_answer") or q.get("answer") or q.get("solution"))


def get_all_questions() -> List[dict]:
    """Get all questions from the question store."""
    from app.services import question_store
    question_store.load_all()
    return question_store._questions


def get_trust_state_breakdown(questions: List[dict]) -> Dict[str, int]:
    """Get breakdown of questions by trust status."""
    return Counter(str(q.get("trust_status", "unverified")).lower() for q in questions)


def get_servable_breakdown(questions: List[dict]) -> Dict[str, int]:
    """Get breakdown of servable questions by trust status."""
    return Counter(str(q.get("trust_status", "unverified")).lower() for q in questions if _is_servable(q))


def get_domain_servable_counts(questions: List[dict]) -> Dict[str, int]:
    """Get servable counts per domain."""
    domain_map = {
        'coding': 'DSA Coding',
        'sql': 'SQL',
        'aptitude': 'Quantitative Aptitude',
        'logical': 'Logical Reasoning',
        'verbal': 'Verbal Ability',
        'cs_fundamentals': 'CS Fundamentals',
        'cs': 'CS Fundamentals',
        'debugging': 'Debugging',
        'system_design': 'System Design',
        'interview': 'Behavioral/Interview',
        'behavioral': 'Behavioral/Interview',
        'hr': 'Behavioral/Interview',
    }
    domain_servable = defaultdict(int)
    for q in questions:
        if _is_servable(q):
            dtype = str(q.get('type', 'coding')).lower()
            domain = domain_map.get(dtype, 'Other')
            domain_servable[domain] += 1
    return dict(domain_servable)


def get_domain_total_counts(questions: List[dict]) -> Dict[str, int]:
    """Get total question counts per domain."""
    domain_map = {
        'coding': 'DSA Coding',
        'sql': 'SQL',
        'aptitude': 'Quantitative Aptitude',
        'logical': 'Logical Reasoning',
        'verbal': 'Verbal Ability',
        'cs_fundamentals': 'CS Fundamentals',
        'cs': 'CS Fundamentals',
        'debugging': 'Debugging',
        'system_design': 'System Design',
        'interview': 'Behavioral/Interview',
        'behavioral': 'Behavioral/Interview',
        'hr': 'Behavioral/Interview',
    }
    domain_total = defaultdict(int)
    for q in questions:
        dtype = str(q.get('type', 'coding')).lower()
        domain = domain_map.get(dtype, 'Other')
        domain_total[domain] += 1
    return dict(domain_total)
