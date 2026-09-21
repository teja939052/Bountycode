import re

def _parse_test_input(raw):
    raw = raw.strip()
    tokens = re.findall(r'"[^"]*"|\[[^\]]*\]|\S+', raw)
    return ", ".join(tokens)

tests = [
    '[1,12,-5,-6,50,3] 4',
    '[5] 1',
    '"abcabcbb"',
    '"ADOBECODEBANC" "ABC"',
    '"eceba" 2',
    '"a" "a"',
    '[2,1,5,1,3,2] 3',
]
for t in tests:
    print(f"{t!r:40} -> {_parse_test_input(t)!r}")
