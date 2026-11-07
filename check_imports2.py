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
            for imp in imports:
                if imp.endswith('Bar') and imp not in ('ProgressBar', 'NavigationBar', 'ScrollBar', 'SearchBar', 'TabBar', 'BottomNav'):
                    usage = re.findall(r'<\s*' + re.escape(imp), content)
                    if not usage:
                        jsx_bars = re.findall(r'<\s*(\w+Bar)', content)
                        if jsx_bars:
                            print(f'{path}: imports {imp} but JSX uses {set(jsx_bars)}')
        except:
            pass
