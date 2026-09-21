#!/usr/bin/env python3
import subprocess

result = subprocess.run(
    ['git', 'show', 'HEAD:backend/app/data/interview_question_bank.py'],
    capture_output=True
)
text = result.stdout.decode('utf-8', errors='replace')
print('Has INTERVIEW_QUESTIONS:', 'INTERVIEW_QUESTIONS' in text)
print('Has COMPANY_QUESTIONS:', 'COMPANY_QUESTIONS' in text)
print('File length:', len(text))

# Find all top-level assignments
import re
assignments = re.findall(r'^([A-Z_]+)\s*=', text, re.MULTILINE)
print('Top-level assignments:', assignments[:20])
