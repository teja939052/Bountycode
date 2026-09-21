import json
from collections import Counter

with open('verified_placement_questions.json', 'r', encoding='utf-8') as f:
    verified = json.load(f)

print('=== VERIFIED BANK PEDAGOGICAL DEPTH ===')
print(f'Total: {len(verified)}')

# Check all fields
field_presence = {}
for q in verified:
    for k in q.keys():
        field_presence[k] = field_presence.get(k, 0) + 1

print(f'\nField presence:')
for k, v in sorted(field_presence.items(), key=lambda x: -x[1]):
    pct = v/len(verified)*100
    print(f'  {k}: {v}/{len(verified)} ({pct:.0f}%)')

# Check by type
print(f'\n=== BY TYPE ===')
for qtype in ['coding', 'aptitude', 'logical', 'verbal', 'cs_fundamentals']:
    qs = [q for q in verified if q.get('type') == qtype]
    print(f'\n{qtype} ({len(qs)}):')
    has_solution = sum(1 for q in qs if q.get('solution'))
    has_testcases = sum(1 for q in qs if q.get('testcases'))
    has_hidden = sum(1 for q in qs if q.get('hidden_testcases'))
    has_explanation = sum(1 for q in qs if q.get('explanation'))
    has_hints = sum(1 for q in qs if q.get('hints'))
    has_constraints = sum(1 for q in qs if q.get('constraints'))
    has_common_trap = sum(1 for q in qs if q.get('common_trap'))
    has_shortcut = sum(1 for q in qs if q.get('shortcut'))
    has_reasoning = sum(1 for q in qs if q.get('reasoning_steps'))
    
    print(f'  solution: {has_solution}/{len(qs)} ({has_solution/len(qs)*100:.0f}%)')
    print(f'  testcases: {has_testcases}/{len(qs)} ({has_testcases/len(qs)*100:.0f}%)')
    print(f'  hidden_testcases: {has_hidden}/{len(qs)} ({has_hidden/len(qs)*100:.0f}%)')
    print(f'  explanation: {has_explanation}/{len(qs)} ({has_explanation/len(qs)*100:.0f}%)')
    print(f'  hints: {has_hints}/{len(qs)} ({has_hints/len(qs)*100:.0f}%)')
    print(f'  constraints: {has_constraints}/{len(qs)} ({has_constraints/len(qs)*100:.0f}%)')
    print(f'  common_trap: {has_common_trap}/{len(qs)} ({has_common_trap/len(qs)*100:.0f}%)')
    print(f'  shortcut: {has_shortcut}/{len(qs)} ({has_shortcut/len(qs)*100:.0f}%)')
    print(f'  reasoning_steps: {has_reasoning}/{len(qs)} ({has_reasoning/len(qs)*100:.0f}%)')

# Check trust reports
print(f'\n=== TRUST REPORTS ===')
has_trust_report = sum(1 for q in verified if q.get('trust_report'))
print(f'Questions with trust_report: {has_trust_report}/{len(verified)} ({has_trust_report/len(verified)*100:.0f}%)')

# Sample trust reports
for q in verified[:3]:
    if q.get('trust_report'):
        print(f'\nSample trust_report:')
        print(json.dumps(q['trust_report'], indent=2)[:300])
