import re

files = [
    "D:/Project-Fremen/backend/app/content/world_resume.py",
    "D:/Project-Fremen/backend/app/content/world_sdlc.py",
]

for filepath in files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Fix field="" → field=" (double quote artifact from first run)
    content = re.sub(r'(\w+)=""', r'\1="', content)
    
    # Fix field":" → field= (original issue)
    content = re.sub(r'(\w+):"(?!\s*\[)', r'\1=', content)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Fixed {filepath}")
