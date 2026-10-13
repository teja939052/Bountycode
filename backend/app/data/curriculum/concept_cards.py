"""Execution-first curriculum data — deterministic, AI-independent.

Each concept card is a self-contained interactive lesson:
  - anime-style visual metadata
  - deterministic code examples
  - misconception-tagged bugs
  - mastery gate retest items
"""
from __future__ import annotations

from typing import Any, Dict, List, Literal

# ---------------------------------------------------------------------------
# Card types
# ---------------------------------------------------------------------------
# concept: syntax + mental model + micro-task
# debug: broken code + diagnosis + fix
# pattern: named algorithm pattern (two-pointer, sliding-window, etc.)
# model: interactive mental-model visualization config
# srs: spaced-repetition card for code patterns

ConceptCard = Dict[str, Any]

_CONCEPT_CARDS: List[ConceptCard] = [
    {
        "id": "concept:variables:1",
        "order": 1,
        "title": "Variables are named boxes",
        "subtitle": "Store, retrieve, and update values",
        "level": "beginner",
        "language": "python",
        "anime_theme": {
            "palette": ["#0ea5e9", "#6366f1", "#a855f7"],
            "emblem": "📦",
            "rarity": "common",
            "frame": "box",
        },
        "concept": "variables",
        "prerequisites": [],
        "mental_model": {
            "type": "memory_box",
            "caption": "A variable is a labeled box in memory.",
            "steps": [
                {"label": "Declare", "action": "create_box", "label_text": "x", "value": 0},
                {"label": "Assign", "action": "store_value", "value": 10},
                {"label": "Update", "action": "replace_value", "value": 20},
            ],
        },
        "micro_task": {
            "instruction": "Create a variable 'apples' with value 5, then add 3 to it.",
            "starter_code": {"python": "# write your code here\n"},
            "solution": {"python": "apples = 5\napples = apples + 3\n"},
            "verification": {"python": "assert apples == 8"},
            "explanation": "Variables can be updated by referencing their current value.",
        },
        "misconception_tags": ["undeclared_variable", "assignment_vs_equality"],
        "pattern_tags": ["assignment", "state"],
        "srs": True,
        "estimated_minutes": 2,
    },
    {
        "id": "concept:conditionals:1",
        "order": 2,
        "title": "If-else branches",
        "subtitle": "Control flow with conditions",
        "level": "beginner",
        "language": "python",
        "anime_theme": {
            "palette": ["#f59e0b", "#ef4444", "#ec4899"],
            "emblem": "🚦",
            "rarity": "common",
            "frame": "diamond",
        },
        "concept": "conditionals",
        "prerequisites": ["concept:variables:1"],
        "mental_model": {
            "type": "branch",
            "caption": "Only one branch executes.",
            "steps": [
                {"label": "Check", "action": "evaluate", "expression": "x > 0"},
                {"label": "True", "action": "enter_branch", "branch": "if"},
                {"label": "False", "action": "enter_branch", "branch": "else"},
            ],
        },
        "micro_task": {
            "instruction": "Print 'positive' if x > 0, else print 'non-positive'.",
            "starter_code": {"python": "x = -5\n# your code here\n"},
            "solution": {"python": "x = -5\nif x > 0:\n    print('positive')\nelse:\n    print('non-positive')\n"},
            "verification": {"python": "import io, sys\nsys.stdout = io.StringIO()\n# solution executes here\noutput = sys.stdout.getvalue()\nassert 'non-positive' in output"},
            "explanation": "Conditions determine which block runs.",
        },
        "misconception_tags": ["assignment_vs_equality", "indentation_error"],
        "pattern_tags": ["branch", "boolean"],
        "srs": True,
        "estimated_minutes": 3,
    },
    {
        "id": "concept:loops:1",
        "order": 3,
        "title": "Repeat with for-loops",
        "subtitle": "Iterate over sequences",
        "level": "beginner",
        "language": "python",
        "anime_theme": {
            "palette": ["#10b981", "#06b6d4", "#3b82f6"],
            "emblem": "🔄",
            "rarity": "common",
            "frame": "circle",
        },
        "concept": "loops",
        "prerequisites": ["concept:conditionals:1"],
        "mental_model": {
            "type": "loop_trace",
            "caption": "Loop repeats body for each item.",
            "steps": [
                {"label": "Init", "action": "set_iter", "iterable": "[1,2,3]"},
                {"label": "Item", "action": "bind", "var": "x", "value": 1},
                {"label": "Body", "action": "run", "statement": "print(x)"},
                {"label": "Next", "action": "advance"},
            ],
        },
        "micro_task": {
            "instruction": "Print each number in [1, 2, 3] using a for-loop.",
            "starter_code": {"python": "nums = [1, 2, 3]\n# your code here\n"},
            "solution": {"python": "nums = [1, 2, 3]\nfor x in nums:\n    print(x)\n"},
            "verification": {"python": "import io, sys\nsys.stdout = io.StringIO()\n# solution executes here\noutput = sys.stdout.getvalue()\nassert '1' in output and '2' in output and '3' in output"},
            "explanation": "Loops repeat actions for each element.",
        },
        "misconception_tags": ["off_by_one", "infinite_loop"],
        "pattern_tags": ["iteration", "traversal"],
        "srs": True,
        "estimated_minutes": 3,
    },
    {
        "id": "concept:functions:1",
        "order": 4,
        "title": "Functions are recipes",
        "subtitle": "Parameters, return values, and scope",
        "level": "beginner",
        "language": "python",
        "anime_theme": {
            "palette": ["#8b5cf6", "#d946ef", "#f43f5e"],
            "emblem": "🧪",
            "rarity": "rare",
            "frame": "hexagon",
        },
        "concept": "functions",
        "prerequisites": ["concept:loops:1"],
        "mental_model": {
            "type": "recipe",
            "caption": "Inputs -> processing -> output.",
            "steps": [
                {"label": "Input", "action": "bind_param", "name": "a", "value": 5},
                {"label": "Process", "action": "compute", "expression": "a * 2"},
                {"label": "Output", "action": "return", "value": 10},
            ],
        },
        "micro_task": {
            "instruction": "Write a function double(x) that returns x * 2.",
            "starter_code": {"python": "def double(x):\n    # your code here\n    pass\n"},
            "solution": {"python": "def double(x):\n    return x * 2\n"},
            "verification": {"python": "assert double(5) == 10\nassert double(-3) == -6"},
            "explanation": "Functions map inputs to outputs.",
        },
        "misconception_tags": ["missing_return", "print_vs_return"],
        "pattern_tags": ["abstraction", "reuse"],
        "srs": True,
        "estimated_minutes": 4,
    },
    {
        "id": "concept:arrays:1",
        "order": 5,
        "title": "Arrays are ordered shelves",
        "subtitle": "Index-based access and mutation",
        "level": "beginner",
        "language": "python",
        "anime_theme": {
            "palette": ["#f97316", "#f59e0b", "#fbbf24"],
            "emblem": "🗄️",
            "rarity": "common",
            "frame": "box",
        },
        "concept": "arrays",
        "prerequisites": ["concept:variables:1"],
        "mental_model": {
            "type": "shelf",
            "caption": "Each slot has an index starting at 0.",
            "steps": [
                {"label": "Create", "action": "allocate", "size": 5},
                {"label": "Access", "action": "read_index", "index": 0},
                {"label": "Mutate", "action": "write_index", "index": 2, "value": 99},
            ],
        },
        "micro_task": {
            "instruction": "Create array [10, 20, 30], change index 1 to 99, print it.",
            "starter_code": {"python": "arr = [10, 20, 30]\n# your code here\n"},
            "solution": {"python": "arr = [10, 20, 30]\narr[1] = 99\nprint(arr)\n"},
            "verification": {"python": "import io, sys\nsys.stdout = io.StringIO()\n# solution executes here\noutput = sys.stdout.getvalue()\nassert '99' in output"},
            "explanation": "Array indices start at 0 and can be reassigned.",
        },
        "misconception_tags": ["off_by_one", "index_error"],
        "pattern_tags": ["index", "mutation"],
        "srs": True,
        "estimated_minutes": 3,
    },
    {
        "id": "concept:strings:1",
        "order": 6,
        "title": "Strings are character sequences",
        "subtitle": "Immutability and slicing",
        "level": "beginner",
        "language": "python",
        "anime_theme": {
            "palette": ["#ec4899", "#f43f5e", "#ef4444"],
            "emblem": "🔤",
            "rarity": "common",
            "frame": "diamond",
        },
        "concept": "strings",
        "prerequisites": ["concept:arrays:1"],
        "mental_model": {
            "type": "tape",
            "caption": "A string is an immutable sequence of characters.",
            "steps": [
                {"label": "Slice", "action": "substring", "start": 0, "end": 3},
                {"label": "Upper", "action": "transform", "method": "upper"},
                {"label": "Concat", "action": "join", "other": "!"},
            ],
        },
        "micro_task": {
            "instruction": "Take 'hello', slice first 3 chars, append '!', print result.",
            "starter_code": {"python": "s = 'hello'\n# your code here\n"},
            "solution": {"python": "s = 'hello'\nresult = s[:3] + '!'\nprint(result)\n"},
            "verification": {"python": "import io, sys\nsys.stdout = io.StringIO()\n# solution executes here\noutput = sys.stdout.getvalue()\nassert 'hel!' in output"},
            "explanation": "Strings can be sliced and concatenated.",
        },
        "misconception_tags": ["immutability_confusion", "slice_boundary"],
        "pattern_tags": ["sequence", "slice"],
        "srs": True,
        "estimated_minutes": 3,
    },
    {
        "id": "concept:pointers:1",
        "order": 7,
        "title": "Pointers are arrows to memory",
        "subtitle": "References, addresses, and indirection",
        "level": "intermediate",
        "language": "c",
        "anime_theme": {
            "palette": ["#6366f1", "#8b5cf6", "#a855f7"],
            "emblem": "🎯",
            "rarity": "epic",
            "frame": "arrow",
        },
        "concept": "pointers",
        "prerequisites": ["concept:functions:1"],
        "mental_model": {
            "type": "arrow_graph",
            "caption": "A pointer holds a memory address.",
            "steps": [
                {"label": "Var", "action": "allocate_box", "name": "x", "value": 10},
                {"label": "Ptr", "action": "create_arrow", "from": "ptr", "to": "x"},
                {"label": "Deref", "action": "follow_arrow", "value": 10},
            ],
        },
        "micro_task": {
            "instruction": "Declare int x=10, int *p=&x, print *p.",
            "starter_code": {"c": "#include <stdio.h>\nint main() {\n    // your code here\n    return 0;\n}\n"},
            "solution": {"c": "#include <stdio.h>\nint main() {\n    int x = 10;\n    int *p = &x;\n    printf(\"%d\", *p);\n    return 0;\n}\n"},
            "verification": {"c": "compile and run; output must contain 10"},
            "explanation": "Pointers store addresses of variables.",
        },
        "misconception_tags": ["dangling_pointer", "null_pointer", "arithmetic_confusion"],
        "pattern_tags": ["memory", "indirection"],
        "srs": True,
        "estimated_minutes": 5,
    },
    {
        "id": "concept:recursion:1",
        "order": 8,
        "title": "Recursion is a stack of calls",
        "subtitle": "Base case, recursive case, and stack frames",
        "level": "intermediate",
        "language": "python",
        "anime_theme": {
            "palette": ["#14b8a6", "#06b6d4", "#0ea5e9"],
            "emblem": "📚",
            "rarity": "epic",
            "frame": "tower",
        },
        "concept": "recursion",
        "prerequisites": ["concept:functions:1"],
        "mental_model": {
            "type": "stack_frames",
            "caption": "Each call pushes a frame; base case pops.",
            "steps": [
                {"label": "Call", "action": "push_frame", "params": {"n": 3}},
                {"label": "Base?", "action": "check_base", "condition": "n == 1"},
                {"label": "Reduce", "action": "recurse", "next_n": 2},
                {"label": "Return", "action": "pop_frame", "value": 6},
            ],
        },
        "micro_task": {
            "instruction": "Write factorial(n) recursively. Base case: n == 1 returns 1.",
            "starter_code": {"python": "def factorial(n):\n    # your code here\n    pass\n"},
            "solution": {"python": "def factorial(n):\n    if n == 1:\n        return 1\n    return n * factorial(n - 1)\n"},
            "verification": {"python": "assert factorial(5) == 120\nassert factorial(1) == 1"},
            "explanation": "Recursion breaks problems into smaller subproblems.",
        },
        "misconception_tags": ["missing_base_case", "stack_overflow", "off_by_one"],
        "pattern_tags": ["decomposition", "self_reference"],
        "srs": True,
        "estimated_minutes": 5,
    },
    {
        "id": "concept:two_pointers:1",
        "order": 9,
        "title": "Two pointers walk together",
        "subtitle": "Opposite-end and same-direction patterns",
        "level": "intermediate",
        "language": "python",
        "anime_theme": {
            "palette": ["#f59e0b", "#f97316", "#ef4444"],
            "emblem": "👣",
            "rarity": "rare",
            "frame": "dual",
        },
        "concept": "two_pointers",
        "prerequisites": ["concept:arrays:1"],
        "mental_model": {
            "type": "pointer_trace",
            "caption": "Two indices move based on a condition.",
            "steps": [
                {"label": "Left", "action": "set", "index": 0},
                {"label": "Right", "action": "set", "index": "len-1"},
                {"label": "Compare", "action": "evaluate_pair"},
                {"label": "Move", "action": "advance", "which": "left"},
            ],
        },
        "micro_task": {
            "instruction": "Check if [1,2,3,4,5] is palindrome using two pointers.",
            "starter_code": {"python": "def is_palindrome(arr):\n    # your code here\n    pass\n"},
            "solution": {"python": "def is_palindrome(arr):\n    i, j = 0, len(arr) - 1\n    while i < j:\n        if arr[i] != arr[j]:\n            return False\n        i += 1\n        j -= 1\n    return True\n"},
            "verification": {"python": "assert is_palindrome([1,2,3,2,1]) == True\nassert is_palindrome([1,2,3]) == False"},
            "explanation": "Two pointers reduce nested loops to linear time.",
        },
        "misconception_tags": ["off_by_one", "infinite_loop"],
        "pattern_tags": ["two_pointers", "palindrome"],
        "srs": True,
        "estimated_minutes": 5,
    },
    {
        "id": "concept:sliding_window:1",
        "order": 10,
        "title": "Sliding window maintains a range",
        "subtitle": "Expand right, shrink left, track state",
        "level": "intermediate",
        "language": "python",
        "anime_theme": {
            "palette": ["#10b981", "#84cc16", "#22d3ee"],
            "emblem": "🪟",
            "rarity": "rare",
            "frame": "window",
        },
        "concept": "sliding_window",
        "prerequisites": ["concept:two_pointers:1"],
        "mental_model": {
            "type": "window_trace",
            "caption": "A window [left, right] slides over the array.",
            "steps": [
                {"label": "Expand", "action": "move_right"},
                {"label": "Update", "action": "add_to_state"},
                {"label": "Shrink", "action": "move_left"},
                {"label": "Best", "action": "record_max"},
            ],
        },
        "micro_task": {
            "instruction": "Find max sum of any window of size 3 in [1,3,-1,4,2].",
            "starter_code": {"python": "def max_window(arr, k):\n    # your code here\n    pass\n"},
            "solution": {"python": "def max_window(arr, k):\n    curr = sum(arr[:k])\n    best = curr\n    for i in range(k, len(arr)):\n        curr += arr[i] - arr[i-k]\n        best = max(best, curr)\n    return best\n"},
            "verification": {"python": "assert max_window([1,3,-1,4,2], 3) == 6"},
            "explanation": "Sliding window reuses the previous sum.",
        },
        "misconception_tags": ["off_by_one", "window_boundary"],
        "pattern_tags": ["sliding_window", "subarray"],
        "srs": True,
        "estimated_minutes": 5,
    },
    {
        "id": "concept:hashmap:1",
        "order": 11,
        "title": "HashMap is a lookup table",
        "subtitle": "O(1) insert and search with keys",
        "level": "intermediate",
        "language": "python",
        "anime_theme": {
            "palette": ["#6366f1", "#8b5cf6", "#d946ef"],
            "emblem": "🗂️",
            "rarity": "rare",
            "frame": "grid",
        },
        "concept": "hashmap",
        "prerequisites": ["concept:arrays:1"],
        "mental_model": {
            "type": "hash_table",
            "caption": "Keys map to values via a hash function.",
            "steps": [
                {"label": "Hash", "action": "compute_index", "key": "apple"},
                {"label": "Store", "action": "set_bucket", "value": 1},
                {"label": "Lookup", "action": "get_bucket", "key": "apple"},
            ],
        },
        "micro_task": {
            "instruction": "Count frequency of each number in [1,2,2,3,1] using a dict.",
            "starter_code": {"python": "nums = [1,2,2,3,1]\nfreq = {}\n# your code here\n"},
            "solution": {"python": "nums = [1,2,2,3,1]\nfreq = {}\nfor n in nums:\n    freq[n] = freq.get(n, 0) + 1\n"},
            "verification": {"python": "nums = [1,2,2,3,1]\nfreq = {}\nfor n in nums:\n    freq[n] = freq.get(n, 0) + 1\nassert freq[2] == 2\nassert freq[1] == 2"},
            "explanation": "HashMaps replace repeated scans with direct lookup.",
        },
        "misconception_tags": ["collision", "default_value"],
        "pattern_tags": ["hashing", "frequency"],
        "srs": True,
        "estimated_minutes": 4,
    },
    {
        "id": "concept:stack_queue:1",
        "order": 12,
        "title": "Stack and Queue",
        "subtitle": "LIFO vs FIFO access patterns",
        "level": "intermediate",
        "language": "python",
        "anime_theme": {
            "palette": ["#f43f5e", "#fb7185", "#fda4af"],
            "emblem": "🥞",
            "rarity": "rare",
            "frame": "tower",
        },
        "concept": "stack_queue",
        "prerequisites": ["concept:arrays:1"],
        "mental_model": {
            "type": "stack_queue",
            "caption": "Stack: last in, first out. Queue: first in, first out.",
            "steps": [
                {"label": "Push", "action": "stack_push", "value": 1},
                {"label": "Pop", "action": "stack_pop"},
                {"label": "Enqueue", "action": "queue_push", "value": 1},
                {"label": "Dequeue", "action": "queue_pop"},
            ],
        },
        "micro_task": {
            "instruction": "Use a list as a stack: push 1, push 2, pop once, print top.",
            "starter_code": {"python": "stack = []\n# your code here\n"},
            "solution": {"python": "stack = []\nstack.append(1)\nstack.append(2)\nstack.pop()\nprint(stack[-1])\n"},
            "verification": {"python": "import io, sys\nsys.stdout = io.StringIO()\n# solution executes here\noutput = sys.stdout.getvalue()\nassert '1' in output"},
            "explanation": "Stacks reverse order; queues preserve it.",
        },
        "misconception_tags": ["lifo_fifo_confusion", "empty_access"],
        "pattern_tags": ["stack", "queue"],
        "srs": True,
        "estimated_minutes": 4,
    },
]

_DEBUG_CARDS: List[ConceptCard] = [
    {
        "id": "debug:off_by_one:1",
        "order": 1,
        "title": "Off-by-one: the silent killer",
        "subtitle": "Index starts at 0, not 1",
        "level": "beginner",
        "language": "python",
        "anime_theme": {
            "palette": ["#ef4444", "#f97316", "#fbbf24"],
            "emblem": "🐛",
            "rarity": "common",
            "frame": "alert",
        },
        "concept": "debug",
        "prerequisites": ["concept:arrays:1"],
        "mental_model": {
            "type": "debug_trace",
            "caption": "Trace the loop and print each index.",
            "steps": [
                {"label": "Bug", "action": "show_error", "error": "IndexError"},
                {"label": "Trace", "action": "print_indices", "range": "range(1, n+1)"},
                {"label": "Fix", "action": "change_range", "new_range": "range(n)"},
            ],
        },
        "micro_task": {
            "instruction": "This code crashes. Fix the loop to sum array correctly.",
            "starter_code": {"python": "arr = [1,2,3]\ntotal = 0\nfor i in range(1, len(arr) + 1):\n    total += arr[i]\nprint(total)\n"},
            "solution": {"python": "arr = [1,2,3]\ntotal = 0\nfor i in range(len(arr)):\n    total += arr[i]\nprint(total)\n"},
            "verification": {"python": "arr = [1,2,3]\ntotal = 0\nfor i in range(len(arr)):\n    total += arr[i]\nassert total == 6"},
            "explanation": "Indices run from 0 to len-1.",
        },
        "misconception_tags": ["off_by_one", "index_error"],
        "pattern_tags": ["debug", "trace"],
        "srs": True,
        "estimated_minutes": 4,
    },
    {
        "id": "debug:null_pointer:1",
        "order": 2,
        "title": "Null pointer dereference",
        "subtitle": "Checking before dereferencing",
        "level": "intermediate",
        "language": "c",
        "anime_theme": {
            "palette": ["#6366f1", "#8b5cf6", "#a855f7"],
            "emblem": "💥",
            "rarity": "epic",
            "frame": "alert",
        },
        "concept": "debug",
        "prerequisites": ["concept:pointers:1"],
        "mental_model": {
            "type": "debug_trace",
            "caption": "A null pointer has no target.",
            "steps": [
                {"label": "Crash", "action": "dereference_null"},
                {"label": "Check", "action": "guard_null"},
                {"label": "Fix", "action": "add_if_check"},
            ],
        },
        "micro_task": {
            "instruction": "This C code crashes. Add a null check before dereferencing.",
            "starter_code": {"c": "#include <stdio.h>\nint main() {\n    int *p = NULL;\n    printf(\"%d\", *p);\n    return 0;\n}\n"},
            "solution": {"c": "#include <stdio.h>\nint main() {\n    int *p = NULL;\n    if (p) {\n        printf(\"%d\", *p);\n    }\n    return 0;\n}\n"},
            "verification": {"c": "compile and run; must not crash"},
            "explanation": "Always check pointers before dereferencing.",
        },
        "misconception_tags": ["null_pointer", "dangling_pointer"],
        "pattern_tags": ["debug", "safety"],
        "srs": True,
        "estimated_minutes": 5,
    },
]

_PATTERN_CARDS: List[ConceptCard] = [
    {
        "id": "pattern:two-pointer:1",
        "order": 1,
        "title": "Two Pointer Pattern",
        "subtitle": "Opposite-end traversal",
        "level": "intermediate",
        "language": "python",
        "anime_theme": {
            "palette": ["#f59e0b", "#f97316", "#ef4444"],
            "emblem": "👣",
            "rarity": "rare",
            "frame": "dual",
        },
        "concept": "pattern",
        "prerequisites": ["concept:arrays:1"],
        "mental_model": {
            "type": "pointer_trace",
            "caption": "Two indices move based on a condition.",
            "steps": [
                {"label": "Left", "action": "set", "index": 0},
                {"label": "Right", "action": "set", "index": "len-1"},
                {"label": "Compare", "action": "evaluate_pair"},
                {"label": "Move", "action": "advance", "which": "left"},
            ],
        },
        "micro_task": {
            "instruction": "Implement two-sum using two pointers on sorted array.",
            "starter_code": {"python": "def two_sum(nums, target):\n    # your code here\n    pass\n"},
            "solution": {"python": "def two_sum(nums, target):\n    i, j = 0, len(nums) - 1\n    while i < j:\n        s = nums[i] + nums[j]\n        if s == target:\n            return [i, j]\n        elif s < target:\n            i += 1\n        else:\n            j -= 1\n    return []\n"},
            "verification": {"python": "assert two_sum([1,2,3,4,5], 6) in [[0,3],[1,2]]"},
            "explanation": "Two pointers reduce nested loops to linear time.",
        },
        "misconception_tags": ["off_by_one", "infinite_loop"],
        "pattern_tags": ["two_pointers", "pair_sum"],
        "srs": True,
        "estimated_minutes": 6,
    },
]

_MODEL_CARDS: List[ConceptCard] = [
    {
        "id": "model:stack_frame:1",
        "order": 1,
        "title": "Stack Frame Visualization",
        "subtitle": "See how recursion builds frames",
        "level": "intermediate",
        "language": "python",
        "anime_theme": {
            "palette": ["#14b8a6", "#06b6d4", "#0ea5e9"],
            "emblem": "📚",
            "rarity": "epic",
            "frame": "tower",
        },
        "concept": "mental_model",
        "prerequisites": ["concept:recursion:1"],
        "mental_model": {
            "type": "stack_frames",
            "caption": "Each recursive call pushes a frame.",
            "animation_steps": [
                {"label": "Push n=3", "action": "push", "params": {"n": 3}},
                {"label": "Push n=2", "action": "push", "params": {"n": 2}},
                {"label": "Push n=1", "action": "push", "params": {"n": 1}},
                {"label": "Pop n=1", "action": "pop", "return_value": 1},
                {"label": "Pop n=2", "action": "pop", "return_value": 2},
                {"label": "Pop n=3", "action": "pop", "return_value": 6},
            ],
        },
        "micro_task": {
            "instruction": "Watch the animation, then explain why factorial(3) returns 6.",
            "starter_code": {"python": "# Watch animation, then write explanation\n"},
            "solution": {"python": "# Each frame waits for the next; base case returns 1; then 2*1=2; then 3*2=6"},
            "verification": {"python": "True"},
            "explanation": "Stack frames build up and collapse in LIFO order.",
        },
        "misconception_tags": ["missing_base_case", "stack_overflow"],
        "pattern_tags": ["recursion", "visualization"],
        "srs": False,
        "estimated_minutes": 3,
    },
]

_SRS_CARDS: List[ConceptCard] = [
    {
        "id": "srs:two-pointer:pair:1",
        "order": 1,
        "title": "Two-pointer pair sum",
        "subtitle": "Retest: implement two-sum",
        "level": "intermediate",
        "language": "python",
        "anime_theme": {
            "palette": ["#f59e0b", "#f97316", "#ef4444"],
            "emblem": "👣",
            "rarity": "rare",
            "frame": "dual",
        },
        "concept": "srs",
        "prerequisites": ["pattern:two-pointer:1"],
        "mental_model": {"type": "spaced_repetition", "caption": "Recall the pattern, write the code."},
        "micro_task": {
            "instruction": "Given sorted array and target, return indices of two numbers that sum to target.",
            "starter_code": {"python": "def two_sum(nums, target):\n    # your code here\n    pass\n"},
            "solution": {"python": "def two_sum(nums, target):\n    i, j = 0, len(nums) - 1\n    while i < j:\n        s = nums[i] + nums[j]\n        if s == target:\n            return [i, j]\n        elif s < target:\n            i += 1\n        else:\n            j -= 1\n    return []\n"},
            "verification": {"python": "assert two_sum([1,2,3,4,5], 6) in [[0,3],[1,2]]"},
            "explanation": "Two pointers reduce nested loops.",
        },
        "misconception_tags": ["off_by_one", "infinite_loop"],
        "pattern_tags": ["two_pointers", "srs"],
        "srs": True,
        "estimated_minutes": 5,
    },
]


def get_concept_cards() -> List[ConceptCard]:
    return list(_CONCEPT_CARDS)


def get_debug_cards() -> List[ConceptCard]:
    return list(_DEBUG_CARDS)


def get_pattern_cards() -> List[ConceptCard]:
    return list(_PATTERN_CARDS)


def get_model_cards() -> List[ConceptCard]:
    return list(_MODEL_CARDS)


def get_srs_cards() -> List[ConceptCard]:
    return list(_SRS_CARDS)


def get_all_cards() -> List[ConceptCard]:
    return (
        get_concept_cards()
        + get_debug_cards()
        + get_pattern_cards()
        + get_model_cards()
        + get_srs_cards()
    )


def get_card_by_id(card_id: str) -> ConceptCard | None:
    for card in get_all_cards():
        if card["id"] == card_id:
            return card
    return None


def get_cards_by_concept(concept: str) -> List[ConceptCard]:
    return [c for c in get_all_cards() if c.get("concept") == concept]


def get_cards_by_level(level: str) -> List[ConceptCard]:
    return [c for c in get_all_cards() if c.get("level") == level]


def get_prerequisites(card_id: str) -> List[ConceptCard]:
    card = get_card_by_id(card_id)
    if not card:
        return []
    prereqs = []
    for pid in card.get("prerequisites", []):
        p = get_card_by_id(pid)
        if p:
            prereqs.append(p)
    return prereqs


def get_next_cards(completed_ids: List[str]) -> List[ConceptCard]:
    completed = set(completed_ids)
    next_cards = []
    for card in get_concept_cards():
        if card["id"] in completed:
            continue
        prereqs = set(card.get("prerequisites", []))
        if prereqs.issubset(completed):
            next_cards.append(card)
    return next_cards
