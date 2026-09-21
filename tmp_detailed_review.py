import sys
sys.path.insert(0, 'backend')

import app.services.question_store as qs
qs._loaded = False
qs._questions = []
qs.load_all()
qs._unverified_loaded = False
qs._unverified_questions = []
qs.load_unverified()

# Detailed review of top Sliding Window candidates
target_ids = [
    "pp-fruit-into-baskets",
    "pp-max-consecutive-ones-iii",
    "tuf_0321",
    "tuf_0324",
    "tuf_0331",
    "tuf_0325",
    "tuf_0326",
    "tuf_0327",
]

for qid in target_ids:
    q = qs.find_one({"id": qid})
    if not q:
        continue
    print(f"\n=== {qid} ===")
    stmt = q.get("statement") or q.get("question", "")
    print(f"Title: {q.get('title')}")
    print(f"Statement: {stmt[:300]}")
    print(f"Difficulty: {q.get('difficulty')}")
    print(f"Pattern: {q.get('pattern')}")
    
    # Check testcases
    tc = q.get("testcases", [])
    print(f"Testcases: {len(tc)}")
    if tc:
        print(f"  Sample: {str(tc[0])[:200]}")
    
    # Check solution
    sol = q.get("solution", {})
    print(f"Solution keys: {list(sol.keys()) if isinstance(sol, dict) else type(sol)}")
    if isinstance(sol, dict):
        code = sol.get("code", "")
        print(f"Solution code length: {len(code)}")
        print(f"  First 200 chars: {code[:200]}")
    
    # Check examples
    ex = q.get("examples", [])
    print(f"Examples: {len(ex)}")
    
    # Check for red flags
    red_flags = []
    if "placeholder" in stmt.lower() or "todo" in stmt.lower() or "fill in" in stmt.lower():
        red_flags.append("Contains placeholder/todo/fill-in")
    if len(stmt) < 50:
        red_flags.append("Statement too short")
    if not tc:
        red_flags.append("No testcases")
    if not sol or (isinstance(sol, dict) and not sol.get("code")):
        red_flags.append("No solution code")
    
    if red_flags:
        print(f"RED FLAGS: {', '.join(red_flags)}")
    else:
        print("PASS: No obvious red flags")
