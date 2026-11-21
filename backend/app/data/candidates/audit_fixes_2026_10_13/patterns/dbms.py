"""Pattern Pack — DBMS."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "dbms",
    "name": "DBMS",
    "emoji": "🛢️",
    "round_id": "cs-core",
    "purpose": "Identify keys, normalization forms, ACID properties, and transaction isolation levels.",
    "prerequisites": ["sql-basics", "file-systems"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Superkey vs candidate key",
            "description": "Treats any superkey as a candidate key without minimality.",
        },
        {
            "id": "M2",
            "label": "Normalization direction",
            "description": "Believes higher normal form is always better regardless of query patterns.",
        },
        {
            "id": "M3",
            "label": "ACID ordering",
            "description": "Confuses isolation level with durability property.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Keys in a table",
            "captain_message": "See how keys constrain rows.",
            "render": {
                "kind": "table_highlight",
                "table": "Students(id, name, email, course)",
                "highlight_key": True,
                "key_column": "id",
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Decompose a table",
            "captain_message": "Split a wide table to remove redundancy.",
            "render": {
                "kind": "decompose",
                "original": "Orders(order_id, customer_name, product, price, address)",
                "target_normal_form": "2NF",
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict the key",
            "captain_message": "Choose the minimal unique identifier.",
            "render": {
                "kind": "multiple_choice",
                "table": "Enrollments(student_id, course_id, semester)",
                "options": ["student_id", "course_id", "(student_id, course_id)", "semester"],
                "answer_index": 2,
                "explanation": "Composite key (student_id, course_id) uniquely identifies each row.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the normalization steps",
            "captain_message": "Write the decomposition chain.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "1NF",
                        "placeholder": "atomic values, no repeating groups",
                        "answer": "atomic values, no repeating groups",
                    },
                    {
                        "label": "2NF",
                        "placeholder": "no partial dependency",
                        "answer": "no partial dependency",
                    },
                    {
                        "label": "3NF",
                        "placeholder": "no transitive dependency",
                        "answer": "no transitive dependency",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break the ACID order",
            "captain_message": "Remember A, C, I, D.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "ACID stands for?",
                "options": [
                    "Atomicity, Consistency, Isolation, Durability",
                    "Access, Consistency, Integrity, Durability",
                    "Atomicity, Concurrency, Isolation, Data",
                    "Association, Consistency, Isolation, Durability",
                ],
                "answer_index": 0,
                "explanation": "Correct: Atomicity, Consistency, Isolation, Durability.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix update anomaly",
            "captain_message": "Decompose to eliminate repeating groups.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Anomaly",
                        "placeholder": "update anomaly in repeating group",
                        "answer": "update anomaly in repeating group",
                    },
                    {
                        "label": "Decompose",
                        "placeholder": "split into separate tables",
                        "answer": "split into separate tables",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to schema design",
            "captain_message": "Apply normalization before adding indexes.",
            "render": {
                "kind": "recall",
                "prompt": "Before adding an index, ensure?",
                "answer": "table is at least in 3NF",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "Key facts: 1NF=atomic, 2NF=no partial, 3NF=no transitive, BCNF=strict 3NF.",
            "render": {
                "kind": "recall",
                "prompt": "BCNF is stricter than?",
                "answer": "3NF",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "Which is a candidate key?",
                "options": ["Superkey", "Minimal superkey", "Foreign key", "Primary key"],
                "answer": "Minimal superkey",
                "explanation": "Candidate key = minimal superkey.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "A table with (emp_id, name, dept, dept_location) has partial dependency. Normal form?",
                "options": ["1NF", "2NF", "3NF", "BCNF"],
                "answer": "1NF",
                "explanation": "Partial dependency means not 2NF. So at most 1NF.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "ACID 'I' stands for?",
                "options": ["Integrity", "Isolation", "Index", "Instance"],
                "answer": "Isolation",
                "explanation": "I = Isolation.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "Which normal form removes transitive dependency?",
                "options": ["1NF", "2NF", "3NF", "BCNF"],
                "answer": "3NF",
                "explanation": "3NF removes transitive dependency.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "Relation R(A,B,C,D) with FDs A→B, B→C, C→D. Highest normal form?",
            "options": ["1NF", "2NF", "3NF", "BCNF"],
            "answer": "2NF",
            "explanation": "A→B, B→C, C→D. No partial dependency if key is A. But transitive dependency exists, so at most 2NF.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "Candidate key definition?",
            "answer": "minimal superkey",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "ACID 'D'?",
            "answer": "Durability",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "3NF removes?",
            "answer": "transitive dependency",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Keys, normalization",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "ACID, SQL",
        },
        {
            "company": "wipro",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Normal forms, indexing",
        },
    ],
    "interview_transfer": {
        "prompt": "How does normalization thinking help in API design?",
        "model_answer": "It trains separating concerns into focused entities, reducing redundant data movement and update anomalies.",
    },
}
