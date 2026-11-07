"""Repair Queue + Content Trust report.

Scans the served bank (questions_bank.json) and classifies each non-verified
question by why it can't be promoted to TRUSTED yet, then ranks the repair
queue by:

    placement relevance + foundational importance
    + frequency + student demand + repairability

Also emits a Content Trust baseline report (existing-infrastructure view of
how much student-facing content is verified vs not).

Outputs (data artifacts, not new systems):
    app/data/repair_queue.json     ordered list of {id, reason, priority}
    question_content_trust_report.json
"""
import json
import os
import re
from collections import Counter

ROOT = r"D:\Project-Fremen\backend\app\data"
BANK = os.path.join(ROOT, "questions_bank.json")
VERIFIED = os.path.join(ROOT, "verified_placement_questions.json")

# Tier-1 placement focus (user's P0 order)
TIER1 = {"tcs", "nqt", "infosys", "accenture", "wipro", "cognizant", "capgemini",
         "tcs nqt", "infosys", "wipro", "cognizant", "capgemini", "amazon", "google",
         "microsoft", "meta", "flipkart", "paytm", "swiggy", "zoho", "oracle"}

# Foundational topics = high leverage to fix
FOUNDATIONAL = {"arrays", "strings", "hashmap", "hashing", "linked list",
                "stack", "queue", "binary search", "two pointers", "sorting",
                "math", "tree", "dynamic programming", "recursion"}

FREQUENCY_KEYS = ("frequency", "attempts", "solved_count", "upvotes")


def priority_score(q):
    """0..1 overall repairability priority."""
    company_tags = {c.lower() for c in (q.get("companies") or [])}
    topic = str(q.get("topic") or "").lower()
    has_tier1 = bool(company_tags & TIER1)
    has_foundational = topic in FOUNDATIONAL or any(t.lower() in FOUNDATIONAL for t in (q.get("pattern") or "").lower().split())

    freq = 0
    for k in FREQUENCY_KEYS:
        try:
            freq = max(freq, float(q.get(k) or 0))
        except (TypeError, ValueError):
            pass
    sc = 0.0
    sc += 0.35 if has_tier1 else 0.0
    sc += 0.25 if has_foundational else 0.0
    sc += min(0.25, freq / 100 * 0.25)
    sc += 0.15 if len(q.get("testcases") or []) > 0 else 0.0   # more repairable
    return sc


def classify_reason(q):
    sol = q.get("solution")
    sol_code = ""
    if isinstance(sol, dict):
        sol_code = sol.get("code") or ""
    elif isinstance(sol, str):
        sol_code = sol
    code = sol_code.strip()
    if not code or len(code) < 20:
        return "SOLUTION_MISSING"
    low = code.lower()
    if "implement optimal solution here" in low or "your code here" in low or "todo" in low or "pass  #" in low:
        return "TEMPLATE_SHELL"
    if not q.get("testcases"):
        return "TEST_CASE_MISSING"
    return "UNVERIFIED_EXPECTED_OUTPUT"


def main():
    with open(BANK, "r", encoding="utf-8") as f:
        bank = json.load(f)

    with open(VERIFIED, "r", encoding="utf-8") as f:
        verified = json.load(f)
    verified_ids = {q.get("id") for q in verified}

    repair = []
    reason_counter = Counter()
    type_counter = Counter()
    company_counter = Counter()

    for q in bank:
        qid = q.get("id", "")
        if qid in verified_ids:
            continue
        if q.get("trust_status") == "verified":
            continue
        reason = classify_reason(q)
        reason_counter[reason] += 1
        type_counter[q.get("type", "unknown")] += 1
        for c in (q.get("companies") or []):
            if c:
                company_counter[str(c).lower()] += 1
        score = priority_score(q)
        repair.append({
            "id": qid,
            "type": q.get("type", "unknown"),
            "topic": q.get("topic", ""),
            "company": list({c for c in (q.get("companies") or [])}),
            "repair_reason": reason,
            "priority": round(score, 3),
        })

    repair.sort(key=lambda r: (-r["priority"], r["type"]))

    with open(os.path.join(ROOT, "repair_queue.json"), "w", encoding="utf-8") as f:
        json.dump(repair, f, indent=2)

    tier1_pending = [r for r in repair if r["priority"] >= 0.35]
    report = {
        "bank_total": len(bank),
        "verified": len(verified_ids),
        "verified_ids": sorted(verified_ids),
        "unverified_pending": len(repair),
        "repair_reasons": dict(reason_counter),
        "type_distribution": dict(type_counter),
        "tier1_pending_repair": len(tier1_pending),
        "top_companies_flagged": dict(company_counter.most_common(15)),
        "next_targets_11_50": tier1_pending[:50],
    }
    with open(os.path.join(ROOT, "question_content_trust_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"Bank total: {len(bank)}")
    print(f"Verified: {len(verified_ids)}  |  Unverified pending: {len(repair)}")
    print("Repair reasons:", dict(reason_counter))
    print("Tier-1 priority pending (>=0.35):", len(tier1_pending))
    print("\nTop 15 next repair candidates by priority:")
    for r in tier1_pending[:15]:
        print(f"  {r['priority']:.2f}  {r['id']}  [{r['type']}] {r['topic']} {r['repair_reason']}")


if __name__ == "__main__":
    main()