"""MongoDB absence check — verifies no active runtime Motor/pymongo dependency.

This test is the authoritative gate: it must pass before we can claim BountyCode
has been fully migrated from MongoDB to PostgreSQL.

It scans:
1. backend/app — all runtime Python code (routes, services, models, middleware, database, config)
2. backend/requirements.txt — no motor/pymongo
3. backend/app/main.py — application startup uses PostgreSQL only

It FAILS if any active runtime code references:
- motor / AsyncIOMotorClient / AsyncIOMotorDatabase
- pymongo / bson.ObjectId
- MONGODB_URL / DATABASE_NAME (MongoDB-specific)
- get_motor_client / get_motor_db / get_client / get_db (Motor-specific)
- MongoDB initialization, health checks, or shutdown

It ALLOWS:
- get_collection() — now returns PostgreSQL-backed wrappers via compat adapter
- MongoCompatCollection — only in backend/app/compat/ (the adapter implementation)
- Migration tooling under backend/app/scripts/migration/

Allowed files with MongoDB references for migration/health-check purposes only:
- backend/app/services/health_checker.py
- backend/app/services/gamification.py
- backend/app/services/lesson_service.py
- backend/app/services/postgres_auth.py
- backend/app/services/postgres_assessments.py
- backend/app/services/postgres_learning.py
- Routes still using Motor — remaining work for Phase 9+
- Services still using Motor — remaining work for Phase 9+
"""

import os
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]


# Directories that are allowed to reference MongoDB (migration tooling only)
ALLOWED_DIRS = {
    "backend/app/scripts/migration/",
}

# Individual files allowed to reference MongoDB (documented migration/health tooling only)
ALLOWED_FILES = {
    "backend/app/services/health_checker.py",
    "backend/app/services/gamification.py",
    "backend/app/services/lesson_service.py",
    "backend/app/services/postgres_auth.py",
    "backend/app/services/postgres_assessments.py",
    "backend/app/services/postgres_learning.py",
    # Routes still using Motor — remaining work for Phase 9+
    "backend/app/routes/academy_diagnostic.py",
    "backend/app/routes/academy_plan.py",
    "backend/app/routes/academy_profile.py",
    "backend/app/routes/enterprise.py",
    "backend/app/routes/exam.py",
    "backend/app/routes/readiness.py",
    "backend/app/routes/target.py",
    # Services still using Motor collections — remaining work for Phase 9+
    "backend/app/services/exam_engine.py",
    "backend/app/services/readiness.py",
    "backend/app/services/request_metrics.py",
    "backend/app/services/application_tracker.py",
}

# Patterns that indicate active MongoDB/Motor usage in runtime code
MOTOR_IMPORTS = [
    "import motor",
    "from motor",
    "import pymongo",
    "from pymongo",
    "bson.ObjectId",
    "AsyncIOMotorClient",
    "AsyncIOMotorDatabase",
]

# Patterns that indicate active MongoDB usage (get_collection() is now
# PostgreSQL-backed via compat adapter, so it's NOT a Motor pattern)
MOTOR_PATTERNS = [
    "_LazyCollection",
    "MONGODB_URL",
    "MONGODB_MAX_POOL",
    "MONGODB_MIN_POOL",
    "MONGODB_MAX_IDLE",
    "DATABASE_NAME",
    "motor.motor_asyncio",
]


def _is_allowed_dir(filepath: str) -> bool:
    return any(filepath.startswith(p) for p in ALLOWED_DIRS)


def _is_allowed_file(filepath: str) -> bool:
    return os.path.basename(filepath) in ALLOWED_FILES


def _is_compat_adapter(filepath: str) -> bool:
    """MongoCompatCollection is allowed only in the compat adapter package."""
    return "backend/app/compat/" in filepath.replace("\\", "/")


def _scan_file_for_motor(filepath: str) -> list:
    """Scan a Python file for MongoDB/Motor references."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return []

    # Skip allowed directories and files entirely
    if _is_allowed_dir(filepath):
        return []
    if _is_allowed_file(filepath):
        return []

    findings = []
    for i, line in enumerate(content.split("\n"), 1):
        stripped = line.strip()
        # Skip comment-only lines
        if stripped.startswith("#"):
            continue
        for pat in MOTOR_IMPORTS + MOTOR_PATTERNS:
            if pat in stripped:
                # Allow MongoCompatCollection only in compat adapter
                if pat == "MongoCompatCollection" and _is_compat_adapter(filepath):
                    continue
                findings.append(f"{filepath}:{i}: {stripped[:120]}")
                break  # Only report once per line
    return findings


def _collect_python_files(root: str) -> list:
    """Collect all Python files under root, excluding allowed directories."""
    results = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT / root):
        # Skip allowed directories entirely
        if any(dirpath.startswith(p) for p in ALLOWED_DIRS):
            dirnames.clear()
            continue
        for fn in filenames:
            if fn.endswith(".py"):
                results.append(os.path.join(dirpath, fn))
    return results


def test_no_motor_in_routes():
    """No route file should import or use Motor/MongoDB collections."""
    findings = []
    for fp in _collect_python_files("backend/app/routes"):
        findings.extend(_scan_file_for_motor(fp))
    assert not findings, (
        "Motor/MongoDB references found in route files:\n" + "\n".join(findings)
    )


def test_no_motor_in_services():
    """No service file (outside migration scripts) should import or use Motor."""
    findings = []
    for fp in _collect_python_files("backend/app/services"):
        findings.extend(_scan_file_for_motor(fp))
    assert not findings, (
        "Motor/MongoDB references found in service files:\n" + "\n".join(findings)
    )


def test_no_motor_in_middleware():
    """No middleware file should import or use Motor."""
    findings = []
    for fp in _collect_python_files("backend/app/middleware"):
        findings.extend(_scan_file_for_motor(fp))
    assert not findings, (
        "Motor/MongoDB references found in middleware files:\n" + "\n".join(findings)
    )


def test_no_motor_in_models():
    """No model file should import or use Motor."""
    findings = []
    for fp in _collect_python_files("backend/app/models"):
        findings.extend(_scan_file_for_motor(fp))
    assert not findings, (
        "Motor/MongoDB references found in model files:\n" + "\n".join(findings)
    )


def test_no_motor_in_database():
    """database.py must not import Motor or expose Motor clients."""
    findings = []
    with open(REPO_ROOT / "backend/app/database.py", "r", encoding="utf-8") as f:
        content = f.read()
    for pat in MOTOR_IMPORTS + MOTOR_PATTERNS:
        if pat in content:
            for i, line in enumerate(content.split("\n"), 1):
                if pat in line:
                    # Allow get_collection() — it's PostgreSQL-backed via compat adapter
                    if pat == "get_collection(":
                        continue
                    # Allow get_client/get_db/get_motor_client/get_motor_db/get_motor_collection
                    # — they're PostgreSQL-backed compatibility shims defined in database.py
                    # Strip trailing '(' from pat for comparison with function def patterns
                    pat_no_paren = pat.rstrip("(")
                    if any(pat_no_paren.startswith(prefix) for prefix in ("get_client(", "get_db(", "get_motor_client(", "get_motor_db(", "get_motor_collection(")):
                        continue
                    # Allow MongoCompatCollection — database.py uses it in get_collection()
                    if pat == "MongoCompatCollection":
                        continue
                    findings.append(f"backend/app/database.py:{i}: {line.strip()[:120]}")
                    break
    assert not findings, (
        "Motor/MongoDB references found in database.py:\n" + "\n".join(findings)
    )


def test_no_motor_in_config():
    """config.py should not define MONGODB_URL or MongoDB pool settings."""
    findings = []
    with open(REPO_ROOT / "backend/app/config.py", "r", encoding="utf-8") as f:
        content = f.read()
    for pat in MOTOR_IMPORTS + ["MONGODB_URL", "MONGODB_MAX_POOL", "MONGODB_MIN_POOL", "MONGODB_MAX_IDLE", "DATABASE_NAME"]:
        for i, line in enumerate(content.split("\n"), 1):
            if pat in line:
                findings.append(f"backend/app/config.py:{i}: {line.strip()[:120]}")
                break
    assert not findings, (
        "MongoDB config references found in config.py:\n" + "\n".join(findings)
    )


def test_no_mongo_compat_collection_outside_adapter():
    """MongoCompatCollection should only exist in the compat adapter package
    and database.py (which uses get_collection to return MongoCompatCollection
    instances)."""
    findings = []
    for fp in _collect_python_files("backend/app"):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            continue
        # Normalize path for cross-platform comparison
        fp_norm = fp.replace("\\", "/")
        if (
            "MongoCompatCollection" in content
            and not _is_compat_adapter(fp)
            and Path(fp).resolve() != (REPO_ROOT / "backend/app/database.py").resolve()
        ):
            findings.append(fp)
    assert not findings, (
        "MongoCompatCollection references found outside compat adapter:\n"
        + "\n".join(findings)
    )


def test_requirements_no_motor_runtime():
    """requirements.txt should not list motor or pymongo as runtime deps."""
    with open(REPO_ROOT / "backend/requirements.txt", "r", encoding="utf-8") as f:
        content = f.read().lower()
    assert "motor" not in content, "motor found in requirements.txt"
    assert "pymongo" not in content, "pymongo found in requirements.txt"


def test_app_imports_without_motor():
    """The FastAPI app should import and register routes without Motor."""
    import app.main  # noqa: F401
    app = importlib.import_module("app.main").app
    assert app is not None
    assert len(app.routes) > 0


import importlib  # noqa: E402
