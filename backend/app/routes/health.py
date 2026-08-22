"""Health check and monitoring endpoints for production monitoring."""

from fastapi import APIRouter, Depends
from app.middleware.auth import get_current_user
from app.services.health_checker import get_health_checker, init_health_checker
from app.database import get_db

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("/ping")
async def ping():
    """Simple health check ping."""
    return {
        "status": "ok",
        "message": "PlacementPro API is running",
    }


@router.get("/status")
async def full_health_check():
    """
    Get comprehensive system health status.
    
    Returns:
    - Overall system status (healthy/degraded/unhealthy)
    - Database health
    - AI service health
    - Cache health
    - Memory usage
    - Request queue status
    """
    try:
        checker = get_health_checker()
        health_report = await checker.full_health_check()
        return health_report
    except Exception as e:
        return {
            "status": "unknown",
            "error": str(e),
            "message": "Health check failed",
        }


@router.get("/ready")
async def readiness():
    """
    Kubernetes-style readiness probe.
    Returns 200 if service is ready to accept traffic.
    """
    try:
        checker = get_health_checker()
        is_ready = await checker.is_healthy()
        
        if is_ready:
            return {"ready": True, "message": "Service is ready"}
        else:
            return {"ready": False, "message": "Service is degraded"}
            
    except Exception as e:
        return {"ready": False, "message": f"Readiness check failed: {e}"}


@router.get("/live")
async def liveness():
    """
    Kubernetes-style liveness probe.
    Returns 200 if service is alive (not stuck).
    """
    return {"alive": True, "message": "Service is alive"}


@router.get("/metrics")
async def get_metrics(user=Depends(get_current_user)):
    """Get system metrics (admin only)."""
    # Check if user is admin
    if not getattr(user, 'is_admin', False):
        return {"error": "Unauthorized", "status": 403}

    try:
        checker = get_health_checker()
        health = await checker.full_health_check()
        
        # Add additional metrics
        return {
            "health": health,
            "timestamp": health.get("timestamp"),
            "system_status": health.get("status"),
        }
    except Exception as e:
        return {"error": str(e), "status": 500}


@router.get("/dependencies")
async def check_dependencies():
    """Check all external service dependencies."""
    try:
        checker = get_health_checker()
        health = await checker.full_health_check()
        
        return {
            "dependencies": {
                "mongodb": health["checks"].get("database"),
                "openrouter_ai": health["checks"].get("ai_service"),
                "redis_cache": health["checks"].get("cache"),
                "job_queue": health["checks"].get("request_queue"),
            },
            "overall_status": health["status"],
        }
    except Exception as e:
        return {
            "error": str(e),
            "overall_status": "unknown",
        }
