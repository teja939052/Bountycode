import json, sys, os
from collections import defaultdict

sys.path.insert(0, r"D:\Project-Fremen\backend")

# Read the bank
with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

total = len(data)

# Type distribution
by_type = {}
for q in data:
    t = q.get("type", "unknown")
    by_type[t] = by_type.get(t, 0) + 1

# Quality tiers
tier_counts = {}
for q in data:
    t = q.get("quality_tier", "B")
    tier_counts[t] = tier_counts.get(t, 0) + 1

# Companies
companies = defaultdict(int)
for q in data:
    for c in q.get("company", []):
        companies[c.lower()] += 1

# Topics
topics = defaultdict(int)
for q in data:
    t = q.get("topic", "")
    if t:
        topics[t.lower()] += 1

# Missing fields
missing = {"question": 0, "correct_answer": 0, "explanation": 0, "difficulty": 0}
for q in data:
    if not q.get("question"):
        missing["question"] += 1
    if not q.get("correct_answer"):
        missing["correct_answer"] += 1
    if not q.get("explanation"):
        missing["explanation"] += 1
    if not q.get("difficulty"):
        missing["difficulty"] += 1

print("=== QUESTION BANK QUALITY SUMMARY ===")
print(f"Total: {total}")
print(f"By type: {by_type}")
print(f"Quality tiers: {tier_counts}")
print(f"Top companies: {dict(sorted(companies.items(), key=lambda x: -x[1])[:10])}")
print(f"Top topics: {dict(sorted(topics.items(), key=lambda x: -x[1])[:15])}")

print(f"\nMissing key fields:")
print(f"  question: {missing['question']}")
print(f"  correct_answer: {missing['correct_answer']}")
print(f"  explanation: {missing['explanation']}")
print(f"  difficulty: {missing['difficulty']}")

# Save summary
report = {
    "total": total,
    "by_type": by_type,
    "quality_tiers": tier_counts,
    "missing_fields": missing,
    "top_companies": dict(sorted(companies.items(), key=lambda x: -x[1])[:10]),
    "top_topics": dict(sorted(topics.items(), key=lambda x: -x[1])[:15])
}

with open(r"D:\Project-Fremen\question_bank_summary.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f"\nSummary saved to question_bank_summary.json")
" 2>&1