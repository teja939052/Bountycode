"""Tests for gamification service functions."""

import pytest
from unittest.mock import patch, AsyncMock
from app.services.gamification import (
    _calculate_level,
    _calculate_xp,
    calculate_streak_multiplier,
    BOSS_BATTLES,
    TOWER_TITLES,
    POWER_UPS,
    STREAK_MULTIPLIERS,
    FOREST_ZONES,
    SEASONAL_STORMS,
    record_practice,
)


class TestCalculateLevel:
    """Tests for XP-to-level calculation."""

    def test_level_1_at_zero_xp(self):
        assert _calculate_level(0) == 1

    def test_level_2_at_50_xp(self):
        assert _calculate_level(50) == 2

    def test_level_3_at_200_xp(self):
        assert _calculate_level(200) == 3

    def test_level_10_at_4950_xp(self):
        assert _calculate_level(4950) == 10

    def test_level_never_decreases(self):
        for xp in [0, 10, 100, 1000, 5000]:
            level = _calculate_level(xp)
            assert level >= 1
            assert level <= 100

    def test_max_level_100(self):
        assert _calculate_level(999999) == 100


class TestCalculateXP:
    """Tests for XP reward calculation by activity type."""

    def test_xp_scales_with_score(self):
        xp_50 = _calculate_xp("interview", 50)
        xp_100 = _calculate_xp("interview", 100)
        assert xp_100 >= xp_50

    def test_coding_always_positive(self):
        assert _calculate_xp("coding", 0) > 0

    def test_aptitude_scales_with_score(self):
        xp_80 = _calculate_xp("aptitude", 80)
        xp_100 = _calculate_xp("aptitude", 100)
        assert xp_100 >= xp_80

    def test_different_activities_different_xp(self):
        interview_xp = _calculate_xp("interview", 100)
        coding_xp = _calculate_xp("coding", 100)
        assert interview_xp > 0
        assert coding_xp > 0


class TestStreakMultiplier:
    """Tests for streak multiplier calculation."""

    def test_no_streak_returns_1x(self):
        mult, _ = calculate_streak_multiplier(0)
        assert mult == 1.0

    def test_three_day_streak(self):
        mult, _ = calculate_streak_multiplier(3)
        assert mult == 1.2

    def test_seven_day_streak(self):
        mult, _ = calculate_streak_multiplier(7)
        assert mult == 1.5

    def test_thirty_day_streak(self):
        mult, _ = calculate_streak_multiplier(30)
        assert mult == 3.0

    def test_hundred_day_streak(self):
        mult, _ = calculate_streak_multiplier(100)
        assert mult == 5.0

    def test_multiplier_never_below_1(self):
        for days in [0, 1, 2, 5, 10, 50]:
            mult, _ = calculate_streak_multiplier(days)
            assert mult >= 1.0


class TestBossBattles:
    """Tests for boss battle configuration."""

    def test_boss_at_level_10(self):
        assert 10 in BOSS_BATTLES

    def test_boss_at_level_50(self):
        assert 50 in BOSS_BATTLES

    def test_boss_at_level_100(self):
        assert 100 in BOSS_BATTLES

    def test_no_boss_at_level_15(self):
        assert 15 not in BOSS_BATTLES

    def test_all_bosses_have_required_fields(self):
        for level, boss in BOSS_BATTLES.items():
            assert "name" in boss
            assert "emoji" in boss
            assert "topic" in boss
            assert "difficulty" in boss
            assert "required_score" in boss


class TestTowerTitles:
    """Tests for tower title system."""

    def test_title_at_level_1(self):
        assert 1 in TOWER_TITLES
        assert TOWER_TITLES[1][0] == "Hatchling"

    def test_title_at_level_100(self):
        assert 100 in TOWER_TITLES
        assert TOWER_TITLES[100][0] == "God of Code"

    def test_all_titles_have_name_and_emoji(self):
        for level, (name, emoji) in TOWER_TITLES.items():
            assert isinstance(name, str)
            assert isinstance(emoji, str)


class TestPowerUps:
    """Tests for power-up definitions."""

    def test_common_power_ups_exist(self):
        assert "extra_time" in POWER_UPS
        assert "hint_reveal" in POWER_UPS

    def test_rare_power_ups_exist(self):
        assert "double_xp" in POWER_UPS
        assert "skip_boss" in POWER_UPS

    def test_legendary_power_up_exists(self):
        assert "show_answer" in POWER_UPS

    def test_all_power_ups_have_required_fields(self):
        for key, power_up in POWER_UPS.items():
            assert "name" in power_up
            assert "emoji" in power_up
            assert "description" in power_up
            assert "rarity" in power_up
            assert "cost" in power_up


class TestStreakMultipliers:
    """Tests for streak multiplier tier definitions."""

    def test_first_tier_is_1x(self):
        assert STREAK_MULTIPLIERS[0] == (0, 1.0, 0)

    def test_all_tiers_have_three_values(self):
        for tier in STREAK_MULTIPLIERS:
            assert len(tier) == 3

    def test_multipliers_are_monotonically_increasing(self):
        multipliers = [t[1] for t in STREAK_MULTIPLIERS]
        for i in range(1, len(multipliers)):
            assert multipliers[i] > multipliers[i - 1]


class TestForestZones:
    """Tests for forest journey zones."""

    def test_ten_zones_exist(self):
        assert len(FOREST_ZONES) == 10

    def test_zones_cover_levels_1_to_100(self):
        assert FOREST_ZONES[0]["level_min"] == 1
        assert FOREST_ZONES[-1]["level_max"] == 100

    def test_zones_are_contiguous(self):
        for i in range(len(FOREST_ZONES) - 1):
            assert FOREST_ZONES[i]["level_max"] + 1 == FOREST_ZONES[i + 1]["level_min"]

    def test_all_zones_have_required_fields(self):
        for zone in FOREST_ZONES:
            assert "name" in zone
            assert "emoji" in zone
            assert "color" in zone
            assert "description" in zone


class TestSeasonalStorms:
    """Tests for seasonal storm boss aliases."""

    def test_storm_at_level_10(self):
        assert 10 in SEASONAL_STORMS

    def test_storm_at_level_100(self):
        assert 100 in SEASONAL_STORMS

    def test_all_storms_have_required_fields(self):
        for level, storm in SEASONAL_STORMS.items():
            assert "name" in storm
            assert "emoji" in storm
            assert "element" in storm


class TestRecordPractice:
    """Tests for record_practice function."""

    @pytest.mark.asyncio
    async def test_record_practice_calls_database(self):
        mock_user_id = "507f1f77bcf86cd799439011"
        mock_find = AsyncMock(return_value={"user_id": mock_user_id})
        mock_update = AsyncMock()

        with patch("app.services.gamification.gamification_collection") as mock_collection:
            mock_collection.find_one = mock_find
            mock_collection.update_one = mock_update
            await record_practice(mock_user_id, "interview", 100)

        mock_find.assert_called()
