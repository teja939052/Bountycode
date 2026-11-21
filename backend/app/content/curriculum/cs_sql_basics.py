"""
Promoted Lesson: SQL Basics
===========================

Service-company technical foundation. Follows the full content contract.

Provenance: Pattern-relevant for service-company technical aptitude (TCS NQT, Wipro, Cognizant, etc.).
Not a claim about any private employer question bank.
"""
from typing import Dict, List, Any

LESSON_ID = "cs_sql_basics_01"
VERSION = "1.0.0"
SKILL_ID = "cs.sql_basics"
COMPANY_RELEVANCE = ["tcs", "wipro", "cognizant", "accenture", "capgemini", "infosys"]
EST_MINUTES = 15
XP_REWARD = 120

SQL_BASICS_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "computer_science:sql_basics",
    "title": "SQL Basics",
    "description": "Master fundamental SQL — SELECT, WHERE, JOIN, GROUP BY for technical aptitude.",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["select_query", "where_clause", "inner_join", "group_by", "aggregate_functions"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Write a basic SELECT query with WHERE clause.",
        "Use INNER JOIN to combine two tables.",
        "Apply GROUP BY with aggregate functions (COUNT, SUM, AVG).",
        "Filter grouped results with HAVING.",
    ],
    "prerequisites": [],
    "concept_explanation": {
        "title": "SQL Fundamentals",
        "text": (
            "SQL (Structured Query Language) manages relational databases. A table has rows "
            "(records) and columns (fields). SELECT retrieves data, WHERE filters rows, "
            "JOIN combines tables, and GROUP BY aggregates."
        ),
        "key_formula": "SELECT columns FROM table WHERE condition JOIN ... GROUP BY column.",
    },
    "worked_example": {
        "title": "Find employees in Sales department",
        "problem": "List names of employees who work in the 'Sales' department.",
        "query": "SELECT name FROM employees WHERE department = 'Sales';",
        "explanation": "SELECT name gets the name column, FROM employees specifies the table, WHERE filters to Sales department.",
    },
    "interactive_practice": [
        {
            "id": "sql_practice_1",
            "type": "mcq",
            "question": "Which SQL clause filters rows before grouping?",
            "options": ["HAVING", "WHERE", "GROUP BY", "ORDER BY"],
            "correct_index": 1,
            "explanation": "WHERE filters individual rows before any GROUP BY aggregation.",
        },
        {
            "id": "sql_practice_2",
            "type": "mcq",
            "question": "Which JOIN returns only matching rows from both tables?",
            "options": ["LEFT JOIN", "RIGHT JOIN", "INNER JOIN", "FULL JOIN"],
            "correct_index": 2,
            "explanation": "INNER JOIN returns only rows with matches in both tables.",
        },
    ],
    "misconception_feedback": {
        "where_vs_having": {
            "title": "Common mistake: WHERE vs HAVING",
            "text": "WHERE filters rows before aggregation; HAVING filters groups after aggregation.",
        },
    },
    "assessment": [
        {
            "id": "sql_assess_1",
            "type": "mcq",
            "question": "SELECT COUNT(*) FROM orders counts what?",
            "options": ["All columns", "All rows", "Distinct orders", "Non-null values"],
            "correct_index": 1,
            "explanation": "COUNT(*) counts all rows in the table.",
        },
        {
            "id": "sql_assess_2",
            "type": "mcq",
            "question": "Which keyword removes duplicate rows?",
            "options": ["UNIQUE", "DISTINCT", "DIFFERENT", "NO DUPLICATES"],
            "correct_index": 1,
            "explanation": "DISTINCT eliminates duplicate values in the result set.",
        },
    ],
    "transfer_task": {
        "title": "Real-world: Sales report",
        "problem": (
            "Write a query to find total sales per product category from a sales table "
            "(columns: category, amount). Show only categories with total > 1000."
        ),
        "query": "SELECT category, SUM(amount) AS total FROM sales GROUP BY category HAVING SUM(amount) > 1000;",
        "expected_columns": ["category", "total"],
    },
    "deterministic_answer_key": {
        "sql_practice_1": 1,
        "sql_practice_2": 2,
        "sql_assess_1": 1,
        "sql_assess_2": 1,
        "transfer_task": "SELECT category, SUM(amount) AS total FROM sales GROUP BY category HAVING SUM(amount) > 1000;",
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://www.w3schools.com/sql/",
        ],
        "note": (
            "This preparation path targets commonly reported patterns and role expectations. "
            "It is not a claim about a private employer question bank."
        ),
    },
    "review_state": "human_reviewed",
    "accessibility_metadata": {
        "color_blind_safe": True,
        "screen_reader_friendly": True,
        "font_scale_support": True,
    },
    "spaced_repetition_metadata": {
        "initial_interval_days": 2,
        "ease_factor": 2.5,
        "retention_target": 0.85,
    },
}
