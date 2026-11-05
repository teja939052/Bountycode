import os

lessons_dir = "D:/Project-Fremen/backend/app/services/lessons"

for f in ["cpp.py", "java.py", "dsa.py", "aptitude.py", "logical.py", "verbal.py", "networks.py", "oop.py", "os.py", "dbms.py", "company_prep.py"]:
    path = os.path.join(lessons_dir, f)
    content = open(path, "r").read()
    marker = "\n# --- Auto-generated"
    idx = content.find(marker)
    if idx != -1:
        original = content[:idx].rstrip()
        # Ensure the original content ends with a closing bracket
        if not original.endswith("]"):
            original = original + "\n]\n"
        else:
            original = original + "\n"
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(original)
        print(f"{f}: kept {len(original)} chars, removed {len(content) - idx} chars of auto-generated content")
    else:
        print(f"{f}: no auto-generated marker found")