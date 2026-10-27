import os, re
archive_dir = 'frontend/src/services/api/archive'
archived = {f.replace('.ts','') for f in os.listdir(archive_dir) if f.endswith('.ts')}
refs = []
for root, dirs, files in os.walk('frontend/src'):
    if 'archive' in root or 'node_modules' in root:
        continue
    for f in files:
        if not f.endswith('.tsx') and not f.endswith('.ts'):
            continue
        path = os.path.join(root, f)
        with open(path, 'r', encoding='utf-8') as fh:
            lines = fh.readlines()
        for i, line in enumerate(lines, 1):
            if not line.strip().startswith('import '):
                continue
            if 'from' not in line:
                continue
            parts = line.split('from')
            if len(parts) < 2:
                continue
            mod = parts[1].strip().strip('"').strip("'").strip(';')
            name = mod.split('/')[-1].replace('.ts','')
            if name in archived:
                refs.append((os.path.relpath(path, 'frontend/src'), i, name))
for item in refs:
    print(f'{item[0]}:{item[1]} -> {item[2]}')
