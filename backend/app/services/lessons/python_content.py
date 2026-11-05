"""MASSIVE Lesson Generator - Real Content at Coddy.tech Scale."""
import os

lessons_dir = "D:/Project-Fremen/backend/app/services/lessons"

# Real topic-specific content for Python
PYTHON_REAL_TOPICS = [
    ("variables", "Variables", "A variable stores a value. Create with = operator. Python is dynamically typed.",
     'name = "Alice"\nage = 25\nheight = 5.6\nis_student = True\nprint(name, age, height, is_student)',
     "Alice 25 5.6 True",
     "Variables store data. Python figures out type automatically.",
     "Create variable 'city'='Tokyo', 'population'=14000000, print both.",
     'city = "Tokyo"\npopulation = 14000000\nprint(city, population)',
     "Tokyo 14000000",
     "Which is a valid Python variable name?",
     ["2nd_name", "first-name", "first_name", "first name"], 2,
     "Variable names can contain letters, digits, underscores. Cannot start with digit or contain spaces/hyphens."),
    ("strings", "Strings", "A string is a sequence of characters. Immutable - can't change individual chars.",
     'name = "Alice"\nprint(name[0])      # A\nprint(name[-1])     # e\nprint(len(name))    # 5\nprint(name.upper()) # ALICE',
     "A\ne\n5\nALICE",
     "Strings support indexing, slicing, and many built-in methods.",
     "Given s='Hello World', print length, uppercase, and replace spaces with underscores.",
     "s = 'Hello World'\nprint(len(s))\nprint(s.upper())\nprint(s.replace(' ', '_'))",
     "11\nHELLO WORLD\nHello_World",
     "What happens when you try s[0] = 'X'?",
     ["It works silently", "It raises TypeError", "It raises IndexError", "It creates a new string"], 1,
     "Strings are immutable. Attempting to modify raises TypeError."),
    ("lists", "Lists", "A list is an ordered, mutable collection. Can contain different types. Add, remove, modify after creation.",
     "fruits = ['apple', 'banana', 'cherry']\nfruits.append('date')\nprint(fruits)\nprint(fruits[1])\nprint(fruits[-1])\nprint(fruits[1:3])",
     "['apple', 'banana', 'cherry', 'date']\nbanana\ndate\n['banana', 'cherry']",
     "Lists are mutable and ordered. Indexing is 0-based. Negative indices count from end.",
     "Create list [1,2,3]. Append 4, remove 2, print list and length.",
     "nums = [1, 2, 3]\nnums.append(4)\nnums.remove(2)\nprint(nums)\nprint(len(nums))",
     "[1, 3, 4]\n3",
     "What does list.insert(1, 'x') do?",
     ["Appends 'x' to end", "Inserts 'x' at index 1", "Replaces index 1 with 'x'", "Removes index 1"], 1,
     "insert(index, value) inserts value at specified position, shifting existing elements right."),
    ("dictionaries", "Dictionaries", "A dictionary stores key-value pairs. Keys must be unique and immutable. Mutable — add, update, remove pairs.",
     "person = {'name': 'Alice', 'age': 25, 'city': 'Tokyo'}\nprint(person['name'])\nperson['age'] = 26\nperson['email'] = 'a@b.com'\nprint(person)\nprint(person.get('phone', 'N/A'))",
     "Alice\n{'name': 'Alice', 'age': 26, 'city': 'Tokyo', 'email': 'a@b.com'}\nN/A",
     "Dictionaries provide O(1) average lookup by key. Use .get() to avoid KeyError.",
     "Create dict with 'name', 'age', 'city'. Update 'age' to 30, add 'country'='Japan', print.",
     "d = {'name': 'Bob', 'age': 25, 'city': 'Osaka'}\nd['age'] = 30\nd['country'] = 'Japan'\nprint(d)",
     "None",
     "Can a list be a dictionary key?",
     ["Yes, always", "No, keys must be immutable", "Only if the list is empty", "Only in Python 3.10+"], 1,
     "Dictionary keys must be hashable (immutable). Lists are mutable and unhashable."),
    ("functions", "Functions", "A function is a reusable block of code. Define with 'def', call by name. Can take parameters and return values.",
     "def greet(name):\n    return f'Hello, {name}!'\n\ndef add(a, b):\n    return a + b\n\nprint(greet('Alice'))\nprint(add(3, 4))",
     "Hello, Alice!\n7",
     "def defines a function. Parameters receive arguments. return sends a value back.",
     "Write function 'multiply(a, b)' returning product. Call with 6 and 7, print result.",
     "def multiply(a, b):\n    return a * b\n\nprint(multiply(6, 7))",
     "42",
     "What is the difference between a parameter and an argument?",
     ["No difference", "Parameter is in definition, argument is in call", "Argument is in definition, parameter is in call", "Parameter is required, argument is optional"], 1,
     "A parameter is the variable name in the function definition. An argument is the actual value passed."),
    ("loops", "Loops", "Use 'for' to iterate over sequences, 'while' to repeat while condition is true. break exits early, continue skips.",
     "for i in range(5):\n    print(i)\n\n# While loop\ncount = 0\nwhile count < 3:\n    print(count)\n    count += 1",
     "0\n1\n2\n3\n4\n0\n1\n2",
     "for iterates over a sequence. while repeats while condition is true. range(5) produces 0,1,2,3,4.",
     "Print the sum of all numbers from 1 to 10 using a for loop.",
     "total = 0\nfor i in range(1, 11):\n    total += i\nprint(total)",
     "55",
     "What does 'break' do in a loop?",
     ["Skips one iteration", "Exits the loop immediately", "Restarts the loop", "Pauses the loop"], 1,
     "break immediately exits the loop, regardless of the loop condition."),
    ("conditionals", "Conditionals", "Use if/elif/else to make decisions. Python uses indentation to define code blocks. No curly braces.",
     "age = 20\nif age < 13:\n    print('Child')\nelif age < 18:\n    print('Teen')\nelse:\n    print('Adult')",
     "Adult",
     "if checks first condition. elif checks next. else runs if none matched. Indentation defines blocks.",
     "Given score = 85, print 'A' if score>=90, 'B' if score>=80, 'C' if score>=70, else 'F'.",
     "score = 85\nif score >= 90:\n    print('A')\nelif score >= 80:\n    print('B')\nelif score >= 70:\n    print('C')\nelse:\n    print('F')",
     "B",
     "How many elif clauses can an if statement have?",
     ["At most 1", "At most 2", "Zero or more", "Exactly 1"], 2,
     "You can have zero or more elif clauses in an if statement."),
    ("comprehensions", "List Comprehensions", "List comprehensions provide a concise way to create lists. Brackets containing expression followed by for clause, then zero or more if clauses.",
     "squares = [x**2 for x in range(5)]\nprint(squares)  # [0, 1, 4, 9, 16]\n\neven = [x for x in range(10) if x % 2 == 0]\nprint(even)  # [0, 2, 4, 6, 8]",
     "[0, 1, 4, 9, 16]\n[0, 2, 4, 6, 8]",
     "Comprehensions are more readable and faster than equivalent for loops with append.",
     "Create a list of cubes (x^3) for x in range(1, 6) using a list comprehension. Print it.",
     "cubes = [x**3 for x in range(1, 6)]\nprint(cubes)",
     "[1, 8, 27, 64, 125]",
     "What is the syntax for a list comprehension?",
     ["[expression for item in iterable]", "(expression for item in iterable)", "{expression for item in iterable}", "expression for item in iterable"], 0,
     "List comprehensions use square brackets: [expression for item in iterable]."),
    ("file_io", "File I/O", "Use open() to read/write files. Always use 'with' statement to ensure files are closed properly. Modes: 'r' (read), 'w' (write), 'a' (append).",
     "with open('example.txt', 'w') as f:\n    f.write('Hello, World!')\n\nwith open('example.txt', 'r') as f:\n    content = f.read()\n    print(content)",
     "Hello, World!",
     "'with' statement automatically closes the file. 'w' writes, 'r' reads.",
     "Write 'Python is awesome' to a file named 'test.txt', then read it back and print the content.",
     "with open('test.txt', 'w') as f:\n    f.write('Python is awesome')\n\nwith open('test.txt', 'r') as f:\n    content = f.read()\n    print(content)",
     "Python is awesome",
     "What does 'a' mode do when opening a file?",
     ["Read only", "Write and truncate", "Append to end", "Read and write"], 2,
     "'a' mode opens file for appending — new content is added to the end."),
    ("exceptions", "Exception Handling", "Use try/except to handle errors gracefully. finally block runs always. raise to throw exceptions.",
     "try:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print('Cannot divide by zero')\nfinally:\n    print('Done')",
     "Cannot divide by zero\nDone",
     "try block contains risky code. except catches specific errors. finally always runs.",
     "Write code that tries to convert 'abc' to int, catches ValueError, and prints 'Invalid number'.",
     "try:\n    int('abc')\nexcept ValueError:\n    print('Invalid number')",
     "Invalid number",
     "What does 'finally' block do?",
     ["Runs only if no exception", "Runs only if exception", "Runs always", "Runs before try"], 2,
     "finally block always runs, whether or not an exception occurred."),
    ("decorators", "Decorators", "Decorators modify or extend function behavior without changing its source. Use @syntax. Functions are first-class objects in Python.",
     "def my_decorator(func):\n    def wrapper():\n        print('Before function')\n        func()\n        print('After function')\n    return wrapper\n\n@my_decorator\ndef say_hello():\n    print('Hello!')\n\nsay_hello()",
     "Before function\nHello!\nAfter function",
     "Decorator takes a function, returns a new function with added behavior.",
     "Write a decorator that prints 'Starting...' before and 'Done!' after the decorated function.",
     "def log_decorator(func):\n    def wrapper(*args, **kwargs):\n        print('Starting...')\n        result = func(*args, **kwargs)\n        print('Done!')\n        return result\n    return wrapper\n\n@log_decorator\ndef greet(name):\n    print(f'Hello, {name}!')\n\ngreet('Alice')",
     "Starting...\nHello, Alice!\nDone!",
     "What is a decorator in Python?",
     ["A function that modifies another function", "A class that inherits from another", "A variable that stores functions", "A loop that repeats functions"], 0,
     "A decorator is a function that takes another function and extends/modify its behavior."),
    ("generators", "Generators", "Generators are functions that yield values one at a time using yield keyword. Memory-efficient for large sequences.",
     "def count_up_to(n):\n    i = 0\n    while i < n:\n        yield i\n        i += 1\n\nfor num in count_up_to(5):\n    print(num)",
     "0\n1\n2\n3\n4",
     "yield pauses function and returns value. Next call resumes from where it left off.",
     "Write a generator that yields even numbers from 0 to n (inclusive).",
     "def even_numbers(n):\n    for i in range(0, n+1, 2):\n        yield i\n\nfor num in even_numbers(10):\n    print(num)",
     "0\n2\n4\n6\n8\n10",
     "What keyword is used to create a generator?",
     ["return", "yield", "generate", "produce"], 1,
     "yield keyword makes a function a generator, pausing execution and returning values one at a time."),
    ("context_managers", "Context Managers", "Context managers handle setup/teardown using 'with' statement. __enter__ and __exit__ methods define behavior.",
     "class FileManager:\n    def __init__(self, filename):\n        self.filename = filename\n    def __enter__(self):\n        self.file = open(self.filename, 'w')\n        return self.file\n    def __exit__(self, *args):\n        self.file.close()\n\nwith FileManager('test.txt') as f:\n    f.write('Hello')\nprint('File closed')",
     "File closed",
     "Context managers ensure resources are properly cleaned up. __enter__ runs on entry, __exit__ on exit.",
     "Write a context manager that measures execution time of a block.",
     "import time\n\nclass Timer:\n    def __enter__(self):\n        self.start = time.time()\n        return self\n    def __exit__(self, *args):\n        print(f'Elapsed: {time.time() - self.start:.4f}s')\n\nwith Timer():\n    sum(range(1000000))",
     "",
     "Which method is called when exiting a 'with' block?",
     ["__enter__", "__exit__", "__init__", "__del__"], 1,
     "__exit__ is called when the 'with' block exits, even if an exception occurred."),
    ("lambda", "Lambda Functions", "Lambda creates anonymous functions. Syntax: lambda arguments: expression. Useful for short, one-line functions.",
     "square = lambda x: x**2\nprint(square(5))  # 25\n\nnumbers = [1, 2, 3, 4, 5]\nsquares = list(map(lambda x: x**2, numbers))\nprint(squares)  # [1, 4, 9, 16, 25]",
     "25\n[1, 4, 9, 16, 25]",
     "Lambda functions are limited to a single expression. Use def for complex logic.",
     "Use lambda with filter to get even numbers from [1,2,3,4,5,6,7,8,9,10].",
     "numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\nevens = list(filter(lambda x: x % 2 == 0, numbers))\nprint(evens)",
     "[2, 4, 6, 8, 10]",
     "What is a lambda function?",
     ["A named function", "An anonymous function", "A class method", "A built-in function"], 1,
     "Lambda creates anonymous (unnamed) functions in a single expression."),
    ("decorators", "Decorators", "Decorators modify or extend function behavior without changing its source. Use @syntax.",
     "def my_decorator(func):\n    def wrapper():\n        print('Before function')\n        func()\n        print('After function')\n    return wrapper\n\n@my_decorator\ndef say_hello():\n    print('Hello!')\n\nsay_hello()",
     "Before function\nHello!\nAfter function",
     "Decorator takes a function, returns a new function with added behavior.",
     "Write a decorator that prints 'Starting...' before and 'Done!' after the decorated function.",
     "def log_decorator(func):\n    def wrapper(*args, **kwargs):\n        print('Starting...')\n        result = func(*args, **kwargs)\n        print('Done!')\n        return result\n    return wrapper\n\n@log_decorator\ndef greet(name):\n    print(f'Hello, {name}!')\n\ngreet('Alice')",
     "Starting...\nHello, Alice!\nDone!",
     "What is a decorator in Python?",
     ["A function that modifies another function", "A class that inherits from another", "A variable that stores functions", "A loop that repeats functions"], 0,
     "A decorator is a function that takes another function and extends/modify its behavior."),
    ("generators", "Generators", "Generators are functions that yield values one at a time using yield keyword. Memory-efficient for large sequences.",
     "def count_up_to(n):\n    i = 0\n    while i < n:\n        yield i\n        i += 1\n\nfor num in count_up_to(5):\n    print(num)",
     "0\n1\n2\n3\n4",
     "yield pauses function and returns value. Next call resumes from where it left off.",
     "Write a generator that yields even numbers from 0 to n (inclusive).",
     "def even_numbers(n):\n    for i in range(0, n+1, 2):\n        yield i\n\nfor num in even_numbers(10):\n    print(num)",
     "0\n2\n4\n6\n8\n10",
     "What keyword is used to create a generator?",
     ["return", "yield", "generate", "produce"], 1,
     "yield keyword makes a function a generator, pausing execution and returning values one at a time."),
    ("context_managers", "Context Managers", "Context managers handle setup/teardown using 'with' statement. __enter__ and __exit__ methods define behavior.",
     "class FileManager:\n    def __init__(self, filename):\n        self.filename = filename\n    def __enter__(self):\n        self.file = open(self.filename, 'w')\n        return self.file\n    def __exit__(self, *args):\n        self.file.close()\n\nwith FileManager('test.txt') as f:\n    f.write('Hello')\nprint('File closed')",
     "File closed",
     "Context managers ensure resources are properly cleaned up. __enter__ runs on entry, __exit__ on exit.",
     "Write a context manager that measures execution time of a block.",
     "import time\n\nclass Timer:\n    def __enter__(self):\n        self.start = time.time()\n        return self\n    def __exit__(self, *args):\n        print(f'Elapsed: {time.time() - self.start:.4f}s')\n\nwith Timer():\n    sum(range(1000000))",
     "",
     "Which method is called when exiting a 'with' block?",
     ["__enter__", "__exit__", "__init__", "__del__"], 1,
     "__exit__ is called when the 'with' block exits, even if an exception occurred."),
    ("lambda", "Lambda Functions", "Lambda creates anonymous functions. Syntax: lambda arguments: expression. Useful for short, one-line functions.",
     "square = lambda x: x**2\nprint(square(5))  # 25\n\nnumbers = [1, 2, 3, 4, 5]\nsquares = list(map(lambda x: x**2, numbers))\nprint(squares)  # [1, 4, 9, 16, 25]",
     "25\n[1, 4, 9, 16, 25]",
     "Lambda functions are limited to a single expression. Use def for complex logic.",
     "Use lambda with filter to get even numbers from [1,2,3,4,5,6,7,8,9,10].",
     "numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\nevens = list(filter(lambda x: x % 2 == 0, numbers))\nprint(evens)",
     "[2, 4, 6, 8, 10]",
     "What is a lambda function?",
     ["A named function", "An anonymous function", "A class method", "A built-in function"], 1,
     "Lambda creates anonymous (unnamed) functions in a single expression."),
]

# Projects with real multi-step content
PYTHON_PROJECTS = [
    {
        "id": "project-calculator",
        "title": "Build a Calculator",
        "track": "python",
        "description": "Build a calculator that can add, subtract, multiply, and divide.",
        "difficulty": "beginner",
        "prerequisites": ["python-functions", "python-conditionals"],
        "xpReward": 100,
        "steps": [
            {
                "id": "calc-1",
                "type": "explain",
                "title": "Calculator Design",
                "content": "We'll build a calculator that takes two numbers and an operation, then returns the result.",
                "code": "def calculate(a, op, b):\n    if op == '+': return a + b\n    if op == '-': return a - b\n    if op == '*': return a * b\n    if op == '/': return a / b",
                "output": "",
                "explanation": "Use if/elif to check the operation and perform the calculation."
            },
            {
                "id": "calc-2",
                "type": "exercise",
                "title": "Implement Calculator",
                "instruction": "Complete the calculate function to handle +, -, *, / operations.",
                "starterCode": "def calculate(a, op, b):\n    # Your code here\n    pass",
                "solution": "def calculate(a, op, b):\n    if op == '+':\n        return a + b\n    elif op == '-':\n        return a - b\n    elif op == '*':\n        return a * b\n    elif op == '/':\n        return a / b\n    else:\n        return 'Invalid operation'",
                "tests": [{"input": None, "expected": "7", "check": "calculate_3_plus_4"}],
                "explanation": "Check each operation with if/elif and return the result.",
                "hints": ["Handle +, -, *, /", "Use if/elif chain"]
            },
            {
                "id": "calc-3",
                "type": "exercise",
                "title": "Add Error Handling",
                "instruction": "Add division by zero handling to the calculator.",
                "starterCode": "def calculate(a, op, b):\n    if op == '+': return a + b\n    if op == '-': return a - b\n    if op == '*': return a * b\n    if op == '/':\n        # Add zero check\n        pass",
                "solution": "def calculate(a, op, b):\n    if op == '+': return a + b\n    if op == '-': return a - b\n    if op == '*': return a * b\n    if op == '/':\n        if b == 0:\n            return 'Cannot divide by zero'\n        return a / b",
                "tests": [{"input": None, "expected": "Cannot divide by zero", "check": "division_by_zero"}],
                "explanation": "Check if b is 0 before dividing.",
                "hints": ["if b == 0: return 'Cannot divide by zero'"]
            },
            {
                "id": "calc-4",
                "type": "quiz",
                "title": "Calculator",
                "question": "What should the calculator return for calculate(10, '/', 0)?",
                "options": ["0", "Error", "Cannot divide by zero", "Infinity"],
                "correctIndex": 2,
                "explanation": "Division by zero should be handled gracefully with an error message."
            }
        ]
    },
    {
        "id": "project-guessing-game",
        "title": "Number Guessing Game",
        "track": "python",
        "description": "Build a number guessing game with random numbers and hints.",
        "difficulty": "beginner",
        "prerequisites": ["python-loops", "python-conditionals", "python-functions"],
        "xpReward": 120,
        "steps": [
            {
                "id": "guess-1",
                "type": "explain",
                "title": "Game Design",
                "content": "Generate a random number between 1 and 100. The player guesses. Give hints 'too high' or 'too low'. Count attempts.",
                "code": "import random\nsecret = random.randint(1, 100)\nguess = int(input('Guess: '))\nif guess < secret: print('Too low')\nelif guess > secret: print('Too high')\nelse: print('Correct!')",
                "output": "",
                "explanation": "Use random module to generate secret number. Compare guess with secret."
            },
            {
                "id": "guess-2",
                "type": "exercise",
                "title": "Generate Secret Number",
                "instruction": "Write code that generates a random number between 1 and 100 and prints it.",
                "starterCode": "import random\n# Your code here\n",
                "solution": "import random\nsecret = random.randint(1, 100)\nprint(secret)",
                "tests": [{"input": None, "expected": None, "check": "prints_random_number"}],
                "explanation": "random.randint(1, 100) generates a number between 1 and 100.",
                "hints": ["import random", "random.randint(1, 100)"]
            },
            {
                "id": "guess-3",
                "type": "exercise",
                "title": "Check Guess",
                "instruction": "Write a function check_guess(guess, secret) that returns 'Too low', 'Too high', or 'Correct'.",
                "starterCode": "def check_guess(guess, secret):\n    # Your code here\n    pass",
                "solution": "def check_guess(guess, secret):\n    if guess < secret:\n        return 'Too low'\n    elif guess > secret:\n        return 'Too high'\n    else:\n        return 'Correct'",
                "tests": [{"input": None, "expected": "Too low", "check": "check_guess_too_low"}],
                "explanation": "Compare guess with secret and return appropriate message.",
                "hints": ["if guess < secret: return 'Too low'", "elif guess > secret: return 'Too high'", "else: return 'Correct'"]
            },
            {
                "id": "guess-4",
                "type": "quiz",
                "title": "Random Module",
                "question": "Which function generates a random integer between a and b inclusive?",
                "options": ["random.random(a, b)", "random.randint(a, b)", "random.choice(a, b)", "random.range(a, b)"],
                "correctIndex": 1,
                "explanation": "random.randint(a, b) returns a random integer N such that a <= N <= b."
            }
        ]
    },
    {
        "id": "project-todo-list",
        "title": "To-Do List App",
        "track": "python",
        "description": "Build a simple to-do list manager with add, view, and remove.",
        "difficulty": "intermediate",
        "prerequisites": ["python-lists", "python-functions", "python-loops"],
        "xpReward": 150,
        "steps": [
            {
                "id": "todo-1",
                "type": "explain",
                "title": "To-Do List Design",
                "content": "Store tasks in a list. Provide functions to add, view, and remove tasks. Use a while loop for the menu.",
                "code": "tasks = []\ndef add_task(task):\n    tasks.append(task)\ndef view_tasks():\n    for i, task in enumerate(tasks, 1):\n        print(f'{i}. {task}')\ndef remove_task(index):\n    tasks.pop(index - 1)",
                "output": "",
                "explanation": "Use a list to store tasks. Functions for each operation."
            },
            {
                "id": "todo-2",
                "type": "exercise",
                "title": "Add Task Function",
                "instruction": "Write add_task(tasks, task) that appends task to tasks list and returns the updated list.",
                "starterCode": "def add_task(tasks, task):\n    # Your code here\n    pass",
                "solution": "def add_task(tasks, task):\n    tasks.append(task)\n    return tasks",
                "tests": [{"input": None, "expected": None, "check": "add_task_works"}],
                "explanation": "Use append() to add the task, then return the list.",
                "hints": ["tasks.append(task)", "return tasks"]
            },
            {
                "id": "todo-3",
                "type": "exercise",
                "title": "View Tasks Function",
                "instruction": "Write view_tasks(tasks) that prints each task with a number starting from 1.",
                "starterCode": "def view_tasks(tasks):\n    # Your code here\n    pass",
                "solution": "def view_tasks(tasks):\n    for i, task in enumerate(tasks, 1):\n        print(f'{i}. {task}')",
                "tests": [{"input": None, "expected": None, "check": "view_tasks_works"}],
                "explanation": "Use enumerate with start=1 to get numbered tasks.",
                "hints": ["enumerate(tasks, 1)", "print(f'{i}. {task}')"]
            },
            {
                "id": "todo-4",
                "type": "quiz",
                "title": "List Operations",
                "question": "What does list.pop(0) do?",
                "options": ["Removes first element", "Removes last element", "Removes element at index 0 and returns it", "Clears the list"],
                "correctIndex": 2,
                "explanation": "pop(index) removes and returns the element at the specified index. pop(0) removes the first element."
            }
        ]
    }
]

def create_lesson(topic, content, difficulty="beginner", xp=50, prerequisites=None):
    return {
        "id": "python-" + topic,
        "title": content["explain"]["title"],
        "track": "python",
        "description": content["explain"]["content"][:80],
        "difficulty": difficulty,
        "prerequisites": prerequisites or [],
        "xpReward": xp,
        "steps": [
            {
                "id": topic + "-explain",
                "type": "explain",
                "title": content["explain"]["title"],
                "content": content["explain"]["content"],
                "code": content["explain"]["code"],
                "output": content["explain"]["output"],
                "explanation": content["explain"]["explanation"]
            },
            {
                "id": topic + "-exercise",
                "type": "exercise",
                "title": content["exercise"]["title"],
                "instruction": content["exercise"]["instruction"],
                "starterCode": content["exercise"]["starterCode"],
                "solution": content["exercise"]["solution"],
                "tests": content["exercise"]["tests"],
                "explanation": content["exercise"]["explanation"],
                "hints": content["exercise"].get("hints", [])
            },
            {
                "id": topic + "-quiz",
                "type": "quiz",
                "title": content["quiz"]["title"],
                "question": content["quiz"]["question"],
                "options": content["quiz"]["options"],
                "correctIndex": content["quiz"]["correctIndex"],
                "explanation": content["quiz"]["explanation"]
            }
        ]
    }

# Build real lessons from content library
real_lessons = []
for topic, content in PYTHON_CONTENT.items():
    lesson = create_lesson(topic, content)
    real_lessons.append(lesson)

# Add project lessons
for project in PYTHON_PROJECTS:
    real_lessons.append(project)

print("Created " + str(len(real_lessons)) + " real Python lessons from content library")
print("Topics:", [l["id"] for l in real_lessons])

# Verify content quality
for lesson in real_lessons:
    print("\n--- " + lesson["id"] + ": " + lesson["title"] + " ---")
    for step in lesson["steps"]:
        print("  Step:", step["id"], "(", step["type"], ")")
        if step["type"] == "explain":
            print("    Code:", step["code"][:80], "...")
        elif step["type"] == "exercise":
            print("    Solution:", step["solution"][:80], "...")
        elif step["type"] == "quiz":
            print("    Q:", step["question"])
            print("    Options:", step["options"])
            print("    Correct:", step["correctIndex"])