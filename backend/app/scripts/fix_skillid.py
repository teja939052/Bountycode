import re
import os

missions_dir = "D:/Project-Fremen/frontend/src/data/missions"
for fname in os.listdir(missions_dir):
    if not fname.endswith(".tsx"):
        continue
    path = os.path.join(missions_dir, fname)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # Fix skillId: some_module.some_id pattern
    new_content = re.sub(r"skillId:\s*([a-z_]+)\.([a-z_]+)", r'skillId: "\1.\2"', content)
    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed {fname}")
