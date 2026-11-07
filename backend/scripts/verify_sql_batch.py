import sys, json
sys.path.insert(0, 'backend')
from app.services import question_store

question_store._loaded = False
question_store._questions = []
question_store.load_all()

total = question_store.count_documents()
sql_qs = question_store.find({'topic': 'sql'}).to_list()
print('Total questions:', total)
print('SQL questions:', len(sql_qs))

new_ids = ['sql-{:03d}'.format(i) for i in range(41, 55)]
for qid in new_ids:
    q = question_store.find_one({'id': qid})
    if not q:
        print('MISSING:', qid)
    else:
        print(qid + ':', q.get('sub_topic'), '-', q.get('difficulty'))

ids = [q.get('id') for q in sql_qs]
print('Unique IDs:', len(set(ids)), 'of', len(ids))

trust = {}
for q in sql_qs:
    ts = q.get('trust_status', 'unknown')
    trust[ts] = trust.get(ts, 0) + 1
print('Trust:', trust)

diffs = {}
for q in sql_qs:
    d = q.get('difficulty')
    diffs[d] = diffs.get(d, 0) + 1
print('Difficulty:', diffs)
