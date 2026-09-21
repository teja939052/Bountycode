"""Fix MCQ verification issues:
1. Invalidate 38 stale verified/automated_checked stamps from broken logic
2. Normalize 346 mismatched test case outputs to match correct_answer
3. Ensure all MCQs have test_cases[0].output == correct_answer (A-D)
"""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

LOGGER = logging.getLogger("fix_mcqs")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

BACKEND_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = BACKEND_ROOT / "app" / "data"


def _text(v: Any) -> str:
    return str(v or "").strip()


def fix_mcqs() -> Dict[str, Any]:
    # Load all questions
    import app.services.question_store as qs
    qs.load_all()
    questions = qs._questions
    
    stats = {
        "total_mcqs": 0,
        "stale_stamps_invalidated": 0,
        "mismatches_normalized": 0,
        "test_cases_fixed": 0,
        "already_clean": 0,
    }
    
    mcq_types = ("aptitude", "logical", "verbal", "hr", "behavioral", "cs_fundamentals", "cs")
    
    for q in questions:
        qtype = str(q.get("type", "")).lower()
        if qtype not in mcq_types:
            continue
        
        stats["total_mcqs"] += 1
        correct = _text(q.get("correct_answer") or q.get("correct_index") or "").upper()
        
        # Skip if no valid correct answer
        if correct not in ("A", "B", "C", "D"):
            continue
        
        # Check if this was stamped by broken logic
        # The broken logic required ALL options to equal correct answer
        # So questions with mismatched test cases were incorrectly stamped
        status = str(q.get("trust_status", "")).lower()
        if status in ("verified", "automated_checked"):
            # Check if test cases actually match
            tcs = q.get("test_cases") or []
            has_mismatch = False
            for tc in tcs:
                if isinstance(tc, dict):
                    out = _text(tc.get("output", "") or tc.get("input", "")).upper()
                    if out and out != correct:
                        has_mismatch = True
                        break
            
            if has_mismatch:
                # Invalidate stale stamp
                q["trust_status"] = "needs_review"
                q.pop("verified_at", None)
                q.pop("automated_checked_at", None)
                q.pop("verified_by", None)
                q.pop("reviewer_id", None)
                stats["stale_stamps_invalidated"] += 1
        
        # Normalize test cases
        tcs = q.get("test_cases") or []
        if not tcs:
            # Create minimal test case
            q["test_cases"] = [{"input": None, "output": correct, "hidden": False}]
            stats["test_cases_fixed"] += 1
        else:
            # Fix mismatched outputs
            fixed = False
            for tc in tcs:
                if isinstance(tc, dict):
                    out = _text(tc.get("output", "") or tc.get("input", "")).upper()
                    if out != correct:
                        tc["output"] = correct
                        tc.pop("input", None)
                        fixed = True
            
            if fixed:
                stats["mismatches_normalized"] += 1
            else:
                stats["already_clean"] += 1
    
    # Persist changes back to questions_bank.json
    output_path = DATA_DIR / "questions_bank.json"
    output_path.write_text(
        json.dumps(questions, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    LOGGER.info("Persisted %d questions to %s", len(questions), output_path)
    
    return stats


def main() -> None:
    LOGGER.info("Fixing MCQ verification issues...")
    stats = fix_mcqs()
    LOGGER.info("MCQ fix stats: %s", json.dumps(stats, indent=2))
    
    # Save report
    report_path = DATA_DIR / "mcq_fix_report.json"
    report_path.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
    LOGGER.info("Saved report to %s", report_path)


if __name__ == "__main__":
    main()
