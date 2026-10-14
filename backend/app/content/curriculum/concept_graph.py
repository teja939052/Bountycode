"""
Concept Clarity Slice: Graph BFS/DFS
======================================

Graphs model connections. BFS explores layer by layer and finds shortest paths
in unweighted graphs. DFS explores as deep as possible before backtracking and
is useful for cycles, connectivity, and topological order.

Misconceptions attacked:
  1. "BFS is always better than DFS" — they solve different problems
  2. "DFS needs recursion" — it can be iterative with an explicit stack
  3. "Graphs need adjacency matrices" — adjacency lists are usually better
"""
from typing import Dict, Any

GRAPH_SLICE: Dict[str, Any] = {
    "lesson_id": "graph_explorer",
    "module_id": "dsa:graph",
    "title": "The Island Explorer",
    "description": "Learn BFS and DFS by exploring islands and rivers on a map.",
    "difficulty": "medium",
    "est_minutes": 18,
    "xp_reward": 270,
    "skills_taught": ["graph", "bfs", "dfs", "traversal", "adjacency_list"],
    "srs_concept_tag": "dsa:graph",
    "story_context": {
        "title": "The Island Explorer",
        "narration": (
            "You have a map of islands connected by bridges. You may walk bridge by "
            "bridge (BFS) or plunge deep into one island chain (DFS). Both can visit "
            "every island, but they visit in different orders."
        ),
        "setting": "island_map",
        "character": "Cartographer Lira",
        "intro_text": (
            "Every bridge connects two islands. I will show you two ways to visit "
            "every island without crossing a bridge twice."
        ),
    },
    "discovery": {
        "title": "Layers vs Depth",
        "steps": [
            {
                "action": "compare",
                "narration": (
                    "BFS visits neighbors first, then neighbors of neighbors. "
                    "DFS visits one path until it ends, then backtracks."
                ),
                "interaction": {
                    "type": "inspect_code",
                    "code": "from collections import deque\n\ngraph = {\n    0: [1, 2],\n    1: [0, 3],\n    2: [0],\n    3: [1],\n}\n\n# BFS order\nqueue = deque([0])\nvisited = {0}\norder = []\nwhile queue:\n    node = queue.popleft()\n    order.append(node)\n    for nb in graph[node]:\n        if nb not in visited:\n            visited.add(nb)\n            queue.append(nb)\nprint('BFS:', order)",
                    "expected_output": "BFS: [0, 1, 2, 3]",
                    "hint": "BFS uses a queue and expands outward.",
                },
            },
        ],
    },
    "manipulation": {
        "title": "DFS with Stack",
        "steps": [
            {
                "action": "dfs",
                "narration": "Visit the graph depth-first using an explicit stack.",
                "interaction": {
                    "type": "code",
                    "starter_code": "graph = {\n    0: [1, 2],\n    1: [0, 3],\n    2: [0],\n    3: [1],\n}\n\nvisited = set()\norder = []\nstack = [0]\n\nwhile stack:\n    # TODO: pop and visit unseen neighbors\n    pass\n\nprint('DFS:', order)\n",
                    "solution": "graph = {\n    0: [1, 2],\n    1: [0, 3],\n    2: [0],\n    3: [1],\n}\n\nvisited = set()\norder = []\nstack = [0]\n\nwhile stack:\n    node = stack.pop()\n    if node in visited:\n        continue\n    visited.add(node)\n    order.append(node)\n    for nb in graph[node]:\n        if nb not in visited:\n            stack.append(nb)\n\nprint('DFS:', order)\n",
                    "expected_output": "DFS: [0, 2, 1, 3]\n",
                    "hint": "Pop from stack, skip if already visited, then push neighbors.",
                },
            },
        ],
    },
    "code": {
        "title": "Count Connected Components",
        "starter_code": "graph = {\n    0: [1],\n    1: [0],\n    2: [3],\n    3: [2],\n    4: [],\n}\n\ndef count_components(graph):\n    # TODO\n    pass\n\nprint(count_components(graph))  # 3\n",
        "solution": "graph = {\n    0: [1],\n    1: [0],\n    2: [3],\n    3: [2],\n    4: [],\n}\n\ndef count_components(graph):\n    visited = set()\n    components = 0\n    for node in graph:\n        if node in visited:\n            continue\n        components += 1\n        stack = [node]\n        while stack:\n            current = stack.pop()\n            if current in visited:\n                continue\n            visited.add(current)\n            for nb in graph[current]:\n                if nb not in visited:\n                    stack.append(nb)\n    return components\n\nprint(count_components(graph))\n",
        "expected_output": "3\n",
    },
    "checks": [
        r"def count_components\(",
        r"visited\.add\(",
        r"stack\.append\(",
    ],
    "success": {
        "before": "You walk the map without a plan.",
        "after": "You traverse with BFS or DFS and count components cleanly.",
        "title": "Island Explorer — you can traverse graphs and count components.",
        "lesson": "Graph traversal order changes the journey, not the reachability.",
        "next": "Try shortest path or cycle detection next.",
    },
}
