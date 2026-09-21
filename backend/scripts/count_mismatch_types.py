import json

with open("app/data/india_placement_depth.json", "r", encoding="utf-8") as f:
    data = json.load(f)

mismatch_count = 0
standard_mismatches = 0
non_standard_mismatches = 0

for q in data:
    t = str(q.get("type", "")).lower()
    if t not in ("aptitude", "logical", "verbal", "hr", "cs_fundamentals"):
        continue
    
    opts = q.get("options", [])
    if not opts:
        continue
    
    all_numbers = all(isinstance(o, (int, float)) for o in opts)
    all_strings = all(isinstance(o, str) for o in opts)
    
    correct_raw = q.get("correct_answer") or q.get("correct_index")
    if correct_raw is None:
        continue
    
    tcs = q.get("test_cases") or q.get("testcases") or []
    for tc in tcs:
        out = str(tc.get("output", "") or tc.get("expected", "") or "").strip().upper()
        
        correct = ""
        if isinstance(correct_raw, (int, float)):
            correct = chr(65 + int(correct_raw))
        else:
            correct = str(correct_raw).strip().upper()
        
        if out and out != correct:
            mismatch_count += 1
            if all_strings and len(opts) == 4:
                standard_mismatches += 1
            else:
                non_standard_mismatches += 1

print(f"Total mismatches: {mismatch_count}")
print(f"Standard MCQ mismatches: {standard_mismatches}")
print(f"Non-standard mismatches: {non_standard_mismatches}")
