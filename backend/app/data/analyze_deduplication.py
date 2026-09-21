import json
from collections import Counter

# Check verified_placement_questions.json for duplication
with open('verified_placement_questions.json', 'r', encoding='utf-8') as f:
    verified = json.load(f)

print(f'=== VERIFIED PLACEMENT QUESTIONS ===')
print(f'Total: {len(verified)}')

# Check duplicates
questions_text = [q.get('question', q.get('title', '')) for q in verified]
unique_questions = set(questions_text)
print(f'Unique question texts: {len(unique_questions)}')
print(f'Duplication rate: {(len(verified) - len(unique_questions)) / len(verified) * 100:.1f}%')

# Check by type
for qtype in ['coding', 'aptitude', 'logical', 'verbal', 'cs_fundamentals']:
    qs = [q for q in verified if q.get('type') == qtype]
    texts = [q.get('question', q.get('title', '')) for q in qs]
    unique = set(texts)
    print(f'{qtype}: {len(qs)} total, {len(unique)} unique, {(len(qs)-len(unique))/len(qs)*100:.0f}% dupes')

# Check TCS bank
with open('tcs_nqt_questions.json', 'r', encoding='utf-8') as f:
    tcs = json.load(f)

print(f'\n=== TCS NQT QUESTIONS ===')
print(f'Total: {len(tcs)}')
tcs_texts = [q.get('question', q.get('question_title', '')) for q in tcs]
tcs_unique = set(tcs_texts)
print(f'Unique: {len(tcs_unique)}')
print(f'Duplication: {(len(tcs)-len(tcs_unique))/len(tcs)*100:.1f}%')

# Check Infosys bank
with open('infosys_questions.json', 'r', encoding='utf-8') as f:
    infosys = json.load(f)

print(f'\n=== INFOSYS QUESTIONS ===')
print(f'Total: {len(infosys)}')
inf_texts = [q.get('question', q.get('question_title', '')) for q in infosys]
inf_unique = set(inf_texts)
print(f'Unique: {len(inf_unique)}')
print(f'Duplication: {(len(infosys)-len(inf_unique))/len(infosys)*100:.1f}%')

# Check what topics are covered in verified bank
print(f'\n=== VERIFIED BANK TOPICS ===')
topics = Counter(q.get('topic', 'untagged') for q in verified)
for t, c in topics.most_common(20):
    print(f'  {t}: {c}')

# Check patterns in verified bank
patterns = Counter(q.get('pattern', 'untagged') for q in verified)
print(f'\nVerified patterns: {dict(patterns)}')
