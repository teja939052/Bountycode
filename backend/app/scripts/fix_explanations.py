import re
with open('add_service_company_questions.py', 'r') as f:
    content = f.read()
# Remove explanation='...' keyword args - already passed positionally
content = re.sub(r"\s+explanation='[^']+',\n", '\n', content)
content = re.sub(r'\s+explanation="[^"]+",\n', '\n', content)
with open('add_service_company_questions.py', 'w') as f:
    f.write(content)
print('Removed duplicate explanation kwargs')
