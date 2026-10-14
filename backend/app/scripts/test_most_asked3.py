import sys
sys.path.insert(0, ".")
import logging
logging.disable(logging.CRITICAL)
from app.services.company_prep_service import get_most_asked_questions

# Test the updated function
for company in ['tcs', 'infosys', 'wipro', 'cognizant', 'capgemini', 'accenture']:
    for freq in ['high', 'medium', 'low']:
        questions = get_most_asked_questions(company, freq, 5)
        if questions:
            sample = questions[0]
            title = sample.get("question_title") or sample.get("question", "")[:60]
            print(f"{company.upper()} {freq}: {len(questions)} questions, top: {title} (freq={sample.get('frequency')})")
        else:
            print(f"{company.upper()} {freq}: 0 questions")
