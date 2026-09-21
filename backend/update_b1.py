import io

with io.open('app/data/worlds_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Binary Search b-1 replacement
b1_old = '''            _level("b-1","The Sorted Shelf","📚",1,"binary search","Halving","searching.binary","searching.binary",
                _story("Binary Borough Library","Librarian Zoe","Books are sorted by title. Find Dragon without checking every shelf."),
                _tutor("Byte","🧭","When things are sorted, you can cut the search in half each time.","Open the middle. If your target is smaller, go left. If bigger, go right. Repeat."),
                _discover("A sorted shelf of 8 books. Find Dragon by checking the middle.","binary-flip","Which book do you check first?","middle = 4"),
                _manipulate("mid-point","Check position ?","middle = (low + high) // 2"),
                _code("Find the target using binary search on a sorted list.","books = ['Ant','Bear','Cat','Dragon','Eagle','Fox','Goat','Hawk']\\n","target = 'Dragon'\\nlo, hi = 0, len(books)-1\\nwhile lo <= hi:\\n    mid = (lo+hi)//2\\n    if books[mid] == target: print(mid); break\\n    elif books[mid] < target: lo = mid+1\\n    else: hi = mid-1"),
                _checks([r"while\\s+lo",r"mid\\s*=\\s*\\(lo\\s*+\\s*hi\\)",r"books\\[mid\\]"]),
                ["The books are sorted — use that!","Check the middle first.","If target is bigger, discard the left half."],
                _success("📚 Full shelf · 🔍 Slow scan","📚 Sorted shelf · ⚡ Found at mid","The librarian is amazed — you found it in 2 checks!","Binary Search — halve the problem each time.","Sorted data unlocks speed.",25)),'''

b1_new = '''            _level("b-1","The Sorted Shelf","📚",1,"binary search","Halving","searching.binary","searching.binary",
                _story("Binary Borough Library","Librarian Zoe","Books are sorted by title. Find Dragon without checking every shelf."),
                _tutor("Byte","🧭","When things are sorted, you can cut the search in half each time.","Open the middle. If your target is smaller, go left. If bigger, go right. Repeat."),
                _discover("A sorted shelf of 8 books. Find Dragon by checking the middle.","binary-flip","Which book do you check first?","middle = 4"),
                _manipulate("mid-point","Check position ?","middle = (low + high) // 2"),
                _predict("If the list is [1,3,5,7] and target is 4, what does the first mid check return?","index 1 (value 3)","Binary search compares the middle element and decides the direction."),
                _break_step("What happens if you write `while lo < hi` for a list of length 1?","lo, hi = 0, 0\\nwhile lo < hi:\\n    mid = (lo+hi)//2\\n    print(nums[mid])\\n","Target at index 0 is skipped"),
                _debug("Fix the off-by-one: this search can miss the first element.","def search(nums, target):\\n    lo, hi = 0, len(nums)\\n    while lo < hi:\\n        mid = (lo+hi)//2\\n        if nums[mid] == target: return mid\\n        elif nums[mid] < target: lo = mid+1\\n        else: hi = mid\\n    return -1", fix_steps=["Use `hi = len(nums)-1` and `while lo <= hi` so the first element is reachable."], answer="lo, hi = 0, len(nums)-1\\nwhile lo <= hi:\\n    mid = (lo+hi)//2\\n    if nums[mid] == target: return mid\\n    elif nums[mid] < target: lo = mid+1\\n    else: hi = mid\\nreturn -1"),
                _code("Find the target using binary search on a sorted list.","books = ['Ant','Bear','Cat','Dragon','Eagle','Fox','Goat','Hawk']\\n","target = 'Dragon'\\nlo, hi = 0, len(books)-1\\nwhile lo <= hi:\\n    mid = (lo+hi)//2\\n    if books[mid] == target: print(mid); break\\n    elif books[mid] < target: lo = mid+1\\n    else: hi = mid-1"),
                _checks([r"while\\s+lo",r"mid\\s*=\\s*\\(lo\\s*+\\s*hi\\)",r"books\\[mid\\]"]),
                ["The books are sorted — use that!","Check the middle first.","If target is bigger, discard the left half."],
                _retrieval("What is the worst-case time complexity of binary search?","O(log n)","Each step halves the search space."),
                _transfer("Find the first occurrence of target 3 in [1,2,3,3,3,4,5].","nums = [1,2,3,3,3,4,5]\\ntarget = 3\\nlo, hi = 0, len(nums)-1\\nans = -1\\nwhile lo <= hi:\\n    mid = (lo+hi)//2\\n    if nums[mid] == target:\\n        ans = mid\\n        hi = mid-1\\n    elif nums[mid] < target:\\n        lo = mid+1\\n    else:\\n        hi = mid-1\\nprint(ans)","Same search, but keep searching left after finding a match."),
                _success("📚 Full shelf · 🔍 Slow scan","📚 Sorted shelf · ⚡ Found at mid","The librarian is amazed — you found it in 2 checks!","Binary Search — halve the problem each time.","Sorted data unlocks speed.",25)),'''

if b1_old in content:
    content = content.replace(b1_old, b1_new)
    print('Replaced b-1')
else:
    print('b-1 old pattern not found')

with io.open('app/data/worlds_data.py', 'w', encoding='utf-8') as f:
    f.write(content)
