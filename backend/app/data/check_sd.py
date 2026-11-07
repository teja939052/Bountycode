import json

with open('questions_trusted.json', 'r', encoding='utf-8') as f:
    trusted = json.load(f)

# Check system_design questions
sd_qs = [q for q in trusted if q.get('pattern') == 'system_design']
print(f'System design questions: {len(sd_qs)}')
for i in [0, 50, 100, 137]:
    if i >= len(sd_qs):
        break
    q = sd_qs[i]
    print(f'\n--- SD {i} ---')
    print(f'  topic: {q.get("topic")}')
    print(f'  question: {str(q.get("question", ""))[:150]}')
    print(f'  mental_model: {str(q.get("mental_model", ""))[:100]}')
    print(f'  solution type: {type(q.get("solution")).__name__}')
    print(f'  test_cases: {len(q.get("test_cases", []))}')

# Check pattern diversity
print(f'\n=== PATTERN DIVERSITY CHECK ===')
patterns = {}
for q in trusted:
    p = q.get('pattern', 'untagged')
    if p not in patterns:
        patterns[p] = []
    patterns[p].append(q.get('question', '')[:80])

for p in list(patterns.keys())[:10]:
    print(f'\n{p} ({len(patterns[p])} questions):')
    for q in patterns[p][:2]:
        print(f'  {q}')
