"""Production-grade error handler with recovery and monitoring."""

import logging
import traceback
import json
from datetime import datetime

from app.utils.timeutil import utcnow
from typing import Any, Optional
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import httpx

logger = logging.getLogger(__name__)


class ProdErrorHandler:
    """Central error handling for production reliability."""
    
    ERROR_CODES = {
        "VALIDATION_ERROR": 1001,
        "AUTH_ERROR": 1002,
        "NOT_FOUND": 1003,
        "RATE_LIMIT": 1004,
        "DB_ERROR": 1005,
        "AI_ERROR": 1006,
        "PAYMENT_ERROR": 1007,
        "RESOURCE_EXHAUSTED": 1008,
        "TIMEOUT": 1009,
        "INTERNAL_ERROR": 1010,
    }
    
    RETRIABLE_ERRORS = {
        "DB_ERROR", "AI_ERROR", "TIMEOUT", "RESOURCE_EXHAUSTED"
    }

    @staticmethod
    async def handle_exception(
        request: Request,
        exc: Exception,
        request_id: Optional[str] = None
    ) -> JSONResponse:
        """
        Handle any exception with proper logging, monitoring, and recovery.
        Returns standardized JSON error response.
        """
        error_code = "INTERNAL_ERROR"
        status_code = 500
        message = "An unexpected error occurred"
        details = None
        is_retriable = False

        # Extract error type
        if isinstance(exc, ValidationError):
            error_code = "VALIDATION_ERROR"
            status_code = 422
            message = "Request validation failed"
            details = exc.errors()

        elif isinstance(exc, HTTPException):
            status_code = exc.status_code
            message = exc.detail
            if status_code == 401:
                error_code = "AUTH_ERROR"
            elif status_code == 404:
                error_code = "NOT_FOUND"
            elif status_code == 429:
                error_code = "RATE_LIMIT"
            elif status_code == 503:
                error_code = "RESOURCE_EXHAUSTED"

        elif isinstance(exc, httpx.TimeoutException):
            error_code = "TIMEOUT"
            status_code = 504
            message = "Request timeout - please retry"
            is_retriable = True

        elif isinstance(exc, httpx.ConnectError):
            error_code = "DB_ERROR"
            status_code = 503
            message = "Database connection failed"
            is_retriable = True

        elif "openrouter" in str(exc).lower() or "ai" in str(exc).lower():
            error_code = "AI_ERROR"
            status_code = 503
            message = "AI service temporarily unavailable"
            is_retriable = True

        # Log with context
        log_entry = {
            "timestamp": utcnow().isoformat(),
            "error_code": error_code,
            "status_code": status_code,
            "message": message,
            "path": request.url.path,
            "method": request.method,
            "request_id": request_id,
            "is_retriable": is_retriable,
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "traceback": traceback.format_exc() if status_code == 500 else None,
        }

        if status_code == 500:
            logger.error(json.dumps(log_entry))
        else:
            logger.warning(json.dumps(log_entry))

        # Return standardized error response
        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "error": {
                    "code": ProdErrorHandler.ERROR_CODES.get(error_code, 9999),
                    "code_name": error_code,
                    "message": message,
                    "details": details,
                    "path": request.url.path,
                    "method": request.method,
                    "request_id": request_id,
                    "retriable": is_retriable,
                    "timestamp": utcnow().isoformat(),
                },
            },
        )

    @staticmethod
    def is_retriable_error(error_code: str) -> bool:
        """Check if error can be safely retried."""
        return error_code in ProdErrorHandler.RETRIABLE_ERRORS

    @staticmethod
    async def log_error_to_db(db, request_id: str, error_details: dict):
        """Store error in database for analysis and monitoring."""
        try:
            error_logs = db["error_logs"]
            await error_logs.insert_one({
                "request_id": request_id,
                "timestamp": utcnow(),
                "error_code": error_details.get("code"),
                "message": error_details.get("message"),
                "path": error_details.get("path"),
                "status_code": error_details.get("status_code"),
            })
        except Exception as e:
            logger.error(f"Failed to log error to database: {e}")
