"""Structural checks for authored step-based placement lessons."""
from __future__ import annotations

import json
from pathlib import Path

LESSONS_DIR = Path(__file__).resolve().parents[1] / "app" / "data" / "lessons"


def test_all_step_based_lessons_have_valid_assessment_keys():
    seen_ids = set()
    lesson_count = 0

    for path in sorted(LESSONS_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        steps = data.get("steps") or []
        assessment = data.get("assessment") or {}
        questions = assessment.get("questions") or []

        # Legacy pattern packs are not served by the step-based lesson player.
        if not steps or not questions:
            continue

        lesson_count += 1
        lesson_id = data.get("id") or path.stem
        assert lesson_id not in seen_ids, f"Duplicate lesson id: {lesson_id}"
        seen_ids.add(lesson_id)
        assert 0 < float(assessment.get("mastery_threshold", data.get("mastery_threshold", 0.7))) <= 1

        for index, step in enumerate(steps):
            if step.get("step_type") not in {"interactive", "practice", "quiz"}:
                continue
            options = step.get("options") or []
            assert step.get("prompt"), f"{path.name} step {index + 1} has no prompt"
            assert len(options) >= 2, f"{path.name} step {index + 1} has fewer than two options"
            correct_index = step.get("correct_index")
            assert isinstance(correct_index, int) and 0 <= correct_index < len(options), (
                f"{path.name} step {index + 1} has an invalid answer key"
            )
            assert step.get("explanation"), f"{path.name} step {index + 1} has no explanation"

        for index, step in enumerate(steps):
            if step.get("step_type") in {"predict_output", "fill_blank"}:
                assert step.get("prompt"), f"{path.name} typed exercise {index + 1} has no prompt"
                assert step.get("expected_answer") is not None, (
                    f"{path.name} typed exercise {index + 1} has no expected answer"
                )
                assert step.get("explanation"), (
                    f"{path.name} typed exercise {index + 1} has no teaching explanation"
                )
                if step.get("step_type") == "predict_output":
                    assert step.get("code"), (
                        f"{path.name} output-prediction exercise {index + 1} has no code"
                    )

        for index, question in enumerate(questions):
            options = question.get("options") or []
            correct_index = question.get("correct_index")
            assert question.get("prompt"), f"{path.name} assessment question {index + 1} has no prompt"
            assert len(options) >= 2, f"{path.name} assessment question {index + 1} has fewer than two options"
            assert isinstance(correct_index, int) and 0 <= correct_index < len(options), (
                f"{path.name} assessment question {index + 1} has an invalid answer key"
            )
            assert question.get("explanation"), (
                f"{path.name} assessment question {index + 1} has no explanation"
            )

    assert lesson_count >= 25, f"Expected a substantial step-based lesson library, found {lesson_count}"

    # Typed exercises make code reading and repair part of the learning loop,
    # rather than limiting every interaction to multiple choice.
    assert any(
        step.get("step_type") in {"predict_output", "fill_blank"}
        for path in sorted(LESSONS_DIR.glob("*.json"))
        for step in (json.loads(path.read_text(encoding="utf-8")).get("steps") or [])
    ), "Expected at least one typed code-tracing or fill-in exercise"



def test_sequence_and_browser_code_labs_have_valid_instructions_and_checks():
    sequence_count = 0
    code_lab_count = 0

    for path in sorted(LESSONS_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for index, step in enumerate(data.get("steps") or []):
            kind = step.get("step_type")
            if kind == "order_steps":
                sequence_count += 1
                options = step.get("options") or []
                order = step.get("correct_order")
                assert step.get("prompt"), f"{path.name} sequence {index + 1} has no prompt"
                assert len(options) >= 3, f"{path.name} sequence {index + 1} needs at least three items"
                assert isinstance(order, list) and sorted(order) == list(range(len(options))), (
                    f"{path.name} sequence {index + 1} must order every item exactly once"
                )
                assert step.get("explanation"), f"{path.name} sequence {index + 1} has no explanation"
            elif kind == "code_lab":
                code_lab_count += 1
                assert step.get("language") == "javascript", (
                    f"{path.name} code lab {index + 1} must use the supported browser language"
                )
                assert step.get("prompt"), f"{path.name} code lab {index + 1} has no task prompt"
                assert step.get("starter_code"), f"{path.name} code lab {index + 1} has no starter code"
                assert isinstance(step.get("expected_output"), str), (
                    f"{path.name} code lab {index + 1} needs a visible deterministic output check"
                )
                assert step.get("hints"), f"{path.name} code lab {index + 1} needs progressive hints"

    assert sequence_count >= 2, "Expected at least two sequence-building exercises"
    assert code_lab_count >= 2, "Expected at least two runnable browser code labs"


def test_sql_labs_keep_grading_keys_server_side_and_ship_a_schema_preview():
    sql_labs = []
    for path in sorted(LESSONS_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for index, step in enumerate(data.get("steps") or []):
            if step.get("step_type") == "sql_lab":
                sql_labs.append((path, index, step))
                assert step.get("prompt"), f"{path.name} SQL lab {index + 1} has no prompt"
                assert step.get("schema_preview"), f"{path.name} SQL lab {index + 1} has no schema preview"
                assert step.get("sample_data"), f"{path.name} SQL lab {index + 1} has no sample data"
                assert step.get("schema_ddl") and step.get("seed_inserts"), f"{path.name} SQL lab {index + 1} needs a dataset"
                assert step.get("expected_query"), f"{path.name} SQL lab {index + 1} has no expected query"
                assert step.get("explanation") and step.get("hints"), f"{path.name} SQL lab {index + 1} needs feedback"
    assert sql_labs, "Expected at least one query-writing SQL lab"



def test_debug_and_api_scenarios_have_context_and_misconception_feedback():
    scenario_count = 0
    for path in sorted(LESSONS_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for index, step in enumerate(data.get("steps") or []):
            kind = step.get("step_type")
            if kind not in {"debug_choice", "api_scenario"}:
                continue
            scenario_count += 1
            options = step.get("options") or []
            answer = step.get("correct_index")
            assert step.get("prompt"), f"{path.name} scenario {index + 1} has no prompt"
            assert len(options) >= 3, f"{path.name} scenario {index + 1} needs at least three options"
            assert isinstance(answer, int) and 0 <= answer < len(options), (
                f"{path.name} scenario {index + 1} has an invalid answer key"
            )
            assert step.get("explanation"), f"{path.name} scenario {index + 1} needs a teaching explanation"
            feedback = step.get("feedback_by_option") or {}
            for option_index in range(len(options)):
                if option_index != answer:
                    assert str(option_index) in feedback, (
                        f"{path.name} scenario {index + 1} needs feedback for wrong option {option_index}"
                    )
            if kind == "debug_choice":
                assert step.get("code"), f"{path.name} debugging scenario {index + 1} needs a code sample"
            if kind == "api_scenario":
                assert step.get("request_preview"), (
                    f"{path.name} API scenario {index + 1} needs a request/response context"
                )
    assert scenario_count >= 2, "Expected at least one debugging and one API scenario"


def test_rich_lesson_authoring_standard_has_depth_and_company_transfer():
    lesson_path = LESSONS_DIR / "arrays_basics.json"
    lesson = json.loads(lesson_path.read_text(encoding="utf-8"))

    assert len(lesson.get("learning_objectives", [])) >= 4
    assert len(lesson.get("prerequisites", [])) >= 1
    assert len(lesson.get("concepts", [])) >= 5
    assert len(lesson.get("common_misconceptions", [])) >= 3
    assert len(lesson.get("worked_examples", [])) >= 3
    assert len(lesson.get("company_applications", [])) >= 3
    assert len(lesson.get("assessment", {}).get("questions", [])) >= 5
    assert len(lesson.get("srs_cards", [])) >= 3

    for example in lesson["worked_examples"]:
        assert example.get("input")
        assert len(example.get("trace", [])) >= 2
        assert example.get("output")
        assert example.get("explanation")

    for misconception in lesson["common_misconceptions"]:
        assert misconception.get("misconception")
        assert misconception.get("correction")

    for question in lesson["assessment"]["questions"]:
        assert question.get("explanation")
        assert len(question.get("options", [])) >= 4
        assert 0 <= question.get("correct_index", -1) < len(question["options"])


def test_core_foundation_lessons_follow_the_rich_authoring_contract():
    core_lessons = [
        "variables_basics",
        "conditions_basics",
        "functions_basics",
        "programming_languages",
        "loops_basics",
        "arrays_basics",
        "strings_basics",
        "dbms_basics",
        "sql_select_basics",
    ]
    for slug in core_lessons:
        lesson = json.loads((LESSONS_DIR / f"{slug}.json").read_text(encoding="utf-8"))
        assert len(lesson.get("learning_objectives", [])) >= 4, slug
        assert len(lesson.get("concepts", [])) >= 5, slug
        assert len(lesson.get("common_misconceptions", [])) >= 3, slug
        assert len(lesson.get("worked_examples", [])) >= 3, slug
        assert len(lesson.get("company_applications", [])) >= 3, slug
        assert len(lesson.get("srs_cards", [])) >= 3, slug
        for example in lesson["worked_examples"]:
            assert example.get("input"), slug
            assert len(example.get("trace", [])) >= 2, slug
            assert example.get("output"), slug
            assert example.get("explanation"), slug



def test_programming_foundations_form_a_complete_prerequisite_chain():
    variables = json.loads((LESSONS_DIR / "variables_basics.json").read_text(encoding="utf-8"))
    conditions = json.loads((LESSONS_DIR / "conditions_basics.json").read_text(encoding="utf-8"))
    functions = json.loads((LESSONS_DIR / "functions_basics.json").read_text(encoding="utf-8"))

    assert variables["prerequisites"] == []
    assert "variables_basics" in conditions["prerequisites"]
    assert {"variables_basics", "conditions_basics"}.issubset(set(functions["prerequisites"]))

    for lesson in (variables, conditions, functions):
        assert len(lesson["steps"]) >= 8
        types = {step["step_type"] for step in lesson["steps"]}
        assert {"explain", "interactive", "practice", "predict_output", "order_steps", "code_lab", "debug_choice"}.issubset(types)
        assert len(lesson["assessment"]["questions"]) >= 5
        assert len(lesson["worked_examples"]) >= 3
        assert len(lesson["company_applications"]) >= 3



def test_programming_foundation_lessons_link_to_the_next_course_step():
    expected = {
        "variables_basics": "conditions_basics",
        "conditions_basics": "functions_basics",
        "functions_basics": "programming_languages",
    }
    for slug, next_slug in expected.items():
        lesson = json.loads((LESSONS_DIR / f"{slug}.json").read_text(encoding="utf-8"))
        assert lesson.get("next_lesson_slug") == next_slug
        assert lesson.get("next_lesson_title")
        quest = lesson.get("quest") or {}
        assert quest.get("chapter")
        assert quest.get("story")
        assert quest.get("mission")
        assert len(quest.get("success_criteria") or []) >= 3
