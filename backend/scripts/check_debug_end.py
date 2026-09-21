#!/usr/bin/env python3
with open('app/data/debugging_bank.json', encoding='utf-8') as f:
    content = f.read()

import json
try:
    data = json.loads(content)
    print(f'Parsed {len(data)} entries')
    print(f'Last ID: {data[-1]["id"]}')
except Exception as e:
    print(f'Parse error: {e}')
    
    # Find where the first valid JSON array ends
    depth = 0
    for i, char in enumerate(content):
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
        elif char == ']' and depth == 0:
            print(f'First valid array ends at position {i}')
            print(f'Content after: {repr(content[i+1:i+100])}')
            break
