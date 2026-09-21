import io
import re

with io.open('app/data/worlds_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Match _debug calls with exactly 4 comma-separated args where the 3rd is not already fix_steps=
pattern = r'_debug\(([^)]+)\)'

def fix_debug_call(match):
    args_str = match.group(1)
    # Don't match if it already has fix_steps= or answer=
    if 'fix_steps=' in args_str or 'answer=' in args_str:
        return match.group(0)
    
    args = []
    current = ''
    in_string = False
    string_char = None
    for c in args_str:
        if c in '"\'':
            if not in_string:
                in_string = True
                string_char = c
            elif string_char == c:
                in_string = False
                string_char = None
        if c == ',' and not in_string:
            args.append(current.strip())
            current = ''
        else:
            current += c
    if current.strip():
        args.append(current.strip())
    
    if len(args) == 4:
        return f'_debug({args[0]}, {args[1]}, fix_steps=[{args[2]}], answer={args[3]})'
    return match.group(0)

new_content = re.sub(pattern, fix_debug_call, content)

with io.open('app/data/worlds_data.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Fixed _debug calls')
