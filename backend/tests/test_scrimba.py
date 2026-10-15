"""Tests for scrimba content.

Scrimba lessons are served through the unified catalog
(``app.services.unified_catalog``); there is no dedicated ``/api/v1/scrimba``
route, so these tests cover the content source only.
"""
from __future__ import annotations

from app.content.scrimba_lessons import (
    LANGUAGES,
    LESSONS,
    LESSON_INDEX,
    get_scrimba_lesson,
    all_scrimba_lessons,
)


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
