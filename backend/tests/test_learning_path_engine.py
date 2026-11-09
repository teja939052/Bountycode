from app.services.learning_path_engine import build_personalized_learning_plan


def _evidence(correct_count=8):
    return [
        {
            "question_id": f"q-{index}",
            "correct": True,
            "server_graded": True,
        }
        for index in range(correct_count)
    ]


def test_path_engine_starts_with_earliest_unproven_prerequisite():
    plan = build_personalized_learning_plan(
        "dsa.recursion",
        observations_by_skill={},
        action_catalog=[
            {
                "action_id": "diagnose-variables",
                "skill_id": "coding.variables",
                "kind": "diagnostic",
                "estimated_minutes": 7,
                "expected_mastery_gain": 0.05,
                "uncertainty_reduction": 0.8,
            },
            {
                "action_id": "jump-to-recursion",
                "skill_id": "dsa.recursion",
                "kind": "challenge",
                "estimated_minutes": 20,
                "expected_mastery_gain": 0.7,
            },
        ],
        time_budget_minutes=20,
    )

    assert plan["status"] == "action_available"
    assert plan["next_skill_id"] == "coding.variables"
    assert plan["selected_action"]["action_id"] == "diagnose-variables"


def test_path_engine_advances_to_target_after_all_prerequisites_are_mastered():
    mastered = {
        skill_id: _evidence()
        for skill_id in (
            "coding.variables",
            "coding.types",
            "coding.conditions",
            "coding.functions",
            "coding.parameters",
            "coding.return",
        )
    }
    plan = build_personalized_learning_plan(
        "dsa.recursion",
        observations_by_skill=mastered,
        action_catalog=[
            {
                "action_id": "recursion-lesson",
                "skill_id": "dsa.recursion",
                "kind": "lesson",
                "estimated_minutes": 15,
                "expected_mastery_gain": 0.3,
            }
        ],
        time_budget_minutes=20,
    )

    assert plan["status"] == "action_available"
    assert plan["next_skill_id"] == "dsa.recursion"
    assert plan["selected_action"]["action_id"] == "recursion-lesson"


def test_path_engine_reports_content_gap_instead_of_selecting_unrelated_content():
    plan = build_personalized_learning_plan(
        "dsa.recursion",
        observations_by_skill={},
        action_catalog=[
            {
                "action_id": "unrelated-arrays",
                "skill_id": "dsa.arrays",
                "kind": "practice",
                "estimated_minutes": 10,
                "expected_mastery_gain": 0.5,
            }
        ],
        time_budget_minutes=20,
    )

    assert plan["status"] == "content_gap"
    assert plan["next_skill_id"] == "coding.variables"
    assert plan["selected_action"] is None


def test_path_engine_does_not_recommend_a_mastered_target_again():
    all_skills = {
        skill_id: _evidence()
        for skill_id in (
            "coding.variables",
            "coding.types",
            "coding.conditions",
            "coding.functions",
            "coding.parameters",
            "coding.return",
            "dsa.recursion",
        )
    }
    plan = build_personalized_learning_plan(
        "dsa.recursion",
        observations_by_skill=all_skills,
        action_catalog=[],
        time_budget_minutes=20,
    )

    assert plan["status"] == "target_mastered"
    assert plan["selected_action"] is None
