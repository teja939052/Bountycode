import io

with io.open('app/data/worlds_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# The prefix town was accidentally inserted inside the hashing world.
# We need to remove it from there and insert it inside the dynamic world.

# First, find and remove the prefix town from inside hashing world
prefix_start = content.find('        _make_town("prefix", "Prefix Plains"')
if prefix_start == -1:
    print('PREFIX TOWN NOT FOUND')
    exit(1)

# Find the end of the prefix town (the closing ]),)
prefix_end = content.find('        ]),\n    ]\n)\n\n# ═══════════════════════════════════════════════════════════════\n# WORLD 9: Tree Grove (trees)', prefix_start)
if prefix_end == -1:
    print('PREFIX END NOT FOUND')
    exit(1)

prefix_town_block = content[prefix_start:prefix_end]

# Remove it from current location
content = content[:prefix_start] + content[prefix_end + len('        ]),\n    ]\n)\n\n# ═══════════════════════════════════════════════════════════════\n# WORLD 9: Tree Grove (trees)'):]

# Now find the dynamic world and insert prefix town before its close
dynamic_marker = '        ]),\n    ]\n)\n\n# ═══════════════════════════════════════════════════════════════\n# WORLD 9: Tree Grove (trees)'
if dynamic_marker in content:
    content = content.replace(dynamic_marker, prefix_town_block + dynamic_marker)
    print('PREFIX TOWN MOVED TO DYNAMIC WORLD')
else:
    print('DYNAMIC MARKER NOT FOUND')

with io.open('app/data/worlds_data.py', 'w', encoding='utf-8') as f:
    f.write(content)
