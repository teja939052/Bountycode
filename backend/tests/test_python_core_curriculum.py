from app.data.lesson_content import get_lesson_content
from app.services.curriculum_quality import score_lesson_content


def test_python_conditionals_use_authored_lesson_content():
    lesson = get_lesson_content(
        "python",
        "python-l04-01",
        "if Statement",
        "theory",
    )

    assert "truthy" in lesson["theory"].lower()
    assert len(lesson["sections"]) == 3
    assert len(lesson["quizzes"]) == 3
    assert len(lesson["exercises"]) == 2
    assert "temperature" in lesson["code_example"]["code"]
    assert score_lesson_content(lesson)["status"] == "ready"


def test_python_loop_and_function_lessons_are_authored_not_generic_shells():
    cases = [
        ("python-l05-01", "for Loop with range()", "range(1, 6)"),
        ("python-l05-02", "while Loop", "attempts < 3"),
        ("python-l06-01", "def & return", "def calculate_total"),
    ]

    for lesson_id, title, expected_code in cases:
        lesson = get_lesson_content("python", lesson_id, title, "theory")
        assert expected_code in lesson["code_example"]["code"]
        assert len(lesson["quizzes"]) == 3
        assert len(lesson["exercises"]) == 2
        assert score_lesson_content(lesson)["status"] == "ready"
