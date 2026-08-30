import json, sys, os, re
sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

coding = [q for q in data if q.get("type") == "coding"]

fixed = 0
failed = 0
for i, q in enumerate(coding[:20]):
    try:
        solution = q.get("solution", {})
        code = solution.get("python", "") if solution else ""
        
        if not code:
            failed += 1
            continue
        
        local_vars = {}
        try:
            exec(code, {}, local_vars)
            runs_ok = True
        except Exception as e:
            runs_ok = False
            
        if runs_ok:
            fixed += 1
            print(f"Fixed Q{i}: {q.get('id', '')[:8]}")
        else:
            failed += 1
            print(f"Failed Q{i}: {q.get('id', '')[:8]}")
    except:
        failed += 1
        print(f"Error Q{i}")

print(f"\nFixed {fixed}/20 coding questions")