"""
Go Language Track — 40 Levels
Built on coddy.tech methodology: build something with EVERY lesson,
short daily lessons, instant feedback, AI tutor hints, gamified streaks.
"""

from .curriculum_base import _L, _bonus_lessons, LEVEL_THEMES

GO_LEVELS = [
    # Level 1: First Steps 🌱
    {"id": "l01", "difficulty": 1, "name": "First Steps", "lessons": [
        _L("What is Go?", 10, 1), _L("Hello World in Go", 10, 1, "practice"),
        _L("Go Modules & go.mod", 10, 1), _L("go run & go build", 10, 1),
        _L("Package Declaration", 10, 1), _L("Practice: Your First Go Program", 15, 1, "practice"),
        _L("Challenge: Package Greeting", 25, 2, "challenge"),
        _L("Project: CLI Greeting Tool", 60, 3, "project",
           "A CLI greeting tool with Go modules, proper package structure, and command-line flags."),
    ]},
    # Level 2: Variables & Types 📦
    {"id": "l02", "difficulty": 1, "name": "Variables & Types", "lessons": [
        _L("var Declaration", 10, 1), _L("short Variable Declaration (:=)", 10, 1),
        _L("Basic Types: int, float64, string, bool", 10, 1), _L("Zero Values", 10, 1),
        _L("Type Conversion", 15, 2), _L("Constants", 15, 1),
        _L("Practice: Type Explorer", 20, 2, "practice"),
        _L("Challenge: Unit Converter", 25, 2, "challenge"),
        _L("Project: Temperature Conversion Tool", 60, 3, "project",
           "A type-safe temperature conversion tool with constants and proper type handling."),
    ]},
    # Level 3: Control Flow 🔀
    {"id": "l03", "difficulty": 2, "name": "Control Flow", "lessons": [
        _L("if / else if / else", 10, 1), _L("switch Statement", 15, 2),
        _L("for Loop (Go's only loop)", 15, 1), _L("break, continue, goto", 15, 2),
        _L("Labels", 15, 2), _L("Short Variable Declaration in for", 15, 2),
        _L("Practice: Loop Patterns", 20, 2, "practice"),
        _L("Challenge: FizzBuzz in Go", 30, 3, "challenge"),
        _L("Project: Number Guessing Game", 60, 3, "project",
           "An interactive number guessing game with for loops and switch statements."),
    ]},
    # Level 4: Functions 🧩
    {"id": "l04", "difficulty": 2, "name": "Functions", "lessons": [
        _L("Function Declaration", 10, 1), _L("Multiple Return Values", 15, 1),
        _L("Named Return Values", 15, 2), _L("Variadic Functions", 20, 2),
        _L("Anonymous Functions", 15, 2), _L("Functions as Values", 20, 2),
        _L("Practice: Math Utilities", 20, 2, "practice"),
        _L("Challenge: Higher-Order Functions", 35, 3, "challenge"),
        _L("Project: Calculator with Function Pointers", 60, 3, "project",
           "A calculator using functions as first-class values with variadic operations."),
    ]},
    # Level 5: Arrays & Slices 📊
    {"id": "l05", "difficulty": 2, "name": "Arrays & Slices", "lessons": [
        _L("Arrays (Fixed Size)", 10, 1), _L("Slices (Dynamic)", 10, 1),
        _L("slice Literals", 15, 1), _L("append & copy", 15, 2),
        _L("Slice Internals: length, capacity, underlying array", 20, 3),
        _L("range over Slices", 15, 1),
        _L("Practice: Slice Operations", 20, 2, "practice"),
        _L("Challenge: Rotate Slice In-Place", 35, 3, "challenge"),
        _L("Project: Dynamic Array List", 60, 3, "project",
           "A dynamic array list using slices with append, copy, and range operations."),
    ]},
    # Level 6: Maps 🗄️
    {"id": "l06", "difficulty": 2, "name": "Maps", "lessons": [
        _L("Map Declaration & Literals", 10, 1), _L("Map Operations: read, write, delete", 15, 1),
        _L("map Existence Check (ok idiom)", 15, 2), _L("range over Maps", 15, 1),
        _L("Nested Maps", 20, 2), _L("Map Concurrency Safety", 20, 3),
        _L("Practice: Word Frequency Counter", 20, 2, "practice"),
        _L("Challenge: Group Anagrams", 35, 3, "challenge"),
        _L("Project: In-Memory Key-Value Store", 60, 3, "project",
           "A thread-safe in-memory key-value store using maps with sync.RWMutex."),
    ]},
    # Level 7: Structs & Methods 🏗️
    {"id": "l07", "difficulty": 2, "name": "Structs & Methods", "lessons": [
        _L("struct Declaration", 10, 1), _L("struct Literals", 10, 1),
        _L("Methods with Value Receivers", 15, 2), _L("Methods with Pointer Receivers", 15, 2),
        _L("Pointer vs Value Receivers", 20, 2), _L("Embedded Structs", 20, 2),
        _L("Practice: Point & Rectangle", 20, 2, "practice"),
        _L("Challenge: Method Sets", 35, 3, "challenge"),
        _L("Project: Employee Management System", 60, 3, "project",
           "An employee management system using structs, methods, and embedding."),
    ]},
    # Level 8: Interfaces 🔷
    {"id": "l08", "difficulty": 3, "name": "Interfaces", "lessons": [
        _L("interface Declaration", 10, 1), _L("Implicit Interface Satisfaction", 10, 1),
        _L("Empty interface (any)", 15, 2), _L("Type Assertions", 15, 2),
        _L("Type Switches", 20, 2), _L("interface Composition", 20, 2),
        _L("Practice: Shape Interface", 20, 2, "practice"),
        _L("Challenge: Sort Interface", 40, 3, "challenge"),
        _L("Project: Payment Processor with Multiple Providers", 60, 3, "project",
           "A payment processor using interfaces for multiple payment providers (Stripe, PayPal, etc.)."),
    ]},
    # Level 9: Pointers & Memory 🧠
    {"id": "l09", "difficulty": 3, "name": "Pointers & Memory", "lessons": [
        _L("Pointer Basics (*T, &)", 10, 1), _L("Pointer Arithmetic (unsafe)", 20, 3),
        _L("new vs make", 15, 2), _L("Stack vs Heap", 15, 2),
        _L("Escape Analysis", 20, 3), _L("nil Pointers", 15, 1),
        _L("Practice: Pointer Swap", 20, 2, "practice"),
        _L("Challenge: Linked List from Scratch", 45, 3, "challenge"),
        _L("Project: Memory Pool Allocator", 60, 3, "project",
           "A memory pool allocator demonstrating stack vs heap, escape analysis, and pointer management."),
    ]},
    # Level 10: Concurrency — Goroutines ⚡
    {"id": "l10", "difficulty": 3, "name": "Concurrency — Goroutines", "lessons": [
        _L("goroutine Basics (go keyword)", 10, 1), _L("Concurrent Execution", 15, 2),
        _L("race Detector", 15, 2), _L("sync.WaitGroup", 20, 2),
        _L("sync.Mutex", 20, 2), _L("sync.RWMutex", 20, 2),
        _L("Practice: Parallel Computation", 25, 2, "practice"),
        _L("Challenge: Worker Pool", 45, 3, "challenge"),
        _L("Project: Concurrent Web Crawler", 60, 3, "project",
           "A concurrent web crawler using goroutines, channels, and sync primitives."),
    ]},
    # Level 11: Channels 📡
    {"id": "l11", "difficulty": 3, "name": "Channels", "lessons": [
        _L("Channel Creation (make chan T)", 10, 1), _L("Send & Receive (<-)", 10, 1),
        _L("Buffered vs Unbuffered Channels", 15, 2), _L("Channel Direction (chan<-, <-chan)", 15, 2),
        _L("range over Channels", 15, 1), _L("close Channel", 15, 1),
        _L("select Statement", 20, 2), _L("select with default", 20, 2),
        _L("Practice: Channel Pipeline", 25, 2, "practice"),
        _L("Challenge: Fan-Out / Fan-In", 45, 3, "challenge"),
        _L("Project: Producer-Consumer Task Queue", 60, 3, "project",
           "A producer-consumer task queue using channels, select, and worker pools."),
    ]},
    # Level 12: Final Challenge 👑
    {"id": "l12", "difficulty": 3, "name": "Final Challenge", "lessons": [
        _L("context Package", 30, 3), _L("context.WithCancel & WithTimeout", 30, 3),
        _L("context Values", 30, 3), _L("sync.Once", 30, 3),
        _L("Practice: Context-Propagated Requests", 40, 3, "practice"),
        _L("Challenge: Distributed Rate Limiter", 50, 3, "challenge"),
        _L("Capstone: Distributed Task Scheduler", 80, 3, "project",
           "A distributed task scheduler with goroutines, channels, context, and worker pools."),
        _L("👑 Go Grandmaster Boss", 80, 3, "boss"),
    ]},
    # Level 13: Error Handling 🛡️
    {"id": "l13", "difficulty": 2, "name": "Error Handling", "lessons": [
        _L("error Interface", 10, 1), _L("errors.New & fmt.Errorf", 10, 1),
        _L("Custom Error Types", 15, 2), _L("error Wrapping (%w)", 15, 2),
        _L("errors.Is & errors.As", 20, 2), _L("panic & recover", 20, 2),
        _L("Practice: Error Wrapping", 20, 2, "practice"),
        _L("Challenge: Custom Validation Errors", 35, 3, "challenge"),
        _L("Project: Resilient File Processor", 60, 3, "project",
           "A resilient file processor with custom error types, wrapping, and recovery."),
    ]},
    # Level 14: Testing & Tooling 🔧
    {"id": "l14", "difficulty": 2, "name": "Testing & Tooling", "lessons": [
        _L("testing Package Basics", 10, 1), _L("Table-Driven Tests", 15, 2),
        _L("Test Coverage", 15, 2), _L("Benchmarking", 20, 2),
        _L("go vet & go fmt", 10, 1), _L("go mod & Dependencies", 15, 1),
        _L("Practice: Write Unit Tests", 20, 2, "practice"),
        _L("Challenge: Benchmark Comparison", 35, 3, "challenge"),
        _L("Project: Test-Driven Library", 60, 3, "project",
           "A test-driven Go library with 100% test coverage, benchmarks, and proper module structure."),
    ]},
]

# Append levels 15-40 for Go
for _i in range(14, 40):
    _meta = LEVEL_THEMES[_i]
    _lessons = [
        _L(f"{_meta['emoji']} {_meta['name']} — Core Concepts", 15, 1, "theory"),
        _L(f"🛠️ {_meta['name']} — Hands-On Practice", 20, 2, "practice"),
        _L(f"⚔️ {_meta['name']} — Challenge Problem", 35, 3, "challenge"),
    ]
    if _i + 1 in (20, 25, 30, 35, 40):
        _lessons.append(_L(f"🐉 {_meta['name']} — Boss Battle", 100, 3, "boss"))
    elif _i + 1 in (36, 37, 38):
        _lessons.append(_L(f"🏗️ {_meta['name']} — Capstone Project", 70, 3, "project",
            f"A comprehensive {_meta['name'].lower()} project demonstrating {_meta['desc'].lower()}"))
    else:
        _lessons.append(_L(f"🎯 {_meta['name']} — Mini Project", 60, 3, "project",
            f"A mini project exploring {_meta['desc'].lower()}"))
    GO_LEVELS.append({"id": _meta["id"], "lessons": _lessons})
