import json, sys
sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

coding = [q for q in data if q.get("type") == "coding"]

# Get a with_answer question and try to execute its solution
with_answer = [q for q in coding if q.get("correct_answer") is not None][0]
print("=== Question WITH answer ===")
print(f"id: {with_answer.get('id')[:8]}")
print(f"prompt: {with_answer.get('prompt', '')[:200]}...")
print(f"solution code preview: {with_answer.get('solution', {}).get('python', '')[:200]}...")
print(f"correct_answer: {with_answer.get('correct_answer')}")
print(f"explanation: {with_answer.get('explanation')[:200]}")
print()

# Try to execute the code
code = with_answer.get("solution", {}).get("python", "")
print(f"Executing code...")
try:
    local_vars = {}
    exec(code, {}, local_vars)
    print(f"Execution succeeded")
    # Check what functions/vars are defined
    print(f"Defined names: {[k for k in local_vars.keys() if not k.startswith('__')]}")
except Exception as e:
    print(f"Execution failed: {e}")

# Also check if there are test_cases or other execution info
print(f"\nFull solution: {json.dumps(with_answer.get('solution', {}), indent=2)[:500]}")
print(f"Full question keys: {list(with_answer.keys())}")