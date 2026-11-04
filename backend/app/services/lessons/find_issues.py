lines = open("D:/Project-Fremen/backend/app/services/lessons/java.py", "r").readlines()
for i, line in enumerate(lines):
    stripped = line.rstrip()
    if stripped.endswith('",') and '"explanation"' in stripped:
        print(f"Line {i+1}: {stripped}")