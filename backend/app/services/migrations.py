"""Database migration system for schema changes."""
import logging
from datetime import datetime, timezone
from app.database import get_db

logger = logging.getLogger(__name__)

MIGRATIONS = []


def migration(version: int, description: str):
    def decorator(func):
        MIGRATIONS.append({"version": version, "description": description, "func": func})
        MIGRATIONS.sort(key=lambda m: m["version"])
        return func
    return decorator


async def get_migration_version() -> int:
    db = get_db()
    doc = await db["_migrations"].find_one({"_id": "schema_version"})
    return doc["version"] if doc else 0


async def set_migration_version(version: int):
    db = get_db()
    await db["_migrations"].update_one(
        {"_id": "schema_version"},
        {"$set": {"version": version, "updated_at": datetime.now(timezone.utc)}},
        upsert=True,
    )


async def run_migrations():
    current = await get_migration_version()
    pending = [m for m in MIGRATIONS if m["version"] > current]
    if not pending:
        logger.info(f"Database schema up to date (v{current})")
        return
    logger.info(f"Running {len(pending)} pending migration(s) from v{current}")
    for m in pending:
        try:
            logger.info(f"Migration v{m['version']}: {m['description']}")
            await m["func"]()
            await set_migration_version(m["version"])
            logger.info(f"Migration v{m['version']} complete")
        except Exception as e:
            logger.error(f"Migration v{m['version']} failed: {e}")
            raise


@migration(1, "Add analytics TTL index if missing")
async def migration_001():
    db = get_db()
    existing = await db["analytics_events"].index_information()
    # Skip if timestamp_dt_1 already exists (even with different TTL)
    if "timestamp_dt_1" not in existing:
        try:
            await db["analytics_events"].create_index(
                "timestamp_dt", expireAfterSeconds=60 * 60 * 24 * 180
            )
        except Exception:
            pass  # Index already exists with different options — safe to ignore


@migration(2, "Ensure gamification tower fields exist for all users")
async def migration_002():
    db = get_db()
    await db["gamification"].update_many(
        {"stars_total": {"$exists": False}},
        {"$set": {
            "stars_total": 0, "coins": 0, "power_ups": {},
            "bosses_defeated": [], "wizard_outfit": "novice robe",
            "streak_freezes": 1, "daily_goal_count": 0,
            "daily_goal_target": 5, "daily_goal_date": None,
        }},
    )
