content = open("D:/Project-Fremen/backend/app/services/lessons/python.py", "r").read()
count = content.count('"id":')
print(f'Total "id": occurrences: {count}')
import re
ids = re.findall(r'"id":\s*"([^"]+)"', content)
print(f'Total lesson IDs found: {len(ids)}')
print(f'First 5 IDs: {ids[:5]}')
print(f'Last 5 IDs: {ids[-5:]}')