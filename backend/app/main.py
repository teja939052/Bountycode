"""Main FastAPI application with improved structure, logging, and error handling."""

import importlib
import json
import logging
import os
import pkgutil
import sys
import time
import asyncio
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

try:
    import resource
    HAS_RESOURCE = True
except ImportError:
    HAS_RESOURCE = False  # Windows

from fastapi import FastAPI, HTTPException, Request, status, WebSocket, WebSocketDisconnect, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import httpx

from app.config import get_settings
from app.database import init_db, close_db, ping_db, get_client
from app.services.cache import init_cache, cache
from app.services.ai import close_http_client
from app.services.analytics_service import refresh_rollups
from app.services.job_queue import init_job_queue, close_job_queue, get_job_queue, Job, JobType
from app.services.code_execution_worker import init_code_execution_worker, close_code_execution_worker
from app.services.websocket_manager import get_connection_manager, WebSocketHandler, WSMessage, MessageType
from app.services.structured_logging import (
    setup_structured_logging,
    request_id_var,
    new_request_id,
    log_context,
)
from app.services.request_metrics import metrics as request_metrics
from app.services.circuit_breaker import ai_breaker, compiler_breaker
from app.services.migrations import run_migrations
from app.services.health_checker import init_health_checker
from app.services.feature_flags import init_feature_flags
from app.services.idempotency import init_idempotency_manager
from app.services.indexing_strategy import create_all_indexes
from app.middleware.rate_limiter import RateLimiterMiddleware
from app.middleware.duplicate_guard import DuplicateRequestGuard
from app.middleware.route_safety import RouteErrorHandlingMiddleware
from app.middleware.auth import get_current_user_ws
from app.services.audit_log import log_audit


EXTRA_ROUTERS = {
    "daily_challenge": ["challenge_router"],
    "world": ["skill_router"],
}


def _register_routers(app: FastAPI) -> None:
    """Auto-discover and register all route routers from app/routes/.

    Scans the routes directory for modules containing a `router` attribute,
    and includes them in the FastAPI app. Special multi-router modules are
    handled via the EXTRA_ROUTERS mapping to ensure all sub-routers are
    registered correctly.
    """
    routes_dir = Path(__file__).parent / "routes"
    registered = []
    failures = []

    for module_info in pkgutil.iter_modules([str(routes_dir)]):
        module_name = module_info.name

        if module_name.startswith("_") or module_name == "__init__":
            continue

        try:
            module = importlib.import_module(f"app.routes.{module_name}")
        except Exception as exc:
            failures.append((module_name, f"{type(exc).__name__}: {exc}"))
            continue

        router = getattr(module, "router", None)
        if router is not None:
            app.include_router(router)
            registered.append(module_name)

        for extra_attr in EXTRA_ROUTERS.get(module_name, []):
            extra_router = getattr(module, extra_attr, None)
            if extra_router is not None:
                app.include_router(extra_router)
                registered.append(f"{module_name}.{extra_attr}")

    logger.info(f"Registered {len(registered)} routers: {', '.join(registered)}")

    if failures:
        details = "; ".join(f"{name} ({err})" for name, err in failures)
        raise RuntimeError(
            f"Failed to import {len(failures)} route module(s): {details}. "
            "Refusing to start with silently missing endpoints."
        )


# Setup structured logging (JSON format with correlation IDs)
setup_structured_logging()

logger = logging.getLogger(__name__)
settings = get_settings()
analytics_rollup_task: asyncio.Task | None = None


def _error_payload(request: Request, code: int, message: str, details=None):
    """Build the standard API error payload."""
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details,
            "path": request.url.path,
            "method": request.method,
            "request_id": getattr(request.state, "request_id", None),
        },
    }


async def _analytics_rollup_worker():
    """Periodically reconcile analytics rollups from raw events."""
    while True:
        try:
            await refresh_rollups(days=2)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.warning(f"Analytics rollup refresh failed: {exc}")
        await asyncio.sleep(300)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    global analytics_rollup_task
    logger.info("Starting PlacementPro API...")
    
    try:
        # Initialize database with retry
        for attempt in range(3):
            try:
                await init_db()
                logger.info("Database initialized successfully")
                break
            except Exception as e:
                if attempt == 2:
                    logger.error(f"Failed to initialize database after 3 attempts: {e}")
                    raise
                logger.warning(f"Database init attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(2)
        
        # Load question store into memory (seed files + MongoDB)
        try:
            from app.services import question_store
            question_store.load_all()
            await question_store.load_from_mongo()
            logger.info("Question store loaded into memory")
        except Exception as e:
            logger.warning(f"Question store initialization failed: {e}")
        
        # Get database client for remaining initialization
        db = get_client()[settings.DATABASE_NAME]
        
        # Run schema migrations
        try:
            await run_migrations()
        except Exception as e:
            logger.warning(f"Migration failed (continuing in degraded mode): {e}")
        
        # Create database indexes for optimal query performance
        try:
            await create_all_indexes(db)
            logger.info("Database indexes created successfully")
        except Exception as e:
            logger.warning(f"Index creation failed (non-fatal): {e}")
        
        # Initialize health checker
        try:
            await init_health_checker(db)
            logger.info("Health checker initialized")
        except Exception as e:
            logger.warning(f"Health checker initialization failed: {e}")
        
        # Initialize feature flags
        try:
            await init_feature_flags(db)
            logger.info("Feature flags initialized")
        except Exception as e:
            logger.warning(f"Feature flags initialization failed: {e}")
        
        # Initialize idempotency manager
        try:
            await init_idempotency_manager(db)
            logger.info("Idempotency manager initialized")
        except Exception as e:
            logger.warning(f"Idempotency manager initialization failed: {e}")
        
        # Initialize cache
        redis_url = getattr(settings, 'REDIS_URL', '')
        try:
            await init_cache(redis_url)
            logger.info(f"Cache initialized (Redis: {'enabled' if redis_url else 'in-memory'})")
        except Exception as e:
            logger.warning(f"Cache initialization failed, using in-memory fallback: {e}")

        # Initialize job queue and worker for async code execution
        try:
            await init_job_queue()
            await init_code_execution_worker()
            logger.info("Job queue and code execution worker initialized")
        except Exception as e:
            logger.warning(f"Job queue initialization failed (will use sync execution): {e}")

        # Initialize WebSocket manager
        get_connection_manager()
        logger.info("WebSocket manager initialized")

        try:
            analytics_rollup_task = asyncio.create_task(_analytics_rollup_worker())
        except Exception as e:
            logger.warning(f"Analytics rollup task could not be started: {e}")

        # Start periodic metrics flush (every 5 minutes)
        try:
            await request_metrics.start_periodic_flush(300)
        except Exception as e:
            logger.warning(f"Metrics flush could not be started: {e}")
        
        logger.info("PlacementPro API startup complete - all services initialized")

        yield
        
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise
    finally:
        # Shutdown: close all connections
        logger.info("Shutting down PlacementPro API...")
        try:
            await request_metrics.stop_periodic_flush()
        except Exception as e:
            logger.warning(f"Metrics flush shutdown failed: {e}")

        if analytics_rollup_task:
            analytics_rollup_task.cancel()
            try:
                await analytics_rollup_task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                logger.warning(f"Analytics rollup shutdown failed: {e}")

        for label, closer in (
            ("code execution worker", close_code_execution_worker),
            ("job queue", close_job_queue),
            ("AI HTTP client", close_http_client),
            ("database", close_db),
        ):
            try:
                await closer()
            except Exception as e:
                logger.warning(f"Shutdown step '{label}' failed: {e}")

        try:
            if cache.redis and cache.redis.client:
                await cache.redis.disconnect()
        except Exception as e:
            logger.warning(f"Cache shutdown failed: {e}")
        logger.info("Shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="PlacementPro API",
    version="1.2.0",
    description="AI-powered placement preparation platform with 53+ company prep, gamified learning, and system design practice",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "Auth", "description": "Registration, login, logout"},
        {"name": "Onboarding", "description": "Onboarding quest and first-run experience"},
        {"name": "Interview", "description": "AI mock interviews"},
        {"name": "Resume", "description": "Resume upload, generation, optimization"},
        {"name": "Aptitude", "description": "Aptitude test practice"},
        {"name": "Coding", "description": "Coding challenges and compiler"},
        {"name": "Questions", "description": "Question bank and problem solving"},
        {"name": "Learning", "description": "Language learning hub (C, C++, Java, Python)"},
        {"name": "Learning Modules", "description": "Duolingo-style step-by-step coding lessons"},
        {"name": "Gamification", "description": "XP, streaks, badges, tower progress"},
        {"name": "Analytics", "description": "Admin analytics dashboard"},
        {"name": "System Health", "description": "Health checks and metrics"},
    ],
)


# ============================================================
# Exception Handlers
# ============================================================

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions with structured response."""
    request_id = getattr(request.state, "request_id", None)
    logger.warning(
        "http_exception",
        extra=log_context(
            status_code=exc.status_code,
            path=request.url.path,
            method=request.method,
            request_id=request_id,
        ),
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_payload(request, exc.status_code, str(exc.detail)),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with detailed feedback."""
    request_id = getattr(request.state, "request_id", None)
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(
        "validation_error",
        extra=log_context(
            path=request.url.path,
            method=request.method,
            request_id=request_id,
            errors=errors,
        ),
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=_error_payload(request, 422, "Validation error", errors),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unhandled exceptions gracefully."""
    request_id = getattr(request.state, "request_id", None)
    logger.error(
        "unhandled_error",
        exc_info=True,
        extra=log_context(
            path=request.url.path,
            method=request.method,
            request_id=request_id,
        ),
    )
    # Surface the exception type + message so errors are diagnosable in the
    # browser console without requiring a server-terminal read. Guarded so it
    # never leaks secrets: only the class name + repr-length-capped message.
    import traceback as _tb
    debug = "PLACEEMEN_DEBUG" in os.environ
    payload = _error_payload(request, 500, "An internal server error occurred")
    if debug:
        payload["error_type"] = exc.__class__.__name__
        payload["error_detail"] = repr(exc)[:500]
        payload["traceback"] = _tb.format_exc()[:2000]
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=payload,
    )


# ============================================================
# Middleware: Logging (inline)
# ============================================================

class LoggingMiddleware(BaseHTTPMiddleware):
    """Request logging middleware with correlation IDs."""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_id = getattr(request.state, "request_id", None) or new_request_id()
        request.state.request_id = request_id
        request_id_var.set(request_id)
        logger.info(f"{request.method} {request.url.path}")
        
        try:
            response = await call_next(request)
            duration = (time.time() - start_time) * 1000
            response.headers["X-Response-Time"] = f"{duration:.2f}ms"
            response.headers["X-Request-ID"] = request_id
            logger.info(f"{request.method} {request.url.path} - {response.status_code} - {duration:.2f}ms")
            return response
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            logger.error(f"{request.method} {request.url.path} - ERROR - {duration:.2f}ms: {e}")
            raise


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' https://cdn.jsdelivr.net https://unpkg.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https://openrouter.ai https://api.openai.com; "
            "frame-src 'none'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Add request ID for tracing."""
    
    async def dispatch(self, request: Request, call_next):
        request_id = uuid.uuid4().hex
        request.state.request_id = request_id
        request_id_var.set(request_id)
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class ApiVersionMiddleware(BaseHTTPMiddleware):
    """Add API version header to all API responses."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/api/"):
            response.headers["X-API-Version"] = settings.API_VERSION
            response.headers["X-API-Latest-Version"] = settings.API_VERSION
        return response


# ============================================================
# Middleware
# ============================================================

# Route safety middleware should wrap the rest of the stack so unexpected
# exceptions become structured responses instead of tearing down requests.
app.add_middleware(RouteErrorHandlingMiddleware)

# Logging middleware
app.add_middleware(LoggingMiddleware)

# Security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# Request ID middleware
app.add_middleware(RequestIdMiddleware)

# API version header
app.add_middleware(ApiVersionMiddleware)

# GZip response compression
app.add_middleware(GZipMiddleware, minimum_size=1024)

# Rate limiting middleware (with Redis support if configured)
app.add_middleware(
    RateLimiterMiddleware,
    use_redis=bool(settings.REDIS_URL)
)

# Duplicate request guard (prevents double-clicks)
app.add_middleware(DuplicateRequestGuard, dedup_window_ms=2000)


class AuditLogMiddleware(BaseHTTPMiddleware):
    """Log admin actions for audit trail."""

    ADMIN_PREFIXES = ("/api/v1/admin", "/api/v1/assignments")

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        is_admin = any(path.startswith(prefix) for prefix in self.ADMIN_PREFIXES)

        if not is_admin:
            return await call_next(request)

        user = getattr(request.state, "user", None)
        if user is None:
            try:
                from app.middleware.auth import get_current_user
                user = await get_current_user(request)
            except Exception:
                user = None

        response = await call_next(request)

        if user:
            await log_audit(
                user_id=user.get("id", ""),
                action=request.method,
                resource=path,
                ip_address=request.client.host if request.client else "unknown",
            )

        return response


app.add_middleware(AuditLogMiddleware)

# CORS middleware
origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
        expose_headers=[
        "X-RateLimit-Limit",
        "X-RateLimit-Remaining",
        "X-RateLimit-Reset",
        "X-Request-ID",
        "X-Response-Time",
        "X-API-Version",
        "X-API-Latest-Version",
    ],
)


# ============================================================
# Routes
# ============================================================

_register_routers(app)


# ============================================================
# WebSocket Endpoint
# ============================================================

ws_manager = get_connection_manager()
ws_handler = WebSocketHandler(ws_manager)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str | None = Query(None)):
    """WebSocket endpoint for real-time updates.

    Connect with: ws://localhost:8000/ws?token=<JWT_TOKEN>
    (token also accepted from the `pp_token` cookie — httpOnly, sent automatically)
    """
    try:
        user = await get_current_user_ws(websocket, token)
    except HTTPException:
        await websocket.close(code=4001, reason="Authentication required")
        return
    if not user:
        await websocket.close(code=4001, reason="Authentication required")
        return

    user_id = user["id"]
    connected = await ws_manager.connect(websocket, user_id)
    if not connected:
        return

    # Send auth success
    await ws_manager.send_to_connection(websocket, WSMessage(
        type=MessageType.AUTH_SUCCESS,
        payload={"user_id": user_id, "message": "Connected to real-time updates"}
    ))

    try:
        while True:
            data = await websocket.receive_text()
            await ws_handler.handle_message(websocket, data)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error("WebSocket error", user_id=user_id, error=str(e))
    finally:
        ws_manager.disconnect(websocket)


# ============================================================
# Health & Status Endpoints
# ============================================================

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "PlacementPro API is running",
        "version": app.version,
        "status": "operational"
    }


@app.get("/health")
async def health():
    """Comprehensive health check: DB, circuit breakers, memory, version."""
    db_ok = await ping_db()
    cache_status = "connected" if cache.redis and cache.redis.client else "in-memory"

    # Circuit breaker states
    ai_state = ai_breaker.state
    compiler_state = compiler_breaker.state

    # Memory usage (Linux / macOS — resource module)
    try:
        if HAS_RESOURCE:
            mem_bytes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            # On Linux ru_maxrss is bytes; on macOS it's KiB
            if os.name != "nt" and mem_bytes > 1_000_000:
                mem_mb = round(mem_bytes / (1024 * 1024), 1)
            else:
                mem_mb = round(mem_bytes / 1024, 1) if mem_bytes > 0 else 0.0
        else:
            mem_mb = 0.0
    except Exception:
        mem_mb = 0.0

    # Metrics snapshot for quick glance
    metrics_snap = await request_metrics.snapshot()

    overall = "healthy"
    if not db_ok or ai_state["is_open"] or compiler_state["is_open"]:
        overall = "degraded"

    return {
        "status": overall,
        "version": app.version,
        "database": "connected" if db_ok else "disconnected",
        "cache": {"status": cache_status, "stats": cache.stats()},
        "circuit_breakers": {
            "ai": ai_state,
            "compiler": compiler_state,
        },
        "memory_mb": mem_mb,
        "metrics": {
            "services": metrics_snap["services"],
            "failures": metrics_snap["failures"],
            "last_error": metrics_snap["last_error"],
        },
        "timestamp": __import__("datetime").datetime.now().isoformat(),
    }


@app.get("/health/ready")
async def ready():
    """Readiness probe for orchestration."""
    db_ok = await ping_db()

    if db_ok:
        return {"ready": True}
    raise HTTPException(status_code=503, detail="Database not ready")
