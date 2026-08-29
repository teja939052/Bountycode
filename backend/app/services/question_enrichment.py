"""
Question Bank Enrichment Service
=================================

Enriches all existing questions in the bank with:
  - why_this_matters: why this problem is important
  - real_world_use: concrete applications in production
  - pattern_recognition: how to identify this pattern
  - common_mistakes: pitfalls to avoid
  - solution_approach: detailed thought process
  - hints: 3 progressive hints
  - xp_reward: based on difficulty
  - prerequisites: what you need to know
  - similar_problems: related problems

This is our MOAT - questions that teach real engineering, not just textbook problems.
"""
import json
import os
import re
from typing import Dict, Any, Optional, List


# =============================================================
# PATTERN-SPECIFIC ENRICHMENT KNOWLEDGE BASE
# =============================================================

PATTERN_ENRICHMENTS = {
    "two-pointers": {
        "why_this_matters": "Two pointers is one of the most versatile techniques in algorithmic problem solving. It transforms O(n²) brute force into O(n) by using two references that traverse the data structure intelligently. Mastering this pattern unlocks dozens of related problems.",
        "real_world_use": "Used in string matching algorithms (KMP), palindrome detection in DNA sequences, deduplication of sorted logs, merge operations in distributed databases, real-time streaming data where you need to compare current and previous values.",
        "pattern_recognition": "Look for: 'sorted array' + 'find pair/triplet' + 'O(n)' required, OR 'palindrome' problems, OR 'in-place operations' on arrays, OR 'compare ends moving inward'. The key insight is that you can make decisions based on which pointer to move without losing optimality.",
        "anti_patterns": "Don't use two pointers on unsorted arrays unless you sort first (costs O(n log n)). Don't try to use it when you need ALL combinations - that's backtracking. Don't forget edge cases (empty array, single element).",
        "common_mistakes": "1. Moving the wrong pointer (always move the one that can't be optimal). 2. Off-by-one errors in loop conditions. 3. Not handling empty input. 4. Forgetting to check if both pointers are valid.",
        "prerequisites": ["Array basics", "Time complexity analysis", "Two Sum problem"],
        "related_concepts": ["Sliding window", "Binary search", "Merge sort merge step"]
    },
    "sliding-window": {
        "why_this_matters": "Sliding window is THE pattern for substring/subarray problems. It's used in network packet analysis, real-time data streams, time-series analysis, and any problem where you need to find a contiguous range satisfying constraints.",
        "real_world_use": "Network traffic analysis (find peak usage windows), stock price analysis (find best trading windows), bioinformatics (find DNA sequences matching patterns), real-time analytics (rolling averages, recent activity), caching (LRU-like eviction).",
        "pattern_recognition": "Look for: 'contiguous subarray/substring' + 'satisfies condition' + 'longest/shortest/maximum/minimum'. The key insight: expand window to find valid state, contract to find optimal. Fixed size vs variable size windows.",
        "anti_patterns": "Don't recompute from scratch each iteration (use running sum/count). Don't use sliding window when you need non-contiguous subsequences. Don't forget to update your tracking variables when sliding.",
        "common_mistakes": "1. Forgetting to shrink window when condition violated. 2. Not tracking all needed metrics (sum, count, distinct chars). 3. Off-by-one in window boundaries. 4. Using O(n²) when O(n) is possible.",
        "prerequisites": ["Two pointers", "Hash maps", "String basics"],
        "related_concepts": ["Two pointers", "Prefix sums", "Queue data structure"]
    },
    "hash-table": {
        "why_this_matters": "Hash tables are the most important data structure in real-world software. They power databases, caches, compilers, and virtually every high-performance system. Understanding when and how to use them is critical.",
        "real_world_use": "Database indexes, caching systems (Redis, Memcached), symbol tables in compilers, object representation in JavaScript, set membership tests, deduplication, counting occurrences, lookups in O(1).",
        "pattern_recognition": "Look for: 'find complement', 'count occurrences', 'check existence', 'group by property', 'detect duplicates'. Whenever you need O(1) lookup, think hash table.",
        "anti_patterns": "Don't use when you need order (use OrderedDict or sort). Don't forget to handle hash collisions in design questions. Don't use when memory is extremely tight.",
        "common_mistakes": "1. Using mutable objects as keys. 2. Not handling None properly. 3. Assuming hash operations are always O(1) (worst case can be O(n)). 4. Forgetting to clear hash between test cases.",
        "prerequisites": ["Basic data structures", "Time complexity"],
        "related_concepts": ["Hash functions", "Collision resolution", "Caching"]
    },
    "binary-search": {
        "why_this_matters": "Binary search is O(log n) and used in databases, file systems, debugging, version control (git bisect), and anywhere you need fast lookup in sorted data. It's also the foundation for many advanced algorithms.",
        "real_world_use": "Database index lookups, finding bugs with git bisect, autocompletion in IDEs, finding versions in package managers, log file analysis, searching sorted records.",
        "pattern_recognition": "Look for: 'sorted array' + 'find target', OR 'find min/max' satisfying condition (binary search on answer), OR 'O(log n)' required. The key insight: eliminate half the search space each iteration.",
        "anti_patterns": "Don't use on unsorted data. Don't use when you need all matches (use linear scan). Don't forget that binary search has many variants (first occurrence, last occurrence, lower bound, upper bound).",
        "common_mistakes": "1. Off-by-one in mid calculation (use lo + (hi - lo) // 2 to avoid overflow). 2. Wrong loop condition (lo <= hi vs lo < hi). 3. Forgetting to handle empty array. 4. Not considering binary search on answer.",
        "prerequisites": ["Arrays", "Time complexity"],
        "related_concepts": ["Divide and conquer", "Tree search", "Search algorithms"]
    },
    "dp-1d": {
        "why_this_matters": "Dynamic programming is the key to solving optimization problems efficiently. It appears in AI, bioinformatics, economics, and operations research. Mastering 1D DP is the foundation for more complex problems.",
        "real_world_use": "Text autocomplete (word prediction), stock trading strategies, optimal caching, fibonacci-like growth models, shortest path algorithms, bioinformatics (sequence alignment), economics (optimal investment).",
        "pattern_recognition": "Look for: 'count ways' + 'optimal', 'previous decisions affect future', 'overlapping subproblems'. The key insight: store results of subproblems to avoid recomputation. State = what changes between subproblems.",
        "anti_patterns": "Don't use when there are no overlapping subproblems. Don't forget to identify the base case. Don't use when greedy works (greedy is simpler and O(n) usually).",
        "common_mistakes": "1. Wrong base case. 2. Wrong state transition. 3. Wrong iteration order. 4. Forgetting to handle edge cases (empty input, single element).",
        "prerequisites": ["Recursion", "Memoization", "Time complexity"],
        "related_concepts": ["Recursion", "Memoization", "Greedy algorithms"]
    },
    "tree-dfs": {
        "why_this_matters": "Tree DFS is fundamental to file systems, organizational hierarchies, AI decision trees, and parsing. Every recursive tree problem uses DFS in some form.",
        "real_world_use": "File system traversal, parsing expressions in compilers, AI game trees, organizational charts, XML/JSON parsing, decision tree algorithms, finding paths in hierarchies.",
        "pattern_recognition": "Look for: 'tree or graph' + 'explore depth first' + 'backtrack'. Use preorder (root first), inorder (left, root, right), or postorder (children first) depending on the problem.",
        "anti_patterns": "Don't use DFS when you need shortest path in unweighted graph (use BFS). Don't use when you need level-by-level processing (use BFS). Don't forget to handle null nodes.",
        "common_mistakes": "1. Forgetting base case (null node). 2. Stack overflow on deep trees (use iterative). 3. Not tracking visited nodes in graphs. 4. Wrong traversal order for the problem.",
        "prerequisites": ["Recursion", "Tree basics", "Stack data structure"],
        "related_concepts": ["BFS", "Recursion", "Backtracking"]
    },
    "tree-bfs": {
        "why_this_matters": "BFS is used for shortest path in unweighted graphs, level-order processing, and many real-time systems. It's the counterpart to DFS and essential for many algorithms.",
        "real_world_use": "Shortest path in maps, social network connections (degrees of separation), web crawlers, peer-to-peer networks, garbage collection, finding nearest neighbors.",
        "pattern_recognition": "Look for: 'level by level', 'shortest path in unweighted graph', 'nearest first'. Use a queue, process all nodes at current level before moving to next.",
        "anti_patterns": "Don't use for finding all paths (use DFS). Don't use for weighted graphs (use Dijkstra). Don't use when memory is limited and graph is very wide (use DFS).",
        "common_mistakes": "1. Not marking nodes as visited (infinite loop). 2. Forgetting to process all nodes at current level. 3. Using stack instead of queue. 4. Not handling empty queue.",
        "prerequisites": ["Queue", "Graph basics", "Tree basics"],
        "related_concepts": ["DFS", "Dijkstra", "Topological sort"]
    },
    "graph-dfs": {
        "why_this_matters": "Graph DFS is essential for cycle detection, topological sort, path finding, and connected components. Used in compilers, dependency resolution, and network analysis.",
        "real_world_use": "Build systems (make, npm), package managers, dependency resolution, social network analysis, web crawlers, garbage collection, deadlock detection in operating systems.",
        "pattern_recognition": "Look for: 'detect cycle', 'topological order', 'connected components', 'path between nodes', 'all reachable nodes'. Use recursion or stack for DFS.",
        "anti_patterns": "Don't forget to mark visited. Don't use for shortest path in unweighted graph (use BFS). Don't use for shortest path in weighted graph (use Dijkstra).",
        "common_mistakes": "1. Not marking visited (infinite loop in cycles). 2. Stack overflow on deep graphs. 3. Wrong edge direction. 4. Not handling disconnected components.",
        "prerequisites": ["Tree DFS", "Recursion", "Graph representation"],
        "related_concepts": ["BFS", "Topological sort", "Union-Find"]
    },
    "graph-bfs": {
        "why_this_matters": "BFS gives shortest path in unweighted graphs. Used in maps, social networks, and routing protocols.",
        "real_world_use": "Google Maps shortest route, social network degree of separation, GPS navigation, network routing, peer discovery, web crawling level-by-level.",
        "pattern_recognition": "Look for: 'shortest path in unweighted graph', 'minimum moves', 'minimum steps', 'level by level'. Use queue.",
        "anti_patterns": "Don't use for weighted graphs. Don't use when you need all paths. Don't use when memory is very limited and graph is wide.",
        "common_mistakes": "1. Not marking visited. 2. Forgetting to track distance/level. 3. Using stack instead of queue. 4. Not handling multiple sources.",
        "prerequisites": ["Queue", "Tree BFS", "Graph basics"],
        "related_concepts": ["DFS", "Dijkstra", "Bidirectional search"]
    },
    "heap": {
        "why_this_matters": "Heaps provide O(log n) insertion and O(1) min/max access. Used in priority queues, scheduling, graph algorithms (Dijkstra), and top-k problems.",
        "real_world_use": "Priority queues (OS process scheduling), Dijkstra's algorithm, event-driven simulation, top-k queries, median maintenance, task scheduling, real-time bidding.",
        "pattern_recognition": "Look for: 'kth largest/smallest', 'top k', 'priority', 'streaming data with min/max'. Use min-heap for top k largest, max-heap for top k smallest.",
        "anti_patterns": "Don't use when you need all elements sorted (sort is O(n log n) total). Don't use when you need to search (O(n)). Don't use when you need O(1) access to arbitrary element (use array).",
        "common_mistakes": "1. Confusing min-heap and max-heap. 2. Wrong heap size. 3. Not handling empty heap. 4. Using heap when sorted array would be simpler for small n.",
        "prerequisites": ["Priority queue", "Tree basics"],
        "related_concepts": ["Priority queue", "Top-k algorithms", "Dijkstra"]
    },
    "stack": {
        "why_this_matters": "Stacks are fundamental to recursion, expression evaluation, browser history, and many algorithms. Mastering stack-based thinking is essential.",
        "real_world_use": "Browser back button, undo/redo in editors, function call stack, expression evaluation, syntax parsing, depth-first search, backtracking.",
        "pattern_recognition": "Look for: 'matching brackets', 'next greater element', 'expression evaluation', 'nested structures', 'LIFO behavior'. The last opened is the first closed.",
        "anti_patterns": "Don't use when you need FIFO (use queue). Don't use when you need random access. Don't use when you need to search.",
        "common_mistakes": "1. Forgetting to handle empty stack. 2. Wrong order of push/pop. 3. Not using stack for nested problems. 4. Off-by-one in indices.",
        "prerequisites": ["LIFO concept", "Array basics"],
        "related_concepts": ["Queue", "Recursion", "DFS"]
    },
    "queue": {
        "why_this_matters": "Queues provide FIFO behavior essential for BFS, scheduling, and real-time systems. Used in OS scheduling, web servers, and messaging systems.",
        "real_world_use": "Print queue, OS process scheduling, web server request handling, message queues (Kafka, RabbitMQ), BFS, breadth-first processing.",
        "pattern_recognition": "Look for: 'BFS', 'level by level', 'FIFO', 'first come first served', 'scheduling'. Use deque for O(1) operations on both ends.",
        "anti_patterns": "Don't use when you need LIFO (use stack). Don't use for random access. Don't use when you need to process recent first (use stack).",
        "common_mistakes": "1. Using list.pop(0) (O(n) - use deque). 2. Forgetting to handle empty queue. 3. Not tracking level/count in BFS. 4. Adding to wrong end.",
        "prerequisites": ["FIFO concept", "Array basics"],
        "related_concepts": ["Stack", "BFS", "Deque"]
    },
    "backtracking": {
        "why_this_matters": "Backtracking is the core of constraint satisfaction, combinatorial generation, and AI search. It powers sudoku solvers, N-queens, and many AI algorithms.",
        "real_world_use": "Sudoku/chess solvers, AI game playing, constraint satisfaction problems, route planning, scheduling, generating combinations, parsing expressions.",
        "pattern_recognition": "Look for: 'all combinations', 'all permutations', 'generate all', 'constraint satisfaction'. Make choice, explore, undo choice.",
        "anti_patterns": "Don't use for simple iteration (use loops). Don't forget to prune invalid branches early. Don't use when greedy works.",
        "common_mistakes": "1. Forgetting to undo choice (backtrack). 2. Not pruning (exponential blowup). 3. Generating duplicates. 4. Not handling base case.",
        "prerequisites": ["Recursion", "Tree DFS"],
        "related_concepts": ["DFS", "Recursion", "Pruning"]
    },
    "greedy": {
        "why_this_matters": "Greedy algorithms make locally optimal choices hoping for global optimum. They're simple, fast, and often optimal. Used in scheduling, Huffman coding, and many optimization problems.",
        "real_world_use": "Huffman coding (compression), activity selection, job scheduling, coin change (some cases), Dijkstra's algorithm, Kruskal's algorithm, interval scheduling.",
        "pattern_recognition": "Look for: 'optimal choice at each step', 'no need to reconsider', 'interval scheduling', 'activity selection'. Prove greedy choice property.",
        "anti_patterns": "Don't use when local optimum doesn't lead to global (e.g., 0/1 knapsack). Don't use without proving correctness. Don't use when DP is needed.",
        "common_mistakes": "1. Using when DP is required. 2. Wrong greedy choice. 3. Not proving correctness. 4. Sorting by wrong criterion.",
        "prerequisites": ["Sorting", "Proof techniques"],
        "related_concepts": ["Dynamic programming", "Sorting", "Priority queue"]
    },
    "linked-list": {
        "why_this_matters": "Linked lists are fundamental to data structures. They enable efficient insertions/deletions, form the basis of more complex structures, and appear in OS memory management.",
        "real_world_use": "OS memory allocation, undo/redo, music player queues, browser history, hash table chaining, adjacency lists in graphs.",
        "pattern_recognition": "Look for: 'pointer manipulation', 'reverse list', 'detect cycle', 'merge lists', 'dummy head trick'. Use slow/fast pointers for middle/cycle.",
        "anti_patterns": "Don't use when you need random access (use array). Don't forget to handle null. Don't use recursion for very long lists (stack overflow).",
        "common_mistakes": "1. Losing head reference. 2. Not handling null next. 3. Forgetting to update pointers in correct order. 4. Stack overflow on recursive solutions.",
        "prerequisites": ["Pointers/References", "Memory model"],
        "related_concepts": ["Stacks", "Queues", "Graphs"]
    },
    "bit-manipulation": {
        "why_this_matters": "Bit manipulation is the foundation of low-level programming, cryptography, and optimization. It's used in system programming, graphics, and competitive programming.",
        "real_world_use": "Cryptography, error detection/correction, compression, graphics (color representation), system programming, network protocols, database indexes.",
        "pattern_recognition": "Look for: 'space optimization', 'fast operations', 'powers of 2', 'flags', 'XOR trick'. XOR cancels pairs, & isolates bits, | sets bits.",
        "anti_patterns": "Don't use when readability matters more than speed. Don't use when operations are naturally decimal. Don't forget to handle signed vs unsigned.",
        "common_mistakes": "1. Overflow with left shift. 2. Sign bit confusion. 3. Wrong operator precedence. 4. Not considering platform differences.",
        "prerequisites": ["Binary representation", "Boolean algebra"],
        "related_concepts": ["XOR trick", "Bit masks", "Flags"]
    }
}

# =============================================================
# DIFFICULTY-SPECIFIC ENRICHMENTS
# =============================================================

DIFFICULTY_XP = {"easy": 10, "medium": 25, "hard": 50, "expert": 100}

DIFFICULTY_TIME_ESTIMATES = {
    "easy": "5-10 minutes",
    "medium": "15-25 minutes",
    "hard": "30-45 minutes",
    "expert": "45-60+ minutes"
}

# =============================================================
# PREREQUISITE LOOKUP BY TOPIC
# =============================================================

TOPIC_PREREQS = {
    "Arrays & Hashing": ["Basic programming", "Hash maps"],
    "Two Pointers": ["Arrays", "Time complexity"],
    "Sliding Window": ["Two Pointers", "Hash maps"],
    "Stack": ["LIFO concept", "Recursion"],
    "Binary Search": ["Arrays", "Time complexity"],
    "Linked List": ["Pointers/References", "Memory model"],
    "Trees": ["Recursion", "Tree basics"],
    "BST": ["Trees", "Binary search"],
    "Graphs": ["Trees", "Recursion"],
    "Dynamic Programming": ["Recursion", "Memoization"],
    "Backtracking": ["Recursion", "Tree DFS"],
    "Greedy": ["Sorting", "Proof techniques"],
    "Bit Manipulation": ["Binary representation"],
    "Heap / Priority Queue": ["Trees", "Priority queue"],
    "Strings": ["Array basics", "ASCII/Unicode"],
    "Sorting": ["Arrays", "Comparison"],
    "Recursion": ["Functions", "Call stack"],
    "Tries": ["Trees", "Strings"],
    "Union-Find": ["Graph basics", "Trees"],
    "Segment Tree": ["Trees", "Recursion"],
    "Fenwick Tree": ["Arrays", "Binary representation"],
    "Matrix": ["2D arrays", "Graph basics"],
    "Math": ["Basic math", "Bit manipulation"],
}


def infer_pattern(question: Dict[str, Any]) -> str:
    """Infer the pattern from the question fields."""
    pattern = question.get("pattern", "")
    if pattern:
        return pattern

    sub_topic = (question.get("sub_topic") or "").lower()
    title = (question.get("title") or "").lower()
    topic = (question.get("topic") or "").lower()

    # Pattern inference rules
    if "two pointer" in sub_topic or "two sum" in title:
        return "two-pointers"
    if "sliding window" in sub_topic:
        return "sliding-window"
    if "hash" in sub_topic or "hashmap" in sub_topic or "hash table" in sub_topic:
        return "hash-table"
    if "binary search" in sub_topic or "bs " in sub_topic:
        return "binary-search"
    if "dp" in sub_topic or "dynamic" in sub_topic:
        return "dp-1d"
    if "tree" in topic and "dfs" in sub_topic:
        return "tree-dfs"
    if "tree" in topic and "bfs" in sub_topic:
        return "tree-bfs"
    if "graph" in topic and "dfs" in sub_topic:
        return "graph-dfs"
    if "graph" in topic and "bfs" in sub_topic:
        return "graph-bfs"
    if "heap" in sub_topic or "priority" in sub_topic:
        return "heap"
    if "stack" in sub_topic or "monotonic" in sub_topic:
        return "stack"
    if "queue" in sub_topic:
        return "queue"
    if "backtrack" in sub_topic or "recursion" in topic:
        return "backtracking"
    if "greedy" in sub_topic:
        return "greedy"
    if "linked list" in topic or "ll" in sub_topic:
        return "linked-list"
    if "bit" in sub_topic:
        return "bit-manipulation"

    return "general"


def enrich_question(question: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich a question with all interactive learning features."""
    pattern = infer_pattern(question)
    enrichment = PATTERN_ENRICHMENTS.get(pattern, {})
    difficulty = question.get("difficulty", "medium")

    # Add why_this_matters if missing
    if not question.get("why_this_matters"):
        question["why_this_matters"] = enrichment.get(
            "why_this_matters",
            f"This is a {difficulty} problem on {question.get('topic', 'a key topic')}. "
            f"Mastering it builds your problem-solving foundation and is tested in interviews "
            f"at major tech companies."
        )

    # Add real_world_use if missing
    if not question.get("real_world_use") and not question.get("real_world_context"):
        question["real_world_use"] = enrichment.get(
            "real_world_use",
            f"This pattern appears in production systems: search engines, databases, "
            f"caching layers, financial systems, and network protocols. Understanding it "
            f"helps you design better software."
        )

    # Add pattern_recognition if missing
    if not question.get("pattern_recognition"):
        question["pattern_recognition"] = enrichment.get(
            "pattern_recognition",
            f"Identify this pattern by looking for: similar constraints, 'optimal' keywords, "
            f"and the data structures involved. Pattern recognition is the first step to "
            f"solving any algorithmic problem."
        )

    # Add anti_patterns if missing
    if not question.get("anti_patterns"):
        question["anti_patterns"] = enrichment.get(
            "anti_patterns",
            f"Avoid: brute force O(n²) when O(n) is possible, ignoring edge cases, "
            f"using wrong data structure, and not considering time/space tradeoffs."
        )

    # Add common_mistakes if missing
    if not question.get("common_mistakes"):
        question["common_mistakes"] = enrichment.get(
            "common_mistakes",
            f"Common pitfalls: 1) Not handling edge cases (empty input, single element). "
            f"2) Off-by-one errors. 3) Forgetting to update state correctly. "
            f"4) Not validating input. Always test with edge cases before submitting."
        )

    # Add solution_approach if missing
    if not question.get("solution_approach"):
        question["solution_approach"] = question.get("explanation", "")

    # Add prerequisites if missing
    if not question.get("prerequisite_concepts"):
        topic = question.get("topic", "")
        question["prerequisite_concepts"] = TOPIC_PREREQS.get(
            topic, ["Basic programming", "Data structures"]
        )

    # Add XP reward if missing
    if not question.get("xp_reward"):
        question["xp_reward"] = DIFFICULTY_XP.get(difficulty, 10)

    # Add estimated_time if missing
    if not question.get("estimated_time"):
        question["estimated_time"] = DIFFICULTY_TIME_ESTIMATES.get(difficulty, "15-25 minutes")

    # Add gamification hooks
    question["badge_eligible"] = difficulty in ["hard", "expert"]
    question["streak_qualifying"] = True
    question["interview_weight"] = {"easy": 1, "medium": 3, "hard": 5, "expert": 8}.get(difficulty, 1)

    # Add hints if missing or insufficient
    hints = question.get("hints", [])
    # Normalize hints - they may be strings or dicts
    normalized_hints = []
    for h in hints:
        if isinstance(h, str):
            normalized_hints.append({"level": len(normalized_hints) + 1, "type": "conceptual", "text": h})
        elif isinstance(h, dict):
            normalized_hints.append(h)
    if len(normalized_hints) < 3:
        # Generate default hints based on the problem
        default_hints = generate_default_hints(question, enrichment)
        existing_texts = [h.get("text", "") for h in normalized_hints]
        for h in default_hints:
            if h["text"] not in existing_texts:
                normalized_hints.append(h)
        question["hints"] = normalized_hints[:3]  # Cap at 3 hints
    else:
        question["hints"] = normalized_hints[:3]

    return question


def generate_default_hints(question: Dict[str, Any], enrichment: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate default 3-tier progressive hints."""
    pattern = enrichment.get("pattern_recognition", "")
    anti = enrichment.get("anti_patterns", "")

    hint_1 = {
        "level": 1,
        "type": "conceptual",
        "text": f"Think about the pattern: {pattern[:120] if pattern else 'what technique fits this problem?'}",
        "reveal_after_attempts": 1,
    }
    hint_2 = {
        "level": 2,
        "type": "structural",
        "text": f"Consider the data structure. What gives you O(1) lookup or O(n) traversal?",
        "reveal_after_attempts": 2,
    }
    hint_3 = {
        "level": 3,
        "type": "optimization",
        "text": f"Avoid: {anti[:120] if anti else 'brute force — think about optimizing to O(n) or O(n log n)'}",
        "reveal_after_attempts": 3,
    }
    return [hint_1, hint_2, hint_3]


def enrich_question_bank(questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Enrich all questions in a list."""
    enriched = []
    for q in questions:
        enriched.append(enrich_question(q))
    return enriched


def enrich_file(input_path: str, output_path: str = None) -> Dict[str, Any]:
    """Enrich all questions in a JSON file."""
    if output_path is None:
        output_path = input_path

    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        questions = data
    elif isinstance(data, dict) and "questions" in data:
        questions = data["questions"]
        is_dict = True
    else:
        return {"error": "Unknown JSON structure"}

    enriched = enrich_question_bank(questions)

    if isinstance(data, list):
        output_data = enriched
    else:
        output_data = data
        output_data["questions"] = enriched

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    return {
        "input": input_path,
        "output": output_path,
        "total": len(enriched),
        "enriched": sum(1 for q in enriched if q.get("why_this_matters") and q.get("real_world_use")),
    }


if __name__ == "__main__":
    import sys
    files = [
        "app/content/questions/curated/curated.json",
        "app/content/questions/curated/learning_objects.json",
        "app/content/questions/curated/placement_questions.json",
    ]
    for f in files:
        if os.path.exists(f):
            result = enrich_file(f)
            print(f"{f}: {result}")
