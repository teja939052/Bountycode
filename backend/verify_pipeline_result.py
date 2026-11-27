import json, os

bank_path = r"D:\Project-Fremen\backend\app\data\questions_bank_pipeline.json"
with open(bank_path, encoding='utf-8') as f:
    bank = json.load(f)

verified = [q for q in bank if q.get('trust_status') == 'verified']
auto = [q for q in bank if q.get('trust_status') == 'automated_checked']
needs = [q for q in bank if q.get('trust_status') == 'needs_review']
quar = [q for q in bank if q.get('trust_status') == 'quarantined']
review = [q for q in bank if q.get('trust_status') == 'reviewed']
unver = [q for q in bank if q.get('trust_status') == 'unverified']

print(f"Total questions: {len(bank)}")
print(f"\nTrust Status Distribution:")
print(f"  verified:   {len(verified):5d} ({len(verified)/len(bank)*100:5.1f}%) - hand-crafted + reviewed")
print(f"  automated:  {len(auto):5d} ({len(auto)/len(bank)*100:5.1f}%) - auto-checked with test cases")
print(f"  needs_review: {len(needs):5d} ({len(needs)/len(bank)*100:5.1f}%) - missing fields, human review required")
print(f"  reviewed:   {len(review):5d} ({len(review)/len(bank)*100:5.1f}%) - reviewed but not fully verified")
print(f"  quarantined:{len(quar):5d} ({len(quar)/len(bank)*100:5.1f}%) - execution-broken")
print(f"  unverified: {len(unver):5d} ({len(unver)/len(bank)*100:5.1f}%) - no trust metadata")
print(f"\n(Note: totals add up to {len(verified)+len(auto)+len(needs)+len(quar)+len(review)+len(unver)})")

# Check verified questions have proper structure
if verified:
    v = verified[0]
    print(f"\nSample verified question structure:")
    print(f"  ID: {v.get('id')}")
    print(f"  Type: {v.get('type')}")
    print(f"  Difficulty: {v.get('difficulty')}")
    print(f"  Topic: {v.get('topic')}")
    print(f"  Section: {v.get('primary_section')}")
    print(f"  Category: {v.get('section_category')}")
    print(f"  Companies: {v.get('companies', [])[:3]}")
    print(f"  Has hidden_testcases: {bool(v.get('hidden_testcases'))}")
    print(f"  Has solution: {bool(v.get('solution'))}")
    print(f"  Quality score: {v.get('quality_score', 'N/A')}")
    print(f"  Quality tier: {v.get('quality_tier', 'N/A')}")
    print(f"  Canonical skill ID: {v.get('canonical_skill_id', 'N/A')}")

# Check needs_review questions
if needs:
    n = needs[0]
    print(f"\nSample needs_review question structure:")
    print(f"  ID: {n.get('id')}")
    print(f"  Type: {n.get('type')}")
    print(f"  Missing fields: {n.get('quality_missing', [])[:3] if n.get('quality_missing') else 'N/A'}")

# Check quarantined questions
if quar:
    print(f"\nQuarantined questions are execution-broken (will not be served)")