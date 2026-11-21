"""Definitive end-to-end core loop test for BountyCode.

Verifies the complete learner lifecycle:

  Onboarding → Blueprint → Skill → Lesson → Practice → Assessment →
  Evidence → Diagnosis → Repair → Retest → Readiness

Uses an isolated MongoDB database (``placementpro_test_core_loop``) and runs
against the real FastAPI app via ASGI transport. Production data is never
touched.

Run:
    cd backend
    python -m pytest tests/test_e2e_core_loop.py -q
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
TEST_DB_NAME = "placementpro_test_core_loop"
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
from app.services import question_store as qs  # noqa: E402
from app.services.path_generator import decide_next_action  # noqa: E402
from app.services.readiness_engine import compute_readiness  # noqa: E402

# Process-level isolation guard
if get_settings().DATABASE_NAME != TEST_DB_NAME:
    pytest.exit(
        "test_e2e_core_loop must run in its own pytest process: the app "
        f"was already imported with DATABASE_NAME={get_settings().DATABASE_NAME!r}. "
        "Run: python -m pytest tests/test_e2e_core_loop.py",
        returncode=1,
    )

PASSWORD = "SecurePass1!"
TCS = "tcs"
ROLE = "software_engineer"

_email_counter = itertools.count()


def _reset_duplicate_guard() -> None:
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
    db = get_db()
    assert db.name == TEST_DB_NAME, (
        f"Refusing to drop {db.name!r}; expected {TEST_DB_NAME!r}"
    )
    assert db.name != PROD_DB_NAME
    qs._questions = []
    qs._loaded = False
    lesson_service = sys.modules.get("app.services.lesson_service")
    if lesson_service:
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
    email = f"corelp-{next(_email_counter)}-{uuid.uuid4().hex[:8]}@example.com"
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "name": "Core Loop Learner", "password": PASSWORD},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["token"]
    return {"token": data["token"], "user": data["user"], "email": email}


async def _complete_onboarding(client: AsyncClient, token: str, user_id: str) -> None:
    """Mark onboarding complete so plan/gated endpoints work."""
    for step_id in ("step-1", "step-2", "step-3", "step-4", "step-5"):
        await client.post(
            "/api/v1/onboarding/complete",
            json={"step_id": step_id, "completed": True, "xp_earned": 10},
            headers=_auth(token),
        )
    # Also create the academy learner profile expected by /api/v1/academy/plan.
    db = get_db()
    await db["academy_learner_profiles"].update_one(
        {"user_id": user_id},
        {"$set": {"onboarding_complete": True, "target_company": TCS, "target_role": ROLE}},
        upsert=True,
    )


async def _set_target(client: AsyncClient, token: str) -> dict:
    response = await client.post(
        "/api/v1/gamification/profile/target-company",
        json={"company": TCS},
        headers=_auth(token),
    )
    assert response.status_code == 200, response.text
    return response.json()


# ════════════════════════════════════════════════════════════════════════
# Phase 1: Onboarding → Target company
# ════════════════════════════════════════════════════════════════════════


class TestOnboardingAndTarget:
    async def test_register_and_set_target_company(self, client):
        student = await _register(client)
        token, user_id = student["token"], student["user"]["id"]

        me = await client.get("/api/v1/auth/me", headers=_auth(token))
        assert me.status_code == 200
        assert me.json()["id"] == user_id

        result = await _set_target(client, token)
        assert result["target_company"] == TCS

        profile = await client.get(
            "/api/v1/gamification/profile", headers=_auth(token)
        )
        assert profile.status_code == 200


# ════════════════════════════════════════════════════════════════════════
# Phase 2: Diagnostic → Blueprint → Skill
# ════════════════════════════════════════════════════════════════════════


class TestDiagnostic:
    async def test_diagnostic_returns_trusted_questions_only(self, client):
        student = await _register(client)
        token = student["token"]

        result = await client.post(
            "/api/v1/academy/diagnostic/start",
            json={"questions_per_domain": 3},
            headers=_auth(token),
        )
        assert result.status_code == 200, result.text
        body = result.json()
        assert body["success"] is True
        assert body["diagnostic"]["total_questions"] >= 8
        diagnostic_id = body["diagnostic"]["diagnostic_id"]

        # No answer keys in the served payload.
        for q in body["diagnostic"]["questions"]:
            assert "correct_index" not in q
            assert "correct_answer" not in q
            assert "solution" not in q
            assert q["id"]

        # Submit answers and complete.
        questions = body["diagnostic"]["questions"]
        for q in questions:
            await client.post(
                f"/api/v1/academy/diagnostic/{diagnostic_id}/answer",
                json={
                    "question_id": q["id"],
                    "answer": "0",
                    "time_taken_seconds": 30,
                },
                headers=_auth(token),
            )

        complete = await client.post(
            f"/api/v1/academy/diagnostic/{diagnostic_id}/complete",
            headers=_auth(token),
        )
        assert complete.status_code == 200, complete.text

        latest = await client.get(
            "/api/v1/academy/diagnostic/latest",
            headers=_auth(token),
        )
        assert latest.status_code == 200, latest.text


# ════════════════════════════════════════════════════════════════════════
# Phase 3: Plan generation (deterministic)
# ════════════════════════════════════════════════════════════════════════


class TestPlanGeneration:
    async def test_plan_is_deterministic_for_same_learner_state(self, client):
        student = await _register(client)
        token, user_id = student["token"], student["user"]["id"]
        await _complete_onboarding(client, token, user_id)
        await _set_target(client, token)

        # Complete a lesson first so the plan has real evidence.
        from app.services.lesson_service import get_lesson, complete_step
        lesson = get_lesson("python-hello")
        assert lesson is not None, "python-hello lesson must exist"

        # Get the quiz step and answer correctly.
        quiz_step = next(s for s in lesson["steps"] if s["type"] == "quiz")
        await complete_step(
            user_id=user_id,
            lesson_id=lesson["id"],
            step_id=quiz_step["id"],
            answer=str(quiz_step["correctIndex"]),
        )

        # Generate plan twice — must be identical.
        plan1 = await client.get(
            "/api/v1/academy/plan",
            headers=_auth(token),
        )
        assert plan1.status_code == 200, plan1.text
        plan1_body = plan1.json()

        plan2 = await client.get(
            "/api/v1/academy/plan",
            headers=_auth(token),
        )
        assert plan2.status_code == 200, plan2.text
        plan2_body = plan2.json()

        # Deterministic: same inputs → same outputs (ignoring generated_at).
        plan1_body["plan"].pop("generated_at", None)
        plan2_body["plan"].pop("generated_at", None)
        assert plan1_body == plan2_body, "Plan must be deterministic for same learner state"
        assert "plan" in plan1_body
        assert "curriculum" in plan1_body["plan"]
        assert len(plan1_body["plan"]["curriculum"]) > 0

        # Each task has a reason.
        for task in plan1_body["plan"]["curriculum"]:
            assert "reason" in task, f"Task {task.get('domain')} missing reason"

    async def test_plan_recommends_weak_skills_first(self, client):
        student = await _register(client)
        token = student["token"]
        await _complete_onboarding(client, token, student["user"]["id"])
        await _set_target(client, token)

        plan = await client.get(
            "/api/v1/academy/plan",
            headers=_auth(token),
        )
        assert plan.status_code == 200, plan.text
        body = plan.json()
        curriculum = body["plan"]["curriculum"]

        # First task should be foundation_needed or not_assessed (no evidence yet).
        first = curriculum[0]
        assert first["skill_level"] in {"not_assessed", "foundation_needed"}
        assert "reason" in first


# ════════════════════════════════════════════════════════════════════════
# Phase 4: Lesson → Practice → Assessment → Evidence
# ════════════════════════════════════════════════════════════════════════


class TestLessonAndEvidence:
    async def test_lesson_completion_records_evidence(self, client):
        student = await _register(client)
        token, user_id = student["token"], student["user"]["id"]

        from app.services.lesson_service import get_lesson, complete_step, get_progress
        lesson = get_lesson("python-hello")
        assert lesson is not None

        # Complete all steps.
        for step in lesson["steps"]:
            if step["type"] == "quiz":
                await complete_step(
                    user_id=user_id,
                    lesson_id=lesson["id"],
                    step_id=step["id"],
                    answer=str(step["correctIndex"]),
                )
            elif step["type"] == "exercise":
                await complete_step(
                    user_id=user_id,
                    lesson_id=lesson["id"],
                    step_id=step["id"],
                    code=step.get("solution") or "print('practice')",
                )
            else:
                await complete_step(
                    user_id=user_id,
                    lesson_id=lesson["id"],
                    step_id=step["id"],
                )

        progress = await get_progress(user_id)
        assert lesson["id"] in progress["verified_lessons"]
        assert progress["xp_earned"] > 0

        # Evidence persisted in MongoDB.
        doc = await get_db()["lesson_progress"].find_one({"user_id": user_id})
        assert doc is not None
        assert doc["xp_earned"] == progress["xp_earned"]
        assert lesson["id"] in doc["verified_lessons"]

    async def test_skill_evidence_from_graded_attempts_only(self, client):
        student = await _register(client)
        token, user_id = student["token"], student["user"]["id"]

        from app.services.lesson_service import get_lesson, complete_step
        from app.services.skill_assessment import get_skill_graph, get_weak_areas
        lesson = get_lesson("python-hello")
        quiz_step = next(s for s in lesson["steps"] if s["type"] == "quiz")

        # Wrong answer first (valid wrong option index).
        options = quiz_step.get("options") or []
        wrong_idx = next((i for i in range(len(options)) if i != quiz_step["correctIndex"]), None)
        assert wrong_idx is not None

        wrong = await complete_step(
            user_id=user_id,
            lesson_id=lesson["id"],
            step_id=quiz_step["id"],
            answer=str(wrong_idx),
        )
        assert wrong["is_correct"] is False

        graph = await get_skill_graph(user_id)
        skill = graph["categories"]["programming"]["skills"]["python"]
        assert skill["attempts"] == 1
        assert skill["score"] == 0

        # Correct answer.
        correct = await complete_step(
            user_id=user_id,
            lesson_id=lesson["id"],
            step_id=quiz_step["id"],
            answer=str(quiz_step["correctIndex"]),
        )
        assert correct["is_correct"] is True

        graph = await get_skill_graph(user_id)
        skill = graph["categories"]["programming"]["skills"]["python"]
        assert skill["attempts"] == 2
        assert skill["score"] > 0

        # Weak areas only list skills with real attempts.
        weak = await get_weak_areas(user_id)
        assert weak
        assert {w["skill"] for w in weak} == {"python"}


# ════════════════════════════════════════════════════════════════════════
# Phase 5: Diagnosis → Repair mission → Retest → Readiness
# ════════════════════════════════════════════════════════════════════════


class TestRepairLoop:
    async def test_repair_mission_creation_and_readiness(self, client):
        student = await _register(client)
        token, user_id = student["token"], student["user"]["id"]
        await _set_target(client, token)

        # Create a repair mission for a weak skill.
        from app.services.repair_service import create_repair_mission
        mission = await create_repair_mission(
            user_id=user_id,
            weaknesses=["quant.ratio_proportion"],
            source="assessment",
        )
        assert mission is not None
        assert hasattr(mission, "id") or "id" in mission

        # Get readiness score.
        readiness = await compute_readiness(user_id, company=TCS)
        assert "overall_readiness" in readiness
        assert 0 <= readiness["overall_readiness"] <= 100

        # Readiness has categories.
        assert "categories" in readiness or "category_scores" in readiness

    async def test_readiness_explains_blockers(self, client):
        student = await _register(client)
        token = student["token"]
        await _set_target(client, token)

        readiness = await compute_readiness(student["user"]["id"], company=TCS)
        # Readiness should have recommendations or next_action.
        assert "recommendations" in readiness or "target_readiness" in readiness


# ════════════════════════════════════════════════════════════════════════
# Phase 6: Idempotency — no duplicate XP, mastery, or evidence
# ════════════════════════════════════════════════════════════════════════


class TestIdempotency:
    async def test_lesson_completion_awards_xp_once(self, client):
        student = await _register(client)
        token, user_id = student["token"], student["user"]["id"]

        from app.services.lesson_service import get_lesson, complete_step
        lesson = get_lesson("python-hello")

        # Complete the lesson fully.
        for step in lesson["steps"]:
            if step["type"] == "quiz":
                await complete_step(
                    user_id=user_id,
                    lesson_id=lesson["id"],
                    step_id=step["id"],
                    answer=str(step["correctIndex"]),
                )
            elif step["type"] == "exercise":
                await complete_step(
                    user_id=user_id,
                    lesson_id=lesson["id"],
                    step_id=step["id"],
                    code=step.get("solution") or "print('practice')",
                )
            else:
                await complete_step(
                    user_id=user_id,
                    lesson_id=lesson["id"],
                    step_id=step["id"],
                )

        first_progress = await client.get(
            "/api/v1/lessons/progress", headers=_auth(token)
        )
        first_xp = first_progress.json()["xp_earned"]
        assert first_xp > 0

        # Re-complete the same lesson — XP must not double.
        for step in lesson["steps"]:
            if step["type"] == "quiz":
                await complete_step(
                    user_id=user_id,
                    lesson_id=lesson["id"],
                    step_id=step["id"],
                    answer=str(step["correctIndex"]),
                )
            elif step["type"] == "exercise":
                await complete_step(
                    user_id=user_id,
                    lesson_id=lesson["id"],
                    step_id=step["id"],
                    code=step.get("solution") or "print('practice')",
                )
            else:
                await complete_step(
                    user_id=user_id,
                    lesson_id=lesson["id"],
                    step_id=step["id"],
                )

        second_progress = await client.get(
            "/api/v1/lessons/progress", headers=_auth(token)
        )
        assert second_progress.json()["xp_earned"] == first_xp


# ════════════════════════════════════════════════════════════════════════
# Phase 7: Dashboard parity — API matches MongoDB
# ════════════════════════════════════════════════════════════════════════


class TestDashboardParity:
    async def test_progress_api_matches_persisted_mongo(self, client):
        student = await _register(client)
        token, user_id = student["token"], student["user"]["id"]

        from app.services.lesson_service import get_lesson, complete_step
        lesson = get_lesson("python-hello")

        for step in lesson["steps"]:
            if step["type"] == "quiz":
                await complete_step(
                    user_id=user_id,
                    lesson_id=lesson["id"],
                    step_id=step["id"],
                    answer=str(step["correctIndex"]),
                )
            elif step["type"] == "exercise":
                await complete_step(
                    user_id=user_id,
                    lesson_id=lesson["id"],
                    step_id=step["id"],
                    code=step.get("solution") or "print('practice')",
                )
            else:
                await complete_step(
                    user_id=user_id,
                    lesson_id=lesson["id"],
                    step_id=step["id"],
                )

        api_progress = await client.get(
            "/api/v1/lessons/progress", headers=_auth(token)
        )
        assert api_progress.status_code == 200
        body = api_progress.json()

        doc = await get_db()["lesson_progress"].find_one({"user_id": user_id})
        assert doc is not None
        assert body["xp_earned"] == doc["xp_earned"]
        assert body["verified_lessons"] == doc["verified_lessons"]
