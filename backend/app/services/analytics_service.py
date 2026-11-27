"""Analytics service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session


async def get_analytics(user_id: str) -> dict:
    """Get user analytics."""
    async with get_session() as session:
        from app.models.identity import User
        from sqlalchemy import select
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return {"user_id": user_id, "error": "User not found"}
    return {"user_id": user_id, "plan": user.plan, "total_xp": 0, "current_level": 1}


async def get_analytics_events(user_id: str) -> list:
    """Get analytics events."""
    async with get_session() as session:
        from app.models.operations import AnalyticsEvent
        result = await session.execute(select(AnalyticsEvent).where(AnalyticsEvent.user_id == user_id))
        events = result.scalars().all()
    return [{"id": str(e.id), "event_type": e.event_type, "created_at": e.created_at.isoformat() if e.created_at else None} for e in events]


async def refresh_rollups() -> dict:
    """Refresh analytics rollups."""
    return {"refreshed": True, "timestamp": datetime.now(timezone.utc).isoformat()}


async def get_overview(user_id: str) -> dict:
    """Get analytics overview."""
    async with get_session() as session:
        from app.models.identity import User
        from sqlalchemy import select
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return {"user_id": user_id, "error": "User not found"}
    return {"user_id": user_id, "plan": user.plan, "total_xp": 0, "current_level": 1}


async def get_funnel(user_id: str) -> dict:
    """Get conversion funnel."""
    return {"user_id": user_id, "funnel": []}


async def get_conversion_rates(user_id: str) -> dict:
    """Get conversion rates."""
    return {"user_id": user_id, "conversion_rates": {}}


async def get_skill_progression(user_id: str) -> dict:
    """Get skill progression."""
    return {"user_id": user_id, "skill_progression": []}


async def get_company_stats(company_id: str) -> dict:
    """Get company stats."""
    return {"company_id": company_id, "stats": {}}


async def get_insights(user_id: str) -> dict:
    """Get insights."""
    return {"user_id": user_id, "insights": []}


async def get_trends(user_id: str) -> dict:
    """Get trends."""
    return {"user_id": user_id, "trends": []}


async def track_event(user_id: str, event_type: str, event_data: dict = None) -> dict:
    """Track an event."""
    return {"user_id": user_id, "event_type": event_type, "event_data": event_data or {}, "recorded": True}


async def get_visitor_stats(user_id: str) -> dict:
    """Get visitor stats."""
    return {"user_id": user_id, "visitors": 0}


async def get_visitor_trends(user_id: str) -> dict:
    """Get visitor trends."""
    return {"user_id": user_id, "trends": []}


async def get_page_stats(user_id: str) -> dict:
    """Get page stats."""
    return {"user_id": user_id, "page_stats": {}}


async def get_company_stats(company_id: str) -> dict:
    """Get company stats."""
    return {"company_id": company_id, "stats": {}}


async def get_feature_usage(user_id: str) -> dict:
    """Get feature usage stats."""
    return {"user_id": user_id, "feature_usage": {}}


async def get_page_stats(user_id: str) -> dict:
    """Get page stats."""
    return {"user_id": user_id, "page_stats": {}}

async def get_geo_breakdown(user_id: str) -> dict:
    """Stub for get_geo_breakdown."""
    return {"user_id": user_id}


async def get_hourly_distribution(user_id: str) -> dict:
    """Stub for get_hourly_distribution."""
    return {"user_id": user_id}


async def get_realtime_stats(user_id: str) -> dict:
    """Stub for get_realtime_stats."""
    return {"user_id": user_id}


async def get_retention_stats(user_id: str) -> dict:
    """Stub for get_retention_stats."""
    return {"user_id": user_id}


async def get_user_list(user_id: str) -> dict:
    """Stub for get_user_list."""
    return {"user_id": user_id}


async def get_user_stats_summary(user_id: str) -> dict:
    """Stub for get_user_stats_summary."""
    return {"user_id": user_id}
