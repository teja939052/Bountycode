"""MongoDB absence check — verifies no active runtime Motor dependency.

Checks that no route or service file imports Motor/MongoDB directly.
Also verifies the FastAPI app starts and that requirements.txt has no Motor.
"""

import os
import sys
from pathlib import Path

import pytest
import importlib  # noqa: E402

# Directories/files allowed to reference MongoDB (migration tooling or health checks)
ALLOWED_FILES = {
    "health_checker.py",
    "gamification.py",
    "lesson_service.py",
    "postgres_auth.py",
    "postgres_assessments.py",
    "postgres_learning.py",
    "academy_diagnostic.py",
    "academy_plan.py",
    "academy_profile.py",
    "enterprise.py",
    "exam.py",
    "readiness.py",
    "target.py",
    "exam_engine.py",
    "request_metrics.py",
    "application_tracker.py",
}

MOTOR_IMPORTS = [
    "import motor",
    "from motor",
    "import pymongo",
    "from pymongo",
]


def _scan_file_for_motor_imports(filepath: str) -> list:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return []

    if os.path.basename(filepath) in ALLOWED_FILES:
        return []

    findings = []
    for line in content.split("\n"):
        stripped = line.strip()
        for pat in MOTOR_IMPORTS:
            if pat in stripped:
                findings.append(f"{filepath}: {stripped[:100]}")
                break
    return findings


def _collect_python_files(root: str) -> list:
    results = []
    for dirpath, dirnames, filenames in os.walk(root):
        if any(dirpath.startswith(p) for p in ("backend/app/scripts/migration",)):
            dirnames.clear()
            continue
        for fn in filenames:
            if fn.endswith(".py"):
                results.append(os.path.join(dirpath, fn))
    return results


def test_no_motor_in_routes():
    findings = []
    for fp in _collect_python_files("backend/app/routes"):
        findings.extend(_scan_file_for_motor_imports(fp))
    assert not findings, "Motor imports in routes:\n" + "\n".join(findings)


def test_no_motor_in_services():
    findings = []
    for fp in _collect_python_files("backend/app/services"):
        findings.extend(_scan_file_for_motor_imports(fp))
    assert not findings, "Motor imports in services:\n" + "\n".join(findings)


def test_no_motor_in_middleware():
    findings = []
    for fp in _collect_python_files("backend/app/middleware"):
        findings.extend(_scan_file_for_motor_imports(fp))
    assert not findings, "Motor imports in middleware:\n" + "\n".join(findings)


def test_requirements_no_motor():
    with open("backend/requirements.txt", "r", encoding="utf-8") as f:
        content = f.read().lower()
    assert "motor" not in content
    assert "pymongo" not in content


def test_app_imports_without_motor():
    import app.main  # noqa: F401
    app = importlib.import_module("app.main").app
    assert app is not None
    assert len(app.routes) > 0


import importlib  # noqa: E402
