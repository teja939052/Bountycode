"""Seed script for PlacementPro scrims — generates 10 pre-built coding screencasts."""
import asyncio
from datetime import datetime, timezone
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from app.config import get_settings
from app.database import init_db, close_db, scrims_collection

settings = get_settings()


def make_snapshots(snap_list):
    return [{"timestamp_ms": ts, "code": c, "language": lang, "description": d, "line": ln}
            for ts, c, lang, d, ln in snap_list]


SCRIMS = [
    {
        "title": "Binary Search in a Sorted Array",
        "description": "Learn how to implement binary search — O(log n) search in a sorted array. We break down the classic algorithm step by step.",
        "topic": "binary-search",
        "difficulty": "beginner",
        "language": "python",
        "tags": ["binary-search", "arrays", "beginner", "divide-and-conquer"],
        "author_name": "Instructor Bot",
        "snapshots": [
            [0, "# Binary Search implementation\n# Goal: Find target in sorted array\n\narr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]\ntarget = 13\n\nprint(f\"Array: {arr}\")\nprint(f\"Target: {target}\")", "python", "Set up our sorted array and target. We'll search for 13.", 1],
            [15000, "# Binary Search in a Sorted Array\n\ndef binary_search(arr, target):\n    left = 0\n    right = len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1\n\narr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]\ntarget = 13\nresult = binary_search(arr, target)\nprint(f\"Found at index: {result}\")", "python", "Complete binary search with two-pointer approach. Halve search space each iteration.", 3],
            [30000, "# Binary Search in a Sorted Array\n\ndef binary_search(arr, target):\n    left = 0\n    right = len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1\n\narr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]\ntarget = 13\nresult = binary_search(arr, target)\nprint(f\"Found at index: {result}\")\n\n# Edge cases\nprint(binary_search(arr, 1))\nprint(binary_search(arr, 19))\nprint(binary_search(arr, 20))", "python", "Added edge case tests: first, last, and not-found cases.", 31],
            [45000, "# Binary Search in a Sorted Array\n\ndef binary_search(arr, target):\n    left = 0\n    right = len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1\n\ndef binary_search_recursive(arr, target, left, right):\n    if left > right:\n        return -1\n    mid = (left + right) // 2\n    if arr[mid] == target:\n        return mid\n    elif arr[mid] < target:\n        return binary_search_recursive(arr, target, mid + 1, right)\n    else:\n        return binary_search_recursive(arr, target, left, mid - 1)\n\narr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]\nprint(binary_search(arr, 13))\nprint(binary_search_recursive(arr, 13, 0, len(arr) - 1))", "python", "Added recursive version. Same algorithm, different expression.", 14],
            [60000, "# Binary Search in a Sorted Array\n\ndef binary_search(arr, target):\n    left = 0\n    right = len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1\n\ndef binary_search_recursive(arr, target, left, right):\n    if left > right:\n        return -1\n    mid = (left + right) // 2\n    if arr[mid] == target:\n        return mid\n    elif arr[mid] < target:\n        return binary_search_recursive(arr, target, mid + 1, right)\n    else:\n        return binary_search_recursive(arr, target, left, mid - 1)\n\ndef binary_search_first(arr, target):\n    left, right = 0, len(arr) - 1\n    result = -1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            result = mid\n            right = mid - 1\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return result\n\narr = [1, 3, 5, 7, 9, 11, 13, 13, 13, 15, 17, 19]\nprint(f\"First 13 at: {binary_search_first(arr, 13)}\")", "python", "Find first occurrence in array with duplicates.", 28],
            [75000, "# Binary Search in a Sorted Array\n\ndef binary_search(arr, target):\n    left = 0\n    right = len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1\n\ndef binary_search_recursive(arr, target, left, right):\n    if left > right:\n        return -1\n    mid = (left + right) // 2\n    if arr[mid] == target:\n        return mid\n    elif arr[mid] < target:\n        return binary_search_recursive(arr, target, mid + 1, right)\n    else:\n        return binary_search_recursive(arr, target, left, mid - 1)\n\ndef binary_search_first(arr, target):\n    left, right = 0, len(arr) - 1\n    result = -1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            result = mid\n            right = mid - 1\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return result\n\nimport time\narr = list(range(1, 100001))\nstart = time.time()\nprint(binary_search(arr, 99999))\nprint(f\"Binary: {(time.time()-start)*1000:.2f}ms\")\nstart = time.time()\nfor i, v in enumerate(arr):\n    if v == 99999:\n        print(i)\n        break\nprint(f\"Linear: {(time.time()-start)*1000:.2f}ms\")", "python", "Performance: binary vs linear search on 100K elements.", 37],
        ]
    },
    {
        "title": "Reverse a Linked List",
        "description": "Walk through reversing a singly linked list in-place using iterative and recursive approaches.",
        "topic": "linked-lists",
        "difficulty": "medium",
        "language": "python",
        "tags": ["linked-lists", "medium", "pointers", "in-place"],
        "author_name": "Instructor Bot",
        "snapshots": [
            [0, "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef print_list(head):\n    vals = []\n    while head:\n        vals.append(str(head.val))\n        head = head.next\n    print(\" -> \".join(vals))\n\nhead = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))\nprint(\"Original:\")\nprint_list(head)", "python", "Setting up ListNode class and sample list 1->2->3->4->5.", 1],
            [15000, "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef print_list(head):\n    vals = []\n    while head:\n        vals.append(str(head.val))\n        head = head.next\n    print(\" -> \".join(vals))\n\ndef reverse_list(head):\n    prev = None\n    current = head\n    while current:\n        next_temp = current.next\n        current.next = prev\n        prev = current\n        current = next_temp\n    return prev\n\nhead = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))\nprint(\"Original:\")\nprint_list(head)\nreversed_head = reverse_list(head)\nprint(\"Reversed:\")\nprint_list(reversed_head)", "python", "Iterative reverse with three pointers: prev, current, next_temp.", 14],
            [30000, "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef print_list(head):\n    vals = []\n    while head:\n        vals.append(str(head.val))\n        head = head.next\n    print(\" -> \".join(vals))\n\ndef reverse_list(head):\n    prev = None\n    current = head\n    while current:\n        next_temp = current.next\n        current.next = prev\n        prev = current\n        current = next_temp\n    return prev\n\ndef reverse_list_recursive(head):\n    if not head or not head.next:\n        return head\n    new_head = reverse_list_recursive(head.next)\n    head.next.next = head\n    head.next = None\n    return new_head\n\nhead = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))\nprint_list(reverse_list_recursive(head))", "python", "Recursive version uses call stack to reverse.", 24],
            [45000, "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef print_list(head):\n    vals = []\n    while head:\n        vals.append(str(head.val))\n        head = head.next\n    print(\" -> \".join(vals))\n\ndef reverse_list(head):\n    prev = None\n    current = head\n    while current:\n        next_temp = current.next\n        current.next = prev\n        prev = current\n        current = next_temp\n    return prev\n\ndef reverse_list_recursive(head):\n    if not head or not head.next:\n        return head\n    new_head = reverse_list_recursive(head.next)\n    head.next.next = head\n    head.next = None\n    return new_head\n\ndef reverse_between(head, left, right):\n    dummy = ListNode(0, head)\n    prev = dummy\n    for _ in range(left - 1):\n        prev = prev.next\n    curr = prev.next\n    for _ in range(right - left):\n        next_temp = curr.next\n        curr.next = next_temp.next\n        next_temp.next = prev.next\n        prev.next = next_temp\n    return dummy.next\n\nhead = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))\nresult = reverse_between(head, 2, 4)\nprint_list(result)", "python", "LeetCode 92: reverse portion between positions 2 and 4.", 31],
            [60000, "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef print_list(head):\n    vals = []\n    while head:\n        vals.append(str(head.val))\n        head = head.next\n    print(\" -> \".join(vals))\n\ndef reverse_list(head):\n    prev = None\n    current = head\n    while current:\n        next_temp = current.next\n        current.next = prev\n        prev = current\n        current = next_temp\n    return prev\n\ndef reverse_list_recursive(head):\n    if not head or not head.next:\n        return head\n    new_head = reverse_list_recursive(head.next)\n    head.next.next = head\n    head.next = None\n    return new_head\n\ndef reverse_between(head, left, right):\n    dummy = ListNode(0, head)\n    prev = dummy\n    for _ in range(left - 1):\n        prev = prev.next\n    curr = prev.next\n    for _ in range(right - left):\n        next_temp = curr.next\n        curr.next = next_temp.next\n        next_temp.next = prev.next\n        prev.next = next_temp\n    return dummy.next\n\ndef is_palindrome(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n    second_half = reverse_list(slow)\n    first_half = head\n    while second_half:\n        if first_half.val != second_half.val:\n            return False\n        first_half = first_half.next\n        second_half = second_half.next\n    return True\n\npal = ListNode(1, ListNode(2, ListNode(3, ListNode(2, ListNode(1)))))\nprint(f\"Is palindrome: {is_palindrome(pal)}\")", "python", "Palindrome Linked List using reverse + slow/fast pointers.", 42],
            [75000, "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef print_list(head):\n    vals = []\n    while head:\n        vals.append(str(head.val))\n        head = head.next\n    print(\" -> \".join(vals))\n\ndef reverse_list(head):\n    prev = None\n    current = head\n    while current:\n        next_temp = current.next\n        current.next = prev\n        prev = current\n        current = next_temp\n    return prev\n\ndef reverse_list_recursive(head):\n    if not head or not head.next:\n        return head\n    new_head = reverse_list_recursive(head.next)\n    head.next.next = head\n    head.next = None\n    return new_head\n\ndef reverse_between(head, left, right):\n    dummy = ListNode(0, head)\n    prev = dummy\n    for _ in range(left - 1):\n        prev = prev.next\n    curr = prev.next\n    for _ in range(right - left):\n        next_temp = curr.next\n        curr.next = next_temp.next\n        next_temp.next = prev.next\n        prev.next = next_temp\n    return dummy.next\n\ndef is_palindrome(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n    second_half = reverse_list(slow)\n    while second_half:\n        if head.val != second_half.val:\n            return False\n        head = head.next\n        second_half = second_half.next\n    return True\n\ndef add_two_numbers(l1, l2):\n    dummy = ListNode()\n    curr = dummy\n    carry = 0\n    while l1 or l2 or carry:\n        v1 = l1.val if l1 else 0\n        v2 = l2.val if l2 else 0\n        total = v1 + v2 + carry\n        carry = total // 10\n        curr.next = ListNode(total % 10)\n        curr = curr.next\n        if l1: l1 = l1.next\n        if l2: l2 = l2.next\n    return dummy.next\n\nl1 = ListNode(2, ListNode(4, ListNode(3)))\nl2 = ListNode(5, ListNode(6, ListNode(4)))\nprint_list(add_two_numbers(l1, l2))", "python", "Add Two Numbers: 342 + 465 = 807.", 55],
        ]
    },
    {
        "title": "Two Sum — Brute Force to Optimal",
        "description": "Solve Two Sum starting from brute force and optimizing to O(n) with a hash map.",
        "topic": "arrays",
        "difficulty": "easy",
        "language": "javascript",
        "tags": ["arrays", "hash-map", "easy", "two-pointers"],
        "author_name": "Instructor Bot",
        "snapshots": [
            [0, "const nums = [2, 7, 11, 15];\nconst target = 9;\n\nconsole.log(`nums: [${nums}], target: ${target}`);", "javascript", "Setting up sample input.", 1],
            [12000, "function twoSumBruteForce(nums, target) {\n    for (let i = 0; i < nums.length; i++) {\n        for (let j = i + 1; j < nums.length; j++) {\n            if (nums[i] + nums[j] === target) {\n                return [i, j];\n            }\n        }\n    }\n    return [];\n}\n\nconst nums = [2, 7, 11, 15];\nconst target = 9;\nconsole.log(twoSumBruteForce(nums, target));", "javascript", "Brute force O(n^2): check every pair.", 1],
            [25000, "function twoSumHash(nums, target) {\n    const map = new Map();\n    for (let i = 0; i < nums.length; i++) {\n        const complement = target - nums[i];\n        if (map.has(complement)) {\n            return [map.get(complement), i];\n        }\n        map.set(nums[i], i);\n    }\n    return [];\n}\n\nconsole.log(twoSumHash([2, 7, 11, 15], 9));", "javascript", "Optimized O(n) using hash map: store seen values, check complement.", 1],
            [38000, "function twoSumHash(nums, target) {\n    const map = new Map();\n    for (let i = 0; i < nums.length; i++) {\n        const complement = target - nums[i];\n        if (map.has(complement)) {\n            return [map.get(complement), i];\n        }\n        map.set(nums[i], i);\n    }\n    return [];\n}\n\nfunction twoSumSorted(arr, target) {\n    const nums = arr.map((v, i) => [v, i]).sort((a, b) => a[0] - b[0]);\n    let left = 0, right = nums.length - 1;\n    while (left < right) {\n        const sum = nums[left][0] + nums[right][0];\n        if (sum === target) return [nums[left][1], nums[right][1]];\n        if (sum < target) left++;\n        else right--;\n    }\n    return [];\n}\n\nconsole.log(twoSumHash([3, 2, 4], 6));\nconsole.log(twoSumSorted([3, 2, 4], 6));", "javascript", "Two-pointer approach on sorted array with index preservation.", 18],
            [50000, "function threeSum(nums) {\n    const result = [];\n    nums.sort((a, b) => a - b);\n    for (let i = 0; i < nums.length - 2; i++) {\n        if (i > 0 && nums[i] === nums[i - 1]) continue;\n        let left = i + 1, right = nums.length - 1;\n        while (left < right) {\n            const sum = nums[i] + nums[left] + nums[right];\n            if (sum === 0) {\n                result.push([nums[i], nums[left], nums[right]]);\n                while (left < right && nums[left] === nums[left + 1]) left++;\n                while (left < right && nums[right] === nums[right - 1]) right--;\n                left++; right--;\n            } else if (sum < 0) left++;\n            else right--;\n        }\n    }\n    return result;\n}\n\nconsole.log(\"Three sum:\", threeSum([-1, 0, 1, 2, -1, -4]));", "javascript", "Extension: Three Sum using sorting + two-pointer to find triplets summing to zero.", 27]
        ]
    },
]


async def seed():
    await init_db()
    col = scrims_collection()
    await col.delete_many({})

    count = 0
    for scrim in SCRIMS:
        snap_list = scrim.pop("snapshots")
        doc = {
            **scrim,
            "author_id": None,
            "snapshots": [{
                "timestamp_ms": s[0],
                "code": s[1],
                "language": s[2],
                "description": s[3],
                "line": s[4]
            } for s in snap_list],
            "final_code": snap_list[-1][1],
            "duration_seconds": snap_list[-1][0] // 1000,
            "views": 0,
            "likes": 0,
            "created_at": datetime.now(timezone.utc),
        }
        await col.insert_one(doc)
        count += 1
        print(f"  ✓ {doc['title']} ({len(doc['snapshots'])} snapshots, {doc['duration_seconds']}s)")

    print(f"\nSeeded {count} scrims successfully!")


if __name__ == "__main__":
    asyncio.run(seed())
