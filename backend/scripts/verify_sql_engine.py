"""Runtime verification script for sql_engine."""
import sys
sys.path.insert(0, ".")
from app.services.sql_engine import SQLEngine

# Test 1: Simple SELECT with WHERE
schema = """
CREATE TABLE Employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary INTEGER
);
"""
seed = """
INSERT INTO Employees VALUES (1, 'Alice', 'Engineering', 70000);
INSERT INTO Employees VALUES (2, 'Bob', 'HR', 50000);
INSERT INTO Employees VALUES (3, 'Charlie', 'Engineering', 55000);
"""
expected = "SELECT name FROM Employees WHERE department = 'Engineering' AND salary > 60000;"
student = "SELECT name FROM Employees WHERE department = 'Engineering' AND salary > 60000;"

result = SQLEngine.verify_query(schema, seed, expected, student, enforce_order=False)
print(f"Test 1 (exact match): correct={result.is_correct}, time={result.execution_time_ms:.2f}ms")
if not result.is_correct:
    print(f"  Error: {result.error_message}")

# Test 2: Wrong answer
student_wrong = "SELECT name FROM Employees WHERE department = 'Engineering' OR salary > 60000;"
result2 = SQLEngine.verify_query(schema, seed, expected, student_wrong, enforce_order=False)
print(f"Test 2 (wrong answer): correct={result2.is_correct}, error={result2.error_message}")

# Test 3: Aggregate query
schema3 = """
CREATE TABLE Sales (
    id INTEGER PRIMARY KEY,
    product TEXT,
    amount INTEGER,
    region TEXT
);
"""
seed3 = """
INSERT INTO Sales VALUES (1, 'A', 100, 'North');
INSERT INTO Sales VALUES (2, 'B', 200, 'South');
INSERT INTO Sales VALUES (3, 'A', 150, 'North');
"""
expected3 = "SELECT product, SUM(amount) as total FROM Sales GROUP BY product;"
student3 = "SELECT product, SUM(amount) as total FROM Sales GROUP BY product;"
result3 = SQLEngine.verify_query(schema3, seed3, expected3, student3, enforce_order=False)
print(f"Test 3 (aggregate): correct={result3.is_correct}, time={result3.execution_time_ms:.2f}ms")

# Test 4: Golden query error propagation
result4 = SQLEngine.verify_query(schema, seed, "SELECT * FROM nonexistent;", student, enforce_order=False)
print(f"Test 4 (bad schema): correct={result4.is_correct}, error={result4.error_message}")

print("\nSQL engine runtime verification complete.")
