import sys
sys.path.insert(0, ".")
import logging
logging.disable(logging.CRITICAL)
import app.services.question_store as qs

qs.load_all()

# Check questions with frequency tag - what are the actual values?
sample_qs = qs._questions[:10]
for q in sample_qs:
    if q.get("frequency") is not None:
        print(f"Sample: {q.get('id')}")
        print(f"  frequency: {q.get('frequency')} (type: {type(q.get('frequency'))})")
        print(f"  topic: {q.get('topic')}")
        print(f"  companies: {q.get('companies')}")
        break

# Check if frequency is already populated
has_freq = sum(1 for q in qs._questions if q.get("frequency") is not None)
print(f"\nQuestions with frequency field: {has_freq}")

# Check unique frequency values
from collections import Counter
freq_values = Counter(str(q.get("frequency")) for q in qs._questions if q.get("frequency") is not None)
print(f"Unique frequency values: {dict(freq_values)}")
