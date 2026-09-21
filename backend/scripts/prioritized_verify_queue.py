"""Prioritized verification queue — deterministic, zero LLM.

Builds an ordered queue of (unverified + needs_review + executable) questions,
sorted so high-traffic content gets human review first:

  score = pattern_weight + company_weight
  - pattern_weight: frequency of the question's Striver pattern across the
    servable bank (what students actually practice gets reviewed first).
  - company_weight: +100 for priority placement companies
    (tcs, infosys, wipro) and +50 for FAANG explicit tags.

Then runs the deterministic auto-verifier (auto_verify.verify_question) over
the queue IN PRIORITY ORDER in this isolated process only (server state is
untouched). Passes become AUTOMATED_CHECKED promotion *candidates* written to
a candidate file for the tranche-approve flow. Nothing is auto-promoted into
a source bank; trust_status in source files is never written by this script.

Writes:
  backend/app/data/prioritized_verify_queue.json   (ordered ids + scores)
  backend/app/data/prioritized_verify_report.json  (pass/fail/quarantine outcome)
  backend/app/data/prioritized_verify_candidates.json (passed items, review only)
"""
import json
import os
import sys
from collections import Counter

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from app.services import question_store  # noqa: E402
from app.services.question_store import _is_executable  # noqa: E402
from app.services.auto_verify import verify_question  # noqa: E402

DATA_DIR = os.path.join(BACKEND_ROOT, "app", "data")
QUEUE_PATH = os.path.join(DATA_DIR, "prioritized_verify_queue.json")
REPORT_PATH = os.path.join(DATA_DIR, "prioritized_verify_report.json")
CANDIDATES_PATH = os.path.join(DATA_DIR, "prioritized_verify_candidates.json")

PRIORITY_COMPANIES = {"tcs": 100, "infosys": 100, "wipro": 100,
                      "amazon": 50, "google": 50, "meta": 50, "microsoft": 50}


def main(limit=None):
    question_store.load_all()

    # Pattern demand = frequency across the currently servable bank.
    pattern_demand = Counter()
    for q in question_store._questions:
        if question_store._is_servable(q):
            pattern_demand[str(q.get("pattern") or "Arrays")] += 1

    queue = []
    for q in question_store._questions:
        status = str(q.get("trust_status", "")).lower()
        if status not in ("unverified", "needs_review"):
            continue
        if not _is_executable(q):
            continue
        pattern = str(q.get("pattern") or "Arrays")
        score = pattern_demand.get(pattern, 0)
        companies = [str(c).lower() for c in (q.get("companies") or [])]
        for c in companies:
            score += PRIORITY_COMPANIES.get(c, 0)
        queue.append({
            "id": q.get("id"),
            "pattern": pattern,
            "companies": q.get("companies") or [],
            "type": q.get("type"),
            "score": score,
        })
    queue.sort(key=lambda e: (-e["score"], str(e["id"])))
    if limit:
        queue = queue[:limit]

    with open(QUEUE_PATH, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=1)

    # Verify in priority order (isolated process; server untouched).
    by_id = {str(q.get("id")): q for q in question_store._questions}
    passed, failed, quarantined = 0, 0, 0
    candidates = []
    details = []
    for entry in queue:
        q = by_id.get(str(entry["id"]))
        if not q:
            continue
        import copy
        probe = copy.deepcopy(q)
        try:
            r = verify_question(probe)
        except Exception as e:
            r = {"id": entry["id"], "verdict": "quarantined",
                 "reason": "verify_exception:%s" % type(e).__name__}
        if r["verdict"] == "passed":
            passed += 1
            candidates.append({
                "id": entry["id"],
                "pattern": entry["pattern"],
                "companies": entry["companies"],
                "type": entry["type"],
                "verify_reason": r.get("reason"),
                "provenance": "deterministic_auto_verify_pass",
                "note": "candidate only — requires human review via tranche-approve",
            })
        elif r["verdict"] == "failed":
            failed += 1
            details.append({"id": entry["id"], "verdict": "failed", "reason": r.get("reason")})
        else:
            quarantined += 1
            details.append({"id": entry["id"], "verdict": "quarantined", "reason": r.get("reason")})

    report = {
        "queued": len(queue),
        "passed_automated_checked_candidates": passed,
        "failed": failed,
        "quarantined": quarantined,
        "top_queue_sample": queue[:20],
        "failure_sample": details[:30],
        "rule": "zero LLM; candidates need human tranche-approve; source banks untouched",
    }
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=1)
    with open(CANDIDATES_PATH, "w", encoding="utf-8") as f:
        json.dump(candidates, f, indent=1)
    print(json.dumps({k: v for k, v in report.items()
                      if k in ("queued", "passed_automated_checked_candidates",
                               "failed", "quarantined", "rule")}, indent=1))
    print("top 10 queue:")
    for e in queue[:10]:
        print("  score=%d id=%s pattern=%s companies=%s" % (
            e["score"], e["id"], e["pattern"], ",".join(e["companies"][:3])))


if __name__ == "__main__":
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    main(lim)
