content = open('D:/Project-Fremen/backend/app/services/lessons/dbms.py', 'r', encoding='utf-8').read()

# Find the start of dbms-transactions-and-isolation lesson
start_marker = '        "id": "dbms-transactions-and-isolation",'
start_idx = content.find(start_marker)
print(f"Found start at: {start_idx}")

# Find the end of the new lesson - look for }, at indentation level 8 spaces
# followed by newline and then { (next lesson) or ] (end of list)
import re

pattern = r'        \},\n    \},'
match = re.search(pattern, content[start_idx:])
if match:
    lesson_end = start_idx + match.end()
    print(f"Lesson ends at: {lesson_end}")
else:
    print("Could not find lesson end with pattern")
    # Try alternative pattern
    pattern2 = r'        \},\n    \},'
    match2 = re.search(pattern2, content[start_idx:])
    if match2:
        lesson_end = start_idx + match2.end()
        print(f"Lesson ends at: {lesson_end}")
    else:
        print("Could not find lesson end")

# Keep everything up to the end of the new lesson, then close the list
new_content = content[:lesson_end] + '\n    ],\n]'

open('D:/Project-Fremen/backend/app/services/lessons/dbms.py', 'w', encoding='utf-8').write(new_content)
print(f'New content length: {len(new_content)}')
print('Done')
PYEOF