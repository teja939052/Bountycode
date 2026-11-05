import os
import sys

lessons_dir = "D:/Project-Fremen/backend/app/services/lessons"
python_file = os.path.join(lessons_dir, "python.py")

# Read the file
content = open(python_file, "r").read()

# Find where real lessons marker starts
marker = "\n# --- Real Python Lessons"
idx = content.find(marker)

if idx == -1:
    print("No real lessons marker found")
    # Just keep the file as is
    exit()

# Keep only the original content (before the real lessons marker)
original_content = content[:idx].rstrip()
print(f"Original content length: {len(original_content)} chars")

# Ensure the original content ends with a closing bracket
if not original_content.rstrip().endswith("]"):
    original_content = original_content.rstrip() + "\n]\n"
    print("Added closing bracket for PYTHON_LESSONS list")
else:
    original_content = original_content.rstrip() + "\n"

# Now import the content library and build real lessons
sys.path.insert(0, lessons_dir)
from python_content import PYTHON_CONTENT, PYTHON_PROJECTS, create_lesson

real_lessons = []
for topic, content_data in PYTHON_CONTENT.items():
    lesson = create_lesson(topic, content_data)
    real_lessons.append(lesson)

for project in PYTHON_PROJECTS:
    real_lessons.append(project)

print(f"Built {len(real_lessons)} real lessons from content library")

# Generate the Python code to append
py_code = "\n# --- Real Python Lessons (coddy.tech quality) ---\nREAL_PYTHON_LESSONS = [\n"
for i, lesson in enumerate(real_lessons):
    py_code += f"    {repr(lesson)}"
    if i < len(real_lessons) - 1:
        py_code += ",\n"
    else:
        py_code += "\n"
py_code += "]\nPYTHON_LESSONS.extend(REAL_PYTHON_LESSONS)\n"

# Write the file with UTF-8 encoding
with open(python_file, "w", encoding="utf-8") as f:
    f.write(original_content + py_code)

print(f"Written {len(original_content) + len(py_code)} chars to {python_file}")

# Verify
import ast
ast.parse(open(python_file, encoding="utf-8").read())
print("File compiles successfully!")

# Import and count
import importlib.util
spec = importlib.util.spec_from_file_location("python", python_file)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
print(f"Total Python lessons: {len(mod.PYTHON_LESSONS)}")