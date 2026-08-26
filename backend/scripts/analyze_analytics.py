import re
p = r'D:\Project-Fermen/backend/app/routes/analytics.py'
f = open(p, encoding='utf-8', errors='replace').read()
print('LINES:', len(f.splitlines()))
for m in re.finditer(r'@router\.(get|post)\("([^"]+)"', f):
    print('ROUTE:', m.group(1), m.group(2))
print('--- has track handler body ---')
i = f.find('/track')
if i >= 0:
    print(f[i-20:i+400])
