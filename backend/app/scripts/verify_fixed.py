"""Verify the fixed question bank quality."""
import json

with open('app/data/questions_bank_fixed.json', 'r', encoding='utf-8') as f:
    bank = json.load(f)

print(f"Total questions: {len(bank)}")

# Type distribution
from collections import Counter
type_counts = Counter(q.get('type', 'MISSING') for q in bank)
print(f"\nType distribution:")
for t, c in type_counts.most_common():
    print(f"  {t:<12}: {c}")

# Check field completeness
missing_solution = sum(1 for q in bank if not q.get('solution'))
missing_tc = sum(1 for q in bank if not q.get('test_cases') and q.get('type') == 'coding')
missing_hints = sum(1 for q in bank if not q.get('hints'))
missing_pattern = sum(1 for q in bank if not q.get('pattern'))

print(f"\nField completeness:")
print(f"  Missing solution: {missing_solution}")
print(f"  Missing test_cases (coding): {missing_tc}")
print(f"  Missing hints: {missing_hints}")
print(f"  Missing pattern: {missing_pattern}")

# Check for remaining 'computed' placeholders
computed_count = 0
for q in bank:
    for tc in q.get('test_cases', []):
        if tc.get('output') == 'computed':
            computed_count += 1
print(f"  Remaining 'computed' outputs: {computed_count}")

# Sample questions
print(f"\n=== SAMPLE QUESTIONS ===")
for q in bank[:3]:
    print(f"\nID: {q.get('id')}")
    print(f"Type: {q.get('type')}, Topic: {q.get('topic')}, Difficulty: {q.get('difficulty')}")
    print(f"Pattern: {q.get('pattern')}")
    print(f"Companies: {q.get('companies', [])}")
    print(f"Title: {q.get('title', '')[:60]}")
    print(f"Test cases: {len(q.get('test_cases', []))}")
    print(f"Hints: {len(q.get('hints', []))}")

# Verify IDs are unique
ids = [q.get('id') for q in bank]
print(f"\n=== ID UNIQUENESS ===")
print(f"Total IDs: {len(ids)}")
print(f"Unique IDs: {len(set(ids))}")
if len(ids) != len(set(ids)):
    dup_ids = [id for id, count in Counter(ids).items() if count > 1]
    print(f"Duplicate IDs: {dup_ids[:10]}")
