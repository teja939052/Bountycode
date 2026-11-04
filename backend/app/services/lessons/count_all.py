import os
lessons_dir = "D:/Project-Fremen/backend/app/services/lessons"
total = 0
for f in sorted(os.listdir(lessons_dir)):
    if f.endswith(".py") and f != "__init__.py":
        filepath = os.path.join(lessons_dir, f)
        content = open(filepath).read()
        count = content.count('"id":') + content.count("'id':")
        print(f"{f}: {count} lessons")
        total += count
print(f"\nTOTAL: {total} lessons across all tracks")