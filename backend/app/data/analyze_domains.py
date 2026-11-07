import json
from collections import Counter

with open('questions_trusted.json', 'r', encoding='utf-8') as f:
    trusted = json.load(f)

with open('verified_placement_questions.json', 'r', encoding='utf-8') as f:
    verified = json.load(f)

# Domain coverage analysis
print('=== DOMAIN COVERAGE ANALYSIS ===')

# Combine all questions
all_qs = []
for q in trusted:
    all_qs.append({'bank': 'trusted', **q})
for q in verified:
    all_qs.append({'bank': 'verified', **q})

# Check by domain
domains = {
    'DSA/Coding': lambda q: q.get('type') == 'coding',
    'Aptitude (quantitative)': lambda q: q.get('type') == 'aptitude' and q.get('topic') in ['aptitude', 'math', 'percentages', 'time-work', 'profit-loss'],
    'Logical Reasoning': lambda q: q.get('type') == 'logical' or (q.get('type') == 'aptitude' and q.get('topic') == 'logical'),
    'Verbal Ability': lambda q: q.get('type') == 'verbal' or (q.get('type') == 'aptitude' and q.get('topic') == 'verbal'),
    'CS Fundamentals': lambda q: q.get('type') == 'cs_fundamentals' or q.get('topic') in ['os', 'dbms', 'networking', 'oops'],
    'Behavioral/HR': lambda q: 'behavioral' in q.get('topic', '').lower() or 'hr' in q.get('topic', '').lower(),
    'SQL/Databases': lambda q: 'sql' in q.get('topic', '').lower() or 'database' in q.get('topic', '').lower(),
    'System Design': lambda q: 'system_design' in q.get('pattern', '').lower() or 'design' in q.get('topic', '').lower(),
    'Debugging': lambda q: 'debug' in q.get('topic', '').lower() or 'debug' in q.get('pattern', '').lower(),
    'Project/Software Engineering': lambda q: 'project' in q.get('topic', '').lower() or 'engineering' in q.get('topic', '').lower(),
}

for domain, predicate in domains.items():
    count = sum(1 for q in all_qs if predicate(q))
    print(f'{domain}: {count} questions')

# Check specific missing domains
missing_domains = [
    'SQL', 'behavioral', 'system_design', 'debugging', 'project',
    'angular', 'react', 'node', 'python', 'java', 'javascript',
    'api', 'rest', 'git', 'docker', 'kubernetes', 'cloud',
    'machine_learning', 'ai', 'data_science'
]

print(f'\n=== MISSING DOMAINS ===')
for domain in missing_domains:
    count = sum(1 for q in all_qs if domain in q.get('topic', '').lower() or domain in q.get('pattern', '').lower())
    if count == 0:
        print(f'  MISSING: {domain}')

# Check depth of coding questions
print(f'\n=== CODING QUESTION DEPTH ===')
coding_qs = [q for q in all_qs if q.get('type') == 'coding']
print(f'Total coding: {len(coding_qs)}')

# Check for specific advanced patterns
advanced_patterns = ['dp', 'graph', 'tree', 'trie', 'segment_tree', 'fenwick', 'bitmask', 'math', 'greedy', 'backtracking']
for pattern in advanced_patterns:
    count = sum(1 for q in coding_qs if pattern in q.get('pattern', '').lower())
    if count > 0:
        print(f'  {pattern}: {count}')

# Check difficulty distribution
print(f'\n=== DIFFICULTY DISTRIBUTION ===')
diff = Counter(q.get('difficulty', 'untagged') for q in coding_qs)
print(f'Coding: {dict(diff)}')

diff_all = Counter(q.get('difficulty', 'untagged') for q in all_qs)
print(f'All: {dict(diff_all)}')
