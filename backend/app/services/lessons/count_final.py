import os, re
lessons_dir = "D:/Project-Fremen/backend/app/services/lessons"
total = 0
for f in sorted(os.listdir(lessons_dir)):
    if f.endswith(".py") and f != "__init__.py":
        path = os.path.join(lessons_dir, f)
        content = open(path).read()
        # Count lesson IDs only (not step IDs which end with -sN)
        lesson_ids = re.findall(r'"id":\s*"([^"]+)"', content)
        # Filter out step IDs (they end with -sN where N is a digit)
        lesson_only = [lid for lid in lesson_ids if not re.search(r'-s\d+$', lid)]
        print(f"{f}: {len(lesson_only)} lessons")
        total += len(lesson_only)
print(f"\nTOTAL: {total} lessons across all tracks")