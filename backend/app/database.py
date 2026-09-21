"""Async MongoDB database layer using Motor with lazy collection proxies.

Provides:
- Connection pooling via AsyncIOMotorClient
- Lazy collection resolution to avoid import-time DB access
- Index creation for 50+ collections
- Connection health checking (ping)
"""
import asyncio
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import get_settings
from app.services.cache import cache

logger = logging.getLogger(__name__)
settings = get_settings()

_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None
_collections: dict = {}


class _LazyCollection:
    """Proxy that lazily resolves to a motor collection on first attribute access.

    Supports both `collection.find_one(...)` and `collection()` call styles.
    Also supports `collection[key]`, `del collection[key]`, and `key in collection`.

    Args:
        name: The MongoDB collection name to proxy.
    """
    __slots__ = ("_name",)

    _KNOWN_METHODS = frozenset({
        "find_one", "find", "insert_one", "insert_many", "update_one", "update_many",
        "replace_one", "delete_one", "delete_many", "count_documents",
        "estimated_document_count", "aggregate", "watch", "bulk_write",
        "create_index", "create_indexes", "drop_index", "drop_indexes",
        "index_information", "list_indexes", "rename", "find_one_and_delete",
        "find_one_and_replace", "find_one_and_update", "distinct",
        "map_reduce", "group", "inline_map_reduce", "options",
    })

    def __init__(self, name: str):
        object.__setattr__(self, "_name", name)

    def _resolve(self):
        """Resolve the lazy proxy to the actual Motor collection.

        Returns:
            AsyncIOMotorCollection: The resolved collection from the current database.
        """
        name = object.__getattribute__(self, "_name")
        return get_db()[name]

    def __getattr__(self, item):
        """Proxy attribute access to the underlying Motor collection.

        Known Motor collection methods are validated upfront to catch typos.
        Unknown attributes raise AttributeError with a helpful suggestion.

        Args:
            item: Attribute name to forward.

        Returns:
            Any: The attribute from the resolved collection.

        Raises:
            AttributeError: If the attribute is not found, with a typo suggestion.
        """
        if item in self._KNOWN_METHODS or item.startswith("_"):
            return getattr(self._resolve(), item)

        resolved = self._resolve()
        if hasattr(resolved, item):
            return getattr(resolved, item)

        suggestions = [m for m in self._KNOWN_METHODS if m.startswith(item[:3]) and m != item]
        suggestion = f" Did you mean {suggestions[0]}?" if suggestions else ""
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{item}'.{suggestion}"
        )

    def __setattr__(self, name, value):
        """Prevent setting attributes on the proxy except for the internal name.

        Args:
            name: Attribute name.
            value: Value to set.

        Raises:
            AttributeError: If trying to set any attribute other than '_name'.
        """
        if name == "_name":
            object.__setattr__(self, "_name", value)
        else:
            raise AttributeError(f"Cannot set attribute '{name}' on _LazyCollection proxy")

    def __call__(self):
        """Allow `collection()` — returns the underlying motor collection.

        Returns:
            AsyncIOMotorCollection: The resolved Motor collection.
        """
        return self._resolve()

    def __getitem__(self, key):
        """Support dictionary-style access to collection documents.

        Args:
            key: Document key or index.

        Returns:
            Any: The value at the given key in the collection.
        """
        return self._resolve()[key]

    def __setitem__(self, key, value):
        """Support dictionary-style assignment to collection documents.

        Args:
            key: Document key or index.
            value: Value to set.
        """
        self._resolve()[key] = value

    def __delitem__(self, key):
        """Support dictionary-style deletion of collection documents.

        Args:
            key: Document key or index to delete.

        Raises:
            KeyError: If the key does not exist in the collection.
        """
        del self._resolve()[key]

    def __contains__(self, key):
        """Support `in` operator for collection membership checks.

        Args:
            key: Key or value to check for existence.

        Returns:
            bool: True if the key exists in the collection, False otherwise.
        """
        return key in self._resolve()

    def __repr__(self):
        """Return a human-readable representation of the lazy collection.

        Returns:
            str: Representation string including the collection name.
        """
        return f"<_LazyCollection '{object.__getattribute__(self, '_name')}'>"

    def __dir__(self):
        """Return available attributes including known Motor methods for IDE support.

        Returns:
            list: Sorted list of known method names plus standard Python attributes.
        """
        return sorted(set(super().__dir__()) | self._KNOWN_METHODS)


def get_client() -> AsyncIOMotorClient:
    """Get or create the singleton AsyncIOMotorClient instance.

    Validates the existing client's I/O loop; recreates the client if the loop
    is closed or the client was never initialized. Uses connection pool settings
    from application config.

    Returns:
        AsyncIOMotorClient: The active Motor database client.
    """
    global _client, _db
    if _client is not None:
        try:
            loop = _client.get_io_loop()
            if loop.is_closed():
                _client = None
                _db = None
                _collections.clear()
            else:
                # Recreate if the running loop differs from the client's IO loop
                # (e.g. pytest-asyncio uses a fresh loop per test). Safe for
                # production where uvicorn runs a single long-lived loop.
                try:
                    if loop is not asyncio.get_running_loop():
                        _client = None
                        _db = None
                        _collections.clear()
                except RuntimeError:
                    pass  # no running loop; keep existing client
        except Exception:
            _client = None
            _db = None
            _collections.clear()

    if _client is None:
        _client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,
            minPoolSize=settings.MONGODB_MIN_POOL_SIZE,
            maxIdleTimeMS=settings.MONGODB_MAX_IDLE_TIME_MS,
            serverSelectionTimeoutMS=15000,
            connectTimeoutMS=10000,
            socketTimeoutMS=30000,
        )
    return _client


def get_db() -> AsyncIOMotorDatabase:
    """Get or create the singleton AsyncIOMotorDatabase instance.

    Returns:
        AsyncIOMotorDatabase: The active Motor database handle.
    """
    global _db
    client = get_client()
    if _db is None:
        _db = client[settings.DATABASE_NAME]
    return _db


def get_collection(name: str):
    """Get a Motor collection by name, caching it for future calls.

    Args:
        name: The name of the MongoDB collection.

    Returns:
        AsyncIOMotorCollection: The requested collection handle.
    """
    if name not in _collections:
        _collections[name] = get_db()[name]
    return _collections[name]


# Lazy collection proxies — work as both `collection.find_one()` and `collection()`
users_collection = _LazyCollection("users")
interviews_collection = _LazyCollection("interviews")
resumes_collection = _LazyCollection("resumes")
aptitude_collection = _LazyCollection("aptitude_tests")
progress_collection = _LazyCollection("progress")
system_design_collection = _LazyCollection("system_design")
coding_challenges_collection = _LazyCollection("coding_challenges")
skill_graph_collection = _LazyCollection("skill_graphs")
gamification_collection = _LazyCollection("gamification")
usage_collection = _LazyCollection("usage_tracking")
predictions_collection = _LazyCollection("predictions")
question_answers_collection = _LazyCollection("question_answers")
company_mock_tests_collection = _LazyCollection("company_mock_tests")
alumni_experiences_collection = _LazyCollection("alumni_experiences")
placement_drives_collection = _LazyCollection("placement_drives")
career_profiles_collection = _LazyCollection("career_profiles")
practice_sessions_collection = _LazyCollection("practice_sessions")
trials_collection = _LazyCollection("trials")
discounts_collection = _LazyCollection("discounts")
solved_problems_collection = _LazyCollection("solved_problems")
submissions_collection = _LazyCollection("submissions")
learning_progress_collection = _LazyCollection("learning_progress")
user_question_state_collection = _LazyCollection("user_question_state")
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
bookmarks_collection = _LazyCollection("bookmarks")
notes_collection = _LazyCollection("notes")
aptitude_leaderboard_collection = _LazyCollection("aptitude_leaderboard")
aptitude_tests_collection = _LazyCollection("aptitude_tests")
system_design_leaderboard_collection = _LazyCollection("system_design_leaderboard")
system_design_tests_collection = _LazyCollection("system_design_tests")
daily_challenges_users_collection = _LazyCollection("daily_challenges_users")
generated_projects_collection = _LazyCollection("generated_projects")
learning_modules_collection = _LazyCollection("learning_modules")
user_learning_progress_collection = _LazyCollection("user_learning_progress")
interview_bookings_collection = _LazyCollection("interview_bookings")
content_modules_collection = _LazyCollection("content_modules")
assignments_collection = _LazyCollection("assignments")
assignment_submissions_collection = _LazyCollection("assignment_submissions")
question_explanations_collection = _LazyCollection("question_explanations")
interview_chat_sessions_collection = _LazyCollection("interview_chat_sessions")
payments_collection = _LazyCollection("payments")
revenue_events_collection = _LazyCollection("revenue_events")
billing_metrics_collection = _LazyCollection("billing_metrics")
coupons_collection = _LazyCollection("coupons")
referrals_collection = _LazyCollection("referrals")
drive_trackers_collection = _LazyCollection("drive_trackers")
srs_collection = _LazyCollection("srs_states")
srs_cards_collection = _LazyCollection("srs_cards")
audit_logs_collection = _LazyCollection("audit_logs")
oa_sessions_collection = _LazyCollection("oa_sessions")
integrity_events_collection = _LazyCollection("integrity_events")
repair_missions_collection = _LazyCollection("repair_missions")
user_weaknesses_collection = _LazyCollection("user_weaknesses")
user_learning_paths_collection = _LazyCollection("user_learning_paths")
user_company_tracks_collection = _LazyCollection("user_company_tracks")
learning_events_collection = _LazyCollection("learning_events")
gamification_events_collection = _LazyCollection("gamification_events")
question_reports_collection = _LazyCollection("question_reports")
served_quarantine_collection = _LazyCollection("served_quarantine")
invoices_collection = _LazyCollection("invoices")
content_tranches_collection = _LazyCollection("content_tranches")
# Crowd-sourced exam memory submissions (student-attested question recollections).
# Questions students report are student state, never question-bank content —
# approved items are promoted to the file-based bank via the trust pipeline
# (see routes/exam_memories.py promote). Threshold: 5 independent reports = verified_crowd.
exam_memories_collection = _LazyCollection("exam_memories")


async def init_db():
    db = get_db()

    async def _safe_create_index(collection, keys, **kwargs):
        """Create an index, silently ignoring conflicts with existing indexes."""
        try:
            await collection.create_index(keys, **kwargs)
        except Exception as e:
            msg = str(e).lower()
            if ("already exists" in msg
                    or "indexoptionsconflict" in msg
                    or "indexkeyspecsconflict" in msg
                    or "same name" in msg):
                pass  # Index exists with different options — safe to ignore
            elif "duplicate key" in msg or "e11000" in msg:
                logger.warning("Index build skipped due to duplicate key conflict: %s", e)
            else:
                raise

    # NOTE: uid index is managed separately via migrations.sparse_uid_index()
    # to avoid E11000 conflict when all existing users have uid=null.
    # Authentication uses email + password, not uid.
    await _safe_create_index(db["users"], "email", unique=True)
    await _safe_create_index(db["users"], "plan")
    await _safe_create_index(db["users"], "created_at")
    await _safe_create_index(db["users"], [("email", 1), ("plan", 1)])

    await _safe_create_index(db["interviews"], "user_id")
    await _safe_create_index(db["interviews"], [("user_id", 1), ("created_at", -1)])
    await _safe_create_index(db["interviews"], "status")
    await _safe_create_index(db["interviews"], [("user_id", 1), ("status", 1)])

    await _safe_create_index(db["resumes"], "user_id")
    await _safe_create_index(db["resumes"], [("user_id", 1), ("created_at", -1)])
    await _safe_create_index(db["resumes"], "ats_score")

    await _safe_create_index(db["aptitude_tests"], "user_id")
    await _safe_create_index(db["aptitude_tests"], [("user_id", 1), ("created_at", -1)])
    await _safe_create_index(db["aptitude_tests"], "category")
    await _safe_create_index(db["aptitude_tests"], "status")
    await _safe_create_index(db["aptitude_tests"], [("user_id", 1), ("category", 1)])

    await _safe_create_index(db["system_design"], "user_id")
    await _safe_create_index(db["system_design"], [("user_id", 1), ("created_at", -1)])
    await _safe_create_index(db["system_design"], "difficulty")

    await _safe_create_index(db["coding_challenges"], "user_id")
    await _safe_create_index(db["coding_challenges"], [("user_id", 1), ("created_at", -1)])
    await _safe_create_index(db["coding_challenges"], "topic")
    await _safe_create_index(db["coding_challenges"], "difficulty")
    await _safe_create_index(db["coding_challenges"], [("topic", 1), ("difficulty", 1)])

    await _safe_create_index(db["skill_graphs"], "user_id", unique=True)

    await _safe_create_index(db["gamification"], "user_id", unique=True)
    await _safe_create_index(db["gamification"], [("diamonds", -1)])
    await _safe_create_index(db["gamification"], [("level", -1), ("diamonds", -1)])

    await _safe_create_index(db["progress"], "user_id")
    await _safe_create_index(db["progress"], [("user_id", 1), ("topic", 1)])

    # Learning paths and company tracks
    await _safe_create_index(db["user_learning_paths"], [("user_id", 1), ("path_id", 1)], unique=True)
    await _safe_create_index(db["user_company_tracks"], [("user_id", 1), ("track_id", 1)], unique=True)
    await _safe_create_index(db["user_learning_paths"], "user_id")
    await _safe_create_index(db["user_company_tracks"], "user_id")
    await _safe_create_index(db["user_learning_paths"], [("user_id", 1), ("completed", 1)])
    await _safe_create_index(db["user_company_tracks"], [("user_id", 1), ("completed", 1)])

    await _safe_create_index(db["usage_tracking"], "user_id")
    await _safe_create_index(db["usage_tracking"], [("user_id", 1), ("feature", 1)])
    await _safe_create_index(db["usage_tracking"], [("user_id", 1), ("period", 1)])

    await _safe_create_index(db["predictions"], "user_id")
    await _safe_create_index(db["predictions"], [("user_id", 1), ("created_at", -1)])

    await _safe_create_index(db["question_answers"], "user_id")
    await _safe_create_index(db["question_answers"], [("user_id", 1), ("question_id", 1)])
    await _safe_create_index(db["question_answers"], [("user_id", 1), ("created_at", -1)])
    await _safe_create_index(db["question_answers"], "question_id")

    await _safe_create_index(db["company_mock_tests"], "user_id")
    await _safe_create_index(db["company_mock_tests"], [("user_id", 1), ("company", 1)])
    await _safe_create_index(db["company_mock_tests"], [("user_id", 1), ("created_at", -1)])
    await _safe_create_index(db["company_mock_tests"], "status")

    await _safe_create_index(db["alumni_experiences"], "company")
    await _safe_create_index(db["alumni_experiences"], [("company", 1), ("year", -1)])
    await _safe_create_index(db["alumni_experiences"], "role")

    await _safe_create_index(db["placement_drives"], "company")
    await _safe_create_index(db["placement_drives"], "deadline")
    await _safe_create_index(db["placement_drives"], [("is_active", 1), ("deadline", 1)])
    await _safe_create_index(db["placement_drives"], "tier")

    await _safe_create_index(db["career_profiles"], "user_id", unique=True)
    await _safe_create_index(db["career_profiles"], "updated_at")

    await _safe_create_index(db["practice_sessions"], "user_id")
    await _safe_create_index(db["practice_sessions"], [("user_id", 1), ("created_at", -1)])
    await _safe_create_index(db["practice_sessions"], "status")

    # OA simulation sessions
    await _safe_create_index(db["oa_sessions"], "user_id")
    await _safe_create_index(db["oa_sessions"], [("user_id", 1), ("created_at", -1)])
    await _safe_create_index(db["oa_sessions"], "status")
    await _safe_create_index(db["oa_sessions"], [("user_id", 1), ("company", 1)])

    # Exam memories (crowd-sourced recollection loop)
    await _safe_create_index(db["exam_memories"], [("fingerprint", 1)])
    await _safe_create_index(db["exam_memories"], [("user_id", 1), ("created_at", -1)])
    await _safe_create_index(db["exam_memories"], [("status", 1), ("created_at", -1)])
    await _safe_create_index(db["exam_memories"], [("fingerprint", 1), ("status", 1)])

    # Integrity events (opt-in browser signals)
    await _safe_create_index(db["integrity_events"], [("user_id", 1), ("session_id", 1)])
    await _safe_create_index(db["integrity_events"], "created_at", expireAfterSeconds=60 * 60 * 24 * 30)

    # Repair missions (closed-loop OA -> repair -> retest)
    await _safe_create_index(db["repair_missions"], [("user_id", 1), ("status", 1)])
    await _safe_create_index(db["repair_missions"], [("user_id", 1), ("created_at", -1)])

    # User weaknesses (misconception-tagged repair loop)
    await _safe_create_index(db["user_weaknesses"], [("user_id", 1), ("misconception_tag", 1)], unique=True)
    await _safe_create_index(db["user_weaknesses"], [("user_id", 1), ("last_triggered", -1)])

    await _safe_create_index(db["trials"], "user_id")
    await _safe_create_index(db["trials"], [("user_id", 1), ("status", 1)])

    await _safe_create_index(db["discounts"], "user_id")
    await _safe_create_index(db["discounts"], [("user_id", 1), ("type", 1), ("status", 1)])

    await _safe_create_index(db["solved_problems"], "user_id")
    await _safe_create_index(db["solved_problems"], [("user_id", 1), ("question_id", 1)], unique=True)
    await _safe_create_index(db["solved_problems"], [("user_id", 1), ("solved_at", -1)])

    await _safe_create_index(db["submissions"], "user_id")
    await _safe_create_index(db["submissions"], [("user_id", 1), ("question_id", 1)])
    await _safe_create_index(db["submissions"], [("user_id", 1), ("submitted_at", -1)])
    await _safe_create_index(db["submissions"], "status")
    await _safe_create_index(db["submissions"], [("question_id", 1), ("status", 1)])

    await _safe_create_index(db["cards"], "user_id")
    await _safe_create_index(db["cards"], [("user_id", 1), ("rarity", 1)])
    await _safe_create_index(db["cards"], [("user_id", 1), ("topic", 1)])
    await _safe_create_index(db["cards"], [("user_id", 1), ("question_id", 1)])

    await _safe_create_index(db["learning_progress"], "user_id", unique=True)
    await _safe_create_index(db["learning_progress"], "total_xp")
    await _safe_create_index(db["learning_progress"], "daily_date")
    await _safe_create_index(db["learning_progress"], "daily_goal_bonus_date")
    await _safe_create_index(db["learning_progress"], "updated_at")

    await _safe_create_index(db["analytics_events"], "event")
    await _safe_create_index(db["analytics_events"], "date")
    # TTL index for auto-cleanup (180 days)
    await _safe_create_index(db["analytics_events"], [("timestamp_dt", 1)], expireAfterSeconds=60 * 60 * 24 * 180)
    await _safe_create_index(db["analytics_events"], [("event", 1), ("date", 1)])
    await _safe_create_index(db["analytics_events"], [("path", 1), ("date", 1)])
    await _safe_create_index(db["analytics_events"], [("event", 1), ("timestamp_dt", -1)])

    await _safe_create_index(db["analytics_rollups"], [("bucket", 1), ("date", 1)], unique=True)
    await _safe_create_index(db["analytics_rollups"], "date")
    # TTL indexes for transient data (auto-cleanup to save storage)
    await _safe_create_index(db["submissions"], [("submitted_at", 1)], expireAfterSeconds=60 * 60 * 24 * 90)
    await _safe_create_index(db["practice_sessions"], [("created_at", 1)], expireAfterSeconds=60 * 60 * 24 * 90)
    await _safe_create_index(db["service_metrics"], [("timestamp", 1)], expireAfterSeconds=60 * 60 * 24 * 30)

    # Canonical Learning Events — the single longitudinal evidence layer.
    # Every meaningful learning/assessment action (lesson, practice, OA,
    # interview, repair, retest, SRS) emits one normalized event here.
    await _safe_create_index(db["learning_events"], [("user_id", 1), ("timestamp", -1)])
    await _safe_create_index(db["learning_events"], [("user_id", 1), ("skill_id", 1)])
    await _safe_create_index(db["learning_events"], [("user_id", 1), ("activity_type", 1)])
    await _safe_create_index(db["learning_events"], [("user_id", 1), ("source", 1)])
    await _safe_create_index(db["learning_events"], [("skill_id", 1), ("passed", 1)])
    await _safe_create_index(db["learning_events"], [("diagnosis_codes", 1)])

    # Immutable reward ledger: every Diamonds award records inputs + outputs so
    # profile.diamonds == sum(ledger.xp_awarded) is checkable (reconcile script).
    # No TTL — audit history must not evaporate.
    await _safe_create_index(db["gamification_events"], [("user_id", 1), ("created_at", -1)])
    await _safe_create_index(db["gamification_events"], [("user_id", 1), ("activity_id", 1)])

    # File-store migration (§1.1): reports, quarantine decisions, invoices,
    # and tranche workflow state live in Mongo (survive restarts); the JSON
    # files under app/data/ are seed/export artifacts only.
    await _safe_create_index(db["question_reports"], [("user_id", 1), ("day", 1)])
    await _safe_create_index(db["question_reports"], [("user_id", 1), ("question_id", 1)], unique=True)
    await _safe_create_index(db["question_reports"], [("question_id", 1)])
    await _safe_create_index(db["served_quarantine"], "question_id", unique=True)
    await _safe_create_index(db["invoices"], "invoice_id", unique=True)
    await _safe_create_index(db["invoices"], [("customer.user_id", 1), ("created_at", -1)])
    await _safe_create_index(db["content_tranches"], "status")

    await _safe_create_index(db["analytics_rollups"], "bucket")

    await _safe_create_index(db["community_posts"], "user_id")
    await _safe_create_index(db["community_posts"], [("created_at", -1)])
    await _safe_create_index(db["community_posts"], [("user_id", 1), ("created_at", -1)])

    # Daily challenges users indexes
    await _safe_create_index(db["daily_challenges_users"], "user_id", unique=True)
    await _safe_create_index(db["daily_challenges_users"], [("total_xp_earned", -1)])
    await _safe_create_index(db["daily_challenges_users"], [("enrolled", 1), ("current_day", 1)])

    # Generated projects indexes
    await _safe_create_index(db["generated_projects"], "user_id")
    await _safe_create_index(db["generated_projects"], [("user_id", 1), ("created_at", -1)])
    await _safe_create_index(db["generated_projects"], "project_id", unique=True)

    # User honor field index for leaderboard
    await _safe_create_index(db["users"], [("honor", -1)])

    # Learning modules indexes
    await _safe_create_index(db["learning_modules"], "question_id", unique=True)
    await _safe_create_index(db["learning_modules"], "difficulty")
    await _safe_create_index(db["learning_modules"], "topic")
    await _safe_create_index(db["learning_modules"], "company_tags")

    # User learning progress indexes
    await _safe_create_index(db["user_learning_progress"], [("user_id", 1), ("module_id", 1)], unique=True)
    await _safe_create_index(db["user_learning_progress"], "user_id")
    await _safe_create_index(db["user_learning_progress"], "completed_at")

    await _safe_create_index(db["interview_bookings"], "user_id")
    await _safe_create_index(db["interview_bookings"], [("user_id", 1), ("scheduled_at", -1)])
    await _safe_create_index(db["interview_bookings"], "status")
    await _safe_create_index(db["interview_bookings"], [("user_id", 1), ("status", 1)])
    await _safe_create_index(db["interview_bookings"], [("user_id", 1), ("scheduled_at", 1), ("status", 1)])

    # Content modules + assignments indexes
    await _safe_create_index(db["content_modules"], [("order", 1)])
    await _safe_create_index(db["content_modules"], "category")
    await _safe_create_index(db["content_modules"], "difficulty")

    await _safe_create_index(db["assignments"], [("created_at", -1)])
    await _safe_create_index(db["assignments"], "assigned_to")
    await _safe_create_index(db["assignments"], "content_id")

    await _safe_create_index(db["assignment_submissions"], [("assignment_id", 1), ("user_id", 1)], unique=True)
    await _safe_create_index(db["assignment_submissions"], "user_id")
    await _safe_create_index(db["assignment_submissions"], "assignment_id")
    await _safe_create_index(db["assignment_submissions"], "status")
    await _safe_create_index(db["assignment_submissions"], [("assignment_id", 1), ("status", 1)])

    # Audit logs — TTL 1 year for compliance
    await _safe_create_index(db["audit_logs"], [("timestamp", -1)])
    await _safe_create_index(db["audit_logs"], [("user_id", 1), ("timestamp", -1)])
    await _safe_create_index(db["audit_logs"], [("action", 1), ("timestamp", -1)])

    # SRS cards — problem-based spaced repetition
    await _safe_create_index(db["srs_cards"], "user_id")
    await _safe_create_index(db["srs_cards"], [("user_id", 1), ("problem_id", 1)], unique=True)
    await _safe_create_index(db["srs_cards"], [("user_id", 1), ("next_review", 1)])
    await _safe_create_index(db["srs_cards"], [("user_id", 1), ("difficulty", 1)])
    await _safe_create_index(db["srs_cards"], [("user_id", 1), ("next_review", 1), ("difficulty", 1)])

    # Skill mastery — per-skill tracking
    await _safe_create_index(db["skill_graphs"], [("user_id", 1), ("topic", 1), ("sub_topic", 1)], unique=True)
    await _safe_create_index(db["skill_graphs"], [("user_id", 1), ("current_level", -1)])
    await _safe_create_index(db["skill_graphs"], [("user_id", 1), ("last_practiced", -1)])

    # Friend system — unique chat IDs + friend graph
    await _safe_create_index(db["users"], "uid", unique=True, sparse=True)

    logger.info("Database indexes created successfully")


async def close_db():
    """Close the Motor client and reset all cached state.

    Clears the client, database handle, and collection proxy cache.
    Logs the closure for observability.
    """
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
        _collections.clear()
        logger.info("Database connection closed")


async def ping_db() -> bool:
    """Check database connectivity by sending an admin ping command.

    Returns:
        bool: True if the database responds to ping, False otherwise.
    """
    try:
        client = get_client()
        await client.admin.command("ping")
        return True
    except Exception as e:
        logger.error(f"Database ping failed: {e}")
        return False