import json, os
bank_path = r"D:\Project-Fremen\backend\app\data\questions_bank.json"
with open(bank_path) as f:
    bank = json.load(f)
verified = [q for q in bank if q.get('trust_status') == 'verified']
automated = [q for q in bank if q.get('trust_status') == 'automated_checked']
needs_review = [q for q in bank if q.get('trust_status') == 'needs_review']
quarantined = [q for q in bank if q.get('trust_status') == 'quarantined']
unverified = [q for q in bank if q.get('trust_status') == 'unverified']
print(f'Total questions: {len(bank)}')
print(f'Verified: {len(verified)}')
print(f'Automated checked: {len(automated)}')
print(f'Needs review: {len(needs_review)}')
print(f'Quarantined: {len(quarantined)}')
print(f'Unverified: {len(unverified)}')
print()
if verified:
    print(f'Example verified question: {verified[0]["id"]}')
    print(f'  Type: {verified[0].get("type")}')
    print(f'  Companies: {verified[0].get("companies", [])[:3]}')