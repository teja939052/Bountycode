"""Tests for scrimba content verification."""
from __future__ import annotations

import pytest

from app.content.scrimba_lessons import LANGUAGES, LESSONS
from app.services.scrimba_verification import verify_scrimba_lessons, ScrimbaVerifier


class TestScrimbaVerification:
    """Tests for automated content verification."""

    def test_all_lessons_pass_automated_checks(self):
        report = verify_scrimba_lessons()
        assert report["total_lessons"] == len(LESSONS)
        assert report["passed_all_checks"] == len(LESSONS)
        assert report["failed"] == 0
        assert report["automated_checked"] == len(LESSONS)

    def test_each_lesson_has_all_checks_passing(self):
        verifier = ScrimbaVerifier()
        report = verifier.verify_all()
        for detail in report["details"]:
            assert detail["all_passed"] is True
            assert detail["recommendation"] == "AUTOMATED_CHECKED"

    def test_all_languages_verified(self):
        verified_ids = {d["language_id"] for d in verify_scrimba_lessons()["details"]}
        expected_ids = {lang["id"] for lang in LANGUAGES}
        assert verified_ids == expected_ids

    def test_lesson_fields_check(self):
        verifier = ScrimbaVerifier()
        for lesson in LESSONS:
            result = verifier._verify_lesson(lesson)
            assert result["checks"]["lesson_fields"]["pass"] is True

    def test_slide_count_check(self):
        verifier = ScrimbaVerifier()
        for lesson in LESSONS:
            result = verifier._verify_lesson(lesson)
            assert result["checks"]["slide_count"]["pass"] is True

    def test_snippets_present_check(self):
        verifier = ScrimbaVerifier()
        for lesson in LESSONS:
            result = verifier._verify_lesson(lesson)
            assert result["checks"]["snippets_present"]["pass"] is True

    def test_syntax_valid_check(self):
        verifier = ScrimbaVerifier()
        for lesson in LESSONS:
            result = verifier._verify_lesson(lesson)
            assert result["checks"]["syntax_valid"]["pass"] is True
