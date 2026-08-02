"""
Massive curriculum expansion — 50 levels per language, each with 10-16 lessons.
7 languages × 50 levels × ~13 lessons = ~4,500+ lessons.
Replaces the 12-level definitions in curriculum.py.
"""
#pylint: skip-file

import random
from .curriculum import LANGUAGES, _L, LEVEL_THEMES as _OLD_THEMES

random.seed(42)

# ─── 50 Level themes ───
LEVELS_50 = [
    ("Hello World", "🌱", "#22C55E", "First program & basic syntax"),
    ("Variables & Data", "📦", "#3B82F6", "Types, declarations, naming"),
    ("Operators", "⚡", "#F59E0B", "Arithmetic, comparison, logical"),
    ("Conditionals", "🔀", "#8B5CF6", "if/else, switch, ternary"),
    ("Loops I", "🔄", "#EF4444", "for, while, do-while"),
    ("Loops II", "🔁", "#EC4899", "Nested loops, patterns"),
    ("Functions I", "🧩", "#06B6D4", "Definition, parameters, return"),
    ("Functions II", "🔧", "#10B981", "Overloading, recursion"),
    ("Arrays I", "📊", "#F97316", "1D arrays, traversal"),
    ("Arrays II", "📈", "#6366F1", "2D arrays, matrix ops"),
    ("Strings I", "📝", "#14B8A6", "String basics, methods"),
    ("Strings II", "🔤", "#7C3AED", "Pattern matching, regex"),
    ("Pointers & Memory", "🧠", "#DB2777", "Pointers, allocation"),
    ("Memory Management", "🗑️", "#0EA5E9", "Stack vs heap, leaks"),
    ("Structs & Unions", "🏗️", "#84CC16", "Custom types, nesting"),
    ("File I/O I", "📂", "#D946EF", "Read/write, streams"),
    ("File I/O II", "💾", "#0284C7", "Binary files, serialization"),
    ("Error Handling", "⚠️", "#E11D48", "Exceptions, error codes"),
    ("Debugging", "🐛", "#64748B", "Tools, strategies"),
    ("Testing", "🧪", "#2563EB", "Unit tests, assertions"),
    ("Recursion Deep", "🔄", "#EA580C", "Advanced recursion"),
    ("Search Algorithms", "🔍", "#16A34A", "Linear, binary, ternary"),
    ("Sorting I", "📶", "#9333EA", "Bubble, selection, insertion"),
    ("Sorting II", "📊", "#0891B2", "Merge, quick, heap sort"),
    ("Data Structures: Stack", "📚", "#D97706", "Stack implementations"),
    ("Data Structures: Queue", "🚶", "#059669", "Queue, circular, deque"),
    ("Linked Lists I", "⛓️", "#BE123C", "Singly linked list"),
    ("Linked Lists II", "🔗", "#1D4ED8", "Doubly, circular lists"),
    ("Trees I", "🌳", "#065F46", "Binary trees, traversals"),
    ("Trees II", "🌲", "#6D28D9", "BST, AVL, Red-Black"),
    ("Heaps & Priority", "⛰️", "#B45309", "Max-heap, min-heap"),
    ("Hashing", "🔑", "#9D174D", "Hash tables, collisions"),
    ("Graphs I", "🕸️", "#1E3A5F", "Adjacency, BFS, DFS"),
    ("Graphs II", "🌐", "#4C1D95", "Shortest path, MST"),
    ("Dynamic Programming I", "🧮", "#701A75", "Memoization, tabulation"),
    ("Dynamic Programming II", "⚗️", "#0F766E", "Knapsack, LCS, edit distance"),
    ("Greedy Algorithms", "💰", "#A16207", "Activity selection, Huffman"),
    ("Backtracking", "↩️", "#831843", "N-Queens, Sudoku"),
    ("Bit Manipulation", "🔢", "#3730A3", "Bitwise ops, masks"),
    ("Advanced Topics I", "🚀", "#0D9488", "Tries, segment trees"),
    ("Advanced Topics II", "🛸", "#6B21A8", "Union find, Bloom filter"),
    ("Design Patterns I", "📐", "#B91C1C", "Singleton, Factory, Observer"),
    ("Design Patterns II", "📏", "#0369A1", "Strategy, Decorator, Adapter"),
    ("Concurrency I", "⚙️", "#15803D", "Threads, basics"),
    ("Concurrency II", "🔩", "#7E22CE", "Locks, race conditions"),
    ("Performance", "📈", "#A21CAF", "Optimization, profiling"),
    ("System Design I", "🏛️", "#0E7490", "Architecture patterns"),
    ("System Design II", "🏗️", "#92400E", "Scaling, databases"),
    ("Interview Prep I", "🎯", "#1E40AF", "Mock questions, tips"),
    ("Final Challenge", "👑", "#EAB308", "Capstone + Boss Battle"),
]

# ─── Phase labels ───
PHASES = [
    (0, "Foundation"), (10, "Core"), (20, "Intermediate"),
    (30, "Advanced"), (40, "Expert"),
]


def _phase_for_level(idx):
    for start, phase in reversed(PHASES):
        if idx >= start:
            return phase
    return "Foundation"


# ─── Topic generators per language ───

C_TOPICS = {
    "base": ["printf formatting", "scanf tricks", "preprocessor directives", "typedef usage", "enum types", "void pointers", "function pointers", "variadic functions", "setjmp/longjmp", "signal handling", "errno handling", "assert macro", "static variables", "extern linkage", "register keyword", "volatile keyword", "const correctness", "restrict keyword", "inline functions", "compound literals"],
    "advanced": ["memory pools", "ring buffers", "lock-free queues", "reference counting", "arena allocators", "buddy allocator", "slab allocator", "object pools", "memory barriers", "cache line padding", "false sharing", "SIMD intrinsics", "inline assembly", "ARM vs x86", "position-independent code", "dynamic loading", "library interposition", "PLT/GOT", "stack smashing", "ROP gadgets"],
    "projects": ["C Compiler", "Tiny Shell", "HTTP Server", "Database Engine", "Network Proxy", "Debugger", "Profiler", "Bootloader", "Device Driver", "Emulator", "Firmware", "OS Kernel Module", "File System", "TLS Library", "Audio Processor", "Game Engine", "Physics Sim", "Chat Server", "Web Assembly", "Crypto Library"],
}

CPP_TOPICS = {
    "base": ["iostream deep", "string_view", "span", "range-based for", "auto & decltype", "nullptr", "constexpr", "static_assert", "enum class", "explicit", "friend functions", "virtual inheritance", "pure virtual", "abstract classes", "virtual destructor", "namespace nesting", "using declarations", "ADL lookup", "SFINAE", "type traits"],
    "advanced": ["CRTP", "Policy classes", "Type erasure", "Expression templates", "Variadic templates", "Fold expressions", "Concepts", "Ranges", "Coroutines", "Modules", "std::optional", "std::variant", "std::any", "std::expected", "std::chrono", "iostream performance", "memory order", "atomic operations", "lock-free programming", "wait-free data structures"],
    "projects": ["STL Implementation", "Game Engine", "Physics Engine", "Audio DAW", "3D Renderer", "Network Library", "Database Client", "Graph Library", "Regex Engine", "JSON Library", "XML Parser", "Protobuf Compiler", "Virtual Machine", "JIT Compiler", "Debugger", "Profiling Tool", "Package Manager", "Build System", "Code Linter", "Static Analyzer"],
}

JAVA_TOPICS = {
    "base": ["JVM architecture", "class loading", "bytecode", "garbage collection", "JIT compilation", "method area", "heap structure", "stack frames", "string pool", "reflection API", "dynamic proxies", "annotation processing", "servlet container", "JDBC connections", "connection pooling", "transaction management", "JPA entities", "lazy loading", "N+1 problem", "caching strategies"],
    "advanced": ["virtual threads", "structured concurrency", "scoped values", "vector API", "foreign memory", "panama project", "value types", "pattern matching", "record patterns", "sequenced collections", "stream gatherers", "string templates", "ZGC tuning", "G1GC tuning", "Shenandoah GC", "heap dump analysis", "thread dump analysis", "flight recorder", "JMC profiling", "async profiling"],
    "projects": ["Spring Boot App", "Microservices", "API Gateway", "Service Mesh", "Event Sourcing", "CQRS System", "Message Broker", "Stream Processor", "Data Pipeline", "Search Engine", "Recommendation System", "Payment Gateway", "Banking System", "Trading Platform", "Monitoring System", "Alert Manager", "Config Server", "Discovery Service", "Circuit Breaker", "Rate Limiter"],
}

PYTHON_TOPICS = {
    "base": ["list comprehensions", "generator expressions", "decorator patterns", "context managers", "descriptors", "metaclasses", "abstract base classes", "protocol classes", "dataclasses", "attrs library", "pydantic models", "type hints deep", "generic types", "overload decorator", "TypedDict", "Literal types", "Optional & Union", "Callable types", "TypeVar bounds", "Protocol structural"],
    "advanced": ["asyncio event loop", "uvloop vs asyncio", "trio nurseries", "anyio backends", "async context managers", "async generators", "async comprehensions", "Cython optimization", "Numba JIT", "ctypes deep", "cffi usage", "C extensions", "PyPy vs CPython", "GIL internals", "multiprocessing", "shared memory", "distributed computing", "Dask graphs", "Ray framework", "Celery workers"],
    "projects": ["Async Web Framework", "Task Queue", "Workflow Engine", "Data Pipeline", "ML Training Pipeline", "Feature Store", "Model Registry", "A/B Testing Platform", "Feature Flag System", "Configuration Service", "Secret Manager", "Rate Limiter", "API Gateway", "GraphQL Server", "gRPC Service", "WebSocket Server", "Pub/Sub System", "Event Store", "Command Bus", "Event Sourcing"],
}

JS_TOPICS = {
    "base": ["hoisting deep", "scope chain", "execution context", "this binding", "call/apply/bind", "prototype chain", "new keyword", "class syntax", "private fields", "static initialization", "decorators proposal", "records & tuples", "temporal API", "array buffers", "typed arrays", "data views", "blob & file", "streams API", "compression API", "encoding API"],
    "advanced": ["V8 optimization", "TurboFan JIT", "inline caching", "hidden classes", "memory profiling", "heap snapshots", "allocation sampling", "async stack traces", "microtask queue", "event loop phases", "message channel", "broadcast channel", "shared workers", "service workers", "cache API", "indexedDB deep", "web locks", "scheduling API", "prioritized tasks", "idle callback"],
    "projects": ["React Framework", "State Manager", "Router Library", "Form Library", "Testing Framework", "Bundler", "Dev Server", "Component Library", "Icon Library", "Animation Library", "Drag & Drop", "Spreadsheet", "Rich Text Editor", "Diagram Editor", "Chart Library", "Data Grid", "Virtual Scroller", "Form Builder", "Workflow Editor", "Low-Code Platform"],
}

GO_TOPICS = {
    "base": ["goroutine lifecycle", "channel types", "buffered channels", "select statement", "context package", "defer deep", "panic/recover", "error wrapping", "error.Is/As", "interface satisfaction", "type assertions", "type switches", "embedding", "reflection", "go generate", "build tags", "vendoring", "go mod graph", "workspaces", "toolchain management"],
    "advanced": ["memory model", "happens-before", "sync.Pool", "singleflight", "errgroup", "semaphore", "ring buffer", "lock-free design", "bounded concurrency", "fan-out/fan-in", "pipeline patterns", "generics deep", "constraints", "comparable", "ordered", "slices package", "maps package", "sort package deep", "testing/synctest", "fuzzing"],
    "projects": ["Web Framework", "REST API Server", "gRPC Service", "GraphQL Server", "CLI Framework", "Task Runner", "File Sync Tool", "Backup System", "Log Aggregator", "Metrics Collector", "Service Mesh Sidecar", "API Gateway", "Load Balancer", "Reverse Proxy", "DNS Server", "Mail Server", "Notification Hub", "Feature Flag Service", "A/B Testing Service", "Configuration Manager"],
}

RUST_TOPICS = {
    "base": ["ownership rules", "borrowing checker", "lifetime elision", "lifetime bounds", "static lifetime", "trait objects", "dyn vs impl", "associated types", "generic associated types", "const generics", "type aliases", "newtype pattern", "phantom types", "pin & unpin", "async traits", "impl Trait", "dyn Trait", "trait bounds", "where clauses", "HRTB"],
    "advanced": ["unsafe deep", "raw pointer rules", "union access", "FFI safety", "ABI compatibility", "no_std programming", "allocator API", "global allocator", "custom allocator", "SIMD in Rust", "inline assembly", "wasm targets", "embedded Rust", "RTIC framework", "type state pattern", "builder pattern", "arena allocation", "generational arena", "ECS architecture", "borrow splitting"],
    "projects": ["Async Runtime", "Web Framework", "Database Driver", "Container Runtime", "Orchestrator", "Monitoring Agent", "Tracing Library", "Logging Framework", "Serialization Lib", "Parser Generator", "Linter", "Formatter", "Language Server", "Package Manager", "Build Cacher", "Test Runner", "Benchmark Harness", "Fuzzing Engine", "Property Tester", "Mutation Tester"],
}

LANG_TOPICS = {
    "c": C_TOPICS, "cpp": CPP_TOPICS, "java": JAVA_TOPICS,
    "python": PYTHON_TOPICS, "javascript": JS_TOPICS,
    "go": GO_TOPICS, "rust": RUST_TOPICS,
}


def _gen_level(topics_pool, lang_id, idx, total):
    """Generate lessons for a single level from topic pools."""
    lessons = []
    theme = LEVELS_50[idx]
    phase = _phase_for_level(idx)
    base_topic = theme[0]
    
    base_pool = topics_pool["base"]
    adv_pool = topics_pool["advanced"]
    proj_pool = topics_pool["projects"]
    
    base_count = len(base_pool)
    adv_count = len(adv_pool)
    proj_count = len(proj_pool)
    
    # Phase-based multipliers
    diff_base = min(3, 1 + idx // 15)
    diff_adv = min(3, 1 + idx // 10)
    xp_base = 10 + idx
    xp_adv = 20 + idx * 2
    xp_proj = 50 + idx * 3
    
    # Base theory lessons
    lessons.append(_L(f"{base_topic}: Introduction", xp_base, diff_base, "theory"))
    lessons.append(_L(f"{base_topic}: Key Concepts", xp_base, diff_base, "theory"))
    
    # Language-specific topic from base pool
    if base_pool:
        bt = base_pool[(idx * 3) % base_count]
        lessons.append(_L(f"{bt} — Theory", xp_base + 5, diff_base, "theory"))
    if len(base_pool) > 1:
        bt2 = base_pool[(idx * 3 + 1) % base_count]
        lessons.append(_L(f"{bt2} — In Practice", xp_base + 10, diff_base + (1 if idx > 15 else 0), "practice"))
    
    # Practice lessons (2-3 per level)
    for p_idx in range(2):
        if base_pool:
            bt = base_pool[(idx * 3 + p_idx * 2) % base_count]
            lessons.append(_L(f"Practice: {bt}", xp_base + 5 + p_idx * 5, diff_base + p_idx, "practice"))
    
    # Coding challenge
    if base_pool:
        bt = base_pool[(idx * 7) % base_count]
        lessons.append(_L(f"Challenge: {bt} Mastery", xp_adv, min(3, diff_adv + 1), "challenge"))
    
    # Advanced topic (from level 10+)
    if idx >= 10 and adv_pool:
        at = adv_pool[(idx * 5) % adv_count]
        lessons.append(_L(f"{at} — Deep Dive", xp_adv, diff_adv, "theory"))
        lessons.append(_L(f"Practice: {at}", xp_adv + 10, diff_adv, "practice"))
        lessons.append(_L(f"Challenge: {at} Implementation", xp_adv + 20, min(3, diff_adv + 1), "challenge"))
    
    # Algorithm practice (mix of classic problems)
    algos = ["Two Sum", "Reverse Array", "Binary Search", "Merge Sorted", 
             "Max Subarray", "Rotate Array", "Find Duplicate", "Valid Parentheses",
             "Linked List Cycle", "Tree Traversal", "Graph BFS", "Graph DFS",
             "DP Fibonacci", "Knapsack Basic", "LCS Basic"]
    algo = algos[(idx * 3) % len(algos)]
    lessons.append(_L(f"Algo: {algo} — {lang_id.upper()} Solution", xp_adv + 15, diff_adv, "challenge"))
    
    if idx >= 25:
        algo2 = algos[(idx * 5 + 2) % len(algos)]
        lessons.append(_L(f"Algo: {algo2} — Optimized Approach", xp_adv + 25, 3, "challenge"))
    
    # Interview practice (from level 20+)
    if idx >= 20:
        interview_topics = ["System Design", "Behavioral", "Leadership", "Conflict Resolution",
                            "Technical Decision", "Code Review", "Estimation", "Trade-offs"]
        it = interview_topics[(idx * 3) % len(interview_topics)]
        lessons.append(_L(f"Interview: {it} Practice", xp_adv + 10, diff_adv, "practice"))
        if idx >= 30:
            it2 = interview_topics[(idx * 5 + 1) % len(interview_topics)]
            lessons.append(_L(f"Mock: {it2} Session", xp_adv + 20, 3, "challenge"))
    
    # Exercise sprint
    lessons.append(_L(f"Sprint: {base_topic} Exercises", xp_adv, diff_adv, "practice"))
    
    # Code review
    lessons.append(_L(f"Review: {base_topic} Code Samples", xp_adv - 5, diff_base, "practice"))
    
    # Quick quiz
    lessons.append(_L(f"Quiz: {base_topic} Fundamentals", xp_base, diff_base, "practice"))
    
    # Weekly challenge
    lessons.append(_L(f"Weekly Challenge: {base_topic}", xp_adv + 10, min(3, diff_adv + 1), "challenge"))
    
    # Project
    if proj_pool:
        project = proj_pool[(idx * 7) % proj_count]
        lessons.append(_L(f"Project: {project}", xp_proj, 3, "project"))
    
    # Phase-specific boss battles
    if idx == 9:
        lessons.append(_L(f"🏆 Core Boss: {base_topic} Gauntlet", 80, 3, "boss"))
    elif idx == 19:
        lessons.append(_L(f"🏆 Intermediate Boss: {base_topic} Challenge", 90, 3, "boss"))
    elif idx == 29:
        lessons.append(_L(f"🏆 Advanced Boss: {base_topic} Trial", 100, 3, "boss"))
    elif idx == 39:
        lessons.append(_L(f"🏆 Expert Boss: {base_topic} Exam", 110, 3, "boss"))
    elif idx == 49:
        lessons.append(_L(f"👑 Grandmaster: Final Boss Battle", 150, 3, "boss"))
    
    return {"id": f"l{idx+1:02d}", "lessons": lessons}


def _build_50_level_language(lang_id, lang_name, icon, color, desc):
    """Build a 50-level language from topic pools."""
    topics = LANG_TOPICS.get(lang_id, C_TOPICS)
    levels = {}
    total = 0
    for i in range(50):
        raw = _gen_level(topics, lang_id, i, 50)
        theme = LEVELS_50[i]
        lessons = []
        for j, l in enumerate(raw["lessons"]):
            lessons.append({
                "id": f"{lang_id}-{raw['id']}-{j+1:02d}",
                "title": l["title"],
                "xp": l["xp"],
                "difficulty": l["difficulty"],
                "type": l["type"],
            })
        total_xp = sum(l["xp"] for l in lessons)
        levels[raw["id"]] = {
            "id": raw["id"],
            "name": theme[0],
            "emoji": theme[1],
            "color": theme[2],
            "bg": "from-gray-500/20 to-gray-600/20",
            "border": "border-gray-500/30",
            "text": "text-gray-400",
            "description": theme[3],
            "order": i + 1,
            "lessons": lessons,
            "total_lessons": len(lessons),
            "total_xp": total_xp,
        }
        total += len(lessons)
    return {
        "id": lang_id,
        "name": lang_name,
        "icon": icon,
        "color": color,
        "description": desc,
        "total_lessons": total,
        "levels": levels,
    }


def install_50_level_curriculum():
    """Replace existing language entries with 50-level versions."""
    # Patch LEVEL_THEMES to 50 entries
    _OLD_THEMES.clear()
    for t in LEVELS_50:
        _OLD_THEMES.append({
            "id": f"l{t[0].split()[0].lower()[:3]}" if len(t[0].split()) > 1 else f"l{t[0][:3].lower()}",
            "name": t[0],
            "emoji": t[1],
            "color": t[2],
            "bg": f"from-{t[2].lower()}/20 to-gray-600/20",
            "border": f"border-{t[2].lower()}/30",
            "text": f"text-{t[2].lower()}",
            "desc": t[3],
        })

    lang_defs = [
        ("c", "C", "⚙️", "#6B7280", "Master the foundation of modern programming — systems, embedded, performance"),
        ("cpp", "C++", "🔷", "#3B82F6", "Object-oriented power with STL, templates, and modern C++20/23"),
        ("java", "Java", "☕", "#F97316", "Enterprise-grade OOP — JVM, collections, concurrency, Spring ecosystem"),
        ("python", "Python", "🐍", "#22C55E", "The most versatile language — AI, web, automation, data science"),
        ("javascript", "JavaScript", "🟨", "#F7DF1E", "The language of the web — from interactive UIs to full-stack apps"),
        ("go", "Go", "🔵", "#00ADD8", "Concurrent systems programming — simple, fast, scalable by Google"),
        ("rust", "Rust", "🦀", "#DE3C4C", "Memory-safe systems programming — blazingly fast with zero-cost abstractions"),
    ]
    for lid, name, icon, color, desc in lang_defs:
        LANGUAGES[lid] = _build_50_level_language(lid, name, icon, color, desc)
    
    return LANGUAGES
