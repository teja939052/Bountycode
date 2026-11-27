import json
bank_path = r"D:\Project-Fremen\backend\app\data\questions_bank_deduplicated.json"
with open(bank_path, encoding='utf-8') as f:
    bank = json.load(f)

verified = [q for q in bank if q.get('trust_status') == 'verified']
auto = [q for q in bank if q.get('trust_status') == 'automated_checked']
needs = [q for q in bank if q.get('trust_status') == 'needs_review']
unverified = [q for q in bank if q.get('trust_status') == 'unverified']

print(f"Total: {len(bank)}")
print(f"Verified: {len(verified)} ({len(verified)/len(bank)*100:.1f}%)")
print(f"Automated: {len(auto)} ({len(auto)/len(bank)*100:.1f}%)")
print(f"Needs review: {len(needs)} ({len(needs)/len(bank)*100:.1f}%)")
print(f"Unverified: {len(unverified)} ({len(unverified)/len(bank)*100:.1f}%)")

# Check a few questions have proper structure
if verified:
    v = verified[0]
    print(f"\nSample verified question structure:")
    print(f"  ID: {v.get('id')}")
    print(f"  Type: {v.get('type')}")
    print(f"  Difficulty: {v.get('difficulty')}")
    print(f"  Topic: {v.get('topic')}")
    print(f"  Companies: {v.get('companies', [])[:3]}")
    print(f"  Section: {v.get('primary_section')}")
    print(f"  Category: {v.get('section_category')}")