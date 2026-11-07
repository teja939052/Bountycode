"""Analyze question bank and write results to file."""
import json
import os

output = []

with open('app/data/questions_bank.json', 'r', encoding='utf-8') as f:
    bank = json.load(f)

output.append(f"Total questions: {len(bank)}")

# Type distribution
from collections import Counter
type_counts = Counter(q.get('type', 'MISSING') for q in bank)
output.append(f"\nType distribution: {dict(type_counts)}")

# Missing fields
missing_sol = sum(1 for q in bank if not q.get('solution'))
missing_tc = sum(1 for q in bank if not q.get('test_cases'))
missing_hints = sum(1 for q in bank if not q.get('hints'))
missing_answer = sum(1 for q in bank if q.get('correct_answer') is None and not q.get('options'))

output.append(f"Missing solution: {missing_sol}")
output.append(f"Missing test_cases: {missing_tc}")
output.append(f"Missing hints: {missing_hints}")
output.append(f"Missing answer: {missing_answer}")

# Duplicates
id_counts = Counter(str(q.get('id', '')) for q in bank)
dups = sum(1 for c in id_counts.values() if c > 1)
output.append(f"Duplicate IDs: {dups}")

# Write results
with open('app/scripts/audit_result.txt', 'w') as f:
    f.write('\n'.join(output))

print("Done - check app/scripts/audit_result.txt")
