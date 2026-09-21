"""
Enhanced Role Curriculum Definitions — role_curriculum_v2.py

This module extends the base role_curriculum.py with:
  - Phase-based progression (Foundation → Core → Advanced → Job Ready)
  - Learning module integration (links to learning_modules collection)
  - Company-specific preparation tracks
  - Enhanced mock test configurations
  - Difficulty distribution per skill
  - Estimated completion times
  - Milestone tracking

This is loaded as an enhancement layer over the base role_curriculum.py.
"""
from typing import Dict, List, Any
import os
import json
from datetime import datetime, timezone


# =============================================================
# CURRICULUM VERSION
# =============================================================

CURRICULUM_VERSION = "2.0.0"
CURRICULUM_GENERATED = datetime.now(timezone.utc).isoformat()


# =============================================================
# PHASE DEFINITIONS
# =============================================================

PHASES = {
    "foundation": {
        "name": "Foundation (Beginner)",
        "description": "Build programming fundamentals and core concepts from scratch",
        "duration_weeks": 4,
        "color": "#10B981",  # green
        "icon": "🌱",
        "completion_criteria": "Complete all foundation skills with 80%+ accuracy on easy problems",
    },
    "core": {
        "name": "Core (Intermediate)",
        "description": "Master core data structures, algorithms, and domain-specific skills",
        "duration_weeks": 6,
        "color": "#3B82F6",  # blue
        "icon": "⚡",
        "completion_criteria": "Complete all core skills with 70%+ accuracy on medium problems",
    },
    "advanced": {
        "name": "Advanced",
        "description": "Tackle hard problems, system design, and specialized topics",
        "duration_weeks": 6,
        "color": "#8B5CF6",  # purple
        "icon": "🚀",
        "completion_criteria": "Complete all advanced skills with 60%+ accuracy on hard problems",
    },
    "job-ready": {
        "name": "Job Ready",
        "description": "Company-specific prep, mock interviews, and behavioral rounds",
        "duration_weeks": 4,
        "color": "#F59E0B",  # amber
        "icon": "🎯",
        "completion_criteria": "Clear 3+ full mock interview loops with 80%+ score",
    },
}


# =============================================================
# LEARNING MODULE CATALOG
# =============================================================

LEARNING_MODULE_CATALOG: Dict[str, Dict[str, Any]] = {
    # SDE Modules
    "variables-state": {
        "title": "Variables & State — The Memory Box",
        "phase": "foundation",
        "topic": "variables",
        "difficulty": "beginner",
        "estimated_time_minutes": 50,
        "xp_reward": 120,
        "prerequisites": [],
        "skills_gained": ["variable-declaration", "assignment", "memory-model", "state-mutation"],
        "learning_objectives": [
            "Understand that programs need a way to remember information",
            "Learn what a variable is (name + value + type)",
            "Understand assignment as 'store this value under this name'",
            "See how variables enable programs to change behavior based on input",
            "Write your first variable declarations and assignments"
        ],
        "mission": {
            "story_context": {
                "setting": "The Memory Vault",
                "character": "Archivist Nyx",
                "narrative": "In the heart of the BountyCode world lies the Memory Vault — an ancient library where every program stores what it knows. The Archivist, Nyx, guards the vault. But the vault is empty. Programs enter, do their work, and leave without remembering anything. You must teach the programs how to remember — by mastering the art of variables."
            },
            "first_principle": {
                "statement": "Programs need a way to remember information.",
                "explanation": "Before a program can do anything useful — calculate a score, track a player's position, remember a user's name — it needs a place to store that information. That place is a variable. Think of it as a labeled box: the label is the name, the contents are the value, and the box type determines what can go inside.",
                "analogy": "Imagine a warehouse with thousands of shelves. Each shelf has a label (variable name) and holds one item (value). The shelf size determines what fits (type). Assignment is placing an item on a shelf. Reading is looking at what's on the shelf."
            },
            "interactive_discovery": {
                "type": "visual_memory_box",
                "description": "Manipulate a visual 'memory box' to understand variables.",
                "steps": [
                    "See an empty shelf labeled 'score'",
                    "Drag a number token (42) onto the shelf — this is assignment",
                    "See the shelf now holds '42'",
                    "Drag a different token (100) onto the shelf — the old value is replaced",
                    "Add a second shelf labeled 'player_name' and place a text token ('Aria')",
                    "Try placing a number on the text shelf — the system prevents type mismatch",
                    "Read values from shelves to make decisions (if score > 50: 'You win!')"
                ],
                "component": "MemoryBoxVisualizer"
            },
            "concept_reveal": {
                "title": "What Just Happened?",
                "content": "You just created variables! Each shelf is a variable. The label is the name (score, player_name). The token is the value (42, 'Aria'). The shelf size is the type (number shelf, text shelf). Assignment is putting a token on a shelf. Reading is checking what's on the shelf.",
                "key_terms": [
                    {"term": "Variable", "definition": "A named storage location in memory that holds a value."},
                    {"term": "Assignment", "definition": "The act of storing a value in a variable (e.g., score = 42)."},
                    {"term": "Type", "definition": "The kind of value a variable can hold (number, text, true/false)."},
                    {"term": "Declaration", "definition": "Telling the program a variable exists and what type it is."},
                    {"term": "Initialization", "definition": "Giving a variable its first value."}
                ]
            },
            "guided_code": {
                "language": "python",
                "steps": [
                    {
                        "instruction": "Create a variable named 'score' and store the number 0 in it.",
                        "starter_code": "# Create a score variable\nscore = \nprint(score)",
                        "solution": "score = 0\nprint(score)",
                        "hint": "The equals sign (=) means 'store the value on the right in the variable on the left.'"
                    },
                    {
                        "instruction": "Create a variable 'player_name' with your name as text.",
                        "starter_code": "# Create player_name variable\nplayer_name = \nprint(f'Welcome, {player_name}!')",
                        "solution": "player_name = 'Aria'\nprint(f'Welcome, {player_name}!')",
                        "hint": "Text values go inside quotes (single or double). This is called a 'string'."
                    },
                    {
                        "instruction": "Change the score to 100 and print it again.",
                        "starter_code": "score = 0\n# Change score to 100 here\nprint(score)",
                        "solution": "score = 0\nscore = 100\nprint(score)",
                        "hint": "You can assign a new value to an existing variable. The old value is replaced."
                    },
                    {
                        "instruction": "Create a variable 'is_winner' set to True, then print a message based on it.",
                        "starter_code": "# Create is_winner variable\nis_winner = \nif is_winner:\n    print('Victory!')\nelse:\n    print('Keep trying!')",
                        "solution": "is_winner = True\nif is_winner:\n    print('Victory!')\nelse:\n    print('Keep trying!')",
                        "hint": "True and False (capitalized) are boolean values. They represent yes/no, on/off."
                    }
                ]
            },
            "immediate_feedback": {
                "type": "world_reaction",
                "description": "Each code execution triggers a visual response in the Memory Vault.",
                "reactions": [
                    {"trigger": "score = 0", "effect": "A '0' token appears on the 'score' shelf"},
                    {"trigger": "player_name = 'Aria'", "effect": "A text token appears on the 'player_name' shelf"},
                    {"trigger": "score = 100", "effect": "The '0' token is replaced by '100' on the shelf"},
                    {"trigger": "is_winner = True", "effect": "A golden checkmark appears; the vault door glows"}
                ]
            },
            "micro_challenges": [
                {
                    "id": "mc-1",
                    "title": "The Counter",
                    "instruction": "Create a variable 'count' set to 5. Then change it to 6. Print both values.",
                    "difficulty": "easy",
                    "diamonds": 10
                },
                {
                    "id": "mc-2",
                    "title": "The Swapper",
                    "instruction": "Create two variables: a = 10, b = 20. Swap their values using a third variable. Print both.",
                    "difficulty": "easy",
                    "diamonds": 15
                },
                {
                    "id": "mc-3",
                    "title": "The Tracker",
                    "instruction": "Create variables for a game: player_health = 100, enemy_damage = 15. Calculate new_health after one hit and print it.",
                    "difficulty": "medium",
                    "diamonds": 20
                },
                {
                    "id": "mc-4",
                    "title": "The Level Up",
                    "instruction": "Create level = 1, diamonds = 0. Add 100 diamonds. If diamonds >= 100, increase level by 1 and reset diamonds to 0. Print level and diamonds.",
                    "difficulty": "medium",
                    "diamonds": 25
                }
            ],
            "hint_ladder": {
                "level_1_conceptual": {
                    "trigger": "Student struggles with variable concept",
                    "hint": "Think of a variable like a labeled box. The name is written on the outside. The value is what's inside. You can look inside (read) or put something new in (assign)."
                },
                "level_2_strategic": {
                    "trigger": "Student doesn't know where to start",
                    "hint": "Start by writing the variable name, then an equals sign, then the value. Example: my_variable = 42"
                },
                "level_3_structural": {
                    "trigger": "Code has syntax errors",
                    "hint": "Check: Is the variable name one word (no spaces)? Are text values in quotes? Are True/False capitalized? Does each line end cleanly?"
                },
                "level_4_near_solution": {
                    "trigger": "Logic is slightly off",
                    "hint": "You're very close! Check the order of operations. In 'score = score + 10', the right side happens first, then the result is stored in 'score'."
                }
            },
            "transfer_challenge": {
                "title": "The Inventory System",
                "instruction": "Build a tiny inventory for a game. Create variables for: player_gold (start 50), potion_price (15), sword_price (100). Calculate if the player can afford the sword. Print 'Can buy sword: True/False'. Then subtract the potion price from gold and print remaining gold.",
                "skills_tested": ["variable-declaration", "assignment", "arithmetic", "boolean-logic", "print-formatting"],
                "starter_code": "# Build your inventory system here\nplayer_gold = \npotion_price = \nsword_price = \n\n# Can afford sword?\ncan_buy = \nprint(f'Can buy sword: {can_buy}')\n\n# Buy potion\nplayer_gold = player_gold - potion_price\nprint(f'Remaining gold: {player_gold}')",
                "solution": "player_gold = 50\npotion_price = 15\nsword_price = 100\n\ncan_buy = player_gold >= sword_price\nprint(f'Can buy sword: {can_buy}')\n\nplayer_gold = player_gold - potion_price\nprint(f'Remaining gold: {player_gold}')",
                "diamonds": 30
            },
            "boss": {
                "title": "The Memory Vault Keeper",
                "instruction": "Prove you understand variables by building a complete mini-program from scratch. The Archivist Nyx will test you with three scenarios. You must write code for each without hints.",
                "scenarios": [
                    {
                        "name": "Scenario 1: The Score Board",
                        "prompt": "Create a two-player score tracker. Start both at 0. Player 1 scores 10, then Player 2 scores 5. Print both scores.",
                        "success_criteria": "Both variables created, both updated, both printed correctly"
                    },
                    {
                        "name": "Scenario 2: The Health Potion",
                        "prompt": "A player has 80 health. They drink a potion that heals 25, but max health is 100. Calculate and print final health (capped at 100).",
                        "success_criteria": "Correct calculation with min() or if-statement, health capped at 100"
                    },
                    {
                        "name": "Scenario 3: The Level Gate",
                        "prompt": "A player needs 200 Diamonds to reach level 2. They currently have 150 Diamonds. They complete a quest worth 60 Diamonds. Calculate new Diamonds, check if they level up, and print both level and Diamonds.",
                        "success_criteria": "Diamonds added correctly, level-up logic works, both printed"
                    }
                ],
                "diamonds": 100,
                "mastery_badge": "Memory Keeper"
            },
            "srs_enrollment": {
                "concept_id": "variables-state",
                "review_schedule_days": [1, 3, 7, 14, 30],
                "questions": [
                    "What is a variable?",
                    "What does assignment (x = 5) do?",
                    "What happens when you assign a new value to an existing variable?",
                    "What is a type, and why does it matter?",
                    "What's the difference between 5 and '5'?"
                ]
            },
            "rewards": {
                "xp_total": 400,
                "xp_breakdown": {
                    "guided_code": 80,
                    "micro_challenges": 70,
                    "transfer_challenge": 30,
                    "boss": 100,
                    "completion_bonus": 120
                },
                "mastery_badge": "Memory Keeper",
                "world_progression": "Unlocks 'Arrays Village' (next mission)"
            }
        },
        "steps": [
            {"type": "theory", "title": "Variables & State", "content": "Learn what variables are and how programs remember information."},
            {"type": "example", "title": "Working with Variables", "content": "Examples of variable declaration and assignment in Python."},
            {"type": "try_it", "title": "Your First Variables", "content": "Create variables of different types and print them.", "language": "python", "code_snippet": "# Declare variables\nscore = 0\nplayer_name = 'Aria'\nis_winner = False\n# Print them\nprint(f'Score: {score}')\nprint(f'Player: {player_name}')\nprint(f'Winner: {is_winner}')"},
            {"type": "solution", "title": "Solution Walkthrough", "content": "Review the solution and best practices."},
        ],
    },
    "programming-basics": {
        "title": "Programming Fundamentals",
        "phase": "foundation",
        "topic": "programming",
        "difficulty": "beginner",
        "estimated_time_minutes": 45,
        "xp_reward": 100,
        "steps": [
            {"type": "theory", "title": "Variables & Data Types", "content": "Learn about integers, strings, floats, booleans, and type systems."},
            {"type": "example", "title": "Working with Variables", "content": "Examples of variable declaration and assignment in Python/Java."},
            {"type": "try_it", "title": "Your First Program", "content": "Write a program that declares variables of different types and prints them.", "language": "python", "code_snippet": "# Declare variables\nname = 'Student'\nage = 20\n# Print them\nprint(f'Name: {name}, Age: {age}')"},
            {"type": "solution", "title": "Solution Walkthrough", "content": "Review the solution and best practices."},
        ],
    },
    "arrays-hashing": {
        "title": "Arrays & Hashing Mastery",
        "phase": "foundation",
        "topic": "arrays",
        "difficulty": "beginner",
        "estimated_time_minutes": 60,
        "xp_reward": 150,
        "steps": [
            {"type": "theory", "title": "Array Fundamentals", "content": "Understanding arrays, indexing, and time complexity."},
            {"type": "theory", "title": "Hash Tables", "content": "How hash maps work, collisions, and when to use them."},
            {"type": "example", "title": "Two Sum Walkthrough", "content": "Step-by-step solution of the classic Two Sum problem."},
            {"type": "try_it", "title": "Solve Two Sum", "content": "Solve the Two Sum problem using a hash map.", "language": "python", "code_snippet": "def two_sum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen:\n            return [seen[target - n], i]\n        seen[n] = i\n    return []"},
            {"type": "try_it", "title": "Group Anagrams", "content": "Group strings that are anagrams of each other.", "language": "python"},
            {"type": "solution", "title": "Best Practices", "content": "Common pitfalls and optimization techniques."},
        ],
    },
    "two-pointers": {
        "title": "Two Pointers Technique",
        "phase": "foundation",
        "topic": "arrays",
        "difficulty": "beginner",
        "estimated_time_minutes": 50,
        "xp_reward": 120,
        "steps": [
            {"type": "theory", "title": "Two Pointer Pattern", "content": "When and why to use two pointers."},
            {"type": "example", "title": "Container With Most Water", "content": "Visual explanation of the two-pointer approach."},
            {"type": "try_it", "title": "Practice: 3Sum", "content": "Find all unique triplets that sum to zero.", "language": "python"},
            {"type": "solution", "title": "Solution Review", "content": "Time/space analysis and edge cases."},
        ],
    },
    "sliding-window": {
        "title": "Sliding Window Pattern",
        "phase": "foundation",
        "topic": "arrays",
        "difficulty": "beginner",
        "estimated_time_minutes": 55,
        "xp_reward": 130,
        "steps": [
            {"type": "theory", "title": "Sliding Window Basics", "content": "Fixed and variable size windows."},
            {"type": "example", "title": "Maximum Sum Subarray of Size K", "content": "Step-by-step walkthrough."},
            {"type": "try_it", "title": "Longest Substring Without Repeating", "content": "Implement the classic sliding window problem.", "language": "python"},
            {"type": "solution", "title": "Solution & Variations", "content": "Common variations and patterns."},
        ],
    },
    "recursion-fundamentals": {
        "title": "Recursion Fundamentals",
        "phase": "foundation",
        "topic": "recursion",
        "difficulty": "beginner",
        "estimated_time_minutes": 50,
        "xp_reward": 120,
        "steps": [
            {"type": "theory", "title": "What is Recursion?", "content": "Base cases, recursive cases, and the call stack."},
            {"type": "example", "title": "Factorial & Fibonacci", "content": "Classic recursive examples."},
            {"type": "try_it", "title": "Reverse a String Recursively", "content": "Write a recursive string reversal.", "language": "python"},
            {"type": "solution", "title": "Common Mistakes", "content": "Stack overflow, infinite recursion, and debugging."},
        ],
    },
    "string-manipulation": {
        "title": "String Manipulation",
        "phase": "foundation",
        "topic": "strings",
        "difficulty": "beginner",
        "estimated_time_minutes": 45,
        "xp_reward": 100,
        "steps": [
            {"type": "theory", "title": "String Basics in Code", "content": "Immutability, slicing, and common operations."},
            {"type": "example", "title": "Valid Palindrome", "content": "Two-pointer approach to palindrome check."},
            {"type": "try_it", "title": "String Compression", "content": "Implement basic string compression.", "language": "python"},
            {"type": "solution", "title": "Solution & Edge Cases", "content": "Handling empty strings, Unicode, and special characters."},
        ],
    },
    "linked-lists-deep-dive": {
        "title": "Linked Lists Deep Dive",
        "phase": "core",
        "topic": "linked-lists",
        "difficulty": "intermediate",
        "estimated_time_minutes": 60,
        "xp_reward": 150,
        "steps": [
            {"type": "theory", "title": "Linked List Anatomy", "content": "Node structure, pointers, and memory layout."},
            {"type": "example", "title": "Reverse a Linked List", "content": "Iterative reversal with three pointers."},
            {"type": "try_it", "title": "Detect Cycle", "content": "Floyd's cycle detection algorithm.", "language": "python"},
            {"type": "try_it", "title": "Merge Two Sorted Lists", "content": "Merge two sorted linked lists.", "language": "python"},
            {"type": "solution", "title": "Advanced: LRU Cache", "content": "Design and implement an LRU cache."},
        ],
    },
    "stacks-queues": {
        "title": "Stacks & Queues",
        "phase": "core",
        "topic": "stacks",
        "difficulty": "intermediate",
        "estimated_time_minutes": 50,
        "xp_reward": 130,
        "steps": [
            {"type": "theory", "title": "Stack & Queue Fundamentals", "content": "LIFO vs FIFO, implementations, and use cases."},
            {"type": "example", "title": "Valid Parentheses", "content": "Stack-based solution with matching."},
            {"type": "try_it", "title": "Min Stack", "content": "Design a stack that supports getMin in O(1).", "language": "python"},
            {"type": "try_it", "title": "Daily Temperatures", "content": "Monotonic stack problem.", "language": "python"},
            {"type": "solution", "title": "Solution & Patterns", "content": "When to use stack vs queue."},
        ],
    },
    "trees-bst": {
        "title": "Trees & Binary Search Trees",
        "phase": "core",
        "topic": "trees",
        "difficulty": "intermediate",
        "estimated_time_minutes": 70,
        "xp_reward": 180,
        "steps": [
            {"type": "theory", "title": "Tree Terminology", "content": "Root, children, depth, height, and traversals."},
            {"type": "example", "title": "DFS & BFS Traversals", "content": "Inorder, preorder, postorder, level order."},
            {"type": "try_it", "title": "Maximum Depth", "content": "Find the maximum depth of a binary tree.", "language": "python"},
            {"type": "try_it", "title": "Validate BST", "content": "Check if a binary tree is a valid BST.", "language": "python"},
            {"type": "try_it", "title": "Lowest Common Ancestor", "content": "Find LCA in a binary tree.", "language": "python"},
            {"type": "solution", "title": "Advanced: Serialize & Deserialize", "content": "Encode and decode a binary tree."},
        ],
    },
    "binary-trees": {
        "title": "Binary Trees",
        "phase": "core",
        "topic": "trees",
        "difficulty": "intermediate",
        "estimated_time_minutes": 60,
        "xp_reward": 150,
        "steps": [
            {"type": "theory", "title": "Binary Tree Properties", "content": "Types of binary trees and their properties."},
            {"type": "example", "title": "Level Order Traversal", "content": "BFS approach to level order."},
            {"type": "try_it", "title": "Invert Binary Tree", "content": "Mirror a binary tree.", "language": "python"},
            {"type": "solution", "title": "Solution & Analysis", "content": "Recursive vs iterative approaches."},
        ],
    },
    "tries": {
        "title": "Tries (Prefix Trees)",
        "phase": "core",
        "topic": "trees",
        "difficulty": "intermediate",
        "estimated_time_minutes": 45,
        "xp_reward": 120,
        "steps": [
            {"type": "theory", "title": "Trie Structure", "content": "When to use tries and how they work."},
            {"type": "example", "title": "Implement a Trie", "content": "Build insert, search, and startsWith."},
            {"type": "try_it", "title": "Word Search II", "content": "Find all words from a dictionary in a board.", "language": "python"},
            {"type": "solution", "title": "Solution Review", "content": "Time/space complexity analysis."},
        ],
    },
    "binary-search-patterns": {
        "title": "Binary Search Patterns",
        "phase": "core",
        "topic": "search",
        "difficulty": "intermediate",
        "estimated_time_minutes": 55,
        "xp_reward": 140,
        "steps": [
            {"type": "theory", "title": "Binary Search Variants", "content": "Standard, lower bound, upper bound, and rotated arrays."},
            {"type": "example", "title": "Search in Rotated Sorted Array", "content": "Modified binary search."},
            {"type": "try_it", "title": "Find Minimum in Rotated Array", "content": "Find the minimum element.", "language": "python"},
            {"type": "try_it", "title": "Koko Eating Bananas", "content": "Binary search on the answer.", "language": "python"},
            {"type": "solution", "title": "Advanced: Median of Two Sorted Arrays", "content": "O(log(min(m,n))) solution."},
        ],
    },
    "graph-fundamentals": {
        "title": "Graph Fundamentals",
        "phase": "core",
        "topic": "graphs",
        "difficulty": "intermediate",
        "estimated_time_minutes": 65,
        "xp_reward": 160,
        "steps": [
            {"type": "theory", "title": "Graph Representations", "content": "Adjacency list, matrix, and edge list."},
            {"type": "example", "title": "Number of Islands", "content": "DFS approach to island counting."},
            {"type": "try_it", "title": "Clone Graph", "content": "Deep copy a graph.", "language": "python"},
            {"type": "try_it", "title": "Course Schedule", "content": "Detect cycle in directed graph.", "language": "python"},
            {"type": "solution", "title": "BFS vs DFS", "content": "When to use which approach."},
        ],
    },
    "graph-advanced": {
        "title": "Advanced Graph Algorithms",
        "phase": "core",
        "topic": "graphs",
        "difficulty": "intermediate",
        "estimated_time_minutes": 60,
        "xp_reward": 150,
        "steps": [
            {"type": "theory", "title": "Topological Sort", "content": "Kahn's algorithm and DFS approach."},
            {"type": "theory", "title": "Shortest Path", "content": "Dijkstra, Bellman-Ford, and BFS."},
            {"type": "try_it", "title": "Word Ladder", "content": "BFS shortest transformation sequence.", "language": "python"},
            {"type": "try_it", "title": "Network Delay Time", "content": "Dijkstra's algorithm application.", "language": "python"},
            {"type": "solution", "title": "Union-Find", "content": "Disjoint set data structure."},
        ],
    },
    "dp-patterns": {
        "title": "Dynamic Programming Patterns",
        "phase": "core",
        "topic": "dynamic-programming",
        "difficulty": "intermediate",
        "estimated_time_minutes": 75,
        "xp_reward": 200,
        "steps": [
            {"type": "theory", "title": "DP Fundamentals", "content": "Memoization, tabulation, and state design."},
            {"type": "example", "title": "Climbing Stairs", "content": "Classic 1D DP example."},
            {"type": "try_it", "title": "Coin Change", "content": "Unbounded knapsack variation.", "language": "python"},
            {"type": "try_it", "title": "Longest Increasing Subsequence", "content": "Classic LIS problem.", "language": "python"},
            {"type": "try_it", "title": "Word Break", "content": "DP with string matching.", "language": "python"},
            {"type": "solution", "title": "2D DP: Unique Paths", "content": "Grid-based DP problem."},
        ],
    },
    "dp-advanced": {
        "title": "Advanced Dynamic Programming",
        "phase": "advanced",
        "topic": "dynamic-programming",
        "difficulty": "advanced",
        "estimated_time_minutes": 80,
        "xp_reward": 220,
        "steps": [
            {"type": "theory", "title": "DP on Strings", "content": "Edit distance, LCS, and pattern matching."},
            {"type": "example", "title": "Edit Distance", "content": "Levenshtein distance with DP."},
            {"type": "try_it", "title": "Longest Common Subsequence", "content": "Classic 2D DP problem.", "language": "python"},
            {"type": "try_it", "title": "Burst Balloons", "content": "Interval DP problem.", "language": "python"},
            {"type": "try_it", "title": "Regular Expression Matching", "content": "Complex DP with state design.", "language": "python"},
            {"type": "solution", "title": "DP on Trees", "content": "Tree DP with house robber III."},
        ],
    },
    "heap-priority-queue": {
        "title": "Heap & Priority Queue",
        "phase": "core",
        "topic": "heap",
        "difficulty": "intermediate",
        "estimated_time_minutes": 50,
        "xp_reward": 130,
        "steps": [
            {"type": "theory", "title": "Heap Fundamentals", "content": "Min-heap, max-heap, and heap operations."},
            {"type": "example", "title": "Kth Largest Element", "content": "Using a heap to find kth largest."},
            {"type": "try_it", "title": "Top K Frequent Elements", "content": "Heap-based frequency counting.", "language": "python"},
            {"type": "try_it", "title": "Task Scheduler", "content": "Greedy + heap approach.", "language": "python"},
            {"type": "solution", "title": "Solution & Variations", "content": "When to use heap vs other data structures."},
        ],
    },
    "system-design-intro": {
        "title": "System Design Introduction",
        "phase": "advanced",
        "topic": "system-design",
        "difficulty": "advanced",
        "estimated_time_minutes": 90,
        "xp_reward": 250,
        "steps": [
            {"type": "theory", "title": "System Design Basics", "content": "Scalability, availability, and consistency."},
            {"type": "theory", "title": "Load Balancing & Caching", "content": "L4 vs L7, cache strategies, and invalidation."},
            {"type": "example", "title": "Design URL Shortener", "content": "Step-by-step design of bit.ly-like service."},
            {"type": "try_it", "title": "Design Twitter", "content": "Design a social media feed.", "language": "python"},
            {"type": "solution", "title": "System Design Template", "content": "How to approach any system design problem."},
        ],
    },
    "system-design-deep-dive": {
        "title": "System Design Deep Dive",
        "phase": "job-ready",
        "topic": "system-design",
        "difficulty": "advanced",
        "estimated_time_minutes": 100,
        "xp_reward": 300,
        "steps": [
            {"type": "theory", "title": "Distributed Systems", "content": "CAP theorem, consensus, and consistency models."},
            {"type": "example", "title": "Design Uber", "content": "Real-time location-based service design."},
            {"type": "try_it", "title": "Design YouTube", "content": "Video streaming platform design.", "language": "python"},
            {"type": "try_it", "title": "Design Dropbox", "content": "File storage and synchronization.", "language": "python"},
            {"type": "solution", "title": "Scaling Strategies", "content": "Sharding, replication, and partitioning."},
        ],
    },
    "dbms-fundamentals": {
        "title": "DBMS Fundamentals",
        "phase": "advanced",
        "topic": "dbms",
        "difficulty": "intermediate",
        "estimated_time_minutes": 60,
        "xp_reward": 150,
        "steps": [
            {"type": "theory", "title": "Database Concepts", "content": "RDBMS, ACID properties, and normalization."},
            {"type": "example", "title": "SQL Joins", "content": "Inner, outer, left, right, and cross joins."},
            {"type": "try_it", "title": "Write Complex Queries", "content": "Practice advanced SQL queries.", "language": "sql"},
            {"type": "solution", "title": "Indexing & Performance", "content": "How indexes work and when to use them."},
        ],
    },
    "sql-advanced": {
        "title": "Advanced SQL",
        "phase": "advanced",
        "topic": "sql",
        "difficulty": "advanced",
        "estimated_time_minutes": 70,
        "xp_reward": 180,
        "steps": [
            {"type": "theory", "title": "Window Functions", "content": "ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD."},
            {"type": "example", "title": "CTEs and Recursive Queries", "content": "Common Table Expressions in action."},
            {"type": "try_it", "title": "Complex Analytics Query", "content": "Write a multi-step analytical query.", "language": "sql"},
            {"type": "solution", "title": "Query Optimization", "content": "Execution plans and optimization techniques."},
        ],
    },
    "oop-design-patterns": {
        "title": "OOP & Design Patterns",
        "phase": "advanced",
        "topic": "oop",
        "difficulty": "intermediate",
        "estimated_time_minutes": 65,
        "xp_reward": 160,
        "steps": [
            {"type": "theory", "title": "OOP Principles", "content": "Encapsulation, inheritance, polymorphism, abstraction."},
            {"type": "theory", "title": "SOLID Principles", "content": "Single responsibility, open/closed, Liskov, interface segregation, dependency inversion."},
            {"type": "example", "title": "Strategy Pattern", "content": "Behavioral design pattern."},
            {"type": "try_it", "title": "Implement Observer", "content": "Build an event system.", "language": "python"},
            {"type": "solution", "title": "When to Use Which Pattern", "content": "Pattern selection guide."},
        ],
    },
    "networking-basics": {
        "title": "Computer Networking Basics",
        "phase": "advanced",
        "topic": "networks",
        "difficulty": "intermediate",
        "estimated_time_minutes": 55,
        "xp_reward": 140,
        "steps": [
            {"type": "theory", "title": "OSI & TCP/IP Model", "content": "Network layers and protocols."},
            {"type": "example", "title": "TCP 3-Way Handshake", "content": "Connection establishment process."},
            {"type": "try_it", "title": "HTTP vs HTTPS", "content": "Protocol differences and security.", "language": "python"},
            {"type": "solution", "title": "Load Balancing & CDN", "content": "How they work in distributed systems."},
        ],
    },
    "os-fundamentals": {
        "title": "Operating Systems Fundamentals",
        "phase": "advanced",
        "topic": "os",
        "difficulty": "intermediate",
        "estimated_time_minutes": 60,
        "xp_reward": 150,
        "steps": [
            {"type": "theory", "title": "Process vs Thread", "content": "Concurrency and parallelism."},
            {"type": "example", "title": "CPU Scheduling", "content": "FCFS, SJF, Round Robin, Priority."},
            {"type": "try_it", "title": "Deadlock Prevention", "content": "Banker's algorithm example.", "language": "python"},
            {"type": "solution", "title": "Memory Management", "content": "Paging, segmentation, and virtual memory."},
        ],
    },
    "behavioral-stars": {
        "title": "Behavioral Interview - STAR Method",
        "phase": "job-ready",
        "topic": "behavioral",
        "difficulty": "beginner",
        "estimated_time_minutes": 40,
        "xp_reward": 100,
        "steps": [
            {"type": "theory", "title": "STAR Method", "content": "Situation, Task, Action, Result framework."},
            {"type": "example", "title": "Sample STAR Answer", "content": "Walkthrough of a strong behavioral answer."},
            {"type": "try_it", "title": "Write Your Own Story", "content": "Draft a STAR answer for a conflict situation."},
            {"type": "solution", "title": "Common Pitfalls", "content": "What to avoid in behavioral interviews."},
        ],
    },
    "amazon-lp": {
        "title": "Amazon Leadership Principles",
        "phase": "job-ready",
        "topic": "behavioral",
        "difficulty": "intermediate",
        "estimated_time_minutes": 50,
        "xp_reward": 130,
        "steps": [
            {"type": "theory", "title": "14 Leadership Principles", "content": "Overview of all Amazon LPs."},
            {"type": "example", "title": "Customer Obsession Story", "content": "Sample LP-aligned answer."},
            {"type": "try_it", "title": "Map Your Experiences", "content": "Match your past to specific LPs."},
            {"type": "solution", "title": "LP-Specific Tips", "content": "How to structure answers for each LP."},
        ],
    },
    "google-googliness": {
        "title": "Googleyness & Leadership",
        "phase": "job-ready",
        "topic": "behavioral",
        "difficulty": "intermediate",
        "estimated_time_minutes": 45,
        "xp_reward": 120,
        "steps": [
            {"type": "theory", "title": "Google's Core Values", "content": "Focus on the user, think 10x, ship."},
            {"type": "example", "title": "Googleyness in Action", "content": "Sample answer showing intellectual humility."},
            {"type": "try_it", "title": "Draft Your Story", "content": "Write about a time you learned from failure."},
            {"type": "solution", "title": "Google Behavioral Tips", "content": "What Google interviewers look for."},
        ],
    },
    # Data Analyst Modules
    "sql-fundamentals": {
        "title": "SQL Fundamentals",
        "phase": "foundation",
        "topic": "sql",
        "difficulty": "beginner",
        "estimated_time_minutes": 60,
        "xp_reward": 150,
        "steps": [
            {"type": "theory", "title": "SELECT, WHERE, ORDER BY", "content": "Basic SQL query structure."},
            {"type": "example", "title": "Filtering & Sorting", "content": "Practical examples of SELECT statements."},
            {"type": "try_it", "title": "Write Your First Query", "content": "Query a sample database.", "language": "sql"},
            {"type": "solution", "title": "Common Mistakes", "content": "NULL handling, case sensitivity, and more."},
        ],
    },
    "sql-window-functions": {
        "title": "SQL Window Functions",
        "phase": "core",
        "topic": "sql",
        "difficulty": "intermediate",
        "estimated_time_minutes": 55,
        "xp_reward": 140,
        "steps": [
            {"type": "theory", "title": "Window Function Basics", "content": "PARTITION BY, ORDER BY, and frame clauses."},
            {"type": "example", "title": "ROW_NUMBER & RANK", "content": "Ranking within groups."},
            {"type": "try_it", "title": "Running Totals", "content": "Calculate cumulative metrics.", "language": "sql"},
            {"type": "solution", "title": "LAG & LEAD", "content": "Accessing previous/next rows."},
        ],
    },
    "python-pandas": {
        "title": "Python Pandas for Data Analysis",
        "phase": "core",
        "topic": "python",
        "difficulty": "intermediate",
        "estimated_time_minutes": 70,
        "xp_reward": 180,
        "steps": [
            {"type": "theory", "title": "DataFrames & Series", "content": "Core pandas data structures."},
            {"type": "example", "title": "Reading & Writing Data", "content": "CSV, JSON, Excel, and SQL."},
            {"type": "try_it", "title": "GroupBy & Aggregation", "content": "Split-apply-combine pattern.", "language": "python"},
            {"type": "try_it", "title": "Merging DataFrames", "content": "Joins in pandas.", "language": "python"},
            {"type": "solution", "title": "Performance Tips", "content": "Vectorization and avoiding loops."},
        ],
    },
    "numpy-fundamentals": {
        "title": "NumPy Fundamentals",
        "phase": "core",
        "topic": "python",
        "difficulty": "intermediate",
        "estimated_time_minutes": 50,
        "xp_reward": 130,
        "steps": [
            {"type": "theory", "title": "NumPy Arrays", "content": "ndarray basics and operations."},
            {"type": "example", "title": "Broadcasting", "content": "How arrays of different shapes interact."},
            {"type": "try_it", "title": "Array Operations", "content": "Reshape, slice, and compute.", "language": "python"},
            {"type": "solution", "title": "NumPy vs Python Lists", "content": "Performance comparison."},
        ],
    },
    "stats-intro": {
        "title": "Statistics Introduction",
        "phase": "foundation",
        "topic": "statistics",
        "difficulty": "beginner",
        "estimated_time_minutes": 50,
        "xp_reward": 120,
        "steps": [
            {"type": "theory", "title": "Descriptive Statistics", "content": "Mean, median, mode, variance, std dev."},
            {"type": "example", "title": "Distribution Shapes", "content": "Normal, skewed, and bimodal."},
            {"type": "try_it", "title": "Calculate Statistics", "content": "Compute summary statistics.", "language": "python"},
            {"type": "solution", "title": "When to Use Which", "content": "Choosing the right measure."},
        ],
    },
    "probability-fundamentals": {
        "title": "Probability Fundamentals",
        "phase": "foundation",
        "topic": "statistics",
        "difficulty": "beginner",
        "estimated_time_minutes": 45,
        "xp_reward": 110,
        "steps": [
            {"type": "theory", "title": "Probability Basics", "content": "Sample space, events, and axioms."},
            {"type": "example", "title": "Bayes' Theorem", "content": "Conditional probability in action."},
            {"type": "try_it", "title": "Solve Probability Problems", "content": "Practice problems.", "language": "python"},
            {"type": "solution", "title": "Common Pitfalls", "content": "Independence, confounding, and more."},
        ],
    },
    "hypothesis-testing": {
        "title": "Hypothesis Testing",
        "phase": "core",
        "topic": "statistics",
        "difficulty": "intermediate",
        "estimated_time_minutes": 60,
        "xp_reward": 150,
        "steps": [
            {"type": "theory", "title": "Hypothesis Testing Framework", "content": "Null, alternative, p-value, significance."},
            {"type": "example", "title": "t-test Walkthrough", "content": "One-sample and two-sample t-tests."},
            {"type": "try_it", "title": "Conduct a Test", "content": "Perform hypothesis testing on data.", "language": "python"},
            {"type": "solution", "title": "Type I vs Type II Errors", "content": "Understanding error types."},
        ],
    },
    "inferential-stats": {
        "title": "Inferential Statistics",
        "phase": "core",
        "topic": "statistics",
        "difficulty": "intermediate",
        "estimated_time_minutes": 55,
        "xp_reward": 140,
        "steps": [
            {"type": "theory", "title": "Confidence Intervals", "content": "How to construct and interpret CIs."},
            {"type": "example", "title": "Chi-Square Test", "content": "Testing categorical independence."},
            {"type": "try_it", "title": "ANOVA", "content": "Compare means across groups.", "language": "python"},
            {"type": "solution", "title": "When to Use Which Test", "content": "Test selection guide."},
        ],
    },
    "ab-testing-deep-dive": {
        "title": "A/B Testing Deep Dive",
        "phase": "advanced",
        "topic": "ab-testing",
        "difficulty": "advanced",
        "estimated_time_minutes": 70,
        "xp_reward": 200,
        "steps": [
            {"type": "theory", "title": "Experiment Design", "content": "Hypothesis, metrics, randomization."},
            {"type": "example", "title": "Sample Size Calculation", "content": "Power analysis in practice."},
            {"type": "try_it", "title": "Analyze an A/B Test", "content": "Real-world A/B test analysis.", "language": "python"},
            {"type": "try_it", "title": "Novelty & Primacy Effects", "content": "Common pitfalls in experimentation."},
            {"type": "solution", "title": "Sequential Testing", "content": "Advanced methods for peeking."},
        ],
    },
    "tableau-mastery": {
        "title": "Tableau Mastery",
        "phase": "advanced",
        "topic": "visualization",
        "difficulty": "intermediate",
        "estimated_time_minutes": 65,
        "xp_reward": 170,
        "steps": [
            {"type": "theory", "title": "Tableau Fundamentals", "content": "Worksheets, dashboards, and stories."},
            {"type": "example", "title": "Calculated Fields", "content": "Custom metrics and aggregations."},
            {"type": "try_it", "title": "Build a Dashboard", "content": "Create an interactive dashboard.", "language": "sql"},
            {"type": "solution", "title": "LOD Expressions", "content": "Level of detail calculations."},
        ],
    },
    "power-bi": {
        "title": "Power BI",
        "phase": "advanced",
        "topic": "visualization",
        "difficulty": "intermediate",
        "estimated_time_minutes": 60,
        "xp_reward": 160,
        "steps": [
            {"type": "theory", "title": "Power BI Basics", "content": "Desktop, Service, and Mobile."},
            {"type": "example", "title": "DAX Formulas", "content": "Data Analysis Expressions."},
            {"type": "try_it", "title": "Power Query", "content": "Data transformation.", "language": "sql"},
            {"type": "solution", "title": "Data Modeling", "content": "Star schema and relationships."},
        ],
    },
    "case-study-frameworks": {
        "title": "Case Study Frameworks",
        "phase": "advanced",
        "topic": "business",
        "difficulty": "intermediate",
        "estimated_time_minutes": 55,
        "xp_reward": 140,
        "steps": [
            {"type": "theory", "title": "Structured Problem Solving", "content": "Frameworks for business cases."},
            {"type": "example", "title": "Metric Tree", "content": "How to decompose metrics."},
            {"type": "try_it", "title": "Solve a Case", "content": "Practice business case analysis."},
            {"type": "solution", "title": "Communication Tips", "content": "Presenting insights effectively."},
        ],
    },
    "product-metrics": {
        "title": "Product Metrics & KPIs",
        "phase": "job-ready",
        "topic": "product",
        "difficulty": "intermediate",
        "estimated_time_minutes": 50,
        "xp_reward": 130,
        "steps": [
            {"type": "theory", "title": "North Star Metric", "content": "Defining product success."},
            {"type": "example", "title": "Funnel & Cohort Analysis", "content": "User behavior metrics."},
            {"type": "try_it", "title": "Define KPIs", "content": "Set metrics for a product."},
            {"type": "solution", "title": "Counter Metrics", "content": "Balancing growth and quality."},
        ],
    },
    "data-preprocessing": {
        "title": "Data Preprocessing",
        "phase": "core",
        "topic": "data-cleaning",
        "difficulty": "intermediate",
        "estimated_time_minutes": 50,
        "xp_reward": 130,
        "steps": [
            {"type": "theory", "title": "Missing Data Strategies", "content": "Imputation, deletion, and prediction."},
            {"type": "example", "title": "Outlier Detection", "content": "IQR, z-score, and isolation forest."},
            {"type": "try_it", "title": "Clean a Dataset", "content": "Handle missing values and outliers.", "language": "python"},
            {"type": "solution", "title": "Feature Scaling", "content": "Normalization and standardization."},
        ],
    },
    "excel-advanced": {
        "title": "Advanced Excel",
        "phase": "foundation",
        "topic": "tools",
        "difficulty": "beginner",
        "estimated_time_minutes": 55,
        "xp_reward": 140,
        "steps": [
            {"type": "theory", "title": "Advanced Formulas", "content": "VLOOKUP, INDEX-MATCH, XLOOKUP."},
            {"type": "example", "title": "Pivot Tables", "content": "Summarize and analyze data."},
            {"type": "try_it", "title": "Build a Dashboard", "content": "Create an interactive Excel dashboard."},
            {"type": "solution", "title": "Power Query", "content": "ETL in Excel."},
        ],
    },
    "r-programming": {
        "title": "R Programming Basics",
        "phase": "core",
        "topic": "r",
        "difficulty": "intermediate",
        "estimated_time_minutes": 55,
        "xp_reward": 140,
        "steps": [
            {"type": "theory", "title": "R Data Structures", "content": "Vectors, lists, data frames."},
            {"type": "example", "title": "dplyr for Data Manipulation", "content": "Filter, mutate, group_by, summarize."},
            {"type": "try_it", "title": "ggplot2 Visualization", "content": "Grammar of graphics.", "language": "r"},
            {"type": "solution", "title": "R Markdown", "content": "Reproducible reports."},
        ],
    },
    "ggplot2": {
        "title": "ggplot2 Visualization",
        "phase": "core",
        "topic": "r",
        "difficulty": "intermediate",
        "estimated_time_minutes": 45,
        "xp_reward": 120,
        "steps": [
            {"type": "theory", "title": "Grammar of Graphics", "content": "Aesthetics, geoms, and facets."},
            {"type": "example", "title": "Common Plot Types", "content": "Scatter, bar, line, box."},
            {"type": "try_it", "title": "Customize Themes", "content": "Make publication-quality plots.", "language": "r"},
            {"type": "solution", "title": "Advanced Visualizations", "content": "Heatmaps, facet grids, and more."},
        ],
    },
    # AI/ML Modules
    "python-for-ml": {
        "title": "Python for Machine Learning",
        "phase": "foundation",
        "topic": "python",
        "difficulty": "beginner",
        "estimated_time_minutes": 60,
        "xp_reward": 150,
        "steps": [
            {"type": "theory", "title": "Python Refresher", "content": "Lists, dicts, comprehensions, functions."},
            {"type": "example", "title": "NumPy Basics", "content": "Arrays and operations."},
            {"type": "try_it", "title": "Pandas DataFrames", "content": "Load and explore data.", "language": "python"},
            {"type": "solution", "title": "Best Practices", "content": "Code organization for ML."},
        ],
    },
    "linear-algebra": {
        "title": "Linear Algebra for ML",
        "phase": "foundation",
        "topic": "math",
        "difficulty": "intermediate",
        "estimated_time_minutes": 60,
        "xp_reward": 150,
        "steps": [
            {"type": "theory", "title": "Vectors & Matrices", "content": "Operations and properties."},
            {"type": "example", "title": "Matrix Multiplication", "content": "Step-by-step computation."},
            {"type": "try_it", "title": "Implement Operations", "content": "Code basic linear algebra.", "language": "python"},
            {"type": "solution", "title": "Eigenvalues & SVD", "content": "Decomposition techniques."},
        ],
    },
    "calculus": {
        "title": "Calculus for ML",
        "phase": "foundation",
        "topic": "math",
        "difficulty": "intermediate",
        "estimated_time_minutes": 55,
        "xp_reward": 140,
        "steps": [
            {"type": "theory", "title": "Derivatives & Gradients", "content": "Partial derivatives and chain rule."},
            {"type": "example", "title": "Gradient Descent", "content": "Optimization algorithm."},
            {"type": "try_it", "title": "Implement Gradient Descent", "content": "Code from scratch.", "language": "python"},
            {"type": "solution", "title": "Backpropagation", "content": "Chain rule in neural networks."},
        ],
    },
    "probability-stats": {
        "title": "Probability & Statistics for ML",
        "phase": "foundation",
        "topic": "math",
        "difficulty": "intermediate",
        "estimated_time_minutes": 60,
        "xp_reward": 150,
        "steps": [
            {"type": "theory", "title": "Probability Distributions", "content": "Normal, binomial, Poisson."},
            {"type": "example", "title": "Bayes' Theorem", "content": "Conditional probability."},
            {"type": "try_it", "title": "Simulate Distributions", "content": "Monte Carlo simulation.", "language": "python"},
            {"type": "solution", "title": "Information Theory", "content": "Entropy and KL divergence."},
        ],
    },
    "ml-intro": {
        "title": "Machine Learning Introduction",
        "phase": "foundation",
        "topic": "ml",
        "difficulty": "beginner",
        "estimated_time_minutes": 65,
        "xp_reward": 170,
        "steps": [
            {"type": "theory", "title": "What is ML?", "content": "Supervised, unsupervised, reinforcement."},
            {"type": "example", "title": "Linear Regression", "content": "From scratch implementation."},
            {"type": "try_it", "title": "Train a Model", "content": "Use scikit-learn.", "language": "python"},
            {"type": "solution", "title": "Bias-Variance Tradeoff", "content": "Understanding model performance."},
        ],
    },
    "supervised-learning": {
        "title": "Supervised Learning",
        "phase": "core",
        "topic": "ml",
        "difficulty": "intermediate",
        "estimated_time_minutes": 70,
        "xp_reward": 180,
        "steps": [
            {"type": "theory", "title": "Classification vs Regression", "content": "Problem types and algorithms."},
            {"type": "example", "title": "Decision Trees", "content": "How trees split data."},
            {"type": "try_it", "title": "Random Forest", "content": "Ensemble method.", "language": "python"},
            {"type": "try_it", "title": "XGBoost", "content": "Gradient boosting library.", "language": "python"},
            {"type": "solution", "title": "Model Selection", "content": "Choosing the right algorithm."},
        ],
    },
    "unsupervised-learning": {
        "title": "Unsupervised Learning",
        "phase": "core",
        "topic": "ml",
        "difficulty": "intermediate",
        "estimated_time_minutes": 55,
        "xp_reward": 140,
        "steps": [
            {"type": "theory", "title": "Clustering", "content": "K-means, hierarchical, DBSCAN."},
            {"type": "example", "title": "Dimensionality Reduction", "content": "PCA and t-SNE."},
            {"type": "try_it", "title": "Customer Segmentation", "content": "Cluster e-commerce data.", "language": "python"},
            {"type": "solution", "title": "Anomaly Detection", "content": "Isolation forest and autoencoders."},
        ],
    },
    "deep-learning-basics": {
        "title": "Deep Learning Basics",
        "phase": "core",
        "topic": "dl",
        "difficulty": "intermediate",
        "estimated_time_minutes": 75,
        "xp_reward": 200,
        "steps": [
            {"type": "theory", "title": "Neural Networks", "content": "Perceptrons, layers, activation functions."},
            {"type": "example", "title": "Backpropagation", "content": "How networks learn."},
            {"type": "try_it", "title": "Build an MLP", "content": "Multi-layer perceptron.", "language": "python"},
            {"type": "solution", "title": "Optimization", "content": "SGD, Adam, learning rate scheduling."},
        ],
    },
    "cnn-architectures": {
        "title": "CNN Architectures",
        "phase": "core",
        "topic": "dl",
        "difficulty": "advanced",
        "estimated_time_minutes": 65,
        "xp_reward": 180,
        "steps": [
            {"type": "theory", "title": "Convolution & Pooling", "content": "How CNNs work."},
            {"type": "example", "title": "ResNet Architecture", "content": "Skip connections and deep networks."},
            {"type": "try_it", "title": "Image Classification", "content": "Train a CNN on CIFAR-10.", "language": "python"},
            {"type": "solution", "title": "Transfer Learning", "content": "Use pre-trained models."},
        ],
    },
    "rnn-lstm": {
        "title": "RNN, LSTM & Sequence Models",
        "phase": "core",
        "topic": "dl",
        "difficulty": "advanced",
        "estimated_time_minutes": 65,
        "xp_reward": 180,
        "steps": [
            {"type": "theory", "title": "Recurrent Networks", "content": "Sequential data processing."},
            {"type": "example", "title": "LSTM & GRU", "content": "Gating mechanisms."},
            {"type": "try_it", "title": "Text Generation", "content": "Character-level RNN.", "language": "python"},
            {"type": "solution", "title": "When to Use RNNs", "content": "vs transformers and other architectures."},
        ],
    },
    "pytorch-basics": {
        "title": "PyTorch Basics",
        "phase": "core",
        "topic": "framework",
        "difficulty": "intermediate",
        "estimated_time_minutes": 65,
        "xp_reward": 170,
        "steps": [
            {"type": "theory", "title": "Tensors & Autograd", "content": "PyTorch fundamentals."},
            {"type": "example", "title": "nn.Module", "content": "Building custom models."},
            {"type": "try_it", "title": "Train a Model", "content": "Full training loop.", "language": "python"},
            {"type": "solution", "title": "GPU Acceleration", "content": "CUDA and distributed training."},
        ],
    },
    "pytorch-advanced": {
        "title": "PyTorch Advanced",
        "phase": "advanced",
        "topic": "framework",
        "difficulty": "advanced",
        "estimated_time_minutes": 70,
        "xp_reward": 200,
        "steps": [
            {"type": "theory", "title": "Custom Datasets", "content": "DataLoader and transforms."},
            {"type": "example", "title": "Distributed Training", "content": "DDP and FSDP."},
            {"type": "try_it", "title": "Mixed Precision", "content": "AMP for faster training.", "language": "python"},
            {"type": "solution", "title": "ONNX Export", "content": "Model serialization."},
        ],
    },
    "tensorflow-keras": {
        "title": "TensorFlow & Keras",
        "phase": "core",
        "topic": "framework",
        "difficulty": "intermediate",
        "estimated_time_minutes": 60,
        "xp_reward": 160,
        "steps": [
            {"type": "theory", "title": "Keras API", "content": "Sequential and Functional models."},
            {"type": "example", "title": "tf.data Pipeline", "content": "Efficient data loading."},
            {"type": "try_it", "title": "Train with Keras", "content": "Build and train a model.", "language": "python"},
            {"type": "solution", "title": "TensorBoard", "content": "Visualization and debugging."},
        ],
    },
    "nlp-fundamentals": {
        "title": "NLP Fundamentals",
        "phase": "core",
        "topic": "nlp",
        "difficulty": "intermediate",
        "estimated_time_minutes": 65,
        "xp_reward": 170,
        "steps": [
            {"type": "theory", "title": "Text Preprocessing", "content": "Tokenization, stemming, lemmatization."},
            {"type": "example", "title": "Word Embeddings", "content": "Word2Vec, GloVe, FastText."},
            {"type": "try_it", "title": "Sentiment Analysis", "content": "Build a text classifier.", "language": "python"},
            {"type": "solution", "title": "NER & POS Tagging", "content": "Sequence labeling tasks."},
        ],
    },
    "transformers-llms": {
        "title": "Transformers & LLMs",
        "phase": "advanced",
        "topic": "nlp",
        "difficulty": "advanced",
        "estimated_time_minutes": 80,
        "xp_reward": 250,
        "steps": [
            {"type": "theory", "title": "Attention Mechanism", "content": "Self-attention and multi-head."},
            {"type": "example", "title": "BERT & GPT", "content": "Encoder vs decoder architectures."},
            {"type": "try_it", "title": "Fine-tune a Model", "content": "Hugging Face transformers.", "language": "python"},
            {"type": "try_it", "title": "RAG Implementation", "content": "Retrieval-augmented generation.", "language": "python"},
            {"type": "solution", "title": "Prompt Engineering", "content": "Techniques for LLM applications."},
        ],
    },
    "cv-basics": {
        "title": "Computer Vision Basics",
        "phase": "core",
        "topic": "cv",
        "difficulty": "intermediate",
        "estimated_time_minutes": 60,
        "xp_reward": 160,
        "steps": [
            {"type": "theory", "title": "Image Processing", "content": "Filters, edges, and features."},
            {"type": "example", "title": "Object Detection", "content": "YOLO, Faster R-CNN."},
            {"type": "try_it", "title": "Image Classification", "content": "Train a CNN.", "language": "python"},
            {"type": "solution", "title": "Segmentation", "content": "Semantic and instance segmentation."},
        ],
    },
    "object-detection": {
        "title": "Object Detection",
        "phase": "advanced",
        "topic": "cv",
        "difficulty": "advanced",
        "estimated_time_minutes": 65,
        "xp_reward": 180,
        "steps": [
            {"type": "theory", "title": "Detection Pipelines", "content": "Two-stage vs one-stage detectors."},
            {"type": "example", "title": "YOLO Architecture", "content": "Real-time detection."},
            {"type": "try_it", "title": "Custom Detector", "content": "Train on your own data.", "language": "python"},
            {"type": "solution", "title": "Evaluation Metrics", "content": "mAP, IoU, and NMS."},
        ],
    },
    "mlops-pipeline": {
        "title": "MLOps Pipeline",
        "phase": "advanced",
        "topic": "mlops",
        "difficulty": "advanced",
        "estimated_time_minutes": 70,
        "xp_reward": 200,
        "steps": [
            {"type": "theory", "title": "MLOps Overview", "content": "From research to production."},
            {"type": "example", "title": "MLflow Tracking", "content": "Experiment management."},
            {"type": "try_it", "title": "Build a Pipeline", "content": "End-to-end ML pipeline.", "language": "python"},
            {"type": "solution", "title": "CI/CD for ML", "content": "Automated training and deployment."},
        ],
    },
    "model-deployment": {
        "title": "Model Deployment",
        "phase": "advanced",
        "topic": "mlops",
        "difficulty": "advanced",
        "estimated_time_minutes": 60,
        "xp_reward": 170,
        "steps": [
            {"type": "theory", "title": "Deployment Strategies", "content": "REST, gRPC, batch, streaming."},
            {"type": "example", "title": "FastAPI for ML", "content": "Serve predictions via API."},
            {"type": "try_it", "title": "Dockerize a Model", "content": "Container deployment.", "language": "python"},
            {"type": "solution", "title": "Cloud Deployment", "content": "AWS, GCP, Azure options."},
        ],
    },
    "model-monitoring": {
        "title": "Model Monitoring",
        "phase": "advanced",
        "topic": "mlops",
        "difficulty": "advanced",
        "estimated_time_minutes": 55,
        "xp_reward": 150,
        "steps": [
            {"type": "theory", "title": "Drift Detection", "content": "Data and concept drift."},
            {"type": "example", "title": "Performance Monitoring", "content": "Track metrics over time."},
            {"type": "try_it", "title": "Set Up Alerts", "content": "Notify on degradation.", "language": "python"},
            {"type": "solution", "title": "Retraining Strategies", "content": "When and how to retrain."},
        ],
    },
    "feature-engineering": {
        "title": "Feature Engineering",
        "phase": "core",
        "topic": "ml",
        "difficulty": "intermediate",
        "estimated_time_minutes": 60,
        "xp_reward": 160,
        "steps": [
            {"type": "theory", "title": "Feature Creation", "content": "Domain-driven features."},
            {"type": "example", "title": "Categorical Encoding", "content": "One-hot, target, embeddings."},
            {"type": "try_it", "title": "Feature Selection", "content": "Reduce dimensionality.", "language": "python"},
            {"type": "solution", "title": "Feature Stores", "content": "Centralized feature management."},
        ],
    },
    "model-evaluation": {
        "title": "Model Evaluation",
        "phase": "advanced",
        "topic": "ml",
        "difficulty": "intermediate",
        "estimated_time_minutes": 50,
        "xp_reward": 140,
        "steps": [
            {"type": "theory", "title": "Classification Metrics", "content": "Precision, recall, F1, ROC-AUC."},
            {"type": "example", "title": "Regression Metrics", "content": "MSE, RMSE, MAE, R²."},
            {"type": "try_it", "title": "Cross-Validation", "content": "K-fold and stratified.", "language": "python"},
            {"type": "solution", "title": "Hyperparameter Tuning", "content": "Grid, random, Bayesian search."},
        ],
    },
    "ml-system-design": {
        "title": "ML System Design",
        "phase": "job-ready",
        "topic": "system-design",
        "difficulty": "advanced",
        "estimated_time_minutes": 90,
        "xp_reward": 300,
        "steps": [
            {"type": "theory", "title": "ML System Components", "content": "Data, features, models, serving."},
            {"type": "example", "title": "Design Recommendation System", "content": "End-to-end ML system."},
            {"type": "try_it", "title": "Design Search Ranking", "content": "Real-time ML pipeline."},
            {"type": "solution", "title": "Scaling ML Systems", "content": "Handle millions of predictions."},
        ],
    },
    "aptitude-quant": {
        "title": "Quantitative Aptitude",
        "phase": "job-ready",
        "topic": "aptitude",
        "difficulty": "beginner",
        "estimated_time_minutes": 50,
        "xp_reward": 120,
        "steps": [
            {"type": "theory", "title": "Percentages & Ratios", "content": "Basic arithmetic for placement."},
            {"type": "example", "title": "Profit & Loss", "content": "Commercial math."},
            {"type": "try_it", "title": "Time & Work Problems", "content": "Practice problems."},
            {"type": "solution", "title": "Time, Speed, Distance", "content": "Motion problems."},
        ],
    },
    "aptitude-logical": {
        "title": "Logical Reasoning",
        "phase": "job-ready",
        "topic": "aptitude",
        "difficulty": "beginner",
        "estimated_time_minutes": 45,
        "xp_reward": 110,
        "steps": [
            {"type": "theory", "title": "Pattern Recognition", "content": "Series and sequences."},
            {"type": "example", "title": "Blood Relations", "content": "Family tree puzzles."},
            {"type": "try_it", "title": "Syllogisms", "content": "Logical deduction."},
            {"type": "solution", "title": "Coding-Decoding", "content": "Pattern-based decoding."},
        ],
    },
    "mock-ai-interview": {
        "title": "AI Engineer Mock Interview",
        "phase": "job-ready",
        "topic": "interview",
        "difficulty": "advanced",
        "estimated_time_minutes": 60,
        "xp_reward": 200,
        "steps": [
            {"type": "theory", "title": "Interview Structure", "content": "What to expect in AI interviews."},
            {"type": "example", "title": "ML Coding Round", "content": "Sample coding question."},
            {"type": "try_it", "title": "System Design Round", "content": "Design an ML system."},
            {"type": "solution", "title": "Behavioral Round", "content": "Tell your story effectively."},
        ],
    },
    "mock-analyst-interview": {
        "title": "Data Analyst Mock Interview",
        "phase": "job-ready",
        "topic": "interview",
        "difficulty": "intermediate",
        "estimated_time_minutes": 60,
        "xp_reward": 200,
        "steps": [
            {"type": "theory", "title": "Analyst Interview Format", "content": "SQL, stats, and case studies."},
            {"type": "example", "title": "SQL Interview", "content": "Common SQL questions."},
            {"type": "try_it", "title": "Case Study Practice", "content": "Business problem solving."},
            {"type": "solution", "title": "Stats Interview", "content": "Probability and hypothesis testing."},
        ],
    },
}


# =============================================================
# COMPANY-SPECIFIC PATHS
# =============================================================

COMPANY_PATHS: Dict[str, Dict[str, Any]] = {
    "amazon": {
        "display_name": "Amazon",
        "icon": "🟠",
        "color": "#FF9900",
        "process": [
            "Online Assessment (2 coding + debugging)",
            "Phone Screen (1 coding + behavioral)",
            "Onsite Loop (4-5 rounds: coding, system design, behavioral)",
            "Bar Raiser Round",
        ],
        "focus_skills": ["arrays-hashing", "dynamic-programming", "trees", "graphs", "system-design", "leadership-principles"],
        "question_count": 150,
        "duration_weeks": 6,
        "difficulty_mix": {"easy": 30, "medium": 80, "hard": 40},
        "key_topics": [
            "Two Sum & variations",
            "LRU Cache",
            "Word Ladder",
            "Serialize/Deserialize Tree",
            "Design Twitter",
            "14 Leadership Principles",
            "System Design: URL Shortener, Design Amazon",
        ],
        "behavioral_focus": "14 Leadership Principles - Customer Obsession, Ownership, Bias for Action, Dive Deep, Frugality",
    },
    "google": {
        "display_name": "Google",
        "icon": "🔴",
        "color": "#4285F4",
        "process": [
            "Online Assessment (1-2 coding)",
            "Phone Screen (1 coding)",
            "Onsite (4-5 rounds: coding, system design, Googliness)",
        ],
        "focus_skills": ["graphs", "dynamic-programming", "trees", "system-design", "transformers"],
        "question_count": 120,
        "duration_weeks": 8,
        "difficulty_mix": {"easy": 20, "medium": 60, "hard": 40},
        "key_topics": [
            "Word Ladder",
            "Edit Distance",
            "Number of Islands",
            "Design Search Autocomplete",
            "Design YouTube",
            "Googliness & Leadership",
            "ML System Design",
        ],
        "behavioral_focus": "Googliness - intellectual humility, bias to action, comfortable with ambiguity, collaboration",
    },
    "microsoft": {
        "display_name": "Microsoft",
        "icon": "🔵",
        "color": "#00A4EF",
        "process": [
            "Online Assessment",
            "Phone Screen",
            "Onsite (4-5 rounds)",
        ],
        "focus_skills": ["arrays-hashing", "linked-lists", "trees", "system-design", "oop"],
        "question_count": 100,
        "duration_weeks": 5,
        "difficulty_mix": {"easy": 30, "medium": 50, "hard": 20},
        "key_topics": [
            "Two Sum",
            "Reverse Linked List",
            "Validate BST",
            "Design URL Shortener",
            "STAR Method",
            "Growth Mindset",
        ],
        "behavioral_focus": "Growth mindset, customer obsession, diversity & inclusion",
    },
    "meta": {
        "display_name": "Meta",
        "icon": "🔷",
        "color": "#1877F2",
        "process": [
            "Coding Screen",
            "Onsite (4 rounds: coding, system design, behavioral)",
        ],
        "focus_skills": ["linked-lists", "trees", "dynamic-programming", "system-design"],
        "question_count": 100,
        "duration_weeks": 5,
        "difficulty_mix": {"easy": 20, "medium": 50, "hard": 30},
        "key_topics": [
            "Reverse Linked List",
            "Validate BST",
            "Word Break",
            "Design Instagram",
            "Move Fast",
        ],
        "behavioral_focus": "Move fast, be bold, be open, build social value",
    },
    "tcs": {
        "display_name": "TCS",
        "icon": "🔷",
        "color": "#0000FF",
        "process": [
            "TCS NQT (National Qualifier Test)",
            "Technical Interview",
            "Managerial Interview",
            "HR Interview",
        ],
        "focus_skills": ["aptitude", "arrays-hashing", "strings", "dbms", "programming-fundamentals"],
        "question_count": 80,
        "duration_weeks": 3,
        "difficulty_mix": {"easy": 50, "medium": 25, "hard": 5},
        "key_topics": [
            "NQT Pattern (Quant + Logical + Verbal + Coding)",
            "TCS CodeVita",
            "Basic Coding (1-2 problems)",
            "Technical MCQs (CS fundamentals)",
            "Project Discussion",
        ],
        "behavioral_focus": "Communication, confidence, basic HR questions",
    },
    "infosys": {
        "display_name": "Infosys",
        "icon": "🟢",
        "color": "#007CC0",
        "process": [
            "InfyTQ/Infosys Certification",
            "Online Test (Aptitude + Coding)",
            "Technical Interview",
            "HR Interview",
        ],
        "focus_skills": ["aptitude", "programming-fundamentals", "oop", "dbms"],
        "question_count": 70,
        "duration_weeks": 3,
        "difficulty_mix": {"easy": 45, "medium": 20, "hard": 5},
        "key_topics": [
            "Aptitude (Quant + Logical)",
            "Pseudo Code",
            "Basic Programming",
            "DBMS & SQL",
            "Project Discussion",
        ],
        "behavioral_focus": "Why Infosys, career goals, teamwork",
    },
    "wipro": {
        "display_name": "Wipro",
        "icon": "🟣",
        "color": "#7B1FA2",
        "process": [
            "Online Test (Aptitude + Coding)",
            "Technical Interview",
            "HR Interview",
        ],
        "focus_skills": ["aptitude", "programming-fundamentals", "networks"],
        "question_count": 60,
        "duration_weeks": 2,
        "difficulty_mix": {"easy": 40, "medium": 18, "hard": 2},
        "key_topics": [
            "Aptitude Test",
            "Coding (Easy-Medium)",
            "Technical MCQs",
            "Communication Skills",
        ],
        "behavioral_focus": "Communication, confidence, cultural fit",
    },
}


# =============================================================
# HELPER FUNCTIONS
# =============================================================

def get_phase(phase_id: str) -> Dict[str, Any] | None:
    return PHASES.get(phase_id)


def get_all_phases() -> List[Dict[str, Any]]:
    return list(PHASES.values())


def get_learning_module(module_id: str) -> Dict[str, Any] | None:
    return LEARNING_MODULE_CATALOG.get(module_id)


def get_all_learning_modules() -> Dict[str, Dict[str, Any]]:
    return LEARNING_MODULE_CATALOG


def get_modules_by_phase(phase: str) -> List[Dict[str, Any]]:
    return [m for m in LEARNING_MODULE_CATALOG.values() if m.get("phase") == phase]


def get_modules_by_topic(topic: str) -> List[Dict[str, Any]]:
    return [m for m in LEARNING_MODULE_CATALOG.values() if m.get("topic") == topic]


def get_company_path(company_id: str) -> Dict[str, Any] | None:
    return COMPANY_PATHS.get(company_id.lower())


def get_all_company_paths() -> Dict[str, Dict[str, Any]]:
    return COMPANY_PATHS


def get_curriculum_stats() -> Dict[str, Any]:
    """Get overall curriculum statistics."""
    total_modules = len(LEARNING_MODULE_CATALOG)
    total_companies = len(COMPANY_PATHS)
    phases_count = {phase: len(get_modules_by_phase(phase)) for phase in PHASES.keys()}

    difficulty_counts = {"beginner": 0, "intermediate": 0, "advanced": 0}
    for module in LEARNING_MODULE_CATALOG.values():
        diff = module.get("difficulty", "intermediate")
        if diff in difficulty_counts:
            difficulty_counts[diff] += 1

    total_xp = sum(m.get("xp_reward", 0) for m in LEARNING_MODULE_CATALOG.values())
    total_time = sum(m.get("estimated_time_minutes", 0) for m in LEARNING_MODULE_CATALOG.values())

    return {
        "version": CURRICULUM_VERSION,
        "generated": CURRICULUM_GENERATED,
        "total_modules": total_modules,
        "total_companies": total_companies,
        "modules_by_phase": phases_count,
        "modules_by_difficulty": difficulty_counts,
        "total_xp_available": total_xp,
        "total_time_minutes": total_time,
        "total_time_hours": round(total_time / 60, 1),
    }


# =============================================================
# EXPORTS
# =============================================================

__all__ = [
    "CURRICULUM_VERSION",
    "CURRICULUM_GENERATED",
    "PHASES",
    "LEARNING_MODULE_CATALOG",
    "COMPANY_PATHS",
    "get_phase",
    "get_all_phases",
    "get_learning_module",
    "get_all_learning_modules",
    "get_modules_by_phase",
    "get_modules_by_topic",
    "get_company_path",
    "get_all_company_paths",
    "get_curriculum_stats",
]
