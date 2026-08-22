"""
WORLD-CLASS CURRICULUM ENRICHMENT LAYER
=======================================

Synthesized from the best learning systems on earth:
  * Coddy.tech     — build something with EVERY lesson; every concept ships a working artifact
  * CS50           — problem sets grounded in real domains (cryptography, finance, forensics)
  * freeCodeCamp   — certification-shaped progression; project-first proof of skill
  * Odin Project   — portfolio-first; "learn, then build, then deploy"
  * MIT 6.006/6.031, Stanford CS106, ThePrimeagen, Exercism — first-principles rigor

What this layer ADDS to every lesson in LANGUAGES (all tracks, all levels):

  why            — Why this matters. Motivation + real reason a working engineer knows it.
  real_world     — What you can DO with this in real life. Concrete products/domains.
  interview      — How interviewers actually ask this (real question stems + STAR hooks).
  build          — A SHIPPABLE project you build using ONLY this module (even "if statements").
  problem_set    — A CS50-style applied problem with constraints + grading rubrik.
  engineering    — How this maps to software engineering practice (systems, scale, teams).
  career         — Which roles/domains/skills this unlocks on a real CV.

Every module produces something. Nobody reads 10 lessons and builds nothing.
"""

#pylint: skip-file

import re
from .curriculum import LANGUAGES

# ============================================================
# CONCEPT KNOWLEDGE BASE
# ============================================================

CONCEPT_META = {
    # ── Foundations ──────────────────────────────────────────
    "hello_world": {
        "keywords": ["hello", "first steps", "first program", "print", "output", "welcome"],
        "why": "Every program, every service, every CLI starts with output. 'Hello world' is the first proof that your toolchain, your editor, and your understanding of program entry points all work. It is the ceremony every developer repeats before building anything real.",
        "real_world": "Log lines in servers, CLI tools printing usage, health-check endpoints returning text, and every 'it works!' milestone in a deployment pipeline.",
        "interview": [
            "What happens between pressing Enter and seeing 'Hello world' on screen? (compile/link/load/exec)",
            "Why do most languages use a `main` entry point? What changes it?",
            "Walk me through how you'd add a command-line flag to print a custom greeting.",
        ],
        "build": "Build a CLI 'Hello World' that prints a formatted greeting based on a name argument, with color and a border — then convert it into a repeatable `say hello <name>` shell command.",
        "problem_set": "Print 'Hello, [name]' where the user supplies the name. If no name is supplied, default to 'world'. Handle names with spaces. Then print it 100 times, once per line, with the index. (CS50-style: correctness, then style.)",
        "engineering": "This is your first CI signal — a buildable, runnable artifact. Real projects start with a stub that compiles; everything else is layered on top.",
        "career": "Everyone. It is the zero point of a developer's measurable output.",
    },
    "variables": {
        "keywords": ["variable", "data", "types", "declaration", "constant", "type", "naming", "primitive"],
        "why": "Variables are how programs remember. All state — a user's balance, a sensor reading, a cart item — lives in typed containers. Choosing the right type and name is the difference between code that survives a year and code that dies in a week.",
        "real_world": "Bank balances (float/decimal), user IDs (int/UUID), names (string), feature flags (bool), timestamps (date/epoch). Every feature you've ever used is variables wired together.",
        "interview": [
            "Why is `1 == 1.0` sometimes true and sometimes false across languages?",
            "What is the difference between int, float, and double precision-wise? When do you need BigDecimal instead?",
            "Explain what happens if you divide two integers in your language of choice.",
        ],
        "build": "Build a personal 'Variable Journal' CLI: define and print a profile (name, age, height, savings, is_student) using the exact right type for each field, then serialize it to JSON.",
        "problem_set": "Implement a simple bank balance: declare balance=100.00, deposit=25.50, withdraw=10.75. Compute the final balance and print it with exactly 2 decimals. Guard against withdrawing more than the balance.",
        "engineering": "Types are contracts. When you choose `int` vs `decimal`, you are making a correctness promise that the rest of the system depends on. Type errors are the cheapest bugs to fix — at compile time.",
        "career": "Every backend/frontend/data role. Type discipline is a core hiring signal.",
    },
    "operators": {
        "keywords": ["operator", "arithmetic", "comparison", "logical", "bitwise", "precedence", "ternary"],
        "why": "Operators are the verbs of code. Understanding precedence and the difference between `=` and `==`, `&&` vs `&`, and short-circuiting prevents a whole class of silent logic bugs.",
        "real_world": "Pricing engines (multiply/round), access control (AND/OR rules), permission flags (bitwise), search filters, game physics (vector math).",
        "interview": [
            "What does short-circuit evaluation mean and how would you exploit it?",
            "When would you use a bitwise operator in a real product?",
            "Explain operator precedence with `2 + 3 * 4 ** 2`.",
        ],
        "build": "Build a 'Pricing Engine' CLI: take price, tax rate, discount %, shipping cost, and compute final total using correct precedence, rounding, and a logical check for free-shipping thresholds.",
        "problem_set": "Write a function `apply_tax(price, rate)` that rounds to cents. Then compute a cart total where each item has different tax treatment. Then add a bulk-discount that only applies when subtotal > $100 AND item_count > 5. (Finance-domain problem set.)",
        "engineering": "Operator correctness is the foundation of billing, auth, and safety systems. One wrong `|` vs `||` has shipped real CVEs.",
        "career": "All engineering roles; especially fintech, game dev, and systems programming.",
    },
    "conditionals": {
        "keywords": ["if", "else", "elif", "switch", "conditional", "ternary", "decision", "branch"],
        "why": "Conditionals are how programs make decisions. Every user experience — whether to show an error, grant access, apply a discount — is a chain of decisions. Master them and you master product logic.",
        "real_world": "Auth checks (allowed/denied), form validation, routing logic, feature flags, game state machines, recommendation branching, business rules engines.",
        "interview": [
            "How do you handle deeply nested if-else without making code unreadable? (early returns, guards, lookup tables)",
            "When should you use a switch instead of if-else? What about a map/dict?",
            "What are the edge cases in this validation? (empty string, null, negative, unicode)",
        ],
        "build": "Build a 'Decision Bot': a CLI that reads a user answer and routes through a decision tree (loan eligibility, admission calculator, or a rock-paper-scissors judge) using ONLY conditionals — no loops, no functions.",
        "problem_set": "CS50-style 'Cash': given an amount owed, compute the fewest coins possible. First implement with a naive if-chain; then refactor using a greedy loop. Both must pass a test harness with edge cases (0, negative, fractional).",
        "engineering": "Conditionals are where business rules live. Interviewers test whether you can turn a paragraph of business requirements into a correct, readable branch structure without spaghetti.",
        "career": "Every role. Business-logic correctness is the #1 junior hiring assessment.",
    },
    "loops": {
        "keywords": ["loop", "for", "while", "do-while", "iterate", "iteration", "nested loop", "range"],
        "why": "Loops are how computers earn their keep — repeating work millions of times. Understanding loop bounds, off-by-one errors, and when NOT to loop (vectorize/parallelize) separates engineers from script-kiddies.",
        "real_world": "Rendering every pixel, polling every sensor, paginating API results, aggregating analytics, batch ETL jobs, retry loops, game tick loops.",
        "interview": [
            "What is an off-by-one error and how do you prevent it?",
            "How would you iterate a 2D matrix efficiently for cache locality?",
            "Write a loop that finds the max value without using a library. Now write it for a stream you can't store in memory.",
        ],
        "build": "Build a 'Pagination Crawler': fetch 100 records in pages of 10 using a loop, stopping when fewer than a page returns — no recursion, no libraries.",
        "problem_set": "CS50-style 'Mario': print a right-aligned pyramid of a given height using nested loops. Then a mirror pyramid. Validate input. (Classic CS50 problem set, fully rebuildable.)",
        "engineering": "Loop efficiency is systems engineering. O(n²) loops inside a hot path are how products die under load. Know your loop's cost.",
        "career": "Every role; essential for data processing, game dev, and backend services.",
    },
    "functions": {
        "keywords": ["function", "method", "return", "parameter", "argument", "def ", "signature"],
        "why": "Functions are the unit of thought. They let you name a behavior, reuse it, test it, and swap it. Every framework, library, and API is ultimately a set of well-named functions.",
        "real_world": "API endpoints, library APIs, validation helpers, math utilities, callbacks/hooks in UI frameworks, Lambda/serverless functions.",
        "interview": [
            "What makes a good function signature? (naming, params, single responsibility)",
            "What is the difference between passing by value vs reference in your language?",
            "When would you split one function into two? What are the signs?",
        ],
        "build": "Build a 'Utility Library' with 5 pure functions (clamp, truncate, format_date, slugify, deep_merge) and a test file proving each — the seed of a real npm/PyPI package.",
        "problem_set": "Write a function that converts a number to words (e.g., 1234 → 'one thousand two hundred thirty-four'). Must handle 0-1,000,000. Test with a table of cases. (CS50 'Indices'-style applied problem.)",
        "engineering": "Functions are the atomic unit of testability and the seam for dependency injection. Code review quality is measured in function design.",
        "career": "Every role; functional decomposition is a core software-engineering interview skill.",
    },
    "recursion": {
        "keywords": ["recurs", "base case", "memoiz", "backtrack", "divide"],
        "why": "Recursion is how you model problems that contain themselves — trees, directories, JSON, parsing. It also trains the mental model interviewers probe hardest: 'can you think recursively?'",
        "real_world": "Directory traversal, JSON/DOM parsing, tree rendering, file-system operations, backtracking solvers (Sudoku, regex), quicksort/mergesort.",
        "interview": [
            "How would you compute the height of a binary tree? Write it recursively, then explain the call stack.",
            "What are the dangers of recursion in production? (stack depth, TCO)",
            "Convert this recursive function to iterative and explain the trade-off.",
        ],
        "build": "Build a recursive 'Directory Size Analyzer' that walks nested folders and reports the largest files per directory — then handle the real-world risk of deep nesting.",
        "problem_set": "CS50-style: implement the Collatz sequence with a recursive function counting steps to 1, then add memoization and graph the speedup for values up to 10^6.",
        "engineering": "Recursion is the natural implementation of divide-and-conquer at scale — search trees, parse trees, and recursion on data structures power compilers, databases, and crawlers.",
        "career": "Required for interviews at every big-tech company; core for systems & compilers roles.",
    },
    "arrays": {
        "keywords": ["array", "matrix", "2d", "index", "slice", "list", "vector", "tuple", "collection"],
        "why": "Arrays are the memory model for nearly everything: images are 2D arrays, tables are arrays of rows, buffers are arrays of bytes. Cache-aware array code is the difference between a fast and a slow product.",
        "real_world": "Image processing (pixel grids), spreadsheets, time-series data, protocol buffers, pagination, ring buffers in networking, game boards.",
        "interview": [
            "Why is array access O(1)? What is the actual memory operation?",
            "Two-sum: brute force then optimize. What data structure do you add?",
            "Rotate an array in place in O(1) space. Explain the reverse-three-times trick.",
        ],
        "build": "Build an 'In-Memory Grid Editor': a 2D array you can navigate, read/write cells, and export as CSV — the core of any spreadsheet or map editor.",
        "problem_set": "CS50-style: read a grayscale bitmap, detect all 'peaks' (cells larger than all 4 neighbors), and mark them. Then implement a simple box-blur convolution on a 2D array. (CS50 'Filter' problem set.)",
        "engineering": "Cache locality, stride access, and amortized growth are the real-world performance skills that array mastery unlocks.",
        "career": "Data-heavy, graphics, game, and performance engineering roles.",
    },
    "strings": {
        "keywords": ["string", "char", "text", "substring", "regex", "regexp", "pattern", "tokeniz", "parse"],
        "why": "Software is 80% text processing: parsing input, sanitizing output, matching patterns, formatting messages. Strings are where security bugs (injection, XSS) and UX bugs (formatting, encoding) are born.",
        "real_world": "Form validation, URL routing, search indexing, log parsing, SQL/query generation (danger!), HTML sanitization, internationalization.",
        "interview": [
            "How do you check if two strings are anagrams? What's the space/time?",
            "What is the performance difference between string concatenation in a loop vs join/builder? Why?",
            "Write a regex to validate an email. Now tell me three ways it's wrong.",
        ],
        "build": "Build a 'Text Toolkit' CLI: slugify, truncate, word-count, camel-to-snake, and a safe HTML-escape function — the utilities every real web backend ships.",
        "problem_set": "CS50-style 'Readability': compute the Flesch-Kincaid reading level of a passage (letters, words, sentences). Then add a tokenizer that correctly splits contractions and URLs.",
        "engineering": "Unicode handling, immutable-vs-builder performance, and injection-safe escaping are production-critical string skills.",
        "career": "Backend, security, data engineering, and full-stack roles.",
    },
    "pointers": {
        "keywords": ["pointer", "memory", "reference", "heap", "stack", "allocat", "malloc", "derefer"],
        "why": "Pointers are how memory actually works. Even in managed languages, references are pointers in disguise. Understanding them explains why some code is fast, why some leaks, and why some crashes.",
        "real_world": "Every systems program (OS, browser, game engine), database buffer pools, zero-copy network stacks, embedded systems, memory-mapped files.",
        "interview": [
            "What is the difference between stack and heap memory? Which is faster and why?",
            "Explain a use-after-free. How would Rust or garbage collection prevent it?",
            "What does a null pointer dereference do at the hardware level?",
        ],
        "build": "Build a manual 'Slab Allocator' (fixed-size blocks with a free list) and benchmark it against the language's default allocator — a real memory-pooling exercise.",
        "problem_set": "CS50-style 'Memory Leak Hunt': given a C program with 5 intentional leaks/UB (double free, use-after-free, uninitialized read), find and fix all 5 using sanitizers and Valgrind, documenting each fix.",
        "engineering": "Memory ownership discipline is the #1 interview topic for systems roles and the origin of entire classes of CVEs.",
        "career": "Systems, embedded, game engines, database internals, and performance roles.",
    },
    "oop": {
        "keywords": ["oop", "class", "object", "inherit", "polymorph", "encapsul", "abstraction", "interface", "struct"],
        "why": "OOP is how teams structure large codebases: entities, contracts, and boundaries. Even in functional shops, you model domain concepts, and interfaces/abstractions are everywhere.",
        "real_world": "Domain models (User, Order, Product), framework components, plugin architectures, GUI widget trees, entity-component systems in games.",
        "interview": [
            "What is the difference between composition and inheritance? When do you choose each?",
            "What does SOLID mean in practice? Give a violation and the fix.",
            "How would you design a system for vehicles (Car, Truck, Motorcycle) using OOP?",
        ],
        "build": "Build a 'Library System' with Book, Member, Loan classes; enforce rules (max 5 loans, overdue fees) via encapsulation — the classic domain-modeling exercise, fully runnable.",
        "problem_set": "CS50-style: model a vending machine as classes with state, then simulate 100 random purchases and validate invariants (never oversell, never negative stock).",
        "engineering": "Interfaces, dependency injection, and polymorphism are how real teams plug components together without rewriting.",
        "career": "Every application-development role; core to backend and enterprise work.",
    },
    "data_structures": {
        "keywords": ["linked list", "stack", "queue", "deque", "tree", "graph", "hash", "heap", "trie", "data structure", "bst", "map", "set"],
        "why": "Data structures are the vocabulary of algorithmic thinking. Choosing the right one (queue vs stack, hash vs tree, trie vs set) is the single highest-leverage optimization decision a developer makes.",
        "real_world": "Undo (stack), print queue (queue), routing (graph), autocorrect (trie), in-memory cache (hash), task scheduler (heap), file system (tree).",
        "interview": [
            "When would you use a hash map over a binary search tree? Compare worst cases.",
            "Implement a queue with two stacks. What's the amortized complexity?",
            "How does a web browser's back button relate to a stack? What about a print queue?",
        ],
        "build": "Build an 'Expression Evaluator' using two stacks (shunting-yard algorithm): parse `3 + 4 * 2` correctly, handle parentheses and unary minus — real calculator technology.",
        "problem_set": "CS50-style 'Trie Autocomplete': build a trie, insert 1000 words, implement prefix autocomplete with ranking. Measure query time vs a linear scan.",
        "engineering": "Data-structure choice determines latency, memory, and cache behavior at scale. This is the most-tested interview category on earth.",
        "career": "Required for every software engineering interview (FAANG and beyond).",
    },
    "sorting": {
        "keywords": ["sort", "merge sort", "quick sort", "heap sort", "insertion", "selection", "bubble", "radix", "counting"],
        "why": "Sorting is the canonical algorithm-thinking lesson: comparisons, recursion, divide-and-conquer, complexity analysis, stability, and in-place vs extra memory. Everything algorithmic builds on it.",
        "real_world": "Database ORDER BY, search ranking, leaderboards, nearest-neighbor, deduplication, merge operations in map-reduce.",
        "interview": [
            "Describe merge sort and its complexity. Why is it stable?",
            "When does insertion sort beat merge sort in practice?",
            "How would you sort a list too large to fit in memory?",
        ],
        "build": "Build a 'Sorting Visualizer' that animates bubble, selection, insertion, merge, and quick sort on a bar array, with step counters for comparisons and swaps.",
        "problem_set": "CS50-style: implement merge sort, then sort 1M integers from a file on disk using external mergesort (chunks + merge) and report total time.",
        "engineering": "Real systems sort petabytes (external mergesort), choose stable sorts for stable pagination, and use counting sort in linear-time special cases.",
        "career": "Interviews + data/backend engineering.",
    },
    "searching": {
        "keywords": ["search", "binary search", "linear search", "find", "lookup"],
        "why": "Search is the most common read operation in software. Binary search turns a billion-record lookup into ~30 comparisons; knowing when you can use it is a superpower.",
        "real_world": "Indexed database lookups, autocomplete, spell-check, log search, game A* uses search algorithms, plagiarism detection.",
        "interview": [
            "Binary search: implement iteratively, then recursively. What's the worst case?",
            "What precondition does binary search need? What if data is sorted but has duplicates?",
            "Find first/last occurrence of a value with binary search.",
        ],
        "build": "Build a 'Gigabyte Log Searcher': given a sorted log file, implement binary search over file offsets to find all entries in a time range without loading the file.",
        "problem_set": "CS50-style: search for a name in a phonebook — first linear, then sort + binary, measuring the difference at 1M records.",
        "engineering": "Indexing IS search done right. Database indexes are B-trees so that range searches stay logarithmic.",
        "career": "Interviews + backend & data roles.",
    },
    "hashing": {
        "keywords": ["hash", "hashmap", "dict", "map", "collision", "hashmap", "hashing"],
        "why": "Hashing turns lookups from O(n) to O(1) average. It powers caches, password storage, deduplication, sharding, and index-free in-memory search. Every developer reaches for a hash table daily.",
        "real_world": "Password verification (bcrypt/argon2), content addressing (git, IPFS), caches (Redis key lookup), distributed sharding (consistent hashing), fingerprinting (MD5/SHA).",
        "interview": [
            "How does a hash table work internally? What happens on collision?",
            "Why do dictionaries not preserve order in some languages? How do they now?",
            "Design a URL shortener that handles 1M URLs — what role does hashing play?",
        ],
        "build": "Build a 'Duplicate File Finder': hash file contents, group by hash, report exact-duplicate groups across nested directories — real storage-recovery tool.",
        "problem_set": "CS50-style 'Speller': load a dictionary into a hash table, then spell-check a text and count misspellings vs load time. Optimize your hash function; report the speedup.",
        "engineering": "Load factor, resizing, and hash quality directly determine cache hit rates and latency at scale.",
        "career": "Interviews + systems/backend/data engineering.",
    },
    "dynamic_programming": {
        "keywords": ["dynamic programming", "dp", "memoiz", "tabulation", "knapsack", "lcs", "edit distance", "fibonacci", "optimal substructure"],
        "why": "DP is the interview gatekeeper and the technique behind route planning, genome alignment, speech recognition, and resource allocation. It trains the single most valuable skill: breaking a problem into overlapping subproblems.",
        "real_world": "Navigation shortest paths, DNA/protein sequence alignment, text diff (LCS), investment portfolio optimization, video compression (rate-distortion DP), OS job scheduling.",
        "interview": [
            "What is the difference between memoization and tabulation?",
            "Explain the 0/1 knapsack recurrence. What changes for unbounded?",
            "How would you compute the edit distance between two strings? Walk through the table.",
        ],
        "build": "Build a 'Text Diff Tool' using LCS DP that shows added/removed lines between two files — the algorithm behind `git diff`.",
        "problem_set": "CS50-style 'Change' extension: given coin denominations, compute minimum coins via DP for any amount up to 1,000,000, then compare against the greedy solution and find a case where greedy fails.",
        "engineering": "DP is how real systems make optimal decisions under constraints — scheduling, compression, and optimization engines all use it.",
        "career": "Required for big-tech interviews; valuable in ML, operations research, and systems.",
    },
    "greedy": {
        "keywords": ["greedy", "interval", "huffman", "activity selection", "minimum spanning"],
        "why": "Greedy algorithms choose the best option at each step. They're fast, elegant, and wrong more often than students expect — learning when they're provably correct is a deeper skill.",
        "real_world": "Scheduling (CPU, meetings), data compression (Huffman), network routing (Dijkstra), coin systems, task assignment, cache eviction (LRU is greedy).",
        "interview": [
            "When is a greedy algorithm provably optimal? Give an example where it fails.",
            "Design a meeting-room scheduler minimizing rooms.",
            "Why is Dijkstra greedy? What happens with negative edges?",
        ],
        "build": "Build a 'Meeting Scheduler' that assigns meetings to the fewest rooms using earliest-end-first greedy, then prove it optimal with a small test harness.",
        "problem_set": "CS50-style: implement Huffman coding to compress a text file, report compression ratio, and decompress losslessly.",
        "engineering": "Real schedulers, load balancers, and compilers use greedy choices every millisecond.",
        "career": "Interviews + systems/algorithmic roles.",
    },
    "backtracking": {
        "keywords": ["backtrack", "n-queens", "sudoku", "permutation", "combination", "search space"],
        "why": "Backtracking is exhaustive search done intelligently. It's how solvers explore impossible spaces — and the same pruning ideas power constraint satisfaction in real products.",
        "real_world": "Sudoku/regex solvers, constraint programming (scheduling, planning), AI game search (with pruning), route optimization (TSP branch-and-bound).",
        "interview": [
            "Solve N-Queens. How do you prune? What is the time complexity?",
            "Generate all permutations of a string. Handle duplicates.",
            "When would you use BFS over backtracking/DFS for a search problem?",
        ],
        "build": "Build a 'Sudoku Solver' using backtracking with constraint propagation (naked singles), loading puzzles from a file and timing the solve.",
        "problem_set": "CS50-style: solve N-Queens for N up to 12, visualizing the board; report solutions vs time as N grows.",
        "engineering": "Constraint-solving and search pruning are core to scheduling engines, regex engines, and AI.",
        "career": "Interviews + AI/games/constraint domains.",
    },
    "bit_manipulation": {
        "keywords": ["bit", "binary", "mask", "bitwise", "bitmask", "bit manipulation", "shift"],
        "why": "Bits are the bottom layer. Bit manipulation is how you represent permissions, flags, and compact state — and how you write code that runs 100x faster than clever-but-wasteful logic.",
        "real_world": "Unix file permissions (chmod 755), network subnet masks, feature flags, image pixel packing, compression, bloom filters, cryptography.",
        "interview": [
            "Check if a number is a power of two in one line.",
            "Count the set bits in an integer (popcount) efficiently.",
            "How would you represent 32 boolean flags in one integer?",
        ],
        "build": "Build a 'Permissions Calculator': take octal chmod like 755, show the permission matrix, and simulate a `ls -l` style output using bit masks.",
        "problem_set": "CS50-style: implement an 8-bit adder (full adder logic) in code, then a 16-bit CRC and validate against known test vectors.",
        "engineering": "Bit-level efficiency shows up in every hot path: network headers, protocol parsing, and low-latency systems.",
        "career": "Systems, networking, embedded, crypto, and interviews.",
    },
    "file_io": {
        "keywords": ["file", "read", "write", "stream", "serializ", "csv", "json", "parse file", "i/o"],
        "why": "Real programs persist. Files, logs, configs, and data exports are the interface between your program and the world. File I/O is where engineers learn about buffers, encoding, and partial failures.",
        "real_world": "Config files, log aggregation, ETL pipelines, database storage engines, save games, CSV exports, backup systems.",
        "interview": [
            "How do you handle a file that is too large to read entirely into memory?",
            "What is a buffered reader and why does it matter?",
            "How do you safely overwrite a config file so you never corrupt it on crash?",
        ],
        "build": "Build a 'CSV to JSON Converter' CLI that streams large files line-by-line, handles quotes/commas in fields, and writes valid JSON — the exact tool every data team writes.",
        "problem_set": "CS50-style: analyze a CSV of campaign donations — read, parse, aggregate by candidate, and report totals; then handle a corrupt line gracefully.",
        "engineering": "Streaming, atomic writes (write-temp-rename), and encoding handling are production-critical file skills.",
        "career": "Backend, data engineering, and systems roles.",
    },
    "error_handling": {
        "keywords": ["error", "exception", "try", "catch", "throw", "finally", "error handling"],
        "why": "Production code fails constantly: networks drop, disks fill, APIs change. Error handling is how you fail gracefully — the difference between a user sees a friendly message vs a 500 stack trace.",
        "real_world": "Retry logic on transient failures, graceful degradation, validation errors with field messages, circuit breakers, dead-letter queues.",
        "interview": [
            "What is the difference between checked and unchecked exceptions (Java) / exceptions vs error values (Go)?",
            "How do you decide when to catch vs propagate?",
            "Design a retry strategy for a flaky third-party API. What about idempotency?",
        ],
        "build": "Build a 'Resilient Downloader' that retries with exponential backoff, jitter, and timeout, and writes partial progress so an interrupted download can resume.",
        "problem_set": "CS50-style: write a JSON parser that must produce structured error messages with line/column on every failure mode (unterminated string, bad number, trailing comma).",
        "engineering": "Robustness is a hiring signal. Interviewers probe how you think about partial failure — the essence of distributed systems.",
        "career": "Every production role; especially backend, SRE, and platform.",
    },
    "debugging": {
        "keywords": ["debug", "bug", "gdb", "profiler", "breakpoint", "trace", "fix"],
        "why": "Debugging is where most developer time goes. Knowing how to isolate a bug — bisect, reproduce, instrument, sanitize — is the difference between a 10-minute fix and a 10-hour spiral.",
        "real_world": "Every bug you'll ever fix: production incidents, off-by-one data corruption, race conditions, memory leaks, flaky tests.",
        "interview": [
            "Walk me through how you'd debug a production outage.",
            "What tools do you use and why? (debugger, logs, profilers, sanitizers)",
            "How do you debug a bug that only happens in production but never locally?",
        ],
        "build": "Build a 'Mini Debugger' that takes a file and a line number, prints the function call stack at that point via a mock trace, then steps through a scripted bug with the user.",
        "problem_set": "CS50-style: a program 'works' but has a race condition under load. Use logs + a scripted stress test to find, document, and fix it; prove the fix with 100 runs.",
        "engineering": "Root-cause analysis, binary search bisection, and reproducible-reduction are the actual daily tools of software engineering.",
        "career": "Every role; SRE/DevRel/backend especially.",
    },
    "testing": {
        "keywords": ["test", "unit", "assert", "testing", "test case", "coverage", "fixture", "mock"],
        "why": "Tests are how you sleep at night. A good test suite makes refactoring safe, documents behavior, and catches regressions before users do. It's the #1 professional habit that separates devs from hobbyists.",
        "real_world": "CI pipelines (every PR runs tests), regression prevention, contract testing between services, property-based testing of parsers, golden-file testing of formatters.",
        "interview": [
            "What makes a good unit test? What makes a bad one?",
            "How do you test a function that calls a flaky external API?",
            "What's the difference between unit, integration, and E2E tests? When is each worth it?",
        ],
        "build": "Build a test suite for a small calculator library covering normal, edge (0, negatives, max-int), and error cases, then wire it into a CI command.",
        "problem_set": "CS50-style: given a sorting function, write a property-based test that runs 1000 random arrays and verifies sortedness + permutation equality (same multiset).",
        "engineering": "Test-driven development, coverage budgets, and CI gating are standard engineering practice, not optional.",
        "career": "Every role; QA/Test/SDET and platform engineering deeply.",
    },
    "concurrency": {
        "keywords": ["thread", "async", "concurren", "parallel", "mutex", "lock", "goroutine", "promise", "await", "race"],
        "why": "Every modern system is concurrent: servers handle millions of requests, UIs stay responsive, data pipelines stream in parallel. Concurrency is where performance, correctness, and debugging all collide.",
        "real_world": "Web servers (async I/O), microservices fan-out, parallel data processing, real-time chat, game loops, background jobs/queues.",
        "interview": [
            "What is a race condition? Give a concrete example and fix.",
            "Explain the difference between concurrency and parallelism.",
            "Deadlock: what are the four necessary conditions? How do you prevent them?",
        ],
        "build": "Build a 'Concurrent Download Manager': download N files in parallel with a worker pool, progress reporting, and a mutex-protected total — then add cancellation.",
        "problem_set": "CS50-style: simulate a producer-consumer queue with a bounded buffer. Add a race detector run, find the race, and fix with the right sync primitive.",
        "engineering": "Async models, thread pools, and race-free shared state are core backend engineering. This is a top-3 interview topic.",
        "career": "Backend, systems, SRE, game, and data roles.",
    },
    "networking": {
        "keywords": ["network", "tcp", "udp", "socket", "http", "tls", "rest", "protocol"],
        "why": "All modern software talks over networks. Understanding TCP vs UDP, HTTP semantics, and TLS gives you the mental model for APIs, caching, load balancing, and distributed systems.",
        "real_world": "APIs, web browsers, chat, streaming, DNS, database connections, message queues, load balancers.",
        "interview": [
            "What happens when you type a URL and press Enter? Walk me through the full stack.",
            "TCP vs UDP: when would you pick UDP in production?",
            "What does a 304 Not Modified actually mean and why does it matter?",
        ],
        "build": "Build a minimal HTTP server from scratch (parse request line, headers, serve files, respond with status codes) using raw sockets — the seed of every web framework.",
        "problem_set": "CS50-style: implement a 'port scanner' that checks which TCP ports are open on localhost using raw sockets, with timeouts, then add a multi-threaded version and compare speed.",
        "engineering": "HTTP caching, connection pooling, keep-alive, and retry/idempotency are daily production concerns.",
        "career": "Backend, web, SRE, security, and game networking roles.",
    },
    "databases": {
        "keywords": ["database", "sql", "sqlite", "index", "query", "table", "schema", "mongo", "nosql", "transaction"],
        "why": "Data is the asset. Databases are how you store, query, and guarantee integrity of data under concurrency. SQL is the most portable skill in tech — it outlives every framework.",
        "real_world": "User accounts, orders, analytics, logs, product catalogs, feature config, billing records — every business runs on a database.",
        "interview": [
            "What is an index and when does it hurt?",
            "Explain a transaction and ACID. What is a phantom read?",
            "Design the schema for a social media app. What would you index?",
        ],
        "build": "Build a 'Task Tracker DB': schema for tasks, tags, and assignments with proper indexes, then run a query showing the slowest queries via EXPLAIN.",
        "problem_set": "CS50-style: load 1M rows into a table, measure query time with/without an index, and add a migration that backfills a new column safely.",
        "engineering": "Schema design, query optimization, and migration discipline are the backbone of backend engineering.",
        "career": "Backend, data engineering, and every full-stack role.",
    },
    "api_design": {
        "keywords": ["api", "rest", "endpoint", "graphql", "grpc", "http server", "route", "middleware"],
        "why": "APIs are the contract between teams and products. A good API is versionable, predictable, and safe to evolve. API design determines developer experience and system decoupling.",
        "real_world": "Every SaaS integration, mobile app backend, internal microservice, and public SDK.",
        "interview": [
            "Design a REST API for a URL shortener. What endpoints, methods, status codes?",
            "How do you version an API and keep old clients working?",
            "Pagination: cursor vs offset. When is each better?",
        ],
        "build": "Build a 'Notes API' with CRUD, validation, pagination, idempotent create, and error responses following a consistent envelope — deployable as a real service.",
        "problem_set": "CS50-style: build an API for a bank that rejects overdrafts, returns proper 4xx with error codes, and passes a contract test suite.",
        "engineering": "API contracts, idempotency, rate limits, and graceful deprecation are core professional concerns.",
        "career": "Backend, full-stack, and platform roles.",
    },
    "design_patterns": {
        "keywords": ["pattern", "singleton", "factory", "observer", "strategy", "decorator", "adapter", "builder"],
        "why": "Patterns are battle-tested solutions to recurring design problems. Knowing them lets you recognize a problem and reach for a proven shape instead of reinventing a worse one.",
        "real_world": "Observer = event systems/UI bindings; Factory = DI containers; Strategy = interchangeable algorithms (payment methods); Adapter = integrating legacy systems.",
        "interview": [
            "Explain the Strategy pattern and give a real use case.",
            "Why is Singleton often considered an anti-pattern now?",
            "How would you add a logging feature to all classes without editing each one? (Decorator/Interceptor)",
        ],
        "build": "Build a 'Payment Gateway Abstraction': Strategy pattern for card/UPI/PayPal with a factory selecting the provider, and an adapter wrapping a legacy API.",
        "problem_set": "CS50-style: refactor a god-class (1000-line) into pattern-based components while keeping all behavior identical — pass the same test suite before and after.",
        "engineering": "Patterns appear constantly in frameworks, DI containers, and event systems. Recognizing them makes you a better reviewer and architect.",
        "career": "Senior/architect roles, all application development.",
    },
    "security": {
        "keywords": ["security", "owasp", "injection", "xss", "csrf", "encrypt", "hash", "auth", "password", "jwt", "oauth"],
        "why": "Security failures destroy products and trust. Understanding the OWASP top 10 — injection, broken auth, XSS, CSRF — is table stakes for shipping anything on the internet.",
        "real_world": "Login systems, payment processing, cookie/session handling, API keys, compliance (PCI, GDPR), third-party integrations.",
        "interview": [
            "How do you prevent SQL injection? Give the vulnerable and safe versions.",
            "How do you store passwords correctly?",
            "What is CSRF and how do you defend against it?",
        ],
        "build": "Build a 'Security Audit Checklist CLI' that scans a small web app's config and reports violations (no HTTPS redirect, weak session cookie, missing CORS restrictions).",
        "problem_set": "CS50-style: given a login form with an injection bug, exploit it, then fix it and prove the fix with a test that would have failed before.",
        "engineering": "Secure defaults, least privilege, input validation, and secret management are production responsibilities in every team.",
        "career": "Security engineers, backend, full-stack, and any team shipping user data.",
    },
    "git": {
        "keywords": ["git", "version control", "branch", "commit", "merge", "rebase", "pull request", "ci"],
        "why": "Git is the coordination layer of all software. Every professional contribution flows through branches, reviews, and merges. Fluency is non-negotiable.",
        "real_world": "Every team's workflow: feature branches, PR reviews, CI checks, release tagging, revert on incident, conflict resolution.",
        "interview": [
            "How do you resolve a merge conflict? Walk through it.",
            "What is the difference between rebase and merge? When do you use each?",
            "You accidentally committed a secret. How do you remove it from history?",
        ],
        "build": "Build a 'Git Workflow Simulator' CLI that models branch, commit, merge, and rebase as data — teaching the graph model interactively.",
        "problem_set": "CS50-style: take a repo, clean up its history with interactive rebase into logical commits, then write a script that verifies the final tree matches the original.",
        "engineering": "Trunk-based vs feature-branch workflows, code review, and release engineering all hang on git discipline.",
        "career": "Every role, everywhere.",
    },
    "ci_cd": {
        "keywords": ["ci", "cd", "pipeline", "deploy", "build system", "automation", "devops"],
        "why": "Shipping software reliably requires automation: every commit tested, every merge deployed. CI/CD turns 'it works on my machine' into 'it works for everyone'.",
        "real_world": "GitHub Actions, GitLab CI, Jenkins — every professional repo runs pipelines for lint, test, build, and deploy.",
        "interview": [
            "Design a CI pipeline for a small service. What stages, in what order?",
            "How do you make a deployment safe to roll back?",
            "What is a blue-green deployment? Canary?",
        ],
        "build": "Build a 'Pipeline Runner': a tiny CI system that watches a folder, runs a list of commands in order, fails fast on error, and writes a build report.",
        "problem_set": "CS50-style: write a CI config for a repo that runs lint → unit tests → build → smoke test, and a deploy job gated on all passing.",
        "engineering": "Automation, reproducibility, and rollback safety are professional engineering core practices.",
        "career": "DevOps/SRE/platform, and expected of all senior backend roles.",
    },
    "system_design": {
        "keywords": ["system design", "architecture", "scalab", "load balanc", "cache", "shard", "microservice", "distributed", "message queue"],
        "why": "System design is how you scale from a weekend project to a product serving millions. It's the highest-weighted senior interview topic and the skill that earns principal-engineer titles.",
        "real_world": "Designing URL shorteners, chat apps, news feeds, rate limiters, distributed caches, and analytics pipelines.",
        "interview": [
            "Design a URL shortener that serves 100M users. Walk through traffic, storage, caching, and failover.",
            "How would you design a rate limiter? Where does it live?",
            "Design Twitter feed: how do you balance push vs pull?",
        ],
        "build": "Build a 'Design Doc Generator': a CLI that takes a product idea and scaffolds a design doc with capacity estimates, architecture diagram (ASCII), data model, and failure modes.",
        "problem_set": "CS50-style: take a small app's monolith and write a migration plan to services, with API contracts, data ownership, and a rollback plan.",
        "engineering": "Capacity planning, trade-off analysis, and operational thinking define senior+ engineering.",
        "career": "Senior+ SWE, architect, staff/principal roles.",
    },
    "performance": {
        "keywords": ["performance", "optimiz", "profil", "latency", "throughput", "cache", "benchmark"],
        "why": "Users feel speed. Understanding profiling, bottlenecks, and the cost of every operation lets you make products 10x faster with 10% of the effort — and know which 10%.",
        "real_world": "Slow API responses, janky UIs, cold starts, hot loops in data pipelines, database query latency.",
        "interview": [
            "A user reports slowness. How do you find the bottleneck?",
            "What is the difference between latency and throughput?",
            "How do you optimize a function that's called 1M times/sec?",
        ],
        "build": "Build a 'Micro-benchmark Harness' that times N function implementations across inputs, prints a table, and flags statistically significant differences.",
        "problem_set": "CS50-style: profile a 10k-iteration pipeline, identify the top-3 hot spots with a profiler, optimize each, and report before/after with evidence.",
        "engineering": "Profiling-driven optimization, caching strategies, and algorithmic improvements are daily senior work.",
        "career": "Backend, systems, game, and performance engineering.",
    },
    "software_engineering": {
        "keywords": ["software engineering", "refactor", "clean code", "code review", "architecture", "maintainab", "scalab"],
        "why": "Software engineering is writing code that others can read, extend, and operate for years. Refactoring, review, and clean architecture are how teams ship together without chaos.",
        "real_world": "Every long-lived codebase: monoliths being decomposed, libraries being maintained, and products that outlive their authors.",
        "interview": [
            "How do you refactor code without tests?",
            "What does 'clean code' mean to you? Give an example of improving something.",
            "How do you handle technical debt on a team?",
        ],
        "build": "Build a 'Refactoring Playground': take a messy code sample, apply a series of refactorings (rename, extract, guard clauses), and show before/after diffs with test continuity.",
        "problem_set": "CS50-style: a legacy 200-line function does 5 things. Extract to modules with tests, then write a short ADR documenting the change.",
        "engineering": "Code review, ADRs, and incremental refactoring are the daily mechanics of professional teams.",
        "career": "All senior roles; essential for staff/architect.",
    },
    # ── Web tracks ──────────────────────────────────────────
    "html": {
        "keywords": ["html", "markup", "semantic", "webpage", "element", "dom"],
        "why": "HTML is the skeleton of the web. Semantic, accessible markup is the foundation of SEO, screen-reader support, and maintainable sites.",
        "real_world": "Every web page, email templates, documentation, landing pages.",
        "interview": [
            "What is semantic HTML and why does it matter for accessibility and SEO?",
            "What's the difference between div, section, and article?",
            "How do you make an image-based page accessible?",
        ],
        "build": "Build a 'Semantic Blog Layout' with header/nav/main/article/footer, accessible forms, and keyboard-navigable menu — pure HTML, no CSS.",
        "problem_set": "CS50-style: take a non-semantic div-soup page and rebuild it with correct semantic structure passing an accessibility lint.",
        "engineering": "Accessibility (a11y) is a professional requirement, not an afterthought.",
        "career": "Frontend, full-stack, web accessibility roles.",
    },
    "css": {
        "keywords": ["css", "style", "flexbox", "grid", "responsive", "animation", "tailwind", "layout"],
        "why": "CSS is how products look and feel. Layout mastery (flexbox/grid), responsive design, and animation are core to every frontend feature.",
        "real_world": "Every responsive website, design systems, marketing pages, dashboards, mobile UIs.",
        "interview": [
            "How do you center a div? Give all the ways.",
            "Flexbox vs Grid: when do you use each?",
            "How do you make a site responsive without a framework?",
        ],
        "build": "Build a 'Design System Component Kit': buttons, cards, modals, and a responsive navbar with pure CSS (flexbox/grid + custom properties).",
        "problem_set": "CS50-style: rebuild a landing page from a screenshot using only CSS (no frameworks), matching the layout at 3 breakpoints.",
        "engineering": "Component-based styling, theming via CSS variables, and responsive correctness are production frontend skills.",
        "career": "Frontend, UI engineering, design systems.",
    },
    "sql": {
        "keywords": ["sql", "query", "select", "join", "where", "aggregate", "database", "relational"],
        "why": "SQL is the most durable, universal skill in tech. Queries, joins, and aggregations are how the world's data is actually interrogated.",
        "real_world": "Every analytics query, product database, reporting tool, and data pipeline.",
        "interview": [
            "Explain JOIN types with a concrete example.",
            "What is the difference between WHERE and HAVING?",
            "Write a query for the second-highest salary in a table.",
        ],
        "build": "Build a 'SQL Playground DB': create schema for orders/items/customers, seed it, and run 10 progressively harder queries ending with a grouped aggregation.",
        "problem_set": "CS50-style: given a 'movies' database, answer a series of analytical queries (joins, subqueries, GROUP BY) and optimize the slowest with an index.",
        "engineering": "Query optimization, indexing, and data integrity are core backend/data skills.",
        "career": "Backend, data analyst/engineer, full-stack.",
    },
    "typescript": {
        "keywords": ["typescript", "type", "interface", "generic", "enum", "union"],
        "why": "Types catch whole classes of bugs before runtime. TypeScript gives JavaScript the safety rails that make large codebases shippable.",
        "real_world": "Every modern frontend framework, large JS codebases, SDK design, full-stack shared types.",
        "interview": [
            "What is the difference between interface and type?",
            "How do you model a discriminated union?",
            "What is a generic and when do you reach for it?",
        ],
        "build": "Build a 'Typed API Client': define TypeScript interfaces for an API, a generic request helper, and strict response validation.",
        "problem_set": "CS50-style: take a 500-line untyped JS module and add strict types, catching 5 latent bugs the compiler now prevents.",
        "engineering": "Type safety is a maintainability and reliability tool for teams of any size.",
        "career": "Frontend, full-stack, and API development.",
    },
    "react": {
        "keywords": ["react", "component", "hook", "props", "state", "context", "jsx"],
        "why": "React's component model — state, props, hooks — is how most of the web is built. Understanding re-renders and state management is core frontend competence.",
        "real_world": "Web apps, dashboards, e-commerce UIs, design systems, mobile (React Native).",
        "interview": [
            "When does a component re-render? How do you optimize?",
            "What is the difference between useEffect and useLayoutEffect?",
            "Controlled vs uncontrolled inputs?",
        ],
        "build": "Build a 'Task Dashboard' with React: components, state, forms, and localStorage persistence — no external state library.",
        "problem_set": "CS50-style: build a weather app fetching from an API, with loading/error/empty states, caching, and a debounced search.",
        "engineering": "Component architecture, performance (memoization), and state design are production React skills.",
        "career": "Frontend and full-stack roles.",
    },
    "node": {
        "keywords": ["node", "express", "server", "backend js", "npm", "middleware", "event loop"],
        "why": "Node brings JS to the server, and its event loop model powers high-concurrency I/O services. It's the glue of the modern full-stack ecosystem.",
        "real_world": "APIs, real-time apps, build tooling, serverless functions, CLI tools.",
        "interview": [
            "How does the Node event loop work? What blocks it?",
            "What is middleware in Express? How does it compose?",
            "How do you handle unhandled promise rejections in production?",
        ],
        "build": "Build an 'Express Notes API' with middleware (logging, auth, error handler), validation, and a health endpoint — deployable.",
        "problem_set": "CS50-style: build a REST API for a blog with auth, pagination, rate limiting, and a test suite hitting it end-to-end.",
        "engineering": "Async correctness, middleware design, and production-grade error handling are core Node skills.",
        "career": "Full-stack and backend roles.",
    },
    # ── Domain / advanced tracks ────────────────────────────
    "ai_ml": {
        "keywords": ["ai", "machine learning", "model", "neural", "training", "inference", "llm", "prompt"],
        "why": "AI is now a core engineering surface: integrating models, engineering prompts, evaluating outputs, and building AI features safely. Understanding the stack makes you an AI-literate engineer.",
        "real_world": "Chatbots, RAG assistants, recommendations, content moderation, code completion, image generation.",
        "interview": [
            "Explain how RAG works and when you'd use it.",
            "How do you evaluate an LLM response? What metrics matter?",
            "What are hallucinations and how do you mitigate them in production?",
        ],
        "build": "Build a 'RAG Knowledge Bot': ingest documents, chunk them, embed, store, retrieve, and answer with sources — a real deployable AI feature.",
        "problem_set": "CS50-style: build an evaluation harness that scores your RAG bot on 50 questions and reports precision/recall.",
        "engineering": "AI features have their own engineering concerns: cost, latency, safety, and evaluation.",
        "career": "ML/AI engineers, AI product engineers, full-stack building AI features.",
    },
    "cloud": {
        "keywords": ["cloud", "aws", "azure", "gcp", "deploy", "serverless", "container", "kubernetes", "docker"],
        "why": "Almost everything ships on cloud infrastructure now. Understanding containers, deployments, and the operational surface is required to build products that actually run.",
        "real_world": "Every deployed service: Docker images, Kubernetes clusters, serverless functions, managed databases, CDN/edge.",
        "interview": [
            "Docker vs VM: what's actually different?",
            "How do you deploy a service with zero downtime?",
            "What is a managed service vs self-managed, and when do you pick each?",
        ],
        "build": "Build a 'Dockerized App': Dockerfile for a small service, compose file with a database, health checks, and a zero-downtime deploy note.",
        "problem_set": "CS50-style: containerize an existing app, add multi-stage builds to shrink the image, and write a docker-compose with volumes + env config.",
        "engineering": "Deployment reproducibility and operational awareness are senior-expected skills.",
        "career": "DevOps/SRE, backend, platform, cloud engineers.",
    },
    "observability": {
        "keywords": ["observability", "log", "metric", "monitor", "alert", "tracing", "dashboard", "slo"],
        "why": "You can't fix what you can't see. Logs, metrics, traces, and alerts are how teams keep production healthy and detect problems before users do.",
        "real_world": "Every production system: dashboards, paging alerts, SLOs, incident post-mortems.",
        "interview": [
            "A service is failing intermittently. What logs/metrics/traces do you add?",
            "What's the difference between logging, metrics, and tracing?",
            "How do you set an alert that doesn't wake you up for noise?",
        ],
        "build": "Build a 'Health Dashboard': an app that exposes /healthz and /metrics, plus a script that scrapes and graphs latency over time.",
        "problem_set": "CS50-style: instrument a small service with structured logs and request tracing, then write an alert rule that fires on p95 > 500ms and self-resolves.",
        "engineering": "Instrumentation, SLOs, and incident response are the operating layer of professional software.",
        "career": "SRE, platform, backend, and on-call engineers.",
    },
    "interview_prep": {
        "keywords": ["interview", "behavioral", "star", "system design interview", "live coding", "resume", "negotiat"],
        "why": "Technical skill gets you shortlisted; interview technique gets you hired. Behavioral stories (STAR), live-coding fluency, and system-design thinking are trainable — and this module makes you train them.",
        "real_world": "Phone screens, onsites, take-homes, behavioral rounds, and offer negotiation — every step of landing a job.",
        "interview": [
            "Tell me about a time you disagreed with a colleague. (STAR)",
            "Walk me through your most technically difficult project.",
            "How do you handle being wrong about an estimate in production?",
        ],
        "build": "Build a 'Personal Interview Prep Tracker': log your STAR stories, track which are practiced, run a mock-interview timer, and score your delivery.",
        "problem_set": "CS50-style: write 10 STAR stories from real projects, then deliver a 2-minute version of each and record + self-grade against a rubric.",
        "engineering": "Communicating technical decisions, giving clear explanations, and receiving feedback are daily professional skills, not just interview ones.",
        "career": "Every candidate, at every level.",
    },
}


# ============================================================
# LESSON-TYPE FALLBACKS
# ============================================================

TYPE_FALLBACK = {
    "theory": {
        "why": "Concepts are the map; code is the territory. This lesson builds the mental model you'll lean on whenever you touch a real codebase that uses this idea.",
        "real_world": "This concept appears in everyday software: web backends, mobile apps, data pipelines, and developer tooling all rely on it.",
        "interview": [
            "Explain this concept to a non-technical stakeholder.",
            "When would you NOT use this approach? What are the trade-offs?",
            "How does this concept behave at scale (1M users)?",
        ],
        "build": "Build a 10-line demo that uses this concept, wrapped in a tiny CLI you can run and show to someone.",
        "problem_set": "Explain the concept in 3 sentences, then write a small program that demonstrates it with a real input and observable output.",
        "engineering": "Every production system is this concept applied under constraints — knowing the why lets you apply it correctly.",
        "career": "Foundation for backend, frontend, and data engineering alike.",
    },
    "practice": {
        "why": "You only really learn by doing. This practice builds muscle memory so the concept is automatic when you're under interview pressure.",
        "real_world": "These exact skills are used daily: writing functions, manipulating data, and reading others' code.",
        "interview": [
            "What did this exercise teach you about edge cases?",
            "How would you make your solution handle 100x more data?",
            "Show me your solution and explain each line's purpose.",
        ],
        "build": "Turn the practice into a scripted exercise file (input → expected output) that a teammate can run and check.",
        "problem_set": "Given this practice, add 3 more edge cases and verify the solution passes all of them.",
        "engineering": "Deliberate practice is how engineering competence is actually built; this is the reps that matter.",
        "career": "Builds the problem-solving muscle every interview and code review tests.",
    },
    "challenge": {
        "why": "Challenges simulate the hard 10% of interviews and production debugging: constrained, time-pressured, and unforgiving.",
        "real_world": "Real tickets are just challenges with a customer attached: a query is slow, a payload is malformed, an edge case crashes.",
        "interview": [
            "What is the time and space complexity of your solution?",
            "What are the edge cases you handled and which did you skip?",
            "How would a teammate review this solution?",
        ],
        "build": "Package the challenge as a runnable solution file with tests proving it against the given constraints.",
        "problem_set": "Solve the challenge, then write a test harness with 5 hidden edge cases and make sure all pass.",
        "engineering": "Challenges are the raw material of technical interviews and the daily puzzle of debugging.",
        "career": "Interview performance and debugging skill are the two biggest career levers.",
    },
    "project": {
        "why": "A shipped project is proof, not promise. This is how you demonstrate to an employer that you can go from blank file to working artifact.",
        "real_world": "This project type mirrors real deliverables: tools, services, and dashboards that someone would actually run.",
        "interview": [
            "Walk me through this project's architecture and your decisions.",
            "What would you do differently if you shipped it to 1M users?",
            "What was the hardest bug you hit building this?",
        ],
        "build": "This IS the build. Finish it, commit it, and add a README with setup + a screenshot or demo.",
        "problem_set": "Add a stretch goal to the project (auth, pagination, tests, deployment) and ship it.",
        "engineering": "Portfolio projects are how you prove engineering judgment beyond what an interview can test.",
        "career": "Your portfolio is the strongest evidence on your resume.",
    },
    "quiz": {
        "why": "Quizzes expose gaps in understanding that feel 'known' until tested. Retrieval is the strongest memory technique there is.",
        "real_world": "Technical screening quizzes and certification exams test exactly this retention.",
        "interview": [
            "Explain the correct answer to the one you got wrong.",
            "How would you explain the concept behind any of these questions to a junior?",
            "What question would you add to this quiz?",
        ],
        "build": "Build a flashcards file for the quiz questions and run through it spaced-repetition style.",
        "problem_set": "Write 5 original questions for a peer on this topic, with explanations.",
        "engineering": "Retention of fundamentals makes you faster in reviews, debugging, and interviews.",
        "career": "Certs, screenings, and every interview trivia round.",
    },
    "boss": {
        "why": "Boss battles consolidate everything you've learned into a single integrated challenge — the real shape of production work, which always combines many skills at once.",
        "real_world": "Production incidents and feature launches never test one skill in isolation; they demand integration, exactly like this.",
        "interview": [
            "Explain how everything you've learned so far combines in this battle.",
            "What's the weakest link in your current understanding?",
            "How would you teach this to someone one level behind you?",
        ],
        "build": "Complete the integrated capstone and commit it as your proof-of-mastery artifact.",
        "problem_set": "Re-solve the boss battle with stricter constraints (less memory, tighter time, more input).",
        "engineering": "Integration is the difference between knowing topics and being an engineer.",
        "career": "Capstones are the strongest portfolio pieces.",
    },
}


# ============================================================
# LESSON TITLE → CONCEPT MATCHING
# ============================================================

def _normalize(text: str) -> str:
    return (text or "").lower()


def _match_concept(title: str, level_name: str = "", description: str = "") -> str:
    """Find the best-matching concept for a lesson."""
    haystack = _normalize(title) + " " + _normalize(level_name) + " " + _normalize(description)
    best_key, best_hits = None, 0
    for key, meta in CONCEPT_META.items():
        hits = sum(1 for kw in meta["keywords"] if kw.lower() in haystack)
        if hits > best_hits:
            best_key, best_hits = key, hits
    return best_key


def _lesson_meta(lesson: dict, level_name: str, level_description: str) -> dict:
    """Build the world-class metadata fields for a single lesson."""
    concept_key = _match_concept(lesson.get("title", ""), level_name, level_description)
    base = CONCEPT_META.get(concept_key) or TYPE_FALLBACK.get(
        lesson.get("type", "theory"), TYPE_FALLBACK["theory"]
    )

    ltype = lesson.get("type", "theory")
    title = lesson.get("title", "")

    # The 'build' must always be project-shaped and specific to THIS lesson.
    build = base["build"]
    if ltype == "boss":
        build = f"Grand challenge: complete the integrated capstone covering {title} end-to-end, commit it, and demo it. This is your mastery proof."
    elif ltype == "project":
        build = f"Ship this project ({title}) to a working state: code, tests, README with setup instructions, and a screenshot or demo link."

    return {
        "why": base["why"],
        "real_world": base["real_world"],
        "interview": base["interview"],
        "build": build,
        "problem_set": base["problem_set"],
        "engineering": base["engineering"],
        "career": base["career"],
        "concept_key": concept_key,
    }


# ============================================================
# LEVEL-LEVEL METADATA (capstone + interview + real-world track)
# ============================================================

LEVEL_META = {
    "interview": [
        "Which interview questions from this level would you struggle to answer? Practice those aloud.",
        "Explain one concept from this level to a complete beginner — that explanation IS the interview.",
        "Pick one project from this level and prepare a 2-minute STAR story about it.",
    ],
    "career": "Completing this level adds one entry to your portfolio and one bullet to your resume. Keep a running 'Levels → Skills' log.",
    "capstone": "Combine 3+ concepts from this level into one integrated mini-app and deploy it somewhere reachable.",
}


# ============================================================
# THE BIG ENRICHMENT PASS
# ============================================================

def install_world_class_curriculum():
    """Enrich every lesson + level in LANGUAGES with world-class metadata.

    Idempotent — safe to call multiple times. Adds:
      lesson:  why, real_world, interview, build, problem_set, engineering, career, concept_key
      level:   interview_prep, career_mapping, capstone_challenge
    """
    for lang_id, lang in LANGUAGES.items():
        levels = lang.get("levels", {})
        for level in levels.values():
            # Level-level metadata
            level["interview_prep"] = LEVEL_META["interview"]
            level["career_mapping"] = LEVEL_META["career"]
            level["capstone_challenge"] = LEVEL_META["capstone"]

            level_name = level.get("name", "")
            level_desc = level.get("description", "")
            for lesson in level.get("lessons", []):
                if "why" not in lesson:  # idempotent: only add once
                    lesson.update(_lesson_meta(lesson, level_name, level_desc))

    return LANGUAGES


# ============================================================
# TRACK/ROLE ACCESSIBILITY + PORTFOLIO MAP
# ============================================================

def get_curriculum_summary():
    """Return a summary of the enriched curriculum (for dashboard/analytics)."""
    total_lessons = 0
    total_projects = 0
    total_interview_qs = 0
    by_language = {}

    for lang_id, lang in LANGUAGES.items():
        lang_lessons = 0
        lang_projects = 0
        for level in lang.get("levels", {}).values():
            for lesson in level.get("lessons", []):
                lang_lessons += 1
                if lesson.get("type") in ("project", "challenge", "boss") or lesson.get("build"):
                    lang_projects += 1
                total_interview_qs += len(lesson.get("interview", []))
        total_lessons += lang_lessons
        total_projects += lang_projects
        by_language[lang_id] = {
            "total_lessons": lang_lessons,
            "project_lessons": lang_projects,
        }

    return {
        "world_class_curriculum": True,
        "version": "1.0.0",
        "total_lessons": total_lessons,
        "project_lessons": total_projects,
        "interview_questions": total_interview_qs,
        "by_language": by_language,
    }


# ============================================================
# Auto-install (matches the existing curriculum_* module pattern)
# ============================================================

_ = install_world_class_curriculum()
