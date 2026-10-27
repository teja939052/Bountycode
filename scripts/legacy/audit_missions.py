import json, os, glob

VALID_CODES = {
    'aptitude': {'apt_percent_base_confusion', 'apt_percentage_point_confusion', 'apt_ratio_interpretation_error', 'apt_average_denominator_error', 'apt_rate_work_relationship', 'apt_unit_conversion_error'},
    'reasoning': {'reasoning_relationship_chain_error', 'reasoning_assumption_error', 'reasoning_ordering_error', 'reasoning_constraint_omission', 'reasoning_sequence_inference', 'reasoning_case_elimination'},
    'verbal': {'verbal_tone_mismatch', 'verbal_grammar_agreement', 'verbal_tense_misuse', 'verbal_inference_error', 'verbal_vocabulary_context'},
    'coding': {'coding_state_trace_error', 'coding_loop_boundary_error', 'coding_condition_boundary_error', 'coding_array_index_error', 'coding_complexity_misconception'},
    'sql': {'sql_join_key_confusion', 'sql_filtering_stage_confusion', 'sql_grouping_grain_error', 'sql_null_semantics_error', 'sql_aggregation_granule_error'},
    'cs_core': {'cs_core_process_thread_confusion', 'cs_core_stack_heap_misconception', 'cs_core_normalization_misconception', 'cs_core_network_layer_confusion', 'cs_core_oop_relationship_misconception'},
}

REQUIRED_FIELDS = ['id', 'title', 'domain', 'concept', 'skill_id', 'tags', 'difficulty', 'estimated_minutes', 'mastery_threshold', 'why_it_matters', 'prerequisites', 'misconceptions', 'captain_byte', 'discover', 'understand', 'manipulate', 'predict', 'build', 'break_step', 'debug', 'retrieval', 'transfer', 'practice', 'proof', 'company_variants', 'srs_key_points', 'srs_review_intervals']

files = sorted(glob.glob(r'D:\Project-Fremen\backend\app\content\mission_packs\*.json'))
results = []

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    filename = os.path.basename(f)
    domain = data.get('domain', '')
    
    missing = [field for field in REQUIRED_FIELDS if field not in data]
    
    misconceptions = data.get('misconceptions', [])
    codes = [m.get('code', '') for m in misconceptions if m.get('code')]
    domain_key = domain
    valid_for_domain = VALID_CODES.get(domain_key, set())
    outdated = [c for c in codes if c not in valid_for_domain]
    
    practice_count = len(data.get('practice', []))
    proof_count = len(data.get('proof', []))
    company_variants_count = len(data.get('company_variants', []))
    srs_points_count = len(data.get('srs_key_points', []))
    
    tags = data.get('tags', [])
    has_service_company_tag = 'service-companies' in tags
    company_variants_ok = company_variants_count > 0 if has_service_company_tag else True
    
    pass_check = (
        len(missing) == 0 and
        len(outdated) == 0 and
        practice_count >= 1 and
        proof_count >= 1 and
        company_variants_ok and
        srs_points_count >= 3
    )
    
    results.append({
        'filename': filename,
        'domain': domain,
        'missing': ', '.join(missing) if missing else '-',
        'outdated': ', '.join(outdated) if outdated else '-',
        'practice': practice_count,
        'proof': proof_count,
        'company_variants': company_variants_count,
        'srs_points': srs_points_count,
        'pass': 'PASS' if pass_check else 'FAIL'
    })

# Print table
print(f'{"filename":<45} {"domain":<12} {"missing":<20} {"outdated":<35} {"practice":>8} {"proof":>5} {"cv":>4} {"srs":>4} {"pass":>5}')
print('-' * 145)
for r in results:
    print(f'{r["filename"]:<45} {r["domain"]:<12} {r["missing"]:<20} {r["outdated"]:<35} {r["practice"]:>8} {r["proof"]:>5} {r["company_variants"]:>4} {r["srs_points"]:>4} {r["pass"]:>5}')

# Summary
passed = sum(1 for r in results if r['pass'] == 'PASS')
failed = sum(1 for r in results if r['pass'] == 'FAIL')
print(f'\nTotal: {len(results)} | PASS: {passed} | FAIL: {failed}')

# Detailed failure reasons
print('\n=== FAILURE DETAILS ===')
for r in results:
    if r['pass'] == 'FAIL':
        reasons = []
        if r['missing'] != '-':
            reasons.append(f'missing fields: {r["missing"]}')
        if r['outdated'] != '-':
            reasons.append(f'outdated codes: {r["outdated"]}')
        if r['practice'] < 1:
            reasons.append(f'practice count={r["practice"]}')
        if r['proof'] < 1:
            reasons.append(f'proof count={r["proof"]}')
        if r['company_variants'] == 0:
            reasons.append('empty company_variants for service-company tag')
        if r['srs_points'] < 3:
            reasons.append(f'srs points={r["srs_points"]}')
        print(f'{r["filename"]}: {\"; \".join(reasons)}')
