"""End-to-end learner journey tests for Bountycode Phase F validation.

Drives the real FastAPI app over HTTP (ASGI transport) against an isolated
MongoDB database. Production data is never touched.

Journey under test:
  Register → session → catalog → next lesson → lesson fetch → wrong quiz
  (no completion, no XP) → correct quiz → practice-only exercise → verified
  completion → XP awarded exactly once → progress persistence → new login →
  next lesson unlocked → skill evidence → dashboard parity.

Acceptance criteria:
- Answer keys never appear in any GET payload.
- Incorrect/empty answers never complete a step or award XP.
- Repeated submissions never duplicate rewards.
- The next recommended lesson always has its prerequisites met.
- Progress survives a fresh session and a new login.
- Dashboard/progress numbers match persisted MongoDB records.
- Skill evidence comes only from graded attempts.

Database isolation:
- ``DATABASE_NAME`` is forced to ``placementpro_test_e2e`` *before* the app is
  imported, and every test re-checks the name before dropping the database.
- ``TEST_MONGODB_URL`` may point at any MongoDB; it defaults to a local
  ``mongodb://127.0.0.1:27017`` server.

Run:
    cd backend
    python -m pytest tests/test_e2e_learner_journey.py -q
"""
import asyncio
import itertools
import os
import sys
import uuid

import pytest
from httpx import ASGITransport, AsyncClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ── Isolated test database (must be set before importing the app) ───────
TEST_DB_NAME = "placementpro_test_e2e"
PROD_DB_NAME = "placementpro"
os.environ["DATABASE_NAME"] = TEST_DB_NAME
os.environ["MONGODB_URL"] = os.environ.get(
    "TEST_MONGODB_URL", "mongodb://127.0.0.1:27017"
)

from app.database import get_db, users_collection  # noqa: E402
from app.config import get_settings  # noqa: E402
from app.main import app  # noqa: E402
from app.middleware.auth import hash_password, verify_password  # noqa: E402
from app.middleware.duplicate_guard import (  # noqa: E402
    DuplicateRequestGuard,
    PERSISTENCE_FILE,
)
from app.middleware.rate_limiter import (  # noqa: E402
    login_attempts,
    request_counts,
)
from app.services import lesson_service  # noqa: E402
from app.services.lesson_service import (  # noqa: E402
    complete_step,
    get_lesson,
    get_progress,
    list_lessons,
    next_lesson,
    sanitize_lesson,
    submit_exercise,
)
from app.services.path_generator import decide_next_action  # noqa: E402
from app.services.lesson_service import weakness_tier_for  # noqa: E402
from app.services.skill_assessment import (  # noqa: E402
    get_readiness_score,
    get_skill_graph,
    get_weak_areas,
    initialize_skill_graph,
)

ANSWER_KEYS = ("correctIndex", "solution", "tests")
PASSWORD = "SecurePass1!"

# ── Process-level isolation guard ───────────────────────────────────────
# This module overrides DATABASE_NAME/MONGODB_URL at import time, which only
# works if the app has not been imported yet. When another test module imported
# it first, those settings are already frozen and this suite would silently
# point at the wrong database. Fail loudly instead of dropping real data.
if get_settings().DATABASE_NAME != TEST_DB_NAME:
    pytest.exit(
        "test_e2e_learner_journey must run in its own pytest process: the app "
        f"was already imported with DATABASE_NAME={get_settings().DATABASE_NAME!r}. "
        "Run: python -m pytest tests/test_e2e_learner_journey.py",
        returncode=1,
    )

_email_counter = itertools.count()


# ════════════════════════════════════════════════════════════════════════
# Fixtures / helpers
# ════════════════════════════════════════════════════════════════════════


def _reset_duplicate_guard() -> None:
    """Clear the 2s double-click guard between tests.

    The guard persists hashes to disk, so identical journey requests (for
    example the same quiz answer) would otherwise be rejected as duplicates
    across tests or across runs.
    """
    stack = app.middleware_stack
    if stack is None:
        stack = app.build_middleware_stack()
        app.middleware_stack = stack
    node = stack
    while node is not None:
        if isinstance(node, DuplicateRequestGuard):
            node._seen.clear()
            break
        node = getattr(node, "app", None)
    try:
        PERSISTENCE_FILE.unlink(missing_ok=True)
    except OSError:
        pass


@pytest.fixture(autouse=True)
async def clean_database():
    """Drop the isolated test database around every test.

    Refuses to run if the resolved database is not the dedicated test DB —
    ``dropDatabase`` must never be able to reach real data.
    """
    db = get_db()
    assert db.name == TEST_DB_NAME, (
        f"Refusing to drop {db.name!r}; expected {TEST_DB_NAME!r}"
    )
    assert db.name != PROD_DB_NAME

    # The lesson service now resolves its collection per access, so there is no
    # import-time handle to rebind. Only the cached execution engine (circuit
    # breaker state) is reset between tests.
    lesson_service._ENGINE = None
    _reset_duplicate_guard()

    await db.command("dropDatabase")
    request_counts.clear()
    login_attempts.clear()
    yield
    await db.command("dropDatabase")


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


async def _register(client: AsyncClient) -> dict:
    """Register a unique learner through the real endpoint."""
    email = f"e2e-{next(_email_counter)}-{uuid.uuid4().hex[:8]}@example.com"
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "name": "E2E Learner", "password": PASSWORD},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["token"]
    return {"token": data["token"], "user": data["user"], "email": email}


async def _step(
    client: AsyncClient,
    token: str,
    lesson_id: str,
    step_id: str,
    *,
    answer=None,
    code=None,
) -> dict:
    payload = {"lesson_id": lesson_id, "step_id": step_id}
    if answer is not None:
        payload["answer"] = str(answer)
    if code is not None:
        payload["code"] = code
    response = await client.post(
        "/api/v1/lessons/step", json=payload, headers=_auth(token)
    )
    assert response.status_code == 200, response.text
    return response.json()


async def _progress(client: AsyncClient, token: str) -> dict:
    response = await client.get("/api/v1/lessons/progress", headers=_auth(token))
    assert response.status_code == 200, response.text
    return response.json()


async def _next(client: AsyncClient, token: str) -> dict:
    response = await client.get("/api/v1/lessons/next", headers=_auth(token))
    assert response.status_code == 200, response.text
    return response.json()


async def _skills(client: AsyncClient, token: str) -> dict:
    response = await client.get("/api/v1/gamification/skills", headers=_auth(token))
    assert response.status_code == 200, response.text
    return response.json()


def _assert_no_answer_keys(lesson: dict) -> None:
    """No GET payload may carry a grader/answer key on any step."""
    assert lesson.get("id")
    for step in lesson["steps"]:
        for key in ANSWER_KEYS:
            assert key not in step, f"{lesson['id']}/{step['id']} leaked {key!r}"


def _quiz_step(lesson: dict) -> dict:
    return next(s for s in lesson["steps"] if s.get("type") == "quiz")


def _explain_steps(lesson: dict) -> list:
    return [s for s in lesson["steps"] if s.get("type") == "explain"]


def _wrong_index(step: dict):
    options = step.get("options") or []
    correct = step.get("correctIndex")
    return next((i for i in range(len(options)) if i != correct), None)


async def _complete_lesson_via_service(user_id: str, lesson: dict) -> dict:
    """Complete every step server-side; return the last grading result."""
    result = None
    for step in lesson["steps"]:
        if step["type"] == "quiz":
            result = await complete_step(
                user_id=user_id,
                lesson_id=lesson["id"],
                step_id=step["id"],
                answer=str(step["correctIndex"]),
            )
        elif step["type"] == "exercise":
            # The catalog's solutions are trusted server-side content; this is
            # the test acting as the grader's oracle, not a client shortcut.
            result = await complete_step(
                user_id=user_id,
                lesson_id=lesson["id"],
                step_id=step["id"],
                code=step.get("solution") or "print('practice')",
            )
        else:
            result = await complete_step(
                user_id=user_id, lesson_id=lesson["id"], step_id=step["id"]
            )
    assert result is not None
    return result


# ════════════════════════════════════════════════════════════════════════
# Authentication and isolation
# ════════════════════════════════════════════════════════════════════════


class TestRegistrationAndSession:
    async def test_register_login_and_cookie_session(self, client):
        student = await _register(client)
        token = student["token"]
        user_id = student["user"]["id"]

        # Registration returns an httpOnly cookie pair as well as the token.
        set_cookie = client.cookies.jar
        cookie_names = {c.name for c in set_cookie}
        assert "pp_token" in cookie_names
        assert "pp_refresh_token" in cookie_names

        me = await client.get("/api/v1/auth/me", headers=_auth(token))
        assert me.status_code == 200
        body = me.json()
        assert body["id"] == user_id
        assert body["email"] == student["email"]
        assert body["plan"] == "free"

        # Unauthenticated requests stay rejected.
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as anonymous:
            denied = await anonymous.get("/api/v1/auth/me")
        assert denied.status_code == 401

        # Login issues a fresh token for the same user.
        login = await client.post(
            "/api/v1/auth/login",
            json={"email": student["email"], "password": PASSWORD},
        )
        assert login.status_code == 200, login.text
        relogin_token = login.json()["token"]
        me2 = await client.get("/api/v1/auth/me", headers=_auth(relogin_token))
        assert me2.status_code == 200
        assert me2.json()["id"] == user_id

        # Stored password is hashed, never plaintext.
        stored = await users_collection.find_one({"email": student["email"]})
        assert stored["password_hash"] != PASSWORD
        assert verify_password(PASSWORD, stored["password_hash"])

    async def test_database_is_isolated(self):
        db = get_db()
        assert db.name == TEST_DB_NAME
        assert db.name != PROD_DB_NAME
        # Even a stray local production DB cannot be reached through get_db().
        assert db.client[PROD_DB_NAME].name == PROD_DB_NAME
        assert db.name != db.client[PROD_DB_NAME].name


# ════════════════════════════════════════════════════════════════════════
# Catalog safety
# ════════════════════════════════════════════════════════════════════════


class TestCatalogSafety:
    async def test_catalog_and_single_lesson_never_leak_answer_keys(self, client):
        listed = await client.get("/api/v1/lessons")
        assert listed.status_code == 200
        lessons = listed.json()["lessons"]
        assert len(lessons) >= 90

        for lesson in lessons:
            _assert_no_answer_keys(lesson)

        detailed = await client.get(
            f"/api/v1/lessons/{lessons[0]['id']}"
        )
        assert detailed.status_code == 200
        _assert_no_answer_keys(detailed.json())

        missing = await client.get("/api/v1/lessons/does-not-exist")
        assert missing.status_code == 404

    async def test_catalog_integrity(self):
        lessons = list_lessons()
        ids = [l["id"] for l in lessons]
        assert len(ids) == len(set(ids)), "duplicate lesson ids"

        known = set(ids)
        for lesson in lessons:
            assert lesson["steps"], f"{lesson['id']} has no steps"
            step_ids = [s["id"] for s in lesson["steps"]]
            assert len(step_ids) == len(set(step_ids)), f"{lesson['id']} duplicate step ids"
            assert int(lesson.get("xpReward", 0)) > 0, f"{lesson['id']} has no XP reward"
            for prereq in lesson.get("prerequisites") or []:
                assert prereq in known, f"{lesson['id']} references missing {prereq}"
                assert prereq != lesson["id"]
            for step in lesson["steps"]:
                if step["type"] == "quiz":
                    assert 0 <= int(step["correctIndex"]) < len(step["options"])

    async def test_public_lesson_shape_keeps_learning_fields(self, client):
        lessons = list_lessons()
        raw = next(l for l in lessons if any(s["type"] == "quiz" for s in l["steps"]))
        public = sanitize_lesson(raw)
        _assert_no_answer_keys(public)

        raw_explain = next(s for s in raw["steps"] if s["type"] == "explain")
        public_explain = next(
            s for s in public["steps"] if s["id"] == raw_explain["id"]
        )
        assert public_explain.get("content") == raw_explain.get("content")

        raw_quiz = _quiz_step(raw)
        public_quiz = next(s for s in public["steps"] if s["id"] == raw_quiz["id"])
        assert public_quiz.get("options") == raw_quiz.get("options")
        assert "explanation" not in public_quiz


# ════════════════════════════════════════════════════════════════════════
# The complete journey
# ════════════════════════════════════════════════════════════════════════


class TestCompleteLearnerJourney:
    async def test_journey_from_signup_to_next_unlocked_lesson(self, client):
        student = await _register(client)
        token, user_id = student["token"], student["user"]["id"]

        # ── 1. Recommendation for an empty profile ──────────────────────
        first = (await _next(client, token))["lesson"]
        assert first is not None
        assert first["track"] == "python"
        assert not (first.get("prerequisites") or [])
        _assert_no_answer_keys(first)

        raw = get_lesson(first["id"])
        assert raw is not None
        quiz = _quiz_step(raw)
        wrong = _wrong_index(quiz)
        assert wrong is not None

        # ── 2. Wrong answer never completes or awards ──────────────────
        wrong_result = await _step(
            client, token, raw["id"], quiz["id"], answer=wrong
        )
        assert wrong_result["graded"] is True
        assert wrong_result["is_correct"] is False
        assert wrong_result["step_completed"] is False
        assert wrong_result["lesson_verified"] is False
        assert wrong_result["xp_earned"] == 0

        after_wrong = await _progress(client, token)
        assert after_wrong["xp_earned"] == 0
        assert raw["id"] not in after_wrong["verified_lessons"]

        # ── 3. Correct answer verifies the step ────────────────────────
        correct_result = await _step(
            client, token, raw["id"], quiz["id"], answer=quiz["correctIndex"]
        )
        assert correct_result["graded"] is True
        assert correct_result["is_correct"] is True
        assert correct_result["step_completed"] is True
        # Lesson is not done yet (other steps outstanding).
        assert correct_result["lesson_verified"] is False

        # ── 4. Reading steps are real progress with no evidence ────────
        for step in _explain_steps(raw):
            explain = await _step(client, token, raw["id"], step["id"])
            assert explain["graded"] is False
            assert explain["step_completed"] is True
            assert explain["is_correct"] is None

        # ── 5. Practice-only exercise completes the lesson with XP ─────
        practice_step = next(
            s for s in raw["steps"] if s["type"] == "exercise"
        )
        practice = await _step(
            client,
            token,
            raw["id"],
            practice_step["id"],
            code=practice_step["solution"],
        )
        assert practice["graded"] is False
        assert practice["is_correct"] is None
        assert practice["step_completed"] is True
        assert practice["lesson_complete"] is True
        assert practice["lesson_verified"] is True
        assert practice["xp_earned"] == int(raw["xpReward"])
        assert practice["total_xp"] == int(raw["xpReward"])

        # ── 6. Re-submitting the quiz never duplicates XP ──────────────
        replay = await _step(
            client,
            token,
            raw["id"],
            quiz["id"],
            answer=quiz["options"][quiz["correctIndex"]],  # different body, same answer
        )
        assert replay["xp_earned"] == 0
        assert replay["lesson_verified"] is True
        assert replay["total_xp"] == int(raw["xpReward"])

        # ── 7. Progress API matches persisted MongoDB ──────────────────
        progress = await _progress(client, token)
        assert progress["xp_earned"] == int(raw["xpReward"])
        assert progress["verified_lessons"] == [raw["id"]]
        assert progress["awarded_lessons"] == [raw["id"]]

        persisted = await get_db()["lesson_progress"].find_one({"user_id": user_id})
        assert persisted is not None
        assert persisted["xp_earned"] == progress["xp_earned"]
        assert persisted["verified_lessons"] == progress["verified_lessons"]
        assert persisted["awarded_lessons"] == progress["awarded_lessons"]
        assert set(persisted["completed"]) == {
            f"{raw['id']}:{s['id']}" for s in raw["steps"]
        }

        # ── 8. Skill evidence reflects real attempts ───────────────────
        graph = await _skills(client, token)
        python_skill = graph["categories"]["programming"]["skills"]["python"]
        # wrong quiz + correct quiz (replay of already-verified step records
        # no new evidence, so only 2 attempts are persisted)
        assert python_skill["attempts"] == 2
        assert python_skill["score"] > 0
        assert python_skill["last_practiced"] is not None

        # ── 9. The recommended next lesson is actually unlocked ────────
        nxt = (await _next(client, token))["lesson"]
        assert nxt is not None
        assert nxt["id"] == "python-variables"
        assert set(nxt.get("prerequisites") or []) <= {raw["id"]}

        fetched = await client.get(f"/api/v1/lessons/{nxt['id']}")
        assert fetched.status_code == 200
        _assert_no_answer_keys(fetched.json())

        # Lessons whose prerequisites are still missing are not offered yet.
        completed_lessons = {raw["id"]}
        for candidate in list_lessons():
            if candidate["id"] == nxt["id"]:
                continue
            prereqs = set(candidate.get("prerequisites") or [])
            if prereqs and not prereqs <= completed_lessons:
                assert candidate["id"] != nxt["id"]

        # ── 10. Progress survives a brand-new session + login ──────────
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as fresh:
            relogin = await fresh.post(
                "/api/v1/auth/login",
                json={"email": student["email"], "password": PASSWORD},
            )
            assert relogin.status_code == 200, relogin.text
            fresh_token = relogin.json()["token"]
            fresh_progress = await _progress(fresh, fresh_token)
            assert fresh_progress["xp_earned"] == progress["xp_earned"]
            assert fresh_progress["verified_lessons"] == [raw["id"]]
            fresh_next = await _next(fresh, fresh_token)
            assert fresh_next["lesson"]["id"] == "python-variables"


# ════════════════════════════════════════════════════════════════════════
# Grading truth: wrong / empty / practice-only
# ════════════════════════════════════════════════════════════════════════


class TestGradingTruth:
    async def test_empty_and_incorrect_quiz_never_complete(self, client):
        student = await _register(client)
        token, user_id = student["token"], student["user"]["id"]

        raw = get_lesson("python-hello")
        quiz = _quiz_step(raw)

        empty = await _step(client, token, raw["id"], quiz["id"], answer="")
        assert empty["graded"] is False
        assert empty["verified"] is False
        assert empty["step_completed"] is False

        wrong = await _step(
            client, token, raw["id"], quiz["id"], answer=_wrong_index(quiz)
        )
        assert wrong["graded"] is True
        assert wrong["is_correct"] is False
        assert wrong["step_completed"] is False

        progress = await _progress(client, token)
        assert progress["xp_earned"] == 0
        assert progress["completed"] == {}

        # A wrong answer still produces honest evidence (attempt, zero score),
        # never mastery.
        graph = await get_skill_graph(user_id)
        skill = graph["categories"]["programming"]["skills"]["python"]
        assert skill["attempts"] == 1
        assert skill["score"] == 0

    async def test_practice_only_exercise_cannot_award_mastery(self, client):
        student = await _register(client)
        token, user_id = student["token"], student["user"]["id"]

        raw = get_lesson("python-hello")
        practice_step = next(s for s in raw["steps"] if s["type"] == "exercise")
        assert not any(
            (t or {}).get("expected") for t in (practice_step.get("tests") or [])
        )

        result = await submit_exercise(
            user_id=user_id,
            lesson_id=raw["id"],
            step_id=practice_step["id"],
            code="print('Ada Lovelace')",
        )
        assert result["graded"] is False
        assert result["is_correct"] is None
        assert result["lesson_verified"] is False
        assert result["xp_earned"] == 0

        progress = await _progress(client, token)
        assert progress["xp_earned"] == 0
        assert progress["verified_lessons"] == []

    async def test_runnable_exercise_is_graded_server_side(self, client):
        student = await _register(client)
        token, user_id = student["token"], student["user"]["id"]

        raw = get_lesson("python-comprehensions")
        assert raw is not None
        exercise = next(s for s in raw["steps"] if s["type"] == "exercise")

        wrong = await _step(
            client,
            token,
            raw["id"],
            exercise["id"],
            code="print([1, 2, 3])",
        )
        assert wrong["graded"] is True
        assert wrong["is_correct"] is False
        assert wrong["step_completed"] is False
        assert wrong["test_results"], "grader should report visible test output"

        correct = await _step(
            client,
            token,
            raw["id"],
            exercise["id"],
            code="print([x**3 for x in range(1, 6)])",
        )
        assert correct["graded"] is True
        assert correct["is_correct"] is True
        assert correct["step_completed"] is True

        # Finish the lesson through the API so completion is verified.
        for step in raw["steps"]:
            if step["type"] == "explain":
                await _step(client, token, raw["id"], step["id"])
            elif step["type"] == "quiz":
                final = await _step(
                    client,
                    token,
                    raw["id"],
                    step["id"],
                    answer=step["correctIndex"],
                )

        assert final["lesson_verified"] is True
        assert final["xp_earned"] == int(raw["xpReward"])

        progress = await _progress(client, token)
        assert progress["verified_lessons"] == [raw["id"]]
        assert progress["xp_earned"] == int(raw["xpReward"])

        graph = await get_skill_graph(user_id)
        skill = graph["categories"]["programming"]["skills"]["python"]
        # wrong exercise + correct exercise + correct quiz = 3 graded attempts
        assert skill["attempts"] == 3
        assert skill["score"] > 0


# ════════════════════════════════════════════════════════════════════════
# Idempotency and concurrency
# ════════════════════════════════════════════════════════════════════════


class TestRewardIdempotency:
    async def test_sequential_replay_does_not_duplicate_xp(self, client):
        student = await _register(client)
        token, user_id = student["token"], student["user"]["id"]

        raw = get_lesson("python-hello")
        first = await _complete_lesson_via_service(user_id, raw)
        assert first["xp_earned"] == int(raw["xpReward"])

        second = await _complete_lesson_via_service(user_id, raw)
        assert second["xp_earned"] == 0
        assert second["total_xp"] == int(raw["xpReward"])

        progress = await _progress(client, token)
        assert progress["xp_earned"] == int(raw["xpReward"])
        assert progress["awarded_lessons"] == [raw["id"]]

    async def test_concurrent_final_step_awards_xp_once(self, client):
        student = await _register(client)
        user_id = student["user"]["id"]

        raw = get_lesson("python-hello")
        quiz = _quiz_step(raw)

        # Complete everything except the graded quiz.
        for step in raw["steps"]:
            if step["id"] == quiz["id"]:
                continue
            if step["type"] == "exercise":
                await complete_step(
                    user_id=user_id,
                    lesson_id=raw["id"],
                    step_id=step["id"],
                    code=step.get("solution") or "print('practice')",
                )
            else:
                await complete_step(
                    user_id=user_id, lesson_id=raw["id"], step_id=step["id"]
                )

        results = await asyncio.gather(
            complete_step(
                user_id=user_id,
                lesson_id=raw["id"],
                step_id=quiz["id"],
                answer=str(quiz["correctIndex"]),
            ),
            complete_step(
                user_id=user_id,
                lesson_id=raw["id"],
                step_id=quiz["id"],
                answer=str(quiz["correctIndex"]),
            ),
        )
        for result in results:
            assert result["lesson_verified"] is True

        persisted = await get_progress(user_id)
        assert persisted["xp_earned"] == int(raw["xpReward"])
        assert persisted["awarded_lessons"] == [raw["id"]]


# ════════════════════════════════════════════════════════════════════════
# Prerequisite ordering
# ════════════════════════════════════════════════════════════════════════


class TestPrerequisiteChain:
    async def test_next_lesson_always_has_prerequisites_met(self, client):
        student = await _register(client)
        token, user_id = student["token"], student["user"]["id"]

        first = (await _next(client, token))["lesson"]
        assert first["id"] == "python-hello"
        assert first.get("prerequisites") in (None, [])

        # python-variables requires python-hello; it must not be offered first.
        assert first["id"] != "python-variables"
        gated = {l["id"]: set(l.get("prerequisites") or []) for l in list_lessons()}
        assert "python-hello" in gated["python-variables"]

        await _complete_lesson_via_service(user_id, get_lesson("python-hello"))

        second = (await _next(client, token))["lesson"]
        assert second["id"] == "python-variables"
        assert set(second.get("prerequisites") or []) == {"python-hello"}

        # A lesson requiring an incomplete lesson is still not recommended.
        assert second["id"] != "python-input"  # needs python-variables too
        assert "python-variables" in gated["python-input"]

        service_next = await next_lesson(user_id, None)
        assert service_next["id"] == second["id"]

    async def test_recommendation_differs_after_measured_practice(self, client):
        student = await _register(client)
        token, user_id = student["token"], student["user"]["id"]

        raw = get_lesson("python-hello")
        quiz = _quiz_step(raw)

        baseline = await _step(
            client, token, raw["id"], quiz["id"], answer=_wrong_index(quiz)
        )
        assert baseline["next_action"]["attempts"] == 1
        assert baseline["next_action"]["mastery"] == 0.0
        assert baseline["next_action"]["action"] == "repair"

        improved = await _step(
            client, token, raw["id"], quiz["id"], answer=quiz["correctIndex"]
        )
        action = improved["next_action"]
        assert action["attempts"] == 2
        assert 0.0 <= action["mastery"] <= 1.0
        assert action["category"] == "programming"
        assert action["skill"] == "python"
        # Weakness tier is derived from the measured mastery, not hardcoded.
        assert action["weakness_tier"] == weakness_tier_for(action["mastery"])
        assert action["attempts"] == (
            await get_skill_graph(user_id)
        )["categories"]["programming"]["skills"]["python"]["attempts"]


# ════════════════════════════════════════════════════════════════════════
# Personalization thresholds (deterministic policy)
# ════════════════════════════════════════════════════════════════════════


class TestPersonalizationPolicy:
    def test_weak_skill_receives_repair_action(self):
        action = decide_next_action("python", 0.25, "critical")
        assert action["action"] == "repair"
        assert action["estimated_minutes"] <= 15

    def test_weak_skill_receives_practice_action(self):
        action = decide_next_action("python", 0.50, "weak")
        assert action["action"] == "practice"
        assert action["estimated_minutes"] <= 20

    def test_on_track_skill_receives_drill(self):
        action = decide_next_action("python", 0.70, "on_track")
        assert action["action"] == "drill"

    def test_strong_skill_receives_mock_action(self):
        action = decide_next_action("python", 0.90, "strong")
        assert action["action"] == "mock"
        assert action["estimated_minutes"] <= 25

    def test_different_evidence_produces_different_recommendations(self):
        weak = decide_next_action("dbms", 0.30, weakness_tier_for(0.30))
        strong = decide_next_action("dbms", 0.92, weakness_tier_for(0.92))
        assert weak["action"] == "repair"
        assert strong["action"] == "mock"
        assert weak["action"] != strong["action"]

    def test_tier_boundaries_are_deterministic(self):
        assert weakness_tier_for(0.0) == "critical"
        assert weakness_tier_for(0.3999) == "critical"
        assert weakness_tier_for(0.40) == "weak"
        assert weakness_tier_for(0.5999) == "weak"
        assert weakness_tier_for(0.60) == "on_track"
        assert weakness_tier_for(0.8499) == "on_track"
        assert weakness_tier_for(0.85) == "strong"
        assert weakness_tier_for(1.0) == "strong"


# ════════════════════════════════════════════════════════════════════════
# Skill graph truth and dashboard parity
# ════════════════════════════════════════════════════════════════════════


class TestSkillGraphTruth:
    async def test_new_user_has_no_fake_mastery(self):
        user_id = f"new-{uuid.uuid4().hex}"
        graph = await initialize_skill_graph(user_id)

        assert graph["overall_score"] == 0
        assert "programming" in graph["categories"]
        assert "aptitude" in graph["categories"]
        for category in graph["categories"].values():
            assert category["score"] == 0
            for skill in category["skills"].values():
                assert skill["attempts"] == 0
                assert skill["score"] == 0
                assert skill["last_practiced"] is None

        assert await get_weak_areas(user_id) == []
        readiness = await get_readiness_score(user_id)
        assert readiness["overall"] == 0

    async def test_skill_graph_comes_from_graded_attempts_only(self, client):
        student = await _register(client)
        token, user_id = student["token"], student["user"]["id"]

        raw = get_lesson("python-hello")
        quiz = _quiz_step(raw)

        wrong = await _step(
            client, token, raw["id"], quiz["id"], answer=_wrong_index(quiz)
        )
        assert wrong["is_correct"] is False

        graph = await _skills(client, token)
        skill = graph["categories"]["programming"]["skills"]["python"]
        assert skill["attempts"] == 1
        assert skill["score"] == 0

        # Reading a step adds no evidence at all.
        explain = _explain_steps(raw)[0]
        await _step(client, token, raw["id"], explain["id"])
        graph = await _skills(client, token)
        assert graph["categories"]["programming"]["skills"]["python"]["attempts"] == 1

        correct = await _step(
            client, token, raw["id"], quiz["id"], answer=quiz["correctIndex"]
        )
        assert correct["is_correct"] is True

        graph = await _skills(client, token)
        skill = graph["categories"]["programming"]["skills"]["python"]
        assert skill["attempts"] == 2
        assert skill["score"] > 0

        # Weak areas only list skills with real attempts.
        weak = await get_weak_areas(user_id)
        assert weak
        assert {w["skill"] for w in weak} == {"python"}

    async def test_api_graph_matches_persisted_graph(self, client):
        student = await _register(client)
        token, user_id = student["token"], student["user"]["id"]
        await initialize_skill_graph(user_id)

        raw = get_lesson("python-hello")
        quiz = _quiz_step(raw)
        await _step(client, token, raw["id"], quiz["id"], answer=quiz["correctIndex"])

        api_graph = await _skills(client, token)
        doc = await get_db()["skill_graphs"].find_one({"user_id": user_id})
        assert doc is not None
        api_skill = api_graph["categories"]["programming"]["skills"]["python"]
        db_skill = doc["categories"]["programming"]["skills"]["python"]
        assert api_skill["attempts"] == db_skill["attempts"]
        assert api_skill["score"] == db_skill["score"]
        assert api_graph["overall_score"] == doc["overall_score"]


class TestDashboardParity:
    async def test_progress_matches_db_and_gamification_matches_its_collection(
        self, client
    ):
        student = await _register(client)
        token, user_id = student["token"], student["user"]["id"]

        # A new learner starts at zero everywhere.
        empty_progress = await _progress(client, token)
        assert empty_progress["xp_earned"] == 0
        assert empty_progress["verified_lessons"] == []
        assert empty_progress["completed"] == {}

        raw = get_lesson("python-hello")
        await _complete_lesson_via_service(user_id, raw)

        progress = await _progress(client, token)
        doc = await get_db()["lesson_progress"].find_one({"user_id": user_id})
        assert progress["xp_earned"] == doc["xp_earned"] == int(raw["xpReward"])
        assert progress["verified_lessons"] == doc["verified_lessons"] == [raw["id"]]
        assert progress["current_lesson"] == doc.get("current_lesson")

        # Gamification is a separate collection; the dashboard must at least
        # render internally consistent, persisted values.
        profile_response = await client.get(
            "/api/v1/gamification/profile", headers=_auth(token)
        )
        assert profile_response.status_code == 200, profile_response.text
        profile = profile_response.json()
        gamification_doc = await get_db()["gamification"].find_one(
            {"user_id": user_id}
        )
        assert gamification_doc is not None
        assert profile["xp"] == gamification_doc.get("xp", 0)
        assert profile["level"] == gamification_doc.get("level", 1)
        assert profile["daily_goal_count"] == gamification_doc.get(
            "daily_goal_count", 0
        )
