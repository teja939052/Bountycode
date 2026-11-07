from app.services.adaptive_quiz_composer import compose_quiz


def _question(qid, skill, difficulty="medium", companies=None):
    return {
        "id": qid,
        "topic": skill,
        "skills": [skill],
        "difficulty": difficulty,
        "companies": companies or [],
        "correct_answer": "ok",
    }


def test_same_evidence_and_seed_produce_same_form_and_explanation():
    questions = [
        _question("arrays-1", "arrays"),
        _question("arrays-2", "arrays"),
        _question("sql-1", "sql", companies=["tcs"]),
        _question("graphs-1", "graphs"),
    ]
    evidence = {
        "skill_scores": {"arrays": 0.25, "sql": 0.8, "graphs": 0.5},
        "weak_skills": ["arrays"],
        "due_skills": ["graphs"],
        "seen_question_ids": ["arrays-1"],
    }
    first = compose_quiz(questions, num_questions=3, seed="learner-1-form-1", evidence=evidence, company="tcs")
    second = compose_quiz(questions, num_questions=3, seed="learner-1-form-1", evidence=evidence, company="tcs")

    assert [q["id"] for q in first["questions"]] == [q["id"] for q in second["questions"]]
    assert first["selection_evidence"] == second["selection_evidence"]
    assert first["strategy"] == "evidence_first_deterministic_v1"
    assert any(item["question_id"] == "sql-1" and item["company_match"] for item in first["selection_evidence"])


def test_composer_does_not_exhaust_one_skill_when_other_skills_are_available():
    questions = [
        _question("arrays-1", "arrays"),
        _question("arrays-2", "arrays"),
        _question("arrays-3", "arrays"),
        _question("graphs-1", "graphs"),
        _question("sql-1", "sql"),
    ]
    result = compose_quiz(
        questions,
        num_questions=4,
        seed="balanced-form",
        evidence={"skill_scores": {"arrays": 0.1, "graphs": 0.2, "sql": 0.2}},
    )

    assert len(result["questions"]) == 4
    assert len(result["skill_distribution"]) >= 2
