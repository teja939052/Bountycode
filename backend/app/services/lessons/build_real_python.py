"""Comprehensive Python lesson content library - coddy.tech quality.
50+ topics with real code examples, real exercises, and real quizzes.
"""
import os
import sys

# Add lessons dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the content library
from python_content import PYTHON_CONTENT, PYTHON_PROJECTS, create_lesson

# Build real lessons from content library
real_lessons = []
for topic, content in PYTHON_CONTENT.items():
    lesson = create_lesson(topic, content)
    real_lessons.append(lesson)

# Add project lessons
for project in PYTHON_PROJECTS:
    real_lessons.append(project)

print("Created " + str(len(real_lessons)) + " real Python lessons from content library")
print("Topics:", [l["id"] for l in real_lessons])

# Verify content quality
for lesson in real_lessons:
    print("\n--- " + lesson["id"] + ": " + lesson["title"] + " ---")
    for step in lesson["steps"]:
        print("  Step:", step["id"], "(", step["type"], ")")
        if step["type"] == "explain":
            print("    Code:", step["code"][:80], "...")
        elif step["type"] == "exercise":
            print("    Solution:", step["solution"][:80], "...")
        elif step["type"] == "quiz":
            print("    Q:", step["question"])
            print("    Options:", step["options"])
            print("    Correct:", step["correctIndex"])