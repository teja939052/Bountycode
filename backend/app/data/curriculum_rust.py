"""
Rust Language Track — 40 Levels
Built on coddy.tech methodology: build something with EVERY lesson,
short daily lessons, instant feedback, AI tutor hints, gamified streaks.
Focus: memory safety without garbage collection, ownership, borrowing, lifetimes.
"""

from .curriculum_base import _L, _bonus_lessons, LEVEL_THEMES

RUST_LEVELS = [
    # Level 1: First Steps 🌱
    {"id": "l01", "difficulty": 2, "name": "First Steps", "lessons": [
        _L("What is Rust?", 10, 1), _L("Hello World in Rust", 10, 1, "practice"),
        _L("cargo new & cargo run", 10, 1), _L("cargo build & cargo test", 10, 1),
        _L("Crate & Module System", 10, 1), _L("Practice: Your First Rust Program", 15, 1, "practice"),
        _L("Challenge: Package Greeting", 25, 2, "challenge"),
        _L("Project: CLI Greeting Tool", 60, 3, "project",
           "A CLI greeting tool with Cargo project structure, dependencies, and build configuration."),
    ]},
    # Level 2: Variables & Ownership 📦
    {"id": "l02", "difficulty": 3, "name": "Variables & Ownership", "lessons": [
        _L("mut vs Immutable", 10, 1), _L("Constants vs Variables", 10, 1),
        _L("Ownership Basics", 15, 3), _L("Move Semantics", 15, 3),
        _L("Clone vs Copy", 15, 2), _L("Shadowing", 10, 1),
        _L("Practice: Ownership Transfer", 20, 2, "practice"),
        _L("Challenge: Move vs Clone Puzzle", 30, 3, "challenge"),
        _L("Project: Type-Safe Configuration", 60, 3, "project",
           "A type-safe configuration system demonstrating ownership, cloning, and shadowing."),
    ]},
    # Level 3: Borrowing & References 🔗
    {"id": "l03", "difficulty": 3, "name": "Borrowing & References", "lessons": [
        _L("References (&T, &mut T)", 10, 1), _L("Borrowing Rules", 15, 3),
        _L("Mutable vs Immutable Borrows", 15, 3), _L("Lifetimes Basics", 20, 3),
        _L("Lifetime Annotations", 20, 3), _L("'static Lifetime", 15, 2),
        _L("Practice: Reference Rules", 20, 2, "practice"),
        _L("Challenge: Lifetime Annotation Challenge", 40, 3, "challenge"),
        _L("Project: Document Editor with References", 60, 3, "project",
           "A document editor demonstrating borrowing rules, mutable/immutable references, and lifetimes."),
    ]},
    # Level 4: Slices & Strings 📝
    {"id": "l04", "difficulty": 2, "name": "Slices & Strings", "lessons": [
        _L("String vs &str", 10, 1), _L("String Slicing", 15, 2),
        _L("str Methods", 15, 2), _L("String Concatenation", 15, 2),
        _L("String Formatting (format!)", 10, 1), _L("Byte Slices (&[u8])", 20, 3),
        _L("Practice: String Manipulation", 20, 2, "practice"),
        _L("Challenge: Word Count Program", 30, 3, "challenge"),
        _L("Project: Text Processing Pipeline", 60, 3, "project",
           "A text processing pipeline with String/&str, slicing, and formatting."),
    ]},
    # Level 5: Structs & Enums 🏗️
    {"id": "l05", "difficulty": 2, "name": "Structs & Enums", "lessons": [
        _L("struct Declaration", 10, 1), _L("Tuple & Unit Structs", 10, 1),
        _L("Methods & impl Blocks", 15, 2), _L("Associated Functions", 15, 2),
        _L("enum & Variants", 15, 1), _L("enum with Data", 15, 2),
        _L("Practice: Shape System", 20, 2, "practice"),
        _L("Challenge: State Machine", 35, 3, "challenge"),
        _L("Project: Inventory Management System", 60, 3, "project",
           "An inventory management system using structs, enums with data, and method implementations."),
    ]},
    # Level 6: Pattern Matching & Control Flow 🔀
    {"id": "l06", "difficulty": 2, "name": "Pattern Matching & Control Flow", "lessons": [
        _L("match Statement", 10, 1), _L("if let & while let", 15, 2),
        _L("Destructuring Structs", 15, 2), _L("Destructuring Enums", 15, 2),
        _L("Nested Pattern Matching", 20, 2), _L("if-let Chains", 15, 2),
        _L("Practice: Pattern Matching", 20, 2, "practice"),
        _L("Challenge: Complex State Transitions", 35, 3, "challenge"),
        _L("Project: Command-Line Router", 60, 3, "project",
           "A command-line router using match, if-let, and destructuring for route handling."),
    ]},
    # Level 7: Vectors & Collections 📊
    {"id": "l07", "difficulty": 2, "name": "Vectors & Collections", "lessons": [
        _L("Vec<T> Basics", 10, 1), _L("vec! Macro", 10, 1),
        _L("Vec Methods: push, pop, insert, remove", 15, 2), _L("HashMap<K, V>", 15, 1),
        _L("HashSet<T>", 15, 1), _L("BTreeMap & BTreeSet", 20, 2),
        _L("Practice: Collection Operations", 20, 2, "practice"),
        _L("Challenge: Duplicate Finder", 35, 3, "challenge"),
        _L("Project: Phone Book Application", 60, 3, "project",
           "A phone book application using Vec, HashMap, and HashSet for contact management."),
    ]},
    # Level 8: Error Handling — Result & Option 🛡️
    {"id": "l08", "difficulty": 3, "name": "Error Handling", "lessons": [
        _L("Option<T>: Some & None", 10, 1), _L("Result<T, E>: Ok & Err", 10, 1),
        _L("The ? Operator", 15, 2), _L("unwrap & expect", 15, 2),
        _L("propagating Errors", 15, 2), _L("Custom Error Types", 20, 3),
        _L("Practice: Safe Division", 20, 2, "practice"),
        _L("Challenge: Error Propagation Pipeline", 40, 3, "challenge"),
        _L("Project: File Parser with Error Recovery", 60, 3, "project",
           "A file parser with Result/Option, custom error types, and graceful error propagation."),
    ]},
    # Level 9: Generics & Traits 🔄
    {"id": "l09", "difficulty": 3, "name": "Generics & Traits", "lessons": [
        _L("Generic Functions", 10, 1), _L("Generic Structs", 10, 1),
        _L("Trait Basics", 15, 2), _L("Trait Bounds", 15, 2),
        _L("Derived Traits (Debug, Clone, etc.)", 15, 1), _L("impl Trait Syntax", 20, 3),
        _L("Practice: Generic Container", 20, 2, "practice"),
        _L("Challenge: Trait Object Dispatch", 45, 3, "challenge"),
        _L("Project: Plugin System with Traits", 60, 3, "project",
           "A plugin system using generics, trait bounds, and trait objects for dynamic dispatch."),
    ]},
    # Level 10: Lifetimes & Smart Pointers 🔒
    {"id": "l10", "difficulty": 3, "name": "Lifetimes & Smart Pointers", "lessons": [
        _L("Box<T> (Heap Allocation)", 10, 1), _L("Rc<T> (Reference Counting)", 15, 2),
        _L("Arc<T> (Atomic Reference Counting)", 15, 2), _L("RefCell<T> (Interior Mutability)", 20, 3),
        _L("Lifetime Elision Rules", 20, 3), _L("Explicit Lifetime Annotations", 20, 3),
        _L("Practice: Smart Pointer Usage", 25, 2, "practice"),
        _L("Challenge: Graph with Rc<RefCell<T>>", 50, 3, "challenge"),
        _L("Project: Thread-Safe Cache", 60, 3, "project",
           "A thread-safe cache using Arc, Mutex, and proper lifetime annotations."),
    ]},
    # Level 11: Concurrency 🧵
    {"id": "l11", "difficulty": 3, "name": "Concurrency", "lessons": [
        _L("std::thread", 10, 1), _L("Move Closures", 15, 2),
        _L("Message Passing (channels)", 15, 2), _L("Shared-State Concurrency", 15, 2),
        _L("Mutex<T> & Arc<Mutex<T>>", 20, 3), _L("Send & Sync Traits", 20, 3),
        _L("Practice: Thread Communication", 25, 2, "practice"),
        _L("Challenge: Parallel Map-Reduce", 45, 3, "challenge"),
        _L("Project: Thread Pool Web Server", 60, 3, "project",
           "A thread pool web server using channels, Mutex, Arc, and Send/Sync traits."),
    ]},
    # Level 12: Final Challenge 👑
    {"id": "l12", "difficulty": 3, "name": "Final Challenge", "lessons": [
        _L("Unsafe Rust", 30, 3), _L("Raw Pointers", 30, 3),
        _L("Foreign Function Interface (FFI)", 30, 3), _L("Procedural Macros", 35, 3),
        _L("Practice: Unsafe Code Review", 40, 3, "practice"),
        _L("Challenge: Custom Allocator", 50, 3, "challenge"),
        _L("Capstone: High-Performance Key-Value Store", 80, 3, "project",
           "A high-performance key-value store with unsafe Rust, FFI, and custom memory management."),
        _L("👑 Rust Grandmaster Boss", 80, 3, "boss"),
    ]},
    # Level 13: Macros & Metaprogramming ✨
    {"id": "l13", "difficulty": 3, "name": "Macros & Metaprogramming", "lessons": [
        _L("declarative Macros (macro_rules!)", 25, 3), _L("Procedural Macros", 30, 3),
        _L("Custom Derive Macros", 30, 3), _L("Attribute-like Macros", 30, 3),
        _L("Function-like Macros", 25, 3), _L("Macro Debugging", 20, 3),
        _L("Practice: Debug Macro", 30, 3, "practice"),
        _L("Challenge: JSON Serialize Macro", 45, 3, "challenge"),
        _L("Project: DSL Builder", 60, 3, "project",
           "A domain-specific language builder using declarative and procedural macros."),
    ]},
    # Level 14: Portfolio Capstone 🏆
    {"id": "l14", "difficulty": 3, "name": "Portfolio Capstone", "lessons": [
        _L("Async Rust (tokio)", 35, 3), _L("Design Patterns in Rust", 40, 3, "practice"),
        _L("Challenge: Async Performance Optimization", 45, 3, "challenge"),
        _L("Project: Async Web Service", 80, 3, "project",
           "A comprehensive async web service with Tokio, database integration, and deployment readiness."),
        _L("🏆 Rust Mastery Finale", 100, 3, "boss"),
    ]},
]

# Append levels 15-40 for Rust
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
    RUST_LEVELS.append({"id": _meta["id"], "lessons": _lessons})
