import asyncio

from app.services import study_engine


class _QuestionQuery:
    def __init__(self, questions):
        self.questions = questions

    def prefer_verified(self):
        return self

    def to_list(self):
        return list(self.questions)


class _QuestionStore:
    def __init__(self, questions):
        self.questions = questions

    def find(self, _query):
        return _QuestionQuery(self.questions)


async def _company_profile(_user_id):
    return {"company_track": "tcs_nqt"}


def test_company_track_does_not_fall_back_to_unrelated_questions(monkeypatch):
    from app.services import question_store

    monkeypatch.setattr(study_engine, "_get_user_profile", _company_profile)
    monkeypatch.setattr(
        question_store,
        "find",
        lambda _query: _QuestionQuery([
            {
                "id": "unrelated-dsa",
                "title": "Binary Tree Traversal",
                "topic": "trees",
                "difficulty": "medium",
            }
        ]),
    )

    tasks = asyncio.run(
        study_engine._get_practice_tasks(
            "learner-1",
            assessment={"skills": {}},
            weak_areas=[{
                "domain_id": "quantitative_aptitude",
                "name": "Quantitative Aptitude",
                "score": 20,
                "reason": "Low demonstrated accuracy",
            }],
        )
    )

    assert len(tasks) == 1
    assert tasks[0]["kind"] == "weak_area"
    assert "question_id" not in tasks[0]


def test_company_track_keeps_matching_questions(monkeypatch):
    from app.services import question_store

    monkeypatch.setattr(study_engine, "_get_user_profile", _company_profile)
    monkeypatch.setattr(
        question_store,
        "find",
        lambda _query: _QuestionQuery([
            {
                "id": "tcs-percentages",
                "title": "Successive Percentages",
                "topic": "percentages",
                "difficulty": "easy",
            },
            {
                "id": "unrelated-dsa",
                "title": "Binary Tree Traversal",
                "topic": "trees",
                "difficulty": "medium",
            },
        ]),
    )

    tasks = __import__("asyncio").run(
        study_engine._get_practice_tasks(
            "learner-1",
            assessment={"skills": {}},
            weak_areas=[{
                "domain_id": "quantitative_aptitude",
                "name": "Quantitative Aptitude",
                "score": 20,
                "reason": "Low demonstrated accuracy",
            }],
        )
    )

    assert len(tasks) == 1
    assert tasks[0]["kind"] == "question"
    assert tasks[0]["question_id"] == "tcs-percentages"


def test_matching_question_rotation_is_stable_for_same_learner_and_day(monkeypatch):
    from app.services import question_store

    monkeypatch.setattr(study_engine, "_get_user_profile", _company_profile)
    monkeypatch.setattr(
        question_store,
        "find",
        lambda _query: _QuestionQuery([
            {"id": "tcs-percentages-a", "topic": "percentages", "companies": ["tcs"]},
            {"id": "tcs-percentages-b", "topic": "percentages", "companies": ["tcs"]},
        ]),
    )
    kwargs = {
        "user_id": "learner-stable",
        "assessment": {"skills": {}},
        "weak_areas": [{"domain_id": "quantitative_aptitude", "name": "Quantitative Aptitude", "score": 20}],
    }

    first = asyncio.run(study_engine._get_practice_tasks(**kwargs))
    second = asyncio.run(study_engine._get_practice_tasks(**kwargs))

    assert first == second
    assert first[0]["selection_reason"] == "stable_daily_rotation"
