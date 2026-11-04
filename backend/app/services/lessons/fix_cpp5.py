# Fix cpp.py in one shot
lines = open("D:/Project-Fremen/backend/app/services/lessons/cpp.py", "r").readlines()
new_lines = []
count = 0
for line in lines:
    stripped = line.rstrip()
    if stripped.endswith('.",') and '"explanation"' in stripped:
        count += 1
        new_lines.append(stripped[:-1] + ',\n')
    else:
        new_lines.append(line)
content = "".join(new_lines)
open("D:/Project-Fremen/backend/app/services/lessons/cpp.py", "w").write(content)
print(f"Fixed {count} lines")

# Verify
lines2 = open("D:/Project-Fremen/backend/app/services/lessons/cpp.py", "r").readlines()
print(f"Line 67 after fix: {repr(lines2[66])}")