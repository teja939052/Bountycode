import re

files = [
    'app/content/worlds_3_to_6.py',
    'app/content/worlds_7_to_9.py',
    'app/content/worlds_10_to_12.py',
]

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add fields after each hidden_tests=N,
    pattern = r'(hidden_tests=\d+,)'
    replacement = r'\1\n                    repair_steps=[],\n                    passing_score=70,\n                    max_attempts=3,'
    
    new_content = re.sub(pattern, replacement, content)
    
    # Handle any without trailing comma
    for n in [2, 3, 4, 5]:
        new_content = new_content.replace(f'hidden_tests={n})', f'hidden_tests={n},\n                    repair_steps=[],\n                    passing_score=70,\n                    max_attempts=3,)')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f'{filepath}: repair_steps={new_content.count("repair_steps")}, passing_score={new_content.count("passing_score")}, max_attempts={new_content.count("max_attempts")}')
