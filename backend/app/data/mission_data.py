"""All 21 mission definitions for the Code Realm.

Each mission has 5 layers: story, concept, interact, code, mastery.
"""
ALL_MISSIONS = {
    "control_flow": {
        "topic": "control_flow",
        "layers": {
            "story": {"title": "The Fork in the Road", "narrative": "Every adventure has crossroads. Should you fight or flee? Heal or attack? Control flow is how your program makes decisions.", "motivation": "Without decisions, a program is just a straight line. Control flow gives your code intelligence."},
            "concept": {"title": "If, Elif, Else", "explanation": "Control flow uses conditions to choose paths:\n\n```python\nif score >= 90:\n    grade = \"A\"\nelif score >= 80:\n    grade = \"B\"\nelse:\n    grade = \"C\"\n```\n\nThe condition is evaluated as True or False.", "examples": [{"code": "x = 10\nif x > 5:\n    print(\"big\")", "output": "big", "explanation": "x > 5 is True, so the block runs"}, {"code": "x = 3\nif x > 5:\n    print(\"big\")\nelse:\n    print(\"small\")", "output": "small", "explanation": "x > 5 is False, so else runs"}], "visualization": "condition → True? → YES branch\n         → False? → NO branch"},
            "interact": {"challenges": [
                {"type": "predict", "prompt": "What is printed?", "code": "x = 7\nif x % 2 == 0:\n    print(\"even\")\nelse:\n    print(\"odd\")", "answer": "odd", "explanation": "7 % 2 = 1, not 0, so else branch"},
                {"type": "trace", "prompt": "Trace the logic", "code": "score = 85\nif score >= 90:\n    result = \"A\"\nelif score >= 80:\n    result = \"B\"\nelse:\n    result = \"C\"\nprint(result)", "answer": "B", "explanation": "85 >= 90 is False, 85 >= 80 is True"},
                {"type": "bug_hunt", "prompt": "Why wrong output?", "code": "x = 5\nif x = 5:\n    print(\"yes\")", "answer": "= is assignment, use ==", "explanation": "Single = assigns, == compares"}
            ]},
            "code": {"challenge": "Write a function that takes a number and prints 'positive', 'negative', or 'zero'.", "boilerplate": "def classify(n):\n    # your code here\n    pass\n\nclassify(5)\nclassify(-3)\nclassify(0)", "tests": [{"input": "5", "expected": "positive"}, {"input": "-3", "expected": "negative"}, {"input": "0", "expected": "zero"}], "hints": ["Start with if n > 0", "Use elif for the next condition", "Use else for the last case"]},
            "mastery": {"boss_name": "Logic Gate Guardian", "pass_score": 70, "challenges": [
                {"type": "predict", "prompt": "Output?", "code": "a, b = True, False\nif a and b:\n    print(\"both\")\nelif a or b:\n    print(\"either\")\nelse:\n    print(\"none\")", "answer": "either", "difficulty": "easy"},
                {"type": "bug_hunt", "prompt": "Fix the logic", "code": "age = 20\nif age > 18:\n    print(\"minor\")", "answer": "print should say adult, not minor", "difficulty": "easy"},
                {"type": "challenge", "prompt": "Write nested if: if age>=18 AND has_id -> 'entry allowed'", "answer": "if age >= 18 and has_id: allowed", "difficulty": "medium"}
            ]}
        }
    },
    "functions": {
        "topic": "functions",
        "layers": {
            "story": {"title": "The Spell Book", "narrative": "A mage doesn't recite the same spell from scratch every time. They write it once and cast it whenever needed. Functions are your spell book.", "motivation": "Functions let you reuse code, organize logic, and build complex systems from simple pieces."},
            "concept": {"title": "Defining & Calling Functions", "explanation": "```python\ndef greet(name):\n    return f\"Hello, {name}!\"\n\nmsg = greet(\"Alex\")\nprint(msg)  # Hello, Alex!\n```\n\nParameters go in parentheses. `return` sends back a value.", "examples": [{"code": "def add(a, b):\n    return a + b\nprint(add(3, 4))", "output": "7", "explanation": "add takes two params, returns their sum"}, {"code": "def square(n):\n    return n * n\nprint(square(5))", "output": "25", "explanation": "5 * 5 = 25"}], "visualization": "input → function body → return value"},
            "interact": {"challenges": [
                {"type": "predict", "prompt": "What is returned?", "code": "def mystery(x):\n    return x * 2 + 1\nprint(mystery(4))", "answer": "9", "explanation": "4 * 2 + 1 = 9"},
                {"type": "trace", "prompt": "Trace the calls", "code": "def double(n):\n    return n * 2\na = double(3)\nb = double(a)\nprint(b)", "answer": "12", "explanation": "double(3)=6, double(6)=12"}
            ]},
            "code": {"challenge": "Write a function `is_even(n)` that returns True if n is even, False otherwise.", "boilerplate": "def is_even(n):\n    # return True if even, False otherwise\n    pass\n\nprint(is_even(4))\nprint(is_even(7))", "tests": [{"input": "4", "expected": "True"}, {"input": "7", "expected": "False"}], "hints": ["Use the modulo operator %", "n % 2 == 0 means even"]},
            "mastery": {"boss_name": "Function Wraith", "pass_score": 70, "challenges": [
                {"type": "predict", "prompt": "Output?", "code": "def f(x, y=10):\n    return x + y\nprint(f(5))\nprint(f(5, 3))", "answer": "15\n8", "difficulty": "easy"},
                {"type": "challenge", "prompt": "Write a recursive factorial function", "answer": "def fact(n): return 1 if n<=1 else n*fact(n-1)", "difficulty": "medium"},
                {"type": "bug_hunt", "prompt": "Why recursion error?", "code": "def count(n):\n    print(n)\n    count(n+1)\ncount(1)", "answer": "No base case — infinite recursion", "difficulty": "medium"}
            ]}
        }
    },
    "strings": {
        "topic": "strings",
        "layers": {
            "story": {"title": "The Cipher Room", "narrative": "Messages, passwords, usernames — strings are everywhere. They're sequences of characters, and mastering them means mastering text processing.", "motivation": "Every app processes text. String manipulation is one of the most common coding tasks in interviews."},
            "concept": {"title": "Strings — Character Sequences", "explanation": "```python\ns = \"Hello\"\nprint(len(s))    # 5\nprint(s[0])      # H\nprint(s[-1])     # o\nprint(s[1:4])    # ell\n```\n\nStrings are immutable — you can't change them in place.", "examples": [{"code": "s = \"hello\"\nprint(s.upper())", "output": "HELLO", "explanation": "upper() returns a new uppercase string"}, {"code": "print(\" \".join([\"a\",\"b\",\"c\"]))", "output": "a b c", "explanation": "join concatenates with separator"}], "visualization": "Index: 0  1  2  3  4\nChar:  H  e  l  l  o"},
            "interact": {"challenges": [
                {"type": "predict", "prompt": "Output?", "code": "s = \"Python\"\nprint(s[1:4])", "answer": "yth", "explanation": "Slicing from index 1 to 4 (exclusive)"},
                {"type": "trace", "prompt": "What happens?", "code": "s = \"racecar\"\nprint(s == s[::-1])", "answer": "True", "explanation": "Reversed string equals original = palindrome"}
            ]},
            "code": {"challenge": "Write a function that counts vowels in a string.", "boilerplate": "def count_vowels(s):\n    # count a, e, i, o, u (case-insensitive)\n    pass\n\nprint(count_vowels(\"Hello World\"))", "tests": [{"input": "Hello World", "expected": "3"}], "hints": ["Convert to lowercase first", "Check each char against 'aeiou'"]},
            "mastery": {"boss_name": "Cipher Master", "pass_score": 70, "challenges": [
                {"type": "predict", "prompt": "Output?", "code": "s = \"abcabc\"\nprint(s.count(\"bc\"))", "answer": "2", "difficulty": "easy"},
                {"type": "challenge", "prompt": "Reverse a string without [::-1]", "answer": "Use a loop or reversed()", "difficulty": "medium"},
                {"type": "bug_hunt", "prompt": "Why error?", "code": "s = \"hello\"\ns[0] = \"H\"", "answer": "Strings are immutable", "difficulty": "easy"}
            ]}
        }
    },
    "sorting": {
        "topic": "sorting",
        "layers": {
            "story": {"title": "The Ranking Arena", "narrative": "Leaderboards, search results, rankings — sorting is how you make sense of chaos. Every efficient program needs it.", "motivation": "Sorting algorithms are a classic interview topic. Understanding them deeply separates good engineers from great ones."},
            "concept": {"title": "Sorting Algorithms", "explanation": "Key algorithms:\n- **Bubble Sort**: Compare adjacent, swap. O(n²)\n- **Merge Sort**: Divide and merge. O(n log n)\n- **Quick Sort**: Pivot and partition. O(n log n) avg\n\nPython's `sorted()` uses Timsort (hybrid).", "examples": [{"code": "arr = [3, 1, 4, 1, 5]\nprint(sorted(arr))", "output": "[1, 1, 3, 4, 5]", "explanation": "sorted() returns a new sorted list"}, {"code": "arr = [3, 1, 4, 1, 5]\narr.sort(reverse=True)\nprint(arr)", "output": "[5, 4, 3, 1, 1]", "explanation": ".sort() sorts in-place, reverse=True for descending"}], "visualization": "Unsorted: [3,1,4,1,5]\nPass 1:   [1,3,1,4,5]\nPass 2:   [1,1,3,4,5] → done"},
            "interact": {"challenges": [
                {"type": "predict", "prompt": "Output?", "code": "words = [\"banana\", \"apple\", \"cherry\"]\nprint(sorted(words, key=len))", "answer": "['apple', 'banana', 'cherry']", "explanation": "Sorted by string length"},
                {"type": "trace", "prompt": "After first pass of bubble sort?", "code": "arr = [5, 3, 1, 4, 2]\n# Compare adjacent, swap if left > right\n# Pass: (5,3)->swap, (5,1)->swap, (5,4)->swap, (5,2)->swap", "answer": "[3, 1, 4, 2, 5]", "explanation": "5 bubbles to the end"}
            ]},
            "code": {"challenge": "Implement bubble sort that returns a sorted list.", "boilerplate": "def bubble_sort(arr):\n    a = arr[:]\n    # implement bubble sort\n    return a\n\nprint(bubble_sort([5, 3, 1, 4, 2]))", "tests": [{"input": "[5,3,1,4,2]", "expected": "[1, 2, 3, 4, 5]"}], "hints": ["Use nested loops", "Compare a[j] and a[j+1], swap if needed"]},
            "mastery": {"boss_name": "Sort Master", "pass_score": 70, "challenges": [
                {"type": "predict", "prompt": "Time complexity of merge sort?", "answer": "O(n log n)", "difficulty": "easy"},
                {"type": "challenge", "prompt": "Sort by second element: [[1,3],[2,1],[3,2]]", "answer": "sorted(arr, key=lambda x: x[1])", "difficulty": "medium"},
                {"type": "bug_hunt", "prompt": "Why not sorted?", "code": "arr = [3,1,2]\narr.sort\nprint(arr)", "answer": "Missing parentheses: arr.sort()", "difficulty": "easy"}
            ]}
        }
    },
    "searching": {
        "topic": "searching",
        "layers": {
            "story": {"title": "The Seeker's Path", "narrative": "Finding a needle in a haystack. Binary search cuts the haystack in half every step — the fastest way to find anything in sorted data.", "motivation": "Binary search is one of the most tested patterns in coding interviews. Master it."},
            "concept": {"title": "Linear & Binary Search", "explanation": "**Linear Search**: Check every element. O(n)\n**Binary Search**: Halve the search space. O(log n)\n\n```python\ndef binary_search(arr, target):\n    lo, hi = 0, len(arr) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: lo = mid + 1\n        else: hi = mid - 1\n    return -1\n```", "examples": [{"code": "arr = [1,3,5,7,9]\nprint(binary_search(arr, 7))", "output": "3", "explanation": "7 is at index 3"}, {"code": "arr = [1,3,5,7,9]\nprint(binary_search(arr, 4))", "output": "-1", "explanation": "4 not found, return -1"}], "visualization": "[1,3,5,7,9] target=7\nmid=5 -> too small -> search right\n[7,9] mid=7 -> found!"},
            "interact": {"challenges": [
                {"type": "predict", "prompt": "After first step of binary search for 7 in [1,3,5,7,9]?", "code": "lo=0, hi=4, mid=2\narr[mid]=5 < 7, so lo = mid+1 = 3", "answer": "lo=3, hi=4", "explanation": "5 < 7, search right half"},
                {"type": "trace", "prompt": "Steps to find 9?", "code": "[1,3,5,7,9] target=9\nStep 1: mid=5, go right\nStep 2: [7,9] mid=7, go right\nStep 3: [9] mid=9, found", "answer": "3 steps", "explanation": "log2(5) ~ 2.3, so 3 steps"}
            ]},
            "code": {"challenge": "Implement binary search. Return the index or -1.", "boilerplate": "def binary_search(arr, target):\n    lo, hi = 0, len(arr) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        # complete the logic\n        pass\n    return -1", "tests": [{"input": "[1,3,5,7,9], 7", "expected": "3"}], "hints": ["If arr[mid] == target, return mid", "If arr[mid] < target, move lo up", "If arr[mid] > target, move hi down"]},
            "mastery": {"boss_name": "Binary Search Guardian", "pass_score": 70, "challenges": [
                {"type": "predict", "prompt": "Max steps for binary search on 1024 elements?", "answer": "10", "difficulty": "easy"},
                {"type": "bug_hunt", "prompt": "Infinite loop?", "code": "while lo < hi:\n    mid = (lo+hi)//2\n    if arr[mid] < target: lo = mid\n    else: hi = mid", "answer": "lo=mid doesn't progress when lo==mid", "difficulty": "medium"},
                {"type": "challenge", "prompt": "Find first occurrence of target in sorted array with duplicates", "answer": "Use binary search, then scan left", "difficulty": "hard"}
            ]}
        }
    },
    "linked_lists": {
        "topic": "linked_lists",
        "layers": {
            "story": {"title": "The Chain of Trust", "narrative": "Like a treasure map where each clue points to the next. Linked lists connect nodes in sequence — insert and delete anywhere in O(1).", "motivation": "Linked lists teach pointer manipulation, a fundamental skill for understanding more complex data structures."},
            "concept": {"title": "Singly & Doubly Linked Lists", "explanation": "```python\nclass Node:\n    def __init__(self, val):\n        self.val = val\n        self.next = None\n\n# 1 -> 2 -> 3 -> None\nhead = Node(1)\nhead.next = Node(2)\nhead.next.next = Node(3)\n```", "examples": [{"code": "# Traverse\ncur = head\nwhile cur:\n    print(cur.val)\n    cur = cur.next", "output": "1 2 3", "explanation": "Follow .next until None"}], "visualization": "[1] -> [2] -> [3] -> None"},
            "interact": {"challenges": [
                {"type": "predict", "prompt": "What's traversed?", "code": "1 -> 2 -> 3 -> None\nhead = Node(1)\nhead.next = Node(2)\nhead.next.next = Node(3)", "answer": "1, 2, 3", "explanation": "Standard traversal"},
                {"type": "trace", "prompt": "After inserting 0 at head?", "code": "0 -> 1 -> 2 -> 3 -> None\nnew_node.next = head\nhead = new_node", "answer": "Head is now 0", "explanation": "New node points to old head, becomes new head"}
            ]},
            "code": {"challenge": "Write a function to reverse a linked list.", "boilerplate": "def reverse(head):\n    prev = None\n    cur = head\n    while cur:\n        nxt = cur.next\n        cur.next = prev\n        prev = cur\n        cur = nxt\n    return prev", "tests": [{"input": "1->2->3", "expected": "3->2->1"}], "hints": ["Use three pointers: prev, cur, nxt", "Reverse each .next pointer"]},
            "mastery": {"boss_name": "Chain Breaker", "pass_score": 70, "challenges": [
                {"type": "predict", "prompt": "Time to insert at head?", "answer": "O(1)", "difficulty": "easy"},
                {"type": "challenge", "prompt": "Find middle of linked list", "answer": "Slow/fast pointer technique", "difficulty": "medium"},
                {"type": "bug_hunt", "prompt": "Lost rest of list?", "code": "cur.next = new_node\ncur = new_node", "answer": "Need to set new_node.next first", "difficulty": "medium"}
            ]}
        }
    },
    "stacks_queues": {
        "topic": "stacks_queues",
        "layers": {
            "story": {"title": "The Tower & The Line", "narrative": "Stacks: plates piled up, last one placed is first removed. Queues: a line at a shop, first in first served. Two fundamental ways to organize data.", "motivation": "Stacks and queues are building blocks for DFS, BFS, undo systems, and more."},
            "concept": {"title": "Stack (LIFO) & Queue (FIFO)", "explanation": "**Stack** — Last In, First Out:\n```python\nstack = []\nstack.append(1)  # push\nstack.pop()       # pop (returns 1)\n```\n\n**Queue** — First In, First Out:\n```python\nfrom collections import deque\nq = deque()\nq.append(1)     # enqueue\nq.popleft()      # dequeue (returns 1)\n```", "examples": [{"code": "stack = [1, 2, 3]\nstack.append(4)\nprint(stack.pop())", "output": "4", "explanation": "Last pushed is first popped"}, {"code": "from collections import deque\nq = deque([1, 2, 3])\nprint(q.popleft())", "output": "1", "explanation": "First enqueued is first dequeued"}], "visualization": "Stack: push 1,2,3 → pop → 3,2,1\nQueue: add 1,2,3 → remove → 1,2,3"},
            "interact": {"challenges": [
                {"type": "predict", "prompt": "Output?", "code": "stack = []\nfor i in [1,2,3]:\n    stack.append(i)\nwhile stack:\n    print(stack.pop(), end=\" \")", "answer": "3 2 1", "explanation": "Stack reverses order"},
                {"type": "trace", "prompt": "Final queue state?", "code": "from collections import deque\nq = deque()\nq.append(\"a\")\nq.append(\"b\")\nq.popleft()\nq.append(\"c\")\nprint(list(q))", "answer": "['b', 'c']", "explanation": "a removed, c added after b"}
            ]},
            "code": {"challenge": "Use a stack to check if parentheses are balanced: ()[]{}", "boilerplate": "def is_balanced(s):\n    stack = []\n    pairs = {')': '(', ']': '[', '}': '{'}\n    for ch in s:\n        if ch in '([{':\n            stack.append(ch)\n        elif ch in ')}]':\n            if not stack or stack[-1] != pairs[ch]:\n                return False\n            stack.pop()\n    return len(stack) == 0", "tests": [{"input": "([])", "expected": "True"}, {"input": "([)]", "expected": "False"}], "hints": ["Push opening brackets", "Pop and check when you see closing"]},
            "mastery": {"boss_name": "Stack Sentinel", "pass_score": 70, "challenges": [
                {"type": "predict", "prompt": "What data structure reverses order?", "answer": "Stack", "difficulty": "easy"},
                {"type": "challenge", "prompt": "Implement a queue using two stacks", "answer": "Push to stack1, pop from stack2 (reverse on empty)", "difficulty": "hard"},
                {"type": "bug_hunt", "prompt": "IndexError on empty stack?", "code": "if stack[-1] == '(':\n    stack.pop()", "answer": "Check if stack is not empty first", "difficulty": "easy"}
            ]}
        }
    },
    "trees": {
        "topic": "trees",
        "layers": {
            "story": {"title": "The Family Tree", "narrative": "Files on your computer, HTML in a browser, database indexes — trees are everywhere. A parent has children, each child has children, forming a hierarchy.", "motivation": "Trees are the foundation of databases, compilers, and DOM manipulation. BST operations are classic interview questions."},
            "concept": {"title": "Binary Trees & BSTs", "explanation": "```python\nclass TreeNode:\n    def __init__(self, val):\n        self.val = val\n        self.left = None\n        self.right = None\n\n# BST: left < parent < right\n```\n\nTraversals: Inorder (L-Root-R), Preorder (Root-L-R), Postorder (L-R-Root)", "examples": [{"code": "#     4\n#    / \\\n#   2   6\n# Inorder: 2, 4, 6", "output": "2, 4, 6", "explanation": "Inorder of BST gives sorted order"}], "visualization": "      4\n     / \\\n    2   6\n   / \\\n  1   3"},
            "interact": {"challenges": [
                {"type": "predict", "prompt": "Inorder traversal?", "code": "#     5\n#    / \\\n#   3   7\n#  / \\\n# 1   4", "answer": "1, 3, 4, 5, 7", "explanation": "Left-most first, then root, then right"},
                {"type": "trace", "prompt": "Where does 6 go in BST?", "code": "# Insert 6 into:\n#     5\n#    / \\\n#   3   7", "answer": "6 goes left of 7 (6 < 7, 6 > 5)", "explanation": "6 > 5 go right, 6 < 7 go left"}
            ]},
            "code": {"challenge": "Implement inorder traversal of a binary tree.", "boilerplate": "def inorder(root):\n    result = []\n    def traverse(node):\n        if not node: return\n        traverse(node.left)\n        result.append(node.val)\n        traverse(node.right)\n    traverse(root)\n    return result", "tests": [{"input": "BST [1,2,3]", "expected": "[1,2,3]"}], "hints": ["Inorder: left, root, right", "Use recursion"]},
            "mastery": {"boss_name": "Tree Keeper", "pass_score": 70, "challenges": [
                {"type": "predict", "prompt": "Height of balanced tree with 7 nodes?", "answer": "3", "difficulty": "easy"},
                {"type": "challenge", "prompt": "Find height of binary tree", "answer": "1 + max(height(left), height(right))", "difficulty": "medium"},
                {"type": "bug_hunt", "prompt": "Stack overflow?", "code": "def traverse(node):\n    traverse(node.left)\n    traverse(node.right)", "answer": "No base case — needs if not node: return", "difficulty": "easy"}
            ]}
        }
    },
    "graphs": {
        "topic": "graphs",
        "layers": {
            "story": {"title": "The Network Map", "narrative": "Social networks, road maps, the internet itself — everything is a graph. Nodes connected by edges. Master graphs and you master the connected world.", "motivation": "Graph problems dominate advanced coding interviews. BFS, DFS, shortest path — these are the real test."},
            "concept": {"title": "BFS & DFS", "explanation": "**BFS** (Breadth-First): Level by level using a queue.\n**DFS** (Depth-First): Deep dive using a stack/recursion.\n\n```python\nfrom collections import deque\ndef bfs(graph, start):\n    visited = {start}\n    queue = deque([start])\n    while queue:\n        node = queue.popleft()\n        for neighbor in graph[node]:\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append(neighbor)\n```", "examples": [{"code": "graph = {'A': ['B','C'], 'B': ['D'], 'C': [], 'D': []}\nbfs(graph, 'A')", "output": "A B C D", "explanation": "Visits level by level"}], "visualization": "BFS: A -> B,C -> D\nDFS: A -> B -> D -> C"},
            "interact": {"challenges": [
                {"type": "predict", "prompt": "BFS order from A?", "code": "graph = {'A':['B','C'], 'B':['D'], 'C':['D'], 'D':[]}", "answer": "A B C D", "explanation": "Level 0: A, Level 1: B,C, Level 2: D"},
                {"type": "trace", "prompt": "DFS order from A?", "code": "graph = {'A':['B','C'], 'B':['D'], 'C':[], 'D':[]}\n# DFS goes deep first", "answer": "A B D C", "explanation": "DFS: A->B->D (dead end) ->C"}
            ]},
            "code": {"challenge": "Implement BFS to find shortest path length in an unweighted graph.", "boilerplate": "from collections import deque\ndef shortest_path(graph, start, end):\n    visited = {start}\n    queue = deque([(start, 0)])\n    while queue:\n        node, dist = queue.popleft()\n        if node == end: return dist\n        for nb in graph.get(node, []):\n            if nb not in visited:\n                visited.add(nb)\n                queue.append((nb, dist+1))\n    return -1", "tests": [{"input": "graph={'A':['B','C'],'B':['D'],'C':['D'],'D':[]}, A->D", "expected": "2"}], "hints": ["Track distance with each queue entry", "Return when you reach the target"]},
            "mastery": {"boss_name": "Graph Guardian", "pass_score": 75, "challenges": [
                {"type": "predict", "prompt": "Time complexity of BFS?", "answer": "O(V + E)", "difficulty": "easy"},
                {"type": "challenge", "prompt": "Detect cycle in undirected graph", "answer": "BFS/DFS with parent tracking", "difficulty": "hard"},
                {"type": "bug_hunt", "prompt": "Infinite loop?", "code": "queue = deque([start])\nwhile queue:\n    node = queue.popleft()\n    for nb in graph[node]:\n        queue.append(nb)", "answer": "No visited set — keeps revisiting", "difficulty": "medium"}
            ]}
        }
    },
    "hashing": {
        "topic": "hashing",
        "layers": {
            "story": {"title": "The Vault Index", "narrative": "Imagine finding any book in a library instantly. Hash maps give you O(1) lookup — the fastest search possible. They power dictionaries, caches, and databases.", "motivation": "Hashing is used in almost every real-world system. Understanding hash collisions and complexity is essential."},
            "concept": {"title": "Hash Maps / Dictionaries", "explanation": "```python\n# Python dict is a hash map\nscores = {\"Alice\": 95, \"Bob\": 87}\nprint(scores[\"Alice\"])  # 95\n\n# Key -> Hash Function -> Index -> Value\n# Average: O(1) lookup, insert, delete\n```", "examples": [{"code": "d = {}\nd[\"x\"] = 10\nd[\"y\"] = 20\nprint(d.get(\"z\", 0))", "output": "0", "explanation": "get() returns default if key missing"}, {"code": "from collections import Counter\ncounts = Counter(\"hello\")\nprint(counts)", "output": "Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})", "explanation": "Counter creates frequency map"}], "visualization": "Key -> hash() -> index -> bucket -> value"},
            "interact": {"challenges": [
                {"type": "predict", "prompt": "Output?", "code": "d = {'a': 1, 'b': 2, 'c': 3}\nresult = {v: k for k, v in d.items()}\nprint(result)", "answer": "{1: 'a', 2: 'b', 3: 'c'}", "explanation": "Dict comprehension swapping keys/values"},
                {"type": "trace", "prompt": "What's the most frequent?", "code": "from collections import Counter\nwords = [\"the\",\"cat\",\"the\",\"dog\"]\nc = Counter(words)\nprint(c.most_common(1)[0])", "answer": "('the', 2)", "explanation": "most_common(1) returns top element as (key, count)"}
            ]},
            "code": {"challenge": "Find the first non-repeating character in a string.", "boilerplate": "from collections import Counter\ndef first_unique(s):\n    counts = Counter(s)\n    for ch in s:\n        if counts[ch] == 1:\n            return ch\n    return None\n\nprint(first_unique(\"aabbcdd\"))", "tests": [{"input": "aabbcdd", "expected": "c"}], "hints": ["Count all characters first", "Then iterate to find first with count 1"]},
            "mastery": {"boss_name": "Hash Lord", "pass_score": 70, "challenges": [
                {"type": "predict", "prompt": "Average lookup time in hash map?", "answer": "O(1)", "difficulty": "easy"},
                {"type": "challenge", "prompt": "Two sum: find indices of two numbers that add to target", "answer": "Use hash map: {complement: index}", "difficulty": "medium"},
                {"type": "bug_hunt", "prompt": "KeyError?", "code": "d = {'a': 1}\nprint(d['b'])", "answer": "Key 'b' doesn't exist — use .get() or check first", "difficulty": "easy"}
            ]}
        }
    },
    "recursion": {
        "topic": "recursion",
        "layers": {
            "story": {"title": "The Mirror Hall", "narrative": "A mirror reflecting a mirror — recursion is a function calling itself. It's how nature solves problems: trees branching, coastlines fractaling, fibonacci spiraling.", "motivation": "Recursion unlocks elegant solutions for trees, graphs, DP, and divide-and-conquer."},
            "concept": {"title": "Recursion & Base Cases", "explanation": "Every recursive function needs:\n1. **Base case** — when to stop\n2. **Recursive case** — how to shrink\n\n```python\ndef factorial(n):\n    if n <= 1: return 1    # base\n    return n * factorial(n-1)  # shrink\n```\n\nfactorial(4) = 4 * 3 * 2 * 1 = 24", "examples": [{"code": "def fib(n):\n    if n <= 1: return n\n    return fib(n-1) + fib(n-2)\nprint(fib(5))", "output": "5", "explanation": "fib(5)=fib(4)+fib(3)=3+2=5"}], "visualization": "factorial(4)\n  4 * factorial(3)\n    3 * factorial(2)\n      2 * factorial(1)\n        return 1\n      return 2\n    return 6\n  return 24"},
            "interact": {"challenges": [
                {"type": "predict", "prompt": "Output?", "code": "def f(n):\n    if n == 0: return 0\n    return n + f(n-1)\nprint(f(4))", "answer": "10", "explanation": "4+3+2+1+0 = 10"},
                {"type": "trace", "prompt": "Trace fib(4)", "code": "fib(4) = fib(3) + fib(2)\nfib(3) = fib(2) + fib(1)\nfib(2) = fib(1) + fib(0)\nfib(1)=1, fib(0)=0", "answer": "fib(2)=1, fib(3)=2, fib(4)=3", "explanation": "Build up from base cases"}
            ]},
            "code": {"challenge": "Write a recursive function to sum all digits of a number.", "boilerplate": "def digit_sum(n):\n    if n < 10: return n\n    return n % 10 + digit_sum(n // 10)\n\nprint(digit_sum(1234))", "tests": [{"input": "1234", "expected": "10"}], "hints": ["Base case: single digit", "Take last digit (n%10) + sum of rest (n//10)"]},
            "mastery": {"boss_name": "Recursion Phantom", "pass_score": 70, "challenges": [
                {"type": "predict", "prompt": "How many calls for fib(5)?", "answer": "15 calls (with overlapping)", "difficulty": "medium"},
                {"type": "challenge", "prompt": "Power function: x^n recursively", "answer": "def power(x,n): return 1 if n==0 else x*power(x,n-1)", "difficulty": "medium"},
                {"type": "bug_hunt", "prompt": "Maximum recursion depth?", "code": "def f(): return f()\nf()", "answer": "No base case — infinite recursion", "difficulty": "easy"}
            ]}
        }
    },
    "dynamic_programming": {
        "topic": "dynamic_programming",
        "layers": {
            "story": {"title": "The Time Weaver", "narrative": "What if you could remember past solutions? DP is recursion + memory. Instead of recalculating the same subproblems, store them. Time collapses from exponential to linear.", "motivation": "DP is the hardest and most rewarding pattern. Master it and you can solve almost any optimization problem."},
            "concept": {"title": "Memoization & Tabulation", "explanation": "**Memoization** (top-down): Cache recursive results\n**Tabulation** (bottom-up): Fill a table iteratively\n\nFibonacci:\n```python\n# Naive: O(2^n)\ndef fib(n): return fib(n-1)+fib(n-2) if n>1 else n\n\n# DP: O(n)\ndef fib(n):\n    dp = [0]*(n+1)\n    dp[1] = 1\n    for i in range(2, n+1):\n        dp[i] = dp[i-1]+dp[i-2]\n    return dp[n]\n```", "examples": [{"code": "def fib_dp(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a+b\n    return a\nprint(fib_dp(10))", "output": "55", "explanation": "Space-optimized Fibonacci O(1) space"}], "visualization": "Fib: 0,1,1,2,3,5,8,13,21,34,55\nEach = sum of previous two"},
            "interact": {"challenges": [
                {"type": "predict", "prompt": "dp[5] for climbing stairs (1 or 2 steps)?", "code": "dp[0]=1, dp[1]=1\ndp[i] = dp[i-1] + dp[i-2]\n# dp: 1,1,2,3,5,8", "answer": "8", "explanation": "Standard Fibonacci-like DP"},
                {"type": "trace", "prompt": "Fill knapsack table?", "code": "Items: [(w=1,v=1),(w=3,v=4),(w=4,v=5)]\nCapacity=5\n# For each item, decide take or skip", "answer": "Max value = 7 (items 1+2)", "explanation": "Take item2 (w=3,v=4) + item1 (w=1,v=1)... or item3(v=5)+item1(v=1)+item2? Think carefully."}
            ]},
            "code": {"challenge": "Solve climbing stairs: n steps, can take 1 or 2 at a time. How many ways?", "boilerplate": "def climb(n):\n    if n <= 2: return n\n    a, b = 1, 2\n    for _ in range(3, n+1):\n        a, b = b, a+b\n    return b\n\nprint(climb(5))", "tests": [{"input": "5", "expected": "8"}], "hints": ["This is Fibonacci in disguise", "dp[i] = dp[i-1] + dp[i-2]"]},
            "mastery": {"boss_name": "DP Wizard", "pass_score": 75, "challenges": [
                {"type": "predict", "prompt": "Time of naive recursive fib vs DP?", "answer": "O(2^n) vs O(n)", "difficulty": "easy"},
                {"type": "challenge", "prompt": "Coin change: min coins for amount", "answer": "dp[i] = min(dp[i-coin]+1) for each coin", "difficulty": "hard"},
                {"type": "bug_hunt", "prompt": "Wrong answer?", "code": "def climb(n):\n    dp = [0]*(n+1)\n    dp[0] = 1\n    for i in range(1, n+1):\n        dp[i] = dp[i-1]", "answer": "Missing dp[i-2] term", "difficulty": "medium"}
            ]}
        }
    },
    "greedy": {
        "topic": "greedy",
        "layers": {
            "story": {"title": "The Quick Decision", "narrative": "Sometimes the best move is the locally optimal one. Greedy algorithms make the best choice at each step — simple, fast, and often correct.", "motivation": "Greedy is the first strategy to try. When it works, it's elegant. When it doesn't, you need DP."},
            "concept": {"title": "Greedy Strategy", "explanation": "At each step, pick the best option available:\n- **Activity Selection**: Sort by end time, pick earliest finishing\n- **Coin Change**: Pick largest coin first (works for some systems)\n- **Huffman Coding**: Build tree from least frequent\n\nKey: Greedy only works if the problem has **greedy-choice property**.", "examples": [{"code": "# Activity Selection\nactivities = [(1,4),(3,5),(0,6),(5,7)]\n# Sort by end time, pick non-overlapping\n# Selected: (1,4), (5,7)", "output": "2 activities selected", "explanation": "Greedy picks earliest finishing"}], "visualization": "Sort by end time\nPick first → skip overlapping → pick next → ..."},
            "interact": {"challenges": [
                {"type": "predict", "prompt": "Min coins for 37 with [1,5,10,25]?", "code": "25 + 10 + 1 + 1 = 37\n# Greedy: always pick largest", "answer": "4 coins (25+10+1+1)", "explanation": "Greedy works for standard US coins"},
                {"type": "trace", "prompt": "Which activities selected?", "code": "activities = [(1,3),(2,5),(4,7),(6,9)]\n# Sort by end: same order\n# Pick (1,3) -> skip (2,5) -> pick (4,7) -> skip (6,9)", "answer": "(1,3) and (4,7)", "explanation": "Non-overlapping, max count"}
            ]},
            "code": {"challenge": "Given intervals [[1,3],[2,4],[5,7]], find minimum rooms needed.", "boilerplate": "def min_rooms(intervals):\n    starts = sorted(i[0] for i in intervals)\n    ends = sorted(i[1] for i in intervals)\n    rooms = max_rooms = 0\n    si = ei = 0\n    while si < len(starts):\n        if starts[si] < ends[ei]:\n            rooms += 1\n            si += 1\n        else:\n            rooms -= 1\n            ei += 1\n        max_rooms = max(max_rooms, rooms)\n    return max_rooms", "tests": [{"input": "[[1,3],[2,4],[5,7]]", "expected": "2"}], "hints": ["Sort start and end times separately", "Increment when meeting starts, decrement when it ends"]},
            "mastery": {"boss_name": "Greedy Goblin", "pass_score": 70, "challenges": [
                {"type": "predict", "prompt": "When does greedy fail for coin change?", "answer": "Non-standard denominations (e.g. [1,3,4] for 6)", "difficulty": "medium"},
                {"type": "challenge", "prompt": "Job scheduling: maximize non-overlapping jobs", "answer": "Sort by end time, greedily pick", "difficulty": "medium"},
                {"type": "bug_hunt", "prompt": "Wrong result?", "code": "coins = [1, 3, 4]\namount = 6\n# Greedy: 4+1+1 = 3 coins\n# Optimal: 3+3 = 2 coins", "answer": "Greedy doesn't always give optimal for non-standard coin systems", "difficulty": "medium"}
            ]}
        }
    },
    "dbms": {
        "topic": "dbms",
        "layers": {
            "story": {"title": "The Data Vault", "narrative": "Every app needs to store data permanently. Databases are the organized vaults where your data lives — structured, queryable, and safe.", "motivation": "Every SDE interview covers databases. SQL, normalization, indexes — these are table stakes."},
            "concept": {"title": "SQL Basics & Normalization", "explanation": "```sql\nSELECT name, age FROM users WHERE age > 18\nORDER BY name LIMIT 10;\n\nINSERT INTO users (name, age) VALUES ('Alex', 22);\nUPDATE users SET age = 23 WHERE name = 'Alex';\nDELETE FROM users WHERE id = 1;\n```\n\n**Normalization**: Split data to reduce redundancy (1NF, 2NF, 3NF).", "examples": [{"code": "-- Find active users\nSELECT name FROM users\nWHERE status = 'active'\nAND created_at > '2024-01-01';", "output": "List of active user names", "explanation": "Simple WHERE clause with date filter"}], "visualization": "users: id | name | age | status\norders: id | user_id | amount"},
            "interact": {"challenges": [
                {"type": "predict", "prompt": "What does this query return?", "code": "SELECT department, COUNT(*) as cnt\nFROM employees\nGROUP BY department\nHAVING COUNT(*) > 5;", "answer": "Departments with more than 5 employees", "explanation": "GROUP BY + HAVING filters groups"},
                {"type": "trace", "prompt": "Trace this JOIN", "code": "SELECT u.name, o.amount\nFROM users u\nINNER JOIN orders o ON u.id = o.user_id;", "answer": "Pairs of user names with their order amounts", "explanation": "INNER JOIN only includes matching rows"}
            ]},
            "code": {"challenge": "Write a SQL query to find the second highest salary.", "boilerplate": "SELECT DISTINCT salary\nFROM employees\nORDER BY salary DESC\nLIMIT 1 OFFSET 1;\n\n-- Alternative with subquery:\n-- SELECT MAX(salary) FROM employees\n-- WHERE salary < (SELECT MAX(salary) FROM employees);", "tests": [{"input": "salaries: [100, 200, 200, 300]", "expected": "200"}], "hints": ["Use DISTINCT to handle duplicates", "LIMIT 1 OFFSET 1 skips the first"]},
            "mastery": {"boss_name": "Data Dragon", "pass_score": 70, "challenges": [
                {"type": "predict", "prompt": "What is 3NF?", "answer": "No transitive dependencies: non-key columns depend only on primary key", "difficulty": "easy"},
                {"type": "challenge", "prompt": "Write query for running total", "answer": "Use window function: SUM(amount) OVER (ORDER BY date)", "difficulty": "hard"},
                {"type": "bug_hunt", "prompt": "Duplicate rows?", "code": "SELECT * FROM users\nJOIN orders ON users.id = orders.user_id", "answer": "Use INNER JOIN or add conditions to avoid cartesian product", "difficulty": "medium"}
            ]}
        }
    },
    "os": {
        "topic": "os",
        "layers": {
            "story": {"title": "The Machine Whisperer", "narrative": "The OS is the invisible manager — allocating memory, scheduling tasks, handling files. Understanding it separates you from 90% of developers.", "motivation": "OS concepts appear in system design interviews and debugging real performance issues."},
            "concept": {"title": "Processes, Threads & Memory", "explanation": "**Process**: Running program with its own memory space\n**Thread**: Lightweight process sharing memory\n**Context Switch**: OS saves/restores process state\n\n**Memory**: Stack (local vars) vs Heap (dynamic alloc)\n**Virtual Memory**: Each process thinks it has full RAM", "examples": [{"code": "# Process = isolated\n# Thread = shared memory\nimport threading\ndef worker(): print(\"thread!\")\nt = threading.Thread(target=worker)\nt.start()", "output": "thread!", "explanation": "Thread runs function in parallel"}], "visualization": "Process A [Stack|Heap] ↔ OS ↔ Process B [Stack|Heap]"},
            "interact": {"challenges": [
                {"type": "predict", "prompt": "What happens during context switch?", "answer": "OS saves current process state, loads next process state", "explanation": "CPU switches between processes rapidly"},
                {"type": "trace", "prompt": "Race condition?", "code": "counter = 0\ndef inc():\n    global counter\n    counter += 1\n# Two threads call inc() simultaneously", "answer": "counter might be 1 instead of 2", "explanation": "counter += 1 is not atomic"}
            ]},
            "code": {"challenge": "Explain the difference between process and thread with a real example.", "boilerplate": "# Process: Two Python scripts running separately\n# Each has its own memory, can't directly share\n\n# Thread: Two functions in same script\n# Share variables, need locks for safety\n\nimport threading\ncount = 0\nlock = threading.Lock()\ndef safe_inc():\n    global count\n    with lock:\n        count += 1", "tests": [{"input": "", "expected": "Correct explanation + code"}], "hints": ["Process = separate memory", "Thread = shared memory, needs locks"]},
            "mastery": {"boss_name": "Kernel Sentinel", "pass_score": 70, "challenges": [
                {"type": "predict", "prompt": "What is deadlock?", "answer": "Two processes waiting for each other's resources forever", "difficulty": "easy"},
                {"type": "challenge", "prompt": "Explain virtual memory", "answer": "OS maps virtual addresses to physical RAM, enabling each process to have its own address space", "difficulty": "medium"},
                {"type": "bug_hunt", "prompt": "Deadlock scenario?", "code": "# Thread 1: lock(A), then lock(B)\n# Thread 2: lock(B), then lock(A)", "answer": "Classic deadlock: each holds what other needs", "difficulty": "medium"}
            ]}
        }
    },
    "networks": {
        "topic": "networks",
        "layers": {
            "story": {"title": "The Global Web", "narrative": "The internet connects billions of devices. Behind every webpage, API call, and message is a stack of protocols working in harmony.", "motivation": "Networking knowledge is essential for web development, system design, and debugging connectivity issues."},
            "concept": {"title": "TCP/IP, HTTP & DNS", "explanation": "**TCP/IP Stack**:\n- Application: HTTP, DNS, SMTP\n- Transport: TCP (reliable) / UDP (fast)\n- Internet: IP addressing\n- Link: Ethernet, WiFi\n\n**HTTP**: Request-Response. Methods: GET, POST, PUT, DELETE\n**DNS**: Translates domain names to IP addresses", "examples": [{"code": "# HTTP Request\nGET /api/users HTTP/1.1\nHost: example.com\n\n# Response\nHTTP/1.1 200 OK\nContent-Type: application/json\n{\"users\": [...]}", "output": "200 OK with JSON data", "explanation": "Basic HTTP request/response cycle"}], "visualization": "Client → DNS → IP → TCP → HTTP → Server → Response"},
            "interact": {"challenges": [
                {"type": "predict", "prompt": "HTTP status 404 means?", "answer": "Not Found — resource doesn't exist", "explanation": "Standard HTTP error code"},
                {"type": "trace", "prompt": "What happens when you type google.com?", "answer": "DNS lookup → TCP connection → TLS handshake → HTTP request → response", "explanation": "Multiple layers involved"}
            ]},
            "code": {"challenge": "Explain the difference between TCP and UDP with use cases.", "boilerplate": "# TCP: Reliable, ordered, slower\n# Use: web browsing, email, file transfer\n\n# UDP: Fast, unreliable, no order\n# Use: video streaming, gaming, DNS\n\n# TCP = phone call (guaranteed delivery)\n# UDP = radio broadcast (send and forget)", "tests": [{"input": "", "expected": "Correct TCP/UDP comparison with examples"}], "hints": ["TCP guarantees delivery", "UDP sacrifices reliability for speed"]},
            "mastery": {"boss_name": "Protocol Pirate", "pass_score": 70, "challenges": [
                {"type": "predict", "prompt": "What is a 3-way handshake?", "answer": "SYN → SYN-ACK → ACK: establishes TCP connection", "difficulty": "easy"},
                {"type": "challenge", "prompt": "HTTP vs HTTPS difference?", "answer": "HTTPS adds TLS encryption layer", "difficulty": "easy"},
                {"type": "bug_hunt", "prompt": "CORS error?", "code": "fetch('https://api.other.com/data')\n// Blocked by browser", "answer": "Cross-origin request blocked — need CORS headers or proxy", "difficulty": "medium"}
            ]}
        }
    },
    "system_design": {
        "topic": "system_design",
        "layers": {
            "story": {"title": "The Architect's Blueprint", "narrative": "Designing a system for millions of users. Load balancers, databases, caching, microservices. This is where engineering meets art.", "motivation": "System design rounds are the gatekeepers to senior roles. This is your biggest career lever."},
            "concept": {"title": "Scalability Fundamentals", "explanation": "**Vertical Scaling**: Bigger machine (limited)\n**Horizontal Scaling**: More machines (scales better)\n\n**Key Components**:\n- **Load Balancer**: Distributes traffic\n- **Cache** (Redis): Fast reads, reduce DB load\n- **Database**: SQL (structured) / NoSQL (flexible)\n- **CDN**: Static content close to users\n- **Message Queue**: Async processing", "examples": [{"code": "# URL Shortener Design\n1. User submits URL\n2. Generate short code (hash/counter)\n3. Store mapping in DB\n4. Redirect on lookup\n\n# Scale: cache hot URLs in Redis", "output": "System design sketch", "explanation": "Simple URL shortener architecture"}], "visualization": "Client → LB → App Server → DB\n                  ↓\n              Cache (Redis)"},
            "interact": {"challenges": [
                {"type": "predict", "prompt": "Why use a cache?", "answer": "Reduce database load, faster reads (O(1) vs O(n))", "explanation": "Cache stores hot data in memory"},
                {"type": "trace", "prompt": "Design a chat app", "answer": "WebSocket for real-time, message queue for persistence, Redis for sessions", "explanation": "Real-time needs push, not pull"}
            ]},
            "code": {"challenge": "Design a rate limiter. Explain the algorithm.", "boilerplate": "# Token Bucket Algorithm\n# - Bucket holds N tokens\n# - Each request removes 1 token\n# - Tokens refill at fixed rate\n# - If empty, reject request\n\nclass RateLimiter:\n    def __init__(self, capacity, refill_rate):\n        self.capacity = capacity\n        self.tokens = capacity\n        self.refill_rate = refill_rate\n    \n    def allow(self):\n        if self.tokens > 0:\n            self.tokens -= 1\n            return True\n        return False", "tests": [{"input": "", "expected": "Working token bucket implementation"}], "hints": ["Start with simple counter", "Token bucket is more flexible"]},
            "mastery": {"boss_name": "Architect Titan", "pass_score": 75, "challenges": [
                {"type": "predict", "prompt": "CAP theorem?", "answer": "Can only have 2 of 3: Consistency, Availability, Partition tolerance", "difficulty": "easy"},
                {"type": "challenge", "prompt": "Design a URL shortener for 1B URLs", "answer": "Base62 encoding, hash collision handling, read-heavy → cache", "difficulty": "hard"},
                {"type": "bug_hunt", "prompt": "Thundering herd?", "code": "# 1000 requests hit cache miss simultaneously\n# All hit database", "answer": "Use cache stampede prevention: lock + single DB query", "difficulty": "hard"}
            ]}
        }
    },
    "oop": {
        "topic": "oop",
        "layers": {
            "story": {"title": "The Builder's Workshop", "narrative": "OOP organizes code like a well-run workshop: tools (methods) grouped by purpose (classes), materials (data) kept safe (encapsulation).", "motivation": "OOP is how real-world codebases are structured. Understanding it is essential for working on any team."},
            "concept": {"title": "Classes, Objects & Inheritance", "explanation": "```python\nclass Animal:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        pass\n\nclass Dog(Animal):\n    def speak(self):\n        return f\"{self.name} says Woof!\"\n\ndog = Dog(\"Rex\")\nprint(dog.speak())  # Rex says Woof!\n```\n\n**4 Pillars**: Encapsulation, Abstraction, Inheritance, Polymorphism", "examples": [{"code": "class Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n    def distance(self, other):\n        return ((self.x-other.x)**2 + (self.y-other.y)**2)**0.5\n\np1 = Point(0, 0)\np2 = Point(3, 4)\nprint(p1.distance(p2))", "output": "5.0", "explanation": "Distance formula between two points"}], "visualization": "Animal (base)\n  ↓ Dog\n  ↓ Cat\n  Each overrides speak()"},
            "interact": {"challenges": [
                {"type": "predict", "prompt": "What is printed?", "code": "class A:\n    def greet(self): return \"Hello\"\nclass B(A):\n    def greet(self): return \"Hi\"\nb = B()\nprint(b.greet())", "answer": "Hi", "explanation": "B overrides A's greet method (polymorphism)"},
                {"type": "trace", "prompt": "What happens?", "code": "class Counter:\n    count = 0\n    def __init__(self):\n        Counter.count += 1\n\na = Counter()\nb = Counter()\nprint(Counter.count)", "answer": "2", "explanation": "Class variable shared across instances"}
            ]},
            "code": {"challenge": "Create a BankAccount class with deposit, withdraw, and balance methods.", "boilerplate": "class BankAccount:\n    def __init__(self, balance=0):\n        self.balance = balance\n    \n    def deposit(self, amount):\n        self.balance += amount\n        return self.balance\n    \n    def withdraw(self, amount):\n        if amount > self.balance:\n            return \"Insufficient funds\"\n        self.balance -= amount\n        return self.balance\n\nacc = BankAccount(100)\nacc.deposit(50)\nprint(acc.withdraw(30))", "tests": [{"input": "", "expected": "120"}], "hints": ["Use __init__ for initial state", "Check balance before withdrawal"]},
            "mastery": {"boss_name": "Class Commander", "pass_score": 70, "challenges": [
                {"type": "predict", "prompt": "What is polymorphism?", "answer": "Same method name, different behavior per class", "difficulty": "easy"},
                {"type": "challenge", "prompt": "Implement __str__ for custom print output", "answer": "def __str__(self): return f'Object({self.name})'", "difficulty": "medium"},
                {"type": "bug_hunt", "prompt": "Shared state bug?", "code": "class Foo:\n    items = []\n    def add(self, x):\n        self.items.append(x)", "answer": "items is a class variable, shared by all instances. Use self.items = [] in __init__", "difficulty": "medium"}
            ]}
        }
    },
}
