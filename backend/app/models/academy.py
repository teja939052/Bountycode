"""PostgreSQL persistence for the Academy onboarding and diagnostic loop."""
from datetime import date, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AcademyLearnerProfile(Base):
    """Learner-owned onboarding configuration used by deterministic planning."""

    __tablename__ = "academy_learner_profiles"

    __table_args__ = (UniqueConstraint("user_id", name="uq_academy_learner_profiles_user_id"),)

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    target_role: Mapped[str] = mapped_column(String(80), nullable=False, default="undecided")
    target_companies: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    assessment_track: Mapped[str] = mapped_column(String(80), nullable=False, default="service_company_core")
    assessment_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    experience_level: Mapped[str] = mapped_column(String(40), nullable=False, default="absolute_beginner")
    preferred_language: Mapped[str] = mapped_column(String(30), nullable=False, default="cpp")
    daily_minutes: Mapped[int] = mapped_column(nullable=False, default=60)
    weekly_days: Mapped[int] = mapped_column(nullable=False, default=5)
    device_type: Mapped[str] = mapped_column(String(30), nullable=False, default="laptop")
    local_runtime_available: Mapped[bool] = mapped_column(nullable=False, default=True)
    accessibility_needs: Mapped[str] = mapped_column(Text, nullable=False, default="")
    placement_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    learning_preference: Mapped[str] = mapped_column(String(40), nullable=False, default="mixed")
    timezone: Mapped[str] = mapped_column(String(80), nullable=False, default="Asia/Kolkata")
    onboarding_complete: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class AcademyDiagnosticSession(Base):
    """Immutable question selection plus learner answers and deterministic result."""

    __tablename__ = "academy_diagnostic_sessions"

    __table_args__ = (
        UniqueConstraint("user_id", "diagnostic_id", name="uq_academy_diagnostic_sessions_user_diagnostic"),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    diagnostic_id: Mapped[str] = mapped_column(String(160), nullable=False)
    question_ids: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    answers: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="in_progress", index=True)
    result: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)


class AcademyLearningPlan(Base):
    """Latest deterministic personalized plan for a learner."""

    __tablename__ = "academy_learning_plans"

    __table_args__ = (UniqueConstraint("user_id", name="uq_academy_learning_plans_user_id"),)

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    plan: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
