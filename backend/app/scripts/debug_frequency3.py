import sys
sys.path.insert(0, ".")
import logging
logging.disable(logging.CRITICAL)
import app.services.question_store as qs

qs.load_all()

# Check what the frequency field represents
print("Frequency field analysis:")
print(f"Total questions: {len(qs._questions)}")
print(f"Questions with frequency=0: {sum(1 for q in qs._questions if q.get('frequency') == 0)}")
print(f"Questions with frequency>0: {sum(1 for q in qs._questions if q.get('frequency', 0) > 0)}")

# Check distribution
from collections import Counter
freq_counts = Counter(q.get("frequency") for q in qs._questions)
print(f"\nTop 20 frequency values:")
for freq, count in freq_counts.most_common(20):
    print(f"  {freq}: {count} questions")

# Check if frequency correlates with company
print("\nSample questions with high frequency:")
high_freq_qs = [q for q in qs._questions if q.get("frequency", 0) >= 90][:5]
for q in high_freq_qs:
    print(f"  {q.get('id')}: freq={q.get('frequency')}, companies={q.get('companies')}, topic={q.get('topic')}")

# Check if frequency correlates with topic
print("\nFrequency by topic (top 10):")
topic_freq = {}
for q in qs._questions:
    topic = q.get("topic", "unknown")
    freq = q.get("frequency", 0)
    if topic not in topic_freq:
        topic_freq[topic] = []
    topic_freq[topic].append(freq)

avg_freq_by_topic = {}
for topic, freqs in topic_freq.items():
    avg_freq_by_topic[topic] = sum(freqs) / len(freqs)

top_topics = sorted(avg_freq_by_topic.items(), key=lambda x: x[1], reverse=True)[:10]
for topic, avg_freq in top_topics:
    count = len(topic_freq[topic])
    print(f"  {topic}: avg={avg_freq:.1f}, count={count}")
