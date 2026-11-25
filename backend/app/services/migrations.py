"""Schema migration system — decorator-based tracking.

Migration state is tracked in application memory. Schema changes are managed
via Supabase CLI version-controlled SQL migrations (backend/supabase/migrations/),
not via Motor/MongoDB.
"""

from typing import Optional

_MIGRATION_VERSION = "2026.08.18_sde_journey"


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


async def run_migrations() -> Optional[str]:
    """
    Run schema migrations.

    Schema changes are managed by Supabase CLI version-controlled SQL migrations
    (backend/supabase/migrations/). This function is a no-op placeholder kept
    for backward compatibility with the application startup sequence.
    """
    from fastapi import FastAPI

    app = FastAPI()  # Get the app instance context
    _ensure_migration_tracking(app)

    # Check if migration already ran
    if _has_migration_run(app, _MIGRATION_VERSION):
        return None

    # Mark migration as ran
    _mark_migration_ran(app, _MIGRATION_VERSION)

    return _MIGRATION_VERSION
