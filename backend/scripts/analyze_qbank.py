import json
with open('D:\\Project-Fremen\\backend\\app\\data\\interview_question_bank.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the question bank dict - it starts with INTERVIEW_QUESTION_BANK = {
# and ends with the last }
import re

# Find all question texts and their IDs
questions = re.findall(r'"id":\s*"([^"]+)".*?"question":\s*"([^"]+)"', content, re.DOTALL)
print(f"Total question entries found: {len(questions)}")

# Count unique IDs
ids = [q[0] for q in questions]
unique_ids = set(ids)
print(f"Unique IDs: {len(unique_ids)}")

# Count unique question texts
texts = [q[1] for q in questions]
unique_texts = set(texts)
print(f"Unique question texts: {len(unique_texts)}")

# Count fill- IDs
fill_ids = [q[0] for q in questions if q[0].startswith('fill-')]
print(f"Fill- IDs count: {len(fill_ids)}")

# Non-fill IDs
non_fill = [q for q in questions if not q[0].startswith('fill-')]
print(f"Non-fill entries: {len(non_fill)}")
non_fill_texts = set(q[1] for q in non_fill)
print(f"Non-fill unique texts: {len(non_fill_texts)}")

# Duplicates in non-fill
non_fill_text_list = [q[1] for q in non_fill]
from collections import Counter
dupes = [(text, count) for text, count in Counter(non_fill_text_list).items() if count > 1]
print(f"Non-fill duplicate texts: {len(dupes)}")
for text, count in sorted(dupes, key=lambda x: -x[1])[:10]:
    print(f"  '{text[:80]}...' appears {count} times")
