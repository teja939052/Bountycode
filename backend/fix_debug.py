import io

with io.open('app/data/worlds_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix all _debug calls where fix_steps is passed as a string instead of list
# Pattern: _debug("prompt", "buggy", "fix_steps_string", "answer")
# Should be: _debug("prompt", "buggy", fix_steps=["fix_steps_string"], answer="answer")

# We need to find all _debug calls with 4 positional args where the 3rd is a string
# and convert them to use fix_steps=[...] keyword

import re

def fix_debug_call(match):
    full = match.group(0)
    # Check if it has 4 positional args
    args = match.group(1).split(',')
    if len(args) == 4:
        prompt = args[0].strip()
        buggy = args[1].strip()
        fix_steps = args[2].strip()
        answer = args[3].strip()
        return f'_debug({prompt}, {buggy}, fix_steps=[{fix_steps}], answer={answer})'
    return full

# Find all _debug(...) calls
pattern = r'_debug\([^)]+\)'
new_content = re.sub(pattern, fix_debug_call, content)

with io.open('app/data/worlds_data.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Fixed _debug calls')
