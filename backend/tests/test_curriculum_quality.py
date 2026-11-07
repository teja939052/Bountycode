from app.services.curriculum_quality import score_lesson_content


def test_generic_template_content_is_flagged_for_authoring():
    result = score_lesson_content({
        "theory": "Learn about arrays. This is important in programming.",
        "sections": [
            {"heading": "Understanding arrays", "body": "Arrays are useful."},
        ],
        "code_example": {"code": "// TODO: Add arrays example\nprint('Learning about arrays')"},
        "exercises": [{
            "description": "Practice arrays",
            "expected_output": "Your program should correctly apply arrays.",
        }],
        "quizzes": [],
        "common_mistakes": [],
    })

    assert result["status"] == "needs_authoring"
    assert "placeholder_or_missing_code" in result["warnings"]
    assert "insufficient_assessment_depth" in result["warnings"]


def test_complete_authored_lesson_can_pass_quality_gate():
    result = score_lesson_content({
        "theory": "Arrays store ordered values in contiguous indexed positions. " * 4,
        "sections": [
            {"heading": "Memory layout", "body": "An array stores elements in contiguous memory. " * 5},
            {"heading": "Indexing", "body": "Indexing begins at zero in C-like languages. " * 5},
            {"heading": "Traversal", "body": "A loop visits each index exactly once. " * 5},
        ],
        "code_example": {"code": "int values[3] = {2, 4, 6};\nprintf(\"%d\", values[1]);"},
        "exercises": [
            {"description": "Return the largest value", "expected_output": "Input [2, 8, 4] returns 8."},
            {"description": "Count even values", "expected_output": "Input [2, 3, 6] returns 2."},
        ],
        "quizzes": [
            {"question": "What is the first index?", "options": ["0", "1"], "correct": 0, "explanation": "The first array index is zero." * 3},
            {"question": "What is indexed lookup complexity?", "options": ["O(1)", "O(n)"], "correct": 0, "explanation": "Indexed lookup is constant time." * 3},
            {"question": "What is traversal complexity?", "options": ["O(n)", "O(1)"], "correct": 0, "explanation": "A full traversal visits each element." * 3},
        ],
        "common_mistakes": [
            {"mistake": "Reading past the last index", "fix": "Stop at length minus one."},
            {"mistake": "Using an uninitialized array", "fix": "Initialize values before reading."},
        ],
    })

    assert result["status"] == "ready"
    assert result["score"] == 100



def test_hand_authored_singular_exercise_quiz_and_wrong_fixed_schema_is_supported():
    result = score_lesson_content({
        "theory": "A sufficiently detailed explanation of a programming concept. " * 5,
        "sections": [
            {"heading": "How it works", "body": "Detailed explanation of the mechanism. " * 5,
             "code": "value = 10\nprint(value)"},
            {"heading": "When to use it", "body": "Detailed explanation of a practical use. " * 5},
        ],
        "code_example": {"code": "value = 10\nprint(value)"},
        "exercise": {
            "description": "Read an integer and print its square.",
            "expected_output": "Input 4 produces 16.",
        },
        "quiz": {
            "question": "What is 4 squared?",
            "options": ["8", "16", "12", "4"],
            "correct": 1,
            "explanation": "Squaring multiplies a number by itself, so 4 times 4 is 16.",
        },
        "common_mistakes": [
            {"wrong": "value = '4' + 2", "fixed": "value = int('4') + 2",
             "why": "Convert text to an integer before arithmetic."},
            {"wrong": "print(Value)", "fixed": "print(value)",
             "why": "Python variable names are case-sensitive."},
        ],
    })

    assert "missing_exercise" not in result["warnings"]
    assert "insufficient_assessment_depth" not in result["warnings"]
    assert "missing_misconception_guidance" not in result["warnings"]


def test_code_embedded_in_sections_is_checked_for_placeholders():
    result = score_lesson_content({
        "theory": "A sufficiently detailed explanation of a programming concept. " * 5,
        "sections": [
            {"heading": "Example one", "body": "Detailed explanation. " * 8,
             "code": "// TODO: Add the real example"},
            {"heading": "Example two", "body": "Another detailed explanation. " * 8},
        ],
        "exercise": {"description": "Calculate a sum from two input numbers.",
                     "expected_output": "Inputs 2 and 3 produce 5."},
        "quiz": {"question": "What is 2 + 3?", "options": ["4", "5"],
                 "correct": 1, "explanation": "Adding two and three gives five." * 2},
        "common_mistakes": [
            {"mistake": "Wrong operator", "fix": "Use the addition operator."},
            {"mistake": "Wrong variable", "fix": "Use the declared variable."},
        ],
    })

    assert "placeholder_or_missing_code" in result["warnings"]
