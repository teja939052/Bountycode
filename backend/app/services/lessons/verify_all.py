import os
lessons_dir = "D:/Project-Fremen/backend/app/services/lessons"
all_ok = True
for f in sorted(os.listdir(lessons_dir)):
    if f.endswith(".py") and f not in ("__init__.py",):
        try:
            import ast
            ast.parse(open(os.path.join(lessons_dir, f), "r", encoding="utf-8").read())
        except SyntaxError as e:
            print(f"{f}: ERROR - {e}")
            all_ok = False
if all_ok:
    print("All lesson files compile successfully!")