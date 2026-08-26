#!/usr/bin/env python3
"""
Massive DSA Question Generator - LeetCode-style expansion
Generates 3000+ coding problems with test cases, solutions, and metadata
"""
import json
import random
from typing import List, Dict, Any
from dataclasses import dataclass, asdict

# ============================================================
# TOPIC & DIFFICULTY DISTRIBUTION (LeetCode-style)
# ============================================================
TOPICS = {
    "arrays": 450,
    "strings": 300,
    "linked-lists": 200,
    "trees": 350,
    "graphs": 300,
    "dynamic-programming": 400,
    "stacks-queues": 150,
    "heaps": 100,
    "tries": 50,
    "backtracking": 150,
    "bit-manipulation": 100,
    "math": 150,
    "greedy": 100,
    "sliding-window": 100,
    "two-pointers": 150,
    "binary-search": 150,
    "prefix-sum": 50,
    "intervals": 50,
    "monotonic-stack": 50,
    "union-find": 50,
}

DIFFICULTY_DIST = {"easy": 0.4, "medium": 0.45, "hard": 0.15}

COMPANIES = [
    "Google", "Amazon", "Microsoft", "Meta", "Apple", "Netflix", "Uber", "Airbnb",
    "LinkedIn", "Twitter", "Stripe", "Databricks", "Snowflake", "Palantir",
    "TCS", "Infosys", "Wipro", "Cognizant", "Accenture", "Capgemini"
]

COMPANY_WEIGHTS = {
    "Google": 8, "Amazon": 8, "Microsoft": 7, "Meta": 7, "Apple": 6,
    "Netflix": 5, "Uber": 5, "Airbnb": 5, "LinkedIn": 4, "Twitter": 4,
    "Stripe": 4, "Databricks": 3, "Snowflake": 3, "Palantir": 3,
    "TCS": 6, "Infosys": 6, "Wipro": 5, "Cognizant": 5, "Accenture": 4, "Capgemini": 4
}

# ============================================================
# QUESTION TEMPLATES BY TOPIC
# ============================================================

ARRAY_TEMPLATES = [
    {
        "pattern": "two-sum-variant",
        "description": "Find {k} elements that sum to target",
        "complexities": ["O(n)", "O(n log n)", "O(n²)"],
        "constraints": "1 <= n <= 10⁵, -10⁹ <= nums[i] <= 10⁹",
    },
    {
        "pattern": "sliding-window",
        "description": "Maximum/Minimum subarray of size k with condition",
        "complexities": ["O(n)", "O(n log n)"],
        "constraints": "1 <= n <= 10⁵, 1 <= k <= n",
    },
    {
        "pattern": "prefix-sum",
        "description": "Subarray sum equals K / Range sum queries",
        "complexities": ["O(n)", "O(n log n)"],
        "constraints": "1 <= n <= 10⁵, -10⁴ <= nums[i] <= 10⁴",
    },
    {
        "pattern": "kadane",
        "description": "Maximum subarray sum with {variant}",
        "complexities": ["O(n)"],
        "constraints": "1 <= n <= 10⁵, -10⁴ <= nums[i] <= 10⁴",
    },
    {
        "pattern": "two-pointers",
        "description": "Sort + two pointers for {condition}",
        "complexities": ["O(n log n)", "O(n²)"],
        "constraints": "1 <= n <= 10⁵, -10⁹ <= nums[i] <= 10⁹",
    },
]

STRING_TEMPLATES = [
    {
        "pattern": "palindrome",
        "description": "Longest palindromic substring/subsequence {variant}",
        "complexities": ["O(n²)", "O(n)"],
        "constraints": "1 <= s.length <= 1000",
    },
    {
        "pattern": "anagram",
        "description": "Group anagrams / Find all anagrams in string",
        "complexities": ["O(n * k log k)", "O(n * k)"],
        "constraints": "1 <= strs.length <= 10⁴, 1 <= strs[i].length <= 100",
    },
    {
        "pattern": "kmp",
        "description": "Pattern matching with KMP / Z-algorithm",
        "complexities": ["O(n + m)"],
        "constraints": "1 <= text.length, pattern.length <= 10⁵",
    },
]

TREE_TEMPLATES = [
    {
        "pattern": "traversal",
        "description": "{order} traversal (iterative/recursive)",
        "complexities": ["O(n)", "O(h) space"],
        "constraints": "0 <= nodes <= 10⁴, -100 <= val <= 100",
    },
    {
        "pattern": "bst",
        "description": "Validate / Insert / Delete / Search in BST",
        "complexities": ["O(h)", "O(n) worst case"],
        "constraints": "0 <= nodes <= 10⁴",
    },
    {
        "pattern": "lca",
        "description": "Lowest Common Ancestor {variant}",
        "complexities": ["O(n)", "O(h)"],
        "constraints": "2 <= nodes <= 10⁵",
    },
]

GRAPH_TEMPLATES = [
    {
        "pattern": "bfs-dfs",
        "description": "Find path / connected components / cycle detection",
        "complexities": ["O(V + E)"],
        "constraints": "1 <= V <= 10⁴, 0 <= E <= 10⁵",
    },
    {
        "pattern": "dijkstra",
        "description": "Shortest path with {variant} weights",
        "complexities": ["O(E log V)"],
        "constraints": "1 <= V <= 10⁴, 1 <= E <= 10⁵, weights >= 0",
    },
    {
        "pattern": "topological",
        "description": "Topological sort / Course schedule / Alien dictionary",
        "complexities": ["O(V + E)"],
        "constraints": "1 <= V <= 10⁴, 0 <= E <= 10⁵",
    },
]

DP_TEMPLATES = [
    {
        "pattern": "knapsack",
        "description": "0/1 Knapsack / Unbounded / Subset sum {variant}",
        "complexities": ["O(n * W)", "O(W) space"],
        "constraints": "1 <= n <= 100, 1 <= W <= 10⁴",
    },
    {
        "pattern": "lcs",
        "description": "Longest Common Subsequence / Substring {variant}",
        "complexities": ["O(n * m)", "O(min(n,m)) space"],
        "constraints": "1 <= len <= 10³",
    },
    {
        "pattern": "lis",
        "description": "Longest Increasing Subsequence {variant}",
        "complexities": ["O(n log n)", "O(n²)"],
        "constraints": "1 <= n <= 2500, -10⁴ <= nums[i] <= 10⁴",
    },
    {
        "pattern": "grid-dp",
        "description": "Unique paths / Min path sum / Cherry pickup",
        "complexities": ["O(m * n)"],
        "constraints": "1 <= m, n <= 100",
    },
    {
        "pattern": "house-robber",
        "description": "House robber {variant} / Max non-adjacent sum",
        "complexities": ["O(n)", "O(1) space"],
        "constraints": "1 <= n <= 10⁴, 0 <= nums[i] <= 10³",
    },
]

# ============================================================
# QUESTION GENERATION
# ============================================================

def generate_test_cases(pattern: str, difficulty: str) -> List[Dict]:
    """Generate test cases for a problem pattern"""
    cases = []
    
    # Base cases
    if pattern in ["two-sum-variant", "two-pointers", "sliding-window"]:
        cases.extend([
            {"input": {"nums": [2,7,11,15], "target": 9}, "output": [0,1], "hidden": False},
            {"input": {"nums": [3,2,4], "target": 6}, "output": [1,2], "hidden": False},
            {"input": {"nums": [3,3], "target": 6}, "output": [0,1], "hidden": False},
        ])
    elif pattern in ["palindrome"]:
        cases.extend([
            {"input": {"s": "babad"}, "output": "bab", "hidden": False},
            {"input": {"s": "cbbd"}, "output": "bb", "hidden": False},
            {"input": {"s": "a"}, "output": "a", "hidden": False},
        ])
    elif pattern in ["traversal", "bst", "lca"]:
        cases.extend([
            {"input": {"root": [3,9,20,None,None,15,7]}, "output": [[3],[9,20],[15,7]], "hidden": False},
            {"input": {"root": [1,None,2,3]}, "output": [1,3,2], "hidden": False},
        ])
    elif pattern in ["knapsack", "lcs", "lis", "grid-dp", "house-robber"]:
        cases.extend([
            {"input": {"nums": [1,2,3,1]}, "output": 4, "hidden": False},
            {"input": {"nums": [2,7,9,3,1]}, "output": 12, "hidden": False},
        ])
    
    # Generate randomized additional cases
    num_hidden = 5 if difficulty == "easy" else (8 if difficulty == "medium" else 12)
    for _ in range(num_hidden):
        cases.append({"input": generate_random_input(pattern), "output": "computed", "hidden": True})
    
    return cases[:10]  # Limit total cases


def generate_random_input(pattern: str) -> Dict:
    """Generate random valid input for pattern"""
    if pattern in ["two-sum-variant", "two-pointers", "sliding-window", "kadane", "prefix-sum"]:
        n = random.randint(1, 20)
        return {"nums": [random.randint(-100, 100) for _ in range(n)], "target": random.randint(-50, 50)}
    elif pattern in ["palindrome", "anagram", "kmp"]:
        length = random.randint(1, 15)
        return {"s": ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=length))}
    elif pattern in ["traversal", "bst", "lca"]:
        return {"root": generate_random_tree()}
    elif pattern in ["bfs-dfs", "dijkstra", "topological"]:
        return generate_random_graph()
    elif pattern in ["knapsack", "lcs", "lis", "grid-dp", "house-robber"]:
        n = random.randint(1, 15)
        return {"nums": [random.randint(1, 100) for _ in range(n)], "target": random.randint(1, 500)}
    return {"data": "random"}


def generate_random_tree() -> List:
    """Generate random binary tree as list"""
    if random.random() < 0.3:
        return []
    nodes = [random.randint(-100, 100)]
    for _ in range(random.randint(1, 10)):
        if random.random() < 0.5:
            nodes.append(random.randint(-100, 100))
        else:
            nodes.append(None)
    return nodes


def generate_random_graph() -> Dict:
    """Generate random graph"""
    n = random.randint(2, 10)
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < 0.3:
                edges.append([i, j, random.randint(1, 20)])
    return {"n": n, "edges": edges}


def select_companies(difficulty: str) -> List[str]:
    """Select 2-5 companies weighted by frequency"""
    num = random.randint(2, 5)
    companies = random.choices(
        list(COMPANY_WEIGHTS.keys()),
        weights=list(COMPANY_WEIGHTS.values()),
        k=num
    )
    return list(set(companies))


def generate_question_id(topic: str, difficulty: str, index: int) -> str:
    return f"{topic[:3]}-{difficulty[0]}-{index:04d}"


def generate_boilerplate(language: str, topic: str) -> str:
    """Generate language-specific boilerplate"""
    templates = {
        "python": f"""class Solution:
    def solve(self, *args):
        # {topic} solution here
        pass

if __name__ == "__main__":
    sol = Solution()
    # Test cases
    print(sol.solve())""",
        "javascript": f"""/**
 * @param {{}} params
 * @return {{}}
 */
var solve = function(params) {{
    // {topic} solution here
    return {{}};
}};
module.exports = {{ solve }};""",
        "java": f"""class Solution {{
    public Object solve(Object args) {{
        // {topic} solution here
        return null;
    }}
}}""",
        "cpp": f"""#include <bits/stdc++.h>
using namespace std;

class Solution {{
public:
    auto solve(auto args) {{
        // {topic} solution here
        return 0;
    }}
}};""",
    }
    return templates.get(language, templates["python"])


def generate_all_questions() -> List[Dict]:
    """Generate all questions based on distribution"""
    all_questions = []
    qid_counter = {topic: 0 for topic in TOPICS}
    
    for topic, count in TOPICS.items():
        # Select templates for this topic
        if topic == "arrays":
            templates = ARRAY_TEMPLATES
        elif topic == "strings":
            templates = STRING_TEMPLATES
        elif topic == "trees":
            templates = TREE_TEMPLATES
        elif topic == "graphs":
            templates = GRAPH_TEMPLATES
        elif topic == "dynamic-programming":
            templates = DP_TEMPLATES
        else:
            templates = [{"pattern": f"{topic}-generic", "description": f"Problem on {topic}", "complexities": ["O(n log n)"], "constraints": "Standard"}]
        
        for i in range(count):
            qid_counter[topic] += 1
            difficulty = random.choices(
                list(DIFFICULTY_DIST.keys()),
                weights=list(DIFFICULTY_DIST.values())
            )[0]
            
            template = random.choice(templates)
            pattern = template["pattern"]
            
            qid = generate_question_id(topic, difficulty, qid_counter[topic])
            companies = select_companies(difficulty)
            
            question = {
                "id": qid,
                "title": f"{template['description']}",
                "topic": topic,
                "difficulty": difficulty,
                "pattern": pattern,
                "companies": companies,
                "description": generate_problem_statement(template, difficulty),
                "constraints": template["constraints"],
                "complexities": template["complexities"],
                "test_cases": generate_test_cases(pattern, difficulty),
                "boilerplate": {
                    "python": generate_boilerplate("python", topic),
                    "javascript": generate_boilerplate("javascript", topic),
                    "java": generate_boilerplate("java", topic),
                    "cpp": generate_boilerplate("cpp", topic),
                },
                "tags": [topic, difficulty, *companies[:2]],
                "hints": generate_hints(pattern, difficulty),
                "solution": generate_solution(pattern, difficulty),
                "related_topics": get_related_topics(topic),
            }
            all_questions.append(question)
    
    return all_questions


def generate_problem_statement(template: Dict, difficulty: str) -> str:
    """Generate detailed problem statement"""
    base = template["description"]
    return f"""{base}

You are given an input satisfying the constraints below. Return the correct output as specified.

**Constraints:**
{template['constraints']}

**Expected Complexities:**
{', '.join(template['complexities'])}"""


def generate_hints(pattern: str, difficulty: str) -> List[str]:
    hints_map = {
        "two-sum-variant": ["Use a hash map for O(n) lookup", "Sort + two pointers for O(n log n)"],
        "sliding-window": ["Maintain window with two pointers", "Use hash map for frequency counting"],
        "prefix-sum": ["Precompute prefix sums", "Hash map for subarray sum equals K"],
        "kadane": ["Track max ending at each position", "Reset when sum goes negative"],
        "two-pointers": ["Sort first", "Move pointers based on sum comparison"],
        "palindrome": ["Expand around center", "Manacher's algorithm for O(n)"],
        "anagram": ["Sort strings as key", "Character frequency as key"],
        "kmp": ["Build prefix function", "Z-alternative algorithm"],
        "traversal": ["Recursive is trivial, try iterative", "Morris traversal for O(1) space"],
        "bst": ["Use BST property: left < root < right", "Inorder gives sorted"],
        "lca": ["Recurse left and right", "If both sides return non-null, current is LCA"],
        "bfs-dfs": ["Queue for BFS, Stack for DFS", "Track visited to avoid cycles"],
        "dijkstra": ["Priority queue for min distance", "Relax edges"],
        "topological": ["Kahn's algorithm (BFS)", "DFS with post-order"],
        "knapsack": ["dp[i][w] = max(dp[i-1][w], dp[i-1][w-wt]+val)", "Space optimize to 1D"],
        "lcs": ["dp[i][j] = dp[i-1][j-1]+1 if match else max(dp[i-1][j], dp[i][j-1])"],
        "lis": ["Patience sorting with binary search", "dp[i] = length of LIS ending at i"],
        "grid-dp": ["dp[i][j] depends on dp[i-1][j] and dp[i][j-1]"],
        "house-robber": ["dp[i] = max(dp[i-1], dp[i-2]+nums[i])", "Two variables for O(1) space"],
    }
    hints = hints_map.get(pattern, ["Think about the optimal substructure", "Consider edge cases"])
    if difficulty == "hard":
        hints.append("Consider advanced optimization techniques")
    return hints[:3]


def generate_solution(pattern: str, difficulty: str) -> str:
    solutions = {
        "two-sum-variant": """def twoSum(self, nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []""",
        "sliding-window": """def maxSubarraySum(self, nums, k):
    window_sum = sum(nums[:k])
    max_sum = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i-k]
        max_sum = max(max_sum, window_sum)
    return max_sum""",
        "kadane": """def maxSubArray(self, nums):
    max_ending_here = max_so_far = nums[0]
    for x in nums[1:]:
        max_ending_here = max(x, max_ending_here + x)
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far""",
    }
    return solutions.get(pattern, f"# {pattern} solution template\n# Implement optimal solution here")


def get_related_topics(topic: str) -> List[str]:
    related = {
        "arrays": ["two-pointers", "sliding-window", "prefix-sum", "hash-map"],
        "strings": ["hash-map", "two-pointers", "dp", "trie"],
        "trees": ["dfs", "bfs", "recursion", "stack"],
        "graphs": ["bfs", "dfs", "union-find", "dp", "heap"],
        "dynamic-programming": ["memoization", "tabulation", "greedy", "math"],
        "linked-lists": ["two-pointers", "recursion", "hash-map"],
        "stacks-queues": ["monotonic-stack", "deque", "linked-list"],
        "heaps": ["greedy", "sorting", "graph"],
        "tries": ["strings", "bit-manipulation", "dfs"],
        "backtracking": ["dfs", "pruning", "bit-manipulation"],
        "bit-manipulation": ["math", "dp", "greedy"],
        "math": ["number-theory", "combinatorics", "probability"],
        "greedy": ["sorting", "heap", "dp"],
        "sliding-window": ["two-pointers", "hash-map", "prefix-sum"],
        "two-pointers": ["sorting", "binary-search", "sliding-window"],
        "binary-search": ["sorting", "math", "dp"],
        "prefix-sum": ["hash-map", "sliding-window", "dp"],
        "intervals": ["sorting", "greedy", "heap"],
        "monotonic-stack": ["stack", "array", "greedy"],
        "union-find": ["graph", "greedy", "mst"],
    }
    return related.get(topic, ["algorithms", "data-structures"])


if __name__ == "__main__":
    print("Generating massive question bank...")
    questions = generate_all_questions()
    print(f"Generated {len(questions)} questions")
    
    # Save to file
    with open("massive_questions.py", "w") as f:
        f.write("# Auto-generated massive question bank\n")
        f.write(f"# Total: {len(questions)} questions\n\n")
        f.write("questions = ")
        json.dump(questions, f, indent=2)
    
    # Print stats
    by_topic = {}
    by_diff = {}
    for q in questions:
        by_topic[q["topic"]] = by_topic.get(q["topic"], 0) + 1
        by_diff[q["difficulty"]] = by_diff.get(q["difficulty"], 0) + 1
    
    print("\\nBy topic:")
    for t, c in sorted(by_topic.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")
    print("\\nBy difficulty:")
    for d, c in sorted(by_diff.items()):
        print(f"  {d}: {c}")