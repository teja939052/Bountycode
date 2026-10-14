"""Tests for scrimba content, routes, and gamification wiring."""
from __future__ import annotations

import pytest
from unittest.mock import patch, AsyncMock

from app.content.scrimba_lessons import (
    LANGUAGES,
    LESSONS,
    LESSON_INDEX,
    get_scrimba_lesson,
    all_scrimba_lessons,
)
from app.services.gamification_core import ACTIVITY_COUNTER_FIELD
from app.services.journey_engine import PRIORITY_WEIGHTS
from app.database import gamification_collection


class TestScrimbaContent:
    """Tests for scrimba lesson generation."""

    def test_all_languages_have_lessons(self):
        assert len(LESSONS) == len(LANGUAGES)
        for lang in LANGUAGES:
            lesson = LESSON_INDEX.get(f"{lang['id']}-first-program")
            assert lesson is not None, f"Missing lesson for {lang['id']}"

    def test_lesson_ids_are_unique(self):
        ids = [lesson["lesson_id"] for lesson in LESSONS]
        assert len(ids) == len(set(ids))

    def test_lesson_slide_count(self):
        for lesson in LESSONS:
            slides = lesson.get("slides", [])
            assert len(slides) >= 30, f"{lesson['lesson_id']} has too few slides"

    def test_lesson_fields(self):
        for lesson in LESSONS:
            assert lesson["language_id"] == lesson["lesson_id"].split("-")[0]
            assert lesson["level_id"] == "scrimba"
            assert lesson["title"]
            assert lesson["description"]

    def test_get_scrimba_lesson(self):
        for lesson in LESSONS:
            found = get_scrimba_lesson(lesson["lesson_id"])
            assert found is not None
            assert found["lesson_id"] == lesson["lesson_id"]

    def test_get_scrimba_lesson_missing(self):
        assert get_scrimba_lesson("does-not-exist") is None

    def test_all_scrimba_lessons(self):
        lessons = all_scrimba_lessons()
        assert len(lessons) == len(LANGUAGES)

    def test_slide_structure(self):
        lesson = get_scrimba_lesson("python-first-program")
        for slide in lesson["slides"]:
            assert "title" in slide
            assert "content" in slide
            assert "language" in slide

    def test_snippets_present_for_all_keys(self):
        required_keys = [
            "welcome", "strings", "comments", "numbers", "variables",
            "naming", "reassign", "fstrings", "input", "int_cast",
            "boolean", "comparisons", "if", "else", "elif", "nested_if",
            "and_or", "not", "for_loop", "range", "while_loop", "break",
            "continue", "list", "list_methods", "dict", "tuple", "set",
            "function", "params", "return", "multiple_returns", "defaults",
            "lambda", "map", "filter", "try_except", "raise", "import",
            "from_import", "pip", "file_read", "file_write", "capstone",
        ]
        for lang in LANGUAGES:
            snippets = lang.get("snippets", {})
            for key in required_keys:
                assert key in snippets, f"Missing snippet {key} for {lang['id']}"
                assert snippets[key].strip(), f"Empty snippet {key} for {lang['id']}"


class TestScrimbaGamificationWiring:
    """Tests for scrimba gamification integration."""

    def test_scrimba_counter_field_registered(self):
        assert "scrimba" in ACTIVITY_COUNTER_FIELD
        assert ACTIVITY_COUNTER_FIELD["scrimba"] == "total_scrimba"

    def test_scrimba_priority_weight_registered(self):
        assert "scrimba_practice" in PRIORITY_WEIGHTS
        assert PRIORITY_WEIGHTS["scrimba_practice"] > 0


class TestScrimbaRoutes:
    """Tests for scrimba API routes."""

    @pytest.fixture
    async def auth_client(self):
        from httpx import AsyncClient, ASGITransport
        from app.main import app
        from app.database import users_collection

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            email = "scrimba_route_test@example.com"
            password = "SecurePass123!"
            await users_collection().delete_many({"email": email})
            reg = await client.post(
                "/api/v1/auth/register",
                json={"email": email, "name": "Scrimba Test", "password": password},
            )
            assert reg.status_code == 200
            login = await client.post(
                "/api/v1/auth/login",
                json={"email": email, "password": password},
            )
            assert login.status_code == 200
            token = login.json().get("token")
            client.headers["Authorization"] = f"Bearer {token}"
            yield client
            await users_collection().delete_many({"email": email})

    @pytest.mark.asyncio
    async def test_list_scrimba_lessons(self, auth_client):
        response = await auth_client.get("/api/v1/scrimba/lessons")
        assert response.status_code == 200
        data = response.json()
        assert "lessons" in data
        assert len(data["lessons"]) == len(LANGUAGES)

    @pytest.mark.asyncio
    async def test_get_scrimba_lesson_detail(self, auth_client):
        response = await auth_client.get("/api/v1/scrimba/lessons/python-first-program")
        assert response.status_code == 200
        data = response.json()
        assert data["lesson_id"] == "python-first-program"
        assert len(data["slides"]) > 0

    @pytest.mark.asyncio
    async def test_get_scrimba_lesson_not_found(self, auth_client):
        response = await auth_client.get("/api/v1/scrimba/lessons/does-not-exist")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_complete_scrimba_lesson(self, auth_client):
        test_user_id = "scrimba_route_test@example.com"
        await gamification_collection().delete_one({"user_id": test_user_id})

        response = await auth_client.post(
            "/api/v1/scrimba/complete",
            json={
                "lesson_id": "python-first-program",
                "score": 10.0,
                "finished": True,
                "time_spent_seconds": 120,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True
        assert data["lesson_id"] == "python-first-program"
        assert "xp_awarded" in data
        assert "coins_earned" in data
        assert "stars_earned" in data
        assert "new_level" in data
        assert "level_up" in data
        assert "new_badges" in data
        assert "reward" in data
        assert data["reward"]["combo"] >= 0
        assert data["reward"]["streak_multiplier"] >= 1.0

    @pytest.mark.asyncio
    async def test_complete_scrimba_lesson_not_found(self, auth_client):
        response = await auth_client.post(
            "/api/v1/scrimba/complete",
            json={"lesson_id": "does-not-exist", "score": 10.0, "finished": True},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_complete_scrimba_requires_auth(self):
        from httpx import AsyncClient, ASGITransport
        from app.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/v1/scrimba/complete",
                json={"lesson_id": "python-first-program", "score": 10.0, "finished": True},
            )
            assert response.status_code in (401, 403)


class TestScrimbaSRS:
    """Tests for scrimba spaced repetition integration."""

    @pytest.fixture
    async def auth_client(self):
        from httpx import AsyncClient, ASGITransport
        from app.main import app
        from app.database import users_collection

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            email = "scrimba_srs_test@example.com"
            password = "SecurePass123!"
            await users_collection().delete_many({"email": email})
            reg = await client.post(
                "/api/v1/auth/register",
                json={"email": email, "name": "Scrimba SRS Test", "password": password},
            )
            assert reg.status_code == 200
            login = await client.post(
                "/api/v1/auth/login",
                json={"email": email, "password": password},
            )
            assert login.status_code == 200
            token = login.json().get("token")
            client.headers["Authorization"] = f"Bearer {token}"
            yield client
            await users_collection().delete_many({"email": email})

    @pytest.mark.asyncio
    async def test_complete_creates_srs_card(self, auth_client):
        from app.database import srs_cards_collection, users_collection

        user_doc = await users_collection().find_one({"email": "scrimba_srs_test@example.com"})
        user_id = str(user_doc["_id"])

        await srs_cards_collection().delete_one({"user_id": user_id, "problem_id": "scrimba:python-first-program"})

        response = await auth_client.post(
            "/api/v1/scrimba/complete",
            json={
                "lesson_id": "python-first-program",
                "score": 10.0,
                "finished": True,
                "time_spent_seconds": 120,
            },
        )
        assert response.status_code == 200

        card = await srs_cards_collection().find_one({
            "user_id": user_id,
            "problem_id": "scrimba:python-first-program",
        })
        assert card is not None
        assert card.get("difficulty") in ("easy", "medium", "hard")
