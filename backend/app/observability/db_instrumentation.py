"""Database infrastructure observability.

Instruments SQLAlchemy async engine events to log:
- Connection checkout/checkin (pool usage)
- Transaction begin/commit/rollback
- Slow query execution (safe fingerprint only — no raw SQL)
- Connection errors (safe category only — no raw exception text)

No SQL bind parameters, connection strings, raw SQL, or raw exception
messages are ever logged.
"""

import hashlib
import logging
import time
from typing import Optional, Set

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.pool import Pool

from app.services.structured_logging import get_logger, log_context, request_id_var

logger = get_logger(__name__)

# Configurable slow-query threshold (ms)
SLOW_QUERY_THRESHOLD_MS = 500

# Track which engines already have listeners attached (idempotency)
_listened_engine_ids: Set[int] = set()


def _safe_query_fingerprint(statement: str) -> str:
    """Return a safe hash fingerprint of a SQL statement.

    Never returns the raw SQL text — only a truncated hash, which cannot
    be reversed to reveal table names, column names, or values.
    """
    if not statement:
        return "unknown"
    return hashlib.sha256(statement.encode("utf-8")).hexdigest()[:16]


def _safe_error_category(exc: BaseException) -> str:
    """Return a safe error category for a database exception.

    Never returns the raw exception message, which may contain table names,
    column names, constraint names, or connection details.
    """
    exc_type = type(exc).__name__
    msg = str(exc).lower()
    if "connection" in msg or "timeout" in msg:
        return "connection_error"
    if "duplicate" in msg or "unique" in msg:
        return "constraint_violation"
    if "syntax" in msg:
        return "syntax_error"
    if "permission" in msg or "privilege" in msg:
        return "authorization_error"
    if "not found" in msg or "does not exist" in msg:
        return "object_not_found"
    if "deadlock" in msg:
        return "deadlock"
    return exc_type


def instrument_sqlalchemy_engine(engine: Engine) -> None:
    """Attach event listeners to a SQLAlchemy Engine for observability.

    Idempotent: calling multiple times on the same engine (by id) does not
    register duplicate listeners. Safe to call when the engine is recreated.
    """
    engine_id = id(engine)
    if engine_id in _listened_engine_ids:
        return
    _listened_engine_ids.add(engine_id)

    @event.listens_for(engine, "connect")
    def _on_connect(dbapi_connection, connection_record):
        rid = request_id_var.get("")
        logger.info(
            "db.connection.opened",
            extra=log_context(
                event="db.connection.opened",
                request_id=rid,
            ),
        )

    @event.listens_for(engine, "close")
    def _on_close(dbapi_connection, connection_record):
        rid = request_id_var.get("")
        logger.info(
            "db.connection.closed",
            extra=log_context(
                event="db.connection.closed",
                request_id=rid,
            ),
        )

    @event.listens_for(Pool, "checkout")
    def _on_checkout(dbapi_connection, connection_record, checkout_pool):
        # The checkout_pool argument is the Pool object, not a connection proxy.
        rid = request_id_var.get("")
        logger.debug(
            "db.pool.checkout",
            extra=log_context(
                event="db.pool.checkout",
                request_id=rid,
                pool_size=checkout_pool.size(),
                checked_out=checkout_pool.checkedout(),
            ),
        )

    @event.listens_for(Pool, "checkin")
    def _on_checkin(dbapi_connection, connection_record):
        rid = request_id_var.get("")
        logger.debug(
            "db.pool.checkin",
            extra=log_context(
                event="db.pool.checkin",
                request_id=rid,
            ),
        )

    @event.listens_for(Engine, "before_cursor_execute")
    def _before_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        # Store start time in the context for the after event
        context._query_start_time = time.time()

    @event.listens_for(Engine, "after_cursor_execute")
    def _after_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        total = time.time() - context._query_start_time
        duration_ms = total * 1000
        rid = request_id_var.get("")

        # Log slow queries with safe fingerprint only — never raw SQL
        if duration_ms >= SLOW_QUERY_THRESHOLD_MS:
            logger.warning(
                "db.slow_query",
                extra=log_context(
                    event="db.slow_query",
                    duration_ms=round(duration_ms, 2),
                    query_fingerprint=_safe_query_fingerprint(statement or ""),
                    request_id=rid,
                ),
            )
        else:
            logger.debug(
                "db.query.executed",
                extra=log_context(
                    event="db.query.executed",
                    duration_ms=round(duration_ms, 2),
                    request_id=rid,
                ),
            )

    @event.listens_for(Engine, "handle_error")
    def _on_db_error(exc):
        rid = request_id_var.get("")
        logger.error(
            "db.error",
            extra=log_context(
                event="db.error",
                error_category=_safe_error_category(exc),
                error_type=type(exc).__name__,
                request_id=rid,
            ),
        )

    # ── Transaction lifecycle listeners ──
    @event.listens_for(Engine, "begin")
    def _on_begin(conn):
        rid = request_id_var.get("")
        logger.info(
            "db.transaction.begin",
            extra=log_context(
                event="db.transaction.begin",
                request_id=rid,
            ),
        )

    @event.listens_for(Engine, "commit")
    def _on_commit(conn):
        rid = request_id_var.get("")
        logger.info(
            "db.transaction.commit",
            extra=log_context(
                event="db.transaction.commit",
                request_id=rid,
            ),
        )

    @event.listens_for(Engine, "rollback")
    def _on_rollback(conn):
        rid = request_id_var.get("")
        logger.warning(
            "db.transaction.rollback",
            extra=log_context(
                event="db.transaction.rollback",
                request_id=rid,
            ),
        )


def reset_listener_tracking() -> None:
    """Clear the set of engines with listeners attached.

    Used in tests to allow re-instrumentation of the same engine object
    after recreation.
    """
    _listened_engine_ids.clear()


# Manual transaction logging helpers (for service-layer call sites where
# automatic engine-level listeners may not capture the right operation name).
# These are intentionally separate from the automatic listeners above.

def log_transaction_begin(operation: str = "unknown") -> None:
    """Log the start of a database transaction."""
    rid = request_id_var.get("")
    logger.info(
        "db.transaction.begin",
        extra=log_context(
            event="db.transaction.begin",
            operation=operation,
            request_id=rid,
        ),
    )


def log_transaction_commit(operation: str = "unknown") -> None:
    """Log the successful commit of a database transaction."""
    rid = request_id_var.get("")
    logger.info(
        "db.transaction.commit",
        extra=log_context(
            event="db.transaction.commit",
            operation=operation,
            request_id=rid,
        ),
    )


def log_transaction_rollback(operation: str = "unknown", reason: Optional[str] = None) -> None:
    """Log the rollback of a database transaction."""
    rid = request_id_var.get("")
    logger.warning(
        "db.transaction.rollback",
        extra=log_context(
            event="db.transaction.rollback",
            operation=operation,
            reason=reason,
            request_id=rid,
        ),
    )
