# Direct fix for remaining problem files
import os

lessons_dir = "D:/Project-Fremen/backend/app/services/lessons"

for f in ["dbms.py", "python.py"]:
    filepath = os.path.join(lessons_dir, f)
    content = open(filepath, "r").read()
    before = content.count('.",')
    content = content.replace('.",', '",')
    after = content.count('.",')
    print(f"{f}: {before} -> {after}")
    open(filepath, "w").write(content)

print("Done")
