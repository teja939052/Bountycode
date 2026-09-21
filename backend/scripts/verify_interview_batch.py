import sys
sys.path.insert(0, 'backend')
from app.services import question_store

question_store._loaded = False
question_store._questions = []
question_store.load_all()

total = question_store.count_documents()
int_qs = question_store.find({'type': 'interview'}).to_list()
print('Total questions:', total)
print('Interview questions:', len(int_qs))

for q in int_qs:
    print(q.get('id') + ':', q.get('topic'), '-', q.get('sub_topic'), '-', q.get('difficulty'))

ids = [q.get('id') for q in int_qs]
print('Unique IDs:', len(set(ids)), 'of', len(ids))

trust = {}
for q in int_qs:
    ts = q.get('trust_status', 'unknown')
    trust[ts] = trust.get(ts, 0) + 1
print('Trust:', trust)
