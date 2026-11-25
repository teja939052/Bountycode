"""PostgreSQL-based authentication service.

Replaces Motor/MongoDB user persistence in auth.py routes with SQLAlchemy
AsyncSession operations on the `users` table plus `user_identity_map` for
legacy ObjectId → UUID mapping.

All write operations use the injected AsyncSession. The caller owns the
transaction boundary (commit/rollback).
"""

import logging
import secrets
from datetime import datetime, timezone, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_

from app.models.identity import User, UserIdentityMap
from app.repositories.identity import UserIdentityMapRepository, UserRepository

logger = logging.getLogger(__name__)


class PostgresAuthService:
    """PostgreSQL-backed authentication operations.

    Provides the same business logic as the Motor-based auth.py routes but
    using PostgreSQL as the authoritative store.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.identity_repo = UserIdentityMapRepository(session)

    # ═══════════════════════════════════════════════════════════════════════════
    # USER LOOKUP
    # ═══════════════════════════════════════════════════════════════════════════

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Look up a user by email (case-insensitive)."""
        result = await self.session.execute(
            select(User).where(User.email == email.lower().strip())
        )
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Look up a user by PostgreSQL UUID."""
        return await self.user_repo.get_by_id(user_id)

    async def get_user_by_legacy_mongo_id(self, legacy_mongo_id: str) -> Optional[User]:
        """Resolve legacy MongoDB ObjectId to PostgreSQL user via identity map."""
        return await self.user_repo.get_by_legacy_mongo_id(legacy_mongo_id)

    async def get_user_by_google_id(self, google_id: str) -> Optional[User]:
        """Look up a user by Google ID."""
        result = await self.session.execute(
            select(User).where(User.google_id == google_id)
        )
        return result.scalar_one_or_none()

    # ═══════════════════════════════════════════════════════════════════════════
    # USER CREATION (REGISTRATION)
    # ═══════════════════════════════════════════════════════════════════════════

    async def create_user(
        self,
        email: str,
        password_hash: str,
        name: str,
        legacy_mongo_id: Optional[str] = None,
        google_id: Optional[str] = None,
        country: Optional[str] = None,
        ip: Optional[str] = None,
    ) -> tuple[User, bool]:
        """Create a new user and optional identity map.

        Returns (user, created). If a user with the same email already
        exists, returns (existing_user, False).
        """
        email_norm = email.lower().strip()

        # Check for existing user by email
        existing = await self.get_user_by_email(email_norm)
        if existing:
            return existing, False

        # Check for existing user by Google ID
        if google_id:
            existing_google = await self.get_user_by_google_id(google_id)
            if existing_google:
                return existing_google, False

        now = datetime.now(timezone.utc)
        user = User(
            email=email_norm,
            password_hash=password_hash,
            name=name,
            plan="free",
            country=country,
            ip=ip,
            email_verified=bool(google_id),  # Google accounts are pre-verified
            email_verification_token=None if google_id else secrets.token_urlsafe(32),
            email_verification_expires=(
                None if google_id else now + timedelta(hours=24)
            ),
            google_id=google_id,
            interviews_used=0,
            resumes_used=0,
            aptitude_used=0,
            mock_interviews_used=0,
            monthly_reset_date=now,
            created_at=now,
            last_active=now,
            onboarding={},
        )
        self.session.add(user)
        await self.session.flush()

        # Create identity map for legacy MongoDB ObjectId → UUID mapping
        if legacy_mongo_id:
            await self.identity_repo.create_mapping(legacy_mongo_id, user.id)

        return user, True

    # ═══════════════════════════════════════════════════════════════════════════
    # REFRESH TOKEN (JTI) MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════════

    async def set_refresh_jti(self, user_id: UUID, jti: str) -> None:
        """Store the current refresh JTI for a user (token rotation)."""
        await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(refresh_jti=jti, last_active=datetime.now(timezone.utc))
        )

    async def verify_refresh_jti(self, user_id: UUID, jti: str) -> bool:
        """Verify that the refresh JTI matches the server-tracked value.

        Returns True if the JTI matches, False otherwise.
        """
        result = await self.session.execute(
            select(User.refresh_jti).where(User.id == user_id)
        )
        stored_jti = result.scalar_one_or_none()
        return stored_jti == jti

    async def clear_refresh_jti(self, user_id: UUID) -> None:
        """Revoke the refresh JTI (logout / password change)."""
        await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(refresh_jti=None)
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # PASSWORD RESET
    # ═══════════════════════════════════════════════════════════════════════════

    async def set_reset_token(
        self,
        user_id: UUID,
        token: str,
        expires_at: datetime,
    ) -> None:
        """Store a password reset token and expiry."""
        await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(reset_token=token, reset_token_expires=expires_at)
        )

    async def verify_reset_token(
        self,
        user_id: UUID,
        token: str,
    ) -> Optional[User]:
        """Verify a password reset token. Returns the user if valid, None otherwise."""
        result = await self.session.execute(
            select(User).where(
                and_(
                    User.id == user_id,
                    User.reset_token == token,
                    User.reset_token_expires > datetime.now(timezone.utc),
                )
            )
        )
        return result.scalar_one_or_none()

    async def clear_reset_token(self, user_id: UUID) -> None:
        """Clear the reset token after successful use."""
        await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(reset_token=None, reset_token_expires=None)
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # EMAIL VERIFICATION
    # ═══════════════════════════════════════════════════════════════════════════

    async def set_email_verification_token(
        self,
        user_id: UUID,
        token: str,
        expires_at: datetime,
    ) -> None:
        """Store an email verification token and expiry."""
        await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                email_verification_token=token,
                email_verification_expires=expires_at,
            )
        )

    async def verify_email_token(self, token: str) -> Optional[User]:
        """Verify an email verification token. Returns the user if valid."""
        result = await self.session.execute(
            select(User).where(
                and_(
                    User.email_verification_token == token,
                    User.email_verification_expires > datetime.now(timezone.utc),
                )
            )
        )
        return result.scalar_one_or_none()

    async def mark_email_verified(self, user_id: UUID) -> None:
        """Mark a user's email as verified and clear the verification token."""
        await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                email_verified=True,
                email_verification_token=None,
                email_verification_expires=None,
            )
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # USER UPDATE
    # ═══════════════════════════════════════════════════════════════════════════

    async def update_user(
        self,
        user_id: UUID,
        updates: dict,
    ) -> Optional[User]:
        """Update user fields. Returns the updated user or None."""
        result = await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(**updates)
            .returning(User)
        )
        return result.scalar_one_or_none()

    async def update_onboarding(
        self,
        user_id: UUID,
        onboarding: dict,
    ) -> Optional[User]:
        """Update onboarding data for a user."""
        return await self.update_user(user_id, {"onboarding": onboarding})
