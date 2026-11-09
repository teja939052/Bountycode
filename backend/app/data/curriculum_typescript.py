"""
TypeScript Language Track — 40 Levels
Built on coddy.tech methodology: build something with EVERY lesson,
short daily lessons, instant feedback, AI tutor hints, gamified streaks.
"""

from .curriculum_base import _L, _bonus_lessons, LEVEL_THEMES

# ── TypeScript Levels (40) ──
# Levels 1-14: Hand-authored with real TypeScript content
# Levels 15-40: Auto-generated from LEVEL_THEMES

TS_LEVELS = [
    # Level 1: First Steps 🌱
    {"id": "l01", "difficulty": 1, "name": "First Steps", "lessons": [
        _L("What is TypeScript?", 10, 1), _L("Hello World in TS", 10, 1, "practice"),
        _L("tsconfig.json Setup", 10, 1), _L("tsc Compiler Basics", 10, 1),
        _L("JavaScript vs TypeScript", 10, 1), _L("Practice: Your First TS Program", 15, 1, "practice"),
        _L("Challenge: Type-Safe Greeting", 25, 2, "challenge"),
        _L("Project: Typed CLI Greeting Card", 60, 3, "project",
           "A CLI greeting card with strict TypeScript types, interfaces, and compile-time safety."),
    ]},
    # Level 2: Types & Variables 📦
    {"id": "l02", "difficulty": 1, "name": "Types & Variables", "lessons": [
        _L("Primitive Types: string, number, boolean", 10, 1), _L("null, undefined, void, never", 10, 1),
        _L("let vs const", 15, 1), _L("Type Annotations", 15, 1),
        _L("Type Inference", 15, 2), _L("Explicit vs Implicit Types", 15, 2),
        _L("Practice: Type Explorer", 20, 2, "practice"),
        _L("Challenge: Type Narrowing Puzzle", 25, 2, "challenge"),
        _L("Project: User Profile Validator", 60, 3, "project",
           "A type-safe user profile validator with interfaces for name, age, email, and preferences."),
    ]},
    # Level 3: Interfaces & Type Aliases 🔷
    {"id": "l03", "difficulty": 2, "name": "Interfaces & Type Aliases", "lessons": [
        _L("interface Basics", 10, 1), _L("type Aliases", 10, 1),
        _L("interface vs type", 15, 2), _L("Optional Properties", 15, 2),
        _L("Readonly Properties", 15, 2), _L("Index Signatures", 20, 2),
        _L("Practice: Product Interface", 20, 2, "practice"),
        _L("Challenge: API Response Types", 30, 3, "challenge"),
        _L("Project: E-commerce Type Catalog", 60, 3, "project",
           "A type-safe product catalog with interfaces for products, categories, and inventory."),
    ]},
    # Level 4: Unions, Intersections & Tuples 🔀
    {"id": "l04", "difficulty": 2, "name": "Unions, Intersections & Tuples", "lessons": [
        _L("Union Types (A | B)", 10, 1), _L("Intersection Types (A & B)", 10, 1),
        _L("Type Guards", 15, 2), _L("Tuple Types", 15, 2),
        _L("Named Tuples", 15, 2), _L("Type Assertions", 20, 2),
        _L("Practice: Result Type", 20, 2, "practice"),
        _L("Challenge: Discriminated Unions", 35, 3, "challenge"),
        _L("Project: Form Validation Engine", 60, 3, "project",
           "A type-safe form validation system using discriminated unions for different field types."),
    ]},
    # Level 5: Enums & Literals 📝
    {"id": "l05", "difficulty": 2, "name": "Enums & Literals", "lessons": [
        _L("Numeric Enums", 10, 1), _L("String Enums", 10, 1),
        _L("Literal Types", 15, 1), _L("Template Literal Types", 20, 3),
        _L("const Assertions", 15, 2), _L("typeof Operator", 15, 2),
        _L("Practice: Status Enum", 20, 2, "practice"),
        _L("Challenge: Route Type System", 30, 3, "challenge"),
        _L("Project: Design System Theme Builder", 60, 3, "project",
           "A type-safe theme builder with enum-based color palettes and literal type constraints."),
    ]},
    # Level 6: Functions & Signatures 🧩
    {"id": "l06", "difficulty": 2, "name": "Functions & Signatures", "lessons": [
        _L("Function Type Annotations", 10, 1), _L("Optional & Default Parameters", 15, 1),
        _L("Rest Parameters", 15, 2), _L("Function Overloads", 20, 3),
        _L("this Parameter", 15, 2), _L("Generic Functions", 25, 3),
        _L("Practice: Higher-Order Function", 25, 2, "practice"),
        _L("Challenge: Type-Safe Event Emitter", 40, 3, "challenge"),
        _L("Project: Math Utility Library", 60, 3, "project",
           "A type-safe math utility library with generic functions and overload signatures."),
    ]},
    # Level 7: Generics 🔄
    {"id": "l07", "difficulty": 3, "name": "Generics", "lessons": [
        _L("Generic Basics", 15, 2), _L("Generic Constraints", 20, 2),
        _L("Generic Interfaces", 20, 2), _L("Generic Type Aliases", 20, 2),
        _L("keyof & typeof", 20, 3), _L("Partial, Required, Readonly", 20, 3),
        _L("Practice: Generic Repository", 30, 3, "practice"),
        _L("Challenge: Type-Safe Cache", 45, 3, "challenge"),
        _L("Project: Generic Data Fetching Hook", 60, 3, "project",
           "A type-safe data fetching utility with generics for request/response types."),
    ]},
    # Level 8: Advanced Types 🧠
    {"id": "l08", "difficulty": 3, "name": "Advanced Types", "lessons": [
        _L("Pick, Omit, Exclude, Extract", 20, 2), _L("Record<T>", 15, 2),
        _L("Exclude & Omit", 15, 2), _L("NonNullable & Required", 15, 2),
        _L("Conditional Types", 25, 3), _L("infer Keyword", 30, 3),
        _L("Practice: Utility Type Builder", 30, 3, "practice"),
        _L("Challenge: Deep Readonly Type", 45, 3, "challenge"),
        _L("Project: API Response Transformer", 60, 3, "project",
           "A type-safe API response transformer using conditional types and inference."),
    ]},
    # Level 9: Classes & OOP 🏗️
    {"id": "l09", "difficulty": 2, "name": "Classes & OOP", "lessons": [
        _L("class & Constructor", 10, 1), _L("Access Modifiers: public, private, protected", 15, 2),
        _L("abstract Classes", 20, 3), _L("Interfaces vs Classes", 15, 2),
        _L("Implements Clause", 15, 2), _L("Static Members", 15, 2),
        _L("Practice: Shape Hierarchy", 25, 2, "practice"),
        _L("Challenge: Abstract Factory Pattern", 40, 3, "challenge"),
        _L("Project: Library Management System", 60, 3, "project",
           "A type-safe library management system with abstract classes and interface implementations."),
    ]},
    # Level 10: Decorators & Metadata ✨
    {"id": "l10", "difficulty": 3, "name": "Decorators & Metadata", "lessons": [
        _L("Class Decorators", 20, 3), _L("Method Decorators", 20, 3),
        _L("Property Decorators", 20, 3), _L("Parameter Decorators", 20, 3),
        _L("Decorator Factories", 25, 3), _L("Reflect Metadata", 25, 3),
        _L("Practice: Log Decorator", 30, 3, "practice"),
        _L("Challenge: Validation Decorator", 45, 3, "challenge"),
        _L("Project: Dependency Injection Container", 60, 3, "project",
           "A dependency injection container using decorators and reflection metadata."),
    ]},
    # Level 11: Modules & Namespaces 📦
    {"id": "l11", "difficulty": 2, "name": "Modules & Namespaces", "lessons": [
        _L("ES Modules: import / export", 10, 1), _L("Default vs Named Exports", 15, 1),
        _L("Namespace Declaration", 20, 2), _L("Module Augmentation", 25, 3),
        _L("Declaration Files (.d.ts)", 20, 2), _L("Ambient Declarations", 20, 2),
        _L("Practice: Module System", 25, 2, "practice"),
        _L("Challenge: Library Type Definitions", 40, 3, "challenge"),
        _L("Project: Modular Plugin Architecture", 60, 3, "project",
           "A modular plugin system with namespace organization and ambient type declarations."),
    ]},
    # Level 12: Final Challenge 👑
    {"id": "l12", "difficulty": 3, "name": "Final Challenge", "lessons": [
        _L("Mapped Types", 30, 3), _L("Template Literal Types Advanced", 30, 3),
        _L("Branded Types", 30, 3), _L("Type-Level Programming", 35, 3),
        _L("Practice: Type-Level Calculator", 40, 3, "practice"),
        _L("Challenge: Type-Safe Router", 50, 3, "challenge"),
        _L("Capstone: Enterprise SaaS — Auth, RBAC, Real-Time", 80, 3, "project",
           "A full enterprise SaaS with TypeScript, authentication, role-based access control, and real-time updates."),
        _L("👑 TypeScript Grandmaster Boss", 80, 3, "boss"),
    ]},
    # Level 13: Mini Compiler ⚙️
    {"id": "l13", "difficulty": 3, "name": "Mini Compiler", "lessons": [
        _L("TypeScript AST with TypeScript Compiler API", 35, 3), _L("Building a Type Checker", 35, 3, "practice"),
        _L("Challenge: Custom TS Plugin", 40, 3, "challenge"),
        _L("Project: TS-to-JS Transpiler", 70, 3, "project",
           "A mini TypeScript-to-JavaScript transpiler using the TypeScript Compiler API."),
    ]},
    # Level 14: Portfolio Capstone 🏆
    {"id": "l14", "difficulty": 3, "name": "Portfolio Capstone", "lessons": [
        _L("Monorepo Setup (Turborepo/Nx)", 35, 3), _L("Design Patterns in TypeScript", 40, 3, "practice"),
        _L("Challenge: Async Performance Optimization", 45, 3, "challenge"),
        _L("Project: Full-Stack TypeScript App", 80, 3, "project",
           "A comprehensive full-stack TypeScript application with React, Node.js, PostgreSQL, and Docker."),
        _L("🏆 TypeScript Mastery Finale", 100, 3, "boss"),
    ]},
]

# Append levels 15-40 for TypeScript
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
    TS_LEVELS.append({"id": _meta["id"], "lessons": _lessons})
