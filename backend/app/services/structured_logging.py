"""Structured logging — PostgreSQL-backed, no MongoDB."""
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import logging
import json

# Module-level correlation ID (ContextVar for async-safe context propagation)
_request_id_var: ContextVar[str] = ContextVar("request_id", default="")


def set_request_id(rid: str) -> str:
    """Set request ID for structured logging."""
    _request_id_var.set(rid)
    return rid


def get_request_id() -> str:
    """Get current request ID."""
    return _request_id_var.get()


async def get_request_id_async(user_id: str) -> dict:
    """Get request ID (async variant)."""
    return {"user_id": user_id, "request_id": _request_id_var.get()}


@contextmanager
def log_context(request_id: str):
    """Context manager for request ID - sets and clears request ID."""
    token = _request_id_var.set(request_id)
    try:
        yield
    finally:
        _request_id_var.reset(token)


def get_logger(name: str) -> logging.Logger:
    """Get a structured logger instance."""
    return logging.getLogger(name)


def setup_structured_logging():
    """Setup structured logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )
    return logging.getLogger(__name__)


def new_request_id() -> str:
    """Generate a new request ID."""
    import uuid
    rid = str(uuid.uuid4())
    set_request_id(rid)
    return rid


async def init_sentry() -> None:
    """Initialize Sentry error tracking."""
    import sentry_sdk
    sentry_sdk.init(
        dsn=None,  # Set SENTRY_DSN environment variable to enable
        traces_sample_rate=1.0,
    )


# Backwards-compatible exports
request_id_var = _request_id_var
trace_id_var = _request_id_var


def redact_sensitive_data(data: dict) -> dict:
    """Redact sensitive fields from a dict for logging."""
    sensitive_keys = {"password", "token", "secret", "api_key", "access_token", "refresh_token"}
    redacted = {}
    for k, v in data.items():
        if k.lower() in sensitive_keys:
            redacted[k] = "[REDACTED]"
        elif isinstance(v, dict):
            redacted[k] = redact_sensitive_data(v)
        else:
            redacted[k] = v
    return redacted


class StructuredFormatter(logging.Formatter):
    """JSON structured log formatter."""

    def format(self, record: logging.LogRecord) -> str:
        import json
        log_entry = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        return json.dumps(log_entry)


class HumanReadableFormatter(logging.Formatter):
    """Human-readable log formatter."""

    def format(self, record: logging.LogRecord) -> str:
        return f"[{record.levelname}] {record.name}: {record.getMessage()}"