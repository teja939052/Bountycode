import re, os

files = [
    'D:/Project-Fremen/backend/seed_questions.py',
    'D:/Project-Fremen/backend/scripts/seed_questions.py',
    'D:/Project-Fremen/backend/scripts/seed_striver.py',
    'D:/Project-Fremen/backend/seed_all_doubled.py',
]

total = 0
for f in files:
    if os.path.exists(f):
        with open(f, 'rb') as fh:
            c = fh.read().decode('utf-8', errors='replace')
        q_count = c.count('"question_title"')
        size = len(c)
        print(f'{os.path.basename(f)}: {q_count} questions ({size:,} bytes)')
        total += q_count

print(f'\nTotal questions across all seed files: {total}')