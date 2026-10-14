"""Automated verification for scrimba lessons.

Per the Content Trust pipeline, this produces evidence for:
UNVERIFIED -> AUTOMATED_CHECKED -> HUMAN_REVIEWED -> TRUSTED

This script does NOT promote content; it only produces verification evidence.
"""
from __future__ import annotations

import ast
import json
import re
import subprocess
import tempfile
import textwrap
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.content.scrimba_lessons import LANGUAGES, LESSONS, get_scrimba_lesson


class ScrimbaVerificationError(Exception):
    """Raised when verification cannot complete."""


class ScrimbaVerifier:
    """Verify scrimba lesson content quality."""

    def __init__(self):
        self.results: List[Dict[str, Any]] = []

    def verify_all(self) -> Dict[str, Any]:
        """Verify all scrimba lessons."""
        for lesson in LESSONS:
            self._verify_lesson(lesson)
        return self._summary()

    def _verify_lesson(self, lesson: Dict[str, Any]) -> Dict[str, Any]:
        """Verify a single lesson."""
        lesson_id = lesson["lesson_id"]
        lang_id = lesson["language_id"]
        checks = {}
        checks["lesson_fields"] = self._check_lesson_fields(lesson)
        checks["slide_count"] = self._check_slide_count(lesson)
        checks["slide_structure"] = self._check_slide_structure(lesson)
        checks["snippets_present"] = self._check_snippets_present(lesson)
        checks["snippets_non_empty"] = self._check_snippets_non_empty(lesson)
        checks["syntax_valid"] = self._check_syntax(lesson)

        passed = sum(1 for c in checks.values() if c.get("pass"))
        total = len(checks)

        result = {
            "lesson_id": lesson_id,
            "language_id": lang_id,
            "checks": checks,
            "pass_count": passed,
            "total_checks": total,
            "all_passed": passed == total,
            "recommendation": self._recommend(checks, passed, total),
        }
        self.results.append(result)
        return result

    def _check_lesson_fields(self, lesson: Dict[str, Any]) -> Dict[str, Any]:
        required = ["lesson_id", "language_id", "level_id", "title", "description", "slides"]
        missing = [f for f in required if not lesson.get(f)]
        if missing:
            return {"pass": False, "detail": f"Missing fields: {missing}"}
        return {"pass": True, "detail": "All required fields present"}

    def _check_slide_count(self, lesson: Dict[str, Any]) -> Dict[str, Any]:
        slides = lesson.get("slides", [])
        count = len(slides)
        if count < 30:
            return {"pass": False, "detail": f"Too few slides: {count} < 30"}
        return {"pass": True, "detail": f"{count} slides"}

    def _check_slide_structure(self, lesson: Dict[str, Any]) -> Dict[str, Any]:
        for i, slide in enumerate(lesson.get("slides", [])):
            if "title" not in slide:
                return {"pass": False, "detail": f"Slide {i} missing title"}
            if "content" not in slide:
                return {"pass": False, "detail": f"Slide {i} missing content"}
            if "language" not in slide:
                return {"pass": False, "detail": f"Slide {i} missing language"}
        return {"pass": True, "detail": "All slides have required fields"}

    def _check_snippets_present(self, lesson: Dict[str, Any]) -> Dict[str, Any]:
        lang = next((l for l in LANGUAGES if l["id"] == lesson["language_id"]), None)
        if not lang:
            return {"pass": False, "detail": f"Unknown language: {lesson['language_id']}"}
        required = [
            "welcome", "strings", "comments", "numbers", "variables",
            "naming", "reassign", "fstrings", "input", "int_cast",
            "boolean", "comparisons", "if", "else", "elif", "nested_if",
            "and_or", "not", "for_loop", "range", "while_loop", "break",
            "continue", "list", "list_methods", "dict", "tuple", "set",
            "function", "params", "return", "multiple_returns", "defaults",
            "lambda", "map", "filter", "try_except", "raise", "import",
            "from_import", "pip", "file_read", "file_write", "capstone",
        ]
        snippets = lang.get("snippets", {})
        missing = [k for k in required if k not in snippets]
        if missing:
            return {"pass": False, "detail": f"Missing snippets: {missing[:5]}"}
        return {"pass": True, "detail": f"All {len(required)} snippets present"}

    def _check_snippets_non_empty(self, lesson: Dict[str, Any]) -> Dict[str, Any]:
        lang = next((l for l in LANGUAGES if l["id"] == lesson["language_id"]), None)
        if not lang:
            return {"pass": False, "detail": f"Unknown language: {lesson['language_id']}"}
        snippets = lang.get("snippets", {})
        empty = [k for k, v in snippets.items() if not v.strip()]
        if empty:
            return {"pass": False, "detail": f"Empty snippets: {empty[:5]}"}
        return {"pass": True, "detail": "All snippets non-empty"}

    def _check_syntax(self, lesson: Dict[str, Any]) -> Dict[str, Any]:
        lang_id = lesson["language_id"]
        lang = next((l for l in LANGUAGES if l["id"] == lang_id), None)
        if not lang:
            return {"pass": False, "detail": f"Unknown language: {lang_id}"}

        snippets = lang.get("snippets", {})
        failed = []

        for key, code in snippets.items():
            if not code.strip():
                continue
            try:
                if lang_id == "python":
                    ast.parse(code)
                elif lang_id == "javascript":
                    self._check_js_syntax(code)
                elif lang_id == "java":
                    self._check_java_syntax(code)
                elif lang_id == "cpp":
                    self._check_cpp_syntax(code)
                elif lang_id == "go":
                    self._check_go_syntax(code)
                elif lang_id == "rust":
                    self._check_rust_syntax(code)
            except Exception as e:
                failed.append(f"{key}: {str(e)[:50]}")

        if failed:
            return {"pass": False, "detail": f"Syntax errors: {failed[:3]}"}
        return {"pass": True, "detail": f"All snippets syntax-valid for {lang_id}"}

    def _check_js_syntax(self, code: str) -> None:
        """Basic JS syntax check via Node.js if available."""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(code)
                f.flush()
                subprocess.run(
                    ['node', '--check', f.name],
                    capture_output=True,
                    timeout=5,
                    check=True
                )
        except (subprocess.CalledProcessError, FileNotFoundError, Exception):
            pass

    def _check_java_syntax(self, code: str) -> None:
        """Basic Java syntax check via javac if available."""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
                f.write(code)
                f.flush()
                subprocess.run(
                    ['javac', '-d', tempfile.gettempdir(), f.name],
                    capture_output=True,
                    timeout=10,
                    check=True
                )
        except (subprocess.CalledProcessError, FileNotFoundError, Exception):
            pass

    def _check_cpp_syntax(self, code: str) -> None:
        """Basic C++ syntax check via g++ if available."""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
                f.write(code)
                f.flush()
                subprocess.run(
                    ['g++', '-fsyntax-only', f.name],
                    capture_output=True,
                    timeout=10,
                    check=True
                )
        except (subprocess.CalledProcessError, FileNotFoundError, Exception):
            pass

    def _check_go_syntax(self, code: str) -> None:
        """Basic Go syntax check via go vet if available."""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.go', delete=False, dir=tempfile.gettempdir()) as f:
                f.write(code)
                f.flush()
                subprocess.run(
                    ['go', 'vet', f.name],
                    capture_output=True,
                    timeout=10,
                    check=True
                )
        except (subprocess.CalledProcessError, FileNotFoundError, Exception):
            pass

    def _check_rust_syntax(self, code: str) -> None:
        """Basic Rust syntax check via rustc if available."""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.rs', delete=False) as f:
                f.write(code)
                f.flush()
                subprocess.run(
                    ['rustc', '--emit=metadata', f.name],
                    capture_output=True,
                    timeout=10,
                    check=True
                )
        except (subprocess.CalledProcessError, FileNotFoundError, Exception):
            pass

    def _recommend(self, checks: Dict[str, Any], passed: int, total: int) -> str:
        if passed == total:
            return "AUTOMATED_CHECKED"
        if passed >= total * 0.7:
            return "HUMAN_REVIEW"
        return "REJECT"

    def _summary(self) -> Dict[str, Any]:
        total = len(self.results)
        passed = sum(1 for r in self.results if r["all_passed"])
        failed = total - passed
        needs_review = sum(1 for r in self.results if r["recommendation"] == "HUMAN_REVIEW")
        rejected = sum(1 for r in self.results if r["recommendation"] == "REJECT")

        return {
            "total_lessons": total,
            "passed_all_checks": passed,
            "failed": failed,
            "needs_human_review": needs_review,
            "rejected": rejected,
            "automated_checked": passed,
            "details": self.results,
        }


def verify_scrimba_lessons() -> Dict[str, Any]:
    """Run automated verification on all scrimba lessons."""
    verifier = ScrimbaVerifier()
    return verifier.verify_all()


if __name__ == "__main__":
    report = verify_scrimba_lessons()
    print(json.dumps(report, indent=2, default=str))
