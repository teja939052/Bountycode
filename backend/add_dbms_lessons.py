content = open('D:/Project-Fremen/backend/app/services/lessons/dbms.py', 'r', encoding='utf-8').read()

# Define new lessons to add
new_lessons = []

# Lesson 1: dbms-sql-joins-aggregation
new_lessons.append('''
    {
        "id": "dbms-sql-joins-aggregation",
        "title": "SQL Joins & Aggregation",
        "track": "dbms",
        "description": "JOIN operations and GROUP BY aggregations.",
        "difficulty": "intermediate",
        "prerequisites": ["dbms-sql-basics"],
        "xpReward": 80,
        "steps": [
            {
                "id": "ja1",
                "type": "explain",
                "title": "JOIN Types",
                "content": "INNER JOIN returns matching rows. LEFT JOIN returns all left rows. RIGHT JOIN returns all right rows. FULL JOIN returns all rows from both.",
                "code": "SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;",
                "output": "",
                "explanation": "INNER JOIN keeps only matching rows from both tables.",
            },
            {
                "id": "ja2",
                "type": "explain",
                "title": "GROUP BY & Aggregates",
                "content": "GROUP BY groups rows. COUNT, SUM, AVG, MIN, MAX aggregate values per group.",
                "code": "SELECT department, COUNT(*), AVG(salary) FROM employees GROUP BY department;",
                "output": "",
                "explanation": "GROUP BY collapses rows with same group key into one row per group.",
            },
            {
                "id": "ja3",
                "type": "quiz",
                "title": "JOIN vs Aggregate",
                "question": "Which clause groups rows into summary rows?",
                "options": ["WHERE", "GROUP BY", "ORDER BY", "LIMIT"],
                "correctIndex": 1,
                "explanation": "GROUP BY groups rows into summary rows for aggregate functions.",
            },
        ],
    },
''')

# Lesson 2: dbms-sql-subqueries-cte
new_lessons.append('''
    {
        "id": "dbms-sql-subqueries-cte",
        "title": "Subqueries & CTEs",
        "track": "dbms",
        "description": "Subqueries and Common Table Expressions (CTE).",
        "difficulty": "intermediate",
        "prerequisites": ["dbms-sql-basics"],
        "xpReward": 80,
        "steps": [
            {
                "id": "sq1",
                "type": "explain",
                "title": "Subqueries",
                "content": "A subquery is a query nested inside another query. Used in WHERE, FROM, SELECT clauses.",
                "code": "SELECT name FROM employees WHERE dept_id IN (SELECT id FROM departments WHERE dept_name = 'Sales');",
                "output": "",
                "explanation": "Subquery returns values used by the outer query.",
            },
            {
                "id": "sq2",
                "type": "explain",
                "title": "CTEs",
                "content": "CTE (WITH clause) defines a temporary result set referenced within the main query.",
                "code": "WITH dept_stats AS (SELECT dept_id, AVG(salary) AS avg_sal FROM employees GROUP BY dept_id) SELECT e.name, d.avg_sal FROM employees e JOIN dept_stats d ON e.dept_id = d.dept_id;",
                "output": "",
                "explanation": "CTE makes complex queries readable by naming intermediate results.",
            },
            {
                "id": "sq3",
                "type": "quiz",
                "title": "Subquery vs CTE",
                "question": "Which is better for reuse within a single query?",
                "options": ["Subquery", "CTE", "Both equal", "Neither"],
                "correctIndex": 1,
                "explanation": "CTEs are more readable and can be referenced multiple times within the same query.",
            },
        ],
    },
''')

# Lesson 3: dbms-indexing-and-query-plans
new_lessons.append('''
    {
        "id": "dbms-indexing-and-query-plans",
        "title": "Indexes & Query Plans",
        "track": "dbms",
        "description": "Database indexes, query plans, and performance optimization.",
        "difficulty": "intermediate",
        "prerequisites": ["dbms-sql-basics"],
        "xpReward": 90,
        "steps": [
            {
                "id": "ix1",
                "type": "explain",
                "title": "Indexes",
                "content": "Indexes speed up data retrieval by creating a sorted structure on columns. Trade-off: slower writes, faster reads.",
                "code": "CREATE INDEX idx_emp_dept ON employees(dept_id);",
                "output": "",
                "explanation": "Index on dept_id speeds up queries filtering by department.",
            },
            {
                "id": "ix2",
                "type": "explain",
                "title": "Query Plans",
                "content": "EXPLAIN shows how the database executes a query - which indexes used, join order, row estimates.",
                "code": "EXPLAIN SELECT * FROM employees WHERE dept_id = 5;",
                "output": "",
                "explanation": "EXPLAIN reveals the query planner's chosen execution strategy.",
            },
            {
                "id": "ix3",
                "type": "quiz",
                "title": "Index Purpose",
                "question": "What is the primary purpose of a database index?",
                "options": ["Data integrity", "Faster data retrieval", "Data encryption", "Automatic backup"],
                "correctIndex": 1,
                "explanation": "Indexes speed up data retrieval at the cost of slower writes and extra storage.",
            },
        ],
    },
''')

# Find the end of dbms-3nf lesson and insert new lessons before dbms-acid-properties
# Find "id": "dbms-acid-properties" and insert new lessons before it
marker = '        "id": "dbms-acid-properties",'
idx = content.find(marker)
if idx != -1:
    # Find the start of that lesson block (the { before "id")
    lesson_start = content.rfind('\n    {', 0, idx)
    # Insert new lessons before dbms-acid-properties
    new_content = content[:lesson_start] + ''.join(new_lessons) + content[lesson_start:]
    open('D:/Project-Fremen/backend/app/services/lessons/dbms.py', 'w', encoding='utf-8').write(new_content)
    print(f'Added {len(new_lessons)} new lessons before dbms-acid-properties')
else:
    print('ERROR: Could not find dbms-acid-properties')
PYEOF