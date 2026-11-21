"""Pattern Pack — Deadlock."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "deadlock",
    "name": "Deadlock",
    "emoji": "🚧",
    "round_id": "technical-interview",
    "purpose": "Identify Coffman conditions, apply prevention/avoidance/recovery strategies, and reason about deadlock in OS and distributed systems.",
    "prerequisites": ["os", "dbms"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Only mutual exclusion causes deadlock",
            "description": "Thinks removing mutual exclusion is sufficient.",
        },
        {
            "id": "M2",
            "label": "Preemption always safe",
            "description": "Assumes preemption never causes consistency issues.",
        },
        {
            "id": "M3",
            "label": "Banker accepts all",
            "description": "Believes Banker's algorithm allows all safe sequences.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Resource allocation graph",
            "captain_message": "See processes and resources as a graph.",
            "render": {
                "kind": "rag",
                "processes": ["P1", "P2"],
                "resources": ["R1", "R2"],
                "edges": [{"from": "P1", "to": "R1", "type": "request"}, {"from": "R1", "to": "P2", "type": "hold"}],
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Break a condition",
            "captain_message": "Remove hold and wait. See graph change.",
            "render": {
                "kind": "condition_toggle",
                "conditions": ["mutual_exclusion", "hold_wait", "no_preemption", "circular_wait"],
                "remove": "hold_wait",
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict deadlock",
            "captain_message": "Choose if deadlock is possible.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "P1 holds R1, requests R2. P2 holds R2, requests R1. Deadlock?",
                "options": ["Yes", "No", "Only if preemptive", "Only if non-preemptive"],
                "answer_index": 0,
                "explanation": "Circular wait exists. Deadlock possible.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build safe sequence",
            "captain_message": "Write order in which processes can finish.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Find process with need <= available",
                        "placeholder": "P?",
                        "answer": "P?",
                    },
                    {
                        "label": "Assume it finishes",
                        "placeholder": "add its allocation to available",
                        "answer": "add its allocation to available",
                    },
                    {
                        "label": "Repeat until all finish",
                        "placeholder": "safe sequence",
                        "answer": "safe sequence",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break circular wait",
            "captain_message": "Order resources. Request in order only.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Preventing circular wait by ordering resources is?",
                "options": ["Prevention", "Avoidance", "Recovery", "Ignorance"],
                "answer_index": 0,
                "explanation": "Ordering resources prevents circular wait, a prevention strategy.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix with Banker's",
            "captain_message": "Check safety before allocating.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Request check",
                        "placeholder": "request <= need and request <= available",
                        "answer": "request <= need and request <= available",
                    },
                    {
                        "label": "Safety check",
                        "placeholder": "find safe sequence",
                        "answer": "find safe sequence",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to distributed locks",
            "captain_message": "Same conditions apply to mutexes in microservices.",
            "render": {
                "kind": "recall",
                "prompt": "Distributed deadlock detection requires?",
                "answer": "wait-for graph across nodes",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "Four Coffman conditions: ME, hold-wait, no-preemption, circular-wait.",
            "render": {
                "kind": "recall",
                "prompt": "Which condition is easiest to break?",
                "answer": "circular wait (via ordering)",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "Which is NOT a Coffman condition?",
                "options": ["Mutual exclusion", "Hold and wait", "Preemption", "Circular wait"],
                "answer": "Preemption",
                "explanation": "No preemption is the condition, not preemption.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "Deadlock prevention strategy?",
                "options": ["Banker's", "Order resources", "Kill process", "Ignore"],
                "answer": "Order resources",
                "explanation": "Ordering resources prevents circular wait.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "Banker's algorithm is?",
                "options": ["Prevention", "Avoidance", "Recovery", "Detection"],
                "answer": "Avoidance",
                "explanation": "Banker's avoids deadlock by checking safety before allocation.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "Deadlock recovery by?",
                "options": ["Preemption", "Process termination", "Checkpointing", "Both A and B"],
                "answer": "Both A and B",
                "explanation": "Recovery can use preemption or process termination.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "Which condition is NOT necessary for deadlock?",
            "options": ["Mutual exclusion", "Hold and wait", "Preemption", "Circular wait"],
            "answer": "Preemption",
            "explanation": "No preemption is required; preemption prevents deadlock.",
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
            "prompt": "Banker's algorithm is?",
            "answer": "deadlock avoidance",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "Deadlock prevention strategy?",
            "answer": "break one Coffman condition",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Coffman conditions, prevention",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Banker's, RAG",
        },
    ],
    "interview_transfer": {
        "prompt": "How does deadlock thinking apply to microservice retries?",
        "model_answer": "It trains spotting circular waits in distributed locks and designing timeouts or ordering to break cycles.",
    },
}
