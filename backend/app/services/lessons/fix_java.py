java_path = "D:/Project-Fremen/backend/app/services/lessons/java.py"
lines = open(java_path, "r").readlines()
new_lines = []
for i, line in enumerate(lines):
    stripped = line.rstrip()
    if stripped.endswith('}),') and '"explanation"' in stripped:
        new_lines.append(stripped[:-2] + '),\n')
    else:
        new_lines.append(line)
content = "".join(new_lines)
open(java_path, "w").write(content)
print("Fixed java.py")
