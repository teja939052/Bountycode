"""Comprehensive Python lesson content library - coddy.tech quality.
Each topic has real code examples, real exercises, and real quizzes.
"""
PYTHON_CONTENT = {
    "variables": {
        "explain": {
            "title": "Variables in Python",
            "content": "A variable is a name that stores a value. In Python, you create a variable by assigning a value to a name using the = operator. No type declaration needed - Python is dynamically typed.",
            "code": "name = \"Alice\"\nage = 25\nheight = 5.6\nis_student = True\nprint(name, age, height, is_student)",
            "output": "Alice 25 5.6 True",
            "explanation": "Variables store data. Python figures out the type automatically from the value assigned."
        },
        "exercise": {
            "title": "Create Variables",
            "instruction": "Create a variable called 'city' with value 'Tokyo', a variable 'population' with value 14000000, and print both.",
            "starterCode": "# Create your variables here\n",
            "solution": 'city = "Tokyo"\npopulation = 14000000\nprint(city, population)',
            "tests": [{"input": None, "expected": "Tokyo 14000000", "check": "prints_city_and_population"}],
            "explanation": "Assign string to city and integer to population, then print both.",
            "hints": ['Use city = "Tokyo"', "Use population = 14000000", "print(city, population)"]
        },
        "quiz": {
            "title": "Variable Rules",
            "question": "Which of these is a valid Python variable name?",
            "options": ["2nd_name", "first-name", "first_name", "first name"],
            "correctIndex": 2,
            "explanation": "Variable names can contain letters, digits, and underscores, but cannot start with a digit or contain spaces or hyphens."
        }
    },
    "strings": {
        "explain": {
            "title": "Strings in Python",
            "content": "A string is a sequence of characters enclosed in single or double quotes. Strings are immutable - you can't change individual characters after creation.",
            "code": "name = \"Alice\"\nprint(name[0])      # First character: A\nprint(name[-1])     # Last character: e\nprint(len(name))    # Length: 5\nprint(name.upper()) # ALICE",
            "output": "A\ne\n5\nALICE",
            "explanation": "Strings support indexing (0-based), slicing, and many built-in methods for transformation."
        },
        "exercise": {
            "title": "String Methods",
            "instruction": "Given s = 'Hello World', print the length of s, then print s with all characters uppercase, then print s with spaces replaced by underscores.",
            "starterCode": "s = 'Hello World'\n# Your code here\n",
            "solution": "s = 'Hello World'\nprint(len(s))\nprint(s.upper())\nprint(s.replace(' ', '_'))",
            "tests": [{"input": None, "expected": "11\nHELLO WORLD\nHello_World", "check": "prints_length_upper_replace"}],
            "explanation": "len(s) gives 11. upper() converts to uppercase. replace(' ', '_') replaces spaces.",
            "hints": ["len(s) gives the length", "s.upper() converts to uppercase", "s.replace(' ', '_') replaces spaces"]
        },
        "quiz": {
            "title": "String Immutability",
            "question": "What happens when you try to change a character in a string: s[0] = 'X'?",
            "options": ["It works silently", "It raises TypeError", "It raises IndexError", "It creates a new string"],
            "correctIndex": 1,
            "explanation": "Strings are immutable in Python. Attempting to modify a character raises TypeError: 'str' object does not support item assignment."
        }
    },
    "lists": {
        "explain": {
            "title": "Lists in Python",
            "content": "A list is an ordered, mutable collection of items. Lists can contain items of different types. You can add, remove, and modify items after creation.",
            "code": "fruits = ['apple', 'banana', 'cherry']\nfruits.append('date')\nprint(fruits)\nprint(fruits[1])\nprint(fruits[-1])\nprint(fruits[1:3])",
            "output": "['apple', 'banana', 'cherry', 'date']\nbanana\ndate\n['banana', 'cherry']",
            "explanation": "Lists are mutable and ordered. Indexing is 0-based. Negative indices count from the end."
        },
        "exercise": {
            "title": "List Operations",
            "instruction": "Create a list with numbers 1, 2, 3. Append 4, then remove 2, then print the list and its length.",
            "starterCode": "# Your code here\n",
            "solution": "nums = [1, 2, 3]\nnums.append(4)\nnums.remove(2)\nprint(nums)\nprint(len(nums))",
            "tests": [{"input": None, "expected": "[1, 3, 4]\n3", "check": "prints_list_and_length"}],
            "explanation": "Start with [1,2,3], append 4, remove 2, length is 3.",
            "hints": ["nums = [1, 2, 3]", "nums.append(4)", "nums.remove(2)"]
        },
        "quiz": {
            "title": "List Methods",
            "question": "What does list.insert(1, 'x') do?",
            "options": ["Appends 'x' to end", "Inserts 'x' at index 1", "Replaces index 1 with 'x'", "Removes index 1"],
            "correctIndex": 1,
            "explanation": "insert(index, value) inserts the value at the specified position, shifting existing elements right."
        }
    },
    "dictionaries": {
        "explain": {
            "title": "Dictionaries in Python",
            "content": "A dictionary stores key-value pairs. Keys must be unique and immutable. Dictionaries are mutable - you can add, update, or remove key-value pairs after creation.",
            "code": "person = {'name': 'Alice', 'age': 25, 'city': 'Tokyo'}\nprint(person['name'])\nperson['age'] = 26\nperson['email'] = 'a@b.com'\nprint(person)\nprint(person.get('phone', 'N/A'))",
            "output": "Alice\n{'name': 'Alice', 'age': 26, 'city': 'Tokyo', 'email': 'a@b.com'}\nN/A",
            "explanation": "Dictionaries provide O(1) average lookup by key. Use .get() to avoid KeyError for missing keys."
        },
        "exercise": {
            "title": "Dictionary Operations",
            "instruction": "Create a dictionary with keys 'name', 'age', 'city'. Update 'age' to 30, add 'country' with value 'Japan', then print the dictionary.",
            "starterCode": "# Your code here\n",
            "solution": "d = {'name': 'Bob', 'age': 25, 'city': 'Osaka'}\nd['age'] = 30\nd['country'] = 'Japan'\nprint(d)",
            "tests": [{"input": None, "expected": None, "check": "prints_dict_with_country"}],
            "explanation": "Create dict, update age to 30, add country key, print.",
            "hints": ["d = {'name': 'Bob', 'age': 25, 'city': 'Osaka'}", "d['age'] = 30", "d['country'] = 'Japan'"]
        },
        "quiz": {
            "title": "Dictionary Keys",
            "question": "Can a list be a dictionary key?",
            "options": ["Yes, always", "No, keys must be immutable", "Only if the list is empty", "Only in Python 3.10+"],
            "correctIndex": 1,
            "explanation": "Dictionary keys must be hashable (immutable). Lists are mutable and unhashable, so they cannot be keys."
        }
    },
    "functions": {
        "explain": {
            "title": "Functions in Python",
            "content": "A function is a reusable block of code. Define with 'def', call by name. Functions can take parameters and return values.",
            "code": "def greet(name):\n    return f'Hello, {name}!'\n\ndef add(a, b):\n    return a + b\n\nprint(greet('Alice'))\nprint(add(3, 4))",
            "output": "Hello, Alice!\n7",
            "explanation": "def defines a function. Parameters receive arguments. return sends a value back."
        },
        "exercise": {
            "title": "Write a Function",
            "instruction": "Write a function 'multiply(a, b)' that returns the product of a and b. Then call it with 6 and 7 and print the result.",
            "starterCode": "# Define multiply function here\n",
            "solution": "def multiply(a, b):\n    return a * b\n\nprint(multiply(6, 7))",
            "tests": [{"input": None, "expected": "42", "check": "prints_42"}],
            "explanation": "Define multiply with two parameters, return a * b, call with 6 and 7.",
            "hints": ["def multiply(a, b):", "return a * b", "print(multiply(6, 7))"]
        },
        "quiz": {
            "title": "Function Parameters",
            "question": "What is the difference between a parameter and an argument?",
            "options": ["No difference", "Parameter is in definition, argument is in call", "Argument is in definition, parameter is in call", "Parameter is required, argument is optional"],
            "correctIndex": 1,
            "explanation": "A parameter is the variable name in the function definition. An argument is the actual value passed when calling."
        }
    },
    "loops": {
        "explain": {
            "title": "Loops in Python",
            "content": "Use 'for' to iterate over sequences, 'while' to repeat while a condition is true. break exits early, continue skips to next iteration.",
            "code": "for i in range(5):\n    print(i)\n\n# While loop\ncount = 0\nwhile count < 3:\n    print(count)\n    count += 1",
            "output": "0\n1\n2\n3\n4\n0\n1\n2",
            "explanation": "for iterates over a sequence. while repeats while condition is true. range(5) produces 0,1,2,3,4."
        },
        "exercise": {
            "title": "Loop Practice",
            "instruction": "Print the sum of all numbers from 1 to 10 using a for loop.",
            "starterCode": "total = 0\n# Your code here\n",
            "solution": "total = 0\nfor i in range(1, 11):\n    total += i\nprint(total)",
            "tests": [{"input": None, "expected": "55", "check": "prints_55"}],
            "explanation": "range(1, 11) gives 1 through 10. Sum them up: 1+2+...+10 = 55.",
            "hints": ["range(1, 11) gives 1 to 10", "Use total += i"]
        },
        "quiz": {
            "title": "Loop Behavior",
            "question": "What does 'break' do in a loop?",
            "options": ["Skips one iteration", "Exits the loop immediately", "Restarts the loop", "Pauses the loop"],
            "correctIndex": 1,
            "explanation": "break immediately exits the loop, regardless of the loop condition."
        }
    },
    "conditionals": {
        "explain": {
            "title": "Conditionals in Python",
            "content": "Use if/elif/else to make decisions. Python uses indentation to define code blocks. No curly braces needed.",
            "code": "age = 20\nif age < 13:\n    print('Child')\nelif age < 18:\n    print('Teen')\nelse:\n    print('Adult')",
            "output": "Adult",
            "explanation": "if checks first condition. elif checks next. else runs if none matched. Indentation defines blocks."
        },
        "exercise": {
            "title": "Grade Calculator",
            "instruction": "Given score = 85, print 'A' if score >= 90, 'B' if score >= 80, 'C' if score >= 70, else 'F'.",
            "starterCode": "score = 85\n# Your code here\n",
            "solution": "score = 85\nif score >= 90:\n    print('A')\nelif score >= 80:\n    print('B')\nelif score >= 70:\n    print('C')\nelse:\n    print('F')",
            "tests": [{"input": None, "expected": "B", "check": "prints_B"}],
            "explanation": "85 >= 80 is True, so prints 'B'.",
            "hints": ["Check 90 first, then 80, then 70"]
        },
        "quiz": {
            "title": "Elif",
            "question": "How many elif clauses can an if statement have?",
            "options": ["At most 1", "At most 2", "Zero or more", "Exactly 1"],
            "correctIndex": 2,
            "explanation": "You can have zero or more elif clauses in an if statement."
        }
    },
    "comprehensions": {
        "explain": {
            "title": "List Comprehensions",
            "content": "List comprehensions provide a concise way to create lists. They consist of brackets containing an expression followed by a for clause, then zero or more if clauses.",
            "code": "squares = [x**2 for x in range(5)]\nprint(squares)  # [0, 1, 4, 9, 16]\n\neven = [x for x in range(10) if x % 2 == 0]\nprint(even)  # [0, 2, 4, 6, 8]",
            "output": "[0, 1, 4, 9, 16]\n[0, 2, 4, 6, 8]",
            "explanation": "Comprehensions are more readable and faster than equivalent for loops with append."
        },
        "exercise": {
            "title": "Create Comprehension",
            "instruction": "Create a list of cubes (x^3) for x in range(1, 6) using a list comprehension. Print it.",
            "starterCode": "# Your code here\n",
            "solution": "cubes = [x**3 for x in range(1, 6)]\nprint(cubes)",
            "tests": [{"input": None, "expected": "[1, 8, 27, 64, 125]", "check": "prints_cubes"}],
            "explanation": "x**3 for x in range(1, 6) gives [1, 8, 27, 64, 125].",
            "hints": ["[x**3 for x in range(1, 6)]"]
        },
        "quiz": {
            "title": "Comprehension Syntax",
            "question": "What is the syntax for a list comprehension?",
            "options": ["[expression for item in iterable]", "(expression for item in iterable)", "{expression for item in iterable}", "expression for item in iterable"],
            "correctIndex": 0,
            "explanation": "List comprehensions use square brackets: [expression for item in iterable]."
        }
    },
    "file_io": {
        "explain": {
            "title": "File I/O in Python",
            "content": "Use open() to read/write files. Always use 'with' statement to ensure files are closed properly. Modes: 'r' (read), 'w' (write), 'a' (append).",
            "code": "with open('example.txt', 'w') as f:\n    f.write('Hello, World!')\n\nwith open('example.txt', 'r') as f:\n    content = f.read()\n    print(content)",
            "output": "Hello, World!",
            "explanation": "'with' statement automatically closes the file. 'w' writes, 'r' reads."
        },
        "exercise": {
            "title": "Read and Write File",
            "instruction": "Write 'Python is awesome' to a file named 'test.txt', then read it back and print the content.",
            "starterCode": "# Your code here\n",
            "solution": "with open('test.txt', 'w') as f:\n    f.write('Python is awesome')\n\nwith open('test.txt', 'r') as f:\n    content = f.read()\n    print(content)",
            "tests": [{"input": None, "expected": "Python is awesome", "check": "reads_written_content"}],
            "explanation": "Write with 'w' mode, read with 'r' mode using with statement.",
            "hints": ["with open('test.txt', 'w') as f:", "f.write('Python is awesome')", "with open('test.txt', 'r') as f:"]
        },
        "quiz": {
            "title": "File Modes",
            "question": "What does 'a' mode do when opening a file?",
            "options": ["Read only", "Write and truncate", "Append to end", "Read and write"],
            "correctIndex": 2,
            "explanation": "'a' mode opens file for appending - new content is added to the end."
        }
    },
    "exceptions": {
        "explain": {
            "title": "Exception Handling in Python",
            "content": "Use try/except to handle errors gracefully. finally block runs always. raise to throw exceptions.",
            "code": "try:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print('Cannot divide by zero')\nfinally:\n    print('Done')",
            "output": "Cannot divide by zero\nDone",
            "explanation": "try block contains risky code. except catches specific errors. finally always runs."
        },
        "exercise": {
            "title": "Handle ValueError",
            "instruction": "Write code that tries to convert 'abc' to int, catches ValueError, and prints 'Invalid number'.",
            "starterCode": "try:\n    # Your code here\n    pass\n",
            "solution": "try:\n    int('abc')\nexcept ValueError:\n    print('Invalid number')",
            "tests": [{"input": None, "expected": "Invalid number", "check": "catches_value_error"}],
            "explanation": "int('abc') raises ValueError, which is caught by except.",
            "hints": ["int('abc') raises ValueError", "except ValueError: print('Invalid number')"]
        },
        "quiz": {
            "title": "Exception Handling",
            "question": "What does 'finally' block do?",
            "options": ["Runs only if no exception", "Runs only if exception", "Runs always", "Runs before try"],
            "correctIndex": 2,
            "explanation": "finally block always runs, whether or not an exception occurred."
        }
    },
    "decorators": {
        "explain": {
            "title": "Decorators in Python",
            "content": "Decorators modify or extend function behavior without changing its source. Use @syntax. Functions are first-class objects in Python.",
            "code": "def my_decorator(func):\n    def wrapper():\n        print('Before function')\n        func()\n        print('After function')\n    return wrapper\n\n@my_decorator\ndef say_hello():\n    print('Hello!')\n\nsay_hello()",
            "output": "Before function\nHello!\nAfter function",
            "explanation": "Decorator takes a function, returns a new function with added behavior."
        },
        "exercise": {
            "title": "Write a Decorator",
            "instruction": "Write a decorator that prints 'Starting...' before and 'Done!' after the decorated function.",
            "starterCode": "def log_decorator(func):\n    # Your code here\n    pass",
            "solution": "def log_decorator(func):\n    def wrapper(*args, **kwargs):\n        print('Starting...')\n        result = func(*args, **kwargs)\n        print('Done!')\n        return result\n    return wrapper\n\n@log_decorator\ndef greet(name):\n    print(f'Hello, {name}!')\n\ngreet('Alice')",
            "tests": [{"input": None, "expected": "Starting...\nHello, Alice!\nDone!", "check": "decorator_works"}],
            "explanation": "Decorator wraps function with before/after behavior.",
            "hints": ["def wrapper(*args, **kwargs):", "print('Starting...')", "result = func(*args, **kwargs)", "print('Done!')"]
        },
        "quiz": {
            "title": "Decorators",
            "question": "What is a decorator in Python?",
            "options": ["A function that modifies another function", "A class that inherits from another", "A variable that stores functions", "A loop that repeats functions"],
            "correctIndex": 0,
            "explanation": "A decorator is a function that takes another function and extends/modify its behavior."
        }
    },
    "generators": {
        "explain": {
            "title": "Generators in Python",
            "content": "Generators are functions that yield values one at a time using yield keyword. Memory-efficient for large sequences.",
            "code": "def count_up_to(n):\n    i = 0\n    while i < n:\n        yield i\n        i += 1\n\nfor num in count_up_to(5):\n    print(num)",
            "output": "0\n1\n2\n3\n4",
            "explanation": "yield pauses function and returns value. Next call resumes from where it left off."
        },
        "exercise": {
            "title": "Write a Generator",
            "instruction": "Write a generator that yields even numbers from 0 to n (inclusive).",
            "starterCode": "def even_numbers(n):\n    # Your code here\n    pass\n",
            "solution": "def even_numbers(n):\n    for i in range(0, n+1, 2):\n        yield i\n\nfor num in even_numbers(10):\n    print(num)",
            "tests": [{"input": None, "expected": "0\n2\n4\n6\n8\n10", "check": "yields_even_numbers"}],
            "explanation": "Use range(0, n+1, 2) to generate even numbers, yield each.",
            "hints": ["for i in range(0, n+1, 2):", "yield i"]
        },
        "quiz": {
            "title": "Generators",
            "question": "What keyword is used to create a generator?",
            "options": ["return", "yield", "generate", "produce"],
            "correctIndex": 1,
            "explanation": "yield keyword makes a function a generator, pausing execution and returning values one at a time."
        }
    },
    "context_managers": {
        "explain": {
            "title": "Context Managers in Python",
            "content": "Context managers handle setup/teardown using 'with' statement. __enter__ and __exit__ methods define behavior.",
            "code": "class FileManager:\n    def __init__(self, filename):\n        self.filename = filename\n    def __enter__(self):\n        self.file = open(self.filename, 'w')\n        return self.file\n    def __exit__(self, *args):\n        self.file.close()\n\nwith FileManager('test.txt') as f:\n    f.write('Hello')\nprint('File closed')",
            "output": "File closed",
            "explanation": "Context managers ensure resources are properly cleaned up. __enter__ runs on entry, __exit__ on exit."
        },
        "exercise": {
            "title": "Write a Context Manager",
            "instruction": "Write a context manager that measures execution time of a block.",
            "starterCode": "import time\n\nclass Timer:\n    def __enter__(self):\n        # Your code here\n        pass\n    def __exit__(self, *args):\n        # Your code here\n        pass\n",
            "solution": "import time\n\nclass Timer:\n    def __enter__(self):\n        self.start = time.time()\n        return self\n    def __exit__(self, *args):\n        print(f'Elapsed: {time.time() - self.start:.4f}s')\n\nwith Timer():\n    sum(range(1000000))",
            "tests": [{"input": None, "expected": None, "check": "timer_context_manager"}],
            "explanation": "Record start time in __enter__, print elapsed in __exit__.",
            "hints": ["self.start = time.time()", "print(f'Elapsed: {time.time() - self.start:.4f}s')"]
        },
        "quiz": {
            "title": "Context Managers",
            "question": "Which method is called when exiting a 'with' block?",
            "options": ["__enter__", "__exit__", "__init__", "__del__"],
            "correctIndex": 1,
            "explanation": "__exit__ is called when the 'with' block exits, even if an exception occurred."
        }
    },
    "lambda": {
        "explain": {
            "title": "Lambda Functions in Python",
            "content": "Lambda creates anonymous functions. Syntax: lambda arguments: expression. Useful for short, one-line functions.",
            "code": "square = lambda x: x**2\nprint(square(5))  # 25\n\nnumbers = [1, 2, 3, 4, 5]\nsquares = list(map(lambda x: x**2, numbers))\nprint(squares)  # [1, 4, 9, 16, 25]",
            "output": "25\n[1, 4, 9, 16, 25]",
            "explanation": "Lambda functions are limited to a single expression. Use def for complex logic."
        },
        "exercise": {
            "title": "Use Lambda with Filter",
            "instruction": "Use lambda with filter to get even numbers from [1,2,3,4,5,6,7,8,9,10].",
            "starterCode": "numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n# Your code here\n",
            "solution": "numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\nevens = list(filter(lambda x: x % 2 == 0, numbers))\nprint(evens)",
            "tests": [{"input": None, "expected": "[2, 4, 6, 8, 10]", "check": "filters_even_numbers"}],
            "explanation": "filter(lambda x: x % 2 == 0, numbers) keeps only even numbers.",
            "hints": ["list(filter(lambda x: x % 2 == 0, numbers))"]
        },
        "quiz": {
            "title": "Lambda Functions",
            "question": "What is a lambda function?",
            "options": ["A named function", "An anonymous function", "A class method", "A built-in function"],
            "correctIndex": 1,
            "explanation": "Lambda creates anonymous (unnamed) functions in a single expression."
        }
    }
}

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