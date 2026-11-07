"""Auto-generate SQL test cases for questions with solutions but no test cases.

For each SQL question that has:
- schema_ddl and seed_inserts
- correct_query or solution_sql
- NO test_cases

Attempt to:
1. Build an in-memory SQLite DB
2. Execute the reference query
3. Capture the canonical result set
4. Store as test_cases[0]

Mark as automated_checked on success, needs_review on failure.
"""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

LOGGER = logging.getLogger("sql_tc_gen")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

BACKEND_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = BACKEND_ROOT / "app" / "data"


def _text(v: Any) -> str:
    return str(v or "").strip()


def generate_sql_test_cases() -> Dict[str, Any]:
    from app.services.sql_test_runner import generate_canonical_result
    
    # Load questions
    import app.services.question_store as qs
    qs.load_all()
    questions = qs._questions
    
    stats = {
        "total_sql": 0,
        "already_has_tc": 0,
        "missing_schema_or_query": 0,
        "generated_tc": 0,
        "generation_failed": 0,
        "marked_needs_review": 0,
    }
    
    for q in questions:
        qtype = str(q.get("type", "")).lower()
        if qtype != "sql":
            continue
        
        stats["total_sql"] += 1
        
        # Skip if already has test cases
        tcs = q.get("test_cases") or q.get("testcases") or []
        if tcs:
            stats["already_has_tc"] += 1
            continue
        
        # Check for required fields
        schema_ddl = _text(q.get("sql_schema") or q.get("schema_ddl") or "")
        seed_inserts = _text(q.get("sample_data") or q.get("seed_inserts") or "")
        correct_query = _text(q.get("correct_query") or q.get("solution_sql") or "")
        
        if not schema_ddl or not seed_inserts or not correct_query:
            stats["missing_schema_or_query"] += 1
            q["trust_status"] = "needs_review"
            stats["marked_needs_review"] += 1
            continue
        
        # Try to generate test case
        try:
            canonical = generate_canonical_result(schema_ddl, seed_inserts, correct_query)
            if canonical:
                q["test_cases"] = [{
                    "input": None,
                    "output": canonical,
                    "type": "sql_result",
                    "hidden": False,
                }]
                q["trust_status"] = "automated_checked"
                stats["generated_tc"] += 1
            else:
                q["trust_status"] = "needs_review"
                stats["generation_failed"] += 1
        except Exception as e:
            LOGGER.warning("Failed to generate TC for %s: %s", q.get("id"), str(e))
            q["trust_status"] = "needs_review"
            stats["generation_failed"] += 1
    
    # Persist changes
    output_path = DATA_DIR / "questions_bank.json"
    output_path.write_text(
        json.dumps(questions, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    LOGGER.info("Persisted %d questions to %s", len(questions), output_path)
    
    return stats


def main() -> None:
    LOGGER.info("Generating SQL test cases...")
    stats = generate_sql_test_cases()
    LOGGER.info("SQL TC generation stats: %s", json.dumps(stats, indent=2))
    
    # Save report
    report_path = DATA_DIR / "sql_tc_generation_report.json"
    report_path.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
    LOGGER.info("Saved report to %s", report_path)


if __name__ == "__main__":
    main()
