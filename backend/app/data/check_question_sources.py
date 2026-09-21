import json

with open('tcs_nqt_questions.json', 'r') as f:
    tcs_data = json.load(f)

with open('verified_placement_questions.json', 'r') as f:
    verified_data = json.load(f)

# Check verbal questions in verified bank
verbal_qs = [q for q in verified_data if q.get('type') == 'verbal']
print(f'Verbal questions in verified bank: {len(verbal_qs)}')
for q in verbal_qs[:3]:
    print(f'  id={q.get("id")}, topic={q.get("topic")}, title={q.get("title", "")[:60]}')
    print(f'  trust_status={q.get("trust_status")}')
    print(f'  testcases={len(q.get("testcases", []))}')
    print(f'  hidden_testcases={len(q.get("hidden_testcases", []))}')
    print()

# Check logical questions
logical_qs = [q for q in verified_data if q.get('type') == 'logical']
print(f'Logical questions in verified bank: {len(logical_qs)}')
for q in logical_qs[:3]:
    print(f'  id={q.get("id")}, topic={q.get("topic")}, title={q.get("title", "")[:60]}')
    print()

# Check TCS aptitude questions with good test coverage
apt_qs = [q for q in tcs_data if q.get('type') == 'aptitude']
print(f'\nTCS aptitude questions: {len(apt_qs)}')
apt_with_hidden = [q for q in apt_qs if q.get('hidden_test_cases') and len(q.get('hidden_test_cases', [])) > 0]
print(f'TCS aptitude with hidden tests: {len(apt_with_hidden)}')

# Check TCS coding questions
coding_qs = [q for q in tcs_data if q.get('type') == 'coding']
print(f'\nTCS coding questions: {len(coding_qs)}')
coding_with_hidden = [q for q in coding_qs if q.get('hidden_test_cases') and len(q.get('hidden_test_cases', [])) > 0]
print(f'TCS coding with hidden tests: {len(coding_with_hidden)}')
for q in coding_with_hidden[:3]:
    print(f'  id={q.get("id")}, topic={q.get("topic")}, title={q.get("question_title", "")[:60]}')
    print(f'  visible tests: {len(q.get("visible_test_cases", []))}')
    print(f'  hidden tests: {len(q.get("hidden_test_cases", []))}')
