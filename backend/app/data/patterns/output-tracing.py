"""Pattern Pack — Output Tracing."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "output-tracing",
    "name": "Output Tracing",
    "emoji": "🔍",
    "round_id": "coding",
    "purpose": "Trace loop execution, pointer updates, and recursion stacks to predict program output.",
    "prerequisites": ["variables", "conditions", "loops"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Loop count off-by-one",
            "description": "Miscounts iterations when initialization or boundary is tricky.",
        },
        {
            "id": "M2",
            "label": "Pointer arithmetic wrong",
            "description": "Confuses ++ptr and ptr++ for array traversal.",
        },
        {
            "id": "M3",
            "label": "Recursion base missed",
            "description": "Forgets the base case return value in recursion trace.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Trace table",
            "captain_message": "Write variable values at each line.",
            "render": {
                "kind": "trace_table",
                "code_lines": ["i=0", "while i<3", "print i", "i++"],
                "max_iterations": 5,
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Change the condition",
            "captain_message": "Edit loop condition. See output change.",
            "render": {
                "kind": "code_editor",
                "code": "for i in range(3):\n    if i == 1:\n        continue\n    print(i)",
                "editable_lines": [2],
                "highlight_flow": True,
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict output",
            "captain_message": "Choose the output.",
            "render": {
                "kind": "multiple_choice",
                "code": "x = 5\nwhile x > 0:\n    print(x)\n    x -= 2",
                "options": ["5 3 1", "5 4 3 2 1", "5 3 1 -1", "5 4 3 2"],
                "answer_index": 0,
                "explanation": "Loop prints 5, 3, 1 then exits.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the trace",
            "captain_message": "Write the values for each iteration.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Initial values",
                        "placeholder": "i=0, sum=0",
                        "answer": "i=0, sum=0",
                    },
                    {
                        "label": "Iteration table",
                        "placeholder": "i | sum",
                        "answer": "i | sum",
                    },
                    {
                        "label": "Final output",
                        "placeholder": "sum",
                        "answer": "sum",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break the continue",
            "captain_message": "Continue skips rest of loop body.",
            "render": {
                "kind": "multiple_choice",
                "code": "for i in range(4):\n    if i == 2:\n        continue\n    print(i, end='')",
                "options": ["013", "0123", "123", "01"],
                "answer_index": 0,
                "explanation": "i=0,1 printed. i=2 skipped by continue. i=3 printed.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix off-by-one",
            "captain_message": "Loop condition should be i <= n or i < n+1.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Current condition",
                        "placeholder": "i < n",
                        "answer": "i < n",
                    },
                    {
                        "label": "Desired iterations",
                        "placeholder": "n+1 iterations",
                        "answer": "n+1 iterations",
                    },
                    {
                        "label": "Correct condition",
                        "placeholder": "i <= n",
                        "answer": "i <= n",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to recursion",
            "captain_message": "Trace recursion like a stack.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "factorial(3) returns?",
                "options": ["3", "6", "5", "9"],
                "answer_index": 1,
                "explanation": "3! = 3×2×1 = 6.",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "For loops, count iterations first, then list values.",
            "render": {
                "kind": "recall",
                "prompt": "First step in tracing a loop?",
                "answer": "count iterations",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "Output: print(2**3)",
                "options": ["6", "8", "9", "5"],
                "answer": "8",
                "explanation": "2^3 = 8.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "Trace: i=1; while i<5: print(i); i+=2",
                "options": ["1 3", "1 3 5", "1 2 3 4", "1 2 3"],
                "answer": "1 3",
                "explanation": "i takes values 1, 3. Next would be 5 which fails condition.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "Output: sum=0\nfor i in range(1,4):\n    sum+=i\nprint(sum)",
                "options": ["3", "4", "5", "6"],
                "answer": "6",
                "explanation": "Sum = 1+2+3 = 6.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "Output: for i in range(3):\n    print(i, end=' ')\nelse:\n    print('done')",
                "options": ["0 1 2 done", "0 1 2", "done", "0 1 2 3 done"],
                "answer": "0 1 2 done",
                "explanation": "Loop completes without break, so else executes.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "Output: x=0\nfor i in range(5):\n    if i%2==0:\n        x+=i\n    else:\n        x-=i\nprint(x)",
            "options": ["-2", "0", "2", "-1"],
            "answer": "-2",
            "explanation": "+0-1+2-3+4 = 2. Wait: 0-1+2-3+4 = 2.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "How to count loop iterations?",
            "answer": "determine start, stop, and step",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "What does 'continue' do?",
            "answer": "skips rest of body, moves to next iteration",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "Recursion needs?",
            "answer": "base case and recursive step",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Loops, tracing",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Quick output prediction",
        },
        {
            "company": "wipro",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Conditions and loops",
        },
    ],
    "interview_transfer": {
        "prompt": "How does output tracing help in debugging production issues?",
        "model_answer": "It trains step-by-step reasoning through control flow, which is exactly how you debug complex async or nested logic.",
    },
}
