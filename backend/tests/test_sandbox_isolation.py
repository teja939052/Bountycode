"""Tests to verify untrusted student code is NOT executed in-process.

code_tracer.py previously used exec() inside the FastAPI server process.
These tests verify that execution is now delegated to an isolated
subprocess via local_sandbox.execute_local().
"""
from unittest.mock import patch, MagicMock
import sys

import pytest


def _import_tracer():
    from app.services import code_tracer
    return code_tracer


class TestCodeTracerIsolation:
    """Verify execute_with_trace does NOT exec() student code in-process."""

    def test_execute_with_trace_uses_subprocess_not_inprocess_exec(self):
        tracer = _import_tracer()

        fake_result = {
            "success": True,
            "stdout": '{"__trace__": [{"step": 0, "line": 1, "vars": {}}]}\n',
            "stderr": "",
            "exit_code": 0,
        }
        with patch("app.services.code_tracer.execute_local_sync", return_value=fake_result) as mock_exec:
            result = tracer.execute_with_trace("x = 1\nprint(x)", stdin="", timeout=5)

        mock_exec.assert_called_once()
        args, kwargs = mock_exec.call_args
        assert args[1] == "python"
        assert isinstance(args[0], str)
        assert "import json" in args[0]
        assert "print(json.dumps({'__trace__': __trace__}))" in args[0]
        assert result["steps"] == [{"step": 0, "line": 1, "vars": {}}]

    def test_execute_with_trace_handles_subprocess_failure(self):
        tracer = _import_tracer()

        with patch("app.services.code_tracer.execute_local_sync", return_value={"success": False, "error": "timeout"}) as mock_exec:
            result = tracer.execute_with_trace("while True: pass", stdin="", timeout=2)

        mock_exec.assert_called_once()
        assert result["error"] == "timeout"
        assert result["steps"] == []

    def test_instrument_python_code_adds_trace_marker(self):
        tracer = _import_tracer()
        instrumented = tracer.instrument_python_code("x = 1")
        assert "import json" in instrumented
        assert "print(json.dumps({'__trace__': __trace__}))" in instrumented


class TestNoInProcessExec:
    """Verify the actual modules do NOT contain dangerous in-process exec() calls."""

    def test_code_tracer_has_no_inprocess_exec_of_student_code(self):
        tracer = _import_tracer()
        source = open(tracer.__file__).read()
        assert "exec(compile(" not in source, "code_tracer.py still contains in-process exec()"
