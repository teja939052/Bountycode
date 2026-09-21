import json

with open('questions_trusted.json', 'r', encoding='utf-8') as f:
    trusted = json.load(f)

print(f'Total trusted questions: {len(trusted)}')

# Check a few samples
for i in [0, 100, 500, 1000, 1500, 2000, 2500]:
    if i >= len(trusted):
        break
    q = trusted[i]
    print(f'=== Question {i} ===')
    print(f'  type: {q.get("type")}')
    print(f'  topic: {q.get("topic")}')
    print(f'  pattern: {q.get("pattern")}')
    print(f'  role: {q.get("role")} (type={type(q.get("role")).__name__})')
    print(f'  placement_stage: {q.get("placement_stage")}')
    cr = q.get('company_relevance')
    print(f'  company_relevance: {str(cr)[:100]} (type={type(cr).__name__})')
    print(f'  mental_model: {str(q.get("mental_model", ""))[:80]}')
    print(f'  has solution: {bool(q.get("solution"))}')
    print(f'  has test_cases: {bool(q.get("test_cases"))}')
    print(f'  has hidden_tests: {bool(q.get("hidden_tests"))}')
    print()

# Stats
from collections import Counter

types = Counter(q.get('type', 'unknown') for q in trusted)
print(f'Types: {dict(types)}')

patterns = Counter(q.get('pattern', 'untagged') for q in trusted)
print(f'Top 10 patterns: {dict(patterns.most_common(10))}')

# Pedagogical depth
has_mental_model = sum(1 for q in trusted if q.get('mental_model'))
has_solution = sum(1 for q in trusted if q.get('solution'))
has_test_cases = sum(1 for q in trusted if q.get('test_cases'))
has_hidden_tests = sum(1 for q in trusted if q.get('hidden_tests'))
has_constraints = sum(1 for q in trusted if q.get('constraints'))
has_explanation = sum(1 for q in trusted if q.get('explanation'))
has_hints = sum(1 for q in trusted if q.get('hints'))
has_enrichment = sum(1 for q in trusted if q.get('enrichment'))

print(f'\nPedagogical depth:')
print(f'  mental_model: {has_mental_model}/{len(trusted)} ({has_mental_model/len(trusted)*100:.0f}%)')
print(f'  solution: {has_solution}/{len(trusted)} ({has_solution/len(trusted)*100:.0f}%)')
print(f'  test_cases: {has_test_cases}/{len(trusted)} ({has_test_cases/len(trusted)*100:.0f}%)')
print(f'  hidden_tests: {has_hidden_tests}/{len(trusted)} ({has_hidden_tests/len(trusted)*100:.0f}%)')
print(f'  constraints: {has_constraints}/{len(trusted)} ({has_constraints/len(trusted)*100:.0f}%)')
print(f'  explanation: {has_explanation}/{len(trusted)} ({has_explanation/len(trusted)*100:.0f}%)')
print(f'  hints: {has_hints}/{len(trusted)} ({has_hints/len(trusted)*100:.0f}%)')
print(f'  enrichment: {has_enrichment}/{len(trusted)} ({has_enrichment/len(trusted)*100:.0f}%)')
