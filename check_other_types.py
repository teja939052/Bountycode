import json, sys
sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Examine aptitude/logical/verbal quality in detail
for t in ["aptitude", "logical", "verbal", "hr"]:
    subset = [q for q in data if q.get("type") == t]
    print(f"\n=== {t.upper()} ({len(subset)} questions) ===")
    
    good = 0
    for q in subset[:5]:
        qid = q.get("id", "")[:12]
        question = str(q.get("question"))[:80] if q.get("question") else str(q.get("description", ""))[:80]
        ca = q.get("correct_answer")
        print(f"  {qid}:")
        print(f"    Q: {question}")
        print(f"    answer: {ca}")
        
        # Check if answer seems like a real answer
        ca_str = str(ca).strip().lower() if ca else ""
        if ca and ca_str not in ("none", "", "needs_authoring"):
            good += 1
        tcs = q.get("testcases", [])
        if tcs:
            print(f"    test case: {tcs[0]}")