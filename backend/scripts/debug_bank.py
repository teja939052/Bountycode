#!/usr/bin/env python3
import re

text = open('app/data/interview_question_bank.py', encoding='utf-8').read()
print('File size (chars):', len(text))
print('First 200 chars:')
print(text[:200])
print()

# Check for INTERVIEW_QUESTIONS vs COMPANY_QUESTIONS
if 'INTERVIEW_QUESTIONS' in text:
    print('Has INTERVIEW_QUESTIONS')
if 'COMPANY_QUESTIONS' in text:
    print('Has COMPANY_QUESTIONS')

# Count questions
if 'INTERVIEW_QUESTIONS' in text:
    ids = re.findall(r'"id":\s*"([^"]+)"', text)
    print(f'IDs found: {len(ids)}')
    print(f'Sample IDs: {ids[:5]}')

# Find the structure
if 'INTERVIEW_QUESTIONS' in text:
    match = re.search(r'INTERVIEW_QUESTIONS\s*=\s*\[', text)
    if match:
        print(f'INTERVIEW_QUESTIONS starts at position: {match.start()}')
        print('Context:')
        print(text[match.start():match.start()+500])
