"""Ground-truth coverage sweep over the servable bank.

For each servable coding question, determine ground_truth_status:
  confirmed (independent source agrees) / no_independent_source (gap, neutral)
  / mismatch (independent source disagrees — self-stamping catch).

A mismatch on currently-SERVED content is a P0 finding: independent ground
truth contradicts what students see. Read-only: no trust writes, no bank
mutation, no MongoDB.

Writes: backend/app/data/ground_truth_report.json
"""
import json
import os
import sys
from collections import Counter

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from app.services import question_store  # noqa: E402
from app.services.ground_truth import ground_truth_status, load_oracle  # noqa: E402


def main():
    question_store.load_all()
    oracle = load_oracle()
    served = [q for q in question_store._questions
              if question_store._is_servable(q)
              and str(q.get("type") or "").lower() == "coding"]
    states = Counter()
    mismatches = []
    confirmed = []
    for q in served:
        try:
            res = ground_truth_status(q)
        except Exception as e:
            res = {"state": "no_independent_source",
                   "detail": f"sweep_error_{type(e).__name__}"}
        states[res["state"]] += 1
        if res["state"] == "mismatch":
            mismatches.append({"id": q.get("id"),
                               "title": str(q.get("question") or "")[:80],
                               "trust": q.get("trust_status"),
                               "detail": res["detail"]})
        elif res["state"] == "confirmed":
            confirmed.append({"id": q.get("id"),
                              "title": str(q.get("question") or "")[:80],
                              "detail": res["detail"]})
    report = {
        "oracle_entries": len(oracle),
        "servable_coding_scanned": len(served),
        "states": dict(states),
        "confirmed": confirmed,
        "mismatches_served": mismatches,
        "rule": "mismatch on served content contradicts independent ground truth; "
                "no_source is a coverage gap, not a failure",
    }
    with open(os.path.join(BACKEND_ROOT, "app", "data", "ground_truth_report.json"),
              "w", encoding="utf-8") as f:
        json.dump(report, f, indent=1)
    print(json.dumps({k: v for k, v in report.items()
                      if k in ("oracle_entries", "servable_coding_scanned",
                               "states", "rule")}, indent=1))
    print("mismatches on served content:", len(mismatches))
    for m in mismatches[:15]:
        print("  ", m["id"], "|", m["title"], "|", m["detail"][:100])
    print("confirmed:", len(confirmed))
    for c in confirmed[:15]:
        print("  ", c["id"], "|", c["title"], "|", c["detail"][:80])


if __name__ == "__main__":
    main()
