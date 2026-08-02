import time
import logging
from collections import defaultdict, deque
from typing import Dict, Deque
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.cache import cache
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

RATE_LIMIT_WINDOW = 60  # seconds
MAX_REQUESTS = settings.RATE_LIMIT_PER_MINUTE
LOGIN_MAX_ATTEMPTS = settings.RATE_LIMIT_LOGIN_ATTEMPTS
LOGIN_LOCKOUT_SECONDS = settings.RATE_LIMIT_LOGIN_LOCKOUT
MAX_IP_ENTRIES = 10000
MAX_EMAIL_ENTRIES = 1000

# In-memory stores (will be replaced with Redis in distributed setup)
login_attempts: Dict[str, Deque[float]] = defaultdict(lambda: deque(maxlen=LOGIN_MAX_ATTEMPTS + 1))
request_counts: Dict[str, Deque[float]] = defaultdict(lambda: deque(maxlen=MAX_REQUESTS + 1))


def _prune_deque(dq: Deque[float], window: float) -> None:
    """Remove entries older than window from the deque."""
    now = time.time()
    while dq and now - dq[0] >= window:
        dq.popleft()


def _cleanup_request_counts():
    """Clean up expired IP entries to prevent memory leaks."""
    if len(request_counts) > MAX_IP_ENTRIES:
        now = time.time()
        expired = [
            ip for ip, timestamps in request_counts.items()
            if timestamps and now - timestamps[-1] > RATE_LIMIT_WINDOW * 2
        ]
        for ip in expired:
            del request_counts[ip]


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware with support for Redis (optional)."""
    
    def __init__(self, app, use_redis: bool = False):
        super().__init__(app)
        self.use_redis = use_redis and settings.REDIS_URL
        if self.use_redis:
            logger.info("Rate limiter using Redis backend")
        else:
            logger.info("Rate limiter using in-memory backend")
    
    async def _check_redis_rate_limit(self, client_ip: str) -> bool:
        """Check rate limit using Redis."""
        try:
            key = f"rate_limit:{client_ip}"
            current = await cache.get("ratelimit", key)
            if current is None:
                await cache.set("ratelimit", key, 1, ttl=RATE_LIMIT_WINDOW)
                return True
            
            if current >= MAX_REQUESTS:
                return False
            
            await cache.incr("ratelimit", key)
            return True
        except Exception as e:
            logger.error(f"Redis rate limit check failed: {e}")
            # Fallback to in-memory
            return self._check_memory_rate_limit(client_ip)
    
    def _check_memory_rate_limit(self, client_ip: str) -> bool:
        """Check rate limit using in-memory storage."""
        dq = request_counts[client_ip]
        _prune_deque(dq, RATE_LIMIT_WINDOW)
        if len(dq) >= MAX_REQUESTS:
            return False
        dq.append(time.time())
        _cleanup_request_counts()
        return True
    
    async def dispatch(self, request: Request, call_next):
        """Process request with rate limiting."""
        client_ip = request.client.host if request.client else "unknown"
        path = request.url.path

        # Skip rate limiting for health and root endpoints
        if path in ("/health", "/", "/docs", "/openapi.json"):
            return await call_next(request)

        # Skip fire-and-forget telemetry endpoints — they're sent on every page
        # view and would otherwise burn the whole IP budget (blocking auth too).
        if path.startswith("/api/v1/analytics/track") or path.startswith("/api/v1/debug/log"):
            return await call_next(request)

        # Check rate limit
        if self.use_redis:
            allowed = await self._check_redis_rate_limit(client_ip)
        else:
            allowed = self._check_memory_rate_limit(client_ip)

        if not allowed:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again in a minute.",
                headers={"Retry-After": str(RATE_LIMIT_WINDOW)}
            )

        return await call_next(request)


def check_login_rate_limit(email: str):
    """Check if login attempts for an email exceed the limit."""
    dq = login_attempts[email]
    _prune_deque(dq, LOGIN_LOCKOUT_SECONDS)
    if len(dq) >= LOGIN_MAX_ATTEMPTS:
        remaining = int(LOGIN_LOCKOUT_SECONDS - (time.time() - dq[0]))
        if remaining > 0:
            raise HTTPException(
                status_code=429,
                detail=f"Account locked. Too many failed attempts. Try again in {remaining} seconds.",
                headers={"Retry-After": str(remaining)}
            )


def record_login_failure(email: str):
    """Record a failed login attempt."""
    login_attempts[email].append(time.time())
    # Cleanup old entries to prevent memory leaks
    if len(login_attempts) > MAX_EMAIL_ENTRIES:
        now = time.time()
        expired = [
            email for email, attempts in login_attempts.items()
            if attempts and now - attempts[-1] > LOGIN_LOCKOUT_SECONDS * 2
        ]
        for email in expired:
            del login_attempts[email]


def clear_login_attempts(email: str):
    """Clear login attempts for an email after successful login."""
    login_attempts.pop(email, None)


def get_rate_limit_status(email: str = None) -> dict:
    """Get current rate limit status for monitoring."""
    return {
        "total_ips": len(request_counts),
        "total_login_attempts": len(login_attempts),
        "requests_per_ip": {
            ip: len(dq) for ip, dq in list(request_counts.items())[:10]
        },
        "login_attempts": {
            email: len(attempts) for email, attempts in list(login_attempts.items())[:10]
        }
    }
