"""
Role Curriculum Definitions — role_curriculum.py

Defines every placement role with its own skill tree, mock test config,
company blueprint, and structured learning path from Foundation → Job Ready.

Each role is an independent end-to-end plan:

  Role → Phase 1: Foundation (Beginner) → Phase 2: Core (Intermediate) →
  Phase 3: Advanced → Phase 4: Job Ready → Mock Test → Booking Slots

  Progression Logic:
    - Foundation: Basic syntax, fundamentals, core concepts (20-30% of total)
    - Core: Core data structures, algorithms, medium-difficulty problems (40-50%)
    - Advanced: Hard problems, system design, real-world scenarios (15-25%)
    - Job Ready: Full mock interviews, company-specific prep, behavioral (5-10%)

Roles:
  1.  SDE              — Full-stack software engineer (DS + Algo + System Design)
  2.  Data Analyst     — SQL + stats + Python/R + BI tools
  3.  AI Engineer      — ML + DL + NLP + MLOps + Python
  4.  Java Engineer    — Core Java + Spring + OOP + DS + concurrency
  5.  ML Engineer      — Supervised/unsupervised + feature eng + deployment
  6.  Data Scientist   — Stats + ML + Python + experimentation
  7.  Technical Assistant — Basic coding + aptitude + HR screening
  8.  DevOps Engineer  — Linux + CI/CD + Docker + Kubernetes + cloud
  9.  QA Engineer      — Testing + automation + Selenium + API testing
  10. Product Analyst  — SQL + stats + A/B testing + product thinking
"""
from typing import Dict, List, Any
import json
import os


def _load_curriculum_json(filename: str) -> dict:
    """Load curriculum JSON from the content directory."""
    path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_curriculum_json(filename: str, data: dict) -> None:
    """Save curriculum JSON to the content directory."""
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# =============================================================
# CURRICULUM VERSIONING & METADATA
# =============================================================

CURRICULUM_META: dict = {
    "version": "2.0.0",
    "generated_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
    "description": "Phase-based curriculum from Foundation to Job Ready",
    "total_roles": 10,
    "progression_phases": ["foundation", "core", "advanced", "job-ready"],
    "learning_module_integration": True,
}


# =============================================================
# HELPER FUNCTIONS
# =============================================================

def get_curriculum_meta() -> dict:
    return CURRICULUM_META


def get_role(role_id: str) -> Dict[str, Any] | None:
    return ROLE_CURRICULA.get(role_id.lower())


def get_all_roles() -> Dict[str, Dict[str, Any]]:
    return ROLE_CURRICULA


def get_role_ids() -> list:
    return list(ROLE_CURRICULA.keys())


def get_role_display_order() -> list:
    return ROLE_DISPLAY_ORDER


def get_skill_tree(role_id: str) -> dict:
    role = get_role(role_id)
    if not role:
        return {}
    return role.get("skill_tree", {})


def get_total_target(role_id: str) -> int:
    skill_tree = get_skill_tree(role_id)
    return sum(s.get("target", 0) for s in skill_tree.values())


def get_phase_targets(role_id: str) -> dict:
    """Get question targets broken down by progression phase."""
    skill_tree = get_skill_tree(role_id)
    phases = {"foundation": 0, "core": 0, "advanced": 0, "job-ready": 0}
    for skill, data in skill_tree.items():
        # Phase assignment based on skill weight and target
        weight = data.get("weight", 1.0)
        target = data.get("target", 0)
        if weight >= 1.2 and "design" in skill.lower():
            phases["advanced"] += target
        elif weight >= 1.0:
            phases["core"] += target
        else:
            phases["foundation"] += target
    # Job ready is typically from mock tests, not skill tree
    phases["job-ready"] = role.get("mock_test", {}).get("total_questions", 0)
    return phases


# =============================================================
# ROLE CURRICULA DEFINITIONS
# =============================================================

ROLE_CURRICULA: Dict[str, Dict[str, Any]] = {

    # =========================================================
    # 1. SDE — Software Development Engineer
    # =========================================================
    "sde": {
        "role_id": "sde",
        "display_name": "SDE (Software Development Engineer)",
        "icon": "🖥️",
        "description": "End-to-end coding interviews: DS, algorithms, system design, and behavioral.",
        "target_companies": ["Amazon", "Google", "Microsoft", "Meta", "TCS", "Infosys", "Wipro", "Apple", "Netflix", "Uber"],
        "estimated_weeks": 16,
        "total_questions_target": 500,
        "progression_phases": {
            "foundation": {
                "name": "Foundation (Beginner)",
                "weeks": 1,
                "description": "Build programming fundamentals and core data structures",
                "skills": ["programming-fundamentals", "arrays-hashing", "strings", "two-pointers-sliding-window", "recursion-backtracking"],
                "learning_module_ids": ["arrays-basics", "strings-intro", "two-pointers-intro", "recursion-fundamentals"],
                "milestone": "Solve 20+ easy problems on arrays and strings",
            },
            "core": {
                "name": "Core (Intermediate)",
                "weeks": 2,
                "description": "Master core data structures and algorithms",
                "skills": ["linked-lists", "stacks-queues", "trees", "binary-search", "graphs", "dynamic-programming", "heap-greedy"],
                "learning_module_ids": ["linked-lists-deep-dive", "trees-bst", "binary-search-patterns", "dp-patterns", "graph-fundamentals"],
                "milestone": "Solve 50+ medium problems across all data structures",
            },
            "advanced": {
                "name": "Advanced",
                "weeks": 3,
                "description": "Tackle hard problems, system design, and CS fundamentals",
                "skills": ["system-design", "dbms", "oop", "networks", "os", "sql", "advanced-dp", "advanced-graphs"],
                "learning_module_ids": ["system-design-intro", "dbms-fundamentals", "oop-design-patterns", "networking-basics"],
                "milestone": "Solve 30+ hard problems and design 5+ systems",
            },
            "job-ready": {
                "name": "Job Ready",
                "weeks": 4,
                "description": "Company-specific prep, mock interviews, and behavioral rounds",
                "skills": ["mock-interviews", "behavioral", "company-specific", "aptitude"],
                "learning_module_ids": ["behavioral-stars", "amazon-lp", "google-googliness", "system-design-deep-dive"],
                "milestone": "Clear 3+ full mock interview loops with 80%+ score",
            },
        },
        "skill_tree": {
            "programming-fundamentals": {
                "name": "Programming Fundamentals",
                "target": 25,
                "weight": 1.0,
                "prerequisites": [],
                "est_hours": 10,
                "phase": "foundation",
                "difficulty_distribution": {"easy": 15, "medium": 8, "hard": 2},
                "sub_topics": ["variables-types", "control-flow", "loops", "functions", "recursion", "string-basics", "array-basics", "input-output", "error-handling", "debugging"],
                "patterns": ["iteration", "recursion", "conditionals"],
                "learning_module_ids": ["programming-basics"],
                "company_sources": {
                    "tcs": ["variables-types", "loops"],
                    "infosys": ["functions", "recursion"],
                },
            },
            "arrays-hashing": {
                "name": "Arrays & Hashing",
                "target": 40,
                "weight": 1.0,
                "prerequisites": ["programming-fundamentals"],
                "est_hours": 15,
                "phase": "foundation",
                "difficulty_distribution": {"easy": 15, "medium": 18, "hard": 7},
                "sub_topics": ["two-sum", "contains-duplicate", "group-anagrams", "product-except-self", "top-k-frequent-elements", "valid-sudoku", "longest-consecutive-sequence", "encode-decode-strings", "design-hashmap", "subarray-sum-equals-k", "majority-element", "missing-number", "find-all-disappeared", "set-matrix-zeroes", "spiral-matrix", "rotate-image", "jump-game", "merge-intervals", "insert-interval", "happy-number"],
                "patterns": ["hash-table", "frequency-count", "prefix-sum", "in-place"],
                "learning_module_ids": ["arrays-hashing", "hash-table-patterns"],
                "company_sources": {
                    "amazon": ["two-sum", "contains-duplicate", "top-k-frequent-elements"],
                    "google": ["product-except-self", "longest-consecutive-sequence"],
                    "microsoft": ["valid-sudoku", "group-anagrams"],
                    "meta": ["encode-decode-strings", "subarray-sum-equals-k"],
                    "tcs": ["two-sum", "majority-element"],
                },
            },
            "two-pointers-sliding-window": {
                "name": "Two Pointers & Sliding Window",
                "target": 25,
                "weight": 1.0,
                "prerequisites": ["arrays-hashing"],
                "est_hours": 10,
                "phase": "foundation",
                "difficulty_distribution": {"easy": 8, "medium": 12, "hard": 5},
                "sub_topics": ["two-sum-ii", "sort-colors", "longest-substring-without-repeating", "min-size-subarray-sum", "longest-repeating-character-replacement", "permutation-in-string", "minimum-window-substring", "container-with-most-water", "trapping-rain-water", "3sum", "4sum", "remove-duplicates", "remove-element", "palindrome-check", "reverse-string"],
                "patterns": ["two-pointers", "sliding-window", "fast-slow-pointers"],
                "learning_module_ids": ["two-pointers", "sliding-window"],
                "company_sources": {
                    "google": ["longest-substring-without-repeating", "minimum-window-substring"],
                    "amazon": ["sort-colors", "container-with-most-water", "trapping-rain-water"],
                    "microsoft": ["two-sum-ii", "longest-repeating-character-replacement"],
                    "meta": ["3sum", "4sum"],
                },
            },
            "strings": {
                "name": "Strings",
                "target": 25,
                "weight": 0.9,
                "prerequisites": ["arrays-hashing"],
                "est_hours": 8,
                "phase": "foundation",
                "difficulty_distribution": {"easy": 8, "medium": 12, "hard": 5},
                "sub_topics": ["valid-palindrome", "reverse-words-in-a-string", "group-anagrams", "minimum-window-substring", "repeated-substring-pattern", "longest-palindromic-substring", "palindromic-substrings", "string-compression", "string-to-integer-atoi", "longest-common-prefix", "valid-anagram", "isomorphic-strings", "word-pattern", "count-and-say"],
                "patterns": ["two-pointers", "hash-table", "sliding-window", "string-manipulation"],
                "learning_module_ids": ["string-manipulation"],
                "company_sources": {
                    "amazon": ["minimum-window-substring", "string-compression"],
                    "google": ["longest-palindromic-substring", "word-pattern"],
                    "microsoft": ["valid-palindrome", "count-and-say"],
                },
            },
            "linked-lists": {
                "name": "Linked Lists",
                "target": 20,
                "weight": 0.9,
                "prerequisites": ["arrays-hashing", "recursion-backtracking"],
                "est_hours": 8,
                "phase": "core",
                "difficulty_distribution": {"easy": 6, "medium": 10, "hard": 4},
                "sub_topics": ["reverse-linked-list", "add-two-numbers", "copy-list-with-random-pointer", "remove-nth-node-from-end", "merge-two-sorted-lists", "palindrome-linked-list", "linked-list-cycle", "linked-list-cycle-ii", "reorder-list", "sort-list", "flatten-multilevel-list", "rotate-list", "design-linked-list", "swap-nodes-in-pairs", "reverse-k-group", "merge-k-sorted-lists", "intersection-of-two-lists", "lru-cache"],
                "patterns": ["linked-list", "two-pointers", "dummy-head", "fast-slow"],
                "learning_module_ids": ["linked-lists-deep-dive"],
                "company_sources": {
                    "amazon": ["add-two-numbers", "merge-k-sorted-lists"],
                    "google": ["copy-list-with-random-pointer", "lru-cache"],
                    "meta": ["reverse-linked-list", "reorder-list"],
                    "microsoft": ["intersection-of-two-lists", "swap-nodes-in-pairs"],
                },
            },
            "stacks-queues": {
                "name": "Stacks & Queues",
                "target": 20,
                "weight": 0.9,
                "prerequisites": ["arrays-hashing"],
                "est_hours": 7,
                "phase": "core",
                "difficulty_distribution": {"easy": 6, "medium": 10, "hard": 4},
                "sub_topics": ["valid-parentheses", "min-stack", "daily-temperatures", "sliding-window-maximum", "implement-queue-using-stacks", "next-greater-element", "evaluate-reverse-polish-notation", "generate-parentheses", "simplify-path", "min-stack", "decode-string", "asteroid-collision", "online-stock-span", "largest-rectangle-in-histogram", "basic-calculator", "basic-calculator-ii", "binary-tree-inorder-traversal-iterative"],
                "patterns": ["stack", "monotonic-stack", "queue", "deque"],
                "learning_module_ids": ["stacks-queues"],
                "company_sources": {
                    "amazon": ["daily-temperatures", "largest-rectangle-in-histogram"],
                    "google": ["min-stack", "basic-calculator"],
                    "meta": ["evaluate-reverse-polish-notation", "simplify-path"],
                },
            },
            "trees": {
                "name": "Trees & BST",
                "target": 35,
                "weight": 1.0,
                "prerequisites": ["recursion-backtracking"],
                "est_hours": 15,
                "phase": "core",
                "difficulty_distribution": {"easy": 10, "medium": 18, "hard": 7},
                "sub_topics": ["inorder-traversal", "validate-binary-search-tree", "lowest-common-ancestor", "serialize-and-deserialize", "level-order-traversal", "path-sum", "binary-tree-maximum-path-sum", "same-tree", "symmetric-tree", "maximum-depth", "minimum-depth", "balanced-binary-tree", "invert-binary-tree", "kth-smallest-in-bst", "construct-bst-from-preorder", "binary-tree-right-side-view", "count-good-nodes", "house-robber-iii", "flatten-binary-tree", "vertical-order-traversal", "serialize-deserialize-bst", "recover-bst", "unique-bsts", "word-search-ii", "implement-trie"],
                "patterns": ["tree-dfs", "tree-bfs", "bst", "trie"],
                "learning_module_ids": ["trees-bst", "binary-trees", "tries"],
                "company_sources": {
                    "amazon": ["serialize-and-deserialize", "lowest-common-ancestor", "binary-tree-maximum-path-sum"],
                    "google": ["kth-smallest-in-bst", "construct-bst-from-preorder"],
                    "meta": ["validate-binary-search-tree", "flatten-binary-tree"],
                    "microsoft": ["same-tree", "recover-bst"],
                },
            },
            "graphs": {
                "name": "Graphs",
                "target": 30,
                "weight": 1.1,
                "prerequisites": ["trees", "recursion-backtracking"],
                "est_hours": 12,
                "phase": "core",
                "difficulty_distribution": {"easy": 8, "medium": 15, "hard": 7},
                "sub_topics": ["clone-graph", "course-schedule", "dijkstra-shortest-path", "bfs-shortest-path", "topological-sort", "number-of-islands", "word-ladder", "rotting-oranges", "surrounded-regions", "walls-and-gates", "pacific-atlantic-water-flow", "redundant-connection", "accounts-merge", "graph-valid-tree", "number-of-connected-components", "reconstruct-itinerary", "cheapest-flights-within-k-stops", "network-delay-time", "swim-in-rising-water", "alien-dictionary", "couples-holding-hands", "optimize-water-distribution"],
                "patterns": ["graph-dfs", "graph-bfs", "topological", "union-find", "shortest-path", "minimum-spanning-tree"],
                "learning_module_ids": ["graph-fundamentals", "graph-advanced"],
                "company_sources": {
                    "google": ["number-of-islands", "word-ladder", "network-delay-time"],
                    "meta": ["clone-graph", "reconstruct-itinerary"],
                    "amazon": ["course-schedule", "cheapest-flights-within-k-stops"],
                    "microsoft": ["alien-dictionary", "accounts-merge"],
                },
            },
            "dynamic-programming": {
                "name": "Dynamic Programming",
                "target": 40,
                "weight": 1.2,
                "prerequisites": ["arrays-hashing", "recursion-backtracking"],
                "est_hours": 20,
                "phase": "core",
                "difficulty_distribution": {"easy": 10, "medium": 18, "hard": 12},
                "sub_topics": ["climbing-stairs", "coin-change", "longest-increasing-subsequence", "edit-distance", "word-break", "house-robber", "unique-paths", "decode-ways", "maximum-product-subarray", "longest-common-subsequence", "longest-common-substring", "minimum-path-sum", "target-sum", "partition-equal-subset-sum", "burst-balloons", "matrix-chain-multiplication", "regular-expression-matching", "wildcard-matching", "distinct-subsequences", "interleaving-string", "minimum-insertion-steps", "longest-increasing-path", "coin-change-2", "best-time-to-buy-sell-stock", "best-time-to-buy-sell-stock-ii", "best-time-to-buy-sell-stock-iii", "best-time-to-buy-sell-stock-iv", "best-time-to-buy-sell-stock-cooldown", "best-time-to-buy-sell-stock-with-fee", "palindromic-substrings", "counting-bits", "integer-break", "decode-ways", "word-break-ii", "concatenated-words", "house-robber-ii", "perfect-squares", "triangle", "minimum-falling-path"],
                "patterns": ["dp-1d", "dp-2d", "dp-on-trees", "knapsack", "lcs", "lis", "matrix-dp", "bitmask-dp"],
                "learning_module_ids": ["dp-patterns", "dp-advanced"],
                "company_sources": {
                    "amazon": ["coin-change", "house-robber", "decode-ways"],
                    "google": ["edit-distance", "longest-increasing-subsequence", "word-break"],
                    "meta": ["word-break", "burst-balloons"],
                    "microsoft": ["unique-paths", "minimum-path-sum"],
                },
            },
            "recursion-backtracking": {
                "name": "Recursion & Backtracking",
                "target": 20,
                "weight": 1.0,
                "prerequisites": ["arrays-hashing"],
                "est_hours": 8,
                "phase": "foundation",
                "difficulty_distribution": {"easy": 6, "medium": 9, "hard": 5},
                "sub_topics": ["subsets", "permutations", "word-search", "n-queens", "sudoku-solver", "letter-combinations-phone-number", "generate-parentheses", "combination-sum", "combination-sum-ii", "permutations-ii", "palindrome-partitioning", "restore-ip-addresses", "subsets-ii", "gray-code", "matchsticks-to-square", "splitting-a-string-into-descending-consecutive-values", "find-the-winner", "robot-room-cleaner"],
                "patterns": ["backtracking", "memoization"],
                "learning_module_ids": ["recursion-fundamentals"],
                "company_sources": {
                    "amazon": ["letter-combinations-phone-number", "generate-parentheses"],
                    "google": ["word-search", "n-queens"],
                    "meta": ["permutations", "combination-sum"],
                },
            },
            "heap-greedy": {
                "name": "Heap & Greedy",
                "target": 20,
                "weight": 0.9,
                "prerequisites": ["arrays-hashing", "stacks-queues"],
                "est_hours": 8,
                "phase": "core",
                "difficulty_distribution": {"easy": 5, "medium": 10, "hard": 5},
                "sub_topics": ["kth-largest-element-in-array", "merge-intervals", "non-overlapping-intervals", "task-scheduler", "minimum-number-of-arrows-to-burst-balloons", "jump-game", "gas-station", "hand-of-straights", "partition-labels", "largest-number", "queue-reconstruction-by-height", "course-schedule-iii", "car-pooling", "ipo", "find-median-from-data-stream", "sliding-window-median", "meeting-rooms-ii", "kth-smallest-in-sorted-matrix", "design-twitter", "trapping-rain-water-ii", "swim-in-rising-water"],
                "patterns": ["heap", "greedy", "priority-queue", "interval-scheduling"],
                "learning_module_ids": ["heap-priority-queue"],
                "company_sources": {
                    "amazon": ["task-scheduler", "merge-intervals", "car-pooling"],
                    "google": ["kth-largest-element-in-array", "find-median-from-data-stream"],
                    "meta": ["meeting-rooms-ii", "design-twitter"],
                },
            },
            "system-design": {
                "name": "System Design",
                "target": 20,
                "weight": 0.8,
                "prerequisites": ["trees", "graphs"],
                "est_hours": 25,
                "phase": "advanced",
                "difficulty_distribution": {"easy": 0, "medium": 5, "hard": 15},
                "sub_topics": ["url-shortener", "message-queue", "cache-strategy", "rate-limiting", "distributed-systems", "design-twitter", "design-web-crawler", "design-youtube", "design-uber", "design-dropbox", "design-whatsapp", "design-tinder", "design-airbnb", "design-yelp", "design-pastebin", "load-balancer", "cdn-design", "distributed-cache", "consistent-hashing", "cap-theorem", "sql-vs-nosql", "sharding", "replication", "message-queues-kafka", "search-autocomplete", "instagram-photo-sharing", "notification-system", "metrics-monitoring"],
                "patterns": ["system-design", "scalability", "distributed-systems"],
                "learning_module_ids": ["system-design-intro", "system-design-deep-dive"],
                "company_sources": {
                    "amazon": ["design-twitter", "cache-strategy", "design-yelp"],
                    "google": ["distributed-systems", "design-web-crawler", "search-autocomplete"],
                    "microsoft": ["url-shortener", "design-pastebin"],
                    "meta": ["design-instagram", "design-whatsapp"],
                    "uber": ["design-uber", "design-yelp"],
                },
            },
            "dbms": {
                "name": "DBMS & SQL",
                "target": 20,
                "weight": 0.7,
                "prerequisites": [],
                "est_hours": 10,
                "phase": "advanced",
                "difficulty_distribution": {"easy": 8, "medium": 9, "hard": 3},
                "sub_topics": ["indexing", "normalization", "transactions", "deadlocks", "acid-properties", "locking", "sql-joins", "sql-aggregations", "sql-subqueries", "sql-window-functions", "sql-cte", "query-optimization", "execution-plans", "stored-procedures", "triggers", "views", "materialized-views", "partitioning", "replication", "nosql-basics", "database-sharding"],
                "patterns": ["dbms", "database-design", "sql"],
                "learning_module_ids": ["dbms-fundamentals", "sql-advanced"],
                "company_sources": {
                    "amazon": ["transactions", "indexing", "sql-window-functions"],
                    "tcs": ["normalization", "sql-joins"],
                    "google": ["query-optimization", "replication"],
                    "microsoft": ["stored-procedures", "partitioning"],
                },
            },
            "oop": {
                "name": "OOP & Design Patterns",
                "target": 15,
                "weight": 0.7,
                "prerequisites": [],
                "est_hours": 8,
                "phase": "advanced",
                "difficulty_distribution": {"easy": 5, "medium": 7, "hard": 3},
                "sub_topics": ["encapsulation", "inheritance", "polymorphism", "design-patterns", "solid-principles", "composite-pattern", "factory-method", "observer-pattern", "singleton-pattern", "strategy-pattern", "decorator-pattern", "adapter-pattern", "facade-pattern", "template-method", "builder-pattern", "prototype-pattern", "abstract-factory", "state-pattern", "command-pattern", "mediator-pattern", "mvc-pattern"],
                "patterns": ["oop", "design-patterns"],
                "learning_module_ids": ["oop-design-patterns"],
                "company_sources": {
                    "amazon": ["design-patterns", "solid-principles"],
                    "microsoft": ["solid-principles", "factory-method"],
                    "google": ["observer-pattern", "strategy-pattern"],
                },
            },
            "networks": {
                "name": "Computer Networks",
                "target": 12,
                "weight": 0.6,
                "prerequisites": ["dbms"],
                "est_hours": 6,
                "phase": "advanced",
                "difficulty_distribution": {"easy": 5, "medium": 5, "hard": 2},
                "sub_topics": ["tcp-handshake", "http-vs-https", "cdn", "load-balancer", "dns", "osi-model", "rest-vs-graphql", "websocket", "http2-http3", "tls-ssl", "subnetting", "routing-protocols", "nat", "firewall", "vpn", "proxy-servers", "network-security", "ddos-mitigation", "rate-limiting", "api-gateway"],
                "patterns": ["networking", "system-design"],
                "learning_module_ids": ["networking-basics"],
                "company_sources": {
                    "google": ["cdn", "load-balancer", "http2-http3"],
                    "amazon": ["http-vs-https", "websocket", "api-gateway"],
                    "microsoft": ["rest-vs-graphql", "tls-ssl"],
                },
            },
            "os": {
                "name": "Operating Systems",
                "target": 12,
                "weight": 0.6,
                "prerequisites": [],
                "est_hours": 6,
                "phase": "advanced",
                "difficulty_distribution": {"easy": 4, "medium": 6, "hard": 2},
                "sub_topics": ["process-vs-thread", "scheduling", "deadlocks", "virtual-memory", "paging", "semaphores", "mutex", "memory-management", "file-systems", "io-management", "interprocess-communication", "context-switching", "page-replacement", "disk-scheduling", "cpu-scheduling", "thrashing", "system-calls"],
                "patterns": ["os", "systems"],
                "learning_module_ids": ["os-fundamentals"],
                "company_sources": {
                    "amazon": ["process-vs-thread", "deadlocks"],
                    "google": ["memory-management", "virtual-memory"],
                    "microsoft": ["scheduling", "semaphores"],
                },
            },
            "behavioral": {
                "name": "Behavioral & HR",
                "target": 8,
                "weight": 0.5,
                "prerequisites": [],
                "est_hours": 4,
                "phase": "job-ready",
                "difficulty_distribution": {"easy": 4, "medium": 4, "hard": 0},
                "sub_topics": ["star-method", "leadership-principles", "conflict-resolution", "failure-handling", "teamwork", "project-deep-dive", "why-company", "why-this-role"],
                "patterns": ["behavioral", "communication"],
                "learning_module_ids": ["behavioral-stars", "amazon-lp", "google-googliness"],
                "company_sources": {
                    "amazon": ["leadership-principles"],
                    "google": ["googliness"],
                    "microsoft": ["growth-mindset"],
                    "meta": ["move-fast"],
                },
            },
            "aptitude": {
                "name": "Quantitative Aptitude",
                "target": 15,
                "weight": 0.5,
                "prerequisites": [],
                "est_hours": 8,
                "phase": "job-ready",
                "difficulty_distribution": {"easy": 6, "medium": 6, "hard": 3},
                "sub_topics": ["percentages", "profit-loss", "time-work", "time-speed-distance", "probability", "permutations-combinations", "number-system", "algebra", "geometry", "mensuration", "data-interpretation", "ratios", "averages", "mixtures", "simple-compound-interest"],
                "patterns": ["aptitude", "quantitative"],
                "learning_module_ids": ["aptitude-quant", "aptitude-logical"],
                "company_sources": {
                    "tcs": ["percentages", "profit-loss", "time-work"],
                    "infosys": ["time-speed-distance", "probability"],
                    "wipro": ["permutations-combinations", "data-interpretation"],
                },
            },
        },
        "mock_test": {
            "name": "SDE Full Mock Interview",
            "total_questions": 5,
            "time_limit_minutes": 120,
            "sections": [
                {"name": "Coding 1 (Easy-Medium)", "type": "coding", "count": 1, "time_minutes": 25, "difficulty": "easy-medium"},
                {"name": "Coding 2 (Medium-Hard)", "type": "coding", "count": 1, "time_minutes": 35, "difficulty": "medium-hard"},
                {"name": "System Design", "type": "design", "count": 1, "time_minutes": 30, "difficulty": "hard"},
                {"name": "Behavioral (Amazon LP)", "type": "behavioral", "count": 1, "time_minutes": 15, "difficulty": "medium"},
                {"name": "CS Fundamentals", "type": "theory", "count": 1, "time_minutes": 15, "difficulty": "medium"},
            ],
        },
        "company_specific_paths": {
            "amazon": {
                "focus_areas": ["arrays-hashing", "dynamic-programming", "trees", "graphs", "system-design", "leadership-principles"],
                "question_count": 150,
                "duration_weeks": 6,
                "key_topics": ["two-sum", "lru-cache", "word-ladder", "serialize-deserialize", "design-twitter", "14-leadership-principles"],
            },
            "google": {
                "focus_areas": ["graphs", "dynamic-programming", "trees", "system-design", "googliness"],
                "question_count": 120,
                "duration_weeks": 8,
                "key_topics": ["word-ladder", "edit-distance", "number-of-islands", "design-search-autocomplete", "design-youtube"],
            },
            "microsoft": {
                "focus_areas": ["arrays-hashing", "linked-lists", "trees", "system-design"],
                "question_count": 100,
                "duration_weeks": 5,
                "key_topics": ["two-sum", "reverse-linked-list", "validate-bst", "design-url-shortener", "star-method"],
            },
            "tcs": {
                "focus_areas": ["aptitude", "arrays-hashing", "strings", "dbms"],
                "question_count": 80,
                "duration_weeks": 3,
                "key_topics": ["nqt-pattern", "coding-easy", "technical-mcq", "hr-round"],
            },
        },
    },

    # =========================================================
    # 2. Data Analyst
    # =========================================================
    "data-analyst": {
        "role_id": "data-analyst",
        "display_name": "Data Analyst",
        "icon": "📊",
        "description": "SQL, statistics, Python/R, data visualization, and business intelligence.",
        "target_companies": ["Amazon", "Google", "Microsoft", "TCS", "Wipro", "Accenture", "Flipkart", "Swiggy", "Razorpay"],
        "estimated_weeks": 12,
        "total_questions_target": 400,
        "progression_phases": {
            "foundation": {
                "name": "Foundation (Beginner)",
                "weeks": 1,
                "description": "SQL basics, statistics fundamentals, Excel",
                "skills": ["sql-basics", "statistics", "excel", "python-basics"],
                "learning_module_ids": ["sql-fundamentals", "stats-intro", "excel-advanced"],
                "milestone": "Write 30+ SQL queries and basic statistical analyses",
            },
            "core": {
                "name": "Core (Intermediate)",
                "weeks": 2,
                "description": "Advanced SQL, Python/R for data, statistical inference",
                "skills": ["sql", "python", "r-language", "statistics-inference", "data-cleaning"],
                "learning_module_ids": ["sql-advanced", "python-pandas", "r-programming", "hypothesis-testing"],
                "milestone": "Build complete data pipeline with SQL + Python",
            },
            "advanced": {
                "name": "Advanced",
                "weeks": 3,
                "description": "A/B testing, visualization, case studies, BI tools",
                "skills": ["ab-testing", "data-viz", "case-studies", "tableau", "powerbi"],
                "learning_module_ids": ["ab-testing-deep-dive", "tableau-mastery", "power-bi", "case-study-frameworks"],
                "milestone": "Design and analyze 5+ A/B tests, build 3+ dashboards",
            },
            "job-ready": {
                "name": "Job Ready",
                "weeks": 4,
                "description": "Mock interviews, product sense, business communication",
                "skills": ["product-analytics", "business-communication", "mock-interviews"],
                "learning_module_ids": ["product-metrics", "mock-analyst-interview"],
                "milestone": "Clear 3+ full mock analyst interview loops",
            },
        },
        "skill_tree": {
            "sql-basics": {
                "name": "SQL Basics",
                "target": 30,
                "weight": 1.0,
                "prerequisites": [],
                "est_hours": 10,
                "phase": "foundation",
                "difficulty_distribution": {"easy": 15, "medium": 12, "hard": 3},
                "sub_topics": ["select-where", "order-by-limit", "joins-inner-outer", "group-by-aggregate", "having-clause", "subqueries", "insert-update-delete", "create-table", "alter-table", "constraints", "string-functions", "date-functions", "null-handling", "case-when", "union-intersect", "exists-not-exists", "in-not-in", "between-and", "like-pattern-matching"],
                "patterns": ["sql-query", "data-filtering", "aggregation"],
                "learning_module_ids": ["sql-fundamentals"],
                "company_sources": {
                    "amazon": ["joins-inner-outer", "group-by-aggregate"],
                    "tcs": ["select-where", "order-by-limit"],
                    "google": ["subqueries", "case-when"],
                },
            },
            "sql": {
                "name": "Advanced SQL",
                "target": 50,
                "weight": 1.0,
                "prerequisites": ["sql-basics"],
                "est_hours": 18,
                "phase": "core",
                "difficulty_distribution": {"easy": 15, "medium": 25, "hard": 10},
                "sub_topics": ["window-functions", "cte-recursive", "pivot-unpivot", "performance-optimization", "execution-plans", "indexing-strategies", "query-rewriting", "correlated-subqueries", "derived-tables", "materialized-views", "stored-procedures", "triggers", "transactions-isolation", "deadlocks-handling", "partitioning", "sharding", "replication", "nosql-basics", "date-time-tricks", "string-aggregation", "array-functions", "json-queries", "hierarchical-queries"],
                "patterns": ["sql", "window-functions", "cte", "optimization"],
                "learning_module_ids": ["sql-advanced", "sql-window-functions"],
                "company_sources": {
                    "amazon": ["window-functions", "cte-recursive", "performance-optimization"],
                    "google": ["query-rewriting", "execution-plans"],
                    "microsoft": ["pivot-unpivot", "json-queries"],
                    "tcs": ["correlated-subqueries", "hierarchical-queries"],
                },
            },
            "statistics": {
                "name": "Statistics & Probability",
                "target": 35,
                "weight": 1.0,
                "prerequisites": [],
                "est_hours": 12,
                "phase": "foundation",
                "difficulty_distribution": {"easy": 12, "medium": 18, "hard": 5},
                "sub_topics": ["mean-median-mode", "variance-stddev", "probability-basics", "distributions-normal", "distributions-binomial", "distributions-poisson", "bayes-theorem", "correlation-vs-causation", "sampling-methods", "central-limit-theorem", "confidence-intervals", "z-score", "percentiles", "outlier-detection", "skewness-kurtosis", "covariance-correlation"],
                "patterns": ["statistics", "probability"],
                "learning_module_ids": ["stats-intro", "probability-fundamentals"],
                "company_sources": {
                    "amazon": ["probability-basics", "bayes-theorem", "confidence-intervals"],
                    "google": ["distributions-normal", "sampling-methods", "central-limit-theorem"],
                },
            },
            "python": {
                "name": "Python for Data Analysis",
                "target": 35,
                "weight": 0.9,
                "prerequisites": ["statistics"],
                "est_hours": 15,
                "phase": "core",
                "difficulty_distribution": {"easy": 12, "medium": 18, "hard": 5},
                "sub_topics": ["pandas-dataframes", "numpy-arrays", "data-aggregation-groupby", "data-merging-joining", "date-time-handling", "missing-data-handling", "pivot-tables", "melt-stack", "apply-map-transform", "lambda-functions", "list-comprehensions", "file-io-csv-json", "regex-basics", "data-validation", "performance-optimization", "vectorization", "categorical-encoding", "scaling-normalization", "outlier-treatment"],
                "patterns": ["python", "pandas", "numpy"],
                "learning_module_ids": ["python-pandas", "numpy-fundamentals"],
                "company_sources": {
                    "google": ["pandas-dataframes", "data-aggregation-groupby"],
                    "amazon": ["data-merging-joining", "performance-optimization"],
                },
            },
            "r-language": {
                "name": "R Programming",
                "target": 20,
                "weight": 0.7,
                "prerequisites": ["statistics"],
                "est_hours": 8,
                "phase": "core",
                "difficulty_distribution": {"easy": 8, "medium": 9, "hard": 3},
                "sub_topics": ["r-data-structures", "dplyr-mutation", "ggplot2", "r-modeling", "r-markdown", "tidyr-reshaping", "purrr-functional", "lubridate-dates", "stringr", "forcats", "shiny-basics"],
                "patterns": ["r-language", "ggplot"],
                "learning_module_ids": ["r-programming", "ggplot2"],
                "company_sources": {},
            },
            "data-viz": {
                "name": "Data Visualization (Tableau/Power BI)",
                "target": 20,
                "weight": 0.8,
                "prerequisites": ["python", "r-language"],
                "est_hours": 10,
                "phase": "advanced",
                "difficulty_distribution": {"easy": 6, "medium": 10, "hard": 4},
                "sub_topics": ["tableau-charts", "tableau-calculated-fields", "tableau-parameters", "tableau-lod", "tableau-dashboards", "tableau-storytelling", "powerbi-dax", "powerbi-power-query", "powerbi-dataflows", "dashboard-design", "storytelling", "interactive-filters", "kpi-dashboards", "data-modeling", "drill-down-hierarchies", "geographic-visualization", "time-series-viz"],
                "patterns": ["data-viz", "bi-tools"],
                "learning_module_ids": ["tableau-mastery", "power-bi"],
                "company_sources": {
                    "amazon": ["dashboard-design", "kpi-dashboards"],
                    "google": ["tableau-calculated-fields", "tableau-lod"],
                    "microsoft": ["powerbi-dax", "powerbi-power-query"],
                },
            },
            "excel": {
                "name": "Advanced Excel",
                "target": 20,
                "weight": 0.7,
                "prerequisites": [],
                "est_hours": 6,
                "phase": "foundation",
                "difficulty_distribution": {"easy": 10, "medium": 8, "hard": 2},
                "sub_topics": ["pivot-tables", "vlookup-hlookup", "index-match", "xlookup", "advanced-formulas", "data-validation", "conditional-formatting", "what-if-analysis", "solver", "macros-vba", "power-query", "power-pivot", "charts-advanced", "sparklines", "slicers-timelines", "data-tables"],
                "patterns": ["excel"],
                "learning_module_ids": ["excel-advanced"],
                "company_sources": {
                    "tcs": ["pivot-tables", "vlookup-hlookup"],
                    "infosys": ["index-match", "xlookup"],
                    "wipro": ["data-validation", "conditional-formatting"],
                },
            },
            "statistics-inference": {
                "name": "Statistical Inference & Hypothesis Testing",
                "target": 30,
                "weight": 1.0,
                "prerequisites": ["statistics"],
                "est_hours": 12,
                "phase": "core",
                "difficulty_distribution": {"easy": 8, "medium": 15, "hard": 7},
                "sub_topics": ["confidence-intervals", "hypothesis-testing", "t-test-one-sample", "t-test-two-sample", "paired-t-test", "chi-square-test", "anova-one-way", "anova-two-way", "p-value-interpretation", "type-i-type-ii-errors", "power-analysis", "non-parametric-tests", "mann-whitney-u", "wilcoxon-signed-rank", "kruskal-wallis", "bootstrap-methods", "permutation-tests", "multiple-testing-correction"],
                "patterns": ["statistics-inference"],
                "learning_module_ids": ["hypothesis-testing", "inferential-stats"],
                "company_sources": {
                    "amazon": ["hypothesis-testing", "t-test-two-sample", "p-value-interpretation"],
                    "google": ["anova-one-way", "chi-square-test", "power-analysis"],
                },
            },
            "ab-testing": {
                "name": "A/B Testing & Experimentation",
                "target": 20,
                "weight": 0.9,
                "prerequisites": ["statistics-inference", "sql"],
                "est_hours": 8,
                "phase": "advanced",
                "difficulty_distribution": {"easy": 5, "medium": 10, "hard": 5},
                "sub_topics": ["experiment-design", "significance-testing", "conversion-rate", "sample-size-calculation", "novelty-effect", "sequential-testing", "multi-armed-bandits", "bayesian-ab-testing", "cupid-peeking", "false-discovery-rate", "interference-network-effects", "long-term-effects", "guardrail-metrics", "power-analysis-experiments", "stratified-sampling", "cluster-randomization"],
                "patterns": ["ab-testing", "experimentation"],
                "learning_module_ids": ["ab-testing-deep-dive"],
                "company_sources": {
                    "google": ["experiment-design", "sequential-testing", "cupid-peeking"],
                    "amazon": ["conversion-rate", "sample-size-calculation"],
                    "microsoft": ["multi-armed-bandits", "bayesian-ab-testing"],
                },
            },
            "data-cleaning": {
                "name": "Data Cleaning & Preprocessing",
                "target": 20,
                "weight": 0.8,
                "prerequisites": ["python"],
                "est_hours": 8,
                "phase": "core",
                "difficulty_distribution": {"easy": 8, "medium": 9, "hard": 3},
                "sub_topics": ["missing-values-imputation", "outlier-detection", "data-types-conversion", "duplicate-handling", "normalization-standardization", "encoding-categorical", "feature-scaling", "text-preprocessing", "regex-cleaning", "data-validation", "schema-validation", "deduplication-strategies", "data-profiling", "data-quality-metrics"],
                "patterns": ["data-cleaning", "preprocessing"],
                "learning_module_ids": ["data-preprocessing"],
                "company_sources": {
                    "tcs": ["missing-values-imputation", "duplicate-handling"],
                    "infosys": ["outlier-detection", "data-types-conversion"],
                },
            },
            "case-studies": {
                "name": "Business Case Studies",
                "target": 15,
                "weight": 0.6,
                "prerequisites": ["sql", "statistics-inference", "excel"],
                "est_hours": 10,
                "phase": "advanced",
                "difficulty_distribution": {"easy": 4, "medium": 8, "hard": 3},
                "sub_topics": ["metric-definition", "problem-framing", "data-collection-strategy", "analysis-plan", "recommendation-writing", "impact-measurement", "stakeholder-communication", "executive-summaries", "data-storytelling", "root-cause-analysis", "cohort-analysis", "funnel-analysis", "retention-analysis", "revenue-analysis"],
                "patterns": ["case-study", "business-analysis"],
                "learning_module_ids": ["case-study-frameworks"],
                "company_sources": {},
            },
            "product-analytics": {
                "name": "Product Analytics & Metrics",
                "target": 15,
                "weight": 0.7,
                "prerequisites": ["ab-testing", "data-viz"],
                "est_hours": 6,
                "phase": "job-ready",
                "difficulty_distribution": {"easy": 5, "medium": 7, "hard": 3},
                "sub_topics": ["north-star-metric", "kpi-definition", "cohort-analysis", "funnel-analysis", "retention-curves", "engagement-metrics", "revenue-metrics", "user-segmentation", "behavioral-analytics", "product-sense", "metric-tree", "counter-metrics"],
                "patterns": ["product-analytics", "metrics"],
                "learning_module_ids": ["product-metrics"],
                "company_sources": {
                    "google": ["north-star-metric", "metric-tree"],
                    "meta": ["engagement-metrics", "user-segmentation"],
                },
            },
        },
        "mock_test": {
            "name": "Data Analyst Case Study Mock",
            "total_questions": 8,
            "time_limit_minutes": 150,
            "sections": [
                {"name": "SQL Problem (3 queries)", "type": "sql", "count": 1, "time_minutes": 45, "difficulty": "medium"},
                {"name": "Statistics Question", "type": "aptitude", "count": 1, "time_minutes": 25, "difficulty": "medium"},
                {"name": "Case Study Analysis", "type": "case_study", "count": 1, "time_minutes": 40, "difficulty": "hard"},
                {"name": "Data Cleaning Challenge", "type": "coding", "count": 1, "time_minutes": 20, "difficulty": "medium"},
                {"name": "Visualization Interpretation", "type": "mcq", "count": 1, "time_minutes": 10, "difficulty": "easy"},
                {"name": "A/B Test Design", "type": "mcq", "count": 1, "time_minutes": 10, "difficulty": "medium"},
                {"name": "Python/R Analysis", "type": "coding", "count": 1, "time_minutes": 0, "difficulty": "medium"},
            ],
        },
        "company_specific_paths": {
            "amazon": {
                "focus_areas": ["sql", "statistics", "ab-testing", "case-studies"],
                "question_count": 100,
                "duration_weeks": 4,
                "key_topics": ["sql-window-functions", "hypothesis-testing", "metric-definition", "business-recommendations"],
            },
            "google": {
                "focus_areas": ["statistics-inference", "ab-testing", "product-analytics", "case-studies"],
                "question_count": 80,
                "duration_weeks": 5,
                "key_topics": ["experiment-design", "statistical-rigor", "product-sense", "data-storytelling"],
            },
        },
    },

    # =========================================================
    # 3. AI Engineer
    # =========================================================
    "ai-engineer": {
        "role_id": "ai-engineer",
        "display_name": "AI/Machine Learning Engineer",
        "icon": "🤖",
        "description": "Machine learning, deep learning, NLP, MLOps, and AI system design.",
        "target_companies": ["Google", "Amazon", "Microsoft", "Meta", "OpenAI", "NVIDIA", "Apple", "Anthropic"],
        "estimated_weeks": 20,
        "total_questions_target": 450,
        "progression_phases": {
            "foundation": {
                "name": "Foundation (Beginner)",
                "weeks": 1,
                "description": "Python, math foundations, ML basics",
                "skills": ["python-ml", "math-foundations", "ml-fundamentals"],
                "learning_module_ids": ["python-for-ml", "linear-algebra", "calculus", "ml-intro"],
                "milestone": "Implement basic ML algorithms from scratch",
            },
            "core": {
                "name": "Core (Intermediate)",
                "weeks": 2,
                "description": "Deep learning, NLP, computer vision, frameworks",
                "skills": ["deep-learning", "pytorch", "tensorflow", "nlp", "feature-engineering"],
                "learning_module_ids": ["pytorch-basics", "tensorflow-keras", "nlp-fundamentals", "cv-basics"],
                "milestone": "Build and train neural networks for real tasks",
            },
            "advanced": {
                "name": "Advanced",
                "weeks": 3,
                "description": "Advanced architectures, MLOps, deployment",
                "skills": ["mlops", "model-evaluation", "mlops-deployment", "computer-vision"],
                "learning_module_ids": ["mlops-pipeline", "transformers-llms", "model-deployment", "model-monitoring"],
                "milestone": "Deploy and monitor ML models in production",
            },
            "job-ready": {
                "name": "Job Ready",
                "weeks": 4,
                "description": "System design, research papers, mock interviews",
                "skills": ["mock-interviews"],
                "learning_module_ids": ["ml-system-design", "mock-ai-interview"],
                "milestone": "Clear 3+ AI engineer mock interview loops",
            },
        },
        "skill_tree": {
            "ml-fundamentals": {
                "name": "ML Fundamentals",
                "target": 30,
                "weight": 1.0,
                "prerequisites": ["math-foundations"],
                "est_hours": 10,
                "sub_topics": ["linear-regression", "logistic-regression", "decision-trees", "random-forest", "gradient-boosting", "svm", "knn", "naive-bayes", "model-selection", "cross-validation"],
                "patterns": ["ml-fundamentals"],
                "company_sources": {
                    "google": ["model-selection", "cross-validation"],
                    "amazon": ["random-forest", "gradient-boosting"],
                },
            },
            "deep-learning": {
                "name": "Deep Learning (Neural Networks)",
                "target": 30,
                "weight": 1.1,
                "prerequisites": ["ml-fundamentals", "math-foundations"],
                "est_hours": 12,
                "sub_topics": ["perceptron", "backpropagation", "cnn", "rnn", "lstm", "transformer", "attention-mechanism", "transfer-learning", "fine-tuning", "distributed-training"],
                "patterns": ["deep-learning", "pytorch", "tensorflow"],
                "company_sources": {
                    "google": ["transformer", "attention-mechanism"],
                    "meta": ["distributed-training", "fine-tuning"],
                    "nvidia": ["cnn", "transfer-learning"],
                },
            },
            "nlp": {
                "name": "Natural Language Processing",
                "target": 25,
                "weight": 1.0,
                "prerequisites": ["ml-fundamentals", "deep-learning"],
                "est_hours": 10,
                "sub_topics": ["tokenization", "word-embeddings", "bert", "gpt", "text-classification", "ner", "sentiment-analysis", "machine-translation", "summarization", "rag"],
                "patterns": ["nlp", "transformer", "pytorch"],
                "company_sources": {
                    "google": ["bert", "rag"],
                    "meta": ["gpt", "summarization"],
                    "openai": ["gpt", "fine-tuning"],
                },
            },
            "computer-vision": {
                "name": "Computer Vision",
                "target": 15,
                "weight": 0.8,
                "prerequisites": ["deep-learning"],
                "est_hours": 8,
                "sub_topics": ["image-classification", "object-detection", "segmentation", "yolo", "faster-rcnn", "unet", "data-augmentation", "transfer-learning", "edge-deployment"],
                "patterns": ["computer-vision", "deep-learning", "pytorch"],
                "company_sources": {
                    "nvidia": ["object-detection", "yolo"],
                    "google": ["image-classification", "segmentation"],
                },
            },
            "mlops": {
                "name": "MLOps & Deployment",
                "target": 20,
                "weight": 0.9,
                "prerequisites": ["ml-fundamentals"],
                "est_hours": 8,
                "sub_topics": ["mlflow", "kubeflow", "model-registry", "ci-cd-ml", "data-versioning", "model-monitoring", "drift-detection", "a-b-testing-ml", "feature-store", "pipeline-orchestration"],
                "patterns": ["mlops", "kubernetes", "docker"],
                "company_sources": {
                    "amazon": ["mlflow", "model-monitoring"],
                    "google": ["kubeflow", "feature-store"],
                },
            },
            "python-ml": {
                "name": "Python for ML (NumPy, Pandas, Scikit-Learn)",
                "target": 25,
                "weight": 0.9,
                "prerequisites": [],
                "est_hours": 6,
                "sub_topics": ["numpy-operations", "pandas-dataframes", "sklearn-pipelines", "preprocessing", "model-evaluation", "hyperparameter-tuning", "cross-validation", "feature-selection"],
                "patterns": ["python-ml", "pandas", "sklearn"],
                "company_sources": {
                    "google": ["sklearn-pipelines", "cross-validation"],
                    "amazon": ["feature-selection", "hyperparameter-tuning"],
                },
            },
            "pytorch": {
                "name": "PyTorch",
                "target": 20,
                "weight": 0.8,
                "prerequisites": ["deep-learning"],
                "est_hours": 6,
                "sub_topics": ["tensors", "autograd", "nn-module", "data-loader", "optimizer", "loss-functions", "custom-layers", "distributed-training", "onnx-export"],
                "patterns": ["pytorch", "deep-learning"],
                "company_sources": {
                    "meta": ["distributed-training", "custom-layers"],
                    "nvidia": ["onnx-export", "tensorrt"],
                },
            },
            "tensorflow": {
                "name": "TensorFlow/Keras",
                "target": 15,
                "weight": 0.7,
                "prerequisites": ["deep-learning"],
                "est_hours": 5,
                "sub_topics": ["keras-api", "tf-data", "estimator", "savedmodel", "tflite", "tf-serving", "distributed-strategies", "custom-training-loops"],
                "patterns": ["tensorflow", "deep-learning"],
                "company_sources": {
                    "google": ["tf-serving", "distributed-strategies"],
                },
            },
            "feature-engineering": {
                "name": "Feature Engineering",
                "target": 20,
                "weight": 0.9,
                "prerequisites": ["ml-fundamentals", "python-ml"],
                "est_hours": 7,
                "sub_topics": ["encoding-categorical", "scaling-normalization", "feature-selection", "polynomial-features", "interaction-features", "embedding-learning", "text-features", "time-series-features", "feature-store"],
                "patterns": ["feature-engineering", "ml-fundamentals"],
                "company_sources": {
                    "amazon": ["feature-store", "encoding-categorical"],
                    "google": ["embedding-learning", "time-series-features"],
                },
            },
            "model-evaluation": {
                "name": "Model Evaluation & Tuning",
                "target": 15,
                "weight": 0.8,
                "prerequisites": ["ml-fundamentals"],
                "est_hours": 5,
                "sub_topics": ["confusion-matrix", "roc-auc", "precision-recall", "f1-score", "calibration", "hyperparameter-search", "bayesian-optimization", "learning-curves", "bias-variance"],
                "patterns": ["model-evaluation", "ml-fundamentals"],
                "company_sources": {
                    "google": ["bayesian-optimization", "calibration"],
                    "amazon": ["precision-recall", "learning-curves"],
                },
            },
            "mlops-deployment": {
                "name": "ML Model Deployment (FastAPI/Flask)",
                "target": 15,
                "weight": 0.8,
                "prerequisites": ["mlops", "python-ml"],
                "est_hours": 6,
                "sub_topics": ["fastapi-endpoints", "model-serialization", "batch-inference", "streaming-inference", "model-quantization", "docker-ml", "k8s-deployment", "monitoring-endpoints", "shadow-deployment"],
                "patterns": ["mlops-deployment", "fastapi", "docker"],
                "company_sources": {
                    "amazon": ["batch-inference", "k8s-deployment"],
                    "google": ["model-quantization", "shadow-deployment"],
                },
            },
            "math-foundations": {
                "name": "Math Foundations (Linear Algebra, Calculus)",
                "target": 20,
                "weight": 1.0,
                "prerequisites": [],
                "est_hours": 8,
                "sub_topics": ["matrix-operations", "eigenvalues", "svd", "gradient-descent", "chain-rule", "convex-optimization", "probability-distributions", "information-theory", "statistical-learning-theory"],
                "patterns": ["math-foundations"],
                "company_sources": {
                    "google": ["gradient-descent", "convex-optimization"],
                    "amazon": ["information-theory", "probability-distributions"],
                },
            },
        },
        "mock_test": {
            "name": "AI Engineer Technical Mock",
            "total_questions": 6,
            "time_limit_minutes": 180,
            "sections": [
                {"name": "ML Theory (10 concepts)", "type": "mcq", "count": 1, "time_minutes": 30},
                {"name": "Coding (Python ML)", "type": "coding", "count": 1, "time_minutes": 50},
                {"name": "NLP Problem", "type": "coding", "count": 1, "time_minutes": 40},
                {"name": "Deep Learning Design", "type": "design", "count": 1, "time_minutes": 30},
                {"name": "MLOps Scenario", "type": "scenario", "count": 1, "time_minutes": 20},
                {"name": "Math Foundations", "type": "math", "count": 1, "time_minutes": 10},
            ],
        },
    },

    # =========================================================
    # 4. Java Engineer
    # =========================================================
    "java-engineer": {
        "role_id": "java-engineer",
        "display_name": "Java Engineer",
        "icon": "☕",
        "description": "Core Java, OOP, Spring Framework, multithreading, and enterprise systems.",
        "target_companies": ["TCS", "Infosys", "Wipro", "Cognizant", "HCL", "Amazon", "JP Morgan", "Goldman Sachs"],
        "estimated_weeks": 14,
        "total_questions_target": 350,
        "progression_phases": {
            "foundation": {
                "name": "Foundation (Beginner)",
                "weeks": 1,
                "description": "Java syntax, OOP fundamentals, basic collections",
                "skills": ["core-java", "java-ds", "oop"],
                "learning_module_ids": ["oop-design-patterns"],
                "milestone": "Write 30+ basic Java programs with OOP",
            },
            "core": {
                "name": "Core (Intermediate)",
                "weeks": 2,
                "description": "Collections, multithreading, design patterns, JDBC",
                "skills": ["multithreading", "design-patterns", "database"],
                "learning_module_ids": ["stacks-queues", "trees-bst"],
                "milestone": "Build a multithreaded Java application",
            },
            "advanced": {
                "name": "Advanced",
                "weeks": 3,
                "description": "Spring ecosystem, microservices, JVM internals",
                "skills": ["spring-framework", "microservices", "jvm", "api-design"],
                "learning_module_ids": ["system-design-intro", "networking-basics"],
                "milestone": "Build and deploy a Spring Boot microservice",
            },
            "job-ready": {
                "name": "Job Ready",
                "weeks": 4,
                "description": "Mock interviews, system design, testing, company prep",
                "skills": ["testing", "mock-interviews"],
                "learning_module_ids": ["behavioral-stars", "mock-ai-interview"],
                "milestone": "Clear 3+ full Java mock interview loops",
            },
        },
        "skill_tree": {
            "core-java": {
                "name": "Core Java (OOP, Collections)",
                "target": 35,
                "weight": 1.0,
                "prerequisites": [],
                "est_hours": 10,
                "phase": "foundation",
                "difficulty_distribution": {"easy": 12, "medium": 18, "hard": 5},
                "sub_topics": ["oop-fundamentals", "collections-framework", "generics", "exceptions", "streams-api", "lambdas", "optional", "equals-hashcode", "immutable-objects", "design-principles", "string-handling", "boxing-unboxing", "var-args", "annotations"],
                "patterns": ["core-java", "oop"],
                "learning_module_ids": ["oop-design-patterns"],
                "company_sources": {
                    "amazon": ["collections-framework", "streams-api"],
                    "tcs": ["oop-fundamentals", "exceptions"],
                    "infosys": ["generics", "lambdas"],
                },
            },
            "spring-framework": {
                "name": "Spring Framework (Boot, MVC, Security)",
                "target": 25,
                "weight": 1.0,
                "prerequisites": ["core-java"],
                "est_hours": 12,
                "sub_topics": ["dependency-injection", "spring-boot", "spring-mvc", "spring-security", "spring-data-jpa", "spring-transaction", "rest-controller", "validation", "actuator", "configuration"],
                "patterns": ["spring-framework", "spring-boot"],
                "company_sources": {
                    "amazon": ["spring-boot", "spring-security"],
                    "tcs": ["dependency-injection", "spring-mvc"],
                    "cognizant": ["spring-data-jpa", "spring-transaction"],
                },
            },
            "multithreading": {
                "name": "Java Multithreading & Concurrency",
                "target": 20,
                "weight": 0.9,
                "prerequisites": ["core-java"],
                "est_hours": 8,
                "sub_topics": ["thread-lifecycle", "synchronization", "executor-service", "completable-future", "concurrent-collections", "locks", "atomic-variables", "thread-pools", "deadlock-avoidance", "virtual-threads"],
                "patterns": ["multithreading", "concurrency"],
                "company_sources": {
                    "amazon": ["executor-service", "completable-future"],
                    "infosys": ["synchronization", "thread-pools"],
                    "wipro": ["concurrent-collections", "locks"],
                },
            },
            "java-ds": {
                "name": "Data Structures in Java",
                "target": 20,
                "weight": 0.9,
                "prerequisites": ["core-java"],
                "est_hours": 6,
                "sub_topics": ["arraylist-linkedlist", "hashmap-hashtable", "treemap", "priorityqueue", "arraydeque", "custom-comparator", "hashcode-equals", "immutable-collections", "stream-collectors", "parallel-streams"],
                "patterns": ["java-ds", "collections"],
                "company_sources": {
                    "amazon": ["hashmap-hashtable", "treemap"],
                    "tcs": ["arraylist-linkedlist", "priorityqueue"],
                },
            },
            "design-patterns": {
                "name": "Java Design Patterns",
                "target": 15,
                "weight": 0.8,
                "prerequisites": ["core-java"],
                "est_hours": 5,
                "sub_topics": ["singleton", "factory-method", "builder", "abstract-factory", "prototype", "adapter", "decorator", "strategy", "observer", "command", "template-method"],
                "patterns": ["design-patterns", "oop"],
                "company_sources": {
                    "amazon": ["factory-method", "strategy"],
                    "infosys": ["singleton", "observer"],
                },
            },
            "testing": {
                "name": "JUnit & Testing",
                "target": 10,
                "weight": 0.6,
                "prerequisites": ["core-java", "spring-framework"],
                "est_hours": 4,
                "sub_topics": ["junit5", "mockito", "unit-testing", "integration-testing", "testcontainers", "parameterized-tests", "assertj", "test-coverage", "tdd"],
                "patterns": ["testing", "junit"],
                "company_sources": {
                    "amazon": ["junit5", "mockito"],
                    "cognizant": ["integration-testing", "testcontainers"],
                },
            },
            "microservices": {
                "name": "Java Microservices",
                "target": 15,
                "weight": 0.8,
                "prerequisites": ["spring-framework", "multithreading"],
                "est_hours": 8,
                "sub_topics": ["service-discovery", "api-gateway", "circuit-breaker", "distributed-tracing", "event-driven", "saga-pattern", "docker-java", "kubernetes-deployment", "config-server", "resilience4j"],
                "patterns": ["microservices", "spring-cloud"],
                "company_sources": {
                    "amazon": ["circuit-breaker", "distributed-tracing"],
                    "cognizant": ["service-discovery", "api-gateway"],
                },
            },
            "jvm": {
                "name": "JVM Internals & Performance",
                "target": 10,
                "weight": 0.7,
                "prerequisites": ["core-java", "multithreading"],
                "est_hours": 5,
                "sub_topics": ["memory-model", "garbage-collection", "class-loading", "jit-compilation", "profiling", "heap-dumps", "gc-tuning", "escape-analysis", "jvm-flags"],
                "patterns": ["jvm", "performance"],
                "company_sources": {
                    "amazon": ["garbage-collection", "jit-compilation"],
                    "hcl": ["profiling", "gc-tuning"],
                },
            },
            "database": {
                "name": "JDBC & Database Integration",
                "target": 15,
                "weight": 0.7,
                "prerequisites": ["core-java", "spring-framework"],
                "est_hours": 6,
                "sub_topics": ["jdbc-template", "connection-pooling", "hibernate", "jpa", "transactions", "lazy-eager-loading", "n-plus-one", "query-optimization", "migrations"],
                "patterns": ["database", "jdbc", "hibernate"],
                "company_sources": {
                    "amazon": ["connection-pooling", "transactions"],
                    "tcs": ["jdbc-template", "hibernate"],
                },
            },
            "api-design": {
                "name": "REST API Design (Java)",
                "target": 10,
                "weight": 0.6,
                "prerequisites": ["spring-framework"],
                "est_hours": 4,
                "sub_topics": ["rest-principles", "http-status-codes", "versioning", "pagination", "filtering", "openapi-swagger", "error-handling", "rate-limiting", "api-security"],
                "patterns": ["api-design", "rest"],
                "company_sources": {
                    "amazon": ["rest-principles", "api-security"],
                    "cognizant": ["versioning", "openapi-swagger"],
                },
            },
        },
        "mock_test": {
            "name": "Java Engineer Mock Interview",
            "total_questions": 6,
            "time_limit_minutes": 120,
            "sections": [
                {"name": "Core Java MCQ (15 Qs)", "type": "mcq", "count": 1, "time_minutes": 25},
                {"name": "OOP & Design (2 problems)", "type": "coding", "count": 1, "time_minutes": 35},
                {"name": "Spring Boot Coding", "type": "coding", "count": 1, "time_minutes": 30},
                {"name": "Multithreading Scenario", "type": "scenario", "count": 1, "time_minutes": 15},
                {"name": "System Design (Java)", "type": "design", "count": 1, "time_minutes": 15},
            ],
        },
    },

    # =========================================================
    # 5. ML Engineer
    # =========================================================
    "ml-engineer": {
        "role_id": "ml-engineer",
        "display_name": "Machine Learning Engineer",
        "icon": "🧠",
        "description": "Applied ML, model deployment, feature engineering, and pipeline engineering.",
        "target_companies": ["Amazon", "Google", "Microsoft", "Meta", "Uber", "Netflix", "Apple"],
        "estimated_weeks": 18,
        "total_questions_target": 400,
        "progression_phases": {
            "foundation": {
                "name": "Foundation (Beginner)",
                "weeks": 1,
                "description": "Python, statistics, ML basics",
                "skills": ["python-ml", "statistics", "ml-algorithms"],
                "learning_module_ids": ["python-for-ml", "stats-intro", "ml-intro"],
                "milestone": "Implement basic ML algorithms from scratch",
            },
            "core": {
                "name": "Core (Intermediate)",
                "weeks": 2,
                "description": "Advanced algorithms, feature engineering, pipelines",
                "skills": ["unsupervised-learning", "feature-engineering", "ml-pipelines"],
                "learning_module_ids": ["supervised-learning", "unsupervised-learning", "feature-engineering"],
                "milestone": "Build complete ML pipeline with feature store",
            },
            "advanced": {
                "name": "Advanced",
                "weeks": 3,
                "description": "Model deployment, monitoring, optimization",
                "skills": ["ml-deployment", "ml-monitoring", "model-optimization"],
                "learning_module_ids": ["model-deployment", "model-monitoring", "model-evaluation"],
                "milestone": "Deploy and monitor ML models in production",
            },
            "job-ready": {
                "name": "Job Ready",
                "weeks": 4,
                "description": "ML system design, mock interviews, behavioral",
                "skills": ["ml-system-design", "mock-interviews"],
                "learning_module_ids": ["ml-system-design", "behavioral-stars", "mock-ai-interview"],
                "milestone": "Clear 3+ ML engineer mock interview loops",
            },
        },
        "skill_tree": {
            "ml-algorithms": {
                "name": "Supervised Learning Algorithms",
                "target": 25,
                "weight": 1.0,
                "prerequisites": ["python-ml", "statistics"],
                "est_hours": 8,
                "phase": "foundation",
                "difficulty_distribution": {"easy": 8, "medium": 12, "hard": 5},
                "sub_topics": ["linear-regression", "logistic-regression", "decision-trees", "random-forest", "xgboost", "lightgbm", "catboost", "svm", "knn", "ensemble-methods", "bagging-boosting", "stacking", "regularization"],
                "patterns": ["ml-algorithms", "python-ml"],
                "learning_module_ids": ["supervised-learning", "ml-intro"],
                "company_sources": {
                    "amazon": ["xgboost", "random-forest"],
                    "google": ["ensemble-methods", "lightgbm"],
                    "uber": ["xgboost", "catboost"],
                },
            },
            "unsupervised-learning": {
                "name": "Unsupervised Learning",
                "target": 15,
                "weight": 0.8,
                "prerequisites": ["ml-algorithms"],
                "est_hours": 6,
                "sub_topics": ["k-means", "hierarchical-clustering", "dbscan", "pca", "tsne", "umap", "anomaly-detection", "association-rules", "market-basket-analysis"],
                "patterns": ["unsupervised-learning", "ml-algorithms"],
                "company_sources": {
                    "netflix": ["anomaly-detection", "pca"],
                    "amazon": ["k-means", "market-basket-analysis"],
                },
            },
            "ml-pipelines": {
                "name": "ML Pipelines (Scikit-learn, TFX)",
                "target": 20,
                "weight": 0.9,
                "prerequisites": ["ml-algorithms", "python-ml"],
                "est_hours": 7,
                "sub_topics": ["sklearn-pipelines", "tfx-components", "kubeflow-pipelines", "airflow-dags", "data-validation", "transform", "trainer", "evaluator", "pusher", "pipeline-versioning"],
                "patterns": ["ml-pipelines", "tf", "kubeflow"],
                "company_sources": {
                    "google": ["tfx-components", "kubeflow-pipelines"],
                    "uber": ["airflow-dags", "pipeline-versioning"],
                },
            },
            "feature-engineering": {
                "name": "Feature Engineering",
                "target": 20,
                "weight": 1.0,
                "prerequisites": ["ml-algorithms", "python-ml"],
                "est_hours": 7,
                "sub_topics": ["encoding-categorical", "scaling-normalization", "feature-selection", "polynomial-features", "interaction-features", "embedding-learning", "text-features", "time-series-features", "feature-store", "feast"],
                "patterns": ["feature-engineering", "ml-algorithms"],
                "company_sources": {
                    "amazon": ["feature-store", "encoding-categorical"],
                    "uber": ["time-series-features", "feast"],
                    "netflix": ["embedding-learning", "interaction-features"],
                },
            },
            "ml-deployment": {
                "name": "ML Model Deployment (Sagemaker, TF Serving)",
                "target": 20,
                "weight": 0.9,
                "prerequisites": ["ml-pipelines", "ml-algorithms"],
                "est_hours": 8,
                "sub_topics": ["sagemaker-endpoints", "tf-serving", "torchserve", "batch-transform", "real-time-inference", "model-registry", "a-b-testing", "canary-deployment", "shadow-mode", "model-signatures"],
                "patterns": ["ml-deployment", "sagemaker", "tf-serving"],
                "company_sources": {
                    "amazon": ["sagemaker-endpoints", "batch-transform"],
                    "google": ["tf-serving", "model-registry"],
                    "netflix": ["canary-deployment", "shadow-mode"],
                },
            },
            "ml-monitoring": {
                "name": "Model Monitoring & Drift Detection",
                "target": 10,
                "weight": 0.7,
                "prerequisites": ["ml-deployment"],
                "est_hours": 5,
                "sub_topics": ["data-drift", "concept-drift", "prediction-drift", "performance-monitoring", "alerting", "dashboarding", "automated-retraining", "sli-slo", "mlops-integration"],
                "patterns": ["ml-monitoring", "mlops"],
                "company_sources": {
                    "amazon": ["data-drift", "automated-retraining"],
                    "google": ["concept-drift", "sli-slo"],
                },
            },
            "python-ml": {
                "name": "Python for ML (Pandas, NumPy)",
                "target": 15,
                "weight": 0.8,
                "prerequisites": [],
                "est_hours": 5,
                "sub_topics": ["numpy-operations", "pandas-dataframes", "sklearn-pipelines", "preprocessing", "model-evaluation", "hyperparameter-tuning", "cross-validation", "feature-selection"],
                "patterns": ["python-ml", "pandas", "sklearn"],
                "company_sources": {
                    "amazon": ["sklearn-pipelines", "cross-validation"],
                    "google": ["feature-selection", "hyperparameter-tuning"],
                },
            },
            "statistics": {
                "name": "Statistics for ML",
                "target": 20,
                "weight": 1.0,
                "prerequisites": [],
                "est_hours": 7,
                "sub_topics": ["probability-distributions", "bayesian-inference", "hypothesis-testing", "confidence-intervals", "statistical-significance", "power-analysis", "bootstrap", "permutation-tests", "multiple-testing-correction"],
                "patterns": ["statistics", "ml-fundamentals"],
                "company_sources": {
                    "google": ["bayesian-inference", "hypothesis-testing"],
                    "amazon": ["statistical-significance", "power-analysis"],
                },
            },
            "ml-system-design": {
                "name": "ML System Design",
                "target": 15,
                "weight": 0.9,
                "prerequisites": ["ml-pipelines", "ml-deployment", "ml-monitoring"],
                "est_hours": 8,
                "sub_topics": ["recommendation-systems", "search-ranking", "ads-targeting", "fraud-detection", "real-time-ml", "feature-store-design", "model-serving-architecture", "data-pipeline-architecture", "ml-platform-design"],
                "patterns": ["ml-system-design", "system-design"],
                "company_sources": {
                    "uber": ["recommendation-systems", "real-time-ml"],
                    "amazon": ["ads-targeting", "feature-store-design"],
                    "netflix": ["search-ranking", "model-serving-architecture"],
                },
            },
            "model-optimization": {
                "name": "Model Optimization & Quantization",
                "target": 10,
                "weight": 0.7,
                "prerequisites": ["ml-algorithms", "ml-deployment"],
                "est_hours": 5,
                "sub_topics": ["quantization", "pruning", "knowledge-distillation", "onnx-runtime", "tensorrt", "tflite", "compilation", "hardware-acceleration", "latency-optimization"],
                "patterns": ["model-optimization", "ml-deployment"],
                "company_sources": {
                    "nvidia": ["tensorrt", "hardware-acceleration"],
                    "google": ["tflite", "knowledge-distillation"],
                    "amazon": ["onnx-runtime", "quantization"],
                },
            },
        },
        "mock_test": {
            "name": "ML Engineer System Design Mock",
            "total_questions": 5,
            "time_limit_minutes": 150,
            "sections": [
                {"name": "ML Algorithm Theory (5 Qs)", "type": "mcq", "count": 1, "time_minutes": 20},
                {"name": "Feature Engineering Problem", "type": "coding", "count": 1, "time_minutes": 35},
                {"name": "Pipeline Design", "type": "design", "count": 1, "time_minutes": 45},
                {"name": "Deployment Scenario", "type": "scenario", "count": 1, "time_minutes": 30},
                {"name": "Model Monitoring Qs (3)", "type": "mcq", "count": 1, "time_minutes": 20},
            ],
        },
    },

    # =========================================================
    # 6. Data Scientist
    # =========================================================
    "data-scientist": {
        "role_id": "data-scientist",
        "display_name": "Data Scientist",
        "icon": "🔬",
        "description": "Statistical analysis, experimental design, ML, and data storytelling.",
        "target_companies": ["Google", "Amazon", "Microsoft", "Meta", "Netflix", "Airbnb", "Uber"],
        "estimated_weeks": 16,
        "total_questions_target": 380,
        "progression_phases": {
            "foundation": {
                "name": "Foundation (Beginner)",
                "weeks": 1,
                "description": "Statistics, probability, Python basics",
                "skills": ["statistics", "python-ds", "r-ds"],
                "learning_module_ids": ["stats-intro", "probability-fundamentals", "python-for-ml"],
                "milestone": "Perform basic statistical analyses with Python",
            },
            "core": {
                "name": "Core (Intermediate)",
                "weeks": 2,
                "description": "Statistical inference, ML, experimental design",
                "skills": ["statistical-inference", "experimental-design", "ml-for-ds"],
                "learning_module_ids": ["hypothesis-testing", "inferential-stats", "supervised-learning"],
                "milestone": "Design and analyze 3+ experiments",
            },
            "advanced": {
                "name": "Advanced",
                "weeks": 3,
                "description": "Advanced ML, visualization, storytelling, time series",
                "skills": ["data-visualization", "time-series", "nlp-ds", "business-analytics"],
                "learning_module_ids": ["tableau-mastery", "power-bi", "ab-testing-deep-dive"],
                "milestone": "Build predictive models and present insights",
            },
            "job-ready": {
                "name": "Job Ready",
                "weeks": 4,
                "description": "Mock interviews, case studies, system design",
                "skills": ["mock-interviews", "case-studies"],
                "learning_module_ids": ["case-study-frameworks", "behavioral-stars", "mock-analyst-interview"],
                "milestone": "Clear 3+ DS mock interview loops with case studies",
            },
        },
        "skill_tree": {
            "statistics": {
                "name": "Statistics & Probability",
                "target": 35,
                "weight": 1.1,
                "prerequisites": [],
                "est_hours": 12,
                "phase": "foundation",
                "difficulty_distribution": {"easy": 10, "medium": 18, "hard": 7},
                "sub_topics": ["descriptive-statistics", "probability-distributions", "bayes-theorem", "central-limit-theorem", "hypothesis-testing", "p-values", "confidence-intervals", "anova", "chi-square", "non-parametric-tests", "correlation-regression", "sampling-distributions"],
                "patterns": ["statistics"],
                "learning_module_ids": ["stats-intro", "probability-fundamentals"],
                "company_sources": {
                    "google": ["bayes-theorem", "hypothesis-testing"],
                    "amazon": ["confidence-intervals", "anova"],
                    "meta": ["chi-square", "non-parametric-tests"],
                },
            },
            "experimental-design": {
                "name": "Experimental Design & A/B Testing",
                "target": 25,
                "weight": 1.0,
                "prerequisites": ["statistics"],
                "est_hours": 8,
                "sub_topics": ["randomization", "blocking", "factorial-design", "power-analysis", "sample-size", "conversion-rate", "novelty-effect", "sequential-testing", "multi-armed-bandit", "experiment-platform"],
                "patterns": ["experimental-design", "ab-testing"],
                "company_sources": {
                    "google": ["experiment-platform", "multi-armed-bandit"],
                    "amazon": ["conversion-rate", "power-analysis"],
                    "netflix": ["sequential-testing", "sample-size"],
                },
            },
            "statistical-inference": {
                "name": "Statistical Inference",
                "target": 20,
                "weight": 0.9,
                "prerequisites": ["statistics"],
                "est_hours": 6,
                "sub_topics": ["point-estimation", "maximum-likelihood", "bayesian-inference", "credible-intervals", "bootstrap", "permutation-tests", "multiple-testing", "fdr", "family-wise-error"],
                "patterns": ["statistical-inference", "statistics"],
                "company_sources": {
                    "google": ["bayesian-inference", "bootstrap"],
                    "amazon": ["maximum-likelihood", "multiple-testing"],
                },
            },
            "ml-for-ds": {
                "name": "ML for Data Science",
                "target": 25,
                "weight": 0.9,
                "prerequisites": ["statistics", "python-ds"],
                "est_hours": 8,
                "sub_topics": ["linear-regression", "logistic-regression", "decision-trees", "random-forest", "clustering", "pca", "model-selection", "cross-validation", "feature-importance", "explainability"],
                "patterns": ["ml-for-ds", "statistics"],
                "company_sources": {
                    "amazon": ["random-forest", "feature-importance"],
                    "meta": ["clustering", "explainability"],
                    "netflix": ["cross-validation", "model-selection"],
                },
            },
            "python-ds": {
                "name": "Python (Pandas, Scipy, Statsmodels)",
                "target": 20,
                "weight": 0.8,
                "prerequisites": ["statistics"],
                "est_hours": 6,
                "sub_topics": ["pandas-advanced", "scipy-stats", "statsmodels", "seaborn", "plotly", "time-series-decomposition", "survival-analysis", "causal-inference", "bayesian-modeling"],
                "patterns": ["python-ds", "pandas", "statsmodels"],
                "company_sources": {
                    "amazon": ["pandas-advanced", "statsmodels"],
                    "airbnb": ["seaborn", "plotly"],
                },
            },
            "r-ds": {
                "name": "R for Statistics",
                "target": 10,
                "weight": 0.6,
                "prerequisites": ["statistics"],
                "est_hours": 4,
                "sub_topics": ["r-basics", "dplyr", "ggplot2", "r-statsmodels", "r-markdown", "shiny", "tidyverse"],
                "patterns": ["r-ds", "r-language"],
                "company_sources": {},
            },
            "data-visualization": {
                "name": "Data Visualization & Storytelling",
                "target": 20,
                "weight": 0.8,
                "prerequisites": ["python-ds", "statistics"],
                "est_hours": 6,
                "sub_topics": ["exploratory-plots", "dashboard-design", "color-theory", "narrative-structure", "interactive-viz", "executive-summaries", "data-storytelling", "executive-presentation"],
                "patterns": ["data-viz", "storytelling"],
                "company_sources": {
                    "google": ["dashboard-design", "interactive-viz"],
                    "netflix": ["data-storytelling", "executive-presentation"],
                },
            },
            "nlp-ds": {
                "name": "NLP for Data Science",
                "target": 10,
                "weight": 0.6,
                "prerequisites": ["python-ds", "ml-for-ds"],
                "est_hours": 4,
                "sub_topics": ["text-preprocessing", "tf-idf", "topic-modeling", "lda", "sentiment-analysis", "named-entity-recognition", "word-embeddings", "text-classification"],
                "patterns": ["nlp-ds", "nlp"],
                "company_sources": {
                    "airbnb": ["topic-modeling", "sentiment-analysis"],
                    "meta": ["named-entity-recognition", "text-classification"],
                },
            },
            "time-series": {
                "name": "Time Series Analysis",
                "target": 15,
                "weight": 0.7,
                "prerequisites": ["statistics", "python-ds"],
                "est_hours": 6,
                "sub_topics": ["stationarity", "arima", "sarima", "prophet", "seasonal-decomposition", "exponential-smoothing", "forecasting", "anomaly-detection", "multivariate-ts"],
                "patterns": ["time-series", "statistics"],
                "company_sources": {
                    "amazon": ["prophet", "forecasting"],
                    "uber": ["arima", "anomaly-detection"],
                    "netflix": ["seasonal-decomposition", "exponential-smoothing"],
                },
            },
            "business-analytics": {
                "name": "Business Analytics & Case Studies",
                "target": 10,
                "weight": 0.6,
                "prerequisites": ["experimental-design", "data-visualization", "ml-for-ds"],
                "est_hours": 4,
                "sub_topics": ["kpi-definition", "cohort-analysis", "retention-analysis", "lifetime-value", "churn-prediction", "revenue-attribution", "product-health", "executive-reporting"],
                "patterns": ["business-analytics", "case-study"],
                "company_sources": {
                    "airbnb": ["cohort-analysis", "lifetime-value"],
                    "netflix": ["churn-prediction", "revenue-attribution"],
                },
            },
        },
        "mock_test": {
            "name": "Data Scientist Case Study Mock",
            "total_questions": 7,
            "time_limit_minutes": 180,
            "sections": [
                {"name": "Statistics (10 Qs)", "type": "mcq", "count": 1, "time_minutes": 25},
                {"name": "A/B Test Design", "type": "case_study", "count": 1, "time_minutes": 35},
                {"name": "Python Analysis", "type": "coding", "count": 1, "time_minutes": 40},
                {"name": "ML Modeling", "type": "coding", "count": 1, "time_minutes": 40},
                {"name": "Statistical Inference Qs (3)", "type": "mcq", "count": 1, "time_minutes": 15},
                {"name": "Storytelling & Viz", "type": "mcq", "count": 1, "time_minutes": 15},
                {"name": "Case Study Discussion", "type": "scenario", "count": 1, "time_minutes": 10},
            ],
        },
    },

    # =========================================================
    # 7. Technical Assistant
    # =========================================================
    "technical-assistant": {
        "role_id": "technical-assistant",
        "display_name": "Technical Assistant",
        "icon": "🔧",
        "description": "Basic coding, aptitude, troubleshooting, and technical support skills.",
        "target_companies": ["TCS", "Infosys", "Wipro", "HCL", "Cognizant", "Tech Mahindra"],
        "estimated_weeks": 8,
        "total_questions_target": 200,
        "progression_phases": {
            "foundation": {
                "name": "Foundation (Beginner)",
                "weeks": 1,
                "description": "Aptitude basics, verbal ability, computer fundamentals",
                "skills": ["aptitude", "verbal-ability", "computer-fundamentals", "ms-office"],
                "learning_module_ids": ["aptitude-quant", "aptitude-logical"],
                "milestone": "Score 80%+ on basic aptitude tests",
            },
            "core": {
                "name": "Core (Intermediate)",
                "weeks": 2,
                "description": "Logical reasoning, basic coding, communication",
                "skills": ["logical-reasoning", "basic-coding", "communication"],
                "learning_module_ids": ["programming-basics"],
                "milestone": "Write 20+ basic programs and solve logical puzzles",
            },
            "advanced": {
                "name": "Advanced",
                "weeks": 3,
                "description": "Problem solving, technical troubleshooting, HR prep",
                "skills": ["problem-solving", "technical-support"],
                "learning_module_ids": ["behavioral-stars"],
                "milestone": "Complete 5+ mock tests with 75%+ score",
            },
            "job-ready": {
                "name": "Job Ready",
                "weeks": 4,
                "description": "Mock interviews, HR rounds, company prep",
                "skills": ["hr-round", "mock-interviews"],
                "learning_module_ids": ["behavioral-stars"],
                "milestone": "Clear 5+ HR mock interview rounds",
            },
        },
        "skill_tree": {
            "aptitude": {
                "name": "Quantitative Aptitude",
                "target": 20,
                "weight": 1.0,
                "prerequisites": [],
                "est_hours": 8,
                "sub_topics": ["percentages", "profit-loss", "ratio-proportion", "averages", "time-work", "time-distance", "simple-compound-interest", "number-system", "simplification", "approximation"],
                "patterns": ["aptitude"],
                "company_sources": {
                    "tcs": ["percentages", "ratio-proportion", "averages"],
                    "infosys": ["time-work", "time-distance"],
                    "wipro": ["number-system", "simplification"],
                },
            },
            "logical-reasoning": {
                "name": "Logical Reasoning",
                "target": 20,
                "weight": 1.0,
                "prerequisites": [],
                "est_hours": 8,
                "sub_topics": ["series", "coding-decoding", "blood-relations", "direction-sense", "syllogism", "puzzle", "seating-arrangement", "input-output", "data-sufficiency", "statement-conclusion"],
                "patterns": ["logical-reasoning"],
                "company_sources": {
                    "tcs": ["series", "coding-decoding", "blood-relations"],
                    "infosys": ["syllogism", "puzzle", "seating-arrangement"],
                },
            },
            "verbal-ability": {
                "name": "Verbal Ability",
                "target": 15,
                "weight": 0.9,
                "prerequisites": [],
                "est_hours": 5,
                "sub_topics": ["synonyms-antonyms", "reading-comprehension", "sentence-correction", "para-jumbles", "fill-in-blanks", "idioms-phrases", "spotting-errors", "vocabulary"],
                "patterns": ["verbal-ability"],
                "company_sources": {
                    "tcs": ["reading-comprehension", "sentence-correction"],
                    "infosys": ["synonyms-antonyms", "para-jumbles"],
                },
            },
            "basic-coding": {
                "name": "Basic Programming (Python/C/Algo)",
                "target": 15,
                "weight": 0.8,
                "prerequisites": [],
                "est_hours": 6,
                "sub_topics": ["variables-datatypes", "control-flow", "loops", "functions", "arrays", "strings", "basic-algorithms", "recursion-basics", "debugging", "io-operations"],
                "patterns": ["basic-coding", "arrays-hashing"],
                "company_sources": {
                    "tcs": ["variables-datatypes", "control-flow", "arrays"],
                    "hcl": ["functions", "loops"],
                },
            },
            "technical-support": {
                "name": "Technical Troubleshooting",
                "target": 15,
                "weight": 0.7,
                "prerequisites": ["computer-fundamentals"],
                "est_hours": 6,
                "sub_topics": ["hardware-basics", "os-troubleshooting", "network-basics", "software-installation", "driver-issues", "backup-recovery", "ticket-management", "remote-support", "documentation"],
                "patterns": ["technical-support"],
                "company_sources": {
                    "tcs": ["hardware-basics", "os-troubleshooting"],
                    "wipro": ["network-basics", "ticket-management"],
                },
            },
            "computer-fundamentals": {
                "name": "Computer Fundamentals (OS, DBMS, CN)",
                "target": 15,
                "weight": 0.8,
                "prerequisites": [],
                "est_hours": 5,
                "sub_topics": ["os-concepts", "process-management", "memory-management", "file-systems", "dbms-basics", "sql-basics", "networking-basics", "ip-addressing", "dns-dhcp"],
                "patterns": ["computer-fundamentals"],
                "company_sources": {
                    "tcs": ["os-concepts", "dbms-basics"],
                    "infosys": ["networking-basics", "sql-basics"],
                },
            },
            "ms-office": {
                "name": "MS Office (Excel, Word, PowerPoint)",
                "target": 10,
                "weight": 0.6,
                "prerequisites": [],
                "est_hours": 3,
                "sub_topics": ["excel-formulas", "pivot-tables", "charts", "vlookup", "word-formatting", "powerpoint-design", "shortcuts"],
                "patterns": ["ms-office", "excel"],
                "company_sources": {
                    "tcs": ["excel-formulas", "pivot-tables"],
                    "hcl": ["word-formatting", "powerpoint-design"],
                },
            },
            "communication": {
                "name": "Technical Communication",
                "target": 10,
                "weight": 0.7,
                "prerequisites": [],
                "est_hours": 3,
                "sub_topics": ["email-etiquette", "technical-writing", "presentation-skills", "active-listening", "meeting-management", "conflict-resolution"],
                "patterns": ["communication"],
                "company_sources": {},
            },
            "problem-solving": {
                "name": "Problem-Solving Ability",
                "target": 10,
                "weight": 0.8,
                "prerequisites": ["aptitude", "logical-reasoning"],
                "est_hours": 3,
                "sub_topics": ["structured-thinking", "root-cause-analysis", "decision-making", "prioritization", "creative-solutions"],
                "patterns": ["problem-solving"],
                "company_sources": {},
            },
            "hr-round": {
                "name": "HR Round & Soft Skills",
                "target": 10,
                "weight": 0.6,
                "prerequisites": [],
                "est_hours": 2,
                "sub_topics": ["self-introduction", "strengths-weaknesses", "career-goals", "situational-questions", "company-research", "salary-negotiation-basics"],
                "patterns": ["hr-round", "behavioral"],
                "company_sources": {},
            },
        },
        "mock_test": {
            "name": "Technical Assistant Mock Test",
            "total_questions": 20,
            "time_limit_minutes": 90,
            "sections": [
                {"name": "Quantitative Aptitude (10 Qs)", "type": "aptitude", "count": 1, "time_minutes": 20},
                {"name": "Logical Reasoning (8 Qs)", "type": "aptitude", "count": 1, "time_minutes": 15},
                {"name": "Verbal Ability (7 Qs)", "type": "aptitude", "count": 1, "time_minutes": 12},
                {"name": "Coding (1 problem)", "type": "coding", "count": 1, "time_minutes": 20},
                {"name": "Technical Qs (5)", "type": "mcq", "count": 1, "time_minutes": 10},
                {"name": "HR Round", "type": "behavioral", "count": 1, "time_minutes": 13},
            ],
        },
    },

    # =========================================================
    # 8. DevOps Engineer
    # =========================================================
    "devops-engineer": {
        "role_id": "devops-engineer",
        "display_name": "DevOps Engineer",
        "icon": "🚀",
        "description": "CI/CD, containerization, cloud platforms, automation, and SRE practices.",
        "target_companies": ["Amazon", "Google", "Microsoft", "Infosys", "TCS", "Netflix", "Uber"],
        "estimated_weeks": 16,
        "total_questions_target": 350,
        "progression_phases": {
            "foundation": {
                "name": "Foundation (Beginner)",
                "weeks": 1,
                "description": "Linux basics, shell scripting, networking fundamentals",
                "skills": ["linux", "networks", "git"],
                "learning_module_ids": ["networking-basics", "os-fundamentals"],
                "milestone": "Set up Linux VM and write 20+ shell scripts",
            },
            "core": {
                "name": "Core (Intermediate)",
                "weeks": 2,
                "description": "Docker, CI/CD, cloud platforms (AWS/Azure/GCP)",
                "skills": ["docker", "ci-cd", "cloud-aws", "cloud-azure", "cloud-gcp"],
                "learning_module_ids": ["system-design-intro"],
                "milestone": "Build and deploy a full CI/CD pipeline",
            },
            "advanced": {
                "name": "Advanced",
                "weeks": 3,
                "description": "Kubernetes, Terraform, monitoring, IaC",
                "skills": ["kubernetes", "infrastructure-as-code", "monitoring", "sre-practices"],
                "learning_module_ids": ["system-design-deep-dive"],
                "milestone": "Deploy a production-grade K8s cluster with monitoring",
            },
            "job-ready": {
                "name": "Job Ready",
                "weeks": 4,
                "description": "Mock interviews, system design, behavioral",
                "skills": ["mock-interviews", "system-design"],
                "learning_module_ids": ["behavioral-stars", "system-design-deep-dive"],
                "milestone": "Clear 3+ DevOps mock interview loops",
            },
        },
        "skill_tree": {
            "linux": {
                "name": "Linux & Shell Scripting",
                "target": 25,
                "weight": 0.9,
                "prerequisites": [],
                "est_hours": 8,
                "sub_topics": ["file-system", "permissions", "process-management", "bash-scripting", "grep-awk-sed", "systemd", "cron", "package-management", "ssh", "performance-tuning"],
                "patterns": ["linux", "shell"],
                "company_sources": {
                    "amazon": ["bash-scripting", "systemd"],
                    "google": ["performance-tuning", "grep-awk-sed"],
                },
            },
            "docker": {
                "name": "Docker & Containerization",
                "target": 20,
                "weight": 1.0,
                "prerequisites": ["linux"],
                "est_hours": 7,
                "sub_topics": ["dockerfile", "images", "containers", "volumes", "networks", "docker-compose", "multi-stage-builds", "security", "registry", "buildkit"],
                "patterns": ["docker", "containerization"],
                "company_sources": {
                    "amazon": ["dockerfile", "multi-stage-builds"],
                    "google": ["security", "docker-compose"],
                },
            },
            "kubernetes": {
                "name": "Kubernetes & Orchestration",
                "target": 20,
                "weight": 1.0,
                "prerequisites": ["docker", "linux"],
                "est_hours": 10,
                "sub_topics": ["pods", "deployments", "services", "ingress", "configmap-secret", "helm", "operators", "crd", "cluster-autoscaler", "rbac"],
                "patterns": ["kubernetes", "orchestration"],
                "company_sources": {
                    "google": ["helm", "operators"],
                    "amazon": ["ingress", "rbac"],
                },
            },
            "ci-cd": {
                "name": "CI/CD (Jenkins, GitLab CI, GitHub Actions)",
                "target": 20,
                "weight": 0.9,
                "prerequisites": ["docker", "linux"],
                "est_hours": 8,
                "sub_topics": ["jenkins-pipelines", "gitlab-ci", "github-actions", "build-test-deploy", "artifact-management", "deployment-strategies", "rollback", "security-scanning", "notification", "variables-secrets"],
                "patterns": ["ci-cd", "jenkins", "github-actions"],
                "company_sources": {
                    "amazon": ["jenkins-pipelines", "deployment-strategies"],
                    "google": ["github-actions", "security-scanning"],
                },
            },
            "cloud-aws": {
                "name": "AWS (EC2, S3, ECS, EKS, Lambda)",
                "target": 25,
                "weight": 1.0,
                "prerequisites": ["linux", "networking-basics"],
                "est_hours": 12,
                "sub_topics": ["ec2", "s3", "vpc", "iam", "rds", "ecs", "eks", "lambda", "cloudformation", "cloudwatch", "route53", "elb"],
                "patterns": ["cloud-aws", "aws"],
                "company_sources": {
                    "amazon": ["ec2", "s3", "lambda", "ecs", "eks", "cloudformation"],
                },
            },
            "cloud-azure": {
                "name": "Azure (AKS, App Service)",
                "target": 10,
                "weight": 0.6,
                "prerequisites": ["cloud-aws"],
                "est_hours": 5,
                "sub_topics": ["aks", "app-service", "azure-devops", "resource-groups", "arm-templates", "key-vault", "monitor", "functions"],
                "patterns": ["cloud-azure", "azure"],
                "company_sources": {
                    "microsoft": ["aks", "azure-devops"],
                },
            },
            "cloud-gcp": {
                "name": "GCP (GKE, Cloud Run)",
                "target": 10,
                "weight": 0.5,
                "prerequisites": ["cloud-aws"],
                "est_hours": 4,
                "sub_topics": ["gke", "cloud-run", "cloud-build", "cloud-sql", "pub-sub", "cloud-storage", "iam", "monitoring"],
                "patterns": ["cloud-gcp", "gcp"],
                "company_sources": {
                    "google": ["gke", "cloud-run"],
                },
            },
            "monitoring": {
                "name": "Monitoring (Prometheus, Grafana, ELK)",
                "target": 15,
                "weight": 0.8,
                "prerequisites": ["kubernetes", "linux"],
                "est_hours": 6,
                "sub_topics": ["prometheus", "grafana", "alertmanager", "elk-stack", "log-aggregation", "distributed-tracing", "sli-slo", "alerting-rules", "dashboarding"],
                "patterns": ["monitoring", "prometheus", "grafana"],
                "company_sources": {
                    "google": ["prometheus", "sli-slo"],
                    "amazon": ["elk-stack", "cloudwatch"],
                },
            },
            "infrastructure-as-code": {
                "name": "Terraform & Ansible",
                "target": 15,
                "weight": 0.8,
                "prerequisites": ["cloud-aws", "linux"],
                "est_hours": 6,
                "sub_topics": ["terraform-state", "modules", "providers", "workspaces", "ansible-playbooks", "roles", "inventory", "vault", "testing", "ci-cd-integration"],
                "patterns": ["infrastructure-as-code", "terraform", "ansible"],
                "company_sources": {
                    "amazon": ["terraform-state", "modules"],
                    "google": ["ansible-playbooks", "ci-cd-integration"],
                },
            },
            "sre-practices": {
                "name": "SRE Practices & SLIs/SLOs",
                "target": 10,
                "weight": 0.7,
                "prerequisites": ["monitoring", "kubernetes"],
                "est_hours": 4,
                "sub_topics": ["sli-slo-sla", "error-budget", "toil-reduction", "incident-response", "postmortem", "capacity-planning", "chaos-engineering", "reliability-patterns"],
                "patterns": ["sre-practices", "monitoring"],
                "company_sources": {
                    "google": ["sli-slo-sla", "error-budget", "chaos-engineering"],
                    "amazon": ["incident-response", "postmortem"],
                },
            },
        },
        "mock_test": {
            "name": "DevOps Engineer Mock Interview",
            "total_questions": 6,
            "time_limit_minutes": 120,
            "sections": [
                {"name": "Linux/Shell (5 Qs)", "type": "mcq", "count": 1, "time_minutes": 20},
                {"name": "Docker Scenario", "type": "scenario", "count": 1, "time_minutes": 20},
                {"name": "K8s Design", "type": "design", "count": 1, "time_minutes": 30},
                {"name": "CI/CD Pipeline Config", "type": "coding", "count": 1, "time_minutes": 25},
                {"name": "AWS Scenario Qs (3)", "type": "mcq", "count": 1, "time_minutes": 15},
                {"name": "Monitoring Strategy", "type": "scenario", "count": 1, "time_minutes": 10},
            ],
        },
    },

    # =========================================================
    # 9. QA Engineer
    # =========================================================
    "qa-engineer": {
        "role_id": "qa-engineer",
        "display_name": "QA Automation Engineer",
        "icon": "🧪",
        "description": "Test automation, API testing, Selenium, performance testing, and QA frameworks.",
        "target_companies": ["Amazon", "Microsoft", "TCS", "Infosys", "Wipro", "Cognizant", "HCL"],
        "estimated_weeks": 12,
        "total_questions_target": 280,
        "progression_phases": {
            "foundation": {
                "name": "Foundation (Beginner)",
                "weeks": 1,
                "description": "Manual testing, test case design, bug life cycle",
                "skills": ["manual-testing", "testing-concepts", "bug-life-cycle", "sql-for-qa"],
                "learning_module_ids": ["dbms-fundamentals"],
                "milestone": "Write 50+ test cases and identify bugs",
            },
            "core": {
                "name": "Core (Intermediate)",
                "weeks": 2,
                "description": "Selenium, API testing, unit testing",
                "skills": ["selenium", "api-testing", "unit-testing", "test-automation"],
                "learning_module_ids": ["oop-design-patterns"],
                "milestone": "Automate 10+ test scenarios with Selenium",
            },
            "advanced": {
                "name": "Advanced",
                "weeks": 3,
                "description": "Performance testing, CI/CD testing pipelines",
                "skills": ["performance-testing", "ci-testing"],
                "learning_module_ids": ["networking-basics"],
                "milestone": "Build a complete automated testing pipeline",
            },
            "job-ready": {
                "name": "Job Ready",
                "weeks": 4,
                "description": "Mock interviews, company-specific prep",
                "skills": ["mock-interviews"],
                "learning_module_ids": ["behavioral-stars"],
                "milestone": "Clear 3+ QA mock interview loops",
            },
        },
        "skill_tree": {
            "manual-testing": {
                "name": "Manual Testing & Test Cases",
                "target": 15,
                "weight": 0.8,
                "prerequisites": [],
                "est_hours": 5,
                "sub_topics": ["test-case-design", "boundary-value-analysis", "equivalence-partitioning", "decision-table", "state-transition", "exploratory-testing", "smoke-testing", "sanity-testing", "regression-testing", "test-plan"],
                "patterns": ["manual-testing", "testing-concepts"],
                "company_sources": {
                    "tcs": ["test-case-design", "boundary-value-analysis"],
                    "infosys": ["equivalence-partitioning", "smoke-testing"],
                },
            },
            "test-automation": {
                "name": "Test Automation Frameworks",
                "target": 20,
                "weight": 0.9,
                "prerequisites": ["manual-testing", "basic-coding"],
                "est_hours": 8,
                "sub_topics": ["framework-design", "page-object-model", "data-driven", "keyword-driven", "hybrid-framework", "testng", "junit", "pytest", "reporting", "parallel-execution"],
                "patterns": ["test-automation", "selenium"],
                "company_sources": {
                    "amazon": ["framework-design", "page-object-model"],
                    "microsoft": ["testng", "reporting"],
                },
            },
            "selenium": {
                "name": "Selenium WebDriver (Java/Python)",
                "target": 20,
                "weight": 1.0,
                "prerequisites": ["test-automation"],
                "est_hours": 8,
                "sub_topics": ["locators", "webdriver-commands", "waits", "actions", "alerts", "frames-windows", "screenshots", "javascript-executor", "grid", "mobile-testing"],
                "patterns": ["selenium", "test-automation"],
                "company_sources": {
                    "amazon": ["locators", "waits", "grid"],
                    "tcs": ["webdriver-commands", "screenshots"],
                },
            },
            "api-testing": {
                "name": "API Testing (Postman, REST Assured)",
                "target": 15,
                "weight": 0.9,
                "prerequisites": ["test-automation", "manual-testing"],
                "est_hours": 6,
                "sub_topics": ["rest-assured", "postman", "request-response", "authentication", "data-driven-api", "schema-validation", "contract-testing", "mocking", "test-containers", "performance-api"],
                "patterns": ["api-testing", "rest-assured"],
                "company_sources": {
                    "amazon": ["rest-assured", "contract-testing"],
                    "microsoft": ["postman", "schema-validation"],
                },
            },
            "performance-testing": {
                "name": "Performance Testing (JMeter, LoadRunner)",
                "target": 15,
                "weight": 0.8,
                "prerequisites": ["test-automation"],
                "est_hours": 6,
                "sub_topics": ["jmeter-basics", "thread-groups", "controllers", "listeners", "assertions", "parameterization", "correlation", "load-testing", "stress-testing", "spike-testing", "analysis"],
                "patterns": ["performance-testing", "jmeter"],
                "company_sources": {
                    "amazon": ["jmeter-basics", "correlation"],
                    "infosys": ["load-testing", "analysis"],
                },
            },
            "unit-testing": {
                "name": "Unit Testing (JUnit, PyTest)",
                "target": 10,
                "weight": 0.7,
                "prerequisites": ["basic-coding"],
                "est_hours": 4,
                "sub_topics": ["junit5", "pytest", "mockito", "mockk", "test-coverage", "parameterized-tests", "assertions", "fixtures", "test-doubles", "mutation-testing"],
                "patterns": ["unit-testing", "testing"],
                "company_sources": {
                    "amazon": ["junit5", "mockito"],
                    "microsoft": ["pytest", "test-coverage"],
                },
            },
            "ci-testing": {
                "name": "CI Testing Pipelines",
                "target": 10,
                "weight": 0.7,
                "prerequisites": ["test-automation", "api-testing"],
                "est_hours": 4,
                "sub_topics": ["jenkins", "github-actions", "gitlab-ci", "test-stages", "artifact-publishing", "quality-gates", "flaky-test-detection", "test-reports", "environment-management", "parallelization"],
                "patterns": ["ci-testing", "ci-cd"],
                "company_sources": {
                    "amazon": ["jenkins", "quality-gates"],
                    "microsoft": ["github-actions", "parallelization"],
                },
            },
            "testing-concepts": {
                "name": "Testing Concepts & Terminology",
                "target": 15,
                "weight": 0.8,
                "prerequisites": [],
                "est_hours": 5,
                "sub_topics": ["v-model", "stlc", "black-box-white-box", "functional-non-functional", "risk-based-testing", "test-pyramid", "shift-left", "test-environments", "test-data-management", "defect-severity-priority"],
                "patterns": ["testing-concepts", "manual-testing"],
                "company_sources": {
                    "tcs": ["v-model", "stlc"],
                    "wipro": ["test-pyramid", "shift-left"],
                },
            },
            "bug-life-cycle": {
                "name": "Bug Life Cycle & Reporting",
                "target": 10,
                "weight": 0.6,
                "prerequisites": ["manual-testing"],
                "est_hours": 3,
                "sub_topics": ["bug-states", "bug-fields", "repro-steps", "bug-triage", "root-cause", "regression-verification", "reopening", "metrics", "jira", "communication"],
                "patterns": ["bug-life-cycle", "testing-concepts"],
                "company_sources": {
                    "tcs": ["bug-states", "jira"],
                    "infosys": ["bug-triage", "regression-verification"],
                },
            },
            "sql-for-qa": {
                "name": "SQL for Testing",
                "target": 10,
                "weight": 0.6,
                "prerequisites": [],
                "est_hours": 3,
                "sub_topics": ["select-where", "joins", "group-by", "subqueries", "data-validation", "data-comparison", "test-data-generation", "schema-validation", "stored-procedures", "triggers"],
                "patterns": ["sql", "testing"],
                "company_sources": {
                    "tcs": ["select-where", "joins"],
                    "infosys": ["data-validation", "subqueries"],
                },
            },
        },
        "mock_test": {
            "name": "QA Engineer Mock Interview",
            "total_questions": 7,
            "time_limit_minutes": 120,
            "sections": [
                {"name": "Testing Concepts (10 Qs)", "type": "mcq", "count": 1, "time_minutes": 15},
                {"name": "Selenium Coding", "type": "coding", "count": 1, "time_minutes": 30},
                {"name": "API Testing Scenario", "type": "scenario", "count": 1, "time_minutes": 25},
                {"name": "Test Case Design (3)", "type": "mcq", "count": 1, "time_minutes": 15},
                {"name": "Performance Testing Qs (3)", "type": "mcq", "count": 1, "time_minutes": 15},
                {"name": "CI/CD Testing Pipeline", "type": "design", "count": 1, "time_minutes": 20},
            ],
        },
    },

    # =========================================================
    # 10. Product Analyst
    # =========================================================
    "product-analyst": {
        "role_id": "product-analyst",
        "display_name": "Product Analyst",
        "icon": "📈",
        "description": "Product metrics, A/B testing, SQL, and data-driven product decisions.",
        "target_companies": ["Google", "Meta", "Amazon", "Microsoft", "Swiggy", "Zomato", "Razorpay", "Flipkart"],
        "estimated_weeks": 12,
        "total_questions_target": 300,
        "progression_phases": {
            "foundation": {
                "name": "Foundation (Beginner)",
                "weeks": 1,
                "description": "SQL basics, statistics, Excel",
                "skills": ["sql-pa", "statistics-pa", "business-strategy"],
                "learning_module_ids": ["sql-fundamentals", "stats-intro", "excel-advanced"],
                "milestone": "Write 30+ SQL queries and basic metrics analysis",
            },
            "core": {
                "name": "Core (Intermediate)",
                "weeks": 2,
                "description": "Advanced SQL, A/B testing, funnel analysis",
                "skills": ["ab-testing", "funnel-analysis", "data-viz-pa"],
                "learning_module_ids": ["sql-advanced", "sql-window-functions", "ab-testing-deep-dive"],
                "milestone": "Design and analyze 5+ A/B tests",
            },
            "advanced": {
                "name": "Advanced",
                "weeks": 3,
                "description": "Product sense, growth analytics, case studies",
                "skills": ["product-case", "product-metrics", "growth-analytics", "python-pa"],
                "learning_module_ids": ["product-metrics", "case-study-frameworks", "tableau-mastery"],
                "milestone": "Build a product analytics dashboard and case study",
            },
            "job-ready": {
                "name": "Job Ready",
                "weeks": 4,
                "description": "Mock interviews, product sense rounds",
                "skills": ["mock-interviews"],
                "learning_module_ids": ["behavioral-stars", "mock-analyst-interview"],
                "milestone": "Clear 3+ Product Analyst mock interview loops",
            },
        },
        "skill_tree": {
            "product-metrics": {
                "name": "Product Metrics & KPIs",
                "target": 20,
                "weight": 1.0,
                "prerequisites": [],
                "est_hours": 6,
                "sub_topics": ["north-star-metric", "leading-lagging-indicators", "dau-mau", "retention-rate", "conversion-rate", "arpu", "ltv", "cac", "payback-period", "health-score"],
                "patterns": ["product-metrics"],
                "company_sources": {
                    "google": ["north-star-metric", "leading-lagging-indicators"],
                    "meta": ["dau-mau", "retention-rate"],
                    "amazon": ["ltv", "cac"],
                },
            },
            "ab-testing": {
                "name": "A/B Testing & Experimentation",
                "target": 25,
                "weight": 1.1,
                "prerequisites": ["statistics-pa", "product-metrics"],
                "est_hours": 8,
                "sub_topics": ["hypothesis-formation", "randomization-unit", "minimum-detectable-effect", "sample-size-calculator", "sequential-testing", "multiple-variants", "guardrail-metrics", "novelty-effect", "ramp-up", "experiment-platform"],
                "patterns": ["ab-testing", "experimental-design"],
                "company_sources": {
                    "google": ["experiment-platform", "guardrail-metrics"],
                    "meta": ["randomization-unit", "sequential-testing"],
                    "amazon": ["minimum-detectable-effect", "ramp-up"],
                },
            },
            "sql-pa": {
                "name": "Advanced SQL for Analytics",
                "target": 30,
                "weight": 1.0,
                "prerequisites": [],
                "est_hours": 10,
                "sub_topics": ["window-functions", "cte-recursive", "time-series-sql", "cohort-sql", "retention-sql", "funnel-sql", "percentile", "lateral-join", "pivot", "performance-tuning"],
                "patterns": ["sql-pa", "sql"],
                "company_sources": {
                    "google": ["window-functions", "cohort-sql"],
                    "meta": ["retention-sql", "funnel-sql"],
                    "amazon": ["time-series-sql", "performance-tuning"],
                },
            },
            "funnel-analysis": {
                "name": "Funnel Analysis & Cohort Analysis",
                "target": 15,
                "weight": 0.9,
                "prerequisites": ["sql-pa", "product-metrics"],
                "est_hours": 5,
                "sub_topics": ["funnel-steps", "drop-off-analysis", "cohort-definition", "retention-curves", "time-to-convert", "multi-touch-attribution", "path-analysis", "segment-comparison", "funnel-visualization", "actionable-insights"],
                "patterns": ["funnel-analysis", "cohort-analysis"],
                "company_sources": {
                    "meta": ["cohort-definition", "retention-curves"],
                    "amazon": ["drop-off-analysis", "path-analysis"],
                },
            },
            "product-case": {
                "name": "Product Sense & Case Studies",
                "target": 15,
                "weight": 0.9,
                "prerequisites": ["product-metrics", "ab-testing", "funnel-analysis"],
                "est_hours": 5,
                "sub_topics": ["problem-identification", "goal-setting", "metric-selection", "solution-brainstorming", "prioritization-frameworks", "trade-off-analysis", "launch-plan", "success-criteria", "post-launch-analysis", "iteration"],
                "patterns": ["product-case", "case-study"],
                "company_sources": {
                    "google": ["problem-identification", "prioritization-frameworks"],
                    "meta": ["solution-brainstorming", "trade-off-analysis"],
                },
            },
            "statistics-pa": {
                "name": "Statistics for Product",
                "target": 20,
                "weight": 0.9,
                "prerequisites": [],
                "est_hours": 6,
                "sub_topics": ["confidence-intervals", "hypothesis-testing", "p-value", "statistical-power", "type-1-2-errors", "multiple-testing", "bayesian-vs-frequentist", "bootstrap", "effect-size", "practical-significance"],
                "patterns": ["statistics-pa", "statistics"],
                "company_sources": {
                    "google": ["bayesian-vs-frequentist", "bootstrap"],
                    "meta": ["statistical-power", "effect-size"],
                    "amazon": ["practical-significance", "multiple-testing"],
                },
            },
            "data-viz-pa": {
                "name": "Data Visualization (Looker, Tableau)",
                "target": 15,
                "weight": 0.7,
                "prerequisites": ["sql-pa", "product-metrics"],
                "est_hours": 5,
                "sub_topics": ["lookml", "explores", "dashboard-design", "drill-down", "scheduled-delivery", "tableau-calculations", "level-of-detail", "parameter-actions", "set-actions", "storytelling"],
                "patterns": ["data-viz-pa", "data-viz"],
                "company_sources": {
                    "google": ["lookml", "explores"],
                    "meta": ["dashboard-design", "storytelling"],
                },
            },
            "growth-analytics": {
                "name": "Growth Analytics & Retention",
                "target": 10,
                "weight": 0.7,
                "prerequisites": ["product-metrics", "funnel-analysis", "ab-testing"],
                "est_hours": 4,
                "sub_topics": ["acquisition-channels", "activation-rate", "retention-curves", "churn-analysis", "win-back", "viral-coefficient", "referral-programs", "engagement-loops", "habit-formation", "product-led-growth"],
                "patterns": ["growth-analytics", "retention"],
                "company_sources": {
                    "meta": ["retention-curves", "engagement-loops"],
                    "swiggy": ["acquisition-channels", "referral-programs"],
                },
            },
            "python-pa": {
                "name": "Python for Product Analytics",
                "target": 10,
                "weight": 0.6,
                "prerequisites": ["sql-pa", "statistics-pa"],
                "est_hours": 4,
                "sub_topics": ["pandas-analysis", "numpy", "scipy-stats", "plotly", "seaborn", "statistical-tests", "cohort-analysis-python", "survival-analysis", "ab-test-analysis", "automation"],
                "patterns": ["python-pa", "python", "pandas"],
                "company_sources": {
                    "amazon": ["pandas-analysis", "ab-test-analysis"],
                    "meta": ["plotly", "seaborn"],
                },
            },
            "business-strategy": {
                "name": "Business Strategy & Market Analysis",
                "target": 10,
                "weight": 0.6,
                "prerequisites": ["product-case", "growth-analytics"],
                "est_hours": 3,
                "sub_topics": ["market-sizing", "competitive-analysis", "pricing-strategy", "go-to-market", "product-positioning", "okrs", "roadmap-planning", "stakeholder-management", "influence-without-authority", "decision-frameworks"],
                "patterns": ["business-strategy", "product-case"],
                "company_sources": {
                    "google": ["okrs", "roadmap-planning"],
                    "meta": ["market-sizing", "pricing-strategy"],
                },
            },
        },
        "mock_test": {
            "name": "Product Analyst Mock Interview",
            "total_questions": 6,
            "time_limit_minutes": 90,
            "sections": [
                {"name": "SQL Problem (3 queries)", "type": "sql", "count": 1, "time_minutes": 30},
                {"name": "A/B Test Case Study", "type": "case_study", "count": 1, "time_minutes": 20},
                {"name": "Product Metrics Design", "type": "design", "count": 1, "time_minutes": 15},
                {"name": "Funnel/Cohort Qs (3)", "type": "mcq", "count": 1, "time_minutes": 10},
                {"name": "Stats Interpretation (2)", "type": "mcq", "count": 1, "time_minutes": 10},
                {"name": "Business Sense Q", "type": "scenario", "count": 1, "time_minutes": 5},
            ],
        },
    },
}

# Convenience: list all role IDs
ALL_ROLES = list(ROLE_CURRICULA.keys())

# Role display order
ROLE_DISPLAY_ORDER = ["sde", "data-analyst", "ai-engineer", "java-engineer", "ml-engineer", "data-scientist", "technical-assistant", "devops-engineer", "qa-engineer", "product-analyst"]


def get_role(role_id: str) -> Dict[str, Any] | None:
    return ROLE_CURRICULA.get(role_id.lower())


def get_all_roles() -> Dict[str, Dict[str, Any]]:
    return ROLE_CURRICULA


def get_role_ids() -> list:
    return ALL_ROLES


def get_role_display_order() -> list:
    return ROLE_DISPLAY_ORDER


def get_skill_tree(role_id: str) -> dict:
    role = get_role(role_id)
    if not role:
        return {}
    return role.get("skill_tree", {})


def get_total_target(role_id: str) -> int:
    skill_tree = get_skill_tree(role_id)
    return sum(s.get("target", 0) for s in skill_tree.values())


print(f"Role Curriculum definitions: {len(ROLE_CURRICULA)} roles")
for rid in ROLE_DISPLAY_ORDER:
    r = ROLE_CURRICULA.get(rid, {})
    target = get_total_target(rid)
    print(f"  {rid:20s}  target={target:3d}  skills={len(r.get('skill_tree', {}))}")