"""
SDE Placement Pack — structured curriculum and company blueprint.

This module defines:
  1. The SDE skill progression tree (320-question target distribution)
  2. Company assessment blueprints (Amazon, Microsoft, Google, TCS, etc.)
  3. The learning loop metadata for each pattern

The question bank is the fuel. This is the engine.
"""
from typing import Dict, List, Any

# =============================================================
# SDE SKILL PROGRESSION TREE
# =============================================================
SDE_SKILL_TREE: Dict[str, Dict[str, Any]] = {
    "programming-fundamentals": {
        "name": "Programming Fundamentals",
        "description": "Basic syntax, control flow, functions, and debugging",
        "question_target": 20,
        "topics": ["variables", "loops", "functions", "recursion"],
        "placement_stage": ["learning"],
    },
    "arrays-hashing": {
        "name": "Arrays & Hashing",
        "description": "Traversal, in-place modification, hash map lookups",
        "question_target": 30,
        "topics": ["two-sum", "group-anagrams", "contains-duplicate", "product-except-self"],
        "placement_stage": ["learning", "oa", "technical-interview"],
    },
    "strings": {
        "name": "Strings",
        "description": "String manipulation, parsing, and pattern matching",
        "question_target": 20,
        "topics": ["valid-palindrome", "reverse-words", "group-anagrams", "min-window-substring"],
        "placement_stage": ["learning", "oa", "technical-interview"],
    },
    "two-pointers-sliding-window": {
        "name": "Two Pointers & Sliding Window",
        "description": "Paired indices and window invariants for subarray problems",
        "question_target": 20,
        "topics": ["two-sum-ii", "sort-colors", "min-size-subarray-sum", "longest-repeating-char"],
        "placement_stage": ["learning", "oa", "technical-interview"],
    },
    "binary-search": {
        "name": "Binary Search",
        "description": "Boundary detection and search-space reduction",
        "question_target": 15,
        "topics": ["search-insert", "find-first-last", "search-rotated", "split-array"],
        "placement_stage": ["learning", "oa", "technical-interview"],
    },
    "linked-lists": {
        "name": "Linked Lists",
        "description": "Pointer manipulation and dummy-head techniques",
        "question_target": 15,
        "topics": ["reverse-linked-list", "add-two-numbers", "copy-list-random-pointer", "remove-nth-node"],
        "placement_stage": ["learning", "technical-interview"],
    },
    "stacks-queues": {
        "name": "Stacks & Queues",
        "description": "Monotonic stacks, balanced brackets, sliding window max",
        "question_target": 20,
        "topics": ["valid-parentheses", "min-stack", "daily-temperatures", "sliding-window-max"],
        "placement_stage": ["learning", "technical-interview"],
    },
    "trees": {
        "name": "Trees",
        "description": "DFS/BFS, recursive decomposition, tree validation",
        "question_target": 25,
        "topics": ["inorder-traversal", "validate-bst", "lca", "serialize-deserialize", "level-order"],
        "placement_stage": ["learning", "technical-interview"],
    },
    "graphs": {
        "name": "Graphs",
        "description": "DFS/BFS, shortest path, topological sort, union-find",
        "question_target": 25,
        "topics": ["clone-graph", "course-schedule", "dijkstra", "bfs-shortest-path", "topological-sort"],
        "placement_stage": ["learning", "technical-interview"],
    },
    "recursion-backtracking": {
        "name": "Recursion & Backtracking",
        "description": "State space exploration with DFS and constraint pruning",
        "question_target": 20,
        "topics": ["subsets", "permutations", "word-search", "n-queens", "sudoku-solver"],
        "placement_stage": ["learning", "technical-interview"],
    },
    "heap-greedy": {
        "name": "Heap & Greedy",
        "description": "Priority queue ordering and locally optimal choices",
        "question_target": 15,
        "topics": ["kth-largest", "merge-intervals", "non-overlapping-intervals", "task-scheduler"],
        "placement_stage": ["oa", "technical-interview"],
    },
    "dynamic-programming": {
        "name": "Dynamic Programming",
        "description": "State transition design and optimal substructure",
        "question_target": 25,
        "topics": ["climbing-stairs", "coin-change", "longest-increasing-subsequence", "edit-distance", "word-break"],
        "placement_stage": ["learning", "oa", "technical-interview"],
    },
    "sql": {
        "name": "SQL",
        "description": "Joins, aggregations, subqueries, window functions",
        "question_target": 20,
        "topics": ["joins", "group-by", "subqueries", "window-functions", "top-k"],
        "placement_stage": ["learning", "oa"],
    },
    "dbms": {
        "name": "DBMS",
        "description": "Indexing, normalization, transactions, ACID",
        "question_target": 15,
        "topics": ["indexing", "normalization", "transactions", "deadlocks"],
        "placement_stage": ["oa", "technical-interview"],
    },
    "os": {
        "name": "Operating Systems",
        "description": "Scheduling, memory management, concurrency, deadlocks",
        "question_target": 10,
        "topics": ["scheduling", "virtual-memory", "process-vs-thread", "semaphores"],
        "placement_stage": ["oa", "technical-interview"],
    },
    "networks": {
        "name": "Computer Networks",
        "description": "OSI layers, TCP/IP, HTTP, CDN, caching",
        "question_target": 10,
        "topics": ["tcp-handshake", "http-vs-https", "cdn", "load-balancer", "dns"],
        "placement_stage": ["oa", "technical-interview"],
    },
    "oop": {
        "name": "Object-Oriented Programming",
        "description": "Classes, inheritance, polymorphism, design patterns",
        "question_target": 10,
        "topics": ["encapsulation", "inheritance", "polymorphism", "design-patterns"],
        "placement_stage": ["technical-interview"],
    },
    "system-design": {
        "name": "System Design",
        "description": "Scalability, load balancing, caching, database design",
        "question_target": 10,
        "topics": ["url-shortener", "message-queue", "cache-strategy", "rate-limiting", "distributed-systems"],
        "placement_stage": ["technical-interview"],
    },
}

TOTAL_SDE_QUESTIONS_TARGET = sum(s["question_target"] for s in SDE_SKILL_TREE.values())
print(f"SDE Placement Pack target: {TOTAL_SDE_QUESTIONS_TARGET} questions across {len(SDE_SKILL_TREE)} skill areas")


# =============================================================
# COMPANY ASSESSMENT BLUEPRINTS
# =============================================================
COMPANY_BLUEPRINTS: Dict[str, Dict[str, Any]] = {
    "amazon": {
        "company_id": "amazon",
        "display_name": "Amazon",
        "icon": "🟠",
        "color": "#ff9900",
        "assessment_ready_score": 0,
        "focus_areas": [
            {"name": "Coding", "score": 0, "target": 80},
            {"name": "DSA", "score": 0, "target": 80},
            {"name": "CS Fundamentals", "score": 0, "target": 70},
            {"name": "System Design", "score": 0, "target": 60},
            {"name": "Behavioral", "score": 0, "target": 85},
            {"name": "Leadership Principles", "score": 0, "target": 80},
        ],
        "process": [
            {"name": "Understand the process", "description": "Online coding + Work Simulation + SDE I loop"},
            {"name": "Core coding patterns", "description": "Focus on arrays, strings, trees, graphs"},
            {"name": "Amazon-style OA", "description": "2 questions in 90 minutes — debugging + coding"},
            {"name": "Leadership Principles", "description": "STAR format aligned with 14 LPs"},
            {"name": "Technical interview", "description": "Code + design + behavioral loop"},
            {"name": "System design", "description": "Scalable system design for SDE II+ roles"},
            {"name": "Final simulation", "description": "Full Amazon mock loop with feedback"},
        ],
        "source_type": {
            "official_sample": "Amazon.jobs published interview prep material",
            "pattern_relevant": "Questions tagged with Amazon-relevant patterns",
            "candidate_reported": "Community-submitted interview experiences",
            "bountycourse_original": "Generated by BountyCode team",
        },
    },
    "microsoft": {
        "company_id": "microsoft",
        "display_name": "Microsoft",
        "icon": "🔵",
        "color": "#00a4ef",
        "assessment_ready_score": 0,
        "focus_areas": [
            {"name": "Coding", "score": 0, "target": 80},
            {"name": "DSA", "score": 0, "target": 80},
            {"name": "CS Fundamentals", "score": 0, "target": 70},
            {"name": "System Design", "score": 0, "target": 65},
            {"name": "Behavioral", "score": 0, "target": 80},
            {"name": "Problem Solving", "score": 0, "target": 85},
        ],
        "process": [
            {"name": "Understand the process", "description": "Phone screen + Onsite loop"},
            {"name": "Core coding patterns", "description": "Arrays, strings, trees, graphs, DP"},
            {"name": "Microsoft-style OA", "description": "2-3 problems, 60-90 minutes"},
            {"name": "Behavioral (STAR-R)", "description": "Situation, Task, Action, Result, Reflection"},
            {"name": "Technical interview", "description": "Live coding + design + behavioral"},
            {"name": "System design", "description": "Design scalable distributed systems"},
            {"name": "Final simulation", "description": "Full Microsoft mock loop"},
        ],
        "source_type": {
            "official_sample": "Microsoft Careers published interview guidance",
            "pattern_relevant": "Questions tagged with Microsoft-relevant patterns",
            "candidate_reported": "Community-submitted interview experiences",
            "bountycourse_original": "Generated by BountyCode team",
        },
    },
    "tcs": {
        "company_id": "tcs",
        "display_name": "TCS",
        "icon": "🔷",
        "color": "#ff0000",
        "assessment_ready_score": 0,
        "focus_areas": [
            {"name": "Aptitude", "score": 0, "target": 85},
            {"name": "Logical Reasoning", "score": 0, "target": 80},
            {"name": "Verbal Ability", "score": 0, "target": 75},
            {"name": "Coding", "score": 0, "target": 70},
            {"name": "Technical", "score": 0, "target": 75},
        ],
        "process": [
            {"name": "NQT Foundation (65Q/75min)", "description": "Numerical 20 + Verbal 25 + Reasoning 20. Gates Ninja. No negative marking; sections lock, no back-navigation — attempt every question."},
            {"name": "NQT Advanced (15Q + 2 coding/115min)", "description": "Advanced Aptitude 15Q/25min gates Digital; Advanced Coding 2 problems/90min with partial marks gates Prime."},
            {"name": "TCS CodeVita", "description": "Contest-style coding challenge"},
            {"name": "Technical interview", "description": "Project + CS fundamentals + coding"},
            {"name": "Final simulation", "description": "Full TCS NQT + Technical mock"},
        ],
        "source_type": {
            "official_sample": "TCS iON published exam pattern",
            "pattern_relevant": "Questions tagged with TCS-relevant patterns",
            "candidate_reported": "Community-submitted NQT experiences",
            "bountycourse_original": "Generated by BountyCode team",
        },
    },
    "google": {
        "company_id": "google",
        "display_name": "Google",
        "icon": "🔴",
        "color": "#4285f4",
        "assessment_ready_score": 0,
        "focus_areas": [
            {"name": "Coding", "score": 0, "target": 85},
            {"name": "DSA", "score": 0, "target": 85},
            {"name": "CS Fundamentals", "score": 0, "target": 80},
            {"name": "System Design", "score": 0, "target": 75},
            {"name": "Behavioral", "score": 0, "target": 70},
        ],
        "process": [
            {"name": "Understand the process", "description": "Googliness + technical loop"},
            {"name": "Core coding patterns", "description": "Arrays, strings, trees, graphs, DP, geometry"},
            {"name": "Google-style OA", "description": "Hard-medium problems, 90-120 minutes"},
            {"name": "System design", "description": "Large-scale distributed systems"},
            {"name": "Behavioral (Googliness)", "description": "Leadership and cultural fit"},
            {"name": "Final simulation", "description": "Full Google mock loop with feedback"},
        ],
        "source_type": {
            "official_sample": "Google published interview guide",
            "pattern_relevant": "Questions tagged with Google-relevant patterns",
            "candidate_reported": "Community-submitted interview experiences",
            "bountycourse_original": "Generated by BountyCode team",
        },
    },
}


def get_company_blueprint(company_id: str) -> Dict[str, Any] | None:
    return COMPANY_BLUEPRINTS.get(company_id.lower())


def get_all_company_ids() -> List[str]:
    return list(COMPANY_BLUEPRINTS.keys())


def get_sde_skill_tree() -> Dict[str, Dict[str, Any]]:
    return SDE_SKILL_TREE
