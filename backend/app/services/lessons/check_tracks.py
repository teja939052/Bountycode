import os, re
lessons_dir = "D:/Project-Fremen/backend/app/services/lessons"
for f in ["cpp.py", "java.py", "dsa.py", "aptitude.py", "logical.py", "verbal.py", "networks.py", "oop.py", "os.py", "dbms.py", "company_prep.py"]:
    path = os.path.join(lessons_dir, f)
    content = open(path, "r").read()
    marker = "\n# --- Auto-generated"
    idx = content.find(marker)
    if idx != -1:
        original = content[:idx]
        ids = re.findall(r'"id":\s*"([^"]+)"', original)
        print(f"{f}: {len(ids)} original lessons, {len(content)} chars total, {len(content) - idx} chars auto-generated")
    else:
        print(f"{f}: no auto-generated marker found, {len(content)} chars")