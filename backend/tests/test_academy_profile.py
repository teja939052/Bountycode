"""Tests for learner onboarding profile validation and serialization."""
from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from app.routes.academy_profile import LearnerProfileInput, _serialize


def test_profile_defaults_are_beginner_friendly():
    profile = LearnerProfileInput()
    assert profile.experience_level == "absolute_beginner"
    assert profile.preferred_language == "cpp"
    assert profile.daily_minutes == 60
    assert profile.target_role == "undecided"
    assert profile.assessment_track == "service_company_core"
    assert profile.weekly_days == 5
    assert profile.device_type == "laptop"


def test_profile_normalizes_and_deduplicates_company_ids():
    profile = LearnerProfileInput(target_companies=["TCS", "Infosys", "TCS"])
    assert profile.target_companies == ["tcs", "infosys"]


@pytest.mark.parametrize("field,value", [
    ("daily_minutes", 0),
    ("daily_minutes", 600),
    ("target_role", "chief_executive"),
    ("experience_level", "expertish"),
    ("preferred_language", "brainfuck"),
    ("learning_preference", "random"),
])
def test_profile_rejects_unsupported_values(field, value):
    with pytest.raises(ValidationError):
        LearnerProfileInput(**{field: value})


def test_profile_rejects_past_placement_date():
    with pytest.raises(ValidationError):
        LearnerProfileInput(placement_date=date.today() - timedelta(days=1))


def test_profile_rejects_unknown_assessment_track_and_device():
    with pytest.raises(ValidationError):
        LearnerProfileInput(assessment_track="random_exam")
    with pytest.raises(ValidationError):
        LearnerProfileInput(device_type="tablet")


def test_profile_serialization_never_exposes_user_id():
    result = _serialize({
        "user_id": "private-id",
        "target_role": "software_engineer",
        "onboarding_complete": True,
        "_id": "mongo-id",
    })
    assert result["onboarding_complete"] is True
    assert result["profile"]["target_role"] == "software_engineer"
    assert "user_id" not in result["profile"]
    assert "_id" not in result["profile"]


def test_missing_profile_is_not_complete():
    assert _serialize(None) == {"profile": None, "onboarding_complete": False}
