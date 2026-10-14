"""Lesson Orchestrator — thin coordinator over canonical learning systems.

This module must NOT own:
  - mastery model
  - SRS engine
  - reward ledger
  - question bank
  - lesson definitions
  - progression graph

It owns only:
  - session flow coordination
  - routing responses to the correct canonical system
  - assembling the frontend payload from canonical system outputs

Canonical systems it delegates to:
  - LessonService             — coding content, execution, grading
  - record_practice()         — gamification, diamonds, XP, streak
  - SpacedRepetitionEngine    — SRS enrollment
  - update_skill_score()      — mastery/skill tracking
  - create_repair_mission()   — closed-loop repair
  - log_interaction_action()  — action trace logging
  - diagnose_misconception()  — misconception detection
  - tutor_act()               — AI tutor hints
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.services.domain_adapters import (
    AptitudeAdapter,
    BehavioralAdapter,
    CodingAdapter,
    DomainAdapter,
    SystemDesignAdapter,
)
from app.services.domain_misconceptions import get_domain_library
from app.services.action_trace_logger import log_interaction_action
from app.services.repair_service import create_repair_mission
from app.services.ai_tutor import tutor_act
from app.services.gamification import record_practice
from app.services.spaced_repetition import SpacedRepetitionEngine
from app.services.skill_assessment import update_skill_score
from app.services.misconception_diagnosis import diagnose_misconception

logger = logging.getLogger(__name__)

# Canonical 9-step vocabulary — shared with frontend and content
STEP_NAMES = [
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

RETEACH_CONFIDENCE_THRESHOLD = 0.7
MIN_EVIDENCE_COUNT = 2  # Need at least 2 wrong answers before reteach triggers


# ═══════════════════════════════════════════════════════════════
# Session — lightweight coordinator state, NOT a source of truth
# ═══════════════════════════════════════════════════════════════

class LessonSession:
    """Minimal session state for coordinating one lesson playthrough.

    This is NOT the student's mastery record, SRS state, or ledger.
    It is transient coordination state only.
    """

    def __init__(
        self,
        session_id: str,
        user_id: str,
        domain: str,
        level_or_context: Any,
        mastery_threshold: int = 80,
        company: str = "",
        role: str = "",
    ):
        self.session_id = session_id
        self.user_id = user_id
        self.domain = domain
        self.level_or_context = level_or_context
        self.mastery_threshold = mastery_threshold
        self.company = company
        self.role = role

        self.adapter: DomainAdapter = _make_adapter(
            domain, level_or_context, user_id, company, role
        )
        self.current_step = 0
        self.step_results: List[Dict[str, Any]] = []
        self.reteach_pending: Optional[Dict[str, Any]] = None
        self.misconception_codes: List[str] = self.adapter.misconception_codes(
            self.adapter._concept()
        )
        self.mastery_unlocked = False
        self.completed = False
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.updated_at = self.created_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "domain": self.domain,
            "current_step": self.current_step,
            "total_steps": len(STEP_NAMES),
            "step_results": self.step_results,
            "reteach_pending": self.reteach_pending,
            "mastery_unlocked": self.mastery_unlocked,
            "completed": self.completed,
            "mastery_threshold": self.mastery_threshold,
            "company": self.company,
            "role": self.role,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


# ═══════════════════════════════════════════════════════════════
# Orchestrator — thin coordinator
# ═══════════════════════════════════════════════════════════════

class LessonOrchestrator:
    """Coordinates a lesson session by delegating to canonical systems.

    Owns: session sequencing, step routing, payload assembly.
    Delegates: grading → domain adapter, rewards → record_practice(),
               SRS → SpacedRepetitionEngine, mastery → update_skill_score(),
               repair → create_repair_mission(), traces → log_interaction_action(),
               diagnosis → diagnose_misconception(), hints → tutor_act().
    """

    def __init__(self):
        self._sessions: Dict[str, LessonSession] = {}
        self._srs = SpacedRepetitionEngine()

    async def start(
        self,
        user_id: str,
        domain: str,
        level_or_context: Any = None,
        company: str = "",
        role: str = "",
        mastery_threshold: int = 80,
    ) -> Dict[str, Any]:
        session_id = f"lesson:{domain}:{uuid.uuid4().hex[:12]}"
        session = LessonSession(
            session_id=session_id,
            user_id=user_id,
            domain=domain,
            level_or_context=level_or_context,
            mastery_threshold=mastery_threshold,
            company=company,
            role=role,
        )
        self._sessions[session_id] = session

        step_name = STEP_NAMES[0]
        step_payload = session.adapter.render_step(0, step_name)

        return {
            "session_id": session_id,
            "domain": domain,
            "current_step": 0,
            "total_steps": len(STEP_NAMES),
            "step_name": step_name,
            "step": step_payload,
            "diagnosis": None,
            "mastery_threshold": mastery_threshold,
            "company": company,
            "role": role,
        }

    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        session = self._sessions.get(session_id)
        if session is None:
            return None
        return session.to_dict()

    async def submit_step(
        self,
        session_id: str,
        step_index: int,
        response: Dict[str, Any],
        time_spent_seconds: int = 0,
    ) -> Dict[str, Any]:
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError(f"Unknown session: {session_id}")

        if session.completed:
            return {"error": "Session already completed", "session": session.to_dict()}

        if session.reteach_pending:
            return await self._handle_reteach_submit(session, response)

        step_index = max(0, min(step_index, len(STEP_NAMES) - 1))
        step_name = STEP_NAMES[step_index]

        # Grade via domain adapter (adapter delegates to LessonService for coding)
        result = await session.adapter.grade(step_name, response)

        # Record step result in session state (transient only)
        session.step_results.append({
            "step_index": step_index,
            "step_name": step_name,
            "passed": result.passed,
            "score": result.score,
            "message": result.message,
            "evidence": result.evidence,
            "feedback": result.feedback,
            "time_spent_seconds": time_spent_seconds,
        })

        # Log action trace via canonical system
        action_type = f"{step_name}_correct" if result.passed else f"{step_name}_wrong"
        trace = log_interaction_action(
            user_id=session.user_id,
            atom_id=f"{session.domain}:{session.adapter._concept()}:{step_name}",
            session_id=session_id,
            interaction_type=step_name,
            action=action_type,
            data={
                "answer": response.get("code", "") or response.get("answer", "") or "",
                "score": result.score,
                "step_index": step_index,
                "domain": session.domain,
            },
            misconception_codes=session.misconception_codes,
        )

        # Misconception diagnosis via canonical system
        diagnosis = None
        if not result.passed and session.misconception_codes:
            diagnosis = trace if trace and trace.get("misconception_code") else None

        # Reteach trigger — requires BOTH high confidence AND sufficient evidence
        # Wrong once → uncertain. Same behavior repeated → higher confidence. Strong evidence → reteach.
        evidence_count = diagnosis.get("evidence_count", 0) if diagnosis else 0
        if (
            diagnosis
            and diagnosis.get("confidence", 0) >= RETEACH_CONFIDENCE_THRESHOLD
            and evidence_count >= MIN_EVIDENCE_COUNT
        ):
            session.reteach_pending = {
                "misconception_code": diagnosis["misconception_code"],
                "reteach_route": diagnosis.get("reteach_route"),
                "reteach_action": diagnosis.get("reteach_action"),
                "confidence": diagnosis["confidence"],
                "evidence_count": evidence_count,
                "failed_step": step_name,
                "failed_step_index": step_index,
            }
            # Delegate repair mission creation to canonical system
            try:
                await create_repair_mission(
                    user_id=session.user_id,
                    weaknesses=[diagnosis["misconception_code"]],
                    source=f"lesson:{session.domain}",
                )
            except Exception:
                pass

            session.updated_at = datetime.now(timezone.utc).isoformat()
            return {
                "session_id": session_id,
                "passed": False,
                "score": result.score,
                "message": result.message,
                "evidence": result.evidence,
                "feedback": result.feedback,
                "diagnosis": diagnosis,
                "reteach_required": True,
                "reteach": session.reteach_pending,
                "current_step": step_index,
                "session": session.to_dict(),
            }

        # Advance or retry
        session.current_step = step_index + 1 if result.passed else step_index

        # Mastery + rewards — delegate to canonical systems
        mastery_unlocked = False
        reward_summary: Dict[str, Any] = {}

        if step_name == "transfer" and result.passed:
            mastery_unlocked = True
            session.mastery_unlocked = True
            session.completed = True
            session.current_step = len(STEP_NAMES)

            # Delegate reward to canonical gamification system
            try:
                xp_result = await record_practice(
                    user_id=session.user_id,
                    activity_type="lesson",
                    score=result.score / 10,
                    metadata={
                        "domain": session.domain,
                        "concept": session.adapter._concept(),
                        "company": session.company,
                        "role": session.role,
                        "session_id": session_id,
                    },
                    role=session.role or "sde",
                )
                reward_summary = {
                    "diamonds": (xp_result or {}).get("xp_gained", 0),
                    "combo": ((xp_result or {}).get("combo") or {}).get("current", 0),
                    "streak_multiplier": (xp_result or {}).get("streak_multiplier", 1.0),
                    "critical_hit": bool((xp_result or {}).get("critical_hit", False)),
                }
            except Exception:
                pass

            # Delegate SRS enrollment to canonical system
            try:
                concept_id = f"{session.domain}:{session.adapter._concept()}"
                existing = await self._srs.collection.find_one({
                    "user_id": session.user_id,
                    "concept_id": concept_id,
                })
                if not existing:
                    state = self._srs.create_new_card(concept_id, session.user_id)
                    await self._srs.collection.insert_one({
                        "user_id": session.user_id,
                        "concept_id": concept_id,
                        "concept_name": session.adapter._concept(),
                        "interval": state.interval,
                        "repetitions": state.repetitions,
                        "ease_factor": state.ease_factor,
                        "next_review": state.next_review,
                        "last_reviewed": None,
                        "learning_step": state.learning_step,
                        "total_reviews": 0,
                        "lapses": 0,
                        "created_at": state.created_at,
                        "updated_at": state.updated_at,
                    })
            except Exception:
                pass

            # Delegate skill mastery update to canonical system
            try:
                await update_skill_score(
                    session.user_id,
                    session.domain,
                    session.adapter._concept(),
                    result.score,
                    True,
                )
            except Exception:
                pass

        session.updated_at = datetime.now(timezone.utc).isoformat()

        response_payload: Dict[str, Any] = {
            "session_id": session_id,
            "passed": result.passed,
            "score": result.score,
            "message": result.message,
            "evidence": result.evidence,
            "feedback": result.feedback,
            "diagnosis": diagnosis,
            "reteach_required": False,
            "mastery_unlocked": mastery_unlocked,
            "reward": reward_summary,
            "current_step": session.current_step,
            "session": session.to_dict(),
        }

        if not session.completed and session.current_step < len(STEP_NAMES):
            next_step_name = STEP_NAMES[session.current_step]
            response_payload["next_step"] = {
                "step_index": session.current_step,
                "step_name": next_step_name,
                "step": session.adapter.render_step(session.current_step, next_step_name),
            }

        return response_payload

    async def request_hint(self, session_id: str, step_index: int) -> Dict[str, Any]:
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError(f"Unknown session: {session_id}")

        step_name = (
            session.reteach_pending["failed_step"]
            if session.reteach_pending
            else STEP_NAMES[min(step_index, len(STEP_NAMES) - 1)]
        )

        # Delegate hint generation to AI tutor (canonical system)
        try:
            tutor_response = await tutor_act(
                "GUIDE",
                concept_id=f"{session.domain}:{session.adapter._concept()}:{step_name}",
                learner_state={
                    "step": step_name,
                    "domain": session.domain,
                    "attempts": len(session.step_results),
                },
                context={"company": session.company, "role": session.role},
            )
            hint_text = tutor_response.get("prompt", "")
        except Exception:
            hints = getattr(session.level_or_context, "hints", [])
            attempt = len(session.step_results)
            hint_text = (
                hints[min(attempt, len(hints) - 1)]
                if hints
                else "Review the step content and try again."
            )

        return {
            "session_id": session_id,
            "step_index": step_index,
            "step_name": step_name,
            "hint": hint_text,
            "tutor_mode": "GUIDE",
        }

    async def _handle_reteach_submit(
        self, session: LessonSession, response: Dict[str, Any]
    ) -> Dict[str, Any]:
        reteach = session.reteach_pending or {}
        answer_text = response.get("answer", "") or response.get("text", "") or ""

        # Evidence check: student must engage with reteach content
        if len(answer_text.strip()) <= 10:
            return {
                "session_id": session.session_id,
                "passed": False,
                "message": "Please engage with the reteach content before continuing.",
                "reteach_required": True,
                "reteach_pending": reteach,
                "current_step": session.current_step,
                "session": session.to_dict(),
            }

        # Retest: re-grade the failed step to verify understanding
        failed_step_index = reteach.get("failed_step_index", session.current_step)
        failed_step_name = reteach.get("failed_step", STEP_NAMES[min(failed_step_index, len(STEP_NAMES) - 1)])
        
        try:
            retest_result = await session.adapter.grade(failed_step_name, response)
        except Exception:
            retest_result = None

        if retest_result and retest_result.passed:
            # Retest passed — clear reteach and advance
            session.reteach_pending = None
            session.current_step = failed_step_index + 1
            session.updated_at = datetime.now(timezone.utc).isoformat()
            return {
                "session_id": session.session_id,
                "passed": True,
                "message": "Reteach verified. Moving forward.",
                "reteach_required": False,
                "reteach_pending": None,
                "current_step": session.current_step,
                "session": session.to_dict(),
            }

        # Retest failed — keep reteach pending
        return {
            "session_id": session.session_id,
            "passed": False,
            "message": "Not yet. Review the reteach plan and try the step again.",
            "reteach_required": True,
            "reteach_pending": reteach,
            "current_step": session.current_step,
            "session": session.to_dict(),
        }

    async def get_reteach_plan(self, session_id: str) -> Dict[str, Any]:
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError(f"Unknown session: {session_id}")
        if not session.reteach_pending:
            return {"reteach_required": False}

        code = session.reteach_pending.get("misconception_code", "")
        from app.services.domain_misconceptions import get_reteach_plan

        plan = get_reteach_plan(code)

        return {
            "reteach_required": True,
            "misconception_code": code,
            "confidence": session.reteach_pending.get("confidence", 0),
            "reteach_route": session.reteach_pending.get("reteach_route"),
            "reteach_action": session.reteach_pending.get("reteach_action"),
            "plan": plan,
            "failed_step": session.reteach_pending.get("failed_step"),
        }

    def cleanup(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)


# ═══════════════════════════════════════════════════════════════
# Adapter factory
# ═══════════════════════════════════════════════════════════════

def _make_adapter(
    domain: str, level_or_context: Any, user_id: str, company: str, role: str
) -> DomainAdapter:
    if domain == "coding":
        return CodingAdapter(level_or_context, user_id)
    if domain == "behavioral":
        return BehavioralAdapter(level_or_context, user_id, company, role)
    if domain == "system_design":
        return SystemDesignAdapter(level_or_context, user_id, company, role)
    if domain == "aptitude":
        return AptitudeAdapter(level_or_context, user_id, company, role)
    if domain == "reasoning":
        return ReasoningAdapter(level_or_context, user_id, company, role)
    if domain == "verbal":
        return VerbalAdapter(level_or_context, user_id, company, role)
    if domain == "sql":
        return SqlAdapter(level_or_context, user_id, company, role)
    if domain == "cs_core":
        return CsCoreAdapter(level_or_context, user_id, company, role)
    raise ValueError(f"Unsupported domain: {domain}")


# Singleton
_orchestrator: LessonOrchestrator | None = None


def get_orchestrator() -> LessonOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = LessonOrchestrator()
    return _orchestrator
