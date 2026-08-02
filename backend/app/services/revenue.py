from datetime import datetime, timezone, timedelta
from typing import Optional
from app.database import (
    users_collection,
    payments_collection,
    revenue_events_collection,
    billing_metrics_collection,
)
from bson import ObjectId

MONTHLY_TARGET_MRR = 166667
ANNUAL_TARGET_ARR = 2000000


async def record_payment(
    user_id: str,
    amount: float,
    currency: str,
    plan: str,
    billing_cycle: str,
    payment_method: str,
    payment_id: str,
    status: str = "completed",
    metadata: Optional[dict] = None,
) -> dict:
    now = datetime.now(timezone.utc)
    doc = {
        "user_id": user_id,
        "amount": amount,
        "currency": currency,
        "plan": plan,
        "billing_cycle": billing_cycle,
        "payment_method": payment_method,
        "payment_id": payment_id,
        "status": status,
        "metadata": metadata or {},
        "created_at": now,
    }
    result = await payments_collection.insert_one(doc)

    await record_revenue_event(
        user_id=user_id,
        event_type="payment_completed",
        amount=amount,
        currency=currency,
        plan=plan,
        billing_cycle=billing_cycle,
        payment_method=payment_method,
        reference_id=str(result.inserted_id),
        metadata=metadata or {},
    )

    return {"payment_id": str(result.inserted_id), "amount": amount, "status": status}


async def record_revenue_event(
    user_id: str,
    event_type: str,
    amount: float,
    currency: str,
    plan: str,
    billing_cycle: str,
    payment_method: str,
    reference_id: str = "",
    metadata: Optional[dict] = None,
) -> dict:
    now = datetime.now(timezone.utc)
    doc = {
        "user_id": user_id,
        "event_type": event_type,
        "amount": amount,
        "currency": currency,
        "plan": plan,
        "billing_cycle": billing_cycle,
        "payment_method": payment_method,
        "reference_id": reference_id,
        "metadata": metadata or {},
        "created_at": now,
    }
    await revenue_events_collection.insert_one(doc)
    return {"status": "recorded", "event_type": event_type, "amount": amount}


async def get_monthly_recurring_revenue() -> dict:
    """Calculate current MRR from all completed recurring payments."""
    now = datetime.now(timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    pipeline = [
        {
            "$match": {
                "status": "completed",
                "created_at": {"$gte": month_start},
                "billing_cycle": {"$in": ["monthly", "yearly", "lifetime"]},
            }
        },
        {
            "$group": {
                "_id": None,
                "total_mrr": {"$sum": "$amount"},
                "count": {"$sum": 1},
            }
        },
    ]

    results = []
    async for doc in payments_collection.aggregate(pipeline):
        results.append(doc)

    total_mrr = results[0]["total_mrr"] if results else 0.0
    count = results[0]["count"] if results else 0

    active_pro = await users_collection.count_documents({"plan": "pro"})
    active_lifetime = await users_collection.count_documents({"plan": "lifetime"})
    active_team = await users_collection.count_documents({"plan": "team"})
    active_enterprise = await users_collection.count_documents({"plan": "enterprise"})
    active_free = await users_collection.count_documents({"plan": "free"})

    total_users = active_free + active_pro + active_lifetime + active_team + active_enterprise

    arpu = total_mrr / total_users if total_users > 0 else 0.0
    annualized_arr = total_mrr * 12

    target_mrr = MONTHLY_TARGET_MRR
    target_arr = ANNUAL_TARGET_ARR
    mrr_progress = min(total_mrr / target_mrr * 100, 100) if target_mrr > 0 else 0
    arr_progress = min(annualized_arr / target_arr * 100, 100) if target_arr > 0 else 0

    return {
        "mrr": round(total_mrr, 2),
        "monthly_payments": count,
        "arpu": round(arpu, 2),
        "annualized_arr": round(annualized_arr, 2),
        "target_arr": target_arr,
        "target_mrr": target_mrr,
        "mrr_progress_percent": round(mrr_progress, 1),
        "arr_progress_percent": round(arr_progress, 1),
        "active_users": {
            "free": active_free,
            "pro": active_pro,
            "lifetime": active_lifetime,
            "team": active_team,
            "enterprise": active_enterprise,
            "total": total_users,
        },
        "payments_by_plan": {
            "pro": active_pro,
            "lifetime": active_lifetime,
            "team": active_team,
            "enterprise": active_enterprise,
        },
        "timestamp": now.isoformat(),
    }


async def get_revenue_analytics(days: int = 30) -> dict:
    """Get revenue analytics for the last N days."""
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)

    pipeline = [
        {
            "$match": {
                "created_at": {"$gte": cutoff},
                "status": "completed",
            }
        },
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$created_at"},
                    "month": {"$month": "$created_at"},
                    "day": {"$dayOfMonth": "$created_at"},
                    "plan": "$plan",
                },
                "total_revenue": {"$sum": "$amount"},
                "count": {"$sum": 1},
                "avg_amount": {"$avg": "$amount"},
            }
        },
        {
            "$sort": {"_id.year": 1, "_id.month": 1, "_id.day": 1}
        },
    ]

    daily_data = []
    async for doc in payments_collection.aggregate(pipeline):
        key = doc["_id"]
        daily_data.append(
            {
                "date": f"{key['year']}-{key['month']:02d}-{key['day']:02d}",
                "plan": key["plan"],
                "revenue": round(doc["total_revenue"], 2),
                "count": doc["count"],
                "avg_amount": round(doc["avg_amount"], 2),
            }
        )

    total_revenue = sum(d["revenue"] for d in daily_data)
    total_payments = sum(d["count"] for d in daily_data)

    plan_breakdown = {}
    for d in daily_data:
        plan = d["plan"]
        if plan not in plan_breakdown:
            plan_breakdown[plan] = {"revenue": 0.0, "count": 0}
        plan_breakdown[plan]["revenue"] += d["revenue"]
        plan_breakdown[plan]["count"] += d["count"]

    for plan in plan_breakdown:
        plan_breakdown[plan]["revenue"] = round(plan_breakdown[plan]["revenue"], 2)
        plan_breakdown[plan]["avg_amount"] = round(
            plan_breakdown[plan]["revenue"] / plan_breakdown[plan]["count"], 2
        ) if plan_breakdown[plan]["count"] > 0 else 0

    events_pipeline = [
        {
            "$match": {
                "created_at": {"$gte": cutoff},
            }
        },
        {
            "$group": {
                "_id": "$event_type",
                "count": {"$sum": 1},
                "total_amount": {"$sum": "$amount"},
            }
        },
    ]

    event_summary = []
    async for doc in revenue_events_collection.aggregate(events_pipeline):
        event_summary.append(
            {
                "event_type": doc["_id"],
                "count": doc["count"],
                "total_amount": round(doc["total_amount"], 2),
            }
        )

    return {
        "period_days": days,
        "total_revenue": round(total_revenue, 2),
        "total_payments": total_payments,
        "daily_breakdown": daily_data,
        "plan_breakdown": plan_breakdown,
        "event_summary": event_summary,
        "timestamp": now.isoformat(),
    }


async def get_revenue_metrics() -> dict:
    """Get key revenue metrics for dashboard."""
    now = datetime.now(timezone.utc)

    mrr_data = await get_monthly_recurring_revenue()

    thirty_days_ago = now - timedelta(days=30)
    sixty_days_ago = now - timedelta(days=60)

    last_30_monthly = await payments_collection.count_documents({
        "status": "completed",
        "created_at": {"$gte": thirty_days_ago},
        "billing_cycle": "monthly",
    })

    last_30_yearly = await payments_collection.count_documents({
        "status": "completed",
        "created_at": {"$gte": thirty_days_ago},
        "billing_cycle": "yearly",
    })

    last_30_lifetime = await payments_collection.count_documents({
        "status": "completed",
        "created_at": {"$gte": thirty_days_ago},
        "billing_cycle": "lifetime",
    })

    last_30_team = await payments_collection.count_documents({
        "status": "completed",
        "created_at": {"$gte": thirty_days_ago},
        "plan": "team",
    })

    last_30_enterprise = await payments_collection.count_documents({
        "status": "completed",
        "created_at": {"$gte": thirty_days_ago},
        "plan": "enterprise",
    })

    prev_30_monthly = await payments_collection.count_documents({
        "status": "completed",
        "created_at": {"$gte": sixty_days_ago, "$lt": thirty_days_ago},
        "billing_cycle": "monthly",
    })

    prev_30_revenue_pipeline = [
        {
            "$match": {
                "status": "completed",
                "created_at": {"$gte": sixty_days_ago, "$lt": thirty_days_ago},
            }
        },
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}},
    ]
    prev_30_results = []
    async for doc in payments_collection.aggregate(prev_30_revenue_pipeline):
        prev_30_results.append(doc)
    prev_30_revenue = prev_30_results[0]["total"] if prev_30_results else 0.0

    current_revenue_pipeline = [
        {
            "$match": {
                "status": "completed",
                "created_at": {"$gte": thirty_days_ago},
            }
        },
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}},
    ]
    current_results = []
    async for doc in payments_collection.aggregate(current_revenue_pipeline):
        current_results.append(doc)
    current_30_revenue = current_results[0]["total"] if current_results else 0.0

    revenue_growth_pct = 0.0
    if prev_30_revenue > 0:
        revenue_growth_pct = round(((current_30_revenue - prev_30_revenue) / prev_30_revenue) * 100, 1)

    monthly_mrr_change = last_30_monthly - prev_30_monthly if prev_30_monthly > 0 else last_30_monthly

    total_revenue_all = await payments_collection.count_documents({"status": "completed"})

    return {
        "mrr": mrr_data["mrr"],
        "arr": mrr_data["annualized_arr"],
        "arpu": mrr_data["arpu"],
        "total_active_users": mrr_data["active_users"]["total"],
        "mrr_progress_percent": mrr_data["mrr_progress_percent"],
        "arr_progress_percent": mrr_data["arr_progress_percent"],
        "target_arr": ANNUAL_TARGET_ARR,
        "target_mrr": MONTHLY_TARGET_MRR,
        "last_30_days": {
            "new_monthly_subs": last_30_monthly,
            "new_yearly_subs": last_30_yearly,
            "new_lifetime_subs": last_30_lifetime,
            "new_team_subs": last_30_team,
            "new_enterprise_subs": last_30_enterprise,
            "revenue": round(current_30_revenue, 2),
            "revenue_growth_percent": revenue_growth_pct,
            "mrr_additions": monthly_mrr_change,
        },
        "total_payments": total_revenue_all,
        "timestamp": now.isoformat(),
    }
