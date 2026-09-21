"""Apply content trust fixes and audit the result.

Run from backend/:
  python scripts/apply_and_audit.py

This applies:
  1. Invalidates 194 stale MCQ stamps → needs_review
  2. Quarantines 829 SQL without test_cases → quarantined
  3. Quarantines 103 verified-not-executable → quarantined

Then outputs the final trust audit table.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services import question_store

# Apply fixes first
question_store.load_all()
stale = question_store.fix_stale_mcq_stamps()
sql_fix = question_store.fix_sql_no_test_cases()
exec_fix = question_store.fix_verified_not_executable()
question_store._dedupe_and_filter(question_store._questions)

print(f"FIXES APPLIED:")
print(f"  Stale MCQ stamps invalidated: {stale}")
print(f"  SQL quarantined (no test_cases): {sql_fix}")
print(f"  Verified-not-executable quarantined: {exec_fix}")
print()

# Now audit
_questions = question_store._questions
_is_executable = question_store._is_executable
_is_servable = question_store._is_servable

# Count by type
by_type = {}
for q in _questions:
    t = q.get("type", "unknown")
    if t not in by_type:
        by_type[t] = {"total": 0, "executable": 0, "servable": 0, "quarantined": 0,
                      "verified": 0, "reviewed": 0, "automated_checked": 0, "needs_review": 0, "unverified": 0}
    by_type[t]["total"] += 1
    if _is_executable(q):
        by_type[t]["executable"] += 1
    if _is_servable(q):
        by_type[t]["servable"] += 1
    status = q.get("trust_status", "unverified")
    if status in by_type[t]:
        by_type[t][status] += 1
    if status == "quarantined":
        by_type[t]["quarantined"] += 1

print("=" * 90)
print("FINAL QUESTION BANK TRUST AUDIT (POST-FIX)")
print("=" * 90)
print(f"{'Type':<20} {'Total':>7} {'Exec':>7} {'Servable':>8} {'Verified':>9} {'Reviewed':>9} {'Auto':>7} {'NeedsRev':>9} {'Unverified':>11} {'Quar':>7}")
print("-" * 90)

totals = {"total": 0, "executable": 0, "servable": 0, "quarantined": 0}
for t in sorted(by_type.keys()):
    d = by_type[t]
    print(f"{t:<20} {d['total']:>7} {d['executable']:>7} {d['servable']:>8} {d['verified']:>9} {d['reviewed']:>9} {d['automated_checked']:>7} {d['needs_review']:>9} {d['unverified']:>11} {d['quarantined']:>7}")
    for k in totals:
        totals[k] += d[k]
print("-" * 90)
print(f"{'TOTAL':<20} {totals['total']:>7} {totals['executable']:>7} {totals['servable']:>8}")
print()

# Summary
print("SUMMARY:")
print(f"  Total questions: {totals['total']}")
print(f"  Executable: {totals['executable']}")
print(f"  Servable (trust + executable): {totals['servable']}")
print(f"  Quarantined: {totals['quarantined']}")
print(f"  Not servable (untrusted or not executable): {totals['total'] - totals['servable']}")
