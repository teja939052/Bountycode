import sys
sys.path.insert(0, '.')
from app.services.question_store import _questions, _load_extra_bank, _dedupe_and_filter, _apply_leetcode_meta, _expand_questions, EXTRA_BANKS, AUTO_CHECKED_BANKS, trust_rank, TRUST_RANK
from collections import Counter

# Load the actual serving pool
_questions = []
_load_extra_bank(_questions)
_load_extra_bank(_questions, AUTO_CHECKED_BANKS)
_dedupe_and_filter(_questions)

print('=== AUTHORITATIVE SERVED QUESTION AUDIT ===')
print(f'Total served: {len(_questions)}')

# By trust status
trust = Counter(q.get('trust_status', 'missing') for q in _questions)
print(f'\nBy trust status:')
for status, count in trust.most_common():
    pct = count/len(_questions)*100
    print(f'  {status}: {count} ({pct:.0f}%)')

# By type
types = Counter(q.get('type', 'unknown') for q in _questions)
print(f'\nBy type:')
for t, c in types.most_common():
    pct = c/len(_questions)*100
    print(f'  {t}: {c} ({pct:.0f}%)')

# By source bank
sources = Counter()
for q in _questions:
    src = q.get('source_bank', 'unknown')
    sources[src] += 1
print(f'\nBy source bank:')
for s, c in sources.most_common(15):
    pct = c/len(_questions)*100
    print(f'  {s}: {c} ({pct:.0f}%)')

# Check for duplicates in serving pool
question_texts = [q.get('question', q.get('question_title', '')) for q in _questions]
unique_texts = set(question_texts)
print(f'\nDuplication in serving pool:')
print(f'  Total: {len(_questions)}')
print(f'  Unique texts: {len(unique_texts)}')
print(f'  Duplication rate: {(len(_questions) - len(unique_texts)) / len(_questions) * 100:.1f}%')

# Check SQL specifically
sql_qs = [q for q in _questions if 'sql' in q.get('type', '').lower() or 'sql' in q.get('topic', '').lower()]
print(f'\nSQL questions in serving pool: {len(sql_qs)}')

# Check behavioral
behavioral_qs = [q for q in _questions if 'behavioral' in q.get('type', '').lower() or 'behavioral' in q.get('topic', '').lower()]
print(f'Behavioral questions in serving pool: {len(behavioral_qs)}')

# Check system design
sd_qs = [q for q in _questions if 'system_design' in q.get('pattern', '').lower() or 'design' in q.get('topic', '').lower()]
print(f'System design questions in serving pool: {len(sd_qs)}')

# Check debugging
debug_qs = [q for q in _questions if 'debug' in q.get('type', '').lower() or 'debug' in q.get('topic', '').lower()]
print(f'Debugging questions in serving pool: {len(debug_qs)}')

# Check llm_draft_checked quality
llm_qs = [q for q in _questions if q.get('source_bank') == 'llm_draft_5000']
print(f'\n=== LLM_DRAFT_CHECKED ({len(llm_qs)} questions) ===')
print(f'Type distribution:')
types = Counter(q.get('type', 'unknown') for q in llm_qs)
for t, c in types.most_common():
    print(f'  {t}: {c}')

has_tests = sum(1 for q in llm_qs if q.get('testcases') or q.get('visible_test_cases'))
has_solution = sum(1 for q in llm_qs if q.get('solution'))
has_explanation = sum(1 for q in llm_qs if q.get('explanation'))
print(f'Pedagogical depth in llm_draft:')
print(f'  testcases: {has_tests}/{len(llm_qs)} ({has_tests/len(llm_qs)*100:.0f}%)')
print(f'  solution: {has_solution}/{len(llm_qs)} ({has_solution/len(llm_qs)*100:.0f}%)')
print(f'  explanation: {has_explanation}/{len(llm_qs)} ({has_explanation/len(llm_qs)*100:.0f}%)')

# Check verified bank quality
verified_qs = [q for q in _questions if q.get('trust_status') == 'verified']
print(f'\n=== VERIFIED BANK ({len(verified_qs)} questions) ===')
print(f'Type distribution:')
vtypes = Counter(q.get('type', 'unknown') for q in verified_qs)
for t, c in vtypes.most_common():
    print(f'  {t}: {c}')

has_tests_v = sum(1 for q in verified_qs if q.get('testcases') or q.get('visible_test_cases'))
has_solution_v = sum(1 for q in verified_qs if q.get('solution'))
has_explanation_v = sum(1 for q in verified_qs if q.get('explanation'))
print(f'Pedagogical depth in verified:')
print(f'  testcases: {has_tests_v}/{len(verified_qs)} ({has_tests_v/len(verified_qs)*100:.0f}%)')
print(f'  solution: {has_solution_v}/{len(verified_qs)} ({has_solution_v/len(verified_qs)*100:.0f}%)')
print(f'  explanation: {has_explanation_v}/{len(verified_qs)} ({has_explanation_v/len(verified_qs)*100:.0f}%)')
