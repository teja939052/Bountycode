"""Learning domain models — skills, skill states, attempts, evidence, mastery, SRS, repair."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import (
    Boolean,
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Skill(Base):
    """Canonical skill definition — from content/lesson_definitions.py and world registries."""

    __tablename__ = "skills"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    topic: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    sub_topic: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    difficulty: Mapped[str] = mapped_column(String(50), nullable=False)  # easy, medium, hard, expert
    prerequisites: Mapped[list[UUID]] = mapped_column(
        JSONB, default=list, server_default=text("'[]'::jsonb"), nullable=False
    )
    content_version: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    prerequisite_links: Mapped[list["SkillPrerequisite"]] = relationship(
        back_populates="skill", foreign_keys="SkillPrerequisite.skill_id", cascade="all, delete-orphan"
    )
    learner_states: Mapped[list["LearnerSkillState"]] = relationship(back_populates="skill", cascade="all, delete-orphan")


class SkillPrerequisite(Base):
    """Skill prerequisite relationship — DAG for learning paths."""

    __tablename__ = "skill_prerequisites"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    skill_id: Mapped[UUID] = mapped_column(ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    prerequisite_skill_id: Mapped[UUID] = mapped_column(ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    skill: Mapped["Skill"] = relationship(back_populates="prerequisite_links", foreign_keys=[skill_id])

    __table_args__ = (
        UniqueConstraint("skill_id", "prerequisite_skill_id", name="uq_skill_prerequisite"),
    )


class LearnerSkillState(Base):
    """Per-user-per-skill mastery state — migrated from MongoDB `skill_graphs`."""

    __tablename__ = "learner_skill_state"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id: Mapped[UUID] = mapped_column(ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    score: Mapped[float] = mapped_column(Integer, default=0, nullable=False)  # 0-100 percent
    mastery_level: Mapped[str] = mapped_column(String(50), default="beginner", nullable=False)  # beginner, intermediate, advanced, master
    total_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_practiced: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="skill_states")
    skill: Mapped["Skill"] = relationship(back_populates="learner_states")

    __table_args__ = (
        UniqueConstraint("user_id", "skill_id", name="uq_learner_skill_state"),
    )


class LearningAttempt(Base):
    """Immutable learning attempt record — one per question/activity interaction."""

    __tablename__ = "learning_attempts"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("skills.id", ondelete="SET NULL"), nullable=True, index=True)
    question_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    activity_type: Mapped[str] = mapped_column(String(50), nullable=False)  # practice, repair, retest, mock, lesson
    score: Mapped[float] = mapped_column(Integer, nullable=False)  # 0-10
    evidence_type: Mapped[str] = mapped_column(String(50), nullable=False)  # independent, assisted, hint, repair
    passing_score: Mapped[float] = mapped_column(Integer, default=7, nullable=False)
    max_attempts: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    attempt_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    attempt_metadata: Mapped[dict] = mapped_column(JSONB, default=dict, server_default=text("'{}'::jsonb"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped["User"] = relationship(back_populates="learning_attempts")
    skill: Mapped[Optional["Skill"]] = relationship()


class LearningEvidence(Base):
    """Evidence of learning — immutable, append-only. Never overwritten."""

    __tablename__ = "learning_evidence"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    attempt_id: Mapped[UUID] = mapped_column(ForeignKey("learning_attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("skills.id", ondelete="SET NULL"), nullable=True, index=True)
    evidence_data: Mapped[dict] = mapped_column(JSONB, default=dict, server_default=text("'{}'::jsonb"), nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(50), nullable=False)  # solution, hint, repair, transfer
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped["User"] = relationship()


class MasterySnapshot(Base):
    """Mastery level snapshots — historical record of skill mastery changes."""

    __tablename__ = "mastery_snapshots"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id: Mapped[UUID] = mapped_column(ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    mastery_level: Mapped[str] = mapped_column(String(50), nullable=False)
    evidence_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    score_at_snapshot: Mapped[float] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class ReviewCard(Base):
    """Spaced repetition card — migrated from MongoDB `srs_cards`."""

    __tablename__ = "review_cards"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    problem_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    next_review: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    difficulty: Mapped[str] = mapped_column(String(50), default="medium", nullable=False)
    interval: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # days
    repetitions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    ease_factor: Mapped[int] = mapped_column(BigInteger, default=2500, nullable=False)  # SM-2 ease factor * 1000
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("user_id", "problem_id", name="uq_review_card"),
    )


class RepairMission(Base):
    """Repair mission — diagnostic → guided practice → retest flow."""

    __tablename__ = "repair_missions"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id: Mapped[UUID] = mapped_column(ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="open", nullable=False)  # open, in_progress, completed, failed
    tier: Mapped[str] = mapped_column(String(50), default="repair", nullable=False)
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    remediation_attempts: Mapped[list["RemediationAttempt"]] = relationship(back_populates="repair_mission", cascade="all, delete-orphan")


class RemediationAttempt(Base):
    """Individual remediation attempt within a repair mission."""

    __tablename__ = "remediation_attempts"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    repair_mission_id: Mapped[UUID] = mapped_column(ForeignKey("repair_missions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    score: Mapped[float] = mapped_column(Integer, nullable=False)  # 0-10
    passed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    repair_mission: Mapped["RepairMission"] = relationship(back_populates="remediation_attempts")
