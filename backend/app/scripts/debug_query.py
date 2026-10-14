import sys
sys.path.insert(0, ".")
import logging
logging.disable(logging.CRITICAL)
import app.services.question_store as qs

qs.load_all()

# Manually test the query
company = "tcs"
query = {"companies": {"$in": [company]}}
cursor = qs.find(query)
print(f"Before prefer_verified: {len(cursor._all)} questions")

cursor.prefer_verified()
print(f"After prefer_verified: {len(cursor._all)} questions")

pool = cursor.to_list()[:500]
print(f"After to_list()[:500]: {len(pool)} questions")

if pool:
    print(f"Sample: {pool[0].get('id')}")
    print(f"  frequency: {pool[0].get('frequency')}")
