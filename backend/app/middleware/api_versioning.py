"""API versioning middleware for BountyCode.

Enforces a single canonical API prefix based on ``config.API_VERSION``.
Requests that hit ``/api/<version>/...`` are allowed; requests that hit
``/api`` with the wrong/missing version receive a 404 with a versioning hint.
Non-API paths and FastAPI docs endpoints are passed through untouched.
"""
from __future__ import annotations

import logging
from typing import Callable

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_404_NOT_FOUND

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_API_PREFIX = "/api"
_EXEMPT_PATHS = {
    "/",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/api/v1/health/live",
    "/api/v1/health/ready",
}


class APIVersioningMiddleware(BaseHTTPMiddleware):
    """Reject requests using an unsupported or missing API version.

    All BountyCode API routes live under ``/api/<API_VERSION>/``. Any request
    that reaches ``/api`` with a different version (or no version) is rejected
    with a 404 and a JSON hint so clients can migrate deterministically.
    """

    def __init__(self, app: Callable) -> None:
        super().__init__(app)
        self.allowed_prefix = f"{_API_PREFIX}/{settings.API_VERSION}"

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Allow exempt paths through without version checks.
        if path in _EXEMPT_PATHS or path.startswith(("/docs", "/redoc", "/openapi.json")):
            return await call_next(request)

        # Only enforce versioning for paths under /api.
        if path == _API_PREFIX or path.startswith(f"{_API_PREFIX}/"):
            if not path.startswith(self.allowed_prefix):
                logger.debug(
                    "Rejected mismatched API version: %s (allowed: %s)",
                    path,
                    self.allowed_prefix,
                )
                return JSONResponse(
                    status_code=HTTP_404_NOT_FOUND,
                    content={
                        "success": False,
                        "error": {
                            "code": 404,
                            "message": "API version not found",
                            "path": path,
                            "allowed_prefix": self.allowed_prefix,
                            "hint": (
                                "Set the current API version to "
                                f"'{settings.API_VERSION}' or upgrade your client."
                            ),
                        },
                    },
                )

        return await call_next(request)
