"""Quarantine served questions that fail deterministic verification.

Companion to scripts/verify_backlog.py: that script triages the source bank
file and writes a report; this one acts on what the live store actually
serves, which is the set students can reach.

Mechanism (same proven path as quarantine_servable_stubs.py): append ids to
backend/app/data/served_quarantine.json, the file-seed layer that
question_store._apply_served_quarantine() flips to "quarantined" at load.
No source-bank mutation, no trust_status writes, no Mongo writes. Reversible
by removing the entries. Idempotent: skips ids already listed.

Only FAIL verdicts are quarantined. SKIP verdicts (no executable oracle,
stdin-style problems, unhandled types) are harness limits and are left alone.
"""
import json
import os
import sys

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from app.services import question_store  # noqa: E402
from scripts.verify_backlog import classify  # noqa: E402

SQ_PATH = os.path.join(BACKEND_ROOT, "app", "data", "served_quarantine.json")

# A FAIL with one of these heads means the harness could not judge the item,
# not that the content is wrong. Refuse to act so good content is never lost.
HARNESS_LIMITS = {
    "STDIN_STYLE",
    "NO_ORACLE",
    "UNHANDLED_TYPE",
    "NO_TESTS",
}


def collect():
    question_store.load_all()
    # find() returns every loaded record, including ones already flipped to
    # 'quarantined' by the file seed — needed so reconcile can re-judge its
    # own past decisions instead of restoring them blindly.
    allq = question_store.find().to_list()
    by_id = {str(q.get("id")): q for q in allq}
    servable = [q for q in allq if question_store._is_servable(q)]
    broken, skipped = [], {}
    for q in servable:
        verdict, reason = classify(q)
        head = reason.split(":")[0].split(" ")[0]
        if verdict == "FAIL":
            if head in HARNESS_LIMITS:
                skipped[reason] = skipped.get(reason, 0) + 1
                continue
            broken.append({
                "id": str(q.get("id")),
                "title": str(q.get("question") or q.get("title") or "")[:80],
                "reason": f"verify_backlog:{reason}"[:200],
                "passed": 0,
                "total": len(q.get("test_cases") or q.get("testcases")
                             or q.get("visible_test_cases") or []),
            })
        elif verdict == "SKIP":
            skipped[reason] = skipped.get(reason, 0) + 1
    return servable, broken, skipped, by_id


def main():
    servable, broken, skipped, by_id = collect()
    with open(SQ_PATH, encoding="utf-8") as f:
        existing = json.load(f)

    # Reconcile only entries this verifier created. Quarantine decisions made
    # by other mechanisms (intake_lint stubs, autocheck seeds) are left alone:
    # their reasons differ and they must not be revived by an execution check.
    broken_ids = {b["id"] for b in broken}
    kept = []
    restored = 0
    for row in existing:
        reason = str(row.get("reason", "")) if isinstance(row, dict) else ""
        qid = str(row.get("id")) if isinstance(row, dict) else ""
        if reason.startswith("verify_backlog:") and qid not in broken_ids:
            item = by_id.get(qid)
            verdict = classify(item)[0] if item else "FAIL"
            if verdict != "FAIL":
                restored += 1
                continue
        kept.append(row)

    have = {str(e.get("id")) for e in kept if isinstance(e, dict)}
    added = 0
    for row in broken:
        if row["id"] in have:
            continue
        kept.append(row)
        have.add(row["id"])
        added += 1

    with open(SQ_PATH, "w", encoding="utf-8") as f:
        json.dump(kept, f, indent=1)

    print(json.dumps({
        "servable_checked": len(servable),
        "broken_served_found": len(broken),
        "harness_limited_left_alone": sum(skipped.values()),
        "quarantine_entries_added": added,
        "quarantine_entries_restored_now_passing": restored,
        "quarantine_file_total": len(kept),
    }, indent=1))
    if skipped:
        print("left alone (harness limits):")
        for reason, n in sorted(skipped.items(), key=lambda kv: -kv[1]):
            print(f"  {reason:34s} {n}")


if __name__ == "__main__":
    main()
