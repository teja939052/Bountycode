"""
MASTER CODING CURRICULUM: A-to-Z Execution Flow & Software Design Mastery

This curriculum covers the COMPLETE picture: from how a single line of code is executed
by the CPU, through memory management and RAM, to large-scale software architecture.
NOT a tutorial site — a first-principles system that makes job seekers actual developers.
"""

# ============================================================
# Core Execution Flow: From Source to CPU
# ============================================================

EXECUTION_FLOW = {
    "overview": "From source code to running program: compiler/parser → AST → machine code → CPU fetch-decode-execute cycle → memory allocation",
    "stages": [
        "Lexical analysis → tokenization",
        "Parsing → AST construction",
        "Semantic analysis → type checking",
        "Intermediate representation → optimization",
        "Code generation → machine code",
        "Linking → resolution",
        "Loading → memory mapping",
        "Execution → fetch-decode-execute cycle"
    ],
    "memory_model": {
        "stack": "LIFO, function call frames, local variables, return addresses, size grows downward",
        "heap": "dynamic allocation, malloc/free (C), new/delete (C++), garbage collection (Java/Python), reference counting",
        "global/data segment": "static variables, global constants",
        "code segment": "compiled machine code, read-only",
        "instruction_pointer": "CPU register pointing to next instruction",
        "frame pointer": "base of current function's stack frame"
    },
    "cpu_pipeline": {
        "fetch": "read instruction from memory at IP",
        "decode": "interpret instruction opcode",
        "execute": "ALU operations, memory access, branch decision",
        "write-back": "store result to register or memory",
        "pipeline_stalls": "cache misses, branch mispredictions, data hazards",
        "instruction_level_parallelism": "out-of-order execution, speculative execution"
    }
}

# ============================================================
# 8 Comprehensive Modules (a to z)
# ============================================================

# Module 1: Foundations
MODULE_FOUNDATIONS = {
    "id": "m-01",
    "title": "Foundations: How Programs Run",
    "description": "The complete picture: from source code to running program. CPU architecture, memory model, execution flow.",
    "level": "beginner",
    "estimated_time_minutes": 45,
    "topics": [
        {
            "id": "m-01-t1",
            "title": "From Source Code to Machine Code",
            "description": "Lexical analysis, parsing, AST, semantic analysis, code generation. Why different languages have different runtimes.",
            "exercises": 3,
            "key_concepts": ["lexical analysis", "parsing", "AST", "semantic analysis", "code generation"],
            "difficulty": "beginner"
        },
        {
            "id": "m-01-t2",
            "title": "CPU Architecture and Instruction Set",
            "description": "x86-64 vs ARM, RISC vs CISC, registers, general-purpose vs special-purpose, instruction formats.",
            "exercises": 3,
            "key_concepts": ["registers", "instruction formats", "x86-64", "ARM", "RISC-CISC"],
            "difficulty": "beginner"
        },
        {
            "id": "m-01-t3",
            "title": "The Fetch-Decode-Execute Cycle",
            "description": "Each CPU cycle: fetch instruction from memory at IP, decode opcode, execute (ALU/memory/branch), write-back. IP increment.",
            "exercises": 3,
            "key_concepts": ["fetch", "decode", "execute", "write-back", "instruction_pointer"],
            "difficulty": "beginner"
        },
        {
            "id": "m-01-t4",
            "type": "design",
            "difficulty": "intermediate",
            "prompt": "Design a simple 8-bit CPU datapath: ALU, register file, program counter, control unit. Explain the clock cycle and signal flow.",
            "mastery": "proficient"
        }
    ]
}

# Module 2: Memory Management
MODULE_MEMORY = {
    "id": "m-02",
    "title": "Memory Management: Stack, Heap, and RAM",
    "description": "How memory actually works: stack vs heap, RAM allocation, garbage collection, memory leaks, fragmentation.",
    "level": "intermediate",
    "estimated_time_minutes": 60,
    "topics": [
        {
            "id": "m-02-t1",
            "title": "Stack Memory: Frame Allocation and Lifetime",
            "description": "Stack frame layout: return address, saved frame pointer, local variables, padding. Stack overflow. Function call overhead. Tail call optimization.",
            "exercises": 3,
            "key_concepts": ["stack frame", "return address", "frame pointer", "stack overflow", "tail call optimization"],
            "difficulty": "beginner"
        },
        {
            "id": "m-02-t2",
            "title": "Heap Memory: Dynamic Allocation and Deallocation",
            "description": "malloc/free (C), new/delete (C++), garbage collection (Java/Python/JS), reference counting, cyclic garbage collection, memory leaks, fragmentation (external + internal).",
            "exercises": 4,
            "key_concepts": ["malloc", "free", "garbage collection", "reference counting", "memory leak", "fragmentation"],
            "difficulty": "intermediate"
        },
        {
            "id": "m-02-t3",
            "type": "design",
            "difficulty": "advanced",
            "prompt": "Design a memory allocator for a real-time system with guaranteed no fragmentation. Compare bump allocator, slab allocator, and segregated fits.",
            "mastery": "expert"
        },
        {
            "id": "m-02-t4",
            "type": "bug",
            "difficulty": "advanced",
            "prompt": "This program has a use-after-free bug. Identify the exact line, explain why the memory is freed but still accessible, how Valgrind/ASan detects it, and fix it using Rust ownership patterns.",
            "mastery": "expert"
        }
    ]
}

# Module 3: Data Structures in Memory
MODULE_DATA_STRUCTURES = {
    "id": "m-03",
    "title": "Data Structures in Memory",
    "description": "How arrays, linked lists, trees, and graphs are actually laid out in RAM, cache locality, and performance implications.",
    "level": "intermediate",
    "estimated_time_minutes": 45,
    "topics": [
        {
            "id": "m-03-t1",
            "title": "Array Memory Layout",
            "description": "Contiguous memory, base + index*element_size, cache lines, prefetching, why insert/delete is O(n) (memmove), dynamic array amortized analysis (doubling strategy).",
            "exercises": 3,
            "key_concepts": ["contiguous memory", "cache lines", "prefetching", "amortized analysis"],
            "difficulty": "beginner"
        },
        {
            "id": "m-03-t2",
            "title": "Linked List Memory Layout",
            "description": "Non-contiguous allocation, pointer chasing, cache misses, linked list vs array trade-offs, circular lists, doubly linked lists.",
            "exercises": 3,
            "key_concepts": ["pointer chasing", "cache misses", "locality"],
            "difficulty": "intermediate"
        },
        {
            "id": "m-03-t3",
            "type": "design",
            "difficulty": "advanced",
            "prompt": "Design a memory-efficient binary search tree node that also stores height for AVL balancing. Calculate the exact memory overhead per node (key + value + height + left pointer + right pointer + balance factor).",
            "mastery": "proficient"
        },
        {
            "id": "m-03-t4",
            "type": "predict",
            "difficulty": "expert",
            "prompt": "Given this code that allocates a 2D array on the stack, will it cause stack overflow? Calculate the total memory (rows * cols * element_size + stack frame overhead) and compare with the typical stack size limit (8MB on Windows, 84MB on Linux).",
            "mastery": "expert"
        }
    ]
}

# Module 4: Algorithms and Complexity
MODULE_ALGORITHMS = {
    "id": "m-04",
    "title": "Algorithms: From First Principles to Practice",
    "description": "How algorithms perform in practice: big-O analysis with constant factors, cache effects, real-world benchmarking.",
    "level": "intermediate",
    "estimated_time_minutes": 60,
    "topics": [
        {
            "id": "m-04-t1",
            "title": "Big-O Notation: What It Really Means",
            "description": "Why O-notation hides constant factors. Why O(n²) can be faster than O(n log n) for small n. Cache effects. Real-world benchmarking examples.",
            "exercises": 3,
            "key_concepts": ["constant factors", "cache effects", "benchmarking", "empirical analysis"],
            "difficulty": "beginner"
        },
        {
            "id": "m-04-t2",
            "type": "design",
            "difficulty": "advanced",
            "prompt": "Your company processes 1M records. Sort them. Should you use built-in sort, implement merge sort, or quicksort? Justify with time, constants, and cache effects.",
            "mastery": "proficient"
        },
        {
            "id": "m-04-t3",
            "type": "optimize",
            "difficulty": "expert",
            "prompt": "Optimize this loop nest for cache performance. Loop interchange, blocking, tiling. Measure before/after with valgrind --tool=cachegrind.",
            "mastery": "expert"
        }
    ]
}

# Module 5: Language Runtimes
MODULE_RUNTIMES = {
    "id": "m-05",
    "title": "Language Runtimes: How Code Actually Executes",
    "description": "Python CPython, Java JVM, JavaScript V8, Rust no runtime: how each executes code, memory management, GC, JIT compilation.",
    "level": "intermediate",
    "estimated_time_minutes": 60,
    "topics": [
        {
            "id": "m-05-t1",
            "title": "Python CPython Runtime",
            "description": "GIL, reference counting, cyclic garbage collection, PyPy JIT, memoryview, ctypes. Why Python is slow and how to optimize.",
            "exercises": 3,
            "key_concepts": ["GIL", "reference counting", "cyclic GC", "PyPy JIT", "ctypes"],
            "difficulty": "intermediate"
        },
        {
            "id": "m-05-t2",
            "title": "Java JVM Runtime",
            "description": "Class loading, bytecode verification, method area, heap, stack, generational GC (young/old), stop-the-world, JIT (C2 optimizer).",
            "exercises": 3,
            "key_concepts": ["class loading", "bytecode", "method area", "heap", "stack", "generational GC", "stop-the-world", "C2 optimizer"],
            "difficulty": "intermediate"
        },
        {
            "id": "m-05-t3",
            "type": "design",
            "difficulty": "advanced",
            "prompt": "Compare Python, Java, and JavaScript runtimes for a high-frequency trading system. What are the latency guarantees? Can any of them guarantee sub-millisecond response times?",
            "mastery": "expert"
        }
    ]
}

# Module 6: Software Design Principles
MODULE_SOFTWARE_DESIGN = {
    "id": "m-06",
    "title": "Software Design: From Patterns to First Principles",
    "description": "Designing maintainable, extensible software from first principles. No templates. Deriving solutions from requirements, constraints, and trade-offs.",
    "level": "advanced",
    "estimated_time_minutes": 90,
    "topics": [
        {
            "id": "m-06-t1",
            "title": "Design Principles: SOLID, DRY, KISS, YAGNI — From First Principles",
            "description": "Why each principle exists. When to apply each. When to violate each. The mathematics of coupling + cohesion.",
            "exercises": 3,
            "key_concepts": ["SOLID", "DRY", "KISS", "YAGNI", "coupling", "cohesion"],
            "difficulty": "advanced"
        },
        {
            "id": "m-06-t2",
            "type": "design",
            "difficulty": "expert",
            "prompt": "Design a microservice for real-time event processing. 100K events/sec, 1ms latency SLA, fault tolerance, horizontal scaling, data consistency model. Walk through the entire design from first principles.",
            "mastery": "expert",
            "interview": True
        },
        {
            "id": "m-06-t2",
            "type": "design",
            "difficulty": "advanced",
            "prompt": "Design a database schema for a social network with 10M users. Friend graphs, follow relationships, feed generation, denormalization vs normalization. Read vs write ratio optimization.",
            "mastery": "proficient"
        }
    ]
}

# Module 7: concurrency and parallelism
MODULE_CONCURRENCY = {
    "id": "m-07",
    "title": "Concurrency and Parallelism: From Threads to Actors",
    "description": "Thread models, async/await, actor model, message passing, lock-free data structures, deadlock prevention, performance profiling.",
    "level": "advanced",
    "estimated_time_minutes": 75,
    "topics": [
        {
            "id": "m-07-t1",
            "title": "Thread Models: Pthreads, C++11, Go Routines",
            "description": "OS-level threads vs green threads, context switch cost, stack size, thread pools, async/await event loop, actor model (Akka, Orleans).",
            "exercises": 3,
            "key_concepts": ["OS threads", "green threads", "context switch", "thread pool", "async/await", "actor model"],
            "difficulty": "intermediate"
        },
        {
            "id": "m-07-t2",
            "type": "bug",
            "difficulty": "expert",
            "prompt": "This program has a deadlock. Identify the deadlock cycle, explain happens-before, draw the resource allocation graph, and fix it with lock ordering or lock-free data structures.",
            "mastery": "expert"
        },
        {
            "id": "m-07-t3",
            "type": "design",
            "difficulty": "expert",
            "prompt": "Design a high-concurrency server for 100K concurrent connections. Reactor pattern vs Proactor pattern vs Actor model. Event loop vs thread pool. Nginx vs Node.js vs Go vs Java Vertx.",
            "mastery": "expert"
        }
    ]
}

# Module 8: Performance Profiling and Optimization
MODULE_PERFORMANCE = {
    "id": "m-08",
    "title": "Performance Profiling and Optimization from First Principles",
    "description": "How to actually profile real programs: perf, gprof, Instruments, valgrind. CPU profiling, memory profiling, benchmarking methodology, regression testing.",
    "level": "advanced",
    "estimated_time_minutes": 60,
    "topics": [
        {
            "id": "m-08-t1",
            "type": "design",
            "difficulty": "advanced",
            "prompt": "Profile this medium-sized C program with perf. Identify the top 3 hot functions, their call graphs, and the percentage of total CPU time. Recommend 3 optimizations with expected speedup.",
            "mastery": "expert"
        },
        {
            "id": "m-08-t2",
            "type": "bug",
            "difficulty": "advanced",
            "prompt": "This program has a memory leak detected by Valgrind. Identify the exact allocation/deallocation pattern causing the leak, fix it, and verify with Valgrind post-fix.",
            "mastery": "expert"
        },
        {
            "id": "m-08-t3",
            "type": "optimize",
            "difficulty": "expert",
            "prompt": "Micro-benchmark this function with 10ns precision. Optimize the loop, use SIMD, reduce cache misses. Report before/after cycles per iteration.",
            "mastery": "expert"
        }
    ]
}

# ============================================================
# Full Curriculum Assembly
# ============================================================

FULL_CURRICULUM = {
    "module_foundations": MODULE_FOUNDATIONS,
    "module_memory": MODULE_MEMORY,
    "module_data_structures": MODULE_DATA_STRUCTURES,
    "module_algorithms": MODULE_ALGORITHMS,
    "module_runtimes": MODULE_RUNTIMES,
    "module_software_design": MODULE_SOFTWARE_DESIGN,
    "module_concurrency": MODULE_CONCURRENCY,
    "module_performance": MODULE_PERFORMANCE,
}

# Topics by module
TOPIC_INDEX = {}
for module_key, module_data in FULL_CURRICULUM.items():
    for topic in module_data["topics"]:
        TOPIC_INDEX[topic["id"]] = {**topic, "module": module_key}

# Exercises by ID
EXERCISE_INDEX = {}
module_keys = list(FULL_CURRICULUM.keys())
for module_key in module_keys:
    for topic in FULL_CURRICULUM[module_key]["topics"]:
        for ex in topic["exercises"]:
            ex_id_key = f"{module_key}_{ex['id']}"
            EXERCISE_INDEX[ex_id_key] = {**ex, "module": module_key, "topic_id": topic["id"]}

# Difficulty distribution
DIFFICULTY_DISTRIBUTION = {"beginner": 0, "intermediate": 0, "advanced": 0, "expert": 0}
for module_key in module_keys:
    for topic in FULL_CURRICULUM[module_key]["topics"]:
        for ex in topic["exercises"]:
            d = ex["difficulty"]
            if d in DIFFICULTY_DISTRIBUTION:
                DIFFICULTY_DISTRIBUTION[d] += 1

# Premium mapping
PREMIUM_MAP = {
    "module_foundations": False,
    "module_memory": False,
    "module_data_structures": False,
    "module_algorithms": False,
    "module_runtimes": True,
    "module_software_design": True,
    "module_concurrency": True,
    "module_performance": True,
}

# Total counts
TOTAL_EXERCISES = sum(
    len(module_data["topics"]) * [len(t["exercises"]) for t in module_data["topics"]]
    for module_data in FULL_CURRICULUM.values()
)
# Actually count properly
TOTAL_EXERCISES = sum(
    sum(len(t["exercises"]) for t in module_data["topics"])
    for module_data in FULL_CURRICULUM.values()
)

# ============================================================
# Ready-to-Use Exports
# ============================================================

__all__ = [
    "FULL_CURRICULUM",
    "EXERCISE_INDEX",
    "TOPIC_INDEX",
    "DIFFICULTY_DISTRIBUTION",
    "PREMIUM_MAP",
    "TOTAL_EXERCISES",
    "MODULE_FOUNDATIONS",
    "MODULE_MEMORY",
    "MODULE_DATA_STRUCTURES",
    "MODULE_ALGORITHMS",
    "MODULE_RUNTIMES",
    "MODULE_SOFTWARE_DESIGN",
    "MODULE_CONCURRENCY",
    "MODULE_PERFORMANCE",
]

# Convenience counts
CURRICULUM_STATS = {
    "total_modules": len(FULL_CURRICULUM),
    "total_topics": sum(len(m["topics"]) for m in FULL_CURRICULUM.values()),
    "total_exercises": TOTAL_EXERCISES,
    "premium_modules": sum(1 for m in FULL_CURRICULUM.values() if PREMIUM_MAP[m]),
    "free_modules": sum(1 for m in FULL_CURRICULUM.values() if not PREMIUM_MAP[m]),
    "exercises_by_difficulty": DIFFICULTY_DISTRIBUTION,
    "exercises_by_type": {
        t: sum(1 for m in FULL_CURRICULUM.values()
               for topic in m["topics"]
               for ex in t["exercises"]
               if EXERCISE_INDEX.get(f"{m}_{ex['id']}", {}).get("challenge_type") == t)
        for t in ["code", "trace", "bug", "predict", "design", "mcq", "optimize", "compare", "refactor"]
    }
}