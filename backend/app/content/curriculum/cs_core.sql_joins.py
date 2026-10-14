"""Lesson module — SQL JOINs — Combine Data Across Tables"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'cs_core.sql_joins',
            'module_id': 'cs_core.sql_joins',
            'title': 'SQL JOINs — Combine Data Across Tables',
            'description': 'SQL JOINs are the most frequently asked DBMS topic in service-company technical interviews. Mastery of INNER, LEFT, RIGHT, and FULL JOINs is expected for any database role.',
            'difficulty': 'medium',
            'est_minutes': 25,
            'xp_reward': 100,
            'skills_taught': ['SQL JOINs'],
            'srs_concept_tag': 'cs_core.sql_joins',
            'domain': 'cs_core',
            'captain_byte': {
            'intro': "JOINs combine tables. The key is understanding what happens when there's no match.",
            'correct': ['Correct JOIN!', 'You see the match!', 'VENN diagram clear!'],
            'wrong': ['Remember: INNER needs a match on both sides.', 'LEFT keeps all from the left table.'],
            'after_break': 'Now you see why unmatched rows disappear in INNER JOIN.',
            'after_mastery': "JOINs are now second nature. You'll ace any DBMS interview question.",
            'retry_prompt': 'Draw the VENN diagram again.'
        },
            'story_context': {
            'title': 'SQL JOINs — Combine Data Across Tables',
            'narration': 'SQL JOINs are the most frequently asked DBMS topic in service-company technical interviews. Mastery of INNER, LEFT, RIGHT, and FULL JOINs is expected for any database role.',
            'setting': 'sql_joins',
            'character': 'Captain Byte',
            'intro_text': 'SQL JOINs are the most frequently asked DBMS topic in service-company technical interviews. Mastery of INNER, LEFT, RIGHT, and FULL JOINs is expected for any database role.'
        },
            'steps': {
            'discover': {
            'prompt': 'Read this problem. What does the query return?',
            'question': 'SELECT * FROM employees e INNER JOIN departments d ON e.dept_id = d.id. What rows appear?',
            'options': ['Only employees with a matching department', 'All employees, even without department', 'All departments, even without employees', 'All combinations'],
            'interaction_kind': 'mcq_read'
        },
            'understand': {
            'prompt': 'INNER JOIN returns rows where BOTH tables have a match. Think of it as the intersection of two sets.',
            'explanation': 'INNER JOIN = VENN diagram overlap. Only rows with matching keys in both tables appear. Unmatched rows are excluded.',
            'interaction_kind': 'read_explanation'
        },
            'manipulate': {
            'prompt': 'Match each JOIN type to its behavior: INNER, LEFT, RIGHT, FULL.',
            'matches': {
            'INNER JOIN': 'Only matching rows from both tables',
            'LEFT JOIN': 'All rows from left + matching from right',
            'RIGHT JOIN': 'All rows from right + matching from left',
            'FULL JOIN': 'All rows from both tables'
        },
            'interaction_kind': 'match_relationships'
        },
            'predict': {
            'prompt': 'A LEFT JOIN of employees (5 rows) and departments (3 rows, 2 matched). How many rows?',
            'answer': '5',
            'options': ['3', '5', '8', '15'],
            'interaction_kind': 'mcq_bottleneck'
        },
            'build': {
            'prompt': 'Write a query to get all employees with their department names (use LEFT JOIN).',
            'answer': 'SELECT e.name, d.dept_name FROM employees e LEFT JOIN departments d ON e.dept_id = d.id',
            'explanation': 'LEFT JOIN ensures all employees appear, even if department is NULL.',
            'interaction_kind': 'code_build'
        },
            'break_step': {
            'prompt': 'What is wrong with using INNER JOIN when you want ALL employees?',
            'broken_query': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id',
            'expected_failure': 'Employees without a department are excluded. Use LEFT JOIN instead.',
            'interaction_kind': 'break_and_debug'
        },
            'debug': {
            'prompt': 'Fix this query to include all employees:',
            'answer': 'SELECT e.name, d.dept_name FROM employees e LEFT JOIN departments d ON e.dept_id = d.id',
            'broken_query': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id',
            'interaction_kind': 'code_debug'
        },
            'retrieval': {
            'prompt': 'What is the difference between INNER JOIN and LEFT JOIN?',
            'answer': 'INNER returns only matching rows. LEFT returns all left rows + matching right rows (NULL if no match).',
            'alternative': ['INNER = intersection. LEFT = all from left + match from right.'],
            'interaction_kind': 'recall_check'
        },
            'transfer': {
            'prompt': 'Write a query to find employees without a department (use LEFT JOIN + WHERE).',
            'answer': 'SELECT e.name FROM employees e LEFT JOIN departments d ON e.dept_id = d.id WHERE d.id IS NULL',
            'explanation': 'LEFT JOIN keeps all employees. WHERE d.id IS NULL filters to those with no match.',
            'interaction_kind': 'code_transfer'
        }
        },
            'practice': [{
            'kind': 'code',
            'prompt': 'What does this return?\nSELECT * FROM A LEFT JOIN B ON A.id = B.id WHERE B.id IS NULL',
            'answer': 'Rows in A with no match in B',
            'explanation': 'LEFT JOIN keeps all A. WHERE B.id IS NULL filters to unmatched A rows.',
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': 'Given tables Employees(id, name, dept_id) and Departments(id, dept_name), write a query to list all departments and the number of employees in each (including 0).',
            'answer_format': 'code',
            'correct': 'SELECT d.dept_name, COUNT(e.id) FROM departments d LEFT JOIN employees e ON d.id = e.dept_id GROUP BY d.dept_name',
            'explanation': 'LEFT JOIN ensures all departments appear. COUNT(e.id) counts employees (0 if none).',
            'time_limit_seconds': 120,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'tcs',
            'role': 'sde',
            'difficulty': 'medium',
            'proof_questions': [{
            'id': 'tcs-p1',
            'prompt': 'TCS: Write a SELF JOIN to find employees who report to the same manager.',
            'answer_format': 'code',
            'correct': 'SELECT e1.name, e2.name FROM employees e1 JOIN employees e2 ON e1.manager_id = e2.manager_id WHERE e1.id != e2.id',
            'explanation': 'SELF JOIN joins the table to itself on manager_id.',
            'time_limit_seconds': 120,
            'company_tags': ['tcs']
        }]
        }],
            'misconceptions': [{
            'code': 'sql_join_key_confusion',
            'signature': 'Student thinks JOIN returns rows from both tables regardless of match.',
            'reteach_route': 'compare_worlds',
            'reteach_action': 'show_venn_diagram'
        }],
            'srs_key_points': ['INNER JOIN = intersection (matching rows only).', 'LEFT JOIN = all left rows + matching right rows (NULL if no match).', 'RIGHT JOIN = all right rows + matching left rows.', 'FULL JOIN = all rows from both tables.', 'Use LEFT JOIN + WHERE right.col IS NULL to find unmatched left rows.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'cs_core',
            'competency_id': 'sql_joins',
            'unlocks_next': [],
            'tower_badge': 'cs_core_sql_joins'
        }
        }

SLUG = 'cs_core.sql_joins'
