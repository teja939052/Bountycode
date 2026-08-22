"""
Analytics service — page views, sessions, feature usage tracking.
Also supports geo-IP tracking and visitor retention.
"""
from datetime import datetime, timezone, timedelta
from app.database import analytics_events_collection, users_collection
from app.database import analytics_rollups_collection


async def track_event(
    event: str,
    path: str = "",
    user_id: str = None,
    meta: dict = None,
    ip_address: str = None,
):
    """Track an analytics event (page_view, feature_use, etc.).

    Optionally capture ip_address in meta for geo tracking.
    """
    now = datetime.now(timezone.utc)
    meta = meta or {}
    if ip_address:
        meta["ip_address"] = ip_address

    doc = {
        "event": event,
        "path": path,
        "user_id": user_id,
        "meta": meta,
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


async def _get_new_returning_stats(days: int = 30):
    """Get new vs returning visitor counts."""
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    # Users with only one event in the period are "new"; multiple events suggest "returning"
    pipeline = [
        {"$match": {"event": "page_view", "date": {"$gte": since}}},
        {"$group": {
            "_id": "$user_id",
            "event_count": {"$sum": 1},
            "first_date": {"$min": "$date"},
        }},
        {"$group": {
            "_id": "$event_count",
            "user_count": {"$sum": 1},
        }},
        {"$sort": {"_id": 1}},
    ]
    cursor = analytics_events_collection.aggregate(pipeline)
    results = {}
    async for doc in cursor:
        results[str(doc["_id"])] = doc["user_count"]
    return results


async def get_geo_breakdown(days: int = 30):
    """Get visitor breakdown by IP address (for geo tracking)."""
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    pipeline = [
        {"$match": {"event": "page_view", "date": {"$gte": since}, "meta.ip_address": {"$exists": True}}},
        {"$group": {
            "_id": "$meta.ip_address",
            "visits": {"$sum": 1},
        }},
        {"$sort": {"visits": -1}},
        {"$limit": 50},
    ]
    cursor = analytics_events_collection.aggregate(pipeline)
    results = []
    async for doc in cursor:
        results.append({"ip": doc["_id"], "visits": doc["visits"]})
    return results


async def get_retention_stats(days: int = 30):
    """Get new vs returning visitor percentages."""
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    # New users: had their first page_view in the period and no events before
    # Returning users: had at least one event before the period
    new_pipeline = [
        {"$match": {"event": "page_view", "date": {"$gte": since}}},
        {"$group": {"_id": "$user_id", "first_event": {"$min": "$timestamp_dt"}}},
        {"$match": {"first_event": {"$gte": datetime.now(timezone.utc) - timedelta(days=days)}}},
        {"$count": "new_users"},
    ]
    returning_pipeline = [
        {"$match": {"event": "page_view", "timestamp_dt": {"$lt": datetime.now(timezone.utc) - timedelta(days=days)}}},
        {"$group": {"_id": None, "count": {"$sum": 1}}},
        {"$count": "returning_users"},
    ]
    new_result = await analytics_events_collection.aggregate(new_pipeline).to_list(length=1)
    returning_result = await analytics_events_collection.aggregate(returning_pipeline).to_list(length=1)
    new_users = new_result[0]["new_users"] if new_result else 0
    returning_users = returning_result[0]["returning_users"] if returning_result else 0
    total = new_users + returning_users
    return {
        "new_users": new_users,
        "returning_users": returning_users,
        "retention_rate": round(returning_users / total * 100, 1) if total > 0 else 0,
        "total_visitors": total,
    }


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


async def get_user_list(days: int = 30, limit: int = 50):
    """Get registered users with their activity counts."""
    from bson import ObjectId

    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    pipeline = [
        {"$match": {"event": "page_view", "date": {"$gte": since}}},
        {"$group": {
            "_id": "$user_id",
            "total_views": {"$sum": 1},
            "last_active": {"$max": "$timestamp_dt"},
            "pages_visited": {"$addToSet": "$path"},
        }},
        {"$project": {
            "user_id": "$_id",
            "total_views": 1,
            "last_active": 1,
            "pages_count": {"$size": "$pages_visited"},
        }},
        {"$sort": {"total_views": -1}},
        {"$limit": limit},
    ]
    cursor = analytics_events_collection.aggregate(pipeline)
    results = []
    async for doc in cursor:
        doc.pop("_id", None)
        uid = doc.get("user_id")
        doc["is_registered"] = uid is not None and uid != ""
        if doc["is_registered"] and ObjectId.is_valid(uid):
            user_doc = await users_collection.find_one(
                {"_id": ObjectId(uid)},
                {"name": 1, "email": 1, "plan": 1, "created_at": 1},
            )
            if user_doc:
                doc["name"] = user_doc.get("name", "")
                doc["email"] = user_doc.get("email", "")
                doc["plan"] = user_doc.get("plan", "free")
        results.append(doc)
    return results


async def get_user_stats_summary():
    """Get aggregate user statistics."""
    total_users = await users_collection.count_documents({})
    pipeline = [
        {"$group": {
            "_id": "$plan",
            "count": {"$sum": 1},
        }},
    ]
    cursor = users_collection.aggregate(pipeline)
    plan_counts = {"free": 0, "pro": 0, "lifetime": 0}
    async for doc in cursor:
        plan_counts[doc["_id"]] = doc["count"]

    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    week_ago = (now - timedelta(days=7)).strftime("%Y-%m-%d")
    month_ago = (now - timedelta(days=30)).strftime("%Y-%m-%d")

    new_today = await users_collection.count_documents({"created_at": {"$gte": today}})
    new_this_week = await users_collection.count_documents({"created_at": {"$gte": week_ago}})
    new_this_month = await users_collection.count_documents({"created_at": {"$gte": month_ago}})

    active_users = 0
    try:
        active_pipeline = [
            {"$match": {"event": "page_view", "date": {"$gte": today}}},
            {"$group": {"_id": "$user_id"}},
            {"$count": "total"},
        ]
        cursor = analytics_events_collection.aggregate(active_pipeline)
        async for doc in cursor:
            active_users = doc["total"]
    except Exception:
        pass

    return {
        "total_users": total_users,
        "plan_counts": plan_counts,
        "new_today": new_today,
        "new_this_week": new_this_week,
        "new_this_month": new_this_month,
        "active_today": active_users,
    }
