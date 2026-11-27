import json, os

bank_path = r"D:\Project-Fremen\backend\app\data\questions_bank_deduplicated.json"
with open(bank_path, encoding='utf-8') as f:
    bank = json.load(f)

verified = [q for q in bank if q.get('trust_status') == 'verified']
auto = [q for q in bank if q.get('trust_status') == 'automated_checked']
needs = [q for q in bank if q.get('trust_status') == 'needs_review']

print(f"Verified sample - has hidden_testcases: {bool(verified[0].get('hidden_testcases')) if verified else 'N/A'}")
print(f"Verified sample - has solution: {bool(verified[0].get('solution')) if verified else 'N/A'}")
print(f"Verified sample - has correct_answer: {verified[0].get('correct_answer') if verified else 'N/A'}")
print(f"Auto sample - has hidden_testcases: {bool(auto[0].get('hidden_testcases')) if auto else 'N/A'}")
print(f"Needs sample - has hidden_testcases: {bool(needs[0].get('hidden_testcases')) if needs else 'N/A'}")