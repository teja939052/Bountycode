"""Schema migration system — decorator-based tracking."""


import uuid
from datetime import datetime, timezone
from typing import Optional

from app.database import get_client


# Track which migrations have run
_MIGRATIONS_KEY = "placementpro:migratiosno"
_MIGRATION_VERSION = "2026.08.18_sde_journey"


# Track run migrations in app state
def _ensure_migration_tracking(app):
    """Initialize migration tracking in app state if not present."""
    if not hasattr(app, "migration_version"):
        app.migration_version = _MIGRATION_VERSION


def _has_migration_run(app, migration_name: str) -> bool:
    """Check if a migration has already run."""
    if not hasattr(app, "migration_ran"):
        app.migration_ran = set()
    return migration_name in app.migration_ran


def _mark_migration_ran(app, migration_name: str):
    """Mark a migration as having run."""
    if hasattr(app, "migration_ran"):
        app.migration_ran.add(migration_name)


async def _create_sparse_uid_index():
    """Create a sparse unique index on users.uid so that:
    - Existing users with uid=null are automatically skipped
    - Future users with a non-null uid get enforced uniqueness
    - No E11000 duplicate key error occurs on startup
    """
    from app.database import get_client
    client = get_client()
    db = client.get_database("placementpro")

    # Create sparse unique index on uid
    # Sparse: only index documents where uid field exists AND is not null
    # This avoids E11000 duplicate key error when all existing users have uid=null
    try:
        await db.users.create_index(
            [("uid", 1)],
            unique=True,
            sparse=True,
        )
        print("Created sparse unique index on users.uid")
    except Exception as e:
        print(f"Sparse uid index setup: {type(e).__name__}: {e}")


async def run_migrations() -> Optional[str]:
    """
    Run schema migrations.

    Returns migration result string or None.
    """
    from fastapi import FastAPI

    app = FastAPI()  # Get the app instance context
    _ensure_migration_tracking(app)

    # Check if migration already ran
    if _has_migration_run(app, _MIGRATION_VERSION):
        print("Migration already ran (version: {_MIGRATION_VERSION})")
        return None

    print(f"Running migration: {_MIGRATION_VERSION}")

    # Run index creation
    await _create_sparse_uid_index()

    # Mark migration as ran
    _mark_migration_ran(app, _MIGRATION_VERSION)

    print("Migration complete")
    return _MIGRATION_VERSION