import re
p = re.compile(r'\bxp\b')
print(p.findall('juice:xp'))
print(p.findall('xp-gained'))
print(p.findall('"xp-gained"'))
