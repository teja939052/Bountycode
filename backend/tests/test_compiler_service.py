"""Compiler service (own infra) + backend hop tests. No docker, no network.

Service runs in-process via TestClient; backend hop is asserted against
real behavior (unconfigured → {}, bad host → {}, no raise, no leak).
"""
import importlib.util
import os
import shutil

import pytest
from fastapi.testclient import TestClient

_SVC_PATH = os.path.join(os.path.dirname(__file__), "..", "compiler-service", "main.py")
_spec = importlib.util.spec_from_file_location("pp_compiler_service", _SVC_PATH)
svc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(svc)

KEY = "test-secret-key"
os.environ["COMPILER_KEY"] = KEY


def _client():
    return TestClient(svc.app)


def _auth():
    return {"Authorization": f"Bearer {KEY}"}


def test_health():
    r = _client().get("/health")
    assert r.status_code == 200
    assert "python" in r.json()["languages"]


def test_unauthorized():
    r = _client().post("/execute", json={"code": "print(1)", "language": "python"})
    assert r.status_code == 401
    r = _client().post("/execute", json={"code": "print(1)", "language": "python"},
                        headers={"Authorization": "Bearer wrong"})
    assert r.status_code == 401


def test_python_success():
    r = _client().post("/execute",
                        json={"code": "print(6 * 7)", "language": "python", "timeout": 5},
                        headers=_auth())
    assert r.status_code == 200
    body = r.json()
    assert body["success"] is True and body["stdout"].strip() == "42"
    assert body["source"] == "gcp_compiler"


def test_python_stdin_and_error_shape():
    r = _client().post("/execute",
                        json={"code": "import sys\nprint(sys.stdin.read().strip())",
                              "language": "python", "stdin": "hi", "timeout": 5},
                        headers=_auth())
    assert r.json()["stdout"].strip() == "hi"
    r = _client().post("/execute",
                        json={"code": "raise ValueError('boom')", "language": "python",
                              "timeout": 5},
                        headers=_auth())
    body = r.json()
    assert body["success"] is False
    assert "boom" in (body["error"] or "")
    assert set(body) >= {"success", "stdout", "stderr", "error", "exit_code",
                         "execution_time", "source"}


def test_timeout_and_caps():
    r = _client().post("/execute",
                        json={"code": "while True:\n    pass", "language": "python",
                              "timeout": 2},
                        headers=_auth())
    body = r.json()
    assert body["success"] is False and "timed out" in (body["error"] or "")
    r = _client().post("/execute",
                        json={"code": "print('x' * 200000)", "language": "python",
                              "timeout": 5},
                        headers=_auth())
    assert len(r.json()["stdout"].encode()) <= 100 * 1024
    r = _client().post("/execute",
                        json={"code": "print(1)", "language": "ruby", "timeout": 5},
                        headers=_auth())
    assert r.status_code == 400


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_javascript_success():
    r = _client().post("/execute",
                        json={"code": "console.log(6 * 7)", "language": "javascript",
                              "timeout": 5},
                        headers=_auth())
    assert r.status_code == 200
    assert r.json()["stdout"].strip() == "42"


def test_backend_hop_unconfigured_and_unreachable():
    import asyncio
    from app.config import get_settings
    from app.services.code_executor import CodeExecutionEngine

    settings = get_settings()
    saved = (settings.COMPILER_SERVICE_URL, settings.COMPILER_SERVICE_KEY)
    try:
        settings.COMPILER_SERVICE_URL = ""
        settings.COMPILER_SERVICE_KEY = ""
        engine = CodeExecutionEngine()
        assert asyncio.run(engine._try_gcp_compiler("python", "print(1)", "", 5)) == {}
        settings.COMPILER_SERVICE_URL = "http://127.0.0.1:9"
        settings.COMPILER_SERVICE_KEY = "x"
        assert asyncio.run(engine._try_gcp_compiler("python", "print(1)", "", 2)) == {}
        # Unsupported language never leaves the process.
        assert asyncio.run(engine._try_gcp_compiler("ruby", "puts 1", "", 2)) == {}
    finally:
        settings.COMPILER_SERVICE_URL, settings.COMPILER_SERVICE_KEY = saved
