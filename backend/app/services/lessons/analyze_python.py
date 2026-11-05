content = open("D:/Project-Fremen/backend/app/services/lessons/python.py", "r").read()

marker1 = "\n# --- Auto-generated"
idx1 = content.find(marker1)
print("Auto-generated marker at:", idx1)

marker2 = "\n# --- Real Python Lessons"
idx2 = content.find(marker2)
print("Real lessons marker at:", idx2)

if idx1 != -1:
    original = content[:idx1].rstrip()
    print("Original content length:", len(original))
    print("Ends with ]:", original.endswith("]"))
    import re
    ids = re.findall(r'"id":\s*"([^"]+)"', original)
    print("Original lesson IDs:", len(ids))
    print("First 5:", ids[:5])
    print("Last 5:", ids[-5:])