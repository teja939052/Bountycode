import asyncio

from app.routes import quiz as quiz_routes


class _Cursor:
    def __init__(self, documents):
        self.documents = documents

    def sort(self, *_args, **_kwargs):
        return self

    async def to_list(self, _limit):
        return list(self.documents)


class _Collection:
    def __init__(self, document=None, documents=None):
        self.document = document
        self.documents = documents or []

    async def find_one(self, _query):
        return self.document

    def find(self, _query):
        return _Cursor(self.documents)


def test_quiz_evidence_reads_nested_skill_graph_records(monkeypatch):
    monkeypatch.setattr(
        quiz_routes,
        "skill_graph_collection",
        _Collection(document={
            "user_id": "learner-1",
            "skills": {
                "arrays_hashing": {"score": 25},
                "sql": {"score": 80},
                "verbal_ability": {"mastery_score": 55},
            },
        }),
    )
    monkeypatch.setattr(
        quiz_routes,
        "learning_events_collection",
        _Collection(documents=[
            {"question_id": "arrays-q1"},
            {"question_id": "sql-q1"},
        ]),
    )
    monkeypatch.setattr(
        quiz_routes,
        "srs_cards_collection",
        _Collection(documents=[]),
    )

    evidence = asyncio.run(quiz_routes._load_quiz_evidence("learner-1"))

    assert evidence["skill_scores"] == {
        "arrays_hashing": 0.25,
        "sql": 0.8,
        "verbal_ability": 0.55,
    }
    assert evidence["weak_skills"] == ["arrays_hashing", "verbal_ability"]
    assert evidence["seen_question_ids"] == ["arrays-q1", "sql-q1"]
