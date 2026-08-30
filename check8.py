import json, sys
sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

coding = [q for q in data if q.get("type") == "coding"]

# Check questions with error answers
error_count = 0
valid_count = 0
for q in coding:
    ca = q.get("correct_answer")
    if ca and isinstance(ca, str) and ca.startswith("RUN_ERROR:"):
        error_count += 1
    elif ca and isinstance(ca, str) and not ca.startswith("RUN_ERROR:"):
        valid_count += 1

print(f"Questions with error answers: {error_count}")
print(f"Questions with valid answers: {valid_count}")
print(f"Total coding: {len(coding)}")
print(f"With None answer: {sum(1 for q in coding if q.get('correct_answer') is None)}")