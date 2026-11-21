import json
from pathlib import Path
from collections import Counter

data_dir = Path('backend/app/data')

# Check all verified_* files and sql_practice_bank.json
files_to_check = [
    'verified_aptitude.json', 'verified_cs_fundamentals.json', 'verified_logical.json', 'verified_verbal.json',
    'debugging_bank.json', 'sql_practice_bank.json', 'system_design_bank.json',
    'verified_placement_questions.json', 'interview_practice_bank.json',
    'capgemini_accenture_verified.json', 'cognizant_genc_verified.json',
    'infosys_infytq_verified.json', 'tcs_nqt_coding_verified.json',
    'tcs_nqt_mcq_verified.json', 'wipro_nlth_verified.json'
]

for fname in sorted(files_to_check):
    fpath = data_dir / fname
    if not fpath.exists():
        print(f'{fname}: NOT FOUND')
        continue
    try:
        with open(fpath, 'r', encoding='utf-8', errors='replace') as fh:
            data = json.load(fh)
    except Exception as e:
        print(f'{fname}: ERROR - {e}')
        continue
    
    items = data if isinstance(data, list) else data.get('questions', [])
    trust_counts = Counter()
    for q in items:
        if isinstance(q, dict):
            ts = str(q.get('trust_status', 'MISSING')).lower()
            trust_counts[ts] += 1
    print(f'{fname}: {len(items)} questions, trust={dict(trust_counts)}')
