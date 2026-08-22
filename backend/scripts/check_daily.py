import re
with open(r'D:\Project-Fremen\backend\app\routes\daily_challenge.py', encoding='utf-8') as f:
    content = f.read()
prefixes = re.findall(r'APIRouter\(prefix="([^"]+)"', content)
routes = re.findall(r'@router\.(get|post|put|delete|patch)\("([^"]+)"', content)
print('Prefixes:', prefixes)
print('Routes:', routes)
