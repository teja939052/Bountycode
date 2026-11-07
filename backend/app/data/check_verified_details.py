import json

with open('verified_placement_questions.json', 'r') as f:
    verified_data = json.load(f)

# Get all verified verbal questions with full details
verbal_qs = [q for q in verified_data if q.get('type') == 'verbal']
print(f'Verified verbal questions: {len(verbal_qs)}')
for q in verbal_qs[:5]:
    print(f'  id={q.get("id")}, topic={q.get("topic")}, sub_topic={q.get("sub_topic")}')
    print(f'  title={q.get("title", "")[:80]}')
    print(f'  correct_answer={q.get("correct_answer")}')
    print(f'  options={q.get("options", [])[:4]}')
    print()

# Get all verified aptitude questions
apt_qs = [q for q in verified_data if q.get('type') == 'aptitude']
print(f'Verified aptitude questions: {len(apt_qs)}')
for q in apt_qs[:5]:
    print(f'  id={q.get("id")}, topic={q.get("topic")}, sub_topic={q.get("sub_topic")}')
    print(f'  title={q.get("title", "")[:80]}')
    print(f'  correct_answer={q.get("correct_answer")}')
    print(f'  options={q.get("options", [])[:4]}')
    print()

# Get all verified logical questions
log_qs = [q for q in verified_data if q.get('type') == 'logical']
print(f'Verified logical questions: {len(log_qs)}')
for q in log_qs[:5]:
    print(f'  id={q.get("id")}, topic={q.get("topic")}, sub_topic={q.get("sub_topic")}')
    print(f'  title={q.get("title", "")[:80]}')
    print(f'  correct_answer={q.get("correct_answer")}')
    print(f'  options={q.get("options", [])[:4]}')
    print()
