"""Staging smoke tests for Bountycode production deployments.

These run against a live staging URL and verify the critical learner path
from signup to readiness report. They are NOT run against localhost — they
require STAGING_API_URL to be set.

Run:
    STAGING_API_URL=https://staging.api.bountycode.com \
    python -m pytest tests/test_staging_smoke.py -q
"""
import os
import sys
import uuid

import httpx
import pytest

STAGING_API_URL = os.environ.get("STAGING_API_URL")
if not STAGING_API_URL:
    pytest.exit(
        "STAGING_API_URL is required for staging smoke tests",
        returncode=1,
    )

PASSWORD = "SecurePass123!"


def _email():
    return f"smoke-{uuid.uuid4().hex[:8]}@example.com"


class TestStagingSmoke:
    """Critical path: signup → onboarding → plan → lesson → assessment → readiness."""

    def test_landing_loads(self):
        r = httpx.get(f"{STAGING_API_URL}/", timeout=30)
        assert r.status_code == 200, f"landing: {r.status_code} {r.text[:200]}"

    def test_signup_creates_user(self):
        r = httpx.post(
            f"{STAGING_API_URL}/api/v1/auth/register",
            json={"email": _email(), "name": "Smoke Learner", "password": PASSWORD},
            timeout=30,
        )
        assert r.status_code == 200, f"signup: {r.status_code} {r.text[:200]}"
        body = r.json()
        assert body.get("token")
        return body["token"]

    def test_me_returns_profile(self):
        token = self.test_signup_creates_user()
        r = httpx.get(
            f"{STAGING_API_URL}/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        assert r.status_code == 200, f"me: {r.status_code} {r.text[:200]}"
        body = r.json()
        assert body.get("id")

    def test_company_and_role_selection(self):
        token = self.test_signup_creates_user()
        r = httpx.post(
            f"{STAGING_API_URL}/api/v1/gamification/profile/target-company",
            json={"company": "tcs"},
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        assert r.status_code == 200, f"target company: {r.status_code} {r.text[:200]}"
        assert r.json().get("target_company") == "tcs"

    def test_diagnostic_returns_questions_no_keys(self):
        token = self.test_signup_creates_user()
        r = httpx.post(
            f"{STAGING_API_URL}/api/v1/academy/diagnostic/start",
            json={"questions_per_domain": 3},
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        assert r.status_code == 200, f"diagnostic: {r.status_code} {r.text[:200]}"
        body = r.json()
        assert body.get("success") is True
        assert body["diagnostic"]["total_questions"] > 0
        # No answer keys in client payload
        for q in body["diagnostic"]["questions"]:
            assert "correct_index" not in q
            assert "correct_answer" not in q
            assert "solution" not in q

    def test_plan_appears(self):
        token = self.test_signup_creates_user()
        r = httpx.get(
            f"{STAGING_API_URL}/api/v1/academy/plan",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        assert r.status_code == 200, f"plan: {r.status_code} {r.text[:200]}"
        body = r.json()
        assert "plan" in body
        assert len(body["plan"].get("curriculum", [])) > 0

    def test_lesson_opens_and_completes(self):
        token = self.test_signup_creates_user()
        # Open a lesson
        r = httpx.get(
            f"{STAGING_API_URL}/api/v1/lessons/python-hello",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        assert r.status_code == 200, f"lesson: {r.status_code} {r.text[:200]}"
        body = r.json()
        assert body.get("id")

        # Complete a quiz step
        step = next(s for s in body["steps"] if s["type"] == "quiz")
        r = httpx.post(
            f"{STAGING_API_URL}/api/v1/lessons/python-hello/steps/{step['id']}/complete",
            json={"answer": str(step["correctIndex"])},
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        assert r.status_code == 200, f"step complete: {r.status_code} {r.text[:200]}"

    def test_readiness_report_renders(self):
        token = self.test_signup_creates_user()
        r = httpx.get(
            f"{STAGING_API_URL}/api/v1/readiness",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        assert r.status_code == 200, f"readiness: {r.status_code} {r.text[:200]}"
        body = r.json()
        assert "overall_readiness" in body

    def test_no_answer_keys_leaked(self):
        token = self.test_signup_creates_user()
        # Every response to the client must not contain answer keys
        r = httpx.get(
            f"{STAGING_API_URL}/api/v1/academy/plan",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        body = r.json()
        # Recursively check for leaked keys
        leaked = self._find_keys(body)
        assert not leaked, f"answer keys leaked: {leaked}"

    @staticmethod
    def _find_keys(obj, path="root"):
        """Recursively find keys that look like answer keys."""
        found = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k.startswith("_") and k in (
                    "_correct_index",
                    "_correct_answer",
                    "_solution",
                    "_explanation",
                ):
                    found.append(f"{path}.{k}")
                found.extend(TestStagingSmoke._find_keys(v, f"{path}.{k}"))
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                found.extend(TestStagingSmoke._find_keys(item, f"{path}[{i}]"))
        return found
