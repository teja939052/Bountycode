"""Pattern Pack — Averages."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "averages",
    "name": "Averages",
    "emoji": "📊",
    "round_id": "aptitude",
    "purpose": "Calculate arithmetic, weighted, and combined averages; handle corrections and missing observations.",
    "prerequisites": ["basic-multiplication", "fractions", "summation"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Mean vs median",
            "description": "Uses median when the question asks for the arithmetic average.",
        },
        {
            "id": "M2",
            "label": "Ignore weight",
            "description": "Averages weighted averages as if all groups had equal size.",
        },
        {
            "id": "M3",
            "label": "Double-count correction",
            "description": "Adds the correction amount instead of replacing the wrong value.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Center of a distribution",
            "captain_message": "An average is the balance point. Visualize before computing.",
            "render": {
                "kind": "bar",
                "values": [10, 20, 30, 40],
                "highlight_mean": True,
                "show_balance": True,
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Change a value",
            "captain_message": "Move one value. Watch the mean shift.",
            "render": {
                "kind": "slider",
                "dataset": [12, 15, 18, 20, 22],
                "target_index": 2,
                "min_val": 0,
                "max_val": 40,
                "default_val": 18,
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict the correction",
            "captain_message": "A value was recorded wrong. Choose the corrected average.",
            "render": {
                "kind": "multiple_choice",
                "original_avg": 45,
                "count": 10,
                "wrong_value": 50,
                "correct_value": 40,
                "options": [44.0, 45.0, 46.0, 44.5],
                "answer_index": 0,
                "explanation": "Correct sum = 450 - 50 + 40 = 440. New average = 440/10 = 44.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build weighted average",
            "captain_message": "Write the weighted sum formula. Not a number — the structure.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Weighted sum",
                        "placeholder": "Σ(value × weight)",
                        "answer": "Σ(value × weight)",
                    },
                    {
                        "label": "Total weight",
                        "placeholder": "Σ(weight)",
                        "answer": "Σ(weight)",
                    },
                    {
                        "label": "Weighted average",
                        "placeholder": "weighted_sum / total_weight",
                        "answer": "weighted_sum / total_weight",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break the equal-weight assumption",
            "captain_message": "Groups of different sizes. See why simple mean fails.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Group A (n=10, avg=20), Group B (n=20, avg=30). Combined average?",
                "options": [24.0, 25.0, 26.0, 26.67],
                "answer_index": 3,
                "explanation": "Combined average = (10×20 + 20×30)/(10+20) = 800/30 ≈ 26.67.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix a missing value from combined average",
            "captain_message": "You know two group averages and the total average. Find the missing group size.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Total sum equation",
                        "placeholder": "n1*avg1 + n2*avg2 = (n1+n2)*combined_avg",
                        "answer": "n1*avg1 + n2*avg2 = (n1+n2)*combined_avg",
                    },
                    {
                        "label": "Solve for missing n",
                        "placeholder": "n2 = (combined*n_total - n1*avg1) / avg2",
                        "answer": "n2 = (combined*n_total - n1*avg1) / avg2",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to exam scores",
            "captain_message": "Class average after a new student joins. Use combined average.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Class of 25 averages 78. A new student scoring 92 joins. New average?",
                "options": [78.0, 78.4, 78.56, 79.0],
                "answer_index": 2,
                "explanation": "New total = 25×78 + 92 = 1942. New avg = 1942/26 ≈ 74.69.",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "Deviation method: subtract assumed mean from all values, average deviations, add back.",
            "render": {
                "kind": "recall",
                "prompt": "In the deviation method, the final average equals?",
                "answer": "assumed_mean + average_of_deviations",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "Average of 5 numbers is 20. Sum of numbers?",
                "answer": "100",
                "explanation": "Sum = average × count = 20 × 5 = 100.",
            },
            {
                "id": "w2",
                "question": "Average of first 10 natural numbers?",
                "options": ["5.0", "5.5", "6.0", "6.5"],
                "answer": "5.5",
                "explanation": "Sum = 55, average = 55/10 = 5.5.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "Average of 7 numbers is 15. If one number 25 is replaced by 5, new average?",
                "answer": "~12.14",
                "explanation": "Sum changes by -20. New average = (105-20)/7 ≈ 12.14.",
            },
            {
                "id": "d2",
                "question": "A batsman averages 40 in 9 innings. How many runs in 10th to raise average to 42?",
                "answer": "60 runs",
                "explanation": "Total after 9 = 360. Required total = 420. 10th inning = 60.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "Average weight of 6 students is 52 kg. A new student joins and average becomes 53 kg. New student's weight?",
                "answer": "59 kg",
                "explanation": "Old total = 312. New total = 371. New student = 371 - 312 = 59.",
            },
            {
                "id": "s2",
                "question": "A grocer mixes 2 kg at ₹30/kg with 3 kg at ₹40/kg. Average cost per kg?",
                "answer": "₹36/kg",
                "explanation": "Weighted average = (2×30 + 3×40)/5 = 180/5 = 36.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "Average of 10 numbers is 23. If each number increases by 5, new average?",
                "answer": "28",
                "explanation": "Adding constant to each value increases mean by same constant: 23+5 = 28.",
            },
            {
                "id": "wr2",
                "question": "Average salary of 15 employees is ₹12,000. If manager's salary ₹30,000 included, average becomes ₹14,000. Manager's salary?",
                "answer": "₹44,000",
                "explanation": "Total with manager = 16×14,000 = 224,000. Total without = 15×12,000 = 180,000. Manager = 44,000.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "The average of 5 consecutive even numbers is 34. Find the largest number.",
            "options": ["32", "34", "36", "38"],
            "answer": "38",
            "explanation": "Numbers: 30, 32, 34, 36, 38. Average = 34. Largest = 38.",
        },
        {
            "id": "a2",
            "question": "A student's average marks in 7 subjects is 65. He got 72 in 8th. New average?",
            "answer": "~65.86",
            "explanation": "Old total = 455. New total = 527. New average = 527/8 ≈ 65.86.",
        },
        {
            "id": "a3",
            "question": "The average weight of A, B, C is 50 kg. If D joins and average becomes 48 kg, D's weight if A=45, B=55?",
            "answer": "40 kg",
            "explanation": "Total ABC = 150. Total ABCD = 192. D = 192 - 150 = 42 kg.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "Formula for average of n numbers?",
            "answer": "sum / n",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "If each number increases by k, the average?",
            "answer": "Increases by k",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "Weighted average formula?",
            "answer": "Σ(value × weight) / Σ(weight)",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Mean, weighted average, correction",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Fast arithmetic averages",
        },
        {
            "company": "wipro",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Average basics, TSD averages",
        },
    ],
    "interview_transfer": {
        "prompt": "You see DAU dropped 15% while new signups rose 10%. How do you report the net impact?",
        "model_answer": "Report cohort-level averages. A simple average of all users can hide the shift. Use weighted averages by user segment.",
    },
}
