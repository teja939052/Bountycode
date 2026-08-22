"""Integrate C++, Java, Python content into lesson_content.py."""
import os, shutil

SRC = r'D:\Project-Fremen\backend\app\data\lesson_content.py'
BACKUP = SRC + '.bak'

shutil.copy(SRC, BACKUP)

with open(SRC, 'r', encoding='utf-8') as f:
    content = f.read()

cpp_code = '''
# ============================================================================
# C++ LANGUAGE - Level 1 (First Steps)
# ============================================================================
HAND_CRAFTED_LESSONS.update({
"""
    "(cpp, cpp-l01-01)": (
        "What is C++?",
        "C++ is a powerful programming language created by Bjarne Stroustrup in 1979. "
        "It builds on top of the C language but adds object-oriented programming features. "
        "Think of it like C with superpowers.",
        [
            {
                "heading": "Why Learn C++?",
                "body": "C++ is used in game engines, operating systems, browsers, and anywhere performance matters. "
                        "It gives you both low-level control and high-level features.",
                "pro_tip": "If you know C, C++ will feel familiar but with a lot more tools in your belt.",
            },
            {
                "heading": "The C++ Ecosystem",
                "body": "C++ is everywhere — from your smartphone's OS to game engines like Unity and Unreal Engine. "
                        "Learning C++ opens doors to systems programming, game development, and high-performance computing.",
                "pro_tip": "Focus on understanding pointers and memory management — these are what set C++ apart.",
            },
        ],
        None,
        None,
        None,
        [
            "C++ is an extension of C with object-oriented features",
            "Learning C++ makes you a stronger programmer in any language",
            "C++ gives you fine-grained control over memory and performance",
        ],
        "Ready to move to the next level? Your first C++ program awaits!",
    ),
    "(cpp, cpp-l01-02)": (
        "Your First C++ Program",
        "Let us write hello world in C++",
        [
            {
                "heading": "Breaking Down the Code",
                "body": "Every C++ program starts with #include for libraries, then a main function where execution begins.",
            },
            {
                "heading": "The cout Arrow",
                "body": "In C, we use printf(). In C++, we use cout with the << operator. The << means \\\"send to output\\\".",
                "pro_tip": "Think of << as an arrow pointing data out of the program to the screen.",
            },
        ],
        {
            "code": "#include <iostream>\\nusing namespace std;\\n\\nint main() {\\n    cout << \\\"Hello, World!\\\" << endl;\\n    return 0;\\n}",
            "annotations": [
                {"line": 1, "text": "Includes the iostream library for input/output"},
                {"line": 2, "text": "Avoids typing std:: before every standard library object"},
                {"line": 3, "text": "Empty line for readability"},
                {"line": 4, "text": "Main function — entry point of every C++ program"},
                {"line": 5, "text": "cout << sends text to the terminal. << endl adds a newline and flushes the output"},
                {"line": 6, "text": "Return 0 means the program finished successfully"},
            ],
        },
        [
            {"mistake": "Forgetting #include <iostream>", "fix": "Always include it for cout/cin", "code": "// compiler error: cout was not declared", "fixed_code": "#include <iostream>"},
            {"mistake": "Forgetting using namespace std", "fix": "Add the line or write std::cout", "code": "cout << \\\"Hello\\\";", "fixed_code": "std::cout << \\\"Hello\\\";"},
            {"mistake": "Using printf() like in C", "fix": "Use cout << ... << endl in C++", "code": "printf(\\\"Hello\\\");", "fixed_code": "cout << \\\"Hello\\\" << endl;"},
        ],
        {
            "description": "Write a program that prints your name and age on separate lines.",
            "starter_code": "#include <iostream>\\nusing namespace std;\\n\\nint main() {\\n    // Print your name and age\\n    return 0;\\n}",
            "hints": ["Use cout << for each line", "End each line with << endl"],
            "expected_output": "YourName\\nYourAge",
        },
        None,
        [
            "C++ uses << (insertion operator) for output instead of printf()",
            "endl both adds a newline and flushes the output buffer",
            "Always include <iostream> for console I/O",
        ],
        "You just wrote your first C++ program! Next learn about variables.",
    ),
})
'''

java_code = '''
# ============================================================================
# JAVA LANGUAGE - Level 1 (First Steps)
# ============================================================================
HAND_CRAFTED_LESSONS.update({
"""
    "(java, java-l01-01)": (
        "What is Java?",
        "Java is a general-purpose programming language created by James Gosling at Sun Microsystems in 1995. "
        "It follows the \\\"Write Once, Run Anywhere\\\" (WORA) principle — Java code compiles to bytecode that runs on "
        "the Java Virtual Machine (JVM), making it platform independent.",
        [
            {
                "heading": "Why Learn Java?",
                "body": "Java is used in Android apps, enterprise systems, web servers, and banking software. "
                        "It is one of the most popular languages for job placement, ranking consistently in the top 3.",
                "pro_tip": "Java's static typing catches errors at compile time, making your code more reliable.",
            },
            {
                "heading": "The JVM Advantage",
                "body": "When you compile Java, it becomes bytecode, not machine code. The JVM (Java Virtual Machine) "
                        "interprets this bytecode on any platform — Windows, Mac, Linux — hence \\\"Write Once, Run Anywhere\\\".",
                "pro_tip": "Think of the JVM as a universal translator: your Java code speaks to the JVM, which speaks to any OS.",
            },
        ],
        None,
        None,
        None,
        [
            "Java is platform-independent thanks to the JVM",
            "Java is statically typed — variable types must be declared",
            "Every Java program needs a class with a main method",
        ],
        "Let us dive into writing your first Java program!",
    ),
    "(java, java-l01-02)": (
        "Your First Java Program",
        "A Java program is always organized inside a class. The main method is where execution starts.",
        [
            {
                "heading": "The anatomy of a Java class",
                "body": "Every Java file contains at least one class. The class holds your methods and data.",
            },
            {
                "heading": "System.out.println()",
                "body": "In C, you use printf(). In Java, you use System.out.println(). "
                        "System is a class, out is a PrintStream object, and println() prints a line.",
                "pro_tip": "Read it left to right: System (class) . out (object) . println() (method).",
            },
        ],
        {
            "code": "public class Main {\\n    public static void main(String[] args) {\\n        System.out.println(\\\"Hello, World!\\\");\\n    }\\n}",
            "annotations": [
                {"line": 1, "text": "Defines a public class named Main (filename must match)"},
                {"line": 2, "text": "The main method — entry point of every Java application"},
                {"line": 3, "text": "System.out.println() prints text to the console with a newline"},
                {"line": 4, "text": "Closing brace of main method"},
                {"line": 5, "text": "Closing brace of class"},
            ],
        },
        [
            {"mistake": "Class name doesn't match filename", "fix": "Save as Main.java when the class is named Main", "code": "class Main { } // but saved as Test.java", "fixed_code": "Save as Main.java"},
            {"mistake": "Forgetting public static void", "fix": "main must be exactly: public static void main(String[] args)", "code": "void main(String[] args)", "fixed_code": "public static void main(String[] args)"},
            {"mistake": "Using printf() like in C", "fix": "Use System.out.println() in Java", "code": "printf(\\\"Hello\\\");", "fixed_code": "System.out.println(\\\"Hello\\\");"},
        ],
        {
            "description": "Write a Java program that prints your name and a welcome message.",
            "starter_code": "public class Main {\\n    public static void main(String[] args) {\\n        // Print your name and welcome\\n    }\\n}",
            "hints": ["Use System.out.println() to print", "Each println creates a new line"],
            "expected_output": "YourName\\nWelcome to Java!",
        },
        None,
        [
            "Java is organized inside classes",
            "System.out.println() is how you print to console",
            "The main method signature must be exact: public static void main(String[] args)",
        ],
        "Great start with Java! Now learn about variables.",
    ),
})
'''

python_code = '''
# ============================================================================
# PYTHON LANGUAGE - Level 1 (First Steps)
# ============================================================================
HAND_CRAFTED_LESSONS.update({
"""
    "(python, python-l01-01)": (
        "What is Python?",
        "Python is a high-level, interpreted programming language created by Guido van Rossum in 1991. "
        "Known for its simple, readable syntax that resembles English, Python is the most popular language "
        "for beginners and is widely used in AI, web development, and data science.",
        [
            {
                "heading": "Why Learn Python?",
                "body": "Python consistently ranks as the #1 most beginner-friendly language. "
                        "It is used at Google, Netflix, NASA, and in virtually every AI and data science project. "
                        "With Python, you can build almost anything.",
                "pro_tip": "Python's simplicity lets you focus on learning programming concepts without getting "
                           "bogged down in complex syntax.",
            },
            {
                "heading": "Python is Interpreted",
                "body": "Unlike C or C++ which need compilation, Python runs line by line. "
                        "This means you can experiment instantly — type code, see results, no waiting.",
                "pro_tip": "This makes Python perfect for learning! You get instant feedback on every line.",
            },
        ],
        None,
        None,
        None,
        [
            "Python has the simplest syntax of any programming language",
            "No semicolons or curly braces — indentation defines code blocks",
            "Python is interpreted so you get instant results",
            "Used everywhere: AI, web, data science, automation",
        ],
        "Let us write your first Python program — it only takes one line!",
    ),
    "(python, python-l01-02)": (
        "Your First Python Program",
        "In Python, you can print something with just the print() function. "
        "No semicolons, no includes, no main function — just pure simplicity.",
        [
            {
                "heading": "The print() Function",
                "body": "Python's print() function works like printf() in C and System.out.println() in Java, "
                        "but much simpler. You just write what you want to print inside parentheses.",
                "pro_tip": "Python was designed to be readable. Code reads almost like English!",
            },
            {
                "heading": "No Semicolons Needed",
                "body": "Unlike C, C++, or Java, Python does not use semicolons to end statements. "
                        "Each line is a complete statement on its own.",
                "pro_tip": "If you come from C/Java, this is the biggest relief! Python just runs.",
            },
        ],
        {
            "code": "print(\\\"Hello, World!\\\")",
            "annotations": [
                {"line": 1, "text": "print() outputs text to the console"},
                {"line": 1, "text": "The text goes inside quotes — \\\"\\\" for a string"},
                {"line": 1, "text": "No semicolon, no #include, no main() — that is it!"},
            ],
        },
        None,
        {
            "description": "Write a Python program that prints your name, age, and city — each on a new line.",
            "starter_code": "# Print your information\\n# Use print() for each line\\n",
            "hints": ["Use print() for each line of output", "Python does not need semicolons"],
            "expected_output": "YourName\\nYourAge\\nYourCity",
        },
        None,
        [
            "Python's syntax is the simplest of any language",
            "print() works without any imports or setup",
            "No semicolons, no curly braces — just clean readable code",
        ],
        "Python is so simple that you have already started! Next, let us learn about variables.",
    ),
})
'''

# Find insertion points: add C++ after C lessons, Java after C++, Python after Java
# Find where the C lessons section ends and the template section begins
# We'll append to the HAND_CRAFTED_LESSONS.update({ block

# Find the end of the C content and the start of generate_template_content
c_end_marker = '    ("c-l03-10"'  # last C lesson key
c_end_idx = content.find(c_end_marker)
if c_end_idx == -1:
    print("Could not find C content end marker, using search instead")
else:
    # Find the end of the C lesson's content (closing of the dict entry)
    # The C lessons are in HAND_CRAFTED_LESSONS.update({...})
    # We need to find the closing of that dict and add C++/Java/Python there

    # Actually, let's just find the HAND_CRAFTED_LESSONS.update({ and add after the closing }
    # before the next section

    # Find "def generate_template_content"
    gen_idx = content.find('def generate_template_content(')
    if gen_idx == -1:
        print("Could not find generate_template_content function")
    else:
        # We need to insert C++/Java/Python content BEFORE generate_template_content
        # Find where HAND_CRAFTED_LESSONS.update({...}) ends and the template section begins

        # Look for the closing pattern before generate_template_content
        # The structure is: HAND_CRAFTED_LESSONS.update({ ... }); then blank lines then "def generate..."

        # Let's find a good insertion point: right before "def generate_template_content"
        # Go back to find a good place (after the last C entry closing brace)

        # Find the last closing brace before generate_template_content
        section_before = content[:gen_idx]

        # Find the last standalone ) or }) before generate_template_content
        last_brace = section_before.rfind(')')
        last_dict_close = section_before.rfind('}')

        # The HAND_CRAFTED_LESSONS.update({...}) ends with })
        # We want to insert after the }) of HAND_CRAFTED_LESSONS.update(
        # But actually the C content is the only thing in that update yet

        # Let's just append new updates after the existing HAND_CRAFTED_LESSONS.update call
        # Find the _lesson function definition line and look for all update block endings

        # SIMPLEST APPROACH: Find the closing of HAND_CRAFTED_LESSONS.update({...})
        # That should end before generate_template_content

        # Let's find the last line that closes the dict
        # Since the insert is complex, let's just do it at the gen_idx point carefully

        # Actually, the cleanest solution: just replace
        # We'll insert the content right before "def generate_template_content"
        # But we need to make sure we close the first HAND_CRAFTED_LESSONS.update({{...}} call

        # The simplest approach: find all the update calls and add new ones.
        # Actually HAND_CRAFTED_LESSONS is just a dict that we update incrementally.

        # The current C content uses HAND_CRAFTED_LESSONS.update({...}) at the end of a large block.
        # Let me just insert the new languages' content AFTER the C block's closing brace
        # and BEFORE def generate_template_content

        # Let me check if the C update block is properly closed already
        update_start = section_before.rfind('HAND_CRAFTED_LESSONS.update')
        print(f"HAND_CRAFTED_LESSONS.update starts at position {update_start}")
        print(f"generate_template_content at position {gen_idx}")
        print(f"Section between them length: {gen_idx - update_start}")

        # Let's just insert before generate_template_content,
        # and check if we need an additional .update() call or if we extend the existing one

        # Actually the simplest: find the last }) before generate_template_content
        # and insert after it

        insert_point = gen_idx
        # Go back to find ")\n" or "})\n" that is the end of update call
        # The C update block ends with: })\n\n# then blank lines then def generate...

        # Let's look at what's just before generate_template_content
        pre_gen = content[max(0, gen_idx-200):gen_idx]
        print(f"Content before generate_template_content (last 200 chars):")
        print(repr(pre_gen[-200:]))

PYEOF