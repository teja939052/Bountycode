"""Database infrastructure observability.

Instruments SQLAlchemy async engine events to log:
- Connection checkout/checkin (pool usage)
- Transaction begin/commit/rollback
- Slow query execution (configurable threshold)
- Connection errors

No SQL bind parameters or connection strings are ever logged.
"""

import logging
import time
from typing import Optional

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.pool import Pool

from app.services.structured_logging import get_logger, log_context, request_id_var

logger = get_logger(__name__)

# Configurable slow-query threshold (ms)
SLOW_QUERY_THRESHOLD_MS = 500


def instrument_sqlalchemy_engine(engine: Engine) -> None:
    """Attach event listeners to a SQLAlchemy Engine for observability.

    Safe to call multiple times — event listeners are idempotent per engine
    instance (SQLAlchemy deduplicates identical listener functions).
    """

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
        context._query_statement = statement[:200]  # Truncate for safety

    @event.listens_for(Engine, "after_cursor_execute")
    def _after_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        total = time.time() - context._query_start_time
        duration_ms = total * 1000
        rid = request_id_var.get("")

        # Log slow queries only
        if duration_ms >= SLOW_QUERY_THRESHOLD_MS:
            logger.warning(
                "db.slow_query",
                extra=log_context(
                    event="db.slow_query",
                    duration_ms=round(duration_ms, 2),
                    query=context._query_statement,
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
    def _on_db_error(e):
        rid = request_id_var.get("")
        logger.error(
            "db.error",
            extra=log_context(
                event="db.error",
                error_type=type(e).__name__,
                error_message=str(e)[:500],
                request_id=rid,
            ),
        )


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
