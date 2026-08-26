"""
Revenue & conversion-funnel analytics.

Owner-facing endpoint to see the free -> trial -> paid funnel and an
approximate MRR, so the business can be optimized toward $1M ARR.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClientSession

from app.middleware.auth import get_current_user, require_admin
from app.database import users_collection, trials_collection

router = APIRouter(prefix="/api/v1/revenue", tags=["Revenue"])

# Approximate monthly recurring value per plan (USD).
_PLAN_MRR = {
    "pro": 19,
    "team": 145,
    "enterprise": 99,
    "pro_yearly": 99 / 12,
    "lifetime": 0,  # one-time, not recurring
    "trial": 0,
    "free": 0,
}


@router.get("/funnel")
async def revenue_funnel(admin=Depends(require_admin)):
    now = datetime.now(timezone.utc)

    # Count users by current plan.
    by_plan = {}
    async for doc in users_collection.aggregate([{"$group": {"_id": "$plan", "count": {"$sum": 1}}}]):
        by_plan[doc["_id"] or "unknown"] = doc["count"]

    total_users = sum(by_plan.values())
    paid_plans = ["pro", "pro_yearly", "team", "enterprise", "lifetime"]
    paid_users = sum(by_plan.get(p, 0) for p in paid_plans)
    active_trials = by_plan.get("trial", 0)
    free_users = by_plan.get("free", 0)

    # Trial volume from the dedicated trials collection.
    trial_signups = await trials_collection.count_documents({})
    trial_converted = await trials_collection.count_documents({"converted": True})
    expired_trials = await trials_collection.count_documents(
        {"trial_end": {"$lt": now}}
    )

    # Approximate MRR.
    mrr = sum(_PLAN_MRR.get(p, 0) * c for p, c in by_plan.items())
    arr = mrr * 12

    # Conversion signals.
    # True trial->paid rate (attributed via converted flag at purchase).
    trial_to_paid = round(trial_converted / trial_signups * 100, 1) if trial_signups else 0.0
    # Overall paying share of the user base.
    paying_share = round(paid_users / total_users * 100, 1) if total_users else 0.0

    return {
        "total_users": total_users,
        "by_plan": by_plan,
        "free_users": free_users,
        "active_trials": active_trials,
        "trial_signups": trial_signups,
        "trial_converted": trial_converted,
        "expired_trials": expired_trials,
        "paid_users": paid_users,
        "paying_share_pct": paying_share,
        "trial_to_paid_rate_pct": trial_to_paid,
        "mrr_usd": round(mrr, 2),
        "arr_usd": round(arr, 2),
        "note": "MRR is approximate (pro_yearly users counted at monthly equiv; lifetime is one-time).",
    }


@router.get("/summary")
async def revenue_summary(admin=Depends(require_admin)):
    funnel = await revenue_funnel(admin)
    return {
        "mrr_usd": funnel["mrr_usd"],
        "arr_usd": funnel["arr_usd"],
        "paying_share_pct": funnel["paying_share_pct"],
        "trial_to_paid_rate_pct": funnel["trial_to_paid_rate_pct"],
        "paid_users": funnel["paid_users"],
        "total_users": funnel["total_users"],
    }
