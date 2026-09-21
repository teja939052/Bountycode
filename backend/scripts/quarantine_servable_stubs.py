"""Quarantine the 26 stub-content questions that are currently servable.

Mechanism (proven): literal-return stub + stub-consistent test cases pass
execution verification by construction. Intake lint now blocks this class
at the door; these 26 predated the lint and carry automated_checked stamps.

Method: append ids to backend/app/data/served_quarantine.json (the file-seed
quarantine layer applied by question_store at load). No source-bank mutation,
no trust_status writes, Mongo untouched. Reversible by removing the entries.
Idempotent: skips ids already listed.
"""
import json
import os
import sys

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from app.services import question_store  # noqa: E402
from app.services.intake_lint import lint_question  # noqa: E402

SQ_PATH = os.path.join(BACKEND_ROOT, "app", "data", "served_quarantine.json")
REASON = ("intake_lint:stub_literal_return_only — literal-return stub with "
          "stub-consistent test cases passes execution by construction; "
          "needs authored solution + independent test cases")


def main():
    question_store.load_all()
    targets = []
    for q in question_store._questions:
        try:
            r = lint_question(q)
        except Exception:
            continue
        if r["verdict"] == "rejected" and question_store._is_servable(q):
            targets.append(q)
    with open(SQ_PATH, encoding="utf-8") as f:
        existing = json.load(f)
    have = {str(e.get("id")) for e in existing if isinstance(e, dict)}
    added = 0
    for q in targets:
        qid = str(q.get("id"))
        if qid in have:
            continue
        existing.append({"id": qid,
                         "title": str(q.get("question") or "")[:80],
                         "reason": REASON, "passed": 0,
                         "total": len(q.get("test_cases") or q.get("testcases") or [])})
        have.add(qid)
        added += 1
    with open(SQ_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=1)
    print(json.dumps({"servable_stubs_found": len(targets),
                      "quarantine_entries_added": added,
                      "quarantine_file_total": len(existing)}, indent=1))


if __name__ == "__main__":
    main()
