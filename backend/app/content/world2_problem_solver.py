"""World 2 — Problem Solver: Algorithms + Problem Solving.

Teaches the patterns behind DSA problems: arrays, trees, graphs, DP.
Each lesson explains WHY the pattern matters and HOW it appears in interviews
and real systems.
"""
from __future__ import annotations

from app.content.lesson_definitions import (
    LessonDefinition, LessonStep, TownDefinition, WorldDefinition,
)

ARRAYS_TOWN = TownDefinition(
    id="arrays",
    name="Arrays & Hashing",
    icon="📊",
    description="The most common interview pattern. Master it first.",
    order=1,
    mental_model="Arrays store sequences; hash maps give instant lookup.",
    canonical_skills=["dsa.arrays", "dsa.hashing"],
    competencies=["two_pointers", "sliding_window", "prefix_sum", "hashing"],
    lessons=[
        LessonDefinition(
            id="arrays-1", title="Two Pointers", icon="👉", order=1,
            concept="two_pointers",
            mental_model="Two pointers walk from opposite ends — O(n) instead of O(n^2).",
            canonical_skill="dsa.two_pointers",
            why_this_matters="Two pointers turn brute-force O(n^2) into O(n). This pattern appears in 30% of array interview questions.",
            engineering_context="In real systems, two pointers merge sorted lists (database joins), find palindromes, detect cycles.",
            builds_toward="DSA Interviews — array pattern recognition",
            steps=[
                LessonStep(step_type="discover", title="Walking from Both Ends",
                    content="left=0, right=len-1. Move inward. One pass, O(n).", visual="-> [1,3,5,7,9] <-"),
                LessonStep(step_type="predict", title="How Many Steps?",
                    question="Array of 5 elements. How many pointer moves?",
                    options=[{"id":"a","text":"5","correct":True},{"id":"b","text":"10","correct":False},{"id":"c","text":"25","correct":False}]),
                LessonStep(step_type="build", title="Two Sum Sorted",
                    function_name="two_sum", signature="def two_sum(nums: list, target: int) -> list:",
                    description="Return 1-based indices of two numbers that add to target.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static int solution() { return 0; }", "cpp": "int solution() { return 0; }", "c": "int solution() { return 0; }"},
                    signatures={"python": "def solution():", "java": "public static int solution()", "cpp": "int solution()", "c": "int solution()"},
                    test_cases=[{"input":[[2,7,11,15],9],"expected":[1,2]}], hidden_tests=4),
            ],
            mastery_evidence=["Solve two-pointer problems in O(n)"],
            unlocks="arrays-2",
        ),
        LessonDefinition(
            id="arrays-2", title="Sliding Window", icon="🪟", order=2,
            concept="sliding_window",
            mental_model="A window slides across the array — add one, remove one, track the best.",
            canonical_skill="dsa.sliding_window",
            why_this_matters="Sliding window solves subarray problems in O(n). Without it, O(n^2).",
            engineering_context="In networking, sliding windows control TCP. In analytics, moving averages.",
            builds_toward="DSA Interviews — subarray optimization",
            steps=[
                LessonStep(step_type="discover", title="The Window",
                    content="Expand right, contract left. Track the best."),
                LessonStep(step_type="predict", title="How Many Windows?",
                    question="Array of 5, window=3. How many windows?",
                    options=[{"id":"a","text":"3","correct":True},{"id":"b","text":"5","correct":False}]),
                LessonStep(step_type="build", title="Longest Unique Substring",
                    function_name="length_of_longest_substring", signature="def length_of_longest_substring(s: str) -> int:",
                    description="Return length of longest substring without repeating characters.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static int solution() { return 0; }", "cpp": "int solution() { return 0; }", "c": "int solution() { return 0; }"},
                    signatures={"python": "def solution():", "java": "public static int solution()", "cpp": "int solution()", "c": "int solution()"},
                    test_cases=[{"input":["abcabcbb"],"expected":3}], hidden_tests=4),
            ],
            mastery_evidence=["Apply sliding window to subarray problems"],
            unlocks="arrays-3",
        ),
        LessonDefinition(
            id="arrays-3", title="Hash Map Lookup", icon="🔑", order=3,
            concept="hashing",
            mental_model="Hash maps trade space for time — O(1) lookup instead of O(n).",
            canonical_skill="dsa.hashing",
            why_this_matters="Hash maps are the most used data structure. They turn lookup from O(n) to O(1).",
            engineering_context="In backend, hash maps power caches (Redis), counters, and deduplication.",
            builds_toward="System Design — caching and indexing",
            steps=[
                LessonStep(step_type="discover", title="Instant Lookup",
                    content="prices = {'apple': 5}. prices['apple'] is 5 in O(1)."),
                LessonStep(step_type="manipulate", title="Count Occurrences",
                    content="For each item, increment its count in a hash map."),
                LessonStep(step_type="build", title="Two Sum Unsorted",
                    function_name="two_sum_unsorted", signature="def two_sum_unsorted(nums: list, target: int) -> list:",
                    description="Return indices of two numbers that add to target. Use hash map.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static int solution() { return 0; }", "cpp": "int solution() { return 0; }", "c": "int solution() { return 0; }"},
                    signatures={"python": "def solution():", "java": "public static int solution()", "cpp": "int solution()", "c": "int solution()"},
                    test_cases=[{"input":[[2,7,11,15],9],"expected":[0,1]}], hidden_tests=4),
            ],
            mastery_evidence=["Use hash maps for O(1) lookups"],
            unlocks="arrays-boss",
        ),
        LessonDefinition(
            id="arrays-boss", title="Arrays Boss", icon="🐉", kind="boss", order=4,
            concept="transfer",
            mental_model="Recognize which array pattern fits a new problem.",
            canonical_skill="dsa.arrays", xp=100, estimated_minutes=15,
            why_this_matters="Interviewers don't tell you which pattern to use. Recognition is the skill.",
            engineering_context="A senior engineer sees nested loops and says 'use a hash map for O(n)'.",
            builds_toward="DSA Interviews — independent pattern recognition",
            steps=[
                LessonStep(step_type="mastery", title="Max Consecutive Ones",
                    function_name="find_max_consecutive_ones", signature="def find_max_consecutive_ones(nums: list) -> int:",
                    description="Return max number of consecutive 1s.",
                    test_cases=[{"input":[[1,1,0,1,1,1]],"expected":3}], hidden_tests=5),
            ],
            mastery_evidence=["Recognize and apply the right array pattern"],
        ),
    ],
)

TREES_TOWN = TownDefinition(
    id="trees", name="Trees", icon="🌳", description="Hierarchical data everywhere.",
    order=2, mental_model="Trees organize hierarchy — traverse them recursively.",
    canonical_skills=["dsa.trees"], competencies=["dfs", "bfs", "recursion", "tree_dp"],
    lessons=[
        LessonDefinition(
            id="trees-1", title="Depth-First Search", icon="⬇️", order=1,
            concept="dfs", mental_model="Go deep first, then backtrack.",
            canonical_skill="dsa.dfs",
            why_this_matters="DFS is the foundation of tree and graph traversal.",
            engineering_context="In compilers, DFS traverses ASTs. In package managers, DFS resolves dependencies.",
            builds_toward="DSA Interviews — tree traversal",
            steps=[
                LessonStep(step_type="discover", title="Go Deep",
                    content="Visit node -> recurse left -> recurse right."),
                LessonStep(step_type="predict", title="Traversal Order",
                    question="Tree: 1->2,3. 2->4,5. DFS order is?"),
                LessonStep(step_type="build", title="Max Depth",
                    function_name="max_depth", signature="def max_depth(root: dict) -> int:",
                    description="Return maximum depth of binary tree.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static int solution() { return 0; }", "cpp": "int solution() { return 0; }", "c": "int solution() { return 0; }"},
                    signatures={"python": "def solution():", "java": "public static int solution()", "cpp": "int solution()", "c": "int solution()"},
                    test_cases=[{"input":[{"val":3,"left":{"val":9},"right":{"val":20}}],"expected":2}], hidden_tests=4),
            ],
            mastery_evidence=["Implement DFS traversal recursively"],
            unlocks="trees-2",
        ),
        LessonDefinition(
            id="trees-2", title="Breadth-First Search", icon="↔️", order=2,
            concept="bfs", mental_model="BFS explores level by level — shortest path.",
            canonical_skill="dsa.bfs",
            why_this_matters="BFS finds shortest path in unweighted graphs.",
            engineering_context="In social networks, BFS computes friend-of-friend distances.",
            builds_toward="DSA Interviews — shortest path problems",
            steps=[
                LessonStep(step_type="discover", title="Level by Level",
                    content="Visit all nodes at depth 0, then depth 1, then depth 2."),
                LessonStep(step_type="build", title="Level Order",
                    function_name="level_order", signature="def level_order(root: dict) -> list:",
                    description="Return values level by level.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static int solution() { return 0; }", "cpp": "int solution() { return 0; }", "c": "int solution() { return 0; }"},
                    signatures={"python": "def solution():", "java": "public static int solution()", "cpp": "int solution()", "c": "int solution()"},
                    test_cases=[{"input":[{"val":3,"left":{"val":9},"right":{"val":20}}],"expected":[[3],[9,20]]}], hidden_tests=4),
            ],
            mastery_evidence=["Implement BFS with a queue"],
            unlocks="trees-boss",
        ),
        LessonDefinition(
            id="trees-boss", title="Trees Boss", icon="🐉", kind="boss", order=3,
            concept="transfer", mental_model="Choose the right tree technique.",
            canonical_skill="dsa.trees", xp=100, estimated_minutes=15,
            why_this_matters="Real tree problems combine traversal, recursion, and DP.",
            engineering_context="Finding LCA requires combining DFS with path tracking.",
            builds_toward="DSA Interviews — combining tree techniques",
            steps=[
                LessonStep(step_type="mastery", title="Lowest Common Ancestor",
                    function_name="lca", signature="def lca(root: dict, p: int, q: int) -> int:",
                    description="Return lowest common ancestor of nodes p and q.",
                    test_cases=[{"input":[{"val":3,"left":{"val":5},"right":{"val":1}},5,1],"expected":3}], hidden_tests=5),
            ],
            mastery_evidence=["Traverse trees with DFS/BFS", "Apply DP to trees"],
        ),
    ],
)

GRAPHS_TOWN = TownDefinition(
    id="graphs", name="Graphs", icon="🕸️", description="Everything is connected.",
    order=3, mental_model="Graphs model relationships — traverse, find path, detect cycles.",
    canonical_skills=["dsa.graphs"], competencies=["graph_bfs", "graph_dfs", "topological_sort", "union_find"],
    lessons=[
        LessonDefinition(
            id="graphs-1", title="Graph Traversal", icon="🔍", order=1,
            concept="graph_bfs", mental_model="Graphs need visited sets.",
            canonical_skill="dsa.graph_bfs",
            why_this_matters="Graphs model the real world: social networks, maps, dependencies.",
            engineering_context="Google's PageRank is graph traversal.",
            builds_toward="DSA Interviews — graph traversal",
            steps=[
                LessonStep(step_type="discover", title="Visited Sets",
                    content="Track visited nodes to avoid infinite loops in cycles."),
                LessonStep(step_type="build", title="Count Components",
                    function_name="count_components", signature="def count_components(n: int, edges: list) -> int:",
                    description="Return number of connected components.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static int solution() { return 0; }", "cpp": "int solution() { return 0; }", "c": "int solution() { return 0; }"},
                    signatures={"python": "def solution():", "java": "public static int solution()", "cpp": "int solution()", "c": "int solution()"},
                    test_cases=[{"input":[[5,[[0,1],[1,2],[3,4]]]],"expected":2}], hidden_tests=4),
            ],
            mastery_evidence=["Traverse graphs with BFS/DFS and visited sets"],
            unlocks="graphs-2",
        ),
        LessonDefinition(
            id="graphs-2", title="Topological Sort", icon="📋", order=2,
            concept="topological_sort", mental_model="Order tasks by dependencies.",
            canonical_skill="dsa.topological_sort",
            why_this_matters="Topological sort solves scheduling problems.",
            engineering_context="Build systems use topological sort for compilation order.",
            builds_toward="DSA Interviews — scheduling problems",
            steps=[
                LessonStep(step_type="build", title="Course Schedule",
                    function_name="can_finish", signature="def can_finish(n: int, prereqs: list) -> bool:",
                    description="Return True if all courses can be finished.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static int solution() { return 0; }", "cpp": "int solution() { return 0; }", "c": "int solution() { return 0; }"},
                    signatures={"python": "def solution():", "java": "public static int solution()", "cpp": "int solution()", "c": "int solution()"},
                    test_cases=[{"input":[[2,[[1,0]]]],"expected":True}], hidden_tests=4),
            ],
            mastery_evidence=["Apply topological sort to dependency problems"],
            unlocks="graphs-boss",
        ),
        LessonDefinition(
            id="graphs-boss", title="Graphs Boss", icon="🐉", kind="boss", order=3,
            concept="transfer", mental_model="Choose the right graph technique.",
            canonical_skill="dsa.graphs", xp=100, estimated_minutes=15,
            why_this_matters="Real graph problems combine multiple techniques.",
            builds_toward="DSA Interviews — combining graph techniques",
            steps=[
                LessonStep(step_type="mastery", title="Clone Graph",
                    function_name="clone_graph", signature="def clone_graph(node: dict) -> dict:",
                    description="Return deep copy of connected undirected graph.",
                    test_cases=[{"input":[{"val":1,"neighbors":[]}],"expected":"copy"}], hidden_tests=5),
            ],
            mastery_evidence=["Traverse graphs", "Topological sort", "Choose the right technique"],
        ),
    ],
)

DP_TOWN = TownDefinition(
    id="dp", name="Dynamic Programming", icon="🧩", description="Break big problems into small ones.",
    order=4, mental_model="DP = recursion + memoization. Solve each subproblem once.",
    canonical_skills=["dsa.dp"], competencies=["memoization", "tabulation", "knapsack", "subsequences"],
    lessons=[
        LessonDefinition(
            id="dp-1", title="Memoization", icon="📝", order=1,
            concept="memoization", mental_model="Cache results — never compute the same thing twice.",
            canonical_skill="dsa.memoization",
            why_this_matters="Memoization turns exponential-time recursion into polynomial time.",
            engineering_context="React's useMemo is memoization. In production, it prevents redundant API calls.",
            builds_toward="DSA Interviews — top-down DP",
            steps=[
                LessonStep(step_type="discover", title="Cache It",
                    content="If f(n) depends on f(n-1) and f(n-2), compute each once and store."),
                LessonStep(step_type="build", title="Climbing Stairs",
                    function_name="climb_stairs", signature="def climb_stairs(n: int) -> int:",
                    description="Return number of ways to climb n stairs.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static int solution() { return 0; }", "cpp": "int solution() { return 0; }", "c": "int solution() { return 0; }"},
                    signatures={"python": "def solution():", "java": "public static int solution()", "cpp": "int solution()", "c": "int solution()"},
                    test_cases=[{"input":[3],"expected":3}], hidden_tests=4),
            ],
            mastery_evidence=["Apply memoization to recursive problems"],
            unlocks="dp-2",
        ),
        LessonDefinition(
            id="dp-2", title="Tabulation", icon="📊", order=2,
            concept="tabulation", mental_model="Build answer bottom-up — fill a table.",
            canonical_skill="dsa.tabulation",
            why_this_matters="Tabulation avoids recursion overhead and stack overflow.",
            engineering_context="Spreadsheet engines use tabulation. Bioinformatics for sequence alignment.",
            builds_toward="DSA Interviews — bottom-up DP",
            steps=[
                LessonStep(step_type="build", title="Coin Change",
                    function_name="coin_change", signature="def coin_change(coins: list, amount: int) -> int:",
                    description="Return minimum coins needed. Return -1 if impossible.",
                    languages=["python", "java", "cpp", "c"],
                    starter_code={"python": "def solution(): pass", "java": "public static int solution() { return 0; }", "cpp": "int solution() { return 0; }", "c": "int solution() { return 0; }"},
                    signatures={"python": "def solution():", "java": "public static int solution()", "cpp": "int solution()", "c": "int solution()"},
                    test_cases=[{"input":[[1,2,5],11],"expected":3}], hidden_tests=4),
            ],
            mastery_evidence=["Build DP tables bottom-up"],
            unlocks="dp-boss",
        ),
        LessonDefinition(
            id="dp-boss", title="DP Boss", icon="🐉", kind="boss", order=3,
            concept="transfer", mental_model="Recognize when a problem is DP.",
            canonical_skill="dsa.dp", xp=100, estimated_minutes=15,
            why_this_matters="The hardest part of DP is recognizing that a problem IS DP.",
            builds_toward="DSA Interviews — DP problem recognition",
            steps=[
                LessonStep(step_type="mastery", title="Edit Distance",
                    function_name="min_distance", signature="def min_distance(word1: str, word2: str) -> int:",
                    description="Return minimum operations to convert word1 to word2.",
                    test_cases=[{"input":["horse","ros"],"expected":3}], hidden_tests=5),
            ],
            mastery_evidence=["Apply memoization", "Build DP tables", "Recognize DP structure"],
        ),
    ],
)

WORLD_2_PROBLEM_SOLVER = WorldDefinition(
    id="problem_solver", name="Problem Solver", icon="🧩",
    subtitle="Algorithms + Problem Solving",
    description="Master the patterns behind DSA: arrays, trees, graphs, DP.",
    order=2, theme="problem_solver",
    towns=[ARRAYS_TOWN, TREES_TOWN, GRAPHS_TOWN, DP_TOWN],
)

def get_world_2() -> WorldDefinition:
    return WORLD_2_PROBLEM_SOLVER

def all_lessons_w2() -> list[LessonDefinition]:
    lessons: list[LessonDefinition] = []
    for town in WORLD_2_PROBLEM_SOLVER.towns:
        lessons.extend(town.lessons)
    return lessons
