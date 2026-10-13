"""Pattern Pack — SQL JOINs.

Covers INNER, LEFT, RIGHT, and FULL JOIN semantics through visual table
merge operations.
"""
from __future__ import annotations

from typing import Any, Dict

pack: Dict[str, Any] = {
    "pattern_id": "sql-joins",
    "name": "SQL JOINs",
    "emoji": "🔗",
    "round_id": "cs-core",
    "purpose": "Choose the correct JOIN type and predict merged table output.",
    "prerequisites": ["dbms", "tables", "keys"],
    "misconceptions": [
        {
            "id": "J1",
            "label": "INNER vs LEFT confusion",
            "description": "Thinks LEFT JOIN returns only matching rows.",
        },
        {
            "id": "J2",
            "label": "Wrong ON condition",
            "description": "Joins on the wrong column pair, producing a Cartesian explosion.",
        },
        {
            "id": "J3",
            "label": "NULL handling",
            "description": "Does not expect NULLs in non-matching LEFT JOIN columns.",
        },
    ],
    "teaching": [
        {
            "id": "visual",
            "type": "visual",
            "title": "Two tables",
            "captain_message": "JOINs are about matching rows. Let's see two tables side by side.",
            "render": {
                "kind": "table_merge",
                "left_table": {"name": "Students", "columns": ["id", "name"], "rows": [[1, "Teja"], [2, "Ravi"], [3, "Anu"]]},
                "right_table": {"name": "Marks", "columns": ["id", "marks"], "rows": [[1, 87], [2, 74], [4, 92]]},
                "join_type": "INNER",
                "on": "id",
            },
        },
        {
            "id": "manipulate",
            "type": "manipulate",
            "title": "Change the JOIN",
            "captain_message": "Switch between INNER, LEFT, RIGHT. Watch the merged table change.",
            "render": {
                "kind": "join_switcher",
                "left_table": {"name": "Students", "columns": ["id", "name"], "rows": [[1, "Teja"], [2, "Ravi"], [3, "Anu"]]},
                "right_table": {"name": "Marks", "columns": ["id", "marks"], "rows": [[1, 87], [2, 74], [4, 92]]},
                "allowed_joins": ["INNER", "LEFT", "RIGHT"],
                "default": "INNER",
                "on": "id",
            },
        },
        {
            "id": "predict",
            "type": "predict",
            "title": "Predict the output",
            "captain_message": "Without running, how many rows does LEFT JOIN produce?",
            "render": {
                "kind": "multiple_choice",
                "question": "Students(3 rows) LEFT JOIN Marks(3 rows) on id. How many rows in the result?",
                "options": ["2", "3", "4", "6"],
                "answer_index": 1,
                "explanation": "LEFT JOIN keeps all left rows. 3 students, 2 matched, 1 unmatched with NULL marks → 3 rows.",
            },
        },
        {
            "id": "change",
            "type": "change",
            "title": "Change one thing",
            "captain_message": "Change INNER JOIN to LEFT JOIN. What row appears?",
            "render": {
                "kind": "compare_outputs",
                "original": {"join": "INNER", "expected_rows": 2},
                "modified": {"join": "LEFT", "expected_rows": 3},
                "highlight_diff": True,
            },
        },
        {
            "id": "build",
            "type": "build",
            "title": "Build the query",
            "captain_message": "Write the LEFT JOIN for these tables.",
            "render": {
                "kind": "fill_sql",
                "starter": "SELECT * FROM Students ___ JOIN Marks ON Students.id = Marks.id",
                "answer": "LEFT",
                "placeholders": ["LEFT"],
            },
        },
        {
            "id": "break",
            "type": "break",
            "title": "Break it",
            "captain_message": "This query looks correct. Find the trap.",
            "render": {
                "kind": "debug_sql",
                "buggy_sql": "SELECT * FROM Students JOIN Marks ON Students.name = Marks.name",
                "expected_failure": "Joining on name instead of id produces 0 rows because names don't match.",
                "diagnosis_code": "wrong_join_condition",
            },
        },
        {
            "id": "fix",
            "type": "fix",
            "title": "Fix the query",
            "captain_message": "Repair the ON clause.",
            "render": {
                "kind": "fix_sql",
                "broken": "ON Students.name = Marks.name",
                "answer": "ON Students.id = Marks.id",
            },
        },
        {
            "id": "transfer",
            "type": "transfer",
            "title": "Transfer: three tables",
            "captain_message": "Same idea. Three tables instead of two.",
            "render": {
                "kind": "chain_joins",
                "tables": ["Students", "Marks", "Subjects"],
                "correct_chain": "Students LEFT JOIN Marks ON id, then LEFT JOIN Subjects ON subject_id",
                "common_error": "Cartesian product from missing ON clause",
                "diagnosis_code": "wrong_join_condition",
            },
        },
        {
            "id": "placement",
            "type": "placement",
            "title": "TCS-style proof",
            "captain_message": "No tables. No hints. 60 seconds.",
            "render": {
                "kind": "timed_question",
                "seconds": 60,
                "question": "Given two tables with 5 and 4 rows, what is the maximum possible rows from a CROSS JOIN?",
                "options": ["5", "9", "4", "20"],
                "answer_index": 3,
                "explanation": "CROSS JOIN is Cartesian product: 5 × 4 = 20.",
            },
        },
    ],
    "practice": {
        "warmup": [
            {
                "id": "sql-w1",
                "topic": "sql-joins",
                "difficulty": "easy",
                "question": "INNER JOIN returns:",
                "options": ["All rows from both tables", "Only matching rows", "All left rows", "All right rows"],
                "answer": "Only matching rows",
                "explanation": "INNER JOIN keeps rows where the join condition is true in both tables.",
            },
        ],
        "drill": [
            {
                "id": "sql-d1",
                "topic": "sql-joins",
                "difficulty": "medium",
                "question": "LEFT JOIN returns:",
                "options": ["Only matching rows", "All left rows + matched right", "All rows from both", "Only non-matching rows"],
                "answer": "All left rows + matched right",
                "explanation": "LEFT JOIN preserves every row from the left table.",
            },
        ],
        "speed_run": [
            {
                "id": "sql-s1",
                "topic": "sql-joins",
                "difficulty": "medium",
                "question": "A JOIN without an ON clause produces:",
                "options": ["INNER JOIN", "LEFT JOIN", "CROSS JOIN", "FULL JOIN"],
                "answer": "CROSS JOIN",
                "explanation": "Missing ON implies Cartesian product.",
            },
        ],
        "weakness_repair": [
            {
                "id": "sql-r1",
                "topic": "sql-joins",
                "difficulty": "medium",
                "question": "A student gets 0 rows from a LEFT JOIN. The most likely cause is:",
                "options": ["LEFT JOIN always returns 0 rows", "No matching rows in right table", "Wrong database", "Syntax error"],
                "answer": "No matching rows in right table",
                "explanation": "LEFT JOIN still returns left rows even with no matches. 0 rows means the left table is empty or the query is filtered.",
                "diagnosis_code": "inner_vs_left_confusion",
            },
        ],
    },
    "assessment": [
        {
            "id": "sql-a1",
            "topic": "sql-joins",
            "difficulty": "medium",
            "question": "Table A has 6 rows, Table B has 4 rows. Maximum rows from INNER JOIN?",
            "options": ["6", "4", "10", "24"],
            "answer": "6",
            "explanation": "INNER JOIN result is bounded by the smaller table when keys are unique.",
        },
    ],
    "retention": [
        {
            "id": "sql-ret-1d",
            "due_days": 1,
            "prompt": "What is the key difference between INNER JOIN and LEFT JOIN?",
            "answer": "INNER keeps only matches; LEFT keeps all left rows.",
            "diagnosis_code": "inner_vs_left_confusion",
        },
        {
            "id": "sql-ret-3d",
            "due_days": 3,
            "prompt": "What happens if you JOIN without an ON clause?",
            "answer": "You get a CROSS JOIN / Cartesian product.",
            "diagnosis_code": "wrong_join_condition",
        },
        {
            "id": "sql-ret-7d",
            "due_days": 7,
            "prompt": "In a LEFT JOIN, unmatched right-table columns contain:",
            "answer": "NULL",
            "diagnosis_code": "null_handling",
        },
    ],
    "company_variants": [
        {
            "company": "tcs",
            "difficulty": "easy",
            "timing_seconds": 60,
            "context": "TCS NQT DBMS",
            "question_count": 3,
        },
        {
            "company": "infosys",
            "difficulty": "medium",
            "timing_seconds": 45,
            "context": "InfyTQ SQL",
            "question_count": 2,
        },
    ],
    "interview_transfer": {
        "prompt": "Explain INNER JOIN vs LEFT JOIN to a non-technical interviewer in 30 seconds.",
        "model_answer": "INNER JOIN is like an intersection: only people present in both lists. LEFT JOIN is like preserving the full guest list and marking absent invitees as null.",
        "success_criteria": ["intersection metaphor", "preservation metaphor", "mentions NULL for missing matches"],
    },
}
