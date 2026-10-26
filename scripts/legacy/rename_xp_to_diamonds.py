import os
import re
import sys

SKIP_DIRS = {'node_modules', 'dist', 'build', '.git', 'venv', '__pycache__', '.next', '.vercel'}
EXTENSIONS = {'.py', '.ts', '.tsx', '.js', '.jsx'}

# Match standalone Diamonds/diamonds as whole words
XP_PATTERN = re.compile(r'\bXP\b')
xp_PATTERN = re.compile(r'\bxp\b')

changed_files = []
skipped_files = []

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for fname in files:
        ext = os.path.splitext(fname)[1]
        if ext not in EXTENSIONS:
            continue
        path = os.path.join(root, fname)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            skipped_files.append((path, str(e)))
            continue

        # Skip backup-like files
        if any(part in path for part in ['backup', 'Backup', 'BACKUP']):
            skipped_files.append((path, 'backup file'))
            continue

        new_content = XP_PATTERN.sub('Diamonds', content)
        new_content = xp_PATTERN.sub('diamonds', new_content)

        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            changed_files.append(path)

print(f"Changed {len(changed_files)} files:")
for p in changed_files:
    print(f"  {p}")

if skipped_files:
    print(f"\nSkipped {len(skipped_files)} files:")
    for p, reason in skipped_files:
        print(f"  {p} ({reason})")
