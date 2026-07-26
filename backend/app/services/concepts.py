"""
Concept cards for the Learning Engine.
Each concept includes: explanation, visualization, code examples, and practice problems.
"""

CONCEPT_CARDS = {
    "Arrays": {
        "title": "Arrays — The Foundation",
        "duration_minutes": 5,
        "video_url": "https://www.youtube.com/results?search_query=array+data+structure+explained+takeuforward",
        "content": {
            "what": "An array is a collection of elements stored at contiguous memory locations. Each element can be accessed directly using its index.",
            "why": "Arrays are the most basic data structure and form the building blocks for more complex structures like stacks, queues, and hash maps.",
            "when_to_use": [
                "When you need O(1) access to elements by index",
                "When the size of data is known in advance",
                "When you need to iterate through all elements"
            ],
            "key_operations": [
                {"operation": "Access", "time": "O(1)", "description": "arr[i] returns element at index i"},
                {"operation": "Search", "time": "O(n)", "description": "Find element by value"},
                {"operation": "Insert (end)", "time": "O(1)", "description": "Add element at the end"},
                {"operation": "Insert (middle)", "time": "O(n)", "description": "Shift elements to make space"},
                {"operation": "Delete", "time": "O(n)", "description": "Remove and shift elements"}
            ],
            "visualization": {
                "type": "array",
                "data": [10, 20, 30, 40, 50],
                "indices": [0, 1, 2, 3, 4],
                "operations": ["Access arr[2] → 30", "Search for 40 → index 3", "Insert 25 at index 2 → shift right"]
            },
            "code_examples": {
                "python": """
# Array basics
arr = [10, 20, 30, 40, 50]

# Access
print(arr[0])  # 10
print(arr[2])  # 30

# Search
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

# Insert at position
def insert(arr, pos, val):
    arr.append(0)
    for i in range(len(arr) - 1, pos, -1):
        arr[i] = arr[i - 1]
    arr[pos] = val

# Two Pointer Technique
def two_sum(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        current = arr[left] + arr[right]
        if current == target:
            return [left, right]
        elif current < target:
            left += 1
        else:
            right -= 1
    return [-1, -1]
""",
                "java": """
// Array basics
int[] arr = {10, 20, 30, 40, 50};

// Access
System.out.println(arr[0]);  // 10
System.out.println(arr[2]);  // 30

// Two Pointer
int[] twoSum(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left < right) {
        int current = arr[left] + arr[right];
        if (current == target) return new int[]{left, right};
        else if (current < target) left++;
        else right--;
    }
    return new int[]{-1, -1};
}
""",
                "cpp": """
// Array basics
int arr[] = {10, 20, 30, 40, 50};

// Access
cout << arr[0] << endl;  // 10
cout << arr[2] << endl;  // 30

// Two Pointer
vector<int> twoSum(vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    while (left < right) {
        int current = arr[left] + arr[right];
        if (current == target) return {left, right};
        else if (current < target) left++;
        else right--;
    }
    return {-1, -1};
}
"""
            },
            "patterns": [
                {"name": "Two Pointers", "description": "Use two pointers moving towards each other", "problems": ["Two Sum", "Container With Most Water", "3Sum"]},
                {"name": "Sliding Window", "description": "Maintain a window of elements and slide it", "problems": ["Maximum Subarray", "Longest Substring Without Repeating"]},
                {"name": "Prefix Sum", "description": "Precompute prefix sums for range queries", "problems": ["Subarray Sum Equals K", "Range Sum Query"]}
            ],
            "common_mistakes": [
                "Off-by-one errors (accessing arr[n] when size is n)",
                "Not handling empty arrays",
                "Modifying array while iterating"
            ]
        }
    },

    "Linked Lists": {
        "title": "Linked Lists — Dynamic Connections",
        "duration_minutes": 5,
        "video_url": "https://www.youtube.com/results?search_query=linked+list+explained+takeuforward",
        "content": {
            "what": "A linked list is a linear data structure where elements are stored in nodes. Each node contains data and a pointer to the next node.",
            "why": "Linked lists allow O(1) insertion/deletion at any position (given a pointer), unlike arrays which require shifting.",
            "when_to_use": [
                "When you need frequent insertions/deletions",
                "When the size is unknown or changes frequently",
                "When you need to implement stacks, queues, or graphs"
            ],
            "key_operations": [
                {"operation": "Insert at head", "time": "O(1)", "description": "Add node at the beginning"},
                {"operation": "Insert at tail", "time": "O(n)", "description": "Add node at the end"},
                {"operation": "Delete", "time": "O(1)", "description": "Remove node (given pointer)"},
                {"operation": "Search", "time": "O(n)", "description": "Find node by value"},
                {"operation": "Access by index", "time": "O(n)", "description": "Must traverse from head"}
            ],
            "visualization": {
                "type": "linked_list",
                "nodes": [1, 2, 3, 4, 5],
                "arrows": ["→", "→", "→", "→", "null"]
            },
            "code_examples": {
                "python": """
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Reverse a linked list
def reverseList(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev

# Detect cycle (Floyd's)
def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

# Merge two sorted lists
def mergeTwoLists(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next
"""
            },
            "patterns": [
                {"name": "Two Pointers", "description": "Slow and fast pointers for cycle detection, middle finding", "problems": ["Detect Cycle", "Find Middle", "Remove Nth From End"]},
                {"name": "Dummy Node", "description": "Use a dummy head to simplify edge cases", "problems": ["Merge Two Lists", "Add Two Numbers", "Partition List"]},
                {"name": "Reversal", "description": "Reverse links between nodes", "problems": ["Reverse List", "Reverse in k-Group", "Reverse Between"]}
            ],
            "common_mistakes": [
                "Losing reference to the rest of the list",
                "Not handling empty list edge cases",
                "Infinite loops from broken links"
            ]
        }
    },

    "Dynamic Programming": {
        "title": "Dynamic Programming — Optimal Substructure",
        "duration_minutes": 8,
        "video_url": "https://www.youtube.com/results?search_query=dynamic+programming+explained+takeuforward",
        "content": {
            "what": "Dynamic Programming is an optimization technique that solves complex problems by breaking them into overlapping subproblems and storing their solutions.",
            "why": "DP transforms exponential-time recursive solutions into polynomial-time solutions by avoiding redundant calculations.",
            "when_to_use": [
                "When the problem has overlapping subproblems",
                "When the problem has optimal substructure",
                "When brute force is too slow (exponential time)"
            ],
            "key_operations": [
                {"operation": "Top-Down (Memoization)", "time": "O(n)", "description": "Recursive + cache"},
                {"operation": "Bottom-Up (Tabulation)", "time": "O(n)", "description": "Iterative table filling"},
                {"operation": "Space Optimization", "time": "O(1)", "description": "Reduce space using variables"}
            ],
            "visualization": {
                "type": "dp_table",
                "example": "Fibonacci: dp[0]=0, dp[1]=1, dp[2]=1, dp[3]=2, dp[4]=3, dp[5]=5"
            },
            "code_examples": {
                "python": """
# Fibonacci - Three Approaches

# 1. Brute Force (O(2^n) - DON'T DO THIS)
def fib_brute(n):
    if n <= 1: return n
    return fib_brute(n-1) + fib_brute(n-2)

# 2. Top-Down with Memoization (O(n) time, O(n) space)
def fib_memo(n, memo={}):
    if n in memo: return memo[n]
    if n <= 1: return n
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]

# 3. Bottom-Up with Tabulation (O(n) time, O(n) space)
def fib_tab(n):
    if n <= 1: return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

# 4. Space Optimized (O(n) time, O(1) space)
def fib_optimized(n):
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Classic DP Pattern: 0/1 Knapsack
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(
                    values[i-1] + dp[i-1][w-weights[i-1]],
                    dp[i-1][w]
                )
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][capacity]
"""
            },
            "patterns": [
                {"name": "Linear DP", "description": "dp[i] depends on dp[i-1], dp[i-2]", "problems": ["Climbing Stairs", "House Robber", "Coin Change"]},
                {"name": "Grid DP", "description": "dp[i][j] depends on neighbors", "problems": ["Unique Paths", "Minimum Path Sum", "Grid Unique Paths"]},
                {"name": "Knapsack", "description": "Include/exclude items", "problems": ["0/1 Knapsack", "Subset Sum", "Partition Equal Subset"]},
                {"name": "String DP", "description": "dp[i][j] for string comparison", "problems": ["Longest Common Subsequence", "Edit Distance", "Longest Palindromic Subsequence"]}
            ],
            "common_mistakes": [
                "Not identifying the right state definition",
                "Off-by-one errors in base cases",
                "Not considering all transitions"
            ]
        }
    },

    "Trees": {
        "title": "Binary Trees — Hierarchical Structure",
        "duration_minutes": 6,
        "video_url": "https://www.youtube.com/results?search_query=binary+tree+explained+takeuforward",
        "content": {
            "what": "A binary tree is a hierarchical data structure where each node has at most two children (left and right).",
            "why": "Trees enable efficient searching (BST), hierarchical data representation, and are the foundation for many algorithms.",
            "when_to_use": [
                "When data has hierarchical relationships",
                "For efficient searching (BST gives O(log n))",
                "For representing file systems, DOM, etc."
            ],
            "key_operations": [
                {"operation": "Inorder (Left-Root-Right)", "time": "O(n)", "description": "Gives sorted order for BST"},
                {"operation": "Preorder (Root-Left-Right)", "time": "O(n)", "description": "Used for tree construction"},
                {"operation": "Postorder (Left-Right-Root)", "time": "O(n)", "description": "Used for deletion"},
                {"operation": "Level Order (BFS)", "time": "O(n)", "description": "Level by level traversal"}
            ],
            "visualization": {
                "type": "binary_tree",
                "nodes": [1, 2, 3, 4, 5, 6, 7],
                "structure": "1 → (2,3) → (4,5,6,7)"
            },
            "code_examples": {
                "python": """
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Inorder Traversal (Iterative)
def inorderTraversal(root):
    result = []
    stack = []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right
    return result

# Level Order Traversal (BFS)
from collections import deque
def levelOrder(root):
    if not root: return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result

# Maximum Depth
def maxDepth(root):
    if not root: return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))

# Lowest Common Ancestor
def lowestCommonAncestor(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right: return root
    return left or right
"""
            },
            "patterns": [
                {"name": "DFS (Recursive)", "description": "Explore as deep as possible first", "problems": ["Max Depth", "Validate BST", "Path Sum"]},
                {"name": "BFS (Level Order)", "description": "Explore level by level", "problems": ["Level Order", "Right Side View", "Zigzag Traversal"]},
                {"name": "Tree Construction", "description": "Build tree from traversals", "problems": ["Construct from Preorder+Inorder", "Serialize/Deserialize"]}
            ],
            "common_mistakes": [
                "Forgetting base case (null node)",
                "Not handling single-node trees",
                "Confusing preorder/inorder/postorder"
            ]
        }
    },

    "Graphs": {
        "title": "Graphs — Connected World",
        "duration_minutes": 7,
        "video_url": "https://www.youtube.com/results?search_query=graph+theory+explained+takeuforward",
        "content": {
            "what": "A graph is a collection of vertices (nodes) connected by edges. Graphs can be directed/undirected, weighted/unweighted.",
            "why": "Graphs model relationships — social networks, maps, dependencies, networks. Most real-world problems involve graphs.",
            "when_to_use": [
                "When relationships between entities matter",
                "For shortest path problems",
                "For connectivity and cycle detection"
            ],
            "key_operations": [
                {"operation": "BFS", "time": "O(V+E)", "description": "Level-by-level traversal"},
                {"operation": "DFS", "time": "O(V+E)", "description": "Deep-first traversal"},
                {"operation": "Dijkstra", "time": "O((V+E)logV)", "description": "Shortest path in weighted graph"},
                {"operation": "Topological Sort", "time": "O(V+E)", "description": "Linear ordering of DAG"}
            ],
            "code_examples": {
                "python": """
from collections import deque, defaultdict

# BFS - Shortest Path in Unweighted Graph
def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order

# DFS - Cycle Detection in Undirected Graph
def hasCycle(graph, V):
    visited = [False] * V
    def dfs(node, parent):
        visited[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True
        return False
    for i in range(V):
        if not visited[i]:
            if dfs(i, -1):
                return True
    return False

# Topological Sort (Kahn's Algorithm)
def topologicalSort(V, adj):
    in_degree = [0] * V
    for i in range(V):
        for neighbor in adj[i]:
            in_degree[neighbor] += 1
    queue = deque([i for i in range(V) if in_degree[i] == 0])
    result = []
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return result

# Dijkstra's Shortest Path
import heapq
def dijkstra(graph, V, src):
    dist = [float('inf')] * V
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]: continue
        for neighbor, weight in graph[node]:
            if dist[node] + weight < dist[neighbor]:
                dist[neighbor] = dist[node] + weight
                heapq.heappush(heap, (dist[neighbor], neighbor))
    return dist
"""
            },
            "patterns": [
                {"name": "BFS", "description": "Level-by-level, shortest path in unweighted", "problems": ["Number of Islands", "Rotting Oranges", "BFS of Graph"]},
                {"name": "DFS", "description": "Deep-first, cycle detection, connectivity", "problems": ["Detect Cycle", "Clone Graph", "Topological Sort"]},
                {"name": "Shortest Path", "description": "Dijkstra, Bellman-Ford, Floyd-Warshall", "problems": ["Dijkstra", "Shortest Path in Weighted Graph"]}
            ],
            "common_mistakes": [
                "Not marking nodes as visited (infinite loops)",
                "Confusing directed vs undirected graphs",
                "Forgetting to handle disconnected components"
            ]
        }
    }
}


def get_concept_card(topic):
    """Get a concept card for a given topic."""
    # Try exact match first
    if topic in CONCEPT_CARDS:
        return CONCEPT_CARDS[topic]

    # Try partial match
    for key in CONCEPT_CARDS:
        if topic.lower() in key.lower() or key.lower() in topic.lower():
            return CONCEPT_CARDS[key]

    return None


def get_available_concepts():
    """Get list of available concept cards."""
    return [
        {
            "topic": topic,
            "title": card["title"],
            "duration_minutes": card["duration_minutes"],
        }
        for topic, card in CONCEPT_CARDS.items()
    ]
