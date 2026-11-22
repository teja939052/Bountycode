"""Tests for question_quality.py - Type-specific question quality validation.

Tests that each question type has its own required fields, that scoring works
correctly per type, and that completeness is separate from correctness.
"""

import pytest
from app.services.question_quality import (
    score_question,
    score_all_servable,
    get_servable_questions,
    get_trust_state_breakdown,
    get_servable_breakdown,
    get_domain_servable_counts,
    get_domain_total_counts,
    tier_for_score,
    _field_present,
    QUESTION_TYPE_SCHEMAS,
    SERVABLE_TYPES,
)
from app.services import question_store
from app.services import question_store


class TestQuestionQualitySchema:
    """Test that each question type has its own required fields."""

    def test_coding_requires_test_cases(self):
        """Coding questions require test_cases field."""
        q = {
            "id": "test-coding-001",
            "type": "coding",
            "question": "Implement a function to reverse a string.",
            "solution": {"code": "def reverse(s): return s[::-1]"},
            "difficulty": "medium",
        }
        assert _field_present(q, "test_cases") is False
        assert _field_present(q, "question") is True
        assert _field_present(q, "solution") is True

    def test_sql_requires_sql_schema(self):
        """SQL questions require sql_schema field."""
        q = {
            "id": "test-sql-001",
            "type": "sql",
            "question": "Find all users.",
            "expected_query": "SELECT * FROM users;",
        }
        assert _field_present(q, "sql_schema") is False
        assert _field_present(q, "question") is True
        assert _field_present(q, "expected_query") is True

    def test_mcq_requires_options(self):
        """MCQ questions require options field."""
        q = {
            "id": "test-mcq-001",
            "type": "aptitude",
            "question": "What is 2+2?",
            "correct_answer": "A",
            "explanation": "2+2 equals 4.",
        }
        assert _field_present(q, "options") is False
        assert _field_present(q, "correct_answer") is True
        assert _field_present(q, "explanation") is True

    def test_logical_requires_correct_answer(self):
        """Logical reasoning questions require correct_answer."""
        q = {
            "id": "test-logical-001",
            "type": "logical",
            "question": "If all A are B, and all B are C, are all A C?",
            "explanation": "Yes, by transitivity.",
        }
        assert _field_present(q, "correct_answer") is False
        assert _field_present(q, "question") is True
        assert _field_present(q, "explanation") is True

    def test_verbal_requires_correct_answer(self):
        """Verbal questions require correct_answer."""
        q = {
            "id": "test-verbal-001",
            "type": "verbal",
            "question": "What is the synonym of happy?",
            "explanation": "Joyful means the same as happy.",
        }
        assert _field_present(q, "correct_answer") is False
        assert _field_present(q, "question") is True
        assert _field_present(q, "explanation") is True

    def test_debugging_requires_buggy_code(self):
        """Debugging questions require buggy_code."""
        q = {
            "id": "test-debug-001",
            "type": "debugging",
            "question": "Fix the bug in this code.",
            "correct_code": "def fix(x): return x + 1",
            "explanation": "The original code was missing +1.",
        }
        assert _field_present(q, "buggy_code") is False
        assert _field_present(q, "correct_code") is True
        assert _field_present(q, "expected_behaviour") is False

    def test_system_design_requires_rubric(self):
        """System design questions require rubric."""
        q = {
            "id": "test-sd-001",
            "type": "system_design",
            "question": "Design a URL shortener.",
        }
        assert _field_present(q, "rubric") is False
        assert _field_present(q, "question") is True

    def test_interview_requires_rubric(self):
        """Interview questions require rubric."""
        q = {
            "id": "test-interview-001",
            "type": "interview",
            "question": "Tell me about a time you failed.",
        }
        assert _field_present(q, "rubric") is False
        assert _field_present(q, "question") is True

    def test_behavioral_requires_rubric(self):
        """Behavioral questions require rubric."""
        q = {
            "id": "test-behavioral-001",
            "type": "behavioral",
            "question": "Tell me about a conflict with a coworker.",
        }
        assert _field_present(q, "rubric") is False
        assert _field_present(q, "question") is True


class TestQuestionQualityScoring:
    """Test scoring against question type standards."""

    def test_complete_coding_question_scores_high(self):
        """A coding question with all required fields scores high."""
        q = {
            "id": "test-coding-002",
            "type": "coding",
            "question": "Implement a function to reverse a string.",
            "solution": {"code": "def reverse(s): return s[::-1]"},
            "test_cases": [{"input": ["hello"], "expected": "olleh"}],
            "constraints": "Input string length <= 1000",
            "examples": ["reverse('hello') -> 'olleh'"],
            "edge_cases": ["empty string returns empty string"],
            "difficulty": "easy",
            "pattern": "two_pointers",
            "skill": "strings",
            "expected_thinking": "Use two pointers to swap characters from both ends.",
            "hints": ["Start from both ends and swap"],
            "complexity": "O(n) time, O(1) space",
            "follow_up": "Can you do it in-place?",
            "interview_explanation": "Explain the two-pointer technique.",
        }
        result = score_question(q)
        assert result["question_type"] == "coding"
        assert result["score"] >= 80  # Should be high score
        assert result["quality_tier"] in ("solid", "premium")
        assert len(result["missing"]) < 5  # Few missing fields

    def test_incomplete_coding_question_scores_low(self):
        """A coding question missing key fields scores low."""
        q = {
            "id": "test-coding-003",
            "type": "coding",
            "question": "Write a function.",
        }
        result = score_question(q)
        assert result["question_type"] == "coding"
        assert result["score"] < 60  # Bronze tier
        assert result["quality_tier"] == "bronze"
        assert len(result["missing"]) > 5  # Many missing fields

    def test_complete_sql_question_scores_high(self):
        """A SQL question with schema, seed data, and expected query scores high."""
        q = {
            "id": "test-sql-002",
            "type": "sql",
            "question": "Find all users.",
            "sql_schema": "CREATE TABLE users (id INT, name VARCHAR(100));",
            "seed_inserts": "INSERT INTO users VALUES (1, 'Alice');",
            "expected_query": "SELECT * FROM users;",
            "test_cases": [{"input": [], "expected": "[(1, 'Alice')]"}],
            "difficulty": "easy",
            "pattern": "select",
            "skill": "sql",
            "explanation": "Simple SELECT from users table.",
        }
        result = score_question(q)
        assert result["question_type"] == "sql"
        assert result["score"] >= 80  # Should be high score
        assert result["quality_tier"] in ("solid", "premium")

    def test_complete_mcq_question_scores_high(self):
        """An MCQ question with options and correct answer scores high."""
        q = {
            "id": "test-aptitude-001",
            "type": "aptitude",
            "question": "What is 2+2?",
            "options": {"A": "3", "B": "4", "C": "5", "D": "6"},
            "correct_answer": "B",
            "explanation": "2+2 equals 4.",
            "difficulty": "easy",
            "skill": "arithmetic",
            "pattern": "arithmetic",
            "hints": ["Think about basic addition"],
            "common_trap": "Don't confuse with multiplication",
            "reasoning_steps": ["2+2 equals 4"],
        }
        result = score_question(q)
        assert result["question_type"] == "aptitude"
        assert result["score"] >= 80  # Should be high score
        assert result["quality_tier"] in ("solid", "premium")

    def test_complete_logical_question_scores_high(self):
        """A logical reasoning question with answer and explanation scores high."""
        q = {
            "id": "test-logical-002",
            "type": "logical",
            "question": "If all A are B, and all B are C, are all A C?",
            "correct_answer": "Yes",
            "explanation": "By transitivity, if all A are B and all B are C, then all A are C.",
            "difficulty": "easy",
            "skill": "syllogism",
            "pattern": "syllogism",
            "hints": ["Think about transitivity"],
            "common_trap": "Don't assume the converse",
            "reasoning_steps": ["All A are B", "All B are C", "Therefore all A are C"],
        }
        result = score_question(q)
        assert result["question_type"] == "logical"
        assert result["score"] >= 80  # Should be high score
        assert result["quality_tier"] in ("solid", "premium")

    def test_complete_verbal_question_scores_high(self):
        """A verbal question with answer and explanation scores high."""
        q = {
            "id": "test-verbal-002",
            "type": "verbal",
            "question": "What is the synonym of happy?",
            "options": {"A": "Sad", "B": "Joyful", "C": "Angry", "D": "Tired"},
            "correct_answer": "B",
            "explanation": "Joyful means the same as happy.",
            "difficulty": "easy",
            "skill": "vocabulary",
            "pattern": "synonym",
            "hints": ["Think of a word meaning the same"],
        }
        result = score_question(q)
        assert result["question_type"] == "verbal"
        assert result["score"] >= 80  # Should be high score
        assert result["quality_tier"] in ("solid", "premium")


class TestQuestionQualityTier:
    """Test tier_for_score function."""

    def test_premium_tier(self):
        assert tier_for_score(90) == "premium"
        assert tier_for_score(95) == "premium"
        assert tier_for_score(100) == "premium"

    def test_solid_tier(self):
        assert tier_for_score(60) == "solid"
        assert tier_for_score(75) == "solid"
        assert tier_for_score(89) == "solid"

    def test_bronze_tier(self):
        assert tier_for_score(0) == "bronze"
        assert tier_for_score(30) == "bronze"
        assert tier_for_score(59) == "bronze"


class TestQuestionQualityIntegration:
    """Integration tests for question quality."""

    def test_servable_questions_have_scores(self):
        """All servable questions should have a score."""
        question_store.load_all()
        from app.services import question_store as qs
        servable = [q for q in question_store._questions if question_store._is_servable(q)]
        assert len(servable) > 0
        for q in servable[:10]:  # Test first 10
            result = score_question(q)
            assert "score" in result
            assert "quality_tier" in result
            assert "missing" in result
            assert result["question_id"] == str(q.get("id", ""))
            assert result["question_type"] == str(q.get("type", "coding")).lower()

    def test_questions_without_required_fields_score_low(self):
        """Questions missing required fields should score low."""
        q = {
            "id": "test-minimal-001",
            "type": "coding",
        }
        result = score_question(q)
        assert result["score"] < 60  # Should be bronze
        assert result["quality_tier"] == "bronze"
        assert len(result["missing"]) > 5  # Many missing fields

    def test_score_against_standard_is_still_available(self):
        """Verify question_quality.score_question still works."""
        q = {
            "id": "test-compat-001",
            "type": "coding",
            "question": "Test question",
            "solution": {"code": "def f(): return 1"},
            "test_cases": [{"input": [], "expected": 1}],
        }
        result = score_question(q)
        assert result["score"] > 0
        assert "total_fields" in result
        assert "missing" in result
        assert "fields" in result


def test_servable_questions_have_scores():
    """Integration test: all servable questions should have scores."""
    question_store.load_all()
    servable = [q for q in question_store._questions if question_store._is_servable(q)]
    assert len(servable) > 0
    for q in servable[:20]:  # Test first 20
        result = score_question(q)
        assert result["score"] >= 0
        assert result["score"] <= 100
        assert result["quality_tier"] in ("premium", "solid", "bronze")
        assert "missing" in result
