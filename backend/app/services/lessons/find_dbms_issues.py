lines = open("D:/Project-Fremen/backend/app/services/lessons/dbms.py", "r").readlines()
for i, line in enumerate(lines):
    stripped = line.rstrip()
    if stripped.endswith('.",'):
        print(f"Line {i+1}: {stripped}")