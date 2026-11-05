content = open("D:/Project-Fremen/backend/app/services/lessons/python.py", "r").read()

marker2 = "\n# --- Real Python Lessons"
idx2 = content.find(marker2)
print("Real lessons marker at:", idx2)

original = content[:idx2].rstrip()
print("Original content length:", len(original))
print("Ends with ]:", original.endswith("]"))
print("Last 50 chars:", repr(original[-50:]))

import re
ids = re.findall(r'"id":\s*"([^"]+)"', original)
print("Original lesson IDs:", len(ids))
print("First 5:", ids[:5])
print("Last 5:", ids[-5:])