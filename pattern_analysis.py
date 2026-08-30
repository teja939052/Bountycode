import json, sys
sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

coding = [q for q in data if q.get("type") == "coding"]

# Group questions by solution code pattern - first 200
sample = coding[:200]

patterns = {}
for q in sample:
    solution = q.get("solution", {})
    code = ""
    if isinstance(solution, dict):
        code = solution.get("code", "") or solution.get("python", "")
    elif isinstance(solution, str):
        code = solution
    
    if not code:
        continue
    
    # Get first line/function name
    if "def solution" in code or code.strip().startswith("def solution"):
        pattern = "solution_func"
    elif "def max" in code or "def min" in code or "def find" in code:
        pattern = "extreme_func"
    elif "def binary" in code:
        pattern = "binary_func"
    elif "def reverse" in code:
        pattern = "reverse_func"
    elif "def sort" in code:
        pattern = "sort_func"
    elif "def fib" in code:
        pattern = "fib_func"
    elif "def dfs" in code.lower() or "def bfs" in code.lower():
        pattern = "graph_traversal"
    elif "def dp" in code.lower() or "def memo" in code.lower():
        pattern = "dp"
    else:
        pattern = "other"
    
    # Get test case count
    tc_count = len(q.get("testcases", []))
    
    key = f"{pattern}_{tc_count}tc"
    if key not in patterns:
        patterns[key] = {"count": 0, "samples": []}
    patterns[key]["count"] += 1
    if len(patterns[key]["samples"]) < 3:
        tc = q.get("testcases", [{}])[0] if q.get("testcases") else {}
        patterns[key]["samples"].append({
            "id": q.get("id", "")[:8],
            "expected": tc.get("expected", "") if tc else "none",
            "correct_answer": str(q.get("correct_answer", ""))[:30] if q.get("correct_answer") else "None"
        })

print("Question patterns (first 200 questions):")
for k, v in sorted(patterns.items(), key=lambda x: -x[1]["count"]):
    print(f"  {k}: {v['count']} questions")
    for s in v["samples"][:2]:
        print(f"    {s['id']}: expected={s['expected']}, answer={s['correct_answer']}")