import json

with open('verified_placement_questions.json', 'r') as f:
    verified_data = json.load(f)

# Find coding questions with real test cases
coding_qs = [q for q in verified_data if q.get('type') == 'coding']
print(f'Verified coding questions: {len(coding_qs)}')

real_test_coding = []
for q in coding_qs:
    tcs = q.get('testcases', [])
    htc = q.get('hidden_testcases', [])
    has_real = False
    for tc in tcs + htc:
        expected = tc.get('expected', '')
        if expected and expected not in ['result', 'sample', '']:
            has_real = True
            break
    if has_real:
        real_test_coding.append(q)

print(f'Verified coding with real tests: {len(real_test_coding)}')
for q in real_test_coding[:5]:
    print(f'  id={q.get("id")}, topic={q.get("topic")}, pattern={q.get("pattern")}')
    print(f'  title={q.get("title", "")[:70]}')
    tcs = q.get('testcases', [])
    htc = q.get('hidden_testcases', [])
    print(f'  visible tests: {len(tcs)}, hidden tests: {len(htc)}')
    if tcs:
        print(f'  sample visible: {tcs[0]}')
    if htc:
        print(f'  sample hidden: {htc[0]}')
    print()

# Check aptitude questions in verified bank
apt_qs = [q for q in verified_data if q.get('type') == 'aptitude']
print(f'\nVerified aptitude questions: {len(apt_qs)}')
for q in apt_qs[:3]:
    print(f'  id={q.get("id")}, topic={q.get("topic")}, title={q.get("title", "")[:70]}')
    print(f'  correct_answer={q.get("correct_answer")}')
    print(f'  options={q.get("options", [])[:2]}')
    print()
