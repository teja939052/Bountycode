c = open('D:\\Project-Fremen\\backend\\seed_questions_mega.py', encoding='utf-8').read()

# Check what the last few lines look like
import re

# Find questions list
match = re.search(r"questions\s*=\s*\[", c)
if match:
    start = match.start()
    depth = 0
    pos = start
    in_str = False
    str_char = None
    while pos < len(c):
        ch = c[pos]
        if in_str:
            if ch == '\\' and pos + 1 < len(c):
                pos += 2
                continue
            if ch == str_char:
                in_str = False
        elif ch in ("'", '"'):
            in_str = True
            str_char = ch
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                print(f"List ends at position {pos}")
                print(f"Content after: {repr(c[pos:pos+200])}")
                break
        pos += 1
    else:
        print("List NEVER closed!")
        print(f"Depth at end: {depth}")
        print(f"Last 100 chars: {repr(c[-100:])}")
else:
    print("No questions list found")

# Count brackets
opens = c.count("[")
closes = c.count("]")
print(f"Total '[' = {opens}, ']' = {closes}, diff = {opens - closes}")
