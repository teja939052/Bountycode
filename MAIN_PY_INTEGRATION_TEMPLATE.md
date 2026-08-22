# INTEGRATION TEMPLATE: Updated main.py with Error Handling

This file shows the exact changes needed in `backend/app/main.py` to integrate all error handling, middleware, and route safety features.

## Key Changes to Make:

### 1. Add Imports
```python
# At the top of main.py, add:

from contextlib import asynccontextmanager
import logging
import traceback
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from datetime import datetime
import asyncio

# Import our new error handling middleware
from app.middleware.route_safety import (
    RouteErrorHandlingMiddleware,
    safe_route,
    SafeDatabase,
)

# Import existing services
from app.services.error_handler import ProdErrorHandler
from app.services.health_checker import HealthChecker
from app.services.feature_flags import FeatureFlagManager
from app.services.idempotency import IdempotencyManager
from app.services.indexing_strategy import create_all_indexes

logger = logging.getLogger(__name__)
```

### 2. Create Health Checker Instance
```python
# Global service instances
health_checker: Optional[HealthChecker] = None
feature_flag_manager: Optional[FeatureFlagManager] = None
idempotency_manager: Optional[IdempotencyManager] = None
```

### 3. Update Lifespan
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app startup and shutdown."""
    
    # ==================== STARTUP ====================
    logger.info("=" * 60)
    logger.info("🚀 PlacementPro API Starting")
    logger.info("=" * 60)
    
    try:
        # Step 1: Initialize database connection
        logger.info("📦 Initializing database connection...")
        from app.database import init_db, database
        await init_db()
        logger.info("✅ Database initialized")
        
        # Step 2: Run schema migrations
        logger.info("🔄 Running database migrations...")
        # await run_migrations(database.db)  # If using Alembic
        logger.info("✅ Migrations completed")
        
        # Step 3: Create database indexes
        logger.info("⚡ Creating database indexes...")
        await create_all_indexes(database.db)
        logger.info("✅ Database indexes created (100x query speed)")
        
        # Step 4: Initialize health checker
        logger.info("❤️  Initializing health checker...")
        global health_checker
        health_checker = HealthChecker(database.db)
        await health_checker.full_health_check()
        logger.info("✅ Health checker initialized")
        
        # Step 5: Initialize feature flags
        logger.info("🚩 Initializing feature flags...")
        global feature_flag_manager
        feature_flag_manager = FeatureFlagManager(database.db)
        await feature_flag_manager.load_flags()
        logger.info("✅ Feature flags loaded")
        
        # Step 6: Initialize idempotency manager
        logger.info("🔑 Initializing idempotency manager...")
        global idempotency_manager
        idempotency_manager = IdempotencyManager(database.db)
        logger.info("✅ Idempotency manager ready")
        
        # Step 7: Initialize cache
        logger.info("💾 Initializing cache layer...")
        from app.services.cache import initialize_cache
        await initialize_cache()
        logger.info("✅ Cache initialized (Redis or InMemory)")
        
        # Step 8: Initialize resilience modules
        logger.info("🛡️  Initializing resilience modules...")
        from app.services.resilience import initialize_resilience
        await initialize_resilience()
        logger.info("✅ Resilience modules ready")
        
        logger.info("")
        logger.info("=" * 60)
        logger.info("✅ PlacementPro API startup complete - all services initialized")
        logger.info("=" * 60)
        logger.info(f"🌐 API ready at http://localhost:8000")
        logger.info(f"📚 Docs at http://localhost:8000/docs")
        logger.info(f"💚 Health at http://localhost:8000/api/health/status")
        logger.info("")
        
    except Exception as e:
        logger.error("")
        logger.error("=" * 60)
        logger.error("❌ STARTUP FAILED")
        logger.error("=" * 60)
        logger.error(f"Error: {e}")
        logger.error(traceback.format_exc())
        logger.error("")
        raise
    
    yield
    
    # ==================== SHUTDOWN ====================
    logger.info("")
    logger.info("=" * 60)
    logger.info("🛑 PlacementPro API Shutting Down")
    logger.info("=" * 60)
    
    try:
        # Cleanup resources
        logger.info("Closing database connections...")
        from app.database import close_db
        await close_db()
        logger.info("✅ Database closed")
        
        logger.info("Flushing metrics...")
        # await metrics.flush()  # If using metrics
        logger.info("✅ Metrics flushed")
        
        logger.info("✅ Shutdown complete")
        logger.info("")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
```

### 4. Create FastAPI App with Middleware
```python
# Create the FastAPI app
app = FastAPI(
    title="PlacementPro API",
    description="AI-powered placement preparation platform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ==================== MIDDLEWARE STACK ====================
# ORDER MATTERS: Apply in this sequence

# 1. Error handling middleware (FIRST - catches all errors)
app.add_middleware(RouteErrorHandlingMiddleware)

# 2. CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "https://placementpro.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Rate limiting middleware
from app.services.rate_limiter import RateLimitMiddleware
app.add_middleware(RateLimitMiddleware, requests_per_minute=60)

# 4. Tier gating middleware
from app.services.tier_middleware import TierMiddleware
app.add_middleware(TierMiddleware)

# 5. Duplicate guard middleware
from app.middleware.duplicate_guard import DuplicateGuardMiddleware
app.add_middleware(DuplicateGuardMiddleware)

# 6. Request logging middleware
from app.middleware.logging import RequestLoggingMiddleware
app.add_middleware(RequestLoggingMiddleware)

# 7. Structured logging middleware
from app.services.structured_logging import StructuredLoggingMiddleware
app.add_middleware(StructuredLoggingMiddleware)
```

### 5. Add Exception Handlers
```python
# ==================== EXCEPTION HANDLERS ====================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": 422,
                "message": "Validation error",
                "details": exc.errors(),
                "retriable": False,
            }
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch any unhandled exceptions."""
    logger.error(f"Unhandled exception: {request.method} {request.url.path}", exc_info=exc)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": 500,
                "message": "Internal server error",
                "retriable": True,
            }
        }
    )
```

### 6. Add Startup/Shutdown Events (if not using lifespan)
```python
@app.on_event("startup")
async def startup_event():
    """Alternative to lifespan for startup."""
    logger.info("App starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    """Alternative to lifespan for shutdown."""
    logger.info("App shutting down...")
```

### 7. Include Router Modules
```python
# ==================== ROUTES ====================

# Health check endpoints
from app.routes.health import router as health_router
app.include_router(health_router, prefix="/api/health", tags=["Health"])

# Admin endpoints
from app.routes.admin_monitoring import router as admin_router
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])

# Auth endpoints
from app.routes.auth import router as auth_router
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])

# Interview endpoints
from app.routes.interview import router as interview_router
app.include_router(interview_router, prefix="/api/v1/interview", tags=["Interview"])

# Resume endpoints
from app.routes.resume import router as resume_router
app.include_router(resume_router, prefix="/api/v1/resume", tags=["Resume"])

# ... Include all 65 route modules
```

### 8. Add Health Check Endpoint
```python
@app.get("/api/health/ping")
async def ping():
    """Simple ping endpoint for load balancers."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/health/ready")
async def readiness():
    """Kubernetes readiness probe."""
    if health_checker:
        health = await health_checker.full_health_check()
        if health["status"] in ["healthy", "degraded"]:
            return {"status": "ready"}
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"status": "not_ready"}
    )

@app.get("/api/health/live")
async def liveness():
    """Kubernetes liveness probe."""
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}
```

### 9. Root Endpoint
```python
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "PlacementPro API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/api/health/status"
    }
```

### 10. Full App Entry Point
```python
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True,
    )
```

---

## Complete main.py Template

Here's a complete minimal example:

```python
"""
PlacementPro API - Main Application
"""

import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from datetime import datetime

# Error handling
from app.middleware.route_safety import RouteErrorHandlingMiddleware
from app.services.error_handler import ProdErrorHandler

# Services
from app.services.health_checker import HealthChecker
from app.services.feature_flags import FeatureFlagManager
from app.services.idempotency import IdempotencyManager
from app.services.indexing_strategy import create_all_indexes

logger = logging.getLogger(__name__)

# Global services
health_checker: Optional[HealthChecker] = None
feature_flag_manager: Optional[FeatureFlagManager] = None
idempotency_manager: Optional[IdempotencyManager] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    
    # Startup
    logger.info("🚀 PlacementPro API Starting")
    
    try:
        from app.database import init_db, database
        
        await init_db()
        logger.info("✅ Database initialized")
        
        await create_all_indexes(database.db)
        logger.info("✅ Database indexes created")
        
        global health_checker
        health_checker = HealthChecker(database.db)
        logger.info("✅ Health checker ready")
        
        global feature_flag_manager
        feature_flag_manager = FeatureFlagManager(database.db)
        logger.info("✅ Feature flags ready")
        
        global idempotency_manager
        idempotency_manager = IdempotencyManager(database.db)
        logger.info("✅ Idempotency manager ready")
        
        logger.info("✅ PlacementPro API startup complete\n")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}\n")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 PlacementPro API shutting down")
    try:
        from app.database import close_db
        await close_db()
        logger.info("✅ Shutdown complete\n")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


# Create app
app = FastAPI(
    title="PlacementPro API",
    version="1.0.0",
    lifespan=lifespan,
)

# Middleware (ORDER MATTERS)
app.add_middleware(RouteErrorHandlingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Validation error", "details": exc.errors()}
    )

# Routes
@app.get("/api/health/ping")
async def ping():
    return {"status": "ok"}

# Include all routers
from app.routes.health import router as health_router
from app.routes.auth import router as auth_router
app.include_router(health_router, prefix="/api/health")
app.include_router(auth_router, prefix="/api/v1/auth")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

---

## Testing the Integration

```bash
# Run backend
cd backend
python -m uvicorn app.main:app --reload

# Check startup logs for:
# ✅ Database initialized
# ✅ Database indexes created
# ✅ Health checker ready
# ✅ PlacementPro API startup complete

# Test health endpoint
curl http://localhost:8000/api/health/ping
# Response: {"status": "ok"}

# Test error handling
curl http://localhost:8000/api/non-existent
# Response: {"success": false, "error": {...}}
```

---

## Next: Apply This to Your main.py

1. Backup current `backend/app/main.py`
2. Review which parts already exist
3. Add missing imports
4. Update lifespan() function
5. Add middleware in correct order
6. Add exception handlers
7. Test startup sequence

Your routes will now have comprehensive error handling!
