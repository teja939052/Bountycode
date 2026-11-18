from app.services import quiz_service


def _question(company):
    return {
        "id": "q1",
        "title": "Percentage change",
        "question": "A value increases by 10%. What is the new value of 100?",
        "topic": "Quantitative Aptitude",
        "difficulty": "easy",
        "companies": [company],
        "options": ["110", "100", "90", "120"],
        "correct_index": 0,
    }


def test_tcs_query_matches_tcs_nqt_question_tag(monkeypatch):
    monkeypatch.setattr(quiz_service, "_load_questions", lambda: [_question("TCS NQT")])

    quiz = quiz_service.build_quiz(
        mode="practice",
        company="TCS",
        num_questions=1,
        adaptive=False,
    )

    assert quiz["total_questions"] == 1
    assert quiz["questions"][0]["id"] == "q1"


def test_company_program_alias_matches_canonical_company_tag(monkeypatch):
    monkeypatch.setattr(quiz_service, "_load_questions", lambda: [_question("TCS")])

    quiz = quiz_service.build_quiz(
        mode="quiz",
        company="TCS NQT",
        num_questions=1,
        adaptive=False,
    )

    assert quiz["total_questions"] == 1


def test_company_matching_does_not_fall_back_to_unrelated_questions(monkeypatch):
    monkeypatch.setattr(quiz_service, "_load_questions", lambda: [_question("Infosys")])

    quiz = quiz_service.build_quiz(
        mode="quiz",
        company="TCS",
        num_questions=1,
        adaptive=False,
    )

    assert quiz["total_questions"] == 0
    assert quiz["empty_reason"] == "No questions match the selected filters."


def test_company_tag_normalization_handles_common_display_names():
    assert quiz_service._normalize_company_tag("Tech Mahindra") == "tech_mahindra"
    assert quiz_service._normalize_company_tag("LTI Mindtree") == "lti_mindtree"
    assert quiz_service._normalize_company_tag("Infosys Specialist Programmer") == "infosys"
    assert quiz_service._normalize_company_tag("Wipro Turbo") == "wipro"
