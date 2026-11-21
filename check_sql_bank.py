import json
from pathlib import Path

data_dir = Path('backend/app/data')
fpath = data_dir / 'sql_practice_bank.json'
with open(fpath, 'r', encoding='utf-8', errors='replace') as fh:
    data = json.load(fh)
items = data if isinstance(data, list) else data.get('questions', [])
print(f'sql_practice_bank.json: {len(items)} total questions')
sql_b2_questions = [q for q in items if isinstance(q, dict) and str(q.get('id', '')).startswith('sql-b2')]
print(f'Questions with sql-b2- id prefix: {len(sql_b2_questions)}')
for q in sql_b2_questions:
    print(f'  id={q.get("id")}, trust_status={q.get("trust_status")}, type={q.get("type")}, has_sql_schema={bool(q.get("sql_schema"))}')
# Also check all trust statuses
from collections import Counter
trust_counts = Counter()
for q in items:
    if isinstance(q, dict):
        ts = str(q.get('trust_status', 'MISSING')).lower()
        trust_counts[ts] += 1
print(f'Trust status breakdown: {dict(trust_counts)}')
