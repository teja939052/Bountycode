from types import SimpleNamespace

from app.services.repair_service import _find_quizzes_for_skills


def test_repair_quizzes_are_filtered_to_the_requested_skills(monkeypatch):
    from app.content import role_content

    monkeypatch.setattr(role_content, "ALL_QUIZZES", {
        "sde": [
            SimpleNamespace(id="sql-joins-check", skills_tested=["sql"]),
            SimpleNamespace(id="array-pattern-check", skills_tested=["arrays_hashing"]),
            SimpleNamespace(id="mixed-check", skills_tested=["sql", "dbms"]),
        ],
    })

    assert _find_quizzes_for_skills(["sql"]) == [
        "sql-joins-check",
        "mixed-check",
    ]


def test_repair_quizzes_return_empty_when_no_quiz_covers_the_skill(monkeypatch):
    from app.content import role_content

    monkeypatch.setattr(role_content, "ALL_QUIZZES", {
        "sde": [
            SimpleNamespace(id="sql-joins-check", skills_tested=["sql"]),
        ],
    })

    assert _find_quizzes_for_skills(["trees"]) == []
