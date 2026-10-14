import sys
sys.path.insert(0, ".")
import logging
logging.disable(logging.CRITICAL)
import app.services.question_store as qs

qs.load_all()

# Check if frequency-tagged questions are servable
high_freq_qs = [q for q in qs._questions if q.get("frequency", 0) >= 50]
print(f"High frequency questions: {len(high_freq_qs)}")
print(f"Servable: {sum(1 for q in high_freq_qs if qs._is_servable(q))}")
print(f"Trust status: {qs._questions[0].get('trust_status')}")

# Check what makes them non-servable
not_servable = [q for q in high_freq_qs if not qs._is_servable(q)]
print(f"Not servable: {len(not_servable)}")
if not_servable:
    sample = not_servable[0]
    print(f"Sample: {sample.get('id')}")
    print(f"  trust_status: {sample.get('trust_status')}")
    print(f"  type: {sample.get('type')}")
    print(f"  has_test_cases: {bool(sample.get('test_cases'))}")
    print(f"  has_examples: {bool(sample.get('examples'))}")
