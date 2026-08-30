import json, sys
sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Check coding questions
coding = [q for q in data if q.get("type") == "coding"]
print(f"Coding questions: {len(coding)}")

# Check correct_answer format
good = 0
bad = 0
for q in coding[:20]:
    ca = q.get("correct_answer")
    # Check if it looks reasonable
    if ca is None:
        bad += 1
        print(f"  MISSING: {q.get('id', '')[:8]}")
    elif isinstance(ca, list):
        if len(ca) >= 1:
            good += 1
        else:
            bad += 1
            print(f"  EMPTY LIST: {q.get('id', '')[:8]}")
    elif isinstance(ca, str):
        if ca.strip():
            good += 1
        else:
            bad += 1
            print(f"  EMPTY STR: {q.get('id', '')[:8]}")
    else:
        bad += 1
        print(f"  OTHER: {q.get('id', '')[:8]} = {ca}")

print(f"\nGood: {good}, Bad: {bad} out of {len(coding)}")