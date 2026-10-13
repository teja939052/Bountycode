"""Pattern Pack — Loops.

Teaches for/while loop execution tracing, off-by-one errors, and
nested-loop output prediction.
"""
from __future__ import annotations

from typing import Any, Dict

pack: Dict[str, Any] = {
    "pattern_id": "loops",
    "name": "Loops",
    "emoji": "🔄",
    "round_id": "coding",
    "purpose": "Predict loop output, recognize off-by-one errors, and trace nested-loop execution.",
    "prerequisites": ["variables", "conditions", "operators"],
    "misconceptions": [
        {
            "id": "L1",
            "label": "Off-by-one",
            "description": "Uses <= instead of <, or vice versa, causing one extra or missing iteration.",
        },
        {
            "id": "L2",
            "label": "Update-order error",
            "description": "Reads the updated value in the same iteration when order matters.",
        },
        {
            "id": "L3",
            "label": "Nested-loop flattening",
            "description": "Confuses inner and outer loop indices.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Watch the program think",
            "captain_message": "Loops aren't magic. They are just repetition with a moving state.",
            "render": {
                "kind": "execution_trace",
                "code": "for i in range(3):\n    print(i)",
                "language": "python",
                "highlights": ["i", "print"],
                "speed_ms": 800,
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Change the bound",
            "captain_message": "Move the upper bound. Watch how many times it prints.",
            "render": {
                "kind": "range_slider",
                "code_template": "for i in range({bound}):\n    print(i)",
                "min": 1,
                "max": 6,
                "default": 3,
                "show_output": True,
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict before running",
            "captain_message": "Don't run it. Tell me the output.",
            "render": {
                "kind": "predict_output",
                "code": "for i in range(1, 4):\n    print(i*2)",
                "options": ["0 2 4", "2 4 6", "1 2 3", "2 4 6 8"],
                "answer_index": 1,
                "explanation": "i takes 1, 2, 3. Multiply by 2: 2, 4, 6.",
            },
        },
        {
            "id": "change",
            "type": "change",
            "title": "Change one thing",
            "captain_message": "Change range(1,4) to range(1,5). What changes?",
            "render": {
                "kind": "compare_outputs",
                "original": "for i in range(1,4):\n    print(i)",
                "modified": "for i in range(1,5):\n    print(i)",
                "highlight_diff": True,
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the loop",
            "captain_message": "Write a loop that prints the first 5 even numbers.",
            "render": {
                "kind": "fill_code",
                "language": "python",
                "starter": "for i in range(___):\n    print(i*2)",
                "answer": "5",
                "placeholders": ["5"],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break it",
            "captain_message": "This answer looks reasonable. That's why it's dangerous.",
            "render": {
                "kind": "debug_solution",
                "buggy_code": "for i in range(0, 5):\n    if i == 3:\n        break\n    print(i)",
                "question": "How many numbers are printed? Student says 4.",
                "expected_failure": "break stops the loop before printing 3, so only 0, 1, 2 are printed.",
                "diagnosis_code": "off_by_one",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix the mistake",
            "captain_message": "Find the misconception and repair it.",
            "render": {
                "kind": "fix_expression",
                "broken": "for i in range(0, 5):\n    print(i)  # student expects 1..5",
                "fix_hint": "range is inclusive start, exclusive end.",
                "answer": "for i in range(1, 6):\n    print(i)",
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer: nested loops",
            "captain_message": "Same idea. Two levels deep.",
            "render": {
                "kind": "nested_trace",
                "code": "for i in range(2):\n    for j in range(3):\n        print(i, j)",
                "answer": "0 0\n0 1\n0 2\n1 0\n1 1\n1 2",
                "explanation": "Outer i stays fixed while j runs fully.",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "TCS-style proof",
            "captain_message": "No trace. No hints. 60 seconds.",
            "render": {
                "kind": "timed_question",
                "seconds": 60,
                "question": "What is the output?\n\nfor i in range(1, 10, 2):\n    print(i, end=' ')",
                "options": ["1 3 5 7 9", "1 3 5 7 9 11", "1 2 3 4 5 6 7 8 9", "1 3 5 7"],
                "answer_index": 0,
                "explanation": "start=1, stop=10 (exclusive), step=2 → 1,3,5,7,9.",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "loop-w1",
                "topic": "loops",
                "difficulty": "easy",
                "question": "How many times does this loop run?\nfor i in range(5): print(i)",
                "options": ["4", "5", "6", "0"],
                "answer": "5",
                "explanation": "range(5) → 0,1,2,3,4. Five iterations.",
            },
        ],
        "drill": [
            {
                "id": "loop-d1",
                "topic": "loops",
                "difficulty": "medium",
                "question": "Output of:\nfor i in range(2):\n  for j in range(3):\n    print(i+j, end=' ')",
                "options": ["0 1 2 1 2 3", "0 1 2 0 1 2", "0 1 2 3 4 5", "1 2 3 1 2 3"],
                "answer": "0 1 2 1 2 3",
                "explanation": "(0+0)(0+1)(0+2) then (1+0)(1+1)(1+2).",
            },
        ],
        "speed_run": [
            {
                "id": "loop-s1",
                "topic": "loops",
                "difficulty": "medium",
                "question": "Output?\nfor i in range(1, 6):\n    if i % 2 == 0:\n        print(i)",
                "options": ["1 3 5", "2 4", "2 4 6", "0 2 4"],
                "answer": "2 4",
                "explanation": "Only even numbers between 1 and 5.",
            },
        ],
        "weakness_repair": [
            {
                "id": "loop-r1",
                "topic": "loops",
                "difficulty": "medium",
                "question": "A student expects this to print 1..10:\nfor i in range(10):\n    print(i+1)\nThey get 1..10. Why did +1 fix it?",
                "options": ["It shifts start to 1", "It shifts end to 11", "Both", "Neither"],
                "answer": "Both",
                "explanation": "range(10) is 0..9. Adding 1 shifts both start and end by 1.",
                "diagnosis_code": "off_by_one",
            },
        ],
    },
    "assessment": [
        {
            "id": "loop-a1",
            "topic": "loops",
            "difficulty": "medium",
            "question": "How many times is 'x' printed?\nfor i in range(3):\n  for j in range(i):\n    print('x', end='')",
            "options": ["3", "4", "5", "6"],
            "answer": "3",
            "explanation": "i=0 → 0 times; i=1 → 1 time; i=2 → 2 times. Total = 3.",
        },
    ],
    "retention": [
        {
            "id": "loop-ret-1d",
            "due_days": 1,
            "prompt": "range(1, 5) produces which values?",
            "answer": "1, 2, 3, 4",
            "diagnosis_code": "off_by_one",
        },
        {
            "id": "loop-ret-3d",
            "due_days": 3,
            "prompt": "A loop runs n-1 times. If n=5, how many iterations?",
            "answer": "4",
            "diagnosis_code": "off_by_one",
        },
        {
            "id": "loop-ret-7d",
            "due_days": 7,
            "prompt": "In nested loops, when does the inner loop reset?",
            "answer": "On every outer-loop iteration",
            "diagnosis_code": "nested-loop-flattening",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "difficulty": "easy",
            "timing_seconds": 60,
            "context": "TCS NQT coding output questions",
            "question_count": 3,
        },
        {
            "company": "infosys",
            "difficulty": "medium",
            "timing_seconds": 45,
            "context": "InfyTQ pseudo-code",
            "question_count": 2,
        },
        {
            "company": "wipro",
            "difficulty": "easy",
            "timing_seconds": 60,
            "context": "Wipro NLTH coding",
            "question_count": 3,
        },
    ],
    "interview_transfer": {
        "prompt": "Explain the difference between a for-loop and a while-loop to an interviewer in 30 seconds.",
        "model_answer": "A for-loop is best when the iteration count is known upfront — it bundles initialization, condition, and update in one line. A while-loop is better when the exit condition depends on something other than a simple counter, like reading until EOF.",
        "success_criteria": ["mentions count-known vs condition-known", "gives use-case for each", "mentions readability"],
    },
}
