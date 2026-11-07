from app.services.prerequisite_graph import (
    SKILL_PREREQUISITES,
    build_prerequisite_plan,
    validate_prerequisite_graph,
)


def _mastered(*skill_ids):
    return {
        skill_id: {"score": 90, "total_attempts": 5}
        for skill_id in skill_ids
    }


def test_prerequisite_graph_has_no_unknown_references_or_cycles():
    assert validate_prerequisite_graph() == []


def test_recursion_requires_functions_parameters_return_values_and_conditions():
    plan = build_prerequisite_plan("dsa.recursion")

    assert plan["status"] == "prerequisites_unassessed"
    assert plan["next_action"] == "diagnostic_assessment"
    assert {
        "coding.functions",
        "coding.parameters",
        "coding.return",
        "coding.conditions",
    }.issubset(set(plan["blockers"]))


def test_recursion_unlocks_only_after_all_prerequisites_have_repeated_evidence():
    plan = build_prerequisite_plan(
        "dsa.recursion",
        _mastered(
            "coding.variables",
            "coding.types",
            "coding.conditions",
            "coding.functions",
            "coding.parameters",
            "coding.return",
        ),
    )

    assert plan["status"] == "ready"
    assert plan["next_action"] == "teach_target"
    assert plan["blockers"] == []


def test_low_prerequisite_score_creates_a_repair_gate():
    evidence = _mastered(
        "coding.variables",
        "coding.types",
        "coding.conditions",
        "coding.parameters",
        "coding.return",
    )
    evidence["coding.functions"] = {"score": 42, "total_attempts": 4}

    plan = build_prerequisite_plan("dsa.recursion", evidence)

    assert plan["status"] == "prerequisite_gap"
    assert plan["next_action"] == "teach_and_reassess"
    assert "coding.functions" in plan["blockers"]


def test_one_lucky_answer_does_not_unlock_a_prerequisite():
    evidence = _mastered(
        "coding.variables",
        "coding.types",
        "coding.conditions",
        "coding.functions",
        "coding.return",
    )
    evidence["coding.parameters"] = {"score": 100, "total_attempts": 1}

    plan = build_prerequisite_plan("dsa.recursion", evidence)

    assert plan["status"] == "prerequisites_unassessed"
    assert "coding.parameters" in plan["blockers"]


def test_unknown_target_does_not_claim_it_is_ready():
    plan = build_prerequisite_plan("dsa.not_a_real_skill")

    assert plan["status"] == "unknown_skill"
    assert plan["next_action"] == "map_curriculum_skill"


def test_graph_validator_reports_unknown_prerequisites_and_cycles():
    invalid_graph = {
        "skill.a": {"prerequisites": ["skill.b"]},
        "skill.b": {"prerequisites": ["skill.a", "skill.missing"]},
    }

    errors = validate_prerequisite_graph(invalid_graph)

    assert any("unknown prerequisite skill.missing" in error for error in errors)
    assert any("dependency cycle" in error for error in errors)
