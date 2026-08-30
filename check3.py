import json, sys
sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

coding = [q for q in data if q.get("type") == "coding"]

# Compare a question with answer vs without
with_answer = [q for q in coding if q.get("correct_answer") is not None][0]
without_answer = [q for q in coding if q.get("correct_answer") is None][0]

print("=== Question WITH correct_answer ===")
print(f"id: {with_answer.get('id')[:8]}")
print(f"prompt: {with_answer.get('prompt', '')[:100]}...")
print(f"solution: {bool(with_answer.get('solution'))}")
print(f"explanation: {bool(with_answer.get('explanation'))}")
print(f"has test_cases: {'test_cases' in with_answer}")
print(f"time_complexity: {with_answer.get('time_complexity')}")
print(f"space_complexity: {with_answer.get('space_complexity')}")
print(f"options: {with_answer.get('options')}")
print()

print("=== Question WITHOUT correct_answer ===")
print(f"id: {without_answer.get('id')[:8]}")
print(f"prompt: {without_answer.get('prompt', '')[:100]}...")
print(f"solution: {bool(without_answer.get('solution'))}")
print(f"explanation: {bool(without_answer.get('explanation'))}")
print(f"has test_cases: {'test_cases' in without_answer}")
print(f"time_complexity: {without_answer.get('time_complexity')}")
print(f"space_complexity: {without_answer.get('space_complexity')}")
print(f"options: {without_answer.get('options')}")