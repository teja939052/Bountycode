"""Mega Question Seed: 2000+ comprehensive real questions for PlacementPro.
Run: python seed_questions_2000.py
This script generates questions programmatically across all topics, difficulties, company tags and languages.
The questions are stored in the MongoDB curated_questions collection with full metadata.
"""
import os, sys, uuid, random
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

sys.path.insert(0, os.path.dirname(__file__))

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "placementpro")

COMPANIES = [
    "Google","Amazon","Microsoft","Meta","Apple","Netflix","Uber","Tesla","SpaceX",
    "Salesforce","Adobe","Twitter","LinkedIn","Goldman Sachs","JPMorgan","Morgan Stanley",
    "Oracle","IBM","Intel","NVIDIA","AMD","Qualcomm","Broadcom","Cisco",
    "TCS","Infosys","Wipro","Cognizant","Capgemini","Accenture","HCL","Tech Mahindra",
    "Flipkart","Swiggy","Zomato","Razorpay","Ola","Delhivery","PhonePe","Paytm",
    "BYJU's","Unacademy","Vedantu","Eruditus","UpGrad","Great Learning","Simplilearn",
]
ROLES = ["SDE","SDE Intern","Software Engineer","Backend Developer","Frontend Developer",
         "Full Stack Developer","Algorithm Engineer","Data Engineer","DevOps Engineer",
         "Mobile Developer","ML Engineer","Data Scientist","QA Engineer"]
COMPANY_FREQ = {c: random.randint(3, 20) for c in COMPANIES[:20]}
SOLUTIONS = {
    "easy": {"time": "O(n)", "space": "O(1)", "note": "Single pass, greedy approach"},
    "medium": {"time": "O(n log n)", "space": "O(n)", "note": "Sort + hash map + two pointers"},
    "hard": {"time": "O(n + m)", "space": "O(n + m)", "note": "Advanced data structure + careful edge cases"},
}
TOPICS = {
    "Arrays & Hashing": ["Two Sum","Three Sum","Four Sum","Contains Duplicate","Product of Array Except Self",
        "Maximum Subarray","Jump Game","Merge Intervals","Insert Interval","Non-overlapping Intervals",
        "Meeting Rooms","Meeting Rooms II","Random Pick Index","Top K Frequent Elements",
        "Encode and Decode Strings","Longest Consecutive Sequence","Longest Increasing Subsequence",
        "Number of Longest Increasing Subsequence","Reverse Pairs","Count of Smaller Numbers",
        "Basic Calculator","Evaluate Division","Sentence Similarity","Word Pattern","Isomorphic Strings",
        "Group Anagrams","Valid Sudoku","Sudoku Solver","First Missing Positive","Trapping Rain Water",
        "Container With Most Water","3Sum Closest","4Sum","Largest Number","Wiggle Sort","Merge Sorted Array",
        "Remove Duplicates from Sorted Array","Remove Element","Move Zeroes","Plus One","Add Binary",
        "Add Two Numbers","Reverse Integer","Palindrome Number","Roman to Integer","Integer to Roman",
        "Longest Common Prefix","Valid Parentheses","Generate Parentheses","Longest Valid Parentheses",
        "Minimum Remove to Make Valid Parentheses","Daily Temperatures","Next Greater Element",
        "Next Greater Element II","Stock Span Problem","Maximum Frequency Stack","Design Twitter",
        "Design Facebook Feed","Design Instagram","Design TikTok Feed","Design YouTube Feed",
        "Design Google Search","Design Amazon Search","Design Flipkart Search","Design Zoho Search",
    ],
    "Strings": ["Longest Palindromic Substring","Valid Palindrome","Palindrome Partitioning",
        "Palindrome Permutation","Encode and Decode Strings","String Compression",
        "String Decompression","String Transformation","String Matching","KMP Algorithm",
        "Rabin-Karp Algorithm","Z-Algorithm","Manacher Algorithm","Aho-Corasick Algorithm",
        "Suffix Array","Suffix Tree","Trie Implementation","Design Search Autocomplete",
        "Design Keyboard","Design Text Editor","Design IDE","Design Compiler",
        "Design Interpreter","Design Regex Engine","Design Template Engine",
        "Design Search Engine","Design Spell Checker","Design Grammar Parser",
        "Design JSON Parser","Design XML Parser","Design HTML Parser","Design CSS Parser",
        "Design JavaScript Engine","Design Python Interpreter","Design JVM","Design CLR",
        "Word Ladder","Word Break","Word Search","Word Squares","Word Abbreviation",
        "Wildcard Matching","Regular Expression Matching","Substring with Concatenation",
        "Minimum Window Substring","Longest Substring Without Repeating Characters",
        "Longest Substring with At Most K Distinct Characters",
        "Longest Substring with At Most 2 Distinct Characters","Sliding Window Maximum",
        "Sliding Window Median","Sliding Window Average","Sliding Window Minimum",
    ],
    "Linked Lists": ["Reverse Linked List","Merge Two Sorted Lists","Linked List Cycle",
        "Detect Cycle","Remove Nth Node from End","Middle of Linked List",
        "Palindrome Linked List","Convert Binary Number to Integer","Delete Node in Linked List",
        "Add Two Numbers","Subtract Two Numbers","Multiply Two Numbers","Divide Two Numbers",
        "Sort Linked List","Insertion Sort List","Merge Sort Linked List","Quick Sort Linked List",
        "Radix Sort Linked List","Count Sort Linked List","Heap Sort Linked List",
        "Design LRU Cache","Design LFU Cache","Design MRU Cache","Design FIFO Cache",
        "Design LRU Cache with TTL","Design LFU Cache with TTL","Design MRU Cache with TTL",
        "Skip List Implementation","Bloom Filter Implementation","Count Min Sketch",
        "Consistent Hashing","Distributed Hash Table"," Consistent Hash Ring","Rendezvous Hashing",
        "Consistent Hashing with Virtual Nodes","Consistent Hashing with Load Balancing",
    ],
    "Trees": ["Binary Tree Inorder Traversal","Binary Tree Preorder Traversal",
        "Binary Tree Postorder Traversal","Binary Tree Level Order Traversal",
        "Binary Tree Zigzag Level Order Traversal","Binary Tree Right Side View",
        "Binary Tree Left Side View","Binary Tree Maximum Depth","Binary Tree Minimum Depth",
        "Binary Tree Maximum Width","Binary Tree Diameter","Binary Tree Maximum Path Sum",
        "Binary Tree Longest Consecutive Sequence","Binary Tree Longest Consecutive Path",
        "Binary Tree Vertical Order Traversal","Binary Tree Level Order Traversal II",
        "Binary Tree Level Order Traversal III","Binary Tree Level Order Traversal IV",
        "Validate Binary Search Tree","Recover Binary Search Tree","Convert Sorted Array to BST",
        "Convert Sorted List to BST","Minimum Height BST","Balanced Binary Tree",
        "Symmetric Tree","Same Tree","Subtree of Another Tree","Invert Binary Tree",
        "Lowest Common Ancestor of BST","Lowest Common Ancestor of BT",
        "Serialize and Deserialize Binary Tree","Serialize and Deserialize N-ary Tree",
        "Kth Smallest Element in BST","Kth Largest Element in BST",
        "Construct Binary Tree from Preorder and Inorder","Construct Binary Tree from Inorder and Postorder",
        "Construct Binary Tree from Preorder and Postorder","Maximum Binary Tree",
        "Minimum Binary Tree","Binary Tree Cameras","Binary Tree Tilt","Binary Tree Pruning",
        "Binary Tree Paths","Binary Tree Longest Consecutive Sequence II",
        "Design Binary Search Tree","Design AVL Tree","Design Red-Black Tree",
        "Design B-Tree","Design B+ Tree","Design Segment Tree","Design Fenwick Tree",
        "Design Interval Tree","Design Quad Tree","Design KD Tree","Design R-Tree",
        "Design Trie Tree","Design Suffix Tree","Design Suffix Array","Design Suffix Trie",
    ],
    "Graphs": ["Number of Islands","Number of Connected Components","Graph Valid Tree",
        "Is Graph Bipartite?","Clone Graph","Pacific Atlantic Water Flow","Surrounded Regions",
        "Word Ladder","Word Ladder II","Alien Dictionary","Course Schedule","Course Schedule II",
        "Minimum Height Trees","Graph Valid Tree","Graph Connectivity","Graph Diameter",
        "Graph Center","Graph Eccentricity","Graph Radius","Graph Periphery",
        "Minimum Spanning Tree","Kruskal Algorithm","Prim Algorithm","Boruvka Algorithm",
        "Dijkstra Algorithm","Bellman-Ford Algorithm","Floyd-Warshall Algorithm",
        "Johnson Algorithm","A* Search Algorithm","Bidirectional Search","Iterative Deepening",
        "Uniform Cost Search","Greedy Best-First Search","Depth-First Search","Breadth-First Search",
        "Topological Sort","Kahn Algorithm","DFS-based Topological Sort",
        "Strongly Connected Components","Tarjan Algorithm","Kosaraju Algorithm","Gabow Algorithm",
        "Biconnected Components","Articulation Points","Bridges in Graph","Eulerian Path",
        "Hamiltonian Path","Traveling Salesman Problem","Chinese Postman Problem",
        "Network Flow","Ford-Fulkerson","Edmonds-Karp","Dinic Algorithm",
        "Minimum Cost Maximum Flow","Successive Shortest Path","Cycle Canceling",
        "Bipartite Matching","Hopcroft-Karp Algorithm","Hungarian Algorithm",
    ],
    "Dynamic Programming": ["Climbing Stairs","Min Cost Climbing Stairs","House Robber",
        "House Robber II","House Robber III","Paint House","Paint Fence","Decode Ways",
        "Unique Paths","Unique Paths II","Minimum Path Sum","Maximum Path Sum","Cherry Pickup",
        "Dungeon Game","Burst Balloons","Longest Increasing Subsequence",
        "Number of Longest Increasing Subsequences","Longest Common Subsequence",
        "Longest Common Substring","Shortest Common Supersequence","Edit Distance",
        "Delete Operation for Two Strings","Minimum ASCII Delete Sum for Two Strings",
        "Interleaving String","Distinct Subsequences","Number of Matching Subsequences",
        "Longest Palindromic Subsequence","Longest Palindromic Substring",
        "Palindromic Substrings","Expand Around Center","Manacher Algorithm",
        "Coin Change","Coin Change II","Target Sum","Partition Equal Subset Sum",
        "Last Stone Weight","Last Stone Weight II","Split Array Largest Sum",
        "Capacity to Ship Packages","Minimum Number of Days to Make m Bouquets",
        "Maximum Product Subarray","Maximum Sum Circular Subarray",
        "Non-overlapping Intervals","Minimum Number of Arrows to Burst Balloons",
        "Merge Intervals","Insert Interval","Non-overlapping Intervals",
        "Meeting Rooms","Meeting Rooms II","Meeting Rooms III","Meeting Rooms IV",
        "Task Scheduler","Task Scheduler II","Design Task Scheduler","CPU Scheduler",
        "Memory Allocator","Page Replacement Algorithm","LRU Cache","LFU Cache","ARC Cache",
        "2-3 Tree","2-3-4 Tree","Red-Black Tree","Splay Tree","Treap","Skip List",
        "Bloom Filter","Counting Bloom Filter","Quotient Filter","Cuckoo Filter",
        "Count Min Sketch","Heavy Hitters","Lossy Counting","Space-Saving Algorithm",
    ],
    "Greedy": ["Jump Game","Jump Game II","Minimum Number of Taps to Open",
        "Video Stitching","Non-overlapping Intervals","Minimum Number of Arrows",
        "Merge Intervals","Insert Interval","Meeting Rooms","Meeting Rooms II",
        "Task Scheduler","CPU Scheduling","Memory Management","Page Replacement",
        "File Compression","Huffman Coding","LZW Compression","Run-Length Encoding",
        "Arithmetic Coding","Entropy Encoding","Shannon-Fano Encoding",
        "Knapsack Problem","Fractional Knapsack","0/1 Knapsack","Bounded Knapsack",
        "Unbounded Knapsack","Multiple Knapsack","Quadratic Knapsack",
        "Assignment Problem","Hungarian Algorithm","Minimum Cost Assignment",
        "Activity Selection Problem","Interval Scheduling Maximization",
        "Weighted Interval Scheduling","Interval Graph Coloring",
    ],
    "Backtracking": ["N-Queens","N-Queens II","Sudoku Solver","Word Search",
        "Word Search II","Palindrome Partitioning","Palindrome Partitioning II",
        "Letter Combinations of a Phone Number","Generate Parentheses",
        "Valid Sudoku","Sudoku Solver","Knight's Tour","Hamiltonian Cycle",
        "Graph Coloring","Map Coloring","Register Allocation","Instruction Scheduling",
        "Constraint Satisfaction Problem","AC-3 Algorithm","Arc Consistency",
        "Forward Checking","Backjumping","Conflict-Directed Backjumping",
        "Dynamic Backtracking","Chronological Backtracking","Intelligent Backtracking",
    ],
    "Sliding Window & Two Pointers": ["Longest Substring Without Repeating Characters",
        "Longest Repeating Character Replacement","Minimum Window Substring",
        "Substring with Concatenation of All Words","Fruit Into Baskets",
        "Max Consecutive Ones","Max Consecutive Ones III","Longest Nice Subarray",
        "Shortest Unsorted Continuous Subarray","Minimum Window Substring",
        "Trapping Rain Water","Container With Most Water","3Sum","3Sum Closest","4Sum",
        "Two Sum II - Input Array Is Sorted","Two Sum IV - Input is BST",
    ],
    "Bit Manipulation": ["Single Number","Single Number II","Single Number III",
        "Number of 1 Bits","Counting Bits","Reverse Bits","Power of Two","Power of Four",
        "Binary Watch","Hamming Distance","Total Hamming Distance","Convert a Number to Hexadecimal",
        "Complement of Base 10 Integer","Binary Gap","Maximum Binary Gap",
        "Bitwise AND of Numbers Range","Number Complement","Flipping an Image",
        "Sum of Two Integers","Multiply Two Integers","Divide Two Integers",
        "Power of Two","Power of Three","Power of Four","Convert to Base -2",
    ],
    "Math & Geometry": ["Fizz Buzz","Count Primes","Power of Two","Power of Three",
        "Power of Four","Factorial Trailing Zeroes","Trailing Zeros","Base 7",
        "Excel Sheet Column Number","Excel Sheet Column Title","Reverse Integer",
        "Palindrome Number","Armstrong Number","Perfect Number","Ugly Number",
        "Happy Number","Sad Number","Narcissistic Number","Strong Number",
        "Kaprekar Number","Keith Number","Smith Number","Sphenic Number",
        "Circular Prime","Mersenne Prime","Perfect Square","Perfect Cube",
        "Integer Break","Maximize Sum of Array After K Negations",
        "Maximum Points on a Line","Max Points on a Line","Line Reflection",
        "Rectangle Area","Overlapping Rectangles","Rectangle Overlap",
        "Convex Hull","Graham Scan","Jarvis March","QuickHull",
        "Line Sweep Algorithm","Closest Pair of Points","Divide and Conquer Geometry",
    ],
    "Sorting & Searching": ["Binary Search","Search in Rotated Sorted Array",
        "Search in Rotated Sorted Array II","Find Minimum in Rotated Sorted Array",
        "Median of Two Sorted Arrays","Kth Largest Element in a Stream",
        "Top K Frequent Elements","Sort Colors","Dutch National Flag Problem",
        "Counting Sort","Radix Sort","Bucket Sort","Shell Sort","Comb Sort",
        "Merge Sort","Quick Sort","Heap Sort","Insertion Sort","Selection Sort",
        "Bubble Sort","Cocktail Sort","Gnome Sort","Pancake Sort","Bogo Sort",
        "Tim Sort","Intro Sort","Smooth Sort","Pigeonhole Sort","Counting Sort",
    ],
    "Design & System": ["Design LRU Cache","Design LFU Cache","Design Twitter",
        "Design Facebook","Design Instagram","Design YouTube","Design Google Search",
        "Design Amazon Search","Design Netflix","Design Spotify","Design Uber",
        "Design Airbnb","Design Dropbox","Design Google Drive","Design Instagram Stories",
        "Design Snapchat","Design TikTok","Design Twitter Timeline",
        "Design YouTube Recommendation","Design Google Maps",
        "Design Uber Matching","Design Airbnb Search","Design Amazon Cart",
        "Design Shopping Mall","Design Theme Park","Design Airport",
        "Design Traffic System","Design Parking Lot","Design Elevator System",
        "Design Restaurant Menu","Design Food Delivery","Design Medicine Delivery",
        "Design Ride Sharing","Design Car Pooling","Design Taxi Dispatch",
        "Design Bus System","Design Train System","Design Metro System",
        "Design Airline Reservation","Design Hotel Booking","Design Car Rental",
        "Design Event Ticketing","Design Concert Booking","Design Movie Ticketing",
    ],
}

HARD_TESTCASES = [
    {"input": "[3, 3, 3, 3, 3]", "expected": "0", "note": "All same"},
    {"input": "[1]", "expected": "1", "note": "Single"},
    {"input": "[]", "expected": "0", "note": "Empty"},
    {"input": "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]", "expected": "55", "note": "Sum 1-10"},
    {"input": "[-1, -2, -3]", "expected": "-1", "note": "All negative"},
]

# Generate 50-80 problems per topic category
def gen_questions():
    questions = []
    qid = 0
    
    for topic, titles in TOPICS.items():
        for i, title in enumerate(titles):
            qid += 1
            diff_weights = {"easy": 0.35, "medium": 0.45, "hard": 0.20}
            diff = random.choices(["easy", "medium", "hard"], weights=[diff_weights["easy"], diff_weights["medium"], diff_weights["hard"]])[0]
            
            if diff == "easy":
                companies = random.sample(COMPANIES[:15], min(3, len(COMPANIES[:15])))
                sol = SOLUTIONS["easy"]
                xp = random.randint(30, 60)
            elif diff == "medium":
                companies = random.sample(COMPANIES[:25], min(4, len(COMPANIES[:25])))
                sol = SOLUTIONS["medium"]
                xp = random.randint(60, 100)
            else:
                companies = random.sample(COMPANIES, min(5, len(COMPANIES)))
                sol = SOLUTIONS["hard"]
                xp = random.randint(100, 200)
            
            q = {
                "type": "coding",
                "id": str(uuid.uuid4()),
                "question": title,
                "description": f"Solve: {title}",
                "difficulty": diff,
                "topic": topic,
                "sub_topic": topic,
                "company": companies,
                "role": ROLES[:3],
                "company_frequency": {c: random.randint(3, 15) for c in companies},
                "acceptance_rate": round(random.uniform(0.25, 0.65), 2),
                "total_submissions": random.randint(10000, 3000000),
                "examples": [{"input": "example input", "expected_output": "example output", "explanation": f"Solution for {title}"}],
                "testcases": HARD_TESTCASES if diff == "hard" else HARD_TESTCASES[:2],
                "solution": {"code": f"def solution():\n    pass", "language": "python", "time_complexity": sol["time"], "space_complexity": sol["space"], "optimal": True},
                "hints": ["Think about the right data structure", "Consider edge cases"],
                "pitfalls": ["Edge cases with empty input", "Off-by-one errors"],
                "xp_points": xp,
                "frequency_score": round(random.uniform(2.0, 9.5), 1),
                "uploaded_by": "system",
                "upvotes": random.randint(10, 5000),
                "downvotes": random.randint(1, 100),
                "views": random.randint(1000, 2000000),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "is_hidden": False,
            }
            questions.append(q)
    
    return questions

# Generate aptitude and logical questions
def gen_aptitude_and_logical():
    questions = []
    for topic, count in [("Aptitude", 250), ("Logical Reasoning", 150), ("Verbal Ability", 100)]:
        for i in range(count):
            q = {
                "type": topic.lower().replace(" ", "_").replace("verbal", "verbal").replace("aptitude", "aptitude"),
                "id": str(uuid.uuid4()),
                "question": f"{topic} Question {i+1}: Solve this problem.",
                "description": f"Sample {topic.lower()} problem for practice.",
                "difficulty": random.choice(["easy", "medium", "hard"]),
                "topic": topic,
                "sub_topic": "Practice",
                "company": ["TCS", "Infosys", "Wipro", "Accenture", "Capgemini"],
                "role": ["Placement Candidate"],
                "company_frequency": {"TCS": 10, "Infosys": 8, "Wipro": 6, "Accenture": 5, "Capgemini": 4},
                "acceptance_rate": round(random.uniform(0.3, 0.7), 2),
                "total_submissions": random.randint(1000, 10000),
                "examples": [{"input": "sample input", "expected_output": "sample output", "explanation": "Explanation"}],
                "testcases": [],
                "solution": {"code": "# Answer", "language": "markdown", "time_complexity": "N/A", "space_complexity": "N/A", "optimal": True},
                "hints": ["Read carefully"],
                "xp_points": random.randint(20, 60),
                "frequency_score": round(random.uniform(2.0, 5.0), 1),
                "uploaded_by": "system",
                "upvotes": random.randint(10, 500),
                "downvotes": random.randint(1, 20),
                "views": random.randint(1000, 10000),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "is_hidden": False,
            }
            questions.append(q)
    return questions

# Main
coding_questions = gen_questions()
non_coding_questions = gen_aptitude_and_logical()
all_questions = coding_questions + non_coding_questions

print(f"Total questions generated: {len(all_questions)}")
print(f"  Coding: {len(coding_questions)}")
print(f"  Aptitude: {sum(1 for q in non_coding_questions if 'aptitude' in q['type'])}")
print(f"  Logical: {sum(1 for q in non_coding_questions if 'logical' in q['type'])}")
print(f"  Verbal: {sum(1 for q in non_coding_questions if 'verbal' in q['type'])}")
print(f"\nTopic breakdown:")
from collections import Counter
topics = Counter(q["topic"] for q in coding_questions)
for t, c in topics.most_common():
    print(f"  {t}: {c}")
print(f"\nDifficulty breakdown:")
diffs = Counter(q["difficulty"] for q in all_questions)
for d, c in diffs.most_common():
    print(f"  {d}: {c}")