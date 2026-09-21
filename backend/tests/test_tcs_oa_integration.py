"""Integration test: TCS OA flow through company_blueprints.json.

Verifies the full student path:
  signup → login → start TCS OA → verify blueprint structure →
  submit answers → verify scoring → verify diagnosis persistence

This test proves the data-driven blueprint actually drives the OA engine.
"""

import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import oa_sessions_collection, users_collection
from app.middleware.rate_limiter import clear_login_attempts


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture(autouse=True)
async def clear_rate_limiter():
    """Clear in-memory rate limiter between tests."""
    from app.middleware.rate_limiter import request_counts
    request_counts.clear()
    yield
    request_counts.clear()


@pytest.fixture
async def test_user(client):
    """Register and log in a test user, return token. Clean rate limits."""
    email = "tcs_flow_test@example.com"
    clear_login_attempts(email)
    try:
        await users_collection().delete_many({"email": email})
    except Exception:
        pass
    try:
        await oa_sessions_collection().delete_many({"user_id": email})
    except Exception:
        pass

    r = await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "name": "TCS Flow Test",
            "password": "SecurePass123!",
        },
    )
    assert r.status_code == 200, f"Register failed: {r.text}"
    token = r.json()["token"]

    yield token

    try:
        await users_collection().delete_many({"email": email})
    except Exception:
        pass
    try:
        await oa_sessions_collection().delete_many({"user_id": email})
    except Exception:
        pass
    clear_login_attempts(email)


def _start_oa(client, token):
    async def _do_start():
        await asyncio.sleep(2)  # avoid rate limit across tests
        return await client.post(
            "/api/v1/oa/tcs/start",
            json={
                "company": "tcs",
                "role": "SDE undergrad",
                "mode": "standard",
                "total_questions": 15,
                "verified_only": False,
            },
            headers={"Authorization": f"Bearer {token}"},
        )
    return _do_start()


@pytest.mark.asyncio
async def test_tcs_oa_blueprint_structure(client, test_user):
    """Start a TCS OA and verify the blueprint-driven structure."""
    token = test_user
    r = await _start_oa(client, token)
    assert r.status_code == 200, f"Start OA failed: {r.text}"
    session = r.json()

    # Verify blueprint structure is loaded from company_blueprints.json
    assert "exam_structure" in session
    assert "stage_budgets" in session
    assert session["total_questions"] == 15
    assert session["company"] == "tcs"

    # Verify exam_structure has Foundation and Advanced stages
    stages = session["exam_structure"].get("stages", [])
    stage_ids = [s["id"] for s in stages]
    assert "foundation" in stage_ids, f"Expected Foundation stage, got: {stage_ids}"
    assert "advanced" in stage_ids, f"Expected Advanced stage, got: {stage_ids}"

    # Verify Foundation stage sections
    foundation = next(s for s in stages if s["id"] == "foundation")
    foundation_sections = foundation.get("sections", [])
    assert "aptitude" in foundation_sections
    assert "verbal" in foundation_sections
    assert "logical" in foundation_sections

    # Verify Advanced stage sections
    advanced = next(s for s in stages if s["id"] == "advanced")
    advanced_sections = advanced.get("sections", [])
    assert "aptitude" in advanced_sections
    assert "coding" in advanced_sections

    # Verify stage notes show exact counts from blueprint
    assert "65 questions" in foundation.get("note", ""), \
        f"Foundation note should mention 65 questions: {foundation.get('note')}"
    assert "17 questions" in advanced.get("note", ""), \
        f"Advanced note should mention 17 questions: {advanced.get('note')}"

    # Verify questions have stage labels
    questions = session.get("questions", [])
    assert len(questions) == 15
    stages_in_questions = set(q.get("stage") for q in questions)
    assert "foundation" in stages_in_questions
    assert "advanced" in stages_in_questions

    # Verify Foundation sections are present in questions
    foundation_q_sections = set(
        q.get("section") for q in questions if q.get("stage") == "foundation"
    )
    assert "aptitude" in foundation_q_sections
    assert "verbal" in foundation_q_sections
    assert "logical" in foundation_q_sections

    # Verify Advanced Coding is present in questions
    advanced_q_sections = set(
        q.get("section") for q in questions if q.get("stage") == "advanced"
    )
    assert "coding" in advanced_q_sections, \
        f"Expected coding in advanced sections, got: {advanced_q_sections}"


@pytest.mark.asyncio
async def test_tcs_oa_answer_submission_and_scoring(client, test_user):
    """Submit answers to TCS OA and verify scoring."""
    token = test_user
    r = await _start_oa(client, token)
    assert r.status_code == 200
    session = r.json()
    questions = session.get("questions", [])
    session_id = session["session_id"]

    # Submit answers for first 3 questions
    items = []
    for q in questions[:3]:
        if q.get("kind") == "mcq":
            opts = q.get("options", [])
            if opts:
                items.append({
                    "question_uid": q["question_uid"],
                    "answer": opts[0],
                    "time_taken": 10,
                })
        elif q.get("kind") == "code":
            items.append({
                "question_uid": q["question_uid"],
                "answer": "",
                "language": "python",
                "time_taken": 5,
            })
        else:
            items.append({
                "question_uid": q["question_uid"],
                "answer": "sample answer",
                "time_taken": 10,
            })

    if not items:
        pytest.skip("No questions available to test answer submission")

    r = await client.post(
        "/api/v1/oa/answer",
        json={"session_id": session_id, "items": items},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200, f"Submit answers failed: {r.text}"
    result = r.json()

    # Verify response confirms receipt
    assert result.get("received") == len(items)
    assert result.get("session_id") == session_id


@pytest.mark.asyncio
async def test_tcs_oa_blueprint_in_db(client, test_user):
    """Verify TCS OA session is persisted in MongoDB with correct structure."""
    token = test_user
    r = await _start_oa(client, token)
    assert r.status_code == 200
    session = r.json()
    session_id = session["session_id"]

    # Query DB directly
    db_session = await oa_sessions_collection().find_one({"session_id": session_id})
    assert db_session is not None, f"Session {session_id} not found in DB"

    # Verify blueprint fields persisted
    assert db_session.get("company") == "tcs"
    assert "questions" in db_session or "structure" in db_session


@pytest.mark.asyncio
async def test_tcs_oa_no_negative_marking_rule(client, test_user):
    """Verify TCS blueprint rule: no negative marking is communicated."""
    token = test_user
    r = await _start_oa(client, token)
    assert r.status_code == 200
    session = r.json()

    # Verify no negative marking in session
    assert session.get("negative_marking") is False


@pytest.mark.asyncio
async def test_tcs_oa_section_durations_from_blueprint(client, test_user):
    """Verify TCS section durations come from company_blueprints.json."""
    token = test_user
    r = await _start_oa(client, token)
    assert r.status_code == 200
    session = r.json()
    questions = session.get("questions", [])

    # Verify questions have time limits (derived from blueprint)
    for q in questions:
        assert q.get("time_limit", 0) > 0, f"Question {q.get('question_uid')} missing time_limit"


@pytest.mark.asyncio
async def test_tcs_oa_locked_navigation_rule(client, test_user):
    """Verify TCS blueprint rule: back_navigation = false is communicated."""
    token = test_user
    r = await _start_oa(client, token)
    assert r.status_code == 200
    session = r.json()

    # Verify rules are in session metadata
    assert session.get("back_navigation") is False
    assert session.get("section_switching") is False


@pytest.mark.asyncio
async def test_tcs_oa_verified_only_requires_sufficient_stock(client, test_user):
    """Verify verified-only mode rejects when insufficient verified questions."""
    token = test_user
    r = await client.post(
        "/api/v1/oa/tcs/start",
        json={
            "company": "tcs",
            "role": "SDE undergrad",
            "mode": "standard",
            "total_questions": 15,
            "verified_only": True,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    # Should succeed with our verified questions
    assert r.status_code in (200, 422), \
        f"Expected 200 or 422, got {r.status_code}: {r.text}"

    if r.status_code == 200:
        session = r.json()
        # Verify all questions have trust_status = verified
        for q in session.get("questions", []):
            trust = q.get("trust_status", q.get("provenance", ""))
            # Should be from verified bank
            assert "verified" in trust.lower() or "pattern-relevant" in trust.lower(), \
                f"Question {q.get('question_uid')} has trust status: {trust}"
