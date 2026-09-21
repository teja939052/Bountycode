import sys
sys.path.insert(0, ".")
import json
from app.services.auto_verify import verify_question

with open("app/data/questions_bank.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Find a 'main' status question (now 'unverified')
main_qs = [q for q in questions if str(q.get("trust_status", "")).lower() == "unverified"]
if main_qs:
    q = main_qs[0]
    qid = q.get("id")
    qtype = q.get("type")
    has_tcs = bool(q.get("test_cases"))
    has_sol = bool(q.get("solution"))
    print(f"Question: {qid}")
    print(f"Type: {qtype}")
    print(f"Has test_cases: {has_tcs}")
    print(f"Has solution: {has_sol}")
    
    result = verify_question(q)
    print(f"Verification result trust_status: {result.get('trust_status')}")
    print(f"Issues: {result.get('issues', [])}")
