lines = open("D:/Project-Fremen/backend/app/services/lessons/java.py", "r").readlines()
new_lines = []
for i, line in enumerate(lines):
    stripped = line.rstrip()
    # Fix lines that end with ", where the ) is stray (should be just ",)
    if stripped.endswith('",') and '"explanation"' in stripped:
        new_lines.append(stripped[:-2] + '",\n')
    else:
        new_lines.append(line)
content = "".join(new_lines)
open("D:/Project-Fremen/backend/app/services/lessons/java.py", "w").write(content)
print("Fixed java.py line 28")
