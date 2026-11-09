"""
C# Language Track — 40 Levels
Built on coddy.tech methodology: build something with EVERY lesson,
short daily lessons, instant feedback, AI tutor hints, gamified streaks.
Focus: .NET ecosystem, LINQ, async/await, enterprise patterns.
"""

from .curriculum_base import _L, _bonus_lessons, LEVEL_THEMES

CSHARP_LEVELS = [
    # Level 1: First Steps 🌱
    {"id": "l01", "difficulty": 1, "name": "First Steps", "lessons": [
        _L("What is C#?", 10, 1), _L("Hello World in C#", 10, 1, "practice"),
        _L("dotnet new & dotnet run", 10, 1), _L("dotnet build & dotnet test", 10, 1),
        _L("Project & Solution Structure", 10, 1), _L("Practice: Your First C# Program", 15, 1, "practice"),
        _L("Challenge: Namespace Greeting", 25, 2, "challenge"),
        _L("Project: CLI Greeting Tool", 60, 3, "project",
           "A CLI greeting tool with .NET project structure, namespaces, and build configuration."),
    ]},
    # Level 2: Variables & Types 📦
    {"id": "l02", "difficulty": 1, "name": "Variables & Types", "lessons": [
        _L("var vs Explicit Types", 10, 1), _L("Value Types vs Reference Types", 10, 1),
        _L("int, double, decimal, bool, char", 10, 1), _L("Nullable Types (?)", 10, 1),
        _L("Type Casting & Conversion", 15, 2), _L("Constants & readonly", 15, 1),
        _L("Practice: Type Explorer", 20, 2, "practice"),
        _L("Challenge: Nullable Type Puzzle", 25, 2, "challenge"),
        _L("Project: Unit Conversion Tool", 60, 3, "project",
           "A type-safe unit conversion tool with nullable types and proper type handling."),
    ]},
    # Level 3: Control Flow 🔀
    {"id": "l03", "difficulty": 2, "name": "Control Flow", "lessons": [
        _L("if / else if / else", 10, 1), _L("switch Statement & switch Expressions", 15, 2),
        _L("for Loop", 15, 1), _L("while & do-while", 15, 1),
        _L("foreach Loop", 15, 1), _L("break, continue, goto", 15, 2),
        _L("Practice: Loop Patterns", 20, 2, "practice"),
        _L("Challenge: FizzBuzz in C#", 30, 3, "challenge"),
        _L("Project: Number Guessing Game", 60, 3, "project",
           "An interactive number guessing game with control flow and switch expressions."),
    ]},
    # Level 4: Methods 🧩
    {"id": "l04", "difficulty": 2, "name": "Methods", "lessons": [
        _L("Method Declaration", 10, 1), _L("Optional & Named Parameters", 15, 2),
        _L("params Arrays", 15, 2), _L("ref & out Parameters", 20, 2),
        _L("Local Functions", 15, 2), _L("Extension Methods", 20, 2),
        _L("Practice: Math Utilities", 20, 2, "practice"),
        _L("Challenge: Extension Method Library", 35, 3, "challenge"),
        _L("Project: String Utility Library", 60, 3, "project",
           "A string utility library using extension methods, optional parameters, and local functions."),
    ]},
    # Level 5: Arrays & Collections 📊
    {"id": "l05", "difficulty": 2, "name": "Arrays & Collections", "lessons": [
        _L("Array Declaration & Initialization", 10, 1), _L("List<T>", 10, 1),
        _L("Dictionary<TKey, TValue>", 15, 2), _L("HashSet<T>", 15, 1),
        _L("Queue<T> & Stack<T>", 15, 2), _L("LINQ Basics (Where, Select)", 20, 2),
        _L("Practice: Collection Operations", 20, 2, "practice"),
        _L("Challenge: LINQ Query Optimization", 35, 3, "challenge"),
        _L("Project: Data Processing Pipeline", 60, 3, "project",
           "A data processing pipeline using LINQ, List, Dictionary, and HashSet."),
    ]},
    # Level 6: OOP — Classes & Objects 🏗️
    {"id": "l06", "difficulty": 2, "name": "OOP — Classes & Objects", "lessons": [
        _L("class & Constructor", 10, 1), _L("Properties (get/set)", 10, 1),
        _L("Access Modifiers (public, private, protected, internal)", 15, 2),
        _L("static Members", 15, 2), _L("Inheritance & base", 20, 2),
        _L("Method Overriding & virtual", 20, 2),
        _L("Practice: Shape Hierarchy", 20, 2, "practice"),
        _L("Challenge: Abstract Class Design", 35, 3, "challenge"),
        _L("Project: Employee Management System", 60, 3, "project",
           "An employee management system using classes, inheritance, properties, and access modifiers."),
    ]},
    # Level 7: Interfaces & Polymorphism 🔷
    {"id": "l07", "difficulty": 3, "name": "Interfaces & Polymorphism", "lessons": [
        _L("interface Declaration", 10, 1), _L("Implicit Interface Implementation", 10, 1),
        _L("Explicit Interface Implementation", 15, 2), _L("Multiple Interfaces", 15, 2),
        _L("default Interface Methods (C# 8+)", 20, 3), _L("Pattern Matching with is", 20, 2),
        _L("Practice: Payment Interface", 20, 2, "practice"),
        _L("Challenge: Strategy Pattern", 40, 3, "challenge"),
        _L("Project: Plugin Architecture", 60, 3, "project",
           "A plugin architecture using interfaces, polymorphism, and pattern matching."),
    ]},
    # Level 8: Delegates & Events ⚡
    {"id": "l08", "difficulty": 3, "name": "Delegates & Events", "lessons": [
        _L("delegate Declaration", 10, 1), _L("Action, Func, Predicate", 10, 1),
        _L("Multicast Delegates", 15, 2), _L("event Declaration", 15, 2),
        _L("EventHandler Pattern", 20, 2), _L("Lambda Expressions", 15, 2),
        _L("Practice: Event System", 20, 2, "practice"),
        _L("Challenge: Observer Pattern", 45, 3, "challenge"),
        _L("Project: Notification System", 60, 3, "project",
           "A notification system using delegates, events, and lambda expressions."),
    ]},
    # Level 9: LINQ & Queries 🔍
    {"id": "l09", "difficulty": 2, "name": "LINQ & Queries", "lessons": [
        _L("LINQ Query Syntax", 10, 1), _L("LINQ Method Syntax", 10, 1),
        _L("Where, Select, SelectMany", 15, 2), _L("OrderBy, ThenBy", 15, 2),
        _L("GroupBy, Join", 20, 2), _L("Deferred vs Immediate Execution", 20, 2),
        _L("Practice: LINQ Queries", 20, 2, "practice"),
        _L("Challenge: Complex LINQ Composition", 35, 3, "challenge"),
        _L("Project: Report Generator", 60, 3, "project",
           "A report generator using LINQ queries with method and query syntax."),
    ]},
    # Level 10: Async & Await 🌐
    {"id": "l10", "difficulty": 3, "name": "Async & Await", "lessons": [
        _L("async & await Keywords", 10, 1), _L("Task & Task<T>", 15, 2),
        _L("Task.Run & Task.WhenAll", 15, 2), _L("Task.WhenAny", 15, 2),
        _L("ConfigureAwait", 15, 2), _L("Async Streams (IAsyncEnumerable)", 20, 3),
        _L("Practice: Async Method", 25, 2, "practice"),
        _L("Challenge: Parallel API Calls", 45, 3, "challenge"),
        _L("Project: Async Data Fetcher", 60, 3, "project",
           "An async data fetcher using Task, await, WhenAll, and async streams."),
    ]},
    # Level 11: Final Challenge 👑
    {"id": "l11", "difficulty": 3, "name": "Final Challenge", "lessons": [
        _L("Reflection", 30, 3), _L("Attributes", 30, 3),
        _L("Dependency Injection", 30, 3), _L("Middleware Pipeline", 30, 3),
        _L("Practice: Reflection-Based Factory", 40, 3, "practice"),
        _L("Challenge: DI Container", 50, 3, "challenge"),
        _L("Capstone: Enterprise Web API", 80, 3, "project",
           "An enterprise web API with ASP.NET Core, dependency injection, middleware, and reflection."),
        _L("👑 C# Grandmaster Boss", 80, 3, "boss"),
    ]},
    # Level 12: Generics & Collections Advanced 🔄
    {"id": "l12", "difficulty": 3, "name": "Generics & Collections Advanced", "lessons": [
        _L("Generic Constraints (where)", 20, 2), _L("Covariance & Contravariance", 25, 3),
        _L("ReadOnlyCollection<T>", 15, 2), _L("Immutable Collections", 20, 3),
        _L("SortedDictionary & SortedList", 15, 2), _L("BitArray & BitVector32", 15, 2),
        _L("Practice: Generic Repository", 30, 3, "practice"),
        _L("Challenge: Type-Safe Cache", 45, 3, "challenge"),
        _L("Project: Generic Data Access Layer", 60, 3, "project",
           "A type-safe data access layer using generics, covariance, and immutable collections."),
    ]},
    # Level 13: File I/O & Serialization 📁
    {"id": "l13", "difficulty": 2, "name": "File I/O & Serialization", "lessons": [
        _L("File.ReadAllText & WriteAllText", 10, 1), _L("StreamReader & StreamWriter", 15, 2),
        _L("FileStream & BufferedStream", 15, 2), _L("JSON Serialization (System.Text.Json)", 20, 2),
        _L("XML Serialization", 15, 2), _L("Binary Serialization", 15, 2),
        _L("Practice: File Processor", 20, 2, "practice"),
        _L("Challenge: Config File Manager", 35, 3, "challenge"),
        _L("Project: Settings Manager", 60, 3, "project",
           "A settings manager using JSON serialization, file I/O streams, and config management."),
    ]},
    # Level 14: Portfolio Capstone 🏆
    {"id": "l14", "difficulty": 3, "name": "Portfolio Capstone", "lessons": [
        _L("ASP.NET Core Basics", 35, 3), _L("Design Patterns in C#", 40, 3, "practice"),
        _L("Challenge: Async Performance Optimization", 45, 3, "challenge"),
        _L("Project: Full-Stack .NET Application", 80, 3, "project",
           "A comprehensive full-stack .NET application with ASP.NET Core, Entity Framework, and SQL Server."),
        _L("🏆 C# Mastery Finale", 100, 3, "boss"),
    ]},
]

# Append levels 15-40 for C#
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
    CSHARP_LEVELS.append({"id": _meta["id"], "lessons": _lessons})
