import json, pathlib, sys

files = sorted(pathlib.Path('app/data/curriculum').glob('module_*.json'))
errors = []
for p in files:
    try:
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"OK: {p.name} (module_id={data.get('module_id')})")
    except Exception as e:
        errors.append((p.name, str(e)))
        print(f"FAIL: {p.name} -> {e}")

if errors:
    sys.exit(1)
else:
    print("\nAll curriculum JSON files valid.")
