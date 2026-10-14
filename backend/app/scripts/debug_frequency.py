import sys
sys.path.insert(0, ".")
import logging
logging.disable(logging.CRITICAL)
import app.services.question_store as qs

qs.load_all()

# Check questions with frequency tag
high_freq = [q for q in qs._questions if q.get("frequency") == "high"]
print(f"Total high frequency questions: {len(high_freq)}")

# Check TCS high frequency
tcs_high = [q for q in high_freq if "tcs" in [c.lower() for c in q.get("companies", [])]]
print(f"TCS high frequency: {len(tcs_high)}")

# Check a sample
if tcs_high:
    sample = tcs_high[0]
    print(f"Sample: {sample.get('id')}")
    print(f"  companies: {sample.get('companies')}")
    print(f"  frequency: {sample.get('frequency')}")
    print(f"  trust_status: {sample.get('trust_status')}")
    print(f"  servable: {qs._is_servable(sample)}")

# Check all frequencies
from collections import Counter
freq_counts = Counter(q.get("frequency") for q in qs._questions)
print(f"\nAll frequencies: {dict(freq_counts)}")
