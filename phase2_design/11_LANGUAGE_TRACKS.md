# 11 FOUR PROGRAMMING-LANGUAGE TRACKS

**BountyCode — Phase 2B Scope-Completeness Review**
**Status: Design-only document**
**No application code written**

---

## 1. Purpose

Define separate, complete learning tracks for C, C++, Python, and Java. Each track covers fundamentals through implementation practice with independent evidence tracking. A learner's capability in one language must not automatically imply capability in another.

This is a design document. No implementation is authorized.

---

## 2. Language Track Architecture

### 2.1 Canonical Concept Mapping

| Concept | Canonical Skill ID | V1 Status |
|---------|-------------------|-----------|
| Variables and types | `coding.fundamentals.variables` | Roadmap (World 4 pseudocode covers logic only) |
| Conditions | `coding.fundamentals.conditions` | Roadmap |
| Loops | `coding.fundamentals.loops` | Roadmap |
| Functions | `coding.fundamentals.functions` | Roadmap |
| Arrays/Strings | `coding.fundamentals.arrays_strings` | Roadmap |
| Memory and pointers | `coding.fundamentals.memory` | Roadmap (C-specific) |
| OOP | `coding.fundamentals.oop` | Roadmap |
| Error handling | `coding.fundamentals.error_handling` | Roadmap |
| Collections | `coding.fundamentals.collections` | Roadmap |
| Data structure implementations | `coding.dsa_implementations` | Roadmap |
| Algorithm implementations | `coding.algo_implementations` | Roadmap |
| Timed coding practice | `coding.timed_practice` | Roadmap |

### 2.2 Language Track Prefixes

| Language | Skill ID Prefix | V1 Status | Roadmap Status |
|----------|----------------|-----------|----------------|
| C | `coding.c.*` | Roadmap | Track 1 |
| C++ | `coding.cpp.*` | Roadmap | Track 2 |
| Python | `coding.python.*` | Roadmap | Track 3 |
| Java | `coding.java.*` | Roadmap | Track 4 |

### 2.3 Independence Rule

Each language track maintains independent evidence:
- `dsa.arrays` mastery in Java does NOT imply `dsa.arrays` mastery in C or Python
- Each language's evidence events reference `language` field
- Mastery claims are language-specific
- A learner must complete each language track independently

---

## 3. C Programming Track (`coding.c.*`)

### 3.1 Concept Hierarchy

| Concept | Skill ID | Prerequisite | Difficulty | Interaction | Assessment | V1/Roadmap |
|---------|----------|--------------|------------|-------------|------------|------------|
| Variables and types | `coding.c.fundamentals.variables` | None | Easy | Fill | Exact match | Roadmap |
| Operators | `coding.c.fundamentals.operators` | Variables | Easy | Manipulate | Deterministic | Roadmap |
| Conditions | `coding.c.fundamentals.conditions` | Operators | Easy | Select | Branch match | Roadmap |
| Loops | `coding.c.fundamentals.loops` | Conditions | Medium | Trace | Loop output | Roadmap |
| Functions | `coding.c.fundamentals.functions` | Loops | Medium | Fill | Return value | Roadmap |
| Arrays | `coding.c.arrays` | Functions | Medium | Manipulate | Index/output | Roadmap |
| Strings | `coding.c.strings` | Arrays | Medium | Manipulate | String output | Roadmap |
| Pointers | `coding.c.pointers.memory` | Arrays | Hard | Trace | Address/output | Roadmap |
| Dynamic memory | `coding.c.memory.dynamic` | Pointers | Hard | Trace | Leak/output | Roadmap |
| Structures | `coding.c.structures` | Pointers | Medium | Fill | Struct output | Roadmap |
| File I/O | `coding.c.file_io` | Structures | Easy | Fill | Output match | Roadmap |
| Preprocessor | `coding.c.preprocessor` | None | Easy | Select | Output match | Roadmap |
| Debugging C | `coding.c.debugging` | Pointers | Hard | Debug | Test cases pass | Roadmap |
| DSA in C | `coding.c.dsa_implementations` | Pointers + Arrays | Hard | Implement | Test cases pass | Roadmap |
| Algorithms in C | `coding.c.algo_implementations` | DSA in C | Hard | Implement | Test cases pass | Roadmap |
| Timed C practice | `coding.c.timed_practice` | DSA in C | Hard | Implement | Hidden tests pass | Roadmap |

### 3.2 C-Specific Features

| Feature | Description | Interaction | Evidence |
|---------|-------------|-------------|----------|
| Memory tracing | Visualize stack/heap, pointer addresses | Trace | Pointer state validation |
| Manual memory management | malloc/free correctness | Debug | Leak detection |
| Pointer arithmetic | Address manipulation | Manipulate | Address validation |
| String null termination | `\0` handling | Fill | Exact match |
| Struct memory layout | Field offsets | Trace | Output match |
| File I/O | fopen/fread/fwrite | Fill | Output match |
| Make/build process | Compile flags, warnings | Select | Warning/error match |

---

## 4. C++ Programming Track (`coding.cpp.*`)

### 4.1 Concept Hierarchy

| Concept | Skill ID | Prerequisite | Difficulty | Interaction | Assessment | V1/Roadmap |
|---------|----------|--------------|------------|-------------|------------|------------|
| C++ fundamentals | `cpp.fundamentals` | C fundamentals | Easy | Fill | Exact match | Roadmap |
| References | `cpp.fundamentals.references` | Pointers | Medium | Trace | Address/output | Roadmap |
| OOP | `cpp.oop` | Functions | Medium | Fill | Class output | Roadmap |
| Classes/Objects | `cpp.oop.classes` | OOP | Medium | Fill | Object state | Roadmap |
| Constructors/Destructors | `cpp.oop.constructors` | Classes | Medium | Trace | Lifecycle output | Roadmap |
| Inheritance | `cpp.oop.inheritance` | Classes | Hard | Fill | Output match | Roadmap |
| Polymorphism | `cpp.oop.polymorphism` | Inheritance | Hard | Trace | Virtual dispatch | Roadmap |
| Encapsulation | `cpp.oop.encapsulation` | Classes | Medium | Select | Access match | Roadmap |
| STL containers | `cpp.stl.containers` | OOP | Medium | Manipulate | Output match | Roadmap |
| STL algorithms | `cpp.stl.algorithms` | Containers | Medium | Fill | Output match | Roadmap |
| Smart pointers | `cpp.stl.smart_pointers` | Pointers | Hard | Trace | Lifecycle output | Roadmap |
| Templates | `cpp.templates` | OOP | Hard | Fill | Instantiation | Roadmap |
| Exception handling | `cpp.exceptions` | OOP | Medium | Fill | Output match | Roadmap |
| Move semantics | `cpp.move_semantics` | Smart pointers | Hard | Trace | Lifecycle output | Roadmap |
| Debugging C++ | `cpp.debugging` | OOP + STL | Hard | Debug | Test cases pass | Roadmap |
| DSA in C++ | `cpp.dsa_implementations` | STL + OOP | Hard | Implement | Test cases pass | Roadmap |
| Algorithms in C++ | `cpp.algo_implementations` | DSA in C++ | Hard | Implement | Test cases pass | Roadmap |
| Timed C++ practice | `cpp.timed_practice` | DSA in C++ | Hard | Implement | Hidden tests pass | Roadmap |

### 4.2 C++-Specific Features

| Feature | Description | Interaction | Evidence |
|---------|-------------|-------------|----------|
| RAII | Resource acquisition is initialization | Trace | Destructor call verification |
| STL vector/list/map | Container operations | Manipulate | Output match |
| STL sort/find/transform | Algorithm usage | Fill | Output match |
| Smart pointer ownership | unique_ptr/shared_ptr | Trace | Reference count |
| Virtual function table | Polymorphism dispatch | Trace | vtable output |
| Template instantiation | Generic code generation | Fill | Compilation + output |
| Move/copy semantics | Resource transfer | Trace | Lifecycle output |

---

## 5. Python Programming Track (`coding.python.*`)

### 5.1 Concept Hierarchy

| Concept | Skill ID | Prerequisite | Difficulty | Interaction | Assessment | V1/Roadmap |
|---------|----------|--------------|------------|-------------|------------|------------|
| Python fundamentals | `python.fundamentals` | None | Easy | Fill | Exact match | Roadmap |
| Dynamic typing | `python.fundamentals.dynamic_types` | Fundamentals | Easy | Manipulate | Type output | Roadmap |
| Conditions | `python.fundamentals.conditions` | Dynamic types | Easy | Select | Branch match | Roadmap |
| Loops | `python.fundamentals.loops` | Conditions | Medium | Trace | Loop output | Roadmap |
| Functions | `python.fundamentals.functions` | Loops | Medium | Fill | Return value | Roadmap |
| Lists | `python.collections.lists` | Functions | Medium | Manipulate | List output | Roadmap |
| Dictionaries | `python.collections.dicts` | Lists | Medium | Manipulate | Dict output | Roadmap |
| Sets | `python.collections.sets` | Dictionaries | Easy | Manipulate | Set output | Roadmap |
| Tuples | `python.collections.tuples` | Lists | Easy | Select | Immutable match | Roadmap |
| String methods | `python.collections.strings` | Lists | Easy | Manipulate | Output match | Roadmap |
| Exceptions | `python.exceptions` | Functions | Medium | Fill | Output match | Roadmap |
| Classes/OOP | `python.oop` | Functions | Medium | Fill | Class output | Roadmap |
| List comprehensions | `python.collections.comprehensions` | Lists | Medium | Fill | List output | Roadmap |
| Generators | `python.generators` | Functions | Hard | Trace | Yield output | Roadmap |
| Decorators | `python.decorators` | Functions | Hard | Fill | Wrapper output | Roadmap |
| File I/O | `python.file_io` | Functions | Easy | Fill | Output match | Roadmap |
| Debugging Python | `python.debugging` | OOP + Exceptions | Hard | Debug | Test cases pass | Roadmap |
| DSA in Python | `python.dsa_implementations` | Collections + OOP | Hard | Implement | Test cases pass | Roadmap |
| Algorithms in Python | `python.algo_implementations` | DSA in Python | Hard | Implement | Test cases pass | Roadmap |
| Timed Python practice | `python.timed_practice` | DSA in Python | Hard | Implement | Hidden tests pass | Roadmap |

### 5.2 Python-Specific Features

| Feature | Description | Interaction | Evidence |
|---------|-------------|-------------|----------|
| Dynamic typing | Type changes at runtime | Manipulate | Type output |
| List comprehensions | Declarative list building | Fill | Exact output |
| Generators | `yield` and lazy evaluation | Trace | Yield sequence |
| Decorators | Function wrapping | Fill | Wrapper output |
| Context managers | `with` statement | Trace | Resource lifecycle |
| Duck typing | Implicit interfaces | Select | Method existence |

---

## 6. Java Programming Track (`coding.java.*`)

### 6.1 Concept Hierarchy

| Concept | Skill ID | Prerequisite | Difficulty | Interaction | Assessment | V1/Roadmap |
|---------|----------|--------------|------------|-------------|------------|------------|
| Java fundamentals | `java.fundamentals` | None | Easy | Fill | Exact match | Roadmap |
| Classes/Objects | `java.oop.classes` | Fundamentals | Medium | Fill | Object state | Roadmap |
| Constructors | `java.oop.constructors` | Classes | Medium | Trace | Lifecycle output | Roadmap |
| Inheritance | `java.oop.inheritance` | Classes | Hard | Fill | Output match | Roadmap |
| Polymorphism | `java.oop.polymorphism` | Inheritance | Hard | Trace | Virtual dispatch | Roadmap |
| Interfaces | `java.oop.interfaces` | Polymorphism | Medium | Fill | Contract match | Roadmap |
| Abstract classes | `java.oop.abstract` | Inheritance | Medium | Fill | Instantiation rule | Roadmap |
| Encapsulation | `java.oop.encapsulation` | Classes | Medium | Select | Access match | Roadmap |
| Exceptions | `java.exceptions` | OOP | Medium | Fill | Output match | Roadmap |
| Collections Framework | `java.collections` | OOP | Medium | Manipulate | Output match | Roadmap |
| ArrayList/LinkedList | `java.collections.list` | Collections | Medium | Manipulate | Output match | Roadmap |
| HashMap/HashSet | `java.collections.map_set` | Collections | Medium | Manipulate | Output match | Roadmap |
| Streams | `java.streams` | Collections | Hard | Fill | Pipeline output | Roadmap |
| File I/O | `java.file_io` | OOP | Easy | Fill | Output match | Roadmap |
| Debugging Java | `java.debugging` | OOP + Collections | Hard | Debug | Test cases pass | Roadmap |
| DSA in Java | `java.dsa_implementations` | Collections + OOP | Hard | Implement | Test cases pass | Roadmap |
| Algorithms in Java | `java.algo_implementations` | DSA in Java | Hard | Implement | Test cases pass | Roadmap |
| Timed Java practice | `java.timed_practice` | DSA in Java | Hard | Implement | Hidden tests pass | Roadmap |

### 6.2 Java-Specific Features

| Feature | Description | Interaction | Evidence |
|---------|-------------|-------------|----------|
| JVM execution | Bytecode interpretation | Select | Output match |
| Garbage collection | Automatic memory management | Trace | Object lifecycle |
| Classpath | Compilation and execution | Select | Command match |
| Package/access modifiers | Visibility rules | Select | Access match |
| Interface implementation | Contract fulfillment | Fill | Method signatures |
| Generics | Type-safe collections | Fill | Type output |
| Lambda expressions | Functional interfaces | Fill | Output match |
| Stream API | Functional pipeline | Fill | Pipeline output |

---

## 7. Compilation, Execution, and Test Cases per Language

| Language | Compiler/Runner | Test Case Format | Runtime Error Handling |
|----------|----------------|------------------|------------------------|
| C | `gcc` | stdin/stdout + expected output | Exit code + stderr capture |
| C++ | `g++` | stdin/stdout + expected output | Exit code + stderr capture |
| Python | `python3` | stdin/stdout + expected output | Exception traceback capture |
| Java | `javac` + `java` | stdin/stdout + expected output | Exception traceback capture |

### 7.1 Test Case Schema (Language-Agnostic)

```json
{
  "question_id": "coding.c.arrays.reverse",
  "language": "c",
  "test_cases": [
    {
      "input": "[1, 2, 3, 4, 5]",
      "expected_output": "[5, 4, 3, 2, 1]",
      "explanation": "Reversed array"
    }
  ],
  "hidden_test_cases": [...],
  "time_limit_seconds": 2,
  "memory_limit_mb": 256
}
```

### 7.2 Evidence Emitted Per Language Attempt

| Field | Description |
|-------|-------------|
| `language` | `"c"` / `"cpp"` / `"python"` / `"java"` |
| `compiler_exit_code` | 0 for success, non-zero for compile error |
| `stderr` | Compiler/runtime error message |
| `test_cases_passed` | Integer count |
| `test_cases_total` | Integer count |
| `execution_time_ms` | Float |
| `memory_used_kb` | Integer |

---

## 8. Design Review Checklist

| # | Question | Status |
|---|----------|--------|
| 1 | Four language tracks defined separately? | Yes |
| 2 | Independent evidence per language? | Yes |
| 3 | No automatic proficiency transfer between languages? | Yes |
| 4 | Each track covers fundamentals through implementation? | Yes |
| 5 | Compilation/execution defined per language? | Yes |
| 6 | Test case schema defined? | Yes |
| 7 | C covers memory/pointers? | Yes |
| 8 | C++ covers OOP/STL/smart pointers? | Yes |
| 9 | Python covers dynamic typing/generators/decorators? | Yes |
| 10 | Java covers OOP/collections/streams? | Yes |
| 11 | All tracks are roadmap (not V1)? | Yes |
| 12 | Aligned with Vision Lock (pseudocode is V1 differentiator)? | Yes |

---

## 13. V1 vs Roadmap Boundary

| Element | V1 Launch | Roadmap |
|---------|-----------|---------|
| Pseudocode/Programming Logic | ✅ World 4 | — |
| C programming track | ❌ | ✅ |
| C++ programming track | ❌ | ✅ |
| Python programming track | ❌ | ✅ |
| Java programming track | ❌ | ✅ |
| Language-specific DSA implementation | ❌ | ✅ |
| Language-specific algorithm implementation | ❌ | ✅ |
| Timed language-specific coding practice | ❌ | ✅ |

---

**End of 11 Four Programming-Language Tracks**
