lines = open("D:/Project-Fremen/backend/app/services/lessons/cpp.py", "r").readlines()
new_lines = []
for line in lines:
    stripped = line.rstrip()
    # Fix explanation lines ending with .", → .",
    if stripped.endswith('.",') and '"explanation"' in stripped:
        new_lines.append(stripped[:-1] + ',\n')
    else:
        new_lines.append(line)
content = "".join(new_lines)
open("D:/Project-Fremen/backend/app/services/lessons/cpp.py", "w").write(content)
print("Fixed cpp.py")
