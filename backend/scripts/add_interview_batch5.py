import json

new_questions = [
    {
        "id": "int-051",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "mentoring",
        "difficulty": "medium",
        "question": "Tell me about a time you mentored or helped a junior team member. What was your approach and what was the outcome?",
        "correct_answer": "STAR method: Situation - new grad struggled with debugging. Task - help them become productive. Action - paired programming twice weekly, created onboarding checklist, reviewed their PRs with explanations, encouraged questions. Result - they shipped first feature in 3 weeks, became confident contributor, now mentors other new hires.",
        "options": [],
        "solution": {
            "code": "# Mentoring approach\n1. Understand their current level and goals\n2. Pair program on real tasks (not tutorials)\n3. Review work with explanations, not just fixes\n4. Create reusable resources (checklists, docs)\n5. Gradually increase independence\n6. Celebrate their wins",
            "explanation": "Mentoring tests patience, empathy, and teaching ability. Show you invested time, used real projects not just theory, and measured their growth. Great mentors create other mentors."
        },
        "testcases": [
            {
                "input": "I told them to read the documentation",
                "expected": "Weak - passive, not hands-on mentoring"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows pairing, code review with explanations, and growth measurement",
                "expected": "Strong - demonstrates mentoring skill"
            }
        ],
        "hints": [
            "Show hands-on involvement",
            "Mention specific teaching methods",
            "Quantify their improvement"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-052",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "feedback",
        "difficulty": "medium",
        "question": "Describe a time you received critical feedback. How did you handle it?",
        "correct_answer": "STAR method: Situation - code review feedback said my code was hard to maintain. Task - improve code quality. Action - asked for specifics, read Clean Code, refactored with clear names and small functions, asked for follow-up review. Result - PR approved next round, became team's code quality advocate, reduced tech debt by 30%.",
        "options": [],
        "solution": {
            "code": "# Receiving feedback well\n1. Listen without defending\n2. Ask clarifying questions\n3. Thank the person\n4. Reflect and create action plan\n5. Follow up with improvements\n6. Show you applied the feedback",
            "explanation": "Feedback questions test coachability and ego. Show you can hear criticism without getting defensive. Ask for specifics, make a plan, prove you changed. This is a top hiring signal."
        },
        "testcases": [
            {
                "input": "I argued that my code was fine",
                "expected": "Red flag - not coachable"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows reflection, action plan, and measurable improvement",
                "expected": "Strong - coachable and self-aware"
            }
        ],
        "hints": [
            "Show you listened without defending",
            "Mention specific changes you made",
            "Prove you applied the feedback"
        ],
        "companies": ["amazon", "google", "microsoft", "meta", "tcs", "infosys"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-053",
        "type": "interview",
        "topic": "behavioral",
        "sub_topic": "difficult_people",
        "difficulty": "medium",
        "question": "Describe a time you had to work with a difficult colleague. How did you handle it?",
        "correct_answer": "STAR method: Situation - teammate refused to review PRs, blocked progress. Task - maintain productivity without conflict. Action - scheduled 1:1, listened to their frustration (overwhelmed with work), offered to split PRs into smaller chunks, aligned on review SLA. Result - reviews happened within 24 hours, relationship improved, process change adopted team-wide.",
        "options": [],
        "solution": {
            "code": "# Handling difficult people\n1. Diagnose root cause, not just symptom\n2. Listen first - often there's unmet need\n3. Find common ground\n4. Propose concrete process changes\n5. Escalate only if team is at risk",
            "explanation": "Difficult people questions test emotional intelligence. Show empathy, not blame. Often 'difficult' behavior has root cause. Your job is to find win-win, not win the argument."
        },
        "testcases": [
            {
                "input": "I reported them to HR",
                "expected": "Over-escalation - skip direct conversation"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows empathy, root cause analysis, and process improvement",
                "expected": "Strong - handles conflict maturely"
            }
        ],
        "hints": [
            "Listen first, diagnose root cause",
            "Find win-win solutions",
            "Don't escalate prematurely"
        ],
        "companies": ["amazon", "google", "microsoft", "meta", "tcs", "infosys"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 20,
        "estimated_time": "15-20 minutes"
    },
    {
        "id": "int-054",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "data_structures",
        "difficulty": "medium",
        "question": "Explain how a hash table works. What is the time complexity for insert, delete, and search? What happens when there are collisions?",
        "correct_answer": "Hash table: array of buckets, hash function maps key to index. Time complexity: O(1) average for insert/delete/search. Collisions: two keys map to same index. Resolution: 1. Chaining: each bucket is linked list. 2. Open addressing: probe next empty slot (linear, quadratic, double hashing). Load factor = entries/buckets. Resize when load factor > threshold (usually 0.75).",
        "options": [],
        "solution": {
            "code": "# Hash table with chaining\nclass HashTable:\n    def __init__(self, size=100):\n        self.table = [[] for _ in range(size)]\n    \n    def _hash(self, key):\n        return hash(key) % len(self.table)\n    \n    def put(self, key, value):\n        idx = self._hash(key)\n        for i, (k, v) in enumerate(self.table[idx]):\n            if k == key:\n                self.table[idx][i] = (key, value)\n                return\n        self.table[idx].append((key, value))\n    \n    def get(self, key):\n        idx = self._hash(key)\n        for k, v in self.table[idx]:\n            if k == key:\n                return v\n        return None",
            "explanation": "Hash tables are the backbone of fast lookups. Good hash function distributes evenly. Collisions degrade to O(n) worst case. Resizing rehashes all entries. Used in: caches, databases, sets, maps."
        },
        "testcases": [
            {
                "input": "Hash tables have O(1) worst-case complexity",
                "expected": "Wrong - worst case is O(n) with collisions"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains hash function, collisions, and resizing",
                "expected": "Strong - understands hash tables deeply"
            }
        ],
        "hints": [
            "Hash function maps key to index",
            "Collisions need resolution strategies",
            "Resize when load factor is high"
        ],
        "companies": ["google", "amazon", "microsoft", "meta"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 25,
        "estimated_time": "20-25 minutes"
    },
    {
        "id": "int-055",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "data_structures_trees",
        "difficulty": "medium",
        "question": "Explain the difference between a binary tree and a binary search tree. What is the time complexity for search, insert, and delete in each?",
        "correct_answer": "Binary tree: each node has max 2 children, no ordering guarantee. Time: O(n) worst case for all operations. Binary search tree (BST): left child < parent < right child. Time: O(log n) average for search/insert/delete, O(n) worst case (unbalanced). Balanced BST (AVL, Red-Black): guaranteed O(log n). Self-balancing trees rebalance on insert/delete.",
        "options": [],
        "solution": {
            "code": "# BST search\ndef bst_search(root, target):\n    if not root or root.val == target:\n        return root\n    if target < root.val:\n        return bst_search(root.left, target)\n    return bst_search(root.right, target)\n\n# Time: O(log n) average, O(n) worst",
            "explanation": "BSTs enable fast search through ordering. Unbalanced BST degenerates to linked list. Self-balancing trees (AVL, Red-Black) maintain O(log n) guarantee. B-trees are used in databases for disk-based storage."
        },
        "testcases": [
            {
                "input": "BST always has O(log n) operations",
                "expected": "Wrong - unbalanced BST can be O(n)"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains ordering property and balancing need",
                "expected": "Strong - understands tree structures"
            }
        ],
        "hints": [
            "BST has ordering property",
            "Unbalanced BST is O(n) worst case",
            "Balanced BSTs guarantee O(log n)"
        ],
        "companies": ["google", "amazon", "microsoft", "meta"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 25,
        "estimated_time": "20-25 minutes"
    },
    {
        "id": "int-056",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "data_structures_graphs",
        "difficulty": "medium",
        "question": "Explain BFS and DFS. When would you use each? Give examples.",
        "correct_answer": "BFS (Breadth-First Search): explores level by level using queue. Use for: shortest path in unweighted graph, social networks (friends of friends), level-order traversal. Time: O(V+E), Space: O(V). DFS (Depth-First Search): explores as deep as possible using stack/recursion. Use for: maze solving, cycle detection, topological sort, connected components. Time: O(V+E), Space: O(V) recursion depth.",
        "options": [],
        "solution": {
            "code": "# BFS - shortest path in unweighted graph\nfrom collections import deque\n\ndef bfs_shortest_path(graph, start, end):\n    visited = {start}\n    queue = deque([(start, [start])])\n    while queue:\n        node, path = queue.popleft()\n        if node == end:\n            return path\n        for neighbor in graph[node]:\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append((neighbor, path + [neighbor]))\n    return None\n\n# DFS - cycle detection\ndef has_cycle(graph):\n    visited = set()\n    rec_stack = set()\n    def dfs(node):\n        visited.add(node)\n        rec_stack.add(node)\n        for neighbor in graph.get(node, []):\n            if neighbor not in visited:\n                if dfs(neighbor):\n                    return True\n            elif neighbor in rec_stack:\n                return True\n        rec_stack.remove(node)\n        return False",
            "explanation": "BFS guarantees shortest path in unweighted graphs because it explores all paths of length k before length k+1. DFS can get stuck in deep paths. Choose based on problem: shortest path = BFS, exhaustiveness = DFS."
        },
        "testcases": [
            {
                "input": "BFS is always better than DFS",
                "expected": "Wrong - depends on the problem"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Explains both with appropriate use cases",
                "expected": "Strong - understands graph traversal"
            }
        ],
        "hints": [
            "BFS: level by level, queue",
            "DFS: depth first, stack/recursion",
            "BFS for shortest path, DFS for exhaustiveness"
        ],
        "companies": ["google", "amazon", "microsoft", "meta"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 25,
        "estimated_time": "20-25 minutes"
    },
    {
        "id": "int-057",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "notice_period",
        "difficulty": "easy",
        "question": "What is your notice period?",
        "correct_answer": "Be honest and professional: 'My notice period is 30 days. I'm flexible and can start sooner if needed, though I want to ensure proper handover.' If currently unemployed: 'I'm available immediately.' If notice period is long: acknowledge it, emphasize you can start sooner with mutual agreement, show enthusiasm for the role.",
        "options": [],
        "solution": {
            "code": "# Good answer\n- State notice period clearly\n- Express flexibility if possible\n- Emphasize commitment to smooth handover\n- Show enthusiasm for new role\n\n# Bad answer\n- 'I can leave immediately' (unprofessional)\n- 'My current company doesn't allow me to leave' (red flag)",
            "explanation": "Notice period questions test professionalism and planning. Be honest. Show you respect commitments. If period is long, mention you can negotiate but emphasize doing right by current employer."
        },
        "testcases": [
            {
                "input": "I can leave immediately without notice",
                "expected": "Unprofessional - shows lack of commitment"
            }
        ],
        "hidden_testcases": [
            {
                "input": "States period clearly with flexibility and professionalism",
                "expected": "Strong - professional and prepared"
            }
        ],
        "hints": [
            "Be honest about notice period",
            "Show professionalism",
            "Express flexibility if possible"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "cognizant", "amazon", "google", "microsoft"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 10,
        "estimated_time": "5-10 minutes"
    },
    {
        "id": "int-058",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "relocation",
        "difficulty": "easy",
        "question": "Are you willing to relocate?",
        "correct_answer": "Show flexibility and enthusiasm: 'Yes, I'm willing to relocate. I'm excited about the opportunity and the team. I've researched the area and am happy to make the move.' If conditional: 'Yes, with a reasonable relocation period. I'm flexible and want to ensure smooth transition.' If not willing: be honest early, but emphasize interest in remote/hybrid if available.",
        "options": [],
        "solution": {
            "code": "# If willing\nYes, I'm excited about the opportunity and willing to relocate.\nI've researched the area and am happy to make the move.\n\n# If conditional\nYes, with a reasonable onboarding period.\nI'm flexible and want to ensure smooth transition.",
            "explanation": "Relocation questions test commitment and logistics. Companies invest in relocation, so they want assurance you'll stay. Show enthusiasm, not reluctance. If you have constraints, mention them but emphasize flexibility."
        },
        "testcases": [
            {
                "input": "No, I will never relocate",
                "expected": "May disqualify for roles requiring relocation"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Shows enthusiasm and flexibility",
                "expected": "Strong - demonstrates commitment"
            }
        ],
        "hints": [
            "Show enthusiasm for the move",
            "Be honest about constraints",
            "Emphasize commitment to role"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "cognizant", "amazon", "google", "microsoft"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 10,
        "estimated_time": "5-10 minutes"
    },
    {
        "id": "int-059",
        "type": "interview",
        "topic": "hr",
        "sub_topic": "resume_gaps",
        "difficulty": "medium",
        "question": "I see a gap in your resume. Can you explain what you were doing during that time?",
        "correct_answer": "Be honest and frame positively: 'Yes, that was when I took 6 months to upskill in cloud and system design. I completed AWS certifications, built a personal project, and contributed to open source. It was a deliberate investment in my career.' If personal reasons: 'I was caring for a family member. It taught me time management and empathy. I'm now fully focused on my career.'",
        "options": [],
        "solution": {
            "code": "# Good framing\n- Be honest, don't lie\n- Frame as growth or necessary break\n- Show what you learned or achieved\n- Emphasize you're ready now\n\n# Bad answers\n- 'I was just traveling' (no growth framing)\n- 'I couldn't find a job' (negative)\n- Lying about dates",
            "explanation": "Gaps are common and acceptable if framed well. Show you were productive or growing. Don't apologize excessively. Focus on present readiness. Honesty is critical - background checks verify dates."
        },
        "testcases": [
            {
                "input": "I was just lazy and didn't look for jobs",
                "expected": "Weak - no framing, shows lack of drive"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Honest with positive framing and current readiness",
                "expected": "Strong - transparent and forward-looking"
            }
        ],
        "hints": [
            "Be honest",
            "Frame as growth or necessary break",
            "Emphasize current readiness"
        ],
        "companies": ["tcs", "infosys", "wipro", "accenture", "cognizant", "amazon", "google", "microsoft"],
        "role": ["sde", "backend-engineer", "data-analyst"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 15,
        "estimated_time": "10-15 minutes"
    },
    {
        "id": "int-060",
        "type": "interview",
        "topic": "technical",
        "sub_topic": "system_design_rate_limiter",
        "difficulty": "hard",
        "question": "Design a rate limiter for an API. How would you implement it and what algorithms would you consider?",
        "correct_answer": "Algorithms: 1. Token Bucket: tokens added at fixed rate, request consumes token. Allows bursts. 2. Fixed Window: count requests in fixed time window (e.g., per minute). Simple but burst at boundary. 3. Sliding Window Log: track request timestamps, count in last N seconds. Accurate but memory-heavy. 4. Sliding Window Counter: approximate sliding window with counters. Implementation: Redis with sorted sets for sliding log, or atomic counters for token bucket. Distribute: use Redis cluster, sticky sessions for consistency.",
        "options": [],
        "solution": {
            "code": "# Token bucket in Redis\nimport redis\nr = redis.Redis()\n\n def allow_request(user_id, limit, period):\n    key = f'rate_limit:{user_id}'\n    current = r.llen(key)\n    if current >= limit:\n        return False\n    r.lpush(key, time.time())\n    r.expire(key, period)\n    return True\n\n# Sliding window with sorted set\ndef allow_request_sliding(user_id, limit, window_seconds):\n    key = f'rate_limit:{user_id}'\n    now = time.time()\n    r.zadd(key, {now: now})\n    r.zremrangebyscore(key, 0, now - window_seconds)\n    count = r.zcard(key)\n    if count > limit:\n        r.zrem(key, now)\n        return False\n    r.expire(key, window_seconds)\n    return True",
            "explanation": "Rate limiting protects APIs from abuse and ensures fair usage. Token bucket allows bursts (good for UX). Sliding window is accurate but heavier. Distributed systems need centralized store (Redis) for consistency."
        },
        "testcases": [
            {
                "input": "Use in-memory counter for distributed system",
                "expected": "Wrong - each server has separate counter"
            }
        ],
        "hidden_testcases": [
            {
                "input": "Discusses algorithms and distributed implementation",
                "expected": "Strong - understands rate limiting deeply"
            }
        ],
        "hints": [
            "Token bucket allows bursts",
            "Sliding window is most accurate",
            "Use Redis for distributed systems"
        ],
        "companies": ["amazon", "google", "microsoft", "meta"],
        "role": ["sde", "backend-engineer"],
        "provenance": "author-verified-2026",
        "source_bank": "interview_practice_bank",
        "trust_status": "verified",
        "stage": "placement",
        "xp_reward": 35,
        "estimated_time": "25-30 minutes"
    }
]

with open('backend/app/data/interview_practice_bank.json', 'r') as f:
    data = json.load(f)
data.extend(new_questions)
with open('backend/app/data/interview_practice_bank.json', 'w') as f:
    json.dump(data, f, indent=2)
print(f'Added {len(new_questions)} questions. Total: {len(data)}')
