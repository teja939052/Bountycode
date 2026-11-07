"""Batch intake-lint spot-check over the canonical store.

Answers: how much stub/filler content is already in the bank, and which
source_bank contributed it. Read-only: never mutates store, banks, MongoDB,
or trust_status.

Writes: backend/app/data/intake_lint_report.json
"""
import json
import os
import sys
from collections import Counter

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from app.services import question_store  # noqa: E402
from app.services.intake_lint import lint_batch  # noqa: E402

DATA_DIR = os.path.join(BACKEND_ROOT, "app", "data")


def main():
    question_store.load_all()
    docs = question_store._questions
    counts, rejected = lint_batch(docs)
    by_reason = Counter()
    by_source = Counter()
    by_type = Counter()
    for r in rejected:
        for reason in r["reasons"]:
            by_reason[reason] += 1
        by_source[str(r.get("source_bank") or "unknown")] += 1
        by_type[str(r.get("type") or "unknown")] += 1
    report = {
        "scanned": len(docs),
        "verdicts": counts,
        "rejected_by_reason": dict(by_reason.most_common()),
        "rejected_by_source_bank_top20": dict(by_source.most_common(20)),
        "rejected_by_type": dict(by_type),
        "rejected_sample": rejected[:40],
        "rule": "intake screen only; no trust_status mutation, no promotion, no quarantine",
    }
    with open(os.path.join(DATA_DIR, "intake_lint_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=1)
    print(json.dumps({k: v for k, v in report.items() if k != "rejected_sample"}, indent=1)[:3000])


if __name__ == "__main__":
    main()
