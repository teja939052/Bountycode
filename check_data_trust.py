import json, os
from pathlib import Path
from collections import Counter

data_dir = Path('backend/app/data')

# Check each verified question bank file for trust_status values
for fname in sorted(data_dir.glob('*.json')):
    try:
        with open(fname, 'r', encoding='utf-8', errors='replace') as fh:
            data = json.load(fh)
    except Exception as e:
        continue
    
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict) and isinstance(data.get('questions'), list):
        items = data['questions']
    else:
        continue
    
    if not items:
        continue
    
    trust_counts = Counter()
    source_counts = Counter()
    for q in items:
        if isinstance(q, dict):
            ts = str(q.get('trust_status', 'MISSING')).lower()
            trust_counts[ts] += 1
            sb = str(q.get('source_bank', 'MISSING'))
            source_counts[sb] += 1
    
    if trust_counts:
        print(f'{fname.name}: {len(items)} questions')
        print(f'  trust: {dict(trust_counts)}')
        top_sources = dict(source_counts.most_common(5))
        print(f'  source_bank: {top_sources}')
