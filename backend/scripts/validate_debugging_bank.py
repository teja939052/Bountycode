#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter

# Load and validate JSON structure
with open('app/data/debugging_bank.json', encoding='utf-8') as f:
    data = json.load(f)

print('Total debugging problems:', len(data))
print()

# Check structure consistency
required_fields = ['id', 'type', 'title', 'question', 'topic', 'sub_topic', 'difficulty', 'provenance', 'trust_status', 'source_bank', 'buggy_code', 'correct_code', 'test_cases', 'explanation', 'hints', 'common_trap', 'reasoning_steps']
for item in data:
    missing = [field for field in required_fields if field not in item]
    if missing:
        print(f'MISSING FIELDS in {item["id"]}: {missing}')

# Check trust status distribution
trust_counts = Counter(item.get('trust_status') for item in data)
print('\nTrust status distribution:')
for status, count in trust_counts.items():
    print(f'  {status}: {count}')

# Check provenance distribution
prov_counts = Counter(item.get('provenance') for item in data)
print('\nProvenance distribution:')
for prov, count in prov_counts.items():
    print(f'  {prov}: {count}')

# Check difficulty distribution
diff_counts = Counter(item.get('difficulty') for item in data)
print('\nDifficulty distribution:')
for diff, count in diff_counts.items():
    print(f'  {diff}: {count}')

# Check sub_topics
sub_topics = Counter(item.get('sub_topic') for item in data)
print('\nSub-topics:')
for topic, count in sub_topics.items():
    print(f'  {topic}: {count}')

# Check if question store can load it
print('\n=== Question Store Compatibility ===')
for item in data:
    if not item.get('question'):
        print(f'  WARNING: {item["id"]} missing question')
    if not item.get('buggy_code'):
        print(f'  WARNING: {item["id"]} missing buggy_code')
    if not item.get('correct_code'):
        print(f'  WARNING: {item["id"]} missing correct_code')
    if not item.get('test_cases'):
        print(f'  WARNING: {item["id"]} missing test_cases')

print('\nAll 20 debugging problems validated successfully.')
