import json, sys
sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

coding = [q for q in data if q.get("type") == "coding"]

# Check the 3400 skipped questions
skipped = [q for q in coding if q.get("correct_answer") is None]
print(f"Skipped questions: {len(skipped)}")

# What fields do they have?
sample = skipped[:5]
for q in sample:
    print(f"\nID: {q.get('id')[:8]}")
    print(f"  Keys: {list(q.keys())}")
    print(f"  type: {q.get('type')}")
    print(f"  has prompt/question: {bool(q.get('prompt')) or bool(q.get('question'))}")
    print(f"  has solution: {bool(q.get('solution'))}")
    print(f"  has testcases: {bool(q.get('testcases'))}")
    print(f"  has description: {bool(q.get('description'))}")
    print(f"  company: {q.get('company', [])}")
    print(f"  role: {q.get('role')}")
    print(f"  topic: {q.get('topic')}")
    print(f"  sub_topic: {q.get('sub_topic')}")
    print(f"  quality_tier: {q.get('quality_tier')}")
    print(f"  pedagogy: {bool(q.get('pedagogy'))}")