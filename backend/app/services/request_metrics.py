from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, List
from collections import defaultdict

logger = logging.getLogger(__name__)

# Lazy import to avoid circular dependency at module load time
_db_collection = None


def _get_service_metrics_collection():
    """Resolve the service_metrics collection once, then cache."""
    global _db_collection
    if _db_collection is None:
        from app.database import get_collection
        _db_collection = get_collection("service_metrics")
    return _db_collection


class RequestMetrics:
    """Lightweight in-memory metrics with optional MongoDB persistence."""

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._counts = defaultdict(int)
        self._latency_ms = defaultdict(float)
        self._failures = defaultdict(int)
        self._last_error: Dict[str, str] = {}
        self._last_seen: Dict[str, str] = {}
        self._flush_task: asyncio.Task | None = None

    # ── Recording ───────────────────────────────────────────────────

    async def record(
        self,
        service: str,
        outcome: str,
        duration_ms: float = 0.0,
        error: str | None = None,
    ) -> None:
        async with self._lock:
            key = f"{service}:{outcome}"
            self._counts[key] += 1
            self._latency_ms[service] += max(duration_ms, 0.0)
            self._last_seen[service] = datetime.now(timezone.utc).isoformat()
            if outcome == "failure":
                self._failures[service] += 1
                if error:
                    self._last_error[service] = error[:240]

    # ── In-memory snapshot ──────────────────────────────────────────

    async def snapshot(self) -> Dict[str, Any]:
        async with self._lock:
            services = set()
            for key in self._counts:
                service, _ = key.split(":", 1)
                services.add(service)
            return {
                "counts": dict(self._counts),
                "latency_ms_total": dict(self._latency_ms),
                "failures": dict(self._failures),
                "last_error": dict(self._last_error),
                "last_seen": dict(self._last_seen),
                "services": sorted(services),
            }

    # ── MongoDB persistence ─────────────────────────────────────────

    async def flush_to_db(self) -> None:
        """Write a snapshot of current metrics to the ``service_metrics`` collection."""
        try:
            snap = await self.snapshot()
            coll = _get_service_metrics_collection()
            doc = {
                "snapshot": snap,
                "timestamp": datetime.now(timezone.utc),
            }
            await coll.insert_one(doc)
            logger.debug("Metrics flushed to MongoDB")
        except Exception as exc:
            logger.warning(f"Failed to flush metrics to MongoDB: {exc}")

    async def start_periodic_flush(self, interval_seconds: float = 300) -> None:
        """Background loop: flush to DB every *interval_seconds* (default 5 min)."""
        if self._flush_task is not None:
            return  # already running
        self._flush_task = asyncio.create_task(self._flush_loop(interval_seconds))
        logger.info(
            f"Periodic metrics flush started (interval={interval_seconds}s)"
        )

    async def stop_periodic_flush(self) -> None:
        if self._flush_task:
            self._flush_task.cancel()
            try:
                await self._flush_task
            except asyncio.CancelledError:
                pass
            self._flush_task = None

    async def _flush_loop(self, interval: float) -> None:
        while True:
            try:
                await asyncio.sleep(interval)
                await self.flush_to_db()
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                logger.warning(f"Metrics flush loop error: {exc}")

    async def get_historical(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Retrieve recent metric snapshots from MongoDB for admin dashboard."""
        try:
            coll = _get_service_metrics_collection()
            cutoff = datetime.now(timezone.utc) - __import__("datetime").timedelta(
                hours=hours
            )
            cursor = coll.find(
                {"timestamp": {"$gte": cutoff}}, {"_id": 0}
            ).sort("timestamp", -1)
            return await cursor.to_list(length=200)
        except Exception as exc:
            logger.warning(f"Failed to read historical metrics: {exc}")
            return []


metrics = RequestMetrics()
