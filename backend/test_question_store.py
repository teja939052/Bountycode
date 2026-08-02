import sys
sys.path.insert(0, 'backend')
from app.services import question_store

question_store.load_all()

total = question_store.count_documents()
print(f"Total questions loaded: {total}")

for t in ['coding', 'aptitude', 'behavioral', 'system_design', 'hr']:
    c = question_store.count_documents({'type': t})
    if c:
        print(f"  {t}: {c}")

for d in ['easy', 'medium', 'hard']:
    c = question_store.count_documents({'difficulty': d})
    if c:
        print(f"  {d}: {c}")

filters = question_store.get_filters()
print(f"Companies: {len(filters['companies'])}")
print(f"Topics: {len(filters['topics'])}")
print(f"Types: {filters['types']}")
print(f"Difficulties: {filters['difficulties']}")

q = question_store.find_one({'type': 'coding', 'difficulty': 'easy'})
if q:
    print(f"Sample: id={q['id']}, question={q['question'][:60]}...")

results = question_store.find({'type': 'coding'}).limit(3).to_list()
print(f"Browse coding limit 3: {len(results)} results")

all_q = question_store.find().to_list()
print(f"All questions: {len(all_q)}")

# Test distinct
companies = question_store.distinct('company')
print(f"Distinct companies: {len(companies)} (first 5: {companies[:5]})")
