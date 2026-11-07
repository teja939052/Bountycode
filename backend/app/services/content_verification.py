"""Content verification service — validates questions before promotion to TRUSTED.

Executes solution code against visible + hidden test cases, checks hint quality,
detects ambiguity, and produces a verification report. This is the automated
gate in the Content Trust pipeline (UNVERIFIED -> AUTOMATED_CHECKED -> HUMAN_REVIEWED -> TRUSTED).

Canonicity: this module does NOT promote content. It only produces evidence.
Promotion decisions belong to the review queue / human reviewers per AGENTS.md.
"""
from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional

from app.services.code_executor import CodeExecutionEngine

logger = logging.getLogger(__name__)


class ContentVerificationError(Exception):
    """Raised when verification cannot complete (e.g., executor unavailable)."""


class ContentVerifier:
    """Verify a single question's correctness and quality."""

    def __init__(self):
        self._engine = CodeExecutionEngine()

    # ── Public API ─────────────────────────────────────────────────────

    async def verify(self, question: Dict[str, Any]) -> Dict[str, Any]:
        """Run all automated checks on a question.

        Returns a report::
            {
                "question_id": "...",
                "checks": {
                    "has_solution": {"pass": true, "detail": "..."},
                    "solution_executes": {"pass": true, "detail": "..."},
                    "solution_passes_tests": {"pass": true, "detail": "...", "score": 100},
                    "has_hints": {"pass": true, "detail": "..."},
                    "hints_not_answer": {"pass": true, "detail": "..."},
                    "question_clarity": {"pass": true, "detail": "..."},
                },
                "pass_count": 5,
                "total_checks": 6,
                "all_passed": false,
                "recommendation": "HUMAN_REVIEW" | "TRUSTED" | "REJECT",
            }
        """
        checks: Dict[str, Any] = {}

        checks["has_solution"] = self._check_has_solution(question)
        checks["has_question_text"] = self._check_has_question_text(question)
        checks["has_test_cases"] = self._check_has_test_cases(question)

        # Code-type questions: execute the solution against test cases
        if question.get("type") == "coding" and checks["has_solution"]["pass"]:
            exec_result = await self._check_solution_executes(question)
            checks["solution_executes"] = exec_result
            if exec_result["pass"]:
                checks["solution_passes_tests"] = await self._check_solution_passes_tests(question)
            else:
                checks["solution_passes_tests"] = {
                    "pass": False,
                    "detail": "Skipped: solution does not execute",
                }

        # Hint quality (all types)
        if question.get("hints"):
            checks["hints_not_answer"] = self._check_hints_not_answer(question)
        else:
            checks["hints_not_answer"] = {
                "pass": True,
                "detail": "No hints provided (optional)",
            }

        checks["question_clarity"] = self._check_question_clarity(question)

        passed = sum(1 for c in checks.values() if c.get("pass"))
        total = len(checks)

        return {
            "question_id": question.get("id", question.get("_id", "unknown")),
            "checks": checks,
            "pass_count": passed,
            "total_checks": total,
            "all_passed": passed == total,
            "recommendation": self._recommend(checks, passed, total),
        }

    async def verify_batch(
        self, questions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Verify a batch of questions. Returns a summary report."""
        results: List[Dict[str, Any]] = []
        for q in questions:
            try:
                report = await self.verify(q)
                results.append(report)
            except Exception as exc:
                logger.warning("Verification failed for %s: %s", q.get("id"), exc)
                results.append({
                    "question_id": q.get("id", "unknown"),
                    "error": str(exc),
                    "recommendation": "REJECT",
                })

        passed = sum(1 for r in results if r.get("all_passed"))
        failed = len(results) - passed
        needs_review = sum(
            1 for r in results if r.get("recommendation") == "HUMAN_REVIEW"
        )

        return {
            "total": len(results),
            "passed_all_checks": passed,
            "failed": failed,
            "needs_human_review": needs_review,
            "results": results,
        }

    # ── Individual checks ──────────────────────────────────────────────

    def _check_has_solution(self, q: Dict[str, Any]) -> Dict[str, Any]:
        sol = q.get("solution")
        if isinstance(sol, dict) and sol.get("code"):
            return {"pass": True, "detail": "Solution code present"}
        if isinstance(sol, str) and sol.strip():
            return {"pass": True, "detail": "Solution text present"}
        return {"pass": False, "detail": "Missing solution"}

    def _check_has_question_text(self, q: Dict[str, Any]) -> Dict[str, Any]:
        text = q.get("question", "")
        if isinstance(text, str) and len(text.strip()) >= 20:
            return {"pass": True, "detail": f"Question text present ({len(text)} chars)"}
        return {"pass": False, "detail": "Question text missing or too short (<20 chars)"}

    def _check_has_test_cases(self, q: Dict[str, Any]) -> Dict[str, Any]:
        tcs = q.get("test_cases", [])
        if isinstance(tcs, list) and len(tcs) >= 1:
            return {"pass": True, "detail": f"{len(tcs)} test case(s)"}
        # MCQ/aptitude may use correct_answer instead
        if q.get("correct_answer") is not None:
            return {"pass": True, "detail": "Uses correct_answer (non-code)"}
        return {"pass": False, "detail": "No test cases or correct_answer"}

    async def _check_solution_executes(self, q: Dict[str, Any]) -> Dict[str, Any]:
        code = self._extract_solution_code(q)
        if not code:
            return {"pass": False, "detail": "Could not extract solution code"}
        language = (
            q.get("solution", {}).get("language", "python")
            if isinstance(q.get("solution"), dict)
            else "python"
        )
        try:
            result = await self._engine.execute_code(code, language)
            if result.get("success"):
                return {"pass": True, "detail": "Solution executes without error"}
            return {
                "pass": False,
                "detail": f"Solution execution failed: {result.get('error', 'unknown')[:200]}",
            }
        except Exception as exc:
            return {"pass": False, "detail": f"Executor error: {exc}"}

    async def _check_solution_passes_tests(self, q: Dict[str, Any]) -> Dict[str, Any]:
        code = self._extract_solution_code(q)
        language = (
            q.get("solution", {}).get("language", "python")
            if isinstance(q.get("solution"), dict)
            else "python"
        )
        test_cases = q.get("test_cases", [])
        if not test_cases:
            return {"pass": True, "detail": "No test cases to run against", "score": 100}

        function_name = q.get("function_name", "")
        try:
            result = await self._engine.execute_against_test_cases(
                code, language, test_cases, function_name
            )
            if result.get("all_passed"):
                return {
                    "pass": True,
                    "detail": f"All {result.get('total_count')} test cases passed",
                    "score": 100,
                }
            return {
                "pass": False,
                "detail": f"{result.get('passed_count')}/{result.get('total_count')} test cases passed",
                "score": result.get("score", 0),
                "failures": [
                    r for r in result.get("results", []) if not r.get("passed")
                ][:3],
            }
        except Exception as exc:
            return {"pass": False, "detail": f"Test execution error: {exc}"}

    def _check_hints_not_answer(self, q: Dict[str, Any]) -> Dict[str, Any]:
        """Check that hints don't just restate the answer."""
        hints = q.get("hints", [])
        answer = str(q.get("correct_answer", "")).strip().lower()
        solution_code = ""
        sol = q.get("solution")
        if isinstance(sol, dict):
            solution_code = str(sol.get("code", "")).lower()

        issues = []
        for i, hint in enumerate(hints):
            h = str(hint).strip().lower()
            # Hint is suspicious if it's identical to the answer
            if answer and h == answer:
                issues.append(f"Hint {i+1} is identical to the answer")
            # Hint is suspicious if it contains the full solution code
            if solution_code and len(solution_code) > 20 and solution_code in h:
                issues.append(f"Hint {i+1} contains the full solution")

        if issues:
            return {"pass": False, "detail": "; ".join(issues)}
        return {"pass": True, "detail": f"{len(hints)} hint(s), none reveal the answer"}

    def _check_question_clarity(self, q: Dict[str, Any]) -> Dict[str, Any]:
        """Basic clarity heuristics."""
        text = str(q.get("question", ""))
        issues = []

        # Very short questions are suspicious
        if len(text) < 30:
            issues.append("Question text is very short (<30 chars)")

        # Check for common ambiguity markers
        ambiguous_patterns = [
            r"\b(etc|and so on|some|any|appropriate)\b",
        ]
        for pat in ambiguous_patterns:
            if re.search(pat, text, re.IGNORECASE):
                issues.append(f"Contains ambiguous term matching: {pat}")

        # MCQ should have options
        if q.get("type") in ("mcq", "aptitude", "logical", "verbal"):
            opts = q.get("options", [])
            if isinstance(opts, list) and len(opts) < 2:
                issues.append("MCQ has fewer than 2 options")

        if issues:
            return {"pass": False, "detail": "; ".join(issues)}
        return {"pass": True, "detail": "Question appears clear"}

    # ── Helpers ────────────────────────────────────────────────────────

    def _extract_solution_code(self, q: Dict[str, Any]) -> str:
        sol = q.get("solution")
        if isinstance(sol, dict):
            return str(sol.get("code", ""))
        if isinstance(sol, str):
            return sol
        return ""

    def _recommend(
        self, checks: Dict[str, Any], passed: int, total: int
    ) -> str:
        """Produce a recommendation based on check results."""
        critical = ["has_solution", "has_question_text", "solution_executes"]
        for key in critical:
            if key in checks and not checks[key].get("pass"):
                return "REJECT"

        if passed == total:
            return "TRUSTED"
        if passed >= total * 0.7:
            return "HUMAN_REVIEW"
        return "REJECT"
