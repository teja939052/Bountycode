"""Pattern Pack — Normalization."""
from __future__ import annotations

from typing import Any, Dict, List

pack: Dict[str, Any] = {
    "pattern_id": "normalization",
    "name": "Normalization",
    "emoji": "📑",
    "round_id": "technical-interview",
    "purpose": "Apply 1NF/2NF/3NF/BCNF decomposition rules, identify anomalies, and decide when to denormalize.",
    "prerequisites": ["dbms", "sql-basics"],
    "misconceptions": [
        {
            "id": "M1",
            "label": "Higher NF always better",
            "description": "Ignores query performance cost of excessive joins.",
        },
        {
            "id": "M2",
            "label": "Primary key = normalization",
            "description": "Believes having a PK means the table is normalized.",
        },
        {
            "id": "M3",
            "label": "BCNF always satisfies 3NF",
            "description": "Reverses the relationship between BCNF and 3NF.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Anomalies in a table",
            "captain_message": "See insert, update, delete anomalies.",
            "render": {
                "kind": "anomaly_table",
                "table": "Employee(emp_id, name, dept, dept_location)",
                "anomalies": ["update", "insert", "delete"],
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Decompose table",
            "captain_message": "Split to remove partial dependency.",
            "render": {
                "kind": "decompose",
                "original": "Order(order_id, customer, product, price)",
                "target_normal_form": "2NF",
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict normal form",
            "captain_message": "Choose the highest normal form.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Table with (A,B,C,D), key=A, FD B→C. Normal form?",
                "options": ["1NF", "2NF", "3NF", "BCNF"],
                "answer_index": 1,
                "explanation": "Partial dependency B→C violates 2NF, so at most 1NF? Actually key is A, B is non-key. B→C is transitive via key? Not exactly. Simplification: partial dep means not 2NF.",
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build decomposition",
            "captain_message": "Write decomposed tables.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Original",
                        "placeholder": "R(A,B,C,D)",
                        "answer": "R(A,B,C,D)",
                    },
                    {
                        "label": "Decomposed",
                        "placeholder": "R1(A,B), R2(B,C,D)",
                        "answer": "R1(A,B), R2(B,C,D)",
                    },
                ],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break update anomaly",
            "captain_message": "Changing dept location requires updating many rows.",
            "render": {
                "kind": "multiple_choice",
                "prompt": "Update anomaly is fixed by?",
                "options": ["Adding more rows", "Decomposing into separate tables", "Adding index", "None"],
                "answer_index": 1,
                "explanation": "Decomposition removes repeating groups and anomalies.",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix to BCNF",
            "captain_message": "Ensure every determinant is a candidate key.",
            "render": {
                "kind": "fill_steps",
                "steps": [
                    {
                        "label": "Violation",
                        "placeholder": "non-key determinant",
                        "answer": "non-key determinant",
                    },
                    {
                        "label": "Decompose",
                        "placeholder": "split on determinant",
                        "answer": "split on determinant",
                    },
                ],
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer to schema design",
            "captain_message": "Normalize first, denormalize only for read performance.",
            "render": {
                "kind": "recall",
                "prompt": "When to denormalize?",
                "answer": "for read-heavy query performance after normalizing",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "Placement shortcut",
            "captain_message": "1NF=atomic, 2NF=no partial, 3NF=no transitive, BCNF=strict 3NF.",
            "render": {
                "kind": "recall",
                "prompt": "BCNF requires every determinant to be?",
                "answer": "candidate key",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "w1",
                "question": "1NF requires?",
                "options": ["Primary key", "Atomic values", "No redundancy", "Foreign keys"],
                "answer": "Atomic values",
                "explanation": "1NF = atomic values, no repeating groups.",
            },
        ],
        "drill": [
            {
                "id": "d1",
                "question": "Which normal form removes transitive dependency?",
                "options": ["1NF", "2NF", "3NF", "BCNF"],
                "answer": "3NF",
                "explanation": "3NF removes transitive dependency.",
            },
        ],
        "speed_run": [
            {
                "id": "s1",
                "question": "BCNF is stricter than?",
                "options": ["1NF", "2NF", "3NF", "All equal"],
                "answer": "3NF",
                "explanation": "BCNF is stricter than 3NF.",
            },
        ],
        "weakness_repair": [
            {
                "id": "wr1",
                "question": "Partial dependency violates?",
                "options": ["1NF", "2NF", "3NF", "BCNF"],
                "answer": "2NF",
                "explanation": "Partial dependency violates 2NF.",
            },
        ],
    },
    "assessment": [
        {
            "id": "a1",
            "question": "Relation R(A,B,C,D) with key A and FD B→C. Highest NF?",
            "options": ["1NF", "2NF", "3NF", "BCNF"],
            "answer": "1NF",
            "explanation": "Partial dependency B→C violates 2NF. So at most 1NF.",
        },
    ],
    "retention": [
        {
            "id": "r1",
            "due_days": 1,
            "prompt": "1NF requires?",
            "answer": "atomic values",
        },
        {
            "id": "r2",
            "due_days": 3,
            "prompt": "3NF removes?",
            "answer": "transitive dependency",
        },
        {
            "id": "r3",
            "due_days": 7,
            "prompt": "BCNF requires every determinant to be?",
            "answer": "candidate key",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "timing_seconds": 60,
            "question_count": 8,
            "focus": "Normal forms, keys",
        },
        {
            "company": "infosys",
            "timing_seconds": 45,
            "question_count": 10,
            "focus": "Anomalies, decomposition",
        },
    ],
    "interview_transfer": {
        "prompt": "How does normalization thinking help in API versioning?",
        "model_answer": "It trains separating concerns into versioned resources, avoiding coupling that creates migration anomalies.",
    },
}
