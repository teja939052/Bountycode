import sys
sys.path.insert(0, ".")
import logging
logging.disable(logging.CRITICAL)
from app.services.company_prep_service import get_most_asked_questions

# Test the new function
questions = get_most_asked_questions('tcs', 'high', 5)
print(f'TCS high-frequency questions: {len(questions)}')
for q in questions[:3]:
    title = q.get("question_title") or q.get("question", "")[:60]
    print(f'  - {q.get("id")}: {title}')
    print(f'    frequency: {q.get("frequency")}')

# Check counts by company and frequency
for company in ['tcs', 'infosys', 'wipro', 'cognizant', 'capgemini', 'accenture']:
    for freq in ['high', 'medium', 'low']:
        count = len(get_most_asked_questions(company, freq, 100))
        print(f'{company.upper()} {freq}: {count} questions available')
