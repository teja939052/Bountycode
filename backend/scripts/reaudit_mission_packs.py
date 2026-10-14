#!/usr/bin/env python3
"""Re-audit all mission packs after misconception code update."""

import json
from pathlib import Path

pack_dir = Path("D:/Project-Fremen/backend/app/content/mission_packs")
failures = []
for f in sorted(pack_dir.glob("*.json")):
    data = json.load(open(f))
    mis = data.get("misconceptions", [])
    company_variants = data.get("company_variants", [])
    srs = data.get("srs_key_points", [])
    practice = data.get("practice", [])
    proof = data.get("proof", [])
    
    required = ['id', 'title', 'domain', 'concept', 'skill_id', 'tags', 'difficulty', 
                'estimated_minutes', 'mastery_threshold', 'why_it_matters', 'prerequisites',
                'misconceptions', 'captain_byte', 'discover', 'understand', 'manipulate',
                'predict', 'build', 'break_step', 'debug', 'retrieval', 'transfer',
                'practice', 'proof', 'company_variants', 'srs_key_points', 'srs_review_intervals']
    missing = [r for r in required if r not in data]
    
    bad_codes = [m['code'] for m in mis if not m['code'].startswith(('apt_', 'reasoning_', 'verbal_', 'coding_', 'sql_', 'cs_core_'))]
    
    is_service = 'service-companies' in data.get('tags', [])
    empty_company_variants = is_service and len(company_variants) == 0
    
    if missing or bad_codes or empty_company_variants:
        failures.append((f.name, missing, bad_codes, empty_company_variants, len(practice), len(proof), len(srs)))

total = len(list(pack_dir.glob("*.json")))
print(f"Total files: {total}")
print(f"Failures: {len(failures)}")
for name, missing, bad_codes, empty_cv, prac, prf, srs in failures:
    print(f"  {name}: missing={missing}, bad_codes={bad_codes}, empty_cv={empty_cv}, practice={prac}, proof={prf}, srs={srs}")
if not failures:
    print("All files pass!")
