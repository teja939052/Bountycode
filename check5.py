import json, sys
sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

coding = [q for q in data if q.get("type") == "coding"]

# Get a without_answer question
without_answer = [q for q in coding if q.get("correct_answer") is None][0]
print("=== Question WITHOUT answer ===")
print(f"id: {without_answer.get('id')[:8]}")
print(f"prompt: {without_answer.get('prompt', '')[:200]}...")
print(f"solution code: {without_answer.get('solution', {}).get('python', '')[:300]}...")
print(f"explanation: {without_answer.get('explanation')}")
print(f"Keys: {list(without_answer.keys())}")
print()

# Check if there are hidden test cases or visible tests
print(f"has 'test_cases' key: {'test_cases' in without_answer}")
print(f"has 'visible_tests' key: {'visible_tests' in without_answer}")
print(f"has 'hidden_tests' key: {'hidden_tests' in without_answer}")
print(f"has 'inputs' key: {'inputs' in without_answer}")
print(f"has 'outputs' key: {'outputs' in without_answer}")
print(f"has 'expected_output' key: {'expected_output' in without_answer}")
print()

# Check other possible fields
for key in without_answer.keys():
    if 'test' in key.lower() or 'case' in key.lower() or 'input' in key.lower() or 'output' in key.lower():
        print(f"Found key: {key} = {without_answer[key]}")