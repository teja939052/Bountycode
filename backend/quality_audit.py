import sys, io
sys.path.insert(0, '.')
from app.services import question_store
from collections import Counter, defaultdict

# Suppress logging
import logging
logging.getLogger('app.services.question_store').setLevel(logging.ERROR)

question_store.load_all()

from app.services.question_standard import score_against_standard, tier_for_score

servable = [q for q in question_store._questions if question_store._is_servable(q)]
print(f"Total servable: {len(servable)}")

# Score all servable questions
scores = {'premium':0,'solid':0,'bronze':0}
q_scores = []
for q in servable:
    result = score_against_standard(q)
    score = result['score']
    tier = tier_for_score(score)
    scores[tier] += 1
    q_scores.append({
        'id': q.get('id'),
        'type': q.get('type'),
        'topic': q.get('topic'),
        'score': score,
        'tier': tier,
        'missing': [f['label'] for f in result['fields'] if not f['present']],
    })

print(f"\nSCORE DISTRIBUTION:")
print(f"  Premium (90+): {scores['premium']}")
print(f"  Solid (60-89): {scores['solid']}")
print(f"  Bronze (<60): {scores['bronze']}")

# Show lowest scoring questions
print()
print("LOWEST SCORED SERVABLE QUESTIONS (first 20):")
low_scores = sorted(q_scores, key=lambda x: x['score'])[:20]
for q in low_scores:
    print(f"  {q['id']} ({q['type']}, {q['topic']}): score={q['score']}, missing={q['missing']}")

# Show highest scoring questions
print()
print("HIGHEST SCORED SERVABLE QUESTIONS (first 20):")
high_scores = sorted(q_scores, key=lambda x: -x['score'])[:20]
for q in high_scores:
    print(f"  {q['id']} ({q['type']}, {q['topic']}): score={q['score']}, missing={q['missing']}")

# Missing fields breakdown
missing_fields_total = Counter()
for q in servable:
    result = score_against_standard(q)
    for f in result['fields']:
        if not f['present']:
            missing_fields_total[f['label']] += 1

print()
print("MISSING FIELDS ACROSS ALL SERVABLE QUESTIONS:")
for label,count in missing_fields_total.most_common():
    print(f"  {label}: {count} missing ({count/len(servable)*100:.1f}%)")

# Check for questions with no solution at all
print()
print("QUESTIONS WITH NO SOLUTION:")
no_solution = [q for q in servable if not (q.get('solution') or q.get('correct_answer') or q.get('correct_index') or q.get('rubric') or q.get('evaluation_criteria'))]
print(f"  Count: {len(no_solution)}")
for q in no_solution[:10]:
    print(f"  {q.get('id')} ({q.get('type')}, {q.get('topic')})")

# Check for empty question text
print()
print("QUESTIONS WITH EMPTY/MISSING QUESTION TEXT:")
no_question = [q for q in servable if not str(q.get('question','') or q.get('question_title','') or q.get('statement','')).strip()]
print(f"  Count: {len(no_question)}")
for q in no_solution[:10]:
    print(f"  {q.get('id')} ({q.get('type')}, {q.get('topic')})")
