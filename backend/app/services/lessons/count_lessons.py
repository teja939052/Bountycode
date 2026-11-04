import os
lessons_dir = "D:/Project-Fremen/backend/app/services/lessons"
for f in ['aptitude.py','company_prep.py','cpp.py','dbms.py','dsa.py','java.py','logical.py','networks.py','oop.py','os.py','python.py','verbal.py']:
    path = os.path.join(lessons_dir, f)
    with open(path) as fh:
        content = fh.read()
    count = content.count('"id":')
    print(f"{f}: {count} lessons")
