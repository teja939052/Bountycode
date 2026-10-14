"""
Lesson service — serves the vertical slice lesson content and grades code submissions.

Responsibilities:
  - Serve lesson content (story, steps, challenges)
  - Run user code against test cases via the code execution engine
  - Record completion: Diamonds, SRS enrollment, mastery update
"""
from typing import Dict, List, Any, Optional
import ast
import logging

from app.services.code_executor import CodeExecutionEngine
from app.services.local_sandbox import execute_local_python_batch
from app.services.spaced_repetition import SpacedRepetitionEngine
from app.services.gamification import record_practice
from app.services.misconception_diagnosis import diagnose_misconception
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
        """Return the full lesson content for this lesson.

        A lesson that ships its own authored `captain_byte` keeps it. Lessons
        shipping no block — or the generic placeholder — get a real one from
        the deterministic library. `mentor` is attached on every response so
        the client has one canonical framing for this lesson.

        Always a shallow copy: the shared registry dict is never mutated.
        """
        from app.services.mentor_service import mentor_block_for_lesson, resolve_captain_byte

        lesson = self._lesson
        # Unknown slug: no lesson, no speech. Never a fake mentor.
        if not lesson:
            return dict(lesson)

        out = dict(lesson)

        block = mentor_block_for_lesson(lesson)
        if block:
            out["captain_byte"] = block

        out["mentor"] = resolve_captain_byte(
            canonical_skill=(
                lesson.get("canonical_skill")
                or (lesson.get("srs_concept_tag") or "").strip()
            ),
            lesson_slug=lesson.get("lesson_id") or "",
            moment="intro",
            fallback_block=lesson.get("captain_byte"),
        )
        return out

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
        if section == "explain":
            return lesson.get("explain")
        if section == "break":
            return lesson.get("break")

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

    def _mentor(
        self,
        moment: str,
        learner_state: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Resolve Captain Byte for a moment of this lesson. One adapter."""
        from app.services.mentor_service import resolve_captain_byte

        return resolve_captain_byte(
            canonical_skill=(
                self._lesson.get("canonical_skill")
                or (self._lesson.get("srs_concept_tag") or "").strip()
            ),
            lesson_slug=self._lesson.get("lesson_id") or "",
            moment=moment,
            learner_state=learner_state,
            fallback_block=self._lesson.get("captain_byte"),
        )

    def _diagnose_misconception(self, stage: str, answer: Any, result: Dict[str, Any]) -> Dict[str, Any]:
        """Run misconception diagnosis when learner answer is wrong."""
        concept = (
            self._lesson.get("canonical_skill")
            or (self._lesson.get("srs_concept_tag") or "").strip()
            or self._lesson.get("lesson_id", "")
        )
        action = f"{stage}_wrong" if not result.get("correct") else f"{stage}_correct"
        trace = [{"type": action, "data": {"answer": str(answer), "stage": stage}}]
        return diagnose_misconception(
            action_trace=trace,
            concept=concept,
        )

    def check_prediction(self, answer_key: str) -> Dict[str, Any]:
        """Check the user's answer to the prediction question."""
        options = self._lesson["prediction"]["options"]
        opt = next((o for o in options if o["id"] == answer_key), None)
        correct = bool(opt.get("correct")) if opt else False
        result = {
            "correct": correct,
            "explanation": opt.get("explanation", "") if opt else "Invalid answer",
            "mentor": self._mentor("correct_1" if correct else "wrong_1"),
        }
        result["misconception"] = self._diagnose_misconception("prediction", answer_key, result)
        return result

    def check_explain(self, answer: str) -> Dict[str, Any]:
        """Grade a natural-language explanation (Explaining stage).

        Correct when the answer contains at least one expected keyword and
        reaches the minimum length. Any-match semantics mirror the concept
        questions in the assessment: the goal is a passing verbal proof, not
        an exact string match.
        """
        section = self._lesson.get("explain") or {}
        keywords = [str(k).lower() for k in section.get("keywords", [])]
        min_words = int(section.get("min_words", 0) or 0) if section else 0

        text = (answer or "").strip()
        word_count = len(text.split())
        matched_keywords = sorted({
            kw for kw in keywords if kw and kw.lower() in text.lower()
        })

        correct = bool(matched_keywords) and word_count >= min_words
        result = {
            "correct": correct,
            "matched_keywords": matched_keywords,
            "word_count": word_count,
            "min_words": min_words,
            "model_answer": section.get("model_answer", ""),
            "intention": section.get("intention", ""),
            "mentor": self._mentor("correct_1" if correct else "wrong_1"),
        }
        result["misconception"] = self._diagnose_misconception("explain", answer, result)
        return result

    def check_break(self, diagnosis: str, fix: str) -> Dict[str, Any]:
        """Grade the Breaking stage: diagnosis choice + one-line fix.

        The fix is matched with whitespace normalisation (same rule as the
        assessment debug questions) so a student can re-indent or respace
        freely. The diagnosis must match the option marked as the cause.
        """
        section = self._lesson.get("break") or {}
        diagnosis_why = ""
        diagnosis_correct = False

        options = (section.get("diagnosis") or {}).get("options", [])
        for opt in options:
            if opt.get("id") == diagnosis:
                diagnosis_correct = bool(opt.get("correct"))
                diagnosis_why = opt.get("why", "")
                break

        expected_fix = str(section.get("fix", "") or "").strip()
        expected_norm = " ".join(expected_fix.split())
        actual_norm = " ".join(str(fix or "").split())
        if expected_norm:
            fix_correct = actual_norm == expected_norm
        else:
            fix_correct = True

        passed = diagnosis_correct and fix_correct
        # Two misses in one stage (diagnosis AND fix) is a repeated
        # misconception — the second line; a single miss is the first.
        if passed:
            moment = "correct_1"
        elif not diagnosis_correct and not fix_correct:
            moment = "wrong_2"
        else:
            moment = "wrong_1"

        result = {
            "diagnosis_correct": diagnosis_correct,
            "fix_correct": fix_correct,
            "passed": passed,
            "diagnosis_why": diagnosis_why,
            "fix": section.get("fix", ""),
            "explanation": section.get("explanation", ""),
            "mentor": self._mentor(moment),
        }
        result["misconception"] = self._diagnose_misconception("break", f"{diagnosis}|{fix}", result)
        return result

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
                expected_norm = " ".join(expected_fix.strip().split())
                actual_norm = " ".join(actual.split())
                correct = actual_norm == expected_norm
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
        passed = score >= self._lesson["assessment"]["mastery_threshold"]
        result = {
            "score": score,
            "passed": passed,
            "earned": earned,
            "total": total,
            "results": results,
            "mentor": self._mentor("after_mastery" if passed else "retry_prompt"),
        }
        result["misconception"] = self._diagnose_misconception("assessment", answers, result)
        return result

    # ──────────────────────────────────────────────────────────────────
    # Completion & rewards
    # ──────────────────────────────────────────────────────────────────

    async def complete_lesson(
        self,
        user_id: str,
        score: float,
        time_spent_seconds: int = 0,
        role: str = "sde",
    ) -> Dict[str, Any]:
        """Record lesson completion: Diamonds, SRS enrollment, mastery update.

        Idempotent: a retry/double-tap that does not beat the stored
        best score awards no Diamonds (no double-credit, no double-advance).
        A strictly better score records the improvement and awards Diamonds.
        """
        from app.database import gamification_collection as _gc

        comp_key = "code_foundations:" + self._lesson.get("world_progression", {}).get(
            "competency_id", self._lesson["lesson_id"]
        )
        # Atomic improvement-claim: of concurrent duplicate submits, exactly
        # one wins the "score beats stored best" filter and awards Diamonds; the
        # losers record attempts only. A read-then-write best check cannot
        # guarantee this under a real double-tap.
        _best_path = f"completed_competencies.{comp_key}.best_score"
        await _gc.update_one(
            {"user_id": user_id},
            {"$setOnInsert": {"user_id": user_id, "completed_competencies": {}}},
            upsert=True,
        )
        _claimed = await _gc.find_one_and_update(
            {"user_id": user_id, "$or": [
                {_best_path: {"$exists": False}},
                {_best_path: {"$lt": float(score)}},
            ]},
            {"$set": {"updated_at": utcnow()}},
        )

        if _claimed is None:
            await self._record_competency(user_id, score)
            # Replay without improvement: no Diamonds (no double-credit), but the
            # replay WAS verified practice — touch last_practice_date so a
            # student replaying to protect a streak doesn't silently lose it
            # when the next real activity sees a stale date. Streak for
            # showing up, Diamonds only for improving. Zero other mutations.
            try:
                await _gc.update_one(
                    {"user_id": user_id},
                    {"$set": {"last_practice_date": utcnow()}},
                )
            except Exception:
                pass
            return {
                "xp_gained": 0,
                "deduplicated": True,
                "streak_protected": True,
                "level": None,
                "level_up": False,
                "srs_enrolled": False,
                "lesson_xp": self._lesson["xp_reward"],
                "mastery_unlocked": score >= self._lesson["assessment"]["mastery_threshold"],
                "mentor": self._mentor(
                    "after_mastery"
                    if score >= self._lesson["assessment"]["mastery_threshold"]
                    else "retry_prompt",
                    learner_state={"stage": "result", "timed": False},
                ),
            }

        # Record Diamonds via gamification
        xp_result = await record_practice(
            user_id=user_id,
            activity_type="lesson",
            score=score / 10,  # gamification expects 0-10 scale
            metadata={"lesson_id": self._lesson["lesson_id"], "time_spent": time_spent_seconds},
            role=role,
        )

        mastery_unlocked = score >= self._lesson["assessment"]["mastery_threshold"]

        # Enroll in SRS only if mastery is achieved
        srs_enrolled = False
        if mastery_unlocked:
            srs_enrolled = await self._enroll_srs(user_id)

        # Record competency completion
        await self._record_competency(user_id, score)

        return {
            "xp_gained": xp_result.get("xp_gained", 0),
            "level": xp_result.get("level", 1),
            "level_up": xp_result.get("level_up", False),
            "srs_enrolled": srs_enrolled,
            "lesson_xp": self._lesson["xp_reward"],
            "mastery_unlocked": mastery_unlocked,
            "mentor": self._mentor(
                "after_mastery" if mastery_unlocked else "retry_prompt",
                learner_state={"stage": "result"},
            ),
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
        """Record competency completion in the gamification collection.

        best_score ratchets only upward and attempts accumulate, so a
        student who struggled then recovered shows the recovery —
        never a clobbered low from a later retry.
        """
        from app.database import gamification_collection
        from app.services.skill_assessment import SKILL_CATEGORIES, update_skill_score

        comp_key = "code_foundations:" + self._lesson.get("world_progression", {}).get(
            "competency_id", self._lesson["lesson_id"]
        )

        _doc = await gamification_collection.find_one({"user_id": user_id}) or {}
        _prev = _doc.get("completed_competencies", {}).get(comp_key, {})

        await gamification_collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    f"completed_competencies.{comp_key}": {
                        "completed": True,
                        "score": score,
                        "best_score": max(float(_prev.get("best_score", 0) or 0), float(score)),
                        "attempts": int(_prev.get("attempts", 0) or 0) + 1,
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

