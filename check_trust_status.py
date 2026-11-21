import json, os, re
from pathlib import Path
from collections import Counter

scripts_dir = Path('backend/scripts')
for f in sorted(scripts_dir.glob('add_*.py')):
    with open(f, 'r') as fh:
        content = fh.read()
    # Count trust_status assignments
    trust_statuses = re.findall(r'trust_status["\']\s*:\s*["\']([^"\']+)["\']', content)
    if trust_statuses:
        counts = Counter(trust_statuses)
        print(f'{f.name}: {dict(counts)}')
