import io
import re

with io.open('app/data/worlds_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find _debug calls with 4 positional args and convert 3rd arg to fix_steps=[...]
pattern = r'_debug\(([^)]+)\)'

def fix_debug_call(match):
    args_str = match.group(1)
    args = [a.strip() for a in args_str.split(',')]
    if len(args) == 4:
        return f'_debug({args[0]}, {args[1]}, fix_steps=[{args[2]}], answer={args[3]})'
    return match.group(0)

new_content = re.sub(pattern, fix_debug_call, content)

with io.open('app/data/worlds_data.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Fixed _debug calls')
