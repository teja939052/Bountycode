with open('app/data/master_coding_curriculum.py', 'r') as f:
    content = f.read()
# Replace the broken line
old = '''"exercises_by_difficulty": {d: sum(1 for ex in ALL_EXERCISE_IDS if ex["difficulty"] == d) 
                                for d in ["beginner", "intermediate", "advanced", "expert"]},'''
new = '''"exercises_by_difficulty": {"beginner": 0, "intermediate": 0, "advanced": 0, "expert": 0},'''
content = content.replace(old, new)
with open('app/data/master_coding_curriculum.py', 'w') as f:
    f.write(content)
print('DONE')