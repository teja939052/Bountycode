import json

with open('verified_placement_questions.json', 'r') as f:
    verified_data = json.load(f)

# Check which companies the verified questions are tagged with
from collections import Counter
company_counts = Counter()
for q in verified_data:
    for c in q.get('companies', []):
        company_counts[c] += 1

print('Company tags in verified bank:', dict(company_counts))

# Check TCS-tagged questions
tcs_verified = [q for q in verified_data if 'tcs' in [c.lower() for c in q.get('companies', [])]]
print(f'\nTCS-tagged verified questions: {len(tcs_verified)}')
for q in tcs_verified[:5]:
    print(f'  id={q.get("id")}, type={q.get("type")}, topic={q.get("topic")}')
    print(f'  title={q.get("title", "")[:70]}')

# Check non-TCS questions
non_tcs = [q for q in verified_data if 'tcs' not in [c.lower() for c in q.get('companies', [])]]
print(f'\nNon-TCS verified questions: {len(non_tcs)}')
for q in non_tcs[:5]:
    print(f'  id={q.get("id")}, type={q.get("type")}, topic={q.get("topic")}')
    print(f'  title={q.get("title", "")[:70]}')
