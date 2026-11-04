import os
import glob

lessons_dir = "D:/Project-Fremen/backend/app/services/lessons"
fixed_count = 0

for f in sorted(os.listdir(lessons_dir)):
    if not f.endswith(".py"):
        continue
    filepath = os.path.join(lessons_dir, f)
    content = open(filepath, "r").read()
    
    # Fix: explanation lines ending with .", should end with .",
    # Pattern: ...text.", → ...text.",  
    import re
    # Find patterns like: "explanation": "...",  and fix to: "explanation": "...",
    # We need to handle: "explanation": "...text.",
    # Replace: .", with .",
    import re as re2
    
    # Count before
    before = content.count('.",')
    # Replace .", with .",
    content = content.replace('.",', '.",')
    after = content.count('.",')
    
    if before != after:
        open(filepath, "w").write(content)
        print(f"{f}: fixed {before - after} lines")
        fixed_count += (before - after)

print(f"\nTotal: {fixed_count} fixes across all files")
