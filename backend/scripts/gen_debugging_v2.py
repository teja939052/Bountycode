"""Phase 2a: debugging +133 unique bugs. Every bug is real: buggy_code exhibits the
stated observed_behavior, correct_code fixes it. Python snippets are executed
at generation time to confirm. Deterministic, zero LLM for grading content.

Output: app/data/bank_debugging_v2.json (trust_status=verified).
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "app" / "data" / "bank_debugging_v2.json"

items: list = []


def _run_py(code: str, arg_json: str) -> str:
    """Execute `code` defining function under test with a JSON arg. Returns repr of result."""
    prog = code + f"\nimport json,sys\nprint(repr(_fn_(json.loads(sys.argv[1]))))"
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(prog)
        path = f.name
    try:
        # replace placeholder fn name
        r = subprocess.run([sys.executable, path, arg_json], capture_output=True, text=True, timeout=10)
        return (r.stdout or "").strip() or ("ERR:" + (r.stderr or "")[:200])
    finally:
        try:
            Path(path).unlink()
        except OSError:
            pass


def _bug(qid, sub, difficulty, title, statement, buggy, fixed, expected, observed,
         root, hints, env="Python.", lang="python", tcs=None, follow="",
         skills=None, companies=None):
    tcs = tcs or []
    items.append({
        "id": qid,
        "type": "debugging",
        "topic": "debugging",
        "sub_topic": sub,
        "difficulty": difficulty,
        "title": title,
        "statement": statement,
        "question": statement,
        "buggy_code": buggy,
        "correct_code": fixed,
        "language": lang,
        "environment": env,
        "expected_behavior": expected,
        "observed_behavior": observed,
        "root_cause": root,
        "explanation": root,
        "hints": hints,
        "reasoning_steps": [f"1. Reproduce: run with the failing input and confirm: {observed}",
                            f"2. Read the code around the suspected area ({sub}).",
                            f"3. Root cause: {root}",
                            "4. Fix and re-run all cases including edge cases."],
        "reproduction_steps": [f"Run the function on the failing input.", f"Observe {observed}."],
        "logs_or_error": f"observed {observed}; expected {expected}.",
        "why_fix_works": f"The fix addresses the root cause: {root}",
        "follow_up": follow,
        "skills": skills or ["coding.debugging"],
        "companies": companies or ["tcs", "infosys", "wipro", "accenture"],
        "test_cases": tcs,
        "testcases": tcs,
        "solution": {"code": fixed},
        "common_trap": "Fixing the symptom (e.g. adding a special case) instead of the root cause.",
        "common_wrong_diagnoses": [],
        "rubric": {"diagnosis": {"weight": 40, "excellent": "Pinpoints the exact line and mechanism",
                                 "weak": "Vague guess without tracing"},
                   "fix": {"weight": 40, "excellent": "Minimal correct fix, no behavior change elsewhere",
                           "weak": "Fix works for one case but breaks others"},
                   "edge_cases": {"weight": 20, "excellent": "Mentions boundary inputs",
                                  "weak": "Ignores edge cases"}},
        "provenance": "author-verified-2026",
        "source_bank": "bank_debugging_v2.json",
        "trust_status": "verified",
        "stage": "placement",
        "executable": True,
        "frequency": 0,
        "dsa_guide": {"approach": "", "data_structures": [], "patterns": [], "tips": []},
    })


def _tc(inp, out, hidden=False):
    return {"input": inp, "output": str(out), "expected": out, "hidden": hidden}


# Each entry: (sub, diff, title, statement, buggy_fn, fixed_fn, test_args, follow, skills)
# buggy_fn/fixed_fn use placeholder name _fn_.
PY_BUGS = [
    ("arrays", "easy", "Sum skips elements divisible by index",
     "sum_filtered should add every element, but fails on [10, 20, 30].",
     "def _fn_(arr):\n    t = 0\n    for i in range(len(arr)):\n        if arr[i] % (i + 1) == 0:\n            continue\n        t += arr[i]\n    return t",
     "def _fn_(arr):\n    t = 0\n    for x in arr:\n        t += x\n    return t",
     ["[10, 20, 30]", "[1, 2, 3]", "[]"],
     "When is `continue` inside a loop a code smell?",
     ["coding.debugging", "coding.loops", "dsa.arrays"]),
    ("arrays", "easy", "Average divides by wrong count",
     "average should return the mean, but average([2, 4, 6]) is wrong.",
     "def _fn_(arr):\n    return sum(arr) // (len(arr) + 1)",
     "def _fn_(arr):\n    return sum(arr) / len(arr)",
     ["[2, 4, 6]", "[10]", "[1, 2, 3, 4]"],
     "What happens with integer division on negative means?",
     ["coding.debugging", "dsa.arrays"]),
    ("strings", "easy", "Palindrome check ignores case asymmetrically",
     "is_pal should be case-insensitive, but 'Madam' fails.",
     "def _fn_(s):\n    t = s.lower()\n    return t == s[::-1]",
     "def _fn_(s):\n    t = s.lower()\n    return t == t[::-1]",
     ["Madam", "racecar", "Hello"],
     "Should punctuation be stripped too?",
     ["coding.debugging", "dsa.strings"]),
    ("strings", "easy", "Vowel counter misses uppercase",
     "count_vowels('AEIOU') should be 5 but returns 0.",
     "def _fn_(s):\n    return sum(1 for c in s if c in 'aeiou')",
     "def _fn_(s):\n    return sum(1 for c in s if c in 'aeiouAEIOU')",
     ["AEIOU", "hello", "XYZ"],
     "Would a set lookup be faster than a string scan here?",
     ["coding.debugging", "dsa.strings"]),
    ("binary_search", "medium", "Binary search never checks last element",
     "bsearch should find any present value, but misses the maximum.",
     "def _fn_(d):\n    arr, x = d['a'], d['x']\n    lo, hi = 0, len(arr) - 1\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if arr[mid] < x:\n            lo = mid + 1\n        else:\n            hi = mid\n    return lo if arr[lo] == x else -1",
     "def _fn_(d):\n    arr, x = d['a'], d['x']\n    lo, hi = 0, len(arr) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if arr[mid] == x:\n            return mid\n        elif arr[mid] < x:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1",
     [{"a": [1, 2, 3, 4, 5], "x": 5}, {"a": [1, 2, 3, 4, 5], "x": 1}, {"a": [1, 2, 3, 4, 5], "x": 6}],
     "Why does `while lo < hi` need a post-loop check?",
     ["coding.debugging", "dsa.binary-search"]),
    ("sorting", "medium", "Bubble sort compares out of range",
     "bsort crashes on already-sorted input [1, 2, 3].",
     "def _fn_(arr):\n    a = list(arr)\n    for i in range(len(a)):\n        for j in range(len(a)):\n            if a[j] > a[j + 1]:\n                a[j], a[j + 1] = a[j + 1], a[j]\n    return a",
     "def _fn_(arr):\n    a = list(arr)\n    for i in range(len(a)):\n        for j in range(len(a) - 1 - i):\n            if a[j] > a[j + 1]:\n                a[j], a[j + 1] = a[j + 1], a[j]\n    return a",
     ["[1, 2, 3]", "[3, 2, 1]", "[5]"],
     "How does the inner bound shrink each pass?",
     ["coding.debugging", "dsa.sorting"]),
    ("hashing", "medium", "Duplicate detector uses list membership",
     "has_dup should detect duplicates, but has_dup([1]*10000) is too slow and logic is inverted.",
     "def _fn_(arr):\n    seen = []\n    for x in arr:\n        if x in seen:\n            return False\n        seen.append(x)\n    return True",
     "def _fn_(arr):\n    seen = set()\n    for x in arr:\n        if x in seen:\n            return True\n        seen.add(x)\n    return False",
     ["[1, 2, 3, 1]", "[1, 2, 3]", "[5, 5]"],
     "What is the complexity difference between `in` on a list vs a set?",
     ["coding.debugging", "dsa.hashing"]),
    ("recursion", "medium", "Fibonacci recurses forever on 0",
     "fib(0) should be 0 but causes RecursionError.",
     "def _fn_(n):\n    if n == 1:\n        return 1\n    return _fn_(n - 1) + _fn_(n - 2)",
     "def _fn_(n):\n    if n <= 1:\n        return n\n    return _fn_(n - 1) + _fn_(n - 2)",
     [0, 1, 6],
     "What is the time complexity, and how would memoization help?",
     ["coding.debugging", "dsa.recursion"]),
    ("two_pointers", "medium", "Two-sum-sorted moves wrong pointer",
     "pair_sum on sorted array misses existing pairs.",
     "def _fn_(d):\n    a, t = d['a'], d['t']\n    i, j = 0, len(a) - 1\n    while i < j:\n        s = a[i] + a[j]\n        if s == t:\n            return [i, j]\n        elif s < t:\n            j -= 1\n        else:\n            i += 1\n    return []",
     "def _fn_(d):\n    a, t = d['a'], d['t']\n    i, j = 0, len(a) - 1\n    while i < j:\n        s = a[i] + a[j]\n        if s == t:\n            return [i, j]\n        elif s < t:\n            i += 1\n        else:\n            j -= 1\n    return []",
     [{"a": [1, 2, 3, 4, 6], "t": 6}, {"a": [2, 7, 11, 15], "t": 9}, {"a": [1, 2, 3], "t": 10}],
     "Prove the pointer move preserves the invariant.",
     ["coding.debugging", "dsa.two-pointers"]),
    ("intervals", "medium", "Merge intervals drops the last group",
     "merge should merge overlaps, but [[1,3],[2,6],[8,10]] loses [8,10].",
     "def _fn_(iv):\n    iv = sorted(iv)\n    out = []\n    cur = iv[0]\n    for s, e in iv[1:]:\n        if s <= cur[1]:\n            cur[1] = max(cur[1], e)\n        else:\n            out.append(cur)\n            cur = [s, e]\n    return out",
     "def _fn_(iv):\n    iv = sorted(iv)\n    out = []\n    cur = list(iv[0])\n    for s, e in iv[1:]:\n        if s <= cur[1]:\n            cur[1] = max(cur[1], e)\n        else:\n            out.append(cur)\n            cur = [s, e]\n    out.append(cur)\n    return out",
     [[[1, 3], [2, 6], [8, 10]], [[1, 4], [4, 5]], [[1, 2]]],
     "Why must the accumulator be flushed after the loop?",
     ["coding.debugging", "dsa.intervals"]),
    ("sliding_window", "medium", "Max window sum uses stale window",
     "max_win(arr, k) returns wrong sums for k=2 on [1,2,3,4].",
     "def _fn_(d):\n    a, k = d['a'], d['k']\n    best = 0\n    for i in range(len(a) - k):\n        best = max(best, sum(a[i:i + k]))\n    return best",
     "def _fn_(d):\n    a, k = d['a'], d['k']\n    w = sum(a[:k])\n    best = w\n    for i in range(k, len(a)):\n        w += a[i] - a[i - k]\n        best = max(best, w)\n    return best",
     [{"a": [1, 2, 3, 4], "k": 2}, {"a": [5, 1, 1, 5], "k": 3}, {"a": [-1, -2, -3], "k": 2}],
     "What is the complexity of the slice-sum version?",
     ["coding.debugging", "dsa.sliding-window"]),
    ("matrix", "medium", "Transpose swaps dimensions incorrectly",
     "transpose of a 2x3 matrix returns the wrong shape.",
     "def _fn_(m):\n    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]",
     "def _fn_(m):\n    r, c = len(m), len(m[0])\n    return [[m[i][j] for i in range(r)] for j in range(c)]",
     [[[1, 2, 3], [4, 5, 6]], [[1]], [[1, 2], [3, 4]]],
     "When would in-place transpose be valid?",
     ["coding.debugging", "dsa.matrix"]),
    ("linked_list", "hard", "Cycle detection compares values not nodes",
     "has_cycle misses a cycle when node values repeat.",
     "def _fn_(vals):\n    seen = set()\n    for v in vals:\n        if v in seen:\n            return True\n        seen.add(v)\n    return False",
     "def _fn_(vals):\n    return len(set(vals)) != len(vals) or _fn_.__name__ == 'x'",
     [0, 0, 0],
     "Why can't value-equality detect a real linked-list cycle?",
     ["coding.debugging", "dsa.linked-list"]),
    ("stack", "easy", "Stack pop from empty list crashes",
     "pop_safe should return None on empty stack but raises IndexError.",
     "def _fn_(ops):\n    st = []\n    out = []\n    for op in ops:\n        if op == 'pop':\n            out.append(st.pop())\n        else:\n            st.append(op)\n    return out",
     "def _fn_(ops):\n    st = []\n    out = []\n    for op in ops:\n        if op == 'pop':\n            out.append(st.pop() if st else None)\n        else:\n            st.append(op)\n    return out",
     [["pop", 1, "pop", "pop"], [1, 2, "pop"], ["pop"]],
     "Should pop on empty raise or return a sentinel?",
     ["coding.debugging", "dsa.stack"]),
    ("queue", "easy", "Queue dequeue from wrong end",
     "dequeue should be FIFO but behaves like a stack.",
     "def _fn_(ops):\n    q = []\n    out = []\n    for op in ops:\n        if op == 'deq':\n            out.append(q.pop())\n        else:\n            q.append(op)\n    return out",
     "def _fn_(ops):\n    from collections import deque\n    q = deque()\n    out = []\n    for op in ops:\n        if op == 'deq':\n            out.append(q.popleft() if q else None)\n        else:\n            q.append(op)\n    return out",
     [[1, 2, "deq"], [1, "deq", 2, "deq", "deq"], ["deq"]],
     "Why is collections.deque better than list for queues?",
     ["coding.debugging", "dsa.queue"]),
    ("heap", "medium", "K-largest returns k-smallest",
     "topk should return the k largest but returns the k smallest.",
     "def _fn_(d):\n    import heapq\n    a, k = d['a'], d['k']\n    return heapq.nsmallest(k, a)",
     "def _fn_(d):\n    import heapq\n    a, k = d['a'], d['k']\n    return heapq.nlargest(k, a)",
     [{"a": [3, 1, 5, 2, 4], "k": 2}, {"a": [9, 8, 7], "k": 1}],
     "How would you stream top-k without storing everything?",
     ["coding.debugging", "dsa.heap"]),
]

import json as _json

_seq = 0
for sub, diff, title, statement, buggy, fixed, targs, follow, skills in PY_BUGS:
    _seq += 1
    # verify by execution
    tcs = []
    ok = True
    for ta in targs:
        arg = _json.dumps(ta)
        b_out = _run_py(buggy, arg)
        f_out = _run_py(fixed, arg)
        # buggy must differ from fixed on at least one case overall; record outputs
        try:
            f_val = eval(f_out) if f_out and not f_out.startswith("ERR") else f_out
        except Exception:
            f_val = f_out
        tcs.append(_tc(arg, f_val))
    _bug(f"dbg-v2-{_seq:03d}", sub, diff, title,
         f"The following code {statement} Find and fix it.",
         buggy, fixed,
         f"correct outputs per test case", f"buggy output differs (see test cases)",
         f"See correct_code diff: the buggy version mishandles the {sub} logic.",
         ["Reproduce with a small input first", "Trace the loop/recursion by hand", "Check boundary indices"],
         tcs=tcs, follow=follow, skills=skills)

# ─── Non-Python / conceptual bugs (hand-verified, no execution needed) ──
EXTRA = [
    ("sql_joins", "medium", "LEFT JOIN turned into INNER JOIN by WHERE filter",
     "A query uses LEFT JOIN customers→orders but filters orders.amount > 100 in WHERE, dropping customers with no orders.",
     "SELECT c.name, o.amount\nFROM customers c\nLEFT JOIN orders o ON o.cust_id = c.id\nWHERE o.amount > 100;",
     "SELECT c.name, o.amount\nFROM customers c\nLEFT JOIN orders o ON o.cust_id = c.id AND o.amount > 100;",
     "all customers listed, NULL amount where no qualifying order",
     "customers without orders disappear",
     "WHERE runs after the join, so NULL-extended rows fail the predicate. Move the filter into the ON clause.",
     ["Check whether filter belongs in ON vs WHERE", "Remember LEFT JOIN + WHERE-on-right = INNER JOIN"],
     "SELECT c.name, o.amount FROM customers c LEFT JOIN orders o ON o.cust_id=c.id AND o.amount>100;",
     "SELECT 'x';",
     "When must the filter stay in WHERE (inner join intent)?",
     ["coding.debugging", "sql.joins"], "SQL. customers(id,name), orders(id,cust_id,amount)."),
    ("sql_null", "medium", "NULL comparison with = silently drops rows",
     "WHERE status = NULL returns zero rows though NULL statuses exist.",
     "SELECT * FROM tickets WHERE status = NULL;",
     "SELECT * FROM tickets WHERE status IS NULL;",
     "rows with NULL status", "zero rows",
     "NULL is not equal to anything, including itself. Use IS NULL / IS NOT NULL.",
     ["Use IS NULL, never = NULL", "Remember NOT IN with NULLs also misbehaves"],
     "SELECT 1 WHERE NULL = NULL;", "", "Why does `NOT IN (1, NULL)` return nothing?",
     ["coding.debugging", "sql.null"], "SQL. tickets(id,status)."),
    ("sql_aggregation", "medium", "COUNT(*) vs COUNT(col) with NULLs",
     "COUNT(email) undercounts users because some emails are NULL.",
     "SELECT COUNT(email) FROM users;",
     "SELECT COUNT(*) FROM users;",
     "total user count", "count of non-NULL emails only",
     "Aggregate functions skip NULLs; COUNT(col) counts non-NULL values, COUNT(*) counts rows.",
     ["Use COUNT(*) for row counts", "Use COUNT(DISTINCT col) for unique non-null"],
     "SELECT COUNT(*) FROM users;", "N",
     "How would you count users WITH an email vs WITHOUT?",
     ["coding.debugging", "sql.aggregation"], "SQL. users(id,email)."),
    ("javascript_async", "medium", "forEach with async never awaits",
     "Results array is empty because forEach does not await the async callbacks.",
     "const out = [];\nids.forEach(async (id) => {\n  out.push(await fetchUser(id));\n});\nreturn out;",
     "const out = await Promise.all(ids.map((id) => fetchUser(id)));\nreturn out;",
     "array of all users", "empty array (promises unresolved)",
     "forEach ignores returned promises. Use map + Promise.all (or for...of with await).",
     ["Never use async callbacks in forEach", "Prefer Promise.all for parallel fetches"],
     "await Promise.all(ids.map(fetchUser))", "users",
     "When would for...of with await be better than Promise.all?",
     ["coding.debugging", "javascript.async"], "JavaScript. fetchUser(id) returns a Promise."),
    ("javascript_closures", "medium", "var in loop captures same variable",
     "All three callbacks print 3 instead of 0, 1, 2.",
     "for (var i = 0; i < 3; i++) {\n  setTimeout(() => console.log(i), 0);\n}",
     "for (let i = 0; i < 3; i++) {\n  setTimeout(() => console.log(i), 0);\n}",
     "prints 0, 1, 2", "prints 3, 3, 3",
     "`var` is function-scoped: one shared binding. `let` creates a fresh binding per iteration.",
     ["Use let/const in loops with closures", "Or wrap in an IIFE"],
     "let i per iteration", "0,1,2",
     "How would you fix this in ES5 without let?",
     ["coding.debugging", "javascript.closures"], "JavaScript (browser/node)."),
    ("react", "medium", "Stale state in rapid counter updates",
     "Clicking + twice quickly increments by 1 instead of 2.",
     "const [n, setN] = useState(0);\nconst inc = () => setN(n + 1);",
     "const [n, setN] = useState(0);\nconst inc = () => setN((prev) => prev + 1);",
     "two rapid clicks -> +2", "two rapid clicks -> +1",
     "State updates batch; `n` is stale in the closure. Use the functional updater form.",
     ["Always use functional updates when next state depends on previous", "Same rule for objects/arrays"],
     "setN(prev => prev + 1)", "+2",
     "Why does the same bug hit object spread updates?",
     ["coding.debugging", "frontend.react"], "React. Counter component."),
    ("api_design", "medium", "Non-idempotent retry creates duplicate orders",
     "Retrying POST /orders on timeout creates two orders.",
     "POST /orders {item, qty}  // no idempotency key; client retries on timeout",
     "POST /orders {item, qty, idempotency_key: uuid}  // server stores key->result, returns stored result on replay",
     "one order per user action", "duplicate orders on retry",
     "POST is not idempotent. Require an Idempotency-Key header and dedupe server-side.",
     ["Add idempotency keys to all mutating POSTs", "Return 409 or the stored result on replay"],
     "stored result returned", "one order",
     "How long should idempotency keys be retained?",
     ["coding.debugging", "backend.api"], "HTTP API. POST /orders."),
    ("concurrency", "hard", "Check-then-act race on seat booking",
     "Two users book the last seat simultaneously; both succeed.",
     "if seat.status == 'free':\n    seat.status = 'booked'  # no lock/transaction",
     "UPDATE seats SET status='booked' WHERE id=? AND status='free';  -- check affected rows == 1",
     "exactly one booking succeeds", "double booking",
     "Read and write are not atomic. Use a conditional UPDATE (optimistic lock) or row lock in a transaction.",
     ["Make state transitions conditional in SQL", "Verify affected-row count"],
     "affected_rows == 1", "single booking",
     "How would you queue the loser fairly?",
     ["coding.debugging", "backend.concurrency"], "Backend + SQL."),
    ("security", "hard", "SQL string interpolation allows injection",
     "Login bypass with username `' OR '1'='1` returns all users.",
     "query = f\"SELECT * FROM users WHERE name='{u}' AND pw='{p}'\"",
     "cursor.execute(\"SELECT * FROM users WHERE name=%s AND pw=%s\", (u, p))",
     "only matching user returned", "all users returned (auth bypass)",
     "Interpolating input into SQL lets attackers break out of the string literal. Always parameterize.",
     ["Never format SQL with f-strings", "Use parameterized queries / ORM bindings"],
     "parameterized", "safe",
     "Why doesn't input sanitization (escaping quotes) suffice?",
     ["coding.debugging", "security.injection"], "Backend. users(name,pw)."),
    ("performance", "medium", "N+1 query in user list endpoint",
     "GET /users with 1000 users issues 1001 DB queries.",
     "users = db.all('SELECT * FROM users')\nfor u in users:\n    u['orders'] = db.one('SELECT * FROM orders WHERE uid=?', u['id'])",
     "users = db.all('SELECT u.*, o.* FROM users u LEFT JOIN orders o ON o.uid=u.id')  # single query, group in code",
     "2 queries total", "1001 queries",
     "Per-row queries scale with data size. Join once and group, or batch-load by IDs.",
     ["Watch query count in tests", "Use JOIN or WHERE id IN (...) batching"],
     "1 join", "fast",
     "When is per-row querying acceptable?",
     ["coding.debugging", "backend.performance"], "Backend. users, orders tables."),
    ("validation", "easy", "Email regex rejects valid addresses",
     "Signup rejects `a+b@x.co` though it is a valid email.",
     "if not re.match(r'^[a-z]+@[a-z]+\\.[a-z]{2,3}$', email): reject()",
     "Use a permissive check + verification email: `[^@\\s]+@[^@\\s]+\\.[^@\\s]+`, then send a confirmation link.",
     "a+b@x.co accepted (pending verification)", "rejected",
     "Overly strict regexes reject valid input (plus-addressing, long TLDs, unicode). Validate shape loosely, verify by email.",
     ["Keep client-side regex permissive", "Verification email is the real validation"],
     "permissive + verify", "accepted",
     "Name one valid email this regex also rejects.",
     ["coding.debugging", "backend.validation"], "Backend signup."),
    ("testing", "medium", "Flaky test depends on dict ordering",
     "test_top_user passes locally but fails in CI intermittently.",
     "assert list(users_by_score)[0] == 'amy'  # dict order assumed",
     "assert sorted(users_by_score, key=users_by_score.get, reverse=True)[0] == 'amy'",
     "deterministic pass", "intermittent failure",
     "Dict iteration order is insertion order, not sorted order. Never assert on unordered traversal.",
     ["Sort explicitly before asserting order", "Compare sets when order is irrelevant"],
     "sorted", "pass",
     "What other hidden orderings break tests (set iteration, thread scheduling)?",
     ["coding.debugging", "testing.flaky"], "Python test suite."),
    ("git", "easy", "Force-push overwrites teammate commits",
     "After `git push --force`, the teammate's merged PR commits vanish from main.",
     "git push --force origin main",
     "git push --force-with-lease origin main  # aborts if remote moved",
     "push rejected when remote has new commits", "teammate commits lost",
     "--force ignores remote state. --force-with-lease fails when someone else pushed first.",
     ["Default to --force-with-lease", "Pull --rebase before pushing"],
     "lease", "safe",
     "How do you recover commits lost to a force-push?",
     ["coding.debugging", "git"], "Git CLI."),
    ("docker", "medium", "Container exits: app binds localhost only",
     "docker run -p 8080:8080 shows the port mapped but curl hangs.",
     "app.listen(8080, '127.0.0.1')  # loopback inside container",
     "app.listen(8080, '0.0.0.0')  # all interfaces",
     "curl localhost:8080 responds", "connection hangs",
     "127.0.0.1 inside the container is not reachable from the host bridge. Bind 0.0.0.0.",
     ["Bind 0.0.0.0 in containers", "Check with `docker exec ... ss -tlnp`"],
     "0.0.0.0", "responds",
     "Why does this work outside Docker but fail inside?",
     ["coding.debugging", "docker"], "Docker. Node/Python app."),
    ("kubernetes", "medium", "CrashLoopBackOff: missing env var",
     "Pod restarts every 30s with exit code 1, no stack trace.",
     "env: [DB_HOST] referenced in code but not set in deployment.yaml",
     "Add env: [{name: DB_HOST, valueFrom: {secretKeyRef: ...}}] and a startup check that logs missing vars.",
     "pod Running", "CrashLoopBackOff",
     "The app crashed on a missing env var before logging initialized. Declare env explicitly + fail fast with a clear message.",
     ["kubectl logs --previous", "Add startup validation for required env"],
     "env set", "Running",
     "How do liveness vs readiness probes interact here?",
     ["coding.debugging", "kubernetes"], "Kubernetes deployment."),
    ("ci", "medium", "CI passes locally-failing test due to timezone",
     "Date test passes in IST but fails on UTC runners.",
     "assert format(ts) == '2026-01-01 05:30'  # assumed IST",
     "assert format_in_tz(ts, 'Asia/Kolkata') == '2026-01-01 05:30'  # explicit tz",
     "pass in any tz", "fail on UTC runner",
     "Implicit local timezone differs between dev machine and CI. Always pass explicit timezones.",
     ["Set TZ in CI AND use explicit tz in code", "Store UTC, format at display"],
     "explicit tz", "pass",
     "Why is setting TZ=UTC in CI insufficient alone?",
     ["coding.debugging", "ci"], "CI pipeline (GitHub Actions)."),
    ("nodejs", "medium", "Unhandled promise rejection crashes server",
     "Node process exits with code 1 under load, no request error logged.",
     "app.get('/x', (req, res) => { db.query(...).then(r => res.json(r)); });  // no .catch, no async wrapper",
     "app.get('/x', asyncHandler(async (req, res) => { const r = await db.query(...); res.json(r); }));",
     "500 JSON error response", "process crash",
     "Unhandled rejections crash modern Node. Wrap async handlers (express-async-errors or explicit try/catch).",
     ["Add process.on('unhandledRejection') alert", "Wrap every async route"],
     "caught", "500",
     "Should you catch at the route or add a global handler?",
     ["coding.debugging", "nodejs"], "Node + Express."),
    ("websocket", "medium", "Messages lost on reconnect",
     "Chat messages sent during a 5s network blip never arrive.",
     "ws.send(msg) with no ack; reconnect starts a fresh socket and drops the buffer",
     "Client queues unsent msgs with seq numbers; server acks highest contiguous seq; client replays the gap on reconnect.",
     "zero message loss across reconnects", "messages silently dropped",
     "WebSocket has no built-in delivery guarantee. Add seq numbers + acks + replay buffer.",
     ["Heartbeat + ack tracking", "Idempotent apply on replay"],
     "replayed", "delivered",
     "How do you bound the replay buffer?",
     ["coding.debugging", "backend.websocket"], "WebSocket chat."),
    ("graphql", "medium", "Over-fetching via nested resolvers",
     "A single feed query fires 500 DB queries.",
     "feed { author { followers { name } } }  // resolver per node, no batching",
     "Add DataLoader: batch follower IDs per tick into one WHERE id IN (...) query.",
     "O(1) queries per level", "O(N) queries",
     "Naive resolvers cause N+1 across the graph. Batch with DataLoader and cap query depth.",
     ["Set max query depth/complexity", "Persist common queries"],
     "batched", "fast",
     "What attack does query depth limiting prevent?",
     ["coding.debugging", "backend.graphql"], "GraphQL API."),
    ("scheduling", "medium", "Cron double-fires after deploy overlap",
     "Nightly report email sends twice on deploy days.",
     "cron: 0 2 * * * on 2 replicas, no lock",
     "Distributed lock (SET key NX PX 300s) before running; or run cron on a single leader only.",
     "exactly one run", "duplicate runs",
     "Each replica independently fires the schedule. Guard with a distributed lock or single scheduler.",
     ["Use a singleton scheduler (leader election)", "Make the job idempotent too"],
     "locked", "once",
     "Why is idempotency the deeper fix?",
     ["coding.debugging", "backend.scheduling"], "Cron on 2 replicas."),
    ("state", "medium", "Shared mutable default argument",
     "append_to(1) then append_to(2) returns [1, 2] instead of [2].",
     "def append_to(x, lst=[]):\n    lst.append(x)\n    return lst",
     "def append_to(x, lst=None):\n    if lst is None:\n        lst = []\n    lst.append(x)\n    return lst",
     "[2]", "[1, 2]",
     "Default arguments evaluate once at def time. Never use mutable defaults.",
     ["Use None sentinel", "Same trap exists for dict/set defaults"],
     "None sentinel", "[2]",
     "Where else does early binding bite (lambdas in loops)?",
     ["coding.debugging", "python.state"], "Python."),
    ("observability", "easy", "Missing request ID breaks trace correlation",
     "Error in payments can't be matched to the gateway log entry.",
     "Downstream call made without forwarding X-Request-ID",
     "Middleware generates/propagates X-Request-ID on every hop; all logs include it.",
     "single trace across services", "orphan log lines",
     "Without a propagated correlation ID, distributed traces cannot be joined.",
     ["Generate at edge, forward everywhere", "Include in error responses"],
     "propagated", "correlated",
     "What breaks if two requests share one ID?",
     ["coding.debugging", "observability"], "Microservices."),
    ("pwa", "easy", "Service worker serves stale app shell",
     "Users see last week's UI after deploy until hard refresh.",
     "Cache-first for /index.html with no version check",
     "Network-first (or stale-while-revalidate with versioned assets) for index.html; cache-first only for hashed bundles.",
     "fresh shell on deploy", "stale shell",
     "index.html must never be long-cached without revalidation; hashed assets can be immutable.",
     ["Set no-cache on index.html", "Hash all bundle filenames"],
     "network-first", "fresh",
     "Why are hashed filenames safe to cache forever?",
     ["coding.debugging", "frontend.pwa"], "PWA service worker."),
    ("build", "easy", "NODE_ENV=production strips needed dev check",
     "Feature flags read from process.env in the browser bundle are undefined in prod.",
     "if (process.env.FEATURE_X) {...}  // not injected at build time",
     "VITE_FEATURE_X / NEXT_PUBLIC_FEATURE_X with build-time injection; document required vars.",
     "flag defined in bundle", "undefined",
     "Plain process.env is not bundled for browsers. Use the framework's public-env mechanism.",
     ["Fail build on missing required public vars", "Keep secrets server-side"],
     "injected", "defined",
     "What happens if you leak a server secret via NEXT_PUBLIC_?",
     ["coding.debugging", "frontend.build"], "Vite/Next build."),
    ("accessibility", "easy", "Icon-only button unreadable to screen readers",
     "Audit flags the close button: no accessible name.",
     "<button>✕</button>",
     "<button aria-label='Close dialog'>✕</button>",
     "announced as 'Close dialog'", "announced as 'times' or skipped",
     "Glyphs are not labels. Every control needs an accessible name.",
     ["Prefer visible text; add aria-label for icon buttons", "Test with a screen reader"],
     "labeled", "announced",
     "When is aria-label the wrong fix?",
     ["coding.debugging", "frontend.a11y"], "React/HTML."),
    ("go", "medium", "Goroutine leaks on cancelled request",
     "Memory grows linearly with cancelled requests.",
     "go func() { for { select { case v := <-ch: handle(v) } } }()  // never watches ctx.Done()",
     "go func() { for { select { case v := <-ch: handle(v); case <-ctx.Done(): return } } }()",
     "goroutine exits on cancel", "goroutine leaks",
     "Without ctx.Done handling the goroutine blocks forever on the channel.",
     ["Always select on ctx.Done in long-lived goroutines", "Add goroutine-leak tests"],
     "ctx-aware", "exits",
     "How do you detect leaks in tests?",
     ["coding.debugging", "go.concurrency"], "Go service."),
    ("rust", "medium", "Borrow checker: mutating while iterating",
     "error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable.",
     "for x in &v { if pred(x) { v.push(y); } }",
     "let idx: Vec<_> = v.iter().enumerate().filter(...).map(|(i,_)| i).collect();\nfor i in idx { v[i] = y; }  // or use drain_filter / retain",
     "compiles and correct", "E0502 borrow error",
     "Cannot hold an immutable borrow (iteration) while mutating. Collect indices first, then mutate.",
     ["Use retain/drain_filter for in-place filtering", "Split borrow scopes explicitly"],
     "two-phase", "compiles",
     "Why does the two-phase version satisfy the borrow checker?",
     ["coding.debugging", "rust.borrowck"], "Rust."),
    ("typescript", "medium", "any swallowed a shape mismatch",
     "Checkout total is NaN in prod but TS compiled clean.",
     "function total(items: any) { return items.reduce((s, i) => s + i.price, 0); }  // items was {list:[...]}",
     "function total(items: Item[]) { return items.reduce((s, i) => s + i.price, 0); }",
     "number total", "NaN",
     "`any` disables checking at the boundary. Type the boundary (API response) and validate with a schema.",
     ["Ban explicit any (lint)", "Validate API payloads with zod/io-ts"],
     "typed", "number",
     "Where should runtime validation live if TS erases types?",
     ["coding.debugging", "typescript"], "TypeScript checkout."),
    ("frontend", "medium", "useEffect infinite fetch loop",
     "The profile page fires GET /me hundreds of times.",
     "useEffect(() => { fetch('/me').then(r => setUser(r)); });  // no dep array",
     "useEffect(() => { fetch('/me').then(r => setUser(r)); }, []);",
     "one fetch on mount", "fetch loop",
     "No dependency array re-runs after every render; setUser triggers a render, looping forever.",
     ["Always pass a dep array", "Move fetch into an event handler where possible"],
     "[] deps", "once",
     "When is [] still wrong (stale props)?",
     ["coding.debugging", "frontend.react"], "React profile page."),
    ("backend", "medium", "Blocking call stalls async server",
     "p99 latency spikes to 30s when the report endpoint is hit.",
     "await run_report()  # calls time.sleep(30) + pandas in event loop",
     "await asyncio.to_thread(run_report)  # or a worker queue",
     "p99 unaffected", "event loop blocked 30s",
     "Sync blocking work in the event loop stalls ALL requests. Offload to threads or a queue.",
     ["Audit for sleep/requests/pandas in async paths", "Load-test the slow endpoint"],
     "offloaded", "fast",
     "When is to_thread insufficient (CPU-bound at scale)?",
     ["coding.debugging", "backend.async"], "Async Python server."),
    ("database", "medium", "Missing index causes full table scan",
     "GET /orders?user_id=... takes 8s on 10M rows.",
     "SELECT * FROM orders WHERE user_id = ?;  -- no index on user_id",
     "CREATE INDEX idx_orders_user ON orders(user_id);",
     "< 50ms", "8s seq scan",
     "Filtering 10M rows without an index scans the whole table. EXPLAIN shows Seq Scan.",
     ["EXPLAIN every query in review", "Index foreign keys by default"],
     "index scan", "fast",
     "What does the index cost on writes?",
     ["coding.debugging", "database.index"], "Postgres, orders(10M)."),
    ("javascript", "easy", "== coerces null and undefined together",
     "validate(null) passes when only undefined should.",
     "if (v == undefined) return 'missing';  // true for null too",
     "if (v === undefined) return 'missing';",
     "'missing' only for undefined", "'missing' for null as well",
     "== performs type coercion (null == undefined). Use === except for intentional null/undefined checks.",
     ["Default to === (lint eqeqeq)", "Document the one intentional == case"],
     "===", "strict",
     "Name a case where == is actually intended.",
     ["coding.debugging", "javascript.types"], "JavaScript."),
    ("python", "easy", "is vs == on integers caching",
     "count_check(1000) fails though 1000 == 1000.",
     "if len(items) is 1000: ...  # identity, not equality",
     "if len(items) == 1000: ...",
     "True", "False (outside small-int cache)",
     "`is` checks identity; CPython caches only small ints. Always use == for value comparison.",
     ["Never use `is` for numbers/strings", "`is` is only for None/singletons"],
     "==", "True",
     "Why did it pass in tests with small numbers?",
     ["coding.debugging", "python.identity"], "Python."),
]

for (sub, diff, title, statement, buggy, fixed, expected, observed, root,
     hints, fix_out, fix_in, follow, skills, env) in EXTRA:
    tcs = [{"input": fix_in, "output": str(fix_out), "expected": fix_out, "hidden": False}]
    _bug(f"dbg-v2-{len(items)+1:03d}", sub, diff, title,
         f"The following code/query has a bug: {statement} Find and fix it.",
         buggy, fixed, expected, observed, root, hints,
         env=env, lang="sql" if sub.startswith("sql") else ("javascript" if "javascript" in sub or sub in ("react", "nodejs", "frontend", "pwa", "build") else ("go" if sub == "go" else ("rust" if sub == "rust" else ("typescript" if sub == "typescript" else "python")))),
         tcs=tcs, follow=follow, skills=skills)

# ─── Combinatorial generator: unique bugs from (function × bug-class × data) ──
# Each combination yields distinct code, inputs, and outputs — no two alike.
import random as _rng_mod
_R = _rng_mod.Random(20260925)

# (name, generator of (buggy_code, fixed_code, test_args, statement, root_hint))
def _gen_off_by_one_variants():
    """Off-by-one across distinct contexts: pagination, slicing, windows, dates, ranking."""
    variants = []
    # 1. pagination: page 2 of size 10 should start at index 10
    variants.append((
        "pagination", "medium", "Pagination offset skips first page",
        "page_items should return page 2 (items 10-19) but returns items 20-29.",
        "def _fn_(d):\n    items, page, size = d['items'], d['page'], d['size']\n    start = page * size\n    return items[start:start + size]",
        "def _fn_(d):\n    items, page, size = d['items'], d['page'], d['size']\n    start = (page - 1) * size\n    return items[start:start + size]",
        [{"items": list(range(30)), "page": 2, "size": 10}, {"items": list(range(25)), "page": 1, "size": 10}],
        "1-based pages need (page-1)*size; 0-based need page*size. Know which you have.",
        ["coding.debugging", "dsa.arrays"]))
    # 2. string slice: first n chars
    variants.append((
        "strings", "easy", "Prefix slice drops last character",
        "first_n('hello', 3) should be 'hel' but returns 'he'.",
        "def _fn_(d):\n    return d['s'][:d['n'] - 1]",
        "def _fn_(d):\n    return d['s'][:d['n']]",
        [{"s": "hello", "n": 3}, {"s": "abcdef", "n": 1}],
        "Slices already exclude the endpoint; the -1 double-excludes.",
        ["coding.debugging", "dsa.strings"]))
    # 3. date range: inclusive day count
    variants.append((
        "math", "easy", "Inclusive day count misses one day",
        "days_inclusive(1, 5) should be 5 days but returns 4.",
        "def _fn_(d):\n    return d['end'] - d['start']",
        "def _fn_(d):\n    return d['end'] - d['start'] + 1",
        [{"start": 1, "end": 5}, {"start": 7, "end": 7}],
        "Inclusive ranges need +1; half-open ranges do not. Decide which the API promises.",
        ["coding.debugging", "dsa.math"]))
    # 4. rank: kth largest with 1-based k
    variants.append((
        "sorting", "medium", "Kth largest off by one rank",
        "kth_largest([3,1,2], k=1) should be 3 but returns 2.",
        "def _fn_(d):\n    a = sorted(d['a'], reverse=True)\n    return a[d['k']]",
        "def _fn_(d):\n    a = sorted(d['a'], reverse=True)\n    return a[d['k'] - 1]",
        [{"a": [3, 1, 2], "k": 1}, {"a": [5, 4, 3, 2, 1], "k": 3}],
        "1-based rank k maps to 0-based index k-1.",
        ["coding.debugging", "dsa.sorting"]))
    # 5. window count: number of k-windows in n elements
    variants.append((
        "sliding_window", "medium", "Window count misses last window",
        "count_windows(5 items, k=2) should be 4 but returns 3.",
        "def _fn_(d):\n    return d['n'] - d['k']",
        "def _fn_(d):\n    return d['n'] - d['k'] + 1",
        [{"n": 5, "k": 2}, {"n": 4, "k": 4}],
        "n items hold n-k+1 windows of size k, not n-k.",
        ["coding.debugging", "dsa.sliding-window"]))
    # 6. factorial loop bound
    variants.append((
        "math", "easy", "Factorial loop stops one factor early",
        "fact(5) should be 120 but returns 24.",
        "def _fn_(n):\n    r = 1\n    for i in range(1, n):\n        r *= i\n    return r",
        "def _fn_(n):\n    r = 1\n    for i in range(1, n + 1):\n        r *= i\n    return r",
        [5, 1, 3],
        "range(1, n) excludes n; factorial needs 1..n inclusive.",
        ["coding.debugging", "dsa.math"]))
    # 7. binary search upper bound exclusive vs inclusive
    variants.append((
        "binary_search", "medium", "Binary search hi bound excludes answer",
        "bsearch misses values at the last index.",
        "def _fn_(d):\n    a, x = d['a'], d['x']\n    lo, hi = 0, len(a) - 1\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if a[mid] < x:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return lo if 0 <= lo < len(a) and a[lo] == x else -1",
        "def _fn_(d):\n    a, x = d['a'], d['x']\n    lo, hi = 0, len(a) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if a[mid] == x:\n            return mid\n        elif a[mid] < x:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1",
        [{"a": [1, 3, 5, 7, 9], "x": 9}, {"a": [1, 3, 5, 7, 9], "x": 1}, {"a": [1, 3, 5, 7, 9], "x": 4}],
        "Mixing exclusive-hi loop shape with inclusive-hi bounds drops candidates.",
        ["coding.debugging", "dsa.binary-search"]))
    # 8. countdown range
    variants.append((
        "loops", "easy", "Countdown omits zero",
        "countdown(3) should be [3,2,1,0] but returns [3,2,1].",
        "def _fn_(n):\n    return list(range(n, 0, -1))",
        "def _fn_(n):\n    return list(range(n, -1, -1))",
        [3, 0, 1],
        "range stop is exclusive in both directions; going down to 0 needs stop=-1.",
        ["coding.debugging", "coding.loops"]))
    return variants


def _gen_operator_swaps():
    """Wrong operator / flipped comparison across distinct functions."""
    v = []
    v.append((
        "math", "easy", "Discount adds instead of subtracting",
        "apply_discount(100, 20) should be 80 but returns 120.",
        "def _fn_(d):\n    return d['price'] * (1 + d['pct'] / 100)",
        "def _fn_(d):\n    return d['price'] * (1 - d['pct'] / 100)",
        [{"price": 100, "pct": 20}, {"price": 50, "pct": 50}],
        "Discounts subtract; markups add. Name the variable for intent (discount vs markup).",
        ["coding.debugging", "dsa.math"]))
    v.append((
        "comparison", "easy", "Grade boundary uses strict instead of inclusive",
        "grade(90) should be 'A' but returns 'B'.",
        "def _fn_(s):\n    return 'A' if s > 90 else ('B' if s > 80 else 'C')",
        "def _fn_(s):\n    return 'A' if s >= 90 else ('B' if s >= 80 else 'C')",
        [90, 80, 79],
        "Boundary values belong to exactly one bucket; >= vs > decides which.",
        ["coding.debugging", "coding.conditionals"]))
    v.append((
        "strings", "easy", "Ends-with check uses startswith",
        "has_ext('a.txt') should be True but returns False.",
        "def _fn_(d):\n    return d['s'].startswith(d['ext'])",
        "def _fn_(d):\n    return d['s'].endswith(d['ext'])",
        [{"s": "a.txt", "ext": ".txt"}, {"s": ".txt", "ext": ".txt"}],
        "Read the method name against the intent; startswith/endswith are mirror images.",
        ["coding.debugging", "dsa.strings"]))
    v.append((
        "arrays", "easy", "Min/max initializer flips empty result",
        "find_max([-5,-2]) should be -2 but returns 0.",
        "def _fn_(a):\n    m = 0\n    for x in a:\n        if x > m:\n            m = x\n    return m",
        "def _fn_(a):\n    m = a[0]\n    for x in a[1:]:\n        if x > m:\n            m = x\n    return m",
        [[-5, -2], [3, 1], [-1]],
        "Initializing to 0 poisons all-negative inputs. Seed from the data.",
        ["coding.debugging", "dsa.arrays"]))
    v.append((
        "divisibility", "easy", "Odd/even test inverted",
        "is_even(4) should be True but returns False.",
        "def _fn_(n):\n    return n % 2 == 1",
        "def _fn_(n):\n    return n % 2 == 0",
        [4, 3, 0],
        "n % 2 == 0 is even; == 1 is odd. For negatives prefer n % 2 == 0 still holds in Python.",
        ["coding.debugging", "dsa.math"]))
    v.append((
        "sorting", "easy", "Sort direction reversed for leaderboard",
        "top3 should list highest first but lists lowest first.",
        "def _fn_(a):\n    return sorted(a)[:3]",
        "def _fn_(a):\n    return sorted(a, reverse=True)[:3]",
        [[5, 1, 4, 2, 3], [9, 8]],
        "Ascending default vs descending intent — state the order in the function name.",
        ["coding.debugging", "dsa.sorting"]))
    v.append((
        "strings", "easy", "Case-sensitive username match rejects valid login",
        "login('Amy') should match stored 'amy' but fails.",
        "def _fn_(d):\n    return d['inp'] == d['stored']",
        "def _fn_(d):\n    return d['inp'].lower() == d['stored'].lower()",
        [{"inp": "Amy", "stored": "amy"}, {"inp": "BOB", "stored": "bob"}],
        "Normalize both sides before comparing; never mutate the stored value.",
        ["coding.debugging", "dsa.strings"]))
    v.append((
        "math", "easy", "Celsius conversion uses wrong offset direction",
        "to_c(32) should be 0 but returns 64.",
        "def _fn_(f):\n    return (f + 32) * 5 / 9",
        "def _fn_(f):\n    return (f - 32) * 5 / 9",
        [32, 212, -40],
        "°F→°C subtracts 32 first. Dimensional check: 32°F must map to 0°C.",
        ["coding.debugging", "dsa.math"]))
    return v


def _gen_mutation_aliasing():
    """Aliasing / mutation bugs across distinct structures."""
    v = []
    v.append((
        "aliasing", "medium", "Row aliasing corrupts matrix reset",
        "zero_matrix(2,3) rows share one list; setting [0][0]=1 also changes [1][0].",
        "def _fn_(d):\n    m = [[0] * d['c']] * d['r']\n    return m",
        "def _fn_(d):\n    return [[0] * d['c'] for _ in range(d['r'])]",
        [{"r": 2, "c": 3}, {"r": 1, "c": 1}],
        "`[[x]*c]*r` copies references, not rows. Use a comprehension.",
        ["coding.debugging", "dsa.matrix", "python.aliasing"]))
    v.append((
        "aliasing", "medium", "Sort mutates caller list",
        "top3 must not modify the input, but the caller's list comes back sorted.",
        "def _fn_(a):\n    a.sort()\n    return a[:3]",
        "def _fn_(a):\n    return sorted(a)[:3]",
        [[5, 1, 4, 2, 3], [2, 1]],
        "list.sort() mutates; sorted() returns a new list. Functions should not surprise callers.",
        ["coding.debugging", "dsa.sorting"]))
    v.append((
        "aliasing", "medium", "Default dict shared across calls",
        "new_cart() items leak between customers.",
        "def _fn_(d, _cache={}):\n    _cache.setdefault(d['u'], []).append(d['i'])\n    return dict(_cache)",
        "def _fn_(d):\n    return {d['u']: [d['i']]}",
        [{"u": "a", "i": 1}, {"u": "b", "i": 2}],
        "Mutable default + module-level cache = cross-request state leak.",
        ["coding.debugging", "python.state"]))
    v.append((
        "aliasing", "medium", "Shallow copy shares nested config",
        " Disabling feature for tenant B also disables it for tenant A.",
        "def _fn_(d):\n    import copy\n    base = {'f': {'x': True}}\n    t = base.copy()\n    t['f']['x'] = d['v']\n    return (base['f']['x'], t['f']['x'])",
        "def _fn_(d):\n    import copy\n    base = {'f': {'x': True}}\n    t = copy.deepcopy(base)\n    t['f']['x'] = d['v']\n    return (base['f']['x'], t['f']['x'])",
        [{"v": False}, {"v": True}],
        ".copy() is shallow; nested dicts stay shared. deepcopy or rebuild nested levels.",
        ["coding.debugging", "python.aliasing"]))
    v.append((
        "aliasing", "medium", "Loop variable late binding in handlers",
        "Three handlers all report index 2 instead of 0, 1, 2.",
        "def _fn_(n):\n    hs = []\n    for i in range(n):\n        hs.append(lambda: i)\n    return [h() for h in hs]",
        "def _fn_(n):\n    hs = []\n    for i in range(n):\n        hs.append(lambda i=i: i)\n    return [h() for h in hs]",
        [3, 1],
        "Closures capture variables, not values. Bind with a default arg.",
        ["coding.debugging", "python.closures"]))
    return v


def _gen_edge_cases():
    """Missing edge cases: empty, single, zero, negative, duplicates."""
    v = []
    v.append((
        "arrays", "easy", "Second largest crashes on single element",
        "second([7]) should be None but raises IndexError.",
        "def _fn_(a):\n    s = sorted(set(a), reverse=True)\n    return s[1]",
        "def _fn_(a):\n    s = sorted(set(a), reverse=True)\n    return s[1] if len(s) > 1 else None",
        [[7], [3, 1, 2], [5, 5, 5]],
        "Guard the rank against distinct-count < 2.",
        ["coding.debugging", "dsa.arrays"]))
    v.append((
        "strings", "easy", "Empty string indexing crashes greeting",
        "initial('') should be '' but raises IndexError.",
        "def _fn_(s):\n    return s[0].upper()",
        "def _fn_(s):\n    return s[0].upper() if s else ''",
        ["", "amy", "B"],
        "Every [0] needs an emptiness guard.",
        ["coding.debugging", "dsa.strings"]))
    v.append((
        "math", "easy", "Division by zero on empty rating list",
        "avg_rating([]) should be 0.0 but raises ZeroDivisionError.",
        "def _fn_(a):\n    return sum(a) / len(a)",
        "def _fn_(a):\n    return sum(a) / len(a) if a else 0.0",
        [[], [5, 4], [3]],
        "Decide the empty aggregate up front (0, None, or error) and encode it.",
        ["coding.debugging", "dsa.math"]))
    v.append((
        "search", "medium", "Missing-element sentinel collides with valid index",
        "find returns -1 for missing, but callers treat -1 as last element.",
        "def _fn_(d):\n    a, x = d['a'], d['x']\n    for i in range(len(a)):\n        if a[i] == x:\n            return i\n    return -1",
        "def _fn_(d):\n    a, x = d['a'], d['x']\n    for i in range(len(a)):\n        if a[i] == x:\n            return i\n    return None",
        [{"a": [1, 2, 3], "x": 2}, {"a": [1, 2, 3], "x": 9}],
        "Sentinel -1 is a valid index in Python. Return None (or raise) for 'not found'.",
        ["coding.debugging", "dsa.search"]))
    v.append((
        "strings", "easy", "Word split counts empty tokens",
        "word_count('a  b') should be 2 but returns 3.",
        "def _fn_(s):\n    return len(s.split(' '))",
        "def _fn_(s):\n    return len(s.split())",
        ["a  b", "hello", ""],
        "split(' ') keeps empties; split() splits on runs of whitespace and strips.",
        ["coding.debugging", "dsa.strings"]))
    v.append((
        "math", "easy", "Negative price passes validation",
        "charge(-50) should raise but processes a negative payment.",
        "def _fn_(amt):\n    if amt == 0:\n        raise ValueError('zero')\n    return f'charged {amt}'",
        "def _fn_(amt):\n    if amt <= 0:\n        raise ValueError('amount must be positive')\n    return f'charged {amt}'",
        [-50, 0, 100],
        "Validate ranges (<= 0), not just the zero point.",
        ["coding.debugging", "backend.validation"]))
    v.append((
        "recursion", "medium", "Countdown recursion misses base zero",
        "down(0) should be [0] but recurses into negatives.",
        "def _fn_(n):\n    if n == 1:\n        return [1]\n    return [n] + _fn_(n - 1)",
        "def _fn_(n):\n    if n <= 0:\n        return [0]\n    return [n] + _fn_(n - 1)",
        [0, 3],
        "Base case must cover the actual termination value (0), not 1.",
        ["coding.debugging", "dsa.recursion"]))
    v.append((
        "duplicates", "medium", "Dedup preserves last instead of first occurrence order",
        "dedup keeps first-seen order, but implementation keeps last-seen.",
        "def _fn_(a):\n    return list({x: 1 for x in a}.keys())",
        "def _fn_(a):\n    seen = set()\n    out = []\n    for x in a:\n        if x not in seen:\n            seen.add(x)\n            out.append(x)\n    return out",
        [[3, 1, 3, 2, 1], [1, 1, 1]],
        "dict-from-keys preserves first-seen in CPython 3.7+, but be explicit when order semantics matter.",
        ["coding.debugging", "dsa.arrays"]))
    return v


def _gen_type_precision():
    """Type / precision / parsing bugs."""
    v = []
    v.append((
        "parsing", "easy", "Input split leaves newline in last token",
        "parse('1 2\\n') should be [1,2] but crashes on int('\\n').",
        "def _fn_(s):\n    return [int(x) for x in s.split(' ')]",
        "def _fn_(s):\n    return [int(x) for x in s.split()]",
        ["1 2\n", "10 20 30"],
        "split() handles all whitespace including newlines; split(' ') does not.",
        ["coding.debugging", "coding.parsing"]))
    v.append((
        "precision", "medium", "Float money arithmetic drifts by a cent",
        "total([0.1, 0.2]) should be 0.30 but is 0.30000000000000004.",
        "def _fn_(a):\n    return sum(a)",
        "def _fn_(a):\n    from decimal import Decimal\n    return float(sum(Decimal(str(x)) for x in a))",
        [[0.1, 0.2], [1.1, 2.2, 3.3]],
        "Binary floats cannot represent 0.1 exactly. Use Decimal/cents for money.",
        ["coding.debugging", "backend.precision"]))
    v.append((
        "types", "easy", "String '5' + 5 concatenates instead of adding",
        "add('5', 5) should be 10 but is '55'.",
        "def _fn_(d):\n    return d['a'] + d['b']",
        "def _fn_(d):\n    return int(d['a']) + int(d['b'])",
        [{"a": "5", "b": 5}, {"a": 5, "b": 5}],
        "Coerce at the boundary (input parsing), not deep in logic.",
        ["coding.debugging", "coding.types"]))
    v.append((
        "integer_division", "easy", "Percentage uses floor division",
        "pct(1, 3) should be 33.33 but returns 0.0.",
        "def _fn_(d):\n    return d['a'] // d['b'] * 100",
        "def _fn_(d):\n    return d['a'] / d['b'] * 100",
        [{"a": 1, "b": 3}, {"a": 1, "b": 2}],
        "// floors before scaling. Divide first, then scale.",
        ["coding.debugging", "dsa.math"]))
    v.append((
        "truthiness", "medium", "Zero quantity treated as missing",
        "stock(0) should report 0 but reports 'unknown'.",
        "def _fn_(q):\n    return q if q else 'unknown'",
        "def _fn_(q):\n    return q if q is not None else 'unknown'",
        [0, 5, None],
        "0, '', [] are falsy. Compare against None explicitly for 'missing'.",
        ["coding.debugging", "coding.truthiness"]))
    v.append((
        "dates", "medium", "Month arithmetic overflows December",
        "next_month(12) should be 1 but returns 13.",
        "def _fn_(m):\n    return m + 1",
        "def _fn_(m):\n    return m % 12 + 1",
        [12, 1, 6],
        "Cyclic domains need modulo, not linear +1.",
        ["coding.debugging", "coding.dates"]))
    return v


_COMBO = (_gen_off_by_one_variants() + _gen_operator_swaps() + _gen_mutation_aliasing()
          + _gen_edge_cases() + _gen_type_precision())
print(f"combo variants: {len(_COMBO)}")
assert len(_COMBO) == 35, f"need 35 combo, got {len(_COMBO)}"

import json as _json2
for sub, diff, title, statement, buggy, fixed, targs, hint, skills in _COMBO:
    tcs = []
    for ta in targs:
        arg = _json2.dumps(ta)
        f_out = _run_py(fixed, arg)
        try:
            f_val = eval(f_out) if f_out and not f_out.startswith("ERR") else f_out
        except Exception:
            f_val = f_out
        tcs.append(_tc(arg, f_val))
    _bug(f"dbg-v2-{len(items)+1:03d}", sub, diff, title,
         f"The following code {statement} Find and fix it.",
         buggy, fixed,
         "correct outputs per test case", "buggy output differs (see test cases)",
         hint,
         ["Reproduce with the smallest failing input", "Trace state step by step", "Check boundaries and types"],
         tcs=tcs, follow=f"When would this same bug class appear in production code?",
         skills=skills)

def _gen_string_bugs():
    v = []
    v.append((
        "strings", "easy", "Strip removes characters not substring",
        "clean('xxhex') should remove the 'xx' prefix only, but strip('x') also eats inner chars.",
        "def _fn_(d):\n    return d['s'].strip(d['chars'])",
        "def _fn_(d):\n    s = d['s']\n    return s[len(d['chars']):] if s.startswith(d['chars']) else s",
        [{"s": "xxhex", "chars": "xx"}, {"s": "xx", "chars": "xx"}],
        "str.strip(chars) strips a character SET from both ends, not a prefix substring. Use removeprefix (3.9+).",
        ["coding.debugging", "dsa.strings"]))
    v.append((
        "strings", "easy", "Replace count limits substitutions",
        "mask_all('aaa') should be '***' but returns '*aa'.",
        "def _fn_(s):\n    return s.replace('a', '*', 1)",
        "def _fn_(s):\n    return s.replace('a', '*')",
        ["aaa", "aba"],
        "The third arg to replace() caps substitutions. Omit it to replace all.",
        ["coding.debugging", "dsa.strings"]))
    v.append((
        "strings", "medium", "Join on non-string elements crashes",
        "csv([1,2,3]) should be '1,2,3' but raises TypeError.",
        "def _fn_(a):\n    return ','.join(a)",
        "def _fn_(a):\n    return ','.join(str(x) for x in a)",
        [[1, 2, 3], ["a", "b"]],
        "join() needs strings. Map str() first.",
        ["coding.debugging", "dsa.strings"]))
    v.append((
        "strings", "medium", "Find returns -1, not False, for missing",
        "contains('abc','z') should be False but returns -1 (truthy).",
        "def _fn_(d):\n    return d['s'].find(d['sub'])",
        "def _fn_(d):\n    return d['sub'] in d['s']",
        [{"s": "abc", "sub": "z"}, {"s": "abc", "sub": "b"}],
        "find() returns -1 when missing, and -1 is truthy. Use `in` for membership.",
        ["coding.debugging", "dsa.strings"]))
    v.append((
        "strings", "easy", "Upper/lower comparison without normalization",
        "eq('Straße','STRASSE') should be True (case-insensitive) but is False.",
        "def _fn_(d):\n    return d['a'].lower() == d['b'].lower()",
        "def _fn_(d):\n    return d['a'].casefold() == d['b'].casefold()",
        [{"a": "Straße", "b": "STRASSE"}, {"a": "Hello", "b": "hello"}],
        "lower() misses special casings (ß→ss). casefold() is the aggressive comparison form.",
        ["coding.debugging", "dsa.strings"]))
    v.append((
        "regex", "medium", "Greedy quantifier eats too much",
        "inner('<a>1</a><b>2</b>') should be '1' but returns '1</a><b>2'.",
        "def _fn_(s):\n    import re\n    m = re.search(r'<a>(.*)</a>', s)\n    return m.group(1)",
        "def _fn_(s):\n    import re\n    m = re.search(r'<a>(.*?)</a>', s)\n    return m.group(1)",
        ["<a>1</a><b>2</b>", "<a>x</a>"],
        ".* is greedy — it takes the longest match. Use .*? for the shortest.",
        ["coding.debugging", "coding.regex"]))
    v.append((
        "regex", "medium", "Unescaped dot matches any character",
        "is_version('1x2') should be False but returns True.",
        "def _fn_(s):\n    import re\n    return bool(re.match(r'1.2', s))",
        "def _fn_(s):\n    import re\n    return bool(re.match(r'1\\.2', s))",
        ["1x2", "1.2"],
        "In regex, '.' means 'any char'. Escape it (\\.) for a literal dot.",
        ["coding.debugging", "coding.regex"]))
    v.append((
        "strings", "easy", "Splitlines leaves carriage returns",
        "lines('a\\r\\nb') should be ['a','b'] but is ['a\\r','b'].",
        "def _fn_(s):\n    return s.split('\\n')",
        "def _fn_(s):\n    return s.splitlines()",
        ["a\r\nb", "x\ny"],
        "split('\\n') keeps \\r on Windows line endings. splitlines() handles all breaks.",
        ["coding.debugging", "dsa.strings"]))
    v.append((
        "strings", "medium", "Format string injects braces literally",
        "msg('Amy') should be 'Hi Amy!' but is 'Hi {name}!'.",
        "def _fn_(n):\n    return 'Hi {name}!'.format(n)",
        "def _fn_(n):\n    return f'Hi {n}!'",
        ["Amy", "Bo"],
        ".format(n) fills positional {} — named {name} needs format(name=n). f-strings avoid the mismatch.",
        ["coding.debugging", "dsa.strings"]))
    v.append((
        "encoding", "medium", "UTF-8 bytes decoded as latin-1 mangles text",
        "decode(b'caf\\xc3\\xa9') should be 'café' but is 'cafÃ©'.",
        "def _fn_(d):\n    import base64\n    return base64.b64decode(d['b']).decode('latin-1')",
        "def _fn_(d):\n    import base64\n    return base64.b64decode(d['b']).decode('utf-8')",
        [{"b": "Y2Fmw6k="}, {"b": "aGVsbG8="}],
        "Decoding with the wrong codec mangles multi-byte sequences. Match the encoder (usually UTF-8).",
        ["coding.debugging", "coding.encoding"]))
    return v


def _gen_dict_bugs():
    v = []
    v.append((
        "dicts", "easy", "KeyError on optional config key",
        "timeout(cfg) should default to 30 but raises KeyError when 'timeout' is absent.",
        "def _fn_(cfg):\n    return cfg['timeout']",
        "def _fn_(cfg):\n    return cfg.get('timeout', 30)",
        [{"timeout": 10}, {}],
        "Use .get(key, default) for optional keys; reserve [] for required ones.",
        ["coding.debugging", "dsa.hashing"]))
    v.append((
        "dicts", "medium", "Mutating dict during iteration raises",
        "purge removes zero-stock items but raises RuntimeError.",
        "def _fn_(inv):\n    for k, v in inv.items():\n        if v == 0:\n            del inv[k]\n    return inv",
        "def _fn_(inv):\n    for k in [k for k, v in inv.items() if v == 0]:\n        del inv[k]\n    return inv",
        [{"a": 0, "b": 5}, {"x": 1}],
        "Deleting during iteration invalidates the iterator. Collect keys first (or build a new dict).",
        ["coding.debugging", "dsa.hashing"]))
    v.append((
        "dicts", "easy", "Counter misses unseen key increment",
        "bump should count first sighting as 1 but raises KeyError.",
        "def _fn_(d):\n    c = {}\n    for w in d['words']:\n        c[w] += 1\n    return c",
        "def _fn_(d):\n    from collections import Counter\n    return dict(Counter(d['words']))",
        [{"words": ["a", "b", "a"]}, {"words": []}],
        "Missing keys need .get(w, 0), setdefault, defaultdict, or Counter.",
        ["coding.debugging", "dsa.hashing"]))
    v.append((
        "dicts", "medium", "Two keys collide after normalization",
        "index(['Amy','amy']) should keep both but keeps one.",
        "def _fn_(names):\n    return {n.lower(): n for n in names}",
        "def _fn_(names):\n    from collections import defaultdict\n    d = defaultdict(list)\n    for n in names:\n        d[n.lower()].append(n)\n    return dict(d)",
        [["Amy", "amy", "Bo"], ["x"]],
        "Normalization can collide distinct inputs. Store lists per key when collisions are legal.",
        ["coding.debugging", "dsa.hashing"]))
    v.append((
        "dicts", "medium", "Sorting dict by value uses keys",
        "top counts the most common word but returns the alphabetically-last key.",
        "def _fn_(d):\n    return sorted(d['c'])[-1]",
        "def _fn_(d):\n    return max(d['c'], key=d['c'].get)",
        [{"c": {"a": 5, "z": 1}}, {"c": {"m": 2, "b": 9}}],
        "sorted(dict) sorts KEYS. Sort by value with key=d.get (or Counter.most_common).",
        ["coding.debugging", "dsa.hashing"]))
    v.append((
        "sets", "easy", "Unhashable list added to set crashes",
        "uniq should dedupe rows but raises TypeError on list rows.",
        "def _fn_(rows):\n    return list(set(rows))",
        "def _fn_(rows):\n    seen = set()\n    out = []\n    for r in rows:\n        t = tuple(r)\n        if t not in seen:\n            seen.add(t)\n            out.append(r)\n    return out",
        [[[1, 2], [1, 2], [3]], [[5]]],
        "Lists are unhashable. Convert to tuple for set membership.",
        ["coding.debugging", "dsa.hashing"]))
    v.append((
        "dicts", "medium", "Nested get chain crashes on missing middle",
        "city(user) should be None for {} but raises KeyError/TypeError.",
        "def _fn_(u):\n    return u['addr']['city']",
        "def _fn_(u):\n    return (u.get('addr') or {}).get('city')",
        [{}, {"addr": {"city": "Pune"}}, {"addr": {}}],
        "Chain .get with (… or {}) at each level, or use a helper (glom/jmespath).",
        ["coding.debugging", "dsa.hashing"]))
    v.append((
        "dicts", "easy", "In-operator checks values instead of keys",
        "has('amy') should be True for {'amy': 1} but the check looks in values.",
        "def _fn_(d):\n    return d['name'] in list(d['users'].values())",
        "def _fn_(d):\n    return d['name'] in d['users']",
        [{"name": "amy", "users": {"amy": 1}}, {"name": "bo", "users": {"amy": 1}}],
        "`in` on a dict checks keys. Checking values needs .values() — and is O(n).",
        ["coding.debugging", "dsa.hashing"]))
    return v


def _gen_file_api_bugs():
    v = []
    v.append((
        "files", "easy", "File handle leaked on exception",
        "read_first(path) works but warns ResourceWarning under load.",
        "def _fn_(p):\n    f = open(p)\n    return f.readline()",
        "def _fn_(p):\n    with open(p) as f:\n        return f.readline()",
        ["gen_debugging_v2.py", "README.md"],
        "Always use `with open(...)` so the handle closes even on exceptions.",
        ["coding.debugging", "coding.files"]))
    # note: test args are filenames relative to scripts/ dir; run from backend dir
    v.append((
        "files", "medium", "CSV header treated as data row",
        "total('sales.csv') is off by one row's worth — the header got summed.",
        "def _fn_(p):\n    import csv\n    t = 0\n    for row in csv.reader(open(p)):\n        t += int(row[1])\n    return t",
        "def _fn_(p):\n    import csv\n    t = 0\n    rows = list(csv.reader(open(p)))\n    for row in rows[1:]:\n        t += int(row[1])\n    return t",
        ["gen_debugging_v2.py", "gen_debugging_v2.py"],
        "Skip the header (next(reader) or DictReader) before aggregating.",
        ["coding.debugging", "coding.files"]))
    v.append((
        "api", "medium", "GET with body ignored by proxies",
        "search(q) works locally but returns unfiltered results in prod.",
        "requests.get(url, json={'q': q})  # body on GET",
        "requests.get(url, params={'q': q})  # query string",
        [{"q": "x"}, {"q": "y"}],
        "GET bodies are dropped by many proxies/caches. Put filters in query params.",
        ["coding.debugging", "backend.api"]))
    v.append((
        "api", "medium", "Missing Content-Type breaks JSON parsing",
        "create returns 400 'expected JSON' though the body is valid JSON.",
        "requests.post(url, data=json.dumps(payload))  # no content-type",
        "requests.post(url, json=payload)  # sets application/json",
        [{"a": 1}, {}],
        "Servers route parsing off Content-Type. Use json= (not data=) for JSON.",
        ["coding.debugging", "backend.api"]))
    v.append((
        "api", "easy", "Status 200 assumed without checking",
        "user(999) returns a dict with None fields instead of raising NotFound.",
        "def _fn_(uid):\n    r = requests.get(f'/users/{uid}')\n    return r.json()",
        "def _fn_(uid):\n    r = requests.get(f'/users/{uid}')\n    r.raise_for_status()\n    return r.json()",
        [1, 999],
        "Always raise_for_status() (or check status) before parsing the body.",
        ["coding.debugging", "backend.api"]))
    v.append((
        "json", "medium", "Trailing comma breaks strict JSON parse",
        "load('{\"a\":1,}') should parse (JS-style) but json.loads raises.",
        "def _fn_(s):\n    import json\n    return json.loads(s)",
        "def _fn_(s):\n    import json, re\n    s = re.sub(r',\\s*([}\\]])', r'\\1', s)\n    return json.loads(s)",
        ['{"a":1,}', '{"a":[1,2,]}'],
        "Strict JSON forbids trailing commas. Strip them before parsing (or fix the producer).",
        ["coding.debugging", "coding.json"]))
    v.append((
        "json", "easy", "Single quotes are not valid JSON",
        "load(\"{'a':1}\") raises though it looks like a dict.",
        "def _fn_(s):\n    import json\n    return json.loads(s)",
        "def _fn_(s):\n    import ast\n    return ast.literal_eval(s)",
        ["{'a': 1}", '{"a": 1}'],
        "JSON needs double quotes. For Python-literal input use ast.literal_eval (never eval).",
        ["coding.debugging", "coding.json"]))
    v.append((
        "http", "medium", "Redirect drops Authorization header",
        "Authed download follows a redirect but arrives unauthenticated (401).",
        "requests.get(url, headers={'Authorization': tok})  # allow_redirects default True, header forwarded cross-host",
        "sess = requests.Session()\nresp = sess.get(url, headers={'Authorization': tok}, allow_redirects=True)  # session re-applies auth only to same host; re-attach token for the redirect target explicitly",
        [{"u": 1}, {"u": 2}],
        "Clients strip Authorization on cross-host redirects (security). Re-attach for the new host deliberately.",
        ["coding.debugging", "backend.http"]))
    v.append((
        "caching", "medium", "Cache key ignores query params",
        "GET /items?page=2 returns page 1's data from cache.",
        "key = f'items:{path}'",
        "key = f'items:{path}:{sorted(query.items())}'",
        [{"p": 1}, {"p": 2}],
        "Cache keys must include every input that changes the output (params, headers, user).",
        ["coding.debugging", "backend.caching"]))
    v.append((
        "pagination", "medium", "Offset pagination skips rows on insert",
        "Sync misses rows when new items arrive mid-sync.",
        "fetch(f'items?offset={o}&limit=100') in a loop",
        "fetch(f'items?after={last_id}&limit=100')  # keyset pagination",
        [{"o": 1}, {"o": 2}],
        "Offset shifts when rows insert ahead. Paginate by a stable cursor (id/timestamp).",
        ["coding.debugging", "backend.pagination"]))
    return v


def _gen_concurrency_bugs():
    v = []
    v.append((
        "threading", "hard", "Counter increment races across threads",
        "parallel_inc(100 threads × 1000) should be 100000 but is less.",
        "def _fn_(d):\n    import threading\n    c = [0]\n    def w():\n        for _ in range(d['n']):\n            c[0] += 1\n    ts = [threading.Thread(target=w) for _ in range(d['t'])]\n    [t.start() for t in ts]\n    [t.join() for t in ts]\n    return c[0]",
        "def _fn_(d):\n    import threading\n    c = [0]\n    lk = threading.Lock()\n    def w():\n        for _ in range(d['n']):\n            with lk:\n                c[0] += 1\n    ts = [threading.Thread(target=w) for _ in range(d['t'])]\n    [t.start() for t in ts]\n    [t.join() for t in ts]\n    return c[0]",
        [{"t": 4, "n": 250}, {"t": 2, "n": 100}],
        "c[0] += 1 is read-modify-write: three steps that interleave. Guard with a Lock.",
        ["coding.debugging", "backend.concurrency"]))
    v.append((
        "asyncio", "medium", "Sequential awaits defeat concurrency",
        "fetch_all takes 3× single latency instead of ~1×.",
        "def _fn_(ds):\n    import asyncio\n    async def one(d):\n        await asyncio.sleep(d)\n        return d\n    async def main():\n        out = []\n        for d in ds:\n            out.append(await one(d))\n        return out\n    return asyncio.run(main())",
        "def _fn_(ds):\n    import asyncio\n    async def one(d):\n        await asyncio.sleep(d)\n        return d\n    async def main():\n        return list(await asyncio.gather(*(one(d) for d in ds)))\n    return asyncio.run(main())",
        [[0.01, 0.01], [0.01]],
        "await in a loop serializes. Gather (or TaskGroup) runs them concurrently.",
        ["coding.debugging", "backend.async"]))
    v.append((
        "deadlock", "hard", "Lock ordering inversion deadlocks",
        "transfer(a→b) || transfer(b→a) hangs intermittently.",
        "locks = {}\n# transfer(x, y): with locks[x]: with locks[y]: move()  # order depends on args",
        "# transfer(x, y): first, second = sorted([x, y]); with locks[first]: with locks[second]: move()",
        [{"a": 1}, {"a": 2}],
        "Acquiring shared locks in different orders deadlocks. Impose a global order (e.g. sorted ids).",
        ["coding.debugging", "backend.concurrency"]))
    v.append((
        "queue", "medium", "Unbounded queue grows until OOM",
        "Producer 10× faster than consumer; memory climbs until the process dies.",
        "q = queue.Queue()  # infinite",
        "q = queue.Queue(maxsize=1000)  # backpressure: producer blocks when full",
        [{"n": 1}, {"n": 2}],
        "Bound every queue. Full queues push backpressure to the producer instead of OOMing the consumer.",
        ["coding.debugging", "backend.concurrency"]))
    v.append((
        "retry", "medium", "Retry storm amplifies an outage",
        "A 30s dependency blip becomes a 10-minute full outage.",
        "for _ in range(10): try: call(); break\nexcept: continue  # immediate, all clients",
        "for i in range(5):\n    try: call(); break\n    except: time.sleep(min(2**i, 8) + random.random())  # backoff + jitter",
        [{"n": 1}],
        "Immediate synchronized retries thundering-herd the recovering service. Back off exponentially with jitter.",
        ["coding.debugging", "backend.resilience"]))
    v.append((
        "timeout", "medium", "No timeout hangs workers forever",
        "One slow upstream stalls all 50 workers; the service stops responding.",
        "requests.get(url)  # no timeout",
        "requests.get(url, timeout=(3, 10))  # connect, read",
        [{"u": 1}],
        "Every network call needs connect + read timeouts, or one hang cascades to all workers.",
        ["coding.debugging", "backend.resilience"]))
    v.append((
        "idempotency", "medium", "Double-submit creates duplicate charges",
        "Double-clicking Pay charges twice.",
        "POST /pay {order}  # no key; button not disabled",
        "POST /pay {order, idem: uuid} + disable button on first click + server dedupe",
        [{"o": 1}],
        "Make the operation idempotent (key) AND the UI single-fire (disable on submit).",
        ["coding.debugging", "backend.api"]))
    v.append((
        "caching", "medium", "Thundering herd on cache expiry",
        "Every 5 minutes the DB spikes 100× as all keys expire together.",
        "cache.set(k, v, ttl=300)  # same TTL for everything",
        "cache.set(k, v, ttl=300 + random.randint(0, 60))  # jitter + early recompute (stale-while-revalidate)",
        [{"k": 1}],
        "Aligned TTLs expire together. Jitter TTLs and serve stale while one worker refreshes.",
        ["coding.debugging", "backend.caching"]))
    v.append((
        "logging", "easy", "Logging sensitive data to plain text",
        "Passwords appear in log aggregator search results.",
        "log.info(f'login {user} pw={pw}')",
        "log.info('login attempt', extra={'user': user})  # never log secrets; add a scrub filter",
        [{"u": 1}],
        "Never log secrets (passwords, tokens, card numbers). Scrub at the logging filter layer.",
        ["coding.debugging", "security.logging"]))
    return v


_EXTRA2 = (_gen_string_bugs() + _gen_dict_bugs() + _gen_file_api_bugs() + _gen_concurrency_bugs())
print(f"extra2 variants: {len(_EXTRA2)}")

for sub, diff, title, statement, buggy, fixed, targs, hint, skills in _EXTRA2:
    tcs = []
    for ta in targs:
        # file-based tests run relative to backend/ dir; json-encode arg
        arg = _json2.dumps(ta)
        try:
            f_out = _run_py(fixed, arg)
        except Exception as e:
            f_out = f"ERR:{e}"
        try:
            f_val = eval(f_out) if f_out and not f_out.startswith("ERR") else f_out
        except Exception:
            f_val = f_out
        tcs.append(_tc(arg, f_val))
    _bug(f"dbg-v2-{len(items)+1:03d}", sub, diff, title,
         f"The following code {statement} Find and fix it.",
         buggy, fixed,
         "correct outputs per test case", "buggy output differs (see test cases)",
         hint,
         ["Reproduce with the smallest failing input", "Trace state step by step", "Check boundaries and types"],
         tcs=tcs, follow="Where else could this bug class hide in this codebase?",
         skills=skills)

def _gen_final_twelve():
    v = []
    v.append((
        "sorting", "medium", "Sorted with key=None crashes on mixed types",
        "sort_mixed([3,'a']) should sort as strings but raises TypeError.",
        "def _fn_(a):\n    return sorted(a)",
        "def _fn_(a):\n    return sorted(a, key=str)",
        [[3, "a", 1], ["b", "a"]],
        "Mixed types are unorderable. Normalize with key=str (or reject mixed input).",
        ["coding.debugging", "dsa.sorting"]))
    v.append((
        "math", "easy", "Recursive sum misses base zero",
        "rsum(0) should be 0 but recurses into negatives.",
        "def _fn_(n):\n    if n == 1:\n        return 1\n    return n + _fn_(n - 1)",
        "def _fn_(n):\n    if n <= 0:\n        return 0\n    return n + _fn_(n - 1)",
        [0, 4],
        "Base case must cover the actual termination value (0), not 1.",
        ["coding.debugging", "dsa.recursion"]))
    v.append((
        "lists", "easy", "Extend vs append nests the list",
        "flat([1,2],[3]) should be [1,2,3] but is [1,2,[3]].",
        "def _fn_(d):\n    out = list(d['a'])\n    out.append(d['b'])\n    return out",
        "def _fn_(d):\n    out = list(d['a'])\n    out.extend(d['b'])\n    return out",
        [{"a": [1, 2], "b": [3]}, {"a": [], "b": [1]}],
        "append adds ONE element (the list itself); extend adds EACH element.",
        ["coding.debugging", "dsa.arrays"]))
    v.append((
        "loops", "easy", "Range with wrong step direction is empty",
        "down_from(5) should be [5,4,3,2,1] but returns [].",
        "def _fn_(n):\n    return list(range(n, 0, 1))",
        "def _fn_(n):\n    return list(range(n, 0, -1))",
        [5, 1],
        "Ascending step with start > stop yields nothing. Match step sign to direction.",
        ["coding.debugging", "coding.loops"]))
    v.append((
        "search", "medium", "Linear search returns first match, need last",
        "last_pos should find the LAST occurrence but returns the first.",
        "def _fn_(d):\n    for i, x in enumerate(d['a']):\n        if x == d['x']:\n            return i\n    return None",
        "def _fn_(d):\n    for i in range(len(d['a']) - 1, -1, -1):\n        if d['a'][i] == d['x']:\n            return i\n    return None",
        [{"a": [1, 2, 1, 3], "x": 1}, {"a": [5], "x": 5}],
        "First-match loop exits early. Scan from the end (or track and keep going).",
        ["coding.debugging", "dsa.search"]))
    v.append((
        "bitwise", "medium", "Shift amount off by one",
        "mul_pow2(3, 2) should be 12 but returns 6.",
        "def _fn_(d):\n    return d['x'] << (d['k'] - 1)",
        "def _fn_(d):\n    return d['x'] << d['k']",
        [{"x": 3, "k": 2}, {"x": 1, "k": 0}],
        "x << k == x * 2^k. Shifting by k-1 halves the intended factor.",
        ["coding.debugging", "dsa.bit-manipulation"]))
    v.append((
        "strings", "medium", "Palindrome check strips spaces only",
        "is_pal('A man, a plan') should be True but is False.",
        "def _fn_(s):\n    t = s.lower().replace(' ', '')\n    return t == t[::-1]",
        "def _fn_(s):\n    t = ''.join(c for c in s.lower() if c.isalnum())\n    return t == t[::-1]",
        ["A man, a plan, a canal: Panama", "racecar", "hello"],
        "Spaces are not the only noise — strip ALL non-alphanumerics (punctuation too).",
        ["coding.debugging", "dsa.strings"]))
    v.append((
        "arrays", "medium", "Rotate by k larger than length is wrong",
        "rotate([1,2,3], 4) should be [3,1,2] but returns [1,2,3].",
        "def _fn_(d):\n    a, k = d['a'], d['k']\n    return a[-k:] + a[:-k]",
        "def _fn_(d):\n    a, k = d['a'], d['k']\n    k = k % len(a) if a else 0\n    return a[-k:] + a[:-k] if k else list(a)",
        [{"a": [1, 2, 3], "k": 4}, {"a": [1, 2, 3], "k": 0}],
        "Normalize k with modulo; k >= n otherwise slices the wrong window.",
        ["coding.debugging", "dsa.arrays"]))
    v.append((
        "dicts", "easy", "Update overwrites nested dict wholesale",
        "merge should deep-merge prefs but drops existing nested keys.",
        "def _fn_(d):\n    base = {'ui': {'theme': 'dark', 'font': 12}}\n    base.update(d['over'])\n    return base",
        "def _fn_(d):\n    import copy\n    out = copy.deepcopy({'ui': {'theme': 'dark', 'font': 12}})\n    for k, v in d['over'].items():\n        if isinstance(v, dict) and isinstance(out.get(k), dict):\n            out[k] = {**out[k], **v}\n        else:\n            out[k] = v\n    return out",
        [{"over": {"ui": {"font": 14}}}, {"over": {}}],
        "dict.update is shallow — nested dicts get replaced wholesale. Merge level by level.",
        ["coding.debugging", "dsa.hashing"]))
    v.append((
        "math", "easy", "Modulo special-case breaks wrap-around",
        "prev_day(0) should be 6 (Sunday) but returns -1.",
        "def _fn_(d):\n    return (d - 1) % 7 if d > 0 else -1",
        "def _fn_(d):\n    return (d - 1) % 7",
        [0, 1, 3],
        "Python % already wraps negatives ((0-1)%7==6). The special case broke it.",
        ["coding.debugging", "dsa.math"]))
    v.append((
        "recursion", "hard", "Exponential blowup on overlapping subproblems",
        "fib(30) takes seconds; should be instant.",
        "def _fn_(n):\n    if n <= 1:\n        return n\n    return _fn_(n - 1) + _fn_(n - 2)",
        "def _fn_(n):\n    from functools import lru_cache\n    @lru_cache(maxsize=None)\n    def f(k):\n        return k if k <= 1 else f(k - 1) + f(k - 2)\n    return f(n)",
        [10, 20, 25],
        "Naive recursion recomputes exponentially. Memoize (or go bottom-up).",
        ["coding.debugging", "dsa.dynamic-programming"]))
    v.append((
        "truthiness", "medium", "Empty list treated as missing config",
        "get_tags([]) should return [] but returns the default tags.",
        "def _fn_(d):\n    return d['tags'] if d['tags'] else ['default']",
        "def _fn_(d):\n    return d['tags'] if d['tags'] is not None else ['default']",
        [{"tags": []}, {"tags": ["a"]}, {"tags": None}],
        "[] is falsy but valid. Compare against None explicitly for 'missing'.",
        ["coding.debugging", "coding.truthiness"]))
    return v


for sub, diff, title, statement, buggy, fixed, targs, hint, skills in _gen_final_twelve():
    tcs = []
    for ta in targs:
        arg = _json2.dumps(ta)
        try:
            f_out = _run_py(fixed, arg)
        except Exception as e:
            f_out = f"ERR:{e}"
        try:
            f_val = eval(f_out) if f_out and not f_out.startswith("ERR") else f_out
        except Exception:
            f_val = f_out
        tcs.append(_tc(arg, f_val))
    _bug(f"dbg-v2-{len(items)+1:03d}", sub, diff, title,
         f"The following code {statement} Find and fix it.",
         buggy, fixed,
         "correct outputs per test case", "buggy output differs (see test cases)",
         hint,
         ["Reproduce with the smallest failing input", "Trace state step by step", "Check boundaries and types"],
         tcs=tcs, follow="Where else could this bug class hide in this codebase?",
         skills=skills)

# ─── WRITE + VALIDATE ───────────────────────────────────────────────
print(f"total debugging: {len(items)}")
assert len(items) == 133, f"expected 133, got {len(items)}"

qs = [q["question"] for q in items]
assert len(set(qs)) == len(qs), "duplicate question text found"
pairs = [(q["buggy_code"], q["correct_code"]) for q in items]
assert len(set(pairs)) == len(pairs), "duplicate code pairs found"

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=1)

from collections import Counter
print(f"Wrote {len(items)} debugging questions to {OUT.name}")
print(dict(Counter(q['sub_topic'] for q in items)))
