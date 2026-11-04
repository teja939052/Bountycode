with open("java.py", "r") as f:
    content = f.read()

# Remove trailing whitespace and the final ]
content = content.rstrip()
if content.endswith("]"):
    content = content[:-1].rstrip()

with open("java_extra.py", "r") as f:
    extra = f.read()

# Remove the first line "JAVA_EXTRA_LESSONS = [" and the last "]"
lines = extra.strip().split("\n")
# Skip first line
lines = lines[1:]
# Remove last line "]"
if lines and lines[-1].strip() == "]":
    lines = lines[:-1]

extra_body = "\n".join(lines)

# Indent extra_body lines by 4 spaces to fit inside the list
indented = "\n".join("    " + line if line.strip() else line for line in extra_body.split("\n"))

content += indented
content += "\n]"

with open("java.py", "w") as f:
    f.write(content)

print("java.py updated successfully")
