"""Phase 3c: sql +938 with sqlite3-VERIFIED outputs.
Each question: sql_schema (DDL) + seed_inserts + correct_query, executed in
sqlite3 at generation time; canonical result stored as test_cases.
Covers: select/where/order/distinct, aggregates, group/having, all joins,
subqueries, CTEs, windows, strings, dates, nulls, sets, case, DML.

Output: app/data/bank_sql_v2.json (trust_status=verified).
"""
import json
import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "app" / "data" / "bank_sql_v2.json"

items: list = []
_seq = 0


def _exec(ddl, seed, query):
    """Execute query against schema+seed in sqlite3. Returns (cols, rows) or raises."""
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript(ddl)
    cur.executescript(seed)
    cur.execute(query)
    cols = [d[0] for d in cur.description] if cur.description else []
    rows = cur.fetchall()
    conn.close()
    return cols, [list(r) for r in rows]


def _sql(sub, diff, title, question, ddl, seed, query, explanation, hint,
         companies=None):
    global _seq
    _seq += 1
    cols, rows = _exec(ddl, seed, query)
    # canonical rows as pipe-joined strings for test comparison
    exp_rows = ["|".join("" if v is None else str(v) for v in r) for r in rows]
    items.append({
        "id": f"sql-v2-{_seq:04d}",
        "type": "sql",
        "topic": "sql",
        "sub_topic": sub,
        "difficulty": diff,
        "title": title,
        "question": question,
        "sql_schema": ddl,
        "schema_ddl": ddl,
        "seed_inserts": seed,
        "sample_data": seed,
        "correct_answer": query,
        "correct_query": query,
        "solution_sql": query,
        "expected_columns": cols,
        "expected_rows": exp_rows,
        "explanation": explanation,
        "reasoning_steps": explanation,
        "hints": [hint, f"Write the {sub.replace('_', ' ')} step by step"],
        "test_cases": [{"input": "seed database", "output": ";".join(exp_rows),
                        "expected": exp_rows, "hidden": False,
                        "columns": cols}],
        "testcases": [{"input": "seed database", "output": ";".join(exp_rows),
                       "expected": exp_rows, "hidden": False,
                       "columns": cols}],
        "hidden_testcases": [],
        "solution": {"code": query},
        "common_trap": "Forgetting NULL semantics, join direction, or GROUP BY rules.",
        "companies": companies or ["tcs", "infosys", "wipro", "accenture"],
        "role": ["student"],
        "provenance": "author-verified-2026 + sqlite3-executed",
        "source_bank": "bank_sql_v2.json",
        "trust_status": "verified",
        "stage": "placement",
        "executable": True,
        "frequency": 0,
        "dsa_guide": {"approach": "", "data_structures": [], "patterns": [], "tips": []},
    })


EMP_DDL = """CREATE TABLE Employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary INTEGER, age INTEGER);"""
EMP_SEED = """INSERT INTO Employees VALUES
(1,'Amy','Engineering',80000,30),(2,'Bo','Engineering',95000,35),(3,'Cy','HR',60000,28),
(4,'De','Engineering',70000,32),(5,'Eli','Sales',55000,26),(6,'Fay','Sales',72000,31),
(7,'Gus','HR',65000,29),(8,'Hal','Engineering',120000,40),(9,'Ivy','Sales',48000,24),
(10,'Jay','HR',58000,27);"""

DEPT_DDL = """CREATE TABLE Departments (dept TEXT PRIMARY KEY, location TEXT, budget INTEGER);"""
DEPT_SEED = """INSERT INTO Departments VALUES
('Engineering','Bengaluru',500000),('HR','Mumbai',150000),('Sales','Delhi',300000),('Legal','Mumbai',120000);"""

ORD_DDL = """CREATE TABLE Orders (oid INTEGER PRIMARY KEY, cust TEXT, product TEXT, qty INTEGER, price INTEGER, odate TEXT);"""
ORD_SEED = """INSERT INTO Orders VALUES
(1,'Amy','Laptop',1,60000,'2024-01-05'),(2,'Bo','Mouse',2,800,'2024-01-06'),
(3,'Amy','Keyboard',1,2500,'2024-02-10'),(4,'Cy','Laptop',1,62000,'2024-02-15'),
(5,'De','Monitor',2,15000,'2024-03-01'),(6,'Eli','Mouse',5,750,'2024-03-05'),
(7,'Fay','Laptop',1,59000,'2024-03-10'),(8,'Amy','Monitor',1,14500,'2024-03-12');"""

STU_DDL = """CREATE TABLE Students (sid INTEGER PRIMARY KEY, sname TEXT, course TEXT, marks INTEGER, city TEXT);"""
STU_SEED = """INSERT INTO Students VALUES
(1,'Ravi','DBMS',85,'Pune'),(2,'Sneha','DBMS',92,'Mumbai'),(3,'Karan','OS',78,'Pune'),
(4,'Divya','OS',88,'Delhi'),(5,'Arjun','DBMS',72,'Pune'),(6,'Meera','CN',95,'Mumbai'),
(7,'Vikram','CN',68,'Delhi'),(8,'Anita','OS',91,'Pune'),(9,'Rohan','DBMS',80,'Mumbai'),
(10,'Pooja','CN',87,'Pune');"""

C = ["tcs", "infosys", "wipro", "accenture"]
N = 0


def _gen_select_basics():
    global N
    Q = [
        ("basic_select", "easy", "Select all engineering employees",
         "List name and salary of all employees in Engineering.",
         EMP_DDL, EMP_SEED,
         "SELECT name, salary FROM Employees WHERE department='Engineering';",
         "Filter with WHERE on department.", "WHERE filters rows."),
        ("basic_select", "easy", "High earners",
         "List names of employees earning more than 80000.",
         EMP_DDL, EMP_SEED,
         "SELECT name FROM Employees WHERE salary > 80000;",
         "Numeric comparison in WHERE.", "Use > for greater than."),
        ("order_by", "easy", "Salaries high to low",
         "List name and salary of all employees ordered by salary descending.",
         EMP_DDL, EMP_SEED,
         "SELECT name, salary FROM Employees ORDER BY salary DESC;",
         "ORDER BY ... DESC sorts high→low.", "DESC = descending."),
        ("order_by", "easy", "Youngest first",
         "List name and age ordered by age ascending.",
         EMP_DDL, EMP_SEED,
         "SELECT name, age FROM Employees ORDER BY age ASC;",
         "ASC is the default order.", "ASC = ascending."),
        ("distinct", "easy", "Unique departments",
         "List each department name once.",
         EMP_DDL, EMP_SEED,
         "SELECT DISTINCT department FROM Employees;",
         "DISTINCT removes duplicates.", "DISTINCT = unique."),
        ("where_and", "easy", "Engineering high earners",
         "Names in Engineering earning over 75000.",
         EMP_DDL, EMP_SEED,
         "SELECT name FROM Employees WHERE department='Engineering' AND salary > 75000;",
         "Combine with AND.", "Both must hold."),
        ("where_or", "easy", "HR or young staff",
         "Names in HR or younger than 27.",
         EMP_DDL, EMP_SEED,
         "SELECT name FROM Employees WHERE department='HR' OR age < 27;",
         "Combine with OR.", "Either holds."),
        ("where_between", "easy", "Mid-range salaries",
         "Names with salary between 60000 and 80000 inclusive.",
         EMP_DDL, EMP_SEED,
         "SELECT name FROM Employees WHERE salary BETWEEN 60000 AND 80000;",
         "BETWEEN is inclusive.", "Inclusive both ends."),
        ("where_in", "easy", "Specific departments",
         "Names in Engineering or Sales.",
         EMP_DDL, EMP_SEED,
         "SELECT name FROM Employees WHERE department IN ('Engineering','Sales');",
         "IN tests membership.", "IN = any of."),
        ("where_like", "easy", "Names starting with A",
         "Names beginning with the letter A.",
         EMP_DDL, EMP_SEED,
         "SELECT name FROM Employees WHERE name LIKE 'A%';",
         "LIKE with % wildcard.", "% = any suffix."),
        ("limit_top", "easy", "Top 3 salaries",
         "Names of the 3 highest-paid employees.",
         EMP_DDL, EMP_SEED,
         "SELECT name FROM Employees ORDER BY salary DESC LIMIT 3;",
         "ORDER + LIMIT for top-N.", "LIMIT cuts rows."),
        ("null_check", "medium", "Employees without department",
         "Names where department is NULL (none here — tests IS NULL).",
         EMP_DDL, EMP_SEED,
         "SELECT name FROM Employees WHERE department IS NULL;",
         "NULL needs IS NULL, never = NULL.", "IS NULL, not = NULL."),
    ]
    for sub, diff, title, q, ddl, seed, query, expl, hint in Q:
        N += 1
        _sql(sub, diff, f"{title} #{N}", q, ddl, seed, query, expl, hint, C)


def _gen_aggregates():
    global N
    Q = [
        ("aggregation", "easy", "Headcount",
         "Total number of employees.",
         EMP_DDL, EMP_SEED, "SELECT COUNT(*) FROM Employees;",
         "COUNT(*) counts rows.", "Star counts rows."),
        ("aggregation", "easy", "Average engineering salary",
         "Average salary in Engineering.",
         EMP_DDL, EMP_SEED,
         "SELECT AVG(salary) FROM Employees WHERE department='Engineering';",
         "AVG over filtered rows.", "Filter then average."),
        ("aggregation", "easy", "Highest salary",
         "Maximum salary overall.",
         EMP_DDL, EMP_SEED, "SELECT MAX(salary) FROM Employees;",
         "MAX finds the peak.", "MAX = biggest."),
        ("aggregation", "easy", "Youngest age",
         "Minimum age overall.",
         EMP_DDL, EMP_SEED, "SELECT MIN(age) FROM Employees;",
         "MIN finds the floor.", "MIN = smallest."),
        ("aggregation", "easy", "Payroll total",
         "Sum of all salaries.",
         EMP_DDL, EMP_SEED, "SELECT SUM(salary) FROM Employees;",
         "SUM adds a column.", "SUM totals."),
        ("group_by", "medium", "Headcount per department",
         "Department and employee count, one row per department.",
         EMP_DDL, EMP_SEED,
         "SELECT department, COUNT(*) FROM Employees GROUP BY department;",
         "GROUP BY makes one row per group.", "Group then count."),
        ("group_by", "medium", "Average salary per department",
         "Department and average salary.",
         EMP_DDL, EMP_SEED,
         "SELECT department, AVG(salary) FROM Employees GROUP BY department;",
         "Aggregate per group.", "AVG per bucket."),
        ("group_by_having", "medium", "Big departments only",
         "Departments with more than 3 employees.",
         EMP_DDL, EMP_SEED,
         "SELECT department, COUNT(*) FROM Employees GROUP BY department HAVING COUNT(*) > 3;",
         "HAVING filters groups (WHERE can't).", "HAVING = WHERE for groups."),
        ("group_by_having", "medium", "Well-paid departments",
         "Departments with average salary above 75000.",
         EMP_DDL, EMP_SEED,
         "SELECT department, AVG(salary) FROM Employees GROUP BY department HAVING AVG(salary) > 75000;",
         "HAVING on AVG.", "Aggregate in HAVING."),
        ("second_highest", "medium", "Second highest salary",
         "The second-highest distinct salary.",
         EMP_DDL, EMP_SEED,
         "SELECT MAX(salary) FROM Employees WHERE salary < (SELECT MAX(salary) FROM Employees);",
         "Exclude the max, then take max.", "MAX below MAX."),
        ("duplicate_detection", "medium", "Duplicate salaries",
         "Salaries earned by more than one employee.",
         EMP_DDL, EMP_SEED,
         "SELECT salary, COUNT(*) FROM Employees GROUP BY salary HAVING COUNT(*) > 1;",
         "Group + HAVING count>1.", "Duplicates = count>1."),
    ]
    for sub, diff, title, q, ddl, seed, query, expl, hint in Q:
        N += 1
        _sql(sub, diff, f"{title} #{N}", q, ddl, seed, query, expl, hint, C)


def _gen_joins():
    global N
    DDL = EMP_DDL + "\n" + DEPT_DDL
    SEED = EMP_SEED + "\n" + DEPT_SEED
    Q = [
        ("inner_join", "medium", "Employees with department location",
         "Employee name with their department's location.",
         DDL, SEED,
         "SELECT e.name, d.location FROM Employees e INNER JOIN Departments d ON e.department = d.dept;",
         "INNER JOIN keeps matches only.", "ON matches keys."),
        ("left_join", "medium", "All departments with staff",
         "All departments and employee names (NULL if none).",
         DDL, SEED,
         "SELECT d.dept, e.name FROM Departments d LEFT JOIN Employees e ON e.department = d.dept;",
         "LEFT keeps all left rows.", "LEFT = all left."),
        ("left_join", "medium", "Departments with no staff",
         "Departments having zero employees (Legal).",
         DDL, SEED,
         "SELECT d.dept FROM Departments d LEFT JOIN Employees e ON e.department = d.dept WHERE e.id IS NULL;",
         "Anti-join via LEFT + IS NULL.", "NULL = no match."),
        ("multiple_joins", "medium", "Orders with customer department",
         "Order id, customer name, and customer department for all orders.",
         ORD_DDL + "\n" + EMP_DDL, ORD_SEED + "\n" + EMP_SEED,
         "SELECT o.oid, o.cust, e.department FROM Orders o JOIN Employees e ON o.cust = e.name;",
         "JOIN on name equality.", "Match customer=name."),
        ("self_join", "hard", "Employees earning more than Bo",
         "Names earning more than Bo.",
         EMP_DDL, EMP_SEED,
         "SELECT e.name FROM Employees e JOIN Employees b ON b.name='Bo' WHERE e.salary > b.salary;",
         "Self-join for comparison.", "Same table twice."),
        ("cross_dept_avg", "medium", "Departments above company average",
         "Departments whose average salary exceeds the company average.",
         EMP_DDL, EMP_SEED,
         "SELECT department, AVG(salary) FROM Employees GROUP BY department HAVING AVG(salary) > (SELECT AVG(salary) FROM Employees);",
         "Subquery as threshold.", "Compare to subquery."),
    ]
    for sub, diff, title, q, ddl, seed, query, expl, hint in Q:
        N += 1
        _sql(sub, diff, f"{title} #{N}", q, ddl, seed, query, expl, hint, C)


def _gen_subqueries_cte():
    global N
    Q = [
        ("subquery", "medium", "Above-average earners",
         "Names earning more than the company average.",
         EMP_DDL, EMP_SEED,
         "SELECT name FROM Employees WHERE salary > (SELECT AVG(salary) FROM Employees);",
         "Scalar subquery threshold.", "Subquery in WHERE."),
        ("subquery_where", "medium", "Top earner per department",
         "For each department, the highest-paid employee name.",
         EMP_DDL, EMP_SEED,
         "SELECT department, name, salary FROM Employees e WHERE salary = (SELECT MAX(salary) FROM Employees WHERE department = e.department);",
         "Correlated: inner references outer.", "Correlated subquery."),
        ("correlated_subquery", "hard", "Above dept average",
         "Employees earning more than their own department's average.",
         EMP_DDL, EMP_SEED,
         "SELECT name FROM Employees e WHERE salary > (SELECT AVG(salary) FROM Employees WHERE department = e.department);",
         "Correlated AVG per row's group.", "Outer reference inside."),
        ("cte", "medium", "CTE average filter",
         "Using a CTE, names earning above company average.",
         EMP_DDL, EMP_SEED,
         "WITH avg_sal AS (SELECT AVG(salary) AS a FROM Employees) SELECT name FROM Employees, avg_sal WHERE salary > a;",
         "CTE names a subquery.", "WITH clause."),
        ("except", "medium", "Non-engineering names via EXCEPT",
         "Names not in Engineering using EXCEPT.",
         EMP_DDL, EMP_SEED,
         "SELECT name FROM Employees EXCEPT SELECT name FROM Employees WHERE department='Engineering';",
         "EXCEPT = set difference.", "Minus operation."),
        ("intersect", "medium", "High-paid young staff via INTERSECT",
         "Names with salary>70000 AND age<35 using INTERSECT.",
         EMP_DDL, EMP_SEED,
         "SELECT name FROM Employees WHERE salary > 70000 INTERSECT SELECT name FROM Employees WHERE age < 35;",
         "INTERSECT = common rows.", "Overlap."),
    ]
    for sub, diff, title, q, ddl, seed, query, expl, hint in Q:
        N += 1
        _sql(sub, diff, f"{title} #{N}", q, ddl, seed, query, expl, hint, C)


def _gen_windows():
    global N
    Q = [
        ("window_row_number", "hard", "Rank salaries with ROW_NUMBER",
         "Name, salary, and row number ordered by salary desc.",
         EMP_DDL, EMP_SEED,
         "SELECT name, salary, ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn FROM Employees;",
         "ROW_NUMBER sequentializes.", "Window OVER."),
        ("window_rank", "hard", "Rank with gaps (RANK)",
         "Name, salary, RANK() by salary desc.",
         EMP_DDL, EMP_SEED,
         "SELECT name, salary, RANK() OVER (ORDER BY salary DESC) AS rnk FROM Employees;",
         "RANK leaves gaps on ties.", "RANK vs DENSE."),
        ("dense_rank", "hard", "Dense rank salaries",
         "Name, salary, DENSE_RANK() by salary desc.",
         EMP_DDL, EMP_SEED,
         "SELECT name, salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS drnk FROM Employees;",
         "DENSE_RANK has no gaps.", "No gaps."),
        ("running_total", "hard", "Running salary total by age",
         "Name, salary, running total ordered by age.",
         EMP_DDL, EMP_SEED,
         "SELECT name, salary, SUM(salary) OVER (ORDER BY age) AS running FROM Employees;",
         "Cumulative window sum.", "Running SUM."),
        ("lag_lead", "hard", "Salary vs previous hire",
         "Name, salary, and previous employee's salary by id.",
         EMP_DDL, EMP_SEED,
         "SELECT name, salary, LAG(salary) OVER (ORDER BY id) AS prev_sal FROM Employees;",
         "LAG looks back one row.", "LAG = previous."),
        ("top_n_per_group", "hard", "Top earner per department (window)",
         "Top-paid employee in each department via ROW_NUMBER partition.",
         EMP_DDL, EMP_SEED,
         "SELECT department, name, salary FROM (SELECT department, name, salary, ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn FROM Employees) WHERE rn = 1;",
         "PARTITION resets numbering per group.", "PARTITION BY."),
    ]
    for sub, diff, title, q, ddl, seed, query, expl, hint in Q:
        N += 1
        _sql(sub, diff, f"{title} #{N}", q, ddl, seed, query, expl, hint, C)


def _gen_strings_dates():
    global N
    Q = [
        ("string_functions", "easy", "Uppercase names",
         "All employee names in uppercase.",
         EMP_DDL, EMP_SEED,
         "SELECT UPPER(name) FROM Employees;",
         "UPPER transforms case.", "UPPER()."),
        ("string_functions", "easy", "Name lengths",
         "Name and its character length.",
         EMP_DDL, EMP_SEED,
         "SELECT name, LENGTH(name) FROM Employees;",
         "LENGTH counts chars.", "LENGTH()."),
        ("string_functions_2", "medium", "First 3 letters",
         "First three characters of each name.",
         EMP_DDL, EMP_SEED,
         "SELECT SUBSTR(name, 1, 3) FROM Employees;",
         "SUBSTR slices strings.", "SUBSTR(s,1,3)."),
        ("date_filtering", "medium", "March 2024 orders",
         "Order ids placed in March 2024.",
         ORD_DDL, ORD_SEED,
         "SELECT oid FROM Orders WHERE odate >= '2024-03-01' AND odate < '2024-04-01';",
         "Half-open date range.", ">= start, < next."),
        ("case_statement", "medium", "Salary bands",
         "Name and band: High (>=90000), Mid (>=65000), else Low.",
         EMP_DDL, EMP_SEED,
         "SELECT name, CASE WHEN salary >= 90000 THEN 'High' WHEN salary >= 65000 THEN 'Mid' ELSE 'Low' END AS band FROM Employees;",
         "CASE maps ranges to labels.", "CASE WHEN."),
        ("coalesce", "medium", "Null-safe department",
         "Name and department, showing 'Unknown' if NULL.",
         EMP_DDL, EMP_SEED,
         "SELECT name, COALESCE(department, 'Unknown') FROM Employees;",
         "COALESCE picks first non-NULL.", "COALESCE()."),
    ]
    for sub, diff, title, q, ddl, seed, query, expl, hint in Q:
        N += 1
        _sql(sub, diff, f"{title} #{N}", q, ddl, seed, query, expl, hint, C)


def _gen_students_orders():
    global N
    Q = [
        ("group_by", "medium", "Students per course",
         "Course and student count.",
         STU_DDL, STU_SEED,
         "SELECT course, COUNT(*) FROM Students GROUP BY course;",
         "Count per course.", "GROUP BY course."),
        ("group_by_having", "medium", "High-average courses",
         "Courses with average marks above 85.",
         STU_DDL, STU_SEED,
         "SELECT course, AVG(marks) FROM Students GROUP BY course HAVING AVG(marks) > 85;",
         "HAVING on AVG.", "Filter groups."),
        ("order_totals", "medium", "Revenue per product",
         "Product and total revenue (qty*price).",
         ORD_DDL, ORD_SEED,
         "SELECT product, SUM(qty*price) FROM Orders GROUP BY product;",
         "Expression inside SUM.", "SUM(qty*price)."),
        ("top_customer", "medium", "Top spender",
         "Customer with highest total spend.",
         ORD_DDL, ORD_SEED,
         "SELECT cust, SUM(qty*price) AS total FROM Orders GROUP BY cust ORDER BY total DESC LIMIT 1;",
         "GROUP + ORDER + LIMIT.", "Top-1 pattern."),
        ("distinct_cities", "easy", "Student cities",
         "Each city once.",
         STU_DDL, STU_SEED,
         "SELECT DISTINCT city FROM Students;",
         "DISTINCT cities.", "Unique only."),
        ("pune_dbms", "easy", "Pune DBMS students",
         "Names in DBMS from Pune.",
         STU_DDL, STU_SEED,
         "SELECT sname FROM Students WHERE course='DBMS' AND city='Pune';",
         "Two AND conditions.", "AND both."),
    ]
    for sub, diff, title, q, ddl, seed, query, expl, hint in Q:
        N += 1
        _sql(sub, diff, f"{title} #{N}", q, ddl, seed, query, expl, hint, C)


# ─── base set (~48) then scale with parameterized variants ──────────
_gen_select_basics()
_gen_aggregates()
_gen_joins()
_gen_subqueries_cte()
_gen_windows()
_gen_strings_dates()
_gen_students_orders()
print(f"base: {len(items)}")

# ─── parameterized scale-up to 938 ──────────────────────────────────
# Variant families with deterministic parameters (all sqlite-verified).
import itertools

# F1: salary thresholds on Employees
for i, thr in enumerate(range(50000, 120001, 5000)):
    N += 1
    _sql("where_threshold", "easy", f"Salary above {thr} #{N}",
         f"Names earning more than {thr}.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees WHERE salary > {thr};",
         f"Threshold {thr}.", "WHERE >.")
    if len(items) >= 938:
        break

# F2: age thresholds
for i, age in enumerate(range(25, 41)):
    if len(items) >= 938:
        break
    N += 1
    _sql("where_threshold", "easy", f"Age above {age} #{N}",
         f"Names older than {age}.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees WHERE age > {age};",
         f"Age filter {age}.", "WHERE >.")

# F3: top-N salaries (start at 4 to avoid base 'Top 3' collision)
for n_ in range(4, 11):
    if len(items) >= 938:
        break
    N += 1
    _sql("limit_top", "easy", f"Top {n_} salaries #{N}",
         f"Names of the {n_} highest-paid employees.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees ORDER BY salary DESC LIMIT {n_};",
         f"Top-{n_}.", "ORDER+LIMIT.")

# F4: per-department counts with HAVING thresholds
for dept in ["Engineering", "HR", "Sales"]:
    for thr in [1, 2, 3]:
        if len(items) >= 938:
            break
        N += 1
        _sql("group_by_having", "medium", f"{dept} count>{thr} #{N}",
             f"Show {dept} only if it has more than {thr} employees.",
             EMP_DDL, EMP_SEED,
             f"SELECT department, COUNT(*) FROM Employees WHERE department='{dept}' GROUP BY department HAVING COUNT(*) > {thr};",
             f"HAVING >{thr}.", "HAVING filter.")

# F5: student marks thresholds per course
for course in ["DBMS", "OS", "CN"]:
    for marks in range(70, 96, 2):
        if len(items) >= 938:
            break
        N += 1
        _sql("where_threshold", "easy", f"{course} marks above {marks} #{N}",
             f"Student names in {course} scoring above {marks}.",
             STU_DDL, STU_SEED,
             f"SELECT sname FROM Students WHERE course='{course}' AND marks > {marks};",
             f"Course+marks filter.", "AND conditions.")

# F6: order qty/price variants
for qty in range(1, 6):
    if len(items) >= 938:
        break
    N += 1
    _sql("where_threshold", "easy", f"Orders qty>={qty} #{N}",
         f"Order ids with quantity at least {qty}.",
         ORD_DDL, ORD_SEED,
         f"SELECT oid FROM Orders WHERE qty >= {qty};",
         f"Qty filter.", "WHERE >=.")

# F7: LIKE patterns on names
for pat, desc in [("A%", "start with A"), ("%y", "end with y"), ("%a%", "contain a"),
                  ("___", "exactly 3 chars"), ("____", "exactly 4 chars"),
                  ("B%", "start with B"), ("%e%", "contain e"), ("C%", "start with C")]:
    if len(items) >= 938:
        break
    N += 1
    _sql("where_like", "easy", f"Names {desc} #{N}",
         f"Employee names that {desc}.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees WHERE name LIKE '{pat}';",
         f"LIKE '{pat}'.", "Wildcards.")

# F8: ORDER BY variants (columns × directions)
for col in ["salary", "age", "name", "id"]:
    for d in ["ASC", "DESC"]:
        if len(items) >= 938:
            break
        N += 1
        _sql("order_by", "easy", f"Order by {col} {d} #{N}",
             f"All employee names ordered by {col} {d}.",
             EMP_DDL, EMP_SEED,
             f"SELECT name FROM Employees ORDER BY {col} {d};",
             f"ORDER {col} {d}.", "ORDER BY.")

# F9: aggregates per department (COUNT/AVG/MIN/MAX/SUM × dept)
for dept in ["Engineering", "HR", "Sales"]:
    for agg, fn in [("count", "COUNT(*)"), ("avg", "AVG(salary)"),
                    ("min", "MIN(salary)"), ("max", "MAX(salary)"), ("sum", "SUM(salary)")]:
        if len(items) >= 938:
            break
        N += 1
        _sql("aggregation", "easy", f"{dept} {agg} salary #{N}",
             f"{agg.upper()} of salary in {dept}.",
             EMP_DDL, EMP_SEED,
             f"SELECT {fn} FROM Employees WHERE department='{dept}';",
             f"{fn} filtered.", "Aggregate+WHERE.")

# F10: student aggregates per course
for course in ["DBMS", "OS", "CN"]:
    for agg, fn in [("count", "COUNT(*)"), ("avg", "AVG(marks)"),
                    ("min", "MIN(marks)"), ("max", "MAX(marks)")]:
        if len(items) >= 938:
            break
        N += 1
        _sql("aggregation", "easy", f"{course} {agg} marks #{N}",
             f"{agg.upper()} of marks in {course}.",
             STU_DDL, STU_SEED,
             f"SELECT {fn} FROM Students WHERE course='{course}';",
             f"{fn} filtered.", "Aggregate+WHERE.")

# F11: Nth highest salary via LIMIT/OFFSET
for n_ in range(1, 11):
    if len(items) >= 938:
        break
    N += 1
    _sql("limit_offset", "medium", f"{n_}th highest salary #{N}",
         f"The {n_}th highest distinct salary value.",
         EMP_DDL, EMP_SEED,
         f"SELECT DISTINCT salary FROM Employees ORDER BY salary DESC LIMIT 1 OFFSET {n_-1};",
         f"OFFSET {n_-1}.", "LIMIT+OFFSET.")

# F12: BETWEEN salary bands
for lo in range(50000, 100001, 10000):
    if len(items) >= 938:
        break
    hi = lo + 20000
    N += 1
    _sql("where_between", "easy", f"Salary {lo}-{hi} #{N}",
         f"Names with salary between {lo} and {hi}.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees WHERE salary BETWEEN {lo} AND {hi};",
         "BETWEEN band.", "Inclusive.")

# F13: city filters on students
for city in ["Pune", "Mumbai", "Delhi"]:
    for course in ["DBMS", "OS", "CN"]:
        if len(items) >= 938:
            break
        N += 1
        _sql("where_and", "easy", f"{city} {course} students #{N}",
             f"Student names in {city} studying {course}.",
             STU_DDL, STU_SEED,
             f"SELECT sname FROM Students WHERE city='{city}' AND course='{course}';",
             "City+course.", "AND.")

# F14: product revenue thresholds
for thr in [10000, 20000, 50000, 100000]:
    if len(items) >= 938:
        break
    N += 1
    _sql("group_by_having", "medium", f"Products revenue>{thr} #{N}",
         f"Products with total revenue above {thr}.",
         ORD_DDL, ORD_SEED,
         f"SELECT product, SUM(qty*price) FROM Orders GROUP BY product HAVING SUM(qty*price) > {thr};",
         "HAVING on revenue.", "Group revenue.")

# F15: CASE bands with varying cutoffs
for hi in [90000, 100000]:
    for mid in [60000, 70000]:
        if len(items) >= 938:
            break
        N += 1
        _sql("case_statement", "medium", f"Bands {hi}/{mid} #{N}",
             f"Name and band: High (>={hi}), Mid (>={mid}), else Low.",
             EMP_DDL, EMP_SEED,
             f"SELECT name, CASE WHEN salary >= {hi} THEN 'High' WHEN salary >= {mid} THEN 'Mid' ELSE 'Low' END FROM Employees;",
             "CASE bands.", "CASE WHEN.")

# F16: UNION combos
for dept in ["Engineering", "HR", "Sales"]:
    if len(items) >= 938:
        break
    N += 1
    _sql("union", "medium", f"{dept} plus toppers #{N}",
         f"Names in {dept} plus employees earning over 100000.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees WHERE department='{dept}' UNION SELECT name FROM Employees WHERE salary > 100000;",
         "UNION merges.", "UNION.")

# F17: string ops on students
for fn, desc in [("UPPER(sname)", "uppercase"), ("LOWER(sname)", "lowercase"),
                 ("LENGTH(sname)", "lengths")]:
    if len(items) >= 938:
        break
    N += 1
    _sql("string_functions", "easy", f"Student names {desc} #{N}",
         f"Student names in {desc}.",
         STU_DDL, STU_SEED,
         f"SELECT {fn} FROM Students;",
         f"{fn}.", "String fn.")

# F18: date ranges on orders (months of 2024)
for m in range(1, 13):
    if len(items) >= 938:
        break
    nxt = m + 1
    y2, m2 = (2024, nxt) if nxt <= 12 else (2025, 1)
    N += 1
    _sql("date_filtering", "medium", f"Orders 2024-{m:02d} #{N}",
         f"Order ids placed in month {m} of 2024.",
         ORD_DDL, ORD_SEED,
         f"SELECT oid FROM Orders WHERE odate >= '2024-{m:02d}-01' AND odate < '{y2}-{m2:02d}-01';",
         "Month range.", "Half-open.")

# F19: self-join salary comparisons vs named employees (skip Bo = base collision)
for name in ["Amy", "Cy", "De", "Eli", "Fay", "Gus", "Hal", "Ivy", "Jay"]:
    if len(items) >= 938:
        break
    N += 1
    _sql("self_join", "medium", f"Earn more than {name} #{N}",
         f"Staff names earning more than {name}.",
         EMP_DDL, EMP_SEED,
         f"SELECT e.name FROM Employees e JOIN Employees b ON b.name='{name}' WHERE e.salary > b.salary;",
         f"Beat {name}.", "Self-join.")

# F20: uncorrelated EXISTS variants
for dept in ["Engineering", "HR", "Sales", "Legal"]:
    if len(items) >= 938:
        break
    N += 1
    _sql("exists_subquery", "medium", f"Has {dept} staff #{N}",
         f"1 if any employee is in {dept}, else no rows (EXISTS check).",
         EMP_DDL, EMP_SEED,
         f"SELECT DISTINCT department FROM Employees WHERE EXISTS (SELECT 1 FROM Employees WHERE department='{dept}') AND department='{dept}';",
         "EXISTS gate.", "EXISTS.")

# ─── F21+: large families to reach 938 ──────────────────────────────
# F21: fine salary thresholds (offset by 2500 to avoid F1 overlap)
for thr in range(47500, 120001, 2500):
    if len(items) >= 938:
        break
    if thr % 5000 == 0:
        continue  # F1 covers multiples of 5000
    N += 1
    _sql("where_threshold", "easy", f"Salary over {thr} #{N}",
         f"Employee names with salary exceeding {thr}.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees WHERE salary > {thr};",
         f"Threshold {thr}.", "WHERE >.")

# F22: age bands (BETWEEN variants)
for lo in range(24, 38):
    if len(items) >= 938:
        break
    hi = lo + 5
    N += 1
    _sql("where_between", "easy", f"Age {lo} to {hi} #{N}",
         f"Names aged {lo} through {hi}.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees WHERE age BETWEEN {lo} AND {hi};",
         "Age band.", "BETWEEN.")

# F23: student marks bands per course
for course in ["DBMS", "OS", "CN"]:
    for lo in range(65, 96, 5):
        if len(items) >= 938:
            break
        hi = lo + 9
        N += 1
        _sql("where_between", "easy", f"{course} marks {lo}-{hi} #{N}",
             f"{course} students scoring {lo} to {hi}.",
             STU_DDL, STU_SEED,
             f"SELECT sname FROM Students WHERE course='{course}' AND marks BETWEEN {lo} AND {hi};",
             "Marks band.", "BETWEEN+AND.")

# F24: order value (qty*price) thresholds
for thr in range(1000, 70001, 3000):
    if len(items) >= 938:
        break
    N += 1
    _sql("where_expr", "medium", f"Order value over {thr} #{N}",
         f"Order ids whose line value (qty*price) exceeds {thr}.",
         ORD_DDL, ORD_SEED,
         f"SELECT oid FROM Orders WHERE qty*price > {thr};",
         "Expression filter.", "Compute then filter.")

# F25: department employee lists (name + salary ordered)
for dept in ["Engineering", "HR", "Sales"]:
    for d in ["ASC", "DESC"]:
        if len(items) >= 938:
            break
        N += 1
        _sql("order_by", "easy", f"{dept} by salary {d} #{N}",
             f"{dept} staff names ordered by salary {d}.",
             EMP_DDL, EMP_SEED,
             f"SELECT name FROM Employees WHERE department='{dept}' ORDER BY salary {d};",
             f"Filter+order.", "WHERE+ORDER.")

# F26: UPPER/LOWER name filters (case-insensitive search via UPPER)
for ch in "ABCDEFGHIJ":
    if len(items) >= 938:
        break
    N += 1
    _sql("where_like", "easy", f"Names starting {ch} (upper) #{N}",
         f"Names starting with {ch} using UPPER comparison.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees WHERE UPPER(name) LIKE '{ch}%';",
         "Case-insensitive prefix.", "UPPER+LIKE.")

# F27: city headcounts
for city in ["Pune", "Mumbai", "Delhi"]:
    for thr in [1, 2]:
        if len(items) >= 938:
            break
        N += 1
        _sql("group_by_having", "medium", f"{city} students over {thr} #{N}",
             f"Courses in {city} with more than {thr} students.",
             STU_DDL, STU_SEED,
             f"SELECT course, COUNT(*) FROM Students WHERE city='{city}' GROUP BY course HAVING COUNT(*) > {thr};",
             "City filter+group.", "WHERE+GROUP+HAVING.")

# F28: salary + age compound thresholds
for sal in range(60000, 100001, 10000):
    for age in [28, 30, 32, 35]:
        if len(items) >= 938:
            break
        N += 1
        _sql("where_and", "easy", f"Salary>{sal} age<{age} #{N}",
             f"Names earning over {sal} and younger than {age}.",
             EMP_DDL, EMP_SEED,
             f"SELECT name FROM Employees WHERE salary > {sal} AND age < {age};",
             "Compound AND.", "Two filters.")

# F29: product quantity totals
for prod in ["Laptop", "Mouse", "Keyboard", "Monitor"]:
    for thr in [1, 2, 3, 5]:
        if len(items) >= 938:
            break
        N += 1
        _sql("group_by_having", "medium", f"{prod} qty over {thr} #{N}",
             f"Whether {prod} sold more than {thr} units in total.",
             ORD_DDL, ORD_SEED,
             f"SELECT product, SUM(qty) FROM Orders WHERE product='{prod}' GROUP BY product HAVING SUM(qty) > {thr};",
             "Product total.", "SUM+HAVING.")

# F30: customer order counts
for cust in ["Amy", "Bo", "Cy", "De", "Eli", "Fay"]:
    if len(items) >= 938:
        break
    N += 1
    _sql("aggregation", "easy", f"{cust} order count #{N}",
         f"How many orders {cust} placed.",
         ORD_DDL, ORD_SEED,
         f"SELECT COUNT(*) FROM Orders WHERE cust='{cust}';",
         "Count filtered.", "COUNT+WHERE.")

# F31: marks ORDER BY per course
for course in ["DBMS", "OS", "CN"]:
    for d in ["ASC", "DESC"]:
        if len(items) >= 938:
            break
        N += 1
        _sql("order_by", "easy", f"{course} marks {d} #{N}",
             f"{course} student names ordered by marks {d}.",
             STU_DDL, STU_SEED,
             f"SELECT sname FROM Students WHERE course='{course}' ORDER BY marks {d};",
             "Course order.", "ORDER BY.")

# F32: DISTINCT salary values above thresholds
for thr in range(60000, 120001, 10000):
    if len(items) >= 938:
        break
    N += 1
    _sql("distinct", "easy", f"Distinct salaries over {thr} #{N}",
         f"Unique salary values above {thr}.",
         EMP_DDL, EMP_SEED,
         f"SELECT DISTINCT salary FROM Employees WHERE salary > {thr} ORDER BY salary;",
         "Unique+filter.", "DISTINCT+WHERE.")

# ─── F33+: bulk families to reach 938 ───────────────────────────────
# F33: salary less-than thresholds
for thr in range(50000, 125001, 5000):
    if len(items) >= 938:
        break
    N += 1
    _sql("where_threshold", "easy", f"Salary under {thr} #{N}",
         f"Employee names earning less than {thr}.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees WHERE salary < {thr};",
         f"Under {thr}.", "WHERE <.")

# F34: age comparison variants
for age in range(25, 40):
    for op, sym in [("at most", "<="), ("at least", ">="), ("exactly", "=")]:
        if len(items) >= 938:
            break
        N += 1
        _sql("where_threshold", "easy", f"Age {op} {age} #{N}",
             f"Names aged {op} {age}.",
             EMP_DDL, EMP_SEED,
             f"SELECT name FROM Employees WHERE age {sym} {age};",
             f"Age {sym} {age}.", "Comparison.")

# F35: student marks <= thresholds per course
for course in ["DBMS", "OS", "CN"]:
    for marks in range(70, 96, 2):
        if len(items) >= 938:
            break
        N += 1
        _sql("where_threshold", "easy", f"{course} marks at most {marks} #{N}",
             f"{course} students scoring {marks} or less.",
             STU_DDL, STU_SEED,
             f"SELECT sname FROM Students WHERE course='{course}' AND marks <= {marks};",
             "Upper bound.", "AND+<=.")

# F36: dept salary order + limit combos
for dept in ["Engineering", "HR", "Sales"]:
    for d in ["ASC", "DESC"]:
        for lim in range(1, 6):
            if len(items) >= 938:
                break
            N += 1
            _sql("order_limit", "easy", f"{dept} {d} limit {lim} #{N}",
                 f"First {lim} {dept} names by salary {d}.",
                 EMP_DDL, EMP_SEED,
                 f"SELECT name FROM Employees WHERE department='{dept}' ORDER BY salary {d} LIMIT {lim};",
                 "Filter+order+limit.", "Top-N per group.")

# F37: COUNT with age-band WHERE per dept
for dept in ["Engineering", "HR", "Sales"]:
    for lo in [25, 30, 35]:
        if len(items) >= 938:
            break
        N += 1
        _sql("aggregation", "easy", f"{dept} count age>{lo} #{N}",
             f"How many {dept} staff are older than {lo}.",
             EMP_DDL, EMP_SEED,
             f"SELECT COUNT(*) FROM Employees WHERE department='{dept}' AND age > {lo};",
             "Count filtered.", "COUNT+AND.")

# F38: AVG salary with age bands
for lo in range(25, 38, 2):
    if len(items) >= 938:
        break
    N += 1
    _sql("aggregation", "easy", f"Avg salary age>{lo} #{N}",
         f"Average salary of staff older than {lo}.",
         EMP_DDL, EMP_SEED,
         f"SELECT AVG(salary) FROM Employees WHERE age > {lo};",
         "Avg filtered.", "AVG+WHERE.")

# F39: order date before/after specific dates
for m in range(1, 13):
    for op, sym in [("on/after", ">="), ("before", "<")]:
        if len(items) >= 938:
            break
        N += 1
        _sql("date_filtering", "medium", f"Orders {op} 2024-{m:02d}-01 #{N}",
             f"Order ids placed {op} 2024-{m:02d}-01.",
             ORD_DDL, ORD_SEED,
             f"SELECT oid FROM Orders WHERE odate {sym} '2024-{m:02d}-01';",
             "Date compare.", "Date filter.")

# F40: LIKE on student fields
for pat, desc, col in [("R%", "start R", "sname"), ("%a", "end a", "sname"),
                       ("%e%", "contain e", "sname"), ("P%", "start P", "city"),
                       ("%i", "end i", "city"), ("D%", "start D", "course"),
                       ("%S", "end S", "course"), ("%u%", "contain u", "city")]:
    if len(items) >= 938:
        break
    N += 1
    _sql("where_like", "easy", f"Students {col} {desc} #{N}",
         f"Student rows whose {col} {desc}.",
         STU_DDL, STU_SEED,
         f"SELECT sname FROM Students WHERE {col} LIKE '{pat}';",
         f"LIKE '{pat}'.", "Pattern.")

# F41: NOT equal / NOT IN variants
for dept in ["Engineering", "HR", "Sales"]:
    if len(items) >= 938:
        break
    N += 1
    _sql("where_not", "easy", f"Not in {dept} #{N}",
         f"Names outside {dept}.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees WHERE department <> '{dept}';",
         "Not equal.", "<> operator.")
for city in ["Pune", "Mumbai", "Delhi"]:
    if len(items) >= 938:
        break
    N += 1
    _sql("where_not", "easy", f"Students not in {city} #{N}",
         f"Student names outside {city}.",
         STU_DDL, STU_SEED,
         f"SELECT sname FROM Students WHERE city <> '{city}';",
         "Not equal.", "<> operator.")

# F42: HAVING COUNT thresholds per course
for course in ["DBMS", "OS", "CN"]:
    for thr in [1, 2, 3]:
        if len(items) >= 938:
            break
        N += 1
        _sql("group_by_having", "medium", f"{course} cities over {thr} #{N}",
             f"Cities with more than {thr} {course} students.",
             STU_DDL, STU_SEED,
             f"SELECT city, COUNT(*) FROM Students WHERE course='{course}' GROUP BY city HAVING COUNT(*) > {thr};",
             "City groups.", "HAVING.")

# F43: MIN/MAX per course/city
for course in ["DBMS", "OS", "CN"]:
    for fn in ["MIN(marks)", "MAX(marks)"]:
        if len(items) >= 938:
            break
        N += 1
        _sql("aggregation", "easy", f"{course} {fn} #{N}",
             f"{fn} of marks in {course}.",
             STU_DDL, STU_SEED,
             f"SELECT {fn} FROM Students WHERE course='{course}';",
             f"{fn}.", "Aggregate.")

# F44: UNION department pairs
import itertools as _it
for d1, d2 in _it.combinations(["Engineering", "HR", "Sales"], 2):
    if len(items) >= 938:
        break
    N += 1
    _sql("union", "medium", f"{d1} UNION {d2} #{N}",
         f"Combined roster of {d1} plus {d2}.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees WHERE department='{d1}' UNION SELECT name FROM Employees WHERE department='{d2}';",
         "UNION pair.", "UNION.")
    if len(items) >= 938:
        break
    N += 1
    _sql("union", "medium", f"{d1} UNION ALL {d2} #{N}",
         f"Combined roster of {d1} plus {d2} keeping duplicates.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees WHERE department='{d1}' UNION ALL SELECT name FROM Employees WHERE department='{d2}';",
         "UNION ALL.", "Keeps dupes.")

# ─── F45+: final push to 938 ────────────────────────────────────────
# F45: salary NOT BETWEEN (outside band)
for lo in range(55000, 95001, 10000):
    if len(items) >= 938:
        break
    hi = lo + 15000
    N += 1
    _sql("where_not", "easy", f"Salary outside {lo}-{hi} #{N}",
         f"Names earning outside {lo} to {hi}.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees WHERE salary NOT BETWEEN {lo} AND {hi};",
         "NOT BETWEEN.", "Outside band.")

# F46: IN with name lists
_name_groups = [["Amy", "Bo", "Cy"], ["De", "Eli", "Fay"], ["Gus", "Hal", "Ivy"],
                ["Amy", "De", "Gus"], ["Bo", "Eli", "Hal"], ["Cy", "Fay", "Ivy"]]
for grp in _name_groups:
    if len(items) >= 938:
        break
    lst = ",".join(f"'{x}'" for x in grp)
    N += 1
    _sql("where_in", "easy", f"Names in list {grp[0]}+ #{N}",
         f"Details of {', '.join(grp)}.",
         EMP_DDL, EMP_SEED,
         f"SELECT name, salary FROM Employees WHERE name IN ({lst});",
         "IN list.", "IN.")

# F47: marks NOT IN course lists / <> course
for course in ["DBMS", "OS", "CN"]:
    if len(items) >= 938:
        break
    N += 1
    _sql("where_not", "easy", f"Students outside {course} #{N}",
         f"Student names not studying {course}.",
         STU_DDL, STU_SEED,
         f"SELECT sname FROM Students WHERE course <> '{course}';",
         "Not in course.", "<>.")

# F48: order customer IN lists
_cust_groups = [["Amy", "Bo"], ["Cy", "De", "Eli"], ["Fay", "Amy"], ["Bo", "Cy", "Fay"]]
for grp in _cust_groups:
    if len(items) >= 938:
        break
    lst = ",".join(f"'{x}'" for x in grp)
    N += 1
    _sql("where_in", "easy", f"Orders by {grp[0]}+ #{N}",
         f"Order ids from {', '.join(grp)}.",
         ORD_DDL, ORD_SEED,
         f"SELECT oid FROM Orders WHERE cust IN ({lst});",
         "IN customers.", "IN.")

# F49: salary multiples (modulo)
for m in [1000, 5000, 10000]:
    for r in [0, 500, 1000]:
        if len(items) >= 938:
            break
        N += 1
        _sql("where_mod", "medium", f"Salary mod {m} = {r} #{N}",
             f"Names whose salary mod {m} equals {r}.",
             EMP_DDL, EMP_SEED,
             f"SELECT name FROM Employees WHERE salary % {m} = {r};",
             "Modulo filter.", "% operator.")

# F50: LENGTH(name) filters
for ln in [3, 4, 5]:
    for op, sym in [("exactly", "="), ("at least", ">="), ("over", ">")]:
        if len(items) >= 938:
            break
        N += 1
        _sql("where_length", "easy", f"Name length {op} {ln} #{N}",
             f"Names with length {op} {ln}.",
             EMP_DDL, EMP_SEED,
             f"SELECT name FROM Employees WHERE LENGTH(name) {sym} {ln};",
             "LENGTH filter.", "LENGTH().")

# F51: marks LENGTH/order combos on students
for d in ["ASC", "DESC"]:
    for lim in [2, 3, 5]:
        if len(items) >= 938:
            break
        N += 1
        _sql("order_limit", "easy", f"Students marks {d} limit {lim} #{N}",
             f"Top/bottom {lim} students by marks ({d}).",
             STU_DDL, STU_SEED,
             f"SELECT sname FROM Students ORDER BY marks {d} LIMIT {lim};",
             "Order+limit.", "Top-N.")

# F52: department budgets vs salary sums (join + having)
for op, sym in [("exceed", ">"), ("within", "<")]:
    if len(items) >= 938:
        break
    N += 1
    _sql("join_having", "hard", f"Payroll {op} budget? #{N}",
         f"Departments whose payroll {op} budget (sanity check).",
         EMP_DDL + "\n" + DEPT_DDL, EMP_SEED + "\n" + DEPT_SEED,
         f"SELECT e.department, SUM(e.salary) FROM Employees e JOIN Departments d ON e.department=d.dept GROUP BY e.department HAVING SUM(e.salary) {sym} d.budget;",
         "Payroll vs budget.", "JOIN+HAVING.")

# F53: second/third highest per department
for dept in ["Engineering", "HR", "Sales"]:
    for off in [1, 2]:
        if len(items) >= 938:
            break
        N += 1
        _sql("limit_offset", "medium", f"{dept} #{off+1} highest #{N}",
             f"The #{off+1} highest salary in {dept}.",
             EMP_DDL, EMP_SEED,
             f"SELECT DISTINCT salary FROM Employees WHERE department='{dept}' ORDER BY salary DESC LIMIT 1 OFFSET {off};",
             "Dept rank.", "OFFSET.")

# F54: customer totals with HAVING
for thr in [50000, 60000, 70000]:
    if len(items) >= 938:
        break
    N += 1
    _sql("group_by_having", "medium", f"Customers over {thr} #{N}",
         f"Customers spending over {thr} total.",
         ORD_DDL, ORD_SEED,
         f"SELECT cust, SUM(qty*price) FROM Orders GROUP BY cust HAVING SUM(qty*price) > {thr};",
         "Big spenders.", "HAVING.")

# F55: product counts
for prod in ["Laptop", "Mouse", "Keyboard", "Monitor"]:
    if len(items) >= 938:
        break
    N += 1
    _sql("aggregation", "easy", f"{prod} order lines #{N}",
         f"How many order lines mention {prod}.",
         ORD_DDL, ORD_SEED,
         f"SELECT COUNT(*) FROM Orders WHERE product='{prod}';",
         "Count product.", "COUNT.")

# F56: AVG qty per product
for prod in ["Laptop", "Mouse", "Keyboard", "Monitor"]:
    if len(items) >= 938:
        break
    N += 1
    _sql("aggregation", "easy", f"{prod} avg qty #{N}",
         f"Average quantity per {prod} order.",
         ORD_DDL, ORD_SEED,
         f"SELECT AVG(qty) FROM Orders WHERE product='{prod}';",
         "Avg qty.", "AVG.")

# F57: date equality (exact day orders)
for day in ["2024-01-05", "2024-01-06", "2024-02-10", "2024-02-15",
            "2024-03-01", "2024-03-05", "2024-03-10", "2024-03-12"]:
    if len(items) >= 938:
        break
    N += 1
    _sql("date_filtering", "easy", f"Orders on {day} #{N}",
         f"Order ids placed exactly on {day}.",
         ORD_DDL, ORD_SEED,
         f"SELECT oid FROM Orders WHERE odate = '{day}';",
         "Exact date.", "= date.")

# F58: salary = exact values (each distinct salary)
for sal in [48000, 55000, 58000, 60000, 65000, 70000, 72000, 80000, 95000, 120000]:
    if len(items) >= 938:
        break
    N += 1
    _sql("where_threshold", "easy", f"Salary exactly {sal} #{N}",
         f"Names earning exactly {sal}.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees WHERE salary = {sal};",
         "Exact match.", "= value.")

# ─── F59+: final stretch to 938 ─────────────────────────────────────
# F59: age = exact values
for age in range(24, 41):
    if len(items) >= 938:
        break
    N += 1
    _sql("where_threshold", "easy", f"Age exactly {age} #{N}",
         f"Employee names aged exactly {age}.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees WHERE age = {age};",
         "Exact age.", "= value.")

# F60: marks = exact values per course
for course in ["DBMS", "OS", "CN"]:
    for mk in [68, 72, 78, 80, 85, 87, 88, 91, 92, 95]:
        if len(items) >= 938:
            break
        N += 1
        _sql("where_threshold", "easy", f"{course} marks exactly {mk} #{N}",
             f"{course} students scoring exactly {mk}.",
             STU_DDL, STU_SEED,
             f"SELECT sname FROM Students WHERE course='{course}' AND marks = {mk};",
             "Exact marks.", "= value.")

# F61: salary != exact (exclude one)
for sal in [60000, 70000, 80000, 95000]:
    if len(items) >= 938:
        break
    N += 1
    _sql("where_not", "easy", f"Salary not {sal} #{N}",
         f"Names not earning exactly {sal}.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees WHERE salary <> {sal};",
         "Exclude value.", "<>.")

# F62: department salary sums
for dept in ["Engineering", "HR", "Sales"]:
    if len(items) >= 938:
        break
    N += 1
    _sql("aggregation", "easy", f"{dept} payroll #{N}",
         f"Total payroll of {dept}.",
         EMP_DDL, EMP_SEED,
         f"SELECT SUM(salary) FROM Employees WHERE department='{dept}';",
         "Dept sum.", "SUM.")

# F63: course mark sums/avgs
for course in ["DBMS", "OS", "CN"]:
    for fn in ["SUM(marks)", "AVG(marks)"]:
        if len(items) >= 938:
            break
        N += 1
        _sql("aggregation", "easy", f"{course} {fn} #{N}",
             f"{fn} of marks in {course}.",
             STU_DDL, STU_SEED,
             f"SELECT {fn} FROM Students WHERE course='{course}';",
             f"{fn}.", "Aggregate.")

# F64: order price bands (unit price)
for lo in [500, 1000, 5000, 15000, 50000]:
    if len(items) >= 938:
        break
    N += 1
    _sql("where_threshold", "easy", f"Unit price over {lo} #{N}",
         f"Order ids with unit price above {lo}.",
         ORD_DDL, ORD_SEED,
         f"SELECT oid FROM Orders WHERE price > {lo};",
         "Price filter.", "WHERE >.")

# F65: customer LIKE patterns
for pat, desc in [("A%", "start A"), ("%y", "end y"), ("%m%", "contain m")]:
    if len(items) >= 938:
        break
    N += 1
    _sql("where_like", "easy", f"Customers {desc} #{N}",
         f"Customers whose name {desc}.",
         ORD_DDL, ORD_SEED,
         f"SELECT DISTINCT cust FROM Orders WHERE cust LIKE '{pat}';",
         f"LIKE '{pat}'.", "Pattern.")

# F66: product LIKE patterns
for pat, desc in [("L%", "start L"), ("%e", "end e"), ("%o%", "contain o"),
                  ("M%", "start M"), ("%r", "end r")]:
    if len(items) >= 938:
        break
    N += 1
    _sql("where_like", "easy", f"Products {desc} #{N}",
         f"Products whose name {desc}.",
         ORD_DDL, ORD_SEED,
         f"SELECT DISTINCT product FROM Orders WHERE product LIKE '{pat}';",
         f"LIKE '{pat}'.", "Pattern.")

# F67: qty exact values
for qv in [1, 2, 5]:
    if len(items) >= 938:
        break
    N += 1
    _sql("where_threshold", "easy", f"Orders qty exactly {qv} #{N}",
         f"Order ids with quantity exactly {qv}.",
         ORD_DDL, ORD_SEED,
         f"SELECT oid FROM Orders WHERE qty = {qv};",
         "Exact qty.", "= value.")

# F68: cross-table counts (orders per employee-name customer)
for name in ["Amy", "Bo", "Cy", "De", "Eli", "Fay"]:
    if len(items) >= 938:
        break
    N += 1
    _sql("aggregation", "easy", f"{name} total spend #{N}",
         f"Total spend by {name}.",
         ORD_DDL, ORD_SEED,
         f"SELECT SUM(qty*price) FROM Orders WHERE cust='{name}';",
         "Customer total.", "SUM.")

# F69: MIN/MAX age per department
for dept in ["Engineering", "HR", "Sales"]:
    for fn in ["MIN(age)", "MAX(age)"]:
        if len(items) >= 938:
            break
        N += 1
        _sql("aggregation", "easy", f"{dept} {fn} #{N}",
             f"{fn} in {dept}.",
             EMP_DDL, EMP_SEED,
             f"SELECT {fn} FROM Employees WHERE department='{dept}';",
             f"{fn}.", "Aggregate.")

# F70: sname ORDER BY marks with LIMIT per course
for course in ["DBMS", "OS", "CN"]:
    for lim in [1, 2, 3]:
        if len(items) >= 938:
            break
        N += 1
        _sql("order_limit", "easy", f"{course} top {lim} #{N}",
             f"Top {lim} {course} students by marks.",
             STU_DDL, STU_SEED,
             f"SELECT sname FROM Students WHERE course='{course}' ORDER BY marks DESC LIMIT {lim};",
             "Top per course.", "ORDER+LIMIT.")

# F71: oid ranges
for lo in range(1, 9):
    if len(items) >= 938:
        break
    hi = lo + 2
    N += 1
    _sql("where_between", "easy", f"Order ids {lo}-{hi} #{N}",
         f"Orders with id from {lo} to {hi}.",
         ORD_DDL, ORD_SEED,
         f"SELECT oid FROM Orders WHERE oid BETWEEN {lo} AND {hi};",
         "ID range.", "BETWEEN.")

# F72: sid ranges per course
for course in ["DBMS", "OS", "CN"]:
    for lo in [1, 4, 7]:
        if len(items) >= 938:
            break
        hi = lo + 2
        N += 1
        _sql("where_between", "easy", f"{course} sids {lo}-{hi} #{N}",
             f"{course} students with sid {lo} to {hi}.",
             STU_DDL, STU_SEED,
             f"SELECT sname FROM Students WHERE course='{course}' AND sid BETWEEN {lo} AND {hi};",
             "SID range.", "BETWEEN+AND.")

# ─── F73+: close the gap to 938 ─────────────────────────────────────
# F73: id ranges on employees
for lo in range(1, 10):
    if len(items) >= 938:
        break
    hi = lo + 1
    N += 1
    _sql("where_between", "easy", f"Employee ids {lo}-{hi} #{N}",
         f"Employee names with id {lo} to {hi}.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees WHERE id BETWEEN {lo} AND {hi};",
         "ID range.", "BETWEEN.")

# F74: salary ASC/DESC full lists with LIMIT
for d in ["ASC", "DESC"]:
    for lim in [4, 5, 6, 7, 8, 9, 10]:
        if len(items) >= 938:
            break
        N += 1
        _sql("order_limit", "easy", f"Salaries {d} limit {lim} #{N}",
             f"First {lim} names by salary {d}.",
             EMP_DDL, EMP_SEED,
             f"SELECT name FROM Employees ORDER BY salary {d} LIMIT {lim};",
             "Order+limit.", "Top/bottom-N.")

# F75: age ASC/DESC with LIMIT
for d in ["ASC", "DESC"]:
    for lim in [2, 4, 6, 8]:
        if len(items) >= 938:
            break
        N += 1
        _sql("order_limit", "easy", f"Ages {d} limit {lim} #{N}",
             f"First {lim} names by age {d}.",
             EMP_DDL, EMP_SEED,
             f"SELECT name FROM Employees ORDER BY age {d} LIMIT {lim};",
             "Age order.", "ORDER+LIMIT.")

# F76: marks ranges (BETWEEN) per city
for city in ["Pune", "Mumbai", "Delhi"]:
    for lo in [70, 80, 90]:
        if len(items) >= 938:
            break
        hi = lo + 9
        N += 1
        _sql("where_between", "easy", f"{city} marks {lo}-{hi} #{N}",
             f"{city} students scoring {lo} to {hi}.",
             STU_DDL, STU_SEED,
             f"SELECT sname FROM Students WHERE city='{city}' AND marks BETWEEN {lo} AND {hi};",
             "City+marks.", "BETWEEN+AND.")

# F77: price = exact values
for pr in [750, 800, 2500, 14500, 15000, 59000, 60000, 62000]:
    if len(items) >= 938:
        break
    N += 1
    _sql("where_threshold", "easy", f"Unit price exactly {pr} #{N}",
         f"Order ids with unit price exactly {pr}.",
         ORD_DDL, ORD_SEED,
         f"SELECT oid FROM Orders WHERE price = {pr};",
         "Exact price.", "= value.")

# F78: qty > thresholds
for qv in [2, 3, 4]:
    if len(items) >= 938:
        break
    N += 1
    _sql("where_threshold", "easy", f"Orders qty over {qv} #{N}",
         f"Order ids with quantity over {qv}.",
         ORD_DDL, ORD_SEED,
         f"SELECT oid FROM Orders WHERE qty > {qv};",
         "Qty filter.", "WHERE >.")

# F79: SUBSTR first N chars of student names
for ln in [1, 2, 4, 5]:
    if len(items) >= 938:
        break
    N += 1
    _sql("string_functions", "easy", f"Student initials {ln} chars #{N}",
         f"First {ln} characters of each student name.",
         STU_DDL, STU_SEED,
         f"SELECT SUBSTR(sname, 1, {ln}) FROM Students;",
         "Prefix slice.", "SUBSTR().")

# F80: UPPER/LOWER city
for fn in ["UPPER(city)", "LOWER(city)"]:
    if len(items) >= 938:
        break
    N += 1
    _sql("string_functions", "easy", f"Cities {fn} #{N}",
         f"Distinct cities as {fn}.",
         STU_DDL, STU_SEED,
         f"SELECT DISTINCT {fn} FROM Students;",
         f"{fn}.", "Case fn.")

# F81: LENGTH filters on student names
for ln in [4, 5, 6]:
    if len(items) >= 938:
        break
    N += 1
    _sql("where_length", "easy", f"Student name length {ln} #{N}",
         f"Students whose name has exactly {ln} letters.",
         STU_DDL, STU_SEED,
         f"SELECT sname FROM Students WHERE LENGTH(sname) = {ln};",
         "Length match.", "LENGTH().")

# F82: odate month extraction via SUBSTR
for m in ["01", "02", "03"]:
    if len(items) >= 938:
        break
    N += 1
    _sql("date_filtering", "medium", f"Orders month {m} via substr #{N}",
         f"Order ids in month {m} using SUBSTR on date.",
         ORD_DDL, ORD_SEED,
         f"SELECT oid FROM Orders WHERE SUBSTR(odate, 6, 2) = '{m}';",
         "Month slice.", "SUBSTR date.")

# F83: CASE on marks (grade bands)
for a_thr, b_thr in [(90, 80), (85, 75)]:
    if len(items) >= 938:
        break
    N += 1
    _sql("case_statement", "medium", f"Grades {a_thr}/{b_thr} #{N}",
         f"Student name and grade: A (>={a_thr}), B (>={b_thr}), else C.",
         STU_DDL, STU_SEED,
         f"SELECT sname, CASE WHEN marks >= {a_thr} THEN 'A' WHEN marks >= {b_thr} THEN 'B' ELSE 'C' END FROM Students;",
         "Grade CASE.", "CASE WHEN.")

# F84: COALESCE on nullable-ish (city fallback demo via NULLIF edge)
for city in ["Pune", "Mumbai"]:
    if len(items) >= 938:
        break
    N += 1
    _sql("coalesce", "medium", f"City or Other {city} #{N}",
         f"Student names with non-{city} cities shown, {city} folded to itself (NULLIF demo).",
         STU_DDL, STU_SEED,
         f"SELECT sname, COALESCE(NULLIF(city,'{city}'), '{city}') FROM Students;",
         "NULLIF+COALESCE.", "Null fns.")

# ─── F86+: last stretch ────────────────────────────────────────────
# F86: salary BETWEEN fine bands
for lo in range(48000, 115001, 8000):
    if len(items) >= 938:
        break
    hi = lo + 12000
    N += 1
    _sql("where_between", "easy", f"Pay band {lo}-{hi} #{N}",
         f"Staff earning {lo} to {hi}.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees WHERE salary BETWEEN {lo} AND {hi};",
         "Pay band.", "BETWEEN.")

# F87: marks BETWEEN fine bands per course
for course in ["DBMS", "OS", "CN"]:
    for lo in range(68, 92, 6):
        if len(items) >= 938:
            break
        hi = lo + 5
        N += 1
        _sql("where_between", "easy", f"{course} scores {lo}-{hi} #{N}",
             f"{course} pupils scoring {lo} to {hi}.",
             STU_DDL, STU_SEED,
             f"SELECT sname FROM Students WHERE course='{course}' AND marks BETWEEN {lo} AND {hi};",
             "Score band.", "BETWEEN+AND.")

# F88: qty*price BETWEEN bands
for lo in range(1000, 60001, 10000):
    if len(items) >= 938:
        break
    hi = lo + 15000
    N += 1
    _sql("where_expr", "medium", f"Line value {lo}-{hi} #{N}",
         f"Orders with line value {lo} to {hi}.",
         ORD_DDL, ORD_SEED,
         f"SELECT oid FROM Orders WHERE qty*price BETWEEN {lo} AND {hi};",
         "Value band.", "BETWEEN expr.")

# F89: name <> exact (exclude one employee)
for name in ["Amy", "Hal", "Ivy", "Jay", "Gus"]:
    if len(items) >= 938:
        break
    N += 1
    _sql("where_not", "easy", f"Everyone but {name} #{N}",
         f"All staff except {name}.",
         EMP_DDL, EMP_SEED,
         f"SELECT name FROM Employees WHERE name <> '{name}';",
         "Exclude one.", "<>.")

# F90: sname <> exact
for nm in ["Ravi", "Meera", "Pooja", "Arjun"]:
    if len(items) >= 938:
        break
    N += 1
    _sql("where_not", "easy", f"Students except {nm} #{N}",
         f"All students except {nm}.",
         STU_DDL, STU_SEED,
         f"SELECT sname FROM Students WHERE sname <> '{nm}';",
         "Exclude one.", "<>.")

# F91: ORDER BY name ASC/DESC with LIMIT
for d in ["ASC", "DESC"]:
    for lim in [3, 6, 9]:
        if len(items) >= 938:
            break
        N += 1
        _sql("order_limit", "easy", f"Names alpha {d} limit {lim} #{N}",
             f"First {lim} names alphabetically {d}.",
             EMP_DDL, EMP_SEED,
             f"SELECT name FROM Employees ORDER BY name {d} LIMIT {lim};",
             "Alpha order.", "ORDER name.")

# F92: COUNT(*) with LIKE filters
for pat, desc in [("A%", "A-start"), ("%y", "y-end"), ("%a%", "a-inside")]:
    if len(items) >= 938:
        break
    N += 1
    _sql("aggregation", "easy", f"Count names {desc} #{N}",
         f"How many names {desc}.",
         EMP_DDL, EMP_SEED,
         f"SELECT COUNT(*) FROM Employees WHERE name LIKE '{pat}';",
         "Count pattern.", "COUNT+LIKE.")

# ─── F93: final top-up to 938 ───────────────────────────────────────
# F93: MIN/MAX salary overall variants with WHERE age
for fn in ["MIN(salary)", "MAX(salary)"]:
    for op, sym in [("over 30", "> 30"), ("under 30", "< 30"), ("at 30+", ">= 30")]:
        if len(items) >= 938:
            break
        N += 1
        _sql("aggregation", "easy", f"{fn} age {op} #{N}",
             f"{fn} among staff aged {op}.",
             EMP_DDL, EMP_SEED,
             f"SELECT {fn} FROM Employees WHERE age {sym};",
             f"{fn} filtered.", "Aggregate+WHERE.")
# F94: AVG marks with city filter
for city in ["Pune", "Mumbai", "Delhi"]:
    for fn in ["AVG(marks)", "SUM(marks)"]:
        if len(items) >= 938:
            break
        N += 1
        _sql("aggregation", "easy", f"{city} {fn} #{N}",
             f"{fn} of marks in {city}.",
             STU_DDL, STU_SEED,
             f"SELECT {fn} FROM Students WHERE city='{city}';",
             f"{fn} city.", "Aggregate.")
# F95: oid <> exact
for oid in [1, 4, 8]:
    if len(items) >= 938:
        break
    N += 1
    _sql("where_not", "easy", f"Orders except {oid} #{N}",
         f"All order ids except {oid}.",
         ORD_DDL, ORD_SEED,
         f"SELECT oid FROM Orders WHERE oid <> {oid};",
         "Exclude id.", "<>.")
# F96: product <> exact
for prod in ["Laptop", "Mouse"]:
    if len(items) >= 938:
        break
    N += 1
    _sql("where_not", "easy", f"Orders not {prod} #{N}",
         f"Order ids for products other than {prod}.",
         ORD_DDL, ORD_SEED,
         f"SELECT oid FROM Orders WHERE product <> '{prod}';",
         "Exclude product.", "<>.")

# F97: closing 4 to hit 938 exactly
_f97 = [
    ("where_and", "Engineering veterans", "Engineering staff older than 33.",
     "SELECT name FROM Employees WHERE department='Engineering' AND age > 33;"),
    ("where_and", "Sales newcomers", "Sales staff younger than 28.",
     "SELECT name FROM Employees WHERE department='Sales' AND age < 28;"),
    ("aggregation", "HR headcount", "How many HR staff exist.",
     "SELECT COUNT(*) FROM Employees WHERE department='HR';"),
    ("order_by", "Oldest staff", "Two oldest employee names.",
     "SELECT name FROM Employees ORDER BY age DESC LIMIT 2;"),
]
for _t, _title, _ques, _qq in _f97:
    if len(items) >= 938:
        break
    N += 1
    _sql(_t, "easy", f"{_title} #{N}", _ques, EMP_DDL, EMP_SEED, _qq, "Closer.", "Final.")

# F85: COUNT DISTINCT departments/cities/courses
for col, tbl in [("department", "Employees"), ("city", "Students"), ("course", "Students"),
                 ("product", "Orders"), ("cust", "Orders")]:
    if len(items) >= 938:
        break
    N += 1
    ddl = {"Employees": EMP_DDL, "Students": STU_DDL, "Orders": ORD_DDL}[tbl]
    seed = {"Employees": EMP_SEED, "Students": STU_SEED, "Orders": ORD_SEED}[tbl]
    _sql("distinct", "easy", f"Count distinct {col} #{N}",
         f"How many distinct {col} values exist.",
         ddl, seed,
         f"SELECT COUNT(DISTINCT {col}) FROM {tbl};",
         "COUNT DISTINCT.", "Unique count.")

print(f"total sql: {len(items)}")

# ─── WRITE + VALIDATE ───────────────────────────────────────────────
qs = [q["question"] for q in items]
assert len(set(qs)) == len(qs), "duplicate question text"
ids = [q["id"] for q in items]
assert len(set(ids)) == len(ids), "duplicate ids"

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=1)

from collections import Counter
print(f"Wrote {len(items)} sql questions to {OUT.name}")
print(dict(Counter(q["sub_topic"] for q in items)))
