import re
with open('app/data/companies_2026_2027.py', 'r') as f:
    content = f.read()

ids = re.findall(r'"id": "([^"]+)"', content)
print('Company IDs:', ids)
print('Total:', len(ids))
