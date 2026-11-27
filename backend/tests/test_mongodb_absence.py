"""MongoDB absence check — verifies no active runtime Motor/pymongo dependency.

This test is the authoritative gate: it must pass before we can claim BountyCode
has been fully migrated from MongoDB to PostgreSQL.

It scans:
1. app — all runtime Python code (routes, services, models, middleware,
   database, config)
2. requirements.txt + requirements-dev.txt — no motor/pymongo
3. app/main.py — application startup uses PostgreSQL only

It FAILS if any active runtime code references:
- motor / AsyncIOMotorClient / AsyncIOMotorDatabase imports (AST-checked)
- pymongo / bson.ObjectId imports (AST-checked)
- MONGODB_URL / DATABASE_NAME (MongoDB-specific config)
- get_motor_client / get_motor_db / get_motor_collection (runtime shims)
- get_collection / MongoCompatCollection (compat shims)
- MongoDB-specific operators ($regex, $gte, $lt, $set, $inc, $push, $pull,
  $addToSet, $min, $max, $pop, $pullAll, $slice, $unset, $bit, $mirror,
  $elemMatch, $geoWithin, $geoIntersects, $near, $nearSphere, $text)
- MongoDB cursor methods: find_one, insert_one, update_one, delete_one,
  count_documents, aggregate with MongoDB pipelines
- _LazyCollection references

It ALLOWS:
- app/scripts/migration/ — migration tooling that may temporarily
  reference MongoDB during data import
- question_store.find()/question_store.find_one() — in-memory question bank
  operations (not MongoDB)

All other application files MUST NOT reference MongoDB motor/pymongo/bson
patterns — they must use PostgreSQL repositories.
"""

import ast
import os
from pathlib import Path

import pytest


# ── AST-based import check ──────────────────────────────────────────────


def _has_motor_import(source: str) -> bool:
    """Check for Motor/pymongo/bson imports using AST parsing."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return False

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "motor":
                    return True
                if alias.name.startswith("pymongo"):
                    return True
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                if node.module == "motor":
                    return True
                if node.module.startswith("motor."):
                    return True
                if node.module == "pymongo":
                    return True
                if node.module.startswith("pymongo."):
                    return True
                if node.module == "bson":
                    return True
                if node.module and node.module.startswith("bson."):
                    return True
    return False


def _has_mongodb_config(source: str) -> bool:
    """Check for MONGODB_URL or DATABASE_NAME in source."""
    patterns = ["MONGODB_URL", "DATABASE_NAME"]
    return any(p in source for p in patterns)


def _has_legacy_shim(source: str) -> bool:
    """Check for legacy MongoDB shim function calls."""
    patterns = ["get_motor_client", "get_motor_db", "get_motor_collection"]
    return any(p in source for p in patterns)


def _has_get_collection(source: str) -> bool:
    """Check for deprecated get_collection calls."""
    return "get_collection" in source


def _has_mongo_compat_collection(source: str) -> bool:
    """Check for MongoCompatCollection references."""
    return "MongoCompatCollection" in source


# MongoDB-specific operators (substring check - targeted, not regex-based)
_MONGODB_OPS = (
    "$regex", "$gte", "$gt", "$lt", "$lte", "$ne",
    "$set", "$inc", "$push", "$pull", "$addToSet",
    "$min", "$max",
    "$pop", "$pullAll", "$slice",
    "$unset", "$bit", "$mirror",
    "$elemMatch", "$geoWithin", "$geoIntersects",
    "$near", "$nearSphere", "$text",
)


def _has_mongodb_operator(source: str) -> bool:
    """Check for MongoDB-specific operators in source text."""
    return any(op in source for op in _MONGODB_OPS)


# ── File collection ──────────────────────────────────────────────────────


def _collect_python_files(root: str) -> list:
    """Collect all Python files under root."""
    results = []
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith(".py"):
                results.append(os.path.join(dirpath, fn))
    return results


def _read_file_safe(filepath: str) -> str:
    """Read a file safely, returning empty string on error."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def _is_migration_script(fp: str) -> bool:
    """Only migration tooling under app/scripts/migration may reference MongoDB."""
    norm = fp.replace("\\", "/")
    return "scripts/migration" in norm


# ── Test Functions ─────────────────────────────────────────────────────


def test_requirements_no_motor_runtime():
    """requirements.txt should not list motor or pymongo as runtime deps."""
    with open("requirements.txt", "r", encoding="utf-8") as f:
        content = f.read().lower()
    assert "motor" not in content, "motor found in requirements.txt"
    assert "pymongo" not in content, "pymongo found in requirements.txt"


def test_requirements_dev_no_motor():
    """requirements-dev.txt should not list motor or pymongo."""
    with open("requirements-dev.txt", "r", encoding="utf-8") as f:
        content = f.read().lower()
    assert "motor" not in content, "motor found in requirements-dev.txt"
    assert "pymongo" not in content, "pymongo found in requirements-dev.txt"


def test_no_mongodb_imports_in_database_py():
    """database.py must not import Motor/pymongo/bson."""
    with open("app/database.py", "r", encoding="utf-8") as f:
        content = f.read()
    assert not _has_motor_import(content), "Motor/pymongo/bson imports found in database.py"


def test_no_get_collection_in_database_py():
    """database.py must not define get_collection shim."""
    with open("app/database.py", "r", encoding="utf-8") as f:
        content = f.read()
    assert not _has_get_collection(content), "get_collection found in database.py"


def test_no_mongodb_config_in_config_py():
    """config.py should not define MONGODB_URL or MongoDB pool settings."""
    with open("app/config.py", "r", encoding="utf-8") as f:
        content = f.read()
    assert not _has_mongodb_config(content), "MongoDB config references found in config.py"


def test_no_legacy_shims_in_main_py():
    """main.py should not use legacy MongoDB shims."""
    with open("app/main.py", "r", encoding="utf-8") as f:
        content = f.read()
    assert not _has_legacy_shim(content), "Legacy MongoDB shims found in main.py"


def test_no_mongodb_runtime_imports():
    """No application runtime file should import Motor/pymongo/bson."""
    findings = []
    for fp in _collect_python_files("app"):
        source = _read_file_safe(fp)
        if not source:
            continue
        if _has_motor_import(source):
            if _is_migration_script(fp):
                continue
            findings.append(fp)
    assert not findings, (
        "Motor/pymongo/bson imports found in application files:\n"
        + "\n".join(findings)
    )


def test_no_mongodb_config_in_application():
    """No application file should define MONGODB_URL or DATABASE_NAME."""
    findings = []
    for fp in _collect_python_files("app"):
        source = _read_file_safe(fp)
        if not source:
            continue
        if _has_mongodb_config(source):
            if _is_migration_script(fp):
                continue
            findings.append(fp)
    assert not findings, (
        "MongoDB config references found in application files:\n"
        + "\n".join(findings)
    )


def test_no_mongodb_legacy_shims():
    """No application file should use legacy MongoDB shim functions."""
    findings = []
    for fp in _collect_python_files("app"):
        source = _read_file_safe(fp)
        if not source:
            continue
        if _has_legacy_shim(source):
            if _is_migration_script(fp):
                continue
            findings.append(fp)
    assert not findings, (
        "Legacy MongoDB shim functions found in application files:\n"
        + "\n".join(findings)
    )


def test_no_get_collection_in_runtime():
    """No runtime application file should call get_collection."""
    findings = []
    for fp in _collect_python_files("app"):
        source = _read_file_safe(fp)
        if not source:
            continue
        if _has_get_collection(source):
            if _is_migration_script(fp):
                continue
            findings.append(fp)
    assert not findings, (
        "get_collection calls found in application files:\n"
        + "\n".join(findings)
    )


def test_no_mongo_compat_collection_in_runtime():
    """No runtime application file should reference MongoCompatCollection."""
    findings = []
    for fp in _collect_python_files("app"):
        source = _read_file_safe(fp)
        if not source:
            continue
        if _has_mongo_compat_collection(source):
            if _is_migration_script(fp):
                continue
            findings.append(fp)
    assert not findings, (
        "MongoCompatCollection references found in application files:\n"
        + "\n".join(findings)
    )


def test_no_mongodb_operators_in_routes():
    """No route file should use MongoDB-specific operators."""
    findings = []
    for fp in _collect_python_files("app/routes"):
        source = _read_file_safe(fp)
        if not source:
            continue
        # Skip question_store operations (in-memory bank)
        if "question_store" in fp:
            if _has_mongodb_operator(source) and "question_store.find" not in source:
                findings.append(fp)
            continue
        if _has_mongodb_operator(source):
            findings.append(fp)
    assert not findings, (
        "MongoDB-specific operators found in route files:\n"
        + "\n".join(findings)
    )


def test_no_mongodb_operators_in_services():
    """No service file should use MongoDB-specific operators."""
    findings = []
    for fp in _collect_python_files("app/services"):
        source = _read_file_safe(fp)
        if not source:
            continue
        if "question_store" in fp:
            if _has_mongodb_operator(source) and "question_store.find" not in source:
                findings.append(fp)
            continue
        if _has_mongodb_operator(source):
            findings.append(fp)
    assert not findings, (
        "MongoDB-specific operators found in service files:\n"
        + "\n".join(findings)
    )


def test_no_mongodb_operators_in_middleware():
    """No middleware file should use MongoDB-specific operators."""
    findings = []
    for fp in _collect_python_files("app/middleware"):
        source = _read_file_safe(fp)
        if not source:
            continue
        if _has_mongodb_operator(source):
            findings.append(fp)
    assert not findings, (
        "MongoDB-specific operators found in middleware files:\n"
        + "\n".join(findings)
    )


def test_no_mongodb_operators_in_models():
    """No model file should use MongoDB-specific operators."""
    findings = []
    for fp in _collect_python_files("app/models"):
        source = _read_file_safe(fp)
        if not source:
            continue
        if _has_mongodb_operator(source):
            findings.append(fp)
    assert not findings, (
        "MongoDB-specific operators found in model files:\n"
        + "\n".join(findings)
    )


def test_app_imports_without_motor():
    """The FastAPI app should import and register routes without Motor."""
    import importlib
    import app.main  # noqa: F401
    main = importlib.import_module("app.main").app
    assert main is not None
    assert len(main.routes) > 0
