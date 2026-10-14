"""Archived from backend/app/data/worlds_data.py during the approved 6-world cut.
Worlds 7-12 (queue/hashing/trees/graphs/dynamic/alpine) plus the Registry-B
merger (_to_level/_to_world + try/except WORLD_REGISTRY injection).
Kept for rollback/reference. NOT imported by active code.
"""

# ═══════════════════════════════════════════════════════════════
# WORLD 7: Queue Plaza (queue)
# ═══════════════════════════════════════════════════════════════
WORLD_QUEUE = World(
    id="queue", name="Queue Plaza", subtitle="First In, First Out",
    description="Stand in line. The first to arrive is the first to be served. Learn queues.",
    icon="🎫", order=7, theme="queue", recommended_roles=["developer"], prerequisites=["stack"],
    towns=[
        _make_town("line", "The Line", "👥", "First come, first served. A fair queue for everyone.", 1, "FIFO", ["data-structures.queue"], ["queue", "fifo", "deque"], [
            _level("q-1","The Line","🚶",1,"queue","FIFO","data-structures.queue","data-structures.queue",
                _story("Queue Plaza — Entrance","Ticket Tina","People line up at the plaza. The first person in line is the first to get in."),
                _tutor("Byte","🧭","A queue is First In, First Out (FIFO). Like a line at a store.","You enqueue at the back and dequeue from the front."),
                _discover("People arrive: Alice, Bob, Charlie. Who goes in first?","queue-line","First person","Alice"),
                _manipulate("enqueue-person","Add person to back of line","queue.append(person)"),
                _code("Implement a queue. Enqueue and dequeue people.","queue = []\n","queue.append('Alice')\nqueue.append('Bob')\nqueue.append('Charlie')\nprint(queue.pop(0))  # Alice"),
                _checks([r"append",r"pop\(0\)",r"queue\s*=\s*\[\]"]),
                ["Enqueue adds to the back.","Dequeue removes from the front.","First in, first out."],
                _success("👥 No line · 🚪 Empty","👥 Line formed · ✅ FIFO working","The queue works fairly!","Queue — First In, First Out.","Enqueue at back, dequeue at front.",20)),
            _level("q-2","The Priority","⭐",2,"priority","Ordering","data-structures.queue","data-structures.queue",
                _story("Queue Plaza — VIP Section","VIP Manager Vera","Some people have priority. They get served before others in the priority queue."),
                _tutor("Byte","🧭","A priority queue serves the highest priority item first, regardless of arrival order.","Useful for scheduling, Dijkstra's algorithm, and more."),
                _discover("Tasks: A(priority 3), B(priority 1), C(priority 2). Serve highest priority first.","priority-tasks","Serve order","B, C, A"),
                _manipulate("priority-serve","Serve highest priority first","sorted by priority"),
                _code("Implement a priority queue and serve tasks by priority.","tasks = [('A',3),('B',1),('C',2)]\n","tasks.sort(key=lambda x: x[1])\nfor task, pri in tasks:\n    print(f'Serving {task} (priority {pri})')"),
                _checks([r"sort",r"key\s*=",r"lambda"]),
                ["Sort by priority.","Serve in priority order.","Highest priority first."],
                _success("⭐ No priority · ❌ Random","⭐ Priority served · ✅ Fair order","Tasks served by priority!","Priority Queue — ordering by importance.","Priority determines service order.",25)),
            _boss("q-boss","The Printer Queue","🖨️",3,"queue-master","Scheduling","data-structures.queue","data-structures.queue",
                _story("Queue Plaza — Center","Printer Manager Paul","A printer queue handles multiple documents. Each job has a priority and page count."),
                _tutor("Byte","🧭","Real-world queues balance priority and fairness. The printer serves jobs efficiently.","Simulate a printer queue with priority handling."),
                _discover("Print jobs: Doc1(3 pages, pri 2), Doc2(1 page, pri 1), Doc3(2 pages, pri 3). Serve by priority.","printer-queue","Serve order","Doc2, Doc1, Doc3"),
                _manipulate("printer-serve","Sort and serve print jobs","priority queue"),
                _code("Simulate a printer queue with priority.","jobs = [('Doc1',3,2),('Doc2',1,1),('Doc3',2,3)]\n","jobs.sort(key=lambda x: x[2])\nfor name, pages, pri in jobs:\n    print(f'Printing {name}: {pages} pages, priority {pri}')"),
                _checks([r"sort",r"lambda",r"jobs"]),
                ["Sort jobs by priority.","Print each job in order.","Track pages and priority."],
                _success("🖨️ Queue chaotic · ❌ Not scheduled","🖨️ Queue ordered · ✅ All printed","All documents printed in priority order!","Queue Master — real-world scheduling.","Queues power real-world systems.",40),
                _reward(diamonds=40,coins=20,badges=["queue-master"],unlocks_town="town-2-hash")),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 8: Hash Harbor (hashing)
# ═══════════════════════════════════════════════════════════════
WORLD_HASHING = World(
    id="hashing", name="Hash Harbor", subtitle="Instant Lookup",
    description="Find anything instantly with a hash function. Learn hash tables and collision resolution.",
    icon="⚡", order=8, theme="hashing", recommended_roles=["developer"], prerequisites=["queue"],
    towns=[
        _make_town("hash", "Hash Dock", "🏗️", "Hash it, store it, find it instantly.", 1, "Key-Value", ["data-structures.hash"], ["hashing", "hash-table", "collision"], [
            _level("h-1","The Hash Function","🔑",1,"hashing","Mapping","data-structures.hash","data-structures.hash",
                _story("Hash Harbor — Dock","Hash Master Hugo","Convert a key into an index using a hash function. The same key always maps to the same index."),
                _tutor("Byte","🧭","A hash function converts a key into an array index. It should be fast and deterministic.","Like a locker number system — your name maps to a specific locker."),
                _discover("Hash function: index = key % 10. Map keys 15, 25, 37 to indices.","hash-calc","Indices","5, 5, 7"),
                _manipulate("compute-hash","index = key % 10","hash function"),
                _code("Implement a simple hash function and map keys to indices.","keys = [15, 25, 37]\n","hash_table = [None]*10\nfor key in keys:\n    idx = key % 10\n    hash_table[idx] = key\nprint(hash_table)"),
                _checks([r"%",r"hash_table",r"idx"]),
                ["The hash function maps keys to indices.","Same key → same index.","Collisions happen when different keys map to the same index."],
                _success("🔑 No mapping · ❌ Lost","🔑 Hash table built · ✅ Keys mapped","Keys are instantly mappable!","Hash Function — key to index mapping.","Deterministic and fast.",20)),
            _level("h-2","The Collision","💥",2,"collision","Resolving","data-structures.hash","data-structures.hash",
                _story("Hash Harbor — Collision Alley","Collision Handler Cara","Two keys hash to the same index! How do you handle it?"),
                _tutor("Byte","🧭","Collisions are handled by chaining (linked list at each index) or open addressing (find next slot).","Chaining is simpler and more common in practice."),
                _discover("Keys 15 and 25 both hash to index 5. Handle the collision.","collision-handle","Resolution","chain at index 5"),
                _manipulate("chain-handle","Store collided keys in a list","hash_table[idx] = [key1, key2]"),
                _code("Handle collisions using chaining.","hash_table = [[] for _ in range(10)]\n","keys = [15, 25, 35]\nfor key in keys:\n    idx = key % 10\n    hash_table[idx].append(key)\nprint(hash_table)"),
                _checks([r"\[\]\s*for",r"append",r"hash_table"]),
                ["Each index holds a chain (list).","Collided keys go into the same chain.","Search through the chain."],
                _success("💥 Collision ignored · ❌ Data lost","💥 Collision chained · ✅ All stored","Collisions are handled with chaining!","Collision Resolution — chaining method.","Every collision has a home.",25)),
            _boss("h-boss","The Dictionary","📖",3,"hash-master","Looking Up","data-structures.hash","data-structures.hash",
                _story("Hash Harbor — Archive","Dictionary Master Dana","Build a dictionary from scratch using a hash table. Look up, insert, and delete in O(1)."),
                _tutor("Byte","🧭","A dictionary (hash map) is the ultimate hash table application. O(1) average lookup, insert, delete.","Python's dict is a built-in hash table. Understanding it from scratch makes you a better developer."),
                _discover("Build a dictionary: {name: age} for Alice:25, Bob:30, Charlie:35.","build-dict","Dictionary","{'Alice':25,'Bob':30,'Charlie':35}"),
                _manipulate("dict-build","Key-value storage","hash map"),
                _code("Implement a simple dictionary with get, set, and delete.","class Dict:\n    def __init__(self):\n        self.size = 10\n        self.buckets = [[] for _ in range(self.size)]\n","def _hash(self, key): return hash(key) % self.size\n    def set(self, key, val):\n        idx = self._hash(key)\n        for i, (k, v) in enumerate(self.buckets[idx]):\n            if k == key: self.buckets[idx][i] = (k, v); return\n        self.buckets[idx].append((key, val))\n    def get(self, key):\n        idx = self._hash(key)\n        for k, v in self.buckets[idx]:\n            if k == key: return v\n        return None"),
                _checks([r"_hash",r"buckets",r"enumerate"]),
                ["Hash the key to find the bucket.","Search the chain for the key.","Update if found, append if new."],
                _success("📖 No dictionary · ❌ Slow lookup","📖 Dictionary built · ✅ O(1) lookup","The dictionary works at lightning speed!","Hash Master — build a hash map from scratch.","O(1) average case for all operations.",40),
                _reward(diamonds=40,coins=20,badges=["hash-master"],unlocks_town="town-2-tree")),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 9: Tree Grove (trees)
# ═══════════════════════════════════════════════════════════════
WORLD_TREES = World(
    id="trees", name="Tree Grove", subtitle="Hierarchical Data",
    description="Trees branch upward and downward. Learn binary trees, BST, and traversal.",
    icon="🌳", order=9, theme="trees", recommended_roles=["developer", "data-analyst"], prerequisites=["hashing"],
    towns=[
        _make_town("binary", "Binary Grove", "🌲", "Each node branches into at most two children.", 1, "Branching", ["data-structures.tree"], ["binary-tree", "traversal", "BST"], [
            _level("t-1","The Branch","🌿",1,"binary tree","Branching","data-structures.tree","data-structures.tree",
                _story("Tree Grove — Root","Tree Keeper Tara","A tree starts with a root. Each node branches into children. The root has no parent."),
                _tutor("Byte","🧭","A binary tree has at most 2 children per node: left and right.","Like a family tree — each person has at most 2 parents in a binary structure."),
                _discover("Build a binary tree: root(1) → left(2), right(3).","tree-build","Tree structure","root with 2 children"),
                _manipulate("branch-node","Node with left and right","TreeNode(val, left, right)"),
                _code("Create a binary tree with root and two children.","class TreeNode:\n    def __init__(self, val):\n        self.val = val\n        self.left = None\n        self.right = None\n","root = TreeNode(1)\nroot.left = TreeNode(2)\nroot.right = TreeNode(3)"),
                _checks([r"class\s+TreeNode",r"self\.left",r"self\.right"]),
                ["Each node has at most 2 children.","Left child < parent, right child > parent (BST).","The root has no parent."],
                _success("🌿 No tree · 🌳 Just a node","🌿 Tree grown · ✅ Rooted","The tree has a root and branches!","Binary Tree — branching structure.","Each node branches into at most two.",20)),
            _level("t-2","The Traversal","🚶",2,"tree traversal","Visiting","data-structures.tree","data-structures.tree",
                _story("Tree Grove — Path","Path Walker Willow","Visit every node in the tree. In-order: left, root, right."),
                _tutor("Byte","🧭","Tree traversal visits all nodes in a specific order. In-order gives sorted output for BSTs.","Pre-order: root, left, right. Post-order: left, right, root. In-order: left, root, right."),
                _discover("Tree: 2(left), 1(root), 3(right). In-order traversal gives?","tree-traverse","Sorted order","2, 1, 3"),
                _manipulate("in-order","Left → Root → Right","recursive"),
                _code("Implement in-order traversal of a binary tree.","root = TreeNode(1)\nroot.left = TreeNode(2)\nroot.right = TreeNode(3)\n","def inorder(node):\n    if node:\n        inorder(node.left)\n        print(node.val)\n        inorder(node.right)\ninorder(root)"),
                _checks([r"if\s+node",r"inorder\(node\.left\)",r"inorder\(node\.right\]"]),
                ["Visit left subtree first.","Then the root.","Then right subtree."],
                _success("🚶 No traversal · ❌ Missed nodes","🚶 Full traversal · ✅ All visited","Every node is visited in order!","Tree Traversal — in-order, pre-order, post-order.","Recursive visiting of all nodes.",25)),
            _boss("t-boss","The BST","🔍",3,"tree-master","Searching","data-structures.tree","data-structures.tree",
                _story("Tree Grove — Summit","BST Master Boris","A Binary Search Tree keeps data sorted. Search in O(log n) by comparing at each node."),
                _tutor("Byte","🧭","BST: left child < parent < right child. Search by comparing and going left or right.","It is like binary search on a tree structure — O(log n) average case."),
                _discover("BST with values 5,3,7,2,4,6,8. Search for 6.","bst-search","Found at node","6"),
                _manipulate("bst-search","Compare, go left or right","recursive"),
                _code("Implement BST search.","root = TreeNode(5)\nroot.left = TreeNode(3)\nroot.right = TreeNode(7)\n","def search(node, val):\n    if not node: return False\n    if node.val == val: return True\n    if val < node.val: return search(node.left, val)\n    return search(node.right, val)\nprint(search(root, 6))"),
                _checks([r"if\s+not\s+node",r"if\s+val\s*==",r"search\(node\.left"]),
                ["Compare with current node.","Go left if smaller, right if larger.","Return True if found, False if not."],
                _success("🔍 No BST · ❌ Linear search","🔍 BST built · ✅ O(log n) search","The BST enables fast searching!","Tree Master — BST operations.","Logarithmic search on a tree.",40),
                _reward(diamonds=40,coins=20,badges=["tree-master"],unlocks_town="town-2-graph")),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 10: Graph Forest (graphs)
# ═══════════════════════════════════════════════════════════════
WORLD_GRAPHS = World(
    id="graphs", name="Graph Forest", subtitle="Networks of Connection",
    description="Everything connects to everything. Learn graphs, BFS, DFS, and shortest paths.",
    icon="🌐", order=10, theme="graphs", recommended_roles=["developer", "ai-engineer"], prerequisites=["trees"],
    towns=[
        _make_town("bfs", "BFS Meadow", "🌾", "Breadth-first search explores neighbors level by level.", 1, "Level Exploration", ["graphs.bfs"], ["bfs", "queue", "shortest-path"], [
            _level("g-1","The Meadow","🌾",1,"BFS","Level-by-level","graphs.bfs","graphs.bfs",
                _story("Graph Forest — Meadow","Explorer Emma","Explore the meadow level by level. Visit all neighbors before going deeper."),
                _tutor("Byte","🧭","BFS uses a queue to explore nodes level by level. It finds the shortest path in unweighted graphs.","Like ripples in water — each level is one ripple further."),
                _discover("Graph: A connects to B, C. B connects to D. C connects to E. BFS from A.","bfs-meadow","Visit order","A, B, C, D, E"),
                _manipulate("bfs-queue","Queue-based level exploration","queue"),
                _code("Implement BFS on a simple graph.","graph = {'A':['B','C'],'B':['D'],'C':['E']}\n","from collections import deque\nq = deque(['A'])\nvisited = set()\nwhile q:\n    node = q.popleft()\n    if node in visited: continue\n    visited.add(node)\n    print(node)\n    for neighbor in graph[node]:\n        if neighbor not in visited: q.append(neighbor)"),
                _checks([r"deque",r"popleft",r"visited"]),
                ["Use a queue for BFS.","Visit all neighbors before going deeper.","Track visited nodes to avoid cycles."],
                _success("🌾 No exploration · ❌ Lost","🌾 Meadow explored · ✅ BFS done","The meadow is fully explored level by level!","BFS — breadth-first exploration.","Finds shortest path in unweighted graphs.",20)),
            _level("g-2","The Shortest Path","📏",2,"shortest path","Optimal","graphs.bfs","graphs.bfs",
                _story("Graph Forest — Path","Path Finder Felix","Find the shortest path from A to E in the graph. BFS guarantees the shortest path."),
                _tutor("Byte","🧭","BFS finds the shortest path in unweighted graphs because it explores level by level.","The first time you reach a node, that is the shortest path to it."),
                _discover("Graph: A-B, A-C, B-D, C-E, D-E. Shortest path from A to E?","shortest-path","Shortest path","A → C → E"),
                _manipulate("find-path","Track parent pointers","BFS with path reconstruction"),
                _code("Find the shortest path using BFS.","graph = {'A':['B','C'],'B':['D'],'C':['E'],'D':['E']}\n","from collections import deque\nq = deque([[start]])\nvisited = set()\nwhile q:\n    path = q.popleft()\n    node = path[-1]\n    if node == end: print(path); break\n    if node in visited: continue\n    for n in graph[node]:\n        if n not in visited: q.append(path + [n])\n    return None"),
                _checks([r"path\s*\+",r"node\s*==",r"popleft"]),
                ["Track the path as you BFS.","The first arrival is the shortest.","Use parent pointers or path tracking."],
                _success("📏 No path · ❌ Lost","📏 Shortest path found · ✅ Optimal","The shortest path is guaranteed by BFS!","Shortest Path — BFS optimality.","Level-by-level guarantees shortest.",25)),
            _boss("g-boss","The Network","🌐",3,"graph-master","Connecting","graphs.bfs","graphs.bfs",
                _story("Graph Forest — Network","Network Architect Nora","Map a social network of 100 people. Find the shortest connection chain between any two people."),
                _tutor("Byte","🧭","Real-world networks use BFS for friend suggestions, degrees of separation, and more.","Six degrees of separation — BFS proves it."),
                _discover("Social network: 100 people, connections between them. Find shortest chain from person 1 to 100.","social-network","Shortest chain","7 hops"),
                _manipulate("social-bfs","BFS on social graph","queue + visited"),
                _code("Implement BFS on a social network graph.","graph = {i: [] for i in range(1,101)}\n","# Add connections\nfrom collections import deque\nq = deque([(1, [1])])\nvisited = {1}\nwhile q:\n    node, path = q.popleft()\n    if node == 100: print(f'{len(path)-1} hops'); break\n    for n in graph[node]:\n        if n not in visited:\n            visited.add(n)\n            q.append((n, path+[n]))"),
                _checks([r"deque",r"visited",r"path\s*\+"]),
                ["Model the network as a graph.","BFS finds shortest connection chain.","Track visited to avoid infinite loops."],
                _success("🌐 Network unmapped · ❌ Lost","🌐 Network mapped · ✅ Shortest path found","The social network is fully analyzed!","Graph Master — BFS on real networks.","BFS powers social network analysis.",40),
                _reward(diamonds=40,coins=20,badges=["graph-master"],unlocks_town="town-2-dp")),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 11: Dynamic Delta (dynamic programming)
# ═══════════════════════════════════════════════════════════════
WORLD_DYNAMIC = World(
    id="dynamic", name="Dynamic Delta", subtitle="Optimal Substructure",
    description="Break problems into overlapping sub-problems. Store results to avoid redundant work.",
    icon="📐", order=11, theme="dynamic", recommended_roles=["developer", "ai-engineer"], prerequisites=["graphs"],
    towns=[
        _make_town("memo", "Memoization Marsh", "🧠", "Remember results of expensive computations. Reuse them.", 1, "Caching", ["algorithms.dynamic"], ["memoization", "overlapping", "optimal-substructure"], [
            _level("d-1","The Memo","📝",1,"dynamic programming","Caching","algorithms.dynamic","algorithms.dynamic",
                _story("Dynamic Delta — Marsh","DP Master Dora","Computing Fibonacci naively repeats work. Store results and reuse them."),
                _tutor("Byte","🧭","Memoization stores computed results so you do not recalculate them. It turns exponential into linear.","Like keeping a notebook of answers you have already solved."),
                _discover("Fibonacci: fib(5) = fib(4) + fib(3). Without memo, how many calls?","fib-calls","Number of calls","15"),
                _manipulate("memo-fib","Store computed fib values","cache = {}"),
                _code("Implement Fibonacci with memoization.","def fib(n):\n","cache = {}\ndef fib(n):\n    if n <= 1: return n\n    if n in cache: return cache[n]\n    cache[n] = fib(n-1) + fib(n-2)\n    return cache[n]\nprint(fib(10))"),
                _checks([r"cache\s*=\s*\{\}",r"if\s+n\s+in\s+cache",r"cache\[n\]"]),
                ["Store results in a cache.","Check cache before computing.","Reuse stored results."],
                _success("📝 No memo · 💥 Exponential","📝 Memo built · ✅ Linear","Fibonacci is now O(n)!","Memoization — caching computed results.","Avoid redundant computation.",20)),
            _level("d-2","The Table","📊",2,"tabulation","Bottom-up","algorithms.dynamic","algorithms.dynamic",
                _story("Dynamic Delta — Table","Table Master Tom","Build a table from the bottom up. Start with base cases, fill the table iteratively."),
                _tutor("Byte","🧭","Tabulation is the bottom-up approach to DP. Fill a table iteratively instead of recursing.","No recursion overhead, no stack overflow risk."),
                _discover("Climbing stairs: 1 or 2 steps at a time. How many ways to climb 5 stairs?","stairs-table","Number of ways","8"),
                _manipulate("fill-table","Bottom-up table filling","dp[i] = dp[i-1] + dp[i-2]"),
                _code("Implement climbing stairs with tabulation.","n = 5\n","dp = [0]*(n+1)\ndp[0], dp[1] = 1, 1\nfor i in range(2, n+1):\n    dp[i] = dp[i-1] + dp[i-2]\nprint(dp[n])"),
                _checks([r"dp\s*=\s*\[0\]",r"dp\[i\]\s*=\s*dp",r"range"]),
                ["Initialize base cases.","Fill the table iteratively.","Each entry depends on previous entries."],
                _success("📊 No table · ❌ Recursive overflow","📊 Table filled · ✅ Bottom-up","The table is complete — no recursion needed!","Tabulation — bottom-up DP.","Iterative, no stack risk.",25)),
            _boss("d-boss","The Knapsack","🎒",3,"DP-master","Optimizing","algorithms.dynamic","algorithms.dynamic",
                _story("Dynamic Delta — Vault","Optimization Officer Oscar","You have a knapsack with limited capacity. Choose items to maximize total value. Each item can be taken once."),
                _tutor("Byte","🧭","The 0/1 knapsack is the classic DP problem. For each item, decide: take it or leave it.","Build a 2D table: rows are items, columns are capacities."),
                _discover("Capacity 10. Items: (weight=2,value=6), (weight=3,value=7), (weight=5,value=8), (weight=7,value=9). Max value?","knapsack-opt","Max value","19"),
                _manipulate("knapsack-table","2D DP: take or skip","dp[i][w]"),
                _code("Solve the 0/1 knapsack problem.","weights=[2,3,5,7]\nvalues=[6,7,8,9]\ncapacity=10\n","n = len(weights)\ndp = [[0]*(capacity+1) for _ in range(n+1)]\nfor i in range(1, n+1):\n    for w in range(capacity+1):\n        if weights[i-1] <= w:\n            dp[i][w] = max(dp[i-1][w], values[i-1]+dp[i-1][w-weights[i-1]])\n        else:\n            dp[i][w] = dp[i-1][w]\nprint(dp[n][capacity])"),
                _checks([r"dp\s*=\s*\[\[0\]",r"dp\[i\]\[w\]",r"max\("]),
                ["Build a 2D DP table.","For each item and capacity, decide: take or skip.","The optimal value is in dp[n][capacity]."],
                _success("🎒 No optimization · ❌ Greedy fails","🎒 Knapsack solved · ✅ Optimal","The knapsack is optimally filled!","DP Master — knapsack optimization.","Dynamic programming for combinatorial optimization.",40),
                _reward(diamonds=40,coins=20,badges=["dp-master"],unlocks_town="town-2-alpine")),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════════════
# WORLD 12: Alpine Summit (advanced)
# ═══════════════════════════════════════════════════════════════
WORLD_ALPINE = World(
    id="alpine", name="Alpine Summit", subtitle="Mastery of Algorithms",
    description="The peak of algorithmic knowledge. Combine all skills to solve the hardest problems.",
    icon="🏔️", order=12, theme="alpine", recommended_roles=["developer", "ai-engineer"], prerequisites=["dynamic"],
    towns=[
        _make_town("synthesis", "Synthesis Peak", "🎯", "Combine all data structures and algorithms to solve complex problems.", 1, "Synthesis", ["algorithms.synthesis"], ["synthesis", "integration", "advanced"], [
            _level("a-1","The Synthesis","🧩",1,"algorithm synthesis","Combining","algorithms.synthesis","algorithms.synthesis",
                _story("Alpine Summit — Base","Summit Sage Sera","Combine sorting, searching, and graph algorithms to solve a complex problem."),
                _tutor("Byte","🧭","Real problems require combining multiple algorithms and data structures.","The best developers know when to use which tool."),
                _discover("Given a list of words, find the shortest unique prefix for each word using a trie.","unique-prefix","Prefixes","['d','do','dog','cat']"),
                _manipulate("build-trie","Insert words into trie","prefix"),
                _code("Find shortest unique prefixes for all words.","words = ['dog','cat','car','apple']\n","class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.count = 0\ndef insert(root, word):\n    node = root\n    for c in word:\n        if c not in node.children: node.children[c] = TrieNode()\n        node = node.children[c]\n        node.count += 1\ndef prefix(root, word):\n    node = root\n    p = ''\n    for c in word:\n        p += c\n        node = node.children[c]\n        if node.count == 1: return p\n    return p\nroot = TrieNode()\nfor w in words: insert(root, w)\nprint([prefix(root, w) for w in words])"),
                _checks([r"class\s+TrieNode",r"children",r"count"]),
                ["Build a trie from all words.","Count how many words pass through each node.","The first unique prefix is where count = 1."],
                _success("🧩 No synthesis · ❌ Fragmented","🧩 Synthesis complete · ✅ Unified","All algorithms work together!","Synthesis — combining algorithms.","The whole is greater than the sum of parts.",25)),
            _level("a-2","The Optimization","⚡",2,"advanced optimization","Refining","algorithms.synthesis","algorithms.synthesis",
                _story("Alpine Summit — Ridge","Optimization Officer Oscar","Optimize a solution that uses multiple data structures. Reduce time and space complexity."),
                _tutor("Byte","🧭","Optimization is about choosing the right data structure and algorithm for each sub-problem.","Sometimes a hash table replaces a search. Sometimes a heap replaces sorting."),
                _discover("Optimize: find the top K frequent elements. Use hash map + heap.","top-k","Optimized","O(n log k)"),
                _manipulate("top-k","Hash map for counts, heap for top K","heapq"),
                _code("Find the top K frequent elements efficiently.","nums=[1,1,1,2,2,3]\nk=2\n","from collections import Counter\nimport heapq\ncount = Counter(nums)\nprint(heapq.nlargest(k, count.keys(), key=count.get))"),
                _checks([r"Counter",r"heapq",r"nlargest"]),
                ["Count frequencies with a hash map.","Use a heap to get top K.","O(n log k) instead of O(n log n)."],
                _success("⚡ No optimization · ❌ Slow","⚡ Optimized · ✅ Fast","The solution is optimized!", "Advanced Optimization — choosing the right tools.", "Hash map + heap = efficiency.",30)),
            _boss("a-boss","The Grand Challenge","👑",3,"algo-master","Mastering","algorithms.synthesis","algorithms.synthesis",
                _story("Alpine Summit — Peak","Grand Master Gemini","The ultimate challenge: design a system that combines search, sort, graph, DP, and hashing to solve a real-world problem."),
                _tutor("Byte","🧭","The grand challenge tests everything you have learned. Combine all your tools to solve it.","This is what it means to be a Code Wanderer — mastery of all algorithms."),
                _discover("Design a route planner: shortest path (BFS), sorted results (sort), cached lookups (hash), optimal choices (DP).","grand-challenge","Complete system","All components working"),
                _manipulate("build-system","Combine all algorithms","integrated solution"),
                _code("Implement a route planner combining BFS, sorting, and caching.","graph = {'A':['B','C'],'B':['D'],'C':['D'],'D':[]}\n","from collections import deque\ndef bfs(graph, start, end):\n    q = deque([[start]])\n    visited = set()\n    while q:\n        path = q.popleft()\n        node = path[-1]\n        if node == end: return path\n        if node in visited: continue\n        for n in graph.get(node, []):\n            if n not in visited: q.append(path + [n])\n    return None\ndef shortest_paths(graph, start):\n    return sorted(bfs(graph, start, end) or [], key=len)\nprint(shortest_paths(graph, 'A', 'D'))"),
                _checks([r"deque",r"sorted",r"bfs"]),
                ["BFS for shortest path.","Sort paths by length.","Cache results for repeated queries."],
                _success("👑 Challenge incomplete · ❌ Failed","👑 Challenge complete · ✅ Grand Master","You have mastered all algorithms! The Alpine Summit is yours!","Algorithm Master — the peak of coding knowledge.","All skills combined into mastery.",50),
                _reward(diamonds=50,coins=50,badges=["alpine-master"],title="Grand Master")),
        ]),
    ]
)


# ---- converters + Registry-B merger (was file tail) ----

def _to_level(lesson):
    mastery_step = next((s for s in lesson.steps if s.step_type == "mastery"), None)
    base = dict(
        id=lesson.id,
        title=lesson.title,
        kind=lesson.kind,
        icon=lesson.icon,
        order=lesson.order,
        concept=lesson.concept,
        mental_model=lesson.mental_model,
        canonical_skill=lesson.canonical_skill,
        maps_to_competency=lesson.canonical_skill or None,
        role_relevance=getattr(lesson, "role_relevance", None),
        company_relevance=getattr(lesson, "company_relevance", None),
        story=Story(location=lesson.location or "", npc=lesson.npc or "", line=lesson.npc_line or ""),
        tutor=Tutor(name="Mentor", avatar="🧭", discover=lesson.tutor_discover or "", explain=lesson.tutor_explain or lesson.mental_model or ""),
        discover=Discover(visual="", interaction="", prompt=lesson.mental_model or lesson.title, answer="", values=None),
        manipulate=Manipulate(type="", template="", answer="", blocks=None, hint=lesson.mental_model),
        predict=None,
        build=None,
        break_step=None,
        debug=None,
        code=Code(prompt=lesson.why_this_matters or lesson.title, starter="", placeholder="", language="python"),
        checks=Checks(required_patterns=[], forbidden=[], hint_triggers=[]),
        hints=[step.hint for step in lesson.steps if step.hint],
        retrieval=None,
        transfer=None,
        mastery=mastery_step.title if mastery_step else None,
        mastery_evidence=lesson.mastery_evidence or [],
        mastery_threshold=70 if lesson.kind != "boss" else 80,
        estimated_minutes=lesson.estimated_minutes,
        reward=Reward(diamonds=lesson.diamonds, coins=0, badges=[], unlocks_town=lesson.unlocks or None, unlocks_world=None, title=None),
        success=Success(world_before=None, world_after=None, world_reaction="", reward_text=lesson.why_this_matters or "", byte_line=None, diamonds=lesson.diamonds),
        unlocks=lesson.unlocks or None,
        languages=getattr(lesson, "languages", ["python", "java", "cpp", "c"]),
        starter_code_per_language=getattr(lesson, "starter_code", {}),
        signatures_per_language=getattr(lesson, "signatures", {}),
        test_cases=[],
        hidden_tests=0,
        repair_steps=[],
        passing_score=70,
        max_attempts=3,
        function_name="",
        signature="",
        description="",
        why_this_matters=getattr(lesson, "why_this_matters", ""),
        engineering_context=getattr(lesson, "engineering_context", ""),
        builds_toward=getattr(lesson, "builds_toward", ""),
    )
    if lesson.kind == "boss":
        return Boss(**base)
    return Level(**base)


def _to_world(world_id, wd):
    towns_out = []
    for td in wd.towns:
        levels_out = []
        for lesson in td.lessons:
            levels_out.append(_to_level(lesson))
        towns_out.append(
            Town(
                id=td.id,
                name=td.name,
                icon=td.icon,
                description=td.description,
                order=td.order,
                mental_model=td.mental_model,
                canonical_skills=td.canonical_skills,
                competencies=td.competencies,
                levels=levels_out,
                boss=levels_out[-1] if levels_out and levels_out[-1].kind == "boss" else None,
            )
        )
    return World(
        id=wd.id,
        name=wd.name,
        subtitle=wd.subtitle or "",
        description=wd.description or "",
        icon=wd.icon,
        order=wd.order,
        theme=wd.theme or "",
        recommended_roles=getattr(wd, "recommended_roles", []),
        recommended_companies=getattr(wd, "recommended_companies", []),
        prerequisites=getattr(wd, "prerequisites", []),
        towns=towns_out,
        completion_reward=None,
    )


try:
    from app.content.world1_foundations import WORLD_1_FOUNDATIONS
    from app.content.world2_problem_solver import WORLD_2_PROBLEM_SOLVER
    from app.content.worlds_3_to_12_expanded import (
        WORLD_3_BUILD_SYSTEMS,
        WORLD_4_WORK_WITH_DATA,
        WORLD_5_SOFTWARE_ENGINEERING,
        WORLD_6_UNDER_PRESSURE,
        WORLD_7_HIRING_ARENA,
        WORLD_8_COMPANY_MISSIONS,
        WORLD_9_AI_ENGINEERING,
        WORLD_10_PRODUCTION,
        WORLD_11_PROJECTS,
        WORLD_12_CREATIVE,
    )

    for _wd in [
        WORLD_1_FOUNDATIONS,
        WORLD_2_PROBLEM_SOLVER,
        WORLD_3_BUILD_SYSTEMS,
        WORLD_4_WORK_WITH_DATA,
        WORLD_5_SOFTWARE_ENGINEERING,
        WORLD_6_UNDER_PRESSURE,
        WORLD_7_HIRING_ARENA,
        WORLD_8_COMPANY_MISSIONS,
        WORLD_9_AI_ENGINEERING,
        WORLD_10_PRODUCTION,
        WORLD_11_PROJECTS,
        WORLD_12_CREATIVE,
    ]:
        WORLD_REGISTRY[_wd.id] = _to_world(_wd.id, _wd)
except Exception:
    pass
