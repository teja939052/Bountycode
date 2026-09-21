"""Free remote code-execution fallbacks (Judge0 + Wandbox + Glot.io).

These are invoked only after the primary Piston API fails, and only when
USE_REMOTE_FALLBACKS=true. All are free JSON APIs with per-IP or key-based
rate limits — best-effort providers, NOT a hard security boundary. Each
provider returns a Piston-shaped dict so the rest of the pipeline stays
agnostic; provider-level failures return None so the chain can move to the
next hop.

Chain in code_executor: Piston -> Judge0 -> Wandbox -> Glot.io -> local
sandbox. Judge0 covers all 12 compiler languages; Wandbox/Glot.io cover
python + javascript only.
"""
import asyncio
import re

import httpx

from app.config import get_settings
from app.services.request_metrics import metrics as request_metrics

REMOTE_FALLBACK_LANGUAGES = {"python", "javascript"}

WANDBOX_LIST_URL = "https://wandbox.org/api/list.json"
WANDBOX_COMPILE_URL = "https://wandbox.org/api/compile.json"
GLOT_RUN_URL = "https://glot.io/api/run/{lang}/latest"

# Fallback compiler names if the Wandbox list can't be fetched. Only used as a
# last resort — the live list is resolved and cached on first use.
WANDBOX_DEFAULT_COMPILERS = {
    "python": "python-3.12.1",
    "javascript": "nodejs-20.17.0",
}

# Language slugs per provider
GLOT_LANGUAGE = {"python": "python", "javascript": "javascript"}

# Judge0 language IDs (api.judge0.com / self-host CE share these IDs).
JUDGE0_LANGUAGE_IDS = {
    "python": 71, "javascript": 63, "typescript": 74, "java": 62,
    "c++": 54, "cpp": 54, "c": 50, "go": 60, "rust": 73,
    "ruby": 72, "php": 68, "swift": 83, "kotlin": 78,
}

# Judge0 status IDs that mean "ran fine" (3) vs user-code errors (4-12).
# Anything else (13+ / null) is provider-side trouble -> next hop.
JUDGE0_OK_STATUS = 3
JUDGE0_USER_ERROR_STATUS = {4, 5, 6, 7, 8, 9, 10, 11, 12}

_wandbox_compilers = None
_wandbox_compiler_lock = None


def _version_key(name: str):
    """Turn a trailing version like '3.12.1' into a sortable tuple."""
    m = re.search(r"(\d+)(?:\.(\d+))?(?:\.(\d+))?", name)
    if not m:
        return (0, 0, 0)
    return (int(m.group(1) or 0), int(m.group(2) or 0), int(m.group(3) or 0))


def _pick_compiler(compilers, prefixes):
    """Pick the newest compiler whose name starts with one of the prefixes."""
    candidates = [
        c["name"]
        for c in (compilers or [])
        if isinstance(c, dict) and any(c.get("name", "").startswith(p) for p in prefixes)
    ]
    if not candidates:
        return None
    return max(candidates, key=_version_key)


async def _resolve_wandbox_compiler(client, language: str) -> str:
    """Resolve the best Wandbox compiler name for a language (cached)."""
    global _wandbox_compilers, _wandbox_compiler_lock
    if _wandbox_compiler_lock is None:
        _wandbox_compiler_lock = asyncio.Lock()

    async with _wandbox_compiler_lock:
        if _wandbox_compilers is None:
            try:
                resp = await client.get(WANDBOX_LIST_URL)
                _wandbox_compilers = resp.json() if resp.status_code == 200 else []
            except Exception:
                _wandbox_compilers = []

    prefixes = {
        "python": ("python-", "cpython-"),
        "javascript": ("nodejs-", "javascript-node-", "node-"),
    }.get(language, (f"{language}-",))

    return _pick_compiler(_wandbox_compilers, prefixes) or WANDBOX_DEFAULT_COMPILERS.get(language)


async def wandbox_execute(code: str, language: str, stdin: str = "", timeout: int = 5):
    """Run code on Wandbox. Returns a Piston-shaped dict or None."""
    if language not in REMOTE_FALLBACK_LANGUAGES:
        return None

    request_timeout = min(max(int(timeout or 5) + 3, 8), 15)
    try:
        async with httpx.AsyncClient(timeout=request_timeout) as client:
            compiler = await _resolve_wandbox_compiler(client, language)
            payload = {
                "compiler": compiler,
                "code": code,
                "stdin": stdin or "",
                "time": min(max(int(timeout or 5), 1), 5),
            }
            resp = await client.post(WANDBOX_COMPILE_URL, json=payload)
            if resp.status_code != 200:
                await request_metrics.record("compiler", "failure", error=f"Wandbox HTTP {resp.status_code}")
                return None

            data = resp.json()
    except Exception:
        await request_metrics.record("compiler", "failure", error="Wandbox error")
        return None

    # Provider-level failure (unknown compiler / API message) has no 'status'.
    if "status" not in data or isinstance(data.get("program"), dict):
        await request_metrics.record("compiler", "failure", error=f"Wandbox bad response: {str(data)[:120]}")
        return None

    status_raw = data.get("status", "0")
    try:
        exit_code = int(status_raw)
    except (TypeError, ValueError):
        exit_code = 0 if str(status_raw) in ("", "0") else 1

    stderr = data.get("stderr", "") or ""
    messages = data.get("messages") or []
    if messages:
        stderr = (stderr + "\n" + "\n".join(str(m) for m in messages)).strip()

    # Provider-side infra failures (sandbox couldn't even start) — not the user's
    # code. Return None so the caller moves to the next fallback hop.
    if exit_code in (126, 127) or "OCI runtime error" in stderr or "crun" in stderr:
        await request_metrics.record("compiler", "failure", error=f"Wandbox infra error (exit {exit_code})")
        return None

    success = exit_code == 0 and not stderr.strip()
    return {
        "success": success,
        "exit_code": exit_code,
        "stdout": (data.get("program", "") or "").strip(),
        "stderr": stderr.strip(),
        "compile_error": None,
        "language": language,
        "execution_time": 0,
        "memory_usage": 0,
        "source": "wandbox",
    }


async def glot_execute(code: str, language: str, stdin: str = "", timeout: int = 5):
    """Run code on Glot.io. Returns a Piston-shaped dict or None."""
    lang = GLOT_LANGUAGE.get(language)
    if not lang:
        return None

    request_timeout = min(max(int(timeout or 5) + 3, 8), 15)
    settings = get_settings()
    headers = {"Content-Type": "application/json"}
    if settings.GLOT_API_TOKEN:
        headers["Authorization"] = f"Token {settings.GLOT_API_TOKEN}"

    filename = "main.py" if lang == "python" else "main.js"
    payload = {
        "files": [{"name": filename, "content": code}],
        "stdin": stdin or "",
    }

    try:
        async with httpx.AsyncClient(timeout=request_timeout) as client:
            resp = await client.post(
                GLOT_RUN_URL.format(lang=lang),
                json=payload,
                headers=headers,
            )
            if resp.status_code != 200:
                await request_metrics.record("compiler", "failure", error=f"Glot HTTP {resp.status_code}")
                return None
            data = resp.json()
    except Exception:
        await request_metrics.record("compiler", "failure", error="Glot error")
        return None

    stdout = data.get("stdout", "") or ""
    stderr = data.get("stderr", "") or ""

    # Provider-level failure (bad token/language) has an 'error' and no output.
    if data.get("error") and not stdout and not stderr:
        await request_metrics.record("compiler", "failure", error=f"Glot error: {str(data.get('error'))[:120]}")
        return None

    exit_code = 0 if not stderr.strip() else 1
    return {
        "success": exit_code == 0,
        "exit_code": exit_code,
        "stdout": stdout.strip(),
        "stderr": stderr.strip(),
        "compile_error": None,
        "language": language,
        "execution_time": 0,
        "memory_usage": 0,
        "source": "glot_io",
    }


async def judge0_execute(code: str, language: str, stdin: str = "", timeout: int = 5):
    """Run code on Judge0 (RapidAPI-hosted with key, or self-host CE without).

    Configured via JUDGE0_URL (+ optional JUDGE0_KEY). Uses wait=true so the
    submission result returns synchronously. Returns a Piston-shaped dict or
    None. Disabled when JUDGE0_URL is empty.
    """
    settings = get_settings()
    base = (settings.JUDGE0_URL or "").rstrip("/")
    lang_id = JUDGE0_LANGUAGE_IDS.get((language or "").lower())
    if not base or not lang_id:
        return None

    headers = {"Content-Type": "application/json"}
    if settings.JUDGE0_KEY:
        # RapidAPI hosting authenticates via key headers.
        headers["X-RapidAPI-Key"] = settings.JUDGE0_KEY
        headers["X-RapidAPI-Host"] = base.split("://", 1)[-1].split("/", 1)[0]

    payload = {
        "source_code": code,
        "language_id": lang_id,
        "stdin": stdin or "",
        "cpu_time_limit": min(max(int(timeout or 5), 1), 15),
    }
    request_timeout = min(max(int(getattr(settings, "JUDGE0_TIMEOUT", 15)), 5), 30)
    try:
        async with httpx.AsyncClient(timeout=request_timeout) as client:
            resp = await client.post(
                f"{base}/submissions?base64_encoded=false&wait=true",
                json=payload,
                headers=headers,
            )
            if resp.status_code in (401, 403):
                await request_metrics.record("compiler", "failure", error="Judge0 auth rejected")
                return None
            if resp.status_code == 429:
                await request_metrics.record("compiler", "failure", error="Judge0 rate limited")
                return None
            if resp.status_code != 201 and resp.status_code != 200:
                await request_metrics.record("compiler", "failure", error=f"Judge0 HTTP {resp.status_code}")
                return None
            data = resp.json()
    except Exception:
        await request_metrics.record("compiler", "failure", error="Judge0 error")
        return None

    status = data.get("status") or {}
    try:
        status_id = int(status.get("id", 0))
    except (TypeError, ValueError):
        status_id = 0
    # Provider-side trouble (queue crush, box error): let the chain continue.
    if status_id not in JUDGE0_OK_STATUS and status_id not in JUDGE0_USER_ERROR_STATUS:
        await request_metrics.record("compiler", "failure", error=f"Judge0 status {status_id}")
        return None

    stdout = (data.get("stdout") or "").strip()
    stderr = ((data.get("stderr") or "") + "\n" + (data.get("compile_output") or "")).strip()
    exit_code = 0 if status_id == JUDGE0_OK_STATUS and not stderr else 1
    try:
        exec_ms = float(data.get("time") or 0) * 1000
    except (TypeError, ValueError):
        exec_ms = 0
    return {
        "success": status_id == JUDGE0_OK_STATUS,
        "exit_code": exit_code,
        "stdout": stdout,
        "stderr": stderr,
        "compile_error": None,
        "language": language,
        "execution_time": exec_ms,
        "memory_usage": data.get("memory") or 0,
        "source": "judge0",
    }


async def execute_remote_fallback(language: str, code: str, stdin: str = "", timeout: int = 5) -> dict:
    """Try Judge0, then Wandbox and Glot.io in parallel; first valid wins.

    Returns {} when no provider produced an answer, so the caller can
    continue down the chain (local sandbox). Judge0 runs first because it
    covers all 12 compiler languages; Wandbox/Glot.io cover python +
    javascript only.
    """
    if not get_settings().USE_REMOTE_FALLBACKS:
        return {}
    lang = (language or "").lower()

    if lang in JUDGE0_LANGUAGE_IDS:
        judge0 = await judge0_execute(code, lang, stdin, timeout)
        if isinstance(judge0, dict) and judge0.get("source"):
            return judge0

    if lang not in REMOTE_FALLBACK_LANGUAGES:
        return {}

    results = await asyncio.gather(
        wandbox_execute(code, lang, stdin, timeout),
        glot_execute(code, lang, stdin, timeout),
        return_exceptions=True,
    )
    for result in results:
        if isinstance(result, dict) and result.get("source"):
            return result
    return {}
