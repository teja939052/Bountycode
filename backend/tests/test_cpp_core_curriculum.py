from app.data.lesson_content import get_lesson_content
from app.services.curriculum_quality import score_lesson_content


def test_cpp_authored_core_lessons_use_specific_content():
    cases = [
        ("cpp-l04-01", "if / else if / else", "score >= 90"),
        ("cpp-l05-01", "for Loop", "i <= 5"),
        ("cpp-l06-01", "Function Basics", "calculateTotal(int price, int quantity)"),
        ("cpp-l06-05", "Pass by Value vs Reference", "void changeOriginal(int& x)"),
        ("cpp-l07-01", "C-style Arrays", "int marks[5]"),
        ("cpp-l07-03", "std::vector Basics", "values.push_back(2)"),
        ("cpp-l09-04", "Smart Pointers: unique_ptr", "make_unique<int>(42)"),
        ("cpp-l10-01", "Classes & Objects", "class Student"),
        ("cpp-l10-02", "Constructors & Destructors", "~User()"),
        ("cpp-l10-05", "Inheritance", "class Dog : public Animal"),
        ("cpp-l11-03", "STL: map & unordered_map", "unordered_map<string, int>"),
    ]

    for lesson_id, title, expected_code in cases:
        lesson = get_lesson_content("cpp", lesson_id, title, "theory")
        assert expected_code in lesson["code_example"]["code"], title
        assert len(lesson["quizzes"]) == 3, title
        assert len(lesson["exercises"]) == 2, title
        assert score_lesson_content(lesson)["status"] == "ready", title
