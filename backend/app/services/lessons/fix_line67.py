lines = open("D:/Project-Fremen/backend/app/services/lessons/cpp.py", "r").readlines()
# Fix line 67 (index 66)
line = lines[66]
stripped = line.rstrip()
print(f"Before: {repr(stripped)}")
if stripped.endswith('.",') and '"explanation"' in stripped:
    new_line = stripped[:-1] + ',\n'
    print(f"After: {repr(new_line)}")
    lines[66] = new_line
content = "".join(lines)
open("D:/Project-Fremen/backend/app/services/lessons/cpp.py", "w").write(content)
print("Done")
