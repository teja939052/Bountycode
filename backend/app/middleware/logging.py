"""Logging middleware for request/response tracking."""

import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging all HTTP requests with timing."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with logging."""
        start_time = time.time()
        
        # Log request
        logger.info(
            f"{request.method} {request.url.path}"
            f" - Client: {request.client.host if request.client else 'unknown'}"
        )
        
        try:
            response = await call_next(request)
            duration = (time.time() - start_time) * 1000
            
            # Add response timing header
            response.headers["X-Response-Time"] = f"{duration:.2f}ms"
            
            # Log response
            logger.info(
                f"{request.method} {request.url.path} - {response.status_code}"
                f" - {duration:.2f}ms"
            )
            
            return response
            
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            logger.error(
                f"{request.method} {request.url.path} - ERROR - {duration:.2f}ms: {str(e)}"
            )
            raise
