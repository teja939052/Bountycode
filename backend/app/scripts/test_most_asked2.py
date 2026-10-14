import sys
sys.path.insert(0, ".")
import logging
logging.disable(logging.CRITICAL)
from app.services.company_prep_service import get_most_asked_questions

# Test the updated function
for company in ['tcs', 'infosys', 'wipro']:
    for freq in ['high', 'medium', 'low']:
        questions = get_most_asked_questions(company, freq, 5)
        if questions:
            print(f"{company.upper()} {freq}: {len(questions)} questions")
            sample = questions[0]
            print(f"  Sample: {sample.get('id')} (freq={sample.get('frequency')})")
