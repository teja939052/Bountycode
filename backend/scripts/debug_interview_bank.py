#!/usr/bin/env python3
import re

lines = open('app/data/interview_question_bank.py', encoding='utf-8').readlines()
print(f'Total lines: {len(lines)}')

# Find INTERVIEW_QUESTIONS start
for i, line in enumerate(lines):
    if 'INTERVIEW_QUESTIONS = [' in line:
        print(f'Found at line {i}: {line.strip()}')
        break

# Count question blocks by looking for 'id': patterns at start of line (indented)
id_count = sum(1 for line in lines if re.search(r'^\s+"id":', line))
print(f'Lines with id: {id_count}')

# Check first few lines of file
print('First 5 lines:')
for i in range(min(5, len(lines))):
    print(f'  {i}: {lines[i].rstrip()}')

# Check lines around question 40 (the first placeholder)
for i, line in enumerate(lines):
    if 'int_q_0040' in line:
        print(f'\nFound int_q_0040 at line {i}:')
        for j in range(max(0, i-2), min(len(lines), i+10)):
            print(f'  {j}: {lines[j].rstrip()}')
        break
