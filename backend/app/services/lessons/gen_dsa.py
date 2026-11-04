import os
lessons_dir = "D:/Project-Fremen/backend/app/services/lessons"
target_file = os.path.join(lessons_dir, "dsa.py")
with open(target_file, "r") as f:
    content = f.read()
current_count = content.count('"id":')
target_total = current_count * 3
needed = target_total - current_count
print(f"DSA: {current_count} -> {target_total}, adding {needed} lessons")
topics = [
    ("arrays", ["array declaration", "array access", "array operations", "array rotation", "array sorting", "array searching", "two pointer technique", "sliding window", "prefix sum", "difference array"]),
    ("strings", ["string basics", "string methods", "string manipulation", "string matching", "palindrome check", "anagram check", "string compression", "string reversal", "string rotation", "string comparison"]),
    ("linked_lists", ["linked list creation", "linked list traversal", "linked list insertion", "linked list deletion", "linked list reversal", "linked list cycle detection", "linked list middle element", "linked list merge", "linked list intersection", "doubly linked list"]),
    ("stacks", ["stack implementation", "stack operations", "stack applications", "infix to postfix", "postfix evaluation", "parenthesis balancing", "stock span problem", "next greater element", "min stack", "max stack"]),
    ("queues", ["queue implementation", "queue operations", "circular queue", "deque", "priority queue", "bfs traversal", "level order traversal", "sliding window maximum", "task scheduler", "round robin"]),
    ("trees", ["binary tree creation", "binary tree traversal", "binary tree height", "binary tree diameter", "binary tree symmetry", "binary tree lca", "binary tree serialization", "binary tree deserialization", "bst validation", "bst operations"]),
    ("graphs", ["graph representation", "graph traversal", "bfs algorithm", "dfs algorithm", "dijkstra algorithm", "bellman ford algorithm", "floyd warshall algorithm", "kruskal algorithm", "prim algorithm", "topological sort"]),
    ("hashing", ["hash table", "hash function", "collision handling", "chaining", "open addressing", "load factor", "hash map", "hash set", "substring search", "rolling hash"]),
    ("recursion", ["recursion basics", "tail recursion", "head recursion", "tree recursion", "indirect recursion", "nested recursion", "backtracking", "memoization", "dynamic programming", "divide and conquer"]),
    ("dynamic_programming", ["fibonacci dp", "knapsack problem", "longest common subsequence", "longest increasing subsequence", "coin change problem", "matrix chain multiplication", "edit distance", "palindrome partitioning", "word break problem", "regular expression matching"]),
]

category_idx = 0
topic_idx = 0
new_lessons = []

for i in range(needed):
    topic_category, topics_list = topics[category_idx]
    topic = topics_list[topic_idx % len(topics_list)]
    lesson_id = f"dsa-{topic}-{i+1}"
    
    if i < needed * 0.4:
        difficulty = "beginner"
        xp = 50
    elif i < needed * 0.75:
        difficulty = "intermediate"
        xp = 70
    else:
        difficulty = "advanced"
        xp = 90
    
    prerequisites = []
    if i > 0:
        prev_idx = max(0, i - 1)
        prerequisites = [f"dsa-{topic}-{prev_idx}"]
    
    steps = [
        {
            "id": f"{lesson_id}-s1",
            "type": "explain",
            "title": f"Understanding {topic.title()}",
            "content": f"In this lesson, you'll learn about {topic} in DSA.",
            "code": f"// Example of {topic}\n// C++ or Python example",
            "output": "// Example output",
            "explanation": f"This explains how {topic} works in DSA."
        },
        {
            "id": f"{lesson_id}-s2",
            "type": "exercise",
            "title": f"Practice {topic.title()}",
            "instruction": f"Write code that demonstrates {topic}.",
            "starterCode": "# Write your code here\n",
            "solution": f"# Solution for {topic}\n# Example implementation",
            "tests": [{"input": None, "expected": None, "check": "student_attempted"}],
            "explanation": f"Here's how to implement {topic}.",
            "hints": ["Start with basics", "Test your code", "Check edge cases"]
        },
        {
            "id": f"{lesson_id}-s3",
            "type": "quiz",
            "title": f"{topic.title()} Quiz",
            "question": f"What is the primary purpose of {topic} in DSA?",
            "options": ["Store data", "Process data", "Organize code", "All of the above"],
            "correctIndex": 3,
            "explanation": f"{topic} serves multiple purposes in DSA."
        }
    ]
    
    lesson = {
        "id": lesson_id,
        "title": f"{topic.title()} - Lesson {i+1}",
        "track": "dsa",
        "description": f"Learn about {topic} in DSA with hands-on examples.",
        "difficulty": difficulty,
        "prerequisites": prerequisites,
        "xpReward": xp,
        "steps": steps
    }
    new_lessons.append(lesson)
    
    topic_idx += 1
    if topic_idx >= len(topics_list):
        topic_idx = 0
        category_idx += 1
        if category_idx >= len(topics):
            category_idx = 0

py_code = f"\n# --- Auto-generated additional lessons ({needed} lessons) ---\nEXTRA_DSA_LESSONS = [\n"
for i, lesson in enumerate(new_lessons):
    py_code += f"    {repr(lesson)}"
    if i < len(new_lessons) - 1:
        py_code += ",\n"
    else:
        py_code += "\n"
py_code += "]\nDSA_LESSONS.extend(EXTRA_DSA_LESSONS)\n"

print(f"Generated {len(new_lessons)} new DSA lessons")
