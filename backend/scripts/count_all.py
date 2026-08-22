import os, re, ast, sys

data_dir = os.path.dirname(os.path.abspath(__file__))

# dsa_problems.py
fpath = os.path.join(data_dir, 'dsa_problems.py')
if os.path.exists(fpath):
    content = open(fpath, encoding='utf-8').read()
    # count PROBlEMS = [...] entries by counting opening braces that start a dict
    entries = re.findall(r'^\s*\{', content, re.MULTILINE)
    print(f'dsa_problems.py: ~{len(entries)} problem dicts')
    titles = re.findall(r'["\']title["\']\s*:\s*["\']([^"\']+)["\']', content)
    print(f'  titles found: {len(titles)}')

# seed_questions files
seed_dir = os.path.dirname(data_dir)  # backend/
for f in os.listdir(seed_dir):
    if f.startswith('seed_') and f.endswith('.py'):
        fpath = os.path.join(seed_dir, f)
        content = open(fpath, encoding='utf-8').read()
        qcount = len(re.findall(r"['\"]question['\"]\s*:", content))
        tcount = len(re.findall(r"['\"]title['\"]\s*:", content))
        print(f'{f}: {qcount} question keys, {tcount} title keys')

# curriculum files
for f in ['curriculum.py', 'curriculum_50_levels.py', 'curriculum_enrichment.py']:
    fpath = os.path.join(data_dir, f)
    if os.path.exists(fpath):
        content = open(fpath, encoding='utf-8').read()
        qcount = len(re.findall(r"['\"]question['\"]\s*:", content))
        tcount = len(re.findall(r"['\"]title['\"]\s*:", content))
        print(f'{f}: {qcount} question keys, {tcount} title keys')
