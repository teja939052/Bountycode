"""Regression tests for the canonical quiz question source."""
from app.services import question_store
from app.services import quiz_service


def test_quiz_loader_uses_canonical_student_servable_store(monkeypatch):
    questions = [
        {
            "id": "trusted-1",
            "topic": "arrays",
            "difficulty": "easy",
            "companies": ["TCS NQT"],
        },
        {
            "id": "trusted-2",
            "topic": "sql",
            "difficulty": "medium",
            "company": "Infosys SP",
        },
    ]
    calls = []

    class Cursor:
        def prefer_verified(self):
            calls.append("prefer_verified")
            return self

        def to_list(self):
            calls.append("to_list")
            return questions

    def canonical_find():
        calls.append("find")
        return Cursor()

    monkeypatch.setattr(question_store, "find", canonical_find)
    monkeypatch.setattr(quiz_service, "_questions_cache", None)
    monkeypatch.setattr(quiz_service, "_questions_by_id", None)
    monkeypatch.setattr(quiz_service, "_questions_by_topic", None)
    monkeypatch.setattr(quiz_service, "_questions_by_difficulty", None)
    monkeypatch.setattr(quiz_service, "_questions_by_company", None)

    loaded = quiz_service._load_questions()

    assert loaded == questions
    assert calls == ["find", "prefer_verified", "to_list"]
    assert quiz_service.get_question_by_id("trusted-1") == questions[0]
    assert quiz_service.get_questions_by_topic("arrays") == [questions[0]]
    assert quiz_service.get_questions_by_difficulty("medium") == [questions[1]]
    assert quiz_service.get_questions_by_company("tcs") == [questions[0]]
    assert quiz_service.get_questions_by_company("infosys") == [questions[1]]
