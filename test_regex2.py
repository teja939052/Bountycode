import re
print(repr(re.findall(r'\bXP\b', 'import XPBar from "../components/XPBar";')))
print(repr(re.findall(r'\bXP\b', 'XPBar')))
print(repr(re.findall(r'\bXP\b', '<XPBar')))
