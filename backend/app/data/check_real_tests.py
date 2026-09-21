import json

with open('tcs_nqt_questions.json', 'r') as f:
    tcs_data = json.load(f)

# Find aptitude questions with real test cases (not just sample/result placeholders)
real_test_apt = []
for q in tcs_data:
    if q.get('type') != 'aptitude':
        continue
    vtc = q.get('visible_test_cases', [])
    htc = q.get('hidden_test_cases', [])
    # Check if any test case has real expected values
    has_real = False
    for tc in vtc + htc:
        expected = tc.get('expected', tc.get('output', ''))
        if expected and expected not in ['result', 'sample', '']:
            has_real = True
            break
    if has_real:
        real_test_apt.append(q)

print(f'Aptitude questions with real test cases: {len(real_test_apt)}')
for q in real_test_apt[:5]:
    print(f'  id={q.get("id")}, topic={q.get("topic")}, title={q.get("question_title", "")[:60]}')
    vtc = q.get('visible_test_cases', [])
    htc = q.get('hidden_test_cases', [])
    print(f'  visible tests: {len(vtc)}, hidden tests: {len(htc)}')
    if vtc:
        print(f'  sample visible: {vtc[0]}')
    if htc:
        print(f'  sample hidden: {htc[0]}')
    print()

# Check coding questions
coding_qs = [q for q in tcs_data if q.get('type') == 'coding']
real_test_coding = []
for q in coding_qs:
    vtc = q.get('visible_test_cases', [])
    htc = q.get('hidden_test_cases', [])
    has_real = False
    for tc in vtc + htc:
        expected = tc.get('expected', tc.get('output', ''))
        if expected and expected not in ['result', 'sample', '']:
            has_real = True
            break
    if has_real:
        real_test_coding.append(q)

print(f'Coding questions with real test cases: {len(real_test_coding)}')
for q in real_test_coding[:5]:
    print(f'  id={q.get("id")}, topic={q.get("topic")}, title={q.get("question_title", "")[:60]}')
    vtc = q.get('visible_test_cases', [])
    htc = q.get('hidden_test_cases', [])
    print(f'  visible tests: {len(vtc)}, hidden tests: {len(htc)}')
    if vtc:
        print(f'  sample visible: {vtc[0]}')
    if htc:
        print(f'  sample hidden: {htc[0]}')
    print()
