import re
from collections import Counter

text = open('app/data/interview_question_bank.py').read()
ids = re.findall(r'"id":\s*"([^"]+)"', text)
print('Total questions:', len(ids))
prefixes = Counter(id.split('_')[0] for id in ids)
print('Prefixes:', dict(prefixes))
print('First 10:', ids[:10])
