"""Quarantine mismatched/non-standard MCQ questions in india_placement_depth.json."""
import json
import sys

BANK_PATH = "app/data/india_placement_depth.json"

def quarantine_mismatches():
    with open(BANK_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if not isinstance(data, list):
        print(f"Expected list in {BANK_PATH}, got {type(data)}")
        return
    
    quarantined = 0
    for q in data:
        if not isinstance(q, dict):
            continue
        t = str(q.get("type", "")).lower()
        if t not in ("aptitude", "logical", "verbal", "hr", "cs_fundamentals"):
            continue
        
        # Get correct answer
        correct_raw = q.get("correct_answer") or q.get("correct_index")
        if correct_raw is None:
            continue
        
        # Determine if this is a standard MCQ (letter answer) or non-standard (value answer)
        opts = q.get("options", [])
        all_numbers = all(isinstance(o, (int, float)) for o in opts) if opts else False
        
        # For non-standard numeric-option questions, quarantine them
        if all_numbers and len(opts) == 4:
            q["trust_status"] = "needs_review"
            quarantined += 1
            continue
        
        # For standard questions, check if test_cases match correct_answer
        if isinstance(correct_raw, (int, float)):
            # correct_answer is a number, not a letter - non-standard
            q["trust_status"] = "needs_review"
            quarantined += 1
            continue
        
        correct = str(correct_raw).strip().upper()
        if correct not in ("A", "B", "C", "D"):
            q["trust_status"] = "needs_review"
            quarantined += 1
            continue
        
        tcs = q.get("testcases") or q.get("test_cases") or []
        for tc in tcs:
            if not isinstance(tc, dict):
                continue
            out = str(tc.get("output", "") or tc.get("expected", "") or "").strip().upper()
            if out and out != correct:
                q["trust_status"] = "needs_review"
                quarantined += 1
                break
    
    with open(BANK_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Quarantined {quarantined} questions in {BANK_PATH}")

if __name__ == "__main__":
    quarantine_mismatches()
