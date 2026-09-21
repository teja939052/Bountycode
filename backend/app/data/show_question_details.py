import json

with open('tcs_nqt_questions.json', 'r') as f:
    tcs_data = json.load(f)

# Show a few aptitude questions in detail
apt_qs = [q for q in tcs_data if q.get('type') == 'aptitude'][:3]
for q in apt_qs:
    print('=== APTITUDE QUESTION ===')
    print(json.dumps(q, indent=2)[:800])
    print()

# Show a few coding questions in detail
coding_qs = [q for q in tcs_data if q.get('type') == 'coding'][:3]
for q in coding_qs:
    print('=== CODING QUESTION ===')
    print(json.dumps(q, indent=2)[:800])
    print()
