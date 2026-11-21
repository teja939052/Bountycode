from app.data.lesson_content import get_lesson_content
from app.services.curriculum_quality import score_lesson_content


def test_c_authored_core_lessons_use_specific_content():
    cases = [
        ("c-l04-01", "if Statement", "temperature > 30"),
        ("c-l04-02", "if-else Statement", "marks >= 40"),
        ("c-l05-01", "for Loop", "i <= 5"),
        ("c-l05-02", "while Loop", "attempts < 3"),
        ("c-l06-01", "Function Basics", "calculate_total(int price, int quantity)"),
        ("c-l07-01", "1D Array Basics", "int marks[5]"),
        ("c-l09-01", "What are Pointers?", "int *pointer = &score"),
        ("c-l10-01", "Structs", "typedef struct"),
        ("c-l11-01", "Singly Linked List", "typedef struct Node"),
        ("c-l11-07", "Binary Search Tree", "void inorder(Node *root)"),
    ]

    for lesson_id, title, expected_code in cases:
        lesson = get_lesson_content("c", lesson_id, title, "theory")
        assert expected_code in lesson["code_example"]["code"], title
        assert len(lesson["quizzes"]) == 3, title
        assert len(lesson["exercises"]) == 2, title
        assert score_lesson_content(lesson)["status"] == "ready", title
