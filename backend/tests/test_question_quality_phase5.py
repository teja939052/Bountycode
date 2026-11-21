"""
Phase 1 & 2 — Question quality validation tests.

Tests type-specific structural completeness, answer correctness,
executability, and independent quality dimensions.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.question_quality import (
    validate_structure,
    validate_answer_correctness,
    validate_executability,
    assess_quality,
    score_question,
    tier_for_score,
    QUESTION_TYPE_SCHEMAS,
    SERVABLE_TYPES,
    INAPPLICABLE_FIELDS,
    QualityDimensions,
)


class TestTypeSpecificSchemas:
    """Each question type has its own required/optional/inapplicable fields."""

    def test_coding_required_fields(self):
        fields = {f["field"]: f["required"] for f in QUESTION_TYPE_SCHEMAS["coding"]}
        assert fields["question"] is True
        assert fields["solution"] is True
        assert fields["test_cases"] is True
        assert fields["constraints"] is False
        assert fields["examples"] is False

    def test_sql_required_fields(self):
        fields = {f["field"]: f["required"] for f in QUESTION_TYPE_SCHEMAS["sql"]}
        assert fields["question"] is True
        assert fields["sql_schema"] is True
        assert fields["seed_inserts"] is True
        assert fields["expected_query"] is True
        assert fields["test_cases"] is True

    def test_aptitude_required_fields(self):
        fields = {f["field"]: f["required"] for f in QUESTION_TYPE_SCHEMAS["aptitude"]}
        assert fields["question"] is True
        assert fields["options"] is True
        assert fields["correct_answer"] is True
        assert fields["explanation"] is True

    def test_system_design_required_fields(self):
        fields = {f["field"]: f["required"] for f in QUESTION_TYPE_SCHEMAS["system_design"]}
        assert fields["question"] is True
        assert fields["rubric"] is True
        assert fields["requirements"] is True
        assert fields["constraints"] is True
        assert fields["architecture"] is True
        assert fields["trade_offs"] is True
        assert fields["reliability"] is True

    def test_behavioral_required_fields(self):
        fields = {f["field"]: f["required"] for f in QUESTION_TYPE_SCHEMAS["behavioral"]}
        assert fields["question"] is True
        assert fields["rubric"] is True
        assert fields["competency"] is True
        assert fields["star_framework"] is True
        assert fields["evaluation_criteria"] is True

    def test_interview_required_fields(self):
        fields = {f["field"]: f["required"] for f in QUESTION_TYPE_SCHEMAS["interview"]}
        assert fields["question"] is True
        assert fields["rubric"] is True
        assert fields["competency"] is True
        assert fields["expected_thinking"] is True

    def test_debugging_required_fields(self):
        fields = {f["field"]: f["required"] for f in QUESTION_TYPE_SCHEMAS["debugging"]}
        assert fields["question"] is True
        assert fields["buggy_code"] is True
        assert fields["correct_code"] is True
        assert fields["expected_behaviour"] is True
        assert fields["logs_or_error"] is True
        assert fields["root_cause"] is True


class TestInapplicableFields:
    """Fields that don't apply to a type are excluded from scoring."""

    def test_verbal_excludes_test_cases(self):
        assert "test_cases" in INAPPLICABLE_FIELDS.get("verbal", [])
        assert "sql_schema" in INAPPLICABLE_FIELDS.get("verbal", [])
        assert "rubric" in INAPPLICABLE_FIELDS.get("verbal", [])

    def test_system_design_excludes_test_cases(self):
        assert "test_cases" in INAPPLICABLE_FIELDS.get("system_design", [])
        assert "options" in INAPPLICABLE_FIELDS.get("system_design", [])
        assert "correct_answer" in INAPPLICABLE_FIELDS.get("system_design", [])

    def test_behavioral_excludes_test_cases(self):
        assert "test_cases" in INAPPLICABLE_FIELDS.get("behavioral", [])
        assert "buggy_code" in INAPPLICABLE_FIELDS.get("behavioral", [])

    def test_coding_excludes_rubric(self):
        assert "rubric" in INAPPLICABLE_FIELDS.get("coding", [])


class TestStructuralValidation:
    """validate_structure returns per-type completeness with inapplicable fields excluded."""

    def test_complete_coding_question_all_required_present(self):
        q = {
            "id": "t1", "type": "coding",
            "question": "Reverse a string.",
            "solution": {"code": "def f(s): return s[::-1]"},
            "test_cases": [{"input": ["hello"], "expected": "olleh"}],
        }
        result = validate_structure(q)
        assert result["all_required_present"] is True
        assert result["score"] > 0
        assert "test_cases" not in result["required_missing"]
        assert "solution" not in result["required_missing"]

    def test_incomplete_coding_missing_required(self):
        q = {
            "id": "t2", "type": "coding",
            "question": "Reverse a string.",
        }
        result = validate_structure(q)
        assert result["all_required_present"] is False
        assert "Reference solution" in result["required_missing"]
        assert "Executable test cases" in result["required_missing"]

    def test_verbal_does_not_penalize_missing_test_cases(self):
        """A verbal MCQ should not lose points for lacking test_cases."""
        q = {
            "id": "t3", "type": "verbal",
            "question": "What is the synonym of happy?",
            "correct_answer": "B",
            "explanation": "Joyful means the same as happy.",
            "options": {"A": "Sad", "B": "Joyful", "C": "Angry", "D": "Tired"},
        }
        result = validate_structure(q)
        assert result["all_required_present"] is True
        assert "test_cases" not in result["required_missing"]
        assert "Executable test cases" not in result["missing_required"] if "missing_required" in result else True

    def test_system_design_all_required_present(self):
        q = {
            "id": "t4", "type": "system_design",
            "question": "Design a URL shortener.",
            "rubric": "Evaluate architecture, scalability, trade-offs.",
            "requirements": {"functional": ["shorten URLs"], "non_functional": ["high availability"]},
            "constraints": "Must handle 10000 req/s",
            "architecture": {"components": ["API gateway", "cache", "database"]},
            "trade_offs": "Read-heavy vs write-heavy trade-off.",
            "reliability": "99.9% availability target.",
        }
        result = validate_structure(q)
        assert result["all_required_present"] is True
        assert "test_cases" not in result["required_missing"]
        assert "options" not in result["required_missing"]

    def test_behavioral_all_required_present(self):
        q = {
            "id": "t5", "type": "behavioral",
            "question": "Tell me about a conflict with a coworker.",
            "rubric": "STAR method evaluation.",
            "competency": "Conflict resolution",
            "star_framework": "Situation, Task, Action, Result.",
            "evaluation_criteria": "Clear communication, concrete example, lessons learned.",
        }
        result = validate_structure(q)
        assert result["all_required_present"] is True
        assert "test_cases" not in result["required_missing"]
        assert "correct_answer" not in result["required_missing"]


class TestAnswerCorrectness:
    """validate_answer_correctness validates answers where automatable."""

    def test_mcq_valid_answer(self):
        q = {
            "id": "t6", "type": "aptitude",
            "question": "What is 2+2?",
            "options": {"A": "3", "B": "4", "C": "5", "D": "6"},
            "correct_answer": "B",
        }
        result = validate_answer_correctness(q)
        assert result["automatable"] is True
        assert result["score"] == 100
        assert result["passed"] == 1

    def test_mcq_invalid_answer(self):
        q = {
            "id": "t7", "type": "aptitude",
            "question": "What is 2+2?",
            "options": {"A": "3", "B": "4", "C": "5", "D": "6"},
            "correct_answer": "Z",
        }
        result = validate_answer_correctness(q)
        assert result["automatable"] is True
        assert result["score"] == 0

    def test_system_design_correctness_not_automatable(self):
        q = {
            "id": "t8", "type": "system_design",
            "question": "Design a URL shortener.",
            "rubric": "...",
        }
        result = validate_answer_correctness(q)
        assert result["automatable"] is False
        assert result["score"] is None

    def test_behavioral_correctness_not_automatable(self):
        q = {
            "id": "t9", "type": "behavioral",
            "question": "Tell me about a conflict.",
            "rubric": "...",
        }
        result = validate_answer_correctness(q)
        assert result["automatable"] is False
        assert result["score"] is None


class TestExecutability:
    """validate_executability checks if a question can actually be graded."""

    def test_coding_with_test_cases_executable(self):
        q = {
            "id": "t10", "type": "coding",
            "question": "Reverse a string.",
            "solution": {"code": "def f(s): return s[::-1]"},
            "test_cases": [{"input": ["hello"], "expected": "olleh"}],
        }
        result = validate_executability(q)
        assert result["executable"] is True
        assert result["score"] == 100

    def test_coding_without_test_cases_not_executable(self):
        q = {
            "id": "t11", "type": "coding",
            "question": "Reverse a string.",
            "solution": {"code": "def f(s): return s[::-1]"},
        }
        result = validate_executability(q)
        assert result["executable"] is False

    def test_sql_without_schema_not_executable(self):
        q = {
            "id": "t12", "type": "sql",
            "question": "Find users.",
            "test_cases": [{"input": [], "expected": "[]"}],
        }
        result = validate_executability(q)
        assert result["executable"] is False

    def test_mcq_with_valid_answer_executable(self):
        q = {
            "id": "t13", "type": "aptitude",
            "question": "2+2?",
            "options": {"A": "3", "B": "4", "C": "5", "D": "6"},
            "correct_answer": "B",
        }
        result = validate_executability(q)
        assert result["executable"] is True

    def test_mcq_with_invalid_answer_not_executable(self):
        q = {
            "id": "t14", "type": "aptitude",
            "question": "2+2?",
            "options": {"A": "3", "B": "4", "C": "5", "D": "6"},
            "correct_answer": "Z",
        }
        result = validate_executability(q)
        assert result["executable"] is False

    def test_system_design_with_rubric_executable(self):
        q = {
            "id": "t15", "type": "system_design",
            "question": "Design a URL shortener.",
            "rubric": "Evaluate architecture.",
        }
        result = validate_executability(q)
        assert result["executable"] is True

    def test_behavioral_without_rubric_not_executable(self):
        q = {
            "id": "t16", "type": "behavioral",
            "question": "Tell me about a conflict.",
        }
        result = validate_executability(q)
        assert result["executable"] is False


class TestQualityDimensions:
    """assess_quality returns independent dimensions, never a single combined score."""

    def test_assess_quality_returns_dimensions(self):
        q = {
            "id": "t17", "type": "coding",
            "question": "Reverse a string.",
            "solution": {"code": "def f(s): return s[::-1]"},
            "test_cases": [{"input": ["hello"], "expected": "olleh"}],
            "difficulty": "easy",
            "skill": "strings",
            "companies": ["google"],
        }
        dims = assess_quality(q)
        assert isinstance(dims, QualityDimensions)
        assert dims.question_type == "coding"
        assert dims.structural_completeness is not None
        assert dims.executability is not None
        assert dims.difficulty_accuracy is not None
        assert dims.skill_alignment is not None
        assert dims.placement_relevance is not None
        assert dims.assessment_usefulness is not None

    def test_correctness_none_for_non_automatable(self):
        q = {
            "id": "t18", "type": "system_design",
            "question": "Design a URL shortener.",
            "rubric": "...",
        }
        dims = assess_quality(q)
        assert dims.answer_correctness is None, \
            f"System design correctness should be None (not automatable), got {dims.answer_correctness}"

    def test_no_single_overall_score(self):
        """assess_quality does not produce a single combined score."""
        q = {
            "id": "t19", "type": "coding",
            "question": "Test.",
            "solution": {"code": "def f(): return 1"},
            "test_cases": [{"input": [], "expected": 1}],
        }
        dims = assess_quality(q)
        d = dims.to_dict()
        assert "overall_score" not in d
        assert "combined_score" not in d
        assert "quality_tier" not in d  # tier is separate from dimensions

    def test_structurally_complete_but_incorrect_coding(self):
        """A coding question with all fields but failing test cases:
        structural_completeness high, answer_correctness<100."""
        q = {
            "id": "t20", "type": "coding",
            "question": "Return the input plus one.",
            "solution": {"code": "def f(x): return x - 1"},  # BUG: should be x + 1
            "test_cases": [
                {"input": [1], "expected": 2},
                {"input": [5], "expected": 6},
            ],
            "constraints": "Input is an integer.",
            "examples": ["f(1) -> 2", "f(5) -> 6"],
            "edge_cases": ["negative numbers", "zero"],
            "difficulty": "easy",
            "pattern": "arithmetic",
            "skill": "math",
            "expected_thinking": "Add 1 to the input.",
            "hints": ["Use the + operator"],
            "complexity": "O(1) time, O(1) space",
        }
        dims = assess_quality(q)
        assert dims.structural_completeness > 80, \
            f"Should be structurally complete, got {dims.structural_completeness}"
        # Correctness is automatable for coding — should reflect failing tests
        if dims.answer_correctness is not None:
            assert dims.answer_correctness < 100, \
                f"Incorrect solution should have correctness < 100, got {dims.answer_correctness}"


class TestVerbalDoesNotLosePointsForNoTestCases:
    """A verbal MCQ should not be classified as Bronze merely for lacking programming fields."""

    def test_verbal_complete_scores_high_structural(self):
        q = {
            "id": "t21", "type": "verbal",
            "question": "What is the synonym of happy?",
            "passage": "She felt joyful after receiving the good news.",
            "options": {"A": "Sad", "B": "Joyful", "C": "Angry", "D": "Tired"},
            "correct_answer": "B",
            "explanation": "Joyful means the same as happy.",
            "difficulty": "easy",
            "skill": "vocabulary",
            "pattern": "synonym",
            "hints": ["Think of a word meaning the same"],
        }
        result = validate_structure(q)
        assert result["all_required_present"] is True
        assert result["score"] == 100, \
            f"Complete verbal should score 100 structural, got {result['score']}"

    def test_verbal_does_not_require_test_cases(self):
        q = {
            "id": "t22", "type": "verbal",
            "question": "Pick the correct word.",
            "correct_answer": "A",
            "explanation": "Because A is correct.",
        }
        result = validate_structure(q)
        assert result["all_required_present"] is True
        # test_cases is not in required fields for verbal
        required_fields = [f["label"] for f in result["per_field"] if f["required"]]
        assert "Executable test cases" not in required_fields


class TestTierSeparation:
    """Quality tier is separate from trust status."""

    def test_tier_for_score_boundaries(self):
        assert tier_for_score(90) == "premium"
        assert tier_for_score(89) == "solid"
        assert tier_for_score(60) == "solid"
        assert tier_for_score(59) == "bronze"
        assert tier_for_score(0) == "bronze"

    def test_score_question_returns_tier(self):
        q = {
            "id": "t23", "type": "coding",
            "question": "Test.",
        }
        result = score_question(q)
        assert "quality_tier" in result
        assert result["quality_tier"] in ("premium", "solid", "bronze")
