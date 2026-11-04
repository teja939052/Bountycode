import os

lessons_dir = "D:/Project-Fremen/backend/app/services/lessons"

for f in sorted(os.listdir(lessons_dir)):
    if not f.endswith(".py"):
        continue
    filepath = os.path.join(lessons_dir, f)
    content = open(filepath, "r").read()
    
    # Fix all remaining ." → ." patterns
    before = content.count('."')
    content = content.replace('."', '."')
    after = content.count('."')
    
    if before != after:
        open(filepath, "w").write(content)
        print(f"{f}: fixed {before - after} lines")

print("Done")
