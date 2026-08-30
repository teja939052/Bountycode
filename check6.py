import json, sys
sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

coding = [q for q in data if q.get("type") == "coding"]

# Check the fixed questions
target_ids = ['d8171e84', 'cf140b5b', '4521670e', '17ce29c1', '8f6408d9']
for q in coding:
    if q.get("id") in target_ids:
        print(f"Q: {q.get('id')[:8]}")
        print(f"  correct_answer: {q.get('correct_answer')}")
        tc = q.get("testcases", [])
        print(f"  testcases: {tc[:2] if tc else 'None'}")
        sc = q.get("solution", {})
        print(f"  solution code: {sc.get('code', '')[:100]}")
        print()