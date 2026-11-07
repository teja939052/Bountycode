"""Unit coverage for personalized diagnostic evidence fields."""

import pytest

from app.routes.academy_diagnostic import DiagnosticAnswer, skill_level


def test_diagnostic_answer_accepts_timing_and_confidence():
    answer = DiagnosticAnswer(
        question_id="q-1",
        answer="2",
        time_taken_seconds=37,
        confidence=4,
    )
    assert answer.time_taken_seconds == 37
    assert answer.confidence == 4


def test_diagnostic_answer_rejects_invalid_confidence():
    with pytest.raises(ValueError):
        DiagnosticAnswer(question_id="q-1", answer="2", confidence=6)


def test_skill_level_is_progressive():
    assert skill_level(20, 4) == "foundation_needed"
    assert skill_level(65, 4) == "developing"
    assert skill_level(90, 4) == "strong"
