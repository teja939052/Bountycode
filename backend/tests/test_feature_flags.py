"""Tests for feature flags and usage tracking."""

import pytest
from app.services.feature_flags import is_feature_enabled, get_enabled_features, set_feature_enabled, FEATURE_FLAGS
from app.services.usage import can_use_feature, mark_feature_used, get_usage_stats, check_and_reset_monthly_usage


class TestFeatureFlags:
    def test_core_features_always_enabled_for_free(self):
        assert is_feature_enabled("interviews", "free") is True
        assert is_feature_enabled("resume", "free") is True
        assert is_feature_enabled("coding", "free") is True
        assert is_feature_enabled("compiler", "free") is True

    def test_admin_features_blocked_for_free(self):
        assert is_feature_enabled("admin_dashboard", "free") is False
        assert is_feature_enabled("admin_content", "free") is False
        assert is_feature_enabled("retention_admin", "free") is False

    def test_admin_features_allowed_for_pro(self):
        assert is_feature_enabled("admin_dashboard", "pro") is True
        assert is_feature_enabled("admin_content", "lifetime") is True
        assert is_feature_enabled("retention_admin", "lifetime") is True

    def test_disabled_feature_returns_false(self):
        set_feature_enabled("interviews", False)
        assert is_feature_enabled("interviews", "pro") is False
        set_feature_enabled("interviews", True)

    def test_get_enabled_features_returns_list(self):
        features = get_enabled_features("free")
        assert isinstance(features, list)
        assert "interviews" in features
        assert "admin_dashboard" not in features

    def test_all_flags_have_description(self):
        for key, flag in FEATURE_FLAGS.items():
            assert "description" in flag, f"{key} missing description"
            assert len(flag["description"]) > 0, f"{key} has empty description"


class TestUsageTracking:
    def test_can_use_feature_free_tier(self):
        user = {"plan": "free", "interviews_used": 2}
        allowed, _ = can_use_feature(user, "interview")
        assert allowed is True

        user_at_limit = {"plan": "free", "interviews_used": 3}
        allowed, msg = can_use_feature(user_at_limit, "interview")
        assert allowed is False
        assert "Free tier limit" in msg

    def test_pro_plan_unlimited(self):
        user = {"plan": "pro", "interviews_used": 999}
        allowed, _ = can_use_feature(user, "interview")
        assert allowed is True

    def test_lifetime_plan_unlimited(self):
        user = {"plan": "lifetime", "resumes_used": 999}
        allowed, _ = can_use_feature(user, "resume")
        assert allowed is True

    def test_usage_stats_structure(self):
        user = {
            "plan": "free",
            "interviews_used": 2,
            "resumes_used": 1,
            "aptitude_used": 3,
        }
        stats = get_usage_stats(user)
        assert stats["plan"] == "free"
        assert stats["interviews_used"] == 2
        assert stats["interviews_limit"] == 3
        assert stats["resumes_limit"] == 3
        assert stats["aptitude_limit"] == 5

    def test_usage_stats_pro_unlimited(self):
        user = {"plan": "pro", "interviews_used": 100}
        stats = get_usage_stats(user)
        assert stats["interviews_limit"] == "unlimited"
        assert stats["resumes_limit"] == "unlimited"

    def test_monthly_reset_new_user(self):
        user = {"id": "000000000000000000000000", "plan": "free", "monthly_reset_date": None}
        import asyncio
        result = asyncio.run(check_and_reset_monthly_usage(user))
        assert result is not None
        assert "id" in result
