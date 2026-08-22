"""
Placement Mastery Track — an in-depth, guided curriculum for job-seekers.

This module adds *depth* on top of the gamified language tracks:
  * A structured 12-week roadmap (aptitude -> DSA foundations -> DSA advanced
    -> core CS -> system design -> HR/behavioral -> mock capstone).
  * Each topic carries REAL pedagogy: learning objectives, a worked code
    example, graded exercises, a quiz, and company relevance.
  * Covers the "core CS for placement" domains (OS / DBMS / CN) that campus
    hiring actually tests but the language tracks leave thin.

Served via GET /api/v1/learning/placement-roadmap.
"""
#pylint: skip-file

PLACEMENT_ROADMAP = {
    "title": "Placement Pro Mastery Track",
    "subtitle": "From zero to job-ready in 12 weeks — aptitude, DSA, core CS, system design, and HR.",
    "total_weeks": 12,
    "phases": [
        {
            "id": "p1",
            "name": "Aptitude & Quantitative Foundations",
            "weeks": "Weeks 1-2",
            "goal": "Clear the screening cutoff used by TCS, Infosys, Wipro, Accenture and similar.",
            "topics": [
                {
                    "id": "apt_arith",
                    "name": "Arithmetic, Percentages & Ratios",
                    "difficulty": "easy",
                    "objectives": [
                        "Solve percentage, profit/loss and ratio problems in under 60s.",
                        "Use the unitary and alligation methods for mixture problems.",
                        "Avoid common traps in successive percentage changes.",
                    ],
                    "example": {
                        "language": "text",
                        "code": "A shirt costs ₹1000. It is discounted 20%, then a 10% tax is added.\nWrong: 1000 * 0.8 * 1.1 = ₹880.\nRight: discount applies first -> 800, then tax -> 800 * 1.1 = ₹880.\nKey: discounts and taxes are applied in stated order; never add 20%+10%=30%.",
                        "explanation": "Successive percentage changes are multiplicative, not additive.",
                    },
                    "exercises": [
                        {"prompt": "What single discount equals two successive 20% discounts?", "hint": "0.8 * 0.8 = 0.64, so 36% total."},
                        {"prompt": "A mixture is 30% alcohol. How much pure alcohol to add to 10L to make 50%?", "hint": "Set up (3 + x)/(10 + x) = 0.5."},
                    ],
                    "quiz": [
                        {"q": "After two successive 25% discounts, the net discount is?", "options": ["50%", "43.75%", "56.25%", "37.5%"], "answer": 1},
                    ],
                    "companies": ["TCS", "Infosys", "Wipro", "Capgemini"],
                },
                {
                    "id": "apt_speed_work",
                    "name": "Time-Speed-Distance & Work",
                    "difficulty": "easy",
                    "objectives": [
                        "Apply distance = speed x time across trains, boats, pipes.",
                        "Solve work-rate problems using LCM of days.",
                        "Handle relative speed for overtaking/passing.",
                    ],
                    "example": {
                        "language": "python",
                        "code": "def meet_time(distance_km, speed_a, speed_b):\n    # trains moving toward each other\n    return distance_km / (speed_a + speed_b)\n\nprint(meet_time(300, 60, 90))  # 2.0 hours",
                        "explanation": "Relative speed adds when objects move toward each other.",
                    },
                    "exercises": [
                        {"prompt": "A fills a tank in 6h, B empties in 8h. Together, how long to fill?", "hint": "Net rate = 1/6 - 1/8 per hour."},
                        {"prompt": "Boat speed in still water 10 km/h, stream 2 km/h. Downstream 24 km time?", "hint": "Effective speed = 12 km/h."},
                    ],
                    "quiz": [
                        {"q": "A and B can do a work in 10 and 15 days. Together they finish in?", "options": ["6 days", "5 days", "12 days", "25 days"], "answer": 0},
                    ],
                    "companies": ["TCS NQT", "Infosys", "Cognizant"],
                },
                {
                    "id": "apt_logical",
                    "name": "Logical Reasoning & Series",
                    "difficulty": "medium",
                    "objectives": [
                        "Decode number/letter series and find the odd one out.",
                        "Solve seating arrangement and blood-relation puzzles.",
                        "Apply syllogism rules (All/Some/No).",
                    ],
                    "exercises": [
                        {"prompt": "Series: 2, 6, 12, 20, 30, ?", "hint": "n*(n+1): 6*7=42."},
                        {"prompt": "If A is B's mother and C is A's father, how is C related to B?", "hint": "C is B's grandfather."},
                    ],
                    "quiz": [
                        {"q": "Next in 1, 1, 2, 3, 5, 8, ?", "options": ["11", "13", "15", "10"], "answer": 1},
                    ],
                    "companies": ["Wipro", "Accenture", "Deloitte"],
                },
            ],
        },
        {
            "id": "p2",
            "name": "Programming & DSA Foundations",
            "weeks": "Weeks 3-4",
            "goal": "Write correct, efficient code and analyze it — the baseline for every coding round.",
            "topics": [
                {
                    "id": "dsa_complexity",
                    "name": "Complexity Analysis (Big-O)",
                    "difficulty": "easy",
                    "objectives": [
                        "Express time/space complexity in Big-O notation.",
                        "Identify nested-loop and divide-and-conquer complexity.",
                        "Reason about worst vs average case.",
                    ],
                    "example": {
                        "language": "python",
                        "code": "def has_pair_sum(arr, target):\n    seen = set()\n    for x in arr:            # O(n)\n        if target - x in seen:\n            return True\n        seen.add(x)\n    return False  # O(n) time, O(n) space",
                        "explanation": "A hash set turns an O(n^2) brute force into O(n).",
                    },
                    "exercises": [
                        {"prompt": "What is the complexity of binary search?", "hint": "O(log n)."},
                        {"prompt": "Merge sort time and space?", "hint": "O(n log n) time, O(n) space."},
                    ],
                    "quiz": [
                        {"q": "A triple nested loop over n elements is?", "options": ["O(n)", "O(n log n)", "O(n^2)", "O(n^3)"], "answer": 3},
                    ],
                    "companies": ["All coding rounds"],
                },
                {
                    "id": "dsa_arrays",
                    "name": "Arrays & Strings",
                    "difficulty": "easy",
                    "objectives": [
                        "Use two-pointer and sliding-window patterns.",
                        "Reverse, rotate, and partition in place.",
                        "Handle edge cases (empty, single element).",
                    ],
                    "example": {
                        "language": "python",
                        "code": "def two_sum_sorted(a, target):\n    l, r = 0, len(a) - 1\n    while l < r:                 # O(n) two-pointer\n        s = a[l] + a[r]\n        if s == target: return (l, r)\n        if s < target: l += 1\n        else: r -= 1\n    return None",
                        "explanation": "Sorted input lets two pointers replace O(n^2).",
                    },
                    "exercises": [
                        {"prompt": "Find the longest substring without repeating characters.", "hint": "Sliding window + last-seen map."},
                        {"prompt": "Rotate an array right by k in O(n) time, O(1) space.", "hint": "Reverse three times."},
                    ],
                    "quiz": [
                        {"q": "Best average time to find a pair summing to target in an UNSORTED array?", "options": ["O(n^2)", "O(n log n)", "O(n)", "O(1)"], "answer": 2},
                    ],
                    "companies": ["Google", "Amazon", "Adobe"],
                },
                {
                    "id": "dsa_recursion",
                    "name": "Recursion & Backtracking",
                    "difficulty": "medium",
                    "objectives": [
                        "Map a problem to a recurrence.",
                        "Add memoization to avoid exponential blowup.",
                        "Implement backtracking with choose/explore/unchoose.",
                    ],
                    "example": {
                        "language": "python",
                        "code": "from functools import lru_cache\ndef fib(n):\n    @lru_cache(None)\n    def f(k):\n        return k if k < 2 else f(k-1) + f(k-2)\n    return f(n)  # O(n) with memo",
                        "explanation": "Memoization turns O(2^n) into O(n).",
                    },
                    "exercises": [
                        {"prompt": "Generate all permutations of a string.", "hint": "Swap-and-recurse backtracking."},
                        {"prompt": "N-Queens: place N queens safely on NxN board.", "hint": "Backtrack with row/col/diag sets."},
                    ],
                    "quiz": [
                        {"q": "Naive recursive fib(40) without memo is roughly?", "options": ["O(40)", "O(2^40)", "O(40^2)", "O(log 40)"], "answer": 1},
                    ],
                    "companies": ["Microsoft", "Flipkart", "Oracle"],
                },
            ],
        },
        {
            "id": "p3",
            "name": "Advanced DSA",
            "weeks": "Weeks 5-7",
            "goal": "Crack the hard problems in product-company coding rounds.",
            "topics": [
                {
                    "id": "adv_linked",
                    "name": "Linked Lists, Stacks & Queues",
                    "difficulty": "medium",
                    "objectives": [
                        "Reverse a linked list iteratively and recursively.",
                        "Use a stack for parentheses and expression evaluation.",
                        "Implement LRU cache with hash map + doubly linked list.",
                    ],
                    "example": {
                        "language": "python",
                        "code": "def reverse_list(head):\n    prev = None\n    while head:                # O(n)\n        nxt = head.next\n        head.next = prev\n        prev = head\n        head = nxt\n    return prev",
                        "explanation": "Three-pointer reversal is the canonical interview solution.",
                    },
                    "exercises": [
                        {"prompt": "Detect a cycle in a linked list (O(1) space).", "hint": "Floyd's tortoise and hare."},
                        {"prompt": "Implement a min-stack supporting push/pop/top/getMin in O(1).", "hint": "Store (value, current_min) tuples."},
                    ],
                    "quiz": [
                        {"q": "A queue implemented with two stacks: worst-case enqueue cost?", "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"], "answer": 1},
                    ],
                    "companies": ["Amazon", " Goldman Sachs", "Paytm"],
                },
                {
                    "id": "adv_trees",
                    "name": "Trees & BSTs",
                    "difficulty": "medium",
                    "objectives": [
                        "Perform in/pre/post-order traversal (recursive + iterative).",
                        "Insert/search/delete in a BST.",
                        "Validate a BST using min/max bounds.",
                    ],
                    "example": {
                        "language": "python",
                        "code": "def is_bst(node, lo=float('-inf'), hi=float('inf')):\n    if not node: return True\n    if not (lo < node.val < hi): return False\n    return is_bst(node.left, lo, node.val) and is_bst(node.right, node.val, hi)",
                        "explanation": "Track valid range per subtree.",
                    },
                    "exercises": [
                        {"prompt": "Find the lowest common ancestor in a BST.", "hint": "Go left/right based on value bounds."},
                        {"prompt": "Serialize and deserialize a binary tree.", "hint": "Preorder with null markers."},
                    ],
                    "quiz": [
                        {"q": "Height of a balanced BST with n nodes is about?", "options": ["n", "n/2", "log2(n)", "sqrt(n)"], "answer": 2},
                    ],
                    "companies": ["Google", "Adobe", "Samsung"],
                },
                {
                    "id": "adv_graphs",
                    "name": "Graphs: BFS, DFS & Shortest Path",
                    "difficulty": "hard",
                    "objectives": [
                        "Represent graphs as adjacency lists.",
                        "Run BFS/DFS for connectivity and traversal order.",
                        "Apply Dijkstra for non-negative shortest paths.",
                    ],
                    "example": {
                        "language": "python",
                        "code": "from collections import deque\ndef bfs(graph, src):\n    seen, q = {src}, deque([src])\n    while q:                    # O(V + E)\n        u = q.popleft()\n        for v in graph[u]:\n            if v not in seen:\n                seen.add(v); q.append(v)\n    return seen",
                        "explanation": "BFS visits nodes in increasing distance from src.",
                    },
                    "exercises": [
                        {"prompt": "Number of islands in a 0/1 grid.", "hint": "DFS/BFS from each unvisited land cell."},
                        {"prompt": "Shortest path in an unweighted graph.", "hint": "BFS with distance tracking."},
                    ],
                    "quiz": [
                        {"q": "Dijkstra's algorithm requires edge weights to be?", "options": ["Positive", "Integer", "Even", "Negative allowed"], "answer": 0},
                    ],
                    "companies": ["Uber", "Flipkart", "Microsoft"],
                },
                {
                    "id": "adv_dp",
                    "name": "Dynamic Programming",
                    "difficulty": "hard",
                    "objectives": [
                        "Identify optimal substructure and overlapping subproblems.",
                        "Build memoized recursion then tabulation.",
                        "Solve classic DP: knapsack, LIS, edit distance.",
                    ],
                    "example": {
                        "language": "python",
                        "code": "def lis(nums):\n    dp = [1]*len(nums)\n    for i in range(len(nums)):\n        for j in range(i):\n            if nums[j] < nums[i]:\n                dp[i] = max(dp[i], dp[j]+1)\n    return max(dp)  # O(n^2)",
                        "explanation": "LIS is the canonical DP interview problem.",
                    },
                    "exercises": [
                        {"prompt": "0/1 Knapsack: maximize value within weight W.", "hint": "dp[i][w] = max(skip, take)."},
                        {"prompt": "Edit distance between two strings.", "hint": "dp[i][j] over insert/delete/replace."},
                    ],
                    "quiz": [
                        {"q": "Longest Common Subsequence of 'ABC' and 'AC' is length?", "options": ["1", "2", "3", "0"], "answer": 1},
                    ],
                    "companies": ["Amazon", "Google", "Arcesium"],
                },
            ],
        },
        {
            "id": "p4",
            "name": "Core CS for Placement (OS / DBMS / CN)",
            "weeks": "Weeks 8-9",
            "goal": "Answer the theory round that filters most campus candidates.",
            "topics": [
                {
                    "id": "cs_os",
                    "name": "Operating Systems",
                    "difficulty": "medium",
                    "objectives": [
                        "Explain process vs thread and context switching.",
                        "Describe virtual memory, paging and thrashing.",
                        "Define deadlock conditions and prevention.",
                    ],
                    "exercises": [
                        {"prompt": "Name the four Coffman conditions for deadlock.", "hint": "Mutual exclusion, hold-and-wait, no preemption, circular wait."},
                        {"prompt": "Why does thrashing happen and how to reduce it?", "hint": "Too many pages faulting; increase frame allocation / reduce multiprogramming."},
                    ],
                    "quiz": [
                        {"q": "Which is NOT a deadlock condition?", "options": ["Mutual exclusion", "Circular wait", "Preemption allowed", "Hold and wait"], "answer": 2},
                    ],
                    "companies": ["Intel", "Nvidia", "Qualcomm"],
                },
                {
                    "id": "cs_dbms",
                    "name": "Database Management Systems",
                    "difficulty": "medium",
                    "objectives": [
                        "Normalize to 1NF/2NF/3NF and explain anomalies.",
                        "Choose and justify indexes (B-tree).",
                        "Explain ACID and transaction isolation levels.",
                    ],
                    "example": {
                        "language": "sql",
                        "code": "SELECT d.name, AVG(e.salary) AS avg_sal\nFROM employees e\nJOIN departments d ON e.dept_id = d.id\nGROUP BY d.name\nHAVING AVG(e.salary) > 60000\nORDER BY avg_sal DESC;",
                        "explanation": "GROUP BY + HAVING filters aggregated rows.",
                    },
                    "exercises": [
                        {"prompt": "Write a query for the N-th highest salary.", "hint": "Use OFFSET/FETCH or a correlated subquery."},
                        {"prompt": "What anomaly does 3NF remove?", "hint": "Transitive dependency on a non-key."},
                    ],
                    "quiz": [
                        {"q": "PRIMARY KEY enforces which normal form at minimum?", "options": ["1NF", "2NF", "3NF", "BCNF"], "answer": 0},
                    ],
                    "companies": ["Oracle", "SAP", "TCS Digital"],
                },
                {
                    "id": "cs_cn",
                    "name": "Computer Networks",
                    "difficulty": "medium",
                    "objectives": [
                        "Contrast TCP (reliable) vs UDP (fast).",
                        "Explain the HTTP request/response cycle and status codes.",
                        "Describe DNS resolution and TLS handshake basics.",
                    ],
                    "exercises": [
                        {"prompt": "When would you pick UDP over TCP?", "hint": "Video calls, games, DNS — loss-tolerant, latency-sensitive."},
                        {"prompt": "What does a 301 vs 404 HTTP status mean?", "hint": "301 permanent redirect; 404 not found."},
                    ],
                    "quiz": [
                        {"q": "Which protocol guarantees in-order delivery?", "options": ["UDP", "TCP", "IP", "ICMP"], "answer": 1},
                    ],
                    "companies": ["Cisco", "Juniper", "Akamai"],
                },
            ],
        },
        {
            "id": "p5",
            "name": "System Design & Coding Rounds",
            "weeks": "Week 10",
            "goal": "Survive the design discussion at startups and product companies.",
            "topics": [
                {
                    "id": "sd_basics",
                    "name": "System Design Fundamentals",
                    "difficulty": "hard",
                    "objectives": [
                        "Clarify requirements (functional, non-functional, scale).",
                        "Estimate capacity (QPS, storage) with back-of-envelope math.",
                        "Sketch a component diagram: clients, API, cache, DB, queue.",
                    ],
                    "exercises": [
                        {"prompt": "Estimate storage for 1M users uploading 1 photo/day at 2MB for a year.", "hint": "1e6 * 365 * 2MB ≈ 730 TB."},
                        {"prompt": "Design a URL shortener (scale, collisions, analytics).", "hint": "Base62 of a counter + cache hot URLs."},
                    ],
                    "quiz": [
                        {"q": "Primary purpose of a CDN?", "options": ["Run databases", "Cache static content near users", "Encrypt traffic", "Balance CPU"], "answer": 1},
                    ],
                    "companies": ["Amazon", "Meta", "Zomato"],
                },
                {
                    "id": "sd_components",
                    "name": "Scaling Building Blocks",
                    "difficulty": "hard",
                    "objectives": [
                        "Use caching (Redis) to cut DB load; handle invalidation.",
                        "Apply load balancing and horizontal scaling.",
                        "Choose SQL vs NoSQL per access pattern.",
                    ],
                    "exercises": [
                        {"prompt": "How to avoid cache stampede on a hot key expiry?", "hint": "Single-flight / lock or jittered TTL."},
                        {"prompt": "When is NoSQL preferable to SQL?", "hint": "High write volume, flexible schema, horizontal scale."},
                    ],
                    "quiz": [
                        {"q": "Cache-aside means the app reads cache, on miss loads from DB and...?", "options": ["Deletes DB", "Populates cache", "Returns null", "Retries forever"], "answer": 1},
                    ],
                    "companies": ["Netflix", "Uber", "Swiggy"],
                },
            ],
        },
        {
            "id": "p6",
            "name": "HR, Behavioral & Company Rounds",
            "weeks": "Week 11",
            "goal": "Convert the offer — most rejections here are from poor communication, not skill.",
            "topics": [
                {
                    "id": "hr_behavioral",
                    "name": "Behavioral Interviews (STAR)",
                    "difficulty": "easy",
                    "objectives": [
                        "Structure answers with Situation-Task-Action-Result.",
                        "Prepare 5 stories covering conflict, failure, leadership.",
                        "Answer 'tell me about yourself' in 90 seconds.",
                    ],
                    "exercises": [
                        {"prompt": "Draft a STAR answer for 'describe a failure'.", "hint": "Show what you learned and changed."},
                        {"prompt": "Why should we hire you? (3 concrete points).", "hint": "Skill fit + proven results + enthusiasm."},
                    ],
                    "quiz": [
                        {"q": "STAR stands for Situation, Task, Action, ?", "options": ["Result", "Review", "Routine", "Risk"], "answer": 0},
                    ],
                    "companies": ["All"],
                },
                {
                    "id": "hr_company",
                    "name": "Resume, HR & Salary Discussion",
                    "difficulty": "easy",
                    "objectives": [
                        "Tailor your resume to the job description (ATS keywords).",
                        "Handle the expected-salary question with a range.",
                        "Ask 2-3 smart questions at the end.",
                    ],
                    "exercises": [
                        {"prompt": "List 3 ATS-friendly resume fixes.", "hint": "Standard headings, keywords, no images/tables."},
                        {"prompt": "How to answer 'what is your expected CTC'?", "hint": "Give a researched market range, not a single number."},
                    ],
                    "quiz": [
                        {"q": "Best time to discuss salary?", "options": ["First call", "After an offer is on the table", "Never", "In the resume"], "answer": 1},
                    ],
                    "companies": ["All"],
                },
            ],
        },
        {
            "id": "p7",
            "name": "Mock Interviews & Capstone",
            "weeks": "Week 12",
            "goal": "Simulate the full loop and fix weak spots before the real thing.",
            "topics": [
                {
                    "id": "capstone_loop",
                    "name": "Full-Loop Simulation Checklist",
                    "difficulty": "medium",
                    "objectives": [
                        "Run a timed 60-minute coding + 30-minute design block.",
                        "Record and critique your own communication.",
                        "Build a weak-area revision plan from your results.",
                    ],
                    "exercises": [
                        {"prompt": "Schedule 3 mock interviews this week (peer or AI).", "hint": "Use PlacementPro AI Interviewer + a friend."},
                        {"prompt": "After each mock, list your top 3 improvement items.", "hint": "Be specific: e.g., 'verbalize brute force before optimizing'."},
                    ],
                    "quiz": [
                        {"q": "Best use of the final week before interviews?", "options": ["Learn a new language", "Targeted revision of weak areas + mocks", "Cram everything", "Take a break only"], "answer": 1},
                    ],
                    "companies": ["All"],
                },
            ],
        },
    ],
}


def get_placement_roadmap() -> dict:
    """Return the full placement curriculum tree."""
    return PLACEMENT_ROADMAP


def get_topic_by_id(topic_id: str) -> dict | None:
    """Flat lookup of a single topic across all phases."""
    for phase in PLACEMENT_ROADMAP["phases"]:
        for topic in phase["topics"]:
            if topic["id"] == topic_id:
                return {**topic, "phase_id": phase["id"], "phase_name": phase["name"]}
    return None
