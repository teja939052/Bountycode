import pytest

from app.services.diagnostic import (
    compute_ema, first_mastery, weakness_tier, diagnose_exam,
)


def test_first_assessment():
    assert first_mastery(0.7) == 0.7


def test_ema_blend():
    assert compute_ema(0.5, 0.7) == round(0.4 * 0.7 + 0.6 * 0.5, 6)


def test_perfect_not_instant():
    assert compute_ema(0.5, 1.0) < 1.0


def test_zero_not_instant():
    assert compute_ema(0.5, 0.0) > 0.0


def test_weakness_tiers():
    assert weakness_tier(0.3) == "critical"
    assert weakness_tier(0.5) == "weak"
    assert weakness_tier(0.7) == "on_track"
    assert weakness_tier(0.9) == "strong"


def test_deterministic():
    qs = [{"id": "q1", "topic": "percentages", "correct_answer": "B", "difficulty": "easy"}]
    ans = {"q1": "B"}
    assert diagnose_exam(qs, ans, {}, "exam1", None) == diagnose_exam(qs, ans, {}, "exam1", None)


def test_linkage():
    qs = [{"id": "q1", "topic": "percentages", "correct_answer": "B", "difficulty": "easy"}]
    res = diagnose_exam(qs, {"q1": "B"}, {}, "exam42", "act99")
    assert res[0]["exam_id"] == "exam42"
    assert res[0]["activity_id"] == "act99"
