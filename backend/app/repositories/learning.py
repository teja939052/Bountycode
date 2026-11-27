"""Learning domain repositories — PostgreSQL replacements for Motor collection operations.

Collections migrated:
- skill_graphs -> learner_skill_state
- srs_cards -> review_cards
- learning_events -> learning_attempts + learning_evidence
- repair_missions -> repair_missions + remediation_attempts

Repositories use injected AsyncSession. Transaction boundaries are owned by
the service layer, not the repository.
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any
from uuid import UUID

from sqlalchemy import select, update, delete, func, and_, or_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import RepositoryBase
from app.models.learning import (
    DailyChallengeUser,
    LearningModule,
    UserLearningProgress,
    Skill,
    SkillPrerequisite,
    LearnerSkillState,
    LearningAttempt,
    LearningEvidence,
    MasterySnapshot,
    RemediationAttempt,
    RepairMission,
    ReviewCard,
    Skill,
    SkillPrerequisite,
)
from app.models.identity import User, AcademyDiagnosticSession, AcademyLearningPlan, AcademyLearnerProfile


# ════════════════════════════════════════════════════════════════════════════════
# SKILL REPOSITORY
# ════════════════════════════════════════════════════════════════════════════════

class SkillRepository(RepositoryBase):
    """Repository for canonical skill definitions — replaces content-driven
    skill lookups from MongoDB."""

    async def get_by_id(self, skill_id: UUID) -> Optional[Skill]:
        result = await self.session.execute(select(Skill).where(Skill.id == skill_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Skill]:
        result = await self.session.execute(select(Skill).where(Skill.name == name))
        return result.scalar_one_or_none()

    async def get_by_topic(self, topic: str, difficulty: Optional[str] = None) -> List[Skill]:
        query = select(Skill).where(Skill.topic == topic, Skill.is_active == True)  # noqa: E712
        if difficulty:
            query = query.where(Skill.difficulty == difficulty)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_all_active(self) -> List[Skill]:
        result = await self.session.execute(
            select(Skill).where(Skill.is_active == True)  # noqa: E712
        )
        return result.scalars().all()

    async def create(self, skill_data: dict) -> Skill:
        skill = Skill(**skill_data)
        self.session.add(skill)
        await self.flush()
        return skill


class SkillPrerequisiteRepository(RepositoryBase):
    """Repository for skill prerequisite DAG."""

    async def get_prerequisites(self, skill_id: UUID) -> List[SkillPrerequisite]:
        result = await self.session.execute(
            select(SkillPrerequisite).where(SkillPrerequisite.skill_id == skill_id)
        )
        return result.scalars().all()

    async def get_dependents(self, prerequisite_skill_id: UUID) -> List[SkillPrerequisite]:
        result = await self.session.execute(
            select(SkillPrerequisite).where(SkillPrerequisite.prerequisite_skill_id == prerequisite_skill_id)
        )
        return result.scalars().all()

    async def add_prerequisite(self, skill_id: UUID, prerequisite_skill_id: UUID) -> SkillPrerequisite:
        sp = SkillPrerequisite(skill_id=skill_id, prerequisite_skill_id=prerequisite_skill_id)
        self.session.add(sp)
        await self.flush()
        return sp


# ════════════════════════════════════════════════════════════════════════════════
# LEARNER SKILL STATE REPOSITORY
# ════════════════════════════════════════════════════════════════════════════════

class LearnerSkillStateRepository(RepositoryBase):
    """Repository for per-user-per-skill mastery state — replaces skill_graphs."""

    async def get_by_user_and_skill(self, user_id: UUID, skill_id: UUID) -> Optional[LearnerSkillState]:
        result = await self.session.execute(
            select(LearnerSkillState).where(
                LearnerSkillState.user_id == user_id,
                LearnerSkillState.skill_id == skill_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: UUID) -> List[LearnerSkillState]:
        result = await self.session.execute(
            select(LearnerSkillState).where(LearnerSkillState.user_id == user_id)
        )
        return result.scalars().all()

    async def get_by_user_and_topic(self, user_id: UUID, topic: str) -> List[LearnerSkillState]:
        result = await self.session.execute(
            select(LearnerSkillState)
            .join(Skill, LearnerSkillState.skill_id == Skill.id)
            .where(LearnerSkillState.user_id == user_id, Skill.topic == topic)
        )
        return result.scalars().all()

    async def get_weak_skills(self, user_id: UUID, threshold: float = 70.0) -> List[LearnerSkillState]:
        result = await self.session.execute(
            select(LearnerSkillState)
            .where(LearnerSkillState.user_id == user_id, LearnerSkillState.score < threshold)
        )
        return result.scalars().all()

    async def create_or_update(
        self,
        user_id: UUID,
        skill_id: UUID,
        score: float,
        mastery_level: str,
        total_attempts: int,
    ) -> LearnerSkillState:
        existing = await self.get_by_user_and_skill(user_id, skill_id)
        if existing:
            existing.score = score
            existing.mastery_level = mastery_level
            existing.total_attempts = total_attempts
            existing.last_practiced = datetime.now(timezone.utc)
            await self.flush()
            return existing
        state = LearnerSkillState(
            user_id=user_id,
            skill_id=skill_id,
            score=score,
            mastery_level=mastery_level,
            total_attempts=total_attempts,
            last_practiced=datetime.now(timezone.utc),
        )
        self.session.add(state)
        await self.flush()
        return state


# ════════════════════════════════════════════════════════════════════════════════
# LEARNING ATTEMPT REPOSITORY
# ════════════════════════════════════════════════════════════════════════════════

class LearningAttemptRepository(RepositoryBase):
    """Repository for immutable learning attempt records — replaces learning_events
    insert-only pattern."""

    async def get_by_id(self, attempt_id: UUID) -> Optional[LearningAttempt]:
        result = await self.session.execute(select(LearningAttempt).where(LearningAttempt.id == attempt_id))
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: UUID, limit: int = 50, offset: int = 0) -> List[LearningAttempt]:
        result = await self.session.execute(
            select(LearningAttempt)
            .where(LearningAttempt.user_id == user_id)
            .order_by(desc(LearningAttempt.created_at))
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def get_by_user_and_question(self, user_id: UUID, question_id: str) -> List[LearningAttempt]:
        result = await self.session.execute(
            select(LearningAttempt).where(
                LearningAttempt.user_id == user_id,
                LearningAttempt.question_id == question_id,
            )
        )
        return result.scalars().all()

    async def get_due_reviews(self, user_id: UUID, limit: int = 20) -> List[ReviewCard]:
        now = datetime.now(timezone.utc)
        result = await self.session.execute(
            select(ReviewCard)
            .where(ReviewCard.user_id == user_id, ReviewCard.next_review <= now)
            .order_by(asc(ReviewCard.next_review))
            .limit(limit)
        )
        return result.scalars().all()

    async def create(self, attempt_data: dict) -> LearningAttempt:
        attempt = LearningAttempt(**attempt_data)
        self.session.add(attempt)
        await self.flush()
        return attempt

    async def count_by_user_and_skill(
        self,
        user_id: UUID,
        skill_id: UUID,
        passed_only: bool = False,
    ) -> int:
        query = select(func.count(LearningAttempt.id)).where(
            LearningAttempt.user_id == user_id,
            LearningAttempt.skill_id == skill_id,
        )
        if passed_only:
            query = query.where(LearningAttempt.passed == True)  # noqa: E712
        result = await self.session.execute(query)
        return result.scalar_one()

    async def get_practice_evidence_by_user(
        self,
        user_id: UUID,
        limit: int = 5000,
    ) -> List[dict]:
        """Return practice evidence rows for prerequisite evaluation.

        Each row is a dict with question_id, skill_id (str), score (float),
        ordered newest first — mirrors the old learning_events_collection shape.
        """
        result = await self.session.execute(
            select(
                LearningAttempt.question_id,
                LearningAttempt.skill_id,
                LearningAttempt.score,
            )
            .where(LearningAttempt.user_id == user_id)
            .where(LearningAttempt.activity_type == "practice")
            .where(LearningAttempt.question_id.is_not(None))
            .where(LearningAttempt.question_id != "")
            .where(LearningAttempt.skill_id.is_not(None))
            .order_by(desc(LearningAttempt.created_at))
            .limit(limit)
        )
        return [
            {
                "question_id": row.question_id,
                "skill_id": str(row.skill_id) if row.skill_id else "",
                "score": float(row.score or 0),
            }
            for row in result.all()
        ]


# ════════════════════════════════════════════════════════════════════════════════
# LEARNING EVIDENCE REPOSITORY
# ════════════════════════════════════════════════════════════════════════════════

class LearningEvidenceRepository(RepositoryBase):
    """Repository for immutable learning evidence — append-only, never overwritten."""

    async def get_by_attempt(self, attempt_id: UUID) -> List[LearningEvidence]:
        result = await self.session.execute(
            select(LearningEvidence).where(LearningEvidence.attempt_id == attempt_id)
        )
        return result.scalars().all()

    async def get_by_user(self, user_id: UUID, limit: int = 50, offset: int = 0) -> List[LearningEvidence]:
        result = await self.session.execute(
            select(LearningEvidence)
            .where(LearningEvidence.user_id == user_id)
            .order_by(desc(LearningEvidence.created_at))
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def get_by_user_and_skill(
        self,
        user_id: UUID,
        skill_id: UUID,
        evidence_type: Optional[str] = None,
    ) -> List[LearningEvidence]:
        query = select(LearningEvidence).where(
            LearningEvidence.user_id == user_id,
            LearningEvidence.skill_id == skill_id,
        )
        if evidence_type:
            query = query.where(LearningEvidence.evidence_type == evidence_type)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def count_by_user_and_skill_and_type(
        self,
        user_id: UUID,
        skill_id: UUID,
        evidence_type: str,
    ) -> int:
        result = await self.session.execute(
            select(func.count(LearningEvidence.id)).where(
                LearningEvidence.user_id == user_id,
                LearningEvidence.skill_id == skill_id,
                LearningEvidence.evidence_type == evidence_type,
            )
        )
        return result.scalar_one()

    async def create(self, evidence_data: dict) -> LearningEvidence:
        evidence = LearningEvidence(**evidence_data)
        self.session.add(evidence)
        await self.flush()
        return evidence


# ════════════════════════════════════════════════════════════════════════════════
# MASTERY SNAPSHOT REPOSITORY
# ════════════════════════════════════════════════════════════════════════════════

class MasterySnapshotRepository(RepositoryBase):
    """Repository for historical mastery snapshots."""

    async def get_by_user_and_skill(self, user_id: UUID, skill_id: UUID) -> List[MasterySnapshot]:
        result = await self.session.execute(
            select(MasterySnapshot)
            .where(MasterySnapshot.user_id == user_id, MasterySnapshot.skill_id == skill_id)
            .order_by(desc(MasterySnapshot.created_at))
        )
        return result.scalars().all()

    async def get_latest_by_user_and_skill(
        self,
        user_id: UUID,
        skill_id: UUID,
    ) -> Optional[MasterySnapshot]:
        result = await self.session.execute(
            select(MasterySnapshot)
            .where(MasterySnapshot.user_id == user_id, MasterySnapshot.skill_id == skill_id)
            .order_by(desc(MasterySnapshot.created_at))
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def create(self, snapshot_data: dict) -> MasterySnapshot:
        snapshot = MasterySnapshot(**snapshot_data)
        self.session.add(snapshot)
        await self.flush()
        return snapshot


# ════════════════════════════════════════════════════════════════════════════════
# REVIEW CARD REPOSITORY (SPACED REPETITION)
# ════════════════════════════════════════════════════════════════════════════════

class ReviewCardRepository(RepositoryBase):
    """Repository for spaced repetition cards — replaces srs_cards."""

    async def get_by_id(self, card_id: UUID) -> Optional[ReviewCard]:
        result = await self.session.execute(select(ReviewCard).where(ReviewCard.id == card_id))
        return result.scalar_one_or_none()

    async def get_by_user_and_problem(self, user_id: UUID, problem_id: str) -> Optional[ReviewCard]:
        result = await self.session.execute(
            select(ReviewCard).where(
                ReviewCard.user_id == user_id,
                ReviewCard.problem_id == problem_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_due_cards(self, user_id: UUID, limit: int = 20) -> List[ReviewCard]:
        now = datetime.now(timezone.utc)
        result = await self.session.execute(
            select(ReviewCard)
            .where(ReviewCard.user_id == user_id, ReviewCard.next_review <= now)
            .order_by(asc(ReviewCard.next_review))
            .limit(limit)
        )
        return result.scalars().all()

    async def get_upcoming_cards(self, user_id: UUID, limit: int = 20) -> List[ReviewCard]:
        now = datetime.now(timezone.utc)
        result = await self.session.execute(
            select(ReviewCard)
            .where(ReviewCard.user_id == user_id, ReviewCard.next_review > now)
            .order_by(asc(ReviewCard.next_review))
            .limit(limit)
        )
        return result.scalars().all()

    async def create_or_update(
        self,
        user_id: UUID,
        problem_id: str,
        next_review: datetime,
        difficulty: str,
        interval: int,
        repetitions: int,
        ease_factor: int,
    ) -> ReviewCard:
        existing = await self.get_by_user_and_problem(user_id, problem_id)
        if existing:
            existing.next_review = next_review
            existing.difficulty = difficulty
            existing.interval = interval
            existing.repetitions = repetitions
            existing.ease_factor = ease_factor
            existing.updated_at = datetime.now(timezone.utc)
            await self.flush()
            return existing
        card = ReviewCard(
            user_id=user_id,
            problem_id=problem_id,
            next_review=next_review,
            difficulty=difficulty,
            interval=interval,
            repetitions=repetitions,
            ease_factor=ease_factor,
        )
        self.session.add(card)
        await self.flush()
        return card

    async def count_due(self, user_id: UUID) -> int:
        now = datetime.now(timezone.utc)
        result = await self.session.execute(
            select(func.count(ReviewCard.id)).where(
                ReviewCard.user_id == user_id,
                ReviewCard.next_review <= now,
            )
        )
        return result.scalar_one()


# ════════════════════════════════════════════════════════════════════════════════
# REPAIR MISSION REPOSITORY
# ════════════════════════════════════════════════════════════════════════════════

class RepairMissionRepository(RepositoryBase):
    """Repository for repair missions — replaces repair_missions."""

    async def get_by_id(self, mission_id: UUID) -> Optional[RepairMission]:
        result = await self.session.execute(select(RepairMission).where(RepairMission.id == mission_id))
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: UUID, status: Optional[str] = None) -> List[RepairMission]:
        query = select(RepairMission).where(RepairMission.user_id == user_id)
        if status:
            query = query.where(RepairMission.status == status)
        result = await self.session.execute(query.order_by(desc(RepairMission.created_at)))
        return result.scalars().all()

    async def get_open_by_user_and_skill(
        self,
        user_id: UUID,
        skill_id: UUID,
    ) -> Optional[RepairMission]:
        result = await self.session.execute(
            select(RepairMission).where(
                RepairMission.user_id == user_id,
                RepairMission.skill_id == skill_id,
                RepairMission.status == "open",
            )
        )
        return result.scalar_one_or_none()

    async def create(self, mission_data: dict) -> RepairMission:
        mission = RepairMission(**mission_data)
        self.session.add(mission)
        await self.flush()
        return mission

    async def update_status(
        self,
        mission_id: UUID,
        status: str,
        completed_at: Optional[datetime] = None,
    ) -> Optional[RepairMission]:
        updates = {"status": status, "updated_at": datetime.now(timezone.utc)}
        if completed_at:
            updates["completed_at"] = completed_at
        result = await self.session.execute(
            update(RepairMission).where(RepairMission.id == mission_id).values(**updates)
        )
        return result.scalar_one_or_none()


# ════════════════════════════════════════════════════════════════════════════════
# REMEDIATION ATTEMPT REPOSITORY
# ════════════════════════════════════════════════════════════════════════════════

class RemediationAttemptRepository(RepositoryBase):
    """Repository for individual remediation attempts within a repair mission."""

    async def get_by_mission(self, mission_id: UUID) -> List[RemediationAttempt]:
        result = await self.session.execute(
            select(RemediationAttempt)
            .where(RemediationAttempt.repair_mission_id == mission_id)
            .order_by(asc(RemediationAttempt.created_at))
        )
        return result.scalars().all()

    async def get_by_user(self, user_id: UUID, limit: int = 20) -> List[RemediationAttempt]:
        result = await self.session.execute(
            select(RemediationAttempt)
            .where(RemediationAttempt.user_id == user_id)
            .order_by(desc(RemediationAttempt.created_at))
            .limit(limit)
        )
        return result.scalars().all()

    async def create(self, attempt_data: dict) -> RemediationAttempt:
        attempt = RemediationAttempt(**attempt_data)
        self.session.add(attempt)
        await self.flush()
        return attempt

    async def count_passed_by_mission(self, mission_id: UUID) -> int:
        result = await self.session.execute(
            select(func.count(RemediationAttempt.id)).where(
                RemediationAttempt.repair_mission_id == mission_id,
                RemediationAttempt.passed == True,  # noqa: E712
            )
        )
        return result.scalar_one()


# ══════════════════════════════════════════════════════════════════════════════
# DAILY CHALLENGE USER REPOSITORY
# ══════════════════════════════════════════════════════════════════════════════

class DailyChallengeUserRepository(RepositoryBase):
    """Repository for per-user daily challenge state.

    Migrated from MongoDB `daily_challenges_users` collection.
    """

    async def get_by_id(self, dcu_id: UUID) -> Optional[DailyChallengeUser]:
        result = await self.session.execute(
            select(DailyChallengeUser).where(DailyChallengeUser.id == dcu_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user_and_date(
        self,
        user_id: UUID,
        challenge_date,
    ) -> Optional[DailyChallengeUser]:
        result = await self.session.execute(
            select(DailyChallengeUser)
            .where(DailyChallengeUser.user_id == user_id)
            .where(DailyChallengeUser.challenge_date == challenge_date)
        )
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> List[DailyChallengeUser]:
        result = await self.session.execute(
            select(DailyChallengeUser)
            .where(DailyChallengeUser.user_id == user_id)
            .order_by(desc(DailyChallengeUser.challenge_date))
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def create(self, dcu_data: dict) -> DailyChallengeUser:
        dcu = DailyChallengeUser(**dcu_data)
        self.session.add(dcu)
        await self.flush()
        return dcu

    async def update(
        self,
        dcu_id: UUID,
        updates: dict,
    ) -> Optional[DailyChallengeUser]:
        result = await self.session.execute(
            update(DailyChallengeUser)
            .where(DailyChallengeUser.id == dcu_id)
            .values(**updates)
            .returning(DailyChallengeUser)
        )
        return result.scalar_one_or_none()


# ═══════════════════════════════════════════════════════════════════════════════
# LEARNING MODULE REPOSITORY
# ══════════════════════════════════════════════════════════════════════════════

class LearningModuleRepository(RepositoryBase):
    """Repository for learning module definitions — replaces learning_modules."""

    async def get_by_id(self, module_id: UUID) -> Optional[LearningModule]:
        result = await self.session.execute(
            select(LearningModule).where(LearningModule.id == module_id)
        )
        return result.scalar_one_or_none()

    async def list(
        self,
        filters: dict = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[LearningModule]:
        query = select(LearningModule)
        if filters:
            for key, value in filters.items():
                if hasattr(LearningModule, key):
                    query = query.where(getattr(LearningModule, key) == value)
        result = await self.session.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    async def count(self, filters: dict = None) -> int:
        query = select(func.count(LearningModule.id))
        if filters:
            for key, value in filters.items():
                if hasattr(LearningModule, key):
                    query = query.where(getattr(LearningModule, key) == value)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def create(self, module_data: dict) -> LearningModule:
        module = LearningModule(**module_data)
        self.session.add(module)
        await self.flush()
        return module


# ══════════════════════════════════════════════════════════════════════════════
# USER LEARNING PROGRESS REPOSITORY
# ══════════════════════════════════════════════════════════════════════════════

class UserLearningProgressRepository(RepositoryBase):
    """Repository for user learning progress — migrated from user_learning_progress."""

    async def get_by_user_and_module(
        self, user_id: UUID, module_id: UUID
    ) -> Optional[UserLearningProgress]:
        result = await self.session.execute(
            select(UserLearningProgress).where(
                UserLearningProgress.user_id == user_id,
                UserLearningProgress.module_id == module_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_by_user(
        self, user_id: UUID, limit: int = 50, offset: int = 0
    ) -> List[UserLearningProgress]:
        result = await self.session.execute(
            select(UserLearningProgress)
            .where(UserLearningProgress.user_id == user_id)
            .order_by(desc(UserLearningProgress.created_at))
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def create(self, data: dict) -> UserLearningProgress:
        progress = UserLearningProgress(**data)
        self.session.add(progress)
        await self.flush()
        return progress

    async def update(
        self,
        module_id: UUID,
        updates: dict,
    ) -> Optional[UserLearningProgress]:
        result = await self.session.execute(
            update(UserLearningProgress)
            .where(UserLearningProgress.module_id == module_id)
            .values(**updates)
            .returning(UserLearningProgress)
        )
        return result.scalar_one_or_none()


# ═══════════════════════════════════════════════════════════════════════════
# ACADEMY LEARNING PLAN REPOSITORY
# ══════════════════════════════════════════════════════════════════════════

class AcademyLearningPlanRepository(RepositoryBase):
    """Repository for academy learning plans — replaces academy_learning_plans."""

    async def get_by_user(self, user_id: UUID) -> Optional[AcademyLearningPlan]:
        result = await self.session.execute(
            select(AcademyLearningPlan).where(AcademyLearningPlan.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_active(self, user_id: UUID) -> Optional[AcademyLearningPlan]:
        result = await self.session.execute(
            select(AcademyLearningPlan).where(
                AcademyLearningPlan.user_id == user_id,
                AcademyLearningPlan.plan.has_key("generated_at"),
            )
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        user_id: UUID,
        plan: dict,
    ) -> AcademyLearningPlan:
        plan_doc = AcademyLearningPlan(
            user_id=user_id,
            plan=plan,
        )
        self.session.add(plan_doc)
        await self.flush()
        return plan_doc

    async def update(
        self,
        user_id: UUID,
        plan: dict,
    ) -> Optional[AcademyLearningPlan]:
        plan_doc = await self.get_by_user(user_id)
        if not plan_doc:
            return None
        plan_doc.plan = plan
        plan_doc.updated_at = datetime.now(timezone.utc)
        await self.flush()
        return plan_doc


# ══════════════════════════════════════════════════════════════════════════
# ACADEMY LEARNER PROFILE REPOSITORY
# ══════════════════════════════════════════════════════════════════════════

class AcademyLearnerProfileRepository(RepositoryBase):
    """Repository for academy learner profiles — replaces academy_learner_profiles."""

    async def get_by_user(self, user_id: UUID) -> Optional[AcademyLearnerProfile]:
        result = await self.session.execute(
            select(AcademyLearnerProfile).where(AcademyLearnerProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_active_by_user(self, user_id: UUID) -> Optional[AcademyLearnerProfile]:
        result = await self.session.execute(
            select(AcademyLearnerProfile).where(AcademyLearnerProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        user_id: UUID,
        profile_data: dict,
    ) -> AcademyLearnerProfile:
        profile = AcademyLearnerProfile(
            user_id=user_id,
            **profile_data,
        )
        self.session.add(profile)
        await self.flush()
        return profile

    async def update(
        self,
        user_id: UUID,
        profile_data: dict,
    ) -> Optional[AcademyLearnerProfile]:
        profile = await self.get_by_user(user_id)
        if not profile:
            return None
        for key, value in profile_data.items():
            setattr(profile, key, value)
        profile.updated_at = datetime.now(timezone.utc)
        await self.flush()
        return profile


# ═════════════════════════════════════════════════════════════════════════════
# ACADEMY DIAGNOSTIC SESSION REPOSITORY
# ════════════════════════════════════════════════════════════════════════════

class AcademyDiagnosticSessionRepository(RepositoryBase):
    """Repository for academy diagnostic sessions — replaces academy_diagnostic_sessions."""

    async def get_by_user(self, user_id: UUID) -> List[AcademyDiagnosticSession]:
        result = await self.session.execute(
            select(AcademyDiagnosticSession).where(AcademyDiagnosticSession.user_id == user_id)
        )
        return result.scalars().all()

    async def get_by_diagnostic_id(self, diagnostic_id: str) -> Optional[AcademyDiagnosticSession]:
        result = await self.session.execute(
            select(AcademyDiagnosticSession).where(AcademyDiagnosticSession.diagnostic_id == diagnostic_id)
        )
        return result.scalar_one_or_none()

    async def get_active_by_user(self, user_id: UUID) -> Optional[AcademyDiagnosticSession]:
        result = await self.session.execute(
            select(AcademyDiagnosticSession)
            .where(AcademyDiagnosticSession.user_id == user_id, AcademyDiagnosticSession.status == "in_progress")
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        user_id: UUID,
        diagnostic_id: str,
        question_ids: list,
    ) -> AcademyDiagnosticSession:
        session = AcademyDiagnosticSession(
            user_id=user_id,
            diagnostic_id=diagnostic_id,
            question_ids=question_ids,
            answers=[],
            status="in_progress",
        )
        self.session.add(session)
        await self.flush()
        return session

    async def add_answer(
        self,
        diagnostic_id: str,
        answer: dict,
    ) -> Optional[AcademyDiagnosticSession]:
        session = await self.get_by_diagnostic_id(diagnostic_id)
        if not session:
            return None
        session.answers.append(answer)
        await self.flush()
        return session

    async def complete(
        self,
        diagnostic_id: str,
        result: dict,
    ) -> Optional[AcademyDiagnosticSession]:
        session = await self.get_by_diagnostic_id(diagnostic_id)
        if not session:
            return None
        session.status = "completed"
        session.result = result
        session.completed_at = datetime.now(timezone.utc)
        await self.flush()
        return session

    async def update_answers(
        self,
        diagnostic_id: str,
        answers: list,
    ) -> Optional[AcademyDiagnosticSession]:
        session = await self.get_by_diagnostic_id(diagnostic_id)
        if not session:
            return None
        session.answers = answers
        await self.flush()
        return session


# ═══════════════════════════════════════════════════════════════════════════
# ACADEMY LEARNING PLAN REPOSITORY
# ═══════════════════════════════════════════════════════════════════════════

class AcademyLearningPlanRepository(RepositoryBase):
    """Repository for academy learning plans — replaces academy_learning_plans."""

    async def get_by_user(self, user_id: UUID) -> Optional[AcademyLearningPlan]:
        result = await self.session.execute(
            select(AcademyLearningPlan).where(AcademyLearningPlan.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_active(self, user_id: UUID) -> Optional[AcademyLearningPlan]:
        result = await self.session.execute(
            select(AcademyLearningPlan).where(
                AcademyLearningPlan.user_id == user_id,
                AcademyLearningPlan.plan.has_key("generated_at"),
            )
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        user_id: UUID,
        plan: dict,
    ) -> AcademyLearningPlan:
        plan_doc = AcademyLearningPlan(
            user_id=user_id,
            plan=plan,
        )
        self.session.add(plan_doc)
        await self.flush()
        return plan_doc

    async def update(
        self,
        user_id: UUID,
        plan: dict,
    ) -> Optional[AcademyLearningPlan]:
        plan_doc = await self.get_by_user(user_id)
        if not plan_doc:
            return None
        plan_doc.plan = plan
        plan_doc.updated_at = datetime.now(timezone.utc)
        await self.flush()
        return plan_doc
