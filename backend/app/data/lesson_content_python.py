"""Hand-crafted lesson content for Python levels 1-3.

Lesson ID format: python-l{level:02d}-{lesson:02d}
"""

from typing import Any


def _lesson(
    lesson_id: str,
    theory: str,
    analogy: str,
    sections: list[dict[str, Any]],
    code_example: dict[str, Any] | None = None,
    common_mistakes: list[dict[str, Any]] | None = None,
    exercise: dict[str, Any] | None = None,
    quiz: dict[str, Any] | None = None,
    key_takeaways: list[str] | None = None,
    next_steps: str = "",
) -> tuple[str, dict[str, Any]]:
    content: dict[str, Any] = {
        "theory": theory,
        "analogy": analogy,
        "sections": sections,
    }
    if code_example:
        content["code_example"] = code_example
    if common_mistakes:
        content["common_mistakes"] = common_mistakes
    if exercise:
        content["exercise"] = exercise
    if quiz:
        content["quiz"] = quiz
    if key_takeaways:
        content["key_takeaways"] = key_takeaways
    if next_steps:
        content["next_steps"] = next_steps
    return lesson_id, content


def _code(code: str, annotations: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"code": code}
    if annotations:
        result["annotations"] = annotations
    return result


HAND_CRAFTED_PYTHON_LESSONS: dict[str, dict[str, Any]] = {}

HAND_CRAFTED_PYTHON_LESSONS.update(dict([
    # =========================================================================
    # LEVEL 1: FIRST STEPS
    # =========================================================================
    _lesson(
        lesson_id="python-l01-01",
        theory=(
            "Python is a programming language created by Guido van Rossum in 1991. "
            "It was designed to be readable and simple so that anyone can learn it. "
            "Today Python powers web apps, data science, artificial intelligence, "
            "automation, and even rockets."
            "\n\n"
            "Python is an interpreted language, which means it runs your code line by line "
            "without a separate compile step. That makes it perfect for beginners because you "
            "can see results almost instantly."
        ),
        analogy=(
            "Python is like a friendly guide who speaks plain English instead of jargon. "
            "Where other languages make you fill out complicated forms before doing anything, "
            "Python just lets you talk and it listens."
        ),
        sections=[
            {
                "heading": "Why Python is everywhere",
                "body": (
                    "Python is the most popular first language in the world. Companies like Google, "
                    "Instagram, Netflix, and NASA use it. Whether you want to build websites, "
                    "analyze data, or train AI models, Python is the common thread."
                ),
                "pro_tip": (
                    "Python's name comes from Monty Python's Flying Circus, not the snake. "
                    "That is why many tutorials use silly examples!"
                ),
            },
            {
                "heading": "Readable by design",
                "body": (
                    "Python uses plain English keywords like print, if, and for instead of symbols. "
                    "Code you write today will still make sense when you read it next month. "
                    "Readability is a core design goal, not an afterthought."
                ),
                "pro_tip": (
                    "Read other people's Python code as often as you write your own. "
                    "You will absorb good style just by looking at it."
                ),
            },
            {
                "heading": "Interpreted, not compiled",
                "body": (
                    "When you run a .py file, Python reads and executes each line immediately. "
                    "There is no separate build step, so you can test ideas quickly. "
                    "This fast feedback loop is why beginners learn Python so fast."
                ),
                "pro_tip": (
                    "You can test a single Python idea instantly in the Python shell without "
                    "creating a file at all. More on that soon!"
                ),
            },
        ],
        code_example=_code(
            """print('Hello, world!')
name = 'Ada'
print('Welcome,', name)""",
            [
                {"line": 1, "text": "Prints a greeting to the screen"},
                {"line": 2, "text": "Stores the text 'Ada' in a variable called name"},
                {"line": 3, "text": "Prints a welcome message using the variable"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "Print('Hello')",
                "fixed": "print('Hello')",
                "why": "Python keywords and built-in functions are lowercase. Print with a capital P is a different name.",
            },
            {
                "wrong": "print Hello",
                "fixed": "print('Hello')",
                "why": "In Python 3, print is a function, so the message must go inside parentheses.",
            },
            {
                "wrong": "print('Hello)",
                "fixed": "print('Hello')",
                "why": "Every string must be wrapped in a matching pair of quotes, both at the start and the end.",
            },
        ],
        exercise={
            "description": "Write a single print() call that prints the text I am learning Python! to the screen, then run your script.",
            "starter_code": (
                "# Your code here"
            ),
            "hints": [
                "Use print() with the message inside parentheses",
                "Wrap the text in either single quotes or double quotes",
                "Run the script to see your output on the screen",
            ],
            "expected_output": "I am learning Python!",
        },
        quiz={
            "question": "Which of these best describes how Python runs your code?",
            "options": [
                "It compiles the whole program before running anything",
                "It is interpreted and runs line by line",
                "It is a markup language like HTML",
                "It only runs on web browsers",
            ],
            "correct": 1,
            "explanation": "Python is an interpreted language that executes your code line by line, giving instant feedback.",
        },
        key_takeaways=[
            "Python was created in 1991 and is designed for readability",
            "Python is interpreted, so code runs line by line with no compile step",
            "Python powers web apps, data science, AI, and automation",
            "print() is one of the first built-in functions you will use",
        ],
        next_steps="Now let us write your very first Python program: Hello World!",
    ),

    _lesson(
        lesson_id="python-l01-02",
        theory=(
            "The first program every programmer writes prints the words Hello, World! to the screen. "
            "It proves your setup works and that you can run code end to end."
            "\n\n"
            "In Python you use the built-in print() function to display text. "
            "You place the text inside quotes, and it appears on your screen the moment you run the program."
        ),
        analogy=(
            "Writing Hello World is like sending your first message on a new phone. "
            "It is a tiny action, but it proves the device, the network, and your thumbs all work together."
        ),
        sections=[
            {
                "heading": "Your first print",
                "body": (
                    "The simplest possible program is one line: print('Hello, World!'). "
                    "Type it exactly, including the quotes and parentheses, then run it. "
                    "What you type between the quotes is what gets displayed."
                ),
                "pro_tip": (
                    "Type the code by hand instead of copying and pasting. "
                    "Your fingers learn the syntax faster than your eyes do."
                ),
            },
            {
                "heading": "Reading the output",
                "body": (
                    "When you run the program you will see Hello, World! printed below your code. "
                    "Python adds a new line automatically after each print() call, so the next output starts fresh."
                ),
                "pro_tip": (
                    "Change the text inside the quotes and run again. "
                    "You are already editing real code!"
                ),
            },
        ],
        code_example=_code(
            """print('Hello, World!')
print('I am learning Python!')""",
            [
                {"line": 1, "text": "Prints the classic Hello, World! message"},
                {"line": 2, "text": "Prints a second line on its own row"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "print(Hello, World!)",
                "fixed": "print('Hello, World!')",
                "why": "Bare words are treated as code in Python. Text must be wrapped in quotes to be a string.",
            },
            {
                "wrong": "print('Hello, World!')",
                "fixed": "print(\"Hello, World!\")",
                "why": "This one is actually valid! Both single and double quotes create strings. Pick one and stay consistent.",
            },
            {
                "wrong": "print('Hello, World!') extra",
                "fixed": "print('Hello, World!')",
                "why": "Each statement should be on its own line. Trailing random text after a print call causes a syntax error.",
            },
        ],
        exercise={
            "description": "Print the text Hello, Python! on the first line and your own name on the second line.",
            "starter_code": (
                "# Your code here"
            ),
            "hints": [
                "Each print() call outputs one line",
                "Wrap each message in quotes",
                "You need exactly two print() calls",
            ],
            "expected_output": "Hello, Python!\n<Your name>",
        },
        quiz={
            "question": "What does the print() function do in Python?",
            "options": [
                "Reads text typed by the user",
                "Displays text or values on the screen",
                "Sends a file to the printer",
                "Stores text inside a variable",
            ],
            "correct": 1,
            "explanation": "print() is the built-in function that sends its arguments to the screen as output.",
        },
        key_takeaways=[
            "Hello World is the traditional first program in every language",
            "print() displays whatever you put inside its parentheses",
            "Text must be wrapped in quotes to be a string",
            "Each print() call automatically starts a new line",
        ],
        next_steps="Great job! Now let us explore everything the print() function can do.",
    ),

    _lesson(
        lesson_id="python-l01-03",
        theory=(
            "The print() function is your window to the outside world. "
            "It accepts any number of arguments and prints them one after another."
            "\n\n"
            "When you pass multiple arguments separated by commas, Python inserts a single space "
            "between them. You can also pass numbers without quotes, and they will print just fine."
            "\n\n"
            "print() has useful optional parameters like sep and end. The sep parameter controls "
            "the separator between arguments, and end controls what appears after the last value."
        ),
        analogy=(
            "print() is like a public announcement speaker. "
            "Everything you hand it gets broadcast out loud, in order, separated by spaces, "
            "and it ends with a pause before the next announcement."
        ),
        sections=[
            {
                "heading": "Printing more than one thing",
                "body": (
                    "print('Python', 'is', 'fun') prints Python is fun with automatic spaces. "
                    "This saves you from adding spaces yourself and keeps your code clean."
                ),
                "pro_tip": (
                    "You can print numbers, text, and even results of calculations: "
                    "print(2 + 3) prints 5."
                ),
            },
            {
                "heading": "The sep parameter",
                "body": (
                    "By default print() separates arguments with a space. "
                    "You can change that: print('01', '07', '2026', sep='-') prints 01-07-2026. "
                    "The separator can be any string you like."
                ),
                "pro_tip": (
                    "Use sep='' (an empty string) when you want arguments glued together "
                    "with no gap at all."
                ),
            },
            {
                "heading": "The end parameter",
                "body": (
                    "Normally each print() ends with a newline. With end=' ' you can keep the "
                    "cursor on the same line, and with end='' you can print a running message "
                    "that later parts of your program continue."
                ),
                "pro_tip": (
                    "Printing a progress indicator in a loop without newlines is a classic "
                    "use of end=''. You will meet loops soon."
                ),
            },
        ],
        code_example=_code(
            """print('Hello')
print('Python', 'is', 'fun')
print(42)
print('End', end='!\\n')""",
            [
                {"line": 1, "text": "Prints a string with the default newline at the end"},
                {"line": 2, "text": "Prints three arguments separated by a space"},
                {"line": 3, "text": "Prints a number without any quotes"},
                {"line": 4, "text": "end='!\\n' replaces the trailing newline with '!' and then a new line"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "print('one' 'two')",
                "fixed": "print('one', 'two')",
                "why": "Adjacent strings without a comma are glued together as one string in Python. Use a comma to print them separately.",
            },
            {
                "wrong": "print('a', 'b', sep='-', end=' ')",
                "fixed": "print('a', 'b', sep='-', end=' ')  # valid, but note the effect",
                "why": "This is actually valid. Just remember sep controls spaces between values and end controls what comes after all of them.",
            },
            {
                "wrong": "print(sep='-', 'a', 'b')",
                "fixed": "print('a', 'b', sep='-')",
                "why": "In Python, positional arguments like 'a' must come before keyword arguments like sep.",
            },
        ],
        exercise={
            "description": "Use one print() call to display the city and country variables, and make sure they appear with a comma and space between them, like New Delhi, India.",
            "starter_code": (
                "city = 'New Delhi'\n"
                "country = 'India'\n"
                "# Your code here"
            ),
            "hints": [
                "Pass both variables to the same print() call",
                "A plain comma inserts one space, not enough here",
                "Use sep=', ' to insert a comma followed by a space",
            ],
            "expected_output": "New Delhi, India",
        },
        quiz={
            "question": "What is the default separator between multiple arguments in print()?",
            "options": ["A comma", "A single space", "A dash", "No separator at all"],
            "correct": 1,
            "explanation": "print('a', 'b') outputs a b, with a single space inserted between arguments by default.",
        },
        key_takeaways=[
            "print() accepts any number of comma-separated arguments",
            "A single space is added between arguments by default",
            "sep lets you change the separator between values",
            "end lets you change what is printed after the last value",
        ],
        next_steps="Now let us learn how to leave notes in your code with comments.",
    ),
    _lesson(
        lesson_id="python-l01-04",
        theory=(
            "Comments are notes you leave inside your code that Python completely ignores. "
            "They start with a # symbol and run to the end of that line."
            "\n\n"
            "Comments help you explain why your code does something, not just what it does. "
            "They are also a great way to temporarily disable a line while debugging."
        ),
        analogy=(
            "Comments are like sticky notes on a recipe. "
            "The chef (Python) skips them completely, but the next person who cooks "
            "instantly understands why the onions go first."
        ),
        sections=[
            {
                "heading": "Writing a comment",
                "body": (
                    "Anything after a # on a line is ignored. "
                    "A comment can be its own line, or it can follow code on the same line. "
                    "Both are useful in different situations."
                ),
                "pro_tip": (
                    "Use whole-line comments to explain the purpose of a block, "
                    "and trailing comments to clarify one tricky line."
                ),
            },
            {
                "heading": "What makes a good comment",
                "body": (
                    "Good comments explain why, not what. The code already shows what it does. "
                    "For example, # keep the discount under 100% explains the reason behind a calculation. "
                    "Avoid obvious comments like # adds one to x."
                ),
                "pro_tip": (
                    "If a comment grows longer than the code it explains, "
                    "consider simplifying the code instead."
                ),
            },
        ],
        code_example=_code(
            """# This whole line is a comment
print('Visible output')  # Comments can follow code
# TODO: add more features later""",
            [
                {"line": 1, "text": "A full-line comment; Python ignores it"},
                {"line": 2, "text": "Code runs, and the trailing comment is ignored"},
                {"line": 3, "text": "A TODO comment reminds you of future work"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "// this is a comment",
                "fixed": "# this is a comment",
                "why": "C-style // comments are not valid in Python. Only # starts a comment.",
            },
            {
                "wrong": "print('Hello') # important message",
                "fixed": "print('Hello')  # important message",
                "why": "This works either way, but two spaces before a trailing comment is the recommended style.",
            },
            {
                "wrong": "#print('Hidden')",
                "fixed": "print('Hidden')",
                "why": "Putting # in front of code disables it. Remove the # when you actually want it to run.",
            },
        ],
        exercise={
            "description": "Add one comment above the print() call explaining that it prints a programmer identity message, and one trailing comment after it. Then run the script.",
            "starter_code": (
                "# Your code here\n"
                "print('I am a programmer')\n"
                "# Your code here"
            ),
            "hints": [
                "The first comment should be on its own line above the print",
                "The second comment sits on the same line, after the code",
                "Both start with the # symbol",
            ],
            "expected_output": "I am a programmer",
        },
        quiz={
            "question": "Which symbol starts a comment in Python?",
            "options": ["//", "/*", "#", "<!--"],
            "correct": 2,
            "explanation": "In Python, everything after a # to the end of the line is a comment and is ignored by the interpreter.",
        },
        key_takeaways=[
            "Comments start with # and are ignored by Python",
            "Comments explain why, not what, the code does",
            "Comments can be full lines or sit after code",
            "Putting # in front of code temporarily disables it",
        ],
        next_steps="Now let us meet the Python interpreter and the interactive shell.",
    ),

    _lesson(
        lesson_id="python-l01-05",
        theory=(
            "The Python interpreter is the program that reads and executes your Python code. "
            "When you run python my_script.py, the interpreter reads the file top to bottom "
            "and executes each statement in order."
            "\n\n"
            "You also have an interactive mode called the REPL (Read-Eval-Print Loop). "
            "Type a line, press Enter, and Python instantly evaluates it and shows the result. "
            "This is perfect for experimenting."
        ),
        analogy=(
            "The interpreter is like a translator who stands next to you. "
            "Give them one sentence at a time in the REPL and they translate instantly. "
            "Give them a whole letter (a .py file) and they translate the entire thing from top to bottom."
        ),
        sections=[
            {
                "heading": "Running a .py file",
                "body": (
                    "Write your code in a file ending in .py, then run it with python filename.py. "
                    "The interpreter executes every line in order and prints all output. "
                    "This is how real programs run."
                ),
                "pro_tip": (
                    "On Windows you can also run python main.py in the terminal from the "
                    "folder where the file lives."
                ),
            },
            {
                "heading": "The interactive REPL",
                "body": (
                    "Type python with no filename to open the interactive shell. "
                    "The >>> prompt is waiting for you. Try typing 2 + 2 and pressing Enter. "
                    "The result appears immediately."
                ),
                "pro_tip": (
                    "Use the REPL to test small snippets before adding them to your script. "
                    "It is the fastest way to verify an idea."
                ),
            },
        ],
        code_example=_code(
            """print('Python runs line by line')
print('Each line executes in order')""",
            [
                {"line": 1, "text": "First statement executes, printing its message"},
                {"line": 2, "text": "Next statement executes next, in file order"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "python print('Hi')",
                "fixed": "python my_script.py",
                "why": "The interpreter takes a filename, not code. Put the code in a file, then run the file.",
            },
            {
                "wrong": "forgetting the .py extension",
                "fixed": "always save scripts as .py files",
                "why": "The .py extension tells tools and editors that the file is Python source code.",
            },
            {
                "wrong": "expecting variables to persist after the script ends",
                "fixed": "re-run the script to rebuild its state",
                "why": "Every run is a fresh start; variables only live while the program runs.",
            },
        ],
        exercise={
            "description": "Write a script that prints three lines: Ready, Set, Go!, each on its own line, to simulate a script running line by line.",
            "starter_code": (
                "# Your code here"
            ),
            "hints": [
                "One print() call per line",
                "Three print() calls in total",
                "Run the script to see all three lines appear",
            ],
            "expected_output": "Ready\nSet\nGo!",
        },
        quiz={
            "question": "What does the interpreter do when you run a .py file?",
            "options": [
                "Compiles the whole file before running anything",
                "Executes each statement in order from top to bottom",
                "Only runs the first line",
                "Translates the file to C first",
            ],
            "correct": 1,
            "explanation": "Python executes statements sequentially, from the top of the file to the bottom.",
        },
        key_takeaways=[
            "The interpreter reads and executes Python code",
            "Run script files with python filename.py",
            "The REPL evaluates code instantly, line by line",
            "Each run of a script starts with a fresh state",
        ],
        next_steps="Now let us learn the most important rule of Python layout: indentation.",
    ),

    _lesson(
        lesson_id="python-l01-06",
        theory=(
            "Python uses indentation to group blocks of code, where most languages use braces. "
            "Every line in a block must be indented by the same amount, usually four spaces."
            "\n\n"
            "An if statement ends with a colon, and the indented lines below it are the block "
            "that runs when the condition is True. "
            "Indentation is not just style in Python, it is part of the syntax."
        ),
        analogy=(
            "Indentation is like the hierarchy of a company org chart. "
            "The boss (the if line) has employees (the indented lines) working under them. "
            "The deeper the indent, the deeper the level of command."
        ),
        sections=[
            {
                "heading": "Why indentation matters",
                "body": (
                    "In Python, a block is created by indentation alone. "
                    "The if line ends with a colon, and every statement that should run when the "
                    "condition is true must be indented one level. If the indentation is inconsistent, "
                    "Python raises an IndentationError."
                ),
                "pro_tip": (
                    "Always use four spaces for one level of indentation. "
                    "Do not mix tabs and spaces in the same file."
                ),
            },
            {
                "heading": "Dedenting ends the block",
                "body": (
                    "The first line that returns to the previous indentation level ends the block. "
                    "That line always runs, whether the condition was true or false. "
                    "This is how you write code that must run no matter what."
                ),
                "pro_tip": (
                    "If your editor auto-uses tabs, change it to spaces. "
                    "Mix-ups between tabs and spaces cause confusing errors."
                ),
            },
        ],
        code_example=_code(
            """age = 18
if age >= 18:
    print('You can vote!')
print('Done')""",
            [
                {"line": 1, "text": "Stores the value 18 in a variable"},
                {"line": 2, "text": "The if statement ends with a colon"},
                {"line": 3, "text": "Indented block: runs only when age is 18 or more"},
                {"line": 4, "text": "Back at the outer level: always runs"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "if age >= 18\n    print('vote')",
                "fixed": "if age >= 18:\n    print('vote')",
                "why": "The colon at the end of the if line is required to open the block.",
            },
            {
                "wrong": "if age >= 18:\n  print('a')\n    print('b')",
                "fixed": "if age >= 18:\n    print('a')\n    print('b')",
                "why": "All lines in one block must share the same indentation. Mixed widths raise an IndentationError.",
            },
            {
                "wrong": "if x:\n\tprint('tabbed')\n    print('spaces')",
                "fixed": "use four spaces consistently",
                "why": "Mixing tabs and spaces in one block raises a TabError or IndentationError in Python 3.",
            },
        ],
        exercise={
            "description": "Complete the if statement so that when age is 18 or more it prints You are an adult, and make sure the final print runs after the block no matter what.",
            "starter_code": (
                "age = 18\n"
                "if age >= 18:\n"
                "    # Your code here\n"
                "print('Program finished')"
            ),
            "hints": [
                "The if line already has its colon",
                "Your print must be indented by four spaces",
                "Leave the final print at the outermost level",
            ],
            "expected_output": "You are an adult\nProgram finished",
        },
        quiz={
            "question": "How does Python know which lines belong to an if block?",
            "options": [
                "They are inside curly braces",
                "They are wrapped in square brackets",
                "They share the same indentation level",
                "They end with a semicolon",
            ],
            "correct": 2,
            "explanation": "Python groups statements into a block purely by their indentation, so consistent indentation is required.",
        },
        key_takeaways=[
            "Indentation creates blocks in Python, not braces",
            "An if statement opens a block with a colon",
            "Use four spaces per indentation level consistently",
            "Dedenting back to the outer level ends the block",
        ],
        next_steps="Time to combine everything into your first real script!",
    ),
    _lesson(
        lesson_id="python-l01-07",
        theory=(
            "Now you will write a small script from scratch that uses variables and print(). "
            "A variable is a name that stores a value, and you create one with the = sign."
            "\n\n"
            "Scripts run from top to bottom, so define your variables before you use them. "
            "When you print a variable, Python prints the value stored inside it."
        ),
        analogy=(
            "A variable is like a labeled jar. "
            "You write a label (the variable name) and drop a value inside. "
            "Whenever you mention the label, Python hands you whatever is in the jar."
        ),
        sections=[
            {
                "heading": "Creating variables",
                "body": (
                    "Write name = 'Alex' to store the string 'Alex' in a variable called name. "
                    "Use = to assign, not ==, which compares. "
                    "Then name behaves exactly like the value it holds."
                ),
                "pro_tip": (
                    "Choose descriptive names: student_name says more than x. "
                    "Future you will thank present you."
                ),
            },
            {
                "heading": "Putting it together",
                "body": (
                    "A script is just statements in order: create variables, then print them. "
                    "print('Hi', name) prints Hi Alex, with the comma adding a space automatically."
                ),
                "pro_tip": (
                    "Run your script often, even mid-way through writing it. "
                    "Small steps make bugs easy to find."
                ),
            },
        ],
        code_example=_code(
            """name = 'Alex'
print('Hi', name)
print('Welcome to Python')""",
            [
                {"line": 1, "text": "Assigns the string 'Alex' to the variable name"},
                {"line": 2, "text": "Prints the greeting and the value of name"},
                {"line": 3, "text": "Prints a closing message"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "name == 'Alex'",
                "fixed": "name = 'Alex'",
                "why": "== compares two values, while = assigns a value to a name.",
            },
            {
                "wrong": "print('Hi', name) before assigning name",
                "fixed": "assign name first, then print it",
                "why": "Scripts run top to bottom. Using a variable before it exists raises NameError.",
            },
            {
                "wrong": "my name = 'Alex'",
                "fixed": "my_name = 'Alex'",
                "why": "Variable names cannot contain spaces. Use underscores to separate words.",
            },
        ],
        exercise={
            "description": "Ask yourself for your favourite colour, store the answer in a variable, then print Your favourite colour is followed by the value.",
            "starter_code": (
                "colour = input('Favourite colour: ')\n"
                "# Your code here"
            ),
            "hints": [
                "Reuse the colour variable in your print",
                "You can print a message and the variable in one call",
                "The comma between parts inserts a space",
            ],
            "expected_output": "Your favourite colour is <colour>",
        },
        quiz={
            "question": "What does the = sign do in Python?",
            "options": [
                "It compares two values for equality",
                "It stores the value on the right into the name on the left",
                "It adds two numbers together",
                "It prints the value",
            ],
            "correct": 1,
            "explanation": "The single = is the assignment operator. It binds a name to a value. == is the comparison operator.",
        },
        key_takeaways=[
            "Variables store values under a chosen name using =",
            "Scripts run from top to bottom",
            "Define variables before you use them",
            "Descriptive names make scripts self-documenting",
        ],
        next_steps="Let us turn up the fun with your first challenge: an ASCII art generator!",
    ),

    _lesson(
        lesson_id="python-l01-08",
        theory=(
            "An ASCII art generator draws pictures using only characters like stars, slashes, and letters. "
            "You create each line with a separate print() call."
            "\n\n"
            "The trick is careful spacing: every space inside the quotes is real output. "
            "By stacking aligned lines you can build trees, faces, animals, and more."
        ),
        analogy=(
            "Building ASCII art is like building with LEGO bricks. "
            "Each print() call is one row of bricks, and spacing decides how the rows line up "
            "into a recognisable shape."
        ),
        sections=[
            {
                "heading": "One print per line",
                "body": (
                    "Every line of your picture is one print() call. "
                    "print('  *  ') outputs two spaces, a star, and two spaces. "
                    "Counting the spaces carefully is what makes the picture line up."
                ),
                "pro_tip": (
                    "Copy the finished picture you want, then count characters column by column "
                    "to write each line accurately."
                ),
            },
            {
                "heading": "Designing a picture",
                "body": (
                    "Draw your picture on paper first. "
                    "Then convert each row into a string inside a print(). "
                    "Row by row, the picture takes shape."
                ),
                "pro_tip": (
                    "Start small: a triangle, a heart, or a rocket. "
                    "Perfect one tiny picture before attempting a huge one."
                ),
            },
        ],
        code_example=_code(
            """print('   *   ')
print('  ***  ')
print(' ***** ')
print('*******')
print('   |   ')""",
            [
                {"line": 1, "text": "Top of the tree: one star, centred"},
                {"line": 2, "text": "Second row widens the tree"},
                {"line": 3, "text": "Third row, still widening"},
                {"line": 4, "text": "The widest row forms the base"},
                {"line": 5, "text": "The trunk, centred under the tree"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "print('  *  ')'\nprint(' *** ')'",
                "fixed": "print('  *  ')\nprint(' *** ')",
                "why": "Two statements on the same line with no operator between them get glued into one string. Use separate lines.",
            },
            {
                "wrong": "print('  *') and print('  * ') producing different art",
                "fixed": "count trailing spaces too; they matter in ASCII art",
                "why": "Trailing spaces are part of the output string, and they keep columns aligned.",
            },
            {
                "wrong": "print(  *  )",
                "fixed": "print('  *  ')",
                "why": "The picture characters must be inside quotes. Unquoted stars are not valid Python.",
            },
        ],
        exercise={
            "description": "Build a snowman with four rows of print() calls: the head, an upper body, a lower body, and a base.",
            "starter_code": (
                "print('===')\n"
                "# Your code here"
            ),
            "hints": [
                "Use ( . ) for the head",
                "Use (   ) for the middle body",
                "End with a wide base like (___)",
            ],
            "expected_output": "===\n( . )\n(   )\n(___)",
        },
        quiz={
            "question": "Why does every row of an ASCII art picture need careful spacing?",
            "options": [
                "Because spaces are the only valid output",
                "Because spaces inside the quotes keep the columns aligned",
                "Because Python ignores spaces in print",
                "Because spaces are never allowed in strings",
            ],
            "correct": 1,
            "explanation": "Spaces are real characters in the string, and matching column widths is what makes the rows form a picture.",
        },
        key_takeaways=[
            "Each row of ASCII art is one print() call",
            "Spaces inside quotes are part of the output",
            "Count columns carefully to keep rows aligned",
            "Design on paper first, then code row by row",
        ],
        next_steps="For your final Level 1 project, let us build an animated greeting card!",
    ),

    _lesson(
        lesson_id="python-l01-09",
        theory=(
            "Your first project combines print(), variables, and a little patience. "
            "The time module has a sleep() function that pauses your program for a given number of seconds."
            "\n\n"
            "By printing, pausing, and printing again, you create a simple animation: "
            "messages that appear one at a time like a slideshow greeting card."
        ),
        analogy=(
            "time.sleep() is like a stage director's pause button. "
            "Each print is an actor walking on stage, and the pause lets the audience "
            "appreciate the moment before the next one arrives."
        ),
        sections=[
            {
                "heading": "Importing time",
                "body": (
                    "The first line, import time, loads Python's time module so you can use it. "
                    "Then time.sleep(1) pauses the program for one second. "
                    "Modules let you reuse battle-tested code written by others."
                ),
                "pro_tip": (
                    "import must appear before you use the module. "
                    "Convention places all imports at the very top of the file."
                ),
            },
            {
                "heading": "Building the card",
                "body": (
                    "Print a title, pause, print a message, pause, then print the closing line. "
                    "The pauses turn three static messages into a timed sequence that feels animated."
                ),
                "pro_tip": (
                    "Adjust the sleep duration to tune the pacing. "
                    "Try 0.5 seconds for a snappier card."
                ),
            },
        ],
        code_example=_code(
            """import time
print('Happy Birthday!')
time.sleep(1)
print('May your day shine!')
time.sleep(1)
print('Have a great year ahead!')""",
            [
                {"line": 1, "text": "Imports the time module so we can pause"},
                {"line": 2, "text": "Prints the card title"},
                {"line": 3, "text": "Pauses the program for 1 second"},
                {"line": 4, "text": "Prints the middle message"},
                {"line": 5, "text": "Pauses again before the final line"},
                {"line": 6, "text": "Prints the closing message"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "print('Hi')\nsleep(1)",
                "fixed": "import time\nprint('Hi')\ntime.sleep(1)",
                "why": "sleep lives inside the time module, so you must import time and call time.sleep() with the module prefix.",
            },
            {
                "wrong": "time.sleep()  # forgot the seconds",
                "fixed": "time.sleep(1)",
                "why": "sleep requires an argument: the number of seconds to pause.",
            },
            {
                "wrong": "import time in the middle of the file",
                "fixed": "import time at the very top",
                "why": "Python style puts all imports at the top, before other code, so dependencies are obvious.",
            },
        ],
        exercise={
            "description": "Create a greeting card that prints a decorated title line, a middle wish, and a decorated bottom line, with the middle wish in its own print.",
            "starter_code": (
                "print('********************')\n"
                "print('* HAPPY BIRTHDAY *')\n"
                "# Your code here\n"
                "print('********************')"
            ),
            "hints": [
                "Add one more print() between the two given lines",
                "Keep the stars aligned with the border",
                "Your message can say anything kind",
            ],
            "expected_output": "********************\n* HAPPY BIRTHDAY *\n* Wishing you joy! *\n********************",
        },
        quiz={
            "question": "What does time.sleep(2) do?",
            "options": [
                "Prints the number 2",
                "Pauses the program for 2 seconds",
                "Ends the program after 2 lines",
                "Repeats the program twice",
            ],
            "correct": 1,
            "explanation": "time.sleep(n) suspends the program for n seconds, which you can use to pace animations and messages.",
        },
        key_takeaways=[
            "import time loads the time module",
            "time.sleep(seconds) pauses the program",
            "Printing then pausing creates a simple animation",
            "A card can be built from a title, message, and footer",
        ],
        next_steps="Level 1 complete! Level 2 introduces the data types that power real programs.",
    ),

    # =========================================================================
    # LEVEL 2: VARIABLES AND DATA TYPES
    # =========================================================================
    _lesson(
        lesson_id="python-l02-01",
        theory=(
            "Python has two built-in number types: int for whole numbers and float for decimals. "
            "An int like 42 has no decimal point, while a float like 3.14 always has one."
            "\n\n"
            "Most of the time you do not need to choose, because Python figures out the type. "
            "When you divide two ints with /, the result is always a float."
        ),
        analogy=(
            "Think of int as counting whole cookies and float as measuring flour. "
            "You would never say you have 2.5 cookies, but you might absolutely use 2.5 cups of flour."
        ),
        sections=[
            {
                "heading": "int: whole numbers",
                "body": (
                    "int values can be positive, negative, or zero: 7, -3, 0. "
                    "They are exact and fast. Use them for counting, indexes, and quantities."
                ),
                "pro_tip": (
                    "int arithmetic is exact, so 10 // 3 gives exactly 3 with no rounding surprises."
                ),
            },
            {
                "heading": "float: decimal numbers",
                "body": (
                    "float values carry a decimal point: 2.5, -0.75, 1.0. "
                    "They are needed for measurements, money, and averages. "
                    "Beware that floats are stored in binary, so some decimals are tiny approximations."
                ),
                "pro_tip": (
                    "round(0.1 + 0.2, 2) gives 0.3 for display, hiding the tiny binary rounding error."
                ),
            },
        ],
        code_example=_code(
            """apples = 10
price = 2.5
total = apples * price
print('Total cost:', total)""",
            [
                {"line": 1, "text": "An int: a whole number without a decimal point"},
                {"line": 2, "text": "A float: a number with a decimal point"},
                {"line": 3, "text": "Multiplying an int and a float gives a float"},
                {"line": 4, "text": "Prints Total cost: 25.0"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "1,000,000",
                "fixed": "1000000",
                "why": "Commas are not allowed inside numbers in Python. Write big numbers without separators.",
            },
            {
                "wrong": "total = '10' + 2.5",
                "fixed": "total = 10 + 2.5",
                "why": "Strings and numbers cannot be added. Convert with int() or float() first.",
            },
            {
                "wrong": "expecting 10 / 4 to give 2",
                "fixed": "10 / 4 gives 2.5 (a float)",
                "why": "True division always returns a float. Use // if you want the integer part.",
            },
        ],
        exercise={
            "description": "Multiply the apples variable by the price variable and print the result.",
            "starter_code": (
                "apples = 10\n"
                "price = 2.5\n"
                "# Your code here"
            ),
            "hints": [
                "Use the * operator to multiply",
                "Store the result in a variable like total",
                "Print the variable with print(total)",
            ],
            "expected_output": "25.0",
        },
        quiz={
            "question": "What type is the value 3.14 in Python?",
            "options": ["int", "float", "decimal", "double"],
            "correct": 1,
            "explanation": "Any number written with a decimal point is a float in Python, regardless of size.",
        },
        key_takeaways=[
            "int holds whole numbers; float holds decimals",
            "Dividing with / always returns a float",
            "Python usually infers the type for you",
            "round() helps present floats cleanly",
        ],
        next_steps="Numbers are just the start. Let us master the next type: strings.",
    ),
    _lesson(
        lesson_id="python-l02-02",
        theory=(
            "A string is a sequence of characters, like a word, a sentence, or an emoji. "
            "You create one by wrapping text in quotes, either 'single' or \"double\"."
            "\n\n"
            "The + operator joins (concatenates) two strings into one. "
            "The len() function returns how many characters a string contains, including spaces."
        ),
        analogy=(
            "A string is a chain of beads. Each bead is one character, and the chain holds them "
            "in exact order. Concatenation is clipping two chains together."
        ),
        sections=[
            {
                "heading": "Quoting strings",
                "body": (
                    "Both 'single' and \"double\" quotes work. "
                    "Single quotes are handy when your text contains double quotes, like 'He said \"hi\"'. "
                    "Just pick one style and stay consistent."
                ),
                "pro_tip": (
                    "Need quotes inside quotes? Use the opposite style for the outer pair and "
                    "you avoid all escaping."
                ),
            },
            {
                "heading": "Joining and measuring",
                "body": (
                    "'Hello' + ' ' + 'World' becomes 'Hello World'. "
                    "len('Hello') returns 5. "
                    "These two operations, joining and measuring, are the foundation of text processing."
                ),
                "pro_tip": (
                    "print(len('hi  there')) counts the space too, giving 8. "
                    "Spaces are characters just like letters."
                ),
            },
        ],
        code_example=_code(
            """greeting = 'Hello'
name = "World"
message = greeting + ', ' + name
print(message)
print(len(message))""",
            [
                {"line": 1, "text": "Single-quoted string assigned to greeting"},
                {"line": 2, "text": "Double-quoted string is also valid"},
                {"line": 3, "text": "+ concatenates the strings into one message"},
                {"line": 4, "text": "Prints Hello, World"},
                {"line": 5, "text": "len() prints the character count of the message"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "print('2' + 3)",
                "fixed": "print(int('2') + 3) or print('2' + str(3))",
                "why": "You cannot mix strings and numbers with +. Convert one side to match the other.",
            },
            {
                "wrong": "text = 'it is' 'fine'",
                "fixed": "text = 'it is' + 'fine'",
                "why": "Adjacent string literals are automatically joined, which is confusing. Use + to be explicit.",
            },
            {
                "wrong": "len('')  # expecting an error",
                "fixed": "len('') returns 0",
                "why": "An empty string has zero characters, so len('') is 0, not an error.",
            },
        ],
        exercise={
            "description": "Join the first, middle, and last name variables with spaces using +, store the result, and print the full name.",
            "starter_code": (
                "first = 'Rahul'\n"
                "middle = 'Kumar'\n"
                "last = 'Sharma'\n"
                "full = first + ' ' + middle + ' ' + last\n"
                "# Your code here"
            ),
            "hints": [
                "The full variable is already built for you",
                "Print it with print(full)",
                "You should see Rahul Kumar Sharma",
            ],
            "expected_output": "Rahul Kumar Sharma",
        },
        quiz={
            "question": "What does len('Python') return?",
            "options": ["5", "6", "7", "It raises an error"],
            "correct": 1,
            "explanation": "len() counts every character in the string, and 'Python' has exactly 6 letters.",
        },
        key_takeaways=[
            "Strings are sequences of characters wrapped in quotes",
            "Single and double quotes both create strings",
            "+ concatenates strings; len() measures them",
            "You cannot mix strings and numbers with +",
        ],
        next_steps="Now let us look at the on/off switch of programming: booleans.",
    ),

    _lesson(
        lesson_id="python-l02-03",
        theory=(
            "Booleans are Python's truth values: exactly True or False. "
            "They answer yes/no questions in your programs and drive every decision."
            "\n\n"
            "The keywords and, or, and not combine booleans. "
            "and is True only when both sides are True; or is True when at least one side is True; "
            "not flips a value."
        ),
        analogy=(
            "Booleans are like a light switch: only two states, on (True) or off (False). "
            "Logical operators are the wiring rules that decide whether the bulb gets power."
        ),
        sections=[
            {
                "heading": "True and False",
                "body": (
                    "True and False are the only boolean values, and they must be capitalized exactly. "
                    "Comparisons produce booleans: 5 > 3 is True, 5 < 3 is False. "
                    "You will store these in variables and use them in if statements."
                ),
                "pro_tip": (
                    "Booleans are really ints underneath: True == 1 and False == 0. "
                    "Knowing this explains some surprising behaviour."
                ),
            },
            {
                "heading": "Combining booleans",
                "body": (
                    "is_logged_in and has_paid is True only if the user did both. "
                    "is_weekend or is_holiday is True if either is true. "
                    "not can_enter flips it to the opposite value."
                ),
                "pro_tip": (
                    "Name boolean variables with is_ or has_ prefixes: is_ready, has_access. "
                    "The name already reads like a yes/no question."
                ),
            },
        ],
        code_example=_code(
            """is_logged_in = True
has_paid = False
can_enter = is_logged_in and has_paid
print('Can enter:', can_enter)""",
            [
                {"line": 1, "text": "A True boolean stored in a variable"},
                {"line": 2, "text": "A False boolean stored in a variable"},
                {"line": 3, "text": "and requires both sides to be True, so this is False"},
                {"line": 4, "text": "Prints Can enter: False"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "is_ready = true",
                "fixed": "is_ready = True",
                "why": "Python's boolean keywords are capitalized: True and False. Lowercase true is a NameError.",
            },
            {
                "wrong": "if x == True:",
                "fixed": "if x:",
                "why": "if already evaluates truthiness. Comparing to True explicitly is redundant and sometimes wrong.",
            },
            {
                "wrong": "value = 'true'  # a string",
                "fixed": "value = True  # a boolean",
                "why": "'true' in quotes is a string, not the boolean True. Booleans are written without quotes.",
            },
        ],
        exercise={
            "description": "Add an else block so that when is_weekend is True the script prints Time to relax!, and otherwise prints Time to work!.",
            "starter_code": (
                "is_weekend = True\n"
                "if is_weekend:\n"
                "    # Your code here\n"
                "else:\n"
                "    print('Time to work!')"
            ),
            "hints": [
                "The if block prints the relaxing message",
                "Indent your print by four spaces",
                "Leave the else block exactly as it is",
            ],
            "expected_output": "Time to relax!",
        },
        quiz={
            "question": "What is the result of True and False in Python?",
            "options": ["True", "False", "Neither; it is an error", "0"],
            "correct": 1,
            "explanation": "The and operator is True only when both operands are True, so True and False evaluates to False.",
        },
        key_takeaways=[
            "Booleans are exactly True or False",
            "Comparisons produce booleans",
            "and requires both; or needs at least one; not flips",
            "Name boolean variables with is_ or has_",
        ],
        next_steps="Now that values have types, let us learn how to name the variables that hold them.",
    ),

    _lesson(
        lesson_id="python-l02-04",
        theory=(
            "Variable names in Python must follow clear rules. "
            "They can contain letters, digits, and underscores, but cannot start with a digit and "
            "cannot contain spaces or most symbols."
            "\n\n"
            "Names are case-sensitive: score and Score are different variables. "
            "Python's convention for multi-word names is snake_case: total_score, not totalScore."
        ),
        analogy=(
            "Variable naming is like labelling files on a shared computer. "
            "The label must be valid, unique, and descriptive enough that a stranger "
            "knows what is inside without opening it."
        ),
        sections=[
            {
                "heading": "The hard rules",
                "body": (
                    "A name cannot start with a number, so 2nd_name is invalid. "
                    "It cannot contain spaces or hyphens, so first name and first-name are invalid. "
                    "Underscores are the joiner: first_name is perfect."
                ),
                "pro_tip": (
                    "Do not name variables after Python keywords like if, for, or class. "
                    "Your editor will usually highlight them in a different colour."
                ),
            },
            {
                "heading": "The style rules",
                "body": (
                    "Use snake_case for variables and functions, and start names with a letter. "
                    "Names are case-sensitive, so use one consistent style everywhere "
                    "to avoid tracking down weird bugs."
                ),
                "pro_tip": (
                    "Aim for 3-4 descriptive words max: student_final_score is clear; "
                    "the_thing_that_we_use_for_the_final_score_of_the_student is not."
                ),
            },
        ],
        code_example=_code(
            """first_name = 'Amit'
age = 21
final_score = 88
print(first_name, age, final_score)""",
            [
                {"line": 1, "text": "snake_case name with two words joined by _"},
                {"line": 2, "text": "Short but perfectly clear name"},
                {"line": 3, "text": "Descriptive multi-word name"},
                {"line": 4, "text": "All three variables print with a space between them"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "1st_place = 'gold'",
                "fixed": "first_place = 'gold'",
                "why": "Names cannot start with a digit, so Python raises a SyntaxError.",
            },
            {
                "wrong": "final score = 88",
                "fixed": "final_score = 88",
                "why": "Spaces are not allowed inside names. Underscores are the correct word joiner.",
            },
            {
                "wrong": "Score = 10 and later score = 20",
                "fixed": "pick one casing and keep it",
                "why": "Python names are case-sensitive, so Score and score are two different variables.",
            },
        ],
        exercise={
            "description": "Create three variables about yourself: your name (string), your age (int), and a score out of 100 (int), all using snake_case, then print them together.",
            "starter_code": (
                "# Your code here"
            ),
            "hints": [
                "Use names like my_name, my_age, and my_score",
                "Strings go in quotes; numbers do not",
                "Print all three in one print() separated by commas",
            ],
            "expected_output": "<name> <age> <score>",
        },
        quiz={
            "question": "Which of these is a valid Python variable name?",
            "options": ["2nd_name", "first-name", "first_name", "first name"],
            "correct": 2,
            "explanation": "first_name uses letters and an underscore, does not start with a digit, and contains no spaces or hyphens.",
        },
        key_takeaways=[
            "Names use letters, digits, and underscores",
            "Names cannot start with a digit or contain spaces",
            "Python names are case-sensitive",
            "Use snake_case for multi-word variables",
        ],
        next_steps="Now let us see a shortcut for creating several variables at once.",
    ),

    _lesson(
        lesson_id="python-l02-05",
        theory=(
            "Multiple assignment lets you assign several variables in one line. "
            "Write a, b, c = 1, 2, 3 and Python pairs them up left to right."
            "\n\n"
            "Its most famous trick is swapping two variables: a, b = b, a. "
            "Python evaluates the right side first, then assigns, so no temporary variable is needed."
        ),
        analogy=(
            "Multiple assignment is like a synchronized juggling move. "
            "You throw all the values into the air at once, and Python catches each one "
            "in the matching hand."
        ),
        sections=[
            {
                "heading": "Assigning many at once",
                "body": (
                    "a, b, c = 1, 2, 3 gives a the value 1, b the value 2, and c the value 3. "
                    "The number of names on the left must match the number of values on the right, "
                    "or Python raises an error."
                ),
                "pro_tip": (
                    "You can unpack lists too: x, y = ['left', 'right'] works the same way."
                ),
            },
            {
                "heading": "The swap trick",
                "body": (
                    "a, b = b, a exchanges the values. "
                    "Other languages need a third temporary variable, but Python evaluates the "
                    "entire right side before assigning anything, making the swap a one-liner."
                ),
                "pro_tip": (
                    "The swap trick also works for three or more variables: "
                    "a, b, c = b, c, a rotates them."
                ),
            },
        ],
        code_example=_code(
            """a, b, c = 1, 2, 3
print(a, b, c)
a, b = b, a
print(a, b)""",
            [
                {"line": 1, "text": "Three values assigned to three names in one line"},
                {"line": 2, "text": "Prints 1 2 3"},
                {"line": 3, "text": "Swaps: a becomes 2 and b becomes 1"},
                {"line": 4, "text": "Prints 2 1"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "a, b, c = 1, 2",
                "fixed": "a, b, c = 1, 2, 3",
                "why": "The number of values must equal the number of variables, or Python raises a ValueError.",
            },
            {
                "wrong": "a = b = c = 10 uses the same object for a, b, and c",
                "fixed": "a, b, c = 10, 10, 10",
                "why": "For simple values both are fine, but chained assignment gives all names the very same object.",
            },
            {
                "wrong": "temp = x\nx = y\ny = temp  # works, but verbose",
                "fixed": "x, y = y, x",
                "why": "The temp-variable dance is valid but longer. Python's multiple assignment swaps in one readable line.",
            },
        ],
        exercise={
            "description": "Swap the variables x and y using a single multiple-assignment line, then print them so 10 appears before 5.",
            "starter_code": (
                "x = 5\n"
                "y = 10\n"
                "# Your code here\n"
                "print(x, y)"
            ),
            "hints": [
                "Use the pattern a, b = b, a",
                "No temporary variable is needed",
                "After the swap x should be 10",
            ],
            "expected_output": "10 5",
        },
        quiz={
            "question": "What does a, b = b, a do?",
            "options": [
                "Adds a and b together",
                "Swaps the values of a and b",
                "Erases both variables",
                "Makes a and b equal",
            ],
            "correct": 1,
            "explanation": "Python evaluates the right side (b, a) first, then assigns, which swaps the two values in place.",
        },
        key_takeaways=[
            "Assign many variables in one line with commas",
            "The number of names must match the number of values",
            "a, b = b, a swaps values without a temp variable",
            "The swap trick extends to rotating three values",
        ],
        next_steps="Now let us learn how to inspect what type a value really is.",
    ),

    _lesson(
        lesson_id="python-l02-06",
        theory=(
            "The type() function tells you the exact type of any value, like <class 'int'>. "
            "The isinstance() function answers a yes/no question: is this value that type?"
            "\n\n"
            "isinstance(value, type) is usually the better check because it returns a boolean "
            "you can use directly in an if statement."
        ),
        analogy=(
            "type() is like reading the badge on a person's uniform to see their exact role. "
            "isinstance() is a quicker check: are you a firefighter? "
            "Yes or no, no other details."
        ),
        sections=[
            {
                "heading": "Inspecting with type()",
                "body": (
                    "type(42) returns <class 'int'>, type('hi') returns <class 'str'>. "
                    "Seeing the class name in angle brackets is normal Python output. "
                    "It is a great debugging tool when a value is not what you expected."
                ),
                "pro_tip": (
                    "print(type(x)) is the fastest way to understand why a value "
                    "is behaving strangely."
                ),
            },
            {
                "heading": "Checking with isinstance()",
                "body": (
                    "isinstance(42, int) returns True and isinstance(42, float) returns False. "
                    "It is perfect for guarding code: if isinstance(amount, float): handle money. "
                    "It also accepts a tuple of types: isinstance(x, (int, float))."
                ),
                "pro_tip": (
                    "isinstance works with inheritance too, so a value passes the check "
                    "if it is an instance of the class or any of its subclasses."
                ),
            },
        ],
        code_example=_code(
            """value = 42
print(type(value))
print(isinstance(value, int))
print(isinstance(value, float))""",
            [
                {"line": 1, "text": "Stores an int in value"},
                {"line": 2, "text": "Prints <class 'int'>"},
                {"line": 3, "text": "True: 42 is an int"},
                {"line": 4, "text": "False: 42 is not a float"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "type(value) == 'int'",
                "fixed": "type(value) == int",
                "why": "type() returns the class int itself, not the string 'int'. Compare against the type, not its name.",
            },
            {
                "wrong": "isinstance('42', int)",
                "fixed": "isinstance(int('42'), int)",
                "why": "The string '42' is a str, not an int. Convert it first if you want a number.",
            },
            {
                "wrong": "using type() and comparing to <class 'int'> as text",
                "fixed": "use isinstance() for boolean checks",
                "why": "isinstance() returns True/False and reads cleaner inside if statements than type() comparisons.",
            },
        ],
        exercise={
            "description": "Read a number from the user, convert it to a float, and print its type.",
            "starter_code": (
                "num = input('Enter a number: ')\n"
                "# Your code here"
            ),
            "hints": [
                "Convert with float(num)",
                "Save the result into a new variable",
                "Print type() of the converted value",
            ],
            "expected_output": "<class 'float'>",
        },
        quiz={
            "question": "What does isinstance(3.5, int) return?",
            "options": ["True", "False", "3", "<class 'int'>"],
            "correct": 1,
            "explanation": "3.5 is a float, not an int, so isinstance() returns False.",
        },
        key_takeaways=[
            "type() returns the exact type of a value",
            "isinstance(value, type) returns a boolean",
            "isinstance() is the cleaner choice in if statements",
            "isinstance() accepts a tuple of types to check against",
        ],
        next_steps="Enough inspecting — let us make our programs interactive with input().",
    ),
    _lesson(
        lesson_id="python-l02-07",
        theory=(
            "The input() function lets a user type text into your program. "
            "It pauses execution, shows a prompt, and returns whatever was typed as a string."
            "\n\n"
            "Crucially, input() always returns a string, even if the user types a number. "
            "Use int() or float() to convert when you need a number."
        ),
        analogy=(
            "input() is like a restaurant order window. "
            "Your program calls out the prompt, waits for the customer, "
            "and receives an order slip. The slip is always paper text — "
            "you translate it if you need a number."
        ),
        sections=[
            {
                "heading": "How input() works",
                "body": (
                    "name = input('What is your name? ') stores the typed answer in name. "
                    "The program waits until the user presses Enter. "
                    "The prompt is printed with no newline, so the cursor sits right after the question."
                ),
                "pro_tip": (
                    "Put a space at the end of your prompt ('Name? ') so the user's "
                    "answer does not collide with the question."
                ),
            },
            {
                "heading": "Always a string",
                "body": (
                    "age = input('Age? ') gives a string like '21', not the number 21. "
                    "To do math you convert first: age = int(age) or int(input('Age? ')). "
                    "Forgetting this is the number one beginner bug."
                ),
                "pro_tip": (
                    "Use float(input(...)) when you expect a decimal like a price or a score."
                ),
            },
        ],
        code_example=_code(
            """name = input('What is your name? ')
print('Hello,', name)
age = input('How old are you? ')
print('You are', age, 'years old')""",
            [
                {"line": 1, "text": "Asks for the name and stores the typed answer"},
                {"line": 2, "text": "Greets the user using their name"},
                {"line": 3, "text": "Asks for age; this value is still a string"},
                {"line": 4, "text": "Prints the age as part of a sentence"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "age = input('Age: ')\nprint(age + 1)",
                "fixed": "age = int(input('Age: '))\nprint(age + 1)",
                "why": "input() returns a string, and '21' + 1 raises TypeError. Convert to int first.",
            },
            {
                "wrong": "input('Age? ') storing nothing",
                "fixed": "assign the result: age = input('Age? ')",
                "why": "Without an assignment the typed value is thrown away. Capture it in a variable.",
            },
            {
                "wrong": "int(input('Age: ')) when the user types 'twenty-one'",
                "fixed": "ask for digits, or handle the ValueError",
                "why": "int() raises ValueError on non-numeric text, so prompt users for numbers.",
            },
        ],
        exercise={
            "description": "Ask the user for their name and age with input(), then print a sentence in the format <name> is <age> years old.",
            "starter_code": (
                "name = input('Enter your name: ')\n"
                "age = input('Enter your age: ')\n"
                "# Your code here"
            ),
            "hints": [
                "Print all three pieces in one call: the name, 'is', the age",
                "Commas add spaces automatically",
                "Add 'years old' at the end",
            ],
            "expected_output": "<name> is <age> years old",
        },
        quiz={
            "question": "What type of value does input() always return?",
            "options": ["int", "float", "str", "It depends on what the user types"],
            "correct": 2,
            "explanation": "input() always returns a string. You must call int() or float() yourself to get a number.",
        },
        key_takeaways=[
            "input() pauses the program and reads a line of text",
            "The prompt is displayed without a newline",
            "input() always returns a string",
            "Convert with int() or float() before doing math",
        ],
        next_steps="Let us put input() to work with a classic: the Mad Libs generator!",
    ),

    _lesson(
        lesson_id="python-l02-08",
        theory=(
            "A Mad Libs generator collects words from the user and drops them into a story template. "
            "It is the perfect exercise for combining input() with print()."
            "\n\n"
            "The story stays the same, but the user's words make every run unique. "
            "Notice that the input values are strings, so they slot directly into the printed sentence."
        ),
        analogy=(
            "A Mad Libs story is a form with blank boxes. "
            "The user fills each box with a word, and you drop those slips into the printed story "
            "exactly where the blanks were."
        ),
        sections=[
            {
                "heading": "Collecting the words",
                "body": (
                    "Ask one question per blank with input(). "
                    "Store each answer in its own variable so you can place them anywhere in the story."
                ),
                "pro_tip": (
                    "Name the variables after the blank they fill: animal, place, colour — "
                    "then the story line reads almost like plain English."
                ),
            },
            {
                "heading": "Printing the story",
                "body": (
                    "Pass the collected variables to print() in the order the blanks appear. "
                    "The comma separator inserts spaces automatically, keeping the sentence readable."
                ),
                "pro_tip": (
                    "Try building longer stories once this works — four or five blanks "
                    "make a surprisingly funny paragraph."
                ),
            },
        ],
        code_example=_code(
            """adjective = input('Enter an adjective: ')
noun = input('Enter a noun: ')
print('The', adjective, noun, 'jumped over the moon.')""",
            [
                {"line": 1, "text": "Asks for one describing word"},
                {"line": 2, "text": "Asks for a person, place, or thing"},
                {"line": 3, "text": "Builds the story from the two user words"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "print('The' adjective noun 'jumped')",
                "fixed": "print('The', adjective, noun, 'jumped')",
                "why": "You need commas between each piece. Without them Python tries to join words into an invalid expression.",
            },
            {
                "wrong": "forgetting the space after 'The' inside quotes",
                "fixed": "use commas and let print add the spaces",
                "why": "Rely on print()'s automatic separator instead of hand-spacing words.",
            },
            {
                "wrong": "asking the same question twice",
                "fixed": "collect each blank exactly once",
                "why": "Repeated questions waste the user's time and can overwrite your variables.",
            },
        ],
        exercise={
            "description": "Build a three-blank Mad Libs: ask for an animal, a place, and a colour, then print the sentence The <colour> <animal> lives in <place>.",
            "starter_code": (
                "animal = input('Enter an animal: ')\n"
                "place = input('Enter a place: ')\n"
                "colour = input('Enter a colour: ')\n"
                "# Your code here"
            ),
            "hints": [
                "Use all three variables in one print()",
                "Keep the order: colour, animal, place",
                "Let commas add the spaces",
            ],
            "expected_output": "The <colour> <animal> lives in <place>",
        },
        quiz={
            "question": "Why do Mad Libs input values fit directly into a printed story?",
            "options": [
                "Because input() returns ints that print as words",
                "Because input() returns strings, and print can show strings",
                "Because Python auto-converts numbers to sentences",
                "Because print ignores strings",
            ],
            "correct": 1,
            "explanation": "input() returns a string, and print() displays strings directly, so the words drop straight into the story.",
        },
        key_takeaways=[
            "Collect one word per blank with input()",
            "Store each answer in its own variable",
            "Commas in print() add spaces between parts",
            "Every run creates a unique story from the same template",
        ],
        next_steps="Now let us level up with a challenge: a type converter!",
    ),

    _lesson(
        lesson_id="python-l02-09",
        theory=(
            "Type conversion (casting) changes a value from one type to another. "
            "int(x) converts to an integer, float(x) to a float, and str(x) to a string."
            "\n\n"
            "Conversions are only possible when the value makes sense: int('42') works, but "
            "int('hello') raises ValueError. Casting strings is how you use user input in math."
        ),
        analogy=(
            "Casting is like exchanging currency at an airport counter. "
            "You can convert a dollar bill to coins, but you cannot convert a restaurant menu "
            "into dollars. The counter only exchanges things that are genuinely money."
        ),
        sections=[
            {
                "heading": "The conversion functions",
                "body": (
                    "int('42') gives 42, float('3.14') gives 3.14, and str(42) gives '42'. "
                    "You can chain them: float(int('42')) turns the string into 42.0. "
                    "The result is a brand new value of the target type."
                ),
                "pro_tip": (
                    "float('3.14') then int() would fail on a decimal string. "
                    "Convert through the type that matches your string's format."
                ),
            },
            {
                "heading": "When conversions fail",
                "body": (
                    "int('abc') and float('12,5') both raise ValueError. "
                    "The value must already be in the target format. "
                    "Handling these errors gracefully is a skill you will learn soon."
                ),
                "pro_tip": (
                    "Use float() for user-entered prices; the input could contain a decimal point."
                ),
            },
        ],
        code_example=_code(
            """num_str = '42'
num_int = int(num_str)
num_float = float(num_int)
print(num_int, type(num_int))
print(num_float, type(num_float))""",
            [
                {"line": 1, "text": "A string that happens to contain digits"},
                {"line": 2, "text": "Converts the string to the int 42"},
                {"line": 3, "text": "Converts the int 42 to the float 42.0"},
                {"line": 4, "text": "Prints 42 <class 'int'>"},
                {"line": 5, "text": "Prints 42.0 <class 'float'>"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "int('3.14')",
                "fixed": "float('3.14') or int(float('3.14'))",
                "why": "int() cannot parse a string with a decimal point. Parse it as float first.",
            },
            {
                "wrong": "value = int('4.7') expecting 4",
                "fixed": "value = int(float('4.7'))",
                "why": "int() truncates floats but refuses decimal-point strings. Convert to float before truncating.",
            },
            {
                "wrong": "int('42')  # but user typed 'forty-two'",
                "fixed": "prompt for numeric input and handle ValueError",
                "why": "Words cannot be cast to numbers. Conversion only works when the string looks like a number.",
            },
        ],
        exercise={
            "description": "Convert the string '3.14' to a float, add 1.86 to it, and print the result rounded to two decimal places.",
            "starter_code": (
                "pi_str = '3.14'\n"
                "# Your code here"
            ),
            "hints": [
                "Use float(pi_str) to cast the string",
                "Add 1.86 to the converted value",
                "Wrap the result with round(value, 2) before printing",
            ],
            "expected_output": "5.0",
        },
        quiz={
            "question": "Which conversion turns the string '99' into a number you can do math with?",
            "options": ["str('99')", "int('99')", "float('99') and int('99') both work", "None of them"],
            "correct": 2,
            "explanation": "Both int('99') and float('99') succeed because '99' is a well-formed numeric string; pick whichever type you need.",
        },
        key_takeaways=[
            "int(), float(), and str() cast between the basic types",
            "Conversions only work when the value's format fits",
            "int('3.14') fails, but float('3.14') succeeds",
            "Casting input strings is required before math",
        ],
        next_steps="Time for the Level 2 project: a universal unit converter!",
    ),

    _lesson(
        lesson_id="python-l02-10",
        theory=(
            "Your unit converter project combines input(), casting, arithmetic, and f-strings. "
            "f-strings let you insert values directly into text with curly braces: "
            "f'{meters} meters' prints the value of meters inside the message."
            "\n\n"
            "The pattern for every conversion is the same: get a number, multiply or divide by "
            "the conversion factor, and print the result with a friendly message."
        ),
        analogy=(
            "A unit converter is a menu of currency and measurement exchanges. "
            "Every row on the menu has one rule — the exchange rate — and the customer "
            "tells you how much they have. You apply the rate and tell them what they get."
        ),
        sections=[
            {
                "heading": "f-strings make messages easy",
                "body": (
                    "Inside an f-string, place {variable} wherever you want its value: "
                    "f'{meters} m = {km} km' becomes '5.0 m = 0.005 km'. "
                    "You can even write expressions inside the braces."
                ),
                "pro_tip": (
                    "Use format specifiers to control decimals: f'{km:.3f}' prints "
                    "three digits after the point."
                ),
            },
            {
                "heading": "The conversion pattern",
                "body": (
                    "Read a value as a number, compute the target unit with one line of arithmetic, "
                    "then print it. To convert meters to kilometres you divide by 1000; "
                    "to convert to centimetres you multiply by 100."
                ),
                "pro_tip": (
                    "Test each conversion in isolation with a known value first. "
                    "If 1000 meters is not 1 km, you will catch it instantly."
                ),
            },
        ],
        code_example=_code(
            """meters = float(input('Enter meters: '))
km = meters / 1000
cm = meters * 100
print(f'{meters} m = {km} km')
print(f'{meters} m = {cm} cm')""",
            [
                {"line": 1, "text": "Reads a number as a float, not a string"},
                {"line": 2, "text": "Divides by 1000 to convert to kilometres"},
                {"line": 3, "text": "Multiplies by 100 to convert to centimetres"},
                {"line": 4, "text": "f-string inserts the two values into the message"},
                {"line": 5, "text": "Second f-string prints the centimetre result"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "meters = input('Enter meters: ') then meters / 1000",
                "fixed": "meters = float(input('Enter meters: '))",
                "why": "input() returns a string; dividing it raises TypeError. Cast with float() immediately.",
            },
            {
                "wrong": "print('{meters} m = {km} km')  # no f",
                "fixed": "print(f'{meters} m = {km} km')",
                "why": "Without the f prefix, the braces print literally instead of showing values.",
            },
            {
                "wrong": "mixing up divide and multiply factors",
                "fixed": "check the direction: to km you divide, to cm you multiply",
                "why": "Getting the factor backwards silently multiplies the value 1000-fold instead of the reverse.",
            },
        ],
        exercise={
            "description": "Write a feet-to-inches converter. Read feet as a float, convert using 1 foot = 12 inches, and print <feet> feet = <inches> inches.",
            "starter_code": (
                "feet = float(input('Enter feet: '))\n"
                "# Your code here"
            ),
            "hints": [
                "Multiply feet by 12 to get inches",
                "Store the result in a variable",
                "Use an f-string for the output message",
            ],
            "expected_output": "<feet> feet = <inches> inches",
        },
        quiz={
            "question": "What does f'{km} km' do in an f-string?",
            "options": [
                "Prints the literal text {km} km",
                "Inserts the value of the km variable into the message",
                "Deletes the km variable",
                "Converts km to a number",
            ],
            "correct": 1,
            "explanation": "In an f-string, {km} is replaced by the current value of the variable km when the string is built.",
        },
        key_takeaways=[
            "f-strings insert variable values with {curly_braces}",
            "Cast input() results with float() before math",
            "Every conversion is multiply or divide by a factor",
            "Test with a known value to verify a converter",
        ],
        next_steps="Level 2 done! Level 3 dives into operators and builds real-world calculators.",
    ),

    # =========================================================================
    # LEVEL 3: OPERATORS AND LOGIC
    # =========================================================================
    _lesson(
        lesson_id="python-l03-01",
        theory=(
            "Arithmetic operators perform math on numbers. "
            "Python has + for addition, - for subtraction, * for multiplication, and / for division."
            "\n\n"
            "Three special operators go further: // is floor division (integer part), "
            "% is the modulo (remainder), and ** is exponentiation (power). "
            "They turn simple arithmetic into real problem-solving tools."
        ),
        analogy=(
            "// is like how many full buses fit your whole school, and % is how many students "
            "are left standing. The bus problem is a package deal: both answers together "
            "describe the trip completely."
        ),
        sections=[
            {
                "heading": "The basics",
                "body": (
                    "10 + 3 is 13, 10 - 3 is 7, 10 * 3 is 30, and 10 / 3 is 3.333... "
                    "Division always returns a float. "
                    "Everything else follows the normal rules you learned in school."
                ),
                "pro_tip": (
                    "Use parentheses to make complex formulas readable: "
                    "(a + b) * c beats a + b * c in clarity every time."
                ),
            },
            {
                "heading": "Floor, modulo, and power",
                "body": (
                    "10 // 3 is 3 (whole times 3 fits), 10 % 3 is 1 (what remains), "
                    "and 2 ** 3 is 8 (2 to the power of 3). "
                    "The modulo is the trickiest; remember it is always the remainder."
                ),
                "pro_tip": (
                    "The modulo is how you check divisibility: x % 2 == 0 means x is even."
                ),
            },
        ],
        code_example=_code(
            """a = 10
b = 3
print(a + b)
print(a - b)
print(a * b)
print(a / b)
print(a // b)
print(a % b)
print(a ** b)""",
            [
                {"line": 1, "text": "First operand"},
                {"line": 2, "text": "Second operand"},
                {"line": 3, "text": "Addition: 13"},
                {"line": 4, "text": "Subtraction: 7"},
                {"line": 5, "text": "Multiplication: 30"},
                {"line": 6, "text": "Division: 3.3333333333333335"},
                {"line": 7, "text": "Floor division: 3 (whole times 3 fits in 10)"},
                {"line": 8, "text": "Modulo: 1 (the remainder)"},
                {"line": 9, "text": "Power: 10 ** 3 is 1000"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "10 / 3  expecting exactly 3",
                "fixed": "use 10 // 3 for the integer part",
                "why": "The single / always performs true division and returns a float.",
            },
            {
                "wrong": "confusing % with percent",
                "fixed": "% is the modulo remainder operator",
                "why": "10 % 3 gives 1, not 0.1. Percentage math needs explicit multiplication like 0.1 * amount.",
            },
            {
                "wrong": "2 ** 3 expecting 6",
                "fixed": "2 ** 3 is 8",
                "why": "** is exponentiation, not repeated multiplication by the number of digits.",
            },
        ],
        exercise={
            "description": "Using // and %, find how many full groups of 7 fit into 100 and how many items remain, then print both.",
            "starter_code": (
                "total = 100\n"
                "group = 7\n"
                "# Your code here"
            ),
            "hints": [
                "Use total // group for the number of full groups",
                "Use total % group for the remainder",
                "Print the results labelled 'Groups:' and 'Remainder:'",
            ],
            "expected_output": "Groups: 14\nRemainder: 2",
        },
        quiz={
            "question": "What does 17 % 5 evaluate to?",
            "options": ["3", "3.4", "2", "4"],
            "correct": 2,
            "explanation": "17 // 5 is 3, and 3 * 5 is 15. The remainder is 17 - 15 = 2, so 17 % 5 is 2.",
        },
        key_takeaways=[
            "+ - * / cover basic arithmetic",
            "/ always returns a float",
            "// gives the integer part; % gives the remainder",
            "** computes powers",
        ],
        next_steps="Now let us compare values and make decisions with comparison operators.",
    ),
    _lesson(
        lesson_id="python-l03-02",
        theory=(
            "Comparison operators ask true/false questions about values. "
            "They always produce a boolean: True or False."
            "\n\n"
            "Python has == (equal), != (not equal), < (less than), > (greater than), "
            "<= (less than or equal), and >= (greater than or equal). "
            "These are the questions your if statements ask."
        ),
        analogy=(
            "Comparison operators are the judges at a weighing scale competition. "
            "Each contestant walks up, the scale compares them, and the judge rules "
            "only one verdict: true or false. There is no 'maybe'."
        ),
        sections=[
            {
                "heading": "Comparing numbers",
                "body": (
                    "10 == 10 is True, 10 != 10 is False, and 10 > 9 is True. "
                    "You can compare any numbers, including floats: 2.5 >= 2.0 is True. "
                    "Chained comparisons like 0 < x < 100 also work in Python."
                ),
                "pro_tip": (
                    "The == checks equality. The single = assigns. "
                    "Mixing them up is the most famous bug in all of programming."
                ),
            },
            {
                "heading": "Comparing strings",
                "body": (
                    "'apple' == 'apple' is True, but 'Apple' == 'apple' is False. "
                    "Strings compare character by character and are case-sensitive. "
                    "Alphabetical ordering uses < and >."
                ),
                "pro_tip": (
                    "Compare strings case-insensitively with .lower(): "
                    "'Apple'.lower() == 'apple'.lower() is True."
                ),
            },
        ],
        code_example=_code(
            """a = 10
b = 20
print(a == b)
print(a != b)
print(a < b)
print(a >= 10)""",
            [
                {"line": 1, "text": "Stores 10"},
                {"line": 2, "text": "Stores 20"},
                {"line": 3, "text": "Equal? False"},
                {"line": 4, "text": "Not equal? True"},
                {"line": 5, "text": "Less than? True"},
                {"line": 6, "text": "Greater than or equal to 10? True"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "if score = 40:",
                "fixed": "if score == 40:",
                "why": "= assigns, == compares. Using = inside if raises a SyntaxError in Python.",
            },
            {
                "wrong": "'A' > 'a'",
                "fixed": "compare via .lower() or remember uppercase sorts first",
                "why": "Strings compare by character codes, and uppercase letters come before lowercase.",
            },
            {
                "wrong": "3 < x < 1  in a meaningless range",
                "fixed": "check the range logic before chaining",
                "why": "Chained comparisons evaluate left to right; a range with no overlap is just always False.",
            },
        ],
        exercise={
            "description": "Read a score as a float and print Passed when it is 40 or more, otherwise print Failed.",
            "starter_code": (
                "score = float(input('Enter score: '))\n"
                "# Your code here"
            ),
            "hints": [
                "Use if score >= 40:",
                "Indent the Passed print inside the if",
                "Add an else branch for the Failed case",
            ],
            "expected_output": "Passed",
        },
        quiz={
            "question": "What is the result of 'cat' == 'Cat'?",
            "options": ["True", "False", "It raises an error", "cat"],
            "correct": 1,
            "explanation": "String comparison is case-sensitive, so 'cat' and 'Cat' differ at the first character.",
        },
        key_takeaways=[
            "Comparison operators return True or False",
            "== checks equality; = assigns",
            "String comparison is case-sensitive",
            "Chained comparisons like 0 < x < 100 are valid",
        ],
        next_steps="Let us combine those true/false answers with logical operators.",
    ),

    _lesson(
        lesson_id="python-l03-03",
        theory=(
            "Logical operators combine boolean values into new booleans. "
            "and is True only if both sides are True. or is True if at least one side is True. "
            "not flips a single value to its opposite."
            "\n\n"
            "Python also supports truthiness: non-boolean values count as True or False "
            "when used in conditions. Zero, empty strings, and empty lists are falsy; "
            "everything else is truthy."
        ),
        analogy=(
            "and is like a two-key safe that needs both keys. or is like a spare key "
            "under the mat — either key opens the door. not is like a 'do not enter' "
            "sign that simply inverts the instruction."
        ),
        sections=[
            {
                "heading": "and and or in decisions",
                "body": (
                    "age >= 18 and has_license lets someone drive only if both hold. "
                    "is_weekend or is_holiday lets you relax on either kind of day. "
                    "Combine several conditions to express real rules."
                ),
                "pro_tip": (
                    "Read conditions aloud: 'if age is at least 18 AND has license'. "
                    "If the English needs an and/or, so does the code."
                ),
            },
            {
                "heading": "not and truthiness",
                "body": (
                    "not True is False and not False is True. "
                    "In conditions, not can_reach_floor reads more naturally as a check. "
                    "And remember, if name: is True for any non-empty string."
                ),
                "pro_tip": (
                    "Use if not x: instead of if x == False: — "
                    "it is shorter and handles all falsy values correctly."
                ),
            },
        ],
        code_example=_code(
            """age = 25
has_license = True
can_drive = age >= 18 and has_license
print('Can drive:', can_drive)
print(not can_drive)""",
            [
                {"line": 1, "text": "A 25-year-old driver"},
                {"line": 2, "text": "Holds a licence"},
                {"line": 3, "text": "and: both conditions must hold, so True"},
                {"line": 4, "text": "Prints Can drive: True"},
                {"line": 5, "text": "not flips it to False"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "age > 18 or age == 18",
                "fixed": "age >= 18",
                "why": ">= already means 'greater than or equal to'. The or version is verbose and easy to misread.",
            },
            {
                "wrong": "if not name == '':",
                "fixed": "if name:",
                "why": "Empty strings are falsy, so if name: already means 'name is not empty'.",
            },
            {
                "wrong": "using && and || symbols",
                "fixed": "use the keywords and and or",
                "why": "Python has no && or || symbols; the words and and or are the operators.",
            },
        ],
        exercise={
            "description": "Read an integer and print In range when it is between 10 and 20 inclusive, otherwise print Out of range.",
            "starter_code": (
                "num = int(input('Enter a number: '))\n"
                "# Your code here"
            ),
            "hints": [
                "Combine num >= 10 and num <= 20 with and",
                "Put that whole condition after if",
                "Print Out of range in the else branch",
            ],
            "expected_output": "In range",
        },
        quiz={
            "question": "What does not (True or False) evaluate to?",
            "options": ["True", "False", "It is an error", "None"],
            "correct": 1,
            "explanation": "True or False is True, and not True flips it to False.",
        },
        key_takeaways=[
            "and is True only when both sides are True",
            "or is True when at least one side is True",
            "not flips a boolean value",
            "Zero, empty strings, and empty lists are falsy",
        ],
        next_steps="Now let us make shorter code with assignment operators.",
    ),

    _lesson(
        lesson_id="python-l03-04",
        theory=(
            "Assignment operators combine an operation with assignment. "
            "Instead of x = x + 5 you can write x += 5."
            "\n\n"
            "Every arithmetic operator has one: +=, -=, *=, /=, //=, %=, and **=. "
            "They always update the variable in place using its own current value."
        ),
        analogy=(
            "Assignment operators are like a bank balance that updates automatically. "
            "You do not compute the new balance yourself; you just say 'add 500' "
            "and the bank updates your running total."
        ),
        sections=[
            {
                "heading": "The shorthand pattern",
                "body": (
                    "score += 5 adds 5 to score's current value and stores it back. "
                    "It is exactly the same as score = score + 5, just shorter. "
                    "The compound operator is the standard style in real code."
                ),
                "pro_tip": (
                    "Compound operators never insert themselves into nearby variables: "
                    "a += b changes only a."
                ),
            },
            {
                "heading": "All the variants",
                "body": (
                    "total -= discount, price *= 2, energy //= 2, and so on. "
                    "String += also works: message += '!' appends text. "
                    "The operator reads naturally: 'add equals', 'subtract equals'."
                ),
                "pro_tip": (
                    "Read x += 1 aloud as 'x gets x plus 1' to keep the "
                    "update-in-place meaning fresh."
                ),
            },
        ],
        code_example=_code(
            """score = 10
score += 5
score *= 2
score -= 3
print('Final score:', score)""",
            [
                {"line": 1, "text": "Starts at 10"},
                {"line": 2, "text": "score becomes 15"},
                {"line": 3, "text": "score becomes 30"},
                {"line": 4, "text": "score becomes 27"},
                {"line": 5, "text": "Prints Final score: 27"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "x += 5  when x was never defined",
                "fixed": "x = 10 first, then x += 5",
                "why": "Compound operators read the current value, so the variable must already exist or you get NameError.",
            },
            {
                "wrong": "x =+ 5",
                "fixed": "x += 5",
                "why": "=+ is parsed as x = +5, assigning positive 5 instead of incrementing.",
            },
            {
                "wrong": "x += 1 and y += 1 written as x += y += 1",
                "fixed": "write two separate statements",
                "why": "Compound assignments are statements, not expressions, and cannot be chained.",
            },
        ],
        exercise={
            "description": "Starting from points = 50, use +=, *=, and -= to reach exactly 75, then print the final value.",
            "starter_code": (
                "points = 50\n"
                "# Your code here\n"
                "print('Final points:', points)"
            ),
            "hints": [
                "Try points += 25, then points *= 2, then points -= 25",
                "Use a different compound operator each time",
                "Verify the final value equals 75",
            ],
            "expected_output": "Final points: 75",
        },
        quiz={
            "question": "What does total -= 10 do?",
            "options": [
                "Sets total to 10",
                "Subtracts 10 from total and stores the result back",
                "Makes total negative",
                "Removes the total variable",
            ],
            "correct": 1,
            "explanation": "total -= 10 is shorthand for total = total - 10: it updates total using its current value.",
        },
        key_takeaways=[
            "Compound operators combine math with assignment",
            "x += 5 means x = x + 5",
            "Every arithmetic operator has a compound form",
            "The variable must already exist before += works",
        ],
        next_steps="Now let us check whether things are the same object or just similar — identity and membership.",
    ),

    _lesson(
        lesson_id="python-l03-05",
        theory=(
            "Identity operators compare whether two things are the exact same object in memory. "
            "The operator is is, and its negation is is not."
            "\n\n"
            "Membership operators check whether a value appears inside a collection. "
            "The operator is in, and its negation is not in. "
            "Use these to test for presence inside lists, strings, and other containers."
        ),
        analogy=(
            "is is like comparing two ID cards: do they point to the same person? "
            "in is like checking a guest list: is this name on the list at all? "
            "Two people with the same name are still different people (== True, is False)."
        ),
        sections=[
            {
                "heading": "Identity with is",
                "body": (
                    "a is b is True only when a and b reference the exact same object. "
                    "For most values, use == to compare contents and reserve is for "
                    "comparing against singletons like None."
                ),
                "pro_tip": (
                    "The classic correct use is if result is None: — "
                    "None is a singleton, so identity is the right check."
                ),
            },
            {
                "heading": "Membership with in",
                "body": (
                    "'apple' in ['apple', 'banana'] is True. "
                    "'py' in 'python' is True because substrings count. "
                    "not in is the opposite: 'grape' not in fruits is True when grape is absent."
                ),
                "pro_tip": (
                    "Membership in a set or dict is extremely fast; "
                    "use them when you check membership in a loop."
                ),
            },
        ],
        code_example=_code(
            """fruits = ['apple', 'banana', 'cherry']
print('apple' in fruits)
print('grape' not in fruits)
a = [1, 2, 3]
b = a
print(a is b)""",
            [
                {"line": 1, "text": "A list holding three fruit strings"},
                {"line": 2, "text": "True: 'apple' is in the list"},
                {"line": 3, "text": "True: 'grape' is not in the list"},
                {"line": 4, "text": "Creates a fresh list object"},
                {"line": 5, "text": "b points to the same list object as a"},
                {"line": 6, "text": "True: a and b reference the exact same object"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "if x == None:",
                "fixed": "if x is None:",
                "why": "None is a singleton, and identity (is) is the idiomatic and safer check.",
            },
            {
                "wrong": "'app' in ['apple', 'banana']",
                "fixed": "check the substring with 'app' in 'apple' or iterate the list",
                "why": "in on a list checks whole items, not substrings. Substrings only match inside strings.",
            },
            {
                "wrong": "using == where object identity matters",
                "fixed": "understand: == compares contents, is compares identity",
                "why": "Two equal-but-separate objects make == True and is False. Choose based on what you need.",
            },
        ],
        exercise={
            "description": "Check whether the string 'python' appears in the languages list, then print the result.",
            "starter_code": (
                "languages = ['python', 'java', 'c++']\n"
                "# Your code here"
            ),
            "hints": [
                "Use the in operator on the list",
                "Store the boolean in a variable",
                "Print the variable with print()",
            ],
            "expected_output": "True",
        },
        quiz={
            "question": "What is the result of 'apple' in ['banana', 'cherry']?",
            "options": ["True", "False", "It raises an error", "'apple'"],
            "correct": 1,
            "explanation": "'apple' is not one of the list items, so the membership check returns False.",
        },
        key_takeaways=[
            "is compares object identity; == compares contents",
            "Use is to check against None",
            "in tests whether a value appears in a collection",
            "Substring checks work on strings, not list items",
        ],
        next_steps="Now let us understand the order in which Python evaluates mixed expressions.",
    ),

    _lesson(
        lesson_id="python-l03-06",
        theory=(
            "Operator precedence decides the order in which operations run in an expression. "
            "Multiplication and division happen before addition and subtraction, "
            "just like in school math."
            "\n\n"
            "Parentheses always beat precedence: (2 + 3) * 4 forces the addition first. "
            "When in doubt, use parentheses — they make your intent crystal clear."
        ),
        analogy=(
            "Precedence is the order of operations in a kitchen. "
            "The head chef (exponents) works first, then sous-chefs (multiply and divide), "
            "and the commis (add and subtract) plate up last. Parentheses are your "
            "'do this first' sticky note."
        ),
        sections=[
            {
                "heading": "The pecking order",
                "body": (
                    "From strongest to weakest: **, then unary - and +, then * / // %, "
                    "then + and -. So 2 + 3 * 4 computes 3 * 4 first, giving 2 + 12 = 14. "
                    "Assignment happens last of all."
                ),
                "pro_tip": (
                    "Power binds tighter than the minus sign: -2 ** 2 is -4, not 4. "
                    "Write (-2) ** 2 if you mean the positive result."
                ),
            },
            {
                "heading": "Parentheses rule everything",
                "body": (
                    "Anything inside parentheses is evaluated first, innermost first. "
                    "(2 + 3) * 4 gives 20, while 2 + 3 * 4 gives 14. "
                    "Precedence prevents ambiguity, but parentheses prevent mistakes."
                ),
                "pro_tip": (
                    "In long expressions, add parentheses even when not required. "
                    "Future readers (including you) will thank you."
                ),
            },
        ],
        code_example=_code(
            """result = 2 + 3 * 4
print(result)
result2 = (2 + 3) * 4
print(result2)""",
            [
                {"line": 1, "text": "* runs first: 2 + 12 = 14"},
                {"line": 2, "text": "Prints 14"},
                {"line": 3, "text": "Parentheses force addition first: 5 * 4 = 20"},
                {"line": 4, "text": "Prints 20"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "result = 2 + 3 * 4  expecting 20",
                "fixed": "result = (2 + 3) * 4",
                "why": "Multiplication binds tighter than addition, so 2 + 3 * 4 is 14. Use parentheses to force the order.",
            },
            {
                "wrong": "2 ** 3 ** 2  assuming left to right",
                "fixed": "2 ** (3 ** 2) is 512",
                "why": "** is right-associative: it evaluates right to left, so 3 ** 2 happens first.",
            },
            {
                "wrong": "writing a == b and c == d without parentheses",
                "fixed": "(a == b) and (c == d)",
                "why": "Comparisons bind tighter than and, so both forms work, but explicit parentheses are easier to read.",
            },
        ],
        exercise={
            "description": "Compute the average of 10, 20, and 30 using parentheses so the sum happens before the division, and print the result.",
            "starter_code": (
                "a, b, c = 10, 20, 30\n"
                "# Your code here"
            ),
            "hints": [
                "Sum the three values inside parentheses",
                "Divide the sum by 3",
                "Print the result with print()",
            ],
            "expected_output": "20.0",
        },
        quiz={
            "question": "What does 2 + 3 * 4 evaluate to?",
            "options": ["20", "14", "24", "9"],
            "correct": 1,
            "explanation": "Multiplication binds tighter than addition, so the expression is 2 + (3 * 4) = 14.",
        },
        key_takeaways=[
            "Precedence sets the order of evaluation",
            "Multiply and divide run before add and subtract",
            "Parentheses always override precedence",
            "Add parentheses to make intent obvious",
        ],
        next_steps="Now let us put operators to work with a tip calculator practice.",
    ),
    _lesson(
        lesson_id="python-l03-07",
        theory=(
            "A tip calculator is the classic first real-world program: read a bill, compute the tip, "
            "and show the total. It combines input(), casting, arithmetic, and rounding."
            "\n\n"
            "To find the tip, multiply the bill by the tip percentage and divide by 100. "
            "The round(value, 2) function keeps money amounts to two decimal places."
        ),
        analogy=(
            "Calculating a tip is like splitting a taxi fare. "
            "You look at the meter (the bill), apply the agreed percentage, "
            "and settle the final amount. The calculator just never forgets the math."
        ),
        sections=[
            {
                "heading": "Reading money as a float",
                "body": (
                    "Bills and percentages can have decimals, so read them with float(input(...)). "
                    "Multiplying a bill by a percentage gives a float with many digits, "
                    "which is exactly why we round at the end."
                ),
                "pro_tip": (
                    "Ask for the percentage as a whole number (15) rather than a fraction (0.15). "
                    "Dividing by 100 keeps the math easy to follow."
                ),
            },
            {
                "heading": "Computing and rounding",
                "body": (
                    "tip = bill * tip_percent / 100 calculates the tip amount. "
                    "total = bill + tip adds it to the bill. "
                    "round(value, 2) formats both for display, like 25.5 becoming 25.5 and 25.55 staying 25.55."
                ),
                "pro_tip": (
                    "You can round inline inside the f-string: f'{tip:.2f}' "
                    "formats to exactly two decimals without a separate round() call."
                ),
            },
        ],
        code_example=_code(
            """bill = float(input('Enter bill amount: '))
tip_percent = float(input('Enter tip percent: '))
tip = bill * tip_percent / 100
total = bill + tip
print('Tip:', round(tip, 2))
print('Total:', round(total, 2))""",
            [
                {"line": 1, "text": "Reads the bill as a float"},
                {"line": 2, "text": "Reads the tip percentage as a float"},
                {"line": 3, "text": "tip = bill * percentage / 100"},
                {"line": 4, "text": "Total is the bill plus the tip"},
                {"line": 5, "text": "Prints the tip rounded to 2 decimals"},
                {"line": 6, "text": "Prints the total rounded to 2 decimals"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "bill = input('Bill: ') then bill * 0.15",
                "fixed": "bill = float(input('Bill: '))",
                "why": "input() returns a string; multiplying it by a float raises TypeError. Cast with float() first.",
            },
            {
                "wrong": "tip = bill * tip_percent  # forgot / 100",
                "fixed": "tip = bill * tip_percent / 100",
                "why": "A percentage like 15 means 15 per 100, so you must divide by 100 or the tip is 15x too big.",
            },
            {
                "wrong": "round(total, 2) then using the original unrounded total elsewhere",
                "fixed": "round at display time, keep the full precision for further math",
                "why": "round() only returns the rounded copy; the original variable keeps its full value.",
            },
        ],
        exercise={
            "description": "Write a program that splits a bill of 250 between 5 people and prints how much each person pays.",
            "starter_code": (
                "bill = 250\n"
                "people = 5\n"
                "# Your code here"
            ),
            "hints": [
                "Divide the bill by the number of people",
                "Store the share in a variable",
                "Print a message like 'Each person pays: <amount>'",
            ],
            "expected_output": "Each person pays: 50.0",
        },
        quiz={
            "question": "On a bill of 200 with a 10 percent tip, what is the total?",
            "options": ["210.0", "220.0", "200.1", "20.0"],
            "correct": 0,
            "explanation": "The tip is 200 * 10 / 100 = 20, and 200 + 20 = 210.0.",
        },
        key_takeaways=[
            "Read money values with float(input(...))",
            "tip = bill * percent / 100 computes the tip",
            "round(value, 2) keeps money display clean",
            "The pattern generalizes to any percentage problem",
        ],
        next_steps="Now let us bend our operator knowledge with the Expression Evaluator challenge!",
    ),

    _lesson(
        lesson_id="python-l03-08",
        theory=(
            "An expression evaluator is a program that computes a multi-operator expression "
            "and prints the result. The real skill is predicting the answer before it runs."
            "\n\n"
            "Apply precedence mentally: powers first, then multiply and divide, then add and subtract. "
            "Then use parentheses to change the order and compare the outcomes."
        ),
        analogy=(
            "Evaluating an expression is like reading a train timetable. "
            "Some trains (operators) leave before others according to the schedule (precedence). "
            "Parentheses are express trains that jump the queue."
        ),
        sections=[
            {
                "heading": "Predict before you run",
                "body": (
                    "Take 7 + 3 * 2 ** 2. The power runs first (4), then the multiplication (12), "
                    "then the addition (19). Cover the output with your hand, solve it, "
                    "then check the result. This habit builds real fluency."
                ),
                "pro_tip": (
                    "Say each step aloud: 'two squared is four, three times four is twelve, "
                    "seven plus twelve is nineteen'."
                ),
            },
            {
                "heading": "Changing order with parentheses",
                "body": (
                    "(7 + 3) * 2 ** 2 computes the sum first (10), then the power (4), "
                    "then multiplies to 40. Same numbers, different grouping, different answer. "
                    "The parentheses fully control the story."
                ),
                "pro_tip": (
                    "Write two versions of the same numbers with different groupings "
                    "to see exactly how precedence changes the result."
                ),
            },
        ],
        code_example=_code(
            """expr = 7 + 3 * 2 ** 2
print('Value:', expr)
expr2 = (7 + 3) * 2 ** 2
print('Value:', expr2)""",
            [
                {"line": 1, "text": "2 ** 2 = 4, then 3 * 4 = 12, then 7 + 12 = 19"},
                {"line": 2, "text": "Prints Value: 19"},
                {"line": 3, "text": "7 + 3 = 10 first, then 10 * 4 = 40"},
                {"line": 4, "text": "Prints Value: 40"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "7 + 3 * 2 ** 2  reading strictly left to right",
                "fixed": "apply precedence: **, then *, then +",
                "why": "Python does not read left to right. It follows precedence rules, giving 19, not 40 or 100.",
            },
            {
                "wrong": "unary minus with powers: -2 ** 2",
                "fixed": "(-2) ** 2 if you want 4; -2 ** 2 is -4",
                "why": "** binds tighter than the unary minus, so -2 ** 2 is -(2 ** 2) = -4.",
            },
            {
                "wrong": "assuming // and % share precedence with /",
                "fixed": "they do: * / // % all sit at the same level",
                "why": "When two operators share a level, left-to-right order applies, e.g. 8 // 2 * 2 is 8.",
            },
        ],
        exercise={
            "description": "Evaluate (5 + 3) * 2 ** 2 // 4 and print the result. Predict the answer in your head first.",
            "starter_code": (
                "result = (5 + 3) * 2 ** 2 // 4\n"
                "# Your code here"
            ),
            "hints": [
                "The parentheses give 8 first",
                "2 ** 2 is 4",
                "8 * 4 is 32, then 32 // 4 is 8",
            ],
            "expected_output": "8",
        },
        quiz={
            "question": "What is the value of 2 + 4 * 5?",
            "options": ["30", "22", "28", "24"],
            "correct": 1,
            "explanation": "Multiplication runs first: 4 * 5 = 20, then 2 + 20 = 22.",
        },
        key_takeaways=[
            "Predict the result before running code",
            "Powers bind tightest, then * / // %, then + -",
            "Parentheses override precedence completely",
            "Left-to-right applies between equal-precedence operators",
        ],
        next_steps="Final project time: a live currency converter that ties everything together!",
    ),

    _lesson(
        lesson_id="python-l03-09",
        theory=(
            "Your final Level 3 project is a live currency converter. "
            "It reads an exchange rate and an amount from the user, multiplies them, "
            "and prints the converted value with f-strings."
            "\n\n"
            "This project ties together everything from Levels 1-3: variables, input(), "
            "casting, arithmetic, precedence, and formatted output."
        ),
        analogy=(
            "A currency converter is a roadside exchange booth. "
            "The rate is posted on the board, the customer hands over their money, "
            "and the booth multiplies to hand back the equivalent amount. "
            "Your program is the booth."
        ),
        sections=[
            {
                "heading": "Reading the inputs",
                "body": (
                    "Read the rate and the amount as floats with float(input(...)). "
                    "The order matters: ask for the rate first, then the amount, "
                    "so the user knows what to type."
                ),
                "pro_tip": (
                    "Use float() for both, because exchange rates always carry decimals."
                ),
            },
            {
                "heading": "Converting and printing",
                "body": (
                    "converted = usd * rate multiplies the two floats. "
                    "The f-string f'{usd} USD = {inr} INR' formats a clear, labelled result. "
                    "You can round the display with {inr:.2f}."
                ),
                "pro_tip": (
                    "Label every number in the output — 'USD', 'INR', 'EUR'. "
                    "Unlabelled numbers confuse real users."
                ),
            },
        ],
        code_example=_code(
            """rate = float(input('Exchange rate (USD to INR): '))
usd = float(input('Amount in USD: '))
inr = usd * rate
print(f'{usd} USD = {inr} INR')""",
            [
                {"line": 1, "text": "Reads the exchange rate as a float"},
                {"line": 2, "text": "Reads the amount to convert"},
                {"line": 3, "text": "Multiplies to get the converted value"},
                {"line": 4, "text": "f-string prints a labelled result"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "usd = input('Amount: ') then usd * rate",
                "fixed": "usd = float(input('Amount: '))",
                "why": "input() returns a string, and multiplying a string raises TypeError. Cast both values with float().",
            },
            {
                "wrong": "reversing the rate and the amount",
                "fixed": "store each input in its own clearly named variable",
                "why": "Swapped inputs silently give a wildly wrong answer. Descriptive names prevent it.",
            },
            {
                "wrong": "print('{usd} USD = {inr} INR')  # missing f",
                "fixed": "print(f'{usd} USD = {inr} INR')",
                "why": "Without the f prefix, the braces and variable names print literally.",
            },
        ],
        exercise={
            "description": "Write a EUR to USD converter. Read the rate and the amount in euros as floats, convert, and print <euros> EUR = <usd> USD.",
            "starter_code": (
                "rate = float(input('EUR to USD rate: '))\n"
                "euros = float(input('Amount in EUR: '))\n"
                "# Your code here"
            ),
            "hints": [
                "Multiply euros by the rate",
                "Store the result in a variable like usd",
                "Use an f-string with labels for the output",
            ],
            "expected_output": "<euros> EUR = <usd> USD",
        },
        quiz={
            "question": "If the USD to INR rate is 83 and you convert 10 USD, how many INR do you get?",
            "options": ["8.3", "830", "0.83", "93"],
            "correct": 1,
            "explanation": "10 * 83 = 830, so 10 USD becomes 830 INR at that rate.",
        },
        key_takeaways=[
            "Converters follow one pattern: read, multiply or divide, print",
            "Read money values with float(input(...))",
            "f-strings with labels make output readable",
            "Level 3 complete: you now handle operators like a pro",
        ],
        next_steps="You have finished Levels 1-3! Your next stop is control flow: if, elif, and else.",
    ),
]))
