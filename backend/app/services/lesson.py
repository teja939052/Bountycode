"""
Lesson service — serves the vertical slice lesson content and grades code submissions.

Responsibilities:
  - Serve lesson content (story, steps, challenges)
  - Run user code against test cases via the code execution engine
  - Record completion: XP, SRS enrollment, mastery update
"""
from typing import Dict, List, Any, Optional
import ast
import logging

from app.services.code_executor import CodeExecutionEngine
from app.services.local_sandbox import execute_local_python_batch
from app.services.spaced_repetition import SpacedRepetitionEngine
from app.services.gamification import record_practice
from app.database import srs_collection
from app.utils.timeutil import utcnow

logger = logging.getLogger(__name__)

LETTTER_TO_OPTION = {
    "a": "a",
    "b": "b",
    "c": "c",
    "d": "d",
}


class LessonService:
    """Generic lesson service, parameterised by a lesson content dict.

    The same engine serves every foundation lesson (variables_state,
    control_flow, …); the lesson-specific content is supplied at construction.
    """

    def __init__(self, lesson: Dict[str, Any]):
        self._lesson = lesson
        self._engine = CodeExecutionEngine()
        self._srs = SpacedRepetitionEngine()

    # ──────────────────────────────────────────────────────────────────
    # Content delivery
    # ──────────────────────────────────────────────────────────────────

    def get_lesson(self) -> Dict[str, Any]:
        """Return the full lesson content for this lesson."""
        return self._lesson

    def get_step(self, step_key: str) -> Optional[Dict[str, Any]]:
        """Return a specific step from the guided_build or assessment.

        step_key format: 'guided_build:<index>' or 'assessment:<index>'
        or 'discovery' or 'prediction' or 'transfer_challenge'
        """
        parts = step_key.split(":", 1)
        section = parts[0]
        idx = parts[1] if len(parts) > 1 else None

        lesson = self._lesson

        if section == "discovery":
            return lesson["discovery"]
        if section == "prediction":
            return lesson["prediction"]
        if section == "transfer_challenge":
            return lesson["transfer_challenge"]

        if section == "guided_build" and idx is not None:
            steps = lesson["guided_build"]["steps"]
            i = int(idx)
            if 0 <= i < len(steps):
                return steps[i]
            return None

        if section == "assessment" and idx is not None:
            questions = lesson["assessment"]["questions"]
            i = int(idx)
            if 0 <= i < len(questions):
                return questions[i]
            return None

        return None

    # ──────────────────────────────────────────────────────────────────
    # Code execution & grading
    # ──────────────────────────────────────────────────────────────────

    def _wrap_python_test(
        self,
        user_code: str,
        function_name: str,
        test_cases: List[Dict[str, Any]],
    ) -> str:
        """Wrap user code with test-case runner for Python."""
        test_lines = []
        for i, tc in enumerate(test_cases):
            inputs = tc.get("input", [])
            expected = tc.get("expected")
            if not isinstance(inputs, list):
                inputs = [inputs]
            args_str = ", ".join(repr(a) for a in inputs)
            test_lines.append(f'_result_{i} = {function_name}({args_str})')
            test_lines.append(
                f'print(f"TEST_{i}:{{_result_{i}}}")'
            )
        return user_code + "\n" + "\n".join(test_lines)

    async def run_code(
        self,
        code: str,
        language: str = "python",
        stdin: str = "",
    ) -> Dict[str, Any]:
        """Execute arbitrary code (for explore/prediction steps)."""
        result = await self._engine.execute_code(
            code=code,
            language=language,
            stdin=stdin,
            timeout=10,
        )
        return result

    async def submit_build_step(
        self,
        user_code: str,
        function_name: str,
        test_cases: List[Dict[str, Any]],
        language: str = "python",
    ) -> Dict[str, Any]:
        """Run user code against test cases and return pass/fail details.

        For Python we use the local batch oracle (zero Piston calls), so the
        lesson judges answers offline and quickly. If the local oracle is
        unavailable we fall back to the per-case Piston execution path.
        """
        if language.lower() == "python":
            local = await self._judge_python_local(user_code, function_name, test_cases)
            if local is not None:
                return local

        # Fallback: wrap code with the TEST_<i>: marker harness and run via the engine.
        wrapped = self._wrap_python_test(user_code, function_name, test_cases)
        result = await self._engine.execute_code(
            code=wrapped,
            language=language,
            stdin="",
            timeout=10,
        )

        if not result.get("success"):
            return {
                "passed": False,
                "all_passed": False,
                "passed_count": 0,
                "total_count": len(test_cases),
                "error": result.get("stderr") or result.get("error", ""),
                "compile_error": result.get("compile_error"),
                "results": [],
            }

        stdout = result.get("stdout", "")
        results = []
        passed_count = 0

        for i, tc in enumerate(test_cases):
            expected = tc.get("expected")
            marker = f"TEST_{i}:"
            actual = None
            for line in stdout.splitlines():
                if line.startswith(marker):
                    actual = line[len(marker):]
                    break

            if actual is None:
                results.append({
                    "test_case_index": i + 1,
                    "passed": False,
                    "input": tc.get("input", ""),
                    "expected": repr(expected),
                    "actual": "(not executed)",
                    "error": "No output marker found",
                })
            else:
                passed = self._values_equal(actual, expected)
                if passed:
                    passed_count += 1
                results.append({
                    "test_case_index": i + 1,
                    "passed": passed,
                    "input": tc.get("input", ""),
                    "expected": repr(expected) if not tc.get("hidden") else "[HIDDEN]",
                    "actual": actual if not tc.get("hidden") else "[HIDDEN]",
                    "error": None if passed else "Output mismatch",
                })

        all_passed = passed_count == len(test_cases)
        score = round(passed_count / len(test_cases) * 100, 1) if test_cases else 0

        return {
            "passed": all_passed,
            "all_passed": all_passed,
            "passed_count": passed_count,
            "total_count": len(test_cases),
            "score": score,
            "results": results,
        }

    async def _judge_python_local(
        self,
        user_code: str,
        function_name: str,
        test_cases: List[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:
        """Judge a Python submission using the local batch oracle (no Piston)."""
        stdins = []
        for tc in test_cases:
            inputs = tc.get("input", [])
            if not isinstance(inputs, (list, tuple)):
                inputs = [inputs]
            stdins.append(str(tuple(inputs)))

        try:
            batch = await execute_local_python_batch(
                code=user_code,
                stdins=stdins,
                function_name=function_name,
            )
        except Exception:
            return None

        if not batch.get("success"):
            return {
                "passed": False,
                "all_passed": False,
                "passed_count": 0,
                "total_count": len(test_cases),
                "error": batch.get("compile_error") or batch.get("error", "Execution failed"),
                "compile_error": batch.get("compile_error"),
                "results": [],
            }

        raw_results = batch.get("results", [])
        results = []
        passed_count = 0

        for i, tc in enumerate(test_cases):
            expected = tc.get("expected")
            passed = False
            actual = "(failed to run)"
            if i < len(raw_results):
                case_ok, actual = raw_results[i]
                if case_ok:
                    passed = self._values_equal(actual, expected)
                else:
                    actual = "(error)"
            if passed:
                passed_count += 1
            hidden = bool(tc.get("hidden") or tc.get("is_hidden"))
            results.append({
                "test_case_index": i + 1,
                "passed": passed,
                "input": tc.get("input", ""),
                "expected": repr(expected) if not hidden else "[HIDDEN]",
                "actual": actual if not hidden else "[HIDDEN]",
                "error": None if passed else "Output mismatch",
                "is_hidden": hidden,
            })

        all_passed = passed_count == len(test_cases) and len(test_cases) > 0
        score = round(passed_count / len(test_cases) * 100, 1) if test_cases else 0

        return {
            "passed": all_passed,
            "all_passed": all_passed,
            "passed_count": passed_count,
            "total_count": len(test_cases),
            "score": score,
            "results": results,
            "engine": "local_oracle_batch",
        }

    def _values_equal(self, actual: str, expected: Any) -> bool:
        """Compare actual stdout value to expected value."""
        try:
            actual_stripped = actual.strip()
            expected_repr = repr(expected).strip()
            if actual_stripped == expected_repr:
                return True
            try:
                actual_eval = ast.literal_eval(actual_stripped)
                if self._deep_values_equal(actual_eval, expected):
                    return True
            except (ValueError, SyntaxError):
                pass
            return actual_stripped == str(expected).strip()
        except Exception:
            return False

    def _deep_values_equal(self, a: Any, b: Any) -> bool:
        """Recursive value equality that treats tuples and lists as interchangeable.

        The local oracle serialises every function return to JSON, so a function
        that returns (2, 1) comes back as [2, 1]. Lesson test cases may express the
        expected answer as a tuple or a list — both should satisfy the same check.
        """
        if type(a) is bool or type(b) is bool:
            return a is b
        if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
            return len(a) == len(b) and all(
                self._deep_values_equal(x, y) for x, y in zip(a, b)
            )
        if isinstance(a, dict) and isinstance(b, dict):
            return a.keys() == b.keys() and all(
                self._deep_values_equal(a[k], b[k]) for k in a
            )
        if isinstance(a, float) or isinstance(b, float):
            try:
                return abs(float(a) - float(b)) < 1e-9
            except (TypeError, ValueError):
                return False
        return a == b

    def check_prediction(self, answer_key: str) -> Dict[str, Any]:
        """Check the user's answer to the prediction question."""
        options = self._lesson["prediction"]["options"]
        for opt in options:
            if opt["id"] == answer_key:
                return {
                    "correct": opt["correct"],
                    "explanation": opt["explanation"],
                }
        return {"correct": False, "explanation": "Invalid answer"}

    def check_assessment(
        self,
        answers: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Grade the final assessment. Returns score and explanations."""
        questions = self._lesson["assessment"]["questions"]
        results = []
        total = 0
        earned = 0

        for i, q in enumerate(questions):
            if q["type"] == "code_tracing":
                expected = q["expected_answer"]
                actual = answers.get(f"q{i}")
                correct = str(actual).strip().lower() == str(expected).strip().lower()
                results.append({
                    "index": i,
                    "type": q["type"],
                    "correct": correct,
                    "explanation": q["explanation"],
                })
                total += 1
                if correct:
                    earned += 1

            elif q["type"] == "concept":
                keywords = q.get("keywords", [])
                answer = str(answers.get(f"q{i}", "")).lower()
                correct = any(kw in answer for kw in keywords)
                results.append({
                    "index": i,
                    "type": q["type"],
                    "correct": correct,
                    "explanation": q["explanation"],
                })
                total += 1
                if correct:
                    earned += 1

            elif q["type"] == "debug":
                expected_fix = q.get("fix", "")
                actual = str(answers.get(f"q{i}", "")).strip()
                correct = actual == expected_fix.strip()
                results.append({
                    "index": i,
                    "type": q["type"],
                    "correct": correct,
                    "explanation": q["explanation"],
                })
                total += 1
                if correct:
                    earned += 1

        score = round(earned / total * 100, 1) if total > 0 else 0
        return {
            "score": score,
            "passed": score >= self._lesson["assessment"]["mastery_threshold"],
            "earned": earned,
            "total": total,
            "results": results,
        }

    # ──────────────────────────────────────────────────────────────────
    # Completion & rewards
    # ──────────────────────────────────────────────────────────────────

    async def complete_lesson(
        self,
        user_id: str,
        score: float,
        time_spent_seconds: int = 0,
    ) -> Dict[str, Any]:
        """Record lesson completion: XP, SRS enrollment, mastery update."""
        # Record XP via gamification
        xp_result = await record_practice(
            user_id=user_id,
            activity_type="lesson",
            score=score / 10,  # gamification expects 0-10 scale
            metadata={"lesson_id": self._lesson["lesson_id"], "time_spent": time_spent_seconds},
        )

        # Enroll in SRS
        srs_enrolled = await self._enroll_srs(user_id)

        # Record competency completion
        await self._record_competency(user_id, score)

        return {
            "xp_gained": xp_result.get("xp_gained", 0),
            "level": xp_result.get("level", 1),
            "level_up": xp_result.get("level_up", False),
            "srs_enrolled": srs_enrolled,
            "lesson_xp": self._lesson["xp_reward"],
            "mastery_unlocked": score >= self._lesson["assessment"]["mastery_threshold"],
        }

    async def _enroll_srs(self, user_id: str) -> bool:
        """Enroll the user's first SRS card for this concept."""
        srs_cfg = self._lesson["srs_enrollment"]
        concept_id = srs_cfg["concept_id"]

        existing = await srs_collection.find_one({
            "user_id": user_id,
            "concept_id": concept_id,
        })
        if existing:
            return False

        state = self._srs.create_new_card(concept_id, user_id)
        card_doc = {
            "user_id": user_id,
            "concept_id": concept_id,
            "concept_name": srs_cfg["concept_name"],
            "interval": state.interval,
            "repetitions": state.repetitions,
            "ease_factor": state.ease_factor,
            "next_review": state.next_review,
            "last_reviewed": None,
            "learning_step": state.learning_step,
            "total_reviews": 0,
            "lapses": 0,
            "key_points": srs_cfg["key_points"],
            "spaced_fields": srs_cfg["spaced_fields"],
            "created_at": state.created_at,
            "updated_at": state.updated_at,
        }
        await srs_collection.insert_one(card_doc)
        return True

    async def _record_competency(self, user_id: str, score: float) -> None:
        """Record competency completion in the gamification collection."""
        from app.database import gamification_collection
        from app.services.skill_assessment import SKILL_CATEGORIES, update_skill_score

        comp_key = "code_foundations:" + self._lesson.get("world_progression", {}).get(
            "competency_id", self._lesson["lesson_id"]
        )

        await gamification_collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    f"completed_competencies.{comp_key}": {
                        "completed": True,
                        "score": score,
                        "best_score": score,
                        "completed_at": utcnow().isoformat(),
                    },
                    "updated_at": utcnow(),
                },
            },
            upsert=True,
        )

        # Update skill scores for each skill taught
        for skill in self._lesson["skills_taught"]:
            for cat_id, cat_info in SKILL_CATEGORIES.items():
                if skill in cat_info.get("skills", []):
                    await update_skill_score(user_id, cat_id, skill, score, True)

