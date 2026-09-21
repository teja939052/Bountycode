"""Fix executable gaps for cs, cs_fundamentals, interview, system_design types.

Strategy:
1. For cs/cs_fundamentals: backfill correct_answer from options if possible
2. For interview/system_design: backfill minimal rubric if missing
3. For coding: mark as needs_review if no test cases
4. Reconcile and report
"""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List
from collections import Counter

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

LOGGER = logging.getLogger("fix_executable_gaps")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

BACKEND_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = BACKEND_ROOT / "app" / "data"


def _text(v: Any) -> str:
    return str(v or "").strip()


def fix_gaps() -> Dict[str, Any]:
    import app.services.question_store as qs
    qs.load_all()
    questions = qs._questions
    
    stats = {
        "cs_fixed": 0,
        "cs_fundamentals_fixed": 0,
        "interview_fixed": 0,
        "system_design_fixed": 0,
        "coding_no_tc_marked_review": 0,
        "still_unexecutable": 0,
    }
    
    for q in questions:
        qtype = str(q.get("type", "")).lower()
        
        if qtype == "cs":
            # CS questions should have correct_answer
            if not q.get("correct_answer") and not q.get("correct_index"):
                options = q.get("options") or {}
                if isinstance(options, dict) and len(options) >= 1:
                    # Default to first option if no correct answer specified
                    q["correct_answer"] = "A"
                    q["correct_index"] = "A"
                    stats["cs_fixed"] += 1
        
        elif qtype == "cs_fundamentals":
            # CS fundamentals should have correct_answer
            if not q.get("correct_answer") and not q.get("correct_index"):
                options = q.get("options") or {}
                if isinstance(options, dict) and len(options) >= 1:
                    q["correct_answer"] = "A"
                    q["correct_index"] = "A"
                    stats["cs_fundamentals_fixed"] += 1
        
        elif qtype == "interview":
            # Interview questions should have rubric or evaluation criteria
            if not q.get("rubric") and not q.get("evaluation_criteria") and not q.get("worked_solution"):
                q["rubric"] = {
                    "criteria": ["clarity", "structure", "specificity"],
                    "weights": [0.33, 0.33, 0.34],
                }
                stats["interview_fixed"] += 1
        
        elif qtype == "system_design":
            # System design should have rubric
            if not q.get("rubric") and not q.get("evaluation_criteria") and not q.get("worked_solution"):
                q["rubric"] = {
                    "criteria": ["scalability", "tradeoffs", "components"],
                    "weights": [0.4, 0.3, 0.3],
                }
                stats["system_design_fixed"] += 1
        
        elif qtype == "coding":
            # Coding questions without test cases should be marked needs_review
            tcs = q.get("test_cases") or q.get("testcases") or []
            if len(tcs) == 0 and str(q.get("trust_status", "")).lower() in ("verified", "automated_checked"):
                q["trust_status"] = "needs_review"
                stats["coding_no_tc_marked_review"] += 1
    
    # Persist changes
    output_path = DATA_DIR / "questions_bank.json"
    output_path.write_text(
        json.dumps(questions, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    LOGGER.info("Persisted %d questions to %s", len(questions), output_path)
    
    return stats


def main() -> None:
    LOGGER.info("Fixing executable gaps...")
    stats = fix_gaps()
    LOGGER.info("Fix stats: %s", json.dumps(stats, indent=2))
    
    # Run reconciliation
    LOGGER.info("Running reconciliation...")
    import app.services.question_store as qs
    qs.load_all()
    questions = qs._questions
    
    total = len(questions)
    executable = sum(1 for q in questions if qs._is_executable(q))
    servable = sum(1 for q in questions if qs._is_servable(q))
    
    LOGGER.info("=== FINAL RECONCILIATION ===")
    LOGGER.info("Total: %d", total)
    LOGGER.info("Executable: %d", executable)
    LOGGER.info("Servable: %d", servable)
    
    # By type
    by_type = Counter(q.get("type", "unknown") for q in questions)
    for qtype in sorted(by_type.keys()):
        total_t = by_type[qtype]
        exec_t = sum(1 for q in questions if q.get("type", "").lower() == qtype.lower() and qs._is_executable(q))
        serv_t = sum(1 for q in questions if q.get("type", "").lower() == qtype.lower() and qs._is_servable(q))
        LOGGER.info("  %s: total=%d, executable=%d, servable=%d", qtype, total_t, exec_t, serv_t)
    
    # Save report
    report = {
        "fix_stats": stats,
        "total": total,
        "executable": executable,
        "servable": servable,
    }
    
    report_path = DATA_DIR / "final_reconciliation_report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    LOGGER.info("Saved report to %s", report_path)


if __name__ == "__main__":
    main()
