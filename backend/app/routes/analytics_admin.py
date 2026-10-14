"""
Analytics routes — tracking, admin dashboard, visitor stats.
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field, field_validator
from app.middleware.auth import get_current_user, require_admin
from app.services.analytics_service import (
    track_event,
    get_visitor_stats,
    get_page_stats,
    get_feature_usage,
    get_realtime_stats,
    get_hourly_distribution,
    get_geo_breakdown,
    get_retention_stats,
    get_user_list,
    get_user_stats_summary,
)
import time
from collections import defaultdict, deque

router = APIRouter(prefix="/api/v1/admin/analytics", tags=["admin-analytics"])

_analytics_rate_limit_window = 60
_analytics_max_requests = 200
_analytics_request_counts: dict[str, deque] = defaultdict(lambda: deque(maxlen=_analytics_max_requests + 1))


def _check_analytics_rate_limit(client_ip: str) -> bool:
    now = time.time()
    dq = _analytics_request_counts[client_ip]
    while dq and now - dq[0] >= _analytics_rate_limit_window:
        dq.popleft()
    if len(dq) >= _analytics_max_requests:
        return False
    dq.append(now)
    return True


class AnalyticsTrackRequest(BaseModel):
    event: str = Field(default="page_view", max_length=64)
    path: str = Field(default="", max_length=2048)
    meta: dict = Field(default_factory=dict, max_length=10000)

    @field_validator("event")
    @classmethod
    def validate_event(cls, v: str) -> str:
        if not v:
            return "page_view"
        import re
        if not re.match(r"^[a-zA-Z0-9_.:-]+$", v):
            raise ValueError("event must match ^[a-zA-Z0-9_.:-]+$")
        return v

    @field_validator("path")
    @classmethod
    def validate_path(cls, v: str) -> str:
        if len(v) > 2048:
            raise ValueError("path must be <= 2048 characters")
        return v

    @field_validator("meta")
    @classmethod
    def validate_meta(cls, v: dict) -> dict:
        if not isinstance(v, dict):
            raise ValueError("meta must be an object")
        if len(v) > 50:
            raise ValueError("meta must have <= 50 keys")
        for key, value in v.items():
            if not isinstance(key, str) or len(key) > 64:
                raise ValueError("meta keys must be strings <= 64 chars")
            if isinstance(value, str) and len(value) > 1024:
                raise ValueError("meta string values must be <= 1024 chars")
            if isinstance(value, (dict, list)):
                raise ValueError("meta values must be scalar (str/number/bool)")
        return v


@router.post("/track")
async def track(request: Request, body: AnalyticsTrackRequest):
    """Track an analytics event. Public endpoint with schema validation and rate limiting."""
    client_ip = request.client.host if request.client else "unknown"
    if not _check_analytics_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Analytics rate limit exceeded")

    event = body.event
    path = body.path
    meta = body.meta

    user_id = None
    try:
        from app.middleware.auth import decode_token
        import jose
        from app.config import settings
        cookies = request.cookies
        token = cookies.get("pp_token")
        if token:
            payload = jose.jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
            user_id = payload.get("sub")
    except Exception:
        pass

    await track_event(event=event, path=path, user_id=user_id, meta=meta, ip_address=client_ip)
    return {"ok": True}


@router.get("/admin/realtime")
async def admin_realtime(admin=Depends(require_admin)):
    """Admin: real-time stats."""
    return await get_realtime_stats()


@router.get("/admin/visitors")
async def admin_visitors(days: int = 30, admin=Depends(require_admin)):
    """Admin: daily visitor stats."""
    return await get_visitor_stats(min(days, 90))


@router.get("/admin/pages")
async def admin_pages(days: int = 7, admin=Depends(require_admin)):
    """Admin: top pages by views."""
    return await get_page_stats(min(days, 30))


@router.get("/admin/features")
async def admin_features(days: int = 7, admin=Depends(require_admin)):
    """Admin: feature usage breakdown."""
    return await get_feature_usage(min(days, 30))


@router.get("/admin/hourly")
async def admin_hourly(days: int = 7, admin=Depends(require_admin)):
    """Admin: hourly traffic distribution."""
    return await get_hourly_distribution(min(days, 30))


@router.get("/admin/geo")
async def admin_geo(days: int = 30, admin=Depends(require_admin)):
    """Admin: geo breakdown by IP address."""
    return await get_geo_breakdown(min(days, 90))


@router.get("/admin/retention")
async def admin_retention(days: int = 30, admin=Depends(require_admin)):
    """Admin: new vs returning visitor stats."""
    return await get_retention_stats(min(days, 90))


@router.get("/admin/users")
async def admin_users(days: int = 30, limit: int = 50, admin=Depends(require_admin)):
    """Admin: user list with activity stats."""
    return await get_user_list(min(days, 90), limit)


@router.get("/admin/summary")
async def admin_summary(admin=Depends(require_admin)):
    """Admin: aggregate user stats summary."""
    return await get_user_stats_summary()


@router.get("/cache-metrics")
async def cache_metrics(admin=Depends(require_admin)):
    """Admin: cache hit/miss stats and backend health."""
    from app.services.cache import cache
    stats = cache.stats() if hasattr(cache, "stats") else {}
    return {
        "cache": stats,
        "redis_connected": getattr(cache, "redis_connected", False),
        "backend": getattr(cache, "backend", "unknown"),
    }