import json
from pathlib import Path

data_dir = Path('backend/app/data')
fpath = data_dir / 'sql_practice_bank.json'

with open(fpath, 'r', encoding='utf-8') as f:
    data = json.load(f)

items = data if isinstance(data, list) else data.get('questions', [])

downgraded = 0
for q in items:
    if isinstance(q, dict) and str(q.get('id', '')).startswith('sql-b2-'):
        old_trust = q.get('trust_status')
        if old_trust == 'verified':
            q['trust_status'] = 'automated_checked'
            q['trust_transitioned_at'] = '2026-11-17T00:00:00Z'
            q['trust_transition_reason'] = 'Batch-added question lacked human review; downgraded to automated_checked pending review'
            downgraded += 1

with open(fpath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f'Downgraded {downgraded} questions from verified to automated_checked in sql_practice_bank.json')
