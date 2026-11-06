"""Compiler child-process environment and deployment fail-closed tests."""
import asyncio
import importlib.util
from pathlib import Path

import pytest
from fastapi import HTTPException


MODULE_PATH = Path(__file__).resolve().parents[1] / "compiler-service" / "main.py"
SPEC = importlib.util.spec_from_file_location("bountycode_compiler_service", MODULE_PATH)
assert SPEC and SPEC.loader
compiler_service = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(compiler_service)


def test_child_environment_does_not_inherit_service_credentials(monkeypatch):
    monkeypatch.setenv("PATH", "/usr/bin")
    monkeypatch.setenv("HOME", "/home/runner")
    monkeypatch.setenv("COMPILER_KEY", "super-secret")
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", "/tmp/cloud-creds.json")
    monkeypatch.setenv("INTERNAL_API_TOKEN", "another-secret")
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy.invalid")

    child_env = compiler_service._sandbox_env()

    assert child_env["PATH"] == "/usr/bin"
    assert child_env["HOME"] == "/home/runner"
    assert "COMPILER_KEY" not in child_env
    assert "GOOGLE_APPLICATION_CREDENTIALS" not in child_env
    assert "INTERNAL_API_TOKEN" not in child_env
    assert "HTTPS_PROXY" not in child_env
    assert child_env["PYTHONNOUSERSITE"] == "1"


def test_compiler_service_fails_closed_without_network_isolation(monkeypatch):
    monkeypatch.setenv("COMPILER_NETWORK_ISOLATION_CONFIRMED", "false")
    monkeypatch.setattr(compiler_service, "_authorized", lambda _authorization: True)

    async def call():
        return await compiler_service.execute(
            compiler_service.ExecuteRequest(code="print('hello')", language="python"),
            authorization="Bearer test",
        )

    with pytest.raises(HTTPException) as exc:
        asyncio.run(call())
    assert exc.value.status_code == 503
