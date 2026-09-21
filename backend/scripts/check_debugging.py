#!/usr/bin/env python3
import json

with open('app/data/debugging_bank.json', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total lines: {len(lines)}')

# Find the first closing bracket at depth 0
depth = 0
closing_line = None
for i, line in enumerate(lines):
    depth += line.count('{') - line.count('}')
    if line.strip() == ']' and depth == 0:
        closing_line = i
        break

if closing_line is not None:
    print(f'First valid closing bracket at line {closing_line + 1}')
    json_str = ''.join(lines[:closing_line + 1])
    try:
        data = json.loads(json_str)
        print(f'Valid entries: {len(data)}')
        print(f'Last ID: {data[-1]["id"]}')
        print(f'Last title: {data[-1]["title"]}')
    except Exception as e:
        print(f'Parse error: {e}')
else:
    print('No closing bracket found')

# Check what's after the closing bracket
if closing_line is not None and closing_line + 1 < len(lines):
    print(f'\\nContent after closing bracket (first 20 lines):')
    for i in range(closing_line + 1, min(closing_line + 21, len(lines))):
        print(f'{i+1}: {lines[i].rstrip()}')
