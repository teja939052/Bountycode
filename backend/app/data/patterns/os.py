"""Pattern Pack — Operating Systems."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "os",
    "name": "Operating Systems",
    "emoji": "⚙️",
    "round_id": "cs-core",
    "purpose": "Compare scheduling algorithms, identify synchronization issues, and reason about deadlock conditions and memory management.",
    "prerequisites": ["computer-basics", "algorithms", "dbms"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "FCFS is always bad",
            "description": "Ignores that FCFS is simple and starvation-free.",
        },
        {
            "id": "M2",
            "label": "Deadlock all four necessary",
            "description": "Thinks breaking any Coffman condition always avoids deadlock.",
        },
        {
            "id": "M3",
            "label": "Page size vs frames",
            "description": "Confuses page size with frame size.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Scheduling timeline",
            "captain_message": "See how algorithms reorder execution.",
            "render": {
                "kind": "gantt",
                "processes": [
                    {"name": "P1", "burst": 4},
                    {"name": "P2", "burst": 3},
                    {"name": "P3", "burst": 5},
                ],
                "algorithm": "fcfs",
                "show_waiting_time": True,
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Change the algorithm",
            "captain_message": "Switch from FCFS to SJF. See waiting time change.",
            "render": {
                "kind": "scheduler",
                "processes": [
                    {"name": "P1", "arrival": 0, "burst": 7},
                    {"name": "P2", "arrival": 2, "burst": 4},
                    {"name": "P3", "arrival": 4, "burst": 1},
                ],
                "algorithms": ["fcfs", "sjf", "rr"],
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict waiting time",
            "captain_message": "Choose the average waiting time.",
            "render": {
                "kind": "multiple_choice",
                "algorithm": "sjf",
                "processes": [
                    {"name": "P1", "arrival": 0, "burst": 5},
                    {"name": "P2", "arrival": 1, "burst": 3},
                ],
                "options": ["1", "2", "3", "4"],
                "answer_index": 1,
                "explanation": "SJF runs shortest next. Compute completion and waiting times.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the scheduler",
            "captain_message": "Write the ready-queue update rule.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Arrival check",
                        "placeholder": "add arrived processes to queue",
                        "answer": "add arrived processes to queue",
                    },
                    {
                        "label": "Pick next",
                        "placeholder": "shortest burst or FCFS",
                        "answer": "shortest burst or FCFS",
                    },
                    {
                        "label": "Update waiting",
                        "placeholder": "waiting += time - arrival",
                        "answer": "waiting += time - arrival",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break the deadlock",
            "captain_message": "All four Coffman conditions together allow deadlock.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Deadlock requires:",
                "options": [
                    "Mutual exclusion, hold and wait, no preemption, circular wait",
                    "Mutual exclusion, no hold and wait, preemption, no circular wait",
                    "Only circular wait",
                    "Only mutual exclusion",
                ],
                "answer_index": 0,
                "explanation": "All four Coffman conditions must hold simultaneously.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix memory fragmentation",
            "captain_message": "Use paging to eliminate external fragmentation.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Fragmentation type",
                        "placeholder": "external fragmentation",
                        "answer": "external fragmentation",
                    },
                    {
                        "label": "Solution",
                        "placeholder": "paging / compaction",
                        "answer": "paging / compaction",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to priority inversion",
            "captain_message": "Low-priority task blocks high-priority via shared resource.",
            "render": {
                "kind": "recall",
                "prompt": "Priority inversion solution?",
                "answer": "priority inheritance or ceiling protocol",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "For scheduling comparisons, focus on waiting time, throughput, and starvation.",
            "render": {
                "kind": "recall",
                "prompt": "SJF minimizes?",
                "answer": "average waiting time",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "Which is NOT a scheduling algorithm?",
                "options": ["FCFS", "SJF", "RR", "FTP"],
                "answer": "FTP",
                "explanation": "FTP is file transfer, not scheduling.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "Round Robin with time quantum 2. Processes P1(4), P2(3). Average waiting time?",
                "options": ["2.5", "3", "4", "1"],
                "answer": "2.5",
                "explanation": "Trace timeline and compute waiting time per process.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "Which condition is NOT required for deadlock?",
                "options": ["Mutual exclusion", "Hold and wait", "Preemption", "Circular wait"],
                "answer": "Preemption",
                "explanation": "No preemption is required; preemption actually prevents deadlock.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "Belady's anomaly occurs in?",
                "options": ["FIFO", "LRU", "Optimal", "LFU"],
                "answer": "FIFO",
                "explanation": "Belady's anomaly is specific to FIFO page replacement.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": " starvation is addressed by?",
            "options": ["Aging", "Priority", "Preemption", "Compaction"],
            "answer": "Aging",
            "explanation": "Aging gradually increases priority of waiting processes.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "Coffman conditions?",
            "answer": "mutual exclusion, hold and wait, no preemption, circular wait",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "SJF minimizes?",
            "answer": "average waiting time",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "Belady's anomaly is for?",
            "answer": "FIFO page replacement",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Scheduling, deadlock",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Memory, CPU scheduling",
        },
        {
            "company": "wipro",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Processes, threads",
        },
    ],
    "interview_transfer": {
        "prompt": "How does OS scheduling thinking apply to task prioritization in product management?",
        "model_answer": "Use weighted shortest job first for throughput, and add aging for fairness — exactly like OS scheduling.",
    },
}
