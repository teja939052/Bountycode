import json, sys
sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

coding = [q for q in data if q.get("type") == "coding"]

# Print first 5 IDs and their correct_answer
for i, q in enumerate(coding[:5]):
    print(f"{i}: id={q.get('id')[:8]}, correct_answer={q.get('correct_answer')}")

# Check how many have correct_answer now
with_ans = sum(1 for q in coding if q.get("correct_answer") is not None)
print(f"\nTotal with correct_answer: {with_ans}/6279")