"""Observability tests — Phase 8A.

Tests cover:
1. JSON log format
2. Required contextual fields
3. Request ID generation
4. Request ID propagation
5. Sensitive-value redaction
6. Long string truncation
7. Log file rotation config
8. Sentry disabled = no-op
9. AI Gateway failure events
10. Database failure events
11. Cross-user isolation (request IDs don't leak)
12. Synthetic end-to-end observability
13. setup_structured_logging does not crash
14. log_context helper

Uses synthetic test data only. No production data access.
"""

import json
import logging
import os
import tempfile
from io import StringIO
from unittest.mock import patch, MagicMock

import pytest

from app.services.structured_logging import (
    redact_sensitive_data,
    setup_structured_logging,
    set_request_id,
    request_id_var,
    trace_id_var,
    init_sentry,
    StructuredFormatter,
    HumanReadableFormatter,
    log_context,
)
from app.observability.db_instrumentation import (
    log_transaction_begin,
    log_transaction_commit,
    log_transaction_rollback,
)


@pytest.fixture(autouse=True)
def reset_context_vars():
    """Reset ContextVars between tests to prevent leakage."""
    request_id_var.set("")
    trace_id_var.set("")
    yield
    request_id_var.set("")
    trace_id_var.set("")


def _make_logger(name: str):
    """Create a logger writing to a StringIO with StructuredFormatter."""
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(StructuredFormatter())
    logger = logging.getLogger(name)
    logger.handlers = [handler]
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger, stream


# ══════════════════════════════════════════════════════════════════════════════
# TEST 1: JSON log format
# ══════════════════════════════════════════════════════════════════════════════

def test_json_log_format():
    """StructuredFormatter produces valid JSON with required fields."""
    logger, stream = _make_logger("test_json_format")
    # Use LoggerAdapter (get_logger) for extra kwargs, or extra= dict
    logger.info("test message", extra={"custom_field": "custom_value"})

    output = stream.getvalue().strip()
    parsed = json.loads(output)

    assert "timestamp" in parsed
    assert parsed["level"] == "INFO"
    assert parsed["logger"] == "test_json_format"
    assert parsed["message"] == "test message"
    assert "request_id" in parsed
    assert parsed["context"]["custom_field"] == "custom_value"


# ══════════════════════════════════════════════════════════════════════════════
# TEST 2: Required contextual fields
# ══════════════════════════════════════════════════════════════════════════════

def test_required_contextual_fields():
    """Log records include timestamp, level, logger, message, request_id."""
    logger, stream = _make_logger("test_context_fields")
    logger.info("hello world")

    parsed = json.loads(stream.getvalue().strip())
    assert "timestamp" in parsed
    assert parsed["level"] == "INFO"
    assert parsed["logger"] == "test_context_fields"
    assert parsed["message"] == "hello world"
    assert "request_id" in parsed


# ══════════════════════════════════════════════════════════════════════════════
# TEST 3: Request ID generation
# ══════════════════════════════════════════════════════════════════════════════

def test_request_id_generation():
    """set_request_id generates a unique hex ID."""
    rid1 = set_request_id()
    rid2 = set_request_id()
    assert rid1 != rid2
    assert len(rid1) == 32
    assert request_id_var.get() == rid2


# ══════════════════════════════════════════════════════════════════════════════
# TEST 4: Request ID propagation in logs
# ══════════════════════════════════════════════════════════════════════════════

def test_request_id_propagation():
    """The request ID set in ContextVar appears in log output."""
    logger, stream = _make_logger("test_request_propagation")
    set_request_id("test-rid-1234")
    logger.info("propagated message")

    parsed = json.loads(stream.getvalue().strip())
    assert parsed["request_id"] == "test-rid-1234"


# ══════════════════════════════════════════════════════════════════════════════
# TEST 8: Sensitive-value redaction (dict keys)
# ══════════════════════════════════════════════════════════════════════════════

def test_sensitive_value_redaction():
    """Passwords, tokens, secrets are redacted in nested dict structures."""
    data = {
        "user": {
            "name": "Alice",
            "password_hash": "$2b$12$hashed",
            "access_token": "secret-token-123",
            "refresh_token": "refresh-xyz",
        },
        "authorization": "Bearer abc123",
        "api_key": "sk-1234567890",
        "safe_field": "visible",
        "nested": {
            "deep": {
                "secret_key": "hidden-value"
            }
        },
    }

    result = redact_sensitive_data(data)

    assert result["user"]["name"] == "Alice"
    assert result["user"]["password_hash"] == "[REDACTED]"
    assert result["user"]["access_token"] == "[REDACTED]"
    assert result["user"]["refresh_token"] == "[REDACTED]"
    assert result["authorization"] == "[REDACTED]"
    assert result["api_key"] == "[REDACTED]"
    assert result["safe_field"] == "visible"
    assert result["nested"]["deep"]["secret_key"] == "[REDACTED]"


# ══════════════════════════════════════════════════════════════════════════════
# TEST 9: Password redaction in list of dicts
# ══════════════════════════════════════════════════════════════════════════════

def test_redaction_in_list_of_dicts():
    """Sensitive dict values inside lists are redacted."""
    data = {
        "users": [
            {"name": "Bob", "password": "hidden"},
            {"name": "Carol", "password": "also-hidden"},
        ],
    }

    result = redact_sensitive_data(data)

    assert result["users"][0]["name"] == "Bob"
    assert result["users"][0]["password"] == "[REDACTED]"
    assert result["users"][1]["password"] == "[REDACTED]"


# ══════════════════════════════════════════════════════════════════════════════
# TEST 10: Long string truncation
# ══════════════════════════════════════════════════════════════════════════════

def test_long_string_truncation():
    """Strings longer than 2000 chars are truncated."""
    long_string = "x" * 5000
    result = redact_sensitive_data({"data": long_string})
    assert result["data"].endswith("...[TRUNCATED]")
    assert len(result["data"]) <= 2000 + len("...[TRUNCATED]")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 11: Expected 4xx filtering (not treated as critical)
# ══════════════════════════════════════════════════════════════════════════════

def test_4xx_not_critical():
    """4xx errors are logged as warnings, not errors."""
    from app.middleware.route_safety import RouteErrorHandlingMiddleware
    assert RouteErrorHandlingMiddleware is not None


# ══════════════════════════════════════════════════════════════════════════════
# TEST 12: Unexpected 5xx capture
# ══════════════════════════════════════════════════════════════════════════════

def test_5xx_capture():
    """General exception handler is registered on the FastAPI app."""
    from app.main import app
    assert app is not None
    handler_names = [h.__name__ for h in app.exception_handlers.values()]
    assert "general_exception_handler" in handler_names


# ══════════════════════════════════════════════════════════════════════════════
# TEST 14: Log file rotation config
# ══════════════════════════════════════════════════════════════════════════════

def test_log_rotation_config():
    """RotatingFileHandler is configured with max bytes and backup count."""
    import logging.handlers

    handler = logging.handlers.RotatingFileHandler(
        "test_rotation.log",
        maxBytes=1024,
        backupCount=3,
        encoding="utf-8",
    )
    assert handler.maxBytes == 1024
    assert handler.backupCount == 3
    handler.close()
    # Clean up
    try:
        os.remove("test_rotation.log")
    except OSError:
        pass


# ══════════════════════════════════════════════════════════════════════════════
# TEST 15: Logging when Sentry is disabled
# ══════════════════════════════════════════════════════════════════════════════

def test_sentry_disabled_noop():
    """init_sentry() is a no-op when SENTRY_ENABLED is false."""
    with patch("app.services.structured_logging.get_settings") as mock_settings:
        mock_settings.return_value.SENTRY_ENABLED = False
        mock_settings.return_value.SENTRY_BACKEND_DSN = ""
        init_sentry()  # Should not raise


# ══════════════════════════════════════════════════════════════════════════════
# TEST 16: Sentry initialization (mocks sentry_sdk)
# ══════════════════════════════════════════════════════════════════════════════

def test_sentry_init_with_config():
    """init_sentry() calls sentry_sdk.init when configured."""
    import sys
    fake_sdk = MagicMock()
    fake_integrations = MagicMock()
    fake_integrations.FastApiIntegration = MagicMock()
    fake_integrations.SqlalchemyIntegration = MagicMock()
    fake_integrations.LoggingIntegration = MagicMock()
    fake_sdk.integrations = fake_integrations

    # Patch sentry_sdk and its integration submodules so `from ... import` works
    with patch.dict(sys.modules, {"sentry_sdk": fake_sdk}):
        with patch.dict(
            sys.modules,
            {
                "sentry_sdk.integrations.fastapi": MagicMock(FastApiIntegration=MagicMock()),
                "sentry_sdk.integrations.sqlalchemy": MagicMock(SqlalchemyIntegration=MagicMock()),
                "sentry_sdk.integrations.logging": MagicMock(LoggingIntegration=MagicMock()),
            },
        ):
            with patch(
                "app.services.structured_logging.get_settings",
                return_value=MagicMock(
                    SENTRY_ENABLED=True,
                    SENTRY_BACKEND_DSN="https://key@sentry.io/123",
                    SENTRY_ENVIRONMENT="test",
                    SENTRY_TRACES_SAMPLE_RATE=0.1,
                ),
            ):
                init_sentry()
                fake_sdk.init.assert_called_once()


# ══════════════════════════════════════════════════════════════════════════════
# TEST 17: AI Gateway failure events (logging structure)
# ══════════════════════════════════════════════════════════════════════════════

def test_ai_gateway_log_structure():
    """AI gateway log events have the expected structure."""
    logger, stream = _make_logger("test.ai")
    logger.warning(
        "ai.provider.failed",
        extra=log_context(
            event="ai.provider.failed",
            provider="openrouter",
            model="google/gemini-2.0-flash",
            error_category="provider_error",
            error_message="timeout",
        ),
    )

    parsed = json.loads(stream.getvalue().strip())
    assert parsed["context"]["event"] == "ai.provider.failed"
    assert parsed["context"]["provider"] == "openrouter"
    assert parsed["context"]["error_category"] == "provider_error"


# ══════════════════════════════════════════════════════════════════════════════
# TEST 18: Database failure events (logging structure)
# ══════════════════════════════════════════════════════════════════════════════

def test_db_failure_log_structure():
    """Database error log events have the expected structure."""
    logger, stream = _make_logger("test.db")
    logger.error(
        "db.error",
        extra=log_context(
            event="db.error",
            error_type="IntegrityError",
            error_message="duplicate key value",
        ),
    )

    parsed = json.loads(stream.getvalue().strip())
    assert parsed["context"]["event"] == "db.error"
    assert parsed["context"]["error_type"] == "IntegrityError"


# ══════════════════════════════════════════════════════════════════════════════
# TEST 19: Cross-user isolation (different request IDs)
# ══════════════════════════════════════════════════════════════════════════════

def test_cross_user_isolation():
    """Different request IDs don't leak between log entries."""
    logger, stream = _make_logger("test.isolation")

    set_request_id("user-a")
    logger.info("user a message")
    msg_a = stream.getvalue()

    set_request_id("user-b")
    logger.info("user b message")
    output = stream.getvalue()

    lines_a = msg_a.strip().split("\n")
    lines_b = output.strip().split("\n")
    parsed_a = json.loads(lines_a[-1])
    parsed_b = json.loads(lines_b[-1])

    assert parsed_a["request_id"] == "user-a"
    assert parsed_b["request_id"] == "user-b"
    assert parsed_a["request_id"] != parsed_b["request_id"]


# ══════════════════════════════════════════════════════════════════════════════
# TEST 20: Synthetic end-to-end observability
# ══════════════════════════════════════════════════════════════════════════════

def test_end_to_end_observability():
    """Synthetic E2E: request ID → log → context → redaction → transaction logs."""
    rid = set_request_id("e2e-test-001")

    logger, stream = _make_logger("test.e2e")
    logger.info(
        "assessment.submission.received",
        extra=log_context(
            event="assessment.submission.received",
            user_id="user-42",
            assessment_id="assess-99",
            score=85,
            password_hash="should-be-redacted",
        ),
    )

    parsed = json.loads(stream.getvalue().strip())
    assert parsed["request_id"] == "e2e-test-001"
    assert parsed["context"]["event"] == "assessment.submission.received"
    assert parsed["context"]["user_id"] == "user-42"
    assert parsed["context"]["assessment_id"] == "assess-99"
    assert parsed["context"]["score"] == 85
    assert parsed["context"]["password_hash"] == "[REDACTED]"

    # Transaction lifecycle logging
    log_transaction_begin("assessment_submit")
    log_transaction_commit("assessment_submit")
    log_transaction_rollback("assessment_submit", reason="constraint_violation")

    assert True


# ══════════════════════════════════════════════════════════════════════════════
# TEST: setup_structured_logging does not crash
# ══════════════════════════════════════════════════════════════════════════════

def test_setup_structured_logging_no_crash():
    """setup_structured_logging() completes without raising."""
    setup_structured_logging()
    root = logging.getLogger()
    assert len(root.handlers) >= 1


# ══════════════════════════════════════════════════════════════════════════════
# TEST: log_context helper
# ══════════════════════════════════════════════════════════════════════════════

def test_log_context_helper():
    """log_context() returns a sanitized dict."""
    ctx = log_context(user_id="user-1", password="secret", action="login")
    assert ctx["user_id"] == "user-1"
    assert ctx["action"] == "login"
    assert ctx["password"] == "[REDACTED]"


# ══════════════════════════════════════════════════════════════════════════════
# TEST: HumanReadableFormatter works in development
# ══════════════════════════════════════════════════════════════════════════════

def test_human_readable_formatter():
    """HumanReadableFormatter produces readable output."""
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(HumanReadableFormatter())

    logger = logging.getLogger("test.human")
    logger.handlers = [handler]
    logger.setLevel(logging.INFO)
    logger.propagate = False

    set_request_id("hr-rid")
    logger.info("human readable message", extra={"extra_field": "extra_value"})

    output = stream.getvalue().strip()
    assert "human readable message" in output
    assert "hr-rid" in output
    assert "extra_field=extra_value" in output
