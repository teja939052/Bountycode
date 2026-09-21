import json
from collections import Counter

with open('tcs_nqt_questions.json', 'r') as f:
    data = json.load(f)

types = Counter(q.get('type', 'unknown') for q in data)
print('Question types:', dict(types))

for t in types.keys():
    examples = [q for q in data if q.get('type') == t][:2]
    print(f'\n{t.upper()} examples:')
    for q in examples:
        title = q.get('question_title', q.get('question', ''))[:80]
        print(f'  id={q.get("id")}, topic={q.get("topic")}, title={title}')

# Also check verified_placement_questions.json
try:
    with open('verified_placement_questions.json', 'r') as f:
        vdata = json.load(f)
    vtypes = Counter(q.get('type', 'unknown') for q in vdata)
    print('\nVerified placement question types:', dict(vtypes))
except Exception as e:
    print(f'\nverified_placement_questions.json error: {e}')
