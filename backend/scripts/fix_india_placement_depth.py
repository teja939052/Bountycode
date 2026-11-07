"""Fix MCQ mismatches in india_placement_depth.json."""
import sys
sys.path.insert(0, ".")
import json

BANK_PATH = "app/data/india_placement_depth.json"

def fix_mismatches():
    with open(BANK_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if not isinstance(data, list):
        print(f"Expected list in {BANK_PATH}, got {type(data)}")
        return
    
    fixed = 0
    for q in data:
        if not isinstance(q, dict):
            continue
        t = str(q.get("type", "")).lower()
        if t not in ("aptitude", "logical", "verbal", "hr", "cs_fundamentals"):
            continue
        
        # Handle both correct_answer (letter) and correct_index (0-based int)
        correct_raw = q.get("correct_answer") or q.get("correct_index")
        if correct_raw is None:
            continue
        
        # Convert to letter
        if isinstance(correct_raw, (int, float)):
            correct = chr(65 + int(correct_raw))  # 0->A, 1->B, etc.
        else:
            correct = str(correct_raw).strip().upper()
        
        if correct not in ("A", "B", "C", "D"):
            continue
        
        # Handle both test_cases and testcases
        tcs = q.get("test_cases") or q.get("testcases") or []
        if not tcs:
            q["test_cases"] = [{"input": None, "output": correct, "hidden": False}]
            fixed += 1
            continue
        
        for tc in tcs:
            if not isinstance(tc, dict):
                continue
            out = str(tc.get("output", "") or tc.get("expected", "") or "").strip().upper()
            if out and out != correct:
                tc["output"] = correct
                tc.pop("input", None)
                fixed += 1
    
    with open(BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Fixed {fixed} mismatches in {BANK_PATH}")

if __name__ == "__main__":
    fix_mismatches()
