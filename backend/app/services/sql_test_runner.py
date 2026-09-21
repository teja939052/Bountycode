"""SQLite-based SQL test runner for placement SQL questions.

Creates an in-memory SQLite database per question, executes the reference
query, and returns a canonical result set for comparison.
"""
from __future__ import annotations

import json
import logging
import sqlite3
import time
import traceback
from typing import Any, Dict, List, Optional, Tuple


LOGGER = logging.getLogger("sql_test_runner")


class SQLValidationResult:
    def __init__(self, is_correct: bool, error_message: Optional[str] = None,
                 student_results: Optional[List[Dict[str, Any]]] = None,
                 expected_results: Optional[List[Dict[str, Any]]] = None,
                 execution_time_ms: float = 0.0):
        self.is_correct = is_correct
        self.error_message = error_message
        self.student_results = student_results
        self.expected_results = expected_results
        self.execution_time_ms = execution_time_ms


def _execute_query(cursor: sqlite3.Cursor, query: str) -> Tuple[List[str], List[Tuple[Any, ...]], Optional[str]]:
    try:
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        return columns, rows, None
    except sqlite3.Error as e:
        return [], [], str(e)


def verify_query(
    schema_ddl: str,
    seed_inserts: str,
    expected_query: str,
    student_query: str,
    enforce_order: bool = False
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
            execution_time_ms=(time.perf_counter() - start_time) * 1000
        )
    
    expected_cols, expected_rows, expected_err = _execute_query(cursor, expected_query)
    if expected_err:
        conn.close()
        return SQLValidationResult(
            is_correct=False,
            error_message=f"Golden Query Error (System Bug): {expected_err}",
            execution_time_ms=(time.perf_counter() - start_time) * 1000
        )
    
    student_cols, student_rows, student_err = _execute_query(cursor, student_query)
    conn.close()
    
    execution_time_ms = (time.perf_counter() - start_time) * 1000
    
    if student_err:
        return SQLValidationResult(
            is_correct=False,
            error_message=f"SQL Syntax/Runtime Error: {student_err}",
            execution_time_ms=execution_time_ms
        )
    
    student_dict_res = [dict(zip(student_cols, row)) for row in student_rows]
    expected_dict_res = [dict(zip(expected_cols, row)) for row in expected_rows]
    
    if len(student_cols) != len(expected_cols):
        return SQLValidationResult(
            is_correct=False,
            error_message=f"Column count mismatch. Expected {len(expected_cols)}, got {len(student_cols)}.",
            student_results=student_dict_res[:10],
            expected_results=expected_dict_res[:10],
            execution_time_ms=execution_time_ms
        )
    
    if len(student_rows) != len(expected_rows):
        return SQLValidationResult(
            is_correct=False,
            error_message=f"Row count mismatch. Expected {len(expected_rows)} rows, got {len(student_rows)}.",
            student_results=student_dict_res[:10],
            expected_results=expected_dict_res[:10],
            execution_time_ms=execution_time_ms
        )
    
    if enforce_order:
        for idx, (s_row, e_row) in enumerate(zip(student_rows, expected_rows)):
            if s_row != e_row:
                return SQLValidationResult(
                    is_correct=False,
                    error_message=f"Row sequence mismatch at row index {idx + 1}.",
                    student_results=student_dict_res[:10],
                    expected_results=expected_dict_res[:10],
                    execution_time_ms=execution_time_ms
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
                execution_time_ms=execution_time_ms
            )
    
    return SQLValidationResult(
        is_correct=True,
        student_results=student_dict_res[:10],
        expected_results=expected_dict_res[:10],
        execution_time_ms=execution_time_ms
    )


def generate_canonical_result(schema_ddl: str, seed_inserts: str, query: str) -> Optional[Dict[str, Any]]:
    """Execute a query and return the canonical result set."""
    try:
        result = verify_query(schema_ddl, seed_inserts, query, query, enforce_order=False)
        if result.is_correct and result.expected_results is not None:
            return {
                "columns": list(result.expected_results[0].keys()) if result.expected_results else [],
                "rows": result.expected_results,
                "execution_time_ms": result.execution_time_ms,
            }
        return None
    except Exception as e:
        LOGGER.warning("Failed to generate canonical result: %s", str(e))
        return None
