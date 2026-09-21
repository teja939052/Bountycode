import json

with open('questions_trusted.json', 'r', encoding='utf-8') as f:
    trusted = json.load(f)

aptitude_qs = [q for q in trusted if q.get('type') == 'aptitude']
coding_qs = [q for q in trusted if q.get('type') == 'coding']

print(f'=== APTITUDE QUESTIONS ({len(aptitude_qs)}) ===')
for i in [0, 50, 100, 150, 200, 250]:
    if i >= len(aptitude_qs):
        break
    q = aptitude_qs[i]
    print(f'\n--- Aptitude {i} ---')
    print(f'  topic: {q.get("topic")}')
    print(f'  pattern: {q.get("pattern")}')
    print(f'  question: {str(q.get("question", ""))[:120]}')
    print(f'  mental_model: {str(q.get("mental_model", ""))[:100]}')
    print(f'  solution: {str(q.get("solution", ""))[:100]}')
    print(f'  test_cases: {q.get("test_cases")}')
    print(f'  constraints: {q.get("constraints")}')
    print(f'  explanation: {str(q.get("explanation", ""))[:100]}')

# Check TCS bank
with open('tcs_nqt_questions.json', 'r', encoding='utf-8') as f:
    tcs = json.load(f)

print(f'\n\n=== TCS NQT QUESTIONS ({len(tcs)}) ===')
for i in [0, 100, 200, 300]:
    if i >= len(tcs):
        break
    q = tcs[i]
    print(f'\n--- TCS {i} ---')
    print(f'  type: {q.get("type")}')
    print(f'  topic: {q.get("topic")}')
    print(f'  question: {str(q.get("question", q.get("question_title", "")))[:100]}')
    print(f'  has solution: {bool(q.get("solution"))}')
    print(f'  has explanation: {bool(q.get("explanation"))}')
    print(f'  test_cases: {len(q.get("test_cases", []))}')
    print(f'  hidden_test_cases: {len(q.get("hidden_test_cases", []))}')
