"""Admin monitoring and operations dashboard."""

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta

from app.utils.timeutil import utcnow
from typing import Optional
import re
import logging

from app.middleware.auth import get_current_user, require_admin
from app.database import get_db
from app.services.health_checker import get_health_checker
from app.services.feature_flags import get_feature_manager, FeatureStatus

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])
logger = logging.getLogger(__name__)


@router.get("/dashboard/overview")
async def admin_dashboard_overview(admin=Depends(require_admin), db=Depends(get_db)):
    """Get admin dashboard overview with key metrics."""
    try:
        users_collection = db["users"]
        billing_collection = db["billing_transactions"]
        
        # Calculate metrics
        total_users = await users_collection.count_documents({})
        
        paid_users = await users_collection.count_documents({
            "tier": {"$in": ["pro", "lifetime"]}
        })
        
        # Today's signups
        today_start = utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_signups = await users_collection.count_documents({
            "created_at": {"$gte": today_start}
        })
        
        # Active users (last 7 days)
        week_ago = utcnow() - timedelta(days=7)
        active_users = await users_collection.count_documents({
            "last_login": {"$gte": week_ago}
        })
        
        # Revenue metrics
        today_revenue = await billing_collection.aggregate([
            {
                "$match": {
                    "created_at": {"$gte": today_start},
                    "status": "completed"
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$amount"}
                }
            }
        ]).to_list(None)
        
        today_revenue_amount = today_revenue[0]["total"] if today_revenue else 0
        
        # MRR calculation (from last 30 days)
        month_ago = utcnow() - timedelta(days=30)
        mrr_data = await billing_collection.aggregate([
            {
                "$match": {
                    "created_at": {"$gte": month_ago},
                    "status": "completed",
                    "plan": {"$in": ["pro", "lifetime"]}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$amount"}
                }
            }
        ]).to_list(None)
        
        mrr = (mrr_data[0]["total"] / 30) if mrr_data else 0
        
        return {
            "timestamp": utcnow().isoformat(),
            "metrics": {
                "total_users": total_users,
                "paid_users": paid_users,
                "paid_percentage": round((paid_users / total_users * 100) if total_users > 0 else 0, 2),
                "today_signups": today_signups,
                "active_users_7d": active_users,
                "today_revenue": round(today_revenue_amount, 2),
                "estimated_mrr": round(mrr, 2),
            },
        }
        
    except Exception as e:
        logger.error(f"Dashboard overview error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard")


@router.get("/system/health")
async def system_health_report(admin=Depends(require_admin)):
    """Get comprehensive system health report."""
    try:
        checker = get_health_checker()
        health = await checker.full_health_check()
        return health
    except Exception as e:
        logger.error(f"Health report error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get health report")


@router.get("/feature-flags")
async def list_feature_flags(admin=Depends(require_admin)):
    """List all feature flags and their status."""
    try:
        manager = get_feature_manager()
        flags = await manager.get_all_flags()
        
        return {
            "feature_flags": [
                {
                    "name": flag.name,
                    "status": flag.status.value,
                    "rollout_percentage": flag.rollout_percentage,
                    "description": flag.description,
                    "users_allowlist": len(flag.users_allowlist),
                    "users_blocklist": len(flag.users_blocklist),
                }
                for flag in flags.values()
            ],
            "total_flags": len(flags),
        }
    except Exception as e:
        logger.error(f"Feature flags error: {e}")
        raise HTTPException(status_code=500, detail="Failed to list feature flags")


@router.post("/feature-flags/{flag_name}/update-status")
async def update_feature_flag_status(
    flag_name: str,
    status: str,
    admin=Depends(require_admin)
):
    """Update feature flag status (enabled/disabled/beta/gradual)."""
    try:
        manager = get_feature_manager()
        
        # Validate status
        valid_statuses = ["disabled", "internal", "beta", "gradual", "enabled"]
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Valid: {valid_statuses}")
        
        await manager.update_flag(flag_name, status=FeatureStatus(status))
        
        logger.info(f"Admin {admin['_id']} updated flag {flag_name} to {status}")
        
        return {
            "success": True,
            "message": f"Feature flag '{flag_name}' updated to {status}",
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update flag error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update flag")


@router.post("/feature-flags/{flag_name}/set-rollout")
async def set_feature_flag_rollout(
    flag_name: str,
    rollout_percentage: int,
    admin=Depends(require_admin)
):
    """Set feature flag rollout percentage for gradual deployment."""
    try:
        if not 0 <= rollout_percentage <= 100:
            raise HTTPException(status_code=400, detail="Rollout must be 0-100")
        
        manager = get_feature_manager()
        await manager.update_flag(flag_name, rollout_percentage=rollout_percentage)
        
        logger.info(f"Admin {admin['_id']} set {flag_name} rollout to {rollout_percentage}%")
        
        return {
            "success": True,
            "message": f"Rollout for '{flag_name}' set to {rollout_percentage}%",
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Set rollout error: {e}")
        raise HTTPException(status_code=500, detail="Failed to set rollout")


@router.get("/users/search")
async def search_users(
    email: Optional[str] = None,
    user_id: Optional[str] = None,
    admin=Depends(require_admin),
    db=Depends(get_db)
):
    """Search for users by email or ID."""
    try:
        users_collection = db["users"]
        
        query = {}
        if email:
            query["email"] = {"$regex": re.escape(email), "$options": "i"}
        elif user_id:
            from bson import ObjectId
            if not ObjectId.is_valid(user_id):
                raise HTTPException(status_code=400, detail="Invalid user_id format")
            query["_id"] = ObjectId(user_id)
        else:
            raise HTTPException(status_code=400, detail="Provide email or user_id")
        
        users = await users_collection.find(query).limit(10).to_list(None)
        
        return {
            "users": [
                {
                    "id": str(u["_id"]),
                    "email": u.get("email"),
                    "name": u.get("name"),
                    "plan": u.get("plan", "free"),
                    "created_at": u.get("created_at"),
                    "last_login": u.get("last_login"),
                }
                for u in users
            ],
            "count": len(users),
        }
        
    except Exception as e:
        logger.error(f"Search users error: {e}")
        raise HTTPException(status_code=500, detail="Failed to search users")


@router.get("/revenue/breakdown")
async def revenue_breakdown(
    days: int = 30,
    admin=Depends(require_admin),
    db=Depends(get_db)
):
    """Get revenue breakdown by plan type."""
    try:
        billing_collection = db["billing_transactions"]
        
        since = utcnow() - timedelta(days=days)
        
        revenue_by_plan = await billing_collection.aggregate([
            {
                "$match": {
                    "created_at": {"$gte": since},
                    "status": "completed"
                }
            },
            {
                "$group": {
                    "_id": "$plan",
                    "count": {"$sum": 1},
                    "total": {"$sum": "$amount"}
                }
            }
        ]).to_list(None)
        
        return {
            "period_days": days,
            "breakdown": [
                {
                    "plan": item["_id"],
                    "transactions": item["count"],
                    "total_revenue": round(item["total"], 2),
                }
                for item in revenue_by_plan
            ],
        }
        
    except Exception as e:
        logger.error(f"Revenue breakdown error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get revenue breakdown")
