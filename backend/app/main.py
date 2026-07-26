"""Main FastAPI application with improved structure, logging, and error handling."""

import logging
import sys
import time
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import httpx

from app.config import get_settings
from app.database import init_db, close_db, ping_db, get_client
from app.services.cache import init_cache, cache
from app.services.ai import close_http_client
from app.middleware.rate_limiter import RateLimiterMiddleware

# Import all route modules
from app.routes import (
    auth, interview, resume, billing, aptitude, cover_letter,
    system_design, salary, company_prep, coding, gamification,
    hook_model, free_practice, enhanced, student_features,
    predictor, real_features, questions, company_conversion,
    career_profile, practice, analytics, ai_feedback, enterprise,
    trial, student_discount, profile_stats, compiler, problems,
    mock_interview, personal_dashboard, readiness, ai_debugger, concepts,
    daily_challenge, discussions, playlists, company_mocks,
    cards, wizard, submissions, progress, features,
    battles, visualizations, distributions, aptitude_tests,
    system_design_tests, indian_placement, placement_questions,
    dsa_fingerprint
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("placementpro.log")
    ]
)

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
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
        
        # Initialize cache
        redis_url = getattr(settings, 'REDIS_URL', '')
        await init_cache(redis_url)
        logger.info(f"Cache initialized (Redis: {'enabled' if redis_url else 'in-memory'})")
        
        yield
        
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise
    finally:
        # Shutdown: close all connections
        logger.info("Shutting down PlacementPro API...")
        await close_http_client()
        await close_db()
        if cache.redis and cache.redis.client:
            await cache.redis.disconnect()
        logger.info("Shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="PlacementPro API",
    version="1.1.0",
    description="AI-powered placement preparation platform",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ============================================================
# Exception Handlers
# ============================================================

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions with structured response."""
    logger.warning(f"HTTP {exc.status_code}: {exc.detail} - {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "path": request.url.path
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with detailed feedback."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(f"Validation error on {request.url.path}: {errors}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": 422,
                "message": "Validation error",
                "details": errors,
                "path": request.url.path
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unhandled exceptions gracefully."""
    logger.error(f"Unhandled error on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": 500,
                "message": "An internal server error occurred",
                "path": request.url.path
            }
        }
    )


# ============================================================
# Middleware: Logging (inline)
# ============================================================

class LoggingMiddleware(BaseHTTPMiddleware):
    """Request logging middleware."""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        logger.info(f"{request.method} {request.url.path}")
        
        try:
            response = await call_next(request)
            duration = (time.time() - start_time) * 1000
            response.headers["X-Response-Time"] = f"{duration:.2f}ms"
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
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://unpkg.com; "
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
        request_id = f"req_{int(time.time() * 1000)}"
        request.state.request_id = request_id
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

# Rate limiting middleware (with Redis support if configured)
app.add_middleware(
    RateLimiterMiddleware,
    use_redis=bool(settings.REDIS_URL)
)

# CORS middleware
origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
    expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset"],
)


# ============================================================
# Routes
# ============================================================

# Include all route routers
app.include_router(auth.router)
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
    """Detailed health check endpoint."""
    db_status = "connected" if await ping_db() else "disconnected"
    cache_status = "connected" if cache.redis and cache.redis.client else "in-memory"
    
    # Check AI service connectivity
    ai_status = "available"
    try:
        # Quick test with a simple prompt
        from app.services.ai import chat_completion
        # Don't actually call, just check API key
        if not settings.OPENROUTER_API_KEY:
            ai_status = "not_configured"
    except Exception:
        ai_status = "error"
    
    return {
        "status": "ok" if db_status == "connected" else "degraded",
        "version": app.version,
        "database": db_status,
        "cache": {
            "status": cache_status,
            "stats": cache.stats()
        },
        "ai": ai_status,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }


@app.get("/health/ready")
async def ready():
    """Readiness probe for orchestration."""
    db_ok = await ping_db()

    if db_ok:
        return {"ready": True}
    raise HTTPException(status_code=503, detail="Database not ready")



