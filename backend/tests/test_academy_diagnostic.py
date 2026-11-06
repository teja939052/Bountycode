from app.routes.academy_diagnostic import (
    canonical_domain,
    grade_diagnostic_answer,
    has_deterministic_key,
    skill_level,
)


def test_canonical_domain_maps_placement_categories():
    assert canonical_domain({"topic": "Quantitative Aptitude"}) == "quantitative_aptitude"
    assert canonical_domain({"domain": "SQL"}) == "sql"
    assert canonical_domain({"topic": "Arrays"}) == "arrays_hashing"


def test_diagnostic_only_uses_deterministically_gradable_questions():
    assert has_deterministic_key({"id": "q1", "options": ["A", "B"], "correct_index": 1})
    assert has_deterministic_key({"id": "q2", "correct_answer": "42"})
    assert not has_deterministic_key({"id": "q3", "question": "Write a program"})


def test_mcq_answer_is_graded_server_side():
    question = {"options": ["wrong", "right"], "correct_index": 1}
    assert grade_diagnostic_answer(question, "1")
    assert not grade_diagnostic_answer(question, "0")
    assert not grade_diagnostic_answer(question, "right")


def test_short_answer_grading_is_case_insensitive():
    assert grade_diagnostic_answer({"correct_answer": "SELECT"}, " select ")
    assert not grade_diagnostic_answer({"correct_answer": "SELECT"}, "UPDATE")


def test_skill_level_uses_conservative_bands():
    assert skill_level(20, 4) == "foundation_needed"
    assert skill_level(45, 4) == "beginner"
    assert skill_level(70, 4) == "developing"
    assert skill_level(90, 4) == "strong"
    assert skill_level(100, 0) == "not_assessed"
