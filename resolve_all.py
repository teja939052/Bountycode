import re

files = [
    '.github/workflows/ci.yml',
    'backend/app/content/world_aptitude_tsd.py',
    'backend/app/services/content_loader.py',
    'backend/app/services/quiz_service.py',
    'backend/app/services/study_engine.py',
]

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Pattern for conflict markers
        # Match: <<<<<<< HEAD ... ======= ... >>>>>>> hash
        pattern = r'<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> [a-f0-9]+\n'
        
        def replace_conflict(match):
            head_content = match.group(1)
            return head_content
        
        new_content = re.sub(pattern, replace_conflict, content, flags=re.DOTALL)
        
        if content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'RESOLVED: {filepath}')
        else:
            print(f'NO CONFLICT: {filepath}')
    except Exception as e:
        print(f'ERROR: {filepath}: {e}')