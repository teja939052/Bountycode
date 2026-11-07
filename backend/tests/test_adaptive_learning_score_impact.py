"""Regression tests for diagnostic-only activity and skill-score impact."""
from app.services.adaptive_learning import _activity_score_delta


def test_zero_impact_diagnostic_does_not_change_skill_score():
    assert _activity_score_delta("diagnostic", True, 0) == 0


def test_positive_impact_preserves_normal_practice_delta():
    assert _activity_score_delta("practice", True, 1) == 5


def test_challenge_keeps_its_existing_higher_delta():
    assert _activity_score_delta("challenge", True, 1) == 8


def test_failed_activity_never_increases_skill_score():
    assert _activity_score_delta("practice", False, 1) == 0


def test_invalid_or_non_finite_impact_is_not_applied():
    assert _activity_score_delta("practice", True, None) == 0
    assert _activity_score_delta("practice", True, float("nan")) == 0
