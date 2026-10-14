"""Independent-learning features: mistake notebook, deck, arena, teach-wall.

DB-backed route tests (skipped when Mongo unreachable) plus pure unit tests
for deterministic helpers. Follows tests/test_qa_15min.py patterns.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database import users_collection
from app.middleware.rate_limiter import clear_login_attempts


def _db_available() -> bool:
    try:
        from app.database import get_client
        import asyncio

        async def _ping():
            await get_client().admin.command("ping")

        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(_ping())
        finally:
            loop.close()
        return True
    except Exception:
        return False


needs_db = pytest.mark.skipif(not _db_available(), reason="MongoDB unreachable")
EMAIL = "indeplearn@example.com"


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.fixture(autouse=True)
async def clear_rate_limiter():
    from app.middleware.rate_limiter import request_counts
    request_counts.clear()
    yield
    request_counts.clear()


@pytest.fixture
async def test_user(client):
    clear_login_attempts(EMAIL)
    try:
        await users_collection().delete_many({"email": EMAIL})
    except Exception:
        pass
    body = None
    for attempt in range(3):
        r = await client.post(
            "/api/v1/auth/register",
            json={"email": EMAIL, "name": "Indie Learner", "password": "SecurePass123!"},
        )
        if r.status_code == 200:
            body = r.json()
            break
        # 504/5xx under load: the user row may still have been created; try login.
        try:
            lr = await client.post(
                "/api/v1/auth/login",
                json={"email": EMAIL, "password": "SecurePass123!"},
            )
            if lr.status_code == 200:
                body = lr.json()
                break
        except Exception:
            pass
    assert body is not None, f"register/login failed after retries: {r.status_code} {r.text[-200:]}"
    uid = body["user"]["id"]
    yield {"token": body["token"], "user_id": uid}
    for col_name in ("users_collection", "user_weaknesses_collection",
                     "srs_cards_collection", "learning_events_collection"):
        try:
            from app import database as db
            await getattr(db, col_name)().delete_many(
                {"email": EMAIL} if col_name == "users_collection" else {"user_id": uid})
        except Exception:
            pass


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


# ─── unit: deterministic helpers (no DB) ────────────────────────────
def test_teachwall_shuffle_is_deterministic():
    from app.routes.teachwall import _shuffle_opts, _teachable_nodes
    from app.services.tutor_engine import get_tutor_tree, load_tutor_trees

    trees = load_tutor_trees()
    assert trees, "no tutor trees on disk"
    tree_id = sorted(trees)[0]
    tree = get_tutor_tree(tree_id)
    nodes = _teachable_nodes(tree)
    assert nodes, f"tree {tree_id} has no teachable nodes"
    nid, node = nodes[0]
    a, _ = _shuffle_opts(f"{tree_id}:{nid}", node["opts"])
    b, _ = _shuffle_opts(f"{tree_id}:{nid}", node["opts"])
    assert [o["text"] for o in a] == [o["text"] for o in b]
    assert sorted(o["index"] for o in a) == list(range(len(node["opts"])))


def test_teachable_nodes_require_resolved_option():
    from app.routes.teachwall import _teachable_nodes
    from app.services.tutor_engine import load_tutor_trees, get_tutor_tree

    for tree_id in sorted(load_tutor_trees()):
        for _, node in _teachable_nodes(get_tutor_tree(tree_id)):
            assert any(o.get("code") == "resolved" for o in node["opts"])


def test_arena_strips_answers():
    from app.routes.arena import _public_question, _STRIP_KEYS

    q = {"id": "x", "question": "2+2?", "options": {"A": "3", "B": "4"},
         "correct_answer": "B", "solution": {"code": "x"}, "explanation": "add",
         "hints": ["think"], "type": "aptitude"}
    pub = _public_question(q)
    for k in _STRIP_KEYS:
        assert k not in pub
    assert "explanation" not in pub
    assert pub["options"] == {"A": "3", "B": "4"}
    assert pub["hints"] == ["think"]


def test_deck_card_shape():
    from app.routes.deck import _card_for_atom

    c = _card_for_atom("python.001", {"title": "T", "mental_model": "M",
                                      "why_this_matters": "W",
                                      "estimated_minutes": 8,
                                      "tutor_tree_id": "tutor.x"}, None)
    assert c["atom_id"] == "python.001"
    assert c["front"] == "T" and c["back"] == "M" and c["why"] == "W"
    assert c["has_tree"] is True


# ─── DB-backed route tests ──────────────────────────────────────────
@needs_db
async def test_recurring_mistakes_empty_for_new_user(client, test_user):
    r = await client.get("/api/v1/evidence/recurring-mistakes",
                         headers=_auth(test_user["token"]))
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["items"] == [] and body["total_tags"] == 0


@needs_db
async def test_recurring_mistakes_aggregates_tags(client, test_user):
    from app.database import user_weaknesses_collection
    uid = test_user["user_id"]
    await user_weaknesses_collection().insert_many([
        {"user_id": uid, "misconception_tag": "program_is_magic",
         "trigger_count": 14, "last_triggered": "2026-09-20T00:00:00",
         "status": "open", "question_id": "q1"},
        {"user_id": uid, "misconception_tag": "computer_guesses",
         "trigger_count": 3, "last_triggered": "2026-09-21T00:00:00",
         "status": "open", "question_id": "q2"},
    ])
    r = await client.get("/api/v1/evidence/recurring-mistakes?limit=5",
                         headers=_auth(test_user["token"]))
    assert r.status_code == 200, r.text
    items = r.json()["items"]
    assert len(items) == 2
    assert items[0]["tag"] == "program_is_magic" and items[0]["count"] == 14
    # program_is_magic maps to python.001 atom in the checked-in content
    assert items[0]["atom_id"] == "python.001"
    assert items[0]["fixable"] is True


@needs_db
async def test_deck_today_and_review_roundtrip(client, test_user):
    h = _auth(test_user["token"])
    r = await client.get("/api/v1/deck/today?limit=5", headers=h)
    assert r.status_code == 200, r.text
    cards = r.json()["cards"]
    assert 1 <= len(cards) <= 5
    assert all({"atom_id", "front", "back"} <= set(c) for c in cards)

    atom = cards[0]["atom_id"]
    r2 = await client.post("/api/v1/deck/review", headers=h,
                           json={"atom_id": atom, "grade": "good"})
    assert r2.status_code == 200, r2.text
    assert r2.json()["atom_id"] == atom

    r3 = await client.post("/api/v1/deck/review", headers=h,
                           json={"atom_id": atom, "grade": "bogus"})
    assert r3.status_code == 400


@needs_db
async def test_deck_review_unknown_atom_404(client, test_user):
    r = await client.post("/api/v1/deck/review", headers=_auth(test_user["token"]),
                          json={"atom_id": "nope.999", "grade": "good"})
    assert r.status_code == 404


@needs_db
async def test_arena_quiz_strips_answers_and_submit_grades(client, test_user):
    h = _auth(test_user["token"])
    r = await client.get("/api/v1/arena/quiz?count=3", headers=h)
    assert r.status_code == 200, r.text
    qs = r.json()["questions"]
    assert 1 <= len(qs) <= 3
    for q in qs:
        assert "correct_answer" not in q and "solution" not in q
        assert q.get("options"), "arena question missing options"

    # grade the first question by fetching the key server-side is impossible;
    # instead submit a wrong sentinel and expect a well-formed miss
    q0 = qs[0]
    r2 = await client.post("/api/v1/arena/submit", headers=h, json={
        "question_id": q0["id"], "answer": "ZZZ_WRONG_ANSWER",
        "time_spent_seconds": 12, "hints_used": 0, "timed": False})
    assert r2.status_code == 200, r2.text
    body = r2.json()
    assert body["correct"] is False and body["score"] == 0.0
    assert "correct_answer" in body and "explanation" in body


@needs_db
async def test_arena_rejects_unknown_and_non_mcq(client, test_user):
    h = _auth(test_user["token"])
    r = await client.post("/api/v1/arena/submit", headers=h,
                          json={"question_id": "nope", "answer": "A"})
    assert r.status_code == 404
    r2 = await client.get("/api/v1/arena/quiz?type=coding", headers=h)
    assert r2.status_code == 400


@needs_db
async def test_teachwall_challenge_answer_flow(client, test_user):
    h = _auth(test_user["token"])
    r = await client.get("/api/v1/teachwall/challenge", headers=h)
    assert r.status_code == 200, r.text
    ch = r.json()
    assert ch["options"] and len(ch["options"]) >= 2
    assert ch["node_ids"] and ch["node_id"] in ch["node_ids"]
    assert all("to" not in o and "code" not in o for o in ch["options"])

    # answer with shown index 0 — well-formed either way
    r2 = await client.post("/api/v1/teachwall/answer", headers=h, json={
        "tree_id": ch["tree_id"], "node_id": ch["node_id"], "option_index": 0})
    assert r2.status_code == 200, r2.text
    body = r2.json()
    assert isinstance(body["correct"], bool) and body["score"] in (0.0, 10.0)

    # determinism: same challenge again yields same option order
    r3 = await client.get("/api/v1/teachwall/challenge", headers=h)
    assert [o["text"] for o in r3.json()["options"]] == [o["text"] for o in ch["options"]]


@needs_db
async def test_teachwall_bad_ids(client, test_user):
    h = _auth(test_user["token"])
    r = await client.get("/api/v1/teachwall/challenge?atom_id=nope.999", headers=h)
    assert r.status_code == 404
    r2 = await client.post("/api/v1/teachwall/answer", headers=h, json={
        "tree_id": "nope", "node_id": "nope", "option_index": 0})
    assert r2.status_code in (400, 404)
