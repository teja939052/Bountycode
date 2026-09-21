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
    print(f"Before verification: {qid}, status={q.get('trust_status')}")
    
    result = verify_question(q)
    print(f"After verification: {qid}, status={q.get('trust_status')}")
    print(f"Result verdict: {result.get('verdict')}")
    print(f"Result reason: {result.get('reason')}")
    print(f"Result passed: {result.get('passed')}/{result.get('total')}")
