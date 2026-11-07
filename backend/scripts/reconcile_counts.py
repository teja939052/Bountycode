"""Global reconciliation: compute exact counts after all fixes."""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List
from collections import Counter, defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

LOGGER = logging.getLogger("reconcile")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

BACKEND_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = BACKEND_ROOT / "app" / "data"


def main() -> None:
    import app.services.question_store as qs
    qs.load_all()
    questions = qs._questions
    
    LOGGER.info("Loaded %d questions", len(questions))
    
    # Compute exact counts
    total = len(questions)
    by_type = Counter()
    executable_by_type = Counter()
    servable_by_type = Counter()
    
    for q in questions:
        qtype = str(q.get("type", "unknown")).lower()
        by_type[qtype] += 1
        
        if qs._is_executable(q):
            executable_by_type[qtype] += 1
        
        if qs._is_servable(q):
            servable_by_type[qtype] += 1
    
    # Compute totals
    total_executable = sum(executable_by_type.values())
    total_servable = sum(servable_by_type.values())
    
    # Print report
    LOGGER.info("=== GLOBAL RECONCILIATION ===")
    LOGGER.info("Total questions: %d", total)
    LOGGER.info("Total executable: %d", total_executable)
    LOGGER.info("Total servable: %d", total_servable)
    LOGGER.info("")
    
    LOGGER.info("By type:")
    for qtype in sorted(by_type.keys()):
        total_t = by_type[qtype]
        exec_t = executable_by_type[qtype]
        serv_t = servable_by_type[qtype]
        LOGGER.info("  %s: total=%d, executable=%d, servable=%d", qtype, total_t, exec_t, serv_t)
    
    # Check for SQL questions with no test cases in servable pool
    sql_servable_no_tc = 0
    for q in questions:
        if not qs._is_servable(q):
            continue
        if str(q.get("type", "")).lower() == "sql":
            tcs = q.get("test_cases") or q.get("testcases") or []
            if len(tcs) == 0:
                sql_servable_no_tc += 1
    
    LOGGER.info("")
    LOGGER.info("SQL servable but NO test cases: %d", sql_servable_no_tc)
    
    # Trust status breakdown
    LOGGER.info("")
    LOGGER.info("Trust status breakdown:")
    status_counts = Counter(q.get("trust_status", "") for q in questions)
    for status, count in status_counts.most_common():
        label = status if status else "(empty)"
        LOGGER.info("  %s: %d", label, count)
    
    # Save report
    report = {
        "total": total,
        "total_executable": total_executable,
        "total_servable": total_servable,
        "by_type": {
            qtype: {
                "total": by_type[qtype],
                "executable": executable_by_type[qtype],
                "servable": servable_by_type[qtype],
            }
            for qtype in sorted(by_type.keys())
        },
        "sql_servable_no_tc": sql_servable_no_tc,
        "trust_status_breakdown": {
            (status if status else "(empty)"): count
            for status, count in status_counts.most_common()
        },
    }
    
    report_path = DATA_DIR / "reconciliation_report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    LOGGER.info("Saved reconciliation report to %s", report_path)


if __name__ == "__main__":
    main()
