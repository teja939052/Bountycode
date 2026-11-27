"""Beta funnel telemetry queries.

Run with::

    cd backend
    python -m app.scripts.beta_funnel

Outputs funnel metrics from PostgreSQL analytics_events.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone, timedelta
from collections import defaultdict

from sqlalchemy import select, func, and_

from app.database import get_session
from app.models.operations import AnalyticsEvent


FUNNEL_EVENTS = [
    "beta_signup_complete",
    "beta_onboarding_complete",
    "beta_activation",
    "beta_first_mission_complete",
    "beta_oa_start",
    "beta_oa_complete",
]


async def get_funnel(days: int = 14) -> dict:
    since = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    since = since - timedelta(days=days)

    async with get_session() as session:
        result = await session.execute(
            select(
                AnalyticsEvent.event_type,
                func.count(func.distinct(AnalyticsEvent.user_id)).label("users"),
                func.count(AnalyticsEvent.id).label("total_occurrences"),
            )
            .where(and_(
                AnalyticsEvent.event_type.in_(FUNNEL_EVENTS),
                AnalyticsEvent.created_at >= since,
            ))
            .group_by(AnalyticsEvent.event_type)
        )
        rows = result.all()

    results = {}
    for event_type, users, total_occurrences in rows:
        results[event_type] = {
            "users": users or 0,
            "total_occurrences": total_occurrences or 0,
        }

    funnel = {}
    for event in FUNNEL_EVENTS:
        funnel[event] = results.get(event, {"users": 0, "total_occurrences": 0})

    return funnel


async def get_daily_signups(days: int = 14) -> dict:
    since = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    since = since - timedelta(days=days)

    async with get_session() as session:
        result = await session.execute(
            select(
                func.date(AnalyticsEvent.created_at).label("day"),
                func.count(AnalyticsEvent.id).label("count"),
            )
            .where(and_(
                AnalyticsEvent.event_type == "beta_signup_complete",
                AnalyticsEvent.created_at >= since,
            ))
            .group_by(func.date(AnalyticsEvent.created_at))
            .order_by(func.date(AnalyticsEvent.created_at))
        )
        rows = result.all()

    return {str(row.day): row.count for row in rows}


async def main():
    print("=== Beta Funnel (last 14 days) ===\n")
    funnel = await get_funnel(days=14)

    for event, data in funnel.items():
        print(f"{event}: {data['users']} users, {data['total_occurrences']} occurrences")

    print("\n=== Conversion Rates ===\n")
    signups = funnel.get("beta_signup_complete", {}).get("users", 0)
    onboarding = funnel.get("beta_onboarding_complete", {}).get("users", 0)
    activation = funnel.get("beta_activation", {}).get("users", 0)
    first_mission = funnel.get("beta_first_mission_complete", {}).get("users", 0)
    oa_start = funnel.get("beta_oa_start", {}).get("users", 0)
    oa_complete = funnel.get("beta_oa_complete", {}).get("users", 0)

    if signups:
        print(f"Signup → Onboarding: {onboarding}/{signups} = {onboarding/signups*100:.1f}%")
        print(f"Signup → Activation: {activation}/{signups} = {activation/signups*100:.1f}%")
        print(f"Signup → First Mission: {first_mission}/{signups} = {first_mission/signups*100:.1f}%")
        print(f"Signup → OA Start: {oa_start}/{signups} = {oa_start/signups*100:.1f}%")
        print(f"OA Start → OA Complete: {oa_complete}/{oa_start} = {oa_complete/oa_start*100:.1f}%" if oa_start else "OA Start → Complete: N/A")

    print("\n=== Daily Signups ===\n")
    daily = await get_daily_signups(days=14)
    for day, count in sorted(daily.items()):
        print(f"{day}: {count}")


if __name__ == "__main__":
    asyncio.run(main())
