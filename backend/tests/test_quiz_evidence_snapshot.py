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



class _SRSCollection:
    def __init__(self, existing=None):
        self.existing = existing
        self.saved = None

    async def find_one(self, _query):
        return self.existing

    async def update_one(self, _query, update, upsert=False):
        self.saved = update["$set"]
        return type("UpdateResult", (), {"modified_count": 1})()


def test_quiz_srs_creates_a_review_card_for_a_new_question(monkeypatch):
    from app.services import study_engine

    collection = _SRSCollection()
    monkeypatch.setattr(quiz_routes, "srs_cards_collection", collection)

    async def no_op_invalidate(_user_id):
        return None

    monkeypatch.setattr(study_engine, "invalidate_daily_plan", no_op_invalidate)

    updated = asyncio.run(quiz_routes._update_quiz_srs(
        "learner-1", "question-1", True
    ))

    assert updated is True
    assert collection.saved["user_id"] == "learner-1"
    assert collection.saved["concept_id"] == "question-1"
    assert collection.saved["problem_id"] == "question-1"
    assert collection.saved["total_reviews"] == 1
    assert collection.saved["next_review"] is not None


def test_failed_quiz_answer_schedules_a_short_srs_retry(monkeypatch):
    from app.services import study_engine

    collection = _SRSCollection()
    monkeypatch.setattr(quiz_routes, "srs_cards_collection", collection)

    async def no_op_invalidate(_user_id):
        return None

    monkeypatch.setattr(study_engine, "invalidate_daily_plan", no_op_invalidate)

    updated = asyncio.run(quiz_routes._update_quiz_srs(
        "learner-1", "question-2", False
    ))

    assert updated is True
    assert collection.saved["total_reviews"] == 1
    assert collection.saved["repetitions"] == 0
    assert collection.saved["interval"] == 0
    assert collection.saved["next_review"] is not None



def test_due_question_card_contributes_its_skill_to_adaptive_evidence(monkeypatch):
    monkeypatch.setattr(
        quiz_routes,
        "skill_graph_collection",
        _Collection(document={"user_id": "learner-1", "skills": {}}),
    )
    monkeypatch.setattr(
        quiz_routes,
        "learning_events_collection",
        _Collection(documents=[]),
    )
    monkeypatch.setattr(
        quiz_routes,
        "srs_cards_collection",
        _Collection(documents=[{
            "user_id": "learner-1",
            "concept_id": "sql-question-1",
            "next_review": "2000-01-01T00:00:00+00:00",
        }]),
    )
    monkeypatch.setattr(
        quiz_routes,
        "get_question_by_id",
        lambda question_id: {
            "id": question_id,
            "topic": "SQL",
            "sub_topic": "joins",
            "difficulty": "easy",
        },
    )

    evidence = asyncio.run(quiz_routes._load_quiz_evidence("learner-1"))

    assert "sql-question-1" in evidence["due_skills"]
    assert "sql" in evidence["due_skills"]
    assert "joins" in evidence["due_skills"]


def test_unknown_quiz_metadata_stays_unclassified():
    assert quiz_routes._quiz_skill_domain({
        "topic": "Unmapped vendor category",
        "sub_topic": "miscellaneous",
    }) is None


def test_known_quiz_metadata_maps_to_a_supported_skill_domain():
    assert quiz_routes._quiz_skill_domain({
        "topic": "SQL",
        "sub_topic": "joins",
    }) == "sql"
