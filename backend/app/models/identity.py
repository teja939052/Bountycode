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
    analytics_events: Mapped[list["AnalyticsEvent"]] = relationship(back_populates="user", cascade="all, delete-orphan")


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
