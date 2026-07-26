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
    """
    __slots__ = ("_name",)

    def __init__(self, name: str):
        object.__setattr__(self, "_name", name)

    def _resolve(self):
        name = object.__getattribute__(self, "_name")
        if name not in _collections:
            _collections[name] = get_db()[name]
        return _collections[name]

    def __getattr__(self, item):
        return getattr(self._resolve(), item)

    def __call__(self):
        """Allow `collection()` — returns the underlying motor collection."""
        return self._resolve()


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,
            minPoolSize=settings.MONGODB_MIN_POOL_SIZE,
            maxIdleTimeMS=settings.MONGODB_MAX_IDLE_TIME_MS,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=30000,
        )
    return _client


def get_db() -> AsyncIOMotorDatabase:
    global _db
    if _db is None:
        client = get_client()
        _db = client[settings.DATABASE_NAME]
    return _db


def get_collection(name: str):
    if name not in _collections:
        _collections[name] = get_db()[name]
    return _collections[name]


# Lazy collection proxies — work as both `collection.find_one()` and `collection()`
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
usage_collection = _LazyCollection("usage_tracking")
predictions_collection = _LazyCollection("predictions")
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
cards_collection = _LazyCollection("cards")


async def init_db():
    db = get_db()

    await db["users"].create_index("email", unique=True)
    await db["users"].create_index("plan")
    await db["users"].create_index("created_at")
    await db["users"].create_index([("email", 1), ("plan", 1)])

    await db["interviews"].create_index("user_id")
    await db["interviews"].create_index([("user_id", 1), ("created_at", -1)])
    await db["interviews"].create_index("status")
    await db["interviews"].create_index([("user_id", 1), ("status", 1)])

    await db["resumes"].create_index("user_id")
    await db["resumes"].create_index([("user_id", 1), ("created_at", -1)])
    await db["resumes"].create_index("ats_score")

    await db["aptitude_tests"].create_index("user_id")
    await db["aptitude_tests"].create_index([("user_id", 1), ("created_at", -1)])
    await db["aptitude_tests"].create_index("category")
    await db["aptitude_tests"].create_index("status")
    await db["aptitude_tests"].create_index([("user_id", 1), ("category", 1)])

    await db["cover_letters"].create_index("user_id")
    await db["cover_letters"].create_index([("user_id", 1), ("created_at", -1)])

    await db["system_design"].create_index("user_id")
    await db["system_design"].create_index([("user_id", 1), ("created_at", -1)])
    await db["system_design"].create_index("difficulty")

    await db["coding_challenges"].create_index("user_id")
    await db["coding_challenges"].create_index([("user_id", 1), ("created_at", -1)])
    await db["coding_challenges"].create_index("topic")
    await db["coding_challenges"].create_index("difficulty")
    await db["coding_challenges"].create_index([("topic", 1), ("difficulty", 1)])

    await db["skill_graphs"].create_index("user_id", unique=True)

    await db["gamification"].create_index("user_id", unique=True)
    await db["gamification"].create_index([("xp", -1)])
    await db["gamification"].create_index([("level", -1), ("xp", -1)])

    await db["offers"].create_index("user_id")
    await db["offers"].create_index([("user_id", 1), ("created_at", -1)])
    await db["offers"].create_index("status")

    await db["progress"].create_index("user_id")
    await db["progress"].create_index([("user_id", 1), ("topic", 1)])

    await db["company_prep"].create_index("user_id")
    await db["company_prep"].create_index([("user_id", 1), ("company", 1)])

    await db["usage_tracking"].create_index("user_id")
    await db["usage_tracking"].create_index([("user_id", 1), ("feature", 1)])
    await db["usage_tracking"].create_index([("user_id", 1), ("period", 1)])

    await db["predictions"].create_index("user_id")
    await db["predictions"].create_index([("user_id", 1), ("created_at", -1)])

    await db["curated_questions"].create_index("company")
    await db["curated_questions"].create_index("topic")
    await db["curated_questions"].create_index("difficulty")
    await db["curated_questions"].create_index("type")
    await db["curated_questions"].create_index([("company", 1), ("topic", 1)])
    await db["curated_questions"].create_index([("company", 1), ("type", 1)])

    await db["question_answers"].create_index("user_id")
    await db["question_answers"].create_index([("user_id", 1), ("question_id", 1)])
    await db["question_answers"].create_index([("user_id", 1), ("created_at", -1)])
    await db["question_answers"].create_index("question_id")

    await db["company_mock_tests"].create_index("user_id")
    await db["company_mock_tests"].create_index([("user_id", 1), ("company", 1)])
    await db["company_mock_tests"].create_index([("user_id", 1), ("created_at", -1)])
    await db["company_mock_tests"].create_index("status")

    await db["alumni_experiences"].create_index("company")
    await db["alumni_experiences"].create_index([("company", 1), ("year", -1)])
    await db["alumni_experiences"].create_index("role")

    await db["placement_drives"].create_index("company")
    await db["placement_drives"].create_index("deadline")
    await db["placement_drives"].create_index([("is_active", 1), ("deadline", 1)])
    await db["placement_drives"].create_index("tier")

    await db["career_profiles"].create_index("user_id", unique=True)
    await db["career_profiles"].create_index("updated_at")

    await db["practice_sessions"].create_index("user_id")
    await db["practice_sessions"].create_index([("user_id", 1), ("created_at", -1)])
    await db["practice_sessions"].create_index("status")

    await db["mock_tests"].create_index("user_id")
    await db["mock_tests"].create_index([("user_id", 1), ("created_at", -1)])
    await db["mock_tests"].create_index("status")

    await db["trials"].create_index("user_id")
    await db["trials"].create_index([("user_id", 1), ("status", 1)])

    await db["discounts"].create_index("user_id")
    await db["discounts"].create_index([("user_id", 1), ("type", 1), ("status", 1)])

    await db["solved_problems"].create_index("user_id")
    await db["solved_problems"].create_index([("user_id", 1), ("question_id", 1)], unique=True)
    await db["solved_problems"].create_index([("user_id", 1), ("solved_at", -1)])

    await db["submissions"].create_index("user_id")
    await db["submissions"].create_index([("user_id", 1), ("question_id", 1)])
    await db["submissions"].create_index([("user_id", 1), ("submitted_at", -1)])
    await db["submissions"].create_index("status")
    await db["submissions"].create_index([("question_id", 1), ("status", 1)])

    await db["cards"].create_index("user_id")
    await db["cards"].create_index([("user_id", 1), ("rarity", 1)])
    await db["cards"].create_index([("user_id", 1), ("topic", 1)])
    await db["cards"].create_index([("user_id", 1), ("question_id", 1)])

    logger.info("Database indexes created successfully")


async def close_db():
    global _client
    if _client:
        _client.close()
        _client = None
        _db = None
        _collections.clear()
        logger.info("Database connection closed")


async def ping_db() -> bool:
    try:
        client = get_client()
        await client.admin.command("ping")
        return True
    except Exception as e:
        logger.error(f"Database ping failed: {e}")
        return False
