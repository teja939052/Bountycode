"""Structured logging with correlation IDs."""
import json
import logging
import uuid
from contextvars import ContextVar
from typing import Any, Mapping

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
}

request_id_var: ContextVar[str] = ContextVar("request_id", default="")

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
            if key_str in SENSITIVE_KEYS or any(s in key_str for s in ("password", "token", "secret", "cookie", "auth")):
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
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": request_id_var.get(""),
        }
        context = extract_log_context(record)
        if context:
            log_entry["context"] = context
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry, default=str)


def setup_structured_logging():
    """Replace root logger handler with structured JSON formatter."""
    root = logging.getLogger()
    for handler in root.handlers[:]:
        root.removeHandler(handler)

    handler = logging.StreamHandler()
    handler.setFormatter(StructuredFormatter())
    root.addHandler(handler)

    file_handler = logging.FileHandler("placementpro.log")
    file_handler.setFormatter(StructuredFormatter())
    root.addHandler(file_handler)


def new_request_id() -> str:
    """Generate and return a new request ID."""
    rid = uuid.uuid4().hex
    request_id_var.set(rid)
    return rid


def log_context(**kwargs: Any) -> dict[str, Any]:
    """Build a sanitized logging context for structured logs."""
    return redact_sensitive_data(kwargs)
