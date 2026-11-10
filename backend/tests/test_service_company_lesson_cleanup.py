"""Student-facing lesson copy must not contain internal drafting notes."""
from __future__ import annotations

import json
from pathlib import Path


LESSON = (
    Path(__file__).resolve().parents[1]
    / "app"
    / "data"
    / "lessons"
    / "flowchart_basics.json"
)


def test_flowchart_iteration_explanation_is_clean_and_correct():
    data = json.loads(LESSON.read_text(encoding="utf-8"))
    step = next(
        item for item in data["steps"]
        if item.get("title") == "Count the Iterations"
    )
    explanation = step["explanation"]

    assert "Wait - let me re-read" not in explanation
    assert "prints 1, 2 and 3" in explanation
    assert "4 <= 3 is false" in explanation
    assert "3 times" in explanation
    assert step["correct_index"] == 1
