lines = open("D:/Project-Fremen/backend/app/services/lessons/java.py", "r").readlines()
new_lines = []
for line in lines:
    stripped = line.rstrip()
    if stripped.endswith('.,') and '"explanation"' in stripped:
        # stripped[:-1] removes just the ',', leaving ...case-sensitive."
        # Then add ',\n' → ...case-sensitive.",\n  (correct!)
        new_lines.append(stripped[:-1] + ',\n')
    else:
        new_lines.append(line)
content = "".join(new_lines)
open("D:/Project-Fremen/backend/app/services/lessons/java.py", "w").write(content)
print("Fixed java.py")
