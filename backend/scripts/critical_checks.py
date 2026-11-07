"""Critical checks on question bank audit."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app.services.question_store as qs
from collections import Counter, defaultdict

qs.load_all()
questions = qs._questions

print('=== CRITICAL CHECKS ===')
print()

# 1. Servable questions with MISSING test cases
print('1. SERVABLE QUESTIONS WITH MISSING/EMPTY TEST CASES')
print('='*60)
coding_servable_no_tc = 0
sql_servable_no_tc = 0

for q in questions:
    if not qs._is_servable(q):
        continue
    
    qtype = str(q.get('type', '')).lower()
    tcs = q.get('test_cases') or q.get('testcases') or []
    has_tc = len(tcs) > 0
    
    if qtype in ('coding', 'sql') and not has_tc:
        if qtype == 'coding':
            coding_servable_no_tc += 1
        elif qtype == 'sql':
            sql_servable_no_tc += 1

print(f'Coding servable but NO test cases: {coding_servable_no_tc}')
print(f'SQL servable but NO test cases: {sql_servable_no_tc}')
print(f'Total servable-without-TC: {coding_servable_no_tc + sql_servable_no_tc}')
print()

# 2. Exact counts by type
print('2. EXACT COUNTS BY TYPE')
print('='*60)
types = Counter(q.get('type', 'unknown') for q in questions)
for t, c in types.most_common():
    servable_count = sum(1 for q in questions if q.get('type', '').lower() == t.lower() and qs._is_servable(q))
    print(f'{t}: {c} total, {servable_count} servable')
print()

# 3. MCQ blast radius check
print('3. MCQ BLAST RADIUS CHECK')
print('='*60)
mcq_types = ('aptitude', 'logical', 'verbal', 'hr', 'behavioral')
mcq_total = 0
mcq_servable = 0
mcq_by_status = Counter()
mcq_trust_rank_issues = []

for q in questions:
    qtype = str(q.get('type', '')).lower()
    if qtype not in mcq_types:
        continue
    
    mcq_total += 1
    if qs._is_servable(q):
        mcq_servable += 1
    
    status = str(q.get('trust_status', '')).lower()
    mcq_by_status[status] += 1
    
    # Check if MCQ has correct test case structure
    tcs = q.get('test_cases') or []
    if tcs:
        for tc in tcs:
            if isinstance(tc, dict):
                out = str(tc.get('output', '')).strip().upper()
                correct = str(q.get('correct_answer') or q.get('correct_index') or '').upper()
                if correct and out != correct:
                    mcq_trust_rank_issues.append({
                        'id': q.get('id', ''),
                        'title': str(q.get('question') or q.get('question_title') or q.get('title') or '')[:50],
                        'expected': correct,
                        'got': out,
                        'status': status
                    })

print(f'Total MCQs: {mcq_total}')
print(f'Servable MCQs: {mcq_servable}')
print('MCQs by trust status:')
for status, count in mcq_by_status.most_common():
    label = status if status else '(empty)'
    print(f'  {label}: {count}')
print(f'MCQs with test case mismatch: {len(mcq_trust_rank_issues)}')
if mcq_trust_rank_issues:
    print('Sample mismatches:')
    for item in mcq_trust_rank_issues[:5]:
        title = item['title'][:50]
        print(f'  {title} -> expected={item["expected"]}, got={item["got"]} [{item["status"]}]')
print()

# 4. Re-verification needed check
print('4. HISTORICAL STAMP BLAST RADIUS')
print('='*60)
stamped_before_fix = 0
needs_reverification = []

for q in questions:
    status = str(q.get('trust_status', '')).lower()
    if status not in ('verified', 'reviewed', 'automated_checked'):
        continue
    
    qtype = str(q.get('type', '')).lower()
    if qtype not in mcq_types:
        continue
    
    # Check if this MCQ has the old broken test case pattern
    tcs = q.get('test_cases') or []
    for tc in tcs:
        if isinstance(tc, dict):
            out = str(tc.get('output', '')).strip().upper()
            correct = str(q.get('correct_answer') or q.get('correct_index') or '').upper()
            if correct and out != correct:
                stamped_before_fix += 1
                needs_reverification.append({
                    'id': q.get('id', ''),
                    'title': str(q.get('question') or q.get('question_title') or q.get('title') or '')[:50],
                    'status': status,
                    'expected': correct,
                    'got': out
                })
                break

print(f'MCQs stamped verified/automated_checked BEFORE fix: {stamped_before_fix}')
print(f'Of which have test case mismatch: {len(needs_reverification)}')
if needs_reverification:
    print('Sample stale stamps:')
    for item in needs_reverification[:5]:
        title = item['title'][:50]
        print(f'  [{item["status"]}] {title} -> expected={item["expected"]}, got={item["got"]}')
print()

# 5. Final corrected counts
print('5. CORRECTED SERVABLE COUNT')
print('='*60)
true_servable = 0
servable_with_tc = 0
servable_without_tc = 0

for q in questions:
    if not qs._is_servable(q):
        continue
    true_servable += 1
    qtype = str(q.get('type', '')).lower()
    tcs = q.get('test_cases') or q.get('testcases') or []
    if qtype in ('coding', 'sql') and len(tcs) == 0:
        servable_without_tc += 1
    else:
        servable_with_tc += 1

print(f'Reported servable: {sum(1 for q in questions if qs._is_servable(q))}')
print(f'Servable WITH test cases: {servable_with_tc}')
print(f'Servable WITHOUT test cases: {servable_without_tc}')
print(f'TRUE servable (with TCs): {servable_with_tc}')
print()

# 6. SQL-specific breakdown
print('6. SQL-SPECIFIC BREAKDOWN')
print('='*60)
sql_total = sum(1 for q in questions if str(q.get('type', '')).lower() == 'sql')
sql_servable = sum(1 for q in questions if str(q.get('type', '')).lower() == 'sql' and qs._is_servable(q))
sql_with_tc = sum(1 for q in questions if str(q.get('type', '')).lower() == 'sql' and (q.get('test_cases') or q.get('testcases')))
sql_verified = sum(1 for q in questions if str(q.get('type', '')).lower() == 'sql' and str(q.get('trust_status', '')).lower() in ('verified', 'reviewed', 'automated_checked'))

print(f'SQL total: {sql_total}')
print(f'SQL servable: {sql_servable}')
print(f'SQL with test cases: {sql_with_tc}')
print(f'SQL verified/checked: {sql_verified}')
print(f'SQL servable WITHOUT TCs: {sql_servable - sql_with_tc}')
print()

# 7. Reconciliation: do trust_status categories sum to total?
print('7. TRUST STATUS RECONCILIATION')
print('='*60)
statuses = Counter(q.get('trust_status', '') for q in questions)
total_by_status = sum(statuses.values())
print(f'Total by status sum: {total_by_status}')
print(f'Actual total: {len(questions)}')
print(f'Match: {total_by_status == len(questions)}')
print()

# 8. Are there verified/automated_checked questions with NO test cases?
print('8. VERIFIED/AUTO_CHECKED QUESTIONS WITH NO TEST CASES')
print('='*60)
verified_no_tc = 0
for q in questions:
    status = str(q.get('trust_status', '')).lower()
    if status not in ('verified', 'reviewed', 'automated_checked'):
        continue
    qtype = str(q.get('type', '')).lower()
    if qtype not in ('coding', 'sql'):
        continue
    tcs = q.get('test_cases') or q.get('testcases') or []
    if len(tcs) == 0:
        verified_no_tc += 1

print(f'Verified/checked coding+sql with NO test cases: {verified_no_tc}')
if verified_no_tc > 0:
    print('WARNING: These are in the servable pool but have no test cases!')
else:
    print('OK: All verified/checked coding+sql questions have test cases.')
