import sys
sys.path.insert(0, '.')
import os
os.environ['MONGODB_URL'] = 'mongodb+srv://bhanu:1234@cluster0.fgh4i8m.mongodb.net/?appName=Cluster0'

# 1. Test question_store
from app.services import question_store
question_store.load_all()
total = question_store.count_documents()
assert total > 0, f"Expected questions, got {total}"
print(f"[OK] QuestionStore loaded {total} questions")

# 2. Test filter retrieval
filters = question_store.get_filters()
assert filters['companies'], "Expected companies"
assert filters['topics'], "Expected topics"
print(f"[OK] Filters: {len(filters['companies'])} companies, {len(filters['topics'])} topics")

# 3. Test find with filters
results = question_store.find({'type': 'coding', 'difficulty': 'easy'}).limit(2).to_list()
assert len(results) == 2, f"Expected 2 results, got {len(results)}"
print(f"[OK] Find+filter returns results")

# 4. Test find_one
q = question_store.find_one({'id': 'q_000000'})
if not q:
    q = question_store.find_one({'type': 'coding'})
assert q, "find_one should return a question"
print(f"[OK] find_one works: {q['question'][:50]}...")

# 5. Test distinct
companies = question_store.distinct('company')
assert len(companies) > 0
print(f"[OK] distinct() returns {len(companies)} companies")

# 6. Test cross-field filter
q_topic = question_store.find_one({'topic': 'Dynamic Programming'})
assert q_topic
print(f"[OK] Filter by topic works")

# 7. Test count
types = question_store.count_documents({'type': 'coding'})
assert types > 0
print(f"[OK] Count by type: {types} coding questions")

# 8. Verify route module imports
from app.routes import questions as questions_route
print(f"[OK] Questions route module loaded")

# 9. Test async cursor
import asyncio
async def test_cursor():
    cursor = question_store.find({'type': 'coding'}).limit(3)
    count = 0
    async for q in cursor:
        count += 1
    assert count == 3, f"Expected 3, got {count}"
    print(f"[OK] Async iteration works (got {count} items)")

asyncio.run(test_cursor())

print("\n=== ALL CHECKS PASSED ===")
