import json

with open('verified_placement_questions.json', 'r', encoding='utf-8') as f:
    verified = json.load(f)

print('=== ENRICHED VERIFIED QUESTIONS SAMPLE ===')
for i in [0, 10, 50, 100]:
    q = verified[i]
    print(f'\n--- Question {i} ---')
    print(f'  type: {q.get("type")}')
    print(f'  topic: {q.get("topic")}')
    print(f'  explanation: {str(q.get("explanation", ""))[:120]}')
    print(f'  hints: {q.get("hints", [])[:2]}')
    print(f'  common_trap: {str(q.get("common_trap", ""))[:80]}')
    print(f'  reasoning_steps: {len(q.get("reasoning_steps", []))} steps')
    print(f'  constraints: {str(q.get("constraints", ""))[:80]}')

# Check coverage stats
has_explanation = sum(1 for q in verified if q.get('explanation'))
has_hints = sum(1 for q in verified if q.get('hints'))
has_traps = sum(1 for q in verified if q.get('common_trap'))
has_reasoning = sum(1 for q in verified if q.get('reasoning_steps'))
has_constraints = sum(1 for q in verified if q.get('constraints'))

print(f'\n=== POST-ENRICHMENT COVERAGE ===')
print(f'  explanation: {has_explanation}/{len(verified)} ({has_explanation/len(verified)*100:.0f}%)')
print(f'  hints: {has_hints}/{len(verified)} ({has_hints/len(verified)*100:.0f}%)')
print(f'  common_trap: {has_traps}/{len(verified)} ({has_traps/len(verified)*100:.0f}%)')
print(f'  reasoning_steps: {has_reasoning}/{len(verified)} ({has_reasoning/len(verified)*100:.0f}%)')
print(f'  constraints: {has_constraints}/{len(verified)} ({has_constraints/len(verified)*100:.0f}%)')
