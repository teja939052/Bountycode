"""
Shared curriculum utilities — no circular dependencies.
Contains _L lesson shorthand, _bonus_lessons, and LEVEL_THEMES.
"""
#pylint: skip-file

# Difficulty: 1=easy, 2=medium, 3=hard
# Diamonds: easy=10-15, medium=20-30, hard=35-50, project=60, boss=80

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


def _L(title, diamonds=15, diff=1, type_="theory", git_desc=None):
    """Shorthand to create a lesson dict."""
    result = {"title": title, "diamonds": diamonds, "difficulty": diff, "type": type_}
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
