import os
lessons_dir = "D:/Project-Fremen/backend/app/services/lessons"
for f in sorted(os.listdir(lessons_dir)):
    if f.endswith(".py") and f not in ("__init__.py",):
        try:
            open(os.path.join(lessons_dir, f), "r", encoding="utf-8").read()
        except UnicodeDecodeError as e:
            print(f"{f}: UTF-8 decode error at position {e.start}")