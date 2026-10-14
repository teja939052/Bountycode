"""Domain adapters — map the canonical 9-step teaching loop to each domain.

Each adapter knows how to:
  - render a step for the frontend
  - grade a learner response
  - produce a misconception code list for the concept
  - describe the mastery check

Domains:
  - Coding        (uses world Level model + code execution)
  - Behavioral    (uses STAR evaluation + company question bank)
  - SystemDesign  (uses bank/AI questions + LLM rubric)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from app.services.domain_misconceptions import get_domain_library


# ═══════════════════════════════════════════════════════════════
# Base
# ═══════════════════════════════════════════════════════════════

class ContentNotFoundError(Exception):
    """Raised when authored content is missing for a requested lesson."""


class StepResult:
    """Normalized result from grading a learner response."""

    def __init__(
        self,
        passed: bool,
        score: float,
        message: str = "",
        evidence: Optional[dict] = None,
        diagnosis_codes: Optional[List[str]] = None,
        feedback: Optional[dict] = None,
    ):
        self.passed = passed
        self.score = max(0.0, min(100.0, float(score)))
        self.message = message
        self.evidence = evidence or {}
        self.diagnosis_codes = diagnosis_codes or []
        self.feedback = feedback or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "score": self.score,
            "message": self.message,
            "evidence": self.evidence,
            "diagnosis_codes": self.diagnosis_codes,
            "feedback": self.feedback,
        }


class DomainAdapter(ABC):
    """Abstract adapter for a learning domain."""

    domain: str = ""

    def __init__(self, level_or_context: Any = None, user_id: str = ""):
        self._level = level_or_context
        self._user_id = user_id

    # ───────────────────────────────────────────────────────────
    # Content
    # ───────────────────────────────────────────────────────────

    @abstractmethod
    def render_step(self, step_index: int, step_name: str) -> Dict[str, Any]:
        """Return the frontend-renderable payload for a step."""

    @abstractmethod
    def mastery_check(self) -> Dict[str, Any]:
        """Return metadata for the mastery/transfer step."""

    # ───────────────────────────────────────────────────────────
    # Grading
    # ───────────────────────────────────────────────────────────

    @abstractmethod
    async def grade(
        self,
        step_name: str,
        response: Dict[str, Any],
    ) -> StepResult:
        """Grade a learner response for a step."""

    # ───────────────────────────────────────────────────────────
    # Misconceptions
    # ───────────────────────────────────────────────────────────

    def misconception_codes(self, concept: str) -> List[str]:
        """Return applicable misconception codes for this concept."""
        lib = get_domain_library(self.domain)
        by_concept = lib.get("by_concept", {})
        return by_concept.get(concept, [])

    # ───────────────────────────────────────────────────────────
    # Helpers
    # ───────────────────────────────────────────────────────────

    def _step_names(self) -> List[str]:
        return [
            "discover",
            "understand",
            "manipulate",
            "predict",
            "build",
            "break_step",
            "debug",
            "retrieval",
            "transfer",
        ]

    def _concept(self) -> str:
        if self._level is None:
            return "general"
        concept = getattr(self._level, "concept", None)
        return concept or getattr(self._level, "topic", None) or "general"

    def _authored_content(self) -> Dict[str, Any]:
        """Load authored lesson content for non-coding domains.

        Raises ContentNotFoundError when no authored content exists.
        """
        concept = self._concept()
        if not concept or concept == "general":
            raise ContentNotFoundError(
                f"No authored content for domain={self.domain} concept={concept!r}"
            )
        try:
            from app.content.curriculum.registry import get_lesson_dict
        except Exception:
            raise ContentNotFoundError("Lesson registry unavailable")

        lesson = get_lesson_dict(concept)
        if lesson is None:
            raise ContentNotFoundError(
                f"No authored lesson for slug={concept!r} in domain={self.domain}"
            )
        if lesson.get("domain") not in (self.domain, ""):
            raise ContentNotFoundError(
                f"Domain mismatch for slug={concept!r}: expected {self.domain}, got {lesson.get('domain')}"
            )
        return lesson


# ═══════════════════════════════════════════════════════════════
# Coding adapter
# ═══════════════════════════════════════════════════════════════

class CodingAdapter(DomainAdapter):
    domain = "coding"

    def render_step(self, step_index: int, step_name: str) -> Dict[str, Any]:
        lvl = self._level
        if lvl is None:
            return {"step_index": step_index, "step_name": step_name, "content": {}}

        step_name = step_name or self._step_names()[step_index]
        content: Dict[str, Any] = {
            "step_index": step_index,
            "step_name": step_name,
            "concept": getattr(lvl, "concept", ""),
            "mental_model": getattr(lvl, "mental_model", ""),
            "story": lvl.story.model_dump() if hasattr(lvl.story, "model_dump") else lvl.story.dict(),
            "tutor": lvl.tutor.model_dump() if hasattr(lvl.tutor, "model_dump") else lvl.tutor.dict(),
        }

        if step_name == "discover":
            content["discover"] = lvl.discover.model_dump() if hasattr(lvl.discover, "model_dump") else lvl.discover.dict()
        elif step_name == "understand":
            content["understand"] = getattr(lvl, "understand", "") or ""
        elif step_name == "manipulate":
            content["manipulate"] = lvl.manipulate.model_dump() if hasattr(lvl.manipulate, "model_dump") else lvl.manipulate.dict()
        elif step_name == "predict":
            pred = getattr(lvl, "predict", None)
            content["predict"] = pred.model_dump() if pred and hasattr(pred, "model_dump") else (pred.dict() if pred else None)
        elif step_name == "build":
            bld = getattr(lvl, "build", None)
            content["build"] = bld.model_dump() if bld and hasattr(bld, "model_dump") else (bld.dict() if bld else None)
        elif step_name == "break_step":
            bs = getattr(lvl, "break_step", None)
            content["break_step"] = bs.model_dump() if bs and hasattr(bs, "model_dump") else (bs.dict() if bs else None)
        elif step_name == "debug":
            dbg = getattr(lvl, "debug", None)
            content["debug"] = dbg.model_dump() if dbg and hasattr(dbg, "model_dump") else (dbg.dict() if dbg else None)
        elif step_name == "retrieval":
            ret = getattr(lvl, "retrieval", None)
            content["retrieval"] = ret.model_dump() if ret and hasattr(ret, "model_dump") else (ret.dict() if ret else None)
        elif step_name == "transfer":
            tr = getattr(lvl, "transfer", None)
            content["transfer"] = tr.model_dump() if tr and hasattr(tr, "model_dump") else (tr.dict() if tr else None)

        content["code"] = lvl.code.model_dump() if hasattr(lvl.code, "model_dump") else lvl.code.dict()
        content["checks"] = lvl.checks.model_dump() if hasattr(lvl.checks, "model_dump") else lvl.checks.dict()
        content["hints"] = getattr(lvl, "hints", [])
        content["mastery_threshold"] = getattr(lvl, "mastery_threshold", 80)
        return content

    def mastery_check(self) -> Dict[str, Any]:
        lvl = self._level
        if lvl is None:
            return {"step_name": "transfer", "threshold": 80}
        tr = getattr(lvl, "transfer", None)
        return {
            "step_name": "transfer",
            "threshold": getattr(lvl, "mastery_threshold", 80),
            "answer": tr.answer if tr else "",
            "context": tr.context if tr else "",
        }

    async def grade(self, step_name: str, response: Dict[str, Any]) -> StepResult:
        from app.routes.worlds import _text_pass, _judge_break_step, _judge_execution, _judge_code_run

        lvl = self._level
        if lvl is None:
            return StepResult(passed=False, score=0, message="No level content")

        user_code = response.get("code", "") or ""
        language = response.get("language", "python")

        if step_name == "predict":
            answer = getattr(lvl, "predict", None)
            if answer and answer.answer:
                passed = _text_pass(user_code, answer.answer)
                return StepResult(
                    passed=passed,
                    score=100.0 if passed else 0.0,
                    message=answer.explanation or ("Correct!" if passed else f"Expected: {answer.answer}"),
                )
            return StepResult(passed=False, score=0, message="Missing predict answer")

        if step_name == "manipulate":
            manip = getattr(lvl, "manipulate", None)
            if manip and manip.answer:
                passed = _text_pass(user_code, manip.answer)
                return StepResult(
                    passed=passed,
                    score=100.0 if passed else 0.0,
                    message=manip.hint or ("Correct!" if passed else f"Expected: {manip.answer}"),
                )
            return StepResult(passed=False, score=0, message="Missing manipulate answer")

        if step_name == "retrieval":
            ret = getattr(lvl, "retrieval", None)
            if ret and ret.answer:
                passed = _text_pass(user_code, ret.answer)
                return StepResult(
                    passed=passed,
                    score=100.0 if passed else 0.0,
                    message=ret.explanation or ("Correct!" if passed else f"Expected: {ret.answer}"),
                )
            return StepResult(passed=False, score=0, message="Missing retrieval answer")

        if step_name == "break_step":
            bs = getattr(lvl, "break_step", None)
            if bs:
                passed, msg, _ = await _judge_break_step(
                    user_code, bs.broken_code, bs.expected_failure, language
                )
                return StepResult(passed=passed, score=100.0 if passed else 0.0, message=msg)
            return StepResult(passed=False, score=0, message="Missing break_step content")

        if step_name == "debug":
            dbg = getattr(lvl, "debug", None)
            if dbg and dbg.answer:
                verdict = await _judge_execution(user_code, dbg.answer, language)
                if verdict is not None:
                    passed, msg, _ = verdict
                    return StepResult(passed=passed, score=100.0 if passed else 0.0, message=msg)
                passed = _text_pass(user_code, dbg.answer)
                return StepResult(passed=passed, score=100.0 if passed else 0.0, message=dbg.answer)
            return StepResult(passed=False, score=0, message="Missing debug answer")

        if step_name == "transfer":
            tr = getattr(lvl, "transfer", None)
            if tr and tr.answer:
                verdict = await _judge_execution(user_code, tr.answer, language)
                if verdict is not None:
                    passed, msg, evidence = verdict
                    return StepResult(
                        passed=passed,
                        score=100.0 if passed else 0.0,
                        message=msg,
                        evidence=evidence,
                    )
                passed = _text_pass(user_code, tr.answer)
                return StepResult(passed=passed, score=100.0 if passed else 0.0)
            return StepResult(passed=False, score=0, message="Missing transfer answer")

        # build / code — run with judge
        verdict = await _judge_code_run(user_code, language, lvl)
        if verdict is not None:
            passed, msg, hint_idx, evidence = verdict
            return StepResult(
                passed=passed,
                score=100.0 if passed else 0.0,
                message=msg,
                evidence=evidence,
            )
        return StepResult(passed=False, score=0, message="Could not judge submission")


# ═══════════════════════════════════════════════════════════════
# Behavioral adapter
# ═══════════════════════════════════════════════════════════════

class BehavioralAdapter(DomainAdapter):
    domain = "behavioral"

    def __init__(self, level_or_context=None, user_id: str = "", company: str = "", role: str = ""):
        super().__init__(level_or_context, user_id)
        self._company = company or getattr(level_or_context, "company", "") or "general"
        self._role = role or getattr(level_or_context, "role", "") or "sde"

    def _interaction_kind(self, step_name: str) -> str:
        kinds = {
            "discover": "read_question",
            "understand": "read_explanation",
            "manipulate": "mcq_classify",
            "predict": "mcq_identify_weakness",
            "build": "guided_writing",
            "break_step": "mcq_diagnose",
            "debug": "guided_improvement",
            "retrieval": "recall_flashcard",
            "transfer": "full_star_answer",
        }
        return kinds.get(step_name, "text_input")

    def _step_content(self, step_name: str) -> Dict[str, Any]:
        lesson = self._authored_content()
        steps = lesson.get("steps") or {}
        step = steps.get(step_name)
        if step is None:
            raise ContentNotFoundError(
                f"Authored lesson missing step={step_name!r} for slug={self._concept()!r}"
            )
        return step

    def render_step(self, step_index: int, step_name: str) -> Dict[str, Any]:
        step_name = step_name or self._step_names()[step_index]
        try:
            content = self._step_content(step_name)
        except ContentNotFoundError:
            content = {}
        return {
            "step_index": step_index,
            "step_name": step_name,
            "domain": self.domain,
            "company": self._company,
            "role": self._role,
            "concept": self._concept(),
            "content": content,
            "interaction_kind": self._interaction_kind(step_name),
            "mastery_threshold": 75,
        }

    def mastery_check(self) -> Dict[str, Any]:
        try:
            transfer = self._step_content("transfer")
            return {
                "step_name": "transfer",
                "threshold": 75,
                "prompt": transfer.get("prompt", ""),
                "guidelines": transfer.get("guidelines", []),
            }
        except ContentNotFoundError:
            return {
                "step_name": "transfer",
                "threshold": 75,
                "prompt": f"Write a complete STAR answer for a behavioral question at {self._company}.",
            }

    async def grade(self, step_name: str, response: Dict[str, Any]) -> StepResult:
        answer_text = response.get("answer", "") or response.get("text", "") or ""

        if step_name == "discover":
            return StepResult(passed=True, score=100.0, message="Read the question carefully.")

        try:
            step = self._step_content(step_name)
        except ContentNotFoundError:
            step = {}

        if step_name == "understand":
            keywords = ["situation", "task", "action", "result", "star"]
            matched = sum(1 for kw in keywords if kw in answer_text.lower())
            passed = matched >= 2
            return StepResult(
                passed=passed,
                score=min(100.0, matched * 25.0),
                message=step.get("prompt", "Explain the STAR framework in your own words."),
            )

        if step_name == "manipulate":
            selected = response.get("selected_component", "")
            expected = step.get("expected_component") or response.get("expected_component", "")
            passed = bool(selected) and (selected == expected or not expected)
            return StepResult(passed=passed, score=100.0 if passed else 0.0, message=step.get("prompt", "Classify the sentence."))

        if step_name == "predict":
            selected = response.get("selected_option", "")
            correct = next((o for o in step.get("options", []) if o.get("correct")), None)
            passed = bool(selected) and (correct and selected == correct.get("id") or not correct)
            return StepResult(
                passed=passed,
                score=100.0 if passed else 0.0,
                message=step.get("prompt", "Identify the weakness."),
            )

        if step_name in ("build", "transfer"):
            try:
                from app.services.behavioral_engine import BehavioralEngine
                engine = BehavioralEngine()
            except ImportError:
                engine = None

            if engine:
                try:
                    import asyncio
                    loop = asyncio.get_event_loop()
                    question = step.get("prompt", "") or response.get("question", "")
                    if loop.is_running():
                        result = asyncio.ensure_future(
                            engine.evaluate_star_strict(
                                question=question,
                                answer=answer_text,
                                company=self._company,
                            )
                        )
                        result = None
                    else:
                        result = loop.run_until_complete(
                            engine.evaluate_star_strict(
                                question=question,
                                answer=answer_text,
                                company=self._company,
                            )
                        )
                    if result:
                        score = float(result.get("overall_score", 50))
                        passed = score >= 75
                        return StepResult(
                            passed=passed,
                            score=score,
                            message=f"STAR score: {score:.1f}/100",
                            feedback=result,
                        )
                except Exception:
                    pass

            guidelines = step.get("guidelines") or []
            star_keywords = {
                "situation": ["when", "during", "at", "while", "background"],
                "task": ["responsible", "tasked", "needed", "goal", "role", "on-call"],
                "action": ["i built", "i created", "i implemented", "i designed", "i led", "i identified", "i rolled back", "i fixed", "i resolved", "i optimized"],
                "result": ["increased", "reduced", "improved", "saved", "achieved", "delivered", "%", "downtime", "faster"],
            }
            scores = {}
            for component, keywords in star_keywords.items():
                count = sum(1 for kw in keywords if kw in answer_text.lower())
                scores[component] = min(100, count * 30)
            if guidelines:
                guideline_hits = sum(1 for g in guidelines if g.lower() in answer_text.lower())
                scores["guidelines"] = min(100, guideline_hits * 25)
            avg = sum(scores.values()) / len(scores) if scores else 0
            passed = avg >= 60
            return StepResult(
                passed=passed,
                score=avg,
                message=f"Heuristic STAR score: {avg:.1f}/100",
                feedback={"star_breakdown": scores, "mode": "heuristic", "guidelines": guidelines},
            )

        if step_name == "break_step":
            selected = response.get("selected_issue", "") or answer_text
            issues = step.get("issues", [])
            passed = bool(selected) and (selected in issues or not issues)
            return StepResult(passed=passed, score=100.0 if passed else 0.0, message=step.get("prompt", "Diagnose the answer."))

        if step_name == "debug":
            improved = response.get("improved_answer", "") or answer_text
            guide = step.get("improvement_guide") or step.get("guidelines") or []
            guide_hits = sum(1 for g in guide if g.lower() in improved.lower())
            star_scores = {}
            for component, keywords in {
                "situation": ["when", "during", "at", "while"],
                "task": ["responsible", "tasked", "needed", "goal"],
                "action": ["i built", "i created", "i implemented", "i designed"],
                "result": ["increased", "reduced", "improved", "saved", "%"],
            }.items():
                count = sum(1 for kw in keywords if kw in improved.lower())
                star_scores[component] = min(100, count * 30)
            if guide:
                star_scores["guide"] = min(100, guide_hits * 25)
            avg = sum(star_scores.values()) / len(star_scores) if star_scores else 0
            passed = avg >= 60
            return StepResult(
                passed=passed,
                score=avg,
                message=f"Improved answer score: {avg:.1f}/100",
                feedback={"star_breakdown": star_scores, "guide_hits": guide_hits},
            )

        if step_name == "retrieval":
            expected = step.get("answer", "") or "Situation, Task, Action, Result"
            passed = expected.lower() in answer_text.lower() or len(answer_text.split()) >= 3
            return StepResult(
                passed=passed,
                score=100.0 if passed else 0.0,
                message=step.get("prompt", "Recall the 4 STAR components."),
            )

        return StepResult(passed=False, score=0, message="Unknown step type")


# ═══════════════════════════════════════════════════════════════
# System Design adapter
# ═══════════════════════════════════════════════════════════════

class SystemDesignAdapter(DomainAdapter):
    domain = "system_design"

    def __init__(self, level_or_context=None, user_id: str = "", company: str = "", role: str = ""):
        super().__init__(level_or_context, user_id)
        self._company = company or getattr(level_or_context, "company", "") or "general"
        self._role = role or getattr(level_or_context, "role", "") or "sde"
        self._question_bank: Dict[str, Any] = {}

    def _step_content(self, step_name: str) -> Dict[str, Any]:
        lesson = self._authored_content()
        steps = lesson.get("steps") or {}
        step = steps.get(step_name)
        if step is None:
            raise ContentNotFoundError(
                f"Authored lesson missing step={step_name!r} for slug={self._concept()!r}"
            )
        return step

    def _interaction_kind(self, step_name: str) -> str:
        kinds = {
            "discover": "read_requirements",
            "understand": "read_explanation",
            "manipulate": "mcq_match",
            "predict": "mcq_bottleneck",
            "build": "guided_design",
            "break_step": "mcq_failure_point",
            "debug": "guided_improvement",
            "retrieval": "recall_dimensions",
            "transfer": "full_design",
        }
        return kinds.get(step_name, "text_input")

    def render_step(self, step_index: int, step_name: str) -> Dict[str, Any]:
        step_name = step_name or self._step_names()[step_index]
        try:
            content = self._step_content(step_name)
        except ContentNotFoundError:
            content = {}
        return {
            "step_index": step_index,
            "step_name": step_name,
            "domain": self.domain,
            "company": self._company,
            "role": self._role,
            "concept": self._concept(),
            "content": content,
            "interaction_kind": self._interaction_kind(step_name),
            "mastery_threshold": 70,
        }

    def mastery_check(self) -> Dict[str, Any]:
        try:
            transfer = self._step_content("transfer")
            return {
                "step_name": "transfer",
                "threshold": 70,
                "prompt": transfer.get("prompt", "Deliver a complete system design."),
                "requirements": transfer.get("requirements", []),
            }
        except ContentNotFoundError:
            return {
                "step_name": "transfer",
                "threshold": 70,
                "prompt": "Deliver a complete system design with requirements, components, trade-offs, and bottleneck analysis.",
            }

    async def grade(self, step_name: str, response: Dict[str, Any]) -> StepResult:
        answer_text = response.get("answer", "") or response.get("text", "") or ""
        diagram = response.get("diagram_description", "") or ""
        combined = f"{answer_text}\n{diagram}".strip()

        try:
            step = self._step_content(step_name)
        except ContentNotFoundError:
            step = {}

        if step_name in ("discover", "understand"):
            return StepResult(passed=True, score=100.0, message=step.get("prompt", "Study the content."))

        if step_name == "manipulate":
            matches = response.get("matches", {})
            correct_count = sum(1 for v in matches.values() if v == "correct")
            total = len(matches) if matches else 1
            score = (correct_count / total) * 100
            passed = score >= 60
            return StepResult(passed=passed, score=score, message=step.get("prompt", f"Matched {correct_count}/{total} components."))

        if step_name == "predict":
            selected = response.get("selected_option", "")
            correct = next((o for o in step.get("options", []) if o.get("correct")), None)
            passed = bool(selected) and (correct and selected == correct.get("id") or not correct)
            return StepResult(passed=passed, score=100.0 if passed else 0.0, message=step.get("prompt", "Identify the bottleneck."))

        if step_name in ("build", "transfer"):
            rubric_result = self._llm_grade(step_name, response, step)
            if rubric_result:
                score = float(rubric_result.get("score", 5))
                passed = score >= 7
                return StepResult(
                    passed=passed,
                    score=score * 10,
                    message=rubric_result.get("ideal_design", ""),
                    feedback=rubric_result,
                )

            dimensions = step.get("key_dimensions") or [
                "scalability", "availability", "consistency", "latency", "caching",
                "load balancer", "database", "redundancy", "sharding", "redis",
                "monitoring", "queue", "partition", "replicate"
            ]
            mentioned = sum(1 for d in dimensions if d in combined.lower())
            score = min(100, mentioned * 15)
            passed = score >= 60
            return StepResult(
                passed=passed,
                score=score,
                message=step.get("prompt", f"Mentioned {mentioned}/{len(dimensions)} key dimensions."),
                feedback={"mode": "heuristic", "dimensions_mentioned": mentioned},
            )

        if step_name == "break_step":
            selected = response.get("selected_failure", "") or answer_text
            failure_points = step.get("failure_points", [])
            passed = bool(selected) and (selected in failure_points or not failure_points)
            return StepResult(passed=passed, score=100.0 if passed else 0.0, message=step.get("prompt", "Identify the failure point."))

        if step_name == "debug":
            fixes = response.get("fixes_applied", [])
            required = step.get("fixes_required") or ["load balancer", "redis", "shard", "cdn", "monitoring"]
            matched = sum(1 for r in required if any(r in f.lower() for f in fixes))
            score = (matched / len(required)) * 100
            passed = score >= 60
            return StepResult(
                passed=passed,
                score=score,
                message=step.get("prompt", f"Applied {matched}/{len(required)} critical fixes."),
            )

        if step_name == "retrieval":
            expected_terms = step.get("key_dimensions") or ["scalability", "availability", "consistency", "latency", "cost"]
            mentioned = sum(1 for t in expected_terms if t in answer_text.lower())
            score = min(100, mentioned * 20)
            passed = score >= 60
            return StepResult(
                passed=passed,
                score=score,
                message=step.get("prompt", f"Recalled {mentioned}/{len(expected_terms)} dimensions."),
            )

        return StepResult(passed=False, score=0, message="Unknown step type")

    def _llm_grade(self, step_name: str, response: Dict[str, Any], step: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        try:
            from app.services.ai_system_design import evaluate_system_design_answer
            import asyncio
            if step is None:
                step = self._step_content("transfer")
            question = response.get("question", "") or step.get("prompt", "") or step.get("question", "")
            answer = response.get("answer", "") or response.get("text", "")
            diagram = response.get("diagram_description", "")
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    return None
                result = loop.run_until_complete(
                    evaluate_system_design_answer(question, answer, diagram)
                )
                return result
            except RuntimeError:
                return None
        except Exception:
            return None


# ═══════════════════════════════════════════════════════════════
# Aptitude adapter
# ═══════════════════════════════════════════════════════════════

class AptitudeAdapter(DomainAdapter):
    domain = "aptitude"

    def __init__(self, level_or_context=None, user_id: str = "", company: str = "", role: str = ""):
        super().__init__(level_or_context, user_id)
        self._company = company or getattr(level_or_context, "company", "") or "general"
        self._role = role or getattr(level_or_context, "role", "") or "sde"
        self._topic = getattr(level_or_context, "topic", "") or ""

    def _step_content(self, step_name: str) -> Dict[str, Any]:
        lesson = self._authored_content()
        steps = lesson.get("steps") or {}
        step = steps.get(step_name)
        if step is None:
            raise ContentNotFoundError(
                f"Authored lesson missing step={step_name!r} for slug={self._concept()!r}"
            )
        return step

    def _interaction_kind(self, step_name: str) -> str:
        kinds = {
            "discover": "mcq_read",
            "understand": "read_explanation",
            "manipulate": "numeric_input",
            "predict": "numeric_input",
            "build": "word_problem",
            "break_step": "mcq_diagnose",
            "debug": "formula_fix",
            "retrieval": "recall_formula",
            "transfer": "word_problem",
        }
        return kinds.get(step_name, "text_input")

    def render_step(self, step_index: int, step_name: str) -> Dict[str, Any]:
        step_name = step_name or self._step_names()[step_index]
        try:
            content = self._step_content(step_name)
        except ContentNotFoundError:
            content = {}
        return {
            "step_index": step_index,
            "step_name": step_name,
            "domain": self.domain,
            "topic": self._topic,
            "company": self._company,
            "role": self._role,
            "concept": self._concept(),
            "content": content,
            "interaction_kind": self._interaction_kind(step_name),
            "mastery_threshold": 70,
        }

    def mastery_check(self) -> Dict[str, Any]:
        try:
            transfer = self._step_content("transfer")
            return {
                "step_name": "transfer",
                "threshold": 70,
                "prompt": transfer.get("prompt", "Solve a new problem in a different context."),
                "answer": transfer.get("answer", ""),
                "explanation": transfer.get("explanation", ""),
            }
        except ContentNotFoundError:
            return {
                "step_name": "transfer",
                "threshold": 70,
                "prompt": "Solve a new problem in a different context.",
            }

    async def grade(self, step_name: str, response: Dict[str, Any]) -> StepResult:
        answer_text = response.get("answer", "") or response.get("text", "") or ""
        selected_option = response.get("selected_option", "")

        try:
            step = self._step_content(step_name)
        except ContentNotFoundError:
            step = {}

        if step_name in ("discover", "understand"):
            return StepResult(passed=True, score=100.0, message=step.get("prompt", "Study the content."))

        if step_name == "build":
            expected = step.get("answer") or step.get("correct_answer") or ""
            if expected:
                passed = self._match_numeric_or_text(answer_text, expected)
                return StepResult(
                    passed=passed,
                    score=100.0 if passed else 0.0,
                    message=step.get("explanation", f"Expected: {expected}"),
                )
            return StepResult(passed=True, score=100.0, message="Build complete.")

        if step_name in ("manipulate", "predict", "transfer"):
            expected = step.get("answer") or step.get("correct_answer") or ""
            if expected:
                passed = self._match_numeric_or_text(answer_text, expected)
                return StepResult(
                    passed=passed,
                    score=100.0 if passed else 0.0,
                    message=step.get("explanation", f"Expected: {expected}"),
                )

        if step_name == "break_step":
            selected = response.get("selected_failure", "") or answer_text
            correct_reasoning = step.get("correct_reasoning", "")
            common_mistake = step.get("common_mistake", "")
            passed = bool(selected) and (correct_reasoning.lower() in selected.lower() or common_mistake.lower() in selected.lower() or not correct_reasoning)
            return StepResult(passed=passed, score=100.0 if passed else 0.0, message=step.get("prompt", "Identify the mistake."))

        if step_name == "debug":
            fixed = answer_text.strip()
            correct_formula = step.get("correct_formula", "")
            passed = bool(correct_formula) and correct_formula.lower() in fixed.lower() or "subtract" in fixed.lower()
            return StepResult(passed=passed, score=100.0 if passed else 0.0, message=step.get("prompt", "Fix the formula."))

        if step_name == "retrieval":
            expected = step.get("answer", "") or "y × (x/100)"
            alternatives = step.get("alternative", [])
            passed = any(alt.lower() in answer_text.lower() for alt in [expected] + alternatives) or len(answer_text.split()) >= 3
            return StepResult(
                passed=passed,
                score=100.0 if passed else 0.0,
                message=step.get("prompt", f"Expected formula: {expected}"),
            )

        return StepResult(passed=False, score=0, message="Unknown step type")

    @staticmethod
    def _match_numeric_or_text(answer_text: str, expected: str) -> bool:
        if not expected:
            return bool(answer_text.strip())
        try:
            expected_num = float(expected)
            import re as _re
            numbers = _re.findall(r"[\d]+(?:\.\d+)?", answer_text)
            if numbers:
                actual_num = float(numbers[-1])
                return abs(expected_num - actual_num) < 0.01
        except (ValueError, TypeError):
            pass
        return expected.lower() in answer_text.lower()


class AuthoredContentAdapter(DomainAdapter):
    """Generic authored-content adapter for domains without specialized grading."""

    domain = ""

    def __init__(self, level_or_context=None, user_id: str = "", company: str = "", role: str = ""):
        super().__init__(level_or_context, user_id)
        self._company = company or getattr(level_or_context, "company", "") or "general"
        self._role = role or getattr(level_or_context, "role", "") or "sde"

    def _step_content(self, step_name: str) -> Dict[str, Any]:
        lesson = self._authored_content()
        steps = lesson.get("steps") or {}
        step = steps.get(step_name)
        if step is None:
            raise ContentNotFoundError(
                f"Authored lesson missing step={step_name!r} for slug={self._concept()!r}"
            )
        return step

    def _interaction_kind(self, step_name: str) -> str:
        return "text_input"

    def render_step(self, step_index: int, step_name: str) -> Dict[str, Any]:
        step_name = step_name or self._step_names()[step_index]
        try:
            content = self._step_content(step_name)
        except ContentNotFoundError:
            content = {}
        return {
            "step_index": step_index,
            "step_name": step_name,
            "domain": self.domain,
            "company": self._company,
            "role": self._role,
            "concept": self._concept(),
            "content": content,
            "interaction_kind": self._interaction_kind(step_name),
            "mastery_threshold": 70,
        }

    def mastery_check(self) -> Dict[str, Any]:
        try:
            transfer = self._step_content("transfer")
            return {
                "step_name": "transfer",
                "threshold": 70,
                "prompt": transfer.get("prompt", "Complete the transfer step."),
            }
        except ContentNotFoundError:
            return {
                "step_name": "transfer",
                "threshold": 70,
                "prompt": "Complete the transfer step.",
            }

    async def grade(self, step_name: str, response: Dict[str, Any]) -> StepResult:
        answer_text = response.get("answer", "") or response.get("text", "") or ""
        if step_name in ("discover", "understand"):
            return StepResult(passed=True, score=100.0, message="Study the content.")

        try:
            step = self._step_content(step_name)
        except ContentNotFoundError:
            return StepResult(passed=False, score=0, message="No authored content for this step.")

        expected = step.get("answer") or step.get("correct_answer") or ""
        if not expected:
            return StepResult(passed=bool(answer_text.strip()), score=50.0, message="Response recorded.")

        passed = expected.lower() in answer_text.lower()
        return StepResult(
            passed=passed,
            score=100.0 if passed else 0.0,
            message=step.get("explanation") or step.get("prompt", f"Expected: {expected}"),
        )


class ReasoningAdapter(AuthoredContentAdapter):
    domain = "reasoning"


class VerbalAdapter(AuthoredContentAdapter):
    domain = "verbal"


class SqlAdapter(AuthoredContentAdapter):
    domain = "sql"


class CsCoreAdapter(AuthoredContentAdapter):
    domain = "cs_core"
