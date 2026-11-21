import sys

with open('.github/workflows/ci.yml', 'r') as f:
    lines = f.readlines()

# Find conflict boundaries
start = None
sep = None
end = None
for i, line in enumerate(lines):
    if '<<<<<<< HEAD' in line:
        start = i
    elif line.strip() == '=======' and start is not None and sep is None:
        sep = i
    elif '>>>>>>> 2513abbf5afd49040fd2f2c6b74d8f92c90e1901' in line:
        end = i

if start is None or sep is None or end is None:
    print(f'FAILED: start={start}, sep={sep}, end={end}')
else:
    # HEAD content is between start+1 and sep-1 (exclusive of <<<<<<< HEAD and =======)
    head_lines = lines[start+1:sep]
    
    # Build new content: everything before <<<<<<< HEAD + HEAD content + everything after >>>>>>>
    new_lines = lines[:start] + head_lines + lines[end+1:]
    
    with open('.github/workflows/ci.yml', 'w') as f:
        f.writelines(new_lines)
    print('SUCCESS: ci.yml resolved')
    print(f'Removed {end - start + 1} lines of conflict markers')