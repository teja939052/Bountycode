import json, sys, inspect
from collections import defaultdict
sys.path.insert(0, r"D:\Project-Fremen\backend")

path = r"D:\Project-Fremen\backend\app\data\questions_bank.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total in questions_bank.json: {len(data)}")

# Type distribution
by_type = defaultdict(int)
for q in data:
    by_type[q.get("type", "unknown")] += 1
print("By type:", dict(by_type))

# Check structure of first question
q = data[0]
print("\nFirst question keys:", list(q.keys()))
print("First question id:", q.get("id", "")[:20])

# Count how many have solutions with code, testcases, options
has_code = 0
has_testcases = 0
has_options = 0
has_correct_answer = 0
for q in data:
    sol = q.get("solution")
    if isinstance(sol, dict) and sol.get("code"):
        has_code += 1
    elif isinstance(sol, str) and sol.strip():
        has_code += 1
    if q.get("testcases"):
        has_testcases += 1
    if q.get("options"):
        has_options += 1
    if q.get("correct_answer") is not None:
        has_correct_answer += 1

print(f"\nHas solution code: {has_code}")
print(f"Has testcases: {has_testcases}")
print(f"Has options: {has_options}")
print(f"Has correct_answer: {has_correct_answer}")

# Company distribution
companies = defaultdict(int)
for q in data:
    for c in (q.get("companies") or []):
        companies[c.lower()] += 1
print("\nTop companies:", dict(sorted(companies.items(), key=lambda x: -x[1])[:10]))
