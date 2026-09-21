"""Diagnostic script: audit question bank trust, executability, and servability.

Run from backend/:
  python scripts/audit_bank.py

Outputs a table of type | total | executable | servable | quarantined
and identifies broken SQL, stale MCQ stamps, MCQ mismatches.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Must import AFTER path setup to get the same module instance
from app.services import question_store

def main():
    question_store.load_all()
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

    print("\n" + "=" * 90)
    print("QUESTION BANK TRUST AUDIT")
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

    # SQL without test_cases or sql_schema
    sql_no_tc = [q for q in _questions if q.get("type") == "sql" and not (q.get("test_cases") or q.get("testcases"))]
    sql_no_schema = [q for q in _questions if q.get("type") == "sql" and not q.get("sql_schema")]
    sql_servable = [q for q in _questions if q.get("type") == "sql" and _is_servable(q)]
    print(f"SQL questions: total={sum(1 for q in _questions if q.get('type')=='sql')}")
    print(f"  without test_cases: {len(sql_no_tc)}")
    print(f"  without sql_schema: {len(sql_no_schema)}")
    print(f"  servable: {len(sql_servable)}")
    print()

    # MCQ verification stamps: questions with trust_status in (verified, automated_checked) 
    # that have MCQ format but might have stale stamps
    mcq_types = ("aptitude", "logical", "verbal", "hr", "cs_fundamentals", "cs")
    mcq_verified = [q for q in _questions if q.get("type") in mcq_types 
                    and q.get("trust_status") in ("verified", "automated_checked")]
    mcq_stale = []
    mcq_mismatches = []
    
    for q in mcq_verified:
        options = q.get("options") or {}
        correct = str(q.get("correct_answer") or q.get("correct_index") or "").strip().upper()
        
        # Check for stale: correct_answer not in A-D
        if correct not in ("A", "B", "C", "D"):
            mcq_stale.append(q)
            continue
        
        # Check for mismatch: test_case output != correct_answer
        tcs = q.get("test_cases") or q.get("testcases") or []
        for tc in tcs:
            tc_out = str(tc.get("output") or "").strip().upper()
            if tc_out and tc_out != correct:
                mcq_mismatches.append(q)
                break

    print(f"MCQ verified/automated_checked: {len(mcq_verified)}")
    print(f"  stale stamps (correct_answer not A-D): {len(mcq_stale)}")
    print(f"  mismatches (tc output != correct_answer): {len(mcq_mismatches)}")
    print()

    # Show first 5 stale stamps as examples
    if mcq_stale:
        print("STALE STAMPS (first 5):")
        for q in mcq_stale[:5]:
            print(f"  id={q.get('id')}, type={q.get('type')}, "
                  f"correct_answer={q.get('correct_answer')!r}, "
                  f"correct_index={q.get('correct_index')!r}, "
                  f"title={str(q.get('question',''))[:50]}")
        print()

    # Show first 5 mismatches as examples
    if mcq_mismatches:
        print("MCQ MISMATCHES (first 5):")
        for q in mcq_mismatches[:5]:
            tcs = q.get("test_cases") or q.get("testcases") or []
            tc_out = str(tcs[0].get("output", "")).strip().upper() if tcs else "?"
            print(f"  id={q.get('id')}, type={q.get('type')}, "
                  f"correct_answer={q.get('correct_answer')!r}, "
                  f"tc_output={tc_out!r}, "
                  f"title={str(q.get('question',''))[:50]}")
        print()

    # Questions that claim to be verified but fail _is_executable
    verified_not_exec = [q for q in _questions 
                         if q.get("trust_status") in ("verified", "automated_checked")
                         and not _is_executable(q)]
    print(f"Verified/automated_checked but NOT executable: {len(verified_not_exec)}")
    by_type_ne = {}
    for q in verified_not_exec:
        t = q.get("type", "unknown")
        by_type_ne[t] = by_type_ne.get(t, 0) + 1
    for t, c in sorted(by_type_ne.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")
    print()

    # Final servable count
    servable = [q for q in _questions if _is_servable(q)]
    print(f"FINAL SERVABLE COUNT: {len(servable)} / {len(_questions)}")

if __name__ == "__main__":
    main()
