"""Lesson module — DBMS Basics — Tables, Keys, and SQL"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'cs_core.dbms_basics',
            'module_id': 'cs_core.dbms_basics',
            'title': 'DBMS Basics — Tables, Keys, and SQL',
            'description': 'DBMS and SQL are asked in every technical interview. Know keys, normalization, and basic queries.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['DBMS Basics'],
            'srs_concept_tag': 'cs_core.dbms_basics',
            'domain': 'cs_core',
            'captain_byte': {
            'intro': 'A DBMS stores data in tables. Keys uniquely identify rows. SQL queries extract data.',
            'correct': ['Right key type.', 'Correct SQL syntax.', 'Right normal form.'],
            'wrong': ['Primary key must be unique and not null.', "Foreign key references another table's primary key.", 'Normalization removes redundancy and anomalies.'],
            'after_break': 'You found the DBMS error. Now fix the key or query.',
            'after_mastery': "You can now reason about databases and SQL. That's interview-ready CS skill.",
            'retry_prompt': 'Try again. Check the key constraints and SQL syntax.'
        },
            'story_context': {
            'title': 'DBMS Basics — Tables, Keys, and SQL',
            'narration': 'DBMS and SQL are asked in every technical interview. Know keys, normalization, and basic queries.',
            'setting': 'dbms_basics',
            'character': 'Captain Byte',
            'intro_text': 'DBMS and SQL are asked in every technical interview. Know keys, normalization, and basic queries.'
        },
            'steps': {
            'discover': {
            'visual_primitives': ['highlight', 'compare', 'reveal'],
            'steps': [{
            'action': 'see_table',
            'narration': 'A table STUDENT has columns ID, NAME, AGE. Which column is the primary key?',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'Which column is the primary key?',
            'options': [{
            'id': 'a',
            'text': 'ID',
            'correct': True
        }, {
            'id': 'b',
            'text': 'NAME',
            'correct': False
        }, {
            'id': 'c',
            'text': 'AGE',
            'correct': False
        }, {
            'id': 'd',
            'text': 'All columns',
            'correct': False
        }],
            'explanation': 'ID uniquely identifies each student.'
        }
        }, {
            'action': 'see_sql',
            'narration': 'SELECT NAME FROM STUDENT WHERE AGE > 18; What does this do?',
            'interaction': {
            'type': 'choose_outcome',
            'prompt': 'What does this query return?',
            'options': [{
            'id': 'a',
            'text': 'Names of students older than 18',
            'correct': True
        }, {
            'id': 'b',
            'text': 'All student names',
            'correct': False
        }, {
            'id': 'c',
            'text': 'Students aged exactly 18',
            'correct': False
        }, {
            'id': 'd',
            'text': 'Student ages',
            'correct': False
        }],
            'explanation': 'SELECT NAME filters rows where AGE > 18.'
        }
        }],
            'conclusion': 'Primary keys uniquely identify rows. Foreign keys link tables. SQL SELECT filters and projects data. Normalization removes redundancy.'
        },
            'understand': 'Primary key uniquely identifies a row. Foreign key references another table. Candidate keys are possible primary keys. Super key includes extra attributes. Normalization reduces redundancy and anomalies.',
            'manipulate': {
            'prompt': 'Write SQL to select all columns from EMPLOYEE where SALARY > 50000.',
            'answer': 'SELECT * FROM EMPLOYEE WHERE SALARY > 50000',
            'hint': 'Use * for all columns. WHERE filters rows.',
            'interaction_kind': 'sql_query'
        },
            'predict': {
            'prompt': 'What does this SQL return?\nSELECT COUNT(*) FROM STUDENT',
            'answer': 'Number of rows in STUDENT',
            'options': ['All student names', 'Number of rows', 'Average age', 'List of columns'],
            'interaction_kind': 'mcq_classify'
        },
            'build': {
            'prompt': 'Write a SQL query to find the second highest salary from EMPLOYEE.',
            'answer': 'SELECT MAX(SALARY) FROM EMPLOYEE WHERE SALARY < (SELECT MAX(SALARY) FROM EMPLOYEE)',
            'explanation': 'Subquery finds max, outer query finds max below that.',
            'interaction_kind': 'sql_query'
        },
            'break_step': {
            'prompt': 'A student writes SELECT NAME FROM STUDENT WHERE AGE = 18 to get all names. What is wrong?',
            'common_mistake': 'Using WHERE instead of removing it to get all rows.',
            'correct_reasoning': 'Without WHERE, all rows are returned. WHERE AGE = 18 filters.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix: SELECT NAME FROM STUDENT WHERE AGE = 18 should return all names.',
            'correct_reasoning': 'Remove the WHERE clause: SELECT NAME FROM STUDENT',
            'interaction_kind': 'sql_query'
        },
            'retrieval': {
            'prompt': 'What is a primary key?',
            'answer': 'Uniquely identifies a row',
            'alternative': ['unique', 'not null', 'single column or minimal set'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'Write SQL to find employees with salary above department average.',
            'answer': 'SELECT * FROM EMPLOYEE e WHERE SALARY > (SELECT AVG(SALARY) FROM EMPLOYEE WHERE DEPT = e.DEPT)',
            'explanation': 'Correlated subquery compares each row to its department average.',
            'interaction_kind': 'sql_query'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'Which key uniquely identifies a row?',
            'answer': 'Primary key',
            'options': ['Foreign key', 'Primary key', 'Candidate key', 'Super key'],
            'explanation': 'Primary key is the chosen unique identifier.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }, {
            'kind': 'mcq',
            'prompt': 'What does JOIN do?',
            'answer': 'Combines rows from two tables',
            'options': ['Deletes rows', 'Combines rows from two tables', 'Creates a new table', 'Updates values'],
            'explanation': 'JOIN combines tables based on a related column.',
            'difficulty': 'easy',
            'company_tags': ['tcs', 'infosys']
        }],
            'proof': [{
            'id': 'p1',
            'prompt': 'Write SQL to list department-wise average salary.',
            'answer_format': 'text',
            'correct': 'SELECT DEPT, AVG(SALARY) FROM EMPLOYEE GROUP BY DEPT',
            'explanation': 'GROUP BY groups rows by department. AVG computes average salary.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'company_variants': [{
            'company': 'tcs',
            'role': 'sde',
            'difficulty': 'medium',
            'extra_practice': ['tcs_sql_joins', 'tcs_sql_queries'],
            'proof_questions': [{
            'id': 'tcs-p1',
            'prompt': 'TCS: What is a foreign key?',
            'answer_format': 'text',
            'correct': 'References primary key of another table',
            'explanation': 'Foreign key enforces referential integrity.',
            'time_limit_seconds': 90,
            'company_tags': ['tcs']
        }]
        }],
            'misconceptions': [{
            'code': 'cs_core_normalization_misconception',
            'signature': 'Student thinks primary keys can have duplicates.',
            'reteach_route': 'bug_surgery',
            'reteach_action': 'show_unique_constraint'
        }, {
            'code': 'cs_core_normalization_misconception',
            'signature': 'Student thinks normalization is optional formatting.',
            'reteach_route': 'worked_example',
            'reteach_action': 'show_anomalies_without_normalization'
        }],
            'srs_key_points': ['Primary key uniquely identifies a row.', "Foreign key references another table's primary key.", 'SQL SELECT filters and projects data.', 'Normalization removes redundancy.', 'JOIN combines tables based on related columns.'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'cs_core',
            'competency_id': 'dbms_basics',
            'unlocks_next': [],
            'tower_badge': 'cs_core_dbms_basics'
        }
        }

SLUG = 'cs_core.dbms_basics'
