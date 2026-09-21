"""Complete question bank audit."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app.services.question_store as qs
from collections import Counter, defaultdict

qs.load_all()
questions = qs._questions

print('=== QUESTION BANK AUDIT ===')
print(f'Total questions: {len(questions)}')
print()

# By type
types = Counter(q.get('type', 'unknown') for q in questions)
print('By type:')
for t, c in types.most_common():
    print(f'  {t}: {c}')
print()

# By trust status
statuses = Counter(q.get('trust_status', '') for q in questions)
print('By trust status:')
for s, c in statuses.most_common():
    label = s if s else '(empty)'
    print(f'  {label}: {c}')
print()

# Servable vs non-servable
servable = sum(1 for q in questions if qs._is_servable(q))
non_servable = len(questions) - servable
print(f'Servable: {servable}')
print(f'Non-servable: {non_servable}')
print()

# Source breakdown
sources = Counter()
for q in questions:
    src = q.get('source_bank') or q.get('provenance') or 'unknown'
    sources[src] += 1
print('Top 15 sources:')
for src, c in sources.most_common(15):
    print(f'  {src}: {c}')
print()

# Check for duplicates
from collections import defaultdict
title_groups = defaultdict(list)
for q in questions:
    title = str(q.get('question') or q.get('question_title') or q.get('title') or '').lower().strip()
    if title:
        title_groups[title].append(q)

dupes = {t: qs for t, qs in title_groups.items() if len(qs) > 1}
print(f'Duplicate titles: {len(dupes)}')
print(f'Duplicate instances: {sum(len(qs)-1 for qs in dupes.values())}')
print()

# Check missing fields
missing = defaultdict(lambda: defaultdict(int))
for q in questions:
    qtype = str(q.get('type') or 'unknown').lower()
    if not q.get('question') and not q.get('question_title') and not q.get('title'):
        missing[qtype]['missing_title'] += 1
    if qtype in ('coding', 'sql') and not (q.get('testcases') or q.get('test_cases')):
        missing[qtype]['missing_testcases'] += 1
    if qtype in ('aptitude', 'logical', 'verbal', 'hr', 'behavioral') and not q.get('options'):
        missing[qtype]['missing_options'] += 1
    if qtype in ('aptitude', 'logical', 'verbal', 'hr', 'behavioral') and not (q.get('correct_answer') or q.get('correct_index')):
        missing[qtype]['missing_answer'] += 1
    if not q.get('explanation') and not q.get('description'):
        missing[qtype]['missing_explanation'] += 1

print('Missing fields by type:')
for qtype, fields in missing.items():
    if fields:
        print(f'  {qtype}:', dict(fields))
print()

# Verification stats
print('=== VERIFICATION STATS ===')
verified = sum(1 for q in questions if str(q.get('trust_status', '')).lower() in ('verified', 'reviewed', 'automated_checked'))
print(f'Verified or higher: {verified}')
print(f'Unverified/needs review: {len(questions) - verified}')
