import pytest

from app.services.scoring import normalize_answer, score_question


def _q(**kw):
    base = {"id": "q1", "topic": "percentages", "difficulty": "easy",
            "question_type": "mcq", "options": {"A": "1", "B": "2"}, "correct_answer": "B"}
    base.update(kw)
    return base


def test_mcq_correct():
    assert score_question(_q(), "B")["is_correct"] is True


def test_mcq_wrong():
    assert score_question(_q(), "A")["is_correct"] is False


def test_missing_answer():
    r = score_question(_q(), None)
    assert r["is_correct"] is False and r["normalized_answer"] is None


def test_invalid_option():
    assert score_question(_q(), "Z")["is_correct"] is False


def test_case_insensitive():
    assert score_question(_q(), "b")["is_correct"] == score_question(_q(), "B")["is_correct"]


def test_numeric_tolerance():
    q = _q(question_type="numeric", correct_answer="10", tolerance=0.5)
    assert score_question(q, "10.2")["is_correct"] is True
    assert score_question(q, "11")["is_correct"] is False


def test_numeric_exact():
    q = _q(question_type="numeric", correct_answer="10")
    assert score_question(q, "10")["is_correct"] is True
    assert score_question(q, "10.1")["is_correct"] is False


def test_deterministic_repeat():
    assert score_question(_q(), "B")["is_correct"] == score_question(_q(), "B")["is_correct"]


def test_normalize_trim():
    assert normalize_answer("  b  ", "mcq") == "B"


def test_score_records_fields():
    r = score_question(_q(), "B", time_spent=12.5)
    for k in ("question_id", "pattern", "difficulty", "user_answer", "correct_answer", "is_correct", "time_spent"):
        assert k in r
    assert r["time_spent"] == 12.5
