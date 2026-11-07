import json
from collections import Counter

with open('questions_trusted.json', 'r', encoding='utf-8') as f:
    trusted = json.load(f)

aptitude_qs = [q for q in trusted if q.get('type') == 'aptitude']
coding_qs = [q for q in trusted if q.get('type') == 'coding']

print(f'=== APTITUDE DUPLICATION ANALYSIS ===')
print(f'Total aptitude: {len(aptitude_qs)}')

# Check for duplicate questions
questions_text = [q.get('question', '') for q in aptitude_qs]
unique_questions = set(questions_text)
print(f'Unique question texts: {len(unique_questions)}')
print(f'Duplication rate: {(len(aptitude_qs) - len(unique_questions)) / len(aptitude_qs) * 100:.1f}%')

# Show duplicates
dupes = {}
for q in aptitude_qs:
    text = q.get('question', '')
    dupes[text] = dupes.get(text, 0) + 1

duplicate_questions = [(text, count) for text, count in dupes.items() if count > 1]
print(f'\nDuplicate questions: {len(duplicate_questions)}')
for text, count in sorted(duplicate_questions, key=lambda x: -x[1])[:10]:
    print(f'  [{count}x] {text[:80]}')

# Check coding duplication
coding_texts = [q.get('question', '') for q in coding_qs]
unique_coding = set(coding_texts)
print(f'\n=== CODING DUPLICATION ===')
print(f'Total coding: {len(coding_qs)}')
print(f'Unique coding questions: {len(unique_coding)}')
print(f'Duplication rate: {(len(coding_qs) - len(unique_coding)) / len(coding_qs) * 100:.1f}%')

# Check pattern coverage in coding
patterns = Counter(q.get('pattern', 'untagged') for q in coding_qs)
print(f'\nCoding patterns: {dict(patterns.most_common(20))}')

# Check topics in coding
topics = Counter(q.get('topic', 'untagged') for q in coding_qs)
print(f'\nCoding topics: {dict(topics.most_common(15))}')

# Check for advanced topics
advanced_topics = ['dp', 'graph', 'tree', 'trie', 'segment_tree', 'fenwick', 'bitmask', 'math', 'greedy', 'backtracking']
for topic in advanced_topics:
    count = sum(1 for q in coding_qs if topic in q.get('topic', '').lower() or topic in q.get('pattern', '').lower())
    if count > 0:
        print(f'  Advanced topic {topic}: {count}')
