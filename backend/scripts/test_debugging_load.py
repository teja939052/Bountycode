#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from app.services.question_store import _load_extra_bank

questions = []
_load_extra_bank(questions, ['debugging_bank.json'])
print(f'QuestionStore loaded {len(questions)} debugging problems')

# Show IDs
for q in questions:
    if 'debug' in q.get('id', ''):
        print(f'  {q["id"]}: {q.get("title", "")}')
