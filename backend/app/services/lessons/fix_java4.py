lines = open("D:/Project-Fremen/backend/app/services/lessons/java.py", "r").readlines()
new_lines = []
for line in lines:
    stripped = line.rstrip()
    if stripped.endswith('",') and '"explanation"' in stripped:
        # Remove extra quote before comma: ...case-sensitive."", -> ...case-sensitive.",
        new_lines.append(stripped[:-1] + ",\n")
    else:
        new_lines.append(line)
content = "".join(new_lines)
open("D:/Project-Fremen/backend/app/services/lessons/java.py", "w").write(content)
print("Fixed java.py")
