"""Capability-Based Curriculum Engine — the new learning model.

Not topic chapters. Not lecture → quiz → XP.

This is: Role → Competency → Scenario → Simulation → Practice → Assessment → Mastery → Readiness.

Every unit is a MISSION that trains a specific job capability through a simulation loop:
  Context → Goal → Explore → Predict → Build → Break → Debug → Real-World Task → Assessment → Mastery

The 8 SDE Worlds:
  1. Code Foundations — build real things that work
  2. Problem Solver — DSA through real scenarios
  3. Build Systems — APIs, databases, scaling
  4. Work with Data — SQL, schema, joins, indexing
  5. Software Engineering — git, debugging, code quality
  6. Engineering Under Pressure — timed, ambiguous, buggy
  7. Hiring Arena — OA simulation, interview, prove it
  8. Company Missions — personalized per-target company
"""

from datetime import datetime, timezone


# ─── Mission Step Types ───
# Each step in a mission simulation loop has a type that determines
# how the frontend renders and interacts with it.
STEP_TYPES = {
    "context": "Set the scene — what system are you working on?",
    "goal": "What must you accomplish?",
    "explore": "Interactive sandbox — run code, inspect data, see what breaks",
    "predict": "Multiple choice or short answer — make a prediction before seeing the answer",
    "build": "Write code — hidden tests verify correctness",
    "break": "Deliberately inject bad input — observe failure modes",
    "debug": "Given buggy code + failing tests — find and fix the bug",
    "real_world": "Remove scaffolding — full requirements + hidden tests, no hints",
    "assessment": "Timed mastery trial — prove you can do it independently",
    "reflection": "Explain your approach — what did you learn, what was hard?",
}

# ─── Mission Structure ───
# Each mission follows the simulation loop:
#   context → goal → explore → predict → build → break → debug → real_world → assessment → mastery


# ══════════════════════════════════════════════════════════════════════════════
# WORLD 1 — CODE FOUNDATIONS
# "Can you write programs that handle real input, process data, and produce output?"
# ══════════════════════════════════════════════════════════════════════════════

WORLD_1 = {
    "id": "code_foundations",
    "title": "Code Foundations",
    "icon": "⌨️",
    "description": "Build programs that actually work with real input",
    "order": 1,
    "competencies": [
        {
            "id": "validator",
            "title": "Build a Validator",
            "skills_taught": ["variables", "types", "conditions", "type_conversion"],
            "scenario": "You're building the registration system for a college placement portal. Users enter Name, Age, CGPA, Email. The app is crashing on bad input.",
            "goal": "Make the registration system survive bad input.",
            "steps": [
                {
                    "type": "context",
                    "title": "The Broken Registration System",
                    "content": "A college placement portal lets students register. But users keep entering bad data and the app crashes.",
                    "simulation": {
                        "type": "interactive_terminal",
                        "initial_state": 'Student Registration\nName: Rahul\nAge: nineteen\n\n❌ Application crashed: TypeError: unsupported operand type(s) for +: \'str\' and \'int\'',
                        "user_can_run": True,
                    },
                },
                {
                    "type": "explore",
                    "title": "Investigate the Crash",
                    "content": "Run this code and see what happens.",
                    "code": 'age = "nineteen"\nresult = age + 1\nprint(result)',
                    "expected_output": "TypeError: can only concatenate str (not \"int\") to str",
                    "hint": "What happens when you try to add a number to text?",
                },
                {
                    "type": "predict",
                    "title": "What Happened?",
                    "question": "The application crashed because:",
                    "options": [
                        {"id": "a", "text": "The computer doesn't understand names", "correct": False},
                        {"id": "b", "text": "Age needs to be a number, not text", "correct": True},
                        {"id": "c", "text": "The print function is broken", "correct": False},
                        {"id": "d", "text": "The internet connection failed", "correct": False},
                    ],
                    "explanation": "Age was given as text ('nineteen') but the program tried to do math with it. Computers need numbers for calculations.",
                },
                {
                    "type": "explore",
                    "title": "Inspect the Value",
                    "content": "Check what type Python thinks this value is.",
                    "code": 'age = "nineteen"\nprint(type(age))\nprint(type(19))',
                    "expected_output": "<class 'str'>\n<class 'int'>",
                    "hint": "Python has a built-in type() function.",
                },
                {
                    "type": "build",
                    "title": "Fix the Registration",
                    "content": "Write a function that safely converts input to the right type.",
                    "function_name": "validate_age",
                    "signature": "def validate_age(input_value) -> int:",
                    "description": "Convert input_value to an integer. If it can't be converted, return -1.",
                    "test_cases": [
                        {"input": "19", "expected": 19},
                        {"input": "nineteen", "expected": -1},
                        {"input": "-5", "expected": -5},
                        {"input": "3.14", "expected": 3},
                        {"input": "hello", "expected": -1},
                    ],
                    "hidden_tests": 3,
                    "xp": 30,
                },
                {
                    "type": "break",
                    "title": "Break It Yourself",
                    "content": "Now try these inputs. Which ones should the app accept?",
                    "inputs_to_try": ["19", "-2", "130", "hello", "0", "200"],
                    "question": "Which ages are valid for a student? (Select all that apply)",
                    "correct_set": ["19", "0"],
                    "explanation": "A student's age should be 0-120 (reasonable range). Negative ages and 200 don't make sense.",
                },
                {
                    "type": "build",
                    "title": "Build the Full Validator",
                    "content": "Write a function that validates a student registration.",
                    "function_name": "register_student",
                    "signature": "def register_student(name, age, cgpa, email) -> str:",
                    "description": "Return 'Valid' if all fields pass validation: name is non-empty string, age is 0-120, cgpa is 0.0-10.0, email contains '@'. Otherwise return 'Invalid: <reason>'.",
                    "test_cases": [
                        {"input": ["Rahul", "19", "8.5", "rahul@college.edu"], "expected": "Valid"},
                        {"input": ["", "19", "8.5", "rahul@college.edu"], "expected": "Invalid: name"},
                        {"input": ["Rahul", "-5", "8.5", "rahul@college.edu"], "expected": "Invalid: age"},
                        {"input": ["Rahul", "19", "11.0", "rahul@college.edu"], "expected": "Invalid: cgpa"},
                        {"input": ["Rahul", "19", "8.5", "rahul"], "expected": "Invalid: email"},
                    ],
                    "hidden_tests": 5,
                    "xp": 50,
                },
                {
                    "type": "assessment",
                    "title": "Registration Boss",
                    "content": "Build a complete order validator. No hints. 12 minutes.",
                    "timed": True,
                    "time_limit_minutes": 12,
                    "function_name": "validate_order",
                    "signature": "def validate_order(order_id, items, total, payment_method) -> dict:",
                    "description": "Validate an e-commerce order. order_id must be alphanumeric, items must be a non-empty list, total must be positive, payment_method must be one of ['card', 'upi', 'cod']. Return {'valid': True} or {'valid': False, 'errors': [...]}",
                    "test_cases": [
                        {"input": ["ORD001", ["item1"], "299.99", "card"], "expected": {"valid": True}},
                        {"input": ["", ["item1"], "299.99", "card"], "expected": {"valid": False, "errors": ["invalid order_id"]}},
                        {"input": ["ORD002", [], "100", "card"], "expected": {"valid": False, "errors": ["empty items"]}},
                        {"input": ["ORD003", ["item1"], "-50", "card"], "expected": {"valid": False, "errors": ["invalid total"]}},
                        {"input": ["ORD004", ["item1"], "100", "bitcoin"], "expected": {"valid": False, "errors": ["invalid payment method"]}},
                    ],
                    "hidden_tests": 8,
                    "xp": 100,
                    "mastery_threshold": 70,
                },
            ],
            "mastery_xp": 150,
        },
        {
            "id": "command_processor",
            "title": "Build a Command Processor",
            "skills_taught": ["loops", "functions", "strings", "string_methods"],
            "scenario": "You're building a CLI tool for a dev team. It processes user commands.",
            "goal": "Build a command processor that parses and executes text commands.",
            "steps": [
                {
                    "type": "context",
                    "title": "The CLI Tool",
                    "content": "A team needs a command-line tool that processes text commands like 'add 5', 'multiply 3', 'reverse hello'.",
                    "simulation": {
                        "type": "interactive_terminal",
                        "initial_state": '> add 5\n???\n> reverse hello\n???',
                    },
                },
                {
                    "type": "explore",
                    "title": "String Splitting",
                    "content": "How do we break 'add 5' into parts?",
                    "code": 'cmd = "add 5"\nparts = cmd.split(" ")\nprint(parts)\nprint(parts[0])\nprint(parts[1])',
                    "expected_output": "['add', '5']\nadd\n5",
                },
                {
                    "type": "build",
                    "title": "Parse Commands",
                    "content": "Write a function that parses a command string.",
                    "function_name": "parse_command",
                    "signature": "def parse_command(cmd: str) -> dict:",
                    "description": "Parse 'add 5' into {'operation': 'add', 'value': 5}. Handle: add, subtract, multiply, divide. Return {'error': 'unknown command'} for invalid commands.",
                    "test_cases": [
                        {"input": ["add 5"], "expected": {"operation": "add", "value": 5}},
                        {"input": ["multiply 3"], "expected": {"operation": "multiply", "value": 3}},
                        {"input": ["reverse hello"], "expected": {"operation": "reverse", "value": "hello"}},
                        {"input": ["unknown"], "expected": {"error": "unknown command"}},
                    ],
                    "hidden_tests": 5,
                    "xp": 40,
                },
                {
                    "type": "build",
                    "title": "Execute Commands in a Loop",
                    "content": "Write a function that processes a list of commands.",
                    "function_name": "execute_commands",
                    "signature": "def execute_commands(commands: list) -> list:",
                    "description": "Process each command. Start with value=0. 'add N' adds N, 'subtract N' subtracts N, 'multiply N' multiplies. Return the list of results.",
                    "test_cases": [
                        {"input": [["add 5", "add 3"]], "expected": [5, 8]},
                        {"input": [["add 10", "subtract 3", "multiply 2"]], "expected": [10, 7, 14]},
                        {"input": [["add 5", "unknown", "add 1"]], "expected": [5, "error", 6]},
                    ],
                    "hidden_tests": 5,
                    "xp": 60,
                },
                {
                    "type": "assessment",
                    "title": "CLI Boss",
                    "content": "Build a text processor that handles multiple command types. 10 minutes.",
                    "timed": True,
                    "time_limit_minutes": 10,
                    "function_name": "process_text",
                    "signature": "def process_text(text: str, commands: list) -> str:",
                    "description": "Apply commands to text: 'uppercase' → all caps, 'reverse' → reversed, 'count X' → count occurrences of X, 'replace X Y' → replace X with Y. Apply in order.",
                    "test_cases": [
                        {"input": ["hello world", ["uppercase"]], "expected": "HELLO WORLD"},
                        {"input": ["hello", ["reverse", "uppercase"]], "expected": "OLLEH"},
                        {"input": ["banana", ["count a"]], "expected": "3"},
                        {"input": ["hello world", ["replace o 0"]], "expected": "hell0 w0rld"},
                    ],
                    "hidden_tests": 8,
                    "xp": 100,
                    "mastery_threshold": 70,
                },
            ],
            "mastery_xp": 150,
        },
        {
            "id": "api_parser",
            "title": "Repair a Broken API Parser",
            "skills_taught": ["data_structures", "exceptions", "debugging", "json"],
            "scenario": "A colleague's API response parser keeps crashing. Fix it.",
            "goal": "Make the parser handle all edge cases gracefully.",
            "steps": [
                {
                    "type": "context",
                    "title": "The Crashing Parser",
                    "content": "An API returns JSON data but the parser crashes on missing fields, wrong types, and empty responses.",
                },
                {
                    "type": "debug",
                    "title": "Find the Bug",
                    "buggy_code": 'def parse_user(data):\n    name = data["name"]\n    age = data["age"]\n    return f"{name} is {age} years old"',
                    "failing_input": {"age": 25},
                    "error": "KeyError: 'name'",
                    "question": "What's wrong? Fix the code.",
                    "hint": "Not all API responses have all fields.",
                    "xp": 30,
                },
                {
                    "type": "build",
                    "title": "Robust Parser",
                    "content": "Write a parser that handles all edge cases.",
                    "function_name": "safe_parse",
                    "signature": "def safe_parse(data: dict) -> dict:",
                    "description": "Parse user data safely. Required fields: name (str), age (int 0-150). Optional: email (str with @), skills (list of str). Return {'error': reason} for invalid data. Return parsed data with defaults for missing optional fields.",
                    "test_cases": [
                        {"input": [{"name": "Rahul", "age": 22}], "expected": {"name": "Rahul", "age": 22, "email": None, "skills": []}},
                        {"input": [{"name": "Rahul", "age": -1}], "expected": {"error": "invalid age"}},
                        {"input": [{}], "expected": {"error": "missing name"}},
                        {"input": [{"name": "X", "age": 20, "email": "x@y.com", "skills": ["Python"]}], "expected": {"name": "X", "age": 20, "email": "x@y.com", "skills": ["Python"]}},
                    ],
                    "hidden_tests": 6,
                    "xp": 60,
                },
                {
                    "type": "assessment",
                    "title": "Parser Boss",
                    "content": "Build a complete data normalizer. 10 minutes.",
                    "timed": True,
                    "time_limit_minutes": 10,
                    "function_name": "normalize",
                    "signature": "def normalize(records: list) -> list:",
                    "description": "Normalize a list of user records. Each record may have name, age, email, department. Standardize: name title-cased, age as int, email lowercased, department from valid set ['engineering', 'design', 'marketing', 'sales']. Skip invalid records (count them). Return {'valid': [...], 'invalid_count': N}.",
                    "test_cases": [
                        {"input": [[{"name": "rahul", "age": "22", "email": "X@Y.COM", "department": "engineering"}]], "expected": {"valid": [{"name": "Rahul", "age": 22, "email": "x@y.com", "department": "engineering"}], "invalid_count": 0}},
                        {"input": [[{"age": 22}]], "expected": {"valid": [], "invalid_count": 1}},
                    ],
                    "hidden_tests": 8,
                    "xp": 100,
                    "mastery_threshold": 70,
                },
            ],
            "mastery_xp": 150,
        },
        {
            "id": "small_cli",
            "title": "Build a Small CLI",
            "skills_taught": ["modules", "files", "input_output", "error_handling"],
            "scenario": "Build a note-taking CLI that saves to a file.",
            "goal": "Create a working CLI app with file persistence.",
            "steps": [
                {
                    "type": "build",
                    "title": "Note Storage",
                    "content": "Write functions to save and load notes from a file.",
                    "function_name": "save_notes",
                    "signature": "def save_notes(notes: list, filename: str) -> None:",
                    "description": "Save a list of notes (strings) to a file, one per line.",
                    "test_cases": [
                        {"input": [["Hello", "World"], "test.txt"], "expected": None, "side_effect_file": "test.txt", "expected_file_content": "Hello\nWorld"},
                    ],
                    "hidden_tests": 3,
                    "xp": 40,
                },
                {
                    "type": "build",
                    "title": "Full CLI",
                    "content": "Build the complete note-taking CLI logic.",
                    "function_name": "process_command",
                    "signature": "def process_command(cmd: str, notes: list) -> tuple:",
                    "description": "Handle: 'add X' adds note, 'list' returns all notes, 'delete N' removes note N (1-indexed), 'search X' finds notes containing X. Return (updated_notes, result_string).",
                    "test_cases": [
                        {"input": ["add Buy milk", []], "expected": (["Buy milk"], "Added: Buy milk")},
                        {"input": ["list", ["A", "B"]], "expected": (["A", "B"], "1. A\n2. B")},
                        {"input": ["delete 1", ["A", "B"]], "expected": (["B"], "Deleted: A")},
                        {"input": ["search milk", ["Buy milk", "Buy eggs"]], "expected": (["Buy milk", "Buy eggs"], "Found: Buy milk")},
                    ],
                    "hidden_tests": 6,
                    "xp": 80,
                },
                {
                    "type": "assessment",
                    "title": "CLI Boss",
                    "content": "Build a task manager CLI. 12 minutes.",
                    "timed": True,
                    "time_limit_minutes": 12,
                    "function_name": "task_manager",
                    "signature": "def task_manager(commands: list) -> list:",
                    "description": "Process task commands: 'add X' (add task), 'done N' (mark complete), 'list' (show all with status), 'stats' (return {'total': N, 'done': N, 'pending': N}). Track completion status.",
                    "test_cases": [
                        {"input": [["add Task1", "add Task2", "done 1", "stats"]], "expected": [{"total": 2, "done": 1, "pending": 1}]},
                    ],
                    "hidden_tests": 8,
                    "xp": 100,
                    "mastery_threshold": 70,
                },
            ],
            "mastery_xp": 150,
        },
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# WORLD 2 — PROBLEM SOLVER
# "Can you solve unfamiliar problems using the right data structures?"
# ══════════════════════════════════════════════════════════════════════════════

WORLD_2 = {
    "id": "problem_solver",
    "title": "Problem Solver",
    "icon": "🧩",
    "description": "Solve real problems with the right algorithms",
    "order": 2,
    "prerequisites": ["code_foundations"],
    "competencies": [
        {
            "id": "delivery_route",
            "title": "Delivery Route",
            "skills_taught": ["arrays", "searching", "sorting", "linear_search"],
            "scenario": "You're building a delivery system. Find the closest available warehouse to a customer.",
            "goal": "Build a function that finds the nearest warehouse.",
            "steps": [
                {
                    "type": "context",
                    "title": "The Delivery Problem",
                    "content": "A logistics company has 5 warehouses at different distances. A customer places an order. Find the closest available one.",
                    "data": {"warehouses": [{"name": "A", "distance": 12, "available": True}, {"name": "B", "distance": 5, "available": False}, {"name": "C", "distance": 8, "available": True}, {"name": "D", "distance": 15, "available": True}, {"name": "E", "distance": 3, "available": True}]},
                },
                {
                    "type": "explore",
                    "title": "Try the Naive Approach",
                    "content": "Try to find the closest warehouse by checking each one.",
                    "code": 'warehouses = [\n    {"name": "A", "distance": 12, "available": True},\n    {"name": "B", "distance": 5, "available": False},\n    {"name": "C", "distance": 8, "available": True},\n]\n\n# Your approach here\nfor wh in warehouses:\n    if wh["available"]:\n        print(f"{wh[\'name\']}: {wh[\'distance\']}km")',
                },
                {
                    "type": "build",
                    "title": "Find Closest Warehouse",
                    "content": "Write a function that finds the closest available warehouse.",
                    "function_name": "find_closest",
                    "signature": "def find_closest(warehouses: list) -> str:",
                    "description": "Return the name of the closest available warehouse. If none available, return 'None'.",
                    "test_cases": [
                        {"input": [[{"name": "A", "distance": 10, "available": True}, {"name": "B", "distance": 5, "available": True}]], "expected": "B"},
                        {"input": [[{"name": "A", "distance": 10, "available": False}]], "expected": "None"},
                        {"input": [[{"name": "A", "distance": 20, "available": True}, {"name": "B", "distance": 5, "available": False}, {"name": "C", "distance": 15, "available": True}]], "expected": "C"},
                    ],
                    "hidden_tests": 5,
                    "xp": 40,
                },
                {
                    "type": "build",
                    "title": "Sort and Search",
                    "content": "Now sort warehouses by distance and find the nearest 3.",
                    "function_name": "nearest_warehouses",
                    "signature": "def nearest_warehouses(warehouses: list, n: int = 3) -> list:",
                    "description": "Return the n nearest available warehouses sorted by distance. Each item: {'name': str, 'distance': int}.",
                    "test_cases": [
                        {"input": [[{"name": "A", "distance": 10, "available": True}, {"name": "B", "distance": 3, "available": True}, {"name": "C", "distance": 7, "available": True}, {"name": "D", "distance": 1, "available": True}], 2], "expected": [{"name": "D", "distance": 1}, {"name": "B", "distance": 3}]},
                    ],
                    "hidden_tests": 5,
                    "xp": 60,
                },
                {
                    "type": "assessment",
                    "title": "Delivery Boss",
                    "content": "Build a priority delivery system. 15 minutes.",
                    "timed": True,
                    "time_limit_minutes": 15,
                    "function_name": "assign_deliveries",
                    "signature": "def assign_deliveries(orders: list, warehouses: list) -> list:",
                    "description": "Assign each order to the nearest available warehouse. Once assigned, a warehouse's capacity decreases by 1. Return list of {order_id, warehouse_name, distance}. If no warehouse available, assign None.",
                    "test_cases": [
                        {"input": [[{"id": "O1", "location": 5}, {"id": "O2", "location": 12}], [{"name": "W1", "location": 3, "capacity": 1}, {"name": "W2", "location": 10, "capacity": 1}]], "expected": [{"order_id": "O1", "warehouse_name": "W1", "distance": 2}, {"order_id": "O2", "warehouse_name": "W2", "distance": 2}]},
                    ],
                    "hidden_tests": 8,
                    "xp": 100,
                    "mastery_threshold": 70,
                },
            ],
            "mastery_xp": 200,
        },
        {
            "id": "support_queue",
            "title": "Customer Support Queue",
            "skills_taught": ["queues", "priority_queues", "heap"],
            "scenario": "A support system receives tickets with different priorities. Process them in the right order.",
            "goal": "Build a priority support queue.",
            "steps": [
                {
                    "type": "build",
                    "title": "Basic Queue",
                    "content": "Implement a first-in-first-out queue.",
                    "function_name": "SupportQueue",
                    "class": True,
                    "signature": "class SupportQueue:\n    def __init__(self):\n        ...\n    def enqueue(self, ticket: dict) -> None:\n        ...\n    def dequeue(self) -> dict:\n        ...\n    def size(self) -> int:\n        ...",
                    "description": "Support queue for tickets. Each ticket has 'id', 'priority' (1-5, 5=highest), 'message'. Dequeue returns highest priority first (FIFO within same priority).",
                    "test_cases": [
                        {"input": ["enqueue({'id': 1, 'priority': 3, 'message': 'bug'})", "enqueue({'id': 2, 'priority': 5, 'message': 'crash'})", "dequeue()"], "expected": {"id": 2, "priority": 5, "message": "crash"}},
                    ],
                    "hidden_tests": 8,
                    "xp": 80,
                },
                {
                    "type": "assessment",
                    "title": "Support Boss",
                    "content": "Build a complete support ticket processor. 15 minutes.",
                    "timed": True,
                    "time_limit_minutes": 15,
                    "function_name": "process_tickets",
                    "signature": "def process_tickets(tickets: list) -> dict:",
                    "description": "Process support tickets. Each has id, priority (1-5), category ('bug', 'feature', 'question'). Return: {'processed': [ticket_ids in order], 'by_category': {'bug': N, ...}, 'avg_wait': float}. Process highest priority first.",
                    "test_cases": [
                        {"input": [[{"id": 1, "priority": 3, "category": "bug"}, {"id": 2, "priority": 5, "category": "feature"}]], "expected": {"processed": [2, 1], "by_category": {"bug": 1, "feature": 1, "question": 0}, "avg_wait": 1.0}},
                    ],
                    "hidden_tests": 8,
                    "xp": 100,
                    "mastery_threshold": 70,
                },
            ],
            "mastery_xp": 200,
        },
        {
            "id": "dedup",
            "title": "Contact Deduplication",
            "skills_taught": ["hashing", "sets", "dictionaries", "fuzzy_matching"],
            "scenario": "A CRM has duplicate contacts. Build a deduplication system.",
            "goal": "Detect and merge duplicate contacts.",
            "steps": [
                {
                    "type": "build",
                    "title": "Exact Match Dedup",
                    "content": "Find exact duplicate contacts.",
                    "function_name": "find_exact_duplicates",
                    "signature": "def find_exact_duplicates(contacts: list) -> list:",
                    "description": "Return list of groups of duplicate contact IDs. Contacts match if name and email are identical (case-insensitive).",
                    "test_cases": [
                        {"input": [[{"id": 1, "name": "Rahul", "email": "r@x.com"}, {"id": 2, "name": "Rahul", "email": "r@x.com"}, {"id": 3, "name": "Priya", "email": "p@x.com"}]], "expected": [[1, 2]]},
                    ],
                    "hidden_tests": 5,
                    "xp": 50,
                },
                {
                    "type": "assessment",
                    "title": "Dedup Boss",
                    "content": "Build a smart deduplication system. 12 minutes.",
                    "timed": True,
                    "time_limit_minutes": 12,
                    "function_name": "smart_dedup",
                    "signature": "def smart_dedup(contacts: list) -> dict:",
                    "description": "Find duplicates: exact match (name+email), fuzzy name match (same email), same phone. Merge: keep the record with most fields. Return {'merged': N, 'kept': [ids], 'removed': [ids]}.",
                    "test_cases": [
                        {"input": [[{"id": 1, "name": "Rahul", "email": "r@x.com", "phone": None}, {"id": 2, "name": "RAHUL", "email": "r@x.com", "phone": "123"}]], "expected": {"merged": 1, "kept": [2], "removed": [1]}},
                    ],
                    "hidden_tests": 8,
                    "xp": 100,
                    "mastery_threshold": 70,
                },
            ],
            "mastery_xp": 200,
        },
        {
            "id": "social_network",
            "title": "Social Network",
            "skills_taught": ["graphs", "bfs", "dfs", "shortest_path"],
            "scenario": "Build the friend suggestion system for a social network.",
            "goal": "Find mutual friends and suggest connections.",
            "steps": [
                {
                    "type": "explore",
                    "title": "Visualize the Network",
                    "content": "A social network is a graph. Each person is a node, each friendship is an edge.",
                    "visualization": {
                        "type": "graph",
                        "nodes": ["Alice", "Bob", "Carol", "Dave", "Eve"],
                        "edges": [["Alice", "Bob"], ["Alice", "Carol"], ["Bob", "Carol"], ["Carol", "Dave"], ["Dave", "Eve"]],
                    },
                },
                {
                    "type": "build",
                    "title": "Find Mutual Friends",
                    "content": "Write a function to find mutual friends between two people.",
                    "function_name": "mutual_friends",
                    "signature": "def mutual_friends(graph: dict, person1: str, person2: str) -> list:",
                    "description": "Given an adjacency list graph, find friends common to both person1 and person2.",
                    "test_cases": [
                        "input: graph={Alice: [Bob, Carol], Bob: [Alice, Carol], Carol: [Alice, Bob, Dave]}, Alice, Bob",
                        "expected: ['Carol']",
                    ],
                    "hidden_tests": 5,
                    "xp": 50,
                },
                {
                    "type": "build",
                    "title": "Friend Suggestions",
                    "content": "Suggest friends: people connected through mutual friends but not already friends.",
                    "function_name": "suggest_friends",
                    "signature": "def suggest_friends(graph: dict, person: str) -> list:",
                    "description": "Return list of suggested friends sorted by number of mutual friends (desc). Each: {'name': str, 'mutual_count': int}.",
                    "test_cases": [
                        {"input": [{"Alice": ["Bob", "Carol"], "Bob": ["Alice"], "Carol": ["Alice", "Dave"], "Dave": ["Carol"]}, "Alice"], "expected": [{"name": "Dave", "mutual_count": 1}]},
                    ],
                    "hidden_tests": 6,
                    "xp": 70,
                },
                {
                    "type": "assessment",
                    "title": "Network Boss",
                    "content": "Build a social network analyzer. 15 minutes.",
                    "timed": True,
                    "time_limit_minutes": 15,
                    "function_name": "analyze_network",
                    "signature": "def analyze_network(graph: dict) -> dict:",
                    "description": "Analyze a social network. Return: {'total_users': N, 'most_connected': str, 'avg_friends': float, 'clusters': int, 'degrees_of_separation': {person: {other: distance}}}. Clusters = connected components.",
                    "test_cases": [
                        {"input": [{"A": ["B"], "B": ["A", "C"], "C": ["B"], "D": ["E"], "E": ["D"]}], "expected": {"total_users": 5, "most_connected": "B", "avg_friends": 1.2, "clusters": 2}},
                    ],
                    "hidden_tests": 8,
                    "xp": 100,
                    "mastery_threshold": 70,
                },
            ],
            "mastery_xp": 200,
        },
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# WORLD 3 — BUILD SYSTEMS
# "Can you build and scale a working backend service?"
# ══════════════════════════════════════════════════════════════════════════════

WORLD_3 = {
    "id": "build_systems",
    "title": "Build Systems",
    "icon": "🏗️",
    "description": "Build real APIs, databases, and scalable services",
    "order": 3,
    "prerequisites": ["code_foundations"],
    "competencies": [
        {
            "id": "url_shortener",
            "title": "URL Shortener",
            "skills_taught": ["http", "apis", "databases", "hashing"],
            "scenario": "Build a URL shortener service from scratch.",
            "goal": "Build a working URL shortener with lookup and analytics.",
            "steps": [
                {
                    "type": "context",
                    "title": "The Requirement",
                    "content": "A startup wants a URL shortener. Users submit long URLs, get back short codes. When someone visits the short URL, redirect them.",
                },
                {
                    "type": "build",
                    "title": "Core Shortener",
                    "content": "Build the URL shortening and lookup logic.",
                    "function_name": "URLShortener",
                    "class": True,
                    "signature": "class URLShortener:\n    def __init__(self):\n        ...\n    def shorten(self, url: str) -> str:\n        ...\n    def resolve(self, code: str) -> str:\n        ...\n    def stats(self, code: str) -> dict:\n        ...",
                    "description": "Shorten URLs to 6-char codes. Track click count. Resolve codes back to URLs.",
                    "test_cases": [
                        {"input": ["shorten('https://example.com/very/long/url')"], "expected": "code returned (6 chars)"},
                        {"input": ["resolve(code)"], "expected": "https://example.com/very/long/url"},
                    ],
                    "hidden_tests": 6,
                    "xp": 60,
                },
                {
                    "type": "build",
                    "title": "Add Caching",
                    "content": "The service is slow. Add a cache layer.",
                    "function_name": "CachedShortener",
                    "class": True,
                    "signature": "class CachedShortener:\n    def __init__(self, cache_size=1000):\n        ...\n    def resolve(self, code: str) -> str:\n        ...",
                    "description": "LRU cache for resolved URLs. Cache hit avoids database lookup.",
                    "test_cases": [
                        {"input": ["same URL resolved twice"], "expected": "second resolve is from cache"},
                    ],
                    "hidden_tests": 5,
                    "xp": 60,
                },
                {
                    "type": "assessment",
                    "title": "Systems Boss",
                    "content": "Build a rate-limited API handler. 15 minutes.",
                    "timed": True,
                    "time_limit_minutes": 15,
                    "function_name": "RateLimiter",
                    "class": True,
                    "signature": "class RateLimiter:\n    def __init__(self, max_requests, window_seconds):\n        ...\n    def allow(self, user_id: str) -> bool:\n        ...\n    def usage(self, user_id: str) -> dict:\n        ...",
                    "description": "Sliding window rate limiter. Track requests per user. Return True if allowed, False if rate limited. usage() returns {count, remaining, reset_in}.",
                    "test_cases": [
                        {"input": ["allow('u1')", "allow('u1')", "usage('u1')"], "expected": [True, True, {'count': 2}]},
                    ],
                    "hidden_tests": 8,
                    "xp": 100,
                    "mastery_threshold": 70,
                },
            ],
            "mastery_xp": 200,
        },
        {
            "id": "scale_api",
            "title": "Scale Under Load",
            "skills_taught": ["caching", "indexes", "scalability", "performance"],
            "scenario": "Your API suddenly receives 10,000 requests/second. It's falling over.",
            "goal": "Make the system handle 10x the load.",
            "steps": [
                {
                    "type": "debug",
                    "title": "The Slow Query",
                    "buggy_code": 'def get_user_orders(user_id, orders_db):\n    results = []\n    for order in orders_db:  # scanning all orders\n        if order["user_id"] == user_id:\n            results.append(order)\n    return results',
                    "question": "Why is this slow with 1M orders?",
                    "hint": "It scans every single order.",
                    "xp": 30,
                },
                {
                    "type": "build",
                    "title": "Index-Based Lookup",
                    "content": "Build a system with proper indexing.",
                    "function_name": "IndexedDB",
                    "class": True,
                    "signature": "class IndexedDB:\n    def __init__(self):\n        ...\n    def insert(self, record: dict) -> None:\n        ...\n    def query(self, field: str, value) -> list:\n        ...\n    def query_range(self, field: str, low, high) -> list:\n        ...",
                    "description": "In-memory DB with automatic indexing. query() uses index for O(1) lookup. query_range() for range queries.",
                    "test_cases": [
                        {"input": ["insert({'id': 1, 'user': 'A', 'amount': 100})", "query('user', 'A')"], "expected": [{'id': 1, 'user': 'A', 'amount': 100}]},
                    ],
                    "hidden_tests": 6,
                    "xp": 70,
                },
                {
                    "type": "assessment",
                    "title": "Scaling Boss",
                    "content": "Build a read-through cache with invalidation. 15 minutes.",
                    "timed": True,
                    "time_limit_minutes": 15,
                    "function_name": "CacheLayer",
                    "class": True,
                    "signature": "class CacheLayer:\n    def __init__(self, backend, ttl_seconds=60):\n        ...\n    def get(self, key: str):\n        ...\n    def set(self, key: str, value, ttl: int = None):\n        ...\n    def invalidate(self, key: str):\n        ...\n    def stats(self) -> dict:\n        ...",
                    "description": "Cache with TTL, hit/miss tracking, and invalidation. stats() returns {hits, misses, hit_rate, size}.",
                    "hidden_tests": 8,
                    "xp": 100,
                    "mastery_threshold": 70,
                },
            ],
            "mastery_xp": 200,
        },
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# WORLD 4 — WORK WITH DATA
# "Can you design schemas, write queries, and fix data problems?"
# ══════════════════════════════════════════════════════════════════════════════

WORLD_4 = {
    "id": "work_with_data",
    "title": "Work with Data",
    "icon": "🗄️",
    "description": "Design schemas, write queries, fix data problems",
    "order": 4,
    "prerequisites": ["code_foundations"],
    "competencies": [
        {
            "id": "payroll_fix",
            "title": "Fix Duplicate Payroll",
            "skills_taught": ["sql", "schema_design", "normalization"],
            "scenario": "Company's employee database produces duplicate payroll records. Fix it.",
            "goal": "Design a correct schema and write deduplication queries.",
            "steps": [
                {
                    "type": "context",
                    "title": "The Data Problem",
                    "content": "The payroll system pays some employees twice. The root cause: the schema allows duplicate records.",
                    "data": {"table": "employees", "rows": [{"id": 1, "name": "Rahul", "dept": "Engineering", "salary": 80000}, {"id": 2, "name": "Rahul", "dept": "Engineering", "salary": 80000}, {"id": 3, "name": "Priya", "dept": "Design", "salary": 75000}]},
                },
                {
                    "type": "build",
                    "title": "Design the Schema",
                    "content": "Write SQL to create a properly normalized schema.",
                    "function_name": "create_schema",
                    "signature": "def create_schema() -> list:",
                    "description": "Return list of SQL CREATE TABLE statements for a company with departments, employees (no duplicates), and payroll. Use proper constraints.",
                    "test_cases": [
                        {"input": [], "expected": "List of valid SQL CREATE statements with PRIMARY KEY, FOREIGN KEY, UNIQUE constraints"},
                    ],
                    "hidden_tests": 4,
                    "xp": 50,
                },
                {
                    "type": "build",
                    "title": "Deduplicate",
                    "content": "Write a function to identify and remove duplicates.",
                    "function_name": "deduplicate",
                    "signature": "def deduplicate(employees: list) -> dict:",
                    "description": "Find duplicate employees (same name+dept). Keep the first occurrence. Return {'unique': [...], 'removed': [...], 'removed_count': N}.",
                    "test_cases": [
                        {"input": [[{"id": 1, "name": "Rahul", "dept": "Eng"}, {"id": 2, "name": "Rahul", "dept": "Eng"}, {"id": 3, "name": "Priya", "dept": "Design"}]], "expected": {"unique": [{"id": 1, "name": "Rahul", "dept": "Eng"}, {"id": 3, "name": "Priya", "dept": "Design"}], "removed": [{"id": 2, "name": "Rahul", "dept": "Eng"}], "removed_count": 1}},
                    ],
                    "hidden_tests": 5,
                    "xp": 50,
                },
                {
                    "type": "assessment",
                    "title": "Data Boss",
                    "content": "Build a query engine. 15 minutes.",
                    "timed": True,
                    "time_limit_minutes": 15,
                    "function_name": "query_engine",
                    "signature": "def query_engine(data: list, filters: dict, sort_by: str = None, limit: int = None) -> list:",
                    "description": "Filter a list of dicts. Filters: {'field': value} for exact match, {'field__gt': N}, {'field__lt': N}, {'field__in': [list]}. Sort by field. Limit results.",
                    "test_cases": [
                        {"input": [[{"name": "A", "age": 25}, {"name": "B", "age": 30}], {"age__gt": 25}], "expected": [{"name": "B", "age": 30}]},
                    ],
                    "hidden_tests": 8,
                    "xp": 100,
                    "mastery_threshold": 70,
                },
            ],
            "mastery_xp": 200,
        },
        {
            "id": "analytics_builder",
            "title": "Analytics Dashboard",
            "skills_taught": ["aggregation", "joins", "grouping", "time_series"],
            "scenario": "Build an analytics engine for an e-commerce platform.",
            "goal": "Process orders and generate business metrics.",
            "steps": [
                {
                    "type": "build",
                    "title": "Order Analytics",
                    "content": "Write functions to compute business metrics.",
                    "function_name": "order_analytics",
                    "signature": "def order_analytics(orders: list) -> dict:",
                    "description": "Compute: total_revenue, avg_order_value, top_product, orders_by_day. Each order: {id, product, amount, date}.",
                    "test_cases": [
                        {"input": [[{"id": 1, "product": "A", "amount": 100, "date": "2024-01-01"}, {"id": 2, "product": "B", "amount": 200, "date": "2024-01-01"}, {"id": 3, "product": "A", "amount": 100, "date": "2024-01-02"}]], "expected": {"total_revenue": 400, "avg_order_value": 200, "top_product": "A", "orders_by_day": {"2024-01-01": 2, "2024-01-02": 1}}},
                    ],
                    "hidden_tests": 6,
                    "xp": 70,
                },
                {
                    "type": "assessment",
                    "title": "Analytics Boss",
                    "content": "Build a cohort analysis engine. 15 minutes.",
                    "timed": True,
                    "time_limit_minutes": 15,
                    "function_name": "cohort_analysis",
                    "signature": "def cohort_analysis(users: list, events: list) -> dict:",
                    "description": "Group users by signup week. Track weekly retention. Return {cohort_week: [retention_pct, ...]}. A user is retained if they have events in that week.",
                    "hidden_tests": 8,
                    "xp": 100,
                    "mastery_threshold": 70,
                },
            ],
            "mastery_xp": 200,
        },
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# WORLD 5 — SOFTWARE ENGINEERING
# "Can you write code that others can maintain?"
# ══════════════════════════════════════════════════════════════════════════════

WORLD_5 = {
    "id": "software_engineering",
    "title": "Software Engineering",
    "icon": "🔧",
    "description": "Write production-quality code",
    "order": 5,
    "prerequisites": ["code_foundations"],
    "competencies": [
        {
            "id": "git_workflow",
            "title": "Recover from Disaster",
            "skills_taught": ["git", "branching", "merging", "conflict_resolution"],
            "scenario": "You broke production. Your teammate pushed a conflicting change. Recover the correct version.",
            "goal": "Use git operations to recover from a bad deploy.",
            "steps": [
                {
                    "type": "context",
                    "title": "Production is Down",
                    "content": "The main branch has a bug. Your teammate pushed a fix but it conflicts with your change. You need to revert your change and apply theirs.",
                },
                {
                    "type": "build",
                    "title": "Git Operations Simulator",
                    "content": "Simulate git operations using string manipulation.",
                    "function_name": "simulate_git",
                    "signature": "def simulate_git(commands: list) -> list:",
                    "description": "Simulate: 'branch X' (create branch), 'commit X' (add to current), 'checkout X' (switch), 'merge X' (merge), 'revert' (undo last). Return list of branch states.",
                    "test_cases": [
                        {"input": [["commit A", "branch feature", "checkout feature", "commit B", "checkout main", "merge feature"]], "expected": [{"main": ["A", "B"], "feature": ["A", "B"]}]},
                    ],
                    "hidden_tests": 6,
                    "xp": 50,
                },
                {
                    "type": "assessment",
                    "title": "Git Boss",
                    "content": "Build a version control simulator. 12 minutes.",
                    "timed": True,
                    "time_limit_minutes": 12,
                    "function_name": "VersionControl",
                    "class": True,
                    "signature": "class VersionControl:\n    def __init__(self):\n        ...\n    def commit(self, message: str) -> int:\n        ...\n    def branch(self, name: str) -> None:\n        ...\n    def checkout(self, name: str) -> None:\n        ...\n    def merge(self, source: str) -> dict:\n        ...\n    def log(self) -> list:\n        ...",
                    "description": "Git-like version control. Branches share history until fork. Merge combines. Detect conflicts (same file changed). Return conflict info on merge.",
                    "hidden_tests": 8,
                    "xp": 100,
                    "mastery_threshold": 70,
                },
            ],
            "mastery_xp": 200,
        },
        {
            "id": "debugging_mastery",
            "title": "Debug Anything",
            "skills_taught": ["debugging", "error_analysis", "logging", "testing"],
            "scenario": "You inherit a buggy codebase. Find and fix all the bugs.",
            "goal": "Debug systematically and fix all issues.",
            "steps": [
                {
                    "type": "debug",
                    "title": "Off-by-One Error",
                    "buggy_code": 'def get_range(n):\n    return list(range(1, n))  # Should return 1 to n inclusive',
                    "question": "What's wrong?",
                    "hint": "range(1, n) stops at n-1",
                    "xp": 20,
                },
                {
                    "type": "debug",
                    "title": "Null Pointer",
                    "buggy_code": 'def get_name(user):\n    return user["profile"]["name"]  # Crashes on some users',
                    "question": "What edge case causes the crash?",
                    "hint": "Not all users have a profile",
                    "xp": 20,
                },
                {
                    "type": "build",
                    "title": "Write Tests",
                    "content": "Write tests for a function before fixing it.",
                    "function_name": "test_divide",
                    "signature": "def test_divide() -> list:",
                    "description": "Write test cases for divide(a, b). Include: normal division, divide by zero, negative numbers, large numbers, None inputs. Return list of {input, expected, description}.",
                    "test_cases": [
                        {"input": [], "expected": "List of test cases covering edge cases"},
                    ],
                    "hidden_tests": 5,
                    "xp": 50,
                },
                {
                    "type": "assessment",
                    "title": "Debug Boss",
                    "content": "Fix a buggy e-commerce checkout. 15 minutes.",
                    "timed": True,
                    "time_limit_minutes": 15,
                    "function_name": "fix_checkout",
                    "signature": "def fix_checkout(cart: list, user: dict, coupon: str = None) -> dict:",
                    "description": "Fix the checkout function. It has 5 bugs: wrong tax calc, coupon not applied, overflow on empty cart, wrong discount on bulk items, missing currency conversion. Fix all and return {total, tax, discount, final}.",
                    "test_cases": [
                        {"input": [[{"price": 100, "qty": 2}], {"country": "IN"}, None], "expected": {"total": 200, "tax": 20, "discount": 0, "final": 220}},
                    ],
                    "hidden_tests": 8,
                    "xp": 100,
                    "mastery_threshold": 70,
                },
            ],
            "mastery_xp": 200,
        },
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# WORLD 6 — ENGINEERING UNDER PRESSURE
# "Can you perform when it matters?"
# ══════════════════════════════════════════════════════════════════════════════

WORLD_6 = {
    "id": "under_pressure",
    "title": "Engineering Under Pressure",
    "icon": "⚡",
    "description": "Perform under constraints — timed, ambiguous, buggy",
    "order": 6,
    "prerequisites": ["code_foundations", "problem_solver"],
    "competencies": [
        {
            "id": "timed_coding",
            "title": "Timed Problem Solving",
            "skills_taught": ["time_management", "problem_solving", "optimization"],
            "scenario": "OA-style timed coding challenges.",
            "goal": "Solve problems under time pressure.",
            "steps": [
                {
                    "type": "assessment",
                    "title": "Speed Run",
                    "timed": True,
                    "time_limit_minutes": 20,
                    "problems": [
                        {"title": "Reverse Words", "difficulty": "easy", "time_minutes": 5},
                        {"title": "Valid Parentheses", "difficulty": "easy", "time_minutes": 5},
                        {"title": "Merge Intervals", "difficulty": "medium", "time_minutes": 10},
                    ],
                },
            ],
            "mastery_xp": 200,
        },
        {
            "id": "ambiguous_reqs",
            "title": "Ambiguous Requirements",
            "skills_taught": ["requirements_analysis", "assumption_making", "communication"],
            "scenario": "Product gives you vague requirements. You need to ask the right questions and make decisions.",
            "goal": "Build a feature with incomplete information.",
            "steps": [
                {
                    "type": "context",
                    "title": "The Vague Request",
                    "content": "Product: 'Build a notification system.' That's all you get.",
                },
                {
                    "type": "build",
                    "title": "Design and Build",
                    "content": "Design a notification system with reasonable assumptions. Document your assumptions.",
                    "function_name": "NotificationSystem",
                    "class": True,
                    "description": "Build a notification system. Support: email, push, in-app. Track delivery status. Handle duplicates. Rate limit. Your design choices matter.",
                    "hidden_tests": 10,
                    "xp": 100,
                },
                {
                    "type": "assessment",
                    "title": "Ambiguity Boss",
                    "content": "Build a feature from a one-line requirement. 20 minutes.",
                    "timed": True,
                    "time_limit_minutes": 20,
                    "description": "Requirement: 'Build a search feature.' Design and implement search with ranking, filters, and pagination. Make your own decisions about behavior.",
                    "hidden_tests": 12,
                    "xp": 150,
                    "mastery_threshold": 70,
                },
            ],
            "mastery_xp": 250,
        },
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# WORLD 7 — HIRING ARENA
# "Prove you can do the job."
# ══════════════════════════════════════════════════════════════════════════════

WORLD_7 = {
    "id": "hiring_arena",
    "title": "Hiring Arena",
    "icon": "🏆",
    "description": "OA simulation, interview prep, prove your readiness",
    "order": 7,
    "prerequisites": ["problem_solver", "build_systems"],
    "competencies": [
        {
            "id": "oa_simulation",
            "title": "OA Simulation",
            "skills_taught": ["oa_timing", "problem_selection", "stress_management"],
            "scenario": "Simulate a real Online Assessment.",
            "goal": "Pass the OA simulation.",
            "steps": [
                {
                    "type": "assessment",
                    "title": "Full OA Simulation",
                    "timed": True,
                    "time_limit_minutes": 60,
                    "description": "2 easy + 2 medium + 1 hard problem. Real OA format. No hints. No peeking at solutions.",
                    "problems": [
                        {"title": "Two Sum Variant", "difficulty": "easy", "time_minutes": 10},
                        {"title": "String Compression", "difficulty": "easy", "time_minutes": 10},
                        {"title": "LRU Cache", "difficulty": "medium", "time_minutes": 15},
                        {"title": "Graph BFS", "difficulty": "medium", "time_minutes": 15},
                        {"title": "Word Break II", "difficulty": "hard", "time_minutes": 10},
                    ],
                },
            ],
            "mastery_xp": 300,
        },
        {
            "id": "interview_prep",
            "title": "Interview Readiness",
            "skills_taught": ["communication", "approach_explanation", "follow_ups"],
            "scenario": "Practice explaining your approach out loud.",
            "goal": "Communicate your thought process clearly.",
            "steps": [
                {
                    "type": "build",
                    "title": "Explain Your Approach",
                    "content": "Solve a problem and explain your reasoning.",
                    "description": "After solving each problem, write a 2-3 sentence explanation of your approach, complexity, and trade-offs.",
                    "xp": 50,
                },
            ],
            "mastery_xp": 200,
        },
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# WORLD 8 — COMPANY MISSIONS (Dynamic)
# Personalized per target company.
# ══════════════════════════════════════════════════════════════════════════════

WORLD_8 = {
    "id": "company_missions",
    "title": "Company Missions",
    "icon": "🏢",
    "description": "Personalized preparation for your target company",
    "order": 8,
    "dynamic": True,  # Generated based on user's job target
}


# ─── All Worlds ───
ALL_WORLDS = {
    "code_foundations": WORLD_1,
    "problem_solver": WORLD_2,
    "build_systems": WORLD_3,
    "work_with_data": WORLD_4,
    "software_engineering": WORLD_5,
    "under_pressure": WORLD_6,
    "hiring_arena": WORLD_7,
    "company_missions": WORLD_8,
}


def get_worlds():
    """Return all worlds with unlock status."""
    return [
        {
            "id": w["id"],
            "title": w["title"],
            "icon": w["icon"],
            "description": w["description"],
            "order": w["order"],
            "competencies": len(w.get("competencies", [])),
            "prerequisites": w.get("prerequisites", []),
        }
        for w in sorted(ALL_WORLDS.values(), key=lambda x: x["order"])
    ]


def get_world(world_id: str):
    """Return a world's full data."""
    return ALL_WORLDS.get(world_id)


def get_competency(world_id: str, competency_id: str):
    """Return a specific competency."""
    world = ALL_WORLDS.get(world_id)
    if not world:
        return None
    for comp in world.get("competencies", []):
        if comp["id"] == competency_id:
            return {"world": world, "competency": comp}
    return None


# ─── Daily Mission Generator ───
# Generates a daily plan based on user's readiness and gaps.

DAILY_MISSION_TYPES = {
    "monday": {"type": "learn", "icon": "🌿", "label": "Learn", "description": "Calm exploration — new concept"},
    "tuesday": {"type": "practice", "icon": "⚔️", "label": "Practice", "description": "Interactive challenge"},
    "wednesday": {"type": "review", "icon": "🧠", "label": "Review", "description": "SRS review — things you're forgetting"},
    "thursday": {"type": "build", "icon": "🏗️", "label": "Build", "description": "Build mission — hands-on project"},
    "friday": {"type": "assess", "icon": "🧪", "label": "Assess", "description": "Mini assessment — 20 min simulation"},
    "saturday": {"type": "company", "icon": "🏢", "label": "Company", "description": "Company-specific challenge"},
    "sunday": {"type": "report", "icon": "📊", "label": "Report", "description": "Weekly readiness report"},
}


def get_daily_plan(day_of_week: str, user_gaps: dict = None):
    """Get today's mission type and recommended activity."""
    day = day_of_week.lower()[:3]  # "Monday" -> "mon"
    day_map = {"mon": "monday", "tue": "tuesday", "wed": "wednesday", "thu": "thursday", "fri": "friday", "sat": "saturday", "sun": "sunday"}
    full_day = day_map.get(day, "monday")

    mission_type = DAILY_MISSION_TYPES[full_day]

    return {
        "day": full_day,
        **mission_type,
        "gaps": user_gaps or {},
    }
