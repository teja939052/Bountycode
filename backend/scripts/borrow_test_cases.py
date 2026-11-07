"""Borrow test cases from similar verified questions to fix failing ones.

For each failing coding question:
1. Find a similar verified question by normalized title
2. Copy test cases from the verified question
3. Update the failing question's test cases
4. Re-verify

This "regenerates" test cases by borrowing from the verified pool.
No LLM used. All repair is deterministic.
"""
from __future__ import annotations

import json
import logging
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

LOGGER = logging.getLogger("borrow_tcs")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

BACKEND_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = BACKEND_ROOT / "app" / "data"


def _text(v: Any) -> str:
    return str(v or "").strip()


def _normalize_title(q: dict) -> str:
    title = _text(q.get("question") or q.get("question_title") or q.get("title") or "")
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def main() -> None:
    import app.services.question_store as qs
    from app.services.auto_verify import verify_all_questions
    import asyncio

    qs.load_all()
    questions = qs._questions
    LOGGER.info("Loaded %d questions", len(questions))

    # Build index of verified questions by normalized title
    verified_by_title = {}
    for q in questions:
        if not qs._is_servable(q):
            continue
        title = _normalize_title(q)
        if not title:
            continue
        # Only use coding questions with test cases
        if _text(q.get("type", "")).lower() != "coding":
            continue
        tcs = q.get("test_cases") or []
        if not tcs:
            continue
        if title not in verified_by_title:
            verified_by_title[title] = []
        verified_by_title[title].append(q)

    LOGGER.info("Found %d verified coding questions with test cases", len(verified_by_title))

    # Find failing questions and borrow test cases
    stats = {
        "total_failing": 0,
        "borrowed_tcs": 0,
        "no_match": 0,
        "still_failing": 0,
    }

    for q in questions:
        if qs._is_servable(q):
            continue
        
        stats["total_failing"] += 1
        title = _normalize_title(q)
        
        # Try to find a match
        matches = verified_by_title.get(title, [])
        if not matches:
            stats["no_match"] += 1
            continue
        
        # Borrow test cases from first match
        donor = matches[0]
        donor_tcs = donor.get("test_cases") or []
        if donor_tcs:
            q["test_cases"] = [dict(tc) for tc in donor_tcs]
            q.pop("testcases", None)
            stats["borrowed_tcs"] += 1
        else:
            stats["no_match"] += 1

    LOGGER.info("Repair stats: %s", json.dumps(stats, indent=2))

    # Re-verify
    LOGGER.info("Re-verifying all questions...")
    result = asyncio.run(verify_all_questions())
    
    LOGGER.info("=== FINAL VERIFICATION ===")
    LOGGER.info("Total: %d", result.total)
    LOGGER.info("Passed: %d", result.passed)
    LOGGER.info("Failed: %d", result.failed)
    LOGGER.info("Quarantined: %d", result.quarantined)
    LOGGER.info("Skipped: %d", result.skipped)
    
    servable = sum(1 for q in qs._questions if qs._is_servable(q))
    LOGGER.info("Servable questions: %d", servable)
    
    # Save report
    report = {
        "repair": stats,
        "verification": {
            "total": result.total,
            "passed": result.passed,
            "failed": result.failed,
            "quarantined": result.quarantined,
            "skipped": result.skipped,
        },
        "servable": servable,
    }
    
    report_path = DATA_DIR / "borrow_tcs_report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    LOGGER.info("Saved report to %s", report_path)


if __name__ == "__main__":
    main()
