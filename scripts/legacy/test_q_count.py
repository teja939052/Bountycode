import sys
sys.path.insert(0, r"D:\Project-Fremen\backend")
from app.services.question_store import load_all
import json

questions = load_all()
print(f'Total loaded questions: {len(questions) if questions else 0}')

if questions:
    q = questions[0]
    print(f'First question type: {type(q)}')
    if isinstance(q, dict):
        print(f'First question keys: {list(q.keys())}')
        # Print relevant fields
        for k in ['topic', 'difficulty', 'company', 'pattern', 'role', 'question', 'answer', 'explanation']:
            if k in q:
                val = q[k]
                print(f'  {k}: {str(val)[:100] if val else None}')