"""Tests for usage tracking and free-tier enforcement."""

import pytest
from datetime import datetime, timezone, timedelta
from bson import ObjectId
from app.services.usage import check_and_reset_monthly_usage, can_use_feature, mark_feature_used
from app.config import get_settings


class TestCheckAndResetMonthlyUsage:
    """Tests for monthly usage reset logic."""

    @pytest.mark.asyncio
    async def test_no_reset_for_new_user(self, mocker):
        mock_user = {
            "id": "507f1f77bcf86cd799439011",
            "plan": "free",
            "monthly_reset_date": None,
            "interviews_used": 0,
        }
        mock_update = mocker.AsyncMock()
        mock_collection = mocker.AsyncMock()
        mock_collection.update_one = mock_update
        mocker.patch(
            "app.services.usage.users_collection",
            mock_collection,
        )

        result = await check_and_reset_monthly_usage(mock_user)

        assert result["monthly_reset_date"] is not None
        mock_update.assert_called_once()

    @pytest.mark.asyncio
    async def test_no_reset_for_pro_user(self, mocker):
        now = datetime.now(timezone.utc)
        last_reset = now - timedelta(days=60)
        mock_user = {
            "id": "507f1f77bcf86cd799439011",
            "plan": "pro",
            "monthly_reset_date": last_reset,
            "interviews_used": 100,
        }

        result = await check_and_reset_monthly_usage(mock_user)

        assert result["interviews_used"] == 100
        assert result["monthly_reset_date"] == last_reset

    @pytest.mark.asyncio
    async def test_reset_when_month_changed(self, mocker):
        last_month = datetime.now(timezone.utc) - timedelta(days=40)
        mock_user = {
            "id": "507f1f77bcf86cd799439011",
            "plan": "free",
            "monthly_reset_date": last_month,
            "interviews_used": 3,
            "resumes_used": 3,
            "aptitude_used": 5,
            "cover_letters_used": 3,
            "company_mocks_used": 1,
            "predictions_used": 3,
            "question_bank_used": 5,
            "streak_repairs_used": 1,
        }
        mock_update = mocker.AsyncMock()
        mock_collection = mocker.AsyncMock()
        mock_collection.update_one = mock_update
        mocker.patch(
            "app.services.usage.users_collection",
            mock_collection,
        )

        result = await check_and_reset_monthly_usage(mock_user)

        assert result["interviews_used"] == 0
        assert result["resumes_used"] == 0
        assert result["aptitude_used"] == 0
        mock_update.assert_called_once()

    @pytest.mark.asyncio
    async def test_no_reset_within_same_month(self, mocker):
        now = datetime.now(timezone.utc)
        mock_user = {
            "id": "507f1f77bcf86cd799439011",
            "plan": "free",
            "monthly_reset_date": now,
            "interviews_used": 1,
        }
        mock_update = mocker.AsyncMock()
        mock_collection = mocker.AsyncMock()
        mock_collection.update_one = mock_update
        mocker.patch(
            "app.services.usage.users_collection",
            mock_collection,
        )

        result = await check_and_reset_monthly_usage(mock_user)

        assert result["interviews_used"] == 1
        mock_update.assert_not_called()

    @pytest.mark.asyncio
    async def test_monthly_reset_date_updated(self, mocker):
        last_month = datetime.now(timezone.utc) - timedelta(days=40)
        mock_user = {
            "id": "507f1f77bcf86cd799439011",
            "plan": "free",
            "monthly_reset_date": last_month,
            "interviews_used": 3,
        }
        mock_update = mocker.AsyncMock()
        mock_collection = mocker.AsyncMock()
        mock_collection.update_one = mock_update
        mocker.patch(
            "app.services.usage.users_collection",
            mock_collection,
        )

        result = await check_and_reset_monthly_usage(mock_user)

        assert result["monthly_reset_date"] > last_month


class TestCanUseFeature:
    """Tests for feature access control."""

    def test_pro_user_can_use_any_feature(self):
        user = {"plan": "pro", "interviews_used": 999}
        can_use, message = can_use_feature(user, "interview")
        assert can_use is True
        assert message == ""

    def test_lifetime_user_can_use_any_feature(self):
        user = {"plan": "lifetime", "interviews_used": 999}
        can_use, message = can_use_feature(user, "interview")
        assert can_use is True
        assert message == ""

    def test_free_user_within_limit(self):
        user = {"plan": "free", "interviews_used": 1}
        can_use, message = can_use_feature(user, "interview")
        assert can_use is True

    def test_free_user_at_limit(self):
        settings = get_settings()
        user = {"plan": "free", "interviews_used": settings.FREE_TIER_INTERVIEW_LIMIT}
        can_use, message = can_use_feature(user, "interview")
        assert can_use is False
        assert "limit" in message.lower() or "upgrade" in message.lower()

    def test_free_user_over_limit(self):
        settings = get_settings()
        user = {"plan": "free", "interviews_used": settings.FREE_TIER_INTERVIEW_LIMIT + 1}
        can_use, message = can_use_feature(user, "interview")
        assert can_use is False

    def test_resume_feature_limit(self):
        settings = get_settings()
        user = {"plan": "free", "resumes_used": settings.FREE_TIER_RESUME_LIMIT}
        can_use, message = can_use_feature(user, "resume")
        assert can_use is False

    def test_unknown_feature_denied(self):
        user = {"plan": "free", "interviews_used": 0}
        can_use, message = can_use_feature(user, "unknown_feature")
        assert can_use is False


class TestMarkFeatureUsed:
    """Tests for mark_feature_used function."""

    @pytest.mark.asyncio
    async def test_mark_feature_used_increments_counter(self, mocker):
        mock_user_id = "507f1f77bcf86cd799439011"
        mock_update = mocker.AsyncMock()
        mock_find = mocker.AsyncMock(
            return_value={
                "_id": ObjectId(mock_user_id),
                "plan": "free",
                "email": "test@example.com",
                "name": "Test",
                "interviews_used": 0,
            }
        )
        mock_collection = mocker.AsyncMock()
        mock_collection.update_one = mock_update
        mock_collection.find_one = mock_find
        mocker.patch(
            "app.services.usage.users_collection",
            mock_collection,
        )

        await mark_feature_used(mock_user_id, "interview")

        mock_update.assert_called_once()
        call_args = mock_update.call_args
        assert call_args[0][0] == {"_id": ObjectId(mock_user_id)}

    @pytest.mark.asyncio
    async def test_mark_feature_used_does_not_increment_for_pro(self, mocker):
        mock_user_id = "507f1f77bcf86cd799439011"
        mock_find = mocker.AsyncMock(
            return_value={
                "_id": ObjectId(mock_user_id),
                "plan": "pro",
                "email": "test@example.com",
                "name": "Test",
                "interviews_used": 100,
            }
        )
        mock_collection = mocker.AsyncMock()
        mock_collection.find_one = mock_find
        mocker.patch(
            "app.services.usage.users_collection",
            mock_collection,
        )

        await mark_feature_used(mock_user_id, "interview")

        mock_find.assert_called_once()
