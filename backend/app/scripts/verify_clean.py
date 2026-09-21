"""Verify clean bank quality."""
import json
from collections import Counter

with open('app/data/questions_bank_clean.json', 'r', encoding='utf-8') as f:
    clean = json.load(f)

print(f"Clean bank: {len(clean)} questions")

# Type distribution
types = Counter(q.get('type', 'MISSING') for q in clean)
print(f"\nBy type:")
for t, c in types.most_common():
    print(f"  {t}: {c}")

# Check for remaining template placeholders
template_count = 0
for q in clean:
    text = q.get('question', '') or q.get('title', '') or q.get('description', '')
    if '{variant' in text or '{k}' in text or '{n}' in text:
        template_count += 1
print(f"\nQuestions with unreplaced templates: {template_count}")

# Check for very short/generic titles
generic = [q for q in clean if len(q.get('title', '') or q.get('question', '')) < 20]
print(f"Very short titles (<20 chars): {len(generic)}")

# Sample questions
print(f"\n=== SAMPLE QUESTIONS ===")
for q in clean[:5]:
    text = q.get('question', '') or q.get('title', '') or q.get('description', '')
    sol = q.get('solution', '')
    if isinstance(sol, dict):
        sol = sol.get('code', '')
    print(f"\nID: {q.get('id')}")
    print(f"Type: {q.get('type')}, Topic: {q.get('topic')}")
    print(f"Text: {text[:80]}")
    print(f"Solution: {str(sol)[:60]}")
    print(f"Test cases: {len(q.get('test_cases', []))}")
