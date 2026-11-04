lines = open("D:/Project-Fremen/backend/app/services/lessons/cpp.py", "r").readlines()
count = 0
new_lines = []
for line in lines:
    stripped = line.rstrip()
    if stripped.endswith('.",') and '"explanation"' in stripped:
        count += 1
        new_lines.append(stripped[:-1] + ',\n')
    else:
        new_lines.append(line)
content = "".join(new_lines)
open("D:/Project-Fremen/backend/app/services/lessons/cpp.py", "w").write(content)
print(f"Fixed {count} lines in cpp.py")
