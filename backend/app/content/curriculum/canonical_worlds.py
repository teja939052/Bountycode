"""
Canonical 6-World Placement Curriculum
========================================

Service-placement campaign structure:
  World 1 — Placement Readiness
  World 2 — Aptitude Gauntlet
  World 3 — Coding Foundations
  World 4 — CS Core
  World 5 — Company Quests
  World 6 — Interview Arena

Each world has 32 levels.
This is the master curriculum. All roles and companies are overlays on top.
"""
from typing import Dict, List, Any

# World definitions
WORLDS = [
    {
        "world_id": "placement_readiness",
        "name": "Placement Readiness",
        "icon": "🎯",
        "subtitle": "Diagnose → Plan → Prepare",
        "description": "Start here. Diagnostic assessment, goal setting, and personalized campaign generation.",
        "color": "blue",
        "levels": 32,
    },
    {
        "world_id": "aptitude_gauntlet",
        "name": "Aptitude Gauntlet",
        "icon": "🧮",
        "subtitle": "Quant + Reasoning + Verbal",
        "description": "Daily timed mixed sets, weekly mocks, and weakness repair for service-company assessments.",
        "color": "amber",
        "levels": 32,
    },
    {
        "world_id": "coding_foundations",
        "name": "Coding Foundations",
        "icon": "💻",
        "subtitle": "Pseudocode → Programs → Debug",
        "description": "Core coding capabilities that matter for placement: output prediction, basic programs, debugging, and selected problems.",
        "color": "violet",
        "levels": 32,
    },
    {
        "world_id": "cs_core",
        "name": "CS Core",
        "icon": "📚",
        "subtitle": "OOP, DBMS, SQL, OS, CN",
        "description": "Learn, practice, and interview-proof the CS subjects asked in service-company written rounds.",
        "color": "emerald",
        "levels": 32,
    },
    {
        "world_id": "company_quests",
        "name": "Company Quests",
        "icon": "🏢",
        "subtitle": "TCS / Infosys / Wipro / Cognizant / Accenture / Capgemini",
        "description": "Company-specific overlays: most-asked topics, pattern drills, and mock formats for each target.",
        "color": "sky",
        "levels": 32,
    },
    {
        "world_id": "interview_arena",
        "name": "Interview Arena",
        "icon": "🎤",
        "subtitle": "Technical + HR + Full Mock",
        "description": "Practice under interview conditions: technical rounds, HR scenarios, project explanation, and full mocks.",
        "color": "rose",
        "levels": 32,
    },
]

# Level templates for each world
# Each level has: id, title, concept, skills, difficulty, est_minutes, diamonds
LEVEL_TEMPLATES: Dict[str, List[Dict[str, Any]]] = {
    "placement_readiness": [
        {"level": 1, "title": "What Are You Preparing For?", "concept": "goal_setting", "skills": ["placement.basics"], "difficulty": "beginner", "est_minutes": 10, "diamonds": 20},
        {"level": 2, "title": "Choose Your Target Company", "concept": "company_selection", "skills": ["placement.company"], "difficulty": "beginner", "est_minutes": 10, "diamonds": 20},
        {"level": 3, "title": "Set Your Assessment Date", "concept": "date_planning", "skills": ["placement.date"], "difficulty": "beginner", "est_minutes": 10, "diamonds": 20},
        {"level": 4, "title": "Placement Diagnostic 1", "concept": "diagnostic_basics", "skills": ["placement.diagnostic"], "difficulty": "beginner", "est_minutes": 12, "diamonds": 25},
        {"level": 5, "title": "Placement Diagnostic 2", "concept": "diagnostic_quant", "skills": ["placement.diagnostic"], "difficulty": "beginner", "est_minutes": 12, "diamonds": 25},
        {"level": 6, "title": "Placement Diagnostic 3", "concept": "diagnostic_coding", "skills": ["placement.diagnostic"], "difficulty": "beginner", "est_minutes": 12, "diamonds": 25},
        {"level": 7, "title": "Understand Your Baseline", "concept": "baseline_analysis", "skills": ["placement.baseline"], "difficulty": "beginner", "est_minutes": 12, "diamonds": 25},
        {"level": 8, "title": "Know Your Weaknesses", "concept": "weakness_mapping", "skills": ["placement.weakness"], "difficulty": "beginner", "est_minutes": 15, "diamonds": 30},
        {"level": 9, "title": "Build Your Campaign Plan", "concept": "campaign_planning", "skills": ["placement.planning"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 10, "title": "Daily Battle Strategy", "concept": "daily_strategy", "skills": ["placement.daily"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 11, "title": "Week 1-2: Foundations", "concept": "phase_foundations", "skills": ["placement.phases"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 12, "title": "Week 3-4: Practice", "concept": "phase_practice", "skills": ["placement.phases"], "difficulty": "intermediate", "est_minutes": 18, "diamonds": 35},
        {"level": 13, "title": "Week 5-6: Assessment", "concept": "phase_assessment", "skills": ["placement.phases"], "difficulty": "intermediate", "est_minutes": 18, "diamonds": 35},
        {"level": 14, "title": "Week 7-8: Interview", "concept": "phase_interview", "skills": ["placement.phases"], "difficulty": "intermediate", "est_minutes": 18, "diamonds": 35},
        {"level": 15, "title": "Track Progress", "concept": "progress_tracking", "skills": ["placement.progress"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 16, "title": "Adapt Your Plan", "concept": "plan_adaptation", "skills": ["placement.adaptation"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 17, "title": "Mock OA 1", "concept": "mock_oa", "skills": ["placement.mock"], "difficulty": "intermediate", "est_minutes": 20, "diamonds": 40},
        {"level": 18, "title": "Mock OA 2", "concept": "mock_oa", "skills": ["placement.mock"], "difficulty": "intermediate", "est_minutes": 20, "diamonds": 40},
        {"level": 19, "title": "Repair Weaknesses 1", "concept": "repair", "skills": ["placement.repair"], "difficulty": "intermediate", "est_minutes": 18, "diamonds": 40},
        {"level": 20, "title": "Repair Weaknesses 2", "concept": "repair", "skills": ["placement.repair"], "difficulty": "intermediate", "est_minutes": 18, "diamonds": 40},
        {"level": 21, "title": "Speed Drill 1", "concept": "speed_drill", "skills": ["placement.speed"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 35},
        {"level": 22, "title": "Speed Drill 2", "concept": "speed_drill", "skills": ["placement.speed"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 35},
        {"level": 23, "title": "Accuracy Drill 1", "concept": "accuracy_drill", "skills": ["placement.accuracy"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 35},
        {"level": 24, "title": "Accuracy Drill 2", "concept": "accuracy_drill", "skills": ["placement.accuracy"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 35},
        {"level": 25, "title": "Full Mock Assessment 1", "concept": "full_mock", "skills": ["placement.mock"], "difficulty": "advanced", "est_minutes": 30, "diamonds": 50},
        {"level": 26, "title": "Full Mock Assessment 2", "concept": "full_mock", "skills": ["placement.mock"], "difficulty": "advanced", "est_minutes": 30, "diamonds": 50},
        {"level": 27, "title": "Interview Readiness Check", "concept": "interview_readiness", "skills": ["placement.interview"], "difficulty": "advanced", "est_minutes": 20, "diamonds": 45},
        {"level": 28, "title": "Company-Specific Prep 1", "concept": "company_prep", "skills": ["placement.company"], "difficulty": "advanced", "est_minutes": 20, "diamonds": 45},
        {"level": 29, "title": "Company-Specific Prep 2", "concept": "company_prep", "skills": ["placement.company"], "difficulty": "advanced", "est_minutes": 20, "diamonds": 45},
        {"level": 30, "title": "Final Weakness Repair", "concept": "final_repair", "skills": ["placement.repair"], "difficulty": "advanced", "est_minutes": 25, "diamonds": 55},
        {"level": 31, "title": "Final Mock OA", "concept": "final_mock", "skills": ["placement.mock"], "difficulty": "expert", "est_minutes": 45, "diamonds": 80},
        {"level": 32, "title": "Placement Ready", "concept": "mastery", "skills": ["placement.mastery"], "difficulty": "expert", "est_minutes": 30, "diamonds": 100},
    ],
    "aptitude_gauntlet": [
        {"level": 1, "title": "Percentages Basics", "concept": "percentages_basics", "skills": ["quant.percentages"], "difficulty": "beginner", "est_minutes": 10, "diamonds": 20},
        {"level": 2, "title": "Percentage Change", "concept": "percentage_change", "skills": ["quant.percentages"], "difficulty": "beginner", "est_minutes": 10, "diamonds": 20},
        {"level": 3, "title": "Profit and Loss", "concept": "profit_loss", "skills": ["quant.profit_loss"], "difficulty": "beginner", "est_minutes": 12, "diamonds": 25},
        {"level": 4, "title": "Ratios and Proportions", "concept": "ratios", "skills": ["quant.ratios"], "difficulty": "beginner", "est_minutes": 12, "diamonds": 25},
        {"level": 5, "title": "Averages", "concept": "averages", "skills": ["quant.averages"], "difficulty": "beginner", "est_minutes": 12, "diamonds": 25},
        {"level": 6, "title": "Time and Work", "concept": "time_work", "skills": ["quant.time_work"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 7, "title": "Time Speed Distance", "concept": "tsd", "skills": ["quant.tsd"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 8, "title": "Simple and Compound Interest", "concept": "interest", "skills": ["quant.interest"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 9, "title": "Data Interpretation 1", "concept": "di_tables", "skills": ["quant.di"], "difficulty": "intermediate", "est_minutes": 18, "diamonds": 40},
        {"level": 10, "title": "Data Interpretation 2", "concept": "di_graphs", "skills": ["quant.di"], "difficulty": "intermediate", "est_minutes": 18, "diamonds": 40},
        {"level": 11, "title": "Number Systems", "concept": "number_systems", "skills": ["quant.numbers"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 35},
        {"level": 12, "title": "LCM and HCF", "concept": "lcm_hcf", "skills": ["quant.numbers"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 35},
        {"level": 13, "title": "Permutations and Combinations", "concept": "pnc", "skills": ["quant.pnc"], "difficulty": "advanced", "est_minutes": 20, "diamonds": 45},
        {"level": 14, "title": "Probability", "concept": "probability", "skills": ["quant.probability"], "difficulty": "advanced", "est_minutes": 20, "diamonds": 45},
        {"level": 15, "title": "Logarithms", "concept": "logarithms", "skills": ["quant.logarithms"], "difficulty": "advanced", "est_minutes": 20, "diamonds": 45},
        {"level": 16, "title": "Progressions", "concept": "progressions", "skills": ["quant.progressions"], "difficulty": "advanced", "est_minutes": 20, "diamonds": 50},
        {"level": 17, "title": "Geometry Basics", "concept": "geometry_basics", "skills": ["quant.geometry"], "difficulty": "advanced", "est_minutes": 22, "diamonds": 50},
        {"level": 18, "title": "Mensuration", "concept": "mensuration", "skills": ["quant.geometry"], "difficulty": "advanced", "est_minutes": 22, "diamonds": 50},
        {"level": 19, "title": "Blood Relations", "concept": "blood_relations", "skills": ["reason.relations"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 20, "title": "Coding-Decoding", "concept": "coding_decoding", "skills": ["reason.coding"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 21, "title": "Seating Arrangements", "concept": "seating_arrangements", "skills": ["reason.seating"], "difficulty": "intermediate", "est_minutes": 18, "diamonds": 35},
        {"level": 22, "title": "Puzzles", "concept": "puzzles", "skills": ["reason.puzzles"], "difficulty": "intermediate", "est_minutes": 18, "diamonds": 35},
        {"level": 23, "title": "Syllogisms", "concept": "syllogisms", "skills": ["reason.syllogisms"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 35},
        {"level": 24, "title": "Direction Sense", "concept": "direction_sense", "skills": ["reason.direction"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 35},
        {"level": 25, "title": "Grammar Basics", "concept": "grammar_basics", "skills": ["verbal.grammar"], "difficulty": "beginner", "est_minutes": 10, "diamonds": 20},
        {"level": 26, "title": "Sentence Correction", "concept": "sentence_correction", "skills": ["verbal.grammar"], "difficulty": "beginner", "est_minutes": 12, "diamonds": 25},
        {"level": 27, "title": "Reading Comprehension 1", "concept": "reading_comprehension", "skills": ["verbal.reading"], "difficulty": "beginner", "est_minutes": 12, "diamonds": 25},
        {"level": 28, "title": "Reading Comprehension 2", "concept": "reading_comprehension", "skills": ["verbal.reading"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 29, "title": "Synonyms and Antonyms", "concept": "vocabulary", "skills": ["verbal.vocabulary"], "difficulty": "intermediate", "est_minutes": 12, "diamonds": 25},
        {"level": 30, "title": "Idioms and Phrases", "concept": "idioms", "skills": ["verbal.vocabulary"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 31, "title": "Aptitude Mock OA", "concept": "mock_oa", "skills": ["aptitude.mock"], "difficulty": "expert", "est_minutes": 30, "diamonds": 70},
        {"level": 32, "title": "Aptitude Mastery", "concept": "mastery", "skills": ["aptitude.mastery"], "difficulty": "expert", "est_minutes": 35, "diamonds": 100},
    ],
    "coding_foundations": [
        {"level": 1, "title": "Pseudocode Basics", "concept": "pseudocode", "skills": ["code.pseudocode"], "difficulty": "beginner", "est_minutes": 10, "diamonds": 20},
        {"level": 2, "title": "Output Prediction 1", "concept": "output_prediction", "skills": ["code.prediction"], "difficulty": "beginner", "est_minutes": 10, "diamonds": 20},
        {"level": 3, "title": "Output Prediction 2", "concept": "output_prediction", "skills": ["code.prediction"], "difficulty": "beginner", "est_minutes": 10, "diamonds": 20},
        {"level": 4, "title": "Variables and Types", "concept": "variables", "skills": ["code.variables"], "difficulty": "beginner", "est_minutes": 12, "diamonds": 25},
        {"level": 5, "title": "Operators and Expressions", "concept": "operators", "skills": ["code.operators"], "difficulty": "beginner", "est_minutes": 12, "diamonds": 25},
        {"level": 6, "title": "Conditions", "concept": "conditions", "skills": ["code.conditions"], "difficulty": "intermediate", "est_minutes": 12, "diamonds": 25},
        {"level": 7, "title": "Loops 1: For and While", "concept": "loops", "skills": ["code.loops"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 8, "title": "Loops 2: Nested and Patterns", "concept": "nested_loops", "skills": ["code.loops"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 9, "title": "Functions", "concept": "functions", "skills": ["code.functions"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 10, "title": "Arrays and Lists", "concept": "arrays", "skills": ["code.arrays"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 35},
        {"level": 11, "title": "Strings", "concept": "strings", "skills": ["code.strings"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 35},
        {"level": 12, "title": "Dictionaries and Sets", "concept": "dicts_sets", "skills": ["code.dicts"], "difficulty": "intermediate", "est_minutes": 18, "diamonds": 40},
        {"level": 13, "title": "Debugging 1", "concept": "debugging", "skills": ["code.debugging"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 14, "title": "Debugging 2", "concept": "debugging", "skills": ["code.debugging"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 15, "title": "Two Pointers", "concept": "two_pointers", "skills": ["dsa.two_pointers"], "difficulty": "intermediate", "est_minutes": 18, "diamonds": 40},
        {"level": 16, "title": "Sliding Window", "concept": "sliding_window", "skills": ["dsa.sliding_window"], "difficulty": "intermediate", "est_minutes": 18, "diamonds": 40},
        {"level": 17, "title": "Binary Search", "concept": "binary_search", "skills": ["dsa.binary_search"], "difficulty": "intermediate", "est_minutes": 18, "diamonds": 40},
        {"level": 18, "title": "Basic Sorting", "concept": "sorting_basics", "skills": ["code.sorting"], "difficulty": "intermediate", "est_minutes": 18, "diamonds": 45},
        {"level": 19, "title": "Linked Lists 1", "concept": "linked_lists", "skills": ["dsa.linked_list"], "difficulty": "advanced", "est_minutes": 22, "diamonds": 45},
        {"level": 20, "title": "Linked Lists 2", "concept": "linked_lists", "skills": ["dsa.linked_list"], "difficulty": "advanced", "est_minutes": 22, "diamonds": 50},
        {"level": 21, "title": "Stacks and Queues", "concept": "stacks_queues", "skills": ["dsa.stack_queue"], "difficulty": "advanced", "est_minutes": 22, "diamonds": 50},
        {"level": 22, "title": "Trees 1: Traversals", "concept": "tree_traversals", "skills": ["dsa.trees"], "difficulty": "advanced", "est_minutes": 25, "diamonds": 50},
        {"level": 23, "title": "Trees 2: BST and AVL", "concept": "tree_advanced", "skills": ["dsa.trees"], "difficulty": "advanced", "est_minutes": 25, "diamonds": 55},
        {"level": 24, "title": "Graphs 1: BFS and DFS", "concept": "graph_traversals", "skills": ["dsa.graphs"], "difficulty": "advanced", "est_minutes": 25, "diamonds": 55},
        {"level": 25, "title": "Graphs 2: Shortest Path", "concept": "graph_algorithms", "skills": ["dsa.graphs"], "difficulty": "advanced", "est_minutes": 25, "diamonds": 55},
        {"level": 26, "title": "Dynamic Programming 1", "concept": "dp_basics", "skills": ["dsa.dp"], "difficulty": "expert", "est_minutes": 28, "diamonds": 60},
        {"level": 27, "title": "Dynamic Programming 2", "concept": "dp_advanced", "skills": ["dsa.dp"], "difficulty": "expert", "est_minutes": 28, "diamonds": 60},
        {"level": 28, "title": "SQL Fundamentals", "concept": "sql_basics", "skills": ["cs_fundamentals.sql"], "difficulty": "intermediate", "est_minutes": 20, "diamonds": 45},
        {"level": 29, "title": "Advanced SQL", "concept": "sql_advanced", "skills": ["cs_fundamentals.sql"], "difficulty": "advanced", "est_minutes": 25, "diamonds": 55},
        {"level": 30, "title": "OOP Concepts", "concept": "oop", "skills": ["cs_fundamentals.oops"], "difficulty": "intermediate", "est_minutes": 20, "diamonds": 45},
        {"level": 31, "title": "Coding Marathon", "concept": "code_marathon", "skills": ["code.marathon"], "difficulty": "expert", "est_minutes": 30, "diamonds": 70},
        {"level": 32, "title": "Coding Mastery", "concept": "mastery", "skills": ["code.mastery"], "difficulty": "expert", "est_minutes": 35, "diamonds": 100},
    ],
    "cs_core": [
        {"level": 1, "title": "OOP Basics", "concept": "oop_basics", "skills": ["cs_fundamentals.oops"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 25},
        {"level": 2, "title": "Inheritance and Polymorphism", "concept": "inheritance", "skills": ["cs_fundamentals.oops"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 25},
        {"level": 3, "title": "Abstraction and Encapsulation", "concept": "abstraction", "skills": ["cs_fundamentals.oops"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 25},
        {"level": 4, "title": "DBMS Basics", "concept": "dbms_basics", "skills": ["cs_fundamentals.dbms"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 25},
        {"level": 5, "title": "Primary Key and Foreign Key", "concept": "keys", "skills": ["cs_fundamentals.dbms"], "difficulty": "intermediate", "est_minutes": 12, "diamonds": 25},
        {"level": 6, "title": "Normalization", "concept": "normalization", "skills": ["cs_fundamentals.dbms"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 7, "title": "SQL Joins", "concept": "sql_joins", "skills": ["cs_fundamentals.sql"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 8, "title": "SQL Subqueries", "concept": "sql_subqueries", "skills": ["cs_fundamentals.sql"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 9, "title": "Indexes and Transactions", "concept": "indexes", "skills": ["cs_fundamentals.dbms"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 10, "title": "OS Basics", "concept": "os_basics", "skills": ["cs_fundamentals.os"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 11, "title": "Processes and Threads", "concept": "processes_threads", "skills": ["cs_fundamentals.os"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 12, "title": "Scheduling", "concept": "scheduling", "skills": ["cs_fundamentals.os"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 13, "title": "Memory Management", "concept": "memory_management", "skills": ["cs_fundamentals.os"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 14, "title": "CN Basics", "concept": "cn_basics", "skills": ["cs_fundamentals.cn"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 15, "title": "OSI Model", "concept": "osi_model", "skills": ["cs_fundamentals.cn"], "difficulty": "intermediate", "est_minutes": 12, "diamonds": 25},
        {"level": 16, "title": "TCP/IP", "concept": "tcp_ip", "skills": ["cs_fundamentals.cn"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 17, "title": "HTTP and HTTPS", "concept": "http_https", "skills": ["cs_fundamentals.cn"], "difficulty": "intermediate", "est_minutes": 12, "diamonds": 25},
        {"level": 18, "title": "Project Explanation 1", "concept": "project_explanation", "skills": ["interview.project"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 19, "title": "Project Explanation 2", "concept": "project_explanation", "skills": ["interview.project"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 20, "title": "OOPS Interview Q1", "concept": "interview_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 21, "title": "OOPS Interview Q2", "concept": "interview_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 22, "title": "DBMS Interview Q1", "concept": "interview_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 23, "title": "DBMS Interview Q2", "concept": "interview_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 24, "title": "OS Interview Q1", "concept": "interview_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 25, "title": "OS Interview Q2", "concept": "interview_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 26, "title": "CN Interview Q1", "concept": "interview_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 27, "title": "CN Interview Q2", "concept": "interview_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 28, "title": "SQL Interview Q1", "concept": "interview_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 29, "title": "SQL Interview Q2", "concept": "interview_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 30, "title": "CS Core Mock 1", "concept": "mock", "skills": ["cs_fundamentals.mock"], "difficulty": "advanced", "est_minutes": 30, "diamonds": 50},
        {"level": 31, "title": "CS Core Mock 2", "concept": "mock", "skills": ["cs_fundamentals.mock"], "difficulty": "advanced", "est_minutes": 30, "diamonds": 50},
        {"level": 32, "title": "CS Core Mastery", "concept": "mastery", "skills": ["cs_fundamentals.mastery"], "difficulty": "expert", "est_minutes": 35, "diamonds": 100},
    ],
    "company_quests": [
        {"level": 1, "title": "TCS NQT Overview", "concept": "company_overview", "skills": ["company.tcs"], "difficulty": "beginner", "est_minutes": 10, "diamonds": 20},
        {"level": 2, "title": "TCS NQT Quant", "concept": "company_quant", "skills": ["company.tcs"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 3, "title": "TCS NQT Reasoning", "concept": "company_reasoning", "skills": ["company.tcs"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 4, "title": "TCS NQT Verbal", "concept": "company_verbal", "skills": ["company.tcs"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 5, "title": "TCS NQT Coding", "concept": "company_coding", "skills": ["company.tcs"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 6, "title": "Infosys InfyTQ Overview", "concept": "company_overview", "skills": ["company.infosys"], "difficulty": "beginner", "est_minutes": 10, "diamonds": 20},
        {"level": 7, "title": "Infosys DSA", "concept": "company_dsa", "skills": ["company.infosys"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 8, "title": "Infosys Pseudocode", "concept": "company_pseudocode", "skills": ["company.infosys"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 9, "title": "Wipro NLTH Overview", "concept": "company_overview", "skills": ["company.wipro"], "difficulty": "beginner", "est_minutes": 10, "diamonds": 20},
        {"level": 10, "title": "Wipro Reasoning", "concept": "company_reasoning", "skills": ["company.wipro"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 11, "title": "Wipro Coding", "concept": "company_coding", "skills": ["company.wipro"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 12, "title": "Accenture AMCAT Overview", "concept": "company_overview", "skills": ["company.accenture"], "difficulty": "beginner", "est_minutes": 10, "diamonds": 20},
        {"level": 13, "title": "Accenture Quant", "concept": "company_quant", "skills": ["company.accenture"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 14, "title": "Accenture English", "concept": "company_verbal", "skills": ["company.accenture"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 15, "title": "Cognizant Overview", "concept": "company_overview", "skills": ["company.cognizant"], "difficulty": "beginner", "est_minutes": 10, "diamonds": 20},
        {"level": 16, "title": "Capgemini Overview", "concept": "company_overview", "skills": ["company.capgemini"], "difficulty": "beginner", "est_minutes": 10, "diamonds": 20},
        {"level": 17, "title": "Company Pattern Drill 1", "concept": "company_patterns", "skills": ["company.patterns"], "difficulty": "intermediate", "est_minutes": 20, "diamonds": 45},
        {"level": 18, "title": "Company Pattern Drill 2", "concept": "company_patterns", "skills": ["company.patterns"], "difficulty": "intermediate", "est_minutes": 20, "diamonds": 45},
        {"level": 19, "title": "Company Mock 1", "concept": "company_mock", "skills": ["company.mock"], "difficulty": "intermediate", "est_minutes": 30, "diamonds": 50},
        {"level": 20, "title": "Company Mock 2", "concept": "company_mock", "skills": ["company.mock"], "difficulty": "intermediate", "est_minutes": 30, "diamonds": 50},
        {"level": 21, "title": "Most Asked Topics 1", "concept": "most_asked", "skills": ["company.topics"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 35},
        {"level": 22, "title": "Most Asked Topics 2", "concept": "most_asked", "skills": ["company.topics"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 35},
        {"level": 23, "title": "Speed Drill 1", "concept": "speed_drill", "skills": ["company.speed"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 35},
        {"level": 24, "title": "Speed Drill 2", "concept": "speed_drill", "skills": ["company.speed"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 35},
        {"level": 25, "title": "Weakness Repair 1", "concept": "repair", "skills": ["company.repair"], "difficulty": "intermediate", "est_minutes": 18, "diamonds": 40},
        {"level": 26, "title": "Weakness Repair 2", "concept": "repair", "skills": ["company.repair"], "difficulty": "intermediate", "est_minutes": 18, "diamonds": 40},
        {"level": 27, "title": "Company-Specific Prep 1", "concept": "company_prep", "skills": ["company.prep"], "difficulty": "advanced", "est_minutes": 20, "diamonds": 45},
        {"level": 28, "title": "Company-Specific Prep 2", "concept": "company_prep", "skills": ["company.prep"], "difficulty": "advanced", "est_minutes": 20, "diamonds": 45},
        {"level": 29, "title": "Full Company Mock 1", "concept": "full_mock", "skills": ["company.mock"], "difficulty": "advanced", "est_minutes": 45, "diamonds": 80},
        {"level": 30, "title": "Full Company Mock 2", "concept": "full_mock", "skills": ["company.mock"], "difficulty": "advanced", "est_minutes": 45, "diamonds": 80},
        {"level": 31, "title": "Company Readiness Check", "concept": "readiness", "skills": ["company.readiness"], "difficulty": "expert", "est_minutes": 30, "diamonds": 70},
        {"level": 32, "title": "Company Ready", "concept": "mastery", "skills": ["company.mastery"], "difficulty": "expert", "est_minutes": 30, "diamonds": 100},
    ],
    "interview_arena": [
        {"level": 1, "title": "Tell Me About Yourself", "concept": "introduction", "skills": ["interview.intro"], "difficulty": "beginner", "est_minutes": 10, "diamonds": 20},
        {"level": 2, "title": "Strengths and Weaknesses", "concept": "strengths_weaknesses", "skills": ["interview.self"], "difficulty": "beginner", "est_minutes": 12, "diamonds": 25},
        {"level": 3, "title": "Why This Role", "concept": "motivation", "skills": ["interview.motivation"], "difficulty": "beginner", "est_minutes": 12, "diamonds": 25},
        {"level": 4, "title": "Why This Company", "concept": "company_knowledge", "skills": ["interview.company"], "difficulty": "beginner", "est_minutes": 12, "diamonds": 25},
        {"level": 5, "title": "OOP Interview Q1", "concept": "technical_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 6, "title": "OOP Interview Q2", "concept": "technical_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 7, "title": "DBMS Interview Q1", "concept": "technical_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 8, "title": "DBMS Interview Q2", "concept": "technical_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 9, "title": "SQL Interview Q1", "concept": "technical_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 10, "title": "SQL Interview Q2", "concept": "technical_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 11, "title": "OS Interview Q1", "concept": "technical_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 12, "title": "OS Interview Q2", "concept": "technical_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 13, "title": "CN Interview Q1", "concept": "technical_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 14, "title": "CN Interview Q2", "concept": "technical_q", "skills": ["interview.technical"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 15, "title": "Project Explanation 1", "concept": "project_explanation", "skills": ["interview.project"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 16, "title": "Project Explanation 2", "concept": "project_explanation", "skills": ["interview.project"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 17, "title": "HR Scenario 1", "concept": "hr_scenario", "skills": ["interview.hr"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 18, "title": "HR Scenario 2", "concept": "hr_scenario", "skills": ["interview.hr"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 19, "title": "Behavioral Q1", "concept": "behavioral", "skills": ["interview.behavioral"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 20, "title": "Behavioral Q2", "concept": "behavioral", "skills": ["interview.behavioral"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 21, "title": "Stress Interview 1", "concept": "stress_interview", "skills": ["interview.stress"], "difficulty": "advanced", "est_minutes": 15, "diamonds": 35},
        {"level": 22, "title": "Stress Interview 2", "concept": "stress_interview", "skills": ["interview.stress"], "difficulty": "advanced", "est_minutes": 15, "diamonds": 35},
        {"level": 23, "title": "Mock Technical 1", "concept": "mock_technical", "skills": ["interview.mock"], "difficulty": "advanced", "est_minutes": 30, "diamonds": 50},
        {"level": 24, "title": "Mock Technical 2", "concept": "mock_technical", "skills": ["interview.mock"], "difficulty": "advanced", "est_minutes": 30, "diamonds": 50},
        {"level": 25, "title": "Mock HR 1", "concept": "mock_hr", "skills": ["interview.mock"], "difficulty": "advanced", "est_minutes": 20, "diamonds": 40},
        {"level": 26, "title": "Mock HR 2", "concept": "mock_hr", "skills": ["interview.mock"], "difficulty": "advanced", "est_minutes": 20, "diamonds": 40},
        {"level": 27, "title": "Full Mock Interview 1", "concept": "full_mock", "skills": ["interview.full"], "difficulty": "advanced", "est_minutes": 45, "diamonds": 80},
        {"level": 28, "title": "Full Mock Interview 2", "concept": "full_mock", "skills": ["interview.full"], "difficulty": "advanced", "est_minutes": 45, "diamonds": 80},
        {"level": 29, "title": "Communication Drill 1", "concept": "communication", "skills": ["interview.communication"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 30, "title": "Communication Drill 2", "concept": "communication", "skills": ["interview.communication"], "difficulty": "intermediate", "est_minutes": 15, "diamonds": 30},
        {"level": 31, "title": "Interview Readiness Check", "concept": "readiness", "skills": ["interview.readiness"], "difficulty": "expert", "est_minutes": 30, "diamonds": 70},
        {"level": 32, "title": "Interview Ready", "concept": "mastery", "skills": ["interview.mastery"], "difficulty": "expert", "est_minutes": 30, "diamonds": 100},
    ],
}


def get_world(world_id: str) -> Dict[str, Any]:
    for w in WORLDS:
        if w["world_id"] == world_id:
            return w
    return {}


def get_all_worlds() -> List[Dict[str, Any]]:
    return list(WORLDS)


def get_level(world_id: str, level_number: int) -> Dict[str, Any]:
    levels = LEVEL_TEMPLATES.get(world_id, [])
    for level in levels:
        if level["level"] == level_number:
            return level
    return {}


def get_all_levels(world_id: str) -> List[Dict[str, Any]]:
    return list(LEVEL_TEMPLATES.get(world_id, []))


def get_next_level(world_id: str, current_level: int) -> Dict[str, Any]:
    levels = LEVEL_TEMPLATES.get(world_id, [])
    for level in levels:
        if level["level"] > current_level:
            return level
    return {}


def get_previous_levels(world_id: str, current_level: int, count: int = 3) -> List[Dict[str, Any]]:
    levels = LEVEL_TEMPLATES.get(world_id, [])
    result = []
    for level in levels:
        if level["level"] < current_level:
            result.append(level)
    return result[-count:] if result else []


def get_world_progress(world_id: str, completed_levels: List[int]) -> Dict[str, Any]:
    levels = LEVEL_TEMPLATES.get(world_id, [])
    total = len(levels)
    completed = sum(1 for l in levels if l["level"] in completed_levels)
    return {
        "world_id": world_id,
        "total_levels": total,
        "completed_levels": completed,
        "progress_percent": round((completed / total) * 100) if total else 0,
        "remaining_levels": total - completed,
    }
