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
from app.services.gamification_core import (
    BADGES,
    BADGE_CONDITIONS,
    ACTIVITY_COUNTER_FIELD,
    GAMIFICATION_COUNTER_FIELDS,
    badge_condition_met,
)


class TestCalculateLevel:
    """Tests for Diamonds-to-level calculation."""

    def test_level_1_at_zero_xp(self):
        assert _calculate_level(0) == 1

    def test_level_2_at_50_xp(self):
        assert _calculate_level(50) == 2

    def test_level_3_at_200_xp(self):
        assert _calculate_level(200) == 3

    def test_level_10_at_4950_xp(self):
        assert _calculate_level(4950) == 10

    def test_level_never_decreases(self):
        for diamonds in [0, 10, 100, 1000, 5000]:
            level = _calculate_level(diamonds)
            assert level >= 1
            assert level <= 100

    def test_max_level_100(self):
        assert _calculate_level(999999) == 100


class TestCalculateXP:
    """Tests for Diamonds reward calculation by activity type."""

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


class TestBadgeConditionParity:
    """CI tripwire: the badge catalog and its conditions must be 1:1.

    A badge with no condition can never be earned (a catalog lie); a
    condition for a badge that doesn't exist is dead configuration.
    """

    def test_badge_catalog_matches_conditions(self):
        assert set(BADGES) == set(BADGE_CONDITIONS)

    def test_all_counter_conditions_reference_canonical_fields(self):
        for badge_id, condition in BADGE_CONDITIONS.items():
            if condition is None:
                continue
            assert isinstance(condition, tuple), f"{badge_id} condition must be a tuple"
            assert 2 <= len(condition) <= 3, f"{badge_id} condition must be (kind, key, min)"
            kind = condition[0]
            assert kind in ("counter", "score", "streak", "level", "bosses"), f"{badge_id} has unknown kind {kind}"
            if kind == "counter":
                assert condition[1] in GAMIFICATION_COUNTER_FIELDS, (
                    f"{badge_id} counter condition references {condition[1]} which record_practice() never writes"
                )

    def test_all_score_conditions_use_known_activities(self):
        for badge_id, condition in BADGE_CONDITIONS.items():
            if condition is None or condition[0] != "score":
                continue
            activity = condition[1]
            assert activity in ACTIVITY_COUNTER_FIELD, (
                f"{badge_id} score condition references activity '{activity}' with no canonical counter"
            )

    def test_resume_badges_never_fire_with_zero_score(self):
        """Resume creation is recorded at score 0; only /optimize (real ATS) earns."""
        profile = {"total_resumes": 3, "level": 1, "bosses_defeated": []}
        assert badge_condition_met(BADGE_CONDITIONS["first_resume"], profile, "resume", 0, 0)
        assert not badge_condition_met(BADGE_CONDITIONS["ats_master"], profile, "resume", 0, 0)
        assert not badge_condition_met(BADGE_CONDITIONS["ats_95"], profile, "resume", 0, 0)

    def test_first_accepted_and_hard_problem_scores(self):
        profile = {"level": 1, "bosses_defeated": []}
        assert badge_condition_met(BADGE_CONDITIONS["first_accepted"], profile, "coding", 80, 0)
        assert not badge_condition_met(BADGE_CONDITIONS["first_accepted"], profile, "coding", 79, 0)
        assert badge_condition_met(BADGE_CONDITIONS["hard_problem"], profile, "coding", 95, 0)
        assert not badge_condition_met(BADGE_CONDITIONS["hard_problem"], profile, "coding", 90, 0)

    def test_coding_score_badges_are_activity_gated(self):
        profile = {"level": 1, "bosses_defeated": []}
        assert not badge_condition_met(BADGE_CONDITIONS["first_accepted"], profile, "aptitude", 100, 0)

    def test_score_scale_thresholds_are_consistent_with_caller_scales(self):
        """Interview/system_design are 0-10; aptitude/coding/resume are 0-100.

        Thresholds in BADGE_CONDITIONS must sit on the same scale the callers
        pass, otherwise a badge is fireable-on-trivial or unreachable.
        """
        profile = {"level": 1, "bosses_defeated": []}
        active = [
            ("perfect_score", "interview", 10),
            ("high_score_streak", "interview", 8),
            ("aptitude_perfect", "aptitude", 100),
            ("first_accepted", "coding", 80),
            ("hard_problem", "coding", 95),
            ("ats_master", "resume", 90),
            ("ats_95", "resume", 95),
            ("system_design_master", "system_design", 9),
        ]
        for badge_id, activity, min_score in active:
            cond = BADGE_CONDITIONS[badge_id]
            assert cond[0] == "score", badge_id
            assert not badge_condition_met(cond, profile, activity, min_score - 1, 0), (
                f"{badge_id} must NOT fire below its threshold"
            )
            assert badge_condition_met(cond, profile, activity, min_score, 0), (
                f"{badge_id} must fire at its threshold"
            )

    def test_unreachable_score_thresholds_rejected(self):
        """A perfect score is 10/10 (interview, system_design) or 100% (others).
        Thresholds above the max possible on each scale are unreachable."""
        max_by_activity = {
            "interview": 10,
            "system_design": 10,
            "aptitude": 100,
            "coding": 100,
            "resume": 100,
        }
        for badge_id, condition in BADGE_CONDITIONS.items():
            if condition is None or condition[0] != "score":
                continue
            activity = condition[1]
            assert condition[2] <= max_by_activity[activity], (
                f"{badge_id} threshold {condition[2]} is unreachable on {activity} scale"
            )

    def test_lucky_streak_is_externally_declared(self):
        assert BADGE_CONDITIONS["lucky_streak"] is None

    def test_counter_badges_respect_profile_thresholds(self):
        profile = {"level": 1, "bosses_defeated": [], "total_interviews": 9}
        assert not badge_condition_met(BADGE_CONDITIONS["interview_10"], profile, "interview", 10, 0)
        profile["total_interviews"] = 10
        assert badge_condition_met(BADGE_CONDITIONS["interview_10"], profile, "interview", 10, 0)

    def test_level_badges_use_server_level(self):
        profile = {"level": 50, "bosses_defeated": []}
        assert badge_condition_met(BADGE_CONDITIONS["tower_floor_5"], profile, "coding", 80, 0)
        assert not badge_condition_met(BADGE_CONDITIONS["tower_floor_10"], profile, "coding", 80, 0)

    def test_boss_badges_use_bosses_defeated(self):
        profile = {"level": 1, "bosses_defeated": [10, 20, 30, 40, 50]}
        assert badge_condition_met(BADGE_CONDITIONS["boss_5"], profile, "coding", 80, 0)
        assert not badge_condition_met(BADGE_CONDITIONS["boss_10"], profile, "coding", 80, 0)

    def test_counter_fields_map_to_singular_names_readers_use(self):
        """record_practice() must increment the same fields readers query.

        Historical bug: the engine wrote plural fields (total_aptitudes) that
        no reader consumed while readers read total_aptitude etc. This tripwire
        pins the canonical names so a regression fails CI."""
        assert ACTIVITY_COUNTER_FIELD["interview"] == "total_interviews"
        assert ACTIVITY_COUNTER_FIELD["aptitude"] == "total_aptitude"
        assert ACTIVITY_COUNTER_FIELD["coding"] == "total_coding"
        assert ACTIVITY_COUNTER_FIELD["system_design"] == "total_system_design"
        assert ACTIVITY_COUNTER_FIELD["resume"] == "total_resumes"
        assert "total_powerups_used" in GAMIFICATION_COUNTER_FIELDS
        assert "total_perfect_scores" in GAMIFICATION_COUNTER_FIELDS
