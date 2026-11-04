cpp_path = "D:/Project-Fremen/backend/app/services/lessons/cpp.py"
extra_path = "D:/Project-Fremen/backend/app/services/lessons/cpp_extra.py"

with open(cpp_path, "r") as f:
    content = f.read()

content = content.rstrip()
if content.endswith("]"):
    content = content[:-1].rstrip()

with open(extra_path, "r") as f:
    extra = f.read()

lines = extra.strip().split("\n")
lines = lines[1:]  # skip "CPP_EXTRA_LESSONS = ["
if lines and lines[-1].strip() == "]":
    lines = lines[:-1]

extra_body = "\n".join(lines)
indented = "\n".join("    " + line if line.strip() else line for line in extra_body.split("\n"))

content += indented
content += "\n]"

with open(cpp_path, "w") as f:
    f.write(content)

print("cpp.py updated successfully")
