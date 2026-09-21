import json

with open("app/data/india_placement_depth.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for q in data:
    t = str(q.get("type", "")).lower()
    if t not in ("aptitude", "logical", "verbal"):
        continue
    
    correct_raw = q.get("correct_answer") or q.get("correct_index")
    if correct_raw is None:
        continue
    
    tcs = q.get("testcases") or q.get("test_cases") or []
    for tc in tcs:
        out = str(tc.get("output", "") or tc.get("expected", "") or "").strip().upper()
        
        correct = ""
        if isinstance(correct_raw, (int, float)):
            correct = chr(65 + int(correct_raw))
        else:
            correct = str(correct_raw).strip().upper()
        
        if out and out != correct:
            print(f"MATCH: {q.get('id')} correct_raw={correct_raw!r} correct={correct!r} out={out!r}")
