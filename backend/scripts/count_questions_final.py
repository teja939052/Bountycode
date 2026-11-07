import os, re

root = 'D:\\Project-Fremen'
total = 0

# Main interview bank (already confirmed 2000)
path = os.path.join(root, 'backend', 'app', 'data', 'interview_question_bank.py')
content = open(path, encoding='utf-8').read()
qs = len(re.findall("question['\"]\s*:", content))
total += qs
print(f"interview_question_bank.py: {qs}")

# All seed files in backend/
for f in sorted(os.listdir(os.path.join(root, 'backend'))):
    if f.startswith('seed_') and f.endswith('.py'):
        path = os.path.join(root, 'backend', f)
        content = open(path, encoding='utf-8').read()
        qs = len(re.findall("question['\"]\s*:", content))
        ts = len(re.findall("title['\"]\s*:", content))
        total += qs
        if qs > 0 or ts > 0:
            print(f"{f}: {qs} questions, {ts} titles")

# data files
for f in sorted(os.listdir(os.path.join(root, 'backend', 'app', 'data'))):
    if f.endswith('.py') and f not in ('__init__.py', 'interview_question_bank.py'):
        path = os.path.join(root, 'backend', 'app', 'data', f)
        content = open(path, encoding='utf-8').read()
        qs = len(re.findall("question['\"]\s*:", content))
        ts = len(re.findall("title['\"]\s*:", content))
        total += qs
        if qs > 0 or ts > 0:
            print(f"data/{f}: {qs} questions, {ts} titles")

# gen_questions.py
path = os.path.join(root, 'backend', 'gen_questions.py')
if os.path.exists(path):
    content = open(path, encoding='utf-8').read()
    qs = len(re.findall("question['\"]\s*:", content))
    total += qs
    if qs > 0:
        print(f"gen_questions.py: {qs}")

print(f"\nTOTAL question keys across all files: {total}")
