"""
Analytics service — page views, sessions, feature usage tracking.
"""
from datetime import datetime, timezone, timedelta
from app.database import analytics_events_collection, users_collection
from app.database import analytics_rollups_collection


async def track_event(event: str, path: str = "", user_id: str = None, meta: dict = None):
    """Track an analytics event (page_view, feature_use, etc.)."""
    now = datetime.now(timezone.utc)
    doc = {
        "event": event,
        "path": path,
        "user_id": user_id,
        "meta": meta or {},
        "timestamp": now.isoformat(),
        "timestamp_dt": now,
        "date": now.strftime("%Y-%m-%d"),
        "hour": now.hour,
    }
    await analytics_events_collection.insert_one(doc)
    await _update_rollups(doc)


async def _update_rollups(doc: dict):
    """Increment rollup counters for fast dashboard queries."""
    bucket = doc.get("event", "unknown")
    date = doc.get("date")
    path = doc.get("path", "")
    user_id = doc.get("user_id")
    update = {
        "$inc": {"count": 1},
        "$setOnInsert": {
            "bucket": bucket,
            "date": date,
            "created_at": datetime.now(timezone.utc),
        },
        "$max": {"updated_at": datetime.now(timezone.utc)},
    }
    await analytics_rollups_collection.update_one(
        {"bucket": bucket, "date": date},
        update,
        upsert=True,
    )
    if path:
        await analytics_rollups_collection.update_one(
            {"bucket": f"{bucket}:path:{path}", "date": date},
            {
                "$inc": {"count": 1},
                "$setOnInsert": {
                    "bucket": f"{bucket}:path:{path}",
                    "date": date,
                    "created_at": datetime.now(timezone.utc),
                },
                "$max": {"updated_at": datetime.now(timezone.utc)},
            },
            upsert=True,
        )
    if user_id:
        await analytics_rollups_collection.update_one(
            {"bucket": f"{bucket}:user:{user_id}", "date": date},
            {
                "$inc": {"count": 1},
                "$setOnInsert": {
                    "bucket": f"{bucket}:user:{user_id}",
                    "date": date,
                    "created_at": datetime.now(timezone.utc),
                },
                "$max": {"updated_at": datetime.now(timezone.utc)},
            },
            upsert=True,
        )


async def get_visitor_stats(days: int = 30):
    """Get daily visitor stats for the last N days."""
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    summary = await _get_rollup_series("page_view", since, days, group_by="date")
    if summary:
        return summary
    pipeline = [
        {"$match": {"event": "page_view", "date": {"$gte": since}}},
        {"$group": {
            "_id": "$date",
            "total_views": {"$sum": 1},
            "unique_visitors": {"$addToSet": "$user_id"},
        }},
        {"$project": {
            "date": "$_id",
            "total_views": 1,
            "unique_visitors": {"$size": "$unique_visitors"},
        }},
        {"$sort": {"date": 1}},
    ]
    cursor = analytics_events_collection.aggregate(pipeline)
    results = []
    async for doc in cursor:
        doc.pop("_id", None)
        results.append(doc)
    return results


async def get_page_stats(days: int = 7):
    """Get top pages by views."""
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    summary = await _get_rollup_top_paths("page_view", since, limit=20)
    if summary:
        return summary
    pipeline = [
        {"$match": {"event": "page_view", "date": {"$gte": since}}},
        {"$group": {"_id": "$path", "views": {"$sum": 1}, "unique_users": {"$addToSet": "$user_id"}}},
        {"$project": {"path": "$_id", "views": 1, "unique_users": {"$size": "$unique_users"}}},
        {"$sort": {"views": -1}},
        {"$limit": 20},
    ]
    cursor = analytics_events_collection.aggregate(pipeline)
    results = []
    async for doc in cursor:
        doc.pop("_id", None)
        results.append(doc)
    return results


async def get_feature_usage(days: int = 7):
    """Get feature usage breakdown."""
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    summary = await _get_rollup_top_paths("feature_use", since, feature_mode=True)
    if summary:
        return summary
    pipeline = [
        {"$match": {"event": "feature_use", "date": {"$gte": since}}},
        {"$group": {"_id": "$path", "uses": {"$sum": 1}, "unique_users": {"$addToSet": "$user_id"}}},
        {"$project": {"feature": "$_id", "uses": 1, "unique_users": {"$size": "$unique_users"}}},
        {"$sort": {"uses": -1}},
    ]
    cursor = analytics_events_collection.aggregate(pipeline)
    results = []
    async for doc in cursor:
        doc.pop("_id", None)
        results.append(doc)
    return results


async def get_realtime_stats():
    """Get real-time stats: today's views, active users, total users."""
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    hour_ago = now - timedelta(hours=1)

    today_pipeline = [
        {"$match": {"event": "page_view", "date": today}},
        {"$group": {"_id": None, "total": {"$sum": 1}, "unique": {"$addToSet": "$user_id"}}},
    ]
    today_cursor = analytics_events_collection.aggregate(today_pipeline)
    today_doc = {"total": 0, "unique": 0}
    async for d in today_cursor:
        today_doc = {"total": d["total"], "unique": len(d.get("unique", []))}

    active_pipeline = [
        {"$match": {"event": "page_view", "timestamp_dt": {"$gte": hour_ago}}},
        {"$group": {"_id": "$user_id"}},
        {"$count": "total"},
    ]
    active_cursor = analytics_events_collection.aggregate(active_pipeline)
    active = 0
    async for d in active_cursor:
        active = d["total"]

    total_users = await users_collection.count_documents({})

    return {
        "today_views": today_doc["total"],
        "today_unique": today_doc["unique"],
        "active_last_hour": active,
        "total_users": total_users,
    }


async def _get_rollup_series(event: str, since: str, days: int, group_by: str = "date"):
    cursor = analytics_rollups_collection.find(
        {"bucket": event, "date": {"$gte": since}},
        {"date": 1, "count": 1},
    ).sort("date", 1)
    rows = []
    async for doc in cursor:
        rows.append({
            "date": doc.get("date"),
            "total_views": doc.get("count", 0),
            "unique_visitors": 0,
        })
    return rows if rows else None


async def _get_rollup_top_paths(event: str, since: str, limit: int = 20, feature_mode: bool = False):
    bucket_prefix = f"{event}:path:"
    cursor = analytics_rollups_collection.find(
        {"bucket": {"$regex": f"^{bucket_prefix}"}, "date": {"$gte": since}},
        {"bucket": 1, "count": 1},
    )
    totals = {}
    async for doc in cursor:
        path = doc.get("bucket", "").replace(bucket_prefix, "", 1)
        totals[path] = totals.get(path, 0) + doc.get("count", 0)
    if not totals:
        return None
    rows = []
    for path, count in sorted(totals.items(), key=lambda item: item[1], reverse=True)[:limit]:
        if feature_mode:
            rows.append({"feature": path, "uses": count, "unique_users": 0})
        else:
            rows.append({"path": path, "views": count, "unique_users": 0})
    return rows


async def refresh_rollups(days: int = 2):
    """Rebuild recent rollups from raw events to heal any missed writes."""
    start = datetime.now(timezone.utc) - timedelta(days=days)
    pipeline = [
        {"$match": {"timestamp_dt": {"$gte": start}}},
        {"$group": {
            "_id": {"bucket": "$event", "date": "$date", "path": "$path", "user_id": "$user_id"},
            "count": {"$sum": 1},
        }},
    ]

    async for doc in analytics_events_collection.aggregate(pipeline):
        key = doc["_id"]
        bucket = key.get("bucket", "unknown")
        date = key.get("date")
        path = key.get("path", "") or ""
        user_id = key.get("user_id")

        await analytics_rollups_collection.update_one(
            {"bucket": bucket, "date": date},
            {
                "$setOnInsert": {
                    "bucket": bucket,
                    "date": date,
                    "created_at": datetime.now(timezone.utc),
                },
                "$max": {"updated_at": datetime.now(timezone.utc)},
                "$set": {"count": doc.get("count", 0)},
            },
            upsert=True,
        )

        if path:
            await analytics_rollups_collection.update_one(
                {"bucket": f"{bucket}:path:{path}", "date": date},
                {
                    "$setOnInsert": {
                        "bucket": f"{bucket}:path:{path}",
                        "date": date,
                        "created_at": datetime.now(timezone.utc),
                    },
                    "$max": {"updated_at": datetime.now(timezone.utc)},
                    "$set": {"count": doc.get("count", 0)},
                },
                upsert=True,
            )

        if user_id:
            await analytics_rollups_collection.update_one(
                {"bucket": f"{bucket}:user:{user_id}", "date": date},
                {
                    "$setOnInsert": {
                        "bucket": f"{bucket}:user:{user_id}",
                        "date": date,
                        "created_at": datetime.now(timezone.utc),
                    },
                    "$max": {"updated_at": datetime.now(timezone.utc)},
                    "$set": {"count": doc.get("count", 0)},
                },
                upsert=True,
            )


async def get_hourly_distribution(days: int = 7):
    """Get page views by hour of day."""
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    pipeline = [
        {"$match": {"event": "page_view", "date": {"$gte": since}}},
        {"$group": {"_id": "$hour", "views": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]
    cursor = analytics_events_collection.aggregate(pipeline)
    results = []
    async for doc in cursor:
        results.append({"hour": doc["_id"], "views": doc["views"]})
    return results
