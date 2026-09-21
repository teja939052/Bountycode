"""Beta funnel telemetry queries.

Run with::

    cd backend
    python -m app.scripts.beta_funnel

Outputs funnel metrics from MongoDB analytics_events.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from collections import defaultdict

from app.database import analytics_events_collection


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
    since = since - __import__("datetime").timedelta(days=days)

    pipeline = [
        {"$match": {
            "event": {"$in": FUNNEL_EVENTS},
            "timestamp_dt": {"$gte": since},
        }},
        {"$sort": {"timestamp_dt": 1}},
        {"$group": {
            "_id": {"user_id": "$user_id", "event": "$event"},
            "first_at": {"$min": "$timestamp_dt"},
            "count": {"$sum": 1},
        }},
        {"$group": {
            "_id": "$_id.event",
            "users": {"$addToSet": "$_id.user_id"},
            "total_occurrences": {"$sum": "$count"},
        }},
    ]

    cursor = analytics_events_collection.aggregate(pipeline)
    results = {}
    async for doc in cursor:
        results[doc["_id"]] = {
            "users": len(doc.get("users", [])),
            "total_occurrences": doc.get("total_occurrences", 0),
        }

    # Build ordered funnel
    funnel = {}
    for event in FUNNEL_EVENTS:
        funnel[event] = results.get(event, {"users": 0, "total_occurrences": 0})

    return funnel


async def get_daily_signups(days: int = 14) -> dict:
    since = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    since = since - __import__("datetime").timedelta(days=days)

    pipeline = [
        {"$match": {
            "event": "beta_signup_complete",
            "timestamp_dt": {"$gte": since},
        }},
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp_dt"}},
            "count": {"$sum": 1},
        }},
        {"$sort": {"_id": 1}},
    ]

    cursor = analytics_events_collection.aggregate(pipeline)
    return {doc["_id"]: doc["count"] async for doc in cursor}


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
