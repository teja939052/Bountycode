"""
Local sandboxed code execution fallback.

Purpose: when the public Piston API is rate-limited or unreachable, execute code in a
restricted subprocess on the local host (no network egress). This is the
self-hosted isolation layer analogous to Judge0/Microsandbox sandboxing, implemented
as a lightweight local runner with:

  - Hard timeout via subprocess `kill` after SANDBOX_TIMEOUT seconds (kills infinite loops).
  - Restricted Python builtins (no open, exec, __import__, eval of dangerous modules).
  - Per-run CPU/memory limits on POSIX via `resource` (RLIMIT_CPU/RLIMIT_AS).
  - Captured stdout/stderr/exit code — same schema shape as the Piston response.

Supported languages: python and javascript (node). Other languages fall back to Piston.

Security note: This is a UX-level safety net for the *fallback* path only. For
multi-tenant / untrusted workloads prefer true container isolation (opencode-sandbox,
Microsandbox, or a self-hosted Piston/Judge0 instance behind auth). See SANDBOX.md.
"""
from __future__ import annotations

import asyncio
import json
import os
import shutil
import sys
import tempfile
from typing import Dict, Any, List, Tuple
from app.config import get_settings

# Languages that have a safe local runner implementation.
LOCAL_LANGUAGES = {"python", "javascript"}


async def execute_local(code: str, language: str, stdin: str = "", timeout: int = 5) -> Dict[str, Any]:
    """Execute `code` in a restricted local subprocess. Returns a Piston-shaped result dict."""
    settings = get_settings()
    timeout = max(1, min(int(timeout or 5), settings.SANDBOX_TIMEOUT or 5))

    if language == "python":
        return await _exec_python(code, stdin, timeout)
    if language == "javascript":
        return await _exec_js(code, stdin, timeout)

    return {
        "success": False,
        "error": f"Local sandbox does not support '{language}'. Falling back to Piston.",
    }


def _resource_preset():
    """Best-effort POSIX resource limits; no-ops on Windows."""
    try:
        import resource

        # Max 30 seconds of CPU time, 256MB address space.
        resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
        mem = 256 * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (mem, mem))
    except Exception:
        return None


async def _exec_python(code: str, stdin: str, timeout: int) -> Dict[str, Any]:
    # Restricted builtins: strip file/exec/network-capable names.
    runner = (
        "import sys, io, contextlib\n"
        "safe_builtins = {\n"
        "  k: (__builtins__ if isinstance(__builtins__, dict) else __builtins__.__dict__)[k] for k in (\n"
        "    'abs','all','any','bin','bool','bytes','chr','dict','divmod',\n"
        "    'enumerate','filter','float','format','frozenset','hash','hex',\n"
        "    'int','len','list','map','max','min','oct','ord','pow','print',\n"
        "    'range','repr','reversed','round','set','slice','sorted','str',\n"
        "    'sum','tuple','type','zip','True','False','None','Exception',\n"
        "    'ValueError','TypeError','IndexError','KeyError','ZeroDivisionError',\n"
        "    'StopIteration','RuntimeError','ArithmeticError','NameError',\n"
        "    '__import__','input',\n"
        "  )\n"
        "}\n"
        "safe_builtins.pop('open', None)\n"
        "SAFE_MODULES = {'sys','math','collections','itertools','functools','re',\n"
        "               'json','bisect','heapq','random','string','statistics',\n"
        "               'typing','dataclasses','copy','decimal','fractions','queue',\n"
        "               'array','struct','calendar','datetime','time','operator','pprint'}\n"
        "def _safe_import(name, globals=None, locals=None, fromlist=(), level=0):\n"
        "    top = name.split('.')[0]\n"
        "    if top not in SAFE_MODULES:\n"
        "        raise ImportError('module ' + name + ' is blocked by sandbox')\n"
        "    return __orig_import__(name, globals, locals, fromlist, level)\n"
        "__orig_import__ = safe_builtins['__import__']\n"
        "safe_builtins['__import__'] = _safe_import\n"
        "import json\n"
        "sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')\n"
        "sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')\n"
        "sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')\n"
        "code = " + repr(code) + "\n"
        "exec_globals = {'__name__':'__main__','__builtins__':safe_builtins}\n"
        "try:\n"
        "    exec(compile(code, '<sandbox>', 'exec'), exec_globals)\n"
        "except SystemExit as e:\n"
        "    sys.exit(e.code if isinstance(e.code, int) else 1)\n"
    )

    try:
        kwargs = {
            "stdin": asyncio.subprocess.PIPE,
            "stdout": asyncio.subprocess.PIPE,
            "stderr": asyncio.subprocess.PIPE,
            "env": {"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"},
        }
        if os.name != "nt":
            kwargs["preexec_fn"] = _resource_preset
        proc = await asyncio.create_subprocess_exec(
            sys.executable, "-c", runner, **kwargs
        )
    except FileNotFoundError:
        return {"success": False, "error": "python interpreter not available for local sandbox"}
    except Exception as e:
        return {"success": False, "error": f"Local sandbox unavailable: {e}"}

    try:
        stdout_b, stderr_b = await asyncio.wait_for(proc.communicate(stdin.encode()), timeout=timeout)
    except asyncio.TimeoutError:
        proc.kill()
        await proc.wait()
        return {
            "success": False,
            "error": "Execution timed out (possible infinite loop)",
            "hint": "Check for infinite loops or very long-running operations",
        }

    stdout = stdout_b.decode("utf-8", errors="replace")
    stderr = stderr_b.decode("utf-8", errors="replace")
    exit_code = await proc.wait()

    success = exit_code == 0
    return {
        "success": success,
        "exit_code": exit_code,
        "stdout": stdout.strip(),
        "stderr": stderr.strip(),
        "compile_error": None,
        "language": "python",
        "execution_time": 0,
        "memory_usage": 0,
        "source": "local_sandbox",
    }


# ── Batched oracle execution ────────────────────────────────────────────────
# Runs user submission ONCE against ALL test cases inside a single sandboxed
# process (stdin swapped per case, stdout captured per case). This is the
# zero-cost judging path: no Piston API call, regardless of test-case count.
#
# Function-call mode: when FUNCTION_NAME is set and the submission defines
# that function, each case's stdin is parsed as a Python-literal argument
# tuple ("[2,7], 9" → args) and the function's return value is serialized
# canonically (str bare, containers as compact JSON). This matches the
# platform-wide question format where starter code defines a named function.

_BATCH_RUNNER = (
    "import ast, contextlib, io, json, sys\n"
    "_USER_CODE = @@CODE@@\n"
    "_CASES = json.loads(@@CASES@@)\n"
    "_FUNC_NAME = @@FUNC@@\n"
    "def _canon(v):\n"
    "    if isinstance(v, str):\n"
    "        return v\n"
    "    if isinstance(v, bool):\n"
    "        return str(v)\n"
    "    if isinstance(v, (list, tuple)):\n"
    "        return json.dumps([_canon(x) for x in v], separators=(',', ':'))\n"
    "    if v is None:\n"
    "        return 'None'\n"
    "    return str(v)\n"
    "_OUT = []\n"
    "_NS = {'__name__': '__main__'}\n"
    "try:\n"
    "    exec(compile(_USER_CODE, '<submission>', 'exec'), _NS)\n"
    "except BaseException as _e:\n"
    "    sys.stdout.write('<<ORACLE_COMPILE>>' + ('%s: %s' % (type(_e).__name__, _e)))\n"
    "    sys.exit(0)\n"
    "_FN = _NS.get(_FUNC_NAME) if _FUNC_NAME else None\n"
    "for _raw in _CASES:\n"
    "    try:\n"
    "        if _FN is not None:\n"
    "            _args = ast.literal_eval('(' + _raw + ')') if _raw.strip() else ()\n"
    "            if not isinstance(_args, tuple):\n"
    "                _args = (_args,)\n"
    "            _OUT.append([True, _canon(_FN(*_args))])\n"
    "        else:\n"
    "            _so = io.StringIO()\n"
    "            _old_in = sys.stdin\n"
    "            try:\n"
    "                sys.stdin = io.StringIO(_raw)\n"
    "                _g = dict(_NS)\n"
    "                with contextlib.redirect_stdout(_so):\n"
    "                    exec(compile(_USER_CODE, '<submission>', 'exec'), _g)\n"
    "                _OUT.append([True, _so.getvalue()])\n"
    "            finally:\n"
    "                sys.stdin = _old_in\n"
    "    except BaseException as _e:\n"
    "        _OUT.append([False, '%s: %s' % (type(_e).__name__, _e)])\n"
    "sys.stdout.write('<<ORACLE>>' + json.dumps(_OUT))\n"
)


async def execute_local_python_batch(
    code: str,
    stdins: List[str],
    timeout: int = 10,
    function_name: str = "",
) -> Dict[str, Any]:
    """Execute `code` once against every case in `stdins` inside one sandboxed
    subprocess. Returns {"success": True, "results": [[ok, output], ...],
    "compile_error": str|None} or {"success": False, "error": str}."""
    settings = get_settings()
    timeout = max(1, min(int(timeout or 10), settings.SANDBOX_TIMEOUT or 10))

    runner = (
        _BATCH_RUNNER
        .replace("@@CODE@@", repr(code))
        .replace("@@CASES@@", repr(json.dumps(stdins)))
        .replace("@@FUNC@@", repr(function_name or ""))
    )

    try:
        kwargs = {
            "stdin": asyncio.subprocess.PIPE,
            "stdout": asyncio.subprocess.PIPE,
            "stderr": asyncio.subprocess.PIPE,
            "env": {"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"},
        }
        if os.name != "nt":
            kwargs["preexec_fn"] = _resource_preset
        proc = await asyncio.create_subprocess_exec(
            sys.executable, "-c", runner, **kwargs
        )
    except Exception as e:
        return {"success": False, "error": f"Local batch runner unavailable: {e}"}

    try:
        stdout_b, stderr_b = await asyncio.wait_for(
            proc.communicate(b""), timeout=timeout
        )
    except asyncio.TimeoutError:
        proc.kill()
        await proc.wait()
        return {
            "success": False,
            "error": "Execution timed out (possible infinite loop)",
        }

    stdout = stdout_b.decode("utf-8", errors="replace")

    compile_marker = "<<ORACLE_COMPILE>>"
    if compile_marker in stdout:
        return {
            "success": True,
            "results": [],
            "compile_error": stdout.split(compile_marker, 1)[1][:500],
        }

    marker = stdout.find("<<ORACLE>>")
    if marker == -1:
        return {
            "success": False,
            "error": stderr.strip()[:500] or "Batch runner produced no results",
        }
    try:
        results = json.loads(stdout[marker + len("<<ORACLE>>"):])
    except ValueError:
        return {"success": False, "error": "Failed to parse batch oracle output"}

    return {"success": True, "results": results, "compile_error": None}


async def _exec_js(code: str, stdin: str, timeout: int) -> Dict[str, Any]:
    node = shutil.which("node")
    if not node:
        return {"success": False, "error": "node interpreter not available for local sandbox"}

    try:
        proc = await asyncio.create_subprocess_exec(
            node, "--input-type=module", "--no-warnings",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={"NODE_NO_WARNINGS": "1"},
        )
    except Exception as e:
        return {"success": False, "error": f"Local sandbox unavailable: {e}"}

    try:
        stdout_b, stderr_b = await asyncio.wait_for(proc.communicate(code.encode()), timeout=timeout)
    except asyncio.TimeoutError:
        proc.kill()
        await proc.wait()
        return {"success": False, "error": "Execution timed out", "source": "local_sandbox"}

    stdout = stdout_b.decode("utf-8", errors="replace")
    stderr = stderr_b.decode("utf-8", errors="replace")
    exit_code = await proc.wait()

    return {
        "success": exit_code == 0,
        "exit_code": exit_code,
        "stdout": stdout.strip(),
        "stderr": stderr.strip(),
        "compile_error": None,
        "language": "javascript",
        "execution_time": 0,
        "memory_usage": 0,
        "source": "local_sandbox",
    }
