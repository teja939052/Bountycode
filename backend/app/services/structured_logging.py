"""Structured logging with correlation IDs, redaction, and rotating file output.

Provides:
- JSON-structured logs for production (machine-searchable)
- Human-readable console output for development
- Rotating local log files with size limits
- Request ID correlation via ContextVar
- Recursive sensitive-data redaction
- Optional Sentry integration (env-gated, never crashes the app)
"""

import json
import logging
import logging.handlers
import os
import sys
import uuid
from contextvars import ContextVar
from typing import Any, Mapping, Optional

from app.config import get_settings

SENSITIVE_KEYS = {
    "password",
    "password_hash",
    "token",
    "access_token",
    "refresh_token",
    "authorization",
    "cookie",
    "set-cookie",
    "secret",
    "api_key",
    "email",
    "jwt",
    "session_id",
}

request_id_var: ContextVar[str] = ContextVar("request_id", default="")
trace_id_var: ContextVar[str] = ContextVar("trace_id", default="")

_STANDARD_LOG_ATTRS = {
    "name", "msg", "args", "levelname", "levelno", "pathname", "filename", "module",
    "exc_info", "exc_text", "stack_info", "lineno", "funcName", "created", "msecs",
    "relativeCreated", "thread", "threadName", "processName", "process", "message",
}


def redact_sensitive_data(value: Any, depth: int = 0) -> Any:
    """Recursively redact sensitive values before they are written to logs."""
    if depth > 6:
        return "[REDACTED]"
    if isinstance(value, Mapping):
        redacted = {}
        for key, item in value.items():
            key_str = str(key).lower()
            if key_str in SENSITIVE_KEYS or any(s in key_str for s in ("password", "token", "secret", "cookie", "auth", "jwt", "session")):
                redacted[key] = "[REDACTED]"
            else:
                redacted[key] = redact_sensitive_data(item, depth + 1)
        return redacted
    if isinstance(value, list):
        return [redact_sensitive_data(item, depth + 1) for item in value]
    if isinstance(value, tuple):
        return tuple(redact_sensitive_data(item, depth + 1) for item in value)
    if isinstance(value, str):
        if len(value) > 2000:
            return value[:2000] + "...[TRUNCATED]"
        return value
    return value


def extract_log_context(record: logging.LogRecord) -> dict[str, Any]:
    """Extract custom log context from a LogRecord."""
    context = {}
    for key, value in record.__dict__.items():
        if key in _STANDARD_LOG_ATTRS or key.startswith("_"):
            continue
        context[key] = redact_sensitive_data(value)
    return context


class StructuredFormatter(logging.Formatter):
    """JSON-structured log formatter for production."""

    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": request_id_var.get(""),
            "trace_id": trace_id_var.get(""),
        }
        context = extract_log_context(record)
        if context:
            log_entry["context"] = context
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry, default=str)


class HumanReadableFormatter(logging.Formatter):
    """Human-readable formatter for development console output."""

    def format(self, record):
        rid = request_id_var.get("")
        rid_part = f" [{rid}]" if rid else ""
        context_parts = []
        for key, value in record.__dict__.items():
            if key in _STANDARD_LOG_ATTRS or key.startswith("_"):
                continue
            context_parts.append(f"{key}={redact_sensitive_data(value)}")
        context_str = " " + " ".join(context_parts) if context_parts else ""
        exc = ""
        if record.exc_info:
            exc = "\n" + self.formatException(record.exc_info)
        return (
            f"{self.formatTime(record)} {record.levelname:8s} {record.name}{rid_part}"
            f" - {record.getMessage()}{context_str}{exc}"
        )


def _should_use_json() -> bool:
    """Decide whether to emit JSON (production) or human-readable (development)."""
    settings = get_settings()
    env = settings.SENTRY_ENVIRONMENT or "development"
    # Force JSON in production/staging; human-readable in local development
    return env not in ("development", "local", "dev")


def setup_structured_logging():
    """Configure root logger with structured JSON + rotating file output.

    - Console: JSON in production, human-readable in development
    - File: rotating JSON log under backend/logs/
    - Logs and archives are Git-ignored (*.log)
    - Never crashes if the log directory cannot be created
    """
    settings = get_settings()
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    root = logging.getLogger()
    root.setLevel(log_level)

    # Remove any pre-existing handlers to avoid duplicates on reload
    for handler in root.handlers[:]:
        root.removeHandler(handler)

    # ── Console handler ──
    console_handler = logging.StreamHandler(sys.stdout)
    if _should_use_json():
        console_handler.setFormatter(StructuredFormatter())
    else:
        console_handler.setFormatter(HumanReadableFormatter())
    root.addHandler(console_handler)

    # ── Rotating file handler ──
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
    try:
        os.makedirs(log_dir, exist_ok=True)
    except OSError:
        # If we cannot create the log directory, continue with console only
        pass

    log_path = os.path.join(log_dir, settings.LOG_FILE)
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            log_path,
            maxBytes=settings.LOG_ROTATION_MAX_BYTES,
            backupCount=settings.LOG_ROTATION_BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setFormatter(StructuredFormatter())
        root.addHandler(file_handler)
    except OSError:
        # If we cannot open the log file, continue with console only
        pass


def set_request_id(rid: Optional[str] = None) -> str:
    """Set and return the current request ID in the ContextVar."""
    if rid is None:
        rid = uuid.uuid4().hex
    request_id_var.set(rid)
    return rid


def set_trace_id(tid: Optional[str] = None) -> str:
    """Set and return the current trace ID in the ContextVar."""
    if tid is None:
        tid = uuid.uuid4().hex
    trace_id_var.set(tid)
    return tid


def new_request_id() -> str:
    """Generate and return a new request ID."""
    return set_request_id()


class _ContextLogger(logging.LoggerAdapter):
    """Logger adapter that injects sanitized context kwargs into log records.

    Usage: get_logger(__name__).info("msg", user_id="abc")
    """

    def process(self, msg, kwargs):
        extra = kwargs.setdefault("extra", {})
        for key in list(kwargs):
            if key not in logging._nameToLevel and key != "extra":
                extra[key] = redact_sensitive_data(kwargs.pop(key))
        return msg, kwargs


def get_logger(name: str) -> logging.LoggerAdapter:
    """Return a structured-capable logger (LoggerAdapter) for the given name."""
    return _ContextLogger(logging.getLogger(name), {})


def log_context(**kwargs: Any) -> dict[str, Any]:
    """Build a sanitized logging context for structured logs."""
    return redact_sensitive_data(kwargs)


def init_sentry() -> None:
    """Initialize Sentry SDK if enabled and a DSN is configured.

    Safe to call even when Sentry is not configured — it silently no-ops.
    Sentry failures never crash the application.
    """
    settings = get_settings()
    if not settings.SENTRY_ENABLED or not settings.SENTRY_BACKEND_DSN:
        return

    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
        from sentry_sdk.integrations.logging import LoggingIntegration

        sentry_logging = LoggingIntegration(
            level=logging.INFO,        # Capture breadcrumbs at INFO
            event_level=logging.ERROR, # Send errors as events
        )

        sentry_sdk.init(
            dsn=settings.SENTRY_BACKEND_DSN,
            environment=settings.SENTRY_ENVIRONMENT,
            traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE,
            integrations=[
                FastApiIntegration(transaction_style="url"),
                SqlalchemyIntegration(),
                sentry_logging,
            ],
            send_default_pii=False,
            # Never attach request bodies or private data
            before_send=lambda event, hint: _scrub_sentry_event(event),
        )
    except Exception:
        # Sentry is optional — never crash the app because of it
        pass


def _scrub_sentry_event(event: dict, hint: dict | None = None) -> dict | None:
    """Scrub sensitive data from Sentry events before transmission."""
    # Remove request bodies that may contain passwords, tokens, etc.
    request = event.get("request", {})
    if request:
        request.pop("data", None)  # request body
        headers = request.get("headers", {})
        if isinstance(headers, dict):
            sensitive_headers = {"authorization", "cookie", "set-cookie", "x-api-key"}
            for h in list(headers.keys()):
                if h.lower() in sensitive_headers:
                    headers[h] = "[REDACTED]"

    # Remove extra/context that might contain PII
    extra = event.get("extra", {})
    if isinstance(extra, dict):
        for key in list(extra.keys()):
            key_lower = key.lower()
            if any(s in key_lower for s in ("password", "token", "secret", "cookie", "auth", "email")):
                extra[key] = "[REDACTED]"

    return event
