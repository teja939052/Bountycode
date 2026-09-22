"""PlacementPro compiler microservice — standalone, Cloud Run free tier.

One job: execute untrusted Python/JavaScript with hard limits and return a
Piston-shaped dict. No app imports, no database, no AI. The main backend
calls POST /execute with a shared bearer secret and falls through to its
existing chain (Piston → Judge0 → local sandbox) on any failure.

Deploy: `gcloud run deploy compiler --source . --region us-central1 \
  --allow-unauthenticated --max-instances 4 --concurrency 4 \
  --memory 512Mi --cpu 1 --timeout 60s --no-cpu-throttling=False \
  --set-env-vars COMPILER_KEY=<secret>`
Free tier covers this comfortably (2M req/mo, scale-to-zero, us-central1).
Harden further in Cloud Run: run as non-root (Dockerfile), read-only
root filesystem + no VPC egress for the service, min-instances 0.
"""
from __future__ import annotations

import hashlib
import hmac
import os
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Optional

try:
    import resource as _resource
except ImportError:  # Windows / non-POSIX dev machines: limits enforced by
    _resource = None  # timeout + container caps instead (service runs on Linux).

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

MAX_TIMEOUT_S = 15
MAX_OUTPUT_BYTES = 100 * 1024
MAX_CODE_BYTES = 64 * 1024
MAX_STDIN_BYTES = 64 * 1024

RUNNERS: Dict[str, List[str]] = {
    "python": [sys.executable, "-I", "-u", "{file}"],
    "javascript": ["node", "{file}"],
}
EXTENSIONS = {"python": ".py", "javascript": ".mjs"}


class ExecuteRequest(BaseModel):
    code: str = Field(max_length=MAX_CODE_BYTES)
    language: str = "python"
    stdin: str = Field(default="", max_length=MAX_STDIN_BYTES)
    timeout: int = Field(default=5, ge=1, le=MAX_TIMEOUT_S)


app = FastAPI(title="PlacementPro compiler service")


def _authorized(authorization: Optional[str]) -> bool:
    key = os.getenv("COMPILER_KEY", "")
    if not key or not authorization or not authorization.startswith("Bearer "):
        return False
    token = authorization[len("Bearer "):]
    return hmac.compare_digest(
        hashlib.sha256(token.encode()).hexdigest(),
        hashlib.sha256(key.encode()).hexdigest(),
    )


def _sandbox_env() -> Dict[str, str]:
    """Child env: inherit the container, drop proxy signalling (defense in
    depth alongside no-egress at the platform layer), enforce interpreter
    safety flags. Full inherit (not a minimal allowlist) because runtimes
    need platform vars like SYSTEMROOT/TEMP to start at all."""
    env = {k: v for k, v in os.environ.items()
           if "proxy" not in k.lower()}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1",
                "NODE_NO_READLINE": "1"})
    return env


def _limit_resources() -> None:
    # Child-process only (preexec_fn): CPU seconds + address space caps.
    # Values are defense-in-depth behind the timeout + container limits.
    if _resource is None:
        return
    try:
        _resource.setrlimit(_resource.RLIMIT_CPU, (MAX_TIMEOUT_S + 2, MAX_TIMEOUT_S + 2))
        mem = 256 * 1024 * 1024
        _resource.setrlimit(_resource.RLIMIT_AS, (mem, mem))
        _resource.setrlimit(_resource.RLIMIT_FSIZE, (MAX_OUTPUT_BYTES, MAX_OUTPUT_BYTES))
        _resource.setrlimit(_resource.RLIMIT_NPROC, (16, 16))
    except Exception:
        pass


def _run_once(code: str, language: str, stdin: str, timeout: int) -> Dict[str, Any]:
    runner = RUNNERS[language]
    with tempfile.TemporaryDirectory(prefix="pp-run-") as tmp:
        path = os.path.join(tmp, "main" + EXTENSIONS[language])
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        cmd = [a.format(file=path) for a in runner]
        try:
            proc = subprocess.run(
                cmd, input=stdin.encode("utf-8", errors="replace"),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                timeout=timeout,
                preexec_fn=_limit_resources if os.name == "posix" else None,
                cwd=tmp, env=_sandbox_env(),
            )
        except subprocess.TimeoutExpired:
            return {"success": False, "stdout": "", "stderr": "",
                    "error": "Execution timed out", "exit_code": 124,
                    "execution_time": float(timeout), "source": "gcp_compiler"}
        stdout = proc.stdout[:MAX_OUTPUT_BYTES].decode("utf-8", errors="replace")
        stderr = proc.stderr[:MAX_OUTPUT_BYTES].decode("utf-8", errors="replace")
        if proc.returncode == 0:
            return {"success": True, "stdout": stdout, "stderr": stderr,
                    "error": None, "exit_code": 0,
                    "execution_time": 0.0, "source": "gcp_compiler"}
        err = (stderr.strip().splitlines() or ["Runtime error"])
        return {"success": False, "stdout": stdout, "stderr": stderr,
                "error": err[-1][:500], "exit_code": proc.returncode,
                "execution_time": 0.0, "source": "gcp_compiler"}


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok", "languages": ",".join(sorted(RUNNERS))}


@app.post("/execute")
async def execute(req: ExecuteRequest,
                  authorization: Optional[str] = Header(default=None)) -> Dict[str, Any]:
    if not _authorized(authorization):
        raise HTTPException(status_code=401, detail="Unauthorized")
    language = (req.language or "").lower()
    if language not in RUNNERS:
        raise HTTPException(status_code=400,
                            detail=f"Unsupported language '{req.language}'")
    return _run_once(req.code, language, req.stdin or "", req.timeout)
