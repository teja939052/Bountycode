"""
SQL/Database Track — 40 Levels
Built on coddy.tech methodology: build something with EVERY lesson,
short daily lessons, instant feedback, AI tutor hints, gamified streaks.
Focus: relational databases, queries, joins, indexing, transactions.
"""

from .curriculum_base import _L, _bonus_lessons, LEVEL_THEMES

SQL_LEVELS = [
    # Level 1: First Steps 🌱
    {"id": "l01", "difficulty": 1, "name": "First Steps", "lessons": [
        _L("What is SQL?", 10, 1), _L("SELECT Statement", 10, 1, "practice"),
        _L("SELECT DISTINCT", 10, 1), _L("WHERE Clause", 10, 1),
        _L("AND / OR / NOT Operators", 15, 2), _L("Practice: Basic Queries", 15, 1, "practice"),
        _L("Challenge: Employee Lookup", 25, 2, "challenge"),
        _L("Project: Library Catalog Query Tool", 60, 3, "project",
           "A SQL query tool for searching a library catalog with SELECT, WHERE, and DISTINCT."),
    ]},
    # Level 2: Ordering & Limiting 📊
    {"id": "l02", "difficulty": 1, "name": "Ordering & Limiting", "lessons": [
        _L("ORDER BY", 10, 1), _L("ASC & DESC", 10, 1),
        _L("LIMIT & OFFSET", 15, 1), _L("FETCH & OFFSET (SQL Standard)", 15, 2),
        _L("TOP (SQL Server)", 10, 1), _L("ROWNUM (Oracle)", 10, 1),
        _L("Practice: Sorted Results", 20, 2, "practice"),
        _L("Challenge: Top N Products", 25, 2, "challenge"),
        _L("Project: Leaderboard System", 60, 3, "project",
           "A leaderboard system using ORDER BY, LIMIT, and pagination for game scores."),
    ]},
    # Level 3: Functions & Expressions 🔢
    {"id": "l03", "difficulty": 2, "name": "Functions & Expressions", "lessons": [
        _L("Aggregate Functions: COUNT, SUM, AVG", 10, 1), _L("MIN & MAX", 10, 1),
        _L("String Functions: UPPER, LOWER, LENGTH", 15, 2), _L("Date Functions: NOW, CURDATE", 15, 2),
        _L("Math Functions: ROUND, CEIL, FLOOR", 15, 2), _L("COALESCE & NULLIF", 15, 2),
        _L("Practice: Aggregation Queries", 20, 2, "practice"),
        _L("Challenge: Sales Summary Report", 30, 3, "challenge"),
        _L("Project: Sales Analytics Dashboard", 60, 3, "project",
           "A sales analytics dashboard using aggregate functions, date functions, and COALESCE."),
    ]},
    # Level 4: Grouping & HAVING 📈
    {"id": "l04", "difficulty": 2, "name": "Grouping & HAVING", "lessons": [
        _L("GROUP BY", 10, 1), _L("HAVING vs WHERE", 15, 2),
        _L("GROUP BY Multiple Columns", 15, 2), _L("ROLLUP & CUBE", 20, 3),
        _L("GROUPING SETS", 20, 3), _L("Window Functions: ROW_NUMBER", 20, 3),
        _L("Practice: Grouped Reports", 20, 2, "practice"),
        _L("Challenge: Department Salary Analysis", 35, 3, "challenge"),
        _L("Project: Department Performance Report", 60, 3, "project",
           "A department performance report using GROUP BY, HAVING, and window functions."),
    ]},
    # Level 5: Joins 🔗
    {"id": "l05", "difficulty": 2, "name": "Joins", "lessons": [
        _L("INNER JOIN", 10, 1), _L("LEFT JOIN", 10, 1),
        _L("RIGHT JOIN", 10, 1), _L("FULL OUTER JOIN", 15, 2),
        _L("CROSS JOIN", 15, 2), _L("Self Join", 15, 2),
        _L("Practice: Multi-Table Queries", 20, 2, "practice"),
        _L("Challenge: Complex Join Chain", 35, 3, "challenge"),
        _L("Project: E-commerce Order System", 60, 3, "project",
           "An e-commerce order system using INNER, LEFT, RIGHT, and FULL OUTER joins."),
    ]},
    # Level 6: Subqueries & CTEs 🔄
    {"id": "l06", "difficulty": 3, "name": "Subqueries & CTEs", "lessons": [
        _L("Subquery in WHERE Clause", 10, 1), _L("Subquery in SELECT Clause", 10, 1),
        _L("Subquery in FROM Clause", 15, 2), _L("Correlated Subqueries", 20, 3),
        _L("CTE (Common Table Expression)", 20, 2), _L("Recursive CTE", 25, 3),
        _L("Practice: Nested Queries", 20, 2, "practice"),
        _L("Challenge: Hierarchical Data Query", 40, 3, "challenge"),
        _L("Project: Organization Chart Query", 60, 3, "project",
           "An organization chart query using recursive CTEs for hierarchical data."),
    ]},
    # Level 7: Data Modification ✏️
    {"id": "l07", "difficulty": 2, "name": "Data Modification", "lessons": [
        _L("INSERT Statement", 10, 1), _L("INSERT Multiple Rows", 10, 1),
        _L("UPDATE Statement", 10, 1), _L("DELETE Statement", 10, 1),
        _L("TRUNCATE vs DELETE", 15, 2), _L("MERGE (Upsert)", 20, 3),
        _L("Practice: Data Modification", 20, 2, "practice"),
        _L("Challenge: Bulk Data Migration", 35, 3, "challenge"),
        _L("Project: Content Management System", 60, 3, "project",
           "A CMS with INSERT, UPDATE, DELETE, and MERGE operations for content management."),
    ]},
    # Level 8: Constraints & Data Integrity 🛡️
    {"id": "l08", "difficulty": 2, "name": "Constraints & Data Integrity", "lessons": [
        _L("PRIMARY KEY", 10, 1), _L("FOREIGN KEY", 10, 1),
        _L("UNIQUE Constraint", 10, 1), _L("CHECK Constraint", 15, 2),
        _L("DEFAULT Constraint", 10, 1), _L("NOT NULL Constraint", 10, 1),
        _L("Practice: Schema Design with Constraints", 20, 2, "practice"),
        _L("Challenge: Constraint Violation Handling", 30, 3, "challenge"),
        _L("Project: Banking Schema with Integrity", 60, 3, "project",
           "A banking database schema with primary keys, foreign keys, unique, check, and NOT NULL constraints."),
    ]},
    # Level 9: Indexes & Performance ⚡
    {"id": "l09", "difficulty": 3, "name": "Indexes & Performance", "lessons": [
        _L("CREATE INDEX", 10, 1), _L("Clustered vs Non-Clustered Index", 15, 2),
        _L("Composite Indexes", 15, 2), _L("Covering Indexes", 20, 2),
        _L("EXPLAIN / EXPLAIN ANALYZE", 20, 3), _L("Query Optimization", 25, 3),
        _L("Practice: Index Creation", 20, 2, "practice"),
        _L("Challenge: Query Plan Analysis", 40, 3, "challenge"),
        _L("Project: High-Performance Search Index", 60, 3, "project",
           "A high-performance search system with indexes, EXPLAIN ANALYZE, and query optimization."),
    ]},
    # Level 10: Transactions & Concurrency 🔐
    {"id": "l10", "difficulty": 3, "name": "Transactions & Concurrency", "lessons": [
        _L("BEGIN TRANSACTION / COMMIT", 10, 1), _L("ROLLBACK", 10, 1),
        _L("ACID Properties", 15, 2), _L("Isolation Levels", 20, 2),
        _L("Deadlocks", 15, 2), _L("Savepoints", 15, 2),
        _L("Practice: Transaction Blocks", 20, 2, "practice"),
        _L("Challenge: Deadlock Prevention", 40, 3, "challenge"),
        _L("Project: Payment Processing System", 60, 3, "project",
           "A payment processing system with transactions, ACID properties, and isolation levels."),
    ]},
    # Level 11: Views & Stored Procedures 📋
    {"id": "l11", "difficulty": 3, "name": "Views & Stored Procedures", "lessons": [
        _L("CREATE VIEW", 10, 1), _L("Updatable Views", 15, 2),
        _L("Materialized Views", 15, 2), _L("Stored Procedures", 20, 2),
        _L("Functions vs Procedures", 15, 2), _L("Triggers", 20, 3),
        _L("Practice: View Creation", 20, 2, "practice"),
        _L("Challenge: Audit Trigger", 40, 3, "challenge"),
        _L("Project: Automated Audit System", 60, 3, "project",
           "An automated audit system with views, stored procedures, and triggers for change tracking."),
    ]},
    # Level 12: Final Challenge 👑
    {"id": "l12", "difficulty": 3, "name": "Final Challenge", "lessons": [
        _L("Window Functions: RANK, DENSE_RANK", 30, 3), _L("Window Functions: LAG, LEAD", 30, 3),
        _L("Window Functions: NTILE, FIRST_VALUE, LAST_VALUE", 30, 3),
        _L("Recursive Queries for Hierarchies", 35, 3),
        _L("Practice: Advanced Window Functions", 40, 3, "practice"),
        _L("Challenge: Time-Series Analysis", 50, 3, "challenge"),
        _L("Capstone: Data Warehouse ETL Pipeline", 80, 3, "project",
           "A data warehouse ETL pipeline with window functions, recursive queries, and complex transformations."),
        _L("👑 SQL Grandmaster Boss", 80, 3, "boss"),
    ]},
    # Level 13: NoSQL & Document Databases 📄
    {"id": "l13", "difficulty": 3, "name": "NoSQL & Document Databases", "lessons": [
        _L("SQL vs NoSQL", 15, 2), _L("Document Model (JSON/BSON)", 15, 2),
        _L("CRUD in Document DB", 20, 2), _L("Indexing in NoSQL", 20, 2),
        _L("Aggregation Pipeline", 25, 3), _L("Sharding Basics", 20, 3),
        _L("Practice: Document Queries", 25, 2, "practice"),
        _L("Challenge: Schema Design for NoSQL", 40, 3, "challenge"),
        _L("Project: Content Platform Database", 60, 3, "project",
           "A content platform database using document model, aggregation pipelines, and sharding."),
    ]},
    # Level 14: Portfolio Capstone 🏆
    {"id": "l14", "difficulty": 3, "name": "Portfolio Capstone", "lessons": [
        _L("Database Design Patterns", 35, 3), _L("ORM vs Raw SQL", 40, 3, "practice"),
        _L("Challenge: Database Migration Strategy", 45, 3, "challenge"),
        _L("Project: Full-Stack Application Database", 80, 3, "project",
           "A comprehensive database design for a full-stack application with SQL, NoSQL, and caching layers."),
        _L("🏆 SQL Mastery Finale", 100, 3, "boss"),
    ]},
]

# Append levels 15-40 for SQL
for _i in range(14, 40):
    _meta = LEVEL_THEMES[_i]
    _lessons = [
        _L(f"{_meta['emoji']} {_meta['name']} — Core Concepts", 15, 1, "theory"),
        _L(f"🛠️ {_meta['name']} — Hands-On Practice", 20, 2, "practice"),
        _L(f"⚔️ {_meta['name']} — Challenge Problem", 35, 3, "challenge"),
    ]
    if _i + 1 in (20, 25, 30, 35, 40):
        _lessons.append(_L(f"🐉 {_meta['name']} — Boss Battle", 100, 3, "boss"))
    elif _i + 1 in (36, 37, 38):
        _lessons.append(_L(f"🏗️ {_meta['name']} — Capstone Project", 70, 3, "project",
            f"A comprehensive {_meta['name'].lower()} project demonstrating {_meta['desc'].lower()}"))
    else:
        _lessons.append(_L(f"🎯 {_meta['name']} — Mini Project", 60, 3, "project",
            f"A mini project exploring {_meta['desc'].lower()}"))
    SQL_LEVELS.append({"id": _meta["id"], "lessons": _lessons})
