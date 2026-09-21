"""Expand the BountyCode Knowledge Corpus with missing and additional concepts.

Usage:
    python backend/scripts/expand_corpus.py
    python backend/scripts/expand_corpus.py --dry-run
    python backend/scripts/expand_corpus.py --validate-only
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

_KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "app" / "data" / "knowledge"
_CORPUS_FILE = _KNOWLEDGE_DIR / "corpus.json"


def load_corpus(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def save_corpus(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, default=str)
    logger.info("Wrote expanded corpus to %s", path)


def validate_corpus_data(data: dict) -> list[str]:
    issues: list[str] = []
    concepts = data.get("concepts", {})
    prereq_graph = data.get("prerequisite_graph", {})

    all_ids = set(concepts.keys())
    for concept_id, prereqs in prereq_graph.items():
        for prereq in prereqs:
            if prereq not in all_ids:
                issues.append(f"Concept '{concept_id}' has prerequisite '{prereq}' which does not exist.")

    def _detect_cycle(node: str, visited: set[str], path: set[str]) -> list[str] | None:
        if node in path:
            return list(path) + [node]
        if node in visited:
            return None
        visited.add(node)
        path.add(node)
        for prereq in prereq_graph.get(node, []):
            cycle = _detect_cycle(prereq, visited, path)
            if cycle:
                return cycle
        path.discard(node)
        return None

    visited: set[str] = set()
    for concept_id in concepts:
        if concept_id not in visited:
            cycle = _detect_cycle(concept_id, visited, set())
            if cycle:
                issues.append(f"Circular dependency detected: {' -> '.join(cycle)}")

    return issues


def concept_template(
    concept_id: str,
    title: str,
    domain: str,
    language: str,
    category: str,
    prerequisites: list[str],
    related_concepts: list[str],
    difficulty: int = 1,
    definition: str = "",
    mental_model: str = "",
    key_rules: list[str] | None = None,
    common_mistakes: list[str] | None = None,
    edge_cases: list[str] | None = None,
    debugging_patterns: list[str] | None = None,
    interview_questions: list[str] | None = None,
    practice_targets: list[str] | None = None,
    placement_relevance: list[str] | None = None,
    source_references: list[dict] | None = None,
) -> dict:
    return {
        "id": concept_id,
        "title": title,
        "domain": domain,
        "language": language,
        "category": category,
        "prerequisites": prerequisites,
        "related_concepts": related_concepts,
        "difficulty": difficulty,
        "definition": definition,
        "mental_model": mental_model,
        "key_rules": key_rules or [],
        "common_mistakes": common_mistakes or [],
        "edge_cases": edge_cases or [],
        "debugging_patterns": debugging_patterns or [],
        "interview_questions": interview_questions or [],
        "practice_targets": practice_targets or [],
        "placement_relevance": placement_relevance or [],
        "source_references": source_references or [],
        "worked_examples": [],
        "misconceptions": [],
        "transfer_targets": [],
        "verification": {
            "sources": source_references or [],
            "last_verified": "2026-09-15",
            "verified_by": "corpus_bootstrap",
            "verification_notes": ""
        },
        "worked_examples": [],
        "misconceptions": [],
        "transfer_targets": [],
        "verification": {
            "sources": source_references or [],
            "last_verified": "2026-09-15",
            "verified_by": "corpus_bootstrap",
            "verification_notes": ""
        },
        "generated_content": {"lessons": [], "exercises": [], "assessments": []},
        "content_status": "AUTO_SCAFFOLDED",
        "last_verified": "2026-09-15",
    }


def generate_missing_concepts() -> dict[str, dict]:
    """Generate all concepts that are referenced in the prerequisite graph but missing."""
    concepts: dict[str, dict] = {}

    # C
    concepts["c_control_flow"] = concept_template(
        "c_control_flow", "C Control Flow", "programming", "c", "basics",
        ["c_basics"], ["c_functions", "c_loops"],
        definition="Control flow statements (if/else, switch, loops) direct execution order in C.",
        mental_model="Control flow is a choose-your-own-adventure book. if/else branches. loops repeat chapters. switch picks by label.",
        key_rules=["if/else branches on boolean", "switch uses integer/char labels", "break exits switch/loop", "continue skips iteration", "for/while/do-while cover all loops"],
        common_mistakes=["Forgetting break in switch", "Using = instead of ==", "Off-by-one in bounds", "Infinite loops from missing increment"],
        edge_cases=["Fall-through can be intentional", "do-while runs at least once", "Comma operator in for init"],
        debugging_patterns=["Trace with printf", "Use gdb breakpoints", "Check loop conditions"],
        interview_questions=["Difference between while and do-while?", "When use switch vs if-else?", "What is fall-through?"],
        practice_targets=["Grade calculator with if-else", "Menu with switch", "Print patterns with loops"],
        placement_relevance=["tcs", "infosys", "wipro"],
    )
    concepts["c_io"] = concept_template(
        "c_io", "C Input/Output", "programming", "c", "basics",
        ["c_basics"], ["c_strings", "c_functions"],
        definition="C provides formatted I/O via stdio.h: printf(), scanf(), and file I/O via fopen(), fprintf(), fscanf().",
        mental_model="printf is a type-safe messenger needing format specifiers. scanf reads using the same specifiers.",
        key_rules=["%d int, %f float, %s char*", "scanf needs & for non-pointers", "return value = successful conversions", "EOF indicates end/error"],
        common_mistakes=["Using & with string arrays", "Mismatched format specifier", "Not checking scanf return", "Forgetting \\n in printf"],
        edge_cases=["scanf stops at whitespace for %s", "Buffer overflow with unbounded %s", "stdin is line-buffered"],
        debugging_patterns=["Check scanf return value", "Use fflush(stdin) carefully", "Print input before processing"],
        interview_questions=["printf vs scanf?", "Why does scanf need & for int but not arrays?", "What does EOF mean?"],
        practice_targets=["Read name and age with scanf", "Print formatted table", "Read until EOF"],
        placement_relevance=["tcs", "infosys", "wipro"],
    )
    concepts["c_functions"] = concept_template(
        "c_functions", "C Functions", "programming", "c", "functions",
        ["c_control_flow", "c_variables"], ["c_arrays", "c_pointers"],
        definition="Functions in C are reusable blocks with return type, name, parameters, and body. Every C program starts at main().",
        mental_model="A function is a worker. Parameters are materials. Return value is the product. main() is the foreman.",
        key_rules=["Declare before use or prototype", "Return type matches return statement", "Parameters passed by value unless pointer", "main() returns int (0 = success)"],
        common_mistakes=["Forgetting prototype", "Mismatched parameter types", "Missing return", "Confusing pass-by-value vs reference"],
        edge_cases=["Empty param list means unspecified (not empty)", "Variadic functions with stdarg.h", "Function pointers for callbacks"],
        debugging_patterns=["Check parameter values at entry", "Verify return value type", "Use gdb to step into function"],
        interview_questions=["Declaration vs definition?", "Why function prototypes?", "What does void mean in signature?"],
        practice_targets=["Swap two numbers", "Factorial recursively", "Return pointer from function"],
        placement_relevance=["tcs", "infosys", "wipro", "cognizant"],
    )
    concepts["c_arrays"] = concept_template(
        "c_arrays", "C Arrays", "programming", "c", "data_structures",
        ["c_functions", "c_pointers"], ["c_strings", "c_structures"],
        definition="Arrays in C are contiguous memory blocks. Array name decays to pointer in most contexts.",
        mental_model="An array is a row of identical lockers. Name is address of locker 0. arr[i] is locker i. C doesn't track length.",
        key_rules=["Size fixed at compile time (except VLAs)", "arr[i] == *(arr + i)", "Array decays to pointer", "Out-of-bounds is undefined behavior", "sizeof(array) vs sizeof(pointer)"],
        common_mistakes=["Off-by-one indexing", "Confusing sizeof(array) with sizeof(pointer)", "Returning address of local array", "Not initializing elements"],
        edge_cases=["VLAs in C99", "Array parameters decay to pointers", "sizeof trick only works on actual arrays"],
        debugging_patterns=["Print addresses with %p", "Use gdb to inspect memory", "Check bounds before access"],
        interview_questions=["What is array decay?", "Why does sizeof(arr) differ inside/outside functions?", "How pass array to function?"],
        practice_targets=["Linear search", "Reverse in place", "Matrix multiplication"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon"],
    )
    concepts["c_strings"] = concept_template(
        "c_strings", "C Strings", "programming", "c", "data_structures",
        ["c_arrays", "c_pointers"], ["c_file_io", "c_dynamic_memory"],
        definition="C strings are null-terminated char arrays. No string type; strings are char* ending with \\0.",
        mental_model="A C string is characters ending with a period (null terminator). strlen counts before period. strcpy copies until period.",
        key_rules=["Ends with \\0", "strlen counts bytes before null", "strcpy needs sufficient destination", "strcmp returns 0 when equal", "String literals are read-only"],
        common_mistakes=["Forgetting null terminator", "Buffer overflow in strcpy", "Using == to compare strings", "Modifying string literals"],
        edge_cases=["strcmp returns negative/positive", "strncpy may not null-terminate", "Literals in read-only memory"],
        debugging_patterns=["Print with %s", "Use strlen to verify length", "Check for null before dereferencing"],
        interview_questions=["How are C strings represented?", "strcpy vs strncpy?", "Why can't compare strings with ==?"],
        practice_targets=["Implement strlen manually", "Write strcpy manually", "String reversal"],
        placement_relevance=["tcs", "infosys", "wipro"],
    )
    concepts["c_memory"] = concept_template(
        "c_memory", "C Memory Layout", "programming", "c", "memory",
        ["c_variables"], ["c_pointers", "c_dynamic_memory"],
        definition="C programs use four memory regions: code (text), global/static, heap (dynamic), and stack (locals/function frames).",
        mental_model="Memory is a building. Ground floor = stack (temporary). Basement = heap (manual). Roof = code. Walls = globals.",
        key_rules=["Stack: automatic, limited size", "Heap: manual malloc/free, larger", "Globals/static: program lifetime", "Code: read-only", "Stack overflow from deep recursion"],
        common_mistakes=["Stack overflow from large locals", "Heap leaks from missing free()", "Use-after-free", "Confusing stack vs heap lifetimes"],
        edge_cases=["alloca on stack (non-standard)", "Stack size varies by OS", "Memory alignment requirements"],
        debugging_patterns=["Use valgrind for leaks", "Check /proc/pid/maps", "Use gdb to inspect stack"],
        interview_questions=["Stack vs heap?", "What causes stack overflow?", "Where are globals stored?"],
        practice_targets=["Trace stack frames for recursion", "Measure stack vs heap speed", "Detect leak with valgrind"],
        placement_relevance=["tcs", "infosys", "cognizant"],
    )
    concepts["c_structures"] = concept_template(
        "c_structures", "C Structures", "programming", "c", "data_structures",
        ["c_pointers"], ["c_oop", "c_dynamic_memory"],
        definition="Structures group related data items of different types. They are the foundation for complex data in C.",
        mental_model="A struct is a custom form. Fields are boxes. Pointer to struct passes the form by reference.",
        key_rules=["struct groups heterogeneous data", "Dot operator for value, arrow for pointer", "sizeof includes padding", "Pass by value or pointer"],
        common_mistakes=["Forgetting & for struct pointer assignment", "Confusing . and ->", "Assuming struct size = sum of members", "Not handling padding"],
        edge_cases=["Flexible array member at end", "Self-referential structs need typedef", "Bit-fields for packed data"],
        debugging_patterns=["Print size with sizeof", "Check field addresses with offsetof", "Use gdb to inspect struct memory"],
        interview_questions=["struct vs union?", "Pass struct efficiently?", "What is struct padding?"],
        practice_targets=["Define Student struct", "Linked list node with struct", "Sort array of structs"],
        placement_relevance=["tcs", "infosys", "wipro"],
    )
    concepts["c_dynamic_memory"] = concept_template(
        "c_dynamic_memory", "C Dynamic Memory Allocation", "programming", "c", "memory",
        ["c_pointers", "c_memory"], ["c_structures", "c_file_io"],
        definition="Dynamic memory allocation uses malloc(), calloc(), realloc(), and free() from stdlib.h.",
        mental_model="Dynamic memory is self-storage. malloc asks heap for a box. free() returns it. Forgetting free causes leaks.",
        key_rules=["malloc(size) returns void* or NULL", "calloc zero-initializes", "realloc resizes", "free returns to heap", "Never free twice or access after free"],
        common_mistakes=["Not checking malloc for NULL", "Memory leaks", "Double free", "Using realloc without backup", "Buffer overflow corrupts heap"],
        edge_cases=["malloc(0) implementation-defined", "realloc(NULL) == malloc", "free(NULL) is safe"],
        debugging_patterns=["Check all malloc returns", "Use valgrind", "Track allocations with wrapper"],
        interview_questions=["What if malloc fails?", "malloc vs calloc?", "Why is free() needed?"],
        practice_targets=["Dynamic array with push_back", "Implement strdup()", "Matrix allocation/deallocation"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon"],
    )
    concepts["c_file_io"] = concept_template(
        "c_file_io", "C File I/O", "programming", "c", "io",
        ["c_arrays", "c_strings"], ["c_dynamic_memory"],
        definition="C file I/O uses FILE* streams: fopen, fprintf/fscanf for formatted, fread/fwrite for binary.",
        mental_model="A file is a stream of bytes. fopen opens a channel. fprintf writes formatted text. fwrite writes raw bytes. fclose shuts the channel.",
        key_rules=["fopen returns FILE* or NULL", "Modes: r, w, a, r+, w+, a+, rb, wb", "fclose flushes and releases", "feof/ferror check status", "rewind/fseek move position"],
        common_mistakes=["Not checking fopen", "Mismatched text/binary modes", "Not checking fclose", "Buffer not flushed on crash"],
        edge_cases=["Text mode translates \\n on Windows", "Binary mode for exact bytes", "fseek beyond end undefined for text"],
        debugging_patterns=["Check fopen with perror", "Use fflush before reading", "Verify position with ftell"],
        interview_questions=["File opening modes?", "Text vs binary mode?", "How check EOF?"],
        practice_targets=["Copy file contents", "Count lines/words/chars", "Write/read struct to binary"],
        placement_relevance=["tcs", "infosys", "wipro"],
    )

    # C++
    concepts["cpp_io"] = concept_template(
        "cpp_io", "C++ Input/Output", "programming", "cpp", "basics",
        ["cpp_basics"], ["cpp_strings", "cpp_streams"],
        definition="C++ uses iostream (cin, cout) for type-safe stream-based I/O.",
        mental_model="Streams are conveyor belts. << sends to cout. >> receives from cin. Compiler checks types.",
        key_rules=["cout << value", "cin >> variable", "Type-safe at compile time", "Can chain: cout << a << b", "endl flushes; \\n often sufficient"],
        common_mistakes=["Mixing cin and printf", "Not checking cin state", "Using endl excessively", "Confusing << and >>"],
        edge_cases=["cin fails on type mismatch (failbit)", "tie() syncs cin/cout", "rdbuf() redirects streams"],
        debugging_patterns=["Check cin.fail()", "Use std::cerr for debug", "Clear failbit with cin.clear()"],
        interview_questions=["cin vs scanf?", "Why type-safe?", "What does std::endl do?"],
        practice_targets=["Read name/age with cin", "Print formatted table", "Handle invalid input"],
        placement_relevance=["tcs", "infosys", "wipro"],
    )
    concepts["cpp_references"] = concept_template(
        "cpp_references", "C++ References", "programming", "cpp", "basics",
        ["cpp_basics"], ["cpp_functions", "cpp_oop"],
        definition="References are aliases for existing variables. Must be initialized and cannot be reseated.",
        mental_model="A reference is a nickname. Once given, nickname and original refer to the same thing. Cannot reseat.",
        key_rules=["Must initialize at declaration", "Cannot be null", "Cannot reseat", "int& ref = var", "Changes affect original"],
        common_mistakes=["Uninitialized reference (compile error)", "Expecting pointer-like behavior", "Returning reference to local", "Confusing & in declaration vs usage"],
        edge_cases=["Const reference binds to temporary", "Reference collapsing in templates", "Rvalue references (&&) for moves"],
        debugging_patterns=["Check initialization", "Verify object lifetime", "Use gdb to inspect through reference"],
        interview_questions=["Reference vs pointer?", "Can reference be null?", "Why const reference?"],
        practice_targets=["Swap using references", "Pass large struct by const ref", "Return reference from accessor"],
        placement_relevance=["tcs", "infosys", "wipro", "cognizant"],
    )
    concepts["cpp_functions"] = concept_template(
        "cpp_functions", "C++ Functions", "programming", "cpp", "functions",
        ["cpp_basics"], ["cpp_templates", "cpp_oop"],
        definition="C++ functions support overloading, default args, pass-by-reference, and can be class members.",
        mental_model="A C++ function is an overloadable worker. Same name, different parameters. References let worker borrow tools without copying.",
        key_rules=["Overloading: same name, different params", "Default args in declaration only", "Pass-by-reference avoids copy", "const member functions promise no mutation", "RVO/NRVO optimization"],
        common_mistakes=["Ambiguous overload resolution", "Default args in definition", "Returning reference to local", "Missing const on getters"],
        edge_cases=["Overload resolution with conversions", "Default args evaluated at call site", "Variadic templates"],
        debugging_patterns=["Check overload resolution errors", "Breakpoints in overloaded functions", "Verify const correctness"],
        interview_questions=["Function overloading?", "Pass by ref vs value?", "What does const at end of member function mean?"],
        practice_targets=["Overload max() for int/float/double", "Swap by reference", "Const-correct accessor"],
        placement_relevance=["tcs", "infosys", "wipro"],
    )
    concepts["cpp_arrays"] = concept_template(
        "cpp_arrays", "C++ Arrays & Vectors", "programming", "cpp", "data_structures",
        ["cpp_basics"], ["cpp_stl"],
        definition="C++ provides C-style arrays and std::vector (dynamic array). std::vector manages memory and provides bounds-checked access.",
        mental_model="std::vector is a smart array that grows automatically. Remembers size, manages memory, indexable like C array. Default choice.",
        key_rules=["std::vector<T> is dynamic, contiguous", "push_back() adds", "size() returns count", "v[i] unchecked, v.at(i) checked", "Grows geometrically (amortized O(1))"],
        common_mistakes=["Using C arrays when vector safer", "Not reserving capacity", "Invalidating iterators", "Confusing size() with capacity()"],
        edge_cases=["vector<bool> is a specialization", "emplace_back constructs in-place", "Shrink-to-fit reduces capacity"],
        debugging_patterns=["Check size vs capacity", "Use at() in debug", "Verify iterators after modification"],
        interview_questions=["vector vs C array?", "push_back complexity?", "How does vector manage memory?"],
        practice_targets=["Dynamic array wrapper", "Frequency counting with vector", "Sort and deduplicate"],
        placement_relevance=["tcs", "infosys", "wipro", "cognizant"],
    )
    concepts["cpp_strings"] = concept_template(
        "cpp_strings", "C++ Strings", "programming", "cpp", "data_structures",
        ["cpp_basics", "cpp_arrays"], ["cpp_stl"],
        definition="std::string is a dynamic, mutable sequence of characters with automatic memory management.",
        mental_model="std::string is a smart char array. No manual allocation. Grows as needed. Concatenate, compare, search safely.",
        key_rules=["Manages memory automatically", "Concatenation with + or +=", "Compare with ==, <, >", "c_str() returns const char*", "substr(pos, len) extracts"],
        common_mistakes=["Using c_str() then modifying", "Assuming null-terminated everywhere", "Inefficient + in loops", "size() and length() are identical"],
        edge_cases=["Empty string not null pointer", "String can contain null bytes", "Small string optimization (SSO)"],
        debugging_patterns=["Print with <<", "Check length with size()", "Use find() for search"],
        interview_questions=["C strings vs std::string?", "How does std::string manage memory?", "What is SSO?"],
        practice_targets=["String reversal", "Word frequency count", "Palindrome check"],
        placement_relevance=["tcs", "infosys", "wipro"],
    )
    concepts["cpp_oop"] = concept_template(
        "cpp_oop", "C++ OOP", "programming", "cpp", "paradigms",
        ["cpp_basics", "cpp_references"], ["cpp_templates", "cpp_stl"],
        definition="C++ OOP uses classes with encapsulation, constructors/destructors, inheritance, and virtual functions for polymorphism.",
        mental_model="Class is blueprint. Object is building. Inheritance is specialized blueprint. Virtual functions call right method without knowing exact type.",
        key_rules=["public/protected/private access", "Constructor initializes, destructor cleans up", "virtual enables runtime polymorphism", "override prevents mistakes", "Virtual destructor needed in base"],
        common_mistakes=["Forgetting virtual in base", "Not marking override", "Object slicing by value", "Missing virtual destructor"],
        edge_cases=["Virtual functions in constructors don't dispatch", "Pure virtual = 0 makes abstract", "Multiple inheritance diamond (virtual inheritance)"],
        debugging_patterns=["Print vtable addresses", "dynamic_cast for safe downcast", "Check destructor calls in gdb"],
        interview_questions=["public/private/protected?", "What is virtual function?", "What is object slicing?"],
        practice_targets=["Shape hierarchy with virtual draw()", "Add virtual destructor", "Override toString()"],
        placement_relevance=["tcs", "infosys", "wipro", "cognizant", "accenture"],
    )
    concepts["cpp_templates"] = concept_template(
        "cpp_templates", "C++ Templates", "programming", "cpp", "generics",
        ["cpp_functions"], ["cpp_stl", "cpp_oop"],
        definition="Templates enable generic programming: functions and classes parameterized by types or compile-time constants.",
        mental_model="Template is a cookie cutter. Define shape once, stamp out for each type. Compiler generates actual code per type.",
        key_rules=["template <typename T>", "T deduced from arguments", "Explicit instantiation: func<int>()", "Specialization for specific types", "Compile-time code generation"],
        common_mistakes=["Forgetting typename vs class (identical)", "Not handling all specializations", "Code bloat from many instantiations", "Template errors hard to read"],
        edge_cases=["SFINAE: substitution failure not an error", "Variadic templates for arbitrary args", "Template metaprogramming at compile time"],
        debugging_patterns=["Read template errors bottom-up", "static_assert for constraints", "Check deduction guides"],
        interview_questions=["What is a template?", "Template specialization?", "What is SFINAE?"],
        practice_targets=["Generic max() function", "Template Stack class", "Specialize for const char*"],
        placement_relevance=["tcs", "infosys", "amazon"],
    )
    concepts["cpp_iterators"] = concept_template(
        "cpp_iterators", "C++ Iterators", "programming", "cpp", "stl",
        ["cpp_stl"], ["cpp_algorithms"],
        definition="Iterators abstract container traversal. Categories: input, output, forward, bidirectional, random access.",
        mental_model="Iterator is universal remote for containers. Works on vectors, lists, sets, maps with same interface. ++ advances. * dereferences.",
        key_rules=["begin() first, end() past-last", "++ advances, * dereferences", "Categories: random_access > bidirectional > forward > input", "Invalidated by container modification"],
        common_mistakes=["Using invalidated iterators", "Confusing iterator categories", "Comparing iterators from different containers", "Not checking end() before dereferencing"],
        edge_cases=["Vector invalidates after insertion point", "List only invalidates erased element", "std::next/prev for non-random-access"],
        debugging_patterns=["Print distance with std::distance", "Check validity before dereferencing", "Use std::find to locate"],
        interview_questions=["What is an iterator?", "Iterator vs pointer?", "Iterator categories?"],
        practice_targets=["Traverse vector with iterators", "std::find with list", "Generic print with iterators"],
        placement_relevance=["tcs", "infosys", "wipro"],
    )
    concepts["cpp_algorithms"] = concept_template(
        "cpp_algorithms", "C++ STL Algorithms", "programming", "cpp", "stl",
        ["cpp_iterators"], ["cpp_stl"],
        definition="<algorithm> provides generic algorithms on iterator ranges: sort, find, transform, accumulate.",
        mental_model="Algorithms are factory machines. Feed iterator range (raw materials) and comparator (blueprint). Get sorted data, found items, or transformed results.",
        key_rules=["Work on [first, last) pairs", "sort needs random-access iterators", "Comparison: function, lambda, or default <", "find returns end() if not found", "transform applies operation to each"],
        common_mistakes=["sort on non-random-access (list)", "Not checking find() against end()", "Modifying container during algorithm", "Wrong comparator"],
        edge_cases=["stable_sort preserves equal order", "partition reorders in-place", "copy needs destination space"],
        debugging_patterns=["Check algorithm return value", "Verify comparator with tests", "Use std::is_sorted to validate"],
        interview_questions=["How does std::sort work?", "sort vs stable_sort?", "Custom condition with find?"],
        practice_targets=["Sort vector of structs by field", "Find first matching predicate", "Transform vector in-place"],
        placement_relevance=["tcs", "infosys", "wipro"],
    )

    # Java
    concepts["java_oop"] = concept_template(
        "java_oop", "Java OOP", "programming", "java", "paradigms",
        ["java_basics"], ["java_collections", "java_exceptions"],
        definition="Java OOP uses classes with access modifiers, constructors, inheritance via extends, and interfaces.",
        mental_model="Class is blueprint. Object is instance. Inheritance is specialized blueprint. Interfaces are contracts. Everything except primitives is an object reference.",
        key_rules=["extends for inheritance, implements for interfaces", "Constructors have no return type", "this = current instance", "super calls parent", "private/protected/public access"],
        common_mistakes=["== vs .equals()", "Forgetting @Override", "Not calling super()", "Using static for instance context"],
        edge_cases=["Autoboxing cache -128 to 127", "String pool", "Default no-arg constructor lost when any constructor defined"],
        debugging_patterns=["IDE debugger with object inspector", "System.out.println", "Check equals/hashCode contract"],
        interview_questions=["== vs equals()?", "Inheritance and when use it?", "What is an interface?"],
        practice_targets=["Vehicle hierarchy with Car/Truck", "Override toString() and equals()", "Payment strategy interface"],
        placement_relevance=["tcs", "infosys", "wipro", "accenture", "cognizant"],
    )
    concepts["java_exceptions"] = concept_template(
        "java_exceptions", "Java Exceptions", "programming", "java", "error_handling",
        ["java_basics"], ["java_collections"],
        definition="Java exceptions separate error handling from normal flow. Checked exceptions must be caught or declared.",
        mental_model="Exceptions are emergency signals. Checked = red alert (must handle). Runtime = programming bug. try-with-resources is automatic cleanup.",
        key_rules=["Checked: IOException, SQLException (must catch/declare)", "Runtime: unchecked (NullPointerException etc)", "try-catch-finally", "throw raises, throws declares", "try-with-resources auto-closes"],
        common_mistakes=["Catching Exception instead of specific", "Swallowing exceptions (empty catch)", "Not closing resources", "Using exceptions for control flow"],
        edge_cases=["Error subclasses not recoverable", "Suppressed exceptions in try-with-resources", "Multi-catch with |"],
        debugging_patterns=["printStackTrace()", "getCause() for wrapped", "Check exception type before catching"],
        interview_questions=["Checked vs unchecked?", "When create custom exception?", "What is try-with-resources?"],
        practice_targets=["File reader with try-with-resources", "Custom validation exception", "Payment error hierarchy"],
        placement_relevance=["tcs", "infosys", "accenture"],
    )
    concepts["java_generics"] = concept_template(
        "java_generics", "Java Generics", "programming", "java", "generics",
        ["java_collections"], ["java_streams"],
        definition="Generics enable type-safe collections by parameterizing types at compile time. Type erasure implements on JVM.",
        mental_model="Generics are type-safe containers. Label container with type it holds. Compiler enforces matching types. Labels erased at runtime.",
        key_rules=["<T> declares type parameter", "? wildcard for unknown", "? extends T upper bounded (read)", "? super T lower bounded (write)", "Type erasure: generic info removed at runtime"],
        common_mistakes=["Creating generic arrays (T[])", "Using raw types", "Confusing ? extends and ? super", "Unchecked warnings from legacy"],
        edge_cases=["instanceof doesn't work with generics", "Bridge methods for overriding", "Generic methods can have different type params"],
        debugging_patterns=["Enable unchecked warnings", "Use diamond operator <>", "Check type erasure behavior"],
        interview_questions=["What is type erasure?", "? extends vs ? super?", "Why can't create generic arrays?"],
        practice_targets=["Generic Pair<K,V>", "Generic max() method", "Bounded wildcard for animal hierarchy"],
        placement_relevance=["tcs", "infosys", "amazon"],
    )
    concepts["java_streams"] = concept_template(
        "java_streams", "Java Streams API", "programming", "java", "libraries",
        ["java_collections", "java_generics"], ["java_lambdas"],
        definition="Streams enable functional-style operations: filter, map, reduce, collect. Intermediate ops lazy, terminal ops eager.",
        mental_model="Stream is assembly line. Items on belt. Intermediate ops (filter, map) are stations. Terminal op (collect, reduce) produces final product.",
        key_rules=["Streams are single-use", "Intermediate ops lazy", "Terminal ops trigger execution", "filter keeps matching", "map transforms each", "reduce combines into single"],
        common_mistakes=["Reusing stream after terminal", "Parallel stream on shared mutable state", "Forgetting boxed() for primitives", "Not understanding short-circuiting"],
        edge_cases=["Stream of arrays needs flatMap", "Optional prevents null in terminal", "groupingBy for multi-level grouping"],
        debugging_patterns=["peek() for debugging", "count() before collect", "Check stream source not null"],
        interview_questions=["Stream vs collection?", "Intermediate vs terminal?", "When use parallelStream()?"],
        practice_targets=["Filter and transform list", "Group employees by department", "Parallel sum with parallelStream"],
        placement_relevance=["tcs", "infosys", "amazon", "microsoft"],
    )
    concepts["java_threads"] = concept_template(
        "java_threads", "Java Threads & Concurrency", "programming", "java", "concurrency",
        ["java_basics"], ["java_concurrency"],
        definition="Java threads enable concurrent execution via Thread/Runnable. synchronized and locks ensure thread safety.",
        mental_model="Threads are workers in factory. Each has own task. Share factory floor (heap). synchronized doors ensure one worker at a time.",
        key_rules=["Thread via extends or implements Runnable", "start() begins, run() is task", "synchronized ensures mutual exclusion", "wait()/notify() for coordination", "volatile ensures visibility"],
        common_mistakes=["Calling run() instead of start()", "Synchronizing on wrong object", "Deadlock from inconsistent locking", "Not handling InterruptedException"],
        edge_cases=["Thread priority is hint", "Daemon threads exit when only daemons remain", "ThreadLocal for thread-isolated state"],
        debugging_patterns=["Print thread name with getName()", "jstack for thread dumps", "JConsole for deadlock detection"],
        interview_questions=["Thread vs Runnable?", "What is synchronized?", "What is deadlock?"],
        practice_targets=["Create and start 3 threads", "Producer-consumer with wait/notify", "Thread-safe counter with synchronized"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft"],
    )
    concepts["java_jvm"] = concept_template(
        "java_jvm", "JVM & Memory Management", "programming", "java", "runtime",
        ["java_basics"], ["java_threads"],
        definition="The JVM executes bytecode with automatic garbage collection. Understanding memory regions helps diagnose performance.",
        mental_model="JVM is container. Stack = method calls (temporary). Heap = objects (GC-managed). Method area = class metadata. GC sweeps unreachable objects.",
        key_rules=["Stack: method frames, primitive locals", "Heap: objects/arrays (GC-managed)", "Method area: class metadata", "GC reclaims unreachable", "finalize() deprecated"],
        common_mistakes=["Memory leaks from static references", "Assuming GC runs immediately", "Forgetting to null large objects", "Relying on finalize()"],
        edge_cases=["G1 GC for large heaps", "ZGC for low latency", "Soft/weak/phantom references for caching"],
        debugging_patterns=["jvisualvm for heap inspection", "Enable GC logging", "jmap for heap dump"],
        interview_questions=["JVM memory areas?", "How does GC work?", "StackOverflowError vs OutOfMemoryError?"],
        practice_targets=["Trace object allocation in heap", "Detect memory leak with VisualVM", "Compare GC algorithms"],
        placement_relevance=["amazon", "microsoft", "google"],
    )

    # Python
    concepts["python_functions"] = concept_template(
        "python_functions", "Python Functions", "programming", "python", "functions",
        ["python_basics"], ["python_control_flow", "python_oop"],
        definition="Python functions are first-class objects defined with def. Support default args, *args, **kwargs, lambdas, closures.",
        mental_model="Function is named recipe. def writes recipe. Call with ingredients (args). Returns dish. Functions are objects: pass, store, call later.",
        key_rules=["def name(params): defines", "return sends value back", "Default args evaluated at def time", "*args collects positional extras", "**kwargs collects keyword extras", "Lambda: anonymous single-expression"],
        common_mistakes=["Mutable default arguments", "Late binding in closures", "Confusing == and is", "Not returning explicit None"],
        edge_cases=["Default arg evaluated once at def time", "Closure captures variable not value", "Lambda limited to single expression"],
        debugging_patterns=["Print signature with inspect", "Check default arg mutation", "IDE breakpoints"],
        interview_questions=["*args and **kwargs?", "What is closure?", "Why mutable defaults dangerous?"],
        practice_targets=["Function with default args", "Closure returning counter", "*args/**kwargs wrapper"],
        placement_relevance=["tcs", "infosys", "wipro", "cognizant", "accenture", "google", "microsoft"],
    )
    concepts["python_control_flow"] = concept_template(
        "python_control_flow", "Python Control Flow", "programming", "python", "basics",
        ["python_basics"], ["python_functions"],
        definition="Python uses indentation-based blocks: if/elif/else, for/while, match (3.10+), and comprehensions.",
        mental_model="Indentation instead of braces. Colons start blocks. Comprehensions are compact loops building collections.",
        key_rules=["Indentation defines blocks", "if/elif/else chain", "for iterates iterable", "while loops while true", "break/continue", "List/dict/set comprehensions"],
        common_mistakes=["Mixing tabs and spaces", "Off-by-one in range()", "Modifying list while iterating", "Confusing is and =="],
        edge_cases=["Empty iterable never executes", "else on for/while (no break)", "match-case structural pattern matching (3.10+)"],
        debugging_patterns=["Print indentation level", "Use range(len()) carefully", "Check loop variable scope"],
        interview_questions=["break vs continue?", "How list comprehension works?", "match statement in 3.10?"],
        practice_targets=["FizzBuzz with if/elif", "Print triangle patterns", "List comprehension for squares"],
        placement_relevance=["tcs", "infosys", "wipro", "google", "microsoft"],
    )
    concepts["python_oop"] = concept_template(
        "python_oop", "Python OOP", "programming", "python", "paradigms",
        ["python_functions", "python_data_structures"], ["python_async"],
        definition="Python OOP uses classes with self, inheritance, property decorators, and dunder methods for operator overloading.",
        mental_model="Class is blueprint with methods. self is instance. Inheritance is is-a. Dunder methods (__str__, __lt__) let objects work with operators.",
        key_rules=["self explicit in instance methods", "__init__ is constructor", "@property for getter/setter", "super() calls parent", "Dunder methods for operators"],
        common_mistakes=["Forgetting self", "Mutable class variables", "Not calling super().__init__()", "Confusing instance vs class attributes"],
        edge_cases=["Class attributes shared", "Multiple inheritance MRO", "__slots__ prevents __dict__"],
        debugging_patterns=["Print self.__dict__", "isinstance() for type checks", "Check MRO with Class.__mro__"],
        interview_questions=["What is self?", "Class vs instance variables?", "How does inheritance work?"],
        practice_targets=["BankAccount class", "Override __str__ and __lt__", "Animal/Cat/Dog inheritance"],
        placement_relevance=["tcs", "infosys", "wipro", "google", "microsoft", "amazon"],
    )
    concepts["python_async"] = concept_template(
        "python_async", "Python Async Programming", "programming", "python", "concurrency",
        ["python_functions"], ["python_testing"],
        definition="asyncio enables async programming with coroutines (async def), await, event loop, and tasks for concurrent I/O-bound work.",
        mental_model="Async is single waiter managing multiple orders. While waiting for one I/O, start next. asyncio is waiter. async def is order ticket.",
        key_rules=["async def defines coroutine", "await suspends until ready", "Event loop runs coroutines", "asyncio.gather runs concurrently", "Never block loop with time.sleep()"],
        common_mistakes=["time.sleep() instead of asyncio.sleep()", "Forgetting await", "Blocking I/O in async", "Too many concurrent tasks"],
        edge_cases=["Asyncio is single-threaded", "CPU-bound needs process pool", "Cancellation with CancelledError"],
        debugging_patterns=["asyncio.run() as entry", "Check unawaited coroutine warnings", "aioconsole for debugging"],
        interview_questions=["What is asyncio?", "Threading vs asyncio?", "What if you forget await?"],
        practice_targets=["Fetch URLs concurrently with aiohttp", "Async task queue", "Async chat server"],
        placement_relevance=["amazon", "microsoft", "google"],
    )
    concepts["python_testing"] = concept_template(
        "python_testing", "Python Testing", "programming", "python", "testing",
        ["python_functions"], ["python_oop"],
        definition="Python testing uses unittest (built-in), pytest (preferred), and doctest. TDD writes tests before code.",
        mental_model="Testing is safety net. unittest is built-in net. pytest is better net. Each test is proof code works.",
        key_rules=["pytest: test_* functions or TestCase classes", "assert for assertions", "@pytest.fixture for setup", "conftest.py for shared fixtures", "pytest-cov for coverage"],
        common_mistakes=["Not testing edge cases", "Tests depending on order", "Hardcoded values instead of fixtures", "Ignoring failing tests"],
        edge_cases=["Parametrize for multiple cases", "Monkeypatch for mocking", "pytest.raises for exceptions"],
        debugging_patterns=["pytest -v verbose", "--pdb to debug on failure", "Check fixture scopes"],
        interview_questions=["unittest vs pytest?", "What are fixtures?", "How test function that raises exception?"],
        practice_targets=["Write pytest tests for calculator", "Fixtures for database setup", "Parametrize for multiple inputs"],
        placement_relevance=["tcs", "infosys", "amazon", "microsoft"],
    )

    # JavaScript
    concepts["javascript_functions"] = concept_template(
        "javascript_functions", "JavaScript Functions", "programming", "javascript", "functions",
        ["javascript_basics"], ["javascript_async", "javascript_objects"],
        definition="JavaScript functions are first-class objects. Support declarations, expressions, arrow functions, closures, higher-order functions.",
        mental_model="JS function is a value you can call. Store in variables, pass around, return from functions. Arrow functions shorthand. Closures remember creation environment.",
        key_rules=["Declaration hoisted, expression not", "Arrow: () => {}", "Closure: inner remembers outer scope", "this depends on call-site", "Higher-order: takes/returns functions"],
        common_mistakes=["Confusing this in arrow vs regular", "Closure in loops (classic i)", "Expecting hoisting for expressions", "Missing return in arrow with braces"],
        edge_cases=["Arrow has no own this/bind/arguments", "IIFE for immediate execution", "Function.name property (inference)"],
        debugging_patterns=["console.log(this)", "DevTools debugger", "Check closure with scope inspection"],
        interview_questions=["What is closure?", "Declaration vs expression?", "How does this work?"],
        practice_targets=["Counter with closure", "Debounce with setTimeout", "Higher-order map function"],
        placement_relevance=["google", "microsoft", "amazon", "flipkart", "zomato"],
    )
    concepts["javascript_objects"] = concept_template(
        "javascript_objects", "JavaScript Objects & Prototypes", "programming", "javascript", "objects",
        ["javascript_basics"], ["javascript_functions", "javascript_dom"],
        definition="JavaScript objects are key-value collections. Prototypes enable inheritance via prototype chain.",
        mental_model="JS object is dictionary. When key not found, check prototype (parent dictionary). class is syntactic sugar over prototype.",
        key_rules=["Objects: {key: value}", "Prototype chain for inheritance", "Object.create() sets prototype", "class is sugar over prototype", "this = calling object"],
        common_mistakes=["object.keys() vs for-in", "Modifying prototype in loops", "Not checking hasOwnProperty", "Expecting class like other languages"],
        edge_cases=["__proto__ vs getPrototypeOf", "Symbol not in for-in", "defineProperty for fine control"],
        debugging_patterns=["console.dir for inspection", "Check prototype with __proto__", "instanceof for prototype check"],
        interview_questions=["What is prototype chain?", "Object.create() vs class?", "How does inheritance work?"],
        practice_targets=["Object with prototype chain", "Inheritance with Object.create()", "Class with class syntax"],
        placement_relevance=["google", "microsoft", "amazon"],
    )
    concepts["javascript_dom"] = concept_template(
        "javascript_dom", "JavaScript DOM Manipulation", "programming", "javascript", "dom",
        ["javascript_basics", "html_css"], ["javascript_async"],
        definition="The DOM represents HTML as a tree of nodes. JavaScript manipulates via selectors, event listeners, property updates.",
        mental_model="DOM is family tree of HTML elements. getElementById finds by ID. querySelector uses CSS selectors. Event listeners are doorbells.",
        key_rules=["getElementById() by ID", "querySelector() CSS selectors", "addEventListener(type, handler)", "textContent changes text safely", "classList for classes"],
        common_mistakes=["innerHTML with untrusted input (XSS)", "Not removing listeners (leak)", "Querying before DOM loads", "textContent vs innerHTML"],
        edge_cases=["Event bubbling vs capturing", "Event delegation for dynamic", "DOMContentLoaded vs load"],
        debugging_patterns=["DevTools Elements panel", "console.log(event.target)", "Break on subtree modifications"],
        interview_questions=["What is DOM?", "Add event listener?", "Bubbling vs capturing?"],
        practice_targets=["Todo list with add/remove/toggle", "Modal with listeners", "Form validation on submit"],
        placement_relevance=["google", "microsoft", "amazon", "flipkart", "zomato"],
    )
    concepts["javascript_async"] = concept_template(
        "javascript_async", "JavaScript Async Programming", "programming", "javascript", "async",
        ["javascript_functions"], ["javascript_dom"],
        definition="JavaScript async uses callbacks, Promises, async/await for non-blocking I/O. Event loop manages call stack and task queue.",
        mental_model="JS is single chef (event loop). Orders queued. While waiting for oven (I/O), start next order. Promises are order tickets. async/await is synchronous recipe writing.",
        key_rules=["Promises: pending -> fulfilled/rejected", "async returns Promise", "await suspends until resolved", "try/catch or .catch() for errors", "Promise.all waits all, Promise.race first"],
        common_mistakes=["Forgetting await", "Not handling rejections", "async/await in sync loops (need Promise.all)", "Confusing setTimeout guarantees"],
        edge_cases=["Unhandled rejection warning", "Microtasks vs macrotasks", "Resolution is async even for resolved"],
        debugging_patterns=["Async stack traces in Chrome", "Log Promise states", "Check unhandled rejections"],
        interview_questions=["What is event loop?", "Promise.all vs Promise.race?", "How async/await work?"],
        practice_targets=["Fetch with async/await", "Retry with Promise", "Parallel calls with Promise.all"],
        placement_relevance=["google", "microsoft", "amazon", "flipkart"],
    )
    concepts["javascript_es6"] = concept_template(
        "javascript_es6", "JavaScript ES6+ Features", "programming", "javascript", "language",
        ["javascript_basics"], ["javascript_functions", "javascript_async"],
        definition="ES6+ added let/const, arrow functions, template literals, destructuring, spread/rest, modules, classes.",
        mental_model="ES6+ is JS growing up. let/const fix scoping. Arrow functions simplify callbacks. Destructuring unpacks. Modules organize. Classes make OOP familiar.",
        key_rules=["let/const block-scoped (avoid var)", "Arrow: () => {}", "Template literals: `Hello ${name}`", "Destructuring: const {a, b} = obj", "Spread: ...array, Rest: ...args", "import/export modules"],
        common_mistakes=["Using var", "Confusing arrow this", "Not understanding destructuring", "Overusing spread"],
        edge_cases=["const prevents reassignment not mutation", "Default params at call time", "Symbol not in for-in"],
        debugging_patterns=["Check scope with let/const", "Babel for older browsers", "Verify module syntax"],
        interview_questions=["let vs const vs var?", "Arrow functions and this?", "What is destructuring?"],
        practice_targets=["Convert var to let/const", "Destructure function params", "Module with import/export"],
        placement_relevance=["google", "microsoft", "amazon", "flipkart", "zomato"],
    )

    # DSA
    concepts["dsa_strings"] = concept_template(
        "dsa_strings", "String Algorithms", "cs", "dsa", "algorithms",
        ["dsa_arrays"], ["dsa_two_pointers", "dsa_dp"],
        definition="String algorithms: pattern matching, searching, manipulation. Techniques: sliding window, KMP, Z-algorithm, rolling hash.",
        mental_model="Strings are character arrays with extra tricks. Rolling hash for O(1) substring compare. KMP avoids redundant compares. Sliding window for subarrays.",
        key_rules=["String compare O(n) worst case", "Rolling hash O(1) substring compare", "KMP precomputes LPS for O(n) search", "Sliding window O(n)", "Frequency arrays O(1) space for alphabet"],
        common_mistakes=["Naive O(n*m) search", "Not handling empty strings", "Confusing index vs length", "Off-by-one in window"],
        edge_cases=["Empty string", "Single char", "All same chars", "Unicode/multibyte"],
        debugging_patterns=["Print LPS array for KMP", "Trace sliding window indices", "Python slicing for verification"],
        interview_questions=["What is KMP?", "Find all anagrams in string?", "Substring search complexity?"],
        practice_targets=["Implement strStr() with KMP", "Longest substring without repeats", "Minimum window substring"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft", "google"],
    )
    concepts["dsa_recursion"] = concept_template(
        "dsa_recursion", "Recursion & Backtracking", "cs", "dsa", "algorithms",
        ["dsa_arrays"], ["dsa_linked_lists", "dsa_trees", "dsa_backtracking"],
        definition="Recursion solves problems by calling same function on smaller subproblems. Backtracking explores choices, undoing when path fails.",
        mental_model="Recursion is Russian dolls. Open biggest (problem), inside is smaller (subproblem). Keep opening until smallest (base case). Close back up combining solutions.",
        key_rules=["Base case stops recursion", "Recursive case reduces problem size", "Call stack stores state", "Backtracking: choose, explore, unchoose", "Memoization caches repeated subproblems"],
        common_mistakes=["Missing/wrong base case", "Not combining subproblem results", "Stack overflow deep recursion", "Recomputing same subproblem"],
        edge_cases=["Empty input base case", "Single element base case", "Very deep recursion"],
        debugging_patterns=["Trace call stack manually", "Print depth parameter", "Recursion visualizer"],
        interview_questions=["What is recursion?", "What is backtracking?", "Convert recursion to iteration?"],
        practice_targets=["Binary search recursively", "Tower of Hanoi", "Generate all subsets"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft", "google"],
    )
    concepts["dsa_stacks"] = concept_template(
        "dsa_stacks", "Stacks & Queues", "cs", "dsa", "data_structures",
        ["dsa_linked_lists"], ["dsa_queues", "dsa_trees"],
        definition="Stack: LIFO with push/pop. Queue: FIFO with enqueue/dequeue. Array-based or linked-list-based.",
        mental_model="Stack is stack of plates (last on, first off). Queue is ticket line (first in, first served).",
        key_rules=["Stack: push/pop/peek O(1)", "Queue: enqueue/dequeue O(1) with linked list", "Circular queue prevents waste", "Stack: LIFO, Queue: FIFO"],
        common_mistakes=["Confusing stack/queue ops", "Off-by-one in circular queue", "Not checking empty before pop", "Using array queue (O(n) dequeue)"],
        edge_cases=["Empty stack/queue", "Single element", "Full circular queue overflow"],
        debugging_patterns=["Print stack top-to-bottom", "Trace queue front/rear", "Array visualization"],
        interview_questions=["Queue using two stacks?", "Stack vs queue?", "When use deque?"],
        practice_targets=["Stack with linked list", "Queue with two stacks", "Valid parentheses with stack"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft"],
    )
    concepts["dsa_queues"] = concept_template(
        "dsa_queues", "Queues & Deques", "cs", "dsa", "data_structures",
        ["dsa_stacks"], ["dsa_graphs"],
        definition="Queues maintain FIFO. Deques allow insertion/deletion at both ends. Priority queues order by priority.",
        mental_model="Queue is line. Deque is line where you can join/leave either end. Priority queue is emergency room - sickest first regardless of arrival.",
        key_rules=["Queue: FIFO", "Deque: both ends", "Priority queue: min/max at top", "Queue with linked list: O(1) all ops", "Priority queue: O(log n) insert, O(1) peek"],
        common_mistakes=["Array-based queue (O(n) dequeue)", "Confusing priority ordering", "Not handling empty deque", "Wrong comparator"],
        edge_cases=["Empty queue/deque", "Single element (front=rear)", "Priority tie-breaking"],
        debugging_patterns=["Print front/rear indices", "Check size after ops", "Verify priority ordering"],
        interview_questions=["Queue using array?", "What is deque?", "Data structure for priority queue?"],
        practice_targets=["Queue with circular array", "Sliding window max with deque", "Task scheduler with priority queue"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon"],
    )
    concepts["dsa_bst"] = concept_template(
        "dsa_bst", "Binary Search Trees", "cs", "dsa", "data_structures",
        ["dsa_trees"], ["dsa_heaps"],
        definition="BST maintains invariant: left < parent < right. Balanced BSTs (AVL, Red-Black) guarantee O(log n) operations.",
        mental_model="BST is sorted phone book that stays sorted. Find: open middle, go left/right, repeat. Inorder = sorted order.",
        key_rules=["Left < parent < right", "Inorder = sorted", "Search/insert/delete: O(h)", "Balanced: h = O(log n)", "AVL height-balanced, Red-Black color-balanced"],
        common_mistakes=["Missing base case (infinite recursion)", "Not combining subproblem results", "Confusing traversal orders", "Not rebalancing after insert/delete"],
        edge_cases=["Empty tree: null root", "Single node", "Skewed tree (degenerates)", "Duplicate keys (usually not allowed)"],
        debugging_patterns=["Trace recursion with stack diagram", "Print inorder to verify sorted", "Small test cases (2-3 nodes)"],
        interview_questions=["Validate BST?", "Search time in balanced BST?", "Find lowest common ancestor?"],
        practice_targets=["BST insert and search", "Inorder traversal", "Validate binary tree is BST"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft", "google"],
    )
    concepts["dsa_heaps"] = concept_template(
        "dsa_heaps", "Heaps & Priority Queues", "cs", "dsa", "data_structures",
        ["dsa_arrays"], ["dsa_trees"],
        definition="Heap is complete binary tree with heap property: max-heap (parent >= children) or min-heap (parent <= children). Implemented as array.",
        mental_model="Heap is priority queue in tree. Most important always at top. Complete (filled left-to-right) so fits in array perfectly.",
        key_rules=["Complete binary tree", "Max-heap: parent >= children", "Min-heap: parent <= children", "Array: parent=i, left=2i+1, right=2i+2", "Insert/poll: O(log n)"],
        common_mistakes=["Confusing heap with sorted array", "Wrong child index calculation", "Not heapifying after insert/delete", "Using heap for full sorting"],
        edge_cases=["Single element heap", "All equal elements", "Extract from empty heap"],
        debugging_patterns=["Print array representation", "Verify heap property after ops", "Use heapq/PriorityQueue"],
        interview_questions=["What is heap used for?", "Find kth largest?", "Heap operation complexities?"],
        practice_targets=["Implement min-heap", "Kth largest with heap", "Merge k sorted lists"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft", "google"],
    )
    concepts["dsa_bfs"] = concept_template(
        "dsa_bfs", "Breadth-First Search", "cs", "dsa", "algorithms",
        ["dsa_graphs"], ["dsa_shortest_path"],
        definition="BFS explores graph level by level using queue. Finds shortest paths in unweighted graphs.",
        mental_model="BFS is ripple in water. Spreads equally in all directions. First to reach destination is shortest path.",
        key_rules=["Uses queue (FIFO)", "Explores level by level", "Shortest path in unweighted graph", "Mark visited to avoid cycles", "O(V + E) time"],
        common_mistakes=["Using DFS for shortest path", "Not marking visited in undirected graphs", "Confusing BFS tree with shortest path tree", "Not handling disconnected components"],
        edge_cases=["Single node graph", "Disconnected graph", "Self-loops"],
        debugging_patterns=["Print queue at each level", "Trace parent pointers", "Count visited nodes"],
        interview_questions=["When use BFS vs DFS?", "How find shortest path?", "Time complexity of BFS?"],
        practice_targets=["BFS on grid (number of islands)", "Shortest path in maze", "Level-order traversal of tree"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft", "google"],
    )
    concepts["dsa_dfs"] = concept_template(
        "dsa_dfs", "Depth-First Search", "cs", "dsa", "algorithms",
        ["dsa_graphs"], ["dsa_backtracking"],
        definition="DFS explores as far as possible along each branch before backtracking. Used for cycle detection, topological sort, connected components.",
        mental_model="DFS is exploring a maze. Go left until wall, backtrack, try right. Stack tracks path. Mark visited to avoid loops.",
        key_rules=["Uses stack (explicit or recursion)", "Explores deeply before broadly", "Mark visited to avoid cycles", "O(V + E) time", "Recursive or iterative implementation"],
        common_mistakes=["Not marking visited (infinite loop)", "Confusing DFS tree with actual graph", "Stack overflow for deep recursion", "Not handling disconnected components"],
        edge_cases=["Single node", "Disconnected graph", "Self-loops and parallel edges"],
        debugging_patterns=["Print recursion stack", "Trace visited set", "Use iterative to avoid stack overflow"],
        interview_questions=["When use BFS vs DFS?", "How detect cycle with DFS?", "What is topological sort?"],
        practice_targets=["DFS for connected components", "Detect cycle in directed graph", "All paths from source to target"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft", "google"],
    )
    concepts["dsa_shortest_path"] = concept_template(
        "dsa_shortest_path", "Shortest Path Algorithms", "cs", "dsa", "algorithms",
        ["dsa_bfs", "dsa_graphs"], ["dsa_dp"],
        definition="Shortest path algorithms find minimum-cost paths: BFS (unweighted), Dijkstra (non-negative), Bellman-Ford (negative weights), Floyd-Warshall (all pairs).",
        mental_model="Shortest path is GPS navigation. BFS is counting blocks (unweighted). Dijkstra is GPS with distances (non-negative). Bellman-Ford handles negative roads (but detects negative cycles).",
        key_rules=["BFS: unweighted, O(V + E)", "Dijkstra: non-negative weights, O((V + E) log V) with heap", "Bellman-Ford: negative weights, O(VE)", "Floyd-Warshall: all pairs, O(V^3)", "Negative cycle: no shortest path exists"],
        common_mistakes=["Using Dijkstra with negative weights", "Not handling disconnected nodes", "Confusing shortest path tree with actual paths", "Forgetting to initialize distances to infinity"],
        edge_cases=["Negative weight edges", "Negative cycles", "Disconnected graph (infinity)"],
        debugging_patterns=["Print distance array after each iteration", "Verify relaxation step", "Check for negative cycles"],
        interview_questions=["When use Dijkstra vs Bellman-Ford?", "How detect negative cycle?", "Time complexity of Dijkstra with heap?"],
        practice_targets=["Dijkstra on weighted graph", "Network delay time (LeetCode 743)", "Cheapest flights with Bellman-Ford"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft", "google"],
    )
    concepts["dsa_backtracking"] = concept_template(
        "dsa_backtracking", "Backtracking Algorithms", "cs", "dsa", "algorithms",
        ["dsa_recursion"], ["dsa_dp"],
        definition="Backtracking explores all possible solutions recursively, abandoning paths that violate constraints. Used for permutation, combination, subset problems.",
        mental_model="Backtracking is trying all paths in a maze. When you hit a dead end, backtrack to last choice point and try different path. Abandon paths that can't lead to solution.",
        key_rules=["Choose, explore, unchoose pattern", "Prune invalid paths early", "Base case: solution found or no more choices", "Time: O(b^d) where b=branching, d=depth", "Space: O(d) for recursion stack"],
        common_mistakes=["Not unchoosing (backtracking) after recursion", "Not pruning early enough", "Generating duplicates without deduplication", "Wrong base case"],
        edge_cases=["Empty input", "Single element", "All elements same (deduplication needed)"],
        debugging_patterns=["Print current path/choices", "Trace recursion tree", "Count recursive calls"],
        interview_questions=["What is backtracking?", "When use backtracking vs DP?", "Generate all permutations of string?"],
        practice_targets=["Generate all subsets", "N-Queens problem", "Generate permutations"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft", "google"],
    )
    concepts["dsa_tries"] = concept_template(
        "dsa_tries", "Tries (Prefix Trees)", "cs", "dsa", "data_structures",
        ["dsa_trees"], ["dsa_strings"],
        definition="A trie stores strings by shared prefixes. Each node represents a character. Efficient for prefix-based operations: autocomplete, spell check.",
        mental_model="Trie is organized filing cabinet. Each drawer is a letter. Inside are sub-drawers for next letters. 'cat' and 'car' share 'ca' drawer. Fast prefix lookup.",
        key_rules=["Each node has children for next chars", "Root is empty string", "End-of-word marker (boolean)", "Insert/search/delete: O(L) where L = word length", "Space: O(N * L) for N words of avg length L"],
        common_mistakes=["Not marking end-of-word", "Confusing node count with string count", "Not handling empty string", "Memory bloat from many nodes"],
        edge_cases=["Empty string (root is end-of-word)", "Common prefixes (shared nodes)", "Delete word that's prefix of another"],
        debugging_patterns=["Print trie level by level", "Trace path for word", "Count nodes vs words"],
        interview_questions=["What is a trie and when use it?", "Time complexity of insert/search?", "How implement autocomplete?"],
        practice_targets=["Implement trie insert/search", "Autocomplete with trie", "Word search in 2D board"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft", "google"],
    )
    concepts["dsa_greedy"] = concept_template(
        "dsa_greedy", "Greedy Algorithms", "cs", "dsa", "algorithms",
        ["dsa_arrays"], ["dsa_dp", "dsa_intervals"],
        definition="Greedy algorithms make locally optimal choices at each step, hoping for global optimum. Works when problem has greedy-choice property.",
        mental_model="Greedy is always taking the best immediate option. Like always picking the biggest bill when making change (if denominations allow). Fast but not always correct.",
        key_rules=["Make locally optimal choice at each step", "Works if problem has greedy-choice property", "Often O(n log n) due to sorting", "Proof by exchange argument or matroid theory", "If in doubt, compare with DP"],
        common_mistakes=["Applying greedy when problem needs DP", "Not proving greedy-choice property", "Wrong ordering (sort by wrong key)", "Greedy works for examples but not all cases"],
        edge_cases=["Tie-breaking when multiple optimal choices", "Problems that look greedy but aren't (knapsack)", "When greedy fails but DP works"],
        debugging_patterns=["Test with counterexample", "Compare greedy result with DP brute force", "Verify greedy-choice property"],
        interview_questions=["What is a greedy algorithm?", "When does greedy work?", "Example where greedy fails?"],
        practice_targets=["Activity selection problem", "Coin change with canonical denominations", "Jump game (can reach end)"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft", "google"],
    )
    concepts["dsa_intervals"] = concept_template(
        "dsa_intervals", "Interval Scheduling & Merging", "cs", "dsa", "algorithms",
        ["dsa_arrays"], ["dsa_greedy"],
        definition="Interval problems involve ranges [start, end]. Key operations: merge overlapping, find gaps, schedule non-overlapping, insert new interval.",
        mental_model="Intervals are time slots on a calendar. Merge overlapping meetings. Find free slots between meetings. Schedule max non-overlapping meetings (earliest finish first).",
        key_rules=["Sort by start time for merging", "Sort by end time for scheduling (greedy)", "Overlap: a.start < b.end AND b.start < a.end", "Merge: [min(start), max(end)]", "Insert: find position, merge if needed"],
        common_mistakes=["Not sorting before merging", "Wrong overlap condition", "Inclusive vs exclusive endpoints", "Not handling edge-touching intervals"],
        edge_cases=["Adjacent intervals [1,2] and [2,3]", "Interval contained within another", "Single interval", "No overlaps"],
        debugging_patterns=["Draw intervals on timeline", "Check overlap condition manually", "Sort and step through"],
        interview_questions=["How merge overlapping intervals?", "How find max non-overlapping intervals?", "Insert and merge interval?"],
        practice_targets=["Merge intervals", "Insert new interval and merge", "Meeting rooms (min rooms needed)"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft", "google"],
    )
    concepts["dsa_sorting"] = concept_template(
        "dsa_sorting", "Sorting Algorithms", "cs", "dsa", "algorithms",
        ["dsa_arrays"], ["dsa_recursion"],
        definition="Sorting arranges elements in order. Key algorithms: bubble, selection, insertion, merge, quick, heap, counting, radix, bucket.",
        mental_model="Sorting is organizing a messy bookshelf. Bubble sort swaps adjacent books repeatedly (slow). Merge sort splits into piles, sorts each, merges (fast). Quick sort picks pivot, partitions, recurses.",
        key_rules=["Comparison sort lower bound: O(n log n)", "Merge sort: guaranteed O(n log n), stable, O(n) space", "Quick sort: average O(n log n), worst O(n^2), in-place", "Heap sort: O(n log n), in-place, not stable", "Counting/radix: O(n) for integer keys"],
        common_mistakes=["Using bubble/selection/insertion for large data", "Not handling duplicates in quicksort (Lomuto vs Hoare)", "Confusing stable vs unstable", "Off-by-one in partition"],
        edge_cases=["All elements equal", "Already sorted (worst for naive quicksort)", "Reverse sorted", "Single element"],
        debugging_patterns=["Trace partition step by step", "Print array after each pass", "Compare with Python sorted()"],
        interview_questions=["When use merge sort vs quick sort?", "What is stable sorting?", "Time complexity of heap sort?"],
        practice_targets=["Implement quicksort", "Implement merge sort", "Sort colors (Dutch national flag)"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft", "google"],
    )

    # CS / DBMS / OS / Networking / Git / Docker
    concepts["dbms_normalization"] = concept_template(
        "dbms_normalization", "Database Normalization", "databases", "sql", "databases",
        ["dbms_sql"], ["dbms_indexing", "dbms_transactions"],
        definition="Normalization organizes tables to reduce redundancy and update anomalies. Normal forms: 1NF, 2NF, 3NF, BCNF.",
        mental_model="Normalization is organizing a filing cabinet. 1NF: each field has one value. 2NF: no partial dependency on part of key. 3NF: no transitive dependency on non-key. BCNF: every determinant is a candidate key.",
        key_rules=["1NF: atomic values, no repeating groups", "2NF: 1NF + no partial dependency", "3NF: 2NF + no transitive dependency", "BCNF: stricter 3NF (every determinant is key)", "Denormalization trades redundancy for performance"],
        common_mistakes=["Stopping at 1NF or 2NF", "Over-normalizing (too many joins)", "Not understanding transitive dependency", "Confusing functional dependency with foreign key"],
        edge_cases=["Multi-valued dependencies (4NF)", "Join dependencies (5NF)", "Practical denormalization for reporting"],
        debugging_patterns=["Draw dependency diagram", "Check each normal form in order", "Verify no redundant data"],
        interview_questions=["What is normalization and why?", "Explain 1NF, 2NF, 3NF with example?", "When would you denormalize?"],
        practice_targets=["Normalize unnormalized table to 3NF", "Identify functional dependencies", "Design schema for e-commerce"],
        placement_relevance=["tcs", "infosys", "wipro", "cognizant"],
    )
    concepts["dbms_indexing"] = concept_template(
        "dbms_indexing", "Database Indexing", "databases", "sql", "databases",
        ["dbms_sql"], ["dbms_normalization"],
        definition="Indexes accelerate data retrieval. Types: B-tree (default), hash (equality), composite (multi-column), covering (includes all needed columns).",
        mental_model="Index is book's table of contents. Without it, read every page (full scan). With it, jump to section. B-tree is balanced tree. Hash is direct lookup. Composite indexes need leftmost prefix.",
        key_rules=["B-tree: O(log n) range and equality", "Hash: O(1) equality only", "Composite: leftmost prefix rule", "Index speeds SELECT, slows INSERT/UPDATE/DELETE", "Covering index avoids table access"],
        common_mistakes=["Indexing every column (write penalty)", "Not using composite indexes", "Forgetting leftmost prefix rule", "Index on low-cardinality column (gender)"],
        edge_cases=["Index on NULL values (usually not indexed)", "Function on column prevents index use", "Index merge for multiple indexes"],
        debugging_patterns=["Run EXPLAIN to see index usage", "Check index selectivity", "Verify leftmost prefix"],
        interview_questions=["What is an index and how does it work?", "When would you NOT use an index?", "What is the leftmost prefix rule?"],
        practice_targets=["Design index for query", "Analyze EXPLAIN plan", "Composite index for multi-column filter"],
        placement_relevance=["tcs", "infosys", "wipro", "cognizant", "amazon"],
    )
    concepts["dbms_transactions"] = concept_template(
        "dbms_transactions", "Database Transactions & ACID", "databases", "sql", "databases",
        ["dbms_sql"], ["dbms_indexing"],
        definition="Transactions are atomic units of work. ACID: Atomicity, Consistency, Isolation, Durability. Isolation levels: READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE.",
        mental_model="Transaction is a protected box. Either everything inside succeeds and becomes visible (commit), or nothing does (rollback). ACID ensures this promise even with concurrent users.",
        key_rules=["Atomicity: all or nothing", "Consistency: valid state before/after", "Isolation: concurrent transactions don't interfere", "Durability: committed changes survive crashes", "Isolation levels trade safety for performance"],
        common_mistakes=["Not handling deadlocks", "Long transactions holding locks", "Assuming isolation level is SERIALIZABLE", "Not committing/rolling back explicitly"],
        edge_cases=["Dirty reads (READ UNCOMMITTED)", "Non-repeatable reads (READ COMMITTED)", "Phantom reads (REPEATABLE READ)", "Serialization anomalies (SERIALIZABLE)"],
        debugging_patterns=["Check isolation level", "Monitor lock waits", "Use transaction logs for recovery"],
        interview_questions=["What is ACID?", "Explain isolation levels?", "What is a deadlock and how prevent it?"],
        practice_targets=["Design transaction for bank transfer", "Demonstrate dirty read", "Deadlock detection and resolution"],
        placement_relevance=["tcs", "infosys", "wipro", "cognizant", "amazon"],
    )
    concepts["os_memory"] = concept_template(
        "os_memory", "Operating Systems: Memory Management", "cs", "os", "operating_systems",
        ["os_processes"], ["os_concurrency"],
        definition="OS memory management handles allocation/deallocation, virtual memory, paging, segmentation, and page replacement algorithms.",
        mental_model="Memory is a large warehouse. Virtual memory lets each process think it has the whole warehouse. Paging divides into fixed-size pages. Page replacement decides what stays in fast cache.",
        key_rules=["Virtual memory: each process has own address space", "Paging: fixed-size pages (4KB typical)", "Page table maps virtual to physical", "TLB accelerates page table lookup", "Page replacement: LRU, FIFO, Optimal"],
        common_mistakes=["Confusing virtual and physical addresses", "Not understanding page fault cost", "Assuming all memory is RAM", "Forgetting TLB in performance analysis"],
        edge_cases=["Thrashing: constant page faults", "Page fault handler runs in kernel mode", "Shared pages between processes"],
        debugging_patterns=["Check page fault rate", "Use /proc/meminfo on Linux", "Monitor TLB miss rate"],
        interview_questions=["What is virtual memory?", "What is a page fault?", "Explain paging vs segmentation?"],
        practice_targets=["Simulate LRU page replacement", "Calculate effective memory access time", "Design virtual memory system"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft"],
    )
    concepts["os_concurrency"] = concept_template(
        "os_concurrency", "Operating Systems: Concurrency", "cs", "os", "operating_systems",
        ["os_processes", "os_memory"], [],
        definition="Concurrency manages multiple executing processes/threads. Synchronization primitives: mutex, semaphore, monitor, condition variable.",
        mental_model="Concurrency is multiple workers sharing tools. Mutex is a lock on a tool (only one worker at a time). Semaphore is a pool of identical tools (N workers). Deadlock is when each worker holds a tool the other needs.",
        key_rules=["Mutex: binary semaphore, ownership", "Semaphore: counting, no ownership", "Deadlock: mutual exclusion, hold-and-wait, no preemption, circular wait", "Prevention: break one condition", "Avoidance: Banker's algorithm"],
        common_mistakes=["Forgetting to lock shared resources", "Creating too many threads", "Deadlock from inconsistent lock ordering", "Race conditions from unsynchronized access"],
        edge_cases=["Priority inversion", "Starvation in scheduling", "Spurious wakeups with condition variables"],
        debugging_patterns=["Thread sanitizers (TSAN)", "Log thread IDs with timestamps", "Stress test for race conditions"],
        interview_questions=["What is race condition?", "How prevent deadlock?", "Mutex vs semaphore?"],
        practice_targets=["Thread-safe counter with mutex", "Producer-consumer with bounded buffer", "Detect deadlock in resource graph"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft"],
    )
    concepts["networking_tcp"] = concept_template(
        "networking_tcp", "TCP Protocol", "cs", "networking", "protocols",
        ["networking_basics"], ["networking_http"],
        definition="TCP is connection-oriented, reliable, ordered delivery. Uses three-way handshake, sliding window, congestion control.",
        mental_model="TCP is registered mail. Guaranteed delivery, order preserved. Handshake confirms both sides ready. Sliding window controls flow. Congestion control prevents post office overload.",
        key_rules=["Three-way handshake: SYN, SYN-ACK, ACK", "Sliding window for flow control", "Congestion control: slow start, congestion avoidance", "TCP is full-duplex", "Connection-oriented: setup and teardown"],
        common_mistakes=["Confusing TCP with UDP", "Not handling connection timeouts", "Assuming TCP preserves message boundaries", "Ignoring Nagle's algorithm impact"],
        edge_cases=["Half-open connections", "TIME_WAIT state (2MSL)", "Packet reordering", "Congestion collapse"],
        debugging_patterns=["Use tcpdump/Wireshark", "Check netstat for connections", "Monitor retransmission rate"],
        interview_questions=["What is difference between TCP and UDP?", "Explain three-way handshake?", "What is sliding window?"],
        practice_targets=["Implement TCP echo server", "Analyze Wireshark capture", "Simulate sliding window"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft"],
    )
    concepts["networking_http"] = concept_template(
        "networking_http", "HTTP Protocol", "cs", "networking", "protocols",
        ["networking_tcp"], ["networking_rest", "web_auth"],
        definition="HTTP is request-response protocol. Methods: GET, POST, PUT, DELETE, PATCH. Status codes: 1xx, 2xx, 3xx, 4xx, 5xx. HTTPS adds TLS.",
        mental_model="HTTP is ordering at a restaurant. You send order (request) with method (GET=look at menu, POST=place order). Kitchen sends back dish (response) with status (200=ready, 404=not found).",
        key_rules=["GET: retrieve, POST: create, PUT: replace, DELETE: remove", "2xx success, 3xx redirect, 4xx client error, 5xx server error", "HTTPS = HTTP + TLS encryption", "Stateless: each request independent", "Headers carry metadata"],
        common_mistakes=["Using GET for mutations (should be POST/PUT)", "Not handling error status codes", "Assuming HTTP is secure (use HTTPS)", "Confusing 401 and 403"],
        edge_cases=["CORS preflight (OPTIONS)", "HTTP/2 multiplexing", "WebSocket upgrade from HTTP"],
        debugging_patterns=["curl -v to inspect", "Browser DevTools Network tab", "Check status codes and headers"],
        interview_questions=["HTTP methods and when to use each?", "What is REST?", "Difference between 401 and 403?"],
        practice_targets=["Build REST API with proper methods", "Handle CORS preflight", "Implement authentication headers"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft"],
    )
    concepts["networking_rest"] = concept_template(
        "networking_rest", "REST API Design", "cs", "networking", "architecture",
        ["networking_http"], ["web_auth", "system_design_basics"],
        definition="REST is architectural style for networked applications. Resources identified by URIs, manipulated via HTTP methods, represented in JSON.",
        mental_model="REST is a filing system. Each document is a resource (URI). GET reads. POST creates new. PUT updates. DELETE removes. JSON is the document format.",
        key_rules=["Resources identified by URIs", "HTTP methods for operations", "Stateless: each request self-contained", "JSON or XML representation", "Versioning: /v1/, /v2/ or headers"],
        common_mistakes=["Using verbs in URIs (/getUser, /createUser)", "Not versioning API", "Returning 200 with error in body", "Ignoring HTTP status codes"],
        edge_cases=["Partial updates (PATCH vs PUT)", "Nested resources (/users/1/orders)", "Rate limiting and pagination"],
        debugging_patterns=["curl to test endpoints", "Postman for API testing", "Check status codes match semantics"],
        interview_questions=["What is REST?", "When use POST vs PUT?", "How version REST API?"],
        practice_targets=["Design todo API with REST", "Implement pagination", "Add authentication to REST endpoints"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft"],
    )
    concepts["git_branching"] = concept_template(
        "git_branching", "Git Branching & Merging", "devops", "git", "version_control",
        ["git_basics"], ["git_collaboration"],
        definition="Git branches enable parallel development. Merge combines branches. Rebase replays commits. Both have trade-offs.",
        mental_model="Branches are parallel timelines. Merge is joining timelines (preserves both histories). Rebase is rewriting timeline to be linear (cleaner but rewrites history).",
        key_rules=["Branch = movable pointer to commit", "Merge: two-parent commit", "Rebase: replay commits on new base", "Fast-forward merge when no divergence", "Resolve conflicts manually"],
        common_mistakes=["Force pushing to shared branches", "Not pulling before pushing", "Large binary files in repo", "Merge conflicts from long-lived branches"],
        edge_cases=["Merge conflict resolution", "Rebase vs merge history", "Detached HEAD state"],
        debugging_patterns=["git log --graph --oneline", "git diff to inspect", "git status for current state"],
        interview_questions=["Merge vs rebase?", "What is a conflict and how resolve?", "Git workflow for feature branch?"],
        practice_targets=["Create branch, make commits, merge", "Resolve merge conflict", "Write .gitignore"],
        placement_relevance=["tcs", "infosys", "wipro", "cognizant", "accenture", "google", "microsoft", "amazon"],
    )
    concepts["git_collaboration"] = concept_template(
        "git_collaboration", "Git Collaboration Workflows", "devops", "git", "version_control",
        ["git_branching"], [],
        definition="Collaboration workflows: feature branching, Git Flow, trunk-based development. Pull requests enable code review.",
        mental_model="Git collaboration is team writing. Feature branch = individual draft. Pull request = asking for review. Main branch = published book. CI = automated proofreading.",
        key_rules=["Feature branch per change", "Pull request for review", "CI runs tests before merge", "Main branch always deployable", "Code review before merge"],
        common_mistakes=["Skipping code review", "Merging without running CI", "Force pushing to main", "Not communicating before large changes"],
        edge_cases=["Squash merge for clean history", "Rebase before merge to avoid merge commits", "Protected branches on GitHub/GitLab"],
        debugging_patterns=["git log to see history", "git blame to see who changed line", "git diff for PR review"],
        interview_questions=["Describe your git workflow?", "What is a pull request?", "How handle merge conflicts in team?"],
        practice_targets=["Simulate feature branch workflow", "Write PR description", "Review and merge PR"],
        placement_relevance=["tcs", "infosys", "wipro", "cognizant", "accenture", "google", "microsoft", "amazon"],
    )
    concepts["linux_basics"] = concept_template(
        "linux_basics", "Linux Fundamentals", "devops", "linux", "os",
        [], ["git_basics", "docker_basics"],
        definition="Linux is open-source OS. Shell (bash/zsh) is command interface. File system is hierarchical tree. Permissions control access.",
        mental_model="Linux is a building. Shell is the lobby where you give instructions. File system is floors and rooms. Permissions are keys: read (view), write (modify), execute (run).",
        key_rules=["File system: / (root), /home, /etc, /var, /usr", "Permissions: rwx for owner/group/others", "chmod changes permissions, chown changes owner", "Shell: bash/zsh, commands with flags", "Piping: | connects commands"],
        common_mistakes=["Running commands as root unnecessarily", "Confusing relative and absolute paths", "Forgetting to quote variables in shell", "Using rm -rf without double-checking"],
        edge_cases=["Hidden files (dotfiles)", "Symbolic vs hard links", "File descriptors and limits"],
        debugging_patterns=["ls -la to inspect permissions", "strace to trace system calls", "journalctl for logs"],
        interview_questions=["What is Linux shell?", "Explain file permissions?", "What is the difference between soft link and hard link?"],
        practice_targets=["Navigate and manipulate files", "Write shell script with loops", "Set permissions with chmod"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft"],
    )
    concepts["docker_compose"] = concept_template(
        "docker_compose", "Docker Compose", "devops", "docker", "containers",
        ["docker_basics"], ["ci_cd"],
        definition="Docker Compose defines multi-container applications in YAML. Services, networks, and volumes are declaratively configured.",
        mental_model="Docker Compose is a recipe book. Each service is a dish (web server, database, cache). docker-compose.yml is the recipe. docker-compose up cooks everything.",
        key_rules=["services: list of containers", "build or image for each service", "ports: expose container ports", "volumes: persistent storage", "depends_on for startup order (not readiness)"],
        common_mistakes=["Not using named volumes for persistence", "Confusing depends_on with actual health checks", "Hardcoding credentials in compose file", "Running multiple services in one container"],
        edge_cases=["Environment variable substitution", "Multiple compose files (override)", "Health checks for service readiness"],
        debugging_patterns=["docker compose logs for output", "docker compose ps for status", "docker compose exec to enter container"],
        interview_questions=["What is Docker Compose?", "When use Compose vs Kubernetes?", "How manage secrets in Compose?"],
        practice_targets=["Define multi-service app with Compose", "Use volumes for database persistence", "Configure network between services"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft"],
    )
    concepts["ci_cd"] = concept_template(
        "ci_cd", "CI/CD Pipelines", "devops", "devops", "automation",
        ["git_basics", "docker_basics"], [],
        definition="CI (Continuous Integration) automatically builds and tests on every commit. CD (Continuous Deployment/Delivery) automatically deploys passing builds.",
        mental_model="CI is automated quality check on every save. CD is automated publishing when quality passes. Pipeline is assembly line: build -> test -> deploy.",
        key_rules=["CI: build + test on every commit", "CD: deploy automatically after CI passes", "Pipeline as code (YAML/DSL)", "Fast feedback on failures", "Deploy to staging, then production"],
        common_mistakes=["CI runs too long (slow feedback)", "Not testing in CI (just building)", "Deploying without approval for production", "Hardcoding secrets in pipeline config"],
        edge_cases=["Feature flags for partial rollout", "Canary deployments", "Rollback on failure"],
        debugging_patterns=["Check CI logs for failure point", "Run pipeline locally with act", "Monitor deployment metrics"],
        interview_questions=["What is CI/CD?", "How design a CI pipeline?", "How handle failed deployment?"],
        practice_targets=["Write GitHub Actions workflow", "Add automated tests to CI", "Implement deployment pipeline"],
        placement_relevance=["tcs", "infosys", "wipro", "amazon", "microsoft"],
    )

    return concepts


def add_missing_from_graph(corpus: dict) -> int:
    """Add concepts referenced in prereq_graph but missing from concepts."""
    concepts = corpus.setdefault("concepts", {})
    prereq_graph = corpus.setdefault("prerequisite_graph", {})
    added = 0
    all_ids = set(concepts.keys())
    for concept_id, prereqs in prereq_graph.items():
        for prereq in prereqs:
            if prereq not in all_ids:
                concepts[prereq] = concept_template(
                    concept_id=prereq,
                    title=prereq.replace("_", " ").title(),
                    domain="unknown",
                    language="unknown",
                    category="unknown",
                    prerequisites=[],
                    related_concepts=[concept_id],
                    definition=f"Auto-generated placeholder for {prereq}. Expand with real content.",
                    mental_model="",
                    key_rules=[],
                    common_mistakes=[],
                    edge_cases=[],
                    debugging_patterns=[],
                    interview_questions=[],
                    practice_targets=[],
                    placement_relevance=[],
                )
                concepts[prereq]["content_status"] = "AUTO_SCAFFOLDED"
                concepts[prereq]["verification"] = {
                    "sources": [],
                    "last_verified": "2026-09-15",
                    "verified_by": "auto_scaffolded",
                    "verification_notes": "Auto-generated from prerequisite graph. Requires enrichment."
                }
                all_ids.add(prereq)
                added += 1
    return added


def expand_corpus(dry_run: bool = False, validate_only: bool = False) -> dict:
    """Main expansion logic."""
    corpus = load_corpus(_CORPUS_FILE)
    original_count = len(corpus.get("concepts", {}))

    if validate_only:
        issues = validate_corpus_data(corpus)
        return {"valid": len(issues) == 0, "issues": issues, "original_concepts": original_count}

    # Step 1: Add missing concepts from prereq graph
    added_from_graph = add_missing_from_graph(corpus)
    logger.info("Added %d missing concepts from prerequisite graph", added_from_graph)

    # Step 2: Add generated concepts
    generated = generate_missing_concepts()
    concepts = corpus.setdefault("concepts", {})
    added_generated = 0
    for cid, concept in generated.items():
        if cid not in concepts:
            concepts[cid] = concept
            added_generated += 1
        else:
            logger.debug("Concept %s already exists, skipping", cid)

    # Step 3: Update curriculum map with new concepts
    curriculum_map = corpus.setdefault("curriculum_map", {})
    for cid in generated:
        if cid not in _flatten_curriculum(curriculum_map):
            _add_to_curriculum_map(curriculum_map, cid)

    # Step 4: Validate
    issues = validate_corpus_data(corpus)
    if issues:
        logger.warning("Validation found %d issues:", len(issues))
        for issue in issues[:10]:
            logger.warning("  - %s", issue)

    final_count = len(corpus.get("concepts", {}))
    summary = {
        "original_concepts": original_count,
        "added_from_graph": added_from_graph,
        "added_generated": added_generated,
        "final_concepts": final_count,
        "validation_issues": issues,
        "dry_run": dry_run,
    }

    if not dry_run:
        save_corpus(_CORPUS_FILE, corpus)
        logger.info("Corpus expanded: %d -> %d concepts", original_count, final_count)
    else:
        logger.info("Dry run: would expand %d -> %d concepts", original_count, final_count)

    return summary


def _flatten_curriculum(curriculum_map: dict) -> set[str]:
    """Flatten curriculum map to set of concept IDs."""
    result: set[str] = set()
    for domain_langs in curriculum_map.values():
        if isinstance(domain_langs, dict):
            for seq in domain_langs.values():
                if isinstance(seq, list):
                    result.update(seq)
        elif isinstance(domain_langs, list):
            result.update(domain_langs)
    return result


def _add_to_curriculum_map(curriculum_map: dict, concept_id: str) -> None:
    """Add concept to appropriate place in curriculum map."""
    # Extract language from concept_id (first part before _)
    lang = concept_id.split("_")[0] if "_" in concept_id else "unknown"

    # Ensure domain exists
    for domain in ["programming", "cs", "web", "databases", "devops", "placement"]:
        if domain in concept_id or lang in ["c", "cpp", "java", "python", "javascript"]:
            domain_map = curriculum_map.setdefault(domain, {})
            lang_list = domain_map.setdefault(lang, [])
            if concept_id not in lang_list:
                lang_list.append(concept_id)
            return


def main():
    parser = argparse.ArgumentParser(description="Expand BountyCode Knowledge Corpus")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--validate-only", action="store_true", help="Only validate current corpus")
    args = parser.parse_args()

    if args.validate_only:
        result = expand_corpus(validate_only=True)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result.get("valid") else 1)

    result = expand_corpus(dry_run=args.dry_run)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
