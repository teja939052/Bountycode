"""Assessments domain models — attempts, sections, responses, coding submissions, OA sessions, interviews."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import (
    Boolean,
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


class AssessmentAttempt(Base):
    """Assessment attempt — one per user per assessment session."""

    __tablename__ = "assessment_attempts"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    assessment_id: Mapped[UUID] = mapped_column(ForeignKey("assessment_definitions.id", ondelete="CASCADE"), nullable=False, index=True)
    variant_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    score: Mapped[Optional[float]] = mapped_column(Integer, nullable=True)  # 0-100 percent
    status: Mapped[str] = mapped_column(String(50), default="in_progress", nullable=False)  # in_progress, completed, abandoned
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)

    user: Mapped["User"] = relationship()


class AssessmentSection(Base):
    """Section within an assessment attempt."""

    __tablename__ = "assessment_sections"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    attempt_id: Mapped[UUID] = mapped_column(ForeignKey("assessment_attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    section_type: Mapped[str] = mapped_column(String(50), nullable=False)  # coding, aptitude, behavioral, system_design
    score: Mapped[Optional[float]] = mapped_column(Integer, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class Response(Base):
    """Individual question response within an assessment section."""

    __tablename__ = "responses"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    section_id: Mapped[UUID] = mapped_column(ForeignKey("assessment_sections.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_correct: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    score: Mapped[Optional[float]] = mapped_column(Integer, nullable=True)  # 0-10
    time_taken_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class CodingSubmission(Base):
    """Coding challenge submission — migrated from MongoDB `submissions`."""

    __tablename__ = "coding_submissions"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)  # pending, accepted, wrong_answer, error
    score: Mapped[Optional[float]] = mapped_column(Integer, nullable=True)  # 0-100 percent
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    execution_result: Mapped[dict] = mapped_column(JSONB, default=dict, server_default=text("'{}'::jsonb"), nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped["User"] = relationship()


class ExecutionResult(Base):
    """Individual test case execution result."""

    __tablename__ = "execution_results"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    submission_id: Mapped[UUID] = mapped_column(ForeignKey("coding_submissions.id", ondelete="CASCADE"), nullable=False, index=True)
    test_case_id: Mapped[str] = mapped_column(String(255), nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    expected: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    actual: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    execution_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class OASession(Base):
    """Online Assessment session — migrated from MongoDB `oa_sessions`."""

    __tablename__ = "oa_sessions"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    company: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    blueprint: Mapped[dict] = mapped_column(JSONB, default=dict, server_default=text("'{}'::jsonb"), nullable=False)  # section weights
    mode: Mapped[str] = mapped_column(String(50), default="calm", nullable=False)  # calm, timed, interview
    integrity_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="in_progress", nullable=False)  # in_progress, completed, abandoned
    questions: Mapped[list[dict]] = mapped_column(JSONB, default=list, server_default=text("'[]'::jsonb"), nullable=False)
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(back_populates="oa_sessions")


class InterviewSession(Base):
    """Mock interview session — AI interviewer session record."""

    __tablename__ = "interview_sessions"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    interview_type: Mapped[str] = mapped_column(String(50), nullable=False)  # behavioral, technical, mixed
    company: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    difficulty: Mapped[str] = mapped_column(String(50), default="medium", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="in_progress", nullable=False)  # in_progress, completed, abandoned
    score: Mapped[Optional[float]] = mapped_column(Integer, nullable=True)  # 0-100
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(back_populates="interview_sessions")


class CompanyAssessmentMetadata(Base):
    """Company-specific assessment metadata."""

    __tablename__ = "company_assessment_metadata"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    company: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    assessment_type: Mapped[str] = mapped_column(String(50), nullable=False)
    assessment_metadata: Mapped[dict] = mapped_column(JSONB, default=dict, server_default=text("'{}'::jsonb"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("company", "role", "assessment_type", name="uq_company_assessment"),
    )


class InterviewBooking(Base):
    """Scheduled mock interview booking.

    Migrated from MongoDB `interview_bookings` collection.
    """

    __tablename__ = "interview_bookings"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    company: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    role: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    interview_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="technical"
    )
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="scheduled"
    )  # scheduled, completed, cancelled, no_show
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship()


class SolvedProblem(Base):
    """Daily challenge / problem solve history.

    Migrated from MongoDB `solved_problems` collection.
    """

    __tablename__ = "solved_problems"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    problem_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    problem_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="coding"
    )  # coding, aptitude, sql
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="solved"
    )  # solved, attempted, failed
    score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 0-100
    language: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    time_taken_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship()


class QuestionAnswer(Base):
    """Question answer record.

    Migrated from MongoDB `question_answers` collection.
    """

    __tablename__ = "question_answers"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    question_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_correct: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    time_taken_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship()
