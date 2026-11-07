"""OS track â€” Operating Systems lessons."""

OS_LESSONS = [
    {
        "id": "os-intro",
        "title": "Introduction to OS",
        "track": "os",
        "description": "OS functions, types, and structure.",
        "difficulty": "beginner",
        "xpReward": 60,
        "steps": [
            {
                "id": "os1",
                "type": "explain",
                "title": "What is an OS?",
                "content": "Operating System is system software that manages computer hardware and software resources and provides common services.",
                "code": "",
                "explanation": "OS acts as intermediary between user and computer hardware.",
            },
            {
                "id": "os2",
                "type": "explain",
                "title": "OS functions",
                "content": "Process management, memory management, file management, device management, security.",
                "code": "",
                "explanation": "OS manages all hardware and software resources efficiently.",
            },
            {
                "id": "os3",
                "type": "quiz",
                "title": "OS function",
                "question": "Which is NOT an OS function?",
                "options": ["Process management", "Memory management", "Application development", "File management"],
                "correctIndex": 2,
                "explanation": "Application development is done by programmers, not OS.",
            },
        ],
    },
    {
        "id": "os-process",
        "title": "Process Management",
        "track": "os",
        "description": "Process states, scheduling, CPU scheduling.",
        "difficulty": "beginner",
        "prerequisites": ["os-intro"],
        "xpReward": 70,
        "steps": [
            {
                "id": "os2",
                "type": "explain",
                "title": "Process states",
                "content": "New, Ready, Running, Waiting, Terminated.",
                "code": "",
                "explanation": "Process moves through states: created, ready to run, executing, waiting for event, terminated.",
            },
            {
                "id": "os3",
                "type": "explain",
                "title": "CPU Scheduling",
                "content": "FCFS, SJF, Round Robin, Priority scheduling.",
                "code": "",
                "explanation": "CPU scheduler decides which process gets CPU next.",
            },
            {
                "id": "os4",
                "type": "exercise",
                "title": "FCFS scheduling",
                "instruction": "Processes arrive at time 0: P1(5ms), P2(3ms), P3(1ms). FCFS order?",
                "starterCode": "",
                "solution": "P1(0-5), P2(5-8), P3(8-9). Order: P1, P2, P3.",
                "tests": [{"input": None, "expected": None, "check": "equals_p1_p2_p3"}],
                "explanation": "FCFS executes in arrival order: P1, P2, P3.",
            },
        ],
    },
    {
        "id": "os-deadlock",
        "title": "Deadlock",
        "track": "os",
        "description": "Deadlock conditions and prevention.",
        "difficulty": "intermediate",
        "prerequisites": ["os-process"],
        "xpReward": 80,
        "steps": [
            {
                "id": "os4",
                "type": "explain",
                "title": "Deadlock conditions",
                "content": "Mutual exclusion, Hold and wait, No preemption, Circular wait.",
                "code": "",
                "explanation": "All four conditions must hold for deadlock to occur.",
            },
            {
                "id": "os5",
                "type": "explain",
                "title": "Deadlock prevention",
                "content": "Break one of the four conditions to prevent deadlock.",
                "code": "",
                "explanation": "Request all resources at once prevents hold and wait.",
            },
            {
                "id": "os6",
                "type": "quiz",
                "title": "Deadlock question",
                "question": "Which is NOT a necessary condition for deadlock?",
                "options": ["Mutual exclusion", "Hold and wait", "No preemption", "Starvation"],
                "correctIndex": 3,
                "explanation": "Starvation is not a necessary condition for deadlock.",
            },
        ],
    },
    {
        "id": "os-scheduling",
        "title": "CPU Scheduling",
        "description": "FCFS, SJF, Round Robin scheduling algorithms.",
        "track": "os",
        "difficulty": "beginner",
        "xpReward": 60,
        "steps": [
            {
                "id": "sch1",
                "type": "explain",
                "title": "Scheduling basics",
                "content": "CPU scheduler selects which process runs next. FCFS = first come first served (non-preemptive). SJF = shortest job first (minimizes average waiting time). Round Robin = fixed time slice per process.",
                "code": "",
                "explanation": "Different algorithms optimize different metrics: waiting time, turnaround time, response time.",
            },
            {
                "id": "sch2",
                "type": "exercise",
                "title": "FCFS waiting time",
                "instruction": "Processes arrive at time 0 with burst times 5, 3, 8. FCFS order P1,P2,P3. What is average waiting time?",
                "starterCode": "",
                "solution": "P1 waits 0, P2 waits 5, P3 waits 8. Average = (0+5+8)/3 = 13/3 = 4.33.",
                "tests": [{"input": None, "expected": None, "check": "equals_4_33"}],
                "explanation": "Waiting times: P1=0, P2=5, P3=5+3=8. Average = 13/3 = 4.33.",
            },
            {
                "id": "sch3",
                "type": "quiz",
                "title": "Round Robin",
                "question": "Round Robin scheduling is:",
                "options": ["Non-preemptive", "Preemptive with fixed time slice", "Always runs shortest job first", "Only for batch systems"],
                "correctIndex": 1,
                "explanation": "Round Robin is preemptive: each process gets a fixed time quantum, then moves to back of ready queue.",
            },
        ],
    },
    {
        "id": "os-memory",
        "title": "Memory Management",
        "description": "Paging, segmentation, virtual memory.",
        "track": "os",
        "difficulty": "intermediate",
        "xpReward": 70,
        "steps": [
            {
                "id": "mem1",
                "type": "explain",
                "title": "Paging",
                "content": "Memory divided into fixed-size frames. Process divided into same-size pages. Pages map to frames via page table. Eliminates external fragmentation.",
                "code": "",
                "explanation": "Logical address = page number + offset. Physical address = frame number + offset.",
            },
            {
                "id": "mem2",
                "type": "exercise",
                "title": "Page table lookup",
                "instruction": "Page size 4KB. Logical address 10000. What is page number and offset?",
                "starterCode": "",
                "solution": "Page number = 10000 / 4096 = 2. Offset = 10000 % 4096 = 1808.",
                "tests": [{"input": None, "expected": None, "check": "equals_page_2_offset_1808"}],
                "explanation": "Page number = floor(10000/4096) = 2. Offset = 10000 mod 4096 = 1808.",
            },
            {
                "id": "mem3",
                "type": "quiz",
                "title": "Virtual memory",
                "question": "Virtual memory allows:",
                "options": ["Programs larger than physical RAM", "Faster CPU execution", "No need for page tables", "Direct hardware access"],
                "correctIndex": 0,
                "explanation": "Virtual memory lets programs use more memory than physically available by swapping pages to disk.",
            },
        ],
    },
,
    {
        "id": "os-threads-synchronization",
        "title": "Threads and Synchronization",
        "track": "os",
        "description": "Understand concurrent execution and protect shared data.",
        "difficulty": "intermediate",
        "prerequisites": ["os-process"],
        "xpReward": 90,
        "steps": [
            {
                "id": "ots1",
                "type": "explain",
                "title": "Process versus thread",
                "content": "A process is a running program with its own address space and resources. Threads are execution paths within a process and typically share that process's memory. Threads can improve responsiveness and parallel work, but shared mutable data creates coordination challenges.",
                "code": "",
                "explanation": "Threads share process resources, while separate processes generally have isolated address spaces."
            },
            {
                "id": "ots2",
                "type": "explain",
                "title": "Understand a race condition",
                "content": "A race condition occurs when the result depends on the timing or interleaving of concurrent operations. If two threads read and update the same counter without coordination, one update can be lost. Protect critical sections with an appropriate synchronization mechanism.",
                "code": "Thread A: read count (5)\nThread B: read count (5)\nThread A: write count (6)\nThread B: write count (6)",
                "output": "Final count: 6 (expected 7)",
                "explanation": "Both threads read the old value before either write is visible, so one increment is lost."
            },
            {
                "id": "ots3",
                "type": "explain",
                "title": "Mutexes and semaphores",
                "content": "A mutex provides mutual exclusion: typically one thread at a time owns the lock protecting a critical section. A semaphore maintains a counter that controls access to a limited number of permits or coordinates events. Use the simplest primitive that matches the coordination requirement.",
                "code": "lock(mutex);\nshared_count++;\nunlock(mutex);",
                "output": "The critical update is protected from concurrent access",
                "explanation": "The lock ensures only one thread at a time executes the protected update."
            },
            {
                "id": "ots4",
                "type": "quiz",
                "title": "Identify a race condition",
                "question": "Two threads update the same shared counter without synchronization. What problem can occur?",
                "options": ["A race condition", "Guaranteed FIFO scheduling", "A DNS lookup", "A page fault every time"],
                "correctIndex": 0,
                "explanation": "Unsynchronized concurrent updates can interleave and produce a result that depends on timing."
            }
        ]
    },
    {
        "id": "os-deadlock-handling",
        "title": "Deadlock Prevention and Avoidance",
        "track": "os",
        "description": "Recognize the conditions for deadlock and compare prevention, avoidance, and detection.",
        "difficulty": "intermediate",
        "prerequisites": ["os-deadlock"],
        "xpReward": 95,
        "steps": [
            {
                "id": "odh1",
                "type": "explain",
                "title": "Four necessary conditions",
                "content": "The four Coffman conditions are mutual exclusion, hold and wait, no preemption, and circular wait. A deadlock requires all four conditions to hold at the same time. Breaking at least one necessary condition can prevent that class of deadlock.",
                "code": "",
                "explanation": "The conditions describe how processes can become permanently blocked while waiting for resources."
            },
            {
                "id": "odh2",
                "type": "explain",
                "title": "Prevention versus avoidance",
                "content": "Deadlock prevention designs the system so at least one necessary condition cannot hold. Deadlock avoidance examines resource-allocation requests and grants them only when the resulting state remains safe. The Banker's algorithm is a classic avoidance method when maximum resource needs are known.",
                "code": "",
                "explanation": "Prevention removes a condition; avoidance checks whether each allocation preserves a safe state."
            },
            {
                "id": "odh3",
                "type": "explain",
                "title": "Detection and recovery",
                "content": "A system may allow deadlocks, detect them using resource-allocation information, and recover by terminating processes or reclaiming resources where safe. Recovery has costs, so the choice depends on system requirements and workload.",
                "code": "",
                "explanation": "Detection finds an existing deadlock; recovery restores progress after it is found."
            },
            {
                "id": "odh4",
                "type": "quiz",
                "title": "Choose an avoidance method",
                "question": "Which classic algorithm checks whether a resource allocation leaves the system in a safe state?",
                "options": ["Banker's algorithm", "Binary search", "Round Robin", "Dijkstra's shortest path"],
                "correctIndex": 0,
                "explanation": "Banker's algorithm is a classic deadlock-avoidance algorithm based on safe states."
            }
        ]
    },
    {
        "id": "os-page-replacement",
        "title": "Virtual Memory and Page Replacement",
        "track": "os",
        "description": "Understand page faults and compare common page-replacement policies.",
        "difficulty": "intermediate",
        "prerequisites": ["os-memory"],
        "xpReward": 100,
        "steps": [
            {
                "id": "opr1",
                "type": "explain",
                "title": "What is a page fault?",
                "content": "Virtual memory divides an address space into pages and physical memory into frames. A page fault occurs when a process references a page that is not currently mapped to a usable physical frame. The operating system handles the fault and may load the page from storage.",
                "code": "",
                "explanation": "A page fault is an event that requires operating-system handling; it is not automatically a program error."
            },
            {
                "id": "opr2",
                "type": "explain",
                "title": "FIFO page replacement",
                "content": "FIFO replaces the page that has been in memory the longest. It is simple to implement with a queue, but it may evict a frequently used page. FIFO can exhibit Belady's anomaly, where adding frames can increase the number of page faults for some reference strings.",
                "code": "Reference string: 1, 2, 3, 1, 4\nFrames: 3\nFIFO evicts the oldest loaded page when a new page arrives and all frames are full.",
                "output": "The page loaded earliest is selected for replacement",
                "explanation": "FIFO uses arrival order, not recent usage, to choose a victim."
            },
            {
                "id": "opr3",
                "type": "explain",
                "title": "LRU page replacement",
                "content": "Least Recently Used (LRU) replaces the page that has not been used for the longest time in the past. It uses recent history as an estimate of future need. Exact LRU tracking has implementation overhead; practical systems often use approximations.",
                "code": "",
                "explanation": "LRU relies on temporal locality: recently used pages may be needed again soon."
            },
            {
                "id": "opr4",
                "type": "quiz",
                "title": "Compare FIFO and LRU",
                "question": "Which policy selects the page that has not been used for the longest time?",
                "options": ["FIFO", "LRU", "FCFS CPU scheduling", "Round Robin"],
                "correctIndex": 1,
                "explanation": "LRU uses the time since the last use; FIFO uses the time since loading."
            }
        ]
    }
]
