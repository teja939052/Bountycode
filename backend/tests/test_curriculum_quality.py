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
            {"options": ["0", "1"], "explanation": "The first array index is zero." * 3},
            {"options": ["O(1)", "O(n)"], "explanation": "Indexed lookup is constant time." * 3},
            {"options": ["O(n)", "O(1)"], "explanation": "A full traversal visits each element." * 3},
        ],
        "common_mistakes": [
            {"mistake": "Reading past the last index", "fix": "Stop at length minus one."},
            {"mistake": "Using an uninitialized array", "fix": "Initialize values before reading."},
        ],
    })

    assert result["status"] == "ready"
    assert result["score"] == 100
