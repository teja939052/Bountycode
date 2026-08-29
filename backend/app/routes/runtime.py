from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, RedirectResponse

router = APIRouter(prefix="/api/v1/runtime", tags=["local-runtime"])

# ──────────────────────────────────────────────────────────────────
# Serve Worker Files
# ──────────────────────────────────────────────────────────────────

@router.get("/workers/python.worker.js")
async def get_python_worker():
    """Serve Pyodide worker JavaScript."""
    from app.services.local_runtime import PYODIDE_WORKER_JS
    return PlainTextResponse(PYODIDE_WORKER_JS, media_type="application/javascript")

@router.get("/workers/js.worker.js")
async def get_js_worker():
    """Serve JavaScript worker."""
    from app.services.local_runtime import JAVASCRIPT_WORKER_JS
    return PlainTextResponse(JAVASCRIPT_WORKER_JS, media_type="application/javascript")

@router.get("/pyodide/{path:path}")
async def get_pyodide_file(path: str):
    """Proxy Pyodide files from CDN."""
    # In production, serve from local static or CDN
    # For development, redirect to CDN
    return RedirectResponse(url=f"https://cdn.jsdelivr.net/pyodide/v0.25.1/full/{path}")

# ──────────────────────────────────────────────────────────────────
# Worker Initialization Config
# ──────────────────────────────────────────────────────────────────

@router.get("/config")
async def get_runtime_config():
    """Get runtime configuration for frontend."""
    return {
        "python": {
            "enabled": True,
            "worker_url": "/api/v1/runtime/workers/python.worker.js",
            "pyodide_cdn": "https://cdn.jsdelivr.net/pyodide/v0.25.1/full/",
            "default_packages": ["micropip", "numpy"],
            "timeout_ms": 10000,
            "max_output_chars": 50000,
        },
        "javascript": {
            "enabled": True,
            "worker_url": "/api/v1/runtime/workers/js.worker.js",
            "timeout_ms": 5000,
            "max_output_chars": 10000,
        },
        "cpp": {
            "enabled": False,  # Requires Emscripten - not implemented
            "note": "C++ execution requires server-side compilation or Emscripten port",
        },
        "java": {
            "enabled": False,  # Requires TeaVM/CheerpJ - not implemented
            "note": "Java execution requires server-side compilation or TeaVM port",
        },
    }

# ──────────────────────────────────────────────────────────────────
# Execution Endpoints (for server-side fallback if needed)
# ──────────────────────────────────────────────────────────────────

# Note: The primary execution happens in browser Workers.
# These endpoints are for cases where browser execution is not available
# or for server-side verification of OA/boss challenges.

@router.post("/execute/python")
async def execute_python_server_fallback(
    code: str,
    stdin: str = "",
    timeout: int = 5000,
):
    """
    Server-side Python execution fallback.
    WARNING: This executes arbitrary code on the server!
    Only enable in development or with proper sandboxing.
    """
    # In production: DISABLED or use secure sandbox
    # For now, return unavailable
    return {
        "success": False,
        "error": "Server-side Python execution disabled. Use browser Pyodide Worker.",
        "stdout": "",
        "stderr": "",
    }

@router.post("/execute/javascript")
async def execute_javascript_server_fallback(
    code: str,
    stdin: str = "",
    timeout: int = 5000,
):
    """
    Server-side JavaScript execution fallback.
    WARNING: This executes arbitrary code on the server!
    """
    return {
        "success": False,
        "error": "Server-side JS execution disabled. Use browser Worker.",
        "stdout": "",
        "stderr": "",
    }