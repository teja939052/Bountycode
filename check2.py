import json, sys
sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

coding = [q for q in data if q.get("type") == "coding"]

# Check first 5
for i, q in enumerate(coding[:5]):
    ca = q.get("correct_answer")
    qid = q.get("id", "")[:8]
    print(f"Q{i}: id={qid}, correct_answer type={type(ca).__name__}, value={ca}")

# Check if ALL have correct_answer but maybe as different format
has_key = sum(1 for q in coding if "correct_answer" in q)
print(f"\nAll have correct_answer key: {has_key}/{len(coding)}")

# Check formats
formats = {}
for q in coding:
    ca = q.get("correct_answer")
    if ca is None:
        fmt = "None"
    elif isinstance(ca, list):
        fmt = f"list({len(ca)} items)"
    elif isinstance(ca, str):
        fmt = f"str(len={len(ca)})"
    else:
        fmt = f"{type(ca).__name__}"
    formats[fmt] = formats.get(fmt, 0) + 1
print(f"Formats: {formats}")