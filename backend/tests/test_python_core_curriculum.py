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



def test_python_decision_and_collection_lessons_use_authored_content():
    cases = [
        ("python-l04-04", "Nested Conditionals", "logged_in = True"),
        ("python-l04-05", "Ternary Expression", "status = 'Adult'"),
        ("python-l04-06", "Match-Case (3.10)", "match command:"),
        ("python-l05-03", "for...in with Lists", "for price in prices:"),
        ("python-l05-06", "List Comprehensions Deep", "squares_of_evens"),
    ]

    for lesson_id, title, expected_code in cases:
        lesson = get_lesson_content("python", lesson_id, title, "theory")
        assert expected_code in lesson["code_example"]["code"]
        assert len(lesson["quizzes"]) == 3
        assert len(lesson["exercises"]) == 2
        assert score_lesson_content(lesson)["status"] == "ready"



def test_python_lists_dictionaries_and_strings_use_authored_content():
    cases = [
        ("python-l07-01", "Lists Basics", "marks = [78, 91, 64]"),
        ("python-l07-02", "List Methods", "tasks.append('revise')"),
        ("python-l07-03", "Slicing", "values[::-1]"),
        ("python-l08-01", "String Methods Deep", "raw.strip().lower()"),
        ("python-l08-02", "f-strings & Formatting", "score:.2f"),
        ("python-l08-05", "dict Basics", "student.get('grade'"),
        ("python-l08-06", "dict Methods", "scores.items()"),
    ]

    for lesson_id, title, expected_code in cases:
        lesson = get_lesson_content("python", lesson_id, title, "theory")
        assert expected_code in lesson["code_example"]["code"]
        assert len(lesson["quizzes"]) == 3
        assert len(lesson["exercises"]) == 2
        assert score_lesson_content(lesson)["status"] == "ready"
