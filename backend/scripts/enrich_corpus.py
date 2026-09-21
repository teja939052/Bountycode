"""Enrich Tier 1 concepts in the corpus with worked_examples, misconceptions, and transfer_targets."""
import json
from pathlib import Path

p = Path('app/data/knowledge/corpus.json')
with open(p, 'r', encoding='utf-8') as f:
    corpus = json.load(f)

concepts = corpus['concepts']

# Enrichment data for Tier 1 concepts
enrichments = {
    'c_basics': {
        'worked_examples': [
            {'title': 'Hello World', 'code': '#include <stdio.h>\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}', 'explanation': 'The minimal C program. #include pulls in stdio.h. main() is the entry point. printf prints formatted output. return 0 signals success to the OS.'},
        ],
        'misconceptions': [
            {'misconception': 'C is obsolete', 'correction': 'C powers operating systems, embedded systems, databases, and game engines. Understanding C teaches how computers actually work.', 'evidence': 'Linux kernel, Windows kernel, PostgreSQL, Redis, and most embedded firmware are written in C.'},
            {'misconception': 'C is just C++ without classes', 'correction': 'C and C++ have diverged. C is simpler, more portable, and preferred for systems programming. C++ has RAII, templates, and STL.'},
        ],
        'transfer_targets': ['cpp_basics', 'python_basics', 'os_processes'],
    },
    'c_pointers': {
        'worked_examples': [
            {'title': 'Swap using pointers', 'code': 'void swap(int *a, int *b) {\n    int temp = *a;\n    *a = *b;\n    *b = temp;\n}', 'explanation': 'Parameters are pointers. *a dereferences to access the original variable. Changes through *a affect the caller\'s variable because we have its address.'},
        ],
        'misconceptions': [
            {'misconception': 'Pointers are optional', 'correction': 'Pointers are fundamental to C. Array indexing, pass-by-reference, dynamic memory, and data structures all use pointers.', 'evidence': 'Every array operation, function parameter passing by reference, and malloc/free call involves pointers.'},
            {'misconception': 'Pointer arithmetic is like integer arithmetic', 'correction': 'p + 1 advances by sizeof(*p) bytes, not 1 byte. For int*, p+1 moves 4 bytes. For char*, p+1 moves 1 byte.', 'evidence': 'int arr[5]; int *p = arr; (p+1) - p == 1, but (char*)(p+1) - (char*)p == sizeof(int).'},
        ],
        'transfer_targets': ['c_dynamic_memory', 'c_structures', 'c_arrays'],
    },
    'python_basics': {
        'worked_examples': [
            {'title': 'List comprehension', 'code': 'squares = [x**2 for x in range(10) if x % 2 == 0]', 'explanation': 'Compact loop that builds a list. for x in range(10) iterates. if x % 2 == 0 filters even numbers. x**2 transforms each element.'},
        ],
        'misconceptions': [
            {'misconception': 'Python is slow', 'correction': 'Python is fast enough for most applications. Performance-critical paths use C extensions (NumPy, Pandas). Developer productivity often matters more than raw speed.', 'evidence': 'Instagram, Spotify, and Dropbox use Python for core services.'},
            {'misconception': 'Indentation is just style', 'correction': 'Indentation is syntax in Python. It defines block structure. Mixed tabs/spaces cause errors.', 'evidence': 'Python will raise IndentationError for inconsistent indentation.'},
        ],
        'transfer_targets': ['python_data_structures', 'python_functions', 'python_control_flow'],
    },
    'dsa_arrays': {
        'worked_examples': [
            {'title': 'Two sum with hash map', 'code': 'def two_sum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []', 'explanation': 'Brute force is O(n^2). Hash map reduces to O(n). For each number, check if its complement was seen earlier. seen stores {value: index}.'},
        ],
        'misconceptions': [
            {'misconception': 'Arrays are always O(1) access', 'correction': 'Random access is O(1), but insertion/deletion in middle is O(n) due to shifting.', 'evidence': 'Inserting at index 0 in a 1000-element array requires shifting all 1000 elements.'},
        ],
        'transfer_targets': ['dsa_strings', 'dsa_two_pointers', 'dsa_sliding_window'],
    },
    'dsa_linked_lists': {
        'worked_examples': [
            {'title': 'Reverse linked list', 'code': 'def reverse(head):\n    prev = None\n    curr = head\n    while curr:\n        nxt = curr.next\n        curr.next = prev\n        prev = curr\n        curr = nxt\n    return prev', 'explanation': 'Classic three-pointer technique. prev tracks reversed portion. curr is current node. nxt saves next before we break the link. Advance all three.'},
        ],
        'misconceptions': [
            {'misconception': 'Linked lists are always better than arrays', 'correction': 'Linked lists have O(1) insert/delete at known positions but O(n) search. Arrays have O(1) random access but O(n) middle insertion. Choose based on access pattern.', 'evidence': 'If you need index-based access 90% of the time, array is better despite slower insertions.'},
        ],
        'transfer_targets': ['dsa_stacks', 'dsa_queues', 'dsa_trees'],
    },
    'dsa_trees': {
        'worked_examples': [
            {'title': 'Inorder traversal', 'code': 'def inorder(root):\n    if not root:\n        return\n    inorder(root.left)\n    print(root.val)\n    inorder(root.right)', 'explanation': 'Left subtree, then current node, then right subtree. For BST, this prints values in sorted order.'},
        ],
        'misconceptions': [
            {'misconception': 'All trees are binary trees', 'correction': 'Binary trees have at most 2 children. B-trees, trie, and segment trees have more. Each type has specific use cases.', 'evidence': 'Database indexes use B-trees (many children per node). Autocomplete uses tries (26 children per node).'},
        ],
        'transfer_targets': ['dsa_bst', 'dsa_heaps', 'dsa_tries'],
    },
    'dsa_graphs': {
        'worked_examples': [
            {'title': 'BFS shortest path', 'code': 'from collections import deque\n\ndef shortest_path(graph, start, end):\n    visited = {start}\n    queue = deque([(start, 0)])\n    while queue:\n        node, dist = queue.popleft()\n        if node == end:\n            return dist\n        for neighbor in graph.get(node, []):\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append((neighbor, dist + 1))\n    return -1', 'explanation': 'BFS explores level by level. queue stores (node, distance). When we reach end, dist is shortest path length in unweighted graph.'},
        ],
        'misconceptions': [
            {'misconception': 'DFS always finds shortest path', 'correction': 'DFS explores deeply first. It may find a path but not necessarily the shortest. BFS guarantees shortest path in unweighted graphs.', 'evidence': 'In a graph where shortest path is A->B->C (2 hops) but DFS goes A->D->E->F->C (4 hops), DFS returns longer path.'},
        ],
        'transfer_targets': ['dsa_bfs', 'dsa_dfs', 'dsa_shortest_path'],
    },
    'dsa_dp': {
        'worked_examples': [
            {'title': 'Fibonacci with memoization', 'code': 'from functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef fib(n):\n    if n <= 1:\n        return n\n    return fib(n-1) + fib(n-2)', 'explanation': 'Naive fib is O(2^n). Memoization caches results. lru_cache decorator handles caching automatically. Each fib(n) computed once. Total O(n).'},
        ],
        'misconceptions': [
            {'misconception': 'DP is only for optimization problems', 'correction': 'DP solves any problem with overlapping subproblems and optimal substructure. Counting, decision, and search problems can use DP.', 'evidence': 'Counting paths in grid, determining if string is interleaving of two others, and finding longest common subsequence all use DP.'},
        ],
        'transfer_targets': ['dsa_recursion', 'dsa_backtracking', 'dsa_greedy'],
    },
    'dbms_sql': {
        'worked_examples': [
            {'title': 'Find second highest salary', 'code': 'SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees)', 'explanation': 'Subquery finds highest salary. Outer query finds maximum salary less than that. Result is second highest.'},
        ],
        'misconceptions': [
            {'misconception': 'SQL is just SELECT', 'correction': 'SQL includes DDL (CREATE, ALTER), DML (INSERT, UPDATE, DELETE), DCL (GRANT, REVOKE), and TCL (COMMIT, ROLLBACK).', 'evidence': 'Database administrators spend most of their time on schema design (DDL) and performance tuning, not just SELECT queries.'},
        ],
        'transfer_targets': ['dbms_normalization', 'dbms_indexing', 'sql_basics'],
    },
    'networking_basics': {
        'worked_examples': [
            {'title': 'HTTP request lifecycle', 'code': '# 1. DNS resolution: google.com -> 142.250.80.46\n# 2. TCP handshake: SYN -> SYN-ACK -> ACK\n# 3. HTTP request: GET / HTTP/1.1\n# 4. Server processes and sends response\n# 5. TCP teardown: FIN -> ACK -> FIN -> ACK', 'explanation': 'Every web request follows this flow. DNS translates domain to IP. TCP establishes connection. HTTP sends request. Server responds. Connection closes.'},
        ],
        'misconceptions': [
            {'misconception': 'HTTP is the only web protocol', 'correction': 'HTTP is application layer. Below it: TCP (transport), IP (network), Ethernet (link). Above it: WebSocket, gRPC, GraphQL.', 'evidence': 'WebSocket upgrades HTTP connection for real-time communication. gRPC uses HTTP/2 for RPC calls.'},
        ],
        'transfer_targets': ['networking_tcp', 'networking_http', 'networking_rest'],
    },
    'git_basics': {
        'worked_examples': [
            {'title': 'Feature branch workflow', 'code': '# Start feature\ngit checkout -b feature/user-auth\n# Make changes\ngit add .\ngit commit -m "Add login form"\n# Update with main\ngit pull origin main --rebase\n# Push\ngit push origin feature/user-auth', 'explanation': 'Create branch from main. Make commits. Rebase on latest main to resolve conflicts early. Push for review.'},
        ],
        'misconceptions': [
            {'misconception': 'Git is just backup', 'correction': 'Git is collaboration tool. Branching, merging, and pull requests enable team development. History tells the story of why changes were made.', 'evidence': 'git blame shows who changed each line. git log --graph shows branching and merging patterns.'},
        ],
        'transfer_targets': ['git_branching', 'git_collaboration', 'ci_cd'],
    },
    'docker_basics': {
        'worked_examples': [
            {'title': 'Dockerfile for Python app', 'code': 'FROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD ["python", "app.py"]', 'explanation': 'FROM sets base image. WORKDIR sets working directory. COPY requirements and install. COPY app code. CMD sets default command.'},
        ],
        'misconceptions': [
            {'misconception': 'Docker is lightweight VMs', 'correction': 'Containers share the host kernel. VMs virtualize hardware. Containers are processes with isolation. Faster startup, less overhead.', 'evidence': 'A container starts in milliseconds. A VM takes minutes. A container uses MBs. A VM uses GBs.'},
        ],
        'transfer_targets': ['docker_compose', 'ci_cd', 'linux_basics'],
    },
    'system_design_basics': {
        'worked_examples': [
            {'title': 'URL shortener design', 'code': '# Components:\n# 1. Client -> Load Balancer\n# 2. Load Balancer -> API Servers (stateless)\n# 3. API Servers -> Cache (Redis) for hot URLs\n# 4. API Servers -> Database (PostgreSQL) for persistence\n# 5. Background job -> Cleanup expired URLs', 'explanation': 'Stateless API servers scale horizontally. Cache reduces database load for hot URLs. Database persists mappings. Background job handles cleanup.'},
        ],
        'misconceptions': [
            {'misconception': 'System design is about technology choices', 'correction': 'System design is about trade-offs. Every choice has costs. CAP theorem: pick 2 of 3. There are no perfect solutions, only appropriate ones.', 'evidence': 'Choosing consistency over availability means some users see errors during partitions. Choosing availability means some users see stale data.'},
        ],
        'transfer_targets': ['system_design_scalability', 'system_design_caching', 'networking_rest'],
    },
}

for cid, data in enrichments.items():
    if cid in concepts:
        concepts[cid]['worked_examples'] = data.get('worked_examples', [])
        concepts[cid]['misconceptions'] = data.get('misconceptions', [])
        concepts[cid]['transfer_targets'] = data.get('transfer_targets', [])
        concepts[cid]['content_status'] = 'enriched'
        if data.get('misconceptions'):
            concepts[cid]['verification'] = {
                'sources': concepts[cid].get('source_references', []),
                'last_verified': '2026-09-15',
                'verified_by': 'corpus_enrichment',
                'verification_notes': f"Enriched with {len(data.get('worked_examples', []))} worked examples, {len(data.get('misconceptions', []))} misconceptions, {len(data.get('transfer_targets', []))} transfer targets."
            }
        print(f"Enriched: {cid}")
    else:
        print(f"SKIP (not found): {cid}")

with open(p, 'w', encoding='utf-8') as f:
    json.dump(corpus, f, indent=2, default=str)

enriched_count = len([c for c in concepts.values() if c.get('content_status') == 'enriched'])
print(f"\nTotal enriched: {enriched_count}")
print("Done.")
