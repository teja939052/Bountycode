content = open("D:/Project-Fremen/backend/app/services/lessons/python.py", "r").read()
import re
lesson_ids = re.findall(r'"id":\s*"([^"]+)"', content)
step_ids = [lid for lid in lesson_ids if re.search(r'-s\d+$', lid)]
true_lesson_ids = [lid for lid in lesson_ids if not re.search(r'-s\d+$', lid)]
print(f'python.py: {len(true_lesson_ids)} lessons')
print(f'First 3: {true_lesson_ids[:3]}')
print(f'Last 3: {true_lesson_ids[-3:]}')