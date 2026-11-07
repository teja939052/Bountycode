from app.data.lesson_content import get_lesson_content
from app.services.curriculum_quality import score_lesson_content


def test_java_authored_core_lessons_use_specific_content():
    cases = [
        ("java-l04-01", "if / else if / else", "score >= 90"),
        ("java-l05-01", "for Loop", "i <= 5"),
        ("java-l06-01", "Method Basics", "calculateTotal(int price, int quantity)"),
        ("java-l06-05", "Pass by Value (Everything)", "box.value = 99"),
        ("java-l07-01", "Arrays Basics", "int[] marks"),
        ("java-l07-04", "ArrayList", "marks.add(80)"),
        ("java-l02-03", "String & StringBuilder", "new StringBuilder()"),
        ("java-l09-01", "Classes & Objects", "class Student"),
        ("java-l09-02", "Constructors", "Product(String name, double price)"),
        ("java-l09-04", "Inheritance", "class Dog extends Animal"),
        ("java-l10-01", "Polymorphism Deep", "Shape shape = new Rectangle()"),
        ("java-l11-01", "HashMap Deep", "new HashMap<>()"),
    ]

    for lesson_id, title, expected_code in cases:
        lesson = get_lesson_content("java", lesson_id, title, "theory")
        assert expected_code in lesson["code_example"]["code"], title
        assert len(lesson["quizzes"]) == 3, title
        assert len(lesson["exercises"]) == 2, title
        assert score_lesson_content(lesson)["status"] == "ready", title
