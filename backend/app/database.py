"""PostgreSQL database layer for BountyCode.

Uses SQLAlchemy 2.x async engine with asyncpg driver. This is the sole
database layer for the application — no MongoDB/Motor dependency remains.

Connection string: SUPABASE_DB_URL (asyncpg format:
postgresql+asyncpg://user:pass@host:5432/db)

If using Supabase transaction pooler (port 6543), set statement_cache_size=0.
"""

import logging
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text

from app.config import get_settings
from app.models.base import Base
from app.observability.db_instrumentation import instrument_sqlalchemy_engine

logger = logging.getLogger(__name__)
settings = get_settings()

# ═══════════════════════════════════════════════════════════════════════════════
# POSTGRESQL — PostgreSQL (PRIMARY — the only database backend)
# ═══════════════════════════════════════════════════════════════════════════════

# Optional SUPABASE_DB_URL overrides the localhost fallback for PostgreSQL
SUPABASE_DB_URL: Optional[str] = getattr(settings, "SUPABASE_DB_URL", None) or None

_engine: Optional[AsyncEngine] = None
_session_factory: Optional[async_sessionmaker[AsyncSession]] = None


def _build_database_url() -> str:
    """Build the async PostgreSQL URL.

    Priority: SUPABASE_DB_URL > localhost fallback.
    If using Supabase transaction pooler (port 6543), set statement_cache_size=0.
    """
    if SUPABASE_DB_URL:
        return SUPABASE_DB_URL
    return "postgresql+asyncpg://postgres:postgres@localhost:5432/bountycode"


def get_engine() -> AsyncEngine:
    """Get or create the singleton async SQLAlchemy engine."""
    global _engine
    if _engine is None:
        database_url = _build_database_url()
        pool_kwargs = {}
        if ":6543" in database_url:
            pool_kwargs["statement_cache_size"] = 0
            logger.info(
                "Detected Supabase transaction pooler — disabling prepared statement cache"
            )

        _engine = create_async_engine(
            database_url,
            echo=False,
            pool_size=20,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800,
            **pool_kwargs,
        )
        instrument_sqlalchemy_engine(_engine.sync_engine)
        logger.info("SQLAlchemy async engine created for PostgreSQL")
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Get or create the async session factory."""
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(
            bind=get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )
    return _session_factory


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency — yields an async SQLAlchemy session with auto-rollback on error."""
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_session_no_commit() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency — yields a session without auto-commit (read-only or manual control)."""
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def ping_db() -> bool:
    """Health check — verify PostgreSQL connectivity."""
    try:
        engine = get_engine()
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            return result.scalar() == 1
    except Exception as exc:
        logger.error("Database health check failed: %s", exc)
        return False


async def init_db() -> None:
    """Initialize database — create tables if they don't exist (dev only).

    In production, schema is managed by Supabase CLI migrations.
    """
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables initialized (dev mode)")


async def close_db() -> None:
    """Dispose all engines — call on application shutdown."""
    global _engine, _session_factory
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _session_factory = None
    logger.info("Database engine disposed")


class RepositoryBase:
    """Base class for domain repositories using SQLAlchemy async session.

    Domain repositories should inherit and add domain-specific methods.
    Avoid creating a giant generic repository that hides domain rules.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def flush(self) -> None:
        await self.session.flush()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


