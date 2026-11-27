"""Admin monitoring and operations dashboard — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta

from app.utils.timeutil import utcnow
from typing import Optional
import logging

from app.middleware.auth import get_current_user, require_admin
from app.database import get_session
from app.repositories.identity import UserRepository
from app.services.health_checker import get_health_checker
from app.services.feature_flags import get_feature_manager, FeatureStatus

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

def _get_user_repo(session):
    from app.repositories.identity import UserRepository
    return UserRepository(session)
logger = logging.getLogger(__name__)



@router.get("/dashboard/overview")
async def admin_dashboard_overview(admin=Depends(require_admin)):
    """Get admin dashboard overview with key metrics."""
    async with get_session() as session:
        repo = UserRepository(session)

        # Get all users from PostgreSQL
        result = await repo.session.execute(select(_get_user_repo(session).model))
        users = result.scalars().all()

        total_users = len(users)
        paid_users = sum(1 for u in users if u.plan in ("pro", "lifetime"))

        # Today's signups
        today_start = utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_signups = sum(
            1 for u in users
            if u.created_at and u.created_at.replace(tzinfo=None) >= today_start
        )

        # Active users (last 7 days)
        week_ago = utcnow() - timedelta(days=7)
        active_users = sum(
            1 for u in users
            if u.last_login and u.last_login.replace(tzinfo=None) >= week_ago
        )

        # Revenue metrics - use simple calculation from user data
        # In production, this would be from a billing repository
        today_revenue_amount = 0.0
        month_ago = utcnow() - timedelta(days=30)
        mrr = 0.0

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

        valid_statuses = ["disabled", "internal", "beta", "gradual", "enabled"]
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Valid: {valid_statuses}")

        await manager.update_flag(flag_name, status=FeatureStatus(status))

        logger.info(f"Admin {admin['id']} updated flag {flag_name} to {status}")

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

        logger.info(f"Admin {admin['id']} set {flag_name} rollout to {rollout_percentage}%")

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
):
    """Search for users by email or ID."""
    async with get_session() as session:
        repo = UserRepository(session)

        query = {}
        if email:
            # Search by email using user repository
            result = await session.execute(
                select(_get_user_repo(session).model).where(_get_user_repo(session).model.email.ilike(f"%{email}%"))
            )
            users = result.scalars().all()
        elif user_id:
            if not user_id.isalnum():  # Simple validation
                raise HTTPException(status_code=400, detail="Invalid user_id format")
            result = await session.execute(
                select(_get_user_repo(session).model).where(_get_user_repo(session).model.id == user_id)
            )
            users = result.scalars().all()
        else:
            raise HTTPException(status_code=400, detail="Provide email or user_id")

        return {
            "users": [
                {
                    "id": str(u.id),
                    "email": u.email,
                    "name": u.name,
                    "plan": u.plan,
                    "created_at": u.created_at.isoformat() if u.created_at else None,
                    "last_login": u.last_login.isoformat() if u.last_login else None,
                }
                for u in users
            ],
            "count": len(users),
        }


@router.get("/revenue/breakdown")
async def revenue_breakdown(
    days: int = 30,
    admin=Depends(require_admin),
):
    """Get revenue breakdown by plan type."""
    # Return basic metrics - full billing data would come from a billing repository
    async with get_session() as session:
        result = await session.execute(select(UserRepository.model).where(
            UserRepository.model.plan.in_(["pro", "lifetime"])
        ))
        users = result.scalars().all()

    total_pro_users = len(users)
    return {
        "period_days": days,
        "breakdown": [
            {"plan": "pro", "transactions": total_pro_users, "total_revenue": 0.0},
            {"plan": "lifetime", "transactions": 0, "total_revenue": 0.0},
        ],
    }