"""
Curriculum enrichment — adds JS, Go, Rust tracks + 1000+ auto-generated lessons.
Patches LANGUAGES at import time.
"""
#pylint: skip-file

import random
from .curriculum import LANGUAGES, _L, _build_language

random.seed(42)

# ─── Topic pools for auto-generation ───

ALGO_TOPICS = [
    "Two Sum", "Max Subarray", "Binary Search", "Merge Sort", "Quick Sort",
    "BFS Traversal", "DFS Traversal", "Dijkstra's Algorithm", "Bellman-Ford",
    "Kruskal's MST", "Prim's MST", "Topological Sort", "KMP String Match",
    "Rabin-Karp", "Z-Algorithm", "Floyd-Warshall", "Knapsack DP",
    "LCS DP", "LIS DP", "Edit Distance", "Coin Change DP",
    "Matrix Chain Multiplication", "N-Queens Backtracking",
    "Sudoku Solver", "Graph Coloring", "Hamiltonian Path",
    "Trie Construction", "Segment Tree", "Fenwick Tree",
    "Union Find (DSU)", "Bloom Filter", "LRU Cache", "Sliding Window Max",
    "Rotate Array", "Next Permutation", "Word Break", "Palindrome Partitioning",
    "House Robber DP", "Jump Game", "Gas Station", "Candy Distribution",
    "Trapping Rain Water", "Largest Rectangle in Histogram",
]

CONCEPT_TOPICS = [
    "Time Complexity Analysis", "Space Complexity", "Amortized Analysis",
    "Recursion Tree Method", "Master Theorem", "Divide & Conquer",
    "Greedy vs DP", "Memoization Techniques", "Tabulation Methods",
    "State Space Search", "Pruning Techniques", "Branch & Bound",
    "Randomized Algorithms", "Approximation Algorithms", "Online Algorithms",
    "Bit Masking", "Meet in the Middle", "Disjoint Set Union",
    "Fenwick Tree Applications", "Segment Tree Lazy Propagation",
]

INTERVIEW_TOPICS = [
    "STAR Method Practice", "Tell Me About Yourself", "Why This Company",
    "Leadership Story", "Conflict Resolution Story", "Failure Story",
    "Success Story", "Teamwork Experience", "Mentoring Experience",
    "Dealing with Ambiguity", "Technical Decision Story",
    "Design Thinking Approach", "Agile/Scrum Experience",
    "Cross-functional Collaboration", "Time Management Story",
    "Taking Initiative Example", "Innovation Story", "Debugging Story",
    "Code Review Experience", "Production Incident Story",
]

LANG_SPECIFIC_TOPICS = {
    "c": [
        "Pointer Arithmetic Deep", "Function Pointers", "Dynamic Memory Allocator",
        "Memory-Mapped Files", "Signal Handling", "setjmp/longjmp",
        "Variadic Functions", "Inline Assembly", "Preprocessor Macros",
        "Bit Fields & Unions", "Structure Padding", "Endianness Handling",
        "C11 Threads", "Atomics in C", "Fast I/O Techniques",
        "Profiling with gprof", "Valgrind Memory Analysis", "GDB Debugging",
        "Makefile Mastery", "Static & Dynamic Libraries",
    ],
    "cpp": [
        "SFINAE Concepts", "CRTP Pattern Deep", "Policy-Based Design",
        "Type Erasure", "Expression Templates", "constexpr All The Things",
        "C++20 Coroutines", "C++20 Modules", "C++23 std::expected",
        "Compile-Time Regex", "Fold Expressions", "Concepts Deep Dive",
        "Ranges & Views", "Span & String View", "Allocator Models",
        "Placement New", "Copy Elision & RVO", "ABI Compatibility",
        "C++ Exception Handling Cost", "Linkage & ODR",
    ],
    "java": [
        "Java 21 Pattern Matching", "Record Patterns", "Sequenced Collections",
        "Foreign Function & Memory API", "Vector API", "Structured Concurrency",
        "Scoped Values", "String Templates (Preview)", "Stream Gatherers",
        "Virtual Threads Deep", "JFR Event Streaming", "JLink Custom Runtime",
        "Module System Deep", "ServiceLoader Pattern", "Annotation Processing",
        "JMX Monitoring", "Instrumentation API", "Bytecode Manipulation",
        "GraalVM Native Image", "ZGC & Shenandoah GC",
    ],
    "python": [
        "Metaclasses Deep", "Descriptor Protocol", "Abstract Base Classes",
        "Protocol & Structural Typing", "TypeVar & Generics", "Overload Decorator",
        "Context Variables", "Async Generators & Comprehensions",
        "AnyIO vs asyncio vs trio", "Signal & Slot Pattern", "C Extension Modules",
        "ctypes & cffi Deep", "Cython Optimization", "Numba JIT Compilation",
        "Profile-guided Optimization", "pytest Fixtures Deep", "Property-based Testing",
        "Sphinx Documentation Generation", "Poetry vs pip vs conda", "Nox & Tox",
    ],
    "javascript": [
        "Proxies & Reflect", "Symbol & Well-known Symbols", "Generator Delegation",
        "Async Iterators", "WeakRef & FinalizationRegistry", "Atomics & SharedArrayBuffer",
        "Microtask Queue Deep", "Event Loop Phases", "V8 Optimization Hints",
        "TurboFan JIT Compiler", "Hidden Classes & Inline Caching", "Memory Leak Patterns",
        "Bundle Splitting Strategies", "Tree Shaking Deep", "Code Splitting Patterns",
        "ESLint Custom Rules", "Babel Plugin Development", "Webpack Plugin Development",
        "Vite Plugin Development", "Rollup Hooks Deep",
    ],
}

# ─── Practice variants for each level ───
PRACTICE_VARIANTS = [
    ("Warm-up: {topic} Quick Solve", 15, 1, "practice"),
    ("Practice: {topic} Implementation", 25, 2, "practice"),
    ("Practice: {topic} Edge Cases", 30, 2, "practice"),
    ("Challenge: {topic} Optimized", 40, 3, "challenge"),
    ("Challenge: {topic} Variant", 45, 3, "challenge"),
    ("Project: {topic} Library", 60, 3, "project"),
    ("Code Review: {topic} Solutions", 20, 2, "practice"),
    ("Quiz: {topic} Fundamentals", 15, 1, "practice"),
]

CONCEPT_VARIANTS = [
    ("Learn: {topic}", 20, 2, "theory"),
    ("Apply: {topic} in Practice", 25, 2, "practice"),
    ("Teach: {topic} Back", 30, 2, "challenge"),
    ("Deep Dive: {topic}", 35, 3, "theory"),
    ("Quiz: {topic}", 15, 1, "practice"),
]

INTERVIEW_VARIANTS = [
    ("Practice: {topic}", 20, 2, "practice"),
    ("Record: {topic} Answer", 25, 2, "practice"),
    ("Review: {topic} Examples", 15, 1, "theory"),
    ("Peer: {topic} Mock", 30, 2, "challenge"),
]


def _generate_lessons(topics, variants, xp_mult=1):
    """Generate lessons from a topic pool and variant templates."""
    result = []
    for topic in topics:
        for title_tmpl, xp, diff, type_ in variants:
            title = title_tmpl.format(topic=topic)
            result.append(_L(title, xp * xp_mult, diff, type_))
    return result


# ────────────────────────────────────────────
#  JAVASCRIPT LANGUAGE — 12 Levels
# ────────────────────────────────────────────
JS_LEVELS = [
    {"id": "l01", "lessons": [
        _L("What is JavaScript?", 10, 1), _L("Hello World in JS", 10, 1, "practice"),
        _L("console.log & Debugging", 10, 1), _L("Script Tags & Execution", 10, 1),
        _L("Comments in JS", 10, 1), _L("Browser DevTools", 10, 1),
        _L("Practice: Interactive Greeting", 15, 1, "practice"),
        _L("Challenge: Alert Prompter Mini-App", 25, 2, "challenge"),
        _L("Project: Personal Dashboard — weather widget, clock, quote, theme switch", 60, 3, "project"),
    ]},
    {"id": "l02", "lessons": [
        _L("let, const, var", 10, 1), _L("Data Types", 10, 1),
        _L("Numbers & Math", 10, 1), _L("String Templates", 15, 1),
        _L("Booleans & Truthy/Falsy", 10, 1), _L("Type Coercion", 15, 2),
        _L("typeof & instanceof", 15, 2), _L("Practice: Type Explorer", 20, 2, "practice"),
        _L("Challenge: Type Guard Function", 25, 2, "challenge"),
        _L("Project: Unit Converter Pro — 100+ units, live conversion, history, favorites", 60, 3, "project"),
    ]},
    {"id": "l03", "lessons": [
        _L("Arithmetic Operators", 10, 1), _L("Comparison Operators", 10, 1),
        _L("Logical Operators", 15, 1), _L("Nullish Coalescing", 15, 2),
        _L("Optional Chaining", 15, 2), _L("Spread & Rest", 20, 2),
        _L("Practice: Expression Calculator", 20, 2, "practice"),
        _L("Challenge: Deep Clone Function", 30, 3, "challenge"),
        _L("Project: Math Game — timed arithmetic, leaderboard, difficulty progression", 60, 3, "project"),
    ]},
    {"id": "l04", "lessons": [
        _L("if / else if / else", 10, 1), _L("Nested Conditionals", 15, 2),
        _L("switch Statement", 15, 2), _L("Ternary Operator", 15, 1),
        _L("Short-Circuit Evaluation", 20, 2), _L("Practice: Grade Calculator", 20, 2, "practice"),
        _L("Challenge: Rock Paper Scissors Lizard Spock", 30, 3, "challenge"),
        _L("Project: Adventure Game Engine — branching story, inventory, combat, save/load", 60, 3, "project"),
    ]},
    {"id": "l05", "lessons": [
        _L("for Loop", 10, 1), _L("while & do-while", 10, 1),
        _L("for...of & for...in", 15, 2), _L("Nested Loops", 15, 2),
        _L("break, continue", 15, 2), _L("Loop Performance", 20, 3),
        _L("Practice: FizzBuzz Pro", 20, 2, "practice"),
        _L("Challenge: Pattern Generator", 30, 3, "challenge"),
        _L("Project: Sorting Visualizer — bubble, quick, merge, heap with animation playback", 60, 3, "project"),
    ]},
    {"id": "l06", "lessons": [
        _L("Function Declaration vs Expression", 10, 1), _L("Arrow Functions", 15, 2),
        _L("Parameters & Arguments", 15, 1), _L("Default Parameters", 15, 2),
        _L("Rest Parameters", 15, 2), _L("Closures", 25, 3),
        _L("IIFE", 20, 2), _L("Recursion", 25, 2),
        _L("Practice: Function Library", 25, 2, "practice"),
        _L("Challenge: Memoization Decorator", 40, 3, "challenge"),
        _L("Project: Pure Function Library — map, filter, reduce, compose, curry from scratch", 60, 3, "project"),
    ]},
    {"id": "l07", "lessons": [
        _L("Array Basics", 10, 1), _L("Array Methods: push, pop, shift", 15, 1),
        _L("map, filter, reduce", 20, 2), _L("sort & reverse", 15, 2),
        _L("Spread with Arrays", 15, 2), _L("Destructuring", 20, 2),
        _L("Nested Arrays", 15, 2), _L("Practice: Array Utilities", 25, 2, "practice"),
        _L("Challenge: Flatten & Group", 35, 3, "challenge"),
        _L("Project: Data Dashboard — CSV load, sort, filter, aggregate, chart export", 60, 3, "project"),
    ]},
    {"id": "l08", "lessons": [
        _L("String Methods Deep", 15, 2), _L("Regex in JavaScript", 25, 3),
        _L("Template Literals Advanced", 15, 2), _L("String Normalization", 20, 2),
        _L("Object Basics", 15, 1), _L("Object Methods & this", 20, 2),
        _L("Object.keys, values, entries", 20, 2), _L("JSON.parse & stringify", 15, 2),
        _L("Practice: Deep Object Compare", 30, 3, "practice"),
        _L("Challenge: Object Path Resolver", 40, 3, "challenge"),
        _L("Project: Document Search Engine — full-text search, relevance scoring, snippets", 60, 3, "project"),
    ]},
    {"id": "l09", "lessons": [
        _L("DOM Basics: querySelector", 15, 2), _L("DOM Manipulation", 20, 2),
        _L("Event Listeners", 20, 2), _L("Event Delegation", 25, 3),
        _L("Creating & Removing Elements", 20, 2), _L("Practice: Dynamic To-Do List", 25, 2, "practice"),
        _L("Practice: Modal & Dropdown Components", 25, 2, "practice"),
        _L("Challenge: Drag & Drop", 40, 3, "challenge"),
        _L("Project: Kanban Board — columns, drag-drop cards, localStorage persistence, theme", 60, 3, "project"),
    ]},
    {"id": "l10", "lessons": [
        _L("Callbacks & Callback Hell", 15, 2), _L("Promises Basics", 20, 2),
        _L("Chaining Promises", 20, 2), _L("async/await", 25, 3),
        _L("Error Handling in Async", 25, 3), _L("Promise.all & race", 25, 3),
        _L("Fetch API", 20, 2), _L("Practice: Promise Utilities", 30, 3, "practice"),
        _L("Challenge: Promise Pool (concurrency limit)", 45, 3, "challenge"),
        _L("Project: Real-Time Chat App — WebSocket, rooms, typing indicator, emoji, notifications", 60, 3, "project"),
    ]},
    {"id": "l11", "lessons": [
        _L("Classes & Constructors", 20, 2), _L("Prototype Chain", 25, 3),
        _L("Inheritance: extends & super", 20, 2), _L("Getters & Setters", 20, 2),
        _L("Static Methods & Fields", 20, 2), _L("Private Fields", 25, 3),
        _L("Mixin Pattern", 25, 3), _L("Practice: Car Dealership OOP", 30, 3, "practice"),
        _L("Challenge: Observer Pattern from Scratch", 40, 3, "challenge"),
        _L("Project: Tiny React — Virtual DOM, JSX renderer, hooks, component lifecycle", 60, 3, "project"),
    ]},
    {"id": "l12", "lessons": [
        _L("Modules: import/export", 20, 2), _L("Module Bundlers: Webpack", 25, 3),
        _L("Web APIs: LocalStorage, SessionStorage", 20, 2), _L("Web Workers", 25, 3),
        _L("Service Workers & PWA", 30, 3), _L("Design Patterns: Module", 25, 3),
        _L("Design Patterns: Singleton", 25, 3), _L("Design Patterns: Factory", 30, 3),
        _L("Performance Optimization", 30, 3), _L("Practice: Bundle Analyzer", 40, 3, "practice"),
        _L("Challenge: Custom Framework Benchmark", 50, 3, "challenge"),
        _L("Capstone: PWA Note App — offline, sync, rich text, export, end-to-end encrypted", 80, 3, "project"),
        _L("👑 JavaScript Grandmaster Boss", 80, 3, "boss"),
    ]},
]

# ────────────────────────────────────────────
#  LANGUAGE-SPECIFIC DEEP CONTENT ──────────────
# ────────────────────────────────────────────

def _build_lang_extra(lang_id):
    """Generate extra lessons for a language."""
    lessons = []

    # Algorithm practice for each topic
    algo_lessons = _generate_lessons(ALGO_TOPICS[:20], PRACTICE_VARIANTS)
    lessons.extend(algo_lessons)

    # Concept deep dives
    concept_lessons = _generate_lessons(CONCEPT_TOPICS[:15], CONCEPT_VARIANTS)
    lessons.extend(concept_lessons)

    # Interview prep lessons
    interview_lessons = _generate_lessons(INTERVIEW_TOPICS[:15], INTERVIEW_VARIANTS)
    lessons.extend(interview_lessons)

    # Language-specific topics
    lang_topics = LANG_SPECIFIC_TOPICS.get(lang_id, [])
    for topic in lang_topics:
        lessons.append(_L(f"Master: {topic}", 35, 3, "theory"))
        lessons.append(_L(f"Practice: {topic}", 40, 3, "practice"))
        lessons.append(_L(f"Challenge: {topic} Pro", 50, 3, "challenge"))

    # Additional general practice
    for i in range(20):
        difficulty = (i % 3) + 1
        xp = 15 + (i * 2)
        t = "practice" if i % 3 != 0 else "challenge"
        lessons.append(_L(f"Sprint #{i+1}: Mixed Skills Challenge", xp, difficulty, t))

    # Interview coding problems
    for i, problem in enumerate([
        "Reverse a Linked List", "Valid Parentheses", "Merge Two Sorted Lists",
        "Maximum Depth of Binary Tree", "Invert Binary Tree", "Best Time to Buy Stock",
        "Contains Duplicate", "Valid Anagram", "Number of Islands",
        "Climbing Stairs", "Diameter of Binary Tree", "Middle of Linked List",
        "Maximum Subarray", "Product of Array Except Self", "3Sum",
        "Set Matrix Zeroes", "Group Anagrams", "Longest Substring Without Repeats",
        "Longest Palindromic Substring", "Container With Most Water",
    ]):
        lessons.append(_L(f"Coding: {problem} — {lang_id.upper()} Solution", 30 + i, 2 + (i % 2), "challenge"))

    return lessons


# ────────────────────────────────────────────
#  GENERATE GO LANGUAGE — 12 Levels ───────────
# ────────────────────────────────────────────
GO_LEVELS = []

LEVEL_NAMES = [
    ("First Steps", "Hello, Go!", "basic syntax"),
    ("Variables & Types", "strong typing, inference, zero values", "data types"),
    ("Control Flow", "if, for, switch, defer", "control structures"),
    ("Functions & Methods", "functions, multiple returns, methods", "functions"),
    ("Arrays & Slices", "fixed arrays, dynamic slices", "collections"),
    ("Maps & Structs", "key-value stores, custom types", "data structures"),
    ("Interfaces & Generics", "interfaces, type params, constraints", "advanced types"),
    ("Concurrency: Goroutines", "goroutines, channels, select", "concurrency"),
    ("Concurrency: Patterns", "worker pools, pipelines, fan-out/in", "async patterns"),
    ("File I/O & Error Handling", "files, errors, panic/recover", "error handling"),
    ("Testing & Benchmarking", "unit tests, table tests, benchmarks", "quality"),
    ("Building CLI & Web Apps", "flag package, HTTP server, middleware", "production"),
]

for li, (name, focus, category) in enumerate(LEVEL_NAMES):
    lessons = []
    lsn = f"l{li+1:02d}"

    # Base theory lessons
    lessons.append(_L(f"Welcome to {name}", 10, 1, "theory"))
    lessons.append(_L(f"{focus} — Overview", 10, 1, "theory"))
    lessons.append(_L(f"Practice: Basic {category}", 15, 1, "practice"))
    lessons.append(_L(f"Practice: {name} In Depth", 20, 2, "practice"))
    lessons.append(_L(f"Challenge: {name} Problems", 30, 3, "challenge"))

    # Add Go-specific content
    if li >= 3:
        lessons.append(_L(f"Go Idiom: {name} Best Practices", 25, 2, "theory"))
    if li >= 6:
        lessons.append(_L(f"Advanced: {name} Patterns", 35, 3, "theory"))
    if li >= 8:
        lessons.append(_L(f"Concurrent: {name} in Practice", 40, 3, "practice"))

    # Add generated content
    lessons.extend(_generate_lessons(ALGO_TOPICS[li*4:(li+1)*4], PRACTICE_VARIANTS[:4]))
    lessons.extend(_generate_lessons(CONCEPT_TOPICS[li*2:(li+1)*2], CONCEPT_VARIANTS[:3]))

    # Project for each level
    project_names = [
        "Hello World HTTP Server with Config & Logging",
        "Type Conversion CLI Tool",
        "File System Walker with Filters",
        "REST API Client Generator",
        "In-Memory Key-Value Store with TTL",
        "CSV to JSON Converter with Validation",
        "Load Balancer Simulator",
        "Concurrent Web Crawler with Rate Limiting",
        "Chat Server with Rooms & History",
        "Git-Lite: Basic Version Control",
        "Complete Unit Test Suite for Production Code",
        "Full-Stack TODO App with Postgres & React Frontend",
    ]
    lessons.append(_L(f"Project: {project_names[li]}", 60 + li*5, 3, "project"))

    # Boss battle at end
    if li == max(range(12)):
        lessons.append(_L("👑 Go Grandmaster Boss Battle", 80, 3, "boss"))

    GO_LEVELS.append({"id": lsn, "lessons": lessons})


# ────────────────────────────────────────────
#  GENERATE RUST LANGUAGE — 12 Levels ─────────
# ────────────────────────────────────────────
RUST_LEVELS = []

RUST_LEVEL_NAMES = [
    ("Rust Fundamentals", "cargo, hello world, rustup", "toolchain"),
    ("Variables & Ownership", "ownership, borrowing, references", "memory model"),
    ("Control Flow & Pattern Matching", "if, match, loops, if let", "control flow"),
    ("Functions & Error Handling", "Result, Option, ?, panic", "error handling"),
    ("Structs & Enums", "struct, enum, impl, Option<T>", "data modeling"),
    ("Collections & Iterators", "Vec, HashMap, iterators, closures", "collections"),
    ("Traits & Generics", "traits, generics, trait bounds, impl Trait", "abstractions"),
    ("Lifetimes & Smart Pointers", "lifetime annotations, Box, Rc, Arc", "memory safety"),
    ("Concurrency: Threads & Async", "threads, async/await, tokio", "concurrency"),
    ("Unsafe Rust & FFI", "unsafe, raw pointers, C bindings", "systems programming"),
    ("Testing & Documentation", "unit tests, integration tests, doc tests", "quality"),
    ("Building CLI & Web in Rust", "clap, actix-web, serde, tracing", "production"),
]

for li, (name, focus, category) in enumerate(RUST_LEVEL_NAMES):
    lessons = []
    lsn = f"l{li+1:02d}"

    lessons.append(_L(f"Welcome to {name}", 10, 1, "theory"))
    lessons.append(_L(f"{focus} — Deep Dive", 15, 1, "theory"))
    lessons.append(_L(f"Practice: {category} Basics", 20, 2, "practice"))
    lessons.append(_L(f"Practice: {name} Patterns", 25, 2, "practice"))
    lessons.append(_L(f"Challenge: {name} Quiz", 30, 3, "challenge"))

    if li >= 2:
        lessons.append(_L(f"Rusty Style: {name} Idiomatic", 25, 2, "theory"))
    if li >= 5:
        lessons.append(_L(f"Advanced: {name} in Systems", 35, 3, "theory"))
    if li >= 7:
        lessons.append(_L(f"Zero-Cost: {name} Optimization", 40, 3, "practice"))

    lessons.extend(_generate_lessons(ALGO_TOPICS[li*4+2:(li+1)*4+2], PRACTICE_VARIANTS[:4]))
    lessons.extend(_generate_lessons(CONCEPT_TOPICS[li*2+1:(li+1)*2+1], CONCEPT_VARIANTS[:3]))

    project_names = [
        "CLI Password Manager with Encryption",
        "Memory-Safe Linked List",
        "Mini grep with Regex Support",
        "HTTP Load Balancer with Health Checks",
        "Custom Allocator Implementation",
        "JSON Parser with Serde-like Macros",
        "Actor Framework for Concurrent State",
        "Async Redis Client from Scratch",
        "WebSocket Chat Server with Tokio",
        "Minimal Container Runtime",
        "Property-based Testing Framework",
        "Production API Server with SQLx & Actix-web",
    ]
    lessons.append(_L(f"Project: {project_names[li]}", 60 + li*5, 3, "project"))

    if li == max(range(12)):
        lessons.append(_L("👑 Rust Grandmaster Boss Battle", 80, 3, "boss"))

    RUST_LEVELS.append({"id": lsn, "lessons": lessons})


# ────────────────────────────────────────────
#  CROSS-LANGUAGE CONTENT ─────────────────────
# ────────────────────────────────────────────

CROSS_LANG_LESSONS = []
lang_pairs = [
    ("C vs Python", "Python vs C", "memory, speed, use cases"),
    ("C++ vs Rust", "Rust vs C++", "safety, zero-cost, ecosystem"),
    ("Java vs Go", "Go vs Java", "concurrency, OOP, simplicity"),
    ("Python vs JavaScript", "JS vs Python", "typing, async, web"),
    ("C vs Rust", "Rust vs C", "systems, control, safety"),
    ("Java vs C#", "C# vs Java", "ecosystem, features, JVM/CLR"),
    ("Go vs Rust", "Rust vs Go", "simplicity vs safety"),
    ("C++ vs Java", "Java vs C++", "OOP, performance, tooling"),
    ("JS vs TypeScript", "TS vs JS", "types, tooling, adoption"),
    ("Python vs C++", "C++ vs Python", "prototyping vs performance"),
]
for a, b, focus in lang_pairs:
    CROSS_LANG_LESSONS.append(_L(f"Compare: {a} — {focus}", 30, 3, "theory"))
    CROSS_LANG_LESSONS.append(_L(f"Port: {a} Code Examples", 35, 3, "practice"))
    CROSS_LANG_LESSONS.append(_L(f"Challenge: Translate {a} Project", 50, 3, "challenge"))


# Install 50-level curriculum (replaces 12-level with 50-level for all languages)
from .curriculum_50_levels import install_50_level_curriculum
_ = install_50_level_curriculum()

# Install web development tracks (HTML, CSS, SQL, TypeScript, React, Node.js)
from .curriculum_web import install_web_curriculum
_ = install_web_curriculum()

# Install depth expansion — doubles every track (core 50 -> 100 levels, web 20 -> 40)
from .curriculum_depth import install_depth_curriculum
_ = install_depth_curriculum()

# Install world-class enrichment — adds why/real_world/interview/build/problem_set/engineering/career
# to every lesson + interview_prep/career_mapping/capstone_challenge to every level.
# Runs LAST so it enriches the fully-built LANGUAGES state (auto-installs on import).
from . import curriculum_world_class  # noqa: E402,F401
