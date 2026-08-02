"""Main FastAPI application with improved structure, logging, and error handling."""

import logging
import sys
import time
import asyncio
import uuid
import os
try:
    import resource
    HAS_RESOURCE = True
except ImportError:
    HAS_RESOURCE = False  # Windows
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
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
from app.services.structured_logging import (
    setup_structured_logging,
    request_id_var,
    new_request_id,
    log_context,
)
from app.services.request_metrics import metrics as request_metrics
from app.services.circuit_breaker import ai_breaker, compiler_breaker
from app.services.migrations import run_migrations
from app.middleware.rate_limiter import RateLimiterMiddleware
from app.middleware.duplicate_guard import DuplicateRequestGuard

# Import all route modules
from app.routes import (
    auth, debug, interview, interview_feedback, interview_replay, referral_system, guild_castle, shareable_achievements, campus_pulse, trending_challenges, resume, billing, aptitude, cover_letter,
    system_design, salary, company_prep, coding, gamification,
    hook_model, free_practice, enhanced, student_features,
    predictor, real_features, questions, questions_solve, company_conversion,
    career_profile, practice, analytics, ai_feedback, enterprise,
    trial, student_discount, profile_stats, compiler, problems,
    mock_interview, personal_dashboard, readiness, ai_debugger, concepts,
    daily_challenge, discussions, playlists, company_mocks,
    cards, wizard, submissions, progress, features,
    battles, visualizations, distributions, aptitude_tests,
    system_design_tests, indian_placement, placement_questions,
    dsa_fingerprint, energy, learning, analytics_admin,
    adaptive_learning, learning_journeys, community, scrims,
    rank, project_generator, learning_modules,
    interview_booking, language_paths,
    free_trial, onboarding,
    showcase, admin_content,
    game_events, campus, college_network,
    steam_profile,
    world, prestige, merchant,
    guilds, dungeons,
    collection, live_events,
    metrics, economy, journey,
    coupon, referral, revenue,
    career_rpg,
    newspaper,
    timeline,
    lucky_wheel,
    chat,
    seasons,
    achievements,
    tournaments,
    teams,
    economy,
     referrals,
     skill_trees,
     battle_pass,
campus_connect,
    campus_wars,
    spaced_repetition,
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
        
        # Run schema migrations
        try:
            await run_migrations()
        except Exception as e:
            logger.warning(f"Migration warning (non-fatal): {e}")
        
        # Initialize cache
        redis_url = getattr(settings, 'REDIS_URL', '')
        await init_cache(redis_url)
        logger.info(f"Cache initialized (Redis: {'enabled' if redis_url else 'in-memory'})")

        analytics_rollup_task = asyncio.create_task(_analytics_rollup_worker())

        # Start periodic metrics flush (every 5 minutes)
        await request_metrics.start_periodic_flush(300)

        yield
        
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise
    finally:
        # Shutdown: close all connections
        logger.info("Shutting down PlacementPro API...")
        await request_metrics.stop_periodic_flush()
        if analytics_rollup_task:
            analytics_rollup_task.cancel()
            try:
                await analytics_rollup_task
            except asyncio.CancelledError:
                pass
        await close_http_client()
        await close_db()
        if cache.redis and cache.redis.client:
            await cache.redis.disconnect()
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
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_error_payload(request, 500, "An internal server error occurred"),
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


# ============================================================
# Middleware
# ============================================================

# Logging middleware
app.add_middleware(LoggingMiddleware)

# Security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# Request ID middleware
app.add_middleware(RequestIdMiddleware)

# GZip response compression
app.add_middleware(GZipMiddleware, minimum_size=1024)

# Rate limiting middleware (with Redis support if configured)
app.add_middleware(
    RateLimiterMiddleware,
    use_redis=bool(settings.REDIS_URL)
)

# Duplicate request guard (prevents double-clicks)
app.add_middleware(DuplicateRequestGuard, dedup_window_ms=2000)

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
    ],
)


# ============================================================
# Routes
# ============================================================

# Include all route routers
app.include_router(auth.router)
app.include_router(debug.router)
app.include_router(interview.router)
app.include_router(resume.router)
app.include_router(billing.router)
app.include_router(aptitude.router)
app.include_router(cover_letter.router)
app.include_router(system_design.router)
app.include_router(salary.router)
app.include_router(company_prep.router)
app.include_router(coding.router)
app.include_router(gamification.router)
app.include_router(hook_model.router)
app.include_router(free_practice.router)
app.include_router(enhanced.router)
app.include_router(student_features.router)
app.include_router(predictor.router)
app.include_router(real_features.router)
app.include_router(questions.router)
app.include_router(company_conversion.router)
app.include_router(career_profile.router)
app.include_router(practice.router)
app.include_router(analytics.router)
app.include_router(ai_feedback.router)
app.include_router(enterprise.router)
app.include_router(trial.router)
app.include_router(student_discount.router)
app.include_router(profile_stats.router)
app.include_router(compiler.router)
app.include_router(problems.router)
app.include_router(mock_interview.router)
app.include_router(personal_dashboard.router)
app.include_router(readiness.router)
app.include_router(ai_debugger.router)
app.include_router(concepts.router)
app.include_router(daily_challenge.router)
app.include_router(daily_challenge.challenge_router)
app.include_router(discussions.router)
app.include_router(playlists.router)
app.include_router(company_mocks.router)
app.include_router(cards.router)
app.include_router(wizard.router)
app.include_router(submissions.router)
app.include_router(progress.router)
app.include_router(features.router)
app.include_router(battles.router)
app.include_router(visualizations.router)
app.include_router(distributions.router)
app.include_router(aptitude_tests.router)
app.include_router(system_design_tests.router)
app.include_router(indian_placement.router)
app.include_router(placement_questions.router)
app.include_router(dsa_fingerprint.router)
app.include_router(energy.router)
app.include_router(learning.router)
app.include_router(analytics_admin.router)
app.include_router(adaptive_learning.router)
app.include_router(learning_journeys.router)
app.include_router(community.router)
app.include_router(scrims.router)
app.include_router(rank.router)
app.include_router(project_generator.router)
app.include_router(learning_modules.router)
app.include_router(interview_booking.router)
app.include_router(language_paths.router)
app.include_router(showcase.router)
app.include_router(admin_content.router)
app.include_router(admin_content.assignments_router)
app.include_router(game_events.router)
app.include_router(campus.router)
app.include_router(college_network.router)
app.include_router(campus_connect.router)
app.include_router(campus_wars.router)
app.include_router(battle_pass.router)
app.include_router(interview_feedback.router)
app.include_router(interview_replay.router)
app.include_router(referral_system.router)
app.include_router(guild_castle.router)
app.include_router(shareable_achievements.router)
app.include_router(campus_pulse.router)
app.include_router(trending_challenges.router)
app.include_router(steam_profile.router)
app.include_router(world.router)
app.include_router(world.skill_router)
app.include_router(prestige.router)
app.include_router(merchant.router)
app.include_router(guilds.router)
app.include_router(dungeons.router)
app.include_router(collection.router)
app.include_router(live_events.router)
app.include_router(metrics.router)
app.include_router(economy.router)
app.include_router(career_rpg.router)
app.include_router(timeline.router)
app.include_router(free_trial.router)
app.include_router(onboarding.router)
app.include_router(coupon.router)
app.include_router(referral.router)
app.include_router(revenue.router)
app.include_router(newspaper.router)
app.include_router(lucky_wheel.router)
app.include_router(chat.router)
app.include_router(seasons.router)
app.include_router(achievements.router)
app.include_router(tournaments.router)
app.include_router(teams.router)
app.include_router(economy.router)
app.include_router(referrals.router)
app.include_router(skill_trees.router)
app.include_router(spaced_repetition.router)
logger.info(f"Loaded {len(app.routes)} routes")


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
