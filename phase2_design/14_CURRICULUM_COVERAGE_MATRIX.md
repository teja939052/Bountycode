# 14 CURRICULUM COVERAGE MATRIX

**BountyCode — Phase 2B Scope-Completeness Review**
**Status: Design-only document**
**No application code written**

---

## 1. Purpose

Produce a curriculum coverage matrix mapping every founder domain to its complete concept inventory:

`Domain → Subject → Concept → Skill ID → Prerequisite → Lesson → Interaction → Assessment → Evidence → Revision/Transfer → Release`

This document establishes complete coverage and identifies where V1 launch scope ends and roadmap begins.

This is a design document. No implementation is authorized.

---

## 2. Domain → Subject → Concept → Skill ID Matrix

### 2.1 Domain: Quantitative Aptitude (World 1 — V1)

| Subject | Concept | Skill ID | Prerequisite | Lesson | Interaction | Assessment | Evidence | Revision/Transfer | Release |
|---------|---------|----------|--------------|--------|-------------|------------|----------|-------------------|---------|
| Percentages | Basics | `aptitude.quantitative.percentages` | None | Percentages basics | Manipulate | Deterministic numeric | SRS | Increased/decreased variants | V1 |
| Percentages | Increase/Decrease | `aptitude.quantitative.percent_change` | Percentages basics | Interactive lesson | Fill | Exact answer | SRS | Markup/markdown variants | V1 |
| Percentages | Successive | `aptitude.quantitative.successive` | Percent change | Interactive lesson | Manipulate | Deterministic | SRS | Compound variants | V1 |
| Ratios | Basics | `aptitude.quantitative.ratios` | None | Easy | Manipulate | Deterministic | SRS | Recipe scaling | V1 |
| Ratios | Proportion | `aptitude.quantitative.proportion` | Ratios | Easy | Fill | Exact | SRS | Recipe variants | V1 |
| Profit/Loss | Basics | `aptitude.quantitative.profit_loss` | Percentages | Easy | Fill | Exact | SRS | Markup variants | V1 |
| Profit/Loss | Discount | `aptitude.quantitative.discount` | Profit/Loss | Easy | Fill | Exact | SRS | Multiple discount | V1 |
| Averages | Basics | `aptitude.quantitative.averages` | None | Easy | Manipulate | Deterministic | SRS | Weighted average | V1 |
| Time & Work | Basics | `aptitude.quantitative.time_work` | Ratios | Medium | Manipulate | Deterministic | SRS | Pipe/cistern | V1 |
| Time Speed Distance | Basics | `aptitude.quantitative.tsd` | Averages | Medium | Manipulate | Deterministic | SRS | Upstream/downstream | V1 |
| SI/CI | Basics | `aptitude.quantitative.si_ci` | Percentages | Medium | Manipulate | Deterministic | SRS | Varying periods | V1 |
| Number Series | Basics | `aptitude.quantitative.number_series` | None | Easy | Arrange | Pattern match | SRS | Different series family | V1 |

### 2.2 Domain: Logical Reasoning (World 2 — V1)

| Subject | Concept | Skill ID | Prerequisite | Lesson | Interaction | Assessment | Evidence | Revision/Transfer | Release |
|---------|---------|----------|--------------|--------|-------------|------------|----------|-------------------|---------|
| Blood Relations | Basics | `aptitude.logical.blood_relations` | None | Easy | Arrange | Family tree | SRS | Extended family | V1 |
| Syllogism | Basics | `aptitude.logical.syllogism` | None | Medium | Arrange | Venn match | SRS | New premises | V1 |
| Coding-Decoding | Basics | `aptitude.logical.coding_decoding` | None | Medium | Fill | Decode exact | SRS | Different cipher | V1 |
| Directions | Basics | `aptitude.logical.directions` | None | Easy | Manipulate | Coordinate | SRS | Multi-step path | V1 |
| Seating | Basics | `aptitude.logical.seating` | None | Hard | Arrange | Constraint | SRS | Circular vs linear | V1 |
| Series | Basics | `aptitude.logical.series` | None | Medium | Predict | Next element | SRS | Alternate pattern | V1 |
| Data Sufficiency | Basics | `aptitude.logical.data_sufficiency` | None | Hard | Select | Sufficient/Not | SRS | New statements | V1 |

### 2.3 Domain: Verbal Ability (World 3 — V1)

| Subject | Concept | Skill ID | Prerequisite | Lesson | Interaction | Assessment | Evidence | Revision/Transfer | Release |
|---------|---------|----------|--------------|--------|-------------|------------|----------|-------------------|---------|
| Grammar | Basics | `aptitude.verbal.grammar` | None | Easy | Fill | Exact match | SRS | New sentence | V1 |
| Reading Comprehension | Basics | `aptitude.verbal.reading` | None | Medium | Select | Answer key | SRS | New passage | V1 |
| Para Jumble | Basics | `aptitude.verbal.para_jumble` | None | Medium | Arrange | Order match | SRS | New set | V1 |
| Sentence Correction | Basics | `aptitude.verbal.sentence_correction` | Grammar | Medium | Select | Corrected | SRS | New errors | V1 |
| Vocabulary | Basics | `aptitude.verbal.vocabulary` | None | Easy | Select | Synonym | SRS | New words | V1 |
| Email Format | Basics | `aptitude.verbal.email_format` | None | Easy | Fill | Structure | SRS | Different email | V1 |

### 2.4 Domain: Programming Logic / Pseudocode (World 4 — V1 Differentiator)

| Subject | Concept | Skill ID | Prerequisite | Lesson | Interaction | Assessment | Evidence | Revision/Transfer | Release |
|---------|---------|----------|--------------|--------|-------------|------------|----------|-------------------|---------|
| Trace Variables | Basics | `pseudo.trace_variables` | None | Easy | Trace | Variable state | SRS | Different values | V1 |
| Predict Output | Basics | `pseudo.predict_output` | Trace Variables | Medium | Predict | Exact output | SRS | Different snippet | V1 |
| Loops | Basics | `pseudo.loops` | Trace Variables | Easy | Manipulate | Loop output | SRS | Different bounds | V1 |
| Nested Loops | Basics | `pseudo.nested_loops` | Loops | Medium | Trace | Pattern output | SRS | Different pattern | V1 |
| Arrays | Basics | `pseudo.arrays` | Nested Loops | Easy | Manipulate | Index output | SRS | Different array | V1 |
| Conditions | Basics | `pseudo.conditions` | Arrays | Easy | Select | Branch output | SRS | Different conditions | V1 |
| Functions | Basics | `pseudo.functions` | Conditions | Medium | Fill | Return value | SRS | Different params | V1 |
| Recursion Basics | Basics | `pseudo.recursion` | Functions | Hard | Trace | Call stack | SRS | Different recursion | V1 |
| Debugging | Basics | `pseudo.debugging` | Recursion | Medium | Debug | Test cases | SRS | Different bug | V1 |

### 2.5 Domain: Data Structures & Algorithms (World 5 — Service-Level Only, V1)

| Subject | Concept | Skill ID | Prerequisite | Lesson | Interaction | Assessment | Evidence | Revision/Transfer | Release |
|---------|---------|----------|--------------|--------|-------------|------------|----------|-------------------|---------|
| Arrays | Basics | `dsa.arrays` | Pseudo Arrays | Easy | Manipulate | Index/output | SRS | Different array | V1 |
| Strings | Basics | `dsa.strings` | Arrays | Easy | Manipulate | String output | SRS | Different string | V1 |
| Hashing | Basics | `dsa.hashing` | Arrays | Medium | Manipulate | Collision | SRS | Different hash | V1 |
| Two Pointers | Basics | `dsa.two_pointers` | Arrays | Medium | Manipulate | Pair output | SRS | Different target | V1 |
| Sliding Window | Basics | `dsa.sliding_window` | Two Pointers | Medium | Manipulate | Max sum | SRS | Different window | V1 |
| Sorting | Basics | `dsa.sorting` | Arrays | Easy | Arrange | Sorted array | SRS | Different sort | V1 |
| Binary Search | Basics | `dsa.binary_search` | Sorting | Medium | Predict | Index/output | SRS | Different target | V1 |
| Stack/Queue Basics | Basics | `dsa.stack_queue` | Arrays | Easy | Manipulate | Output order | SRS | Different ops | V1 |
| Linked List Basics | Basics | `dsa.linked_list` | Arrays | Medium | Trace | Traversal | SRS | Different list | V1 |
| Tree Basics | Basics | `dsa.trees` | Linked List | Medium | Trace | Traversal | SRS | Different tree | V1 |
| Heap | Basics | `dsa.heap` | Trees | Hard | Trace | Heapify | SRS | Different heap | Roadmap |
| Graph | Basics | `dsa.graph` | Trees | Hard | Trace | Traversal | SRS | Different graph | Roadmap |
| Recursion | Basics | `dsa.recursion` | Pseudo Recursion | Hard | Trace | Call stack | SRS | Different recursion | Roadmap |
| Greedy | Basics | `dsa.greedy` | Graph | Hard | Fill | Greedy choice | SRS | Different problem | Roadmap |
| Backtracking | Basics | `dsa.backtracking` | Recursion | Hard | Arrange | Solution path | SRS | Different problem | Roadmap |
| Dynamic Programming | Basics | `dsa.dp` | Recursion | Hard | Fill | DP table | SRS | Different problem | Roadmap |

### 2.6 Domain: SQL and Databases (Roadmap)

| Subject | Concept | Skill ID | Prerequisite | Lesson | Interaction | Assessment | Evidence | Revision/Transfer | Release |
|---------|---------|----------|--------------|--------|-------------|------------|----------|-------------------|---------|
| Query Writing | SELECT | `cs_fundamentals.databases.sql.query` | None | Easy | Fill | Exact output | SRS | Different table | Roadmap |
| Joins | INNER/LEFT/RIGHT | `cs_fundamentals.databases.sql.joins` | Query | Medium | Manipulate | Join result | SRS | Different join | Roadmap |
| Aggregations | GROUP BY | `cs_fundamentals.databases.sql.aggregations` | Query | Easy | Select | Aggregate | SRS | Different group | Roadmap |
| Subqueries | Nested SELECT | `cs_fundamentals.databases.sql.subqueries` | Aggregations | Medium | Fill | Subquery output | SRS | Different nesting | Roadmap |
| CTEs | WITH clause | `cs_fundamentals.databases.sql.ctes` | Subqueries | Hard | Fill | CTE output | SRS | Different CTE | Roadmap |
| Window Functions | ROW_NUMBER/RANK | `cs_fundamentals.databases.sql.window` | CTEs | Hard | Fill | Window output | SRS | Different window | Roadmap |
| Data Modification | INSERT/UPDATE/DELETE | `cs_fundamentals.databases.sql.dml` | Query | Easy | Fill | Row count | SRS | Different data | Roadmap |
| Constraints/Keys | PK/FK/CHECK | `cs_fundamentals.databases.sql.constraints` | DML | Easy | Select | Constraint match | SRS | Different schema | Roadmap |
| Normalization | 1NF/2NF/3NF | `cs_fundamentals.databases.sql.normalization` | Constraints | Medium | Select | Normal form | SRS | Different schema | Roadmap |
| Indexes | B-tree/Hash | `cs_fundamentals.databases.sql.indexes` | Normalization | Medium | Select | Index match | SRS | Different index | Roadmap |
| Transactions | ACID | `cs_fundamentals.databases.sql.transactions` | Indexes | Hard | Select | Commit/rollback | SRS | Different scenario | Roadmap |

### 2.7 Domain: Computer Science Fundamentals (Roadmap)

| Subject | Concept | Skill ID | Prerequisite | Lesson | Interaction | Assessment | Evidence | Revision/Transfer | Release |
|---------|---------|----------|--------------|--------|-------------|------------|----------|-------------------|---------|
| OOP | Basics | `cs_fundamentals.oop` | Programming fundamentals | Medium | MCQ + code | Test cases | SRS | Different language | Roadmap |
| DBMS | Basics | `cs_fundamentals.databases.theory` | None | Easy | MCQ | Concept match | SRS | Different scenario | Roadmap |
| Operating Systems | Basics | `cs_fundamentals.os` | None | Medium | MCQ | Concept match | SRS | Different scenario | Roadmap |
| Computer Networks | Basics | `cs_fundamentals.networks` | OS | Medium | MCQ | Concept match | SRS | Different scenario | Roadmap |
| Software Engineering | Basics | `cs_fundamentals.se` | None | Easy | MCQ + case | Case match | SRS | Different case | Roadmap |
| Testing | Basics | `cs_fundamentals.testing` | SE | Medium | MCQ + code | Test cases | SRS | Different code | Roadmap |

### 2.8 Domain: Four Programming Languages (Roadmap)

#### 2.8.1 C Programming Track

| Concept | Skill ID | Prerequisite | Difficulty | Interaction | Assessment | Evidence | Revision/Transfer | Release |
|---------|----------|--------------|------------|-------------|------------|----------|-------------------|---------|
| Variables/Types | `coding.c.fundamentals.variables` | None | Easy | Fill | Exact | SRS | Different values | Roadmap |
| Operators | `coding.c.fundamentals.operators` | Variables | Easy | Manipulate | Deterministic | SRS | Different ops | Roadmap |
| Conditions | `coding.c.fundamentals.conditions` | Operators | Easy | Select | Branch match | SRS | Different conditions | Roadmap |
| Loops | `coding.c.fundamentals.loops` | Conditions | Medium | Trace | Loop output | SRS | Different bounds | Roadmap |
| Functions | `coding.c.fundamentals.functions` | Loops | Medium | Fill | Return value | SRS | Different params | Roadmap |
| Arrays | `coding.c.arrays` | Functions | Medium | Manipulate | Index/output | SRS | Different array | Roadmap |
| Strings | `coding.c.strings` | Arrays | Medium | Manipulate | String output | SRS | Different string | Roadmap |
| Pointers/Memory | `coding.c.pointers.memory` | Arrays | Hard | Trace | Address/output | SRS | Different address | Roadmap |
| Dynamic Memory | `coding.c.memory.dynamic` | Pointers | Hard | Trace | Leak/output | SRS | Different scenario | Roadmap |
| Structures | `coding.c.structures` | Pointers | Medium | Fill | Struct output | SRS | Different struct | Roadmap |
| File I/O | `coding.c.file_io` | Structures | Easy | Fill | Output match | SRS | Different file | Roadmap |
| Preprocessor | `coding.c.preprocessor` | None | Easy | Select | Output match | SRS | Different directive | Roadmap |
| Debugging C | `coding.c.debugging` | Pointers | Hard | Debug | Test cases pass | SRS | Different bug | Roadmap |
| DSA in C | `coding.c.dsa_implementations` | Pointers + Arrays | Hard | Implement | Test cases pass | SRS | Different problem | Roadmap |
| Algorithms in C | `coding.c.algo_implementations` | DSA in C | Hard | Implement | Test cases pass | SRS | Different problem | Roadmap |
| Timed C Practice | `coding.c.timed_practice` | DSA in C | Hard | Implement | Hidden tests pass | SRS | Different problem | Roadmap |

#### 2.8.2 C++ Programming Track

| Concept | Skill ID | Prerequisite | Difficulty | Interaction | Assessment | Evidence | Revision/Transfer | Release |
|---------|----------|--------------|------------|-------------|------------|----------|-------------------|---------|
| C++ Fundamentals | `cpp.fundamentals` | C fundamentals | Easy | Fill | Exact match | SRS | Different values | Roadmap |
| References | `cpp.fundamentals.references` | Pointers | Medium | Trace | Address/output | SRS | Different refs | Roadmap |
| OOP Classes | `cpp.oop.classes` | Functions | Medium | Fill | Class output | SRS | Different class | Roadmap |
| Constructors/Destructors | `cpp.oop.constructors` | Classes | Medium | Trace | Lifecycle | SRS | Different class | Roadmap |
| Inheritance | `cpp.oop.inheritance` | Classes | Hard | Fill | Output match | SRS | Different hierarchy | Roadmap |
| Polymorphism | `cpp.oop.polymorphism` | Inheritance | Hard | Trace | Virtual dispatch | SRS | Different virtual | Roadmap |
| Encapsulation | `cpp.oop.encapsulation` | Classes | Medium | Select | Access match | SRS | Different access | Roadmap |
| STL Containers | `cpp.stl.containers` | OOP | Medium | Manipulate | Output match | SRS | Different container | Roadmap |
| STL Algorithms | `cpp.stl.algorithms` | Containers | Medium | Fill | Output match | SRS | Different algorithm | Roadmap |
| Smart Pointers | `cpp.stl.smart_pointers` | Pointers | Hard | Trace | Lifecycle | SRS | Different scenario | Roadmap |
| Templates | `cpp.templates` | OOP | Hard | Fill | Instantiation | SRS | Different type | Roadmap |
| Exceptions | `cpp.exceptions` | OOP | Medium | Fill | Output match | SRS | Different exception | Roadmap |
| Move Semantics | `cpp.move_semantics` | Smart pointers | Hard | Trace | Lifecycle | SRS | Different move | Roadmap |
| Debugging C++ | `cpp.debugging` | OOP + STL | Hard | Debug | Test cases pass | SRS | Different bug | Roadmap |
| DSA in C++ | `cpp.dsa_implementations` | STL + OOP | Hard | Implement | Test cases pass | SRS | Different problem | Roadmap |
| Algorithms in C++ | `cpp.algo_implementations` | DSA in C++ | Hard | Implement | Test cases pass | SRS | Different problem | Roadmap |
| Timed C++ Practice | `cpp.timed_practice` | DSA in C++ | Hard | Implement | Hidden tests pass | SRS | Different problem | Roadmap |

#### 2.8.3 Python Programming Track

| Concept | Skill ID | Prerequisite | Difficulty | Interaction | Assessment | Evidence | Revision/Transfer | Release |
|---------|----------|--------------|------------|-------------|------------|----------|-------------------|---------|
| Python Fundamentals | `python.fundamentals` | None | Easy | Fill | Exact match | SRS | Different values | Roadmap |
| Dynamic Typing | `python.fundamentals.dynamic_types` | Fundamentals | Easy | Manipulate | Type output | SRS | Different types | Roadmap |
| Conditions | `python.fundamentals.conditions` | Dynamic types | Easy | Select | Branch match | SRS | Different conditions | Roadmap |
| Loops | `python.fundamentals.loops` | Conditions | Medium | Trace | Loop output | SRS | Different bounds | Roadmap |
| Functions | `python.fundamentals.functions` | Loops | Medium | Fill | Return value | SRS | Different params | Roadmap |
| Lists | `python.collections.lists` | Functions | Medium | Manipulate | List output | SRS | Different list | Roadmap |
| Dictionaries | `python.collections.dicts` | Lists | Medium | Manipulate | Dict output | SRS | Different dict | Roadmap |
| Sets | `python.collections.sets` | Dictionaries | Easy | Manipulate | Set output | SRS | Different set | Roadmap |
| Tuples | `python.collections.tuples` | Lists | Easy | Select | Immutable match | SRS | Different tuple | Roadmap |
| String Methods | `python.collections.strings` | Lists | Easy | Manipulate | Output match | SRS | Different string | Roadmap |
| Exceptions | `python.exceptions` | Functions | Medium | Fill | Output match | SRS | Different exception | Roadmap |
| Classes/OOP | `python.oop` | Functions | Medium | Fill | Class output | SRS | Different class | Roadmap |
| List Comprehensions | `python.collections.comprehensions` | Lists | Medium | Fill | List output | SRS | Different comprehension | Roadmap |
| Generators | `python.generators` | Functions | Hard | Trace | Yield output | SRS | Different generator | Roadmap |
| Decorators | `python.decorators` | Functions | Hard | Fill | Wrapper output | SRS | Different decorator | Roadmap |
| File I/O | `python.file_io` | Functions | Easy | Fill | Output match | SRS | Different file | Roadmap |
| Debugging Python | `python.debugging` | OOP + Exceptions | Hard | Debug | Test cases pass | SRS | Different bug | Roadmap |
| DSA in Python | `python.dsa_implementations` | Collections + OOP | Hard | Implement | Test cases pass | SRS | Different problem | Roadmap |
| Algorithms in Python | `python.algo_implementations` | DSA in Python | Hard | Implement | Test cases pass | SRS | Different problem | Roadmap |
| Timed Python Practice | `python.timed_practice` | DSA in Python | Hard | Implement | Hidden tests pass | SRS | Different problem | Roadmap |

#### 2.8.4 Java Programming Track

| Concept | Skill ID | Prerequisite | Difficulty | Interaction | Assessment | Evidence | Revision/Transfer | Release |
|---------|----------|--------------|------------|-------------|------------|----------|-------------------|---------|
| Java Fundamentals | `java.fundamentals` | None | Easy | Fill | Exact match | SRS | Different values | Roadmap |
| Classes/Objects | `java.oop.classes` | Fundamentals | Medium | Fill | Object state | SRS | Different class | Roadmap |
| Constructors | `java.oop.constructors` | Classes | Medium | Trace | Lifecycle | SRS | Different class | Roadmap |
| Inheritance | `java.oop.inheritance` | Classes | Hard | Fill | Output match | SRS | Different hierarchy | Roadmap |
| Polymorphism | `java.oop.polymorphism` | Inheritance | Hard | Trace | Virtual dispatch | SRS | Different virtual | Roadmap |
| Interfaces | `java.oop.interfaces` | Polymorphism | Medium | Fill | Contract match | SRS | Different interface | Roadmap |
| Abstract Classes | `java.oop.abstract` | Inheritance | Medium | Fill | Instantiation rule | SRS | Different abstract | Roadmap |
| Encapsulation | `java.oop.encapsulation` | Classes | Medium | Select | Access match | SRS | Different access | Roadmap |
| Exceptions | `java.exceptions` | OOP | Medium | Fill | Output match | SRS | Different exception | Roadmap |
| Collections Framework | `java.collections` | OOP | Medium | Manipulate | Output match | SRS | Different collection | Roadmap |
| ArrayList/LinkedList | `java.collections.list` | Collections | Medium | Manipulate | Output match | SRS | Different list | Roadmap |
| HashMap/HashSet | `java.collections.map_set` | Collections | Medium | Manipulate | Output match | SRS | Different map | Roadmap |
| Streams | `java.streams` | Collections | Hard | Fill | Pipeline output | SRS | Different stream | Roadmap |
| File I/O | `java.file_io` | OOP | Easy | Fill | Output match | SRS | Different file | Roadmap |
| Debugging Java | `java.debugging` | OOP + Collections | Hard | Debug | Test cases pass | SRS | Different bug | Roadmap |
| DSA in Java | `java.dsa_implementations` | Collections + OOP | Hard | Implement | Test cases pass | SRS | Different problem | Roadmap |
| Algorithms in Java | `java.algo_implementations` | DSA in Java | Hard | Implement | Test cases pass | SRS | Different problem | Roadmap |
| Timed Java Practice | `java.timed_practice` | DSA in Java | Hard | Implement | Hidden tests pass | SRS | Different problem | Roadmap |

### 2.9 Domain: Company-Specific Placement Preparation (World 6 — V1 Partial)

| Company | Blueprint ID | Sections | Skill IDs Covered | V1 Status |
|---------|-------------|----------|-------------------|-----------|
| TCS NQT | `company.tcs` | Numerical, Verbal, Reasoning, Pseudocode, Coding | All World 1-4 skills + DSA | V1 (excellent) |
| Accenture | `company.accenture` | Cognitive, Technical, Coding | All World 1-4 skills + DSA | V1 (excellent) |
| Infosys | `company.infosys` | Cognitive, Technical, Coding | All World 1-4 skills + DSA | Roadmap (weights only) |
| Wipro | `company.wipro` | Quantitative, Verbal, Reasoning, Coding | All World 1-4 skills + DSA | Roadmap (weights only) |
| Cognizant | `company.cognizant` | Cognitive, Technical, Coding | All World 1-4 skills + DSA | Roadmap (weights only) |

### 2.10 Domain: Interview and Career Preparation (Roadmap)

| Subject | Concept | Skill ID | Prerequisite | Lesson | Interaction | Assessment | Evidence | Revision/Transfer | Release |
|---------|---------|----------|--------------|--------|-------------|------------|----------|-------------------|---------|
| Behavioral | STAR method | `interview.behavioral` | None | Easy | Fill | STAR match | SRS | Different question | Roadmap |
| HR Interview | Basics | `interview.hr` | None | Easy | Select | Answer match | SRS | Different question | Roadmap |
| Technical | Code + theory | `interview.technical` | DSA fundamentals | Medium | Implement | Test cases | SRS | Different problem | Roadmap |
| System Design | Architecture | `interview.system_design` | DSA + OS | Hard | Arrange | Architecture match | SRS | Different system | Roadmap |
| GD Topics | Group discussion | `interview.gd` | Verbal + reasoning | Hard | Arrange | Argument match | SRS | Different topic | Roadmap |
| Resume Builder | Generate | `resume.build` | None | Easy | Fill | ATS score | SRS | Different job | Roadmap |
| ATS Optimizer | Optimize | `resume.ats` | Resume builder | Medium | Fill | Keyword match | SRS | Different JD | Roadmap |

---

## 3. Language Independence Rule

| Language Pair | Independence Rule | Evidence |
|---------------|-------------------|----------|
| C → C++ | Not transferable | Separate `coding.c.*` and `coding.cpp.*` skill IDs |
| C++ → Java | Not transferable | Separate `coding.cpp.*` and `coding.java.*` skill IDs |
| Java → Python | Not transferable | Separate `coding.java.*` and `coding.python.*` skill IDs |
| C → Python | Not transferable | Separate `coding.c.*` and `coding.python.*` skill IDs |

Each language track maintains independent:
- Skill IDs (`coding.c.*`, `coding.cpp.*`, `coding.python.*`, `coding.java.*`)
- Evidence events (language field)
- Mastery claims (0-5 per language per skill)
- Readiness calculations (language-specific)

---

## 4. Concept Hierarchy Depth

| Domain | Max Depth | Example Path |
|--------|-----------|-------------|
| Quantitative Aptitude | 3 | Domain → Subject → Concept → Skill ID |
| Logical Reasoning | 3 | Domain → Subject → Concept → Skill ID |
| Verbal Ability | 3 | Domain → Subject → Concept → Skill ID |
| Programming Logic | 3 | Domain → Subject → Concept → Skill ID |
| C Programming | 4 | Domain → Subject → Concept → Sub-concept → Skill ID |
| C++ Programming | 4 | Domain → Subject → Concept → Sub-concept → Skill ID |
| Python Programming | 4 | Domain → Subject → Concept → Sub-concept → Skill ID |
| Java Programming | 4 | Domain → Subject → Concept → Sub-concept → Skill ID |
| DSA | 3 | Domain → Subject → Concept → Skill ID |
| SQL | 3 | Domain → Subject → Concept → Skill ID |
| CS Fundamentals | 3 | Domain → Subject → Concept → Skill ID |
| Company Simulation | 2 | Domain → Company → Blueprint |
| Interview/Career | 2 | Domain → Subject → Skill ID |

---

**End of 14 Curriculum Coverage Matrix**
