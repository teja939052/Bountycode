import json
import sys

sys.path.insert(0, ".")
import app.services.question_store as qs
qs.load_all()

mismatch_ids = []
for q in qs._questions:
    t = str(q.get("type", "")).lower()
    if t not in ("aptitude", "logical", "verbal", "hr", "cs_fundamentals", "behavioral"):
        continue
    correct_raw = q.get("correct_answer") or q.get("correct_index")
    if correct_raw is None:
        continue
    if isinstance(correct_raw, (int, float)):
        correct = chr(65 + int(correct_raw))
    else:
        correct = str(correct_raw).strip().upper()
    if correct not in ("A", "B", "C", "D"):
        continue
    tcs = q.get("test_cases") or q.get("testcases") or []
    for tc in tcs:
        out = str(tc.get("output", "") or tc.get("expected", "") or "").strip().upper()
        if out and out != correct:
            mismatch_ids.append(q.get("id"))
            break

QUARANTINE_PATH = "app/data/served_quarantine.json"
with open(QUARANTINE_PATH, "r", encoding="utf-8") as f:
    existing = json.load(f)

existing_ids = {str(r.get("id")) for r in existing if isinstance(r, dict)}
added = 0
for qid in mismatch_ids:
    if qid not in existing_ids:
        existing.append({
            "id": qid,
            "title": f"MCQ mismatch quarantine: {qid}",
            "reason": "MCQ test_case output does not match correct_answer letter",
            "passed": 0,
            "total": 0,
        })
        added += 1

with open(QUARANTINE_PATH, "w", encoding="utf-8") as f:
    json.dump(existing, f, indent=2, ensure_ascii=False)

print(f"Added {added} new entries to served_quarantine.json")
print(f"Total quarantine entries: {len(existing)}")
