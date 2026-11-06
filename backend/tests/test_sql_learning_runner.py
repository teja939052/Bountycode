"""Regression tests for safe, deterministic SQL lesson grading."""
from app.services.sql_engine import SQLEngine

SCHEMA = "CREATE TABLE employee (id INTEGER, department TEXT);"
SEED = "INSERT INTO employee VALUES (1, 'Sales'); INSERT INTO employee VALUES (2, 'Sales'); INSERT INTO employee VALUES (3, 'Engineering');"


def test_read_only_sql_lab_accepts_correct_select():
    result = SQLEngine.verify_read_only_query(SCHEMA, SEED,
        "SELECT department FROM employee ORDER BY id;",
        "SELECT department FROM employee ORDER BY id;", enforce_order=True)
    assert result.is_correct is True


def test_read_only_sql_lab_compares_duplicate_rows():
    result = SQLEngine.verify_read_only_query(SCHEMA, SEED,
        "SELECT department FROM employee;",
        "SELECT DISTINCT department FROM employee;")
    assert result.is_correct is False


def test_read_only_sql_lab_rejects_write_statements():
    result = SQLEngine.verify_read_only_query(SCHEMA, SEED,
        "SELECT department FROM employee;", "DELETE FROM employee;")
    assert result.is_correct is False
    assert "read-only" in (result.error_message or "").lower()


def test_read_only_sql_lab_rejects_attach_and_pragma():
    for query in ("ATTACH DATABASE ':memory:' AS extra;", "PRAGMA database_list;"):
        result = SQLEngine.verify_read_only_query(SCHEMA, SEED,
            "SELECT department FROM employee;", query)
        assert result.is_correct is False


def test_read_only_sql_lab_enforces_execution_budget():
    result = SQLEngine.verify_read_only_query(SCHEMA, SEED,
        "SELECT department FROM employee;",
        "WITH RECURSIVE loop(x) AS (SELECT 1 UNION ALL SELECT x + 1 FROM loop) SELECT sum(x) FROM loop;",
        timeout_seconds=0.03)
    assert result.is_correct is False
    assert "budget" in (result.error_message or "").lower() or "interrupted" in (result.error_message or "").lower()


def test_read_only_sql_lab_limits_result_rows():
    schema = "CREATE TABLE numbers (value INTEGER);"
    seed = "INSERT INTO numbers VALUES " + ", ".join(f"({i})" for i in range(105)) + ";"
    result = SQLEngine.verify_read_only_query(schema, seed,
        "SELECT value FROM numbers;", "SELECT value FROM numbers;", max_rows=100)
    assert result.is_correct is False
    assert "100 rows" in (result.error_message or "").lower()
