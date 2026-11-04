content = open("D:/Project-Fremen/backend/app/services/lessons/python.py", "r").read()
count = content.count('"id":')
print(f"python.py: {count} lesson IDs found, length: {len(content)} chars")