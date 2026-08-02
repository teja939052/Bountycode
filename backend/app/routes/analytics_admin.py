"""
Analytics routes — tracking, admin dashboard, visitor stats.
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from app.middleware.auth import get_current_user
from app.services.analytics_service import (
    track_event,
    get_visitor_stats,
    get_page_stats,
    get_feature_usage,
    get_realtime_stats,
    get_hourly_distribution,
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

    # Try to get user_id from cookie (optional)
    user_id = None
    try:
        from app.middleware.auth import decode_token
        from fastapi.security import HTTPBearer
        import jose
        from app.config import settings
        cookies = request.cookies
        token = cookies.get("token")
        if token:
            payload = jose.jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
            user_id = payload.get("sub")
    except Exception:
        pass

    await track_event(event=event, path=path, user_id=user_id, meta=meta)
    return {"ok": True}


@router.get("/admin/realtime")
async def admin_realtime(user=Depends(get_current_user)):
    """Admin: real-time stats."""
    return await get_realtime_stats()


@router.get("/admin/visitors")
async def admin_visitors(days: int = 30, user=Depends(get_current_user)):
    """Admin: daily visitor stats."""
    return await get_visitor_stats(min(days, 90))


@router.get("/admin/pages")
async def admin_pages(days: int = 7, user=Depends(get_current_user)):
    """Admin: top pages by views."""
    return await get_page_stats(min(days, 30))


@router.get("/admin/features")
async def admin_features(days: int = 7, user=Depends(get_current_user)):
    """Admin: feature usage breakdown."""
    return await get_feature_usage(min(days, 30))


@router.get("/admin/hourly")
async def admin_hourly(days: int = 7, user=Depends(get_current_user)):
    """Admin: hourly traffic distribution."""
    return await get_hourly_distribution(min(days, 30))
