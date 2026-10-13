"""Pattern Pack — Arrays.

Covers array traversal, index errors, and basic searching.
"""
from __future__ import annotations

from typing import Any, Dict

pack: Dict[str, Any] = {
    "pattern_id": "arrays",
    "name": "Arrays",
    "emoji": "📋",
    "round_id": "coding",
    "purpose": "Traverse arrays safely, avoid index-out-of-bounds, and recognize O(n) search patterns.",
    "prerequisites": ["variables", "loops", "conditions"],
    "misconceptions": [
        {
            "id": "A1",
            "label": "Off-by-one index",
            "description": "Uses <= len instead of < len, causing an extra iteration or IndexError.",
        },
        {
            "id": "A2",
            "label": "Confuses value with index",
            "description": "Treats arr[i] as the index rather than the value at position i.",
        },
        {
            "id": "A3",
            "label": "Modifies while iterating",
            "description": "Inserts/deletes during forward traversal and skips elements.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Memory cells",
            "captain_message": "An array is a row of labeled boxes. Each box holds one value.",
            "render": {
                "kind": "array_visual",
                "values": [10, 20, 30, 40, 50],
                "highlight_indices": [0, 2, 4],
                "show_indices": True,
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Walk the array",
            "captain_message": "Change the index and see which box is accessed.",
            "render": {
                "kind": "index_slider",
                "values": [10, 20, 30, 40, 50],
                "min": 0,
                "max": 4,
                "default": 0,
                "show_warning": True,
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict the sum",
            "captain_message": "Before running, what does this print?",
            "render": {
                "kind": "predict_output",
                "code": "arr = [5, 10, 15]\n total = 0\n for x in arr:\n     total += x\n print(total)",
                "options": ["15", "30", "25", "20"],
                "answer_index": 1,
                "explanation": "5+10+15 = 30.",
            },
        },
        {
            "id": "change",
            "type": "change",
            "title": "Change the bound",
            "captain_message": "Change range(len(arr)) to range(1, len(arr)). What disappears?",
            "render": {
                "kind": "compare_outputs",
                "original": "arr = [2,4,6,8]\nfor i in range(len(arr)):\n    print(arr[i])",
                "modified": "arr = [2,4,6,8]\nfor i in range(1, len(arr)):\n    print(arr[i])",
                "highlight_diff": True,
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the search",
            "captain_message": "Write a loop that finds the index of the first even number.",
            "render": {
                "kind": "fill_code",
                "language": "python",
                "starter": "arr = [1,3,4,5,6]\nfor i in range(len(arr)):\n    if ___:\n        print(i)\n        break",
                "answer": "arr[i] % 2 == 0",
                "placeholders": ["arr[i] % 2 == 0"],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break it",
            "captain_message": "This answer looks reasonable. That's why it's dangerous.",
            "render": {
                "kind": "debug_solution",
                "buggy_code": "arr = [1,2,3]\nfor i in range(len(arr)+1):\n    print(arr[i])",
                "question": "Student says this prints 1 2 3. What actually happens?",
                "expected_failure": "IndexError on the fourth iteration because valid indices are 0..2.",
                "diagnosis_code": "off_by_one",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix the mistake",
            "captain_message": "Repair the bound.",
            "render": {
                "kind": "fix_expression",
                "broken": "for i in range(len(arr)+1):",
                "fix_hint": "Use len(arr), not len(arr)+1.",
                "answer": "for i in range(len(arr)):",
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer: max in array",
            "captain_message": "Same traversal idea. Different goal.",
            "render": {
                "kind": "fill_code",
                "language": "python",
                "starter": "arr = [7,2,9,4]\nmax_val = arr[0]\nfor i in range(1, len(arr)):\n    if ___:\n        max_val = arr[i]\nprint(max_val)",
                "answer": "arr[i] > max_val",
                "placeholders": ["arr[i] > max_val"],
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "TCS-style proof",
            "captain_message": "No array visual. No hints. 60 seconds.",
            "render": {
                "kind": "timed_question",
                "seconds": 60,
                "question": "int[] a = {2, 4, 6, 8};\nSystem.out.println(a[a.length - 2]);",
                "options": ["4", "6", "8", "Error"],
                "answer_index": 1,
                "explanation": "length=4, length-2=2, a[2]=6.",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "arr-w1",
                "topic": "arrays",
                "difficulty": "easy",
                "question": "arr = [1,2,3]. What is arr[1]?",
                "options": ["1", "2", "3", "Error"],
                "answer": "2",
                "explanation": "0-based indexing: index 1 is the second element.",
            },
        ],
        "drill": [
            {
                "id": "arr-d1",
                "topic": "arrays",
                "difficulty": "medium",
                "question": "Sum of arr = [4,7,9] is:",
                "options": ["18", "20", "21", "24"],
                "answer": "20",
                "explanation": "4+7+9 = 20.",
            },
        ],
        "speed_run": [
            {
                "id": "arr-s1",
                "topic": "arrays",
                "difficulty": "medium",
                "question": "Last index of arr with length 5:",
                "options": ["4", "5", "3", "Error"],
                "answer": "4",
                "explanation": "Indices run 0..length-1.",
            },
        ],
        "weakness_repair": [
            {
                "id": "arr-r1",
                "topic": "arrays",
                "difficulty": "medium",
                "question": "A student loops range(len(arr)+1) and gets an error. Fix the bound.",
                "options": ["range(len(arr))", "range(1,len(arr))", "range(len(arr)-1)", "range(0,len(arr))"],
                "answer": "range(len(arr))",
                "explanation": "Valid indices are 0 to len-1 inclusive.",
                "diagnosis_code": "off_by-one",
            },
        ],
    },
    "assessment": [
        {
            "id": "arr-a1",
            "topic": "arrays",
            "difficulty": "medium",
            "question": "Given arr = {1,3,5,7}, what is arr[arr[2]]?",
            "options": ["3", "5", "7", "Error"],
            "answer": "7",
            "explanation": "arr[2]=5, arr[5] is out of bounds → Error.",
        },
    ],
    "retention": [
        {
            "id": "arr-ret-1d",
            "due_days": 1,
            "prompt": "In a 5-element array, what is the last valid index?",
            "answer": "4",
            "diagnosis_code": "off_by-one",
        },
        {
            "id": "arr-ret-3d",
            "due_days": 3,
            "prompt": "Does range(len(arr)) include the last element?",
            "answer": "Yes, because the stop is exclusive.",
            "diagnosis_code": "off_by-one",
        },
        {
            "id": "arr-ret-7d",
            "due_days": 7,
            "prompt": "When scanning an array for max, what is the correct initialization?",
            "answer": "max_val = arr[0]",
            "diagnosis_code": "wrong_base",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "difficulty": "easy",
            "timing_seconds": 60,
            "context": "TCS NQT coding output",
            "question_count": 3,
        },
        {
            "company": "wipro",
            "difficulty": "easy",
            "timing_seconds": 60,
            "context": "Wipro NLTH arrays",
            "question_count": 3,
        },
    ],
    "interview_transfer": {
        "prompt": "Explain array indexing and a common off-by-one bug to an interviewer.",
        "model_answer": "Arrays are 0-indexed: the first element is at index 0, so the last is at length-1. The most common bug is using <= instead of < in loops, which causes an off-by-one or IndexError.",
        "success_criteria": ["0-based indexing", "last index = length-1", "example of off-by-one"],
    },
}
