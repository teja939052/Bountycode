"""Tests for tier middleware and free-tier gating logic."""

import pytest
from app.middleware.tier_middleware import (
    TIER_LIMITS,
    FEATURE_TO_LIMIT_KEY,
    USED_KEY_MAP,
    MONTHLY_FEATURES,
    DAILY_FEATURES,
    _get_tier,
    _get_current_month_key,
    _get_daily_key,
    check_tier_limit,
)


class TestGetTier:
    """Tests for plan-to-tier mapping."""

    def test_free_plan_maps_to_free(self):
        assert _get_tier("free") == "free"

    def test_pro_plan_maps_to_pro(self):
        assert _get_tier("pro") == "pro"

    def test_lifetime_plan_maps_to_lifetime(self):
        assert _get_tier("lifetime") == "lifetime"

    def test_unknown_plan_defaults_to_free(self):
        assert _get_tier("enterprise") == "free"

    def test_case_sensitive(self):
        assert _get_tier("Free") == "free"
        assert _get_tier("PRO") == "free"


class TestDateKeys:
    """Tests for date key generation."""

    def test_current_month_key_format(self):
        key = _get_current_month_key()
        parts = key.split("-")
        assert len(parts) == 2
        year, month = int(parts[0]), int(parts[1])
        assert 2020 <= year <= 2030
        assert 1 <= month <= 12

    def test_daily_key_format(self):
        key = _get_daily_key()
        parts = key.split("-")
        assert len(parts) == 3


class TestTierLimits:
    """Tests for tier limit definitions."""

    def test_free_tier_has_limits(self):
        free_limits = TIER_LIMITS["free"]
        assert free_limits["interviews_per_month"] == 3
        assert free_limits["resume_reviews_per_month"] == 3
        assert free_limits["aptitude_tests_per_month"] == 5

    def test_pro_tier_has_high_limits(self):
        pro_limits = TIER_LIMITS["pro"]
        assert pro_limits["interviews_per_month"] == 999
        assert pro_limits["daily_compiler_runs"] == 999

    def test_lifetime_tier_has_high_limits(self):
        lifetime_limits = TIER_LIMITS["lifetime"]
        assert lifetime_limits["interviews_per_month"] == 999
        assert lifetime_limits["daily_mystery_boxes"] == 5

    def test_all_tiers_have_same_keys(self):
        free_keys = set(TIER_LIMITS["free"].keys())
        pro_keys = set(TIER_LIMITS["pro"].keys())
        lifetime_keys = set(TIER_LIMITS["lifetime"].keys())
        assert free_keys == pro_keys == lifetime_keys


class TestFeatureMapping:
    """Tests for feature-to-limit-key mapping."""

    def test_interview_features_map_correctly(self):
        assert FEATURE_TO_LIMIT_KEY["interview"] == "interviews_per_month"
        assert FEATURE_TO_LIMIT_KEY["interviews"] == "interviews_per_month"

    def test_resume_features_map_correctly(self):
        assert FEATURE_TO_LIMIT_KEY["resume"] == "resume_reviews_per_month"
        assert FEATURE_TO_LIMIT_KEY["resumes"] == "resume_reviews_per_month"

    def test_compiler_features_map_correctly(self):
        assert FEATURE_TO_LIMIT_KEY["compiler_run"] == "daily_compiler_runs"
        assert FEATURE_TO_LIMIT_KEY["compiler_runs"] == "daily_compiler_runs"

    def test_daily_features_map_to_daily_keys(self):
        assert FEATURE_TO_LIMIT_KEY["compiler_run"] == "daily_compiler_runs"
        assert FEATURE_TO_LIMIT_KEY["problem"] == "problems_per_day"
        assert FEATURE_TO_LIMIT_KEY["ai_question"] == "daily_ai_questions"

    def test_all_mapped_features_exist_in_tier_limits(self):
        for feature, limit_key in FEATURE_TO_LIMIT_KEY.items():
            assert limit_key in TIER_LIMITS["free"], f"{limit_key} not in free tier limits"


class TestUsedKeyMap:
    """Tests for feature-to-used-field mapping."""

    def test_interview_maps_to_interviews_used(self):
        assert USED_KEY_MAP["interview"] == "interviews_used"
        assert USED_KEY_MAP["interviews"] == "interviews_used"

    def test_resume_maps_to_resumes_used(self):
        assert USED_KEY_MAP["resume"] == "resumes_used"
        assert USED_KEY_MAP["resumes"] == "resumes_used"

    def test_aptitude_maps_to_aptitude_used(self):
        assert USED_KEY_MAP["aptitude"] == "aptitude_used"

    def test_cover_letter_maps_to_cover_letters_used(self):
        assert USED_KEY_MAP["cover_letter"] == "cover_letters_used"

    def test_mock_interview_maps_to_mock_interviews_used(self):
        assert USED_KEY_MAP["mock_interview"] == "mock_interviews_used"

    def test_monthly_features_have_used_keys(self):
        for feature in MONTHLY_FEATURES:
            if feature in FEATURE_TO_LIMIT_KEY:
                limit_key = FEATURE_TO_LIMIT_KEY[feature]
                if not limit_key.startswith("daily_"):
                    assert feature in USED_KEY_MAP


class TestMonthlyFeatures:
    """Tests for monthly feature classification."""

    def test_interview_is_monthly(self):
        assert "interview" in MONTHLY_FEATURES
        assert "interviews" in MONTHLY_FEATURES

    def test_resume_is_monthly(self):
        assert "resume" in MONTHLY_FEATURES
        assert "resume_review" in MONTHLY_FEATURES
        assert "resume_reviews" in MONTHLY_FEATURES

    def test_compiler_is_not_monthly(self):
        assert "compiler_run" not in MONTHLY_FEATURES
        assert "compiler_runs" not in MONTHLY_FEATURES


class TestDailyFeatures:
    """Tests for daily feature classification."""

    def test_compiler_is_daily(self):
        assert "compiler_run" in DAILY_FEATURES
        assert "compiler_runs" in DAILY_FEATURES

    def test_problem_is_daily(self):
        assert "problem" in DAILY_FEATURES
        assert "problems" in DAILY_FEATURES

    def test_interview_is_not_daily(self):
        assert "interview" not in DAILY_FEATURES
        assert "interviews" not in DAILY_FEATURES

    def test_no_overlap_between_monthly_and_daily(self):
        assert not MONTHLY_FEATURES.intersection(DAILY_FEATURES)


class TestCheckTierLimit:
    """Tests for check_tier_limit function."""

    @pytest.mark.asyncio
    async def test_pro_user_passes_all_limits(self):
        mock_user = {"plan": "pro", "interviews_used": 999}
        await check_tier_limit(mock_user, "interview")

    @pytest.mark.asyncio
    async def test_lifetime_user_passes_all_limits(self):
        mock_user = {"plan": "lifetime", "interviews_used": 999}
        await check_tier_limit(mock_user, "interview")

    @pytest.mark.asyncio
    async def test_free_user_within_limit(self):
        mock_user = {"plan": "free", "interviews_used": 1}
        await check_tier_limit(mock_user, "interview")

    @pytest.mark.asyncio
    async def test_free_user_at_limit_raises(self):
        mock_user = {"plan": "free", "interviews_used": 3}
        with pytest.raises(Exception) as exc_info:
            await check_tier_limit(mock_user, "interview")
        assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_unknown_feature_does_not_raise(self):
        mock_user = {"plan": "free", "interviews_used": 0}
        await check_tier_limit(mock_user, "nonexistent_feature")
