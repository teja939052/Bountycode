import os
import re

SKIP_DIRS = {'node_modules', 'dist', 'build', '.git', 'venv', '__pycache__', '.next', '.vercel'}

for root, dirs, files in os.walk('frontend/src'):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for fname in files:
        if not fname.endswith(('.ts', '.tsx')):
            continue
        path = os.path.join(root, fname)
        if 'rename' in path or 'revert' in path or 'test' in path:
            continue
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            imports = re.findall(r'import\s+(\w+)\s+from\s+["\'][^"\']*["\']', content)
            if 'DiamondsBar' in imports:
                # Find all component usages in JSX
                usages = re.findall(r'<\s*(DiamondsBar|\w+Bar)', content)
                if usages and not all(u == 'DiamondsBar' for u in usages):
                    print(f'{path}: imports DiamondsBar but also uses {set(usages)}')
        except:
            pass
