"""Lesson content service for the learning platform.

Hand-crafted content for C levels 1-3 (28 lessons) plus
template-based generation for levels 4-12.

Lesson ID format: {lang}-l{level:02d}-{lesson:02d}
Example: c-l01-01 = C, level 1, lesson 1
"""

from typing import Any
import re


HAND_CRAFTED_LESSONS: dict[str, dict[str, Any]] = {}


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


# ============================================================================
# LEVEL 1: FIRST STEPS
# ============================================================================

HAND_CRAFTED_LESSONS.update(dict([
    _lesson(
        lesson_id="c-l01-01",
        theory=(
            "C is a programming language created in the 1970s by Dennis Ritchie at Bell Labs. "
            "It is one of the oldest languages still in active use and it is the foundation that "
            "modern languages like Python, Java, and JavaScript are built on top of. Think of C as "
            "the grandparent of the coding world: old but incredibly powerful."
        ),
        analogy=(
            "Learning C is like learning to cook from scratch instead of using a microwave dinner. "
            "Cooking from scratch (C) teaches you how ingredients work, how heat affects food, "
            "and why certain techniques matter. Once you know how to cook from scratch, "
            "you can make anything."
        ),
        sections=[
            {
                "heading": "What makes C special?",
                "body": (
                    "Three things: speed, control, and portability. C code runs extremely fast because "
                    "it is compiled directly into machine instructions. You have precise control "
                    "over memory you decide when to allocate it and when to free it. And C code can run "
                    "on almost any device, from tiny microcontrollers to supercomputers."
                ),
                "pro_tip": (
                    "C is the language of choice for embedded systems (traffic lights, "
                    "elevators, car computers) because it is fast and uses very little memory."
                ),
            },
            {
                "heading": "Who uses C today?",
                "body": (
                    "C programmers work on operating systems, game engines, databases, compilers, "
                    "and robotics. Companies like Microsoft, Apple, Google, and Oracle all use C."
                ),
                "pro_tip": (
                    "Knowing C makes you a better programmer in every other language because "
                    "you understand memory, pointers, and how data actually flows through a computer."
                ),
            },
        ],
        key_takeaways=[
            "C is a powerful, low-level language that gives you control over hardware",
            "C is the foundation of most modern operating systems and languages",
            "C is fast because it is compiled directly to machine code",
            "Learning C teaches you how computers actually work",
        ],
        next_steps="Ready to write your first C program? Let us go to the next lesson!",
    ),

    _lesson(
        lesson_id="c-l01-02",
        theory=(
            "Time to write your first C program! The classic first program in any language is one "
            "that says Hello World on the screen. It is a tradition that goes back decades."
            "\n\n"
            "A C program has a specific structure. Every C program needs a function called main. "
            "Think of main as the starting line of a race when your program runs, the computer "
            "looks for main and starts executing the code inside it."
            "\n\n"
            "You will also see #include <stdio.h> at the top. This line tells the computer to include "
            "a library of input/output functions. stdio.h stands for standard input output header. "
            "Without it, you cannot use printf() to print things on the screen."
            "\n\n"
            "The return 0; at the end is like saying everything went fine, no errors here. "
            "When a program succeeds, it returns 0. If something went wrong, it might return 1."
        ),
        analogy=(
            "A C program is like a recipe. #include <stdio.h> is like gathering your ingredients "
            "and tools. int main() is the instruction to start cooking. The curly braces {} "
            "contain the actual steps. Each statement ends with a semicolon like a period "
            "at the end of a sentence. And return 0; is like saying the dish is ready, serve it!"
        ),
        sections=[
            {
                "heading": "The hello world program",
                "body": (
                    "Here is the complete program. Every single character matters C is very "
                    "particular about punctuation. Notice the semicolons, the parentheses, "
                    "and the curly braces. One missing character and the program will not compile."
                ),
                "code": (
                    '#include <stdio.h>\n'
                    '\n'
                    'int main() {\n'
                    '    printf("Hello, World!\\n");\n'
                    '    return 0;\n'
                    '}'
                ),
                "pro_tip": (
                    "The \\n inside the string is a newline character. It is like pressing "
                    "Enter on your keyboard it moves the cursor to the next line."
                ),
            },
            {
                "heading": "How to run this program",
                "body": (
                    "To run a C program, you need to compile it first. If you have GCC "
                    "installed, save the code in a file called hello.c and run:"
                ),
                "code": "gcc hello.c -o hello\n./hello",
                "pro_tip": (
                    "If you are on Windows, you might use hello.exe instead of ./hello."
                ),
            },
        ],
        code_example={
            "code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    printf("Hello, World!\\n");\n'
                '    return 0;\n'
                '}'
            ),
            "annotations": [
                {"line": 1, "text": "Includes the standard input/output library so you can use printf()"},
                {"line": 3, "text": "Declares the main function the entry point of every C program"},
                {"line": 4, "text": "Calls printf() to print text to the terminal; \\n adds a new line"},
                {"line": 5, "text": "Returns 0 to tell the OS the program finished successfully"},
            ],
        },
        common_mistakes=[
            {
                "mistake": "Forgetting the semicolon at the end of printf() or return statement",
                "fix": "Every statement in C ends with a semicolon ;",
                "code": 'printf("Hello")\nreturn 0',
                "fixed_code": 'printf("Hello");\nreturn 0;',
            },
            {
                "mistake": "Writing main without int before it",
                "fix": "Always write int main() the int part tells C that main returns an integer",
                "code": "main() { }",
                "fixed_code": "int main() { }",
            },
        ],
        exercise={
            "description": (
                "Write a C program that prints your name and your favorite hobby "
                "on two separate lines."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    // Write your code here\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "Use printf() for each line",
                "Add \\n at the end of each string to move to a new line",
                "You can call printf() multiple times",
            ],
            "expected_output": (
                "My name is Alex\n"
                "I love programming"
            ),
        },
        key_takeaways=[
            "#include <stdio.h> imports the input/output library",
            "int main() is where every C program starts executing",
            "printf() prints text to the terminal",
            "Every statement must end with a semicolon",
            "return 0; tells the computer the program succeeded",
        ],
        next_steps="Great job! Now let us learn more about printf() and how to format text.",
    ),

    _lesson(
        lesson_id="c-l01-03",
        theory=(
            "You already used printf() in your first program. Now let us really understand it. "
            "printf() is short for print formatted it does not just print text, it can also print "
            "numbers, variables, and format them exactly how you want."
            "\n\n"
            "The magic happens with format specifiers. A format specifier starts with a % sign "
            "and tells printf() what kind of data you are printing. Think of them as placeholders. "
            "You put them inside the string, and then list the actual values afterward."
            "\n\n"
            "Common format specifiers:"
            "\n- %d or %i for integers (whole numbers like 42)"
            "\n- %f for decimal numbers (like 3.14)"
            "\n- %c for a single character (like A)"
            "\n- %s for a string (like Hello)"
            "\n\n"
            "You can also control spacing and decimal places. %.2f prints a number "
            "with exactly 2 digits after the decimal point."
        ),
        analogy=(
            "Think of printf() like a fill-in-the-blanks worksheet. The format string is your "
            "worksheet with blanks marked by % signs. The values after the string are the answers "
            "you fill in."
        ),
        sections=[
            {
                "heading": "Printing multiple values",
                "body": (
                    "You can put multiple format specifiers in one printf() call. Just make sure "
                    "the order of the values matches the order of your placeholders."
                ),
                "code": (
                    '#include <stdio.h>\n'
                    '\n'
                    'int main() {\n'
                    '    printf("Name: %s, Age: %d, Height: %.1f\\n", "Alex", 18, 5.9);\n'
                    '    return 0;\n'
                    '}'
                ),
                "pro_tip": (
                    "If you use the wrong format specifier like %d for a decimal number "
                    "you will get weird output. C will not warn you, it will just print garbage."
                ),
            },
            {
                "heading": "Escape sequences",
                "body": (
                    "You saw \\n for newline. There are other escape sequences too:"
                    "\n- \\t adds a tab (like pressing Tab)"
                    "\n- \\\\ prints a single backslash"
                    "\n- \\\" prints a double quote inside a string"
                ),
                "code": (
                    '#include <stdio.h>\n'
                    '\n'
                    'int main() {\n'
                    '    printf("Column1\\tColumn2\\tColumn3\\n");\n'
                    '    printf("Value1\\tValue2\\tValue3\\n");\n'
                    '    return 0;\n'
                    '}'
                ),
            },
        ],
        code_example={
            "code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int age = 18;\n'
                '    float pi = 3.14159;\n'
                '    char grade = \'A\';\n'
                '    printf("Age: %d\\n", age);\n'
                '    printf("Pi to 2 decimals: %.2f\\n", pi);\n'
                '    printf("Grade: %c\\n", grade);\n'
                '    return 0;\n'
                '}'
            ),
            "annotations": [
                {"line": 4, "text": "Declares an integer variable named age with value 18"},
                {"line": 5, "text": "Declares a float (decimal) variable named pi"},
                {"line": 6, "text": "Declares a character variable with value A"},
                {"line": 7, "text": "%d prints the integer value of age"},
                {"line": 8, "text": "%.2f prints pi with exactly 2 decimal places"},
            ],
        },
        common_mistakes=[
            {
                "mistake": "Using %d to print a decimal number instead of %f",
                "fix": "Use %d for integers (int), %f for decimals (float/double)",
                "code": 'float x = 5.5; printf("%d", x);',
                "fixed_code": 'float x = 5.5; printf("%f", x);',
            },
        ],
        exercise={
            "description": (
                "Write a program that prints a mini profile card with your name, "
                "age, height with 2 decimal places, and your initial."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "Use %s for string (name), %d for age, %.2f for height, %c for initial",
                "Use \\t to align columns nicely",
            ],
            "expected_output": (
                "Name:   Alex\n"
                "Age:    18\n"
                "Height: 1.75m\n"
                "Initial: A"
            ),
        },
        quiz={
            "question": "What format specifier do you use to print a decimal number?",
            "options": ["%d", "%f", "%c", "%s"],
            "correct": 1,
            "explanation": (
                "%f is used for floating-point (decimal) numbers."
            ),
        },
        key_takeaways=[
            "printf() uses format specifiers (%d, %f, %c, %s) as placeholders",
            "List the values after the format string in the same order",
            "\\n creates a new line, \\t adds a tab",
            "%.Nf controls how many decimal places are shown",
        ],
        next_steps="Now you can print anything! Next up: adding comments to your code.",
    ),

    _lesson(
        lesson_id="c-l01-04",
        theory=(
            "Comments are notes you leave in your code for yourself and other programmers. "
            "The computer completely ignores comments they are purely for humans to read. "
            "Think of them as sticky notes attached to your code."
            "\n\n"
            "C has two types of comments:"
            "\n\n"
            "Single-line comments start with //. Everything after // on that line is ignored. "
            "Use these for short notes about a specific line."
            "\n\n"
            "Multi-line comments go between /* and */. Everything between them is ignored, "
            "even if it spans multiple lines. Use these for longer explanations or to temporarily "
            "disable a block of code."
            "\n\n"
            "Good comments explain WHY you did something, not WHAT you did. The code itself "
            "should already show what it is doing."
        ),
        analogy=(
            "Comments are like the labels on a diagram. A blueprint of a house has labels "
            "pointing to rooms. Those labels do not build the house, "
            "but they help the builder understand the plan."
        ),
        sections=[
            {
                "heading": "When to use comments",
                "body": (
                    "Use comments when:"
                    "\n- The code has a complex or non-obvious logic"
                    "\n- You made a design decision that might not make sense at first glance"
                    "\n- You are explaining a bug fix or workaround"
                    "\n- You want to temporarily disable code without deleting it"
                    "\n- You are writing documentation for a function"
                ),
                "pro_tip": (
                    "If you find yourself explaining what a line does with a comment, "
                    "consider making the code clearer instead."
                ),
            },
        ],
        code_example={
            "code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    // This is a single-line comment\n'
                '    printf("Hello!\\n");\n'
                '\n'
                '    /*\n'
                '     * This is a multi-line comment.\n'
                '     * It can span several lines.\n'
                '     */\n'
                '    printf("World!\\n");\n'
                '\n'
                '    // printf("This line is disabled\\n");\n'
                '\n'
                '    return 0;\n'
                '}'
            ),
            "annotations": [
                {"line": 4, "text": "Single-line comment explaining the next line"},
                {"line": 7, "text": "Multi-line comment block spanning several lines"},
            ],
        },
        common_mistakes=[
            {
                "mistake": "Nesting /* */ comments inside each other",
                "fix": "You cannot nest /* */ comments. Use // inside /* */ blocks instead.",
                "code": (
                    '/* Outer comment\n'
                    '   /* Inner comment */\n'
                    '   Broken! */'
                ),
                "fixed_code": (
                    '/* Outer comment\n'
                    '   // Inner comment\n'
                    '   Works! */'
                ),
            },
        ],
        exercise={
            "description": (
                "Take the hello world program and add at least three comments explaining "
                "what each part does."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    printf("Hello, World!\\n");\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "Use // for short comments",
                "Use /* */ for longer explanations",
            ],
            "expected_output": "Hello, World!",
        },
        quiz={
            "question": "What happens when the compiler encounters a comment?",
            "options": [
                "It prints the comment to the screen",
                "It skips the comment and continues compiling",
                "It stores the comment in a separate file",
            ],
            "correct": 1,
            "explanation": (
                "The compiler completely ignores comments."
            ),
        },
        key_takeaways=[
            "Comments are ignored by the compiler they are for humans",
            "// makes everything after it on that line a comment",
            "/* */ creates block comments that can span multiple lines",
            "Comments should explain WHY, not WHAT",
        ],
        next_steps="Now let us understand the compilation process.",
    ),

    _lesson(
        lesson_id="c-l01-05",
        theory=(
            "When you write C code, your computer does not understand it directly. Computers speak "
            "in 1s and 0s machine code. The process of turning your human-readable C code into "
            "machine code is called compilation."
            "\n\n"
            "Compilation happens in four stages:"
            "\n\n"
            "1. Preprocessing handles all lines that start with #. It replaces #include <stdio.h> "
            "with the actual content of that file."
            "\n\n"
            "2. Compilation translates the preprocessed C code into assembly language."
            "\n\n"
            "3. Assembly converts assembly into machine code (object code), creating a .o file."
            "\n\n"
            "4. Linking combines all object files with library code into a single executable."
        ),
        analogy=(
            "Think of compilation like baking a cake from a recipe. Preprocessing is gathering "
            "ingredients. Compilation is mixing. Assembly is putting batter in the pan. "
            "Linking is baking it all together into the final cake."
        ),
        sections=[
            {
                "heading": "The gcc command explained",
                "body": (
                    "When you run gcc hello.c -o hello:"
                    "\n- gcc: Invokes the GNU C Compiler"
                    "\n- hello.c: The source file to compile"
                    "\n- -o hello: Names the output file hello"
                ),
                "code": (
                    "# Full compilation\n"
                    "gcc -Wall hello.c -o hello\n"
                    "\n"
                    "# Preprocessing only\n"
                    "gcc -E hello.c -o hello.i\n"
                    "\n"
                    "# Compile to assembly only\n"
                    "gcc -S hello.c -o hello.s"
                ),
                "pro_tip": (
                    "Use gcc -Wall to enable all warnings. The compiler tells you "
                    "about potential mistakes before you run the code."
                ),
            },
        ],
        common_mistakes=[
            {
                "mistake": "Trying to run the .c file directly instead of the compiled executable",
                "fix": "Compile first, then run the output file (hello, not hello.c)",
                "code": "./hello.c",
                "fixed_code": "gcc hello.c -o hello && ./hello",
            },
        ],
        exercise={
            "description": (
                "Write a C program that prints Compilation is magic! Then run "
                "the preprocessor step with gcc -E and look at the output file "
                "to see how much code was added by #include."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    printf("Compilation is magic!\\n");\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "Save as compile_test.c",
                "Run gcc -E compile_test.c -o compile_test.i",
                "Open compile_test.i to see the expanded file",
            ],
            "expected_output": "Compilation is magic!",
        },
        quiz={
            "question": "What does gcc -c hello.c do?",
            "options": [
                "Compiles and runs the program",
                "Only preprocesses the file",
                "Compiles to object code but does not link",
            ],
            "correct": 2,
            "explanation": (
                "The -c flag compiles to object code (.o) but stops before linking."
            ),
        },
        key_takeaways=[
            "Compilation translates C code into machine code",
            "Four stages: preprocessing, compilation, assembly, linking",
            "gcc -Wall shows all warnings to help catch mistakes",
            "Fix the first error first later errors are often side effects",
        ],
        next_steps="Time to practice writing and compiling your own program!",
    ),

    _lesson(
        lesson_id="c-l01-06",
        theory=(
            "Now it is time to write, compile, and run a C program entirely on your own. "
            "The goal is to get comfortable with the edit-compile-run loop."
            "\n\n"
            "Here is the workflow:"
            "\n1. Create a .c file"
            "\n2. Write code"
            "\n3. Save"
            "\n4. Compile with gcc -Wall"
            "\n5. Fix any errors"
            "\n6. Run the program"
        ),
        analogy=(
            "The edit-compile-run loop is like learning to ride a bike. "
            "At first you wobble and fall, but each time you try you get better. "
            "Every programmer started exactly where you are."
        ),
        sections=[
            {
                "heading": "What you will practice",
                "body": (
                    "You will write a program that prints a greeting, your favorite number, "
                    "and your reason for learning C."
                ),
                "pro_tip": (
                    "Always compile with -Wall to catch potential issues."
                ),
            },
        ],
        exercise={
            "description": (
                "Write a complete C program that prints three lines: "
                "a greeting, your favorite number, and why you are learning C."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "Use printf() for each line",
                "Run: gcc -Wall program.c -o program && ./program",
            ],
            "expected_output": (
                "Hello, I am Alex!\n"
                "My favorite number is 42\n"
                "I am learning C to understand computers"
            ),
        },
        key_takeaways=[
            "The edit-compile-run loop is the standard C workflow",
            "Always compile with -Wall",
            "Practice makes perfect",
        ],
        next_steps="Let us try a challenge: printing patterns!",
    ),

    _lesson(
        lesson_id="c-l01-07",
        theory=(
            "Now that you know how to print text, let us use printf() creatively to make patterns. "
            "Printing patterns teaches you about repetition and careful spacing."
            "\n\n"
            "ASCII art is creating pictures using only text characters. "
            "People have been making ASCII art since the 1960s."
        ),
        analogy=(
            "Printing patterns is like using a typewriter to draw a picture. "
            "Each key press leaves a character on the page."
        ),
        sections=[
            {
                "heading": "Pattern design tips",
                "body": (
                    "When designing a pattern:"
                    "\n- Draw it on paper first"
                    "\n- Count characters carefully"
                    "\n- Use printf() with \\n for each line"
                ),
                "pro_tip": (
                    "Use a monospace font where every character "
                    "takes the same width for perfect alignment."
                ),
            },
        ],
        exercise={
            "description": (
                "Print a diamond pattern using asterisks (*):"
                "\n  *"
                "\n ***"
                "\n*****"
                "\n ***"
                "\n  *"
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    printf("  *\\n");\n'
                '    // Add more lines\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "Middle line has 5 asterisks with no spaces",
                "Count spaces: 2 then 1 then 0 then 1 then 2",
            ],
            "expected_output": (
                "  *\n ***\n*****\n ***\n  *"
            ),
        },
        key_takeaways=[
            "printf() can create visual patterns and ASCII art",
            "Plan your output on paper before coding",
            "Spacing is critical for patterns",
        ],
        next_steps="Ready for your first project: a terminal startup banner!",
    ),

    _lesson(
        lesson_id="c-l01-08",
        theory=(
            "Welcome to your first project! A project combines multiple concepts "
            "into a larger program. This project will be a terminal startup banner."
            "\n\n"
            "You will combine printf(), format specifiers, escape sequences, "
            "ASCII art, and comments."
            "\n\n"
            "A good terminal banner includes an ASCII art logo, a welcome message, "
            "system info, and clean formatting."
        ),
        analogy=(
            "A terminal startup banner is like a welcome mat at the entrance of a house. "
            "It sets the tone and makes people feel welcome."
        ),
        sections=[
            {
                "heading": "Project requirements",
                "body": (
                    "Your banner must include an ASCII art logo, a welcome message, "
                    "fictional system stats, and a motivational quote."
                ),
                "pro_tip": (
                    "Keep your ASCII art simple. A 4-5 line design is plenty."
                ),
            },
        ],
        exercise={
            "description": (
                "Build a terminal startup banner with ASCII art, welcome message, "
                "system stats, and a quote."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    printf("\\n");\n'
                '    // Build your banner here\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "Break the banner into sections",
                "Use characters like + - | for borders",
                "Test each printf() line separately",
            ],
            "expected_output": (
                "A multi-line terminal banner with ASCII art and system stats."
            ),
        },
        key_takeaways=[
            "Projects combine multiple skills into a single program",
            "Plan on paper first, then code",
            "Break large programs into smaller pieces",
            "Congratulations on your first project!",
        ],
        next_steps="Level 1 complete! Now let us move to Level 2: Variables.",
    ),
]))


# ============================================================================
# LEVEL 2: VARIABLES
# ============================================================================

HAND_CRAFTED_LESSONS.update(dict([
    _lesson(
        lesson_id="c-l02-01",
        theory=(
            "Variables are named containers that hold values. In C, every variable has a type "
            "that tells the computer what kind of data it holds."
            "\n\n"
            "Three number types:"
            "\n- int stores whole numbers like 42, -7, or 0"
            "\n- float stores decimal numbers like 3.14 (4 bytes, ~6-7 digits precision)"
            "\n- double stores decimal numbers with double precision (8 bytes, ~15-16 digits)"
        ),
        analogy=(
            "Types are like different container sizes. int is a shot glass (whole numbers only). "
            "float is a measuring cup (handles decimals). double is a scientific beaker "
            "(very precise, takes more space)."
        ),
        sections=[
            {
                "heading": "When to use which?",
                "body": (
                    "Use int for counting things. Use float for general decimals. "
                    "Use double for high-precision work like science or finance."
                ),
                "pro_tip": (
                    "When dividing two integers, the result is TRUNCATED. "
                    "5 / 2 gives 2, not 2.5! Use 5 / 2.0 to get 2.5."
                ),
            },
        ],
        code_example={
            "code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int age = 18;\n'
                '    float temp = 36.5;\n'
                '    double pi = 3.14159265358979;\n'
                '    printf("int: %d, float: %.1f, double: %.10f\\n", age, temp, pi);\n'
                '    return 0;\n'
                '}'
            ),
            "annotations": [
                {"line": 4, "text": "int variable holding a whole number"},
                {"line": 5, "text": "float variable with one decimal place"},
                {"line": 6, "text": "double with many decimal places high precision"},
            ],
        },
        common_mistakes=[
            {
                "mistake": "Assigning a decimal to an int truncates the value",
                "fix": "Make sure the variable type matches the data",
                "code": "int x = 3.9;",
                "fixed_code": "double x = 3.9;",
            },
        ],
        exercise={
            "description": (
                "Declare an int, float, and double. Print them in a table "
                "with columns for Type, Value, and Size."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int i = 42;\n'
                '    float f = 3.14;\n'
                '    double d = 2.71828;\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "Use \\t to align columns",
                "Print header row first",
            ],
            "expected_output": (
                "Type    Value   Size\\n"
                "int     42      4\\n"
                "float   3.14    4\\n"
                "double  2.7183  8"
            ),
        },
        quiz={
            "question": "What happens if you assign 3.9 to an int?",
            "options": ["Rounded to 4", "Truncated to 3", "Compiler error", "Crash"],
            "correct": 1,
            "explanation": "C truncates the decimal part. 3.9 becomes 3, not 4."
        },
        key_takeaways=[
            "int stores whole numbers, float/double store decimals",
            "double has twice the precision of float",
            "Integer division truncates 5/2 = 2",
            "Use .0 to force decimal division",
        ],
        next_steps="Now let us learn about the char type!",
    ),

    _lesson(
        lesson_id="c-l02-02",
        theory=(
            "The char type stores a single character like A or z or 3. Under the hood, "
            "a char is actually a small integer. Every character has an ASCII code: "
            "A=65, B=66, a=97, 0=48."
            "\n\n"
            "This means you can do math with characters. A + 1 = B. "
            "a minus 32 = A (the difference between upper and lowercase is 32)."
        ),
        analogy=(
            "A char is like a locker in a school hallway. Each locker has a number "
            "(the ASCII code) but you refer to it by the student's name (the character). "
            "A is the student, 65 is the locker number."
        ),
        sections=[
            {
                "heading": "Printing characters as numbers",
                "body": (
                    "Use %c to print a char as a letter, %d to print its ASCII code."
                ),
                "pro_tip": (
                    "Memorize: A=65, a=97, 0=48. These three values help with debugging."
                ),
            },
        ],
        code_example={
            "code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    char grade = \'A\';\n'
                '    printf("Char: %c, ASCII: %d\\n", grade, grade);\n'
                '    char lower = \'m\';\n'
                '    char upper = lower - 32;\n'
                '    printf("%c -> %c\\n", lower, upper);\n'
                '    return 0;\n'
                '}'
            ),
            "annotations": [
                {"line": 4, "text": "Stores the character A"},
                {"line": 5, "text": "%c prints A, %d prints 65"},
                {"line": 7, "text": "Lowercase to uppercase by subtracting 32"},
            ],
        },
        common_mistakes=[
            {
                "mistake": "Using double quotes for a char instead of single quotes",
                "fix": "Single quotes for chars, double quotes for strings",
                "code": 'char c = "A";',
                "fixed_code": "char c = 'A';",
            },
        ],
        exercise={
            "description": (
                "Assign a lowercase letter to a char and print: the character, "
                "its ASCII value, the uppercase version, and the next/previous letters."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    char letter = \'f\';\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "Uppercase = letter - 32",
                "Next = letter + 1, Previous = letter - 1",
            ],
            "expected_output": (
                "Character: f, ASCII: 102\\n"
                "Uppercase: F, Next: g, Previous: e"
            ),
        },
        quiz={
            "question": "What is the ASCII value of A?",
            "options": ["48", "65", "97", "32"],
            "correct": 1,
            "explanation": "A is 65. a is 97. 0 is 48. Space is 32."
        },
        key_takeaways=[
            "char stores a single character using 1 byte",
            "Characters are stored as integer ASCII codes",
            "Lowercase and uppercase differ by 32",
            "Use %c for character, %d for ASCII value",
        ],
        next_steps="Now let us learn how to declare variables properly!",
    ),

    _lesson(
        lesson_id="c-l02-03",
        theory=(
            "Declaring a variable means telling C: type name; or type name = value;"
            "\n\n"
            "Variable naming rules:"
            "\n- Letters, digits, and underscores allowed"
            "\n- Must start with letter or underscore"
            "\n- Cannot use C keywords (int, return, if, etc.)"
            "\n- Case-sensitive: age, Age, and AGE are three different variables"
            "\n- Use descriptive snake_case names: student_count"
        ),
        analogy=(
            "Declaring a variable is like renting a storage unit. You tell the company "
            "what size unit you need (the type) and what label to put on it (the name). "
            "If you do not put anything in it, it might contain garbage from before."
        ),
        sections=[
            {
                "heading": "Uninitialized variables are dangerous",
                "body": (
                    "If you declare a variable without a value, it contains garbage. "
                    "Always initialize your variables when you declare them."
                ),
                "pro_tip": (
                    "Always initialize variables. It is free safety that prevents bugs."
                ),
            },
        ],
        code_example={
            "code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int student_count = 30;\n'
                '    float average = 85.5;\n'
                '    char grade = \'A\';\n'
                '    int a = 1, b = 2, c = 3;\n'
                '    int width = 10, height = 20;\n'
                '    int area = width * height;\n'
                '    printf("Area: %d\\n", area);\n'
                '    return 0;\n'
                '}'
            ),
            "annotations": [
                {"line": 4, "text": "Descriptive name clear what it stores"},
                {"line": 8, "text": "Multiple declarations in one line"},
                {"line": 9, "text": "Self-documenting code with good names"},
            ],
        },
        common_mistakes=[
            {
                "mistake": "Using a C keyword as a variable name",
                "fix": "Keywords are reserved. Use a different name.",
                "code": "int return = 5;",
                "fixed_code": "int result = 5;",
            },
            {
                "mistake": "Starting a variable name with a digit",
                "fix": "Must start with a letter or underscore",
                "code": "int 1st_place = 1;",
                "fixed_code": "int first_place = 1;",
            },
        ],
        exercise={
            "description": (
                "Declare variables for a report card: three subject scores, "
                "calculate average, assign a grade (A for 90+ etc.), and print."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int s1 = 85, s2 = 92, s3 = 78;\n'
                '    double avg;\n'
                '    char grade;\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "avg = (s1 + s2 + s3) / 3.0",
                "A for 90+, B for 80+, C for 70+",
            ],
            "expected_output": (
                "Average: 85.00, Grade: B"
            ),
        },
        quiz={
            "question": "Which is a valid variable name?",
            "options": ["2nd_place", "my-var", "_count", "int"],
            "correct": 2,
            "explanation": "_count starts with underscore (valid). Others start with digit, contain hyphen, or are keywords."
        },
        key_takeaways=[
            "Declare with type name; or type name = value;",
            "Names: letters, digits, underscores, start with letter or underscore",
            "Always initialize variables to avoid garbage values",
            "Use descriptive snake_case names",
        ],
        next_steps="Sometimes values should never change. Let us learn about constants!",
    ),

    _lesson(
        lesson_id="c-l02-04",
        theory=(
            "Constants are values that never change after you set them."
            "\n\n"
            "Two ways to create constants in C:"
            "\n- const keyword: const int DAYS = 7; (type-safe, debuggable)"
            "\n- #define directive: #define DAYS 7 (text replacement before compilation)"
            "\n\n"
            "By convention, constant names are ALL_CAPS."
        ),
        analogy=(
            "Constants are like speed limit signs. The limit is a fixed value. "
            "const is like a police officer who enforces the limit. "
            "#define is like a note in your car it reminds you but does not stop you."
        ),
        sections=[
            {
                "heading": "const vs #define",
                "body": (
                    "const creates an actual typed variable the compiler enforces. "
                    "#define is text replacement the preprocessor replaces the name "
                    "with the value before the compiler even sees it."
                ),
                "pro_tip": (
                    "Use const for function-scoped constants, "
                    "#define for true compile-time constants."
                ),
            },
        ],
        code_example={
            "code": (
                '#include <stdio.h>\n'
                '#define PI 3.14159\n'
                '\n'
                'int main() {\n'
                '    const int DAYS = 7;\n'
                '    printf("PI = %f, Days = %d\\n", PI, DAYS);\n'
                '    // DAYS = 8;  // Error! Cannot modify const\n'
                '    return 0;\n'
                '}'
            ),
            "annotations": [
                {"line": 2, "text": "#define replaces PI with 3.14159 everywhere"},
                {"line": 5, "text": "const makes DAYS read-only"},
                {"line": 7, "text": "This line would cause a compiler error"},
            ],
        },
        common_mistakes=[
            {
                "mistake": "Semicolon at end of #define line",
                "fix": "#define is a directive, not a statement no semicolon",
                "code": "#define PI 3.14;",
                "fixed_code": "#define PI 3.14",
            },
        ],
        exercise={
            "description": (
                "Calculate area and circumference of a circle using #define for PI "
                "and const for radius."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '#define PI 3.14159\n'
                '\n'
                'int main() {\n'
                '    const double r = 5.0;\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "Area = PI * r * r",
                "Circumference = 2 * PI * r",
            ],
            "expected_output": (
                "Area: 78.54, Circumference: 31.42"
            ),
        },
        quiz={
            "question": "What is the difference between const and #define?",
            "options": [
                "No difference",
                "#define creates a variable, const is text replacement",
                "const is typed and debuggable, #define is text replacement",
                "const can be changed, #define cannot",
            ],
            "correct": 2,
            "explanation": "const is a typed variable the compiler enforces. #define is preprocessor text replacement."
        },
        key_takeaways=[
            "Constants cannot be changed after being set",
            "Use const for type-safe constants",
            "Use #define for compile-time text substitution",
            "Name constants in ALL_CAPS",
        ],
        next_steps="Let us explore memory sizes with sizeof!",
    ),

    _lesson(
        lesson_id="c-l02-05",
        theory=(
            "The sizeof operator tells you how many bytes a type or variable uses. "
            "C types have different sizes on different systems. On a 64-bit system: "
            "char=1, int=4, float=4, double=8, short=2, long=8 bytes."
            "\n\n"
            "Use sizeof(type) or sizeof variable. It returns size_t use %zu to print it."
        ),
        analogy=(
            "sizeof is like a luggage scale for data types. Each type has a different weight. "
            "Before you pack (write code), the scale tells you how much space each item takes."
        ),
        sections=[
            {
                "heading": "sizeof with arrays",
                "body": (
                    "sizeof(array) / sizeof(array[0]) gives the number of elements "
                    "in an array. This is a classic C pattern."
                ),
                "pro_tip": (
                    "Always use sizeof for memory allocation instead of hardcoding sizes."
                ),
            },
        ],
        code_example={
            "code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    printf("int: %zu bytes\\n", sizeof(int));\n'
                '    printf("double: %zu bytes\\n", sizeof(double));\n'
                '    int arr[10];\n'
                '    size_t count = sizeof(arr) / sizeof(arr[0]);\n'
                '    printf("Array elements: %zu\\n", count);\n'
                '    return 0;\n'
                '}'
            ),
            "annotations": [
                {"line": 4, "text": "sizeof with a type needs parentheses"},
                {"line": 7, "text": "Classic pattern to find array length"},
            ],
        },
        common_mistakes=[
            {
                "mistake": "Using %d instead of %zu for sizeof values",
                "fix": "sizeof returns size_t, use %zu",
                "code": 'printf("%d", sizeof(int));',
                "fixed_code": 'printf("%zu", sizeof(int));',
            },
        ],
        exercise={
            "description": (
                "Print a table of C types and their sizes on your system. "
                "Include char, short, int, long, long long, float, double."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    printf("Type\\tSize\\n");\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "Use sizeof(type) for each type",
                "Use %zu for the size values",
            ],
            "expected_output": (
                "Type    Size\\n"
                "char    1\\n"
                "int     4\\n"
                "double  8"
            ),
        },
        quiz={
            "question": "What does sizeof(array)/sizeof(array[0]) calculate?",
            "options": [
                "Size of one element",
                "Number of elements in the array",
                "Total bytes of the array",
            ],
            "correct": 1,
            "explanation": "Total bytes divided by bytes per element gives the element count."
        },
        key_takeaways=[
            "sizeof tells you how many bytes a type or variable uses",
            "C types have different sizes on different systems",
            "Use %zu to print size_t",
            "sizeof(array)/sizeof(array[0]) gives array length",
        ],
        next_steps="Now let us read input from users with scanf()!",
    ),

    _lesson(
        lesson_id="c-l02-06",
        theory=(
            "scanf() reads input from the keyboard and stores it in variables. "
            "Syntax: scanf(\"format\", &variable);"
            "\n\n"
            "The & is the address-of operator it tells scanf where to store the value. "
            "Forgetting & is the #1 beginner mistake with scanf."
            "\n\n"
            "Format specifiers for scanf: %d (int), %f (float), %lf (double), "
            "%c (char), %s (string no & needed)."
        ),
        analogy=(
            "scanf() is like a delivery person asking for your address. "
            "The & is like saying deliver to this address. Without it, "
            "scanf knows what to deliver but not where to put it."
        ),
        sections=[
            {
                "heading": "Reading characters with scanf",
                "body": (
                    "When reading a char, add a space before %c: scanf(\" %c\", &ch); "
                    "The space skips any leftover whitespace from previous input."
                ),
                "pro_tip": (
                    "Always check scanf's return value. It returns the number of "
                    "items successfully read. If it fails, handle the error."
                ),
            },
        ],
        code_example={
            "code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int age;\n'
                '    printf("Enter age: ");\n'
                '    scanf("%d", &age);\n'
                '    printf("You are %d years old\\n", age);\n'
                '    return 0;\n'
                '}'
            ),
            "annotations": [
                {"line": 6, "text": "&age gives scanf the address to store the value"},
                {"line": 7, "text": "Prints the value that was read"},
            ],
        },
        common_mistakes=[
            {
                "mistake": "Forgetting & before the variable in scanf",
                "fix": "scanf needs the memory address of the variable",
                "code": 'scanf("%d", age);',
                "fixed_code": 'scanf("%d", &age);',
            },
            {
                "mistake": "Using %f for double in scanf (should be %lf)",
                "fix": "Use %lf for double with scanf",
                "code": 'double x; scanf("%f", &x);',
                "fixed_code": 'double x; scanf("%lf", &x);',
            },
        ],
        exercise={
            "description": (
                "Ask the user for their initial, age, and favorite number. "
                "Then print them in a sentence."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    char initial;\n'
                '    int age;\n'
                '    float favorite;\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "Use \" %c\" for reading char (space before %c)",
                "Prompt clearly so the user knows what to enter",
            ],
            "expected_output": (
                "Enter initial: A\\n"
                "Enter age: 18\\n"
                "Enter number: 42.5\\n"
                "Hi A, 18 years old, favorite: 42.50"
            ),
        },
        quiz={
            "question": "Why do you need & before a variable in scanf?",
            "options": [
                "It is optional",
                "It gives scanf the memory address to store the value",
                "It converts the variable type",
            ],
            "correct": 1,
            "explanation": "scanf needs to know where in memory to store the input value."
        },
        key_takeaways=[
            "scanf() reads keyboard input using format specifiers",
            "Always use & before variable names (except strings)",
            "Use %lf for double with scanf",
            "Add space before %c to skip whitespace",
            "Check scanf's return value for error handling",
        ],
        next_steps="Let us learn about type casting!",
    ),

    _lesson(
        lesson_id="c-l02-07",
        theory=(
            "Type casting converts a value from one type to another. "
            "Implicit casting happens automatically when mixing types. "
            "Explicit casting uses (type) syntax: (int), (double), etc."
            "\n\n"
            "Going from smaller to larger type (int to double) is safe. "
            "Going from larger to smaller (double to int) loses data."
        ),
        analogy=(
            "Type casting is like pouring water between containers. "
            "Small cup to big bucket everything fits. "
            "Big bucket to small cup you spill the extra."
        ),
        sections=[
            {
                "heading": "The integer division trap",
                "body": (
                    "5 / 2 gives 2 not 2.5 because both are ints. "
                    "Fix: (double)5 / 2 or 5 / 2.0"
                ),
                "pro_tip": (
                    "Cast one operand BEFORE the operation, not the result."
                ),
            },
        ],
        code_example={
            "code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int a = 10, b = 3;\n'
                '    double result = (double)a / b;\n'
                '    printf("Result: %.2f\\n", result);\n'
                '    double pi = 3.14159;\n'
                '    int truncated = (int)pi;\n'
                '    printf("Truncated: %d\\n", truncated);\n'
                '    return 0;\n'
                '}'
            ),
            "annotations": [
                {"line": 5, "text": "Casting a to double makes the division floating-point"},
                {"line": 8, "text": "Truncates to 3, not rounded to 4"},
            ],
        },
        common_mistakes=[
            {
                "mistake": "Casting the result instead of an operand in division",
                "fix": "Cast one operand BEFORE the division",
                "code": 'double x = (double)(5 / 2);',
                "fixed_code": 'double x = (double)5 / 2;',
            },
        ],
        exercise={
            "description": (
                "Ask for a decimal number, then print the original, "
                "truncated, rounded, and decimal part."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    double val;\n'
                '    printf("Enter a number: ");\n'
                '    scanf("%lf", &val);\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "Truncated: (int)val",
                "Rounded: (int)(val + 0.5)",
                "Decimal: val - (int)val",
            ],
            "expected_output": (
                "Original: 7.80\\n"
                "Truncated: 7\\n"
                "Rounded: 8\\n"
                "Decimal: 0.80"
            ),
        },
        quiz={
            "question": "What is (int)(3.9) in C?",
            "options": ["4", "3", "3.9", "Error"],
            "correct": 1,
            "explanation": "(int) truncates toward zero. 3.9 becomes 3."
        },
        key_takeaways=[
            "Implicit casting happens automatically",
            "Explicit casting uses (type) syntax",
            "Integer division truncates cast one operand to fix",
            "(int) truncates toward zero it does not round",
        ],
        next_steps="Practice with a temperature converter!",
    ),

    _lesson(
        lesson_id="c-l02-08",
        theory=(
            "This practice combines variables, constants, input, casting, and output "
            "into a temperature converter."
            "\n\n"
            "Formulas:"
            "\n- Fahrenheit = Celsius x 9/5 + 32"
            "\n- Kelvin = Celsius + 273.15"
        ),
        analogy=(
            "Temperature conversion is like translating between languages. "
            "The same meaning expressed with different words."
        ),
        sections=[
            {
                "heading": "Watch your division",
                "body": (
                    "Use 9.0/5.0 instead of 9/5 to avoid integer truncation."
                ),
                "pro_tip": (
                    "Use double for all temperature calculations."
                ),
            },
        ],
        exercise={
            "description": (
                "Ask for Celsius, print Fahrenheit and Kelvin with 2 decimal places."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    double c, f, k;\n'
                '    printf("Celsius: ");\n'
                '    scanf("%lf", &c);\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "f = c * 9.0 / 5.0 + 32.0",
                "k = c + 273.15",
            ],
            "expected_output": (
                "Celsius: 25.00 C\\n"
                "Fahrenheit: 77.00 F\\n"
                "Kelvin: 298.15 K"
            ),
        },
        key_takeaways=[
            "Practice combining variables, input, output, and casting",
            "Always use double for temperature calculations",
            "Use 9.0/5.0 not 9/5",
        ],
        next_steps="Challenge: swap two numbers!",
    ),

    _lesson(
        lesson_id="c-l02-09",
        theory=(
            "Swap two variables exchange their values. "
            "If a=5 and b=10, after swap a=10 and b=5."
            "\n\n"
            "The classic solution uses a temporary variable:"
            "\ntemp = a;"
            "\na = b;"
            "\nb = temp;"
        ),
        analogy=(
            "Swapping is like swapping the contents of two cups. "
            "You need a third cup to hold one drink while you move the other."
        ),
        sections=[
            {
                "heading": "The XOR trick",
                "body": (
                    "a ^= b; b ^= a; a ^= b; also works but only for integers. "
                    "Always prefer the temp variable approach it is clearer."
                ),
                "pro_tip": (
                    "In real code, use the temp variable. It is readable and works for all types."
                ),
            },
        ],
        exercise={
            "description": (
                "Ask for two integers, print before and after swapping."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int a, b, temp;\n'
                '    printf("Enter two numbers: ");\n'
                '    scanf("%d %d", &a, &b);\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "temp = a; a = b; b = temp;",
            ],
            "expected_output": (
                "Before: a=5, b=10\\n"
                "After: a=10, b=5"
            ),
        },
        quiz={
            "question": "What is the most reliable way to swap two variables?",
            "options": [
                "XOR trick",
                "Temporary variable",
                "Addition/subtraction",
            ],
            "correct": 1,
            "explanation": "Temp variable works for all types and is clearest."
        },
        key_takeaways=[
            "Swap uses a temp variable as a holding space",
            "Three-step swap: temp=a, a=b, b=temp",
            "Temp variable is clearest and works for all types",
        ],
        next_steps="Now build a memory-safe calculator project!",
    ),

    _lesson(
        lesson_id="c-l02-10",
        theory=(
            "Build a calculator with error checking. Check for:"
            "\n- Division by zero"
            "\n- Overflow"
            "\n- Invalid input"
            "\n\n"
            "Support +, -, *, /, % and keep a history log of calculations."
        ),
        analogy=(
            "A memory-safe calculator is like a cashier who double-checks your change. "
            "Instead of just giving any answer, they verify it is reasonable."
        ),
        sections=[
            {
                "heading": "Error checking",
                "body": (
                    "Always check for division by zero before dividing. "
                    "Check if the user enters valid numbers."
                ),
                "pro_tip": (
                    "Use double for decimal results from division. "
                    "Only use int for % (modulo)."
                ),
            },
        ],
        exercise={
            "description": (
                "Build a calculator that asks for two numbers and an operator. "
                "Perform the operation with error checking. "
                "Store results in history variables and print at the end."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    double num1, num2, result;\n'
                '    char op;\n'
                '    double hist1 = 0, hist2 = 0;\n'
                '    char hop1, hop2;\n'
                '    int count = 0;\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "Use if-else for each operator",
                "Check for division by zero",
                "Remember %% to print %",
                "Use \" %c\" to read operator",
            ],
            "expected_output": (
                "10 / 3 = 3.33\\n"
                "5 * 0 = 0.00\\n"
                "--- History ---\\n"
                "10.00 / 3.00 = 3.33\\n"
                "5.00 * 0.00 = 0.00"
            ),
        },
        key_takeaways=[
            "Error checking makes programs robust and professional",
            "Always check for division by zero",
            "Use history/logging to make programs more useful",
            "Building real projects is the fastest way to learn",
        ],
        next_steps="Level 2 complete! Now Level 3: Operators.",
    ),
]))


# ============================================================================
# LEVEL 3: OPERATORS
# ============================================================================

HAND_CRAFTED_LESSONS.update(dict([
    _lesson(
        lesson_id="c-l03-01",
        theory=(
            "Arithmetic operators let you do math. The full set:"
            "\n- + Addition"
            "\n- - Subtraction"
            "\n- * Multiplication"
            "\n- / Division"
            "\n- % Modulo (remainder)"
            "\n\n"
            "Modulo gives the remainder after division. 17 % 5 = 2. "
            "It is great for checking even/odd (n % 2 == 0) and extracting digits."
        ),
        analogy=(
            "Arithmetic operators are like basic tools. + is a hammer, - is a screwdriver, "
            "* is a drill, / is a saw, and % is a measuring tape it tells you what is left over."
        ),
        sections=[
            {
                "heading": "Operator precedence",
                "body": (
                    "C follows standard math order: parentheses first, "
                    "then */%, then +-. Use parentheses to make your intent clear."
                ),
                "pro_tip": (
                    "To print a literal %, write %% in the printf string."
                ),
            },
        ],
        code_example={
            "code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int a = 17, b = 5;\n'
                '    printf("%d + %d = %d\\n", a, b, a + b);\n'
                '    printf("%d %% %d = %d\\n", a, b, a % b);\n'
                '    int num = 42;\n'
                '    if (num % 2 == 0) printf("even\\n");\n'
                '    return 0;\n'
                '}'
            ),
            "annotations": [
                {"line": 6, "text": "%% prints a literal % sign"},
                {"line": 8, "text": "Modulo 2 checks if a number is even"},
            ],
        },
        common_mistakes=[
            {
                "mistake": "Using / when you mean %",
                "fix": "/ gives quotient, % gives remainder",
                "code": "int r = 17 / 5;",
                "fixed_code": "int r = 17 % 5;",
            },
        ],
        exercise={
            "description": (
                "Ask for seconds and convert to h:m:s using / and %. "
                "Then extract each digit of the original number."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int sec;\n'
                '    printf("Seconds: ");\n'
                '    scanf("%d", &sec);\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "hours = sec / 3600",
                "minutes = (sec % 3600) / 60",
                "secs = sec % 60",
            ],
            "expected_output": (
                "3665 seconds = 1h 1m 5s"
            ),
        },
        quiz={
            "question": "What does 17 % 5 equal?",
            "options": ["3", "2", "3.4", "12"],
            "correct": 1,
            "explanation": "17 / 5 = 3 remainder 2. % gives the remainder."
        },
        key_takeaways=[
            "Arithmetic operators: +, -, *, /, %",
            "/ gives quotient, % gives remainder",
            "Modulo is great for even/odd checks and digit extraction",
            "Use parentheses to control order of operations",
        ],
        next_steps="Now let us compare values with relational operators!",
    ),

    _lesson(
        lesson_id="c-l03-02",
        theory=(
            "Relational operators compare two values and give 1 (true) or 0 (false):"
            "\n- == Equal to (not = which is assignment!)"
            "\n- != Not equal to"
            "\n- < Less than"
            "\n- > Greater than"
            "\n- <= Less than or equal to"
            "\n- >= Greater than or equal to"
            "\n\n"
            "The = vs == mistake is the most common C bug. if (x = 5) assigns 5 to x "
            "and is always true. if (x == 5) compares x to 5."
        ),
        analogy=(
            "Relational operators are like a referee comparing two fighters. "
            "The answer is always yes (1) or no (0)."
        ),
        sections=[
            {
                "heading": "The = vs == trap",
                "body": (
                    "Write constant on the left: if (5 == x). "
                    "If you type if (5 = x), the compiler catches it."
                ),
                "pro_tip": (
                    "Enable -Wall. The compiler warns about if (x = 5)."
                ),
            },
            {
                "heading": "Comparing floating-point numbers",
                "body": (
                    "Never use == with float/double. Tiny precision errors make it unreliable. "
                    "Instead, check if the absolute difference is tiny."
                ),
                "pro_tip": (
                    "Use fabs(a - b) < 0.0001 for safe float comparison."
                ),
            },
        ],
        code_example={
            "code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int a = 10, b = 20;\n'
                '    printf("a == b: %d\\n", a == b);\n'
                '    printf("a < b:  %d\\n", a < b);\n'
                '    int x = 5;\n'
                '    if (x == 5) printf("x is 5\\n");\n'
                '    return 0;\n'
                '}'
            ),
            "annotations": [
                {"line": 5, "text": "false, so prints 0"},
                {"line": 6, "text": "true, so prints 1"},
            ],
        },
        common_mistakes=[
            {
                "mistake": "Using = instead of == in comparison",
                "fix": "Write constant on the left as a safeguard",
                "code": "if (x = 5) {}",
                "fixed_code": "if (5 == x) {}",
            },
        ],
        exercise={
            "description": (
                "Ask for two numbers and print all six comparison results."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int a, b;\n'
                '    printf("Enter two: ");\n'
                '    scanf("%d %d", &a, &b);\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "Use all six operators: == != < > <= >=",
            ],
            "expected_output": (
                "10 == 20: 0\n"
                "10 != 20: 1\n"
                "10 < 20:  1\n"
                "10 > 20:  0"
            ),
        },
        quiz={
            "question": "What is wrong with if (x = 10)?",
            "options": [
                "Nothing",
                "It assigns 10 to x instead of comparing",
                "Missing parentheses",
            ],
            "correct": 1,
            "explanation": "Single = assigns. It sets x to 10, and since 10 is non-zero, it is always true."
        },
        key_takeaways=[
            "Relational operators: ==, !=, <, >, <=, >=",
            "They return 1 (true) or 0 (false)",
            "Never confuse = (assignment) with == (comparison)",
            "Never use == with float/double use a tolerance",
        ],
        next_steps="Combine conditions with logical operators!",
    ),

    _lesson(
        lesson_id="c-l03-03",
        theory=(
            "Logical operators combine multiple conditions:"
            "\n- && AND true only if BOTH are true"
            "\n- || OR true if AT LEAST ONE is true"
            "\n- ! NOT flips true to false and vice versa"
            "\n\n"
            "C uses short-circuit evaluation. For &&, if the first condition is false, "
            "C skips the second. For ||, if the first is true, C skips the second."
        ),
        analogy=(
            "AND is a bouncer who checks both your ID and the guest list. "
            "OR is a bouncer who checks if you are on the list OR know the password. "
            "NOT lets in everyone who is NOT a VIP."
        ),
        sections=[
            {
                "heading": "Common patterns",
                "body": (
                    "Range check: x >= 0 && x <= 100"
                    "\nEither condition: is_admin || is_owner"
                    "\nNegation: !finished"
                    "\nGuard: ptr != NULL && ptr->value > 0"
                ),
                "pro_tip": (
                    "Use De Morgan's laws: !(A && B) = !A || !B"
                ),
            },
        ],
        code_example={
            "code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int age = 18, has_id = 1;\n'
                '    if (age >= 18 && has_id) {\n'
                '        printf("You can enter\\n");\n'
                '    }\n'
                '    if (!has_id) {\n'
                '        printf("Need ID\\n");\n'
                '    }\n'
                '    return 0;\n'
                '}'
            ),
            "annotations": [
                {"line": 5, "text": "Both conditions must be true"},
                {"line": 8, "text": "!has_id is false, so this does not print"},
            ],
        },
        common_mistakes=[
            {
                "mistake": "Using & instead of &&",
                "fix": "& is bitwise AND, && is logical AND",
                "code": "if (x > 0 & x < 100) {}",
                "fixed_code": "if (x > 0 && x < 100) {}",
            },
            {
                "mistake": "Writing 0 < x < 10 like math",
                "fix": "C evaluates left to right. Use &&",
                "code": "if (0 < x < 10) {}",
                "fixed_code": "if (0 < x && x < 10) {}",
            },
        ],
        exercise={
            "description": (
                "Ask for a number and check: positive AND even, "
                "negative OR zero, NOT divisible by 5, between 10 and 50."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int num;\n'
                '    printf("Number: ");\n'
                '    scanf("%d", &num);\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "num > 0 && num % 2 == 0",
                "num < 0 || num == 0",
                "num % 5 != 0",
                "num >= 10 && num <= 50",
            ],
            "expected_output": (
                "24 is positive and even: true\n"
                "24 is negative or zero: false\n"
                "24 is NOT divisible by 5: true\n"
                "24 is between 10-50: true"
            ),
        },
        quiz={
            "question": "What does !(x > 5 || x < 0) simplify to?",
            "options": [
                "x <= 5 && x >= 0",
                "x > 5 && x < 0",
                "!(x > 5) && !(x < 0)",
            ],
            "correct": 0,
            "explanation": "De Morgan: !(A || B) = !A && !B. So x <= 5 && x >= 0."
        },
        key_takeaways=[
            "&& (AND), || (OR), ! (NOT) combine boolean conditions",
            "Short-circuit evaluation skips second condition if result is known",
            "Use && for range checks: x > 0 && x < 100",
            "De Morgan's laws simplify negated conditions",
        ],
        next_steps="Let us work with individual bits using bitwise operators!",
    ),

    _lesson(
        lesson_id="c-l03-04",
        theory=(
            "Bitwise operators work on individual bits of a number. "
            "Computers store everything as 1s and 0s (binary). "
            "Bitwise operators let you manipulate those bits directly."
            "\n\n"
            "The operators:"
            "\n- & AND 1 if both bits are 1"
            "\n- | OR 1 if at least one bit is 1"
            "\n- ^ XOR 1 if the bits are different"
            "\n- ~ NOT flips all bits"
            "\n- << Left shift moves bits left"
            "\n- >> Right shift moves bits right"
        ),
        analogy=(
            "Think of bits as light switches. & is like two switches in series "
            "both must be on. | is like two switches in parallel either one works. "
            "^ is like a hallway light you flip either switch to toggle it."
        ),
        sections=[
            {
                "heading": "What are bitwise operators good for?",
                "body": (
                    "They are used in graphics, cryptography, device drivers, "
                    "performance-critical code, and flags/options."
                ),
                "pro_tip": (
                    "Left shift by 1 multiplies by 2. Right shift by 1 divides by 2. "
                    "This is much faster than regular multiplication."
                ),
            },
        ],
        code_example={
            "code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    unsigned int a = 5;   // 0101\n'
                '    unsigned int b = 3;   // 0011\n'
                '    printf("a & b = %u\\n", a & b);  // 0001 = 1\n'
                '    printf("a | b = %u\\n", a | b);  // 0111 = 7\n'
                '    printf("a ^ b = %u\\n", a ^ b);  // 0110 = 6\n'
                '    printf("a << 1 = %u\\n", a << 1); // 1010 = 10\n'
                '    printf("a >> 1 = %u\\n", a >> 1); // 0010 = 2\n'
                '    return 0;\n'
                '}'
            ),
            "annotations": [
                {"line": 6, "text": "0101 & 0011 = 0001 which is 1"},
                {"line": 7, "text": "0101 | 0011 = 0111 which is 7"},
                {"line": 9, "text": "Left shift by 1 multiplies by 2: 5 x 2 = 10"},
            ],
        },
        common_mistakes=[
            {
                "mistake": "Confusing & (bitwise) with && (logical)",
                "fix": "& is bitwise AND on bits. && is logical AND on conditions.",
                "code": "if (x & y) {}  // Bitwise, not logical!",
                "fixed_code": "if (x > 0 && y > 0) {}",
            },
        ],
        exercise={
            "description": (
                "Take a number, show its binary representation concept, "
                "then show the result of &, |, ^, <<, >> with another number."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    unsigned int a = 12, b = 10;\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "a=12 (1100), b=10 (1010) in binary",
                "Calculate each operation manually first",
            ],
            "expected_output": (
                "12 & 10 = 8\\n"
                "12 | 10 = 14\\n"
                "12 ^ 10 = 6\\n"
                "12 << 1 = 24\\n"
                "12 >> 1 = 6"
            ),
        },
        quiz={
            "question": "What does left shifting by 1 do to a number?",
            "options": ["Adds 1", "Multiplies by 2", "Divides by 2", "Subtracts 1"],
            "correct": 1,
            "explanation": "Left shift by 1 moves all bits left, multiplying the value by 2."
        },
        key_takeaways=[
            "Bitwise operators work on individual bits: & | ^ ~ << >>",
            "Left shift multiplies by 2, right shift divides by 2",
            "Use unsigned int for bitwise operations to avoid surprises",
            "Bitwise AND & is different from logical AND &&",
        ],
        next_steps="Learn about assignment operators that combine operation with assignment!",
    ),

    _lesson(
        lesson_id="c-l03-05",
        theory=(
            "Assignment operators combine an operation with assignment. "
            "Instead of writing x = x + 5, you can write x += 5."
            "\n\n"
            "All arithmetic operators have assignment versions:"
            "\n- +=, -=, *=, /=, %="
            "\n- <<=, >>=, &=, |=, ^="
            "\n\n"
            "x += 5 is exactly the same as x = x + 5. "
            "The compound form is shorter and often clearer."
        ),
        analogy=(
            "Assignment operators are like a vending machine with a built-in coin counter. "
            "Instead of taking out your money, counting it, and putting it back in, "
            "you just add to the total. += is that shortcut."
        ),
        sections=[
            {
                "heading": "Why use them?",
                "body": (
                    "Compound assignment operators:"
                    "\n- Are shorter to write"
                    "\n- Make the intent clearer (you are modifying the variable)"
                    "\n- Can be more efficient (the variable is evaluated once)"
                    "\n- Are idiomatic in C code you will see them everywhere"
                ),
                "pro_tip": (
                    "Use += for counters and accumulators. "
                    "It is the standard pattern in C and looks professional."
                ),
            },
        ],
        code_example={
            "code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int score = 10;\n'
                '    score += 5;  // same as score = score + 5\n'
                '    printf("%d\\n", score);  // 15\n'
                '    score *= 2;  // same as score = score * 2\n'
                '    printf("%d\\n", score);  // 30\n'
                '    score %= 7;  // same as score = score % 7\n'
                '    printf("%d\\n", score);  // 2\n'
                '    return 0;\n'
                '}'
            ),
            "annotations": [
                {"line": 5, "text": "score += 5 adds 5 to score"},
                {"line": 7, "text": "score *= 2 doubles score"},
                {"line": 9, "text": "score %= 7 gives remainder after division by 7"},
            ],
        },
        common_mistakes=[
            {
                "mistake": "Writing =+ instead of +=",
                "fix": "=+ is assignment with a positive sign, not compound assignment",
                "code": "x =+ 5;  // Assigns +5 to x, does not add!",
                "fixed_code": "x += 5;",
            },
        ],
        exercise={
            "description": (
                "Start with a variable at 100. Apply -= 25, /= 3, *= 5, "
                "and %= 7 in sequence. Print the value after each step."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int x = 100;\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "After x -= 25: 75",
                "After x /= 3: 25 (integer division)",
                "After x *= 5: 125",
                "After x %= 7: 125 % 7 = 6",
            ],
            "expected_output": (
                "100 -= 25 = 75\n"
                "75 /= 3 = 25\n"
                "25 *= 5 = 125\n"
                "125 %= 7 = 6"
            ),
        },
        quiz={
            "question": "What does x += 5 do?",
            "options": [
                "Sets x to 5",
                "Adds 5 to x",
                "Checks if x equals 5",
                "Multiplies x by 5",
            ],
            "correct": 1,
            "explanation": "x += 5 is shorthand for x = x + 5. It adds 5 to the current value of x."
        },
        key_takeaways=[
            "Compound assignment operators combine operation with =",
            "+=, -=, *=, /=, %= for arithmetic",
            "<<=, >>=, &=, |=, ^= for bitwise",
            "They are idiomatic C and make code cleaner",
        ],
        next_steps="Not all operators are equal. Let us learn about precedence!",
    ),

    _lesson(
        lesson_id="c-l03-06",
        theory=(
            "Operator precedence determines which operations happen first in an expression. "
            "C follows rules similar to math class (PEMDAS/BODMAS), but with many more operators."
            "\n\n"
            "Precedence from highest to lowest (simplified):"
            "\n1. Parentheses ()"
            "\n2. Unary: ! ~ ++ -- + - (type) * &"
            "\n3. Arithmetic: * / %"
            "\n4. Arithmetic: + -"
            "\n5. Bitwise shift: << >>"
            "\n6. Relational: < > <= >="
            "\n7. Equality: == !="
            "\n8. Bitwise AND: &"
            "\n9. Bitwise XOR: ^"
            "\n10. Bitwise OR: |"
            "\n11. Logical AND: &&"
            "\n12. Logical OR: ||"
            "\n13. Assignment: = += -= etc."
        ),
        analogy=(
            "Operator precedence is like the hierarchy in a restaurant. "
            "The chef (parentheses) decides the special menu first. "
            "Then the sous chef (* / %) prepares the main ingredients. "
            "Then line cooks (+ -) add seasoning. "
            "Finally, the waiter (assignment) brings it to the table."
        ),
        sections=[
            {
                "heading": "The golden rule",
                "body": (
                    "When in doubt, use parentheses. They are free and make your code "
                    "clearer. Writing (a + b) * c is better than relying on knowing "
                    "that * has higher precedence than +."
                ),
                "pro_tip": (
                    "Do not try to memorize the entire precedence table. "
                    "Just remember: parentheses first, multiplication/division before "
                    "addition/subtraction, assignment last. Use () for everything else."
                ),
            },
        ],
        code_example={
            "code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int a = 5, b = 3, c = 2;\n'
                '    // Without parentheses\n'
                '    int r1 = a + b * c;      // 5 + 6 = 11\n'
                '    // With parentheses\n'
                '    int r2 = (a + b) * c;    // 8 * 2 = 16\n'
                '    printf("Without: %d, With: %d\\n", r1, r2);\n'
                '    // Complex expression\n'
                '    int r3 = a > b && b < c || a == c;\n'
                '    int r4 = (a > b && b < c) || (a == c);\n'
                '    printf("Clearer with (): %d\\n", r4);\n'
                '    return 0;\n'
                '}'
            ),
            "annotations": [
                {"line": 6, "text": "* has higher precedence than +, so b*c happens first"},
                {"line": 8, "text": "() forces addition first, then multiplication"},
                {"line": 11, "text": "Hard to read relies on precedence knowledge"},
            ],
        },
        common_mistakes=[
            {
                "mistake": "Assuming left-to-right for all operators",
                "fix": "Precedence overrides left-to-right. * before + even if + comes first.",
                "code": "int x = 2 + 3 * 4;  // 14, not 20",
                "fixed_code": "int x = (2 + 3) * 4;  // 20, clear intent",
            },
        ],
        exercise={
            "description": (
                "Calculate these expressions manually, then write a program to check:"
                "\n1. 2 + 3 * 4 - 5"
                "\n2. (2 + 3) * (4 - 5)"
                "\n3. 10 / 2 + 3 * 2"
                "\n4. 10 / (2 + 3) * 2"
                "\n5. 8 % 3 + 6 / 2"
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    printf("1: %d\\n", 2 + 3 * 4 - 5);\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "Work out each expression step by step",
                "Use parentheses to make your program clear",
            ],
            "expected_output": (
                "1: 9\\n2: -5\\n3: 11\\n4: 4\\n5: 5"
            ),
        },
        quiz={
            "question": "What is the value of 2 + 3 * 4 in C?",
            "options": ["20", "14", "24", "9"],
            "correct": 1,
            "explanation": "* has higher precedence than +, so 3 * 4 = 12, then 2 + 12 = 14."
        },
        key_takeaways=[
            "Operator precedence determines evaluation order",
            "* / % before + -",
            "Assignment (=) has very low precedence",
            "Use parentheses to make your intent clear",
            "Do not memorize the full table use () for clarity",
        ],
        next_steps="The ternary operator is a compact if-else. Let us learn it!",
    ),

    _lesson(
        lesson_id="c-l03-07",
        theory=(
            "The ternary operator is a shorthand for if-else. "
            "Syntax: condition ? value_if_true : value_if_false"
            "\n\n"
            "Example: int max = (a > b) ? a : b;"
            "\nThis reads as: if a > b, max = a, else max = b."
            "\n\n"
            "The ternary operator is an expression it produces a value. "
            "This means you can use it inside printf() or assignments."
        ),
        analogy=(
            "The ternary operator is like a coin flip decision. "
            "Heads (true) you get one outcome, tails (false) you get another. "
            "It is a compact way to choose between two options."
        ),
        sections=[
            {
                "heading": "When to use the ternary operator",
                "body": (
                    "Use it for simple if-else choices. It makes code concise. "
                    "Do not nest ternary operators it becomes unreadable. "
                    "If the logic has more than two branches, use if-else."
                ),
                "pro_tip": (
                    "Ternary is great for printf() to change messages based on a condition. "
                    "printf(\"You %s the exam\\n\", passed ? \"passed\" : \"failed\");"
                ),
            },
        ],
        code_example={
            "code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int score = 85;\n'
                '    char *result = (score >= 60) ? "Pass" : "Fail";\n'
                '    printf("Result: %s\\n", result);\n'
                '    int a = 10, b = 20;\n'
                '    int max = (a > b) ? a : b;\n'
                '    printf("Max: %d\\n", max);\n'
                '    // Ternary inside printf\n'
                '    printf("%d is %s\\n", a, (a % 2 == 0) ? "even" : "odd");\n'
                '    return 0;\n'
                '}'
            ),
            "annotations": [
                {"line": 5, "text": "If score >= 60, result = Pass, else Fail"},
                {"line": 8, "text": "Sets max to the larger of a and b"},
                {"line": 11, "text": "Ternary inside printf for conditional text"},
            ],
        },
        common_mistakes=[
            {
                "mistake": "Using assignment = instead of comparison == in the condition",
                "fix": "The condition in ternary must evaluate to true/false",
                "code": "int x = (a = 5) ? 1 : 0;  // Assigns 5 to a, always true!",
                "fixed_code": "int x = (a == 5) ? 1 : 0;",
            },
            {
                "mistake": "Nesting ternary operators makes code unreadable",
                "fix": "Use if-else for complex conditions",
                "code": "int r = a > b ? a > c ? a : c : b > c ? b : c;",
                "fixed_code": "// Use if-else for clarity",
            },
        ],
        exercise={
            "description": (
                "Ask for a number and print: whether it is positive or negative, "
                "even or odd, and whether it is a multiple of 10 all using ternary operators."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int num;\n'
                '    printf("Number: ");\n'
                '    scanf("%d", &num);\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "num > 0 ? \"positive\" : \"negative\"",
                "num % 2 == 0 ? \"even\" : \"odd\"",
                "num % 10 == 0 ? \"multiple of 10\" : \"not multiple of 10\"",
            ],
            "expected_output": (
                "24 is positive, even, and not a multiple of 10"
            ),
        },
        quiz={
            "question": "What does (a > b) ? a : b do?",
            "options": [
                "Returns the smaller of a and b",
                "Returns the larger of a and b",
                "Swaps a and b",
                "Adds a and b",
            ],
            "correct": 1,
            "explanation": "If a > b, returns a. Otherwise returns b. So it returns the larger value."
        },
        key_takeaways=[
            "Ternary: condition ? value_if_true : value_if_false",
            "It is an expression that produces a value",
            "Great for simple if-else choices",
            "Do not nest ternary operators",
            "Use it in printf() for conditional messages",
        ],
        next_steps="Practice with a quiz score calculator!",
    ),

    _lesson(
        lesson_id="c-l03-08",
        theory=(
            "Practice lesson: build a quiz score calculator. "
            "This combines arithmetic operators, relational operators, ternary, "
            "and if-else in a practical application."
            "\n\n"
            "The program will:"
            "\n1. Ask for the number of questions and correct answers"
            "\n2. Calculate the percentage"
            "\n3. Assign a grade (A=90+, B=80+, C=70+, D=60+, F below)"
            "\n4. Tell the user if they passed or failed"
            "\n5. Give encouragement based on the score"
        ),
        analogy=(
            "A grade calculator is like a teacher grading papers. "
            "You count correct answers, calculate the percentage, "
            "and look up the grade in a table."
        ),
        sections=[
            {
                "heading": "What you will practice",
                "body": (
                    "This exercise combines: variable declaration, scanf() input, "
                    "arithmetic operators (division, multiplication), "
                    "relational operators (comparisons), logical operators (&&), "
                    "ternary operator (pass/fail), and if-else chains (grades)."
                ),
                "pro_tip": (
                    "Use double for the percentage calculation to avoid integer truncation. "
                    "cast the total to double before dividing."
                ),
            },
        ],
        exercise={
            "description": (
                "Write a program that asks for total questions and correct answers. "
                "Calculate the percentage and assign a grade. "
                "Print whether the user passed (60% or above) using ternary. "
                "Then give a custom message: Excellent for 90+, Good for 70+, "
                "Needs improvement for below 70."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    int total, correct;\n'
                '    double percentage;\n'
                '    char grade;\n'
                '    printf("Total questions: ");\n'
                '    scanf("%d", &total);\n'
                '    printf("Correct answers: ");\n'
                '    scanf("%d", &correct);\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "percentage = (double)correct / total * 100",
                "Grade A: >= 90, B: >= 80, C: >= 70, D: >= 60, F: < 60",
                "Use ternary for pass/fail message",
                "Use if-else chain for grade and custom message",
            ],
            "expected_output": (
                "Score: 85.00%\\n"
                "Grade: B\\n"
                "Status: Pass\\n"
                "Good work! Keep it up!"
            ),
        },
        key_takeaways=[
            "Practice combining multiple operator types",
            "Use double for percentage to avoid truncation",
            "Cast to double before division: (double)correct / total",
            "If-else chains work well for grade boundaries",
            "Ternary is great for simple pass/fail messages",
        ],
        next_steps="Challenge: bit manipulation puzzles!",
    ),

    _lesson(
        lesson_id="c-l03-09",
        theory=(
            "Bit manipulation challenges test your understanding of bitwise operators. "
            "These are common in coding interviews and embedded programming."
            "\n\n"
            "Common bit manipulation tricks:"
            "\n- Check if a bit is set: (num & (1 << n)) != 0"
            "\n- Set a bit: num |= (1 << n)"
            "\n- Clear a bit: num &= ~(1 << n)"
            "\n- Toggle a bit: num ^= (1 << n)"
            "\n- Check if power of 2: (n & (n - 1)) == 0"
            "\n- Count set bits: Brian Kernighan's algorithm"
        ),
        analogy=(
            "Bit manipulation is like a control panel with many switches. "
            "Each switch is a bit. You can check if a switch is on (check bit), "
            "flip a switch on (set bit), turn it off (clear bit), "
            "or toggle it (XOR)."
        ),
        sections=[
            {
                "heading": "Why bit manipulation matters",
                "body": (
                    "Bit manipulation is used in:"
                    "\n- Embedded systems (control registers)"
                    "\n- Graphics (color values packed into integers)"
                    "\n- Cryptography"
                    "\n- Compression algorithms"
                    "\n- Performance-critical code"
                    "\n- Interview questions at top tech companies"
                ),
                "pro_tip": (
                    "Brian Kernighan's algorithm counts set bits: "
                    "while (n) { count++; n &= n - 1; }. "
                    "Each iteration removes the rightmost set bit."
                ),
            },
        ],
        code_example={
            "code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    unsigned int n = 29;  // 11101\n'
                '    // Check if bit 3 is set (zero-indexed from right)\n'
                '    if (n & (1 << 3)) printf("Bit 3 is set\\n");\n'
                '    // Count set bits (popcount)\n'
                '    int count = 0;\n'
                '    unsigned int temp = n;\n'
                '    while (temp) {\n'
                '        temp &= temp - 1;\n'
                '        count++;\n'
                '    }\n'
                '    printf("Set bits in %u: %d\\n", n, count);\n'
                '    // Check power of 2\n'
                '    unsigned int p = 16;\n'
                '    if ((p & (p - 1)) == 0) printf("%u is power of 2\\n", p);\n'
                '    return 0;\n'
                '}'
            ),
            "annotations": [
                {"line": 6, "text": "Checks if the 3rd bit (value 8) is set in 29"},
                {"line": 10, "text": "Kernighan's algorithm each iteration clears one set bit"},
                {"line": 17, "text": "Power of 2 check: only one bit is set"},
            ],
        },
        common_mistakes=[
            {
                "mistake": "Forgetting that bits are zero-indexed from the right",
                "fix": "Bit 0 is the least significant bit (value 1)",
                "code": "// Checking bit 3 means the 4th bit from right",
                "fixed_code": "(1 << 3) checks the bit with value 8",
            },
        ],
        exercise={
            "description": (
                "Write a program that demonstrates three bit manipulation challenges:"
                "\n1. Given a number and a bit position, set that bit and show the result"
                "\n2. Given a number and a bit position, clear that bit and show the result"
                "\n3. Given a number, count how many bits are set to 1"
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                'int main() {\n'
                '    unsigned int num = 0b10110110;\n'
                '    int bit = 3;\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "Set bit: num |= (1 << bit)",
                "Clear bit: num &= ~(1 << bit)",
                "Count bits: use while(n) { n &= n - 1; count++; }",
            ],
            "expected_output": (
                "Original: 182 (10110110)\\n"
                "After setting bit 3: 190 (10111110)\\n"
                "After clearing bit 3: 182 (10110110)\\n"
                "Set bits count: 5"
            ),
        },
        quiz={
            "question": "What does (n & (n - 1)) == 0 check for?",
            "options": [
                "If n is odd",
                "If n is a power of 2",
                "If n is even",
                "If n is zero",
            ],
            "correct": 1,
            "explanation": "If n is a power of 2, it has exactly one bit set. Subtracting 1 flips that bit and all bits below. AND gives 0."
        },
        key_takeaways=[
            "Bit manipulation directly controls individual bits",
            "Check bit: n & (1 << pos)",
            "Set bit: n |= (1 << pos)",
            "Clear bit: n &= ~(1 << pos)",
            "Toggle bit: n ^= (1 << pos)",
            "Kernighan's algorithm efficiently counts set bits",
        ],
        next_steps="Final Level 3 project: a multi-format unit converter!",
    ),

    _lesson(
        lesson_id="c-l03-10",
        theory=(
            "Final project for Level 3: a multi-format unit converter. "
            "This project combines arithmetic operators, if-else chains, "
            "switch statements, and everything you have learned."
            "\n\n"
            "Your converter will support multiple categories:"
            "\n- Length: meters, feet, inches, kilometers, miles"
            "\n- Weight: kilograms, pounds, ounces, grams"
            "\n- Temperature: Celsius, Fahrenheit, Kelvin"
            "\n- Data: bytes, kilobytes, megabytes, gigabytes"
            "\n\n"
            "Each conversion is a formula using arithmetic operators. "
            "The user selects the category, chooses source and target units, "
            "enters a value, and gets the converted result."
        ),
        analogy=(
            "A unit converter is like a universal translator from Star Trek. "
            "You speak a measurement in one unit, and it translates to another. "
            "The converter knows all the 'languages' (units) and the conversion rates."
        ),
        sections=[
            {
                "heading": "Project structure",
                "body": (
                    "Use a menu system with nested if-else or switch:"
                    "\n1. Ask which category (length, weight, temp, data)"
                    "\n2. Ask source unit"
                    "\n3. Ask target unit"
                    "\n4. Get the value"
                    "\n5. Calculate and display"
                    "\n\nFor file I/O bonus: save the last 5 conversions to a file."
                ),
                "pro_tip": (
                    "Store conversion factors as constants. "
                    "For example: #define METERS_TO_FEET 3.28084"
                    "\nThis makes your code more readable and maintainable."
                ),
            },
        ],
        exercise={
            "description": (
                "Build a unit converter supporting at least 4 categories "
                "with 3+ units each. Use constants for conversion factors. "
                "Make it loop until the user chooses to quit."
            ),
            "starter_code": (
                '#include <stdio.h>\n'
                '\n'
                '#define METERS_TO_FEET 3.28084\n'
                '#define KG_TO_LBS 2.20462\n'
                '\n'
                'int main() {\n'
                '    int choice;\n'
                '    double value, result;\n'
                '    printf("=== Unit Converter ===\\n");\n'
                '    printf("1. Length\\n2. Weight\\n3. Temperature\\n4. Data\\n");\n'
                '    printf("Choose category: ");\n'
                '    scanf("%d", &choice);\n'
                '    return 0;\n'
                '}'
            ),
            "hints": [
                "Use switch(choice) for the category menu",
                "Nested switch for source/target units",
                "For temperature, use formulas: F = C * 9/5 + 32",
                "For data: 1 KB = 1024 bytes",
                "Wrap everything in a do-while loop for repeated use",
            ],
            "expected_output": (
                "=== Unit Converter ===\\n"
                "1. Length 2. Weight 3. Temp 4. Data\\n"
                "Choice: 1\\n"
                "Source (1-m, 2-ft, 3-in): 1\\n"
                "Target (1-m, 2-ft, 3-in): 2\\n"
                "Value: 10\\n"
                "10.00 m = 32.81 ft\\n"
                "Convert again? (1=yes): 0"
            ),
        },
        key_takeaways=[
            "Large programs need structure: menus, constants, clear flow",
            "Use #define constants for conversion factors",
            "switch statements handle multi-way branching cleanly",
            "do-while loops create menu systems that run at least once",
            "Test each conversion formula separately",
            "Congratulations on completing Level 3!",
        ],
        next_steps="Level 3 complete! You now understand C operators. Next: Conditionals (if, else, switch).",
    ),
]))


# ============================================================================
# TEMPLATE GENERATOR FOR LEVELS 4-12
# ============================================================================

_C_KEYWORDS = [
    "if", "else", "switch", "case", "break", "default",
    "for", "while", "do", "continue",
    "int", "float", "double", "char", "void", "long", "short", "unsigned",
    "return", "struct", "union", "enum", "typedef",
    "const", "static", "extern", "register", "volatile",
    "sizeof", "typedef",
]


def _extract_concept(title: str) -> str:
    """Extract the main concept keyword from a lesson title."""
    t = title.lower()
    t = t.replace("(", "").replace(")", "").replace(":", "").replace("-", " ").replace("\u2014", " ").replace("\u2013", " ")
    words = t.split()
    for w in words:
        if w in ["practice", "challenge", "project", "lab", "review", "blitz", "builder", "hunt", "quick", "session"]:
            continue
        if w in _C_KEYWORDS:
            return w
    for w in words:
        if len(w) > 3 and w not in ["with", "from", "that", "this", "your", "into", "what", "core", "mini"]:
            return w
    return words[-1] if words else title


def generate_template_content(
    language_id: str,
    lesson_title: str,
    lesson_type: str,
    lesson_id: str,
) -> dict[str, Any]:
    """Generate lesson content from title/type when no hand-crafted content exists."""
    concept = _extract_concept(lesson_title)

    lang_configs = {
        "c": {
            "include_stmt": "#include <stdio.h>",
            "main_header": "int main() {",
            "main_footer": "    return 0;\n}",
            "output_stmt": 'printf("{}",\n',
            "output_fn": "printf",
            "input_stmt": "scanf(\"%d\", &var);",
            "header_desc": "C is a foundational systems programming language.",
            "platform_note": "Compiled and executed directly on the hardware.",
            "output_example": f'printf("Learning about {concept}");',
            "code_comment": "//",
            "code_template": (
                f"#include <stdio.h>\n\n"
                f"int main() {{\n"
                f"    // TODO: Add {concept} example\n"
                f"    printf(\"Learning about {concept}\");\n"
                f"    return 0;\n"
                f"}}"
            ),
            "exercise_starter": (
                f"#include <stdio.h>\n\n"
                f"int main() {{\n"
                f"    // Implement {concept}\n"
                f"    return 0;\n"
                f"}}"
            ),
            "analogies": [
                f"Think of {concept} as a function in a C program — it gives structure and purpose to your code.",
                f"Like a header file in C, {concept} provides a blueprint that other parts of your program depend on.",
            ],
            "mistakes": [
                {
                    "mistake": f"Misunderstanding the syntax of {concept}",
                    "fix": f"Review the exact syntax rules for {concept} in C",
                    "code": f"// Wrong syntax for {concept}",
                    "fixed_code": f"// Correct syntax for {concept}",
                },
                {
                    "mistake": f"Using {concept} incorrectly with other types",
                    "fix": f"Make sure the types match when using {concept}",
                    "code": f"// Type mismatch with {concept}",
                    "fixed_code": f"// Proper type usage with {concept}",
                },
            ],
            "quiz_question": f"What is the main purpose of {concept} in C?",
            "quiz_explanation": f"{concept} is a fundamental C feature used to organize and structure code.",
            "key_takeaway_prefix": "C",
        },
        "cpp": {
            "include_stmt": "#include <iostream>\nusing namespace std;",
            "main_header": "int main() {",
            "main_footer": "    return 0;\n}",
            "output_stmt": 'cout << "{}" << endl;',
            "output_fn": "cout",
            "input_stmt": "cin >> var;",
            "header_desc": "C++ extends C with object-oriented features and the Standard Template Library.",
            "platform_note": "Compiled, strongly typed, and supports both procedural and OOP paradigms.",
            "output_example": f'cout << "Learning about {concept}" << endl;',
            "code_comment": "//",
            "code_template": (
                f"#include <iostream>\n"
                f"using namespace std;\n\n"
                f"int main() {{\n"
                f"    // TODO: Add {concept} example\n"
                f"    cout << \"Learning about {concept}\" << endl;\n"
                f"    return 0;\n"
                f"}}"
            ),
            "exercise_starter": (
                f"#include <iostream>\n"
                f"using namespace std;\n\n"
                f"int main() {{\n"
                f"    // Implement {concept}\n"
                f"    return 0;\n"
                f"}}"
            ),
            "analogies": [
                f"Think of {concept} as a class member in C++ — it encapsulates behavior and data together.",
                f"Like a template in the C++ STL, {concept} is a reusable building block that adapts to different types.",
            ],
            "mistakes": [
                {
                    "mistake": f"Forgetting to include the correct header for {concept}",
                    "fix": f"Always include <iostream> or the relevant header when using {concept}",
                    "code": f"// Missing header or using namespace std",
                    "fixed_code": f"#include <iostream>\nusing namespace std;",
                },
                {
                    "mistake": f"Using printf instead of cout with {concept}",
                    "fix": f"Use cout << with endl for C++ streams instead of printf",
                    "code": f'printf("Learning about {concept}");',
                    "fixed_code": f'cout << "Learning about {concept}" << endl;',
                },
                {
                    "mistake": f"Confusing :: scope resolution with . member access for {concept}",
                    "fix": f"Use :: for static/class members and . for object members when working with {concept}",
                    "code": f"// Wrong scope: obj::method() instead of obj.method()",
                    "fixed_code": f"// Correct scope: obj.method()",
                },
            ],
            "quiz_question": f"How does {concept} differ in C++ compared to C?",
            "quiz_explanation": f"In C++, {concept} benefits from type safety, namespaces, and the STL.",
            "key_takeaway_prefix": "C++",
        },
        "java": {
            "include_stmt": "",
            "main_header": "public class Main {\n    public static void main(String[] args) {",
            "main_footer": "    }\n}",
            "output_stmt": 'System.out.println("{}");',
            "output_fn": "System.out.println",
            "input_stmt": 'Scanner sc = new Scanner(System.in);\nint var = sc.nextInt();',
            "header_desc": "Java is a platform-independent, object-oriented language that runs on the JVM.",
            "platform_note": "Compiled to bytecode and executed on the Java Virtual Machine (JVM).",
            "output_example": f'System.out.println("Learning about {concept}");',
            "code_comment": "//",
            "code_template": (
                f"public class Main {{\n"
                f"    public static void main(String[] args) {{\n"
                f"        // TODO: Add {concept} example\n"
                f"        System.out.println(\"Learning about {concept}\");\n"
                f"    }}\n"
                f"}}"
            ),
            "exercise_starter": (
                f"public class Main {{\n"
                f"    public static void main(String[] args) {{\n"
                f"        // Implement {concept}\n"
                f"    }}\n"
                f"}}"
            ),
            "analogies": [
                f"Think of {concept} as a method in a Java class — it belongs to an object and can be called on instances.",
                f"Like a class in Java, {concept} defines a blueprint that determines how objects of that type behave.",
            ],
            "mistakes": [
                {
                    "mistake": f"Making the class name differ from the filename when using {concept}",
                    "fix": f"The public class name must match the filename when using {concept}",
                    "code": f"// File: Main.java but class is declared as public class WrongName",
                    "fixed_code": f"// File: Main.java must contain public class Main",
                },
                {
                    "mistake": f"Missing the main method signature when using {concept}",
                    "fix": f"The main method must be exactly: public static void main(String[] args)",
                    "code": f"// Wrong: public void main() or missing String[] args",
                    "fixed_code": f"// Correct: public static void main(String[] args)",
                },
                {
                    "mistake": f"Using == to compare Strings instead of .equals() when working with {concept}",
                    "fix": f"Always use .equals() for String comparison, never ==, when using {concept}",
                    "code": f'if (str == "value") // Wrong',
                    "fixed_code": f'if (str.equals("value")) // Correct',
                },
            ],
            "quiz_question": f"Why must the class name match the filename in Java when using {concept}?",
            "quiz_explanation": f"Java requires the public class name to match the filename so the compiler can locate and compile the source file correctly.",
            "key_takeaway_prefix": "Java",
        },
        "python": {
            "include_stmt": "",
            "main_header": "",
            "main_footer": "",
            "output_stmt": 'print("{}")',
            "output_fn": "print",
            "input_stmt": "var = int(input())",
            "header_desc": "Python is a dynamically typed, interpreted language known for readability.",
            "platform_note": "Interpreted at runtime — no compilation step needed.",
            "output_example": f'print("Learning about {concept}")',
            "code_comment": "#",
            "code_template": (
                f"# TODO: Add {concept} example\n"
                f'print("Learning about {concept}")'
            ),
            "exercise_starter": (
                f"# Implement {concept}\n"
                f"# Write your code below this line"
            ),
            "analogies": [
                f"Think of {concept} as a word in Python's simple vocabulary — it works directly without ceremony.",
                f"Like a Python dictionary entry, {concept} maps an idea to an implementation in a straightforward way.",
            ],
            "mistakes": [
                {
                    "mistake": f"Forgetting proper indentation when using {concept}",
                    "fix": f"Python uses indentation to define blocks — always indent consistently (4 spaces) when using {concept}",
                    "code": f"# Wrong: no indentation or mixed tabs/spaces",
                    "fixed_code": f"# Correct: consistent 4-space indentation",
                },
                {
                    "mistake": f"Forgetting the colon at the end of a statement when using {concept}",
                    "fix": f"Control structures in Python require a colon — : — at the end of the line, especially when using {concept}",
                    "code": f"if x == 1  # Missing colon",
                    "fixed_code": f"if x == 1:  # Colon present",
                },
                {
                    "mistake": f"Using = instead of == when comparing values with {concept}",
                    "fix": f"Use == for comparison, not = (assignment) when working with {concept}",
                    "code": f"if x = 5:  # Assignment, not comparison",
                    "fixed_code": f"if x == 5:  # Comparison",
                },
                {
                    "mistake": f" Mixing tabs and spaces in {concept} code blocks",
                    "fix": f"Use spaces only (4 per indent level) — never mix tabs and spaces when writing {concept}",
                    "code": f"# Mixed indentation",
                    "fixed_code": f"# Consistent 4-space indentation only",
                },
            ],
            "quiz_question": f"What makes Python different from C when using {concept}?",
            "quiz_explanation": f"Python is dynamically typed and interpreted, so {concept} works without explicit type declarations or compilation.",
            "key_takeaway_prefix": "Python",
        },
    }

    config = lang_configs.get(language_id, lang_configs["c"])
    lang_label = language_id.upper() if language_id != "cpp" else "C++"
    if language_id == "python":
        lang_label = "Python"
    elif language_id == "java":
        lang_label = "Java"
    elif language_id == "c":
        lang_label = "C"

    base_theory = (
        f"In this lesson, we explore {concept}. "
        f"This is an important concept in {lang_label} programming."
    )

    theory_by_type = {
        "theory": (
            f"Let us learn about {concept}. "
            f"This concept is fundamental to writing effective {lang_label} programs. "
            f"Understanding {concept} will help you write more powerful and flexible code."
        ),
        "practice": (
            f"Time to practice {concept}. The best way to learn is by writing code. "
            f"In this hands-on session, you will apply what you have learned about {concept} "
            f"to solve practical problems."
        ),
        "challenge": (
            f"Challenge yourself with {concept}. This problem will test your understanding "
            f"and push you to think creatively. Try to solve it before looking at hints!"
        ),
        "project": (
            f"Build a project using {concept}. This is your chance to create something real "
            f"that combines multiple skills into a complete program."
        ),
        "boss": (
            f"Boss battle! This comprehensive challenge tests everything you have learned "
            f"about {concept} and related topics. Show what you have mastered!"
        ),
        "quiz": (
            f"Test your knowledge of {concept} with these questions. "
            f"Quizzes help reinforce what you have learned and identify areas to review."
        ),
    }

    paragraph2 = (
        f"In {lang_label}, {concept} is a building block that you will use in almost every program. "
        f"It connects with concepts you have already learned like variables and functions. "
        f"Take your time to understand it deeply before moving on."
    )

    platform_notes = {
        "C": "Compiled and executed directly on the hardware with minimal runtime overhead.",
        "C++": "Compiled, strongly typed, and supports both procedural and OOP paradigms with the STL.",
        "Java": "Compiled to bytecode and executed on the Java Virtual Machine (JVM) for platform independence.",
        "Python": "Interpreted at runtime — no compilation step needed, making it ideal for rapid prototyping.",
    }

    analogy_count = len(config["analogies"])

    return {
        "theory": theory_by_type.get(lesson_type, base_theory),
        "analogy": (
            f"{config['analogies'][0]} "
            f"As you practice, using {concept} will become second nature."
        ),
        "sections": [
            {
                "heading": f"Understanding {concept}",
                "body": (
                    f"When working with {concept} in {lang_label}, there are several important aspects "
                    f"to consider. First, understand the basic syntax and rules. "
                    f"Then practice with simple examples. Finally, combine {concept} "
                    f"with other {lang_label} features to build more complex programs."
                ),
                "code": config["code_template"],
                "pro_tip": (
                    f"When learning {concept}, start with the simplest example and "
                    f"gradually add complexity. Test each step before moving on."
                ),
            },
            {
                "heading": f"Common uses of {concept}",
                "body": (
                    f"{concept} appears in many real-world scenarios. "
                    f"Professional {lang_label} programmers use {concept} daily in their work. "
                    f"By mastering this concept, you add another powerful skill to your toolkit."
                ),
                "pro_tip": (
                    f"The best way to master {concept} is to write at least "
                    f"three different programs that use it in different ways."
                ),
            },
            {
                "heading": f"{lang_label} Specific Notes",
                "body": (
                    f"{config['header_desc']} "
                    f"{platform_notes.get(lang_label, '')} "
                    f"Unlike lower-level languages, {lang_label} provides features that make "
                    f"using {concept} more accessible while maintaining performance."
                ),
                "pro_tip": (
                    f"Explore how {lang_label}'s standard library simplifies working with {concept}."
                ),
            },
        ],
        "code_example": {
            "code": (
                f"{config['code_comment']} {concept} example\n"
                f"{config['include_stmt']}\n"
                f"\n"
                f"{config['main_header']}\n"
                f"    {config['code_comment']} Demonstrate {concept}\n"
                f"    {config['output_example']}\n"
                f"{config['main_footer']}"
            ),
            "annotations": [
                {"line": 1, "text": f"Comment indicating this demonstrates {concept}"},
                {"line": 6, "text": "Placeholder for the actual implementation"},
            ],
        },
        "common_mistakes": config["mistakes"],
        "exercise": {
            "description": (
                f"Write a program that demonstrates {concept} in {lang_label}. "
                f"Start with a simple example and then extend it. "
                f"Test your program with different inputs to make sure it works correctly."
            ),
            "starter_code": config["exercise_starter"],
            "hints": [
                f"Start by understanding the basic {concept} syntax in {lang_label}",
                f"Test with simple inputs first",
                f"Add error handling for edge cases",
            ],
            "expected_output": f"Your program should correctly demonstrate {concept}.",
        },
        "quiz": None if lesson_type == "project" else {
            "question": config["quiz_question"],
            "options": [
                f"To organize code using {concept}",
                f"To replace variables with {concept}",
                f"To make programs run faster",
                f"To delete unnecessary code",
            ],
            "correct": 0,
            "explanation": config["quiz_explanation"],
        },
        "key_takeaways": [
            f"{concept} is an important concept in {lang_label} programming",
            f"Understanding {concept} helps you write better code",
            f"Practice with {concept} to build mastery",
            f"Combine {concept} with other features for powerful programs",
        ],
        "next_steps": f"Great progress! Keep practicing {concept} in your own {lang_label} projects.",
    }


def get_lesson_content(
    language_id: str,
    lesson_id: str,
    lesson_title: str,
    lesson_type: str,
) -> dict[str, Any]:
    """Get lesson content. Returns hand-crafted content if available, else generates from template.

    Args:
        language_id: Language identifier (e.g., 'c', 'cpp', 'python')
        lesson_id: Full lesson identifier (e.g., 'c-l01-01')
        lesson_title: The title of the lesson
        lesson_type: Type of lesson ('theory', 'practice', 'challenge', 'project', 'boss', 'quiz')

    Returns:
        Dict with keys: theory, analogy, sections, code_example, common_mistakes,
        exercise, quiz, key_takeaways, next_steps
    """
    if lesson_id in HAND_CRAFTED_LESSONS:
        return HAND_CRAFTED_LESSONS[lesson_id]

    try:
        from app.data.lesson_content_cpp import HAND_CRAFTED_CPP_LESSONS
        from app.data.lesson_content_java import HAND_CRAFTED_JAVA_LESSONS
        from app.data.lesson_content_python import HAND_CRAFTED_PYTHON_LESSONS
    except ImportError:
        HAND_CRAFTED_CPP_LESSONS = {}
        HAND_CRAFTED_JAVA_LESSONS = {}
        HAND_CRAFTED_PYTHON_LESSONS = {}

    if lesson_id in HAND_CRAFTED_CPP_LESSONS:
        return HAND_CRAFTED_CPP_LESSONS[lesson_id]
    if lesson_id in HAND_CRAFTED_JAVA_LESSONS:
        return HAND_CRAFTED_JAVA_LESSONS[lesson_id]
    if lesson_id in HAND_CRAFTED_PYTHON_LESSONS:
        return HAND_CRAFTED_PYTHON_LESSONS[lesson_id]

    if language_id == "c":
        return generate_template_content(language_id, lesson_title, lesson_type, lesson_id)

    lang_name = {"cpp": "C++", "java": "Java", "python": "Python"}.get(language_id, language_id.upper())
    return {
        "theory": f"Learn about {lesson_title} in {lang_name}.",
        "analogy": f"Think of this concept like a tool in {lang_name} programming.",
        "sections": [
            {
                "heading": f"Understanding {lesson_title}",
                "body": f"This lesson covers {lesson_title} in {lang_name}.",
                "pro_tip": f"Practice {lesson_title} regularly to build proficiency.",
            },
        ],
        "code_example": None,
        "common_mistakes": [],
        "exercise": {
            "description": f"Write a {lang_name} program that demonstrates {lesson_title}.",
            "starter_code": f"// Your {lang_name} code here\n",
            "hints": [f"Review the {lesson_title} concept before starting"],
            "expected_output": f"A working {lang_name} program demonstrating {lesson_title}.",
        },
        "quiz": None,
        "key_takeaways": [
            f"{lesson_title} is a key concept in {lang_name}",
            f"Practice using {lesson_title} in different contexts",
            f"Mastering {lesson_title} improves your {lang_name} skills",
        ],
        "next_steps": f"Continue practicing {lesson_title} in your own projects.",
    }
