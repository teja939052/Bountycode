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

# ═════════════════════════════════════════════════════════════════════════════════
# POSTGRESQL — PostgreSQL (PRIMARY — the only database backend)
# ════════════════════════════════════════════════════════════════════════════════

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
    return "postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/bountycode"


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


# Compatibility wrapper — get_collection() routes to PostgreSQL repositories
# via the compat adapter. This is a transitional shim; routes should be
# migrated to use repositories directly via dependency injection.
# No Motor/MongoDB is involved — all operations go to PostgreSQL tables.
def get_collection(name: str):
    """Get a PostgreSQL-backed collection wrapper by name.

    This is a transitional compatibility shim. Routes should migrate to using
    repositories directly via dependency injection.
    No Motor/MongoDB is involved — all operations go to PostgreSQL tables.
    """
    from app.compat.mongo_adapter import MongoCompatCollection

    return MongoCompatCollection(name)


# Collection name aliases for backward compatibility with existing route imports.
# These are PostgreSQL-backed wrappers via get_collection(). Routes should
# migrate to using repositories directly.
users_collection = get_collection("users")
interviews_collection = get_collection("interviews")
interview_bookings_collection = get_collection("interview_bookings")
interview_sessions_collection = get_collection("interview_sessions")
oa_sessions_collection = get_collection("oa_sessions")
coding_challenges_collection = get_collection("coding_challenges")
submissions_collection = get_collection("submissions")
resumes_collection = get_collection("resumes")
aptitude_tests_collection = get_collection("aptitude_tests")
cover_letters_collection = get_collection("cover_letters")
progress_collection = get_collection("progress")
system_design_collection = get_collection("system_design")
offers_collection = get_collection("offers")
company_prep_collection = get_collection("company_prep")
skill_graph_collection = get_collection("skill_graphs")
gamification_collection = get_collection("gamification")
gamification_events_collection = get_collection("gamification_events")
usage_collection = get_collection("usage_tracking")
predictions_collection = get_collection("predictions")
prediction_outcomes_collection = get_collection("prediction_outcomes")
curated_questions_collection = get_collection("curated_questions")
question_answers_collection = get_collection("question_answers")
company_mock_tests_collection = get_collection("company_mock_tests")
alumni_experiences_collection = get_collection("alumni_experiences")
placement_drives_collection = get_collection("placement_drives")
career_profiles_collection = get_collection("career_profiles")
practice_sessions_collection = get_collection("practice_sessions")
mock_tests_collection = get_collection("mock_tests")
trials_collection = get_collection("trials")
discounts_collection = get_collection("discounts")
solved_problems_collection = get_collection("solved_problems")
learning_progress_collection = get_collection("learning_progress")
analytics_events_collection = get_collection("analytics_events")
analytics_rollups_collection = get_collection("analytics_rollups")
service_metrics_collection = get_collection("service_metrics")
applications_collection = get_collection("applications")
study_groups_collection = get_collection("study_groups")
contests_collection = get_collection("contests")
contest_entries_collection = get_collection("contest_entries")
playlists_collection = get_collection("playlists")
discussions_collection = get_collection("discussions")
community_posts_collection = get_collection("community_posts")
battles_collection = get_collection("battles")
bookmarks_collection = get_collection("bookmarks")
notes_collection = get_collection("notes")
aptitude_leaderboard_collection = get_collection("aptitude_leaderboard")
system_design_leaderboard_collection = get_collection("system_design_leaderboard")
system_design_tests_collection = get_collection("system_design_tests")
matchmaking_queue_collection = get_collection("matchmaking_queue")
ranks_collection = get_collection("ranks")
daily_challenges_users_collection = get_collection("daily_challenges_users")
generated_projects_collection = get_collection("generated_projects")
learning_modules_collection = get_collection("learning_modules")
user_learning_progress_collection = get_collection("user_learning_progress")
language_modules_collection = get_collection("language_modules")
language_levels_collection = get_collection("language_levels")
language_progress_collection = get_collection("language_progress")
content_modules_collection = get_collection("content_modules")
assignments_collection = get_collection("assignments")
assignment_submissions_collection = get_collection("assignment_submissions")
question_explanations_collection = get_collection("question_explanations")
interview_chat_sessions_collection = get_collection("interview_chat_sessions")
user_deadlines_collection = get_collection("user_deadlines")
payments_collection = get_collection("payments")
revenue_events_collection = get_collection("revenue_events")
billing_metrics_collection = get_collection("billing_metrics")
coupons_collection = get_collection("coupons")
referrals_collection = get_collection("referrals")
chat_messages_collection = get_collection("chat_messages")
gd_rooms_collection = get_collection("gd_rooms")
gd_ratings_collection = get_collection("gd_ratings")
cgpa_calculations_collection = get_collection("cgpa_calculations")
drive_trackers_collection = get_collection("drive_trackers")
peer_reviews_collection = get_collection("peer_reviews")
study_squads_collection = get_collection("study_squads")
achievements_collection = get_collection("achievements")
shares_collection = get_collection("shares")
pulse_battles_collection = get_collection("pulse_battles")
pulse_daily_collection = get_collection("pulse_daily")
debug_logs_collection = get_collection("debug_logs")
srs_collection = get_collection("srs_states")
srs_cards_collection = get_collection("srs_cards")
audit_logs_collection = get_collection("audit_logs")
friend_requests_collection = get_collection("friend_requests")
friends_collection = get_collection("friends")
integrity_events_collection = get_collection("integrity_events")
daily_quests_collection = get_collection("daily_quests")
content_tranches_collection = get_collection("content_tranches")
exam_memories_collection = get_collection("exam_memories")
invoices_collection = get_collection("invoices")
learning_events_collection = get_collection("learning_events")
question_reports_collection = get_collection("question_reports")
repair_missions_collection = get_collection("repair_missions")
season_xp_collection = get_collection("season_xp")
served_quarantine_collection = get_collection("served_quarantine")
user_company_tracks_collection = get_collection("user_company_tracks")
user_learning_paths_collection = get_collection("user_learning_paths")
user_weaknesses_collection = get_collection("user_weaknesses")


# Compatibility wrapper — get_collection() routes to PostgreSQL repositories
# via the compat adapter. This is a transitional shim; routes should be
# migrated to use repositories directly via dependency injection.
# No Motor/MongoDB is involved — all operations go to PostgreSQL tables.
def get_collection(name: str):
    """Get a PostgreSQL-backed collection wrapper by name.

    This is a transitional compatibility shim. Routes should migrate to using
    repositories directly via dependency injection.
    No Motor/MongoDB is involved — all operations go to PostgreSQL tables.
    """
    from app.compat.mongo_adapter import MongoCompatCollection

    return MongoCompatCollection(name)


# Compatibility shims for code that imports get_client, get_db, etc.
# These return PostgreSQL-backed wrappers via get_collection.
def get_client():
    """Compatibility shim — returns a wrapper that supports [db_name] indexing
    to access PostgreSQL-backed collections."""
    return _MongoClientCompat()


def get_db():
    """Compatibility shim — returns a wrapper that provides collection access."""
    return get_collection("users")


def get_motor_client():
    """Compatibility shim — returns a wrapper that supports [db_name] indexing."""
    return get_client()


def get_motor_db():
    """Compatibility shim — returns a wrapper that provides collection access."""
    return get_db()


def get_motor_collection(name: str):
    """Compatibility shim — returns a PostgreSQL-backed collection wrapper."""
    return get_collection(name)


class _MongoClientCompat:
    """Wrapper that mimics Motor client's [db_name] indexing."""

    def __getitem__(self, db_name: str):
        return _MongoDatabaseCompat(db_name)


class _MongoDatabaseCompat:
    """Wrapper that mimics Motor database's collection access."""

    def __init__(self, name: str):
        self._name = name

    def __getitem__(self, collection_name: str):
        return get_collection(collection_name)

    def __call__(self, collection_name: str):
        return get_collection(collection_name)


# Module-level __getattr__ for any collection name not explicitly defined above.
# Routes that import e.g. `from app.database import aptitude_collection` will
# get a PostgreSQL-backed wrapper via get_collection().
def __getattr__(name: str):
    if name.startswith("_"):
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return get_collection(name)
