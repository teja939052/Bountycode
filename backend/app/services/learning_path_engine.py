"""BALMA orchestration: turn learner evidence into the next learning action.

This pure decision layer composes:
  1. BKT learner-state estimates,
  2. the canonical prerequisite dependency graph,
  3. BLPA value-per-minute action ranking.

Database access and event trust boundaries deliberately remain outside this
module. The API/service adapter must load persisted, server-graded observations
and normalize them with server_graded=True before calling this function.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping

from app.services.adaptive_action_planner import (
    DEFAULT_PLANNER_WEIGHTS,
    PlannerWeights,
    rank_actions,
)
from app.services.learner_state_engine import (
    DEFAULT_BKT_PARAMETERS,
    BKTParameters,
    estimate_skill_state,
)
from app.services.prerequisite_graph import SKILL_PREREQUISITES


def _ordered_prerequisites(target_skill_id: str) -> list[str]:
    """Return transitive prerequisites in dependency-first order."""
    ordered: list[str] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(skill_id: str) -> None:
        if skill_id in visiting:
            raise ValueError(f"Prerequisite cycle detected at {skill_id}")
        if skill_id in visited:
            return
        if skill_id not in SKILL_PREREQUISITES:
            raise ValueError(f"Unknown skill in prerequisite graph: {skill_id}")

        visiting.add(skill_id)
        for prerequisite in SKILL_PREREQUISITES[skill_id].get("prerequisites", []):
            if prerequisite not in SKILL_PREREQUISITES:
                raise ValueError(
                    f"Unknown prerequisite {prerequisite} for {skill_id}"
                )
            visit(prerequisite)
            if prerequisite not in ordered:
                ordered.append(prerequisite)
        visiting.remove(skill_id)
        visited.add(skill_id)

    visit(target_skill_id)
    return ordered


def build_personalized_learning_plan(
    target_skill_id: str,
    observations_by_skill: Mapping[str, Iterable[Mapping[str, Any]]],
    action_catalog: Iterable[Mapping[str, Any]],
    *,
    time_budget_minutes: float,
    goal_weights: Mapping[str, float] | None = None,
    bkt_parameters: BKTParameters = DEFAULT_BKT_PARAMETERS,
    planner_weights: PlannerWeights = DEFAULT_PLANNER_WEIGHTS,
    min_distinct_questions: int = 3,
    mastery_threshold: float = 0.80,
) -> dict[str, Any]:
    """Choose the first unmastered prerequisite/target and rank its actions.

    The graph is traversed dependency-first. The first skill without sufficient
    evidence or below the BKT mastery threshold becomes the learning focus.
    Only actions for that focus skill are ranked, preventing the planner from
    jumping to an advanced target while a prerequisite remains unproven.

    Candidate expected_mastery_gain values must be provided by a trusted,
    versioned estimator or experiment. This module does not invent them.
    """
    if target_skill_id not in SKILL_PREREQUISITES:
        return {
            "status": "unknown_target_skill",
            "target_skill_id": target_skill_id,
            "next_skill_id": None,
            "selected_action": None,
            "reason": "Target skill is not present in the canonical prerequisite graph.",
        }

    prerequisite_order = _ordered_prerequisites(target_skill_id)
    skill_order = prerequisite_order + [target_skill_id]
    learner_states: dict[str, dict[str, Any]] = {}

    for skill_id in skill_order:
        learner_states[skill_id] = estimate_skill_state(
            skill_id,
            observations_by_skill.get(skill_id, []),
            parameters=bkt_parameters,
            min_distinct_questions=min_distinct_questions,
            mastery_threshold=mastery_threshold,
        )

    next_skill_id = next(
        (
            skill_id for skill_id in skill_order
            if learner_states[skill_id]["status"] != "mastered"
        ),
        None,
    )

    if next_skill_id is None:
        return {
            "status": "target_mastered",
            "target_skill_id": target_skill_id,
            "next_skill_id": None,
            "selected_action": None,
            "learner_states": learner_states,
            "required_skill_order": skill_order,
            "reason": "The target and all registered prerequisites meet the current mastery rule.",
        }

    skill_definition = SKILL_PREREQUISITES[next_skill_id]
    direct_prerequisites = list(skill_definition.get("prerequisites", []))
    prerequisites_met = all(
        learner_states.get(prerequisite, {}).get("status") == "mastered"
        for prerequisite in direct_prerequisites
    )

    relevant_candidates: list[dict[str, Any]] = []
    for candidate in action_catalog:
        if not isinstance(candidate, Mapping):
            continue
        if str(candidate.get("skill_id") or "") != next_skill_id:
            continue

        normalized = dict(candidate)
        normalized["prerequisites_met"] = prerequisites_met
        if goal_weights is not None and next_skill_id in goal_weights:
            normalized["goal_relevance"] = goal_weights[next_skill_id]
        relevant_candidates.append(normalized)

    ranking = rank_actions(
        relevant_candidates,
        time_budget_minutes=time_budget_minutes,
        weights=planner_weights,
    )

    if ranking["selected"] is None:
        status = "content_gap"
        reason = (
            "No eligible, quality-approved action is available for the earliest "
            "unmastered skill. Author or repair content before advancing."
        )
    else:
        status = "action_available"
        reason = (
            "The selected action targets the earliest unmastered prerequisite "
            "or target skill and fits the learner's time budget."
        )

    return {
        "status": status,
        "target_skill_id": target_skill_id,
        "next_skill_id": next_skill_id,
        "next_skill_title": skill_definition.get("title", next_skill_id),
        "next_skill_state": learner_states[next_skill_id],
        "selected_action": ranking["selected"],
        "ranked_actions": ranking["ranked_actions"],
        "rejected_actions": ranking["rejected_actions"],
        "learner_states": learner_states,
        "required_skill_order": skill_order,
        "direct_prerequisites_met": prerequisites_met,
        "time_budget_minutes": float(time_budget_minutes),
        "planner_policy_version": planner_weights.version,
        "bkt_parameter_version": bkt_parameters.version,
        "reason": reason,
        "calibration_note": (
            "BKT parameters and planner weights are initial assumptions. "
            "Expected mastery gains must be estimated and calibrated separately."
        ),
    }
