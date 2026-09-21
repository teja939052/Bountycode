import json

with open('tcs_nqt_questions.json', 'r') as f:
    tcs_data = json.load(f)

with open('verified_placement_questions.json', 'r') as f:
    verified_data = json.load(f)

# Check if tcs questions have trust_status
print('TCS question sample keys:', list(tcs_data[0].keys()))
print('TCS question trust_status values:', set(q.get('trust_status', 'missing') for q in tcs_data))

# Check verified question structure
print('\nVerified question sample keys:', list(verified_data[0].keys()))
print('Verified question sample:', json.dumps(verified_data[0], indent=2)[:500])

# Find TCS aptitude questions with test cases
apt_with_tests = [q for q in tcs_data if q.get('type') == 'aptitude' and q.get('visible_test_cases')][:3]
print(f'\nTCS aptitude with tests: {len(apt_with_tests)}')
for q in apt_with_tests[:2]:
    print(f'  id={q.get("id")}, topic={q.get("topic")}')
    print(f'  title={q.get("question_title", "")[:60]}')
    print(f'  tests={len(q.get("visible_test_cases", []))}')
    if q.get('visible_test_cases'):
        print(f'  sample test: {q["visible_test_cases"][0]}')

# Find TCS coding questions with test cases
coding_with_tests = [q for q in tcs_data if q.get('type') == 'coding' and q.get('visible_test_cases')][:3]
print(f'\nTCS coding with tests: {len(coding_with_tests)}')
for q in coding_with_tests[:2]:
    print(f'  id={q.get("id")}, topic={q.get("topic")}')
    print(f'  title={q.get("question_title", "")[:60]}')
    print(f'  tests={len(q.get("visible_test_cases", []))}')
    if q.get('visible_test_cases'):
        print(f'  sample test: {q["visible_test_cases"][0]}')
