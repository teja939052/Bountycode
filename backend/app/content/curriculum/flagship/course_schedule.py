"""
Flagship Lesson — Course Schedule
 ==================================

 Gold-standard interactive lesson for topological sort / cycle detection.

 Full teaching loop with Captain Byte authored mentor moments.
 """
from typing import Dict, Any

SLUG = "course_schedule"

LESSON: Dict[str, Any] = {
    "lesson_id": "course_schedule_topological_sort",
    "module_id": "dsa:graphs:topological_sort",
    "title": "The Prerequisite Chain",
    "description": "Detect cycles in a directed graph and return a valid course ordering using Kahn's algorithm.",
    "difficulty": "intermediate",
    "est_minutes": 18,
    "xp_reward": 140,
    "skills_taught": ["topological_sort", "cycle_detection", "bfs", "graph"],
    "srs_concept_tag": "dsa:graphs:topological_sort",
    "captain_byte": {
        "intro": (
            "🧭 **Captain Byte**\n"
            "“The Prerequisite Chain is a directed graph. Every course is a node. "
            "Every prerequisite is a directed edge. A cycle means impossible ordering. "
            "Kahn’s algorithm removes zero-indegree nodes one by one. If nodes remain, there is a cycle.”"
        ),
        "correct": [
            "🧭 **Captain Byte**\n“Nice. You used indegree to find the next safe course.”",
            "🧭 **Captain Byte**\n“Clean. BFS over indegrees gives a valid topological order.”",
        ],
        "wrong": [
            "🧭 **Captain Byte**\n“Stop. Don’t DFS blindly. Count indegrees first.”",
            "🧭 **Captain Byte**\n“You’re missing a cycle. If nodes remain at the end, there is a cycle.”",
        ],
        "after_break": "🧭 **Captain Byte**\n“You found the broken assumption. Now track indegrees correctly.”",
        "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any dependency-ordering problem.”",
        "retry_prompt": "🧭 **Captain Byte**\n“Try again. Build indegree map, queue zero-indegree nodes, process edges.”",
    },
    "story_context": {
        "title": "The Prerequisite Chain",
        "narration": (
            "The Prerequisite Chain is a directed graph. Every course is a node. "
            "Every prerequisite is a directed edge."
        ),
        "setting": "prerequisite_chain",
        "character": "Captain Byte",
        "intro_text": (
            "Topological sort answers: can all courses be completed? "
            "If the graph has a cycle, the answer is no."
        ),
    },
    "discovery": {
        "title": "Map the Chain",
        "visual_primitives": ["trace", "move", "reveal"],
        "steps": [
            {
                "action": "indegree",
                "narration": "Indegree counts how many prerequisites a course has. Zero-indegree courses can start immediately.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "from collections import deque, defaultdict\nn = 4\ndeps = [[1, 0], [2, 0], [3, 1], [3, 2]]\nindegree = [0] * n\nadj = defaultdict(list)\nfor a, b in deps:\n    adj[b].append(a)\n    indegree[a] += 1\nprint('indegree:', indegree)\nprint('adj:', dict(adj))",
                    "expected_output": "indegree: [0, 1, 1, 2]",
                    "hint": "Course 0 has no prerequisites. Courses 1 and 2 each have 1. Course 3 has 2.",
                },
            },
            {
                "action": "kahn_queue",
                "narration": "Kahn’s algorithm starts with all zero-indegree nodes in a queue and processes them BFS-style.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "from collections import deque, defaultdict\nn = 4\ndeps = [[1, 0], [2, 0], [3, 1], [3, 2]]\nindegree = [0] * n\nadj = defaultdict(list)\nfor a, b in deps:\n    adj[b].append(a)\n    indegree[a] += 1\nqueue = deque([i for i in range(n) if indegree[i] == 0])\norder = []\nwhile queue:\n    node = queue.popleft()\n    order.append(node)\n    for nxt in adj[node]:\n        indegree[nxt] -= 1\n        if indegree[nxt] == 0:\n            queue.append(nxt)\nprint('order:', order)\nprint('possible:', len(order) == n)",
                    "expected_output": "order: [0, 1, 2, 3]",
                    "hint": "0 first, then 1 and 2 (order may vary), then 3.",
                },
            },
            {
                "action": "cycle_detection",
                "narration": "If the BFS processes fewer than n nodes, a cycle exists. Those nodes can never be reached.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "deps = [[0, 1], [1, 2], [2, 0]]. After Kahn’s algorithm, what is the result?",
                    "options": [
                        {"id": "a", "text": "Empty order — cycle detected", "correct": True},
                        {"id": "b", "text": "[0, 1, 2]", "correct": False},
                        {"id": "c", "text": "Any order is valid", "correct": False},
                        {"id": "d", "text": "Depends on queue order", "correct": False},
                    ],
                    "explanation": "All three nodes have indegree 1. No node has indegree 0, so the queue is empty and order is empty.",
                },
            },
            {
                "action": "dfs_alternative",
                "narration": "DFS can also produce a topological order by appending nodes after visiting all descendants.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "def dfs_order(n, deps):\n    adj = [[] for _ in range(n)]\n    for a, b in deps:\n        adj[b].append(a)\n    visited = [0] * n\nn    order = []\n    def dfs(node):\n        visited[node] = 1\n        for nxt in adj[node]:\n            if visited[nxt] == 1:\n                raise ValueError('cycle')\n            if not visited[nxt]:\n                dfs(nxt)\n        visited[node] = 2\n        order.append(node)\n    for i in range(n):\n        if not visited[i]:\n            dfs(i)\n    return order[::-1]\n\nprint(dfs_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]))",
                    "expected_output": "[0, 2, 1, 3]",
                    "hint": "DFS post-order reversed gives a valid topological sort.",
                },
            },
        ],
        "conclusion": (
            "Kahn’s algorithm removes zero-indegree nodes BFS-style. "
            "If all nodes are processed, the order is valid. Otherwise, a cycle exists."
        ),
    },
    "prediction": {
        "title": "Before You Sort",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Before you code it, predict whether completion is possible.”",
        "question": "Can you complete 3 courses with prerequisites [[1, 0], [2, 1]]?",
        "options": [
            {"id": "a", "text": "Yes — order [0, 1, 2]", "correct": True, "explanation": "0 has no prerequisites, then 1, then 2."},
            {"id": "b", "text": "No — circular dependency", "correct": False, "explanation": "There is no cycle."},
            {"id": "c", "text": "Yes — any order works", "correct": False, "explanation": "Order must respect prerequisites."},
            {"id": "d", "text": "Depends on the number of courses", "correct": False, "explanation": "The prerequisite structure determines feasibility."},
        ],
        "explanation": "The prerequisites form a DAG: 0 -> 1 -> 2. Completion is possible.",
    },
    "explain": {
        "title": "Explain the Chain",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Why does Kahn’s algorithm detect cycles?”",
        "prompt": "Why does Kahn's algorithm detect cycles?",
        "answer_format": "short_answer",
        "keywords": ["indegree", "zero", "cycle", "remaining", "queue", "process", "node", "edge"],
        "min_words": 10,
        "model_answer": (
            "Kahn's algorithm removes nodes with zero indegree. In a DAG, at least one node has zero indegree. "
            "In a cycle, every node has indegree >= 1, so no node can be removed. "
            "If nodes remain after processing, a cycle exists."
        ),
        "intention": "The explanation must connect indegree zero to cycle detection.",
    },
    "guided_build": {
        "title": "Write the Scheduler",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Now you write Kahn’s algorithm.”",
        "steps": [
            {
                "step_order": 1,
                "title": "Course Schedule",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Build indegree map, queue zero-indegree nodes, process edges.”",
                "description": "Return True if you can finish all courses, False if there is a cycle.",
                "starter_code": "from collections import deque, defaultdict\n\ndef can_finish(num_courses, prerequisites):\n    adj = defaultdict(list)\n    indegree = [0] * num_courses\n    for dest, src in prerequisites:\n        adj[src].append(dest)\n        indegree[dest] += 1\n    queue = deque([i for i in range(num_courses) if indegree[i] == 0])\n    count = 0\n    while queue:\n        node = queue.popleft()\n        count += 1\n        for nxt in adj[node]:\n            indegree[nxt] -= 1\n            if indegree[nxt] == 0:\n                queue.append(nxt)\n    return count == num_courses\n",
                "function_name": "can_finish",
                "signature": "def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:",
                "test_cases": [
                    {"input": [2, [[1, 0]]], "expected": True},
                    {"input": [2, [[1, 0], [0, 1]]], "expected": False},
                ],
                "hidden_test_cases": [
                    {"input": [3, [[0, 1], [1, 2]]], "expected": True},
                    {"input": [3, [[0, 1], [1, 2], [2, 0]]], "expected": False},
                ],
                "diamonds": 50,
                "scaffolded_hints": [
                    {"level": 1, "text": "Build an adjacency list and an indegree array."},
                    {"level": 2, "text": "Start BFS from all zero-indegree nodes."},
                    {"level": 3, "text": "If processed count == num_courses, no cycle."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Alien Dictionary",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Same sort idea. Derive character order from a sorted word list.”",
        "description": (
            "Given a sorted dictionary of an alien language, return the order of characters. "
            "If the order is invalid, return empty string."
        ),
        "function_name": "alien_order",
        "signature": "def alien_order(words: List[str]) -> str:",
        "description_full": (
            "Return the order of characters in the alien language.\n\n"
            "Example:\n"
            "  alien_order([\"wrt\", \"wrf\", \"er\", \"ett\", \"rftt\"]) -> \"wertf\"\n\n"
            "Build a graph from adjacent word comparisons, then topological sort."
        ),
        "test_cases": [
            {"input": [["wrt", "wrf", "er", "ett", "rftt"]], "expected": "wertf"},
        ],
        "hidden_test_cases": [
            {"input": [["z", "x"]], "expected": "zx"},
        ],
        "time_limit_minutes": 8,
        "diamonds": 70,
        "scaffolded_hints": [
            {"level": 1, "text": "Compare adjacent words to find the first differing character."},
            {"level": 2, "text": "Build a directed edge from word1[c] to word2[c]."},
            {"level": 3, "text": "Topological sort the graph; detect cycles."},
        ],
    },
    "assessment": {
        "title": "Prerequisite Chain Final Test",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Prove you can order any DAG. Timed.”",
        "description": "Detect cycles, explain indegree, and fix a DFS cycle miss.",
        "questions": [
            {
                "type": "code_tracing",
                "code": "from collections import deque, defaultdict\ndef can_finish(n, deps):\n    adj = defaultdict(list)\n    indegree = [0] * n\n    for a, b in deps:\n        adj[b].append(a)\n        indegree[a] += 1\n    q = deque([i for i in range(n) if indegree[i] == 0])\n    count = 0\n    while q:\n        node = q.popleft()\n        count += 1\n        for nxt in adj[node]:\n            indegree[nxt] -= 1\n            if indegree[nxt] == 0:\n                q.append(nxt)\n    return count == n\n\nprint(can_finish(3, [[0, 1], [1, 2]]))",
                "answer_format": "single_choice",
                "expected_answer": "True",
                "options": [
                    {"id": "a", "text": "True", "correct": True},
                    {"id": "b", "text": "False", "correct": False},
                ],
                "explanation": "The prerequisites form a DAG. All 3 courses can be completed.",
            },
            {
                "type": "concept",
                "question": "Why does Kahn’s algorithm detect cycles?",
                "answer_format": "short_answer",
                "keywords": ["indegree", "zero", "cycle", "remaining", "queue", "process", "node", "edge"],
                "explanation": "In a cycle, every node has indegree >= 1, so no node can be removed.",
            },
            {
                "type": "debug",
                "code": "def can_finish(n, deps):\n    adj = [[] for _ in range(n)]\n    for a, b in deps:\n        adj[b].append(a)\n    visited = [0] * n\n    def dfs(node):\n        visited[node] = 1\n        for nxt in adj[node]:\n            if visited[nxt] == 1:\n                return False\n            if not dfs(nxt):\n                return False\n        visited[node] = 2\n        return True\n    return all(dfs(i) for i in range(n))\n# should detect all cycles",
                "error": "DFS back-edge detection misses some cycles because it doesn't restart from unvisited nodes correctly.",
                "question": "Fix the cycle detection.",
                "fix": "for i in range(n):\n    if not visited[i]:\n        if not dfs(i):\n            return False\nreturn True",
                "explanation": "DFS must restart from every unvisited node to detect all cycles.",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 100,
    },
    "break": {
        "title": "The Missing Edge",
        "captain_byte_intro": "🧭 **Captain Byte**\n“I forgot to build the adjacency list. Find the broken assumption.”",
        "story": (
            "A programmer checked indegrees but forgot to build adjacency edges. "
            "The queue processed nodes, but no edges were ever decremented. "
            "What assumption is wrong?"
        ),
        "buggy_code": "def can_finish(n, deps):\n    indegree = [0] * n\n    for a, b in deps:\n        indegree[a] += 1\n    queue = [i for i in range(n) if indegree[i] == 0]\n    count = 0\n    while queue:\n        node = queue.pop(0)\n        count += 1\n    return count == n\n",
        "expected_output": "False for cycle",
        "actual_output": "True for cycle — edges never processed",
        "diagnosis": {
            "question": "Which assumption makes this scheduler miss cycles?",
            "options": [
                {"id": "a", "text": "It counts indegrees but never decrements them via adjacency edges", "correct": True, "why": "Without adjacency edges, indegrees never change, so the count always equals n."},
                {"id": "b", "text": "It uses a list instead of deque", "correct": False, "why": "List vs deque is not the issue; the missing adjacency is."},
                {"id": "c", "text": "It doesn't handle empty prerequisites", "correct": False, "why": "Empty prerequisites would work fine."},
                {"id": "d", "text": "The cycle check is wrong", "correct": False, "why": "The cycle check logic is correct if edges were processed."},
            ],
        },
        "fix": "Build adjacency list and decrement indegrees when processing edges.",
        "fixed_code": "def can_finish(n, deps):\n    from collections import deque, defaultdict\n    adj = defaultdict(list)\n    indegree = [0] * n\n    for a, b in deps:\n        adj[b].append(a)\n        indegree[a] += 1\n    queue = deque([i for i in range(n) if indegree[i] == 0])\n    count = 0\n    while queue:\n        node = queue.popleft()\n        count += 1\n        for nxt in adj[node]:\n            indegree[nxt] -= 1\n            if indegree[nxt] == 0:\n                queue.append(nxt)\n    return count == n\n",
        "explanation": (
            "Indegree counts alone are static. Processing edges decrements indegrees, "
            "revealing new zero-indegree nodes. Without edges, the algorithm never detects cycles."
        ),
    },
    "srs_enrollment": {
        "concept_id": "dsa:graphs:topological_sort",
        "concept_name": "Course Schedule",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "build adjacency list and indegree map",
            "queue zero-indegree nodes",
            "decrement indegree when processing edges",
            "cycle if processed count < total nodes",
        ],
        "spaced_fields": [
            "indegree_map",
            "zero_indegree_queue",
            "process_edges",
            "cycle_detection",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "course_schedule",
        "unlocks_next": ["graph_patterns"],
        "tower_badge": "prerequisite_chain",
        "world_node": {
            "level": 24,
            "title": "The Prerequisite Chain",
            "color": "teal",
            "icon": "⛓️",
            "description": "Detect cycles and return valid course ordering using Kahn's algorithm",
        },
    },
}
