"""PostgreSQL-based Learning service — replaces Motor-based learning event persistence.

Mirrors study_engine.record_activity but uses SQLAlchemy async repositories.
All writes go through repositories; transaction boundaries are owned by the
caller (service layer). Falls back gracefully if AsyncSession is not provided.

Dual-database safety: never silently falls back to Motor for PostgreSQL-owned
operations. If PostgreSQL is unavailable, raises an explicit error.
"""

from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4
import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSession as AsyncSessionType
from app.repositories.learning import (
    LearningAttemptRepository,
    LearningEvidenceRepository,
    LearnerSkillStateRepository,
    ReviewCardRepository,
    RepairMissionRepository,
    RemediationAttemptRepository,
    SkillRepository,
)
from app.repositories.gamification import (
    GamificationProfileRepository,
    XPEventLedgerRepository,
)
from app.repositories.identity import UserRepository
from app.models.learning import (
    LearningAttempt,
    LearningEvidence,
    LearnerSkillState,
    ReviewCard,
    RepairMission,
    RemediationAttempt,
)
from app.models.identity import User

logger = logging.getLogger(__name__)


class PostgresLearningService:
    """PostgreSQL-backed learning service.

    Provides the canonical learning event persistence flow:
      1. Idempotency check (by idempotency_key)
      2. Create learning attempt
      3. Create learning evidence
      4. Update learner skill state (mastery)
      5. Update SRS review card
      6. Open repair mission on failure
      7. Award XP via gamification (single writer)

    All operations use the injected AsyncSession. No Motor fallback.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.attempt_repo = LearningAttemptRepository(session)
        self.evidence_repo = LearningEvidenceRepository(session)
        self.skill_state_repo = LearnerSkillStateRepository(session)
        self.review_card_repo = ReviewCardRepository(session)
        self.repair_repo = RepairMissionRepository(session)
        self.remediation_repo = RemediationAttemptRepository(session)
        self.skill_repo = SkillRepository(session)
        self.gamification_repo = GamificationProfileRepository(session)
        self.xp_ledger_repo = XPEventLedgerRepository(session)
        self.user_repo = UserRepository(session)

    # ══════════════════════════════════════════════════════════════════════════════
    # RECORD ACTIVITY — canonical learning event persistence
    # ══════════════════════════════════════════════════════════════════════════════

    async def record_activity(
        self,
        user_id: UUID,
        activity_type: str,
        score: float,
        activity_data: Dict[str, Any],
        award_reward: bool = True,
    ) -> Dict[str, Any]:
        """Record a learning activity with full fan-out.

        Mirrors study_engine.record_activity but uses PostgreSQL repositories.
        All writes are in a single transaction managed by the caller.

        Args:
            user_id: PostgreSQL UUID of the user.
            activity_type: learn | review | practice | challenge | repair | retest | ...
            score: 0-10 pedagogical score.
            activity_data: Additional activity context (skill_id, question_id,
                passed, time_spent_seconds, hints_used, attempt_number,
                idempotency_key, diagnosis_codes, etc.).
            award_reward: Whether to award XP/diamonds via gamification.

        Returns:
            Dict with recorded, activity_type, skill_id, passed, score,
            diamonds, mastery_before, mastery_after, diagnosis_codes,
            repair_id, event_id.
        """
        # Normalize score to 0-10 scale
        try:
            score = float(score)
        except (TypeError, ValueError):
            score = 0.0
        if score > 10:
            score /= 10.0
        score = max(0.0, min(score, 10.0))

        passed = bool(activity_data.get("passed", False))
        time_spent = int(activity_data.get("time_spent_seconds", 0))
        diagnosis_codes = list(activity_data.get("diagnosis_codes", []))
        idempotency_key = activity_data.get("idempotency_key")
        skill_id_str = activity_data.get("skill_id")
        question_id = activity_data.get("question_id")
        source = activity_data.get("source", "postgres_learning_engine")
        role = activity_data.get("role")
        company = activity_data.get("company")
        hints_used = int(activity_data.get("hints_used", 0))
        attempt_number = int(activity_data.get("attempt_number", 1))

        # ── Resolve skill_id to UUID if provided ──
        skill_uuid = None
        skill_exists = False
        if skill_id_str:
            try:
                parsed_uuid = UUID(str(skill_id_str))
                skill = await self.skill_repo.get_by_id(parsed_uuid)
                if skill:
                    skill_uuid = parsed_uuid
                    skill_exists = True
                else:
                    # UUID format valid but skill not in DB
                    skill_uuid = None
            except (ValueError, AttributeError):
                # Try to find by name
                skill = await self.skill_repo.get_by_name(str(skill_id_str))
                if skill:
                    skill_uuid = skill.id
                    skill_exists = True

        # ── Idempotency ──
        if idempotency_key:
            prior = await self.attempt_repo.get_by_user_and_question(user_id, question_id or "")
            if prior:
                # Check if any prior attempt matches the idempotency key in metadata
                for attempt in prior:
                    attempt_meta = attempt.attempt_metadata or {}
                    if attempt_meta.get("idempotency_key") == idempotency_key:
                        logger.info("Idempotent replay detected for %s", user_id)
                        return {
                            "recorded": False,
                            "deduplicated": True,
                            "activity_type": attempt.activity_type,
                            "skill_id": str(attempt.skill_id) if attempt.skill_id else None,
                            "passed": attempt.passed,
                            "score": float(attempt.score),
                            "diamonds": 0,
                            "xp_awarded": 0,
                            "xp": 0,
                            "xp_applied": False,
                            "mastery_before": None,
                            "mastery_after": None,
                            "diagnosis_codes": [],
                            "repair_id": None,
                            "event_id": str(attempt.id),
                        }

        # ── Failure → diagnosis + repair mission ──
        repair_id = None
        if not passed and skill_uuid:
            if not diagnosis_codes:
                # Auto-diagnose (best-effort)
                try:
                    from app.services.diagnosis import diagnose_question_failure
                    diag = diagnose_question_failure(
                        score, "", "mcq", {},
                        metadata={
                            "all_passed": False,
                            "passed_count": 0,
                            "total": 1,
                            "time_spent": time_spent,
                            "hints_used": hints_used,
                        },
                    )
                    if isinstance(diag, dict):
                        diagnosis_codes = diag.get("codes", []) or diagnosis_codes
                except Exception as exc:
                    logger.warning("Auto-diagnosis failed for %s: %s", user_id, exc)

            # Open repair mission (best-effort)
            try:
                existing_mission = await self.repair_repo.get_open_by_user_and_skill(user_id, skill_uuid)
                if not existing_mission:
                    mission = await self.repair_repo.create({
                        "user_id": user_id,
                        "skill_id": skill_uuid,
                        "title": f"Repair: {skill_id_str}",
                        "description": "Auto-generated repair mission from failed activity",
                        "status": "open",
                        "tier": "repair",
                        "estimated_minutes": 15,
                    })
                    repair_id = mission.id
            except Exception as exc:
                logger.warning("Auto-repair mission failed for %s: %s", user_id, exc)

        # ── Mastery update ──
        mastery_before = None
        mastery_after = None
        if skill_exists:
            try:
                existing_state = await self.skill_state_repo.get_by_user_and_skill(user_id, skill_uuid)
                mastery_before = existing_state.score if existing_state else None

                # Simple mastery update: weighted average of new score
                new_score = score if existing_state is None else (
                    (existing_state.score * existing_state.total_attempts + score) /
                    (existing_state.total_attempts + 1)
                )
                new_score = round(new_score, 1)

                if new_score >= 80:
                    mastery_level = "master"
                elif new_score >= 70:
                    mastery_level = "advanced"
                elif new_score >= 50:
                    mastery_level = "intermediate"
                else:
                    mastery_level = "beginner"

                await self.skill_state_repo.create_or_update(
                    user_id=user_id,
                    skill_id=skill_uuid,
                    score=new_score,
                    mastery_level=mastery_level,
                    total_attempts=(existing_state.total_attempts + 1 if existing_state else 1),
                )
                mastery_after = new_score

                # Record mastery snapshot
                from app.repositories.learning import MasterySnapshotRepository
                snapshot_repo = MasterySnapshotRepository(self.session)
                await snapshot_repo.create({
                    "user_id": user_id,
                    "skill_id": skill_uuid,
                    "mastery_level": mastery_level,
                    "evidence_count": (existing_state.total_attempts + 1 if existing_state else 1),
                    "score_at_snapshot": new_score,
                })
            except Exception as exc:
                logger.warning("Mastery update failed for %s: %s", user_id, exc)

        # ── SRS card update ──
        if skill_exists or activity_data.get("competency_id"):
            try:
                from app.services.spaced_repetition import (
                    SpacedRepetitionEngine,
                    ReviewGrade,
                )
                prob_id = str(skill_uuid) if skill_uuid else activity_data.get("competency_id", "")
                if prob_id:
                    existing_card = await self.review_card_repo.get_by_user_and_problem(user_id, prob_id)
                    engine = SpacedRepetitionEngine()
                    grade = ReviewGrade.GOOD if passed else ReviewGrade.AGAIN
                    if existing_card:
                        # Deserialize existing card state
                        state = engine.create_new_card(concept_id=prob_id, user_id=str(user_id))
                        state.interval = existing_card.interval
                        state.repetitions = existing_card.repetitions
                        state.ease_factor = existing_card.ease_factor
                        state.next_review = existing_card.next_review
                    else:
                        state = engine.create_new_card(concept_id=prob_id, user_id=str(user_id))
                    state = engine.review(state, grade)
                    await self.review_card_repo.create_or_update(
                        user_id=user_id,
                        problem_id=prob_id,
                        next_review=state.next_review,
                        difficulty=state.difficulty if hasattr(state, 'difficulty') else "medium",
                        interval=state.interval,
                        repetitions=state.repetitions,
                        ease_factor=int(state.ease_factor * 100),
                    )
            except Exception as exc:
                logger.warning("SRS update skipped for %s: %s", user_id, exc)

        # ── Gamification / XP ──
        diamonds = 0
        xp_awarded = 0
        if award_reward:
            try:
                from app.services.postgres_gamification import record_practice as pg_record_practice
                prac_result = await pg_record_practice(
                    self.session,
                    str(user_id),
                    activity_type=activity_type,
                    score=score,
                    metadata={
                        "skill_id": skill_id_str,
                        "time_spent": time_spent,
                        "passed": passed,
                        "question_id": question_id,
                        "source": source,
                    },
                    role=role or "sde",
                )
                if isinstance(prac_result, dict):
                    xp_awarded = int(prac_result.get("xp_gained", 0) or 0)
                    diamonds = xp_awarded
            except Exception as exc:
                logger.warning("Gamification record failed for %s: %s", user_id, exc)

        # ── Persist learning attempt ──
        # evidence_type = assistance dimension (independent vs assisted hints)
        # passed = correctness dimension (separate field)
        evidence_type = "assisted" if hints_used > 0 else "independent"
        try:
            attempt = await self.attempt_repo.create({
                "user_id": user_id,
                "skill_id": skill_uuid,
                "question_id": question_id or "",
                "activity_type": activity_type,
                "score": int(score),
                "evidence_type": evidence_type,
                "passing_score": 7,
                "max_attempts": 3,
                "attempt_number": attempt_number,
                "passed": passed,
                "idempotency_key": idempotency_key,
                "attempt_metadata": {
                    "idempotency_key": idempotency_key,
                    "source": source,
                    "role": role,
                    "company": company,
                    "trust_status": activity_data.get("trust_status"),
                    "verification_version": activity_data.get("verification_version"),
                    "source_bank": activity_data.get("source_bank"),
                },
            })
        except IntegrityError:
            # Database-enforced idempotency: duplicate (user_id, idempotency_key)
            await self.session.rollback()
            logger.info("DB idempotency replay detected for %s", user_id)
            return {
                "recorded": False,
                "deduplicated": True,
                "activity_type": activity_type,
                "skill_id": skill_id_str,
                "passed": passed,
                "score": score,
                "diamonds": 0,
                "xp_awarded": 0,
                "xp": 0,
                "xp_applied": False,
                "mastery_before": None,
                "mastery_after": None,
                "diagnosis_codes": [],
                "repair_id": None,
                "event_id": None,
            }

        # ── Persist learning evidence ──
        # evidence_type = assistance dimension (independent vs assisted hints)
        # passed = correctness dimension (separate field on attempt)
        # These are distinct dimensions: a correct answer with hints is
        # "assisted success", not failure.
        evidence_type = "assisted" if hints_used > 0 else "independent"
        evidence = await self.evidence_repo.create({
            "attempt_id": attempt.id,
            "user_id": user_id,
            "skill_id": skill_uuid,
            "evidence_data": {
                "passed": passed,
                "score": score,
                "time_spent_seconds": time_spent,
                "hints_used": hints_used,
                "attempt_number": attempt_number,
                "diagnosis_codes": diagnosis_codes,
                "repair_id": str(repair_id) if repair_id else None,
                "question_id": question_id,
            },
            "evidence_type": evidence_type,
        })

        return {
            "recorded": True,
            "deduplicated": False,
            "activity_type": activity_type,
            "skill_id": skill_id_str,
            "passed": passed,
            "score": score,
            "diamonds": diamonds,
            "xp_awarded": xp_awarded,
            "xp_applied": award_reward,
            "mastery_before": mastery_before,
            "mastery_after": mastery_after,
            "diagnosis_codes": diagnosis_codes,
            "repair_id": str(repair_id) if repair_id else None,
            "event_id": str(attempt.id),
        }

    # ══════════════════════════════════════════════════════════════════════════════
    # DUE REVIEWS — SRS cards due now
    # ══════════════════════════════════════════════════════════════════════════════

    async def get_due_reviews(self, user_id: UUID, limit: int = 5) -> List[Dict[str, Any]]:
        """Get due spaced-repetition cards for a user."""
        cards = await self.review_card_repo.get_due_cards(user_id, limit=limit)
        return [
            {
                "id": str(card.id),
                "problem_id": card.problem_id,
                "difficulty": card.difficulty,
                "interval": card.interval,
                "repetitions": card.repetitions,
                "next_review": card.next_review.isoformat() if card.next_review else None,
                "ease_factor": card.ease_factor / 1000.0,
            }
            for card in cards
        ]

    # ══════════════════════════════════════════════════════════════════════════════
    # WEAK SKILLS — for practice task generation
    # ══════════════════════════════════════════════════════════════════════════════

    async def get_weak_skills(self, user_id: UUID, threshold: float = 70.0) -> List[Dict[str, Any]]:
        """Get skills below threshold for practice task generation."""
        states = await self.skill_state_repo.get_weak_skills(user_id, threshold)
        return [
            {
                "skill_id": str(state.skill_id),
                "score": state.score,
                "mastery_level": state.mastery_level,
                "total_attempts": state.total_attempts,
            }
            for state in states
        ]

    # ══════════════════════════════════════════════════════════════════════════════
    # EMIT LEARNING EVENT — lightweight event without full fan-out
    # ══════════════════════════════════════════════════════════════════════════════

    async def emit_learning_event(
        self,
        user_id: UUID,
        activity_type: str,
        score: float,
        passed: bool,
        activity_data: Dict[str, Any],
    ) -> Optional[UUID]:
        """Persist a learning event without the full mastery/SRS/gamification fan-out.

        Used by OA, interview, question submission routes that produce
        evidence but don't need the full recalculation.
        """
        try:
            skill_id_str = activity_data.get("skill_id")
            skill_uuid = None
            if skill_id_str:
                try:
                    skill_uuid = UUID(str(skill_id_str))
                except (ValueError, AttributeError):
                    skill = await self.skill_repo.get_by_name(str(skill_id_str))
                    if skill:
                        skill_uuid = skill.id

            attempt = await self.attempt_repo.create({
                "user_id": user_id,
                "skill_id": skill_uuid,
                "question_id": activity_data.get("question_id", ""),
                "activity_type": activity_type,
                "score": int(score),
                "evidence_type": "assisted" if activity_data.get("hints_used", 0) > 0 else "independent",
                "passed": passed,
                "idempotency_key": activity_data.get("idempotency_key"),
                "attempt_metadata": activity_data.get("metadata", {}),
            })

            await self.evidence_repo.create({
                "attempt_id": attempt.id,
                "user_id": user_id,
                "skill_id": skill_uuid,
                "evidence_data": {
                    "passed": passed,
                    "score": score,
                    "time_spent_seconds": activity_data.get("time_spent_seconds", 0),
                    "hints_used": activity_data.get("hints_used", 0),
                    "attempt_number": activity_data.get("attempt_number", 1),
                },
                "evidence_type": "assisted" if activity_data.get("hints_used", 0) > 0 else "independent",
            })

            return attempt.id
        except Exception as exc:
            logger.error("emit_learning_event failed for %s: %s", user_id, exc)
            return None
