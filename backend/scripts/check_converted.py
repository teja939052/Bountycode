import sys
sys.path.insert(0, ".")
import json

with open("app/data/questions_bank.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Find questions that were originally 'main' (now 'unverified')
main_qs = [q for q in questions if str(q.get("trust_status", "")).lower() == "unverified"]
print(f"Total unverified questions: {len(main_qs)}")

# Check a sample
for q in main_qs[:5]:
    qid = q.get("id")
    qtype = q.get("type")
    has_opts = bool(q.get("options"))
    has_tcs = bool(q.get("test_cases"))
    correct = q.get("correct_answer")
    print(f"  {qid}: type={qtype}, has_options={has_opts}, has_test_cases={has_tcs}, correct_answer={correct!r}")
