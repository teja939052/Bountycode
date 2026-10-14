"""Tests to verify untrusted student code is NOT executed in-process.

Phase 3 remediation: code_tracer.py and concept_engine.py previously used
exec() inside the FastAPI server process. These tests verify that execution
is now delegated to an isolated subprocess via local_sandbox.execute_local().
"""
from unittest.mock import patch, MagicMock
import sys

import pytest


def _import_tracer():
    from app.services import code_tracer
    return code_tracer


def _import_concept_engine():
    from app.services import concept_engine
    return concept_engine


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


class TestConceptEngineIsolation:
    """Verify concept_engine grading does NOT exec() student code in-process."""

    def test_grade_manipulate_frame_uses_subprocess(self):
        engine = _import_concept_engine()
        frame = MagicMock()
        frame.manipulate.target_variable = "score"

        fake_result = {
            "success": True,
            "stdout": '{"target": 10}\n',
            "stderr": "",
            "exit_code": 0,
        }
        with patch("app.services.concept_engine.execute_local_sync", return_value=fake_result) as mock_exec:
            correct, explanation = engine._grade_manipulate_frame(frame, "score = 10")

        mock_exec.assert_called_once()
        args, kwargs = mock_exec.call_args
        assert args[1] == "python"
        assert correct is True
        assert explanation == (frame.manipulate.hint or "Good.")

    def test_grade_manipulate_frame_handles_missing_variable(self):
        engine = _import_concept_engine()
        frame = MagicMock()
        frame.manipulate.target_variable = "missing"

        fake_result = {
            "success": True,
            "stdout": "hello\n",
            "stderr": "",
            "exit_code": 0,
        }
        with patch("app.services.concept_engine.execute_local_sync", return_value=fake_result):
            correct, explanation = engine._grade_manipulate_frame(frame, 'print("hello")')

        assert correct is False
        assert "not found" in explanation

    def test_grade_transfer_frame_uses_subprocess(self):
        engine = _import_concept_engine()
        frame = MagicMock()
        frame.transfer = MagicMock()

        fake_result = {
            "success": True,
            "stdout": "",
            "stderr": "",
            "exit_code": 0,
        }
        with patch("app.services.concept_engine.execute_local_sync", return_value=fake_result) as mock_exec:
            correct, explanation = engine._grade_transfer_frame(frame, "print('done')")

        mock_exec.assert_called_once()
        args, kwargs = mock_exec.call_args
        assert args[1] == "python"
        assert correct is True

    def test_grade_transfer_frame_handles_runtime_error(self):
        engine = _import_concept_engine()
        frame = MagicMock()
        frame.transfer = MagicMock()

        fake_result = {
            "success": False,
            "stdout": "",
            "stderr": "NameError: name 'x' is not defined",
            "exit_code": 1,
        }
        with patch("app.services.concept_engine.execute_local_sync", return_value=fake_result):
            correct, explanation = engine._grade_transfer_frame(frame, "print(x)")

        assert correct is False
        assert "NameError" in explanation


class TestNoInProcessExec:
    """Verify the actual modules do NOT contain dangerous in-process exec() calls."""

    def test_code_tracer_has_no_inprocess_exec_of_student_code(self):
        tracer = _import_tracer()
        source = open(tracer.__file__).read()
        assert "exec(compile(" not in source, "code_tracer.py still contains in-process exec()"

    def test_concept_engine_has_no_inprocess_exec_of_student_code(self):
        engine = _import_concept_engine()
        source = open(engine.__file__).read()
        assert "exec(code, ns)" not in source, "concept_engine.py still contains in-process exec(code, ns)"
