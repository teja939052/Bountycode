import re

# Read the file
with open('../../app/data/worlds_data.py', 'r') as f:
    content = f.read()

# Define transfer additions for each level in World 1
transfers = {
    'level-1': '                 _transfer(prompt="A new crate holds 7 loaves of bread. Label it and print the count.", answer="bread = 7\\nprint(bread)", context="Same idea, different item and value."),\n',
    'level-2': '                 _transfer(prompt="Track two more items in the shop: eggs=12 and milk=3. Print both.", answer="eggs = 12\\nmilk = 3\\nprint(eggs)\\nprint(milk)", context="More boxes, same pattern."),\n',
    'level-3': '                 _transfer(prompt="A stock starts at 50 and drops to 35 after sales. Update and print.", answer="stock = 50\\nstock = 35\\nprint(stock)", context="State changes in a sales scenario."),\n',
    'level-4': '                 _transfer(prompt="Track three new items: pens=10, notebooks=5, erasers=8. Print all.", answer="pens = 10\\nnotebooks = 5\\nerasers = 8\\nprint(pens, notebooks, erasers)", context="More state, same structure."),\n',
    'level-5': '                 _transfer(prompt="Compute total cost: price=200, quantity=3, tax=12. Print total.", answer="price = 200\\nquantity = 3\\ntax = 12\\ntotal = price * quantity + tax\\nprint(total)", context="Expressions in a shopping context."),\n',
    'boss-1': '                 _transfer(prompt="A new stockroom has 8 TVs, 3 laptops, and 15 phones. Compute and print the total items.", answer="tvs = 8\\nlaptops = 3\\nphones = 15\\ntotal = tvs + laptops + phones\\nprint(total)", context="Transfer: same pattern, new inventory."),\n',
}

# Add transfer parameter to each _level/_boss call
# Pattern: _level("level-1", ...) or _boss("boss-1", ...)
# We need to add transfer=Transfer(...) before the closing parenthesis

def add_transfer_to_level(match):
    level_id = match.group(1)
    body = match.group(2)
    if level_id in transfers:
        # Add transfer before the closing )
        if 'transfer=' not in body:
            # Find the last parameter before )
            body = body.rstrip()
            if body.endswith(')'):
                body = body[:-1].rstrip() + ',\n' + transfers[level_id] + ')'
    return match.group(0).replace(body, body) if False else match.group(0)

# Actually, let's do a simpler approach - find each level/boss definition and add transfer
lines = content.split('\n')
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    new_lines.append(line)
    
    # Check if this is a _level or _boss line
    if '_level(' in line or '_boss(' in line:
        # Collect the full call
        call_lines = [line]
        j = i + 1
        while j < len(lines) and ')' not in lines[j-1] or call_lines[-1].count('(') > call_lines[-1].count(')'):
            if ')' in lines[j-1] and call_lines[-1].count('(') == call_lines[-1].count(')'):
                break
            call_lines.append(lines[j])
            j += 1
        if j < len(lines):
            call_lines.append(lines[j])
        
        # Check if this is a World 1 level/boss
        call_text = '\n'.join(call_lines)
        if 'WORLD_FOUNDATIONS' in content.split('_level(')[0] or any(x in call_text for x in ['"level-1"', '"level-2"', '"level-3"', '"level-4"', '"level-5"', '"boss-1"']):
            # Find the level/boss ID
            id_match = re.search(r'_(?:level|boss)\("([^"]+)"', call_text)
            if id_match:
                level_id = id_match.group(1)
                if level_id in transfers and 'transfer=' not in call_text:
                    # Find where to insert - before the closing )
                    for k in range(len(call_lines) - 1, -1, -1):
                        if call_lines[k].strip() == ')':
                            call_lines.insert(k, transfers[level_id])
                            break
        
        # Skip the lines we just processed
        i = j + 1
        new_lines.extend(call_lines[len(new_lines) - i:])
        continue
    
    i += 1

# This approach is getting complicated. Let me use a simpler regex-based approach.
