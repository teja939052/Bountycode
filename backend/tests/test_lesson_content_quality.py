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
