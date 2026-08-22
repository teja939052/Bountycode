"""Study Library expansion: SQL, C, and Full-Stack articles + interactives.

Authored for the Learning Hub. This module defines:
  NEW_ARTICLES : 9 full article dicts (4 SQL, 2 C, 3 full-stack)
  INTERACTIVES : {article_id: {"quiz": [...], "exercise": {...}}}
                 for the seven articles defined in study_materials.py.

Imported by study_materials.py via _load_expansion(). The helper functions
below are copied here (not imported) because this module is a dependency of
study_materials, not a consumer of it.
"""


def _section(heading, body, code=None, pro_tip=""):
    s = {"heading": heading, "body": body}
    if code:
        s["code"] = code
    if pro_tip:
        s["pro_tip"] = pro_tip
    return s


def _quiz(question, options, answer, explanation):
    return {"question": question, "options": options, "answer": answer, "explanation": explanation}


def _exercise(title, task, starter, solution, hint=""):
    ex = {"title": title, "task": task, "starter": starter, "solution": solution}
    if hint:
        ex["hint"] = hint
    return ex


NEW_ARTICLES = [
    # ────────────────────────── SQL (4) ──────────────────────────
    {
        "id": "sql-joins",
        "title": "SQL JOINs: Inner, Left, Right, Full, and Self",
        "category": "sql",
        "summary": "Joins are how SQL answers questions across multiple tables. Master INNER, LEFT, RIGHT, FULL, and self-joins — and the NULL traps that come with them.",
        "level": "intermediate",
        "read_time_min": 15,
        "related_topics": ["sql-select", "sql-database", "sql-aggregation"],
        "sections": [
            _section(
                "Tables are friends: the ON clause",
                "Normalized databases split data across many tables: employees live in one, departments in another. A JOIN reassembles them by pairing each row of one table with rows of another when the ON condition is true. The ON clause names the bridge columns (usually keys). Always think of a join as rows times matches: how many rows come out depends on how many rows match on each side.",
                "SELECT e.name, d.name AS department\nFROM employees e\nINNER JOIN departments d ON e.dept_id = d.id;",
            ),
            _section(
                "INNER JOIN and LEFT JOIN: the daily workhorses",
                "INNER JOIN returns only rows with a match on BOTH sides; unmatched rows vanish. LEFT JOIN returns every row from the left table (the one before the JOIN keyword) and fills in the right columns with NULL when there is no match. The rule of thumb: start with INNER JOIN, and switch to LEFT JOIN when you cannot afford to lose rows from the primary table.",
                "-- INNER: only employees who actually belong to a department\nSELECT e.name, d.name AS department\nFROM employees e\nINNER JOIN departments d ON e.dept_id = d.id;\n\n-- LEFT: every employee, department is NULL when unmatched\nSELECT e.name, d.name AS department\nFROM employees e\nLEFT JOIN departments d ON e.dept_id = d.id;",
            ),
            _section(
                "RIGHT, FULL OUTER, and the NULL pitfall",
                "RIGHT JOIN is LEFT JOIN with the tables swapped: every right row survives, and the left side gets NULLs. FULL OUTER JOIN keeps rows from both sides, with NULL on whichever side lacks a match. The classic trap: after a LEFT JOIN, a WHERE filter on a column from the optional side deletes the NULL rows, silently turning your LEFT JOIN into an INNER JOIN. Move such filters into the ON clause instead.",
                "SELECT e.name, d.name\nFROM employees e\nFULL OUTER JOIN departments d ON e.dept_id = d.id;\n\n-- BUG: WHERE deletes the NULL rows, dropping unmatched employees\nSELECT e.name, d.name\nFROM employees e\nLEFT JOIN departments d ON e.dept_id = d.id\nWHERE d.name = 'Engineering';\n\n-- FIX: filter inside ON so unmatched rows survive\nSELECT e.name, d.name\nFROM employees e\nLEFT JOIN departments d ON e.dept_id = d.id\n  AND d.name = 'Engineering';",
            ),
            _section(
                "Self-joins: a table joined to itself",
                "Sometimes the comparison is inside one table — employees and their managers both live in employees. Give the table two aliases and join on the self-referencing column (manager_id pointing at another row's id). Self-joins also power finding duplicates, hierarchies, and pairs. Multi-table queries work the same way: chain joins left to right, each adding its own ON clause.",
                "SELECT e.name AS employee, m.name AS manager\nFROM employees e\nLEFT JOIN employees m ON e.manager_id = m.id;",
                "When a join returns more rows than you expected, you almost always have duplicate keys on one side of the ON condition — check for duplicate values in the join column before touching your logic.",
            ),
        ],
        "key_takeaways": [
            "INNER keeps matches; LEFT keeps the left table; FULL keeps both",
            "A filter on the optional side's column in WHERE erases unmatched rows",
            "RIGHT JOIN is LEFT JOIN with the tables swapped",
            "Self-joins use two aliases for one table to compare rows within it",
        ],
        "tag": "core",
        "quiz": [
            _quiz(
                "Which JOIN keeps every row from the table on the left, filling missing right-side values with NULL?",
                ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN"],
                1,
                "LEFT JOIN returns all rows from the first-named (left) table; where no match exists on the right, the right columns come back as NULL.",
            ),
            _quiz(
                "An INNER JOIN returns a row only when...",
                ["the left row exists", "both sides have a matching row", "the right row exists", "at least one side is NULL"],
                1,
                "INNER JOIN keeps only the intersections — a row must satisfy the ON condition on both tables or it is dropped entirely.",
            ),
            _quiz(
                "You LEFT JOIN departments and add WHERE d.name = 'Engineering'. Employees with no department disappear. Why?",
                ["LEFT JOIN drops them anyway", "WHERE runs after the join and removes the NULL department rows", "d.name is misspelled", "FULL JOIN is required"],
                1,
                "The join runs first, producing NULL for missing departments; the WHERE filter then deletes those rows. Put the filter in the ON clause to keep them.",
            ),
        ],
        "exercise": _exercise(
            "List every employee with their department",
            "The starter query uses an INNER JOIN, so employees without a department vanish from the results. Rewrite it to keep EVERY employee, showing NULL for the department when there is no match.",
            "SELECT e.name, d.name AS department\nFROM employees e\nINNER JOIN departments d ON e.dept_id = d.id\nORDER BY e.name;",
            "SELECT e.name, d.name AS department\nFROM employees e\nLEFT JOIN departments d ON e.dept_id = d.id\nORDER BY e.name;",
            "Change INNER JOIN to LEFT JOIN — the left table (employees) keeps all of its rows.",
        ),
        "curriculum": ["sql"],
    },
    {
        "id": "sql-aggregation",
        "title": "GROUP BY, HAVING, and Aggregate Functions",
        "category": "sql",
        "summary": "Aggregates turn thousands of rows into one answer: counts, totals, averages. Learn the five core functions, when GROUP BY kicks in, and why HAVING exists.",
        "level": "intermediate",
        "read_time_min": 14,
        "related_topics": ["sql-select", "sql-window-functions", "sql-database"],
        "sections": [
            _section(
                "The five core aggregate functions",
                "COUNT, SUM, AVG, MIN, and MAX summarize a set of rows into a single value. Run without GROUP BY, they summarize the whole table. SUM and AVG need numbers; COUNT, MIN, and MAX work on any type. These functions ignore NULL values — except COUNT(*), which counts rows regardless of their contents.",
                "SELECT COUNT(*)    AS total_orders,\n       SUM(amount) AS revenue,\n       AVG(amount) AS avg_order,\n       MIN(amount) AS smallest,\n       MAX(amount) AS largest\nFROM orders;",
            ),
            _section(
                "GROUP BY: from rows to groups",
                "GROUP BY collapses all rows sharing the same column values into one group, and every aggregate then runs per group. This is how you go from a table of individual orders to one summary row per customer. Any column in the SELECT that is not aggregated MUST appear in the GROUP BY — otherwise the database has no idea which value to show.",
                "SELECT customer_id,\n       COUNT(*)   AS orders,\n       SUM(amount) AS total_spent\nFROM orders\nGROUP BY customer_id;",
            ),
            _section(
                "HAVING vs WHERE: filter order matters",
                "WHERE filters individual rows BEFORE grouping; it cannot see aggregates because they do not exist yet. HAVING filters GROUPS AFTER aggregation and can use aggregate functions. Mix them up and you either get a syntax error (WHERE with an aggregate) or silently wrong answers. Use WHERE for row-level cuts, HAVING for group-level cuts.",
                "SELECT customer_id, COUNT(*) AS orders\nFROM orders\nWHERE amount > 10          -- skips small orders first\nGROUP BY customer_id\nHAVING COUNT(*) > 3;       -- keeps only busy customers\n\n-- WHERE cannot reference an aggregate:\n-- WHERE COUNT(*) > 3   -- ERROR",
            ),
            _section(
                "COUNT(*) vs COUNT(col) and the NULL truth",
                "COUNT(*) counts every row, including rows full of NULLs. COUNT(col) counts only non-NULL values in col. The same NULL-skipping applies to AVG, SUM, MIN, and MAX — so a few missing salaries can quietly lower your average. When NULLs carry meaning, make them explicit with COALESCE.",
                "SELECT COUNT(*)              AS all_employees,  -- includes NULL emails\n       COUNT(email)          AS with_email,     -- skips NULLs\n       AVG(salary)           AS avg_paid,       -- skips NULLs\n       AVG(COALESCE(salary, 0)) AS avg_everyone -- counts NULLs as 0\nFROM employees;",
                "If your average looks suspiciously high, suspect NULL rows being skipped — COALESCE or an explicit WHERE reveals the truth.",
            ),
        ],
        "key_takeaways": [
            "COUNT, SUM, AVG, MIN, MAX summarize a set of rows into one value",
            "GROUP BY collapses rows into groups; unaggregated columns must be grouped",
            "WHERE filters rows before grouping; HAVING filters groups after",
            "COUNT(*) counts rows; COUNT(col) counts non-NULL values only",
        ],
        "tag": "core",
        "quiz": [
            _quiz(
                "Which of these ignores NULL values?",
                ["COUNT(*)", "AVG", "None of them", "All of them"],
                1,
                "COUNT(*) counts rows and includes NULLs; AVG, SUM, MIN, and MAX skip NULL values — which can silently skew averages.",
            ),
            _quiz(
                "In SELECT dept_id, COUNT(*) FROM employees GROUP BY dept_id HAVING COUNT(*) > 5 — which step runs last?",
                ["WHERE", "GROUP BY", "HAVING", "ORDER BY"],
                2,
                "Execution order: WHERE filters rows, GROUP BY forms groups, then HAVING filters the groups. HAVING is evaluated after grouping, which is why it can see aggregates.",
            ),
            _quiz(
                "Why is WHERE COUNT(*) > 3 an error?",
                ["COUNT is misspelled", "WHERE runs before grouping, so aggregates do not exist yet", "WHERE only works on integers", "It is valid — no error"],
                1,
                "WHERE processes individual rows before GROUP BY runs, so no aggregate has been computed at that point. Use HAVING, which runs after grouping.",
            ),
        ],
        "exercise": _exercise(
            "Customers with more than two orders",
            "Count the orders per customer and return only the customers who placed MORE than 2 orders, ordered by order count from high to low. The starter query is missing the filter on groups.",
            "SELECT customer_id, COUNT(*) AS order_count\nFROM orders\nGROUP BY customer_id\nORDER BY order_count DESC;",
            "SELECT customer_id, COUNT(*) AS order_count\nFROM orders\nGROUP BY customer_id\nHAVING COUNT(*) > 2\nORDER BY order_count DESC;",
            "WHERE cannot see aggregates — add HAVING COUNT(*) > 2 after the GROUP BY.",
        ),
        "curriculum": ["sql"],
    },
    {
        "id": "sql-window-functions",
        "title": "Window Functions: ROW_NUMBER, RANK, and OVER",
        "category": "sql",
        "summary": "Window functions compute ranks, running totals, and per-group values without collapsing your rows. This is the superpower GROUP BY cannot give you.",
        "level": "advanced",
        "read_time_min": 16,
        "related_topics": ["sql-aggregation", "sql-joins", "sql-select"],
        "sections": [
            _section(
                "Why GROUP BY is not enough",
                "GROUP BY collapses many rows into one, destroying the detail rows. Sometimes you want the aggregate value AND the original rows side by side — a running total under each order, or each employee's salary next to their department average. Window functions compute a value over a window of rows while returning one result per input row, so nothing is lost.",
                "SELECT name, salary,\n       AVG(salary) OVER () AS company_avg\nFROM employees;",
            ),
            _section(
                "The OVER clause: PARTITION BY and ORDER BY",
                "OVER defines the window. PARTITION BY splits rows into independent groups, exactly like GROUP BY without the collapsing. ORDER BY inside OVER sets the order used by ranks and running totals. Every window function needs OVER; the plainest form is OVER () meaning the whole result set.",
                "SELECT name, department_id, salary,\n       AVG(salary) OVER (PARTITION BY department_id) AS dept_avg\nFROM employees;\n\nSELECT name, salary,\n       SUM(salary) OVER (ORDER BY id) AS running_total\nFROM employees;",
            ),
            _section(
                "ROW_NUMBER, RANK, and DENSE_RANK",
                "All three number rows inside a partition. ROW_NUMBER gives unique sequential numbers — ties are broken arbitrarily. RANK gives tied rows the same number and then SKIPS: for salaries 100, 90, 90, 80 you get 1, 2, 2, 4. DENSE_RANK does not skip: 1, 2, 2, 3. Leaderboards care about this distinction — RANK says 'two people are second, next is fourth', DENSE_RANK says 'three distinct levels so far'.",
                "SELECT name, salary,\n       ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn,\n       RANK()       OVER (ORDER BY salary DESC) AS rk,\n       DENSE_RANK() OVER (ORDER BY salary DESC) AS drk\nFROM employees;",
            ),
            _section(
                "Frames: the sliding window",
                "ORDER BY inside OVER gives running aggregates their direction, but the FRAME controls exactly which rows are included. The default frame is everything from the partition's start to the current row. ROWS BETWEEN 2 PRECEDING AND CURRENT ROW builds a moving window of three rows — perfect for moving averages. Frames are the difference between a cumulative total and a rolling three-day trend.",
                "SELECT date, amount,\n       SUM(amount) OVER (ORDER BY date) AS running_total,\n       AVG(amount) OVER (ORDER BY date\n           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_3\nFROM sales;",
                "Window functions run after WHERE and GROUP BY, so you cannot filter on their result in the same query — wrap the query in a subquery, or use QUALIFY in databases that support it.",
            ),
        ],
        "key_takeaways": [
            "Window functions return one value per row instead of collapsing to groups",
            "PARTITION BY splits the window; ORDER BY inside OVER sets rank/order",
            "RANK skips numbers after ties; DENSE_RANK and ROW_NUMBER do not",
            "Frames (ROWS BETWEEN) control running totals and moving averages",
        ],
        "tag": "advanced",
        "quiz": [
            _quiz(
                "RANK() and DENSE_RANK() differ because...",
                ["RANK skips numbers after ties, DENSE_RANK does not", "DENSE_RANK skips numbers after ties, RANK does not", "They are identical", "RANK cannot use PARTITION BY"],
                0,
                "For salaries 100, 90, 90, 80: RANK gives 1, 2, 2, 4 while DENSE_RANK gives 1, 2, 2, 3 — RANK counts the tied positions, DENSE_RANK only counts distinct values.",
            ),
            _quiz(
                "What does PARTITION BY do inside a window function?",
                ["Filters the table", "Splits rows into groups, each computed independently", "Sorts the whole result", "Merges two tables"],
                1,
                "PARTITION BY divides the rows into independent windows; the window function computes a value within each partition, like a per-group aggregate that does not collapse the rows.",
            ),
            _quiz(
                "You want the top 3 salaries per department. Why can't you write WHERE salary_rank <= 3 in the same query?",
                ["salary_rank is misspelled", "Window functions run after WHERE, so the result is not visible yet", "WHERE cannot compare numbers", "You can — it works"],
                1,
                "Windows are computed after WHERE, GROUP BY, and HAVING. To filter on a window result, wrap the query in a subquery (or use QUALIFY where supported).",
            ),
        ],
        "exercise": _exercise(
            "Rank employees by salary within each department",
            "Add a salary_rank column that ranks employees by salary from highest to lowest INSIDE each department, using RANK so employees with equal salaries share a rank.",
            "SELECT name, department_id, salary\nFROM employees\nORDER BY department_id, salary DESC;",
            "SELECT name, department_id, salary,\n       RANK() OVER (PARTITION BY department_id\n                    ORDER BY salary DESC) AS salary_rank\nFROM employees\nORDER BY department_id, salary DESC;",
            "Use RANK() with OVER (PARTITION BY department_id ORDER BY salary DESC).",
        ),
        "curriculum": ["sql"],
    },
    {
        "id": "sql-indexes-performance",
        "title": "Indexes and Query Performance",
        "category": "sql",
        "summary": "The difference between a fast query and a table scan is usually an index. Understand the B-tree, when indexes hurt, and how EXPLAIN proves the truth.",
        "level": "advanced",
        "read_time_min": 15,
        "related_topics": ["sql-database", "sql-select", "sql-joins"],
        "sections": [
            _section(
                "What an index is: the phone book",
                "Without an index the database reads every row to answer a lookup — a sequential scan that gets slower with every new row. An index is a separate, sorted structure (usually a B-tree) that maps key values to row locations. Because it is sorted, finding a value takes O(log n) comparisons instead of an O(n) scan. Indexes are most valuable on the columns you filter (WHERE), join (ON), and sort (ORDER BY) with.",
                "CREATE INDEX idx_orders_customer ON orders(customer_id);\n\n-- now this lookup jumps straight to the matching rows\nSELECT * FROM orders WHERE customer_id = 42;",
            ),
            _section(
                "The trade-off: reads get faster, writes get slower",
                "Every INSERT, UPDATE, and DELETE must maintain every index on the table — each write now touches the table AND the sorted tree. Too many indexes slow writes and eat disk, while unused ones do nothing but cost money. The discipline: index what real queries filter on, and drop indexes nothing uses.",
                "CREATE INDEX idx_orders_status ON orders(status);   -- good if filtered often\n-- Do NOT create an index for every column 'just in case'.",
            ),
            _section(
                "Composite indexes and the leftmost prefix",
                "A composite index on (country, city) is one sorted tree keyed by country first, then city. It accelerates queries on country alone, and on country + city, but it is USELESS for city alone — the leftmost prefix rule. Functions on a column also defeat indexes: WHERE YEAR(created_at) = 2024 forces the engine to compute YEAR() for every row. Rewrite it as a range on the raw column to stay index-friendly (sargable).",
                "CREATE INDEX idx_customers_country_city ON customers(country, city);\n\n-- uses the index (full key)\nSELECT * FROM customers\nWHERE country = 'US' AND city = 'Boston';\n\n-- uses the index (leftmost part)\nSELECT * FROM customers WHERE country = 'US';\n\n-- CANNOT use the index — city is not the leading column\nSELECT * FROM customers WHERE city = 'Boston';\n\n-- defeats the index:\nSELECT * FROM orders WHERE YEAR(created_at) = 2024;\n\n-- index-friendly rewrite:\nSELECT * FROM orders\nWHERE created_at >= '2024-01-01'\n  AND created_at <  '2025-01-01';",
            ),
            _section(
                "EXPLAIN: prove it, do not guess",
                "EXPLAIN prints the query planner's execution plan. The two lines you care about are 'Seq Scan' (reading every row — usually bad on big tables) and 'Index Scan' (using an index — good). Run EXPLAIN on a slow query, add a candidate index, run EXPLAIN again, and let the plan be the judge. EXPLAIN ANALYZE even shows the real timings.",
                "EXPLAIN SELECT * FROM orders WHERE customer_id = 42;\n-- Look for: \"Seq Scan\" (bad) vs\n--            \"Index Scan using idx_orders_customer\" (good)",
                "Indexes speed up reads but every write pays for them. Add an index only when a real query needs it — and let EXPLAIN ANALYZE be the judge.",
            ),
        ],
        "key_takeaways": [
            "A B-tree index turns O(n) lookups into O(log n)",
            "Writes slow down with every index; index only what real queries use",
            "Composite indexes follow the leftmost prefix rule",
            "EXPLAIN shows whether a query scans or uses the index",
        ],
        "tag": "advanced",
        "quiz": [
            _quiz(
                "What is the main cost of adding an index?",
                ["Queries return wrong data", "Writes become slower and the index consumes storage", "Tables can no longer be deleted", "NULL values are forbidden"],
                1,
                "Every INSERT/UPDATE/DELETE must keep the index tree sorted, so write cost grows with each index, and the index itself takes disk space.",
            ),
            _quiz(
                "An index on (country, city) can speed up which query?",
                ["WHERE city = 'Boston'", "WHERE country = 'US' AND city = 'Boston'", "WHERE name = 'Ada'", "ORDER BY name"],
                1,
                "Composite indexes follow the leftmost prefix rule — country is the leading column, so a query filtering on country (alone or with city) can use the index; city alone cannot.",
            ),
            _quiz(
                "Why can't WHERE YEAR(created_at) = 2024 use an index on created_at?",
                ["YEAR is not valid SQL", "Wrapping the column in a function hides its raw value from the index", "Indexes only work on integers", "It can — functions never block indexes"],
                1,
                "The index stores raw column values. Applying a function forces the engine to compute YEAR(...) for every row, so it scans the table. Use a range: created_at >= '2024-01-01' AND created_at < '2025-01-01'.",
            ),
        ],
        "exercise": _exercise(
            "Speed up the slow query",
            "This query scans the whole table every time. Create an index that makes the lookup fast, then rewrite the query so it can actually use that index.",
            "-- slow: no index, and the function defeats any index\nSELECT * FROM orders WHERE YEAR(created_at) = 2024;",
            "CREATE INDEX idx_orders_created ON orders(created_at);\n\nSELECT * FROM orders\nWHERE created_at >= '2024-01-01'\n  AND created_at <  '2025-01-01';",
            "Range predicates on the column itself can use a B-tree index; a function wrapper cannot.",
        ),
        "curriculum": ["sql"],
    },
    # ────────────────────────── C Programming (2) ──────────────────────────
    {
        "id": "c-strings",
        "title": "C Strings and Characters: The Null-Terminated Reality",
        "category": "c-programming",
        "summary": "A C string is a char array that ends with a '\\0'. Forget the terminator and every string function will happily read past your buffer.",
        "level": "intermediate",
        "read_time_min": 14,
        "related_topics": ["c-pointers", "c-preprocessors-files", "c-memory"],
        "sections": [
            _section(
                "Strings are arrays of char, nothing more",
                "C has no string type. A string is an array of char with a trailing NUL character ('\\0', value 0) that marks the end. No length is stored anywhere — every string function finds the end by scanning for '\\0'. That is why sizeof gives one more than strlen: the array includes the terminator, but the string's logical length does not.",
                "#include <stdio.h>\n#include <string.h>\n\nint main(void) {\n  char name[] = \"Ada\";   // size is 4: 'A' 'd' 'a' '\\0'\n\n  printf(\"size: %zu\\n\", sizeof name);   // 4 — includes the terminator\n  printf(\"len:  %zu\\n\", strlen(name));  // 3 — without the terminator\n  return 0;\n}",
            ),
            _section(
                "The dangerous trio: strcpy, strcat, strlen",
                "strcpy copies bytes from the source until its '\\0' — it never checks that the destination has room, so a long source overflows the buffer. strcat appends after the destination's terminator, equally unchecked. Buffer overflows are how real-world vulnerabilities happen: you write past the array and corrupt adjacent memory. strlen is safe to call, but your buffers still need room for the terminator.",
                "#include <string.h>\n\nint main(void) {\n  char src[] = \"Ada\";\n  char dst[4];\n  strcpy(dst, src);     // fine: 3 chars + '\\0' fits\n\n  char tiny[3];\n  strcpy(tiny, src);    // BOOM: writes 4 bytes into a 3-byte array\n  return 0;\n}",
            ),
            _section(
                "The safe versions: strncat, snprintf",
                "The bounded functions still need discipline. strncpy(dst, src, n) writes at most n bytes but may leave the string UNTERMINATED when src is that long — you must force the last byte to '\\0'. strncat(dst, src, n) is the friendlier one: it appends at most n chars and always adds its own terminator (given room). For building text, snprintf is the most reliable tool: it truncates safely and always terminates.",
                "#include <stdio.h>\n#include <string.h>\n\nint main(void) {\n  char dst[16] = \"Hello, \";\n  strncat(dst, \"world!\", 9);  // appends at most 9 chars, always NUL-terminates\n  printf(\"%s\\n\", dst);\n\n  char buf[16];\n  snprintf(buf, sizeof buf, \"%s %s\", \"Ada\", \"Lovelace\");\n  printf(\"%s\\n\", buf);\n  return 0;\n}",
            ),
            _section(
                "Walking a string with a pointer",
                "Because a string ends at '\\0', loops that scan for the terminator are the core idiom: counting length, copying, reversing, counting vowels. The while loop keeps going until it sees the NUL — the terminator is both the data boundary and the loop condition.",
                "#include <stdio.h>\n\nsize_t my_strlen(const char *s) {\n  const char *p = s;\n  while (*p != '\\0') p++;   // advance until the terminator\n  return (size_t)(p - s);\n}\n\nint main(void) {\n  printf(\"%zu\\n\", my_strlen(\"hello\"));  // 5\n  return 0;\n}",
                "When you allocate room for a string, add one extra byte for the '\\0' — the most common bug in C is the off-by-one buffer overflow.",
            ),
        ],
        "key_takeaways": [
            "A C string is a char array ending in '\\0' — no length is stored",
            "sizeof includes the terminator; strlen does not",
            "strcpy/strcat are unbounded and overflow small buffers",
            "Prefer strncat and snprintf, and always reserve the terminator byte",
        ],
        "tag": "core",
        "quiz": [
            _quiz(
                "What marks the end of a C string?",
                ["A newline character", "The NUL character '\\0'", "The byte 0xFF", "Its length stored in memory"],
                1,
                "Every C string is a char array that ends at the first '\\0' (NUL). String functions scan forward for that terminator; there is no stored length.",
            ),
            _quiz(
                "Why is strcpy(dst, src) dangerous?",
                ["It copies in reverse order", "It never checks that dst has room, so it can overflow the buffer", "It only works on integers", "It deletes the source"],
                1,
                "strcpy copies bytes until it finds src's '\\0', writing wherever dst points. If dst is too small, it writes past the end of the array — a buffer overflow.",
            ),
            _quiz(
                "For char s[] = \"hello\"; what does strlen(s) return?",
                ["6", "5", "4", "0"],
                1,
                "strlen counts the characters before the terminator — h, e, l, l, o is 5 — and does NOT count the trailing '\\0' (which is why sizeof would give 6).",
            ),
        ],
        "exercise": _exercise(
            "Safe concatenation",
            "Complete the append function so it safely adds src to the end of dst without overflowing, keeping the result NUL-terminated at all times. Use strncat with the space that is actually left.",
            "#include <stdio.h>\n#include <string.h>\n\nvoid append(char *dst, size_t dst_size, const char *src) {\n  // TODO: append src to dst, never writing past dst_size - 1 bytes,\n  // and always keeping dst NUL-terminated.\n}\n\nint main(void) {\n  char buf[12] = \"Hello, \";\n  append(buf, sizeof buf, \"world!\");\n  printf(\"%s\\n\", buf);   // Hello, world!\n  return 0;\n}",
            "#include <stdio.h>\n#include <string.h>\n\nvoid append(char *dst, size_t dst_size, const char *src) {\n  size_t used = strlen(dst);\n  if (used >= dst_size) return;                 // already full\n  strncat(dst + used, src, dst_size - used - 1);\n}\n\nint main(void) {\n  char buf[12] = \"Hello, \";\n  append(buf, sizeof buf, \"world!\");\n  printf(\"%s\\n\", buf);   // Hello, world!\n  return 0;\n}",
            "strncat writes at most n bytes from src and then adds its own '\\0' — pass the remaining capacity minus one.",
        ),
        "curriculum": ["c"],
    },
    {
        "id": "c-functions-recursion",
        "title": "C Functions, Pointers to Functions, and Recursion",
        "category": "c-programming",
        "summary": "Functions keep C readable, function pointers let you treat code as data, and recursion solves problems that are naturally nested — when it stops.",
        "level": "advanced",
        "read_time_min": 16,
        "related_topics": ["c-pointers", "c-enums-structs", "c-strings"],
        "sections": [
            _section(
                "Prototypes: declare before you call",
                "C compiles top to bottom, so a function must be declared before it is called. A prototype — the function's signature with a trailing semicolon — announces the name, parameters, and return type. This is exactly why headers exist: they carry prototypes so many source files can share functions. With a prototype, a mismatched call is a compile-time error; without one, C guesses and produces silent, corrupt code.",
                "#include <stdio.h>\n\nint add(int a, int b);   // prototype — declares the signature\n\nint main(void) {\n  printf(\"%d\\n\", add(2, 3));  // OK even though add is defined below\n  return 0;\n}\n\nint add(int a, int b) {      // definition\n  return a + b;\n}",
            ),
            _section(
                "Pass by value vs pass by pointer",
                "C passes everything by value — the function receives a COPY. Changing a parameter inside the function never touches the caller's variable. To modify the caller's data you must pass a pointer and dereference it. Arrays are the exception: an array argument decays to a pointer to its first element, so functions effectively see the original array and can modify it.",
                "#include <stdio.h>\n\nvoid no_change(int x) { x = 99; }        // copies — caller unaffected\nvoid real_change(int *x) { *x = 99; }    // writes through the pointer\n\nint main(void) {\n  int v = 1;\n  no_change(v);\n  printf(\"%d\\n\", v);    // 1\n  real_change(&v);\n  printf(\"%d\\n\", v);    // 99\n  return 0;\n}",
            ),
            _section(
                "Function pointers: functions as data",
                "A function name is just an address — you can store it in a pointer. The syntax reads right-to-left: int (*fp)(int, int) means 'fp is a pointer to a function taking two ints and returning an int'. Call through the pointer with fp(a, b). Function pointers power callbacks (qsort's comparator, signal handlers) and dispatch tables, letting one piece of code invoke many different behaviors.",
                "#include <stdio.h>\n\nint add(int a, int b) { return a + b; }\nint mul(int a, int b) { return a * b; }\n\nint main(void) {\n  int (*fp)(int, int);   // fp: pointer to a function(int, int) -> int\n\n  fp = add;\n  printf(\"%d\\n\", fp(2, 3));   // 5\n  fp = mul;\n  printf(\"%d\\n\", fp(2, 3));   // 6\n  return 0;\n}",
            ),
            _section(
                "Recursion: base case + recursive case",
                "A recursive function calls itself. Two parts are mandatory: a base case that stops the recursion, and a recursive case that shrinks the problem toward the base. Every call pushes a new frame onto the stack, so a missing base case means unbounded growth and a stack overflow. When the recursion depth scales with the input, an iterative loop uses constant stack instead.",
                "#include <stdio.h>\n\nunsigned long factorial(unsigned int n) {\n  if (n <= 1) return 1;              // base case\n  return n * factorial(n - 1);       // recursive case\n}\n\nint main(void) {\n  printf(\"%lu\\n\", factorial(5));   // 120\n  return 0;\n}",
                "Every recursive call consumes stack memory. If the recursion depth is proportional to the input size, prefer an iterative loop — it is the same algorithm with constant stack.",
            ),
        ],
        "key_takeaways": [
            "Prototypes declare signatures so calls can be checked at compile time",
            "Parameters are copies; pointers are how functions modify caller data",
            "int (*fp)(int, int) declares a pointer to a function — call via fp(a, b)",
            "Recursion needs a base case and a shrinking recursive case, or the stack overflows",
        ],
        "tag": "advanced",
        "quiz": [
            _quiz(
                "Which correctly declares a pointer to a function taking an int and returning an int?",
                ["int *fp(int)", "int (*fp)(int)", "int fp(int *)", "(int) *fp(int)"],
                1,
                "Parentheses bind the * to the name: int (*fp)(int) reads 'fp is a pointer to a function taking an int and returning an int'. int *fp(int) would mean a function returning int*.",
            ),
            _quiz(
                "A recursive function with no base case will...",
                ["run once and stop", "keep calling itself until the stack overflows", "be optimized away automatically", "return 0"],
                1,
                "Each call pushes a new frame on the stack. Without a base case the calls never stop, the stack grows until memory runs out, and the program crashes.",
            ),
            _quiz(
                "void f(int x) { x = 99; } — after calling f(v), what is v?",
                ["99", "unchanged", "NULL", "undefined"],
                1,
                "C passes arguments by value — f receives a copy of v. Changing the copy leaves the caller's variable untouched. To modify v, pass &v and use a pointer parameter.",
            ),
        ],
        "exercise": _exercise(
            "Recursive array sum",
            "Write sum_rec so it returns the sum of the first n elements of the array. Base case: when n is 0 the sum is 0. The recursive case shrinks the problem by one element.",
            "#include <stdio.h>\n\nint sum_rec(int arr[], int n) {\n  // TODO: recursive sum of the first n elements\n}\n\nint main(void) {\n  int nums[] = {2, 4, 6, 8};\n  printf(\"%d\\n\", sum_rec(nums, 4));  // 20\n  return 0;\n}",
            "#include <stdio.h>\n\nint sum_rec(int arr[], int n) {\n  if (n == 0) return 0;                    // base case\n  return arr[n - 1] + sum_rec(arr, n - 1); // recursive case\n}\n\nint main(void) {\n  int nums[] = {2, 4, 6, 8};\n  printf(\"%d\\n\", sum_rec(nums, 4));  // 20\n  return 0;\n}",
            "Make the problem smaller: the sum of n elements is the last element plus the sum of the first n - 1.",
        ),
        "curriculum": ["c"],
    },
    # ────────────────────────── Full-Stack (3) ──────────────────────────
    {
        "id": "fs-crud-todo",
        "title": "Build a Full-Stack Todo App: React + Express + SQL",
        "category": "full-stack",
        "summary": "The classic first full-stack app: a todo list. Follow one request through React, Express, and SQL, and see how the CRUD verbs map to endpoints.",
        "level": "intermediate",
        "read_time_min": 17,
        "related_topics": ["fullstack-architecture", "sql-database", "fs-api-design"],
        "sections": [
            _section(
                "The shape of the project",
                "A full-stack todo app is three layers in two folders: a React frontend that renders and sends requests, an Express backend that validates and talks to the database, and a SQL table that stores the truth. During development, Vite proxies /api calls to the Express port so the frontend can use friendly relative URLs.",
                "todo-app/\n├── frontend/            # React (Vite)\n│   └── src/App.jsx      # fetches and renders todos\n├── backend/             # Express\n│   ├── index.js         # server + routes\n│   └── db.js            # database connection + queries\n└── schema.sql           # CREATE TABLE todos",
            ),
            _section(
                "The schema and the CRUD routes",
                "One table is enough. The four CRUD verbs map cleanly onto HTTP: POST creates, GET reads, PUT/PATCH updates, DELETE removes. The server's job is to validate input at the boundary and run SQL with parameterized queries ($1 placeholders) so user input is treated as data, never as executable SQL. Returning rows with RETURNING * hands the created row straight back.",
                "CREATE TABLE todos (\n  id SERIAL PRIMARY KEY,\n  title TEXT NOT NULL,\n  done BOOLEAN NOT NULL DEFAULT FALSE,\n  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()\n);\n\n// Express (node-postgres style)\napp.post('/api/todos', async (req, res) => {\n  const { title } = req.body;\n  const { rows } = await db.query(\n    'INSERT INTO todos (title) VALUES ($1) RETURNING *',\n    [title]\n  );\n  res.status(201).json(rows[0]);\n});",
            ),
            _section(
                "React: fetch, render, add, toggle, delete",
                "React fetches the list on mount and keeps it in state. Handlers call the API and update state from the RESPONSE, not from guesses: the created todo is appended, the deleted one is filtered out. Because state is the only thing React re-renders from, every mutation flows through setState.",
                "import { useEffect, useState } from 'react';\n\nfunction App() {\n  const [todos, setTodos] = useState([]);\n\n  useEffect(() => {\n    fetch('/api/todos').then(r => r.json()).then(setTodos);\n  }, []);\n\n  const addTodo = async () => {\n    const res = await fetch('/api/todos', {\n      method: 'POST',\n      headers: { 'Content-Type': 'application/json' },\n      body: JSON.stringify({ title: 'Learn SQL' }),\n    });\n    const created = await res.json();\n    setTodos(prev => [...prev, created]);   // append the created row\n  };\n\n  return (\n    <ul>\n      {todos.map(t => <li key={t.id}>{t.title}</li>)}\n      <button onClick={addTodo}>Add</button>\n    </ul>\n  );\n}",
            ),
            _section(
                "Connecting the pieces — and the pitfalls",
                "In development, a proxy sends /api requests to Express so there is no CORS pain; in production the API is on its own origin or behind a reverse proxy. The common failures: mutating state arrays in place (React needs a NEW array to re-render), trusting the client for ids and timestamps, and forgetting that the server — not the client — owns validation.",
                "// vite.config.js — dev proxy\nimport { defineConfig } from 'vite';\nexport default defineConfig({\n  server: {\n    proxy: { '/api': 'http://localhost:3000' }\n  }\n});",
                "Never trust the client to compute the id or created_at — let the database generate them and RETURN them. The response is your source of truth.",
            ),
        ],
        "key_takeaways": [
            "CRUD maps to HTTP: POST create, GET read, PUT/PATCH update, DELETE remove",
            "The server validates input and uses parameterized queries",
            "React updates state from the server's response, never from guesses",
            "A dev proxy (/api) keeps development CORS-free",
        ],
        "tag": "projects",
        "quiz": [
            _quiz(
                "Which HTTP method creates a new resource?",
                ["GET", "POST", "DELETE", "HEAD"],
                1,
                "POST sends data to create a resource (201 Created). GET reads, PUT/PATCH update, and DELETE removes.",
            ),
            _quiz(
                "Why use a parameterized query like VALUES ($1) instead of string interpolation?",
                ["It is faster to type", "It prevents SQL injection and keeps data as data", "It makes queries return JSON", "It is required for indexes"],
                1,
                "The database treats $1 as a bound value, never as SQL, so a malicious title cannot inject commands. String interpolation turns user input into executable SQL.",
            ),
            _quiz(
                "After POST /api/todos returns the created row, why should React append that row instead of rebuilding it from the input?",
                ["It shouldn't — always refetch", "The response is the server's source of truth with the real id and timestamps", "It saves electricity", "Rows are immutable"],
                1,
                "The database generates id and created_at. Using the returned row keeps the client in sync without a second round trip and avoids id mismatches.",
            ),
        ],
        "exercise": _exercise(
            "Create a todo — the Express POST route",
            "Write the Express route that reads a title from the request body, validates it, inserts it with a parameterized query, and returns 201 with the created row.",
            "app.post('/api/todos', async (req, res) => {\n  const { title } = req.body;\n  // TODO: validate, insert with $1, return 201 + the created row\n});",
            "app.post('/api/todos', async (req, res) => {\n  const { title } = req.body;\n  if (!title || typeof title !== 'string') {\n    return res.status(400).json({ error: 'title is required' });\n  }\n  const { rows } = await db.query(\n    'INSERT INTO todos (title) VALUES ($1) RETURNING *',\n    [title]\n  );\n  res.status(201).json(rows[0]);\n});",
            "Validate first, then INSERT ... RETURNING *, then res.status(201).json(rows[0]).",
        ),
        "curriculum": ["html", "css", "javascript", "react", "node", "sql"],
    },
    {
        "id": "fs-deploy",
        "title": "Deploying a Full-Stack App: Build, Host, and Monitor",
        "category": "full-stack",
        "summary": "Deploying turns 'works on my machine' into 'works for the internet'. Learn the build step, hosting options, secrets, and how to watch what you shipped.",
        "level": "intermediate",
        "read_time_min": 15,
        "related_topics": ["fs-crud-todo", "fs-api-design", "fullstack-architecture"],
        "sections": [
            _section(
                "The build step: source becomes artifacts",
                "The frontend source (JSX, modules, imports) is not what ships — the bundler transforms it into optimized static files. npm run build produces a dist/ folder of minified HTML, CSS, and JavaScript ready to serve. The backend ships as source plus its dependencies and a start command. Environments differ: dev watches files, production serves the built result.",
                "# frontend\nnpm run build        # produces dist/ with static assets\n\n# backend\nnpm run start        # runs the Node server, often on PORT from env",
            ),
            _section(
                "Hosting choices: platform vs server",
                "Platforms like Vercel, Netlify, Render, and Railway abstract away servers: you push, they build and scale. A VPS or container host gives full control but you manage everything. Two full-stack patterns work: a single origin where Express also serves the built frontend, or a split where a CDN serves static files and the API lives on its own domain.",
                "// pattern A: one origin — Express serves the built React app\nconst path = require('path');\napp.use(express.static(path.join(__dirname, '../frontend/dist')));\n\n// pattern B: split — static files on a CDN, API on its own host\n// frontend fetches https://api.yourdomain.com/api/todos",
            ),
            _section(
                "Secrets and configuration",
                "Environment variables keep configuration out of code. DATABASE_URL, JWT_SECRET, ports, and API keys live in the hosting platform's secret store, never in a committed .env file. Commit a .env.example with placeholders so teammates know what to set, and give each environment (dev, staging, prod) its own values — and its own database.",
                "# .env.example — committed, with placeholder values only\nDATABASE_URL=postgres://user:pass@host:5432/db\nPORT=3000\nJWT_SECRET=change-me",
                "Rotate secrets the moment they leak, and give each environment its own database — pointing staging at production is how someone deletes real data.",
            ),
            _section(
                "Monitor, log, rollback",
                "Once deployed, you need eyes: structured logs, error tracking, and a health endpoint. A real health check verifies its dependencies. Run database migrations before each release, keep the previous version around, and make rollback a one-command operation. You are not 'done' after the first deploy — you are watching it.",
                "GET /api/health\n-> 200 {\"status\": \"ok\", \"db\": \"connected\"}\n\n# release flow\nmigrate up        # 1. apply schema changes\nnpm run build     # 2. build the frontend\nrelease           # 3. swap to the new version",
                "Make the health check actually check the database — an endpoint that returns 200 while the DB is down tells you nothing.",
            ),
        ],
        "key_takeaways": [
            "The build step turns frontend source into optimized static files",
            "Platforms abstract servers; VPSes give control — pick per trade-offs",
            "Secrets live in the platform's store, never in a committed .env",
            "Real health checks, structured logs, and one-command rollbacks",
        ],
        "tag": "projects",
        "quiz": [
            _quiz(
                "What does npm run build produce for a React app?",
                ["A Node server", "Optimized static files (HTML/CSS/JS) in dist/", "A database dump", "A source map only"],
                1,
                "The bundler (Vite) transforms JSX and imports into minified static assets ready to serve — usually in dist/. The server code is not built this way.",
            ),
            _quiz(
                "Where should DATABASE_URL and JWT_SECRET live in production?",
                ["In a committed .env file", "In the hosting platform's environment variables or secret store", "In the frontend code", "In the database"],
                1,
                "Secrets belong in the platform's secret store, never committed to git or shipped to the browser. Each environment gets its own set.",
            ),
            _quiz(
                "Your /api/health always returns 200 even when the database is down. What is the problem?",
                ["Health checks cannot return 200", "It lies — monitoring will not catch a real outage", "It should return 300", "No problem — that is correct"],
                1,
                "A health endpoint that does not verify its dependencies reports 'healthy' during an outage. It should run a trivial query (SELECT 1) and return 5xx when that fails.",
            ),
        ],
        "exercise": _exercise(
            "A health check that means something",
            "Write the /api/health endpoint so it actually verifies the database connection and reports its status, returning 200 only when the database is reachable and 503 when it is not.",
            "app.get('/api/health', (req, res) => {\n  res.json({ status: 'ok' });   // TODO: actually check the database\n});",
            "app.get('/api/health', async (req, res) => {\n  try {\n    await db.query('SELECT 1');\n    res.json({ status: 'ok', db: 'connected' });\n  } catch (err) {\n    res.status(503).json({ status: 'degraded', db: 'down' });\n  }\n});",
            "Run a trivial query like SELECT 1 and wrap it in try/catch.",
        ),
        "curriculum": ["html", "css", "javascript", "react", "node", "sql"],
    },
    {
        "id": "fs-api-design",
        "title": "REST API Design: Resources, Status Codes, Pagination",
        "category": "full-stack",
        "summary": "A well-designed API is predictable: nouns for resources, verbs for actions, honest status codes, and pagination that survives big data.",
        "level": "advanced",
        "read_time_min": 16,
        "related_topics": ["fullstack-architecture", "fs-crud-todo", "sql-select"],
        "sections": [
            _section(
                "Resources, not actions",
                "REST models resources with nouns and uses the HTTP methods as the verbs. The URL names the thing; the method says what to do. POST /api/getUser and GET /api/users?action=fetch bury the action in the URL and make clients guess — the method already told you. Consistency is the feature: learn the pattern once, understand every well-built API.",
                "GET    /api/users       read a list\nPOST   /api/users       create one\nGET    /api/users/42    read one\nPUT    /api/users/42    replace\nPATCH  /api/users/42    partial update\nDELETE /api/users/42    remove",
            ),
            _section(
                "Status codes that mean something",
                "Status codes are part of the API contract. 200/201/204 for success, 400 bad request, 401 unauthenticated, 403 authenticated but not allowed, 404 not found, 422 validation failure, 409 conflict, 500 server error. Return 201 with the created resource on POST, 204 on a successful DELETE. Returning 200 for everything hides bugs and forces clients to guess.",
                "POST /api/users       -> 201 Created   + body: the new user\nGET  /api/users/9999    -> 404 Not Found\nPOST /api/todos         -> 400 Bad Request (missing title)\nDELETE /api/users/42    -> 204 No Content",
            ),
            _section(
                "Pagination: limit/offset vs cursors",
                "?limit&offset is simple but degrades: an OFFSET of 100000 still requires the database to find and skip 100000 rows. Cursor (keyset) pagination keys off a unique indexed column — usually the id — with WHERE id > $cursor ORDER BY id LIMIT n. That is O(log n) at any depth. Return the next cursor so clients can keep walking the list, plus total when it is cheap to compute.",
                "GET /api/todos?limit=20&offset=0\nGET /api/todos?limit=20&offset=40     -- offset pagination\n\nGET /api/todos?limit=20&cursor=1984   -- cursor pagination\nSELECT * FROM todos\nWHERE id > $1\nORDER BY id ASC\nLIMIT $2;\n-- response: { \"items\": [...], \"next_cursor\": 2017 }",
            ),
            _section(
                "Consistency: versioning, errors, validation",
                "A versioned path (/api/v1/users) lets you break things deliberately and safely. Validate at the boundary — the server never trusts the client. And return errors in one consistent shape with a machine-readable code clients can branch on, a human message, and the offending field. Consistency is what makes error handling on the client a five-line helper instead of a pile of hacks.",
                "{ \"error\": { \"code\": \"VALIDATION_FAILED\",\n             \"message\": \"title is required\",\n             \"field\": \"title\" } }",
                "Return 401 for 'who are you' and 403 for 'you are known but not allowed'. Mixing them up confuses clients — and your security audits.",
            ),
        ],
        "key_takeaways": [
            "URLs name resources; HTTP methods express the action",
            "Status codes are contract: 201/204, 400/401/403/404, 422, 500",
            "Cursor pagination scales; offset pagination degrades at depth",
            "Version paths, validate at the boundary, keep error shapes consistent",
        ],
        "tag": "advanced",
        "quiz": [
            _quiz(
                "Which URL follows REST conventions?",
                ["POST /api/getUser", "GET /api/users/42", "GET /api/user?action=fetch", "DELETE /api/remove-user/42"],
                1,
                "REST names resources with nouns and uses HTTP methods for actions: GET /api/users/42 reads the user with id 42. Verbs in the URL (/getUser) are an anti-pattern.",
            ),
            _quiz(
                "What status code best fits 'the client sent a request missing a required field'?",
                ["200", "404", "422", "500"],
                2,
                "422 Unprocessable Entity means the request was well-formed but failed validation. 400 also works; the point is the failure is the client's fault, not 500 (server) or 404 (missing resource).",
            ),
            _quiz(
                "Why does cursor pagination scale better than offset pagination?",
                ["It returns fewer columns", "WHERE id > $cursor skips directly to the next batch instead of scanning past skipped rows", "It uses LIMIT 1", "It does not hit the database"],
                1,
                "Offset jumps (OFFSET 100000) still require the engine to find and discard 100000 rows. Keyset pagination on a unique indexed column jumps straight to the next rows — O(log n).",
            ),
        ],
        "exercise": _exercise(
            "Paginated todos endpoint",
            "Implement cursor pagination on GET /api/todos: accept limit and cursor query parameters, return rows with id greater than the cursor ordered by id, plus a next_cursor equal to the last returned id (null when the page is empty).",
            "app.get('/api/todos', async (req, res) => {\n  const limit = parseInt(req.query.limit || '20', 10);\n  // TODO: cursor pagination against the todos table\n});",
            "app.get('/api/todos', async (req, res) => {\n  const limit = parseInt(req.query.limit || '20', 10);\n  const cursor = parseInt(req.query.cursor || '0', 10);\n  const { rows } = await db.query(\n    'SELECT * FROM todos WHERE id > $1 ORDER BY id ASC LIMIT $2',\n    [cursor, limit]\n  );\n  res.json({\n    items: rows,\n    next_cursor: rows.length ? rows[rows.length - 1].id : null,\n  });\n});",
            "Keyset pagination: WHERE id > cursor ORDER BY id LIMIT n — the next cursor is the last returned id.",
        ),
        "curriculum": ["html", "css", "javascript", "react", "node", "sql"],
    },
]
INTERACTIVES = {
    # ────────────── quizzes + exercises for existing articles ──────────────
    "sql-select": {
        "quiz": [
            _quiz(
                "Which clause removes rows BEFORE they reach GROUP BY?",
                ["HAVING", "WHERE", "ORDER BY", "LIMIT"],
                1,
                "WHERE filters individual rows before any grouping; HAVING filters groups afterward and can see aggregates. Filter row-level, then group-level.",
            ),
            _quiz(
                "SELECT DISTINCT city FROM customers returns...",
                ["every city, sorted", "unique city values with duplicates removed", "a table with each city duplicated", "only NULL cities"],
                1,
                "DISTINCT removes duplicate rows from the RESULT — it does not delete data from the table. It is the quick way to list the set of unique values in a column.",
            ),
            _quiz(
                "A JOIN query returns far more rows than expected. Most likely cause?",
                ["LIMIT is too large", "Duplicate values in the join column create extra matches", "INNER vs LEFT semantics", "NULL columns"],
                1,
                "When the join key has duplicate values on either side, each pair is a match — duplicates multiply rows. Check for duplicate keys in the ON column.",
            ),
        ],
        "exercise": _exercise(
            "Top earners with their departments",
            "Write a query that returns the name, salary, and department name of the 5 highest-paid employees. Keep every employee even if their department is missing.",
            "SELECT e.name, e.salary\nFROM employees e\nORDER BY e.salary DESC;",
            "SELECT e.name, e.salary, d.name AS department\nFROM employees e\nLEFT JOIN departments d ON e.dept_id = d.id\nORDER BY e.salary DESC\nLIMIT 5;",
            "Add a LEFT JOIN to departments on e.dept_id = d.id, then LIMIT 5.",
        ),
    },
    "sql-database": {
        "quiz": [
            _quiz(
                "What does a foreign key enforce?",
                ["That values are unique across the table", "That a column references an existing row in another table", "That a column is never NULL", "That rows are stored in order"],
                1,
                "A foreign key points at a key in another table and blocks inserts that would create orphans, preserving referential integrity.",
            ),
            _quiz(
                "A many-to-many relationship is modeled with...",
                ["A single foreign key", "A join table holding two foreign keys", "One big table of duplicated data", "Two primary keys in one table"],
                1,
                "Many-to-many needs a join table whose rows pair a book_id with an author_id — two foreign keys, each pointing at one side.",
            ),
            _quiz(
                "The main cost of an index is...",
                ["slower reads", "slower writes and extra storage", "wrong query results", "NULLs being disallowed"],
                1,
                "Every write must maintain the index tree, so writes slow down, and the index itself consumes disk. Reads are the part that speeds up.",
            ),
        ],
        "exercise": _exercise(
            "Model a library",
            "Complete the schema: write the CREATE TABLE statements for books and a book_authors join table so that a book can have many authors and an author many books. The authors table is given.",
            "CREATE TABLE authors (\n  id SERIAL PRIMARY KEY,\n  name TEXT NOT NULL\n);",
            "CREATE TABLE books (\n  id SERIAL PRIMARY KEY,\n  title TEXT NOT NULL,\n  published_year INTEGER\n);\n\nCREATE TABLE book_authors (\n  book_id INTEGER REFERENCES books(id),\n  author_id INTEGER REFERENCES authors(id),\n  PRIMARY KEY (book_id, author_id)\n);",
            "The join table holds two foreign keys (book_id, author_id) and a composite primary key over both.",
        ),
    },
    "c-pointers": {
        "quiz": [
            _quiz(
                "What does the expression *p give you?",
                ["The address stored in p", "The value stored at the address p holds", "The address of p", "The size of p"],
                1,
                "*p dereferences p: it reads the memory at the address p stores. Without the *, p is just the address itself.",
            ),
            _quiz(
                "In int *p = &x; what does &x produce?",
                ["The value of x", "A copy of x", "The memory address of x", "The type of x"],
                2,
                "The address-of operator & yields x's memory location. That address is what the pointer variable p stores.",
            ),
            _quiz(
                "arr[i] is equivalent to...",
                ["*(arr + i)", "&arr[i]", "arr + i", "*arr + i"],
                0,
                "Subscripting is pointer arithmetic in disguise: an array name decays to a pointer to its first element, and arr[i] is shorthand for *(arr + i).",
            ),
        ],
        "exercise": _exercise(
            "Swap by pointer",
            "Complete swap so it truly exchanges the caller's variables, then call it in main to make x and y swap values.",
            "void swap(int *a, int *b) {\n  // TODO: swap the values that a and b point to\n}\n\nint main(void) {\n  int x = 3, y = 7;\n  swap(&x, &y);\n  printf(\"%d %d\\n\", x, y);   // expect 7 3\n  return 0;\n}",
            "void swap(int *a, int *b) {\n  int tmp = *a;\n  *a = *b;\n  *b = tmp;\n}\n\nint main(void) {\n  int x = 3, y = 7;\n  swap(&x, &y);\n  printf(\"%d %d\\n\", x, y);   // expect 7 3\n  return 0;\n}",
            "Dereference both pointers with * to read and write the caller's variables; keep a temporary copy of one value.",
        ),
    },
    "c-memory": {
        "quiz": [
            _quiz(
                "Which pair must balance out?",
                ["printf and scanf", "malloc and free", "open and write", "strcpy and strlen"],
                1,
                "Every block from malloc (or calloc/realloc) must eventually be freed. printf/scanf and open/write have no such pairing rule.",
            ),
            _quiz(
                "int *p = malloc(100); p = malloc(200); — what is wrong?",
                ["Nothing", "The first block leaks — its address is overwritten and lost", "A double free", "A stack overflow"],
                1,
                "The second assignment overwrites the only pointer to the first block, so free() can never reach it — that memory stays reserved forever.",
            ),
            _quiz(
                "What does calloc do that malloc does not?",
                ["It is faster", "It zero-initializes the allocated memory", "It resizes existing blocks", "It frees memory"],
                1,
                "calloc allocates AND zeroes every byte; malloc leaves the memory untouched, so it may contain garbage. realloc resizes; free releases.",
            ),
        ],
        "exercise": _exercise(
            "Allocate, fill, sum, free",
            "Allocate an array of 5 ints on the heap with malloc, check the result for NULL, fill it with 1..5, print the sum (15), and free it.",
            "#include <stdio.h>\n#include <stdlib.h>\n\nint main(void) {\n  // TODO: malloc 5 ints, check NULL, fill, sum, print, free\n  return 0;\n}",
            "#include <stdio.h>\n#include <stdlib.h>\n\nint main(void) {\n  int *arr = malloc(5 * sizeof(int));\n  if (arr == NULL) return 1;\n\n  int sum = 0;\n  for (int i = 0; i < 5; i++) {\n    arr[i] = i + 1;\n    sum += arr[i];\n  }\n  printf(\"%d\\n\", sum);   // 15\n\n  free(arr);\n  return 0;\n}",
            "malloc(5 * sizeof(int)) returns NULL on failure — always check before writing through the pointer.",
        ),
    },
    "c-enums-structs": {
        "quiz": [
            _quiz(
                "By default, enum Color { RED, GREEN, BLUE }; assigns what values?",
                ["1, 2, 3", "0, 1, 2", "R, G, B", "Random values"],
                1,
                "Enum constants start at 0 by default and increment by one. You can override: enum Weekday { MON = 1, ... }.",
            ),
            _quiz(
                "Given Student *p, how do you access the age field?",
                ["p.age", "p->age", "*p.age", "age.p"],
                1,
                "Through a pointer you use the arrow operator: p->age is shorthand for (*p).age. The dot operator works on struct VALUES, not pointers.",
            ),
            _quiz(
                "Passing a large struct to a function by value...",
                ["is always the best choice", "copies the whole struct — expensive", "is impossible", "is faster than passing a pointer"],
                1,
                "By-value parameters copy the entire struct onto the stack. For big structs, pass a pointer instead so only the address is copied.",
            ),
        ],
        "exercise": _exercise(
            "A Point type with addition",
            "Define a Point struct with two int fields (x and y), write add_points that returns a new Point, and print the sum of (1,2) + (3,4) which is (4,6).",
            "#include <stdio.h>\n\n// TODO: define Point, add_points, and main\n\nint main(void) {\n  return 0;\n}",
            "#include <stdio.h>\n\ntypedef struct {\n  int x, y;\n} Point;\n\nPoint add_points(Point a, Point b) {\n  Point r = { a.x + b.x, a.y + b.y };\n  return r;\n}\n\nint main(void) {\n  Point a = {1, 2}, b = {3, 4};\n  Point s = add_points(a, b);\n  printf(\"%d %d\\n\", s.x, s.y);   // 4 6\n  return 0;\n}",
            "A struct is a value — build the result with a compound literal and return it by value with return r;.",
        ),
    },
    "c-preprocessors-files": {
        "quiz": [
            _quiz(
                "What does #include <stdio.h> do?",
                ["Runs the file", "Pastes the header's contents before compilation", "Compiles a library", "Defines a macro"],
                1,
                "The preprocessor textually inserts the header's declarations before the compiler runs. The result of #define, on the other hand, is a macro.",
            ),
            _quiz(
                "Which file mode overwrites existing contents?",
                ["r", "a", "w", "r+"],
                2,
                "'w' truncates the file to zero length and starts fresh. 'r' reads, 'a' appends at the end, 'r+' opens for read/write without truncating.",
            ),
            _quiz(
                "Include guards (#ifndef/#define/#endif) exist to...",
                ["speed up compilation", "prevent a header from being included twice", "stop memory leaks", "add error handling"],
                1,
                "When two files both include a header that itself includes another, the guards ensure each header's body is pasted only once — avoiding duplicate definitions.",
            ),
        ],
        "exercise": _exercise(
            "Append a log line",
            "Open log.txt in append mode, write the line \"Score: 42\\n\", and close the file. Handle the case where fopen fails.",
            "#include <stdio.h>\n\nint main(void) {\n  // TODO: open log.txt in append mode, write \"Score: 42\\n\", close\n  return 0;\n}",
            "#include <stdio.h>\n\nint main(void) {\n  FILE *f = fopen(\"log.txt\", \"a\");\n  if (f == NULL) return 1;\n  fprintf(f, \"Score: %d\\n\", 42);\n  fclose(f);\n  return 0;\n}",
            "Use mode \"a\" for append and always check that fopen did not return NULL before writing.",
        ),
    },
    "fullstack-architecture": {
        "quiz": [
            _quiz(
                "In the request's journey, which layer receives an HTTP request first?",
                ["The SQL database", "The Express server route", "React's state", "The browser's cache"],
                1,
                "The browser sends HTTP to the server: React -> Express route -> SQL query -> JSON -> React re-render. The server is the first stop on the backend side.",
            ),
            _quiz(
                "The authoritative copy of data belongs to...",
                ["the React client", "the database", "localStorage", "the bundler"],
                1,
                "The database owns truth. The server validates and shapes it, React renders and caches it — but the database is the source of record.",
            ),
            _quiz(
                "Why do servers set auth tokens as httpOnly cookies?",
                ["They are larger that way", "Browser JavaScript cannot read them, blocking XSS theft", "The law requires it", "So clients can put them in URLs"],
                1,
                "httpOnly cookies are invisible to JavaScript, so a cross-site scripting attack cannot exfiltrate the token. The cookie rides along on every request automatically.",
            ),
        ],
        "exercise": _exercise(
            "Protect a route",
            "Write a requireAuth middleware that returns 401 when the Authorization header is missing, and calls next() to continue the chain when it is present.",
            "const requireAuth = (req, res, next) => {\n  // TODO: 401 when the Authorization header is missing, else next()\n};\n\napp.get('/api/me', requireAuth, (req, res) => {\n  res.json({ user: 'you' });\n});",
            "const requireAuth = (req, res, next) => {\n  if (!req.headers.authorization) {\n    return res.status(401).json({ error: 'missing token' });\n  }\n  next();\n};\n\napp.get('/api/me', requireAuth, (req, res) => {\n  res.json({ user: 'you' });\n});",
            "Check req.headers.authorization; call next() to pass control to the route handler.",
        ),
    },
}





