"""Identity domain repositories — PostgreSQL replacements for Motor collection operations."""

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import RepositoryBase
from app.models.identity import (
    User,
    UserProfile,
    UserSession,
    RefreshToken,
    UserIdentityMap,
)


class UserRepository(RepositoryBase):
    """Repository for user accounts — replaces users_collection Motor operations."""

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_uid(self, uid: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.uid == uid))
        return result.scalar_one_or_none()

    async def get_by_legacy_mongo_id(self, legacy_mongo_id: str) -> Optional[User]:
        """Resolve legacy MongoDB ObjectId to PostgreSQL user via identity map."""
        result = await self.session.execute(
            select(UserIdentityMap).where(UserIdentityMap.legacy_mongo_id == legacy_mongo_id)
        )
        identity_map = result.scalar_one_or_none()
        if not identity_map:
            return None
        return await self.get_by_id(identity_map.postgres_user_id)

    async def create(self, user_data: dict) -> User:
        user = User(**user_data)
        self.session.add(user)
        await self.flush()
        return user

    async def update(self, user_id: UUID, updates: dict) -> Optional[User]:
        result = await self.session.execute(
            update(User).where(User.id == user_id).values(**updates).returning(User)
        )
        return result.scalar_one_or_none()

    async def delete(self, user_id: UUID) -> bool:
        result = await self.session.execute(delete(User).where(User.id == user_id))
        return result.rowcount > 0

    async def count(self) -> int:
        result = await self.session.execute(select(func.count(User.id)))
        return result.scalar_one()


class UserProfileRepository(RepositoryBase):
    """Repository for user profiles."""

    async def get_by_user_id(self, user_id: UUID) -> Optional[UserProfile]:
        result = await self.session.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_or_update(self, user_id: UUID, profile_data: dict) -> UserProfile:
        existing = await self.get_by_user_id(user_id)
        if existing:
            for key, value in profile_data.items():
                setattr(existing, key, value)
            await self.flush()
            return existing
        profile = UserProfile(user_id=user_id, **profile_data)
        self.session.add(profile)
        await self.flush()
        return profile


class UserSessionRepository(RepositoryBase):
    """Repository for user sessions — JWT session tracking."""

    async def create(self, user_id: UUID, expires_at: datetime) -> UserSession:
        session = UserSession(user_id=user_id, expires_at=expires_at)
        self.session.add(session)
        await self.flush()
        return session

    async def get_valid(self, session_id: UUID) -> Optional[UserSession]:
        now = datetime.now(timezone.utc)
        result = await self.session.execute(
            select(UserSession).where(
                UserSession.id == session_id,
                UserSession.expires_at > now,
                UserSession.revoked_at.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def revoke(self, session_id: UUID) -> bool:
        result = await self.session.execute(
            update(UserSession).where(UserSession.id == session_id).values(revoked_at=datetime.now(timezone.utc))
        )
        return result.rowcount > 0

    async def revoke_all_for_user(self, user_id: UUID) -> int:
        result = await self.session.execute(
            update(UserSession)
            .where(UserSession.user_id == user_id, UserSession.revoked_at.is_(None))
            .values(revoked_at=datetime.now(timezone.utc))
        )
        return result.rowcount or 0


class RefreshTokenRepository(RepositoryBase):
    """Repository for refresh tokens — rotation and revocation support."""

    async def create(self, jti: str, user_id: UUID, token_hash: str, expires_at: datetime) -> RefreshToken:
        token = RefreshToken(jti=jti, user_id=user_id, token_hash=token_hash, expires_at=expires_at)
        self.session.add(token)
        await self.flush()
        return token

    async def get_by_jti(self, jti: str) -> Optional[RefreshToken]:
        result = await self.session.execute(select(RefreshToken).where(RefreshToken.jti == jti))
        return result.scalar_one_or_none()

    async def revoke(self, jti: str) -> bool:
        result = await self.session.execute(
            update(RefreshToken).where(RefreshToken.jti == jti).values(revoked_at=datetime.now(timezone.utc))
        )
        return result.rowcount > 0

    async def rotate(self, old_jti: str, new_jti: str, new_token_hash: str, new_expires_at: datetime) -> Optional[RefreshToken]:
        """Rotate a refresh token — mark old as revoked, create new."""
        await self.revoke(old_jti)
        return await self.create(new_jti, old_jti and None, new_token_hash, new_expires_at)  # user_id filled by caller


class UserIdentityMapRepository(RepositoryBase):
    """Repository for legacy MongoDB ObjectId → PostgreSQL UUID mapping."""

    async def get_postgres_id(self, legacy_mongo_id: str) -> Optional[UUID]:
        result = await self.session.execute(
            select(UserIdentityMap.postgres_user_id).where(UserIdentityMap.legacy_mongo_id == legacy_mongo_id)
        )
        return result.scalar_one_or_none()

    async def create_mapping(self, legacy_mongo_id: str, postgres_user_id: UUID) -> UserIdentityMap:
        mapping = UserIdentityMap(legacy_mongo_id=legacy_mongo_id, postgres_user_id=postgres_user_id)
        self.session.add(mapping)
        await self.flush()
        return mapping
