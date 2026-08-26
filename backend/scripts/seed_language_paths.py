"""Language Learning Path Seed: 7 languages x 100 levels x 80 modules.
Each language covers first principles -> DSA -> OOPs -> complex systems.
Run: python seed_language_paths.py
"""
import os, sys, uuid, random
from datetime import datetime

LANGUAGES = [
    {"id": "python", "name": "Python", "icon": "🐍", "primary_use": "Web, Data Science, AI/ML, Automation"},
    {"id": "javascript", "name": "JavaScript", "icon": "🟨", "primary_use": "Web Frontend, Backend (Node.js), Mobile"},
    {"id": "java", "name": "Java", "icon": "☕", "primary_use": "Enterprise, Android, Web Backend"},
    {"id": "cpp", "name": "C++", "icon": "⚡", "primary_use": "Systems, Game Dev, High Performance"},
    {"id": "c", "name": "C", "icon": "🔷", "primary_use": "Systems Programming, Embedded, OS"},
    {"id": "go", "name": "Go", "icon": "🟢", "primary_use": "Cloud, Backend, DevOps, Microservices"},
    {"id": "rust", "name": "Rust", "icon": "🦀", "primary_use": "Systems, WebAssembly, Performance-Critical"},
]

# 80 modules per language, organized into 10 tiers of 8 modules each
# Each tier = 10 levels, so 100 levels total per language
MODULE_TEMPLATES = [
    # TIER 1: First Principles (Levels 1-10)
    {"name": "Hello World", "description": "Write your first program. Learn syntax basics, comments, and output.", "xp": 50, "difficulty": "beginner", "type": "tutorial"},
    {"name": "Variables & Data Types", "description": "Understand variables, memory allocation, and primitive data types.", "xp": 80, "difficulty": "beginner", "type": "tutorial"},
    {"name": "Operators", "description": "Arithmetic, comparison, logical, and bitwise operators.", "xp": 80, "difficulty": "beginner", "type": "tutorial"},
    {"name": "Input/Output", "description": "Reading user input and formatting output.", "xp": 100, "difficulty": "beginner", "type": "tutorial"},
    {"name": "Control Flow: If-Else", "description": "Conditional statements and branching logic.", "xp": 100, "difficulty": "beginner", "type": "tutorial"},
    {"name": "Loops: For & While", "description": "Iteration constructs and loop control.", "xp": 120, "difficulty": "beginner", "type": "tutorial"},
    {"name": "Functions Basics", "description": "Defining and calling functions, parameters, return values.", "xp": 150, "difficulty": "beginner", "type": "tutorial"},
    {"name": "Mini Project 1", "description": "Build a simple calculator or number guessing game.", "xp": 200, "difficulty": "beginner", "type": "project"},
    
    # TIER 2: Core Programming (Levels 11-20)
    {"name": "Arrays & Lists", "description": "Working with collections, indexing, and basic operations.", "xp": 150, "difficulty": "beginner", "type": "tutorial"},
    {"name": "Strings", "description": "String manipulation, methods, and common patterns.", "xp": 150, "difficulty": "beginner", "type": "tutorial"},
    {"name": "2D Arrays & Matrices", "description": "Multi-dimensional arrays and grid-based problems.", "xp": 200, "difficulty": "beginner", "type": "tutorial"},
    {"name": "Hash Maps & Dictionaries", "description": "Key-value stores, hashing, and O(1) lookups.", "xp": 200, "difficulty": "beginner", "type": "tutorial"},
    {"name": "Recursion Fundamentals", "description": "Base cases, recursive calls, and stack frames.", "xp": 250, "difficulty": "beginner", "type": "tutorial"},
    {"name": "Debugging Techniques", "description": "Using debuggers, print statements, and error tracing.", "xp": 150, "difficulty": "beginner", "type": "tutorial"},
    {"name": "Error Handling", "description": "Try-catch blocks, exceptions, and graceful failure.", "xp": 200, "difficulty": "beginner", "type": "tutorial"},
    {"name": "Mini Project 2", "description": "Build a todo list or simple text-based game.", "xp": 300, "difficulty": "beginner", "type": "project"},
    
    # TIER 3: Data Structures I (Levels 21-30)
    {"name": "Linked Lists", "description": "Singly and doubly linked lists, pointer manipulation.", "xp": 250, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Stacks", "description": "LIFO data structure, stack operations and applications.", "xp": 250, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Queues", "description": "FIFO, circular queues, priority queues, deque.", "xp": 250, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Sets", "description": "Set operations, uniqueness, and membership testing.", "xp": 200, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Time & Space Complexity", "description": "Big O notation, analyzing algorithms.", "xp": 300, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Sorting Algorithms I", "description": "Bubble, selection, insertion sort.", "xp": 250, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Sorting Algorithms II", "description": "Merge sort, quick sort, heap sort.", "xp": 300, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Mini Project 3", "description": "Build a sorting visualizer or expression evaluator.", "xp": 400, "difficulty": "intermediate", "type": "project"},
    
    # TIER 4: Data Structures II (Levels 31-40)
    {"name": "Binary Trees", "description": "Tree structure, traversal methods (inorder, preorder, postorder).", "xp": 300, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Binary Search Trees", "description": "BST properties, insertion, deletion, searching.", "xp": 300, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Heaps & Priority Queues", "description": "Min-heap, max-heap, heap operations.", "xp": 350, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Tries", "description": "Prefix trees, autocomplete, word search.", "xp": 350, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Graphs Fundamentals", "description": "Graph representation, BFS, DFS.", "xp": 350, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Union-Find (Disjoint Set)", "description": "Connected components, Kruskal's algorithm.", "xp": 350, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Bit Manipulation", "description": "Bitwise operators, bit tricks, optimization.", "xp": 300, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Mini Project 4", "description": "Build a contact book or file system indexer.", "xp": 500, "difficulty": "intermediate", "type": "project"},
    
    # TIER 5: Algorithms I (Levels 41-50)
    {"name": "Two Pointers", "description": "Pair problems, sliding window technique.", "xp": 300, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Sliding Window", "description": "Fixed and variable window, substring problems.", "xp": 350, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Binary Search", "description": "Classic binary search, modified variants.", "xp": 300, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Greedy Algorithms", "description": "Activity selection, Huffman coding, job sequencing.", "xp": 400, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Backtracking", "description": "N-Queens, Sudoku, permutations.", "xp": 400, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Dynamic Programming I", "description": "Fibonacci, knapsack, memoization vs tabulation.", "xp": 450, "difficulty": "intermediate", "type": "tutorial"},
    {"name": "Dynamic Programming II", "description": "Longest common subsequence, edit distance.", "xp": 500, "difficulty": "advanced", "type": "tutorial"},
    {"name": "Mini Project 5", "description": "Build a pathfinding visualizer or word solver.", "xp": 600, "difficulty": "advanced", "type": "project"},
    
    # TIER 6: Object-Oriented Programming (Levels 51-60)
    {"name": "OOP Fundamentals", "description": "Classes, objects, encapsulation, abstraction.", "xp": 400, "difficulty": "advanced", "type": "tutorial"},
    {"name": "Inheritance", "description": "Single, multiple, multilevel inheritance.", "xp": 400, "difficulty": "advanced", "type": "tutorial"},
    {"name": "Polymorphism", "description": "Method overriding, method overloading, duck typing.", "xp": 400, "difficulty": "advanced", "type": "tutorial"},
    {"name": "Interfaces & Abstract Classes", "description": "Contracts, abstract methods, design patterns.", "xp": 450, "difficulty": "advanced", "type": "tutorial"},
    {"name": "Design Patterns I", "description": "Singleton, Factory, Observer, Strategy.", "xp": 500, "difficulty": "advanced", "type": "tutorial"},
    {"name": "Design Patterns II", "description": "Decorator, Adapter, Proxy, Command.", "xp": 500, "difficulty": "advanced", "type": "tutorial"},
    {"name": "SOLID Principles", "description": "Single responsibility, open-closed, Liskov substitution.", "xp": 550, "difficulty": "advanced", "type": "tutorial"},
    {"name": "Mini Project 6", "description": "Build a library management system or e-commerce cart.", "xp": 700, "difficulty": "advanced", "type": "project"},
    
    # TIER 7: Advanced Data Structures (Levels 61-70)
    {"name": "Segment Trees", "description": "Range queries, lazy propagation.", "xp": 550, "difficulty": "advanced", "type": "tutorial"},
    {"name": "Fenwick Trees (BIT)", "description": "Binary indexed trees, prefix sums.", "xp": 550, "difficulty": "advanced", "type": "tutorial"},
    {"name": "AVL Trees", "description": "Self-balancing BST, rotations.", "xp": 550, "difficulty": "advanced", "type": "tutorial"},
    {"name": "Red-Black Trees", "description": "Balanced tree properties, insertion/deletion.", "xp": 600, "difficulty": "advanced", "type": "tutorial"},
    {"name": "B-Trees", "description": "Database indexing, multi-way trees.", "xp": 600, "difficulty": "advanced", "type": "tutorial"},
    {"name": "Suffix Arrays & Trees", "description": "String matching, pattern search.", "xp": 600, "difficulty": "advanced", "type": "tutorial"},
    {"name": "Disjoint Set Union", "description": "Advanced union-find with path compression.", "xp": 550, "difficulty": "advanced", "type": "tutorial"},
    {"name": "Mini Project 7", "description": "Build a database index simulator or text search engine.", "xp": 800, "difficulty": "advanced", "type": "project"},
    
    # TIER 8: Algorithms II (Levels 71-80)
    {"name": "Graph Algorithms I", "description": "Dijkstra, Bellman-Ford, Floyd-Warshall.", "xp": 600, "difficulty": "advanced", "type": "tutorial"},
    {"name": "Graph Algorithms II", "description": "Topological sort, SCC, MST (Kruskal, Prim).", "xp": 650, "difficulty": "advanced", "type": "tutorial"},
    {"name": "Network Flow", "description": "Max flow, min cut, Ford-Fulkerson.", "xp": 700, "difficulty": "advanced", "type": "tutorial"},
    {"name": "String Algorithms", "description": "KMP, Rabin-Karp, Z-algorithm.", "xp": 650, "difficulty": "advanced", "type": "tutorial"},
    {"name": "Computational Geometry", "description": "Convex hull, closest pair, line sweep.", "xp": 700, "difficulty": "advanced", "type": "tutorial"},
    {"name": "Advanced DP", "description": "Bitmask DP, tree DP, digit DP.", "xp": 750, "difficulty": "advanced", "type": "tutorial"},
    {"name": "Randomized Algorithms", "description": "Quickselect, Las Vegas, Monte Carlo.", "xp": 700, "difficulty": "advanced", "type": "tutorial"},
    {"name": "Mini Project 8", "description": "Build a route optimizer or recommendation engine.", "xp": 900, "difficulty": "advanced", "type": "project"},
    
    # TIER 9: System Design & Architecture (Levels 81-90)
    {"name": "System Design Fundamentals", "description": "Scalability, load balancing, caching.", "xp": 750, "difficulty": "expert", "type": "tutorial"},
    {"name": "Database Design", "description": "Normalization, indexing, ACID vs BASE.", "xp": 750, "difficulty": "expert", "type": "tutorial"},
    {"name": "API Design", "description": "REST principles, GraphQL, versioning.", "xp": 700, "difficulty": "expert", "type": "tutorial"},
    {"name": "Concurrency & Parallelism", "description": "Threads, async/await, race conditions.", "xp": 800, "difficulty": "expert", "type": "tutorial"},
    {"name": "Memory Management", "description": "Garbage collection, manual memory, leaks.", "xp": 750, "difficulty": "expert", "type": "tutorial"},
    {"name": "Distributed Systems", "description": "CAP theorem, consensus, sharding.", "xp": 850, "difficulty": "expert", "type": "tutorial"},
    {"name": "Security Fundamentals", "description": "Authentication, encryption, OWASP.", "xp": 800, "difficulty": "expert", "type": "tutorial"},
    {"name": "Mini Project 9", "description": "Build a distributed key-value store or chat server.", "xp": 1000, "difficulty": "expert", "type": "project"},
    
    # TIER 10: Capstone & Mastery (Levels 91-100)
    {"name": "Capstone Project I", "description": "Build a full-stack web application from scratch.", "xp": 1200, "difficulty": "expert", "type": "project"},
    {"name": "Capstone Project II", "description": "Build a data processing pipeline or ML system.", "xp": 1200, "difficulty": "expert", "type": "project"},
    {"name": "Performance Optimization", "description": "Profiling, bottlenecks, optimization techniques.", "xp": 1000, "difficulty": "expert", "type": "tutorial"},
    {"name": "Testing & CI/CD", "description": "Unit tests, integration tests, deployment pipelines.", "xp": 900, "difficulty": "expert", "type": "tutorial"},
    {"name": "Documentation & Best Practices", "description": "Code style, documentation, maintainability.", "xp": 800, "difficulty": "expert", "type": "tutorial"},
    {"name": "Open Source Contribution", "description": "Contributing to real projects, PR workflow.", "xp": 1000, "difficulty": "expert", "type": "tutorial"},
    {"name": "Interview Preparation", "description": "FAANG-level problems, system design mock interviews.", "xp": 1000, "difficulty": "expert", "type": "tutorial"},
    {"name": "Graduation Project", "description": "Build a portfolio-worthy application showcasing all skills.", "xp": 1500, "difficulty": "expert", "type": "project"},
]

# Language-specific code snippets for each module
CODE_SNIPPETS = {
    "python": "def solution():\n    # Python solution\n    pass",
    "javascript": "function solution() {\n    // JavaScript solution\n}",
    "java": "public class Solution {\n    public void solution() {\n        // Java solution\n    }\n}",
    "cpp": "class Solution {\npublic:\n    void solution() {\n        // C++ solution\n    }\n};",
    "c": "void solution() {\n    // C solution\n}",
    "go": "func solution() {\n    // Go solution\n}",
    "rust": "fn solution() {\n    // Rust solution\n}",
}

def generate_language_path(lang):
    """Generate 100 levels x 80 modules for a language."""
    modules = []
    levels = []
    
    for tier in range(10):  # 10 tiers
        for mod_idx in range(8):  # 8 modules per tier
            global_mod_idx = tier * 8 + mod_idx
            level_num = tier * 10 + 1  # Level starts at tier*10+1
            
            mod_template = MODULE_TEMPLATES[global_mod_idx]
            
            # Create 5 levels per module (80 modules * 5 levels = 400 steps... 
            # Actually we need 100 levels total, so each module maps to ~1.25 levels)
            # Let's do: each module is one "step" and we have 100 levels where each level has multiple modules
            # Actually, re-reading: 100 levels AND 80 modules. So modules < levels.
            # Each level can have multiple modules, or modules span multiple levels.
            # Let's make 80 modules spread across 100 levels - some levels have 2 modules.
            
            module = {
                "id": str(uuid.uuid4()),
                "language_id": lang["id"],
                "language_name": lang["name"],
                "level": level_num,
                "tier": tier + 1,
                "module_index": global_mod_idx + 1,
                "name": mod_template["name"],
                "description": mod_template["description"],
                "xp_reward": mod_template["xp"],
                "difficulty": mod_template["difficulty"],
                "type": mod_template["type"],
                "estimated_time": f"{mod_template['xp'] // 20 + 10} min",
                "content": {
                    "introduction": f"Welcome to {mod_template['name']} in {lang['name']}. {mod_template['description']}",
                    "steps": [
                        {"step": 1, "title": "Understanding the Concept", "content": f"Learn the fundamentals of {mod_template['name']}.", "code": CODE_SNIPPETS[lang["id"]]},
                        {"step": 2, "title": "Hands-on Practice", "content": f"Apply {mod_template['name']} with practical examples.", "code": CODE_SNIPPETS[lang["id"]]},
                        {"step": 3, "title": "Common Pitfalls", "content": "Avoid these common mistakes.", "code": ""},
                        {"step": 4, "title": "Real-world Application", "content": f"How {mod_template['name']} is used in production.", "code": ""},
                        {"step": 5, "title": "Challenge", "content": f"Test your knowledge with a challenge problem.", "code": CODE_SNIPPETS[lang["id"]]},
                    ],
                    "key_points": [f"Master {mod_template['name']}", "Understand use cases", "Practice regularly"],
                    "resources": [
                        {"type": "video", "title": f"{mod_template['name']} Tutorial", "url": f"/videos/{lang['id']}/{global_mod_idx+1}"},
                        {"type": "article", "title": f"{mod_template['name']} Deep Dive", "url": f"/articles/{lang['id']}/{global_mod_idx+1}"},
                        {"type": "practice", "title": f"{mod_template['name']} Exercises", "url": f"/practice/{lang['id']}/{global_mod_idx+1}"},
                    ],
                },
                "prerequisites": [MODULE_TEMPLATES[i]["name"] for i in range(max(0, global_mod_idx-3), global_mod_idx)] if global_mod_idx > 0 else [],
                "related_modules": [MODULE_TEMPLATES[i]["name"] for i in range(min(len(MODULE_TEMPLATES)-1, global_mod_idx+1), min(len(MODULE_TEMPLATES), global_mod_idx+4))],
                "tags": [mod_template["difficulty"], mod_template["type"], lang["id"]],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
            modules.append(module)
    
    # Generate 100 levels (each level = ~10 modules, so we have 80 modules spread across 100 levels)
    # Actually: 80 modules, 100 levels. So some levels have modules, some don't.
    # Let's make: levels 1-80 have 1 module each, levels 81-100 are "review" levels
    for level_num in range(1, 101):
        if level_num <= 80:
            level_modules = [m for m in modules if m["module_index"] == level_num]
            level = {
                "language_id": lang["id"],
                "level": level_num,
                "tier": min((level_num - 1) // 10 + 1, 10),
                "name": f"Level {level_num}: {modules[level_num-1]['name']}" if level_num <= len(modules) else f"Level {level_num}",
                "description": modules[level_num-1]["description"] if level_num <= len(modules) else "Review and practice all previous concepts.",
                "modules": [m["id"] for m in level_modules],
                "xp_required": level_num * 100,
                "xp_reward": 200 if level_num <= len(modules) else 100,
                "unlocks_at": level_num,
                "is_review": level_num > 80,
                "badge": f"level_{level_num}_complete",
            }
        else:
            level = {
                "language_id": lang["id"],
                "level": level_num,
                "tier": 10,
                "name": f"Level {level_num}: Mastery Review",
                "description": "Review all concepts and prepare for the capstone project.",
                "modules": [],
                "xp_required": level_num * 100,
                "xp_reward": 100,
                "unlocks_at": level_num,
                "is_review": True,
                "badge": f"level_{level_num}_complete",
            }
        levels.append(level)
    
    return modules, levels

def generate_all():
    all_modules = []
    all_levels = []
    
    for lang in LANGUAGES:
        modules, levels = generate_language_path(lang)
        all_modules.extend(modules)
        all_levels.extend(levels)
    
    print(f"Total modules generated: {len(all_modules)}")
    print(f"Total levels generated: {len(all_levels)}")
    print(f"\nPer language breakdown:")
    for lang in LANGUAGES:
        lang_modules = [m for m in all_modules if m["language_id"] == lang["id"]]
        lang_levels = [l for l in all_levels if l["language_id"] == lang["id"]]
        print(f"  {lang['name']}: {len(lang_modules)} modules, {len(lang_levels)} levels")
    
    print(f"\nModule type breakdown:")
    from collections import Counter
    types = Counter(m["type"] for m in all_modules)
    for t, c in types.most_common():
        print(f"  {t}: {c}")
    
    print(f"\nDifficulty breakdown:")
    diffs = Counter(m["difficulty"] for m in all_modules)
    for d, c in diffs.most_common():
        print(f"  {d}: {c}")
    
    print(f"\nTier breakdown:")
    tiers = Counter(m["tier"] for m in all_modules)
    for t, c in sorted(tiers.items()):
        print(f"  Tier {t}: {c} modules")
    
    return all_modules, all_levels

if __name__ == "__main__":
    generate_all()