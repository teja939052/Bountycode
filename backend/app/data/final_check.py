import app.services.question_store as qs

qs._loaded = False
qs.load_all()

# The verified MCQs are in the store with source_bank="tcs_nqt_all"
# because my verification script set that. Let's check serveability.
total = qs.count_documents()
tcs_all = qs.count_documents({"company": {"$in": ["TCS"]}})
tcs_servable = qs.count_documents({
    "company": {"$in": ["TCS"]},
    "trust_status": {"$in": ["verified", "automated_checked", "reviewed"]},
})

print(f"Total questions: {total}")
print(f"TCS questions: {tcs_all}")
print(f"TCS serveable (verified+): {tcs_servable}")

# Check source_bank distribution for TCS serveable
from collections import Counter
sources = Counter()
for q in qs._questions:
    if 'TCS' in (q.get('companies') or []):
        status = str(q.get('trust_status', '')).lower()
        if status in ('verified', 'automated_checked', 'reviewed'):
            sources[q.get('source_bank')] += 1

print('\nTCS serveable by source_bank:')
for src, count in sources.most_common(10):
    print(f'  {src}: {count}')

# Get a sample
mcq = qs.find_one_verified({"source_bank": "tcs_nqt_all"})
if mcq:
    print('\nMCQ sample:')
    print('  id:', mcq.get('id'))
    print('  type:', mcq.get('type'))
    print('  trust_status:', mcq.get('trust_status'))
    print('  question:', str(mcq.get('question') or '')[:60])
    print('  options:', mcq.get('options'))
    print('  correct_answer:', mcq.get('correct_answer'))
