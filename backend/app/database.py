"""Database layer supporting both Motor (MongoDB, legacy) and SQLAlchemy async + asyncpg (PostgreSQL, new).

During the MongoDB→PostgreSQL migration, both databases coexist:
- Motor client: connects to existing MongoDB (used by routes not yet migrated)
- SQLAlchemy engine: connects to new PostgreSQL (used by migrated routes)

Connection string: SUPABASE_DB_URL (asyncpg format: postgresql+asyncpg://user:pass@host:5432/db)
If using Supabase transaction pooler (port 6543), set statement_cache_size=0.
"""

import logging
from typing import AsyncGenerator, Optional
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
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

logger = logging.getLogger(__name__)
settings = get_settings()

# ════════════════════════════════════════════════════════════════════════════════
# MOTOR / MONGODB (LEGACY — kept during migration for routes not yet migrated)
# ════════════════════════════════════════════════════════════════════════════════

_motor_client: Optional[AsyncIOMotorClient] = None
_motor_db: Optional[AsyncIOMotorDatabase] = None
_motor_collections: dict = {}


def get_motor_client() -> AsyncIOMotorClient:
    """Get or create the singleton AsyncIOMotorClient instance (legacy MongoDB)."""
    global _motor_client, _motor_db
    if _motor_client is None:
        _motor_client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,
            minPoolSize=settings.MONGODB_MIN_POOL_SIZE,
            maxIdleTimeMS=settings.MONGODB_MAX_IDLE_TIME_MS,
            serverSelectionTimeoutMS=15000,
            connectTimeoutMS=10000,
            socketTimeoutMS=30000,
        )
        _motor_db = _motor_client[settings.DATABASE_NAME]
    return _motor_client


def get_motor_db() -> AsyncIOMotorDatabase:
    """Get or create the singleton AsyncIOMotorDatabase instance (legacy MongoDB)."""
    if _motor_db is None:
        get_motor_client()
    return _motor_db


def get_motor_collection(name: str):
    """Get a Motor collection by name, caching it (legacy MongoDB)."""
    if name not in _motor_collections:
        _motor_collections[name] = get_motor_db()[name]
    return _motor_collections[name]


# Lazy collection proxies — backward compatibility for routes not yet migrated.
# These delegate to Motor collections. New code should use SQLAlchemy repositories.
class _LazyCollection:
    """Proxy that lazily resolves to a motor collection on first attribute access."""

    __slots__ = ("_name",)

    def __init__(self, name: str):
        object.__setattr__(self, "_name", name)

    def _resolve(self):
        return get_motor_collection(object.__getattribute__(self, "_name"))

    def __getattr__(self, item):
        return getattr(self._resolve(), item)

    def __call__(self):
        return self._resolve()

    def __repr__(self):
        return f"<_LazyCollection '{object.__getattribute__(self, '_name')}'>"


# ════════════════════════════════════════════════════════════════════════════════
# SQLALCHEMY ASYNC + ASYNCPG (POSTGRESQL — new, migrated routes use this)
# ════════════════════════════════════════════════════════════════════════════════

# Optional SUPABASE_DB_URL overrides MONGODB_URL for PostgreSQL
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
            logger.info("Detected Supabase transaction pooler — disabling prepared statement cache")

        _engine = create_async_engine(
            database_url,
            echo=False,
            pool_size=settings.MONGODB_MAX_POOL_SIZE if hasattr(settings, "MONGODB_MAX_POOL_SIZE") else 20,
            max_overflow=settings.MONGODB_MAX_POOL_SIZE if hasattr(settings, "MONGODB_MAX_POOL_SIZE") else 10,
            pool_timeout=30,
            pool_recycle=1800,
            **pool_kwargs,
        )
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


async def ping_motor() -> bool:
    """Health check — verify MongoDB connectivity."""
    try:
        client = get_motor_client()
        await client.admin.command("ping")
        return True
    except Exception as exc:
        logger.error("MongoDB health check failed: %s", exc)
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
    global _engine, _session_factory, _motor_client, _motor_db, _motor_collections
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _session_factory = None
    if _motor_client is not None:
        _motor_client.close()
        _motor_client = None
        _motor_db = None
        _motor_collections.clear()
    logger.info("Database engines disposed")


# Compatibility shims — get_client() and get_db() were the Motor accessors.
# During migration, these return Motor client/db so existing code continues to work.
def get_client():
    """Compatibility shim — returns the Motor client (legacy MongoDB)."""
    return get_motor_client()


def get_db():
    """Compatibility shim — returns the Motor database (legacy MongoDB)."""
    return get_motor_db()


def get_collection(name: str):
    """Compatibility shim — returns a Motor collection (legacy MongoDB)."""
    return get_motor_collection(name)


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


# ════════════════════════════════════════════════════════════════════════════════
# LAZY COLLECTION PROXIES (backward compatibility)
# ════════════════════════════════════════════════════════════════════════════════

users_collection = _LazyCollection("users")
interviews_collection = _LazyCollection("interviews")
resumes_collection = _LazyCollection("resumes")
aptitude_collection = _LazyCollection("aptitude_tests")
cover_letters_collection = _LazyCollection("cover_letters")
progress_collection = _LazyCollection("progress")
system_design_collection = _LazyCollection("system_design")
offers_collection = _LazyCollection("offers")
company_prep_collection = _LazyCollection("company_prep")
coding_challenges_collection = _LazyCollection("coding_challenges")
skill_graph_collection = _LazyCollection("skill_graphs")
gamification_collection = _LazyCollection("gamification")
gamification_events_collection = _LazyCollection("gamification_events")
usage_collection = _LazyCollection("usage_tracking")
predictions_collection = _LazyCollection("predictions")
prediction_outcomes_collection = _LazyCollection("prediction_outcomes")
curated_questions_collection = _LazyCollection("curated_questions")
question_answers_collection = _LazyCollection("question_answers")
company_mock_tests_collection = _LazyCollection("company_mock_tests")
alumni_experiences_collection = _LazyCollection("alumni_experiences")
placement_drives_collection = _LazyCollection("placement_drives")
career_profiles_collection = _LazyCollection("career_profiles")
practice_sessions_collection = _LazyCollection("practice_sessions")
mock_tests_collection = _LazyCollection("mock_tests")
trials_collection = _LazyCollection("trials")
discounts_collection = _LazyCollection("discounts")
solved_problems_collection = _LazyCollection("solved_problems")
submissions_collection = _LazyCollection("submissions")
learning_progress_collection = _LazyCollection("learning_progress")
analytics_events_collection = _LazyCollection("analytics_events")
analytics_rollups_collection = _LazyCollection("analytics_rollups")
service_metrics_collection = _LazyCollection("service_metrics")
applications_collection = _LazyCollection("applications")
study_groups_collection = _LazyCollection("study_groups")
contests_collection = _LazyCollection("contests")
contest_entries_collection = _LazyCollection("contest_entries")
playlists_collection = _LazyCollection("playlists")
discussions_collection = _LazyCollection("discussions")
community_posts_collection = _LazyCollection("community_posts")
battles_collection = _LazyCollection("battles")
bookmarks_collection = _LazyCollection("bookmarks")
notes_collection = _LazyCollection("notes")
aptitude_leaderboard_collection = _LazyCollection("aptitude_leaderboard")
aptitude_tests_collection = _LazyCollection("aptitude_tests")
system_design_leaderboard_collection = _LazyCollection("system_design_leaderboard")
system_design_tests_collection = _LazyCollection("system_design_tests")
matchmaking_queue_collection = _LazyCollection("matchmaking_queue")
ranks_collection = _LazyCollection("ranks")
daily_challenges_users_collection = _LazyCollection("daily_challenges_users")
generated_projects_collection = _LazyCollection("generated_projects")
learning_modules_collection = _LazyCollection("learning_modules")
user_learning_progress_collection = _LazyCollection("user_learning_progress")
interview_bookings_collection = _LazyCollection("interview_bookings")
language_modules_collection = _LazyCollection("language_modules")
language_levels_collection = _LazyCollection("language_levels")
language_progress_collection = _LazyCollection("language_progress")
content_modules_collection = _LazyCollection("content_modules")
assignments_collection = _LazyCollection("assignments")
assignment_submissions_collection = _LazyCollection("assignment_submissions")
question_explanations_collection = _LazyCollection("question_explanations")
interview_chat_sessions_collection = _LazyCollection("interview_chat_sessions")
user_deadlines_collection = _LazyCollection("user_deadlines")
payments_collection = _LazyCollection("payments")
revenue_events_collection = _LazyCollection("revenue_events")
billing_metrics_collection = _LazyCollection("billing_metrics")
coupons_collection = _LazyCollection("coupons")
referrals_collection = _LazyCollection("referrals")
chat_messages_collection = _LazyCollection("chat_messages")
gd_rooms_collection = _LazyCollection("gd_rooms")
gd_ratings_collection = _LazyCollection("gd_ratings")
cgpa_calculations_collection = _LazyCollection("cgpa_calculations")
drive_trackers_collection = _LazyCollection("drive_trackers")
peer_reviews_collection = _LazyCollection("peer_reviews")
study_squads_collection = _LazyCollection("study_squads")
achievements_collection = _LazyCollection("achievements")
shares_collection = _LazyCollection("shares")
pulse_battles_collection = _LazyCollection("pulse_battles")
pulse_daily_collection = _LazyCollection("pulse_daily")
debug_logs_collection = _LazyCollection("debug_logs")
srs_collection = _LazyCollection("srs_states")
srs_cards_collection = _LazyCollection("srs_cards")
audit_logs_collection = _LazyCollection("audit_logs")
friend_requests_collection = _LazyCollection("friend_requests")
friends_collection = _LazyCollection("friends")
oa_sessions_collection = _LazyCollection("oa_sessions")
integrity_events_collection = _LazyCollection("integrity_events")
daily_quests_collection = _LazyCollection("daily_quests")
content_tranches_collection = _LazyCollection("content_tranches")
exam_memories_collection = _LazyCollection("exam_memories")
invoices_collection = _LazyCollection("invoices")
learning_events_collection = _LazyCollection("learning_events")
gamification_events_collection = _LazyCollection("gamification_events")
question_reports_collection = _LazyCollection("question_reports")
repair_missions_collection = _LazyCollection("repair_missions")
season_xp_collection = _LazyCollection("season_xp")
served_quarantine_collection = _LazyCollection("served_quarantine")
user_company_tracks_collection = _LazyCollection("user_company_tracks")
user_learning_paths_collection = _LazyCollection("user_learning_paths")
user_weaknesses_collection = _LazyCollection("user_weaknesses")
