import math

import pytest

from app.services.learner_state_engine import (
    BKTParameters,
    estimate_skill_state,
    update_bkt,
)
from app.services.adaptive_action_planner import rank_actions, score_action
from app.services.retention_model import (
    days_until_target_retention,
    estimate_retention,
    review_urgency,
)


def test_bkt_correct_observation_increases_mastery():
    result = update_bkt(0.4, True)
    assert result["mastery_after_transition"] > 0.4
    assert 0 <= result["mastery_after_transition"] <= 1


def test_bkt_incorrect_observation_reduces_observed_mastery_before_transition():
    result = update_bkt(0.8, False)
    assert result["posterior_after_observation"] < 0.8
    assert result["mastery_after_transition"] >= result["posterior_after_observation"]


def test_bkt_rejects_invalid_parameters_and_non_boolean_outcomes():
    with pytest.raises(ValueError):
        BKTParameters(p_g=1.0)
    with pytest.raises(ValueError):
        update_bkt(0.5, 1)  # type: ignore[arg-type]


def test_bkt_guards_degenerate_prior_without_division_error():
    result = update_bkt(0.0, False)
    assert math.isfinite(result["mastery_after_transition"])


def test_learner_state_requires_distinct_server_graded_questions():
    state = estimate_skill_state("coding.loops", [
        {"question_id": "q1", "correct": True, "server_graded": True},
        {"question_id": "q1", "correct": False, "server_graded": True},
        {"question_id": "q2", "correct": True, "server_graded": True},
        {"question_id": "q3", "correct": True, "server_graded": False},
    ])
    assert state["distinct_questions"] == 1
    assert state["status"] == "insufficient_evidence"
    assert state["ignored_observations"] == 2


def test_learner_state_reports_mastery_only_after_minimum_evidence():
    state = estimate_skill_state("coding.variables", [
        {"question_id": f"q{i}", "correct": True, "server_graded": True}
        for i in range(1, 9)
    ])
    assert state["distinct_questions"] == 8
    assert state["status"] == "mastered"
    assert state["parameter_version"] == "bkt-v1-initial"


def test_planner_prefers_high_value_action_per_minute():
    result = rank_actions([
        {
            "action_id": "long-low-value", "skill_id": "dsa.arrays",
            "kind": "practice", "estimated_minutes": 30,
            "expected_mastery_gain": 0.25, "goal_relevance": 0.8,
            "dependency_importance": 0.7,
        },
        {
            "action_id": "short-high-value", "skill_id": "coding.loops",
            "kind": "lesson", "estimated_minutes": 10,
            "expected_mastery_gain": 0.35, "goal_relevance": 0.9,
            "dependency_importance": 0.9,
        },
    ], time_budget_minutes=30)
    assert result["selected"]["action_id"] == "short-high-value"


def test_planner_blocks_advanced_action_when_prerequisites_are_missing():
    with pytest.raises(ValueError, match="prerequisites_not_met"):
        score_action({
            "action_id": "dp-challenge", "skill_id": "dsa.dp",
            "kind": "challenge", "estimated_minutes": 20,
            "expected_mastery_gain": 0.5, "prerequisites_met": False,
        }, time_budget_minutes=30)


def test_planner_allows_a_diagnostic_to_resolve_unknown_prerequisites():
    result = score_action({
        "action_id": "diagnose-loops", "skill_id": "coding.loops",
        "kind": "diagnostic", "estimated_minutes": 8,
        "expected_mastery_gain": 0.05, "uncertainty_reduction": 0.8,
        "prerequisites_met": False,
    }, time_budget_minutes=15)
    assert result["score"] > 0


def test_planner_rejects_low_quality_content_and_over_budget_actions():
    result = rank_actions([
        {
            "action_id": "weak-content", "skill_id": "coding.types",
            "kind": "lesson", "estimated_minutes": 5,
            "expected_mastery_gain": 0.6, "content_quality": 0.2,
        },
        {
            "action_id": "too-long", "skill_id": "dsa.graph",
            "kind": "challenge", "estimated_minutes": 45,
            "expected_mastery_gain": 0.7,
        },
    ], time_budget_minutes=20)
    assert result["selected"] is None
    assert {item["reason"] for item in result["rejected_actions"]} == {
        "content_quality_below_release_threshold", "exceeds_time_budget"
    }


def test_retention_curve_and_due_urgency_are_monotonic():
    assert estimate_retention(0) == pytest.approx(1.0)
    assert estimate_retention(7, half_life_days=7) == pytest.approx(0.5)
    assert review_urgency(14) > review_urgency(3)
    assert days_until_target_retention() > 0


def test_retention_rejects_invalid_inputs():
    with pytest.raises(ValueError):
        estimate_retention(-1)
    with pytest.raises(ValueError):
        review_urgency(2, target_retention=1.0)
