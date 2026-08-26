"""
Analytics routes — tracking, admin dashboard, visitor stats.
"""
from fastapi import APIRouter, Depends, HTTPException, Request
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

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


@router.post("/track")
async def track(request: Request):
    """Track an analytics event. No auth required (public endpoint)."""
    try:
        body = await request.json()
    except Exception:
        body = {}

    event = body.get("event", "page_view")
    path = body.get("path", "")
    meta = body.get("meta", {})
    ip_address = request.client.host if request.client else None

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

    await track_event(event=event, path=path, user_id=user_id, meta=meta, ip_address=ip_address)
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