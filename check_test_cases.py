import json, sys
sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

coding = [q for q in data if q.get("type") == "coding"]

# Find questions with test_cases (underscore)
with_test_cases = [q for q in coding if q.get("test_cases")]
print(f"Questions with test_cases (underscore): {len(with_test_cases)}")

# Sample a few
for q in with_test_cases[:5]:
    print(f"\nID: {q.get('id')[:8]}")
    print(f"  test_cases: {q.get('test_cases')[:2] if q.get('test_cases') else 'None'}")
    print(f"  correct_answer: {q.get('correct_answer')}")
    print(f"  title: {q.get('title', '')[:80]}")
    print(f"  description: {q.get('description', '')[:80]}")
    print(f"  solution: {q.get('solution', '')[:100]}")