import os, re, sys

data_dir = os.path.dirname(os.path.abspath(__file__))

# 1. interview_question_bank.py - already counted 2000
fpath = os.path.join(data_dir, 'interview_question_bank.py')
if os.path.exists(fpath):
    content = open(fpath, encoding='utf-8').read()
    qcount = len(re.findall(r"['\"]question['\"]\s*:", content))
    print(f"interview_question_bank.py: {qcount} questions")

# 2. dsa_problems.py - check if it has actual data
fpath = os.path.join(data_dir, 'dsa_problems.py')
if os.path.exists(fpath):
    size = os.path.getsize(fpath)
    print(f"dsa_problems.py: {size} bytes")
    if size > 1000:
        content = open(fpath, encoding='utf-8').read()
        qcount = len(re.findall(r"['\"]question['\"]\s*:", content))
        tcount = len(re.findall(r"['\"]title['\"]\s*:", content))
        print(f"  -> {qcount} question keys, {tcount} title keys")

# 3. Seed files in backend/
seed_dir = os.path.dirname(data_dir)
for f in os.listdir(seed_dir):
    if f.startswith('seed_') and f.endswith('.py'):
        fpath = os.path.join(seed_dir, f)
        content = open(fpath, encoding='utf-8').read()
        qcount = len(re.findall(r"['\"]question['\"]\s*:", content))
        tcount = len(re.findall(r"['\"]title['\"]\s*:", content))
        print(f"{f}: {qcount} question keys, {tcount} title keys")

# 4. Also count curated_questions references in seed files
print()
print("--- Also checking questions.json / JSON data ---")
for f in os.listdir(seed_dir):
    if f.endswith('.json'):
        fpath = os.path.join(seed_dir, f)
        try:
            import json
            data = json.load(open(fpath, encoding='utf-8'))
            if isinstance(data, list):
                print(f"{f}: {len(data)} items")
            elif isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, list):
                        print(f"{f}[{k}]: {len(v)} items")
        except:
            pass
