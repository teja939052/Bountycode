import re

filepath = "D:/Project-Fremen/backend/app/content/world_resume.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Fix field="" → field=" (double quote artifact from first bad run)
content = re.sub(r'(\w+)=""', r'\1="', content)

# Fix field":" → field= (keep existing " as string opening)
content = re.sub(r'(\w+):"(?!\s*\[)', r'\1=', content)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Done")
