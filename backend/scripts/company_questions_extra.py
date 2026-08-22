"""Extra company-specific interview questions layered onto the big bank."""
from __future__ import annotations

COMPANY_QUESTIONS_EXTRA = {
    "google": {
        "name": "Google",
        "icon": "G",
        "color": "#4285F4",
        "leadership_principles": ["User focus", "Technical excellence", "Collaboration"],
        "questions": {
            "behavioral": [
                {
                    "id": "gxx-beh-0001",
                    "question": "Tell me about a time you simplified a complex system for your team.",
                    "category": "behavioral",
                    "difficulty": "medium",
                    "company_id": "google",
                    "company": "Google",
                },
                {
                    "id": "gxx-beh-0002",
                    "question": "Describe a time you used data to change a technical decision.",
                    "category": "behavioral",
                    "difficulty": "medium",
                    "company_id": "google",
                    "company": "Google",
                },
            ],
            "coding": [
                {
                    "id": "gxx-cod-0001",
                    "question": "Design a search autocomplete system.",
                    "category": "coding",
                    "difficulty": "hard",
                    "company_id": "google",
                    "company": "Google",
                },
                {
                    "id": "gxx-cod-0002",
                    "question": "Find the shortest path in a weighted graph with non-negative edges.",
                    "category": "coding",
                    "difficulty": "hard",
                    "company_id": "google",
                    "company": "Google",
                },
            ],
            "system_design": [
                {
                    "id": "gxx-sys-0001",
                    "question": "Design a global rate limiter for millions of requests per second.",
                    "category": "system_design",
                    "difficulty": "hard",
                    "company_id": "google",
                    "company": "Google",
                }
            ],
        },
    },
    "amazon": {
        "name": "Amazon",
        "icon": "A",
        "color": "#FF9900",
        "leadership_principles": ["Customer Obsession", "Ownership", "Dive Deep"],
        "questions": {
            "behavioral": [
                {
                    "id": "axx-beh-0001",
                    "question": "Tell me about a time you owned a problem end-to-end without being asked.",
                    "category": "behavioral",
                    "difficulty": "medium",
                    "company_id": "amazon",
                    "company": "Amazon",
                },
                {
                    "id": "axx-beh-0002",
                    "question": "Describe a time you disagreed with a teammate and still delivered results.",
                    "category": "behavioral",
                    "difficulty": "medium",
                    "company_id": "amazon",
                    "company": "Amazon",
                },
            ],
            "coding": [
                {
                    "id": "axx-cod-0001",
                    "question": "Merge k sorted linked lists efficiently.",
                    "category": "coding",
                    "difficulty": "hard",
                    "company_id": "amazon",
                    "company": "Amazon",
                }
            ],
        },
    },
    "meta": {
        "name": "Meta",
        "icon": "M",
        "color": "#1877F2",
        "leadership_principles": ["Move fast", "Be bold", "Focus on impact"],
        "questions": {
            "behavioral": [
                {
                    "id": "mxx-beh-0001",
                    "question": "Tell me about a product improvement you shipped quickly and measured.",
                    "category": "behavioral",
                    "difficulty": "medium",
                    "company_id": "meta",
                    "company": "Meta",
                }
            ],
            "system_design": [
                {
                    "id": "mxx-sys-0001",
                    "question": "Design a real-time feed ranking system.",
                    "category": "system_design",
                    "difficulty": "hard",
                    "company_id": "meta",
                    "company": "Meta",
                }
            ],
        },
    },
    "tcs": {
        "name": "TCS",
        "icon": "T",
        "color": "#1C4E80",
        "questions": {
            "behavioral": [
                {
                    "id": "tcx-beh-0001",
                    "question": "Tell me about a time you learned a new technology quickly for a project.",
                    "category": "behavioral",
                    "difficulty": "easy",
                    "company_id": "tcs",
                    "company": "TCS",
                }
            ],
            "technical": [
                {
                    "id": "tcx-tech-0001",
                    "question": "Explain the difference between stack and queue with an example.",
                    "category": "technical",
                    "difficulty": "easy",
                    "company_id": "tcs",
                    "company": "TCS",
                }
            ],
            "coding": [
                {
                    "id": "tcx-cod-0001",
                    "question": "Write a function to check if a string is a palindrome.",
                    "category": "coding",
                    "difficulty": "easy",
                    "company_id": "tcs",
                    "company": "TCS",
                }
            ],
        },
    },
    "infosys": {
        "name": "Infosys",
        "icon": "I",
        "color": "#007CC3",
        "questions": {
            "behavioral": [
                {
                    "id": "ifx-beh-0001",
                    "question": "Tell me about a time you worked in a team with conflicting priorities.",
                    "category": "behavioral",
                    "difficulty": "easy",
                    "company_id": "infosys",
                    "company": "Infosys",
                }
            ],
            "technical": [
                {
                    "id": "ifx-tech-0001",
                    "question": "What is the difference between compiler and interpreter?",
                    "category": "technical",
                    "difficulty": "easy",
                    "company_id": "infosys",
                    "company": "Infosys",
                }
            ],
        },
    },
    "wipro": {
        "name": "Wipro",
        "icon": "W",
        "color": "#5A2D82",
        "questions": {
            "behavioral": [
                {
                    "id": "wpx-beh-0001",
                    "question": "Tell me about a time you handled a tight deadline calmly.",
                    "category": "behavioral",
                    "difficulty": "easy",
                    "company_id": "wipro",
                    "company": "Wipro",
                }
            ],
            "technical": [
                {
                    "id": "wpx-tech-0001",
                    "question": "What is the difference between process and thread?",
                    "category": "technical",
                    "difficulty": "easy",
                    "company_id": "wipro",
                    "company": "Wipro",
                }
            ],
        },
    },
}

COMPANY_QUESTIONS_EXTRA_2 = {
    "google": {
        "questions": {
            "coding": [
                {"id": "g2-cod-0001", "question": "Design a URL shortener.", "category": "coding", "difficulty": "medium", "company_id": "google", "company": "Google"},
                {"id": "g2-cod-0002", "question": "Find the kth largest element in an array.", "category": "coding", "difficulty": "medium", "company_id": "google", "company": "Google"},
            ],
            "behavioral": [
                {"id": "g2-beh-0001", "question": "Tell me about a time you handled ambiguous requirements.", "category": "behavioral", "difficulty": "medium", "company_id": "google", "company": "Google"},
            ],
        },
    },
    "amazon": {
        "questions": {
            "coding": [
                {"id": "a2-cod-0001", "question": "Implement an LRU cache.", "category": "coding", "difficulty": "hard", "company_id": "amazon", "company": "Amazon"},
                {"id": "a2-cod-0002", "question": "Merge intervals efficiently.", "category": "coding", "difficulty": "medium", "company_id": "amazon", "company": "Amazon"},
            ],
            "behavioral": [
                {"id": "a2-beh-0001", "question": "Describe a time you took ownership of a failing process.", "category": "behavioral", "difficulty": "medium", "company_id": "amazon", "company": "Amazon"},
            ],
        },
    },
    "meta": {
        "questions": {
            "coding": [
                {"id": "m2-cod-0001", "question": "Design a news feed ranking service.", "category": "coding", "difficulty": "hard", "company_id": "meta", "company": "Meta"},
                {"id": "m2-cod-0002", "question": "Find the longest increasing path in a matrix.", "category": "coding", "difficulty": "hard", "company_id": "meta", "company": "Meta"},
            ],
        },
    },
    "tcs": {
        "questions": {
            "technical": [
                {"id": "t2-tech-0001", "question": "Explain the difference between stack and heap memory.", "category": "technical", "difficulty": "easy", "company_id": "tcs", "company": "TCS"},
                {"id": "t2-tech-0002", "question": "What is the difference between process and thread?", "category": "technical", "difficulty": "easy", "company_id": "tcs", "company": "TCS"},
            ],
            "behavioral": [
                {"id": "t2-beh-0001", "question": "Tell me about a time you adapted to a new team quickly.", "category": "behavioral", "difficulty": "easy", "company_id": "tcs", "company": "TCS"},
            ],
        },
    },
    "infosys": {
        "questions": {
            "technical": [
                {"id": "i2-tech-0001", "question": "What is the difference between compiler and interpreter?", "category": "technical", "difficulty": "easy", "company_id": "infosys", "company": "Infosys"},
                {"id": "i2-tech-0002", "question": "Explain encapsulation in OOP.", "category": "technical", "difficulty": "easy", "company_id": "infosys", "company": "Infosys"},
            ],
        },
    },
    "wipro": {
        "questions": {
            "technical": [
                {"id": "w2-tech-0001", "question": "What is the difference between array and linked list?", "category": "technical", "difficulty": "easy", "company_id": "wipro", "company": "Wipro"},
                {"id": "w2-tech-0002", "question": "What is recursion?", "category": "technical", "difficulty": "easy", "company_id": "wipro", "company": "Wipro"},
            ],
        },
    },
}

_EXTRA_2_BASE = [
    ("google", "coding", "Design a URL shortener.", "medium"),
    ("google", "coding", "Find the kth largest element in an array.", "medium"),
    ("google", "behavioral", "Tell me about a time you handled ambiguous requirements.", "medium"),
    ("amazon", "coding", "Implement an LRU cache.", "hard"),
    ("amazon", "coding", "Merge intervals efficiently.", "medium"),
    ("amazon", "behavioral", "Describe a time you took ownership of a failing process.", "medium"),
    ("meta", "coding", "Design a news feed ranking service.", "hard"),
    ("meta", "coding", "Find the longest increasing path in a matrix.", "hard"),
    ("tcs", "technical", "Explain the difference between stack and heap memory.", "easy"),
    ("tcs", "technical", "What is the difference between process and thread?", "easy"),
    ("tcs", "behavioral", "Tell me about a time you adapted to a new team quickly.", "easy"),
    ("infosys", "technical", "What is the difference between compiler and interpreter?", "easy"),
    ("infosys", "technical", "Explain encapsulation in OOP.", "easy"),
    ("wipro", "technical", "What is the difference between array and linked list?", "easy"),
    ("wipro", "technical", "What is recursion?", "easy"),
]

_EXTRA_2_MORE = {
    "google": [
        "Design a distributed cache for low-latency reads.",
        "Detect cycles in a directed graph.",
        "Explain the trade-offs of using sharding versus replication.",
        "Write a function to merge overlapping intervals.",
        "Design a notification fanout service.",
        "Find all nodes at distance k from a target node.",
        "Explain how you would index a search dataset.",
        "Design a feature flag rollout system.",
        "Describe a time you improved the reliability of a service.",
        "Tell me about a time you mentored someone technically.",
    ],
    "amazon": [
        "Design an order processing pipeline.",
        "Implement a rate limiter.",
        "Detect whether a linked list has a cycle.",
        "Design a scalable cart service.",
        "Explain a time you dove deep into a bug.",
        "Tell me about a time you influenced without authority.",
        "Design a metrics aggregation system.",
        "Find the median of a data stream.",
        "Implement a task scheduler.",
        "Describe a time you improved customer experience.",
    ],
    "meta": [
        "Design a real-time comment feed.",
        "Implement shortest path on a weighted graph.",
        "Design a friend suggestion system.",
        "Explain how you would rank posts in a feed.",
        "Tell me about a product metric you improved.",
        "Describe a time you shipped quickly with limited data.",
        "Design a push notification backend.",
        "Find connected components in a graph.",
        "Implement top-k frequent elements.",
        "Explain a time you balanced speed and quality.",
    ],
    "tcs": [
        "What is polymorphism in OOP?",
        "Explain the difference between SQL and NoSQL.",
        "What is normalization in databases?",
        "Write a function to check if a number is prime.",
        "Tell me about a time you met a deadline.",
        "Explain the software development lifecycle.",
        "What is the difference between class and object?",
        "Write a function to reverse a string.",
        "How do you handle feedback?",
        "What is encapsulation?",
    ],
    "infosys": [
        "What is inheritance in OOP?",
        "Explain the difference between array and linked list.",
        "Write a function to find the maximum element in an array.",
        "What is a database index?",
        "Tell me about a time you solved a tricky problem.",
        "Explain REST APIs in simple terms.",
        "What is recursion?",
        "Write a function to check palindrome strings.",
        "How do you prioritize work?",
        "What is the difference between compiler and interpreter?",
    ],
    "wipro": [
        "What is the difference between a stack and a queue?",
        "Explain loops and conditionals.",
        "Write a function to count vowels in a string.",
        "What is multithreading?",
        "Tell me about a time you collaborated on a team project.",
        "Explain object-oriented programming basics.",
        "What is the difference between process and thread?",
        "Write a function to remove duplicates from a list.",
        "How do you handle learning a new tool?",
        "What is recursion?",
    ],
}

for company_id, prompts in _EXTRA_2_MORE.items():
    for idx, prompt in enumerate(prompts, start=1):
        _EXTRA_2_BASE.append((company_id, "behavioral" if "Tell me" in prompt or "Describe" in prompt or "How do" in prompt else ("coding" if "Write a function" in prompt or "Implement" in prompt or "Design" in prompt or "Find " in prompt else "technical"), prompt, "easy" if company_id in {"tcs", "infosys", "wipro"} else ("medium" if idx % 2 else "hard")))

for i in range(100):
    company_id, category, question, difficulty = _EXTRA_2_BASE[i % len(_EXTRA_2_BASE)]
    COMPANY_QUESTIONS_EXTRA_2.setdefault(company_id, {}).setdefault("questions", {}).setdefault(category, [])
    COMPANY_QUESTIONS_EXTRA_2[company_id]["questions"][category].append({
        "id": f"{company_id[:2]}2-{category[:4]}-{i + 1:04d}",
        "question": f"{question} Variant {i // len(_EXTRA_2_BASE) + 1}",
        "category": category,
        "difficulty": difficulty,
        "company_id": company_id,
        "company": company_id.title() if company_id not in {"tcs"} else "TCS",
    })

COMPANY_QUESTIONS_EXTRA_3 = {
    "google": {"questions": {"coding": [], "behavioral": []}},
    "amazon": {"questions": {"coding": [], "behavioral": []}},
    "meta": {"questions": {"coding": [], "behavioral": []}},
    "tcs": {"questions": {"technical": [], "behavioral": []}},
    "infosys": {"questions": {"technical": [], "behavioral": []}},
    "wipro": {"questions": {"technical": [], "behavioral": []}},
}

_SPECS = [
    ("google", "coding", "Design a scalable autocomplete backend."),
    ("google", "coding", "Find the shortest path in an unweighted graph."),
    ("google", "behavioral", "Tell me about a time you learned a complex system quickly."),
    ("amazon", "coding", "Implement a queue using two stacks."),
    ("amazon", "coding", "Design a metrics dashboard pipeline."),
    ("amazon", "behavioral", "Describe a time you handled a production incident."),
    ("meta", "coding", "Implement a trie with prefix search."),
    ("meta", "behavioral", "Tell me about a time you made a fast product decision."),
    ("tcs", "technical", "What is the difference between class and object?"),
    ("tcs", "behavioral", "Tell me about a time you worked under pressure."),
    ("infosys", "technical", "What is SQL normalization?"),
    ("infosys", "behavioral", "Tell me about a time you solved a technical problem."),
    ("wipro", "technical", "What is recursion?"),
    ("wipro", "behavioral", "Tell me about a time you collaborated with a team."),
]

for i in range(100):
    cid, category, question = _SPECS[i % len(_SPECS)]
    COMPANY_QUESTIONS_EXTRA_3[cid]["questions"][category].append({
        "id": f"{cid[:2]}3-{category[:4]}-{i + 1:04d}",
        "question": f"{question} Variant {i // len(_SPECS) + 1}",
        "category": category,
        "difficulty": "hard" if (i % 9 == 8 and cid in {"google", "amazon", "meta"}) else ("medium" if i % 3 else "easy"),
        "company_id": cid,
        "company": cid.title() if cid != "tcs" else "TCS",
    })

COMPANY_QUESTIONS_EXTRA_4 = {
    "google": {"questions": {"coding": [], "behavioral": [], "system_design": []}},
    "amazon": {"questions": {"coding": [], "behavioral": [], "system_design": []}},
    "meta": {"questions": {"coding": [], "behavioral": [], "system_design": []}},
    "tcs": {"questions": {"technical": [], "behavioral": []}},
    "infosys": {"questions": {"technical": [], "behavioral": []}},
    "wipro": {"questions": {"technical": [], "behavioral": []}},
}

_COMPANY_4_SPECS = [
    ("google", "coding", "Design a URL shortener.", "medium"),
    ("google", "coding", "Implement a trie with autocomplete.", "medium"),
    ("google", "system_design", "Design a distributed cache.", "hard"),
    ("google", "behavioral", "Tell me about a time you improved a system using data.", "medium"),
    ("amazon", "coding", "Implement a rate limiter.", "hard"),
    ("amazon", "coding", "Merge k sorted lists.", "hard"),
    ("amazon", "system_design", "Design an order processing pipeline.", "hard"),
    ("amazon", "behavioral", "Describe a time you owned a problem end to end.", "medium"),
    ("meta", "coding", "Implement top-k frequent elements.", "medium"),
    ("meta", "system_design", "Design a real-time feed ranking system.", "hard"),
    ("meta", "behavioral", "Tell me about a time you shipped a product quickly.", "medium"),
    ("tcs", "technical", "What is encapsulation in OOP?", "easy"),
    ("tcs", "technical", "What is the difference between stack and queue?", "easy"),
    ("tcs", "behavioral", "Tell me about a time you adapted to a team quickly.", "easy"),
    ("infosys", "technical", "What is the difference between compiler and interpreter?", "easy"),
    ("infosys", "technical", "What is SQL normalization?", "easy"),
    ("infosys", "behavioral", "Tell me about a time you solved a technical problem.", "easy"),
    ("wipro", "technical", "What is recursion?", "easy"),
    ("wipro", "technical", "What is the difference between array and linked list?", "easy"),
    ("wipro", "behavioral", "Tell me about a time you collaborated under pressure.", "easy"),
]

for i in range(800):
    cid, category, question, difficulty = _COMPANY_4_SPECS[i % len(_COMPANY_4_SPECS)]
    variant = i // len(_COMPANY_4_SPECS) + 1
    COMPANY_QUESTIONS_EXTRA_4[cid]["questions"][category].append({
        "id": f"{cid[:2]}4-{category[:4]}-{i + 1:04d}",
        "question": f"{question} Variant {variant}",
        "category": category,
        "difficulty": difficulty if i % 7 else ("hard" if cid in {"google", "amazon", "meta"} else "medium"),
        "company_id": cid,
        "company": cid.title() if cid != "tcs" else "TCS",
    })
