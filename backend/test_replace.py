import io

with io.open('app/data/worlds_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Helper to create debug block
def debug_block(prompt, buggy, fix_steps_list, answer):
    fix_steps_str = ', '.join([f'"{s}"' for s in fix_steps_list])
    return f'_debug({prompt!r}, {buggy!r}, fix_steps=[{fix_steps_str}], answer={answer!r})'

# Binary Search b-1
b1_debug = debug_block(
    "Fix the off-by-one: this search can miss the first element.",
    "def search(nums, target):\n    lo, hi = 0, len(nums)\n    while lo < hi:\n        mid = (lo+hi)//2\n        if nums[mid] == target: return mid\n        elif nums[mid] < target: lo = mid+1\n        else: hi = mid\n    return -1",
    ["Use `hi = len(nums)-1` and `while lo <= hi` so the first element is reachable."],
    "lo, hi = 0, len(nums)-1\nwhile lo <= hi:\n    mid = (lo+hi)//2\n    if nums[mid] == target: return mid\n    elif nums[mid] < target: lo = mid+1\n    else: hi = mid\nreturn -1"
)

print('b1_debug:', b1_debug[:100])

# Test if we can find b-1 in content
idx = content.find('_level("b-1"')
print(f'b-1 found at index: {idx}')

if idx != -1:
    # Find the end of this level (next _level or _boss or ]),)
    end_idx = content.find('            _level("b-2"', idx)
    if end_idx == -1:
        end_idx = content.find('            _boss("b-boss"', idx)
    print(f'b-1 ends at index: {end_idx}')
    print('Content around b-1:', repr(content[idx:idx+200]))
