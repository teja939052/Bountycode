"""Quick count of questions in bank."""
import json

print("Loading...")
with open('app/data/questions_bank.json', 'r') as f:
    content = f.read()

print(f"File size: {len(content)} chars")

# Parse just the first 100 questions
import ast
# Find question boundaries
count = 0
idx = 0
while idx < len(content):
    # Find next question start
    start = content.find('{"type"', idx)
    if start == -1:
        break
    # Find matching closing brace
    depth = 0
    end = start
    in_string = False
    escape = False
    while end < len(content):
        c = content[end]
        if escape:
            escape = False
        elif c == '\\':
            escape = True
        elif c == '"' and not escape:
            in_string = not in_string
        elif not in_string:
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    break
        end += 1
    count += 1
    idx = end + 1
    if count % 1000 == 0:
        print(f"  Counted {count}...")

print(f"Total questions: {count}")
