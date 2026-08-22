"""Health check and monitoring system for production observability."""

import asyncio
import time
from datetime import datetime, timedelta

from app.utils.timeutil import utcnow
from typing import Dict, Any, Optional
import logging
import httpx
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

logger = logging.getLogger(__name__)


class HealthChecker:
    """Comprehensive health check system for all critical services."""

    def __init__(self, db: Optional[AsyncIOMotorDatabase] = None):
        self.db = db
        self.last_check = {}
        self.check_interval = 30  # seconds

    async def check_database(self) -> Dict[str, Any]:
        """Check MongoDB connectivity and performance."""
        start = time.time()
        try:
            # Ping database
            await self.db.command("ping")
            duration = (time.time() - start) * 1000  # ms
            
            return {
                "status": "healthy" if duration < 100 else "degraded",
                "latency_ms": round(duration, 2),
                "message": "MongoDB responding normally" if duration < 100 else "Database slow",
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "message": "Cannot connect to MongoDB",
            }

    async def check_ai_service(self) -> Dict[str, Any]:
        """Check OpenRouter AI service connectivity."""
        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Simple health check ping to OpenRouter
                response = await client.get("https://openrouter.ai/api/v1/models")
                duration = (time.time() - start) * 1000
                
                if response.status_code == 200:
                    return {
                        "status": "healthy",
                        "latency_ms": round(duration, 2),
                        "message": "OpenRouter API responding",
                    }
                else:
                    return {
                        "status": "degraded",
                        "status_code": response.status_code,
                        "message": "OpenRouter API not responding normally",
                    }
        except asyncio.TimeoutError:
            return {
                "status": "unhealthy",
                "error": "timeout",
                "message": "OpenRouter API timeout",
            }
        except Exception as e:
            logger.error(f"AI service health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "message": "Cannot reach OpenRouter API",
            }

    async def check_cache_service(self) -> Dict[str, Any]:
        """Check Redis cache connectivity."""
        try:
            from app.services.cache import cache
            
            start = time.time()
            # Test set/get operation
            test_key = f"health_check_{int(time.time())}"
            await cache.set(test_key, "ok", 10)
            value = await cache.get(test_key)
            duration = (time.time() - start) * 1000
            
            if value == "ok":
                return {
                    "status": "healthy",
                    "latency_ms": round(duration, 2),
                    "message": "Cache service operational",
                }
            else:
                return {
                    "status": "unhealthy",
                    "message": "Cache set/get mismatch",
                }
        except Exception as e:
            logger.warning(f"Cache health check failed (non-critical): {e}")
            return {
                "status": "degraded",
                "error": str(e),
                "message": "Cache service unavailable (using in-memory)",
            }

    async def check_memory_usage(self) -> Dict[str, Any]:
        """Check application memory usage."""
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            memory_percent = process.memory_percent()
            
            status = "healthy"
            if memory_percent > 80:
                status = "warning"
            elif memory_percent > 90:
                status = "critical"
            
            return {
                "status": status,
                "memory_mb": round(memory_info.rss / 1024 / 1024, 2),
                "memory_percent": round(memory_percent, 2),
                "message": f"Memory usage {memory_percent}%",
            }
        except Exception as e:
            logger.warning(f"Memory check failed: {e}")
            return {
                "status": "unknown",
                "error": str(e),
                "message": "Cannot determine memory usage",
            }

    async def check_request_queue(self) -> Dict[str, Any]:
        """Check if request queue is healthy."""
        try:
            from app.services.job_queue import job_queue
            
            queue_size = len(job_queue.queue) if hasattr(job_queue, 'queue') else 0
            status = "healthy"
            
            if queue_size > 100:
                status = "warning"
            if queue_size > 500:
                status = "critical"
            
            return {
                "status": status,
                "queue_size": queue_size,
                "message": f"Job queue has {queue_size} pending tasks",
            }
        except Exception as e:
            logger.warning(f"Queue check failed: {e}")
            return {
                "status": "unknown",
                "message": "Queue status unavailable",
            }

    async def full_health_check(self) -> Dict[str, Any]:
        """Run all health checks in parallel."""
        checks = await asyncio.gather(
            self.check_database(),
            self.check_ai_service(),
            self.check_cache_service(),
            self.check_memory_usage(),
            self.check_request_queue(),
            return_exceptions=True,
        )

        db_check, ai_check, cache_check, memory_check, queue_check = checks

        # Determine overall status
        all_statuses = [
            db_check.get("status"),
            ai_check.get("status"),
            cache_check.get("status"),
            memory_check.get("status"),
            queue_check.get("status"),
        ]

        if "unhealthy" in all_statuses:
            overall = "unhealthy"
        elif "critical" in all_statuses:
            overall = "critical"
        elif "degraded" in all_statuses or "warning" in all_statuses:
            overall = "degraded"
        else:
            overall = "healthy"

        return {
            "status": overall,
            "timestamp": utcnow().isoformat(),
            "checks": {
                "database": db_check,
                "ai_service": ai_check,
                "cache": cache_check,
                "memory": memory_check,
                "request_queue": queue_check,
            },
            "uptime_seconds": int(time.time()),
        }

    async def is_healthy(self) -> bool:
        """Quick check if system is in acceptable state."""
        health = await self.full_health_check()
        return health["status"] in ["healthy", "degraded"]


# Global health checker instance
_health_checker: Optional[HealthChecker] = None


async def init_health_checker(db: AsyncIOMotorDatabase):
    """Initialize global health checker."""
    global _health_checker
    _health_checker = HealthChecker(db)
    logger.info("Health checker initialized")


def get_health_checker() -> HealthChecker:
    """Get global health checker instance."""
    if _health_checker is None:
        raise RuntimeError("Health checker not initialized")
    return _health_checker
