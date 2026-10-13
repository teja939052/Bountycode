import re

with open(r'D:\Project-Fremen\backend\app\data\companies_2026_2027.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract IDs and names
id_name = re.findall(r'"id": "([^"]+)",\s*"name": "([^"]+)"', content)
print('Total companies:', len(id_name))

# Extract focus_areas blocks
focus_areas = re.findall(r'"focus_areas": \[([^\]]+)\]', content)
print('Focus area blocks:', len(focus_areas))

# Map company id to focus_areas by position
companies = []
for i, (cid, name) in enumerate(id_name):
    areas = []
    if i < len(focus_areas):
        areas = [a.strip().strip('"') for a in focus_areas[i].split(',')]
    companies.append({'id': cid, 'name': name, 'focus_areas': areas})

for c in companies:
    print(c['id'], '|', c['name'], '|', ', '.join(c['focus_areas']))
