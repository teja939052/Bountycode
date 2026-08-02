"""
Candy Crush-style learning curriculum.
40 levels per language (C, C++, Java, Python) = 160 total levels.
Each level has a theme, color, icon, lessons with difficulty stars, projects, and boss battles.
"""
#pylint: skip-file

# Difficulty: 1=easy, 2=medium, 3=hard
# XP: easy=10-15, medium=20-30, hard=35-50, project=60, boss=80

LEVEL_THEMES = [
    {"id": "l01", "name": "First Steps",        "emoji": "🌱", "color": "#22C55E", "bg": "from-green-500/20 to-emerald-600/20",  "border": "border-green-500/30",  "text": "text-green-400",  "desc": "Hello World & basic output"},
    {"id": "l02", "name": "Variables",           "emoji": "📦", "color": "#3B82F6", "bg": "from-blue-500/20 to-blue-600/20",      "border": "border-blue-500/30",   "text": "text-blue-400",   "desc": "Data types, constants, declarations"},
    {"id": "l03", "name": "Operators",           "emoji": "⚡", "color": "#F59E0B", "bg": "from-amber-500/20 to-yellow-600/20",   "border": "border-amber-500/30",  "text": "text-amber-400",  "desc": "Arithmetic, comparison, logical"},
    {"id": "l04", "name": "Conditionals",        "emoji": "🔀", "color": "#8B5CF6", "bg": "from-violet-500/20 to-purple-600/20",  "border": "border-violet-500/30", "text": "text-violet-400", "desc": "if/else, switch, ternary"},
    {"id": "l05", "name": "Loops",               "emoji": "🔄", "color": "#EF4444", "bg": "from-red-500/20 to-rose-600/20",       "border": "border-red-500/30",    "text": "text-red-400",    "desc": "for, while, do-while, patterns"},
    {"id": "l06", "name": "Functions",           "emoji": "🧩", "color": "#06B6D4", "bg": "from-cyan-500/20 to-teal-600/20",     "border": "border-cyan-500/30",   "text": "text-cyan-400",   "desc": "Functions, params, recursion"},
    {"id": "l07", "name": "Arrays",              "emoji": "📊", "color": "#10B981", "bg": "from-emerald-500/20 to-green-600/20",  "border": "border-emerald-500/30","text": "text-emerald-400","desc": "1D, 2D arrays, algorithms"},
    {"id": "l08", "name": "Strings",             "emoji": "📝", "color": "#EC4899", "bg": "from-pink-500/20 to-fuchsia-600/20",  "border": "border-pink-500/30",   "text": "text-pink-400",   "desc": "String manipulation & parsing"},
    {"id": "l09", "name": "Pointers & Memory",   "emoji": "🧠", "color": "#F97316", "bg": "from-orange-500/20 to-amber-600/20",   "border": "border-orange-500/30", "text": "text-orange-400", "desc": "Pointers, refs, memory mgmt"},
    {"id": "l10", "name": "OOP",                 "emoji": "🏗️", "color": "#6366F1", "bg": "from-indigo-500/20 to-blue-600/20",   "border": "border-indigo-500/30", "text": "text-indigo-400", "desc": "Classes, inheritance, polymorphism"},
    {"id": "l11", "name": "Data Structures",     "emoji": "🌳", "color": "#14B8A6", "bg": "from-teal-500/20 to-cyan-600/20",     "border": "border-teal-500/30",   "text": "text-teal-400",   "desc": "Linked lists, trees, graphs"},
    {"id": "l12", "name": "Final Challenge",     "emoji": "👑", "color": "#EAB308", "bg": "from-yellow-500/20 to-amber-600/20",   "border": "border-yellow-500/30", "text": "text-yellow-400", "desc": "Boss battle + capstone project"},
    {"id": "l13", "name": "Mini Compiler",       "emoji": "⚙️", "color": "#06B6D4", "bg": "from-cyan-500/20 to-cyan-600/20",       "border": "border-cyan-500/30",   "text": "text-cyan-400",   "desc": "Compilers, interpreters & expression evaluation"},
    {"id": "l14", "name": "Portfolio Capstone",  "emoji": "🏆", "color": "#FFD700", "bg": "from-yellow-400/20 to-amber-500/20",     "border": "border-yellow-400/30", "text": "text-yellow-300", "desc": "Full portfolio project combining everything learned"},
    # Group 4: Systems & Memory (l15-l20)
    {"id": "l15", "name": "Bits & Bytes",           "emoji": "🔲", "color": "#6EE7B7", "bg": "from-emerald-400/20 to-green-500/20",   "border": "border-emerald-400/30","text": "text-emerald-300","desc": "Bit manipulation, binary ops, bit masks"},
    {"id": "l16", "name": "Advanced Recursion",      "emoji": "🔁", "color": "#A78BFA", "bg": "from-violet-400/20 to-purple-500/20",  "border": "border-violet-400/30", "text": "text-violet-300", "desc": "Backtracking, memoization, divide & conquer"},
    {"id": "l17", "name": "File I/O Deep Dive",      "emoji": "📁", "color": "#60A5FA", "bg": "from-blue-400/20 to-blue-500/20",     "border": "border-blue-400/30",   "text": "text-blue-300",   "desc": "File operations, streams, serialization"},
    {"id": "l18", "name": "Dynamic Memory",           "emoji": "🧩", "color": "#F472B6", "bg": "from-pink-400/20 to-rose-500/20",     "border": "border-pink-400/30",   "text": "text-pink-300",   "desc": "Heap allocation, memory pools, allocators"},
    {"id": "l19", "name": "Preprocessors & Build",    "emoji": "🔧", "color": "#FB923C", "bg": "from-orange-400/20 to-amber-500/20",  "border": "border-orange-400/30", "text": "text-orange-300", "desc": "Macros, conditional compilation, build systems"},
    {"id": "l20", "name": "Systems Mastery",          "emoji": "🐉", "color": "#EF4444", "bg": "from-red-500/20 to-rose-600/20",      "border": "border-red-500/30",    "text": "text-red-400",    "desc": "Boss level: system programming challenge"},
    # Group 5: DS & Algorithms (l21-l25)
    {"id": "l21", "name": "Advanced Sorting",         "emoji": "📊", "color": "#34D399", "bg": "from-emerald-400/20 to-green-500/20",  "border": "border-emerald-400/30","text": "text-emerald-300","desc": "Quick sort, merge sort, heap sort, radix sort"},
    {"id": "l22", "name": "Trees & Graphs",           "emoji": "🌲", "color": "#818CF8", "bg": "from-indigo-400/20 to-indigo-500/20",  "border": "border-indigo-400/30", "text": "text-indigo-300", "desc": "BSTs, AVL, graph algorithms, shortest paths"},
    {"id": "l23", "name": "Hashing & Maps",           "emoji": "🗄️", "color": "#FBBF24", "bg": "from-amber-400/20 to-yellow-500/20",  "border": "border-amber-400/30",  "text": "text-amber-300",  "desc": "Hash functions, collision resolution, hash maps"},
    {"id": "l24", "name": "Heaps & Tries",            "emoji": "📈", "color": "#2DD4BF", "bg": "from-teal-400/20 to-cyan-500/20",     "border": "border-teal-400/30",   "text": "text-teal-300",   "desc": "Priority queues, heap sort, trie structures"},
    {"id": "l25", "name": "Algorithms Mastery",       "emoji": "🐉", "color": "#EF4444", "bg": "from-red-500/20 to-rose-600/20",      "border": "border-red-500/30",    "text": "text-red-400",    "desc": "Boss level: DS & algorithm challenge"},
    # Group 6: Professional Dev (l26-l30)
    {"id": "l26", "name": "Concurrency",              "emoji": "⚡", "color": "#F87171", "bg": "from-red-400/20 to-rose-500/20",      "border": "border-red-400/30",    "text": "text-red-300",    "desc": "Threads, sync, race conditions, locks"},
    {"id": "l27", "name": "Networking",               "emoji": "🌐", "color": "#38BDF8", "bg": "from-sky-400/20 to-blue-500/20",      "border": "border-sky-400/30",    "text": "text-sky-300",    "desc": "TCP/UDP, sockets, HTTP, REST"},
    {"id": "l28", "name": "Testing & Debugging",      "emoji": "🔍", "color": "#A78BFA", "bg": "from-violet-400/20 to-purple-500/20",  "border": "border-violet-400/30", "text": "text-violet-300", "desc": "Unit tests, debugging, profiling"},
    {"id": "l29", "name": "CI/CD & Tooling",          "emoji": "🛠️", "color": "#F59E0B", "bg": "from-amber-400/20 to-yellow-500/20",  "border": "border-amber-400/30",  "text": "text-amber-300",  "desc": "Git, CI/CD pipelines, containers"},
    {"id": "l30", "name": "Pro Dev Mastery",          "emoji": "🐉", "color": "#EF4444", "bg": "from-red-500/20 to-rose-600/20",      "border": "border-red-500/30",    "text": "text-red-400",    "desc": "Boss level: professional development challenge"},
    # Group 7: Advanced Topics (l31-l35)
    {"id": "l31", "name": "Design Patterns",          "emoji": "🏗️", "color": "#EC4899", "bg": "from-pink-400/20 to-fuchsia-500/20",  "border": "border-pink-400/30",   "text": "text-pink-300",   "desc": "Common patterns, SOLID, refactoring"},
    {"id": "l32", "name": "Performance Tuning",       "emoji": "📈", "color": "#10B981", "bg": "from-emerald-400/20 to-green-500/20",  "border": "border-emerald-400/30","text": "text-emerald-300","desc": "Profiling, optimization, caching"},
    {"id": "l33", "name": "Security",                 "emoji": "🔒", "color": "#8B5CF6", "bg": "from-violet-400/20 to-purple-500/20",  "border": "border-violet-400/30", "text": "text-violet-300", "desc": "Secure coding, OWASP, auth, encryption"},
    {"id": "l34", "name": "Architecture",             "emoji": "🏛️", "color": "#F97316", "bg": "from-orange-400/20 to-amber-500/20",  "border": "border-orange-400/30", "text": "text-orange-300", "desc": "System architecture, microservices, APIs"},
    {"id": "l35", "name": "Advanced Mastery",         "emoji": "🐉", "color": "#EF4444", "bg": "from-red-500/20 to-rose-600/20",      "border": "border-red-500/30",    "text": "text-red-400",    "desc": "Boss level: advanced topics challenge"},
    # Group 8: Mastery (l36-l40)
    {"id": "l36", "name": "Real-World API",           "emoji": "🚀", "color": "#06B6D4", "bg": "from-cyan-400/20 to-cyan-500/20",     "border": "border-cyan-400/30",   "text": "text-cyan-300",   "desc": "Building production APIs, error handling"},
    {"id": "l37", "name": "Database Integration",     "emoji": "🗄️", "color": "#6366F1", "bg": "from-indigo-400/20 to-indigo-500/20",  "border": "border-indigo-400/30", "text": "text-indigo-300", "desc": "SQLite, DB drivers, connection pools"},
    {"id": "l38", "name": "Full Stack Mini",          "emoji": "💼", "color": "#14B8A6", "bg": "from-teal-400/20 to-cyan-500/20",     "border": "border-teal-400/30",   "text": "text-teal-300",   "desc": "Combined frontend/backend project"},
    {"id": "l39", "name": "Code Review Pro",          "emoji": "🔍", "color": "#8B5CF6", "bg": "from-violet-400/20 to-purple-500/20",  "border": "border-violet-400/30", "text": "text-violet-300", "desc": "Professional code review, clean code"},
    {"id": "l40", "name": "Grand Master",             "emoji": "👑", "color": "#EAB308", "bg": "from-yellow-400/20 to-amber-500/20",   "border": "border-yellow-400/30", "text": "text-yellow-300", "desc": "Final boss: comprehensive mastery challenge"},
]


def _L(title, xp=15, diff=1, type_="theory", git_desc=None):
    """Shorthand to create a lesson dict."""
    result = {"title": title, "xp": xp, "difficulty": diff, "type": type_}
    if git_desc:
        result["git_description"] = git_desc
    return result


def _bonus_lessons(lang_id, theme):
    """Add extra high-value quests to every level so the path feels denser."""
    label = theme["name"]
    lang_tag = lang_id.upper()
    return [
        _L(f"Practice Sprint: {label} Blitz", 20, 2, "practice"),
        _L(f"Project Lab: {label} Builder ({lang_tag})", 70, 3, "project"),
        _L(f"Code Review: {label} Bug Hunt", 20, 2, "challenge"),
        _L(f"Quick Quiz: {label} Checkpoint", 20, 1, "quiz"),
    ]


# ────────────────────────────────────────────
#  C LANGUAGE — 12 Levels
# ────────────────────────────────────────────
C_LEVELS = [
    # Level 1: First Steps 🌱
    {"id": "l01", "lessons": [
        _L("What is C?", 10, 1), _L("Your First C Program", 10, 1, "practice"),
        _L("printf() Basics", 10, 1), _L("Comments in C", 10, 1),
        _L("Compilation Process", 15, 1), _L("Practice: Hello World", 15, 1, "practice"),
        _L("Challenge: Print Patterns", 25, 2, "challenge"),
        _L("Project: Terminal Startup Banner with ASCII Art & System Info", 60, 3, "project",
           "A customizable terminal startup banner that displays ASCII art and system information, perfect for personalizing your development environment."),
    ]},
    # Level 2: Variables 📦
    {"id": "l02", "lessons": [
        _L("Int, Float, Double", 10, 1), _L("char Type", 10, 1),
        _L("Variable Declaration", 15, 1), _L("Constants & #define", 15, 1),
        _L("Type Sizes with sizeof", 15, 2), _L("scanf() Input", 15, 1, "practice"),
        _L("Type Casting", 20, 2), _L("Practice: Temperature Converter", 20, 2, "practice"),
        _L("Challenge: Swap Two Numbers", 25, 2, "challenge"),
        _L("Project: Memory-Safe Calculator with History Logging", 60, 3, "project",
           "A calculator application with memory-safe practices, featuring history logging and robust error handling for reliable daily use."),
    ]},
    # Level 3: Operators ⚡
    {"id": "l03", "lessons": [
        _L("Arithmetic Operators", 10, 1), _L("Relational Operators", 10, 1),
        _L("Logical Operators", 15, 1), _L("Bitwise Operators", 20, 2),
        _L("Assignment Operators", 10, 1), _L("Operator Precedence", 15, 2),
        _L("Ternary Operator", 15, 2), _L("Practice: Quiz Score Calculator", 20, 2, "practice"),
        _L("Challenge: Bit Manipulation", 30, 3, "challenge"),
        _L("Project: Multi-Format Unit Converter with File I/O", 60, 3, "project",
           "A versatile unit converter supporting multiple measurement categories with file I/O for saving and loading conversion presets."),
    ]},
    # Level 4: Conditionals 🔀
    {"id": "l04", "lessons": [
        _L("if Statement", 10, 1), _L("if-else Statement", 10, 1),
        _L("Nested if-else", 15, 2), _L("Switch Statement", 15, 2),
        _L("Fall-through in Switch", 20, 2), _L("Practice: Grade Calculator", 20, 2, "practice"),
        _L("Challenge: Vowel or Consonant", 25, 2, "challenge"),
        _L("Challenge: Leap Year Check", 30, 3, "challenge"),
        _L("Project: Health Dashboard — BMI, BMR & Calorie Tracker", 60, 3, "project",
           "A comprehensive health tracking dashboard that calculates BMI, BMR, and calorie metrics with persistent data logging."),
    ]},
    # Level 5: Loops 🔄
    {"id": "l05", "lessons": [
        _L("for Loop", 10, 1), _L("while Loop", 10, 1),
        _L("do-while Loop", 15, 1), _L("Nested Loops", 15, 2),
        _L("break & continue", 15, 2), _L("Pattern Printing", 25, 3, "practice"),
        _L("Practice: Multiplication Table", 20, 2, "practice"),
        _L("Challenge: Sum of Digits", 25, 2, "challenge"),
        _L("Challenge: Number Pyramid", 35, 3, "challenge"),
        _L("Project: Number Guessing Game", 60, 2, "project",
           "An interactive number guessing game with difficulty levels and scoring, demonstrating loops and random number generation."),
    ]},
    # Level 6: Functions 🧩
    {"id": "l06", "lessons": [
        _L("Function Basics", 10, 1), _L("Parameters & Return", 15, 1),
        _L("Function Prototypes", 15, 2), _L("Call by Value", 15, 2),
        _L("Call by Reference", 20, 2), _L("Recursion Basics", 25, 2),
        _L("Recursive Factorial", 25, 2), _L("Practice: Fibonacci", 30, 3, "practice"),
        _L("Challenge: Tower of Hanoi", 40, 3, "challenge"),
        _L("Project: Dungeon Crawler RPG with Save/Load System", 60, 3, "project",
           "A terminal-based dungeon crawler RPG featuring save/load functionality, combat system, and procedural map generation."),
    ]},
    # Level 7: Arrays 📊
    {"id": "l07", "lessons": [
        _L("1D Array Basics", 10, 1), _L("Array Input/Output", 15, 1, "practice"),
        _L("2D Arrays", 15, 2), _L("Array Traversal", 15, 2),
        _L("Linear Search", 15, 2), _L("Binary Search", 25, 3),
        _L("Bubble Sort", 25, 2), _L("Selection Sort", 25, 2),
        _L("Practice: Matrix Operations", 30, 3, "practice"),
        _L("Challenge: Rotate Array", 35, 3, "challenge"),
        _L("Project: School Management System with CSV Import & Analytics", 60, 3, "project",
           "A complete school management system with CSV import/export, student records, grade tracking, and analytics dashboards."),
    ]},
    # Level 8: Strings 📝
    {"id": "l08", "lessons": [
        _L("Character Arrays", 10, 1), _L("String Functions", 15, 1),
        _L("strlen, strcpy, strcat", 15, 2, "practice"), _L("strcmp & strncmp", 15, 2),
        _L("String Reversal", 20, 2, "practice"), _L("Palindrome Check", 25, 2, "practice"),
        _L("Practice: Word Counter", 25, 2, "practice"),
        _L("Challenge: String Compression", 35, 3, "challenge"),
        _L("Challenge: Anagram Checker", 30, 3, "challenge"),
        _L("Project: Real-Time Word Frequency Analyzer & Word Cloud Generator", 60, 3, "project",
           "A real-time word frequency analysis tool that generates word clouds and statistical insights from text input."),
    ]},
    # Level 9: Pointers & Memory 🧠
    {"id": "l09", "lessons": [
        _L("What are Pointers?", 15, 2), _L("Pointer Operators &", 15, 2),
        _L("Pointer Arithmetic", 20, 2), _L("Pointers & Arrays", 20, 2),
        _L("Pointer to Pointer", 25, 3), _L("malloc & free", 20, 2),
        _L("calloc & realloc", 25, 3), _L("Memory Leaks", 25, 3),
        _L("Practice: Dynamic Array", 30, 3, "practice"),
        _L("Challenge: Custom Memory Allocator", 40, 3, "challenge"),
        _L("Project: Custom String Library rivaling string.h — with unit tests", 60, 3, "project",
           "A custom string manipulation library implementing all standard string.h functions with comprehensive unit tests."),
    ]},
    # Level 10: OOP in C 🏗️
    {"id": "l10", "lessons": [
        _L("Structs", 15, 2), _L("Nested Structs", 15, 2),
        _L("Struct Pointers", 20, 2), _L("Enums & Typedef", 15, 2),
        _L("Function Pointers", 25, 3), _L("Polymorphism via Tables", 30, 3),
        _L("Opaque Pointers (Encapsulation)", 30, 3),
        _L("Practice: Card Game with Structs", 35, 3, "practice"),
        _L("Challenge: Mini OOP Library", 40, 3, "challenge"),
        _L("Project: Library System with Binary Search Index & File Persistence", 60, 3, "project",
           "A library system with binary search indexing and file persistence for managing books, members, and transactions."),
    ]},
    # Level 11: Data Structures 🌳
    {"id": "l11", "lessons": [
        _L("Singly Linked List", 25, 2), _L("Doubly Linked List", 25, 3),
        _L("Stack (Array)", 20, 2), _L("Stack (Linked List)", 25, 3),
        _L("Queue (Array)", 20, 2), _L("Circular Queue", 25, 3),
        _L("Binary Search Tree", 30, 3), _L("Tree Traversals", 30, 3),
        _L("Practice: Expression Evaluator", 40, 3, "practice"),
        _L("Challenge: Graph BFS/DFS", 45, 3, "challenge"),
        _L("Project: Virtual File System with mkdir, ls, cp, rm, tree commands", 60, 3, "project",
           "A simulated Unix-like file system supporting mkdir, ls, cp, rm, and tree commands with in-memory directory structures."),
    ]},
    # Level 12: Final Challenge 👑
    {"id": "l12", "lessons": [
        _L("Sorting Algorithms Review", 30, 3), _L("Searching Deep Dive", 30, 3),
        _L("Dynamic Programming Intro", 35, 3), _L("DP: Knapsack Problem", 40, 3),
        _L("Greedy Algorithms", 35, 3), _L("Bit Manipulation Mastery", 35, 3),
        _L("Practice: Contest Problems", 45, 3, "practice"),
        _L("Challenge: Trie Implementation", 45, 3, "challenge"),
        _L("Challenge: Hash Table from Scratch", 50, 3, "challenge"),
        _L("Capstone: Unix Shell with Pipes, Redirection, Job Control & History", 80, 3, "project", "A functional Unix shell implementation featuring pipes, I/O redirection, job control, and command history."),
        _L("👑 C Grandmaster Boss", 80, 3, "boss"),
    ]},
    # Level 13: Mini Compiler ⚙️
    {"id": "l13", "lessons": [
        _L("How C Compilers Work (GCC/Clang Internals)", 30, 3),
        _L("Lexing: Tokenizing C Source Code", 35, 3, "practice"),
        _L("Challenge: Build an AST", 40, 3, "challenge"),
        _L("Project: Mini Expression Compiler — compile arithmetic to x86-like assembly", 70, 3, "project",
           "A mini expression compiler that parses and compiles arithmetic expressions into x86-like assembly instructions."),
    ]},
    # Level 14: Portfolio Capstone 🏆
    {"id": "l14", "lessons": [
        _L("Project Architecture for Large C Programs", 35, 3),
        _L("Design Patterns in C: Modular Architecture", 40, 3, "practice"),
        _L("Challenge: Performance Optimization & Profiling", 45, 3, "challenge"),
        _L("Project: Full Portfolio — Chat Server, Database, Shell, Compiler", 80, 3, "project",
           "A comprehensive portfolio project combining a chat server, database, shell, and compiler into a unified C application."),
        _L("🏆 C Mastery Finale", 100, 3, "boss"),
    ]},
]


# ────────────────────────────────────────────
#  C++ LANGUAGE — 12 Levels
# ────────────────────────────────────────────
CPP_LEVELS = [
    # Level 1: First Steps 🌱
    {"id": "l01", "lessons": [
        _L("What is C++?", 10, 1), _L("Hello World in C++", 10, 1, "practice"),
        _L("iostream & cout", 10, 1), _L("cin for Input", 10, 1, "practice"),
        _L("Namespaces", 10, 1), _L("Comments in C++", 10, 1),
        _L("Practice: Greeting Program", 15, 1, "practice"),
        _L("Challenge: Mini Calculator", 25, 2, "challenge"),
        _L("Project: Rich Terminal Profile Card with Box Drawing & Colors", 60, 3, "project",
           "A rich terminal-based profile card with box drawing characters and color formatting for displaying user information."),
    ]},
    # Level 2: Variables 📦
    {"id": "l02", "lessons": [
        _L("Primitive Types", 10, 1), _L("auto Keyword", 15, 1),
        _L("String Type", 15, 1), _L("Constants: const & constexpr", 15, 2),
        _L("Type Inference", 15, 2), _L("Reference Variables", 20, 2),
        _L("Practice: Type Explorer", 20, 2, "practice"),
        _L("Challenge: Sizeof Puzzle", 25, 2, "challenge"),
        _L("Project: Shopping Cart with Discount Engine & Receipt Generator", 60, 3, "project",
           "An e-commerce shopping cart system with discount engine, tax calculations, and receipt generation."),
    ]},
    # Level 3: Operators ⚡
    {"id": "l03", "lessons": [
        _L("Arithmetic & Assignment", 10, 1), _L("Comparison Operators", 10, 1),
        _L("Logical Operators", 15, 1), _L("Bitwise Operators", 20, 2),
        _L("Ternary Operator", 15, 1), _L("Operator Overloading Intro", 25, 3),
        _L("Practice: Bool Expressions", 20, 2, "practice"),
        _L("Challenge: Bit Flags", 30, 3, "challenge"),
        _L("Project: Math Expression Parser — supports +,-,*,/,^,sin,cos,log", 60, 3, "project",
           "A mathematical expression parser supporting arithmetic operators, trigonometric functions, and logarithms."),
    ]},
    # Level 4: Conditionals 🔀
    {"id": "l04", "lessons": [
        _L("if / else if / else", 10, 1), _L("Nested Conditionals", 15, 2),
        _L("Switch Statement", 15, 2), _L("Switch with Strings", 20, 2),
        _L("Structured Bindings (C++17)", 20, 3),
        _L("Practice: Rock Paper Scissors", 20, 2, "practice"),
        _L("Challenge: Mini Compiler (if/else)", 35, 3, "challenge"),
        _L("Project: Multiplayer Quiz Game with Timer, Scoring & Leaderboard", 60, 3, "project",
           "A multiplayer quiz game with timer-based rounds, scoring system, and persistent leaderboard."),
    ]},
    # Level 5: Loops 🔄
    {"id": "l05", "lessons": [
        _L("for Loop", 10, 1), _L("Range-based for", 15, 1),
        _L("while & do-while", 15, 1), _L("Nested Loops", 15, 2),
        _L("break, continue, goto", 15, 2), _L("Loop Patterns", 25, 3, "practice"),
        _L("Practice: FizzBuzz Variants", 20, 2, "practice"),
        _L("Challenge: Spiral Matrix", 35, 3, "challenge"),
        _L("Project: 3D Terminal Starfield with Depth & Speed Controls", 60, 3, "project",
           "A real-time 3D starfield animation rendered in the terminal with adjustable depth and speed parameters."),
    ]},
    # Level 6: Functions 🧩
    {"id": "l06", "lessons": [
        _L("Function Basics", 10, 1), _L("Default Arguments", 15, 2),
        _L("Function Overloading", 20, 2), _L("Inline Functions", 15, 2),
        _L("Pass by Value vs Reference", 20, 2), _L("Const References", 20, 2),
        _L("Recursion", 25, 2), _L("Practice: Power Function", 25, 2, "practice"),
        _L("Challenge: Recursive Permutations", 40, 3, "challenge"),
        _L("Project: Scientific Calculator Library with Complex Number Support", 60, 3, "project",
           "A scientific calculator library with complex number support, mathematical functions, and extensible architecture."),
    ]},
    # Level 7: Arrays & Vectors 📊
    {"id": "l07", "lessons": [
        _L("C-style Arrays", 10, 1), _L("std::array", 15, 2),
        _L("std::vector Basics", 15, 2), _L("Vector Methods", 20, 2),
        _L("Iterators", 20, 2), _L("Algorithms: sort, find, count", 25, 2),
        _L("2D Vectors", 20, 2), _L("Practice: Matrix Class", 30, 3, "practice"),
        _L("Challenge: Two Sum Optimized", 35, 3, "challenge"),
        _L("Project: University Grade Book — GPA Calculator, Transcript Generator", 60, 3, "project",
           "A university grade management system with GPA calculation, transcript generation, and course analytics."),
    ]},
    # Level 8: Strings 📝
    {"id": "l08", "lessons": [
        _L("std::string Basics", 10, 1), _L("String Methods", 15, 1),
        _L("String Concatenation", 15, 2), _L("String Streams", 20, 2),
        _L("Substring & Find", 20, 2), _L("Regex Basics", 30, 3),
        _L("Practice: CSV Parser", 25, 2, "practice"),
        _L("Challenge: String Interning", 35, 3, "challenge"),
        _L("Project: Nano Clone — Full Text Editor with Search, Replace, Syntax Highlight", 60, 3, "project",
           "A terminal-based text editor with search, replace, syntax highlighting, and file management capabilities."),
    ]},
    # Level 9: Pointers & Memory 🧠
    {"id": "l09", "lessons": [
        _L("Raw Pointers Review", 15, 2), _L("Heap vs Stack", 15, 2),
        _L("new & delete", 15, 2), _L("Smart Pointers: unique_ptr", 20, 2),
        _L("Smart Pointers: shared_ptr", 20, 2), _L("Weak Pointers", 25, 3),
        _L("RAII Pattern", 25, 3), _L("Practice: Own Smart Pointer", 35, 3, "practice"),
        _L("Challenge: Memory Pool", 40, 3, "challenge"),
        _L("Project: Complete JSON Parser with Validation, Pretty-Print & Schema Check", 60, 3, "project",
           "A complete JSON parser with validation, pretty-printing, schema checking, and nested object support."),
    ]},
    # Level 10: OOP 🏗️
    {"id": "l10", "lessons": [
        _L("Classes & Objects", 15, 2), _L("Constructors & Destructors", 15, 2),
        _L("Copy Constructor", 20, 2), _L("Move Semantics", 25, 3),
        _L("Inheritance", 20, 2), _L("Virtual Functions & vtable", 25, 3),
        _L("Operator Overloading", 30, 3), _L("RAII Classes", 25, 3),
        _L("Practice: String Class", 35, 3, "practice"),
        _L("Challenge: Inheritance Design", 40, 3, "challenge"),
        _L("Project: 2D Graphics Engine — Draw circles, rectangles, lines on terminal grid", 60, 3, "project",
           "A terminal-based 2D graphics engine capable of drawing circles, rectangles, and lines on a grid display."),
    ]},
    # Level 11: STL & Templates 🌳
    {"id": "l11", "lessons": [
        _L("Templates Basics", 25, 2), _L("Template Specialization", 30, 3),
        _L("STL: map & unordered_map", 20, 2), _L("STL: set & multiset", 20, 2),
        _L("STL: stack & queue", 20, 2), _L("STL Algorithms Deep", 30, 3),
        _L("Lambdas", 25, 3), _L("Practice: Custom Container", 35, 3, "practice"),
        _L("Challenge: LRU Cache", 45, 3, "challenge"),
        _L("Project: Custom STL — vector, map, set, list implementations with iterators", 60, 3, "project",
           "A custom implementation of standard template library containers including vector, map, set, and list with iterators."),
    ]},
    # Level 12: Final Challenge 👑
    {"id": "l12", "lessons": [
        _L("Concurrency: threads", 30, 3), _L("Mutex & Locks", 30, 3),
        _L("Async & Futures", 35, 3), _L("Design Patterns: Singleton", 30, 3),
        _L("Design Patterns: Factory", 30, 3), _L("Design Patterns: Observer", 30, 3),
        _L("Practice: Thread Pool", 40, 3, "practice"),
        _L("Challenge: Lock-Free Stack", 50, 3, "challenge"),
        _L("Challenge: Network Library", 50, 3, "challenge"),
        _L("Capstone: Embedded Key-Value Database with WAL, MVCC & Range Queries", 80, 3, "project", "An embedded key-value database with write-ahead logging, MVCC concurrency, and range query support."),
        _L("👑 C++ Grandmaster Boss", 80, 3, "boss"),
    ]},
    # Level 13: Mini Compiler ⚙️
    {"id": "l13", "lessons": [
        _L("Compilation Pipeline: Preprocessing to Linking", 30, 3),
        _L("Parsing C++ with Recursive Descent", 35, 3, "practice"),
        _L("Challenge: Template-Aware Parser", 40, 3, "challenge"),
        _L("Project: Mini Language Compiler with LLVM IR Generation", 70, 3, "project",
           "A mini programming language compiler with LLVM IR generation, demonstrating the full compilation pipeline from lexing to code generation."),
    ]},
    # Level 14: Portfolio Capstone 🏆
    {"id": "l14", "lessons": [
        _L("System Design: Large-Scale C++ Projects", 35, 3),
        _L("Modern C++ Design Patterns in Practice", 40, 3, "practice"),
        _L("Challenge: Template Metaprogramming Optimization", 45, 3, "challenge"),
        _L("Project: Full Portfolio — Game Engine, DB, Graphics, Network Lib", 80, 3, "project",
           "A comprehensive portfolio project combining a game engine, database, graphics engine, and network library in C++."),
        _L("🏆 C++ Mastery Finale", 100, 3, "boss"),
    ]},
]


# ────────────────────────────────────────────
#  JAVA LANGUAGE — 12 Levels
# ────────────────────────────────────────────
JAVA_LEVELS = [
    # Level 1: First Steps 🌱
    {"id": "l01", "lessons": [
        _L("What is Java?", 10, 1), _L("Hello World in Java", 10, 1, "practice"),
        _L("Class & main Method", 10, 1), _L("System.out.println", 10, 1),
        _L("JDK, JRE, JVM", 10, 1), _L("Comments in Java", 10, 1),
        _L("Practice: Greeting Program", 15, 1, "practice"),
        _L("Challenge: Mini Calculator", 25, 2, "challenge"),
        _L("Project: Animated Terminal Profile Card with Color Themes", 60, 3, "project",
           "An animated terminal profile card with customizable color themes and dynamic display effects."),
    ]},
    # Level 2: Variables 📦
    {"id": "l02", "lessons": [
        _L("Primitive Types", 10, 1), _L("Wrapper Classes", 15, 2),
        _L("String & StringBuilder", 15, 1), _L("var Keyword (Java 10)", 15, 1),
        _L("Constants: final", 15, 2), _L("Type Casting", 15, 2),
        _L("Scanner for Input", 15, 1, "practice"),
        _L("Practice: Temperature Converter", 20, 2, "practice"),
        _L("Challenge: Type Puzzle", 25, 2, "challenge"),
        _L("Project: Smart Shopping Cart with Tax, Discount & Coupon Engine", 60, 3, "project",
           "A smart shopping cart engine supporting tax brackets, discount codes, coupon stacking, and detailed receipts."),
    ]},
    # Level 3: Operators ⚡
    {"id": "l03", "lessons": [
        _L("Arithmetic Operators", 10, 1), _L("Relational Operators", 10, 1),
        _L("Logical Operators", 15, 1), _L("Bitwise Operators", 20, 2),
        _L("Instanceof Operator", 20, 2), _L("Ternary Operator", 15, 1),
        _L("Practice: Bool Expressions", 20, 2, "practice"),
        _L("Challenge: Bit Flags", 30, 3, "challenge"),
        _L("Project: Math Expression Evaluator with Variable Support & History", 60, 3, "project",
           "A mathematical expression evaluator with variable assignment, operator precedence, and computation history."),
    ]},
    # Level 4: Conditionals 🔀
    {"id": "l04", "lessons": [
        _L("if / else if / else", 10, 1), _L("Nested Conditionals", 15, 2),
        _L("Switch Statement", 15, 2), _L("Enhanced Switch (Java 14)", 20, 2),
        _L("Pattern Matching (Java 21)", 25, 3),
        _L("Practice: Rock Paper Scissors", 20, 2, "practice"),
        _L("Challenge: Mini Parser", 35, 3, "challenge"),
        _L("Project: Trivia Quest — Multiplayer Quiz with Difficulty Tiers & Power-Ups", 60, 3, "project",
           "A multiplayer trivia quiz game with difficulty tiers, power-ups, and real-time scoring."),
    ]},
    # Level 5: Loops 🔄
    {"id": "l05", "lessons": [
        _L("for Loop", 10, 1), _L("Enhanced for Loop", 15, 1),
        _L("while & do-while", 15, 1), _L("Nested Loops", 15, 2),
        _L("break, continue", 15, 2), _L("Loop Patterns", 25, 3, "practice"),
        _L("Practice: FizzBuzz Variants", 20, 2, "practice"),
        _L("Challenge: Spiral Matrix", 35, 3, "challenge"),
        _L("Project: Advanced Pattern Generator — 20+ ASCII art patterns with custom size", 60, 3, "project",
           "An advanced ASCII art pattern generator featuring 20+ patterns with customizable sizes and character sets."),
    ]},
    # Level 6: Methods 🧩
    {"id": "l06", "lessons": [
        _L("Method Basics", 10, 1), _L("Static Methods", 15, 2),
        _L("Method Overloading", 20, 2), _L("Varargs", 20, 2),
        _L("Pass by Value (Everything)", 20, 2), _L("Recursion", 25, 2),
        _L("Practice: Power Function", 25, 2, "practice"),
        _L("Challenge: Recursive Permutations", 40, 3, "challenge"),
        _L("Project: Linear Algebra Library — matrices, vectors, determinants, eigenvalues", 60, 3, "project",
           "A comprehensive linear algebra library implementing matrix operations, vector math, determinants, and eigenvalue computation."),
    ]},
    # Level 7: Arrays & Collections 📊
    {"id": "l07", "lessons": [
        _L("Arrays Basics", 10, 1), _L("2D Arrays", 15, 2),
        _L("Arrays Utility Class", 15, 2), _L("ArrayList", 15, 2),
        _L("LinkedList", 20, 2), _L("Iteration Patterns", 20, 2),
        _L("Practice: Matrix Operations", 30, 3, "practice"),
        _L("Challenge: Two Sum Optimized", 35, 3, "challenge"),
        _L("Project: University Grade Book — analytics dashboard, GPA, class rank, export", 60, 3, "project",
           "A university grade book with analytics dashboard, GPA computation, class ranking, and data export features."),
    ]},
    # Level 8: Strings 📝
    {"id": "l08", "lessons": [
        _L("String Immutability", 15, 2), _L("StringBuilder", 15, 1),
        _L("String Methods Deep", 15, 2), _L("String.split & join", 20, 2),
        _L("Regex in Java", 25, 3), _L("Pattern & Matcher", 25, 3),
        _L("Practice: CSV Parser", 25, 2, "practice"),
        _L("Challenge: Palindrome Variants", 35, 3, "challenge"),
        _L("Project: Document Processor — Markdown to HTML, spell check, readability score", 60, 3, "project",
           "A document processing pipeline converting Markdown to HTML with spell checking and readability scoring."),
    ]},
    # Level 9: OOP Fundamentals 🏗️
    {"id": "l09", "lessons": [
        _L("Classes & Objects", 15, 2), _L("Constructors", 15, 2),
        _L("this Keyword", 15, 2), _L("Inheritance", 20, 2),
        _L("Method Overriding", 20, 2), _L("super Keyword", 15, 2),
        _L("Abstract Classes", 25, 3), _L("Interfaces", 25, 3),
        _L("Practice: Shape Hierarchy", 35, 3, "practice"),
        _L("Challenge: Animal Shelter", 40, 3, "challenge"),
        _L("Project: NeoBank — accounts, transfers, transaction history, interest calc", 60, 3, "project",
           "A banking system supporting account management, fund transfers, transaction history, and interest calculations."),
    ]},
    # Level 10: OOP Advanced 🌳
    {"id": "l10", "lessons": [
        _L("Polymorphism Deep", 20, 2), _L("Enums & Enum Methods", 20, 2),
        _L("Records (Java 16)", 20, 2), _L("Sealed Classes", 25, 3),
        _L("Inner Classes", 20, 2), _L("Anonymous Classes", 20, 2),
        _L("Generics Basics", 25, 3), _L("Bounded Generics", 30, 3),
        _L("Practice: Generic Stack", 35, 3, "practice"),
        _L("Challenge: Type-Safe Builder", 40, 3, "challenge"),
        _L("Project: Mini Hibernate — ORM with annotations, SQL generation, relations", 60, 3, "project",
           "A lightweight ORM framework with annotation-based mappings, SQL generation, and entity relationship management."),
    ]},
    # Level 11: Collections & Functional 👑
    {"id": "l11", "lessons": [
        _L("HashMap Deep", 20, 2), _L("TreeMap & LinkedHashMap", 25, 3),
        _L("HashSet & TreeSet", 20, 2), _L("PriorityQueue", 25, 3),
        _L("Comparable vs Comparator", 25, 3), _L("Streams API", 30, 3),
        _L("Collectors Deep", 30, 3), _L("Lambda Expressions", 25, 3),
        _L("Optional & Functional Interfaces", 30, 3),
        _L("Practice: Stream Pipeline", 35, 3, "practice"),
        _L("Challenge: Parallel Streams", 45, 3, "challenge"),
        _L("Project: Stream ETL Pipeline — CSV to Transform to JSON/DB with parallel processing", 60, 3, "project",
           "An ETL pipeline using Java Streams for CSV parsing, data transformation, and parallel processing with JSON output."),
    ]},
    # Level 12: Final Challenge 👑
    {"id": "l12", "lessons": [
        _L("Threading Basics", 30, 3), _L("Synchronized & Locks", 30, 3),
        _L("ExecutorService", 30, 3), _L("CompletableFuture", 35, 3),
        _L("Concurrent Collections", 30, 3), _L("Design Patterns: Singleton", 30, 3),
        _L("Design Patterns: Factory", 30, 3), _L("Design Patterns: Builder", 30, 3),
        _L("Practice: Thread Pool Impl", 40, 3, "practice"),
        _L("Challenge: Dining Philosophers", 50, 3, "challenge"),
        _L("Capstone: Production HTTP Server — routing, middleware, static files, WebSocket", 80, 3, "project", "A production-ready HTTP server with routing, middleware pipeline, static file serving, and WebSocket support."),
        _L("👑 Java Grandmaster Boss", 80, 3, "boss"),
    ]},
    # Level 13: Mini Compiler ⚙️
    {"id": "l13", "lessons": [
        _L("Java Compiler Architecture: javac Internals", 30, 3),
        _L("Parsing with ANTLR", 35, 3, "practice"),
        _L("Challenge: Bytecode Generation", 40, 3, "challenge"),
        _L("Project: Mini Java-to-Bytecode Compiler", 70, 3, "project",
           "A mini Java source-to-bytecode compiler demonstrating lexing, parsing, semantic analysis, and bytecode generation phases."),
    ]},
    # Level 14: Portfolio Capstone 🏆
    {"id": "l14", "lessons": [
        _L("Enterprise Architecture: Microservices vs Monoliths", 35, 3),
        _L("System Design Patterns in Practice", 40, 3, "practice"),
        _L("Challenge: JVM Performance Tuning", 45, 3, "challenge"),
        _L("Project: Full Portfolio — Web Server, ORM, CLI Tools, API Gateway", 80, 3, "project",
           "A comprehensive portfolio project combining a web server, ORM framework, CLI tools, and API gateway in Java."),
        _L("🏆 Java Mastery Finale", 100, 3, "boss"),
    ]},
]


# ────────────────────────────────────────────
#  PYTHON LANGUAGE — 12 Levels
# ────────────────────────────────────────────
PYTHON_LEVELS = [
    # Level 1: First Steps 🌱
    {"id": "l01", "lessons": [
        _L("What is Python?", 10, 1), _L("Hello World in Python", 10, 1, "practice"),
        _L("print() Function", 10, 1), _L("Comments in Python", 10, 1),
        _L("Python Interpreter", 10, 1), _L("Indentation Matters", 10, 1),
        _L("Practice: Your First Script", 15, 1, "practice"),
        _L("Challenge: ASCII Art Generator", 25, 2, "challenge"),
        _L("Project: Animated Greeting Card Generator with Templates & PDF Export", 60, 3, "project",
           "An animated greeting card generator with customizable templates and PDF export functionality."),
    ]},
    # Level 2: Variables 📦
    {"id": "l02", "lessons": [
        _L("Numbers: int & float", 10, 1), _L("Strings in Python", 10, 1),
        _L("Booleans", 10, 1), _L("Variable Naming Rules", 10, 1),
        _L("Multiple Assignment", 15, 1), _L("type() & isinstance()", 15, 2),
        _L("Input with input()", 15, 1, "practice"),
        _L("Practice: Mad Libs Generator", 20, 2, "practice"),
        _L("Challenge: Type Converter", 25, 2, "challenge"),
        _L("Project: Universal Unit Converter — 50+ units, currency rates, CLI & web", 60, 3, "project",
           "A unit converter supporting 50+ units across categories with live currency rates and dual CLI/web interfaces."),
    ]},
    # Level 3: Operators ⚡
    {"id": "l03", "lessons": [
        _L("Arithmetic Operators", 10, 1), _L("Comparison Operators", 10, 1),
        _L("Logical Operators", 15, 1), _L("Assignment Operators", 10, 1),
        _L("Identity & Membership", 20, 2), _L("Operator Precedence", 15, 2),
        _L("Practice: Tip Calculator", 20, 2, "practice"),
        _L("Challenge: Expression Evaluator", 30, 3, "challenge"),
        _L("Project: Live Currency Converter with Rate History Charts & Alert System", 60, 3, "project",
           "A currency converter with real-time rate updates, historical charts, and configurable alert thresholds."),
    ]},
    # Level 4: Conditionals 🔀
    {"id": "l04", "lessons": [
        _L("if Statement", 10, 1), _L("if-else Statement", 10, 1),
        _L("elif Chain", 15, 1), _L("Nested Conditionals", 15, 2),
        _L("Ternary Expression", 15, 2), _L("Match-Case (3.10)", 20, 3),
        _L("Practice: Grade Calculator", 20, 2, "practice"),
        _L("Challenge: Rock Paper Scissors", 25, 2, "challenge"),
        _L("Challenge: Vending Machine", 35, 3, "challenge"),
        _L("Project: AI Number Duel — hints system, difficulty scaling, multiplayer", 60, 3, "project",
           "An AI-powered number guessing game with adaptive difficulty, hint system, and multiplayer support."),
    ]},
    # Level 5: Loops 🔄
    {"id": "l05", "lessons": [
        _L("for Loop with range()", 10, 1), _L("while Loop", 10, 1),
        _L("for...in with Lists", 15, 1), _L("Nested Loops", 15, 2),
        _L("break, continue, else", 15, 2), _L("List Comprehensions", 20, 2),
        _L("Practice: Multiplication Table", 20, 2, "practice"),
        _L("Challenge: FizzBuzz Variants", 25, 2, "challenge"),
        _L("Challenge: Collatz Sequence", 35, 3, "challenge"),
        _L("Project: Password Fortress — generator, strength analyzer, breach checker, vault", 60, 3, "project",
           "A password management tool with generator, strength analyzer, breach checking, and encrypted vault storage."),
    ]},
    # Level 6: Functions 🧩
    {"id": "l06", "lessons": [
        _L("def & return", 10, 1), _L("Parameters & Arguments", 15, 1),
        _L("Default Parameters", 15, 2), _L("*args & **kwargs", 20, 2),
        _L("Lambda Functions", 20, 2), _L("Recursion", 25, 2),
        _L("Scope: local vs global", 20, 2), _L("Closures", 25, 3),
        _L("Practice: Factorial & Fibonacci", 25, 2, "practice"),
        _L("Challenge: Decorator Basics", 40, 3, "challenge"),
        _L("Project: Todo CLI with SQLite, priorities, deadlines, tags, search & export", 60, 3, "project",
           "A feature-rich todo list CLI with SQLite persistence, priority levels, deadlines, tags, and export capabilities."),
    ]},
    # Level 7: Lists & Tuples 📊
    {"id": "l07", "lessons": [
        _L("Lists Basics", 10, 1), _L("List Methods", 15, 1),
        _L("Slicing", 15, 2), _L("Nested Lists", 15, 2),
        _L("Tuples", 15, 1), _L("List Comprehensions Deep", 20, 2),
        _L("Sorting & Searching", 20, 2), _L("Practice: Matrix Operations", 30, 3, "practice"),
        _L("Challenge: Spiral Matrix", 35, 3, "challenge"),
        _L("Project: Contact Manager — CRUD, search, merge duplicates, vCard import/export", 60, 3, "project",
           "A contact management system with CRUD operations, duplicate detection, search, and vCard import/export."),
    ]},
    # Level 8: Strings & Dictionaries 📝
    {"id": "l08", "lessons": [
        _L("String Methods Deep", 15, 2), _L("f-strings & Formatting", 15, 1),
        _L("String Slicing", 15, 2), _L("Regular Expressions", 25, 3),
        _L("dict Basics", 15, 1), _L("dict Methods", 15, 2),
        _L("Nested Dictionaries", 20, 2), _L("JSON Parsing", 20, 2),
        _L("Practice: Word Frequency Counter", 25, 2, "practice"),
        _L("Challenge: Caesar Cipher", 30, 3, "challenge"),
        _L("Project: Finance Tracker — categories, budgets, charts, CSV/JSON export, alerts", 60, 3, "project",
           "A personal finance tracker with category management, budget tracking, charts, and CSV/JSON export."),
    ]},
    # Level 9: File I/O & Error Handling 🧠
    {"id": "l09", "lessons": [
        _L("Reading Files", 15, 2), _L("Writing Files", 15, 2),
        _L("with Statement (Context Manager)", 15, 2), _L("CSV Files", 20, 2),
        _L("try / except / finally", 15, 2), _L("Custom Exceptions", 25, 3),
        _L("Raising Exceptions", 20, 2), _L("Practice: Log Parser", 30, 3, "practice"),
        _L("Challenge: File Deduplicator", 35, 3, "challenge"),
        _L("Project: Markdown Engine — full spec support, themes, syntax highlighting", 60, 3, "project",
           "A Markdown processing engine with full spec support, multiple themes, and syntax highlighting."),
    ]},
    # Level 10: OOP 🏗️
    {"id": "l10", "lessons": [
        _L("Classes & Objects", 15, 2), _L("__init__ & self", 15, 2),
        _L("Instance vs Class Variables", 20, 2), _L("Methods", 15, 2),
        _L("Inheritance", 20, 2), _L("Method Overriding", 20, 2),
        _L("super()", 15, 2), _L("Polymorphism", 25, 3),
        _L("Magic Methods (__str__, __len__)", 25, 3), _L("Properties & @property", 25, 3),
        _L("Practice: Bank Account Class", 30, 3, "practice"),
        _L("Challenge: Card Game Engine", 40, 3, "challenge"),
        _L("Project: Digital Library — catalog, borrowing, reservations, overdue tracking", 60, 3, "project",
           "A digital library system with catalog management, borrowing, reservations, and overdue tracking."),
    ]},
    # Level 11: Advanced Python 🌳
    {"id": "l11", "lessons": [
        _L("Generators & yield", 25, 3), _L("Iterators", 25, 3),
        _L("Decorators with Parameters", 30, 3), _L("Context Managers", 25, 3),
        _L("Map, Filter, Reduce", 20, 2), _L("Sets & Frozensets", 15, 2),
        _L("Collections Module", 20, 2), _L("Virtual Environments", 15, 2),
        _L("Practice: Custom Iterator", 30, 3, "practice"),
        _L("Challenge: Web Scraper", 40, 3, "challenge"),
        _L("Project: Production REST API — auth, CRUD, rate limiting, Swagger docs, tests", 60, 3, "project",
           "A production-grade REST API with authentication, CRUD operations, rate limiting, and Swagger documentation."),
    ]},
    # Level 12: Final Challenge 👑
    {"id": "l12", "lessons": [
        _L("List/Dict Comprehensions Master", 25, 3), _L("Algorithms: Sorting", 30, 3),
        _L("Algorithms: Searching", 30, 3), _L("Data Structures: Stacks & Queues", 30, 3),
        _L("Threading Basics", 30, 3), _L("asyncio Fundamentals", 35, 3),
        _L("Design Patterns: Singleton", 30, 3), _L("Design Patterns: Observer", 30, 3),
        _L("Practice: Algorithm Challenges", 40, 3, "practice"),
        _L("Challenge: Build a Database ORM", 50, 3, "challenge"),
        _L("Capstone: Full-Stack SaaS — auth, dashboard, real-time updates, deployment ready", 80, 3, "project", "A full-stack SaaS application with authentication, dashboard, real-time updates, and deployment configuration."),
        _L("👑 Python Grandmaster Boss", 80, 3, "boss"),
    ]},
    # Level 13: Mini Compiler ⚙️
    {"id": "l13", "lessons": [
        _L("CPython Internals: How Python Runs Your Code", 30, 3),
        _L("Parsing with the AST Module", 35, 3, "practice"),
        _L("Challenge: Custom DSL Parser", 40, 3, "challenge"),
        _L("Project: Mini Python-to-Python Transpiler", 70, 3, "project",
           "A mini Python-to-Python transpiler that transforms source code using AST manipulation and custom DSL parsing."),
    ]},
    # Level 14: Portfolio Capstone 🏆
    {"id": "l14", "lessons": [
        _L("Python Project Architecture: Best Practices", 35, 3),
        _L("System Design Patterns for Python", 40, 3, "practice"),
        _L("Challenge: Async Performance Optimization", 45, 3, "challenge"),
        _L("Project: Full Portfolio — REST API, CLI, Data Pipeline, Web Dashboard", 80, 3, "project",
           "A comprehensive portfolio project combining a REST API, CLI tool, data processing pipeline, and web dashboard in Python."),
        _L("🏆 Python Mastery Finale", 100, 3, "boss"),
    ]},
]


def _generate_lessons_for_level(level_meta, lang_id, level_index):
    """Generate lesson content for levels 15+ using template-based approach.
    Returns a list of lesson dicts with realistic content for each lesson type.
    """
    name = level_meta["name"]
    emoji = level_meta["emoji"]
    desc = level_meta["desc"]
    is_boss = level_index + 1 in (20, 25, 30, 35, 40)
    is_project_level = level_index + 1 in (36, 37, 38)

    lessons = []

    # Theory lesson
    lessons.append(_L(f"{emoji} {name} \u2014 Core Concepts", 15, 1, "theory"))

    # Practice lesson
    lessons.append(_L(f"\u270f\ufe0f {name} \u2014 Hands-On Practice", 20, 2, "practice"))

    # Challenge lesson
    lessons.append(_L(f"\u2694\ufe0f {name} \u2014 Challenge Problem", 35, 3, "challenge"))

    # Project or Boss
    if is_boss:
        lessons.append(_L(f"\U0001f451 {name} \u2014 Boss Battle", 100, 3, "boss"))
    elif is_project_level:
        lessons.append(_L(f"\U0001f4e6 {name} \u2014 Capstone Project", 70, 3, "project",
            git_desc=f"A comprehensive {name.lower()} project demonstrating {desc.lower()}"))
    else:
        lessons.append(_L(f"\U0001f3d7\ufe0f {name} \u2014 Mini Project", 60, 3, "project",
            git_desc=f"A mini project exploring {desc.lower()}"))

    return lessons


# Append levels 15-40 for C
for _i in range(14, 40):
    _meta = LEVEL_THEMES[_i]
    _lessons = _generate_lessons_for_level(_meta, "c", _i)
    C_LEVELS.append({"id": _meta["id"], "lessons": _lessons})

# Append levels 15-40 for C++
for _i in range(14, 40):
    _meta = LEVEL_THEMES[_i]
    _lessons = _generate_lessons_for_level(_meta, "cpp", _i)
    CPP_LEVELS.append({"id": _meta["id"], "lessons": _lessons})

# Append levels 15-40 for Java
for _i in range(14, 40):
    _meta = LEVEL_THEMES[_i]
    _lessons = _generate_lessons_for_level(_meta, "java", _i)
    JAVA_LEVELS.append({"id": _meta["id"], "lessons": _lessons})

# Append levels 15-40 for Python
for _i in range(14, 40):
    _meta = LEVEL_THEMES[_i]
    _lessons = _generate_lessons_for_level(_meta, "python", _i)
    PYTHON_LEVELS.append({"id": _meta["id"], "lessons": _lessons})


def _build_level(lang_id, level_cfg, level_index):
    """Convert level config to full level dict with computed fields."""
    theme = LEVEL_THEMES[level_index]
    lessons = []
    merged_lessons = list(level_cfg["lessons"]) + _bonus_lessons(lang_id, theme)

    for i, l in enumerate(merged_lessons):
        lid = f"{lang_id}-{level_cfg['id']}-{i+1:02d}"
        lesson = {
            "id": lid,
            "title": l["title"],
            "xp": l["xp"],
            "difficulty": l["difficulty"],
            "type": l["type"],
        }
        if "git_description" in l:
            lesson["git_description"] = l["git_description"]
        lessons.append(lesson)
    total_xp = sum(l["xp"] for l in lessons)
    return {
        "id": level_cfg["id"],
        "name": theme["name"],
        "emoji": theme["emoji"],
        "color": theme["color"],
        "bg": theme["bg"],
        "border": theme["border"],
        "text": theme["text"],
        "description": theme["desc"],
        "order": level_index + 1,
        "lessons": lessons,
        "total_lessons": len(lessons),
        "total_xp": total_xp,
    }


def _build_language(lang_id, lang_name, lang_icon, lang_color, lang_desc, levels_cfg):
    """Build full language dict."""
    levels = {}
    total = 0
    for i, cfg in enumerate(levels_cfg):
        level = _build_level(lang_id, cfg, i)
        levels[level["id"]] = level
        total += level["total_lessons"]
    return {
        "id": lang_id,
        "name": lang_name,
        "icon": lang_icon,
        "color": lang_color,
        "description": lang_desc,
        "total_lessons": total,
        "levels": levels,
    }


LANGUAGES = {
    "c": _build_language("c", "C", "⚙️", "#6B7280",
        "Master the foundation of modern programming", C_LEVELS),
    "cpp": _build_language("cpp", "C++", "🔷", "#3B82F6",
        "Object-oriented power with STL and modern features", CPP_LEVELS),
    "java": _build_language("java", "Java", "☕", "#F97316",
        "Enterprise-grade OOP with platform independence", JAVA_LEVELS),
    "python": _build_language("python", "Python", "🐍", "#22C55E",
        "The most popular language for AI, web, and data science", PYTHON_LEVELS),
}


def get_language(language_id: str):
    return LANGUAGES.get(language_id)


def get_all_languages():
    return list(LANGUAGES.values())


def get_level(language_id: str, level_id: str):
    lang = LANGUAGES.get(language_id)
    if not lang:
        return None
    return lang["levels"].get(level_id)


def get_lesson(language_id: str, level_id: str, lesson_id: str):
    level = get_level(language_id, level_id)
    if not level:
        return None
    for lesson in level["lessons"]:
        if lesson["id"] == lesson_id:
            return lesson
    return None


def get_next_lesson(language_id: str, level_id: str, lesson_id: str):
    level = get_level(language_id, level_id)
    if not level:
        return None
    for i, lesson in enumerate(level["lessons"]):
        if lesson["id"] == lesson_id:
            if i + 1 < len(level["lessons"]):
                return level["lessons"][i + 1]
            return None
    return None


def get_random_lessons(language_id: str, count: int = 3):
    """Get random unlocked lessons for quick practice."""
    import random
    lang = LANGUAGES.get(language_id)
    if not lang:
        return []
    all_lessons = []
    for level in lang["levels"].values():
        for lesson in level["lessons"]:
            if lesson["type"] in ("theory", "practice", "challenge"):
                all_lessons.append({**lesson, "level_id": level["id"]})
    return random.sample(all_lessons, min(count, len(all_lessons)))
