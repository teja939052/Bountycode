"""CS Fundamentals theory cards — versioned file content, loaded at import.

Service-company depth for OS, DBMS, OOP, CN, and SQL: what screening and
technical interviews actually ask at TCS/Infosys/Wipro/Accenture/Cognizant
level. Definitions, must-know facts, one worked example, and the
one-liner interviewers expect. Served read-only — no database, no LLM.
"""

THEORY = [
    # ── Operating Systems ────────────────────────────────────────────
    {
        "id": "os-process-thread",
        "title": "Process vs Thread",
        "domain": "os",
        "definition": "A process is an independent program in execution with its own memory space. A thread is a lightweight unit inside a process sharing the process memory.",
        "key_facts": [
            "Process: own address space, costly context switch, isolated crashes",
            "Thread: shared memory, cheap switch, one crash can kill the process",
            "Multithreading speeds I/O-bound work, not CPU-bound work on one core",
            "Context switch = saving registers/stack and loading the next task",
        ],
        "worked_example": {
            "problem": "A server handles 1000 simultaneous downloads. Processes or threads?",
            "solution": "Threads — downloads wait on I/O, and threads share memory cheaply. One process per download would exhaust RAM.",
        },
        "interview_ask": "Why is a thread switch faster than a process switch?",
        "triggers": ["'multithreading', 'concurrency vs parallelism'"],
        "practice_hint": "Drill Technical MCQs for OS one-liners",
    },
    {
        "id": "os-scheduling",
        "title": "CPU Scheduling",
        "domain": "os",
        "definition": "Scheduling decides which ready process gets the CPU next. Goals: high throughput, low waiting time, fairness.",
        "key_facts": [
            "FCFS: simple, convoy effect (long job blocks short ones)",
            "SJF: optimal average waiting time, but starves long jobs",
            "Round Robin: each job gets a time quantum; fair, used in practice",
            "Priority scheduling can starve low-priority jobs; aging fixes it",
        ],
        "worked_example": {
            "problem": "Jobs A(5ms), B(2ms), C(8ms) arrive together. Average wait under SJF?",
            "solution": "Order B,A,C. Waits: 0, 2, 7. Average = 3ms vs FCFS average 7.67ms.",
        },
        "interview_ask": "What is starvation, and how does aging prevent it?",
        "triggers": ["'time quantum', 'convoy effect', 'starvation'"],
        "practice_hint": "Drill Technical MCQs for scheduling numbers",
    },
    {
        "id": "os-deadlock",
        "title": "Deadlocks",
        "domain": "os",
        "definition": "Deadlock = two or more processes each holding a resource while waiting for one held by another. Four Coffman conditions must all hold.",
        "key_facts": [
            "Conditions: mutual exclusion, hold-and-wait, no preemption, circular wait",
            "Break any ONE condition to prevent deadlock",
            "Banker's algorithm avoids deadlock by granting only 'safe' allocations",
            "Detection + recovery (kill/rollback) is what real OSes mostly do",
        ],
        "worked_example": {
            "problem": "P1 holds printer, wants scanner. P2 holds scanner, wants printer. Deadlock?",
            "solution": "Yes — hold-and-wait plus circular wait. Fix: force an order (always take printer first).",
        },
        "interview_ask": "Name the four deadlock conditions and one way to break each.",
        "triggers": ["'dining philosophers', 'resource allocation graph cycle'"],
        "practice_hint": "Drill Technical MCQs for Coffman conditions",
    },
    {
        "id": "os-memory",
        "title": "Memory: Paging & Virtual Memory",
        "domain": "os",
        "definition": "Virtual memory gives every process its own large address space; paging maps virtual pages to physical frames on demand.",
        "key_facts": [
            "Page = fixed block of virtual memory; frame = fixed block of RAM",
            "Page fault = needed page not in RAM; OS loads it from disk",
            "Thrashing = CPU spends more time paging than executing; add RAM or kill processes",
            "LRU approximates optimal replacement; FIFO can suffer Belady's anomaly",
        ],
        "worked_example": {
            "problem": "RAM keeps swapping and CPU usage drops to 5%. Diagnosis?",
            "solution": "Thrashing — working sets exceed RAM. Reduce load or add memory.",
        },
        "interview_ask": "What happens step by step on a page fault?",
        "triggers": ["'thrashing', 'Belady', 'demand paging'"],
        "practice_hint": "Drill Technical MCQs for paging terms",
    },
    # ── DBMS ─────────────────────────────────────────────────────────
    {
        "id": "dbms-keys",
        "title": "Keys: Primary, Foreign, Candidate",
        "domain": "dbms",
        "definition": "Keys identify rows and link tables. Primary key uniquely identifies a row; foreign key references another table's primary key.",
        "key_facts": [
            "Primary key: unique + NOT NULL, one per table",
            "Candidate key: any minimal unique column set; primary is the chosen one",
            "Foreign key: enforces referential integrity to the parent table",
            "Super key: any unique set (not necessarily minimal)",
        ],
        "worked_example": {
            "problem": "Students(roll, email, name), Enroll(roll, course). Keys?",
            "solution": "Students PK = roll (email is candidate). Enroll.roll is a foreign key to Students.",
        },
        "interview_ask": "Primary key vs unique key in one line?",
        "triggers": ["'referential integrity', 'candidate key'"],
        "practice_hint": "Drill Technical MCQs for key definitions",
    },
    {
        "id": "dbms-normalization",
        "title": "Normalization (1NF–3NF, BCNF)",
        "domain": "dbms",
        "definition": "Normalization removes redundancy by splitting tables so each fact lives in exactly one place.",
        "key_facts": [
            "1NF: atomic values, no repeating groups",
            "2NF: 1NF + no partial dependency on part of a composite key",
            "3NF: 2NF + no transitive dependency (non-key depending on non-key)",
            "BCNF: every determinant is a candidate key; over-normalize and joins get slow",
        ],
        "worked_example": {
            "problem": "Orders(order_id, customer_name, customer_city) — what breaks?",
            "solution": "Transitive dependency: city depends on name, not the order. Split Customers out (3NF).",
        },
        "interview_ask": "When would you deliberately denormalize?",
        "triggers": ["'transitive dependency', 'partial dependency'"],
        "practice_hint": "Drill Technical MCQs for normal-form riddles",
    },
    {
        "id": "dbms-acid-index",
        "title": "ACID & Indexing",
        "domain": "dbms",
        "definition": "ACID guarantees reliable transactions. Indexes are lookup structures that speed reads at the cost of slower writes.",
        "key_facts": [
            "Atomicity: all-or-nothing; Consistency: valid state to valid state",
            "Isolation: concurrent transactions don't see each other's halves; Durability: committed = survived crashes",
            "B-tree index: O(log n) lookups, the default workhorse",
            "Index every WHERE/JOIN column you filter on; don't index tiny or write-heavy tables blindly",
        ],
        "worked_example": {
            "problem": "Transfer ₹500 A→B. Power fails mid-way. What saves you?",
            "solution": "Atomicity via write-ahead log: either both halves commit or the whole transaction rolls back.",
        },
        "interview_ask": "Why can too many indexes hurt performance?",
        "triggers": ["'dirty read', 'phantom read', 'B-tree vs hash'"],
        "practice_hint": "Drill Technical MCQs for ACID expansions",
    },
    {
        "id": "dbms-joins",
        "title": "SQL JOINs",
        "domain": "dbms",
        "definition": "JOINs combine rows from two tables on a related column. The JOIN type decides which unmatched rows survive.",
        "key_facts": [
            "INNER: only matching rows on both sides",
            "LEFT: all left rows + matches (NULLs where no match)",
            "RIGHT: mirror of LEFT; FULL OUTER: everything both sides",
            "SELF JOIN: table joined to itself with aliases (managers/employees)",
        ],
        "worked_example": {
            "problem": "List all students with their course names, including students with no course.",
            "solution": "SELECT s.name, c.name FROM Students s LEFT JOIN Enroll e ON s.roll=e.roll LEFT JOIN Courses c ON e.course=c.id;",
        },
        "interview_ask": "LEFT JOIN vs INNER JOIN with one example each.",
        "triggers": ["'employees without departments', 'unmatched rows'"],
        "practice_hint": "Write each JOIN once in the playground",
    },
    # ── OOP ──────────────────────────────────────────────────────────
    {
        "id": "oop-pillars",
        "title": "The 4 Pillars of OOP",
        "domain": "oop",
        "definition": "OOP models software as interacting objects: encapsulation hides state, abstraction hides complexity, inheritance reuses behaviour, polymorphism swaps implementations.",
        "key_facts": [
            "Encapsulation: private fields + public methods; invariants enforced in one place",
            "Abstraction: expose WHAT, hide HOW (interfaces/abstract classes)",
            "Inheritance: IS-A reuse; prefer composition when it's HAS-A",
            "Polymorphism: same call, different behaviour (overriding at runtime, overloading at compile time)",
        ],
        "worked_example": {
            "problem": "Model Payment with UPI, Card, NetBanking options.",
            "solution": "PaymentMethod interface with pay() — each option implements it. Checkout code never changes when a 4th option arrives.",
        },
        "interview_ask": "Overloading vs overriding, with where each is resolved?",
        "triggers": ["'IS-A vs HAS-A', 'interface vs abstract class'"],
        "practice_hint": "Drill Technical MCQs for pillar definitions",
    },
    {
        "id": "oop-solid",
        "title": "SOLID in One Minute",
        "domain": "oop",
        "definition": "Five design principles that keep OOP code changeable: single responsibility, open/closed, Liskov substitution, interface segregation, dependency inversion.",
        "key_facts": [
            "S: one class, one reason to change",
            "O: open for extension, closed for modification (extend, don't edit)",
            "L: subclasses must honour the parent contract (no surprising exceptions)",
            "I: small focused interfaces beat one fat interface",
            "D: depend on abstractions, inject implementations",
        ],
        "worked_example": {
            "problem": "Report class that fetches data, formats PDF, and emails it. Fix it?",
            "solution": "Split into Fetcher, Formatter, Mailer behind interfaces (S+I+D). Add Excel by adding a class, not editing (O).",
        },
        "interview_ask": "Explain Liskov with a Rectangle/Square trap.",
        "triggers": ["'god class', 'tight coupling'"],
        "practice_hint": "Drill Technical MCQs for SOLID expansions",
    },
    {
        "id": "oop-java",
        "title": "Java/C++ Screening Favourites",
        "domain": "oop",
        "definition": "The handful of language facts that screening MCQs repeat: static, final/const, virtual, constructors, access control.",
        "key_facts": [
            "static belongs to the class: one copy shared by all objects",
            "Constructors run at creation; destructors/virtual destructors clean up (C++)",
            "virtual (C++) / dynamic dispatch (Java): the object type decides at runtime",
            "Java: no multiple class inheritance (interfaces instead); C++: has it (diamond risk)",
        ],
        "worked_example": {
            "problem": "Base* p = new Derived(); p->show(); show() is virtual. What runs?",
            "solution": "Derived::show() — virtual dispatches on the real object type, not the pointer type.",
        },
        "interview_ask": "Why must a polymorphic base class have a virtual destructor?",
        "triggers": ["'static', 'final', 'virtual', 'constructor order'"],
        "practice_hint": "Predict outputs in the playground, then verify",
    },
    {
        "id": "oop-design-patterns",
        "title": "Singleton & Factory (Enough to Talk About)",
        "domain": "oop",
        "definition": "Patterns are named reusable solutions. Singleton guarantees one instance; Factory creates objects without exposing the class choice.",
        "key_facts": [
            "Singleton: private constructor + static getInstance; watch thread-safety",
            "Factory: caller asks for a type string, gets back an interface",
            "Observer: publisher notifies subscribers (event systems, UI)",
            "Don't force patterns — name one only when the problem fits",
        ],
        "worked_example": {
            "problem": "App needs exactly one config object read from disk once.",
            "solution": "Singleton Config with lazy getInstance(); synchronise it if threads exist.",
        },
        "interview_ask": "Where does tight coupling hurt, and which pattern loosens it here?",
        "triggers": ["'exactly one instance', 'create without new'"],
        "practice_hint": "Drill Technical MCQs for pattern names",
    },
    # ── Computer Networks ────────────────────────────────────────────
    {
        "id": "cn-osi-tcp",
        "title": "OSI vs TCP/IP",
        "domain": "cn",
        "definition": "Layer models split networking into jobs: link, network (routing), transport (reliability), application (protocols you name).",
        "key_facts": [
            "OSI 7: Physical, Data Link, Network, Transport, Session, Presentation, Application",
            "TCP/IP 4: Link, Internet, Transport, Application — the model actually used",
            "IP lives at Network layer; TCP/UDP at Transport; HTTP/DNS at Application",
            "Switches work at Data Link; routers at Network",
        ],
        "worked_example": {
            "problem": "Where does routing happen, and which device does it?",
            "solution": "Network layer (IP), by routers — switches only forward within a LAN.",
        },
        "interview_ask": "What happens at each layer when you open a website?",
        "triggers": ["'which layer', 'router vs switch vs hub'"],
        "practice_hint": "Drill Technical MCQs for layer numbers",
    },
    {
        "id": "cn-tcp-udp",
        "title": "TCP vs UDP",
        "domain": "cn",
        "definition": "TCP is reliable, ordered, connection-first. UDP is fire-and-forget: fast, no guarantees.",
        "key_facts": [
            "TCP: 3-way handshake (SYN, SYN-ACK, ACK), ACKs, retransmission, flow control",
            "UDP: no handshake, no ordering — voice/video/DNS/Gaming",
            "TCP suits files, web, email; UDP suits live streams where late = useless",
            "Congestion control (slow start) protects the network, not just your app",
        ],
        "worked_example": {
            "problem": "Video call stutters on TCP but is smooth (if lossy) on UDP. Why?",
            "solution": "TCP retransmits lost packets (delay); UDP drops them and moves on — right trade for live media.",
        },
        "interview_ask": "Walk through the 3-way handshake and why each step exists.",
        "triggers": ["'handshake', 'reliable vs fast'"],
        "practice_hint": "Drill Technical MCQs for protocol matching",
    },
    {
        "id": "cn-http-dns",
        "title": "HTTP, HTTPS & DNS",
        "domain": "cn",
        "definition": "DNS turns names into IPs; HTTP(S) fetches web resources. HTTPS is HTTP inside TLS encryption.",
        "key_facts": [
            "DNS: recursive resolver → root → TLD → authoritative; results cached by TTL",
            "HTTP methods: GET reads, POST creates, PUT replaces, DELETE removes",
            "Status codes: 2xx success, 3xx redirect, 4xx client error, 5xx server error",
            "HTTPS: certificates + TLS handshake encrypt everything after",
        ],
        "worked_example": {
            "problem": "Type example.com, press enter. First three network steps?",
            "solution": "1) DNS resolve example.com → IP. 2) TCP handshake. 3) TLS handshake, then HTTP GET.",
        },
        "interview_ask": "HTTP vs HTTPS — what exactly does the S add?",
        "triggers": ["'status codes', 'cookies vs sessions'"],
        "practice_hint": "Drill Technical MCQs for codes and methods",
    },
    {
        "id": "cn-ip-subnet",
        "title": "IP Addressing & Subnetting Basics",
        "domain": "cn",
        "definition": "IPv4 = 32-bit address (network part + host part). The subnet mask says where the split is.",
        "key_facts": [
            "Classes: A 1–126, B 128–191, C 192–223 (know the ranges)",
            "Private ranges: 10/8, 172.16/12, 192.168/16 — never routed on the internet",
            "/24 = 256 addresses, 254 usable (network + broadcast reserved)",
            "IPv6 = 128-bit, written in hex, solves exhaustion",
        ],
        "worked_example": {
            "problem": "How many usable hosts in 192.168.1.0/26?",
            "solution": "Host bits = 32−26 = 6 → 64 addresses − 2 = 62 usable.",
        },
        "interview_ask": "Why subtract 2 from every subnet?",
        "triggers": ["'/24', 'default gateway', 'private IP'"],
        "practice_hint": "Drill Technical MCQs for class ranges",
    },
    # ── SQL ──────────────────────────────────────────────────────────
    {
        "id": "sql-select",
        "title": "SELECT, WHERE, ORDER BY",
        "domain": "sql",
        "definition": "SELECT reads columns, WHERE filters rows, ORDER BY sorts. Execution order: FROM → WHERE → SELECT → ORDER BY.",
        "key_facts": [
            "WHERE filters before grouping; HAVING filters after GROUP BY",
            "DISTINCT removes duplicates; TOP/LIMIT caps rows",
            "BETWEEN, IN, LIKE ('A%' starts-with, '%a' ends-with) do the filtering work",
            "ORDER BY col DESC puts biggest first; NULLs sort first in most engines",
        ],
        "worked_example": {
            "problem": "Employees with salary > 50000, highest first, name only.",
            "solution": "SELECT name FROM Employees WHERE salary > 50000 ORDER BY salary DESC;",
        },
        "interview_ask": "WHERE vs HAVING — when does each run?",
        "triggers": ["'second highest', 'duplicates', 'top-N'"],
        "practice_hint": "Write each clause once in the playground",
    },
    {
        "id": "sql-group",
        "title": "GROUP BY & Aggregates",
        "domain": "sql",
        "definition": "Aggregates (COUNT/SUM/AVG/MIN/MAX) collapse rows; GROUP BY collapses per group instead of the whole table.",
        "key_facts": [
            "Every non-aggregated SELECT column must be in GROUP BY",
            "COUNT(*) counts rows; COUNT(col) skips NULLs",
            "HAVING filters groups (e.g. departments with AVG salary > 60000)",
            "Nth-highest salary classic: ORDER BY salary DESC LIMIT 1 OFFSET 1",
        ],
        "worked_example": {
            "problem": "Departments with more than 5 employees.",
            "solution": "SELECT dept, COUNT(*) FROM Emp GROUP BY dept HAVING COUNT(*) > 5;",
        },
        "interview_ask": "Find duplicate emails in a Users table.",
        "triggers": ["'per department', 'average by', 'having'"],
        "practice_hint": "Write the Nth-salary query from memory",
    },
    {
        "id": "sql-joins-practice",
        "title": "JOINs in Practice",
        "domain": "sql",
        "definition": "The interview favourite: combine tables correctly and handle the rows with no match.",
        "key_facts": [
            "INNER for matches only; LEFT to keep every left row",
            "Join on keys, filter in WHERE, aggregate after",
            "Alias every table (e, d) — readability is graded in interviews",
            "UNION stacks result sets (same columns); UNION ALL keeps duplicates",
        ],
        "worked_example": {
            "problem": "Employees and their department names, including employees with none.",
            "solution": "SELECT e.name, d.name FROM Emp e LEFT JOIN Dept d ON e.dept_id = d.id;",
        },
        "interview_ask": "When would you use a SELF JOIN?",
        "triggers": ["'without department', 'combine two queries'"],
        "practice_hint": "Solve 3 JOIN problems in Question Bank",
    },
    {
        "id": "sql-dml-ddl",
        "title": "DML vs DDL vs Constraints",
        "domain": "sql",
        "definition": "DDL defines structure (CREATE/ALTER/DROP), DML changes data (INSERT/UPDATE/DELETE), constraints guard correctness.",
        "key_facts": [
            "DELETE removes rows (rollback-able); TRUNCATE empties fast (usually not rollback-able); DROP deletes the table",
            "Constraints: NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK, DEFAULT",
            "Transactions: BEGIN, COMMIT, ROLLBACK — group changes atomically",
            "GRANT/REVOKE (DCL) control who can do what",
        ],
        "worked_example": {
            "problem": "Safely give every intern a ₹2000 hike.",
            "solution": "BEGIN; UPDATE Emp SET salary = salary + 2000 WHERE level='intern'; -- verify, then COMMIT;",
        },
        "interview_ask": "DELETE vs TRUNCATE vs DROP in one line each.",
        "triggers": ["'rollback', 'constraints', 'grant'"],
        "practice_hint": "Drill Technical MCQs for DDL/DML splits",
    },
]


def get_cs_domains():
    """Domain list for the CS Fundamentals index."""
    seen = []
    for t in THEORY:
        if t["domain"] not in seen:
            seen.append(t["domain"])
    return seen


def get_cs_topics():
    """Lightweight topic list for the index."""
    return [
        {"id": t["id"], "title": t["title"], "domain": t["domain"]}
        for t in THEORY
    ]


def get_cs_theory(topic_id: str):
    """Full theory card for one topic, or None."""
    tid = (topic_id or "").strip().lower()
    for t in THEORY:
        if t["id"] == tid:
            return t
    return None


def get_cs_by_domain(domain: str):
    """Theory cards for one domain (os/dbms/oop/cn/sql)."""
    d = (domain or "").strip().lower()
    return [t for t in THEORY if t["domain"] == d]
