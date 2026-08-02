"""Prevents duplicate requests from double-clicks within a time window."""
import asyncio
import time
import hashlib
import json
import os
from pathlib import Path
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

PERSISTENCE_FILE = Path(__file__).parent.parent.parent.parent / "data" / "duplicate_hashes.json"


class DuplicateRequestGuard(BaseHTTPMiddleware):
    """Blocks identical POST/PUT/DELETE requests within the dedup window."""

    def __init__(self, app, dedup_window_ms: int = 2000):
        super().__init__(app)
        self._seen: dict[str, float] = {}
        self._window = dedup_window_ms / 1000
        self._lock = asyncio.Lock()
        self._load_persisted()

    def _load_persisted(self):
        try:
            if PERSISTENCE_FILE.exists():
                with open(PERSISTENCE_FILE, "r") as f:
                    data = json.load(f)
                    now = time.time()
                    self._seen = {
                        k: v for k, v in data.items() if now - v < self._window * 2
                    }
        except Exception:
            self._seen = {}

    def _persist(self):
        try:
            PERSISTENCE_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(PERSISTENCE_FILE, "w") as f:
                json.dump(self._seen, f)
        except Exception:
            pass

    async def dispatch(self, request, call_next):
        if request.method not in ("POST", "PUT", "DELETE"):
            return await call_next(request)

        # Fire-and-forget telemetry is sent repeatedly with identical bodies
        # (page views, error reports) — never dedupe it.
        path = request.url.path
        if path.startswith("/api/v1/analytics/track") or path.startswith("/api/v1/debug/log"):
            return await call_next(request)

        body = await request.body()
        client_ip = request.client.host if request.client else "unknown"
        request_id = getattr(request.state, "request_id", None) or ""
        key = hashlib.sha256(
            f"{client_ip}:{path}:{request_id}:{body[:2048]}".encode()
        ).hexdigest()

        now = time.time()
        async with self._lock:
            if key in self._seen and now - self._seen[key] < self._window:
                return JSONResponse(
                    {"detail": "Duplicate request"}, status_code=429
                )
            self._seen[key] = now
            self._seen = {
                k: v for k, v in self._seen.items() if now - v < self._window * 2
            }
            self._persist()

        return await call_next(request)
