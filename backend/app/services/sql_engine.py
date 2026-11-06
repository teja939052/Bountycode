# backend/app/services/sql_engine.py
import sqlite3
import time
import re
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel


class SQLSchemaMetadata(BaseModel):
    schema_ddl: str
    seed_inserts: str
    expected_query: str
    enforce_order: bool = False


class SQLValidationResult(BaseModel):
    is_correct: bool
    error_message: Optional[str] = None
    student_results: Optional[List[Dict[str, Any]]] = None
    expected_results: Optional[List[Dict[str, Any]]] = None
    execution_time_ms: float = 0.0


class SQLEngine:
    @staticmethod
    def _execute_query(cursor: sqlite3.Cursor, query: str) -> Tuple[List[str], List[Tuple[Any, ...]], Optional[str]]:
        try:
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
            return columns, rows, None
        except sqlite3.Error as e:
            return [], [], str(e)

    @classmethod
    def verify_query(
        cls,
        schema_ddl: str,
        seed_inserts: str,
        expected_query: str,
        student_query: str,
        enforce_order: bool = False,
    ) -> SQLValidationResult:
        start_time = time.perf_counter()

        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()

        try:
            cursor.executescript(schema_ddl)
            cursor.executescript(seed_inserts)
            conn.commit()
        except sqlite3.Error as e:
            conn.close()
            return SQLValidationResult(
                is_correct=False,
                error_message=f"DB Initialization Failure: {str(e)}",
                execution_time_ms=(time.perf_counter() - start_time) * 1000,
            )

        expected_cols, expected_rows, expected_err = cls._execute_query(cursor, expected_query)
        if expected_err:
            conn.close()
            return SQLValidationResult(
                is_correct=False,
                error_message=f"Golden Query Error (System Bug): {expected_err}",
                execution_time_ms=(time.perf_counter() - start_time) * 1000,
            )

        student_cols, student_rows, student_err = cls._execute_query(cursor, student_query)
        conn.close()

        execution_time_ms = (time.perf_counter() - start_time) * 1000

        if student_err:
            return SQLValidationResult(
                is_correct=False,
                error_message=f"SQL Syntax/Runtime Error: {student_err}",
                execution_time_ms=execution_time_ms,
            )

        student_dict_res = [dict(zip(student_cols, row)) for row in student_rows]
        expected_dict_res = [dict(zip(expected_cols, row)) for row in expected_rows]

        if len(student_cols) != len(expected_cols):
            return SQLValidationResult(
                is_correct=False,
                error_message=f"Column count mismatch. Expected {len(expected_cols)}, got {len(student_cols)}.",
                student_results=student_dict_res[:10],
                expected_results=expected_dict_res[:10],
                execution_time_ms=execution_time_ms,
            )

        if len(student_rows) != len(expected_rows):
            return SQLValidationResult(
                is_correct=False,
                error_message=f"Row count mismatch. Expected {len(expected_rows)} rows, got {len(student_rows)}.",
                student_results=student_dict_res[:10],
                expected_results=expected_dict_res[:10],
                execution_time_ms=execution_time_ms,
            )

        if enforce_order:
            for idx, (s_row, e_row) in enumerate(zip(student_rows, expected_rows)):
                if s_row != e_row:
                    return SQLValidationResult(
                        is_correct=False,
                        error_message=f"Row sequence mismatch at row index {idx + 1}.",
                        student_results=student_dict_res[:10],
                        expected_results=expected_dict_res[:10],
                        execution_time_ms=execution_time_ms,
                    )
        else:
            student_set = set(student_rows)
            expected_set = set(expected_rows)
            if student_set != expected_set:
                return SQLValidationResult(
                    is_correct=False,
                    error_message="Dataset matched in volume but returned incorrect values/rows.",
                    student_results=student_dict_res[:10],
                    expected_results=expected_dict_res[:10],
                    execution_time_ms=execution_time_ms,
                )

        return SQLValidationResult(
            is_correct=True,
            student_results=student_dict_res[:10],
            expected_results=expected_dict_res[:10],
            execution_time_ms=execution_time_ms,
        )

    @classmethod
    def verify_read_only_query(
        cls,
        schema_ddl: str,
        seed_inserts: str,
        expected_query: str,
        student_query: str,
        enforce_order: bool = False,
        timeout_seconds: float = 0.35,
        max_rows: int = 100,
    ) -> SQLValidationResult:
        """Grade one SELECT/WITH query against a fresh, read-only in-memory DB.

        Schema and seed SQL are trusted authored lesson data. Student SQL is a
        single read-only statement, with write/attach/pragma actions denied,
        a progress-handler deadline and a bounded result set.
        """
        started = time.perf_counter()
        query = (student_query or "").strip()
        if not query or len(query) > 8_000:
            return SQLValidationResult(
                is_correct=False,
                error_message="Enter a SQL query of at most 8,000 characters.",
                execution_time_ms=(time.perf_counter() - started) * 1000,
            )
        if not re.match(r"^(SELECT|WITH)\\b", query, flags=re.IGNORECASE):
            return SQLValidationResult(
                is_correct=False,
                error_message="This exercise accepts read-only SELECT or WITH queries only.",
                execution_time_ms=(time.perf_counter() - started) * 1000,
            )

        conn = sqlite3.connect(":memory:")
        try:
            cursor = conn.cursor()
            cursor.executescript(schema_ddl)
            cursor.executescript(seed_inserts)
            conn.commit()

            expected_cols, expected_rows, expected_error = cls._execute_query(cursor, expected_query)
            if expected_error:
                return SQLValidationResult(
                    is_correct=False,
                    error_message=f"Lesson data error: {expected_error}",
                    execution_time_ms=(time.perf_counter() - started) * 1000,
                )

            cursor.execute("PRAGMA query_only = ON")
            denied_actions = {
                getattr(sqlite3, name)
                for name in (
                    "SQLITE_ATTACH", "SQLITE_DETACH", "SQLITE_INSERT", "SQLITE_UPDATE",
                    "SQLITE_DELETE", "SQLITE_ALTER_TABLE", "SQLITE_CREATE_INDEX",
                    "SQLITE_CREATE_TABLE", "SQLITE_CREATE_TEMP_INDEX",
                    "SQLITE_CREATE_TEMP_TABLE", "SQLITE_CREATE_TEMP_TRIGGER",
                    "SQLITE_CREATE_TEMP_VIEW", "SQLITE_CREATE_TRIGGER",
                    "SQLITE_CREATE_VIEW", "SQLITE_CREATE_VTABLE", "SQLITE_DROP_INDEX",
                    "SQLITE_DROP_TABLE", "SQLITE_DROP_TEMP_INDEX", "SQLITE_DROP_TEMP_TABLE",
                    "SQLITE_DROP_TEMP_TRIGGER", "SQLITE_DROP_TEMP_VIEW", "SQLITE_DROP_TRIGGER",
                    "SQLITE_DROP_VIEW", "SQLITE_DROP_VTABLE", "SQLITE_PRAGMA",
                    "SQLITE_TRANSACTION", "SQLITE_SAVEPOINT",
                )
                if hasattr(sqlite3, name)
            }

            def authorize(action, arg1, arg2, _database, _trigger):
                if action in denied_actions:
                    return sqlite3.SQLITE_DENY
                if action == getattr(sqlite3, "SQLITE_FUNCTION", -1):
                    function_name = str(arg2 or arg1 or "").lower()
                    if function_name in {"load_extension", "readfile", "writefile"}:
                        return sqlite3.SQLITE_DENY
                return sqlite3.SQLITE_OK

            deadline = time.perf_counter() + max(0.02, min(float(timeout_seconds), 1.0))
            conn.set_authorizer(authorize)
            conn.set_progress_handler(lambda: 1 if time.perf_counter() > deadline else 0, 1_000)

            try:
                cursor.execute(query)  # execute(), not executescript(): one statement only.
                student_cols = [desc[0] for desc in cursor.description] if cursor.description else []
                student_rows = cursor.fetchmany(max_rows + 1)
            except sqlite3.Error as exc:
                message = str(exc)
                if "interrupted" in message.lower():
                    message = "Query exceeded the short execution budget. Reduce the amount of work."
                elif "not authorized" in message.lower() or "readonly" in message.lower():
                    message = "Only read-only SELECT or WITH queries are allowed in this exercise."
                return SQLValidationResult(
                    is_correct=False,
                    error_message=message,
                    execution_time_ms=(time.perf_counter() - started) * 1000,
                )

            if len(student_rows) > max_rows:
                return SQLValidationResult(
                    is_correct=False,
                    error_message=f"Return at most {max_rows} rows for this exercise.",
                    execution_time_ms=(time.perf_counter() - started) * 1000,
                )

            student_dict = [dict(zip(student_cols, row)) for row in student_rows]
            if len(student_cols) != len(expected_cols):
                correct = False
                message = f"Expected {len(expected_cols)} columns, but your query returned {len(student_cols)}."
            elif enforce_order:
                correct = student_rows == expected_rows
                message = None if correct else "Your rows or their order do not match the required result."
            else:
                correct = Counter(student_rows) == Counter(expected_rows)
                message = None if correct else "Your query runs, but its rows or values do not match the required result."

            return SQLValidationResult(
                is_correct=correct,
                error_message=message,
                student_results=student_dict[:10],
                expected_results=None,
                execution_time_ms=(time.perf_counter() - started) * 1000,
            )
        except sqlite3.Error as exc:
            return SQLValidationResult(
                is_correct=False,
                error_message=f"Lesson data error: {exc}",
                execution_time_ms=(time.perf_counter() - started) * 1000,
            )
        finally:
            conn.close()

    @classmethod
    def generate_canonical_result(cls, schema_ddl: str, seed_inserts: str, query: str) -> Optional[Dict[str, Any]]:
        try:
            result = cls.verify_query(schema_ddl, seed_inserts, query, query, enforce_order=False)
            if result.is_correct and result.expected_results is not None:
                return {
                    "columns": list(result.expected_results[0].keys()) if result.expected_results else [],
                    "rows": result.expected_results,
                    "execution_time_ms": result.execution_time_ms,
                }
            return None
        except Exception:
            return None
