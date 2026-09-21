with open('backend/app/data/behavioral_question_bank.py', 'r', encoding='utf-8') as f:
    content = f.read()
count = content.count('"id":')
print('Behavioral questions in file:', count)
