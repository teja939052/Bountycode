import json

with open('backend/app/content/questions/curated/learning_objects.json', 'r') as f:
    data = json.load(f)

from collections import Counter
types = Counter(q.get('type', 'unknown') for q in data)
print('Question types:', dict(types))

# Check if questions have testcases
coding_with_tests = [q for q in data if q.get('type') == 'coding' and q.get('testcases')]
print(f'Coding with testcases: {len(coding_with_tests)}')
for q in coding_with_tests[:2]:
    print(f'  id={q.get("id")}, topic={q.get("topic")}')
    print(f'  testcases={len(q.get("testcases", []))}')
    if q.get('testcases'):
        print(f'  sample: {q["testcases"][0]}')
    print()

# Check MCQs
mcq_qs = [q for q in data if q.get('type') in ('mcq', 'aptitude', 'verbal', 'logical')]
print(f'MCQ-type questions: {len(mcq_qs)}')
for q in mcq_qs[:3]:
    print(f'  id={q.get("id")}, type={q.get("type")}, topic={q.get("topic")}')
    print(f'  options={q.get("options", [])[:2]}')
    print(f'  correct_answer={q.get("correct_answer")}')
    print()
