"""Examine the incomplete questions (MISSING type) to understand what needs fixing."""
import json

output = []

with open('app/data/questions_bank.json', 'r', encoding='utf-8') as f:
    bank = json.load(f)

# Find questions with MISSING type
missing_type = [q for q in bank if not q.get('type')]
output.append(f"Questions with MISSING type: {len(missing_type)}")

if missing_type:
    output.append(f"\nFirst 3 MISSING type questions:")
    for i, q in enumerate(missing_type[:3]):
        output.append(f"\n--- Question {i+1} ---")
        output.append(f"Keys: {list(q.keys())}")
        for k, v in q.items():
            val_str = str(v)[:80].encode('ascii', errors='replace').decode()
            output.append(f"  {k}: {val_str}")

# Check what fields the "complete" coding questions have
coding = [q for q in bank if q.get('type') == 'coding']
output.append(f"\n\n=== CODING QUESTIONS ({len(coding)}) ===")
if coding:
    output.append(f"Keys in first coding q: {list(coding[0].keys())}")
    with_tc = [q for q in coding if q.get('test_cases')]
    output.append(f"With test_cases: {len(with_tc)}")
    if with_tc:
        output.append(f"Sample test_cases: {str(with_tc[0]['test_cases'][:1])[:200]}")
    with_sol = [q for q in coding if q.get('solution')]
    output.append(f"With solution: {len(with_sol)}")
    if with_sol:
        sol = with_sol[0]['solution']
        output.append(f"Solution keys: {list(sol.keys()) if isinstance(sol, dict) else type(sol)}")

# Check aptitude/logical/verbal structure
for t in ['aptitude', 'logical', 'verbal']:
    qs = [q for q in bank if q.get('type') == t]
    if qs:
        output.append(f"\n=== {t.upper()} ({len(qs)}) ===")
        output.append(f"Keys: {list(qs[0].keys())}")
        output.append(f"Has correct_answer: {qs[0].get('correct_answer') is not None}")
        output.append(f"Has options: {bool(qs[0].get('options'))}")

# Write to file
with open('app/scripts/examine_result.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
print("Done - check app/scripts/examine_result.txt")
