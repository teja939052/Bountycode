"""Identity domain models — users, profiles, sessions, refresh tokens, legacy ID mapping.

Primary keys are UUIDs generated server-side via gen_random_uuid().
Legacy MongoDB ObjectIds are mapped via user_identity_map.
"""

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


class User(Base):
    """Core user account — migrated from MongoDB `users` collection."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    plan: Mapped[str] = mapped_column(String(50), default="free", nullable=False)
    paypal_customer_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    paypal_order_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    plan_pending: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    interviews_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    resumes_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    aptitude_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    mock_interviews_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    monthly_reset_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    daily_usage: Mapped[dict] = mapped_column(JSONB, default=dict, server_default=text("'{}'::jsonb"), nullable=False)
    all_time_usage: Mapped[dict] = mapped_column(JSONB, default=dict, server_default=text("'{}'::jsonb"), nullable=False)
    honor: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    uid: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True, index=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    last_active: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    refresh_jti: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    reset_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    reset_token_expires: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    email_verification_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    email_verification_expires: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    google_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    onboarding: Mapped[Optional[dict]] = mapped_column(JSONB, default=dict, server_default=text("'{}'::jsonb"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    profile: Mapped[Optional["UserProfile"]] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    sessions: Mapped[list["UserSession"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    gamification: Mapped[Optional["GamificationProfile"]] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    skill_states: Mapped[list["LearnerSkillState"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    learning_attempts: Mapped[list["LearningAttempt"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    coding_submissions: Mapped[list["CodingSubmission"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    oa_sessions: Mapped[list["OASession"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    interview_sessions: Mapped[list["InterviewSession"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    assessment_attempts: Mapped[list["AssessmentAttempt"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    career_profile: Mapped[Optional["CareerProfile"]] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    resume_metadata: Mapped[list["ResumeMetadata"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    analytics_events: Mapped[list["AnalyticsEvent"]] = relationship(cascade="all, delete-orphan")


class UserProfile(Base):
    """Extended user profile — career info, bio, skills, portfolio."""

    __tablename__ = "user_profiles"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    skills: Mapped[list[str]] = mapped_column(JSONB, default=list, server_default=text("'[]'::jsonb"), nullable=False)
    experience: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    portfolio_urls: Mapped[list[str]] = mapped_column(JSONB, default=list, server_default=text("'[]'::jsonb"), nullable=False)
    github_username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    leetcode_username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    target_company: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    target_role: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="profile")


class UserSession(Base):
    """User access session — tracks active JWT sessions."""

    __tablename__ = "user_sessions"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(back_populates="sessions")


class RefreshToken(Base):
    """Refresh token record — supports rotation and revocation."""

    __tablename__ = "refresh_tokens"

    jti: Mapped[str] = mapped_column(String(255), primary_key=True)  # JWT ID
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(Text, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    replaced_by_jti: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # rotation chain

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")


class UserIdentityMap(Base):
    """Maps legacy MongoDB ObjectIds to PostgreSQL UUIDs during migration.

    Kept indefinitely for audit and backward-compatible auth resolution.
    """

    __tablename__ = "user_identity_map"

    legacy_mongo_id: Mapped[str] = mapped_column(String(255), primary_key=True)  # ObjectId as string
    postgres_user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class AcademyDiagnosticSession(Base):
    """Academy diagnostic session records — migrated from MongoDB academy_diagnostic_sessions."""

    __tablename__ = "academy_diagnostic_sessions"

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
    diagnostic_id: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    question_ids: Mapped[list[str]] = mapped_column(JSONB, default=list, server_default=text("'[]'::jsonb"), nullable=False)
    answers: Mapped[list[dict]] = mapped_column(JSONB, default=list, server_default=text("'[]'::jsonb"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="in_progress", nullable=False)
    result: Mapped[Optional[dict]] = mapped_column(JSONB, default=None, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship()


class AcademyLearnerProfile(Base):
    """Academy learner profile — migrated from MongoDB academy_learner_profiles."""

    __tablename__ = "academy_learner_profiles"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    target_role: Mapped[str] = mapped_column(String(50), default="undecided", nullable=False)
    target_companies: Mapped[list[str]] = mapped_column(JSONB, default=list, server_default=text("'[]'::jsonb"), nullable=False)
    assessment_track: Mapped[str] = mapped_column(String(50), default="service_company_core", nullable=False)
    assessment_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    experience_level: Mapped[str] = mapped_column(String(50), default="absolute_beginner", nullable=False)
    preferred_language: Mapped[str] = mapped_column(String(20), default="cpp", nullable=False)
    daily_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    weekly_days: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    device_type: Mapped[str] = mapped_column(String(20), default="laptop", nullable=False)
    local_runtime_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    accessibility_needs: Mapped[str] = mapped_column(String(240), default="", nullable=False)
    placement_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    learning_preference: Mapped[str] = mapped_column(String(20), default="mixed", nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), default="Asia/Kolkata", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship()


class AcademyLearningPlan(Base):
    """Academy learning plan records — migrated from MongoDB academy_learning_plans."""

    __tablename__ = "academy_learning_plans"

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
    plan: Mapped[dict] = mapped_column(JSONB, default=dict, server_default=text("'{}'::jsonb"), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped["User"] = relationship()
