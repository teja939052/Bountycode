"""Hand-crafted lesson content for Java levels 1-3.

Lesson ID format: java-l{level:02d}-{lesson:02d}
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


HAND_CRAFTED_JAVA_LESSONS: dict[str, dict[str, Any]] = {}

HAND_CRAFTED_JAVA_LESSONS.update(dict([
    # =========================================================================
    # LEVEL 1: FIRST STEPS
    # =========================================================================
    _lesson(
        lesson_id="java-l01-01",
        theory=(
            "Java is a high-level, object-oriented programming language created by James Gosling "
            "and his team at Sun Microsystems, first released in 1995. It follows a "
            "write once, run anywhere philosophy: compiled Java code runs on any device that has "
            "a Java Virtual Machine (JVM). Today Java powers Android apps, enterprise banking "
            "systems, web backends built with Spring Boot, and big-data tools like Hadoop."
        ),
        analogy=(
            "Learning Java is like learning to cook in a professional kitchen. The recipe "
            "(your source code) can be cooked in any kitchen that has a stove (the JVM) without "
            "changing a single ingredient. Once you learn the core recipes, you can cook "
            "anything from a street snack (an Android app) to a five-star banquet (an enterprise "
            "banking system)."
        ),
        sections=[
            {
                "heading": "Why learn Java?",
                "body": (
                    "Java is one of the most widely used languages on the planet. It is the "
                    "default choice for Android development, the backbone of most large banks and "
                    "insurance companies, and the language behind popular frameworks like Spring "
                    "Boot and Hibernate. This means a steady stream of job openings for Java "
                    "developers around the world."
                ),
                "pro_tip": (
                    "Java has ranked in the top 3 of the TIOBE index for over 25 years and is one "
                    "of the top languages for campus placements in India."
                ),
            },
            {
                "heading": "Write once, run anywhere",
                "body": (
                    "You write Java in a .java source file, then compile it into bytecode with "
                    "the javac compiler. Bytecode is not machine code; it is a platform-neutral "
                    "instruction set that the JVM executes. Because of this, the same compiled "
                    "program runs on Windows, macOS, Linux, and even inside a browser without "
                    "being recompiled."
                ),
                "pro_tip": (
                    "The JVM is not just for Java: languages like Kotlin, Scala, and Groovy also "
                    "compile to bytecode and run on it."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        System.out.println(\"Java version: \" + System.getProperty(\"java.version\"));\n"
            "    }\n"
            "}",
            [
                {"line": 1, "text": "Declares a class named Main; the file must be called Main.java"},
                {"line": 2, "text": "The main method is where the JVM starts executing"},
                {"line": 3, "text": "Prints the Java version running on this machine"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "Saving the file as main.java or MAIN.JAVA",
                "fixed": "Saving it as Main.java, matching the public class name exactly",
                "why": "The file name must match the public class name and case on most systems.",
            },
            {
                "wrong": "Saving the source code as Main.txt and running it",
                "fixed": "Saving the source as Main.java",
                "why": "The Java compiler only recognises .java source files.",
            },
            {
                "wrong": "Believing compiled Java runs directly on the hardware",
                "fixed": "Understanding bytecode runs on the JVM, not the CPU",
                "why": "Java compiles to bytecode which the JVM interprets or JIT-compiles.",
            },
        ],
        exercise={
            "description": "Write a complete Java program that prints the text: Java is my first language!",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        // Your code here\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "Use System.out.println(\"Java is my first language!\"); to print the line",
                "Remember the semicolon at the end of the statement",
                "The class must be named Main so the program compiles",
            ],
            "expected_output": "Java is my first language!",
        },
        quiz={
            "question": "Who created Java?",
            "options": ["Dennis Ritchie", "Bjarne Stroustrup", "James Gosling", "Guido van Rossum"],
            "correct": 2,
            "explanation": "James Gosling and his team at Sun Microsystems created Java in the early 1990s.",
        },
        key_takeaways=[
            "Java is an object-oriented language created by James Gosling in 1995",
            "Java follows write once, run anywhere through the JVM",
            "Java powers Android, enterprise systems, and web backends",
            "You write .java files, compile to bytecode, and run it on the JVM",
        ],
        next_steps="Ready to write your first Java program and watch it run? Let us move on!",
    ),

    _lesson(
        lesson_id="java-l01-02",
        theory=(
            "Every Java program begins inside a class, and execution starts from a special method "
            "called main. The line public static void main(String[] args) is the exact entry "
            "point the JVM looks for, so it must be typed precisely. System.out.println(\"Hello, "
            "World!\") sends text to the console followed by a new line, and every statement in "
            "Java ends with a semicolon ;."
        ),
        analogy=(
            "Your program is a play. public class Main is the theatre building, the main method "
            "is the stage entrance, and System.out.println is the actor speaking your lines to "
            "the audience (the console). The semicolon is the full stop that ends every spoken "
            "sentence."
        ),
        sections=[
            {
                "heading": "Anatomy of Hello World",
                "body": (
                    "public means the class is accessible from anywhere. static means main belongs "
                    "to the class itself, so the JVM can call it without creating an object. void "
                    "means the method returns nothing. The parameter String[] args lets you pass "
                    "command-line arguments later."
                ),
                "pro_tip": (
                    "Because Main is public, the file must be named Main.java or javac will "
                    "refuse to compile it."
                ),
            },
            {
                "heading": "Running your program",
                "body": (
                    "First compile: javac Main.java. This creates a Main.class bytecode file. "
                    "Then run: java Main. Notice you run java Main, not java Main.class or "
                    "java Main.java."
                ),
                "pro_tip": (
                    "In most code editors you can skip the terminal entirely and just press the "
                    "Run button; the same two steps happen behind the scenes."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        System.out.println(\"Hello, World!\");\n"
            "    }\n"
            "}",
            [
                {"line": 1, "text": "Class declaration; filename must be Main.java"},
                {"line": 2, "text": "The exact main signature the JVM looks for"},
                {"line": 3, "text": "Prints Hello, World! followed by a new line"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "public static void main() {",
                "fixed": "public static void main(String[] args) {",
                "why": "The JVM requires the exact parameter list String[] args as the entry point.",
            },
            {
                "wrong": "public static void Main(String[] args) {",
                "fixed": "public static void main(String[] args) {",
                "why": "Java is case-sensitive; the method must be lowercase main.",
            },
            {
                "wrong": "System.out.println(\"Hello\")",
                "fixed": "System.out.println(\"Hello\");",
                "why": "Every statement must end with a semicolon in Java.",
            },
        ],
        exercise={
            "description": "Modify the Hello World program to print Hello, World! on the first line and your name on the second line.",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        // Your code here\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "Use System.out.println(\"Hello, World!\"); for the first line",
                "Add a second System.out.println line with your name",
                "Every statement ends with a semicolon",
            ],
            "expected_output": (
                "Hello, World!\n"
                "<your name>"
            ),
        },
        quiz={
            "question": "What is the entry point of every Java program?",
            "options": [
                "public static void main(String[] args)",
                "public void run()",
                "public static void start()",
                "private void init()",
            ],
            "correct": 0,
            "explanation": "The JVM always begins executing at the exact signature public static void main(String[] args).",
        },
        key_takeaways=[
            "Every Java program needs a class and a main method",
            "The main signature must be exactly public static void main(String[] args)",
            "System.out.println prints text to the console",
            "Every statement ends with a semicolon",
        ],
        next_steps="Now let us dig deeper into classes and the main method!",
    ),

    _lesson(
        lesson_id="java-l01-03",
        theory=(
            "A class is a blueprint that groups related code together, and in Java every program "
            "must be wrapped in at least one class. The main method is the JVM's starting point; "
            "without it the program cannot run. You can also define your own methods inside the "
            "class and call them from main, which keeps your code organized and reusable."
        ),
        analogy=(
            "A class is like a house plan and the main method is the front door. No matter how "
            "many rooms (methods) the house has, visitors always enter through the front door. "
            "The builder (JVM) ignores everything until it finds that door and walks through it."
        ),
        sections=[
            {
                "heading": "Classes are the building blocks",
                "body": (
                    "Every line of Java lives inside a class. A file can have several classes, but "
                    "only one public class, and that class must share its name with the file. The "
                    "public keyword means other classes can use it."
                ),
                "pro_tip": (
                    "Keep your file name and public class name identical, letter for letter, to "
                    "avoid compile errors."
                ),
            },
            {
                "heading": "Calling methods from main",
                "body": (
                    "Once you define a static method like greet() inside your class, main can call "
                    "it simply by writing its name followed by parentheses. The method's code runs "
                    "and then control returns to main. This is how big programs are built: many "
                    "small methods, each doing one thing."
                ),
                "pro_tip": (
                    "Because main is static, it can only call other static methods directly. "
                    "Instance methods need an object first; you will meet those with classes later."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        greet();\n"
            "    }\n"
            "\n"
            "    static void greet() {\n"
            "        System.out.println(\"Welcome to Java!\");\n"
            "    }\n"
            "}",
            [
                {"line": 1, "text": "The public class Main, matching the file name"},
                {"line": 2, "text": "The main method, entry point of the program"},
                {"line": 3, "text": "Calls the greet method defined below"},
                {"line": 6, "text": "A custom static method named greet"},
                {"line": 7, "text": "Prints a message when greet() is called"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "File Main.java contains: class Helper { ... }",
                "fixed": "Making the public class in the file named Main",
                "why": "The public class name must match the file name.",
            },
            {
                "wrong": "Writing a program with no main method at all",
                "fixed": "Adding public static void main(String[] args)",
                "why": "Without main, there is no entry point and the JVM cannot start the program.",
            },
            {
                "wrong": "Calling greet() from main but defining greet in another file",
                "fixed": "Defining greet in the same class, or importing the other class",
                "why": "Methods must be visible to the calling code, usually in the same class or package.",
            },
        ],
        exercise={
            "description": "Add a method named wish() that prints Good luck for your placement drive! and call it from main.",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        // Call your wish method here\n"
                "    }\n"
                "\n"
                "    // Define the wish method here\n"
                "}"
            ),
            "hints": [
                "Define the method like this: static void wish() { ... }",
                "Inside the braces, print the message with System.out.println",
                "Call it from main using wish();",
            ],
            "expected_output": "Good luck for your placement drive!",
        },
        quiz={
            "question": "Which statement about a public class is true?",
            "options": [
                "The file name must match the public class name",
                "It can never contain methods",
                "A file can have two public classes",
                "Its name must start with a lowercase letter",
            ],
            "correct": 0,
            "explanation": "The public class name must match the file name so javac can find it.",
        },
        key_takeaways=[
            "Every Java program lives inside at least one class",
            "main is the entry point and must exist for a program to run",
            "You can define your own methods and call them from main",
            "The public class name must match the file name",
        ],
        next_steps="Now let us master printing with System.out.println!",
    ),

    _lesson(
        lesson_id="java-l01-04",
        theory=(
            "System.out is the standard output stream that points to your console, and println "
            "prints a message followed by a new line. Its cousin print prints without moving to a "
            "new line, which is perfect for prompts. You can print text, numbers, and expressions "
            "by combining them with the + operator."
        ),
        analogy=(
            "System.out.println is like typing on an old typewriter: println presses the carriage "
            "return after every line, while print leaves the carriage in place so the next text "
            "continues on the same line. The result is tidy, aligned output instead of a messy "
            "wall of text."
        ),
        sections=[
            {
                "heading": "println vs print",
                "body": (
                    "System.out.println(\"one\"); followed by System.out.println(\"two\"); prints "
                    "one and then two on separate lines. Using System.out.print instead keeps "
                    "everything on a single line. Mixed together, print lays the foundation and "
                    "println finishes the sentence."
                ),
                "pro_tip": (
                    "print is ideal for prompts like Enter your name: so the user types on the "
                    "same line as the question."
                ),
            },
            {
                "heading": "Printing different things",
                "body": (
                    "println works with text inside double quotes, numbers, variables, and whole "
                    "expressions. When you write \"Score: \" + 95, the + joins the text and number "
                    "into one string. Java converts the number to text for you."
                ),
                "pro_tip": (
                    "Parentheses matter: \"Sum: \" + (a + b) prints the computed sum, while "
                    "\"Sum: \" + a + b joins the numbers as text (for example 12 + 4 becomes 124)."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        System.out.println(\"Line one\");\n"
            "        System.out.println(\"Line two\");\n"
            "        System.out.print(\"No newline here. \");\n"
            "        System.out.println(\"This stays on the same line!\");\n"
            "    }\n"
            "}",
            [
                {"line": 3, "text": "Prints Line one and moves to a new line"},
                {"line": 5, "text": "Prints without a newline at the end"},
                {"line": 6, "text": "Continues on the same line as the previous print"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "System.out.println('Hello');",
                "fixed": "System.out.println(\"Hello\");",
                "why": "Single quotes are for char values; text must use double quotes.",
            },
            {
                "wrong": "System.out.println Hello;",
                "fixed": "System.out.println(\"Hello\");",
                "why": "println is a method, so its argument must be inside parentheses.",
            },
            {
                "wrong": "System.out.Println(\"Hi\");",
                "fixed": "System.out.println(\"Hi\");",
                "why": "Java is case-sensitive; Println with a capital P does not exist.",
            },
        ],
        exercise={
            "description": "Print Java is fun! on the first line and Keep practicing daily on the second line.",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        // Your code here\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "Use System.out.println for each message",
                "Each message goes inside double quotes",
                "End every statement with a semicolon",
            ],
            "expected_output": (
                "Java is fun!\n"
                "Keep practicing daily"
            ),
        },
        quiz={
            "question": "What does System.out.print do compared to println?",
            "options": [
                "Prints text and moves to a new line",
                "Prints text without adding a new line",
                "Clears the console screen",
                "Reads input from the keyboard",
            ],
            "correct": 1,
            "explanation": "print writes text but does not append a newline, so the next output continues on the same line.",
        },
        key_takeaways=[
            "println prints followed by a new line; print prints without one",
            "Use double quotes for text and single quotes for char values",
            "The + operator joins text, numbers, and expressions into one string",
            "Java is case-sensitive: System.out.println must be exact",
        ],
        next_steps="Now let us understand the JDK, JRE, and JVM that make all of this run!",
    ),

    _lesson(
        lesson_id="java-l01-05",
        theory=(
            "The JVM (Java Virtual Machine) is the engine that executes Java bytecode, which is "
            "what makes Java platform-independent. The JRE (Java Runtime Environment) bundles the "
            "JVM together with the core class libraries needed to run programs. The JDK (Java "
            "Development Kit) adds the compiler (javac), debugger, and other tools on top of the "
            "JRE, making it the full toolkit for developers."
        ),
        analogy=(
            "Think of the JDK as a fully equipped workshop, the JRE as the finished machines "
            "rolling out of it, and the JVM as the motor inside each machine. To build a product "
            "you need the workshop; to use a product you only need the machine. Every Java "
            "developer installs the JDK, while end users only need the JRE."
        ),
        sections=[
            {
                "heading": "The three layers",
                "body": (
                    "The JVM is a program that runs on your operating system and executes bytecode. "
                    "The JRE wraps the JVM with the libraries (like java.util and java.lang) that "
                    "your programs use. The JDK wraps the JRE with development tools: javac to "
                    "compile, java to run, and javadoc to generate documentation."
                ),
                "pro_tip": (
                    "You only need the JRE to run someone else's Java application, but you need "
                    "the JDK to compile your own code."
                ),
            },
            {
                "heading": "Bytecode, the universal language",
                "body": (
                    "When you run javac Main.java, your source code becomes Main.class bytecode. "
                    "This bytecode is identical on every platform. Each platform has its own JVM "
                    "that translates the bytecode into that machine's instructions, so your "
                    "compiled program runs anywhere."
                ),
                "pro_tip": (
                    "Check javac -version in your terminal to confirm the JDK is installed before "
                    "you start."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        System.out.println(\"Java version: \" + System.getProperty(\"java.version\"));\n"
            "        System.out.println(\"OS name: \" + System.getProperty(\"os.name\"));\n"
            "    }\n"
            "}",
            [
                {"line": 3, "text": "Reads the Java runtime version via a system property"},
                {"line": 4, "text": "Reads the operating system name at runtime"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "javac Main.class",
                "fixed": "javac Main.java then java Main",
                "why": "javac compiles source (.java) files; java runs the compiled class.",
            },
            {
                "wrong": "Believing the JDK is smaller than the JRE",
                "fixed": "Understanding the JDK contains the JRE plus development tools",
                "why": "The JDK is a superset: JRE + javac + debugger + utilities.",
            },
            {
                "wrong": "Trying to compile with only the JRE installed",
                "fixed": "Installing the JDK, which provides javac",
                "why": "The compiler javac ships with the JDK, not the JRE.",
            },
        ],
        exercise={
            "description": "Write a program that prints the name of your operating system using System.getProperty(\"os.name\").",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        // Your code here\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "Call System.getProperty(\"os.name\") to get the OS name",
                "Join it with text using + and print with System.out.println",
                "The output will look like: OS: Windows 10",
            ],
            "expected_output": "OS: <your operating system name>",
        },
        quiz={
            "question": "Which component contains the compiler javac?",
            "options": ["JVM", "JRE", "JDK", "Bytecode"],
            "correct": 2,
            "explanation": "The JDK (Java Development Kit) bundles the JRE plus development tools like javac.",
        },
        key_takeaways=[
            "The JVM executes bytecode, making Java platform-independent",
            "The JRE is the JVM plus the core runtime libraries",
            "The JDK adds the compiler, debugger, and tools on top of the JRE",
            "javac compiles .java files; java runs the compiled bytecode",
        ],
        next_steps="Let us make our code clearer by learning about comments!",
    ),

    _lesson(
        lesson_id="java-l01-06",
        theory=(
            "Comments are human-readable notes in your code that the compiler completely ignores. "
            "Java has three kinds: single-line // comments, multi-line /* ... */ comments, and "
            "documentation /** ... */ (Javadoc) comments. Good comments explain why the code "
            "exists, not what it does, because the code itself already shows what it does."
        ),
        analogy=(
            "Comments are like sticky notes on a recipe: they remind you why you use a certain "
            "ingredient or which step matters most. The kitchen robot (compiler) completely "
            "ignores the notes, but they help the next cook (your teammate) understand your "
            "thinking without reading your mind."
        ),
        sections=[
            {
                "heading": "Three ways to comment",
                "body": (
                    "Use // for short notes that fit on one line. Use /* ... */ when the note "
                    "spans several lines, and use /** ... */ to document classes and methods so "
                    "the javadoc tool can generate HTML documentation from your code. The compiler "
                    "skips all three."
                ),
                "pro_tip": (
                    "Your editor will usually colour comments grey or green so you can instantly "
                    "tell which lines are ignored."
                ),
            },
            {
                "heading": "Comment hygiene",
                "body": (
                    "A great comment answers why: why this approach, why this magic number, why "
                    "this edge case matters. A useless comment repeats the code, like saying "
                    "// increments i right above i++. Write comments that save the next developer "
                    "time, not ones that pad the file."
                ),
                "pro_tip": (
                    "If you change your code, update its comments in the same edit. Stale comments "
                    "that contradict the code are worse than no comments at all."
                ),
            },
        ],
        code_example=_code(
            "// This is a single-line comment.\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        // The compiler ignores this line.\n"
            "        System.out.println(\"Comments do not print.\"); // trailing comment\n"
            "        /*\n"
            "           A multi-line comment.\n"
            "           Still ignored.\n"
            "        */\n"
            "    }\n"
            "}",
            [
                {"line": 1, "text": "A single-line comment above the class"},
                {"line": 4, "text": "A single-line comment inside the method"},
                {"line": 5, "text": "A trailing comment after a statement"},
                {"line": 6, "text": "A multi-line comment block opens"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "System.out.println(\"http://java.example.com\");",
                "fixed": "The // inside the string is part of the text, not a comment",
                "why": "Comment markers inside double quotes belong to the string and print normally.",
            },
            {
                "wrong": "/* outer /* inner */ still code */",
                "fixed": "Using separate comment blocks: /* outer */ and /* inner */",
                "why": "Block comments do not nest; the first */ ends the comment.",
            },
            {
                "wrong": "/* a comment that never gets closed",
                "fixed": "/* a comment */ closed properly",
                "why": "An unclosed block comment silently swallows every line after it.",
            },
        ],
        exercise={
            "description": "Add three comments to the program: a single-line comment at the top, a multi-line comment before the print statement, and a trailing comment on the print line.",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        System.out.println(\"Comments help us explain code.\");\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "Use // at the very top for a single-line comment",
                "Use /* and */ around a multi-line comment",
                "A trailing comment sits on the same line as the print statement",
            ],
            "expected_output": "Comments help us explain code.",
        },
        quiz={
            "question": "Which comment type is used for Javadoc documentation?",
            "options": ["//", "/* */", "/** */", "#"],
            "correct": 2,
            "explanation": "Javadoc comments start with /** and end with */, and the javadoc tool reads them.",
        },
        key_takeaways=[
            "Comments are ignored by the compiler",
            "Use // for single lines, /* */ for blocks, /** */ for Javadoc",
            "Good comments explain why, not what",
            "Comment markers inside strings are just text",
        ],
        next_steps="Time for your first real practice: build a Greeting Program!",
    ),

    _lesson(
        lesson_id="java-l01-07",
        theory=(
            "A greeting program combines everything you have learned: a class, a main method, and "
            "print statements. This practice lesson asks you to write a program that welcomes a "
            "user in your own style. Practice builds muscle memory, so type every line yourself "
            "instead of copy-pasting, and run your program after each change to catch errors "
            "early."
        ),
        analogy=(
            "Writing your first programs is like learning to write by hand: you cannot become "
            "fluent just by reading essays. Each program you type is a letter you write, and "
            "every mistake you fix makes the next letter smoother. By the end you will write "
            "without even thinking about semicolons."
        ),
        sections=[
            {
                "heading": "Your first original program",
                "body": (
                    "Start from the skeleton: a class named Main with a main method. Inside main, "
                    "use System.out.println for each line of your greeting. Try three lines: a "
                    "welcome message, your name, and an encouraging note. Run it and admire your "
                    "work."
                ),
                "pro_tip": (
                    "Run your program after every single change. Small runs make bugs obvious "
                    "and easy to fix."
                ),
            },
            {
                "heading": "Experiment freely",
                "body": (
                    "This program cannot break anything, so experiment. Print a random thought, "
                    "remove a semicolon on purpose and read the error, swap the order of your "
                    "lines. Understanding error messages is a superpower; beginners who fear "
                    "errors learn half as fast."
                ),
                "pro_tip": (
                    "The compiler points at the exact line and column of an error. Read the "
                    "message, fix it, and rerun; debugging is part of the craft."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        System.out.println(\"Welcome to PlacementPro!\");\n"
            "        System.out.println(\"Your coding journey starts today.\");\n"
            "        System.out.println(\"Stay consistent and keep learning!\");\n"
            "    }\n"
            "}",
            [
                {"line": 3, "text": "A welcome line from the platform"},
                {"line": 4, "text": "A motivational line for the journey"},
                {"line": 5, "text": "An encouraging closing line"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "System.out.println(\"Hi\");)",
                "fixed": "System.out.println(\"Hi\");",
                "why": "Every opening parenthesis must have exactly one closing parenthesis.",
            },
            {
                "wrong": "class 1Greeting { ... }",
                "fixed": "class Greeting { ... }",
                "why": "Java identifiers cannot start with a digit.",
            },
            {
                "wrong": "System.out.println(\"He said \"hi\" to me\");",
                "fixed": "System.out.println(\"He said \\\"hi\\\" to me\");",
                "why": "Double quotes inside a string must be escaped with a backslash.",
            },
        ],
        exercise={
            "description": "Write a program that prints a three-line greeting: a welcome line, your name, and an encouraging message.",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        // Your code here\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "Print each line with its own System.out.println call",
                "Line two should be your name, like My name is Priya",
                "End each statement with a semicolon",
            ],
            "expected_output": (
                "Welcome, future developer!\n"
                "My name is <your name>\n"
                "Keep practising every day"
            ),
        },
        quiz={
            "question": "What character ends every statement in Java?",
            "options": [".", ",", ";", ":"],
            "correct": 2,
            "explanation": "Java statements are terminated with a semicolon ;.",
        },
        key_takeaways=[
            "A greeting program uses a class, a main method, and print statements",
            "Type code yourself to build muscle memory",
            "Run your program often to catch errors early",
            "Read error messages; they point at the exact problem",
        ],
        next_steps="Feeling brave? Let us tackle the Mini Calculator challenge!",
    ),

    _lesson(
        lesson_id="java-l01-08",
        theory=(
            "A calculator program shows how variables store values and how expressions compute "
            "results. We use two int variables and Java's +, -, *, and / operators to compute "
            "and print results. Division of two integers in Java gives an integer result, so "
            "17 / 5 becomes 3 (the decimal part is dropped)."
        ),
        analogy=(
            "Think of variables as labelled boxes on a shelf and operators as the tools you use "
            "on their contents. Your Mini Calculator grabs two boxes, applies each tool, and "
            "shouts the result through println. The % remainder operator is a bonus tool that "
            "tells you what is left after sharing out."
        ),
        sections=[
            {
                "heading": "Variables store values",
                "body": (
                    "int a = 12; declares an int variable named a and stores 12 in it. Variables "
                    "give your numbers names, so the calculator reads like a story: a and b go in, "
                    "Sum, Difference, Product, and Quotient come out. Choose names that describe "
                    "what the value means."
                ),
                "pro_tip": (
                    "Meaningful names like firstNumber and secondNumber make code self-"
                    "documenting and impress reviewers."
                ),
            },
            {
                "heading": "Expressions compute results",
                "body": (
                    "An expression like a + b is evaluated to a single value. When printing, wrap "
                    "the expression in parentheses: \"Sum: \" + (a + b). Without the parentheses, "
                    "the + operator joins the text and numbers one by one, producing surprising "
                    "results like Sum: 124 instead of Sum: 16."
                ),
                "pro_tip": (
                    "Addition, subtraction, and multiplication always behave as expected; the "
                    "division is the tricky one because of integer division."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        int a = 12;\n"
            "        int b = 4;\n"
            "        System.out.println(\"Sum: \" + (a + b));\n"
            "        System.out.println(\"Difference: \" + (a - b));\n"
            "        System.out.println(\"Product: \" + (a * b));\n"
            "        System.out.println(\"Quotient: \" + (a / b));\n"
            "    }\n"
            "}",
            [
                {"line": 3, "text": "Stores 12 in the int variable a"},
                {"line": 4, "text": "Stores 4 in the int variable b"},
                {"line": 5, "text": "Parentheses ensure 12 + 4 is computed before printing"},
                {"line": 8, "text": "12 / 4 is integer division, giving 3"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "System.out.println(\"Sum: \" + a + b);",
                "fixed": "System.out.println(\"Sum: \" + (a + b));",
                "why": "+ joins strings left to right, so the numbers become text: \"Sum: 124\".",
            },
            {
                "wrong": "int price = 4.5;",
                "fixed": "double price = 4.5;",
                "why": "An int variable cannot hold a decimal value.",
            },
            {
                "wrong": "Int a = 10;",
                "fixed": "int a = 10;",
                "why": "int is a keyword and must be written in lowercase.",
            },
        ],
        exercise={
            "description": "Change the calculator to work with 100 and 25, and add a Remainder line using the % operator.",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        int a = 100;\n"
                "        int b = 25;\n"
                "        System.out.println(\"Quotient: \" + (a / b));\n"
                "        // Add a remainder line here\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "The remainder of 100 divided by 25 is written as (a % b)",
                "Print it as \"Remainder: \" + (a % b)",
                "100 % 25 is 0 because 25 divides 100 exactly",
            ],
            "expected_output": (
                "Quotient: 4\n"
                "Remainder: 0"
            ),
        },
        quiz={
            "question": "What is 17 / 5 in Java when both values are int?",
            "options": ["3.4", "3", "2", "3.5"],
            "correct": 1,
            "explanation": "Integer division truncates the decimal part, so 17 / 5 is 3.",
        },
        key_takeaways=[
            "Variables store values under meaningful names",
            "+ - * / compute results; wrap expressions in parentheses when printing",
            "Integer division drops the decimal part",
            "The % operator gives the remainder of a division",
        ],
        next_steps="Now build your grand project: an Animated Terminal Profile Card!",
    ),

    _lesson(
        lesson_id="java-l01-09",
        theory=(
            "Escape sequences are special characters that start with a backslash and let you "
            "control the terminal. \\n inserts a new line and \\t inserts a tab, which helps you "
            "align text into neat columns. By combining println with escape sequences, you can "
            "draw text-based art, the foundation of terminal games, loading screens, and "
            "beautiful CLI tools."
        ),
        analogy=(
            "Escape sequences are like choreography notes in a dance script: \\n tells the dancer "
            "to step to a new row and \\t tells them to take four steps right. The audience "
            "(console) sees only the final stage picture, never the notes in the margin."
        ),
        sections=[
            {
                "heading": "Taming the newline and tab",
                "body": (
                    "A single println can print several lines when you embed \\n: "
                    "System.out.println(\"A\\nB\") prints A and then B. The \\t escape inserts a "
                    "tab, which jumps the cursor to the next tab stop. You can also print a "
                    "literal backslash with \\\\ and a double quote with \\\"."
                ),
                "pro_tip": (
                    "\\t is perfect for aligning table columns: Name:\\tAnanya prints with the "
                    "value neatly indented."
                ),
            },
            {
                "heading": "Designing a profile card",
                "body": (
                    "An animated terminal card is just many print lines composed into a frame. "
                    "Use a row of = characters as a border, one line per field, and keep the "
                    "whole card under about 80 characters wide so it fits the terminal. Add your "
                    "own fields, borders, and a tagline to make it yours."
                ),
                "pro_tip": (
                    "Sketch the card on paper first, then translate each line into a "
                    "System.out.println call. Designing before coding saves you many rewrites."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        System.out.println(\"========================\");\n"
            "        System.out.println(\"   PROFILE CARD v1.0\");\n"
            "        System.out.println(\"========================\");\n"
            "        System.out.println(\"Name:\\tAnanya\");\n"
            "        System.out.println(\"Role:\\tJava Developer\");\n"
            "        System.out.println(\"Level:\\tBeginner\");\n"
            "        System.out.println(\"------------------------\");\n"
            "        System.out.println(\"> Keep coding every day!\");\n"
            "    }\n"
            "}",
            [
                {"line": 3, "text": "A border made of = characters"},
                {"line": 4, "text": "A title line for the card"},
                {"line": 6, "text": "\\t aligns the value after a tab stop"},
                {"line": 10, "text": "A motivational tagline at the bottom"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "System.out.println(\"Line 1 /n Line 2\");",
                "fixed": "System.out.println(\"Line 1 \\n Line 2\");",
                "why": "Escape sequences use a backslash, not a forward slash.",
            },
            {
                "wrong": "System.out.println(\"Path: C:\\new\");",
                "fixed": "System.out.println(\"Path: C:\\\\new\");",
                "why": "\\n is interpreted as a newline; write \\\\ to print a literal backslash.",
            },
            {
                "wrong": "System.out.println(\"Tab\\t\"\");",
                "fixed": "System.out.println(\"Tab\\t\\\"\");",
                "why": "A double quote inside a string must be escaped as \\\".",
            },
        ],
        exercise={
            "description": "Design your own two-line profile card: your name on the first line aligned with a tab, and your target role on the second line.",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        // Print your card here\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "Use System.out.println(\"Name:\\t<your name>\"); for the first line",
                "Use System.out.println(\"Role:\\t<your role>\"); for the second",
                "Add a border with = signs if you want it to look complete",
            ],
            "expected_output": (
                "Name:\t<your name>\n"
                "Role:\t<your role>"
            ),
        },
        quiz={
            "question": "What does \\t do inside a Java string?",
            "options": [
                "Moves the output to a new line",
                "Inserts a tab character",
                "Prints a backslash",
                "Deletes the previous character",
            ],
            "correct": 1,
            "explanation": "\\t is the tab escape sequence; it inserts a horizontal tab.",
        },
        key_takeaways=[
            "Escape sequences start with a backslash",
            "\\n prints a new line and \\t inserts a tab",
            "Use \\\\ for a literal backslash and \\\" for a literal quote",
            "Terminal art is just print lines composed into a frame",
        ],
        next_steps="Level 1 complete! Let us level up to variables and primitive types!",
    ),

    # =========================================================================
    # LEVEL 2: VARIABLES
    # =========================================================================
    _lesson(
        lesson_id="java-l02-01",
        theory=(
            "Java has eight primitive types: byte, short, int, long, float, double, char, and "
            "boolean. int and double are the most common, for whole numbers and decimals "
            "respectively. Each type has a fixed size and range, so choosing the right type "
            "keeps your programs correct and memory-efficient."
        ),
        analogy=(
            "Primitive types are like different-sized storage boxes in a warehouse. An int box "
            "holds up to about 2.1 billion whole numbers, a long box holds quadrillions, and a "
            "boolean box is just a switch with two positions. You pick the box that fits your "
            "cargo without wasting shelf space."
        ),
        sections=[
            {
                "heading": "The eight primitives",
                "body": (
                    "int and long hold whole numbers, while double and float hold decimals. "
                    "char holds exactly one character inside single quotes, like 'A'. boolean "
                    "holds only true or false. byte and short are small whole numbers used when "
                    "memory is precious, like in image processing."
                ),
                "pro_tip": (
                    "When in doubt, use int for whole numbers and double for decimals; they "
                    "cover almost every beginner program."
                ),
            },
            {
                "heading": "Size and range",
                "body": (
                    "A byte is 1 byte, short is 2, int is 4, long is 8, float is 4, and double "
                    "is 8. Choosing the right box matters in large systems: a billion-row table "
                    "saves gigabytes by using int instead of long. Java literals tell you the "
                    "type: 90L is a long and 3.14f is a float."
                ),
                "pro_tip": (
                    "Underscores in numbers are legal and readable: long bankBalance = "
                    "9_000_000_000L;"
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        int age = 22;\n"
            "        double salary = 75000.50;\n"
            "        boolean isStudent = true;\n"
            "        char grade = 'A';\n"
            "        System.out.println(\"Age: \" + age);\n"
            "        System.out.println(\"Salary: \" + salary);\n"
            "        System.out.println(\"Is student: \" + isStudent);\n"
            "        System.out.println(\"Grade: \" + grade);\n"
            "    }\n"
            "}",
            [
                {"line": 3, "text": "An int for a whole number"},
                {"line": 4, "text": "A double for a decimal number"},
                {"line": 5, "text": "A boolean holding true or false"},
                {"line": 6, "text": "A char holding one character in single quotes"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "int price = 99.99;",
                "fixed": "double price = 99.99;",
                "why": "An int cannot hold a decimal value; the compiler rejects it.",
            },
            {
                "wrong": "long huge = 9000000000;",
                "fixed": "long huge = 9000000000L;",
                "why": "The L suffix marks the literal as long; without it, the number exceeds int range.",
            },
            {
                "wrong": "boolean flag = 1;",
                "fixed": "boolean flag = true;",
                "why": "A boolean accepts only true or false, not numbers.",
            },
        ],
        exercise={
            "description": "Declare variables for your age (int), your height in meters (double), and whether you are preparing for placements (boolean), then print all three.",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        // Declare your variables here\n"
                "        // Then print each one\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "Declare int age = 22; double height = 5.9; boolean preparing = true;",
                "Print each with a label, like \"Age: \" + age",
                "A char literal uses single quotes; text uses double quotes",
            ],
            "expected_output": (
                "Age: <your age>\n"
                "Height: <your height>\n"
                "Preparing: true"
            ),
        },
        quiz={
            "question": "Which of these is a valid char literal?",
            "options": ["'A'", "\"A\"", "'AB'", "AB"],
            "correct": 0,
            "explanation": "A char literal is exactly one character inside single quotes, like 'A'.",
        },
        key_takeaways=[
            "Java has eight primitive types",
            "int for whole numbers, double for decimals, boolean for true/false",
            "char holds one character in single quotes",
            "Add L to long literals and f to float literals",
        ],
        next_steps="Now let us meet the object versions of these types: wrapper classes!",
    ),

    _lesson(
        lesson_id="java-l02-02",
        theory=(
            "Each primitive type has a wrapper class that treats its value as an object: Integer "
            "for int, Double for double, Character for char, and so on. Java automatically "
            "converts between primitives and wrappers, a mechanism called autoboxing and "
            "unboxing. Wrappers also provide useful static methods like Integer.parseInt() to "
            "convert strings into numbers."
        ),
        analogy=(
            "Primitives are like loose change in your pocket, while wrappers are the same coins "
            "kept in a coin album. You can flip through the album pages (call methods) but you "
            "pay with loose change. Java converts between them automatically, so you barely "
            "notice the album exists."
        ),
        sections=[
            {
                "heading": "Autoboxing and unboxing",
                "body": (
                    "Integer score = 95; boxes the primitive int 95 into an Integer object. "
                    "Reading it back into an int later unboxes it automatically. This lets you "
                    "store numbers in collections like ArrayList, which only accept objects, "
                    "without writing tedious conversion code."
                ),
                "pro_tip": (
                    "Boxing = primitive to object; unboxing = object to primitive. Remember the "
                    "direction with the mnemonic B for Box-in."
                ),
            },
            {
                "heading": "Parsing strings",
                "body": (
                    "Static methods like Integer.parseInt(\"42\") and Double.parseDouble(\"3.14\") "
                    "turn text into numbers, which is exactly what you need when reading "
                    "numbers typed by a user. Each wrapper also has valueOf(), toString(), and "
                    "comparison helpers."
                ),
                "pro_tip": (
                    "Parsing malformed text throws NumberFormatException. Validate input or wrap "
                    "the parse in a try-catch before trusting user data."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Integer score = 95;\n"
            "        Double cgpa = 8.7;\n"
            "        int parsed = Integer.parseInt(\"42\");\n"
            "        System.out.println(\"Score: \" + score);\n"
            "        System.out.println(\"CGPA: \" + cgpa);\n"
            "        System.out.println(\"Parsed: \" + parsed);\n"
            "    }\n"
            "}",
            [
                {"line": 3, "text": "Autoboxing: int 95 is wrapped in an Integer object"},
                {"line": 4, "text": "Double wraps the primitive double"},
                {"line": 5, "text": "parseInt turns the string \"42\" into the int 42"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "int n = Integer.parseInt(\"12abc\");",
                "fixed": "Parsing a clean number string like \"12\", or handling the exception",
                "why": "Malformed text throws NumberFormatException at runtime.",
            },
            {
                "wrong": "Integer number = null; int n = number;",
                "fixed": "Checking number != null before unboxing",
                "why": "Unboxing a null Integer throws NullPointerException.",
            },
            {
                "wrong": "Integer a = 128; Integer b = 128; a == b",
                "fixed": "Using a.equals(b) to compare wrapper values",
                "why": "== compares references for objects, and values above 127 are not cached.",
            },
        ],
        exercise={
            "description": "Create an Integer from the int 42, unbox it into a plain int, add 8 to it, and print the sum.",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        Integer value = 42;\n"
                "        int unboxed = value; // unboxing\n"
                "        // Add 8 and print the result\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "Store the sum in a new int like int sum = unboxed + 8;",
                "Print it with a label: \"Sum: \" + sum",
                "Remember the result will be 50",
            ],
            "expected_output": "Sum: 50",
        },
        quiz={
            "question": "What does Integer.parseInt(\"123\") return?",
            "options": ["The string \"123\"", "An Integer object", "The int 123", "The double 123.0"],
            "correct": 2,
            "explanation": "Integer.parseInt returns a primitive int parsed from the given string.",
        },
        key_takeaways=[
            "Wrappers turn primitives into objects: Integer, Double, Character",
            "Autoboxing and unboxing happen automatically",
            "Wrappers provide parseInt, parseDouble, and other static helpers",
            "Comparing wrappers needs equals(), not ==",
        ],
        next_steps="Let us master text handling with String and StringBuilder!",
    ),

    _lesson(
        lesson_id="java-l02-03",
        theory=(
            "String objects are immutable: every time you change one, Java creates a brand-new "
            "object. That is fine for a few concatenations but wasteful inside loops. "
            "StringBuilder is mutable, so it modifies the same object in place and is the fast "
            "choice for building text piece by piece."
        ),
        analogy=(
            "A String is like a printed newspaper: you cannot edit it, so you must print a whole "
            "new edition. A StringBuilder is a whiteboard: you erase and add words directly. "
            "For a small note either works, but for a long speech the whiteboard wins by far."
        ),
        sections=[
            {
                "heading": "Strings are immutable",
                "body": (
                    "Methods like length(), toUpperCase(), and charAt() return new values and "
                    "never modify the original string. So String big = name.toUpperCase(); is "
                    "needed to capture the result. Because strings never change, Java can safely "
                    "share them between threads, which is a big reliability win."
                ),
                "pro_tip": (
                    "s.length() counts characters; s.charAt(0) reads the first character at "
                    "index 0."
                ),
            },
            {
                "heading": "StringBuilder for heavy building",
                "body": (
                    "new StringBuilder(\"Java\") creates a mutable text buffer. append() adds to "
                    "the end, and the toString() method gives you the final String when you are "
                    "done. In a loop that runs ten thousand times, StringBuilder is dramatically "
                    "faster than string concatenation."
                ),
                "pro_tip": (
                    "Chaining works nicely: sb.append(\"Java\").append(\" is fun\"); reads left "
                    "to right."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        String greeting = \"Hello\";\n"
            "        String full = greeting + \", Java!\";\n"
            "        System.out.println(full);\n"
            "        System.out.println(\"Length: \" + full.length());\n"
            "\n"
            "        StringBuilder sb = new StringBuilder(\"Java\");\n"
            "        sb.append(\" is fun\");\n"
            "        System.out.println(sb);\n"
            "    }\n"
            "}",
            [
                {"line": 3, "text": "A String is immutable"},
                {"line": 4, "text": "Concatenation creates a new String"},
                {"line": 6, "text": "length() returns the character count"},
                {"line": 8, "text": "A mutable StringBuilder"},
                {"line": 9, "text": "append modifies the same object in place"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "String s = \"Java\"; s.toUpperCase();",
                "fixed": "s = s.toUpperCase();",
                "why": "Strings are immutable; the new value must be captured in a variable.",
            },
            {
                "wrong": "if (s1 == s2) to compare string content",
                "fixed": "if (s1.equals(s2))",
                "why": "== compares references, not the text inside the strings.",
            },
            {
                "wrong": "StringBuilder sb = \"hello\";",
                "fixed": "StringBuilder sb = new StringBuilder(\"hello\");",
                "why": "StringBuilder is a class and must be constructed with new.",
            },
        ],
        exercise={
            "description": "Build the sentence Placement preparation requires consistency. by calling append three times on a StringBuilder, then print it.",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        StringBuilder sb = new StringBuilder();\n"
                "        // Append the three words in order\n"
                "        System.out.println(sb);\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "Call sb.append(\"Placement \") first, then sb.append(\"preparation \")",
                "Finish with sb.append(\"requires consistency.\")",
                "println prints the StringBuilder directly thanks to toString",
            ],
            "expected_output": "Placement preparation requires consistency.",
        },
        quiz={
            "question": "Why is StringBuilder preferred over String concatenation inside loops?",
            "options": [
                "It is immutable and safe",
                "It modifies one object instead of creating many",
                "It cannot be printed",
                "It is a primitive type",
            ],
            "correct": 1,
            "explanation": "StringBuilder mutates one buffer, while concatenation allocates a new String each time.",
        },
        key_takeaways=[
            "String is immutable; every change creates a new object",
            "Capture method results in variables: s = s.toUpperCase()",
            "StringBuilder is mutable and fast for building text",
            "Compare string content with equals(), never ==",
        ],
        next_steps="Let us type less and infer more with the var keyword!",
    ),

    _lesson(
        lesson_id="java-l02-04",
        theory=(
            "Introduced in Java 10, the var keyword lets the compiler infer a local variable's "
            "type from its initializer. var name = \"Riya\" is exactly the same as String name = "
            "\"Riya\". var can only be used for local variables that have an initializer; it is "
            "not allowed for fields, method parameters, or variables without an initial value."
        ),
        analogy=(
            "var is like a self-labelling storage box: you drop your things in and the label "
            "appears automatically. The box is still exactly the right size, and the contents "
            "still have a fixed type. You just did not have to write the label yourself."
        ),
        sections=[
            {
                "heading": "Inference, not dynamic typing",
                "body": (
                    "The inferred type is fixed at compile time. var score = 92.5 infers double, "
                    "so you cannot later assign a string to it. Java is still a statically typed "
                    "language; var simply lets the compiler do the paperwork instead of you. "
                    "Readability is the only reason to use it."
                ),
                "pro_tip": (
                    "var shines with long generic types: var map = new HashMap<String, "
                    "List<String>>(); removes a wall of text."
                ),
            },
            {
                "heading": "Where var is allowed",
                "body": (
                    "var works for local variables and even inside loops, but the compiler needs "
                    "an initializer to infer from. You cannot write var x; and you cannot use var "
                    "for class fields or method parameters. When the type is not obvious, spell "
                    "it out for the reader."
                ),
                "pro_tip": (
                    "Use var only when it makes code clearer. Hiding an obvious type like int "
                    "with var adds nothing."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        var name = \"Rahul\";\n"
            "        var age = 21;\n"
            "        var score = 92.5;\n"
            "        System.out.println(name + \" is \" + age + \" years old.\");\n"
            "        System.out.println(\"Score: \" + score);\n"
            "    }\n"
            "}",
            [
                {"line": 3, "text": "var infers String from the initializer"},
                {"line": 4, "text": "var infers int"},
                {"line": 5, "text": "var infers double"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "var x;",
                "fixed": "var x = 0;",
                "why": "var needs an initializer so the compiler can infer the type.",
            },
            {
                "wrong": "var count = 5; then count = 2.5;",
                "fixed": "Assigning another int, or declaring a double instead",
                "why": "The inferred type is fixed; a var that inferred int cannot hold a double.",
            },
            {
                "wrong": "public void greet(var name) { }",
                "fixed": "public void greet(String name) { }",
                "why": "var is not allowed for method parameters.",
            },
        ],
        exercise={
            "description": "Use var to declare a string, an int, and a boolean, then print all three.",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        // Declare three vars here\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "var language = \"Java\"; var level = 2; var isFun = true;",
                "Print each one with a label",
                "The inferred types are String, int, and boolean",
            ],
            "expected_output": (
                "Language: Java\n"
                "Level: 2\n"
                "Fun: true"
            ),
        },
        quiz={
            "question": "Which declaration using var is valid?",
            "options": ["var x;", "var x = 3.14;", "public var x = 3;", "var(int x);"],
            "correct": 1,
            "explanation": "var requires an initializer and is only for local variables, so var x = 3.14; is valid.",
        },
        key_takeaways=[
            "var lets the compiler infer the type from the initializer",
            "Java stays statically typed; var only hides the explicit type",
            "var needs an initializer and cannot be used for fields or parameters",
            "Use var when it improves readability",
        ],
        next_steps="Now let us freeze values forever with final constants!",
    ),

    _lesson(
        lesson_id="java-l02-05",
        theory=(
            "The final keyword makes a variable's value unchangeable after it is set, turning it "
            "into a constant. By convention, constants are named in UPPER_SNAKE_CASE like "
            "MAX_RETRIES. Constants make code clearer and safer by removing magic numbers "
            "scattered through your program."
        ),
        analogy=(
            "A final variable is a framed contract hanging on the office wall: everyone can read "
            "it, but nobody may edit it. Naming it in capitals is like stamping it with a big "
            "NOT FOR EDITING seal so every developer knows it is sacred."
        ),
        sections=[
            {
                "heading": "Declaring constants",
                "body": (
                    "final double PI = 3.14159; creates a value that can never change. The "
                    "compiler enforces this: any later assignment is a compile error. Constants "
                    "also document intent. Reading MAX_SPEED is far clearer than seeing the "
                    "mysterious number 120 in your code."
                ),
                "pro_tip": (
                    "If a value is a fixed rule of your program, like a tax rate or a retry "
                    "limit, make it final so it cannot change by mistake."
                ),
            },
            {
                "heading": "final beyond variables",
                "body": (
                    "Java also uses final to prevent change at other levels: a final class cannot "
                    "be subclassed, a final method cannot be overridden, and a final field must "
                    "be assigned exactly once. For now, remember final variables = constants."
                ),
                "pro_tip": (
                    "Combining static and final is the classic way to declare shared constants: "
                    "public static final int MAX_RETRIES = 3;"
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        final double PI = 3.14159;\n"
            "        final int MAX_SPEED = 120;\n"
            "        System.out.println(\"Pi: \" + PI);\n"
            "        System.out.println(\"Max speed: \" + MAX_SPEED);\n"
            "    }\n"
            "}",
            [
                {"line": 3, "text": "A final double constant in UPPER_SNAKE_CASE"},
                {"line": 4, "text": "A final int constant"},
                {"line": 5, "text": "Constants are read, never modified"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "final int MAX = 10; then MAX = 20;",
                "fixed": "Using a different variable instead of reassigning",
                "why": "Assigning to a final variable is a compile-time error.",
            },
            {
                "wrong": "final int max_speed = 120;",
                "fixed": "final int MAX_SPEED = 120;",
                "why": "Java constants follow the UPPER_SNAKE_CASE convention.",
            },
            {
                "wrong": "const int MAX = 10;",
                "fixed": "final int MAX = 10;",
                "why": "Java uses final, not const, to declare constants.",
            },
        ],
        exercise={
            "description": "Declare a constant TAX_RATE of 0.18, compute the tax on a purchase of 1000, and print it.",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        final double TAX_RATE = 0.18;\n"
                "        double price = 1000;\n"
                "        // Compute and print the tax\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "Tax is price * TAX_RATE",
                "Store it in a variable like double tax = price * TAX_RATE;",
                "Print \"Tax: \" + tax",
            ],
            "expected_output": "Tax: 180.0",
        },
        quiz={
            "question": "What naming convention do Java constants follow?",
            "options": ["camelCase", "UPPER_SNAKE_CASE", "kebab-case", "ALLlowercase"],
            "correct": 1,
            "explanation": "Constants are conventionally named in UPPER_SNAKE_CASE like MAX_RETRIES.",
        },
        key_takeaways=[
            "final makes a variable's value unchangeable",
            "Name constants in UPPER_SNAKE_CASE",
            "Constants remove magic numbers and document intent",
            "Assigning to a final variable is a compile-time error",
        ],
        next_steps="Now let us convert between types with casting!",
    ),

    _lesson(
        lesson_id="java-l02-06",
        theory=(
            "Casting converts a value from one type to another. Widening conversions happen "
            "automatically when moving from a smaller to a larger type, like int to long. "
            "Narrowing conversions, like double to int, require an explicit cast with (int) and "
            "may lose precision by truncating the decimal part."
        ),
        analogy=(
            "Widening is like pouring juice from a small glass into a big jug: nothing spills, "
            "so Java does it for you. Narrowing is like pouring from a big jug into a small "
            "glass: you must decide what to leave out (the decimal part), so Java makes you grip "
            "the glass with (int) and pour deliberately."
        ),
        sections=[
            {
                "heading": "Widening is automatic",
                "body": (
                    "Moving from a smaller type to a larger one always succeeds: byte, short, "
                    "int, long, float, double. long bigger = small; where small is an int works "
                    "silently because every int fits inside a long. The value never changes."
                ),
                "pro_tip": (
                    "Remember the ladder byte < short < int < long < float < double; you may "
                    "climb it for free, but every step down needs a cast."
                ),
            },
            {
                "heading": "Narrowing needs a cast",
                "body": (
                    "(int) 3.99 becomes 3, not 4: the cast truncates toward zero rather than "
                    "rounding. You are telling the compiler, I know I am losing information and "
                    "I accept it. Narrowing from a large long can also overflow silently, so "
                    "only narrow when you are sure the value fits."
                ),
                "pro_tip": (
                    "When you need rounding instead of truncation, use Math.round(3.99) which "
                    "gives 4."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        double pi = 3.14;\n"
            "        int rounded = (int) pi;\n"
            "        int small = 10;\n"
            "        long bigger = small;\n"
            "        System.out.println(\"Pi as int: \" + rounded);\n"
            "        System.out.println(\"Widened: \" + bigger);\n"
            "    }\n"
            "}",
            [
                {"line": 4, "text": "Explicit narrowing cast truncates 3.14 to 3"},
                {"line": 6, "text": "Implicit widening from int to long"},
                {"line": 7, "text": "The decimal part is gone"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "int x = 3.99;",
                "fixed": "int x = (int) 3.99;",
                "why": "Narrowing from double to int requires an explicit cast.",
            },
            {
                "wrong": "int x = (int) 3_000_000_000L;",
                "fixed": "long x = 3_000_000_000L;",
                "why": "The value exceeds int range, so narrowing overflows silently.",
            },
            {
                "wrong": "char c = (char) \"A\";",
                "fixed": "char c = \"A\".charAt(0);",
                "why": "Casting works between primitives, not from a String.",
            },
        ],
        exercise={
            "description": "Convert the double 98.76 to an int and an int 50 to a long, then print both.",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        double value = 98.76;\n"
                "        // Narrow it to an int and print it\n"
                "        int small = 50;\n"
                "        // Widen it to a long and print it\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "int truncated = (int) value; gives 98",
                "long widened = small; needs no cast",
                "Print labels like \"Truncated: \" and \"Widened: \"",
            ],
            "expected_output": (
                "Truncated: 98\n"
                "Widened: 50"
            ),
        },
        quiz={
            "question": "What is the value of (int) 7.9?",
            "options": ["8", "7.9", "7", "8.0"],
            "correct": 2,
            "explanation": "An explicit cast to int truncates the decimal part, so (int) 7.9 is 7.",
        },
        key_takeaways=[
            "Widening conversions happen automatically",
            "Narrowing requires an explicit cast and can lose precision",
            "(int) truncates toward zero; it does not round",
            "Only narrow when you are sure the value fits",
        ],
        next_steps="Enough theory: let us make programs interactive with Scanner!",
    ),

    _lesson(
        lesson_id="java-l02-07",
        theory=(
            "The Scanner class reads input from the keyboard and is our gateway to interactive "
            "programs. You create one with new Scanner(System.in), import it with import "
            "java.util.Scanner;, and call methods like nextInt() and nextLine() to read values. "
            "Always close the scanner with close() when you are done to free its resources."
        ),
        analogy=(
            "Scanner is a waiter at your table: you tell it what you want (the method), it "
            "brings it from the kitchen (the keyboard), and you hand it back when you leave "
            "(close()). Forgetting to close is like leaving without settling the bill, and the "
            "table stays booked."
        ),
        sections=[
            {
                "heading": "Creating and using a Scanner",
                "body": (
                    "The import line tells Java where the Scanner class lives. Then "
                    "Scanner scanner = new Scanner(System.in); connects it to the keyboard. "
                    "nextLine() reads a whole line of text, nextInt() reads an int, nextDouble() "
                    "reads a double, and next() reads a single word."
                ),
                "pro_tip": (
                    "Always print a prompt with System.out.print before each read so the user "
                    "knows exactly what to type."
                ),
            },
            {
                "heading": "Common pitfalls",
                "body": (
                    "nextInt() reads the number but leaves the Enter key in the buffer. If you "
                    "call nextLine() right after, it swallows that leftover newline and returns "
                    "an empty string. Fix it by reading the name first with nextLine(), or by "
                    "consuming the leftover newline with an extra nextLine()."
                ),
                "pro_tip": (
                    "When reading a name and a number, read the String first, then the number, "
                    "and you will never hit the leftover-newline trap."
                ),
            },
        ],
        code_example=_code(
            "import java.util.Scanner;\n"
            "\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner scanner = new Scanner(System.in);\n"
            "        System.out.print(\"Enter your name: \");\n"
            "        String name = scanner.nextLine();\n"
            "        System.out.print(\"Enter your age: \");\n"
            "        int age = scanner.nextInt();\n"
            "        System.out.println(\"Hello \" + name + \"! You are \" + age + \" years old.\");\n"
            "        scanner.close();\n"
            "    }\n"
            "}",
            [
                {"line": 1, "text": "Imports the Scanner class from java.util"},
                {"line": 5, "text": "Creates a Scanner connected to the keyboard"},
                {"line": 7, "text": "Reads a whole line of text"},
                {"line": 9, "text": "Reads an int"},
                {"line": 11, "text": "Closes the scanner to release its resources"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "Using Scanner without importing java.util.Scanner",
                "fixed": "Adding import java.util.Scanner; at the top",
                "why": "Scanner lives in the java.util package and must be imported.",
            },
            {
                "wrong": "int age = scanner.next();",
                "fixed": "int age = scanner.nextInt();",
                "why": "next() returns a String, which cannot be stored in an int.",
            },
            {
                "wrong": "Forgetting to call scanner.close()",
                "fixed": "Calling scanner.close() when reading is done",
                "why": "An open Scanner holds resources; closing it is good practice.",
            },
        ],
        exercise={
            "description": "Write a program that asks for your city (String) and your CGPA (double), then prints a summary line.",
            "starter_code": (
                "import java.util.Scanner;\n"
                "\n"
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        Scanner scanner = new Scanner(System.in);\n"
                "        // Ask for and read the city and CGPA\n"
                "        scanner.close();\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "Ask with System.out.print and read the city with scanner.nextLine()",
                "Read the CGPA with scanner.nextDouble()",
                "Print something like \"City: Pune, CGPA: 8.5\"",
            ],
            "expected_output": "City: <your city>, CGPA: <your cgpa>",
        },
        quiz={
            "question": "Which Scanner method reads a whole line of text?",
            "options": ["nextInt()", "nextDouble()", "nextLine()", "nextBoolean()"],
            "correct": 2,
            "explanation": "nextLine() reads an entire line including spaces until the Enter key.",
        },
        key_takeaways=[
            "Scanner reads keyboard input; import java.util.Scanner first",
            "nextLine reads text, nextInt reads ints, nextDouble reads doubles",
            "Print a prompt before each read",
            "Close the scanner when you are done",
        ],
        next_steps="Now let us put Scanner to work with a Temperature Converter!",
    ),

    _lesson(
        lesson_id="java-l02-08",
        theory=(
            "This practice combines Scanner, double variables, and an arithmetic formula. The "
            "formula to convert Celsius to Fahrenheit is F = C x 9/5 + 32. Watch the order of "
            "operations: multiplication and division happen before addition, and when both 9 "
            "and 5 are doubles, 9/5 is 1.8, not 1."
        ),
        analogy=(
            "Converting temperatures is like exchanging currency at an airport booth: you feed "
            "in an amount in one currency, the booth applies a fixed formula, and you walk out "
            "with the converted amount. Your program is the booth, and nextDouble is the slot "
            "where the amount goes in."
        ),
        sections=[
            {
                "heading": "The formula",
                "body": (
                    "fahrenheit = (celsius * 9 / 5) + 32. Because celsius is a double, the whole "
                    "expression is computed with doubles, so 9 / 5 becomes 1.8 instead of "
                    "truncating to 1. The parentheses keep the formula readable and match the "
                    "mathematical order exactly."
                ),
                "pro_tip": (
                    "Write the formula in one line exactly as it appears in mathematics, then "
                    "test it with a known pair like 0 C = 32 F and 100 C = 212 F."
                ),
            },
            {
                "heading": "Reading a double",
                "body": (
                    "scanner.nextDouble() reads a decimal number typed by the user. Users can "
                    "type whole numbers too: entering 25 gives 25.0, and the converter prints "
                    "77.0. Printing prompts before every read keeps the terminal clear about "
                    "what input is expected."
                ),
                "pro_tip": (
                    "Test your converter with edge values: 0, 37 (body temperature), and 100 "
                    "(boiling) to make sure the formula is right."
                ),
            },
        ],
        code_example=_code(
            "import java.util.Scanner;\n"
            "\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner scanner = new Scanner(System.in);\n"
            "        System.out.print(\"Enter temperature in Celsius: \");\n"
            "        double celsius = scanner.nextDouble();\n"
            "        double fahrenheit = (celsius * 9 / 5) + 32;\n"
            "        System.out.println(\"Fahrenheit: \" + fahrenheit);\n"
            "        scanner.close();\n"
            "    }\n"
            "}",
            [
                {"line": 7, "text": "Reads a decimal temperature from the user"},
                {"line": 8, "text": "Applies the conversion formula"},
                {"line": 9, "text": "Prints the converted temperature"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "int celsius = scanner.nextDouble();",
                "fixed": "double celsius = scanner.nextDouble();",
                "why": "nextDouble returns a double, which cannot be stored in an int.",
            },
            {
                "wrong": "System.out.println(\"Temp: \" + celsius * 9 / 5 + 32);",
                "fixed": "System.out.println(\"Temp: \" + ((celsius * 9 / 5) + 32));",
                "why": "Without parentheses, + joins text left to right and produces jumbled output.",
            },
            {
                "wrong": "(celsius + 32) * 9 / 5",
                "fixed": "(celsius * 9 / 5) + 32",
                "why": "The correct formula adds 32 last; adding it to celsius first gives wrong results.",
            },
        ],
        exercise={
            "description": "Write a Fahrenheit to Celsius converter using the formula C = (F - 32) x 5 / 9. Read F, compute C, and print it.",
            "starter_code": (
                "import java.util.Scanner;\n"
                "\n"
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        Scanner scanner = new Scanner(System.in);\n"
                "        // Read F, convert, and print\n"
                "        scanner.close();\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "Read with double f = scanner.nextDouble();",
                "Compute c = (f - 32) * 5 / 9;",
                "Print with a label like \"Celsius: \" + c",
            ],
            "expected_output": "Celsius: 100.0",
        },
        quiz={
            "question": "What is 9 / 5 when both are ints in Java?",
            "options": ["1.8", "1", "2", "9"],
            "correct": 1,
            "explanation": "Integer division truncates the decimal, so 9 / 5 as ints is 1.",
        },
        key_takeaways=[
            "Scanner reads doubles with nextDouble",
            "The formula F = C x 9/5 + 32 converts Celsius to Fahrenheit",
            "Doubles in the expression keep 9/5 = 1.8 instead of 1",
            "Test your converter with known values like 0, 37, and 100",
        ],
        next_steps="Ready for the Type Puzzle challenge? Let us test your casting skills!",
    ),

    _lesson(
        lesson_id="java-l02-09",
        theory=(
            "Real programs mix many types in one expression, and Java applies automatic widening "
            "as it evaluates. When an int multiplies a double, the int is promoted to double and "
            "the result is double. You can capture the full precision in a double, or "
            "deliberately narrow with a cast when you only need a whole number."
        ),
        analogy=(
            "A mixed-type expression is like a conversation between teammates who speak "
            "different languages: everyone automatically translates to the most widely spoken "
            "language (the widest type) so nobody gets lost. The result always comes back "
            "speaking the widest language, here double."
        ),
        sections=[
            {
                "heading": "Type promotion in action",
                "body": (
                    "int apples = 10 and double price = 2.5 combine as apples * price. Because "
                    "one operand is double, Java promotes apples to 10.0 and the result is the "
                    "double 25.0. This automatic promotion is why the total variable must be "
                    "declared as double, not int."
                ),
                "pro_tip": (
                    "Mixed arithmetic follows the rule: if any operand is double, the result is "
                    "double. If both are int, the result is int."
                ),
            },
            {
                "heading": "Why the cast matters",
                "body": (
                    "An explicit cast like (int) total is a deliberate, visible decision. It "
                    "tells every reader, I know I am losing decimals here and that is fine. "
                    "Truncation is not rounding, so (int) 149.97 gives 149. For a nearest-number "
                    "answer, reach for Math.round() instead."
                ),
                "pro_tip": (
                    "Reviewers love seeing a comment next to an intentional cast, like // price "
                    "is always a whole rupee here."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        int apples = 10;\n"
            "        double price = 2.5;\n"
            "        double total = apples * price;\n"
            "        int roundedTotal = (int) total;\n"
            "        System.out.println(\"Total: \" + total);\n"
            "        System.out.println(\"Rounded total: \" + roundedTotal);\n"
            "    }\n"
            "}",
            [
                {"line": 5, "text": "int x double promotes to double: 25.0"},
                {"line": 6, "text": "Explicit cast truncates to 25"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "int total = apples * price;",
                "fixed": "double total = apples * price;",
                "why": "An int times a double produces a double, which cannot be stored in an int.",
            },
            {
                "wrong": "int rounded = (int) total; expecting a nearest-integer round",
                "fixed": "int rounded = (int) Math.round(total);",
                "why": "(int) truncates toward zero; Math.round rounds to the nearest value.",
            },
            {
                "wrong": "double sum = apples + price; assuming the result is exact",
                "fixed": "Accepting small floating-point rounding, or using BigDecimal for money",
                "why": "Binary floats cannot represent every decimal exactly (0.1 + 0.2 is 0.30000000000000004).",
            },
        ],
        exercise={
            "description": "An item costs 49.99 and you buy 3. Compute the double total, then print the truncated total and the rounded total.",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        double price = 49.99;\n"
                "        int quantity = 3;\n"
                "        // Compute and print the totals\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "double total = price * quantity; gives 149.97",
                "int truncated = (int) total; gives 149",
                "int rounded = (int) Math.round(total); gives 150",
            ],
            "expected_output": (
                "Total: 149.97\n"
                "Truncated: 149\n"
                "Rounded: 150"
            ),
        },
        quiz={
            "question": "What type does apples * price have when apples is int and price is double?",
            "options": ["int", "double", "long", "float"],
            "correct": 1,
            "explanation": "If any operand is double, the arithmetic is done in double, so the result is double.",
        },
        key_takeaways=[
            "Mixed-type arithmetic promotes to the widest type",
            "int times double produces a double",
            "Casting is a deliberate decision that can lose precision",
            "Use Math.round for rounding and (int) for truncation",
        ],
        next_steps="Time to build a real-world app: the Smart Shopping Cart project!",
    ),

    _lesson(
        lesson_id="java-l02-10",
        theory=(
            "The Smart Shopping Cart ties together Scanner input, variables of several types, "
            "and arithmetic. You read an item name (String), price (double), and quantity "
            "(int), then compute the total. This is the exact pattern behind real billing "
            "systems in shops, restaurants, and e-commerce platforms."
        ),
        analogy=(
            "Your program is a billing counter. A customer hands you an item, its price tag, "
            "and how many they want. You multiply and announce the total. Here the customer "
            "types at the keyboard, the Scanner is your ears, and your program is the cash "
            "register that prints the receipt."
        ),
        sections=[
            {
                "heading": "Plan before you code",
                "body": (
                    "Good developers plan variables before writing statements. This program "
                    "needs: item (String), price (double), quantity (int), and total (double). "
                    "Write the plan as comments first, then fill each step. Planning turns a "
                    "wall of code into a checklist you can tick off."
                ),
                "pro_tip": (
                    "Sketch the input/output flow on paper: prompt, read, prompt, read, "
                    "compute, print. Then translate each box into 1-2 lines of code."
                ),
            },
            {
                "heading": "Reading different types in sequence",
                "body": (
                    "Read the item name first with nextLine(), then the price with nextDouble(), "
                    "then the quantity with nextInt(). Reading the string first sidesteps the "
                    "leftover-newline problem where a nextLine() after a number swallows the "
                    "Enter key and returns an empty string."
                ),
                "pro_tip": (
                    "After computing the total, add more fields like a discount or GST later; "
                    "the structure of prompt, read, compute, print scales to any receipt."
                ),
            },
        ],
        code_example=_code(
            "import java.util.Scanner;\n"
            "\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner scanner = new Scanner(System.in);\n"
            "        System.out.print(\"Enter item name: \");\n"
            "        String item = scanner.nextLine();\n"
            "        System.out.print(\"Enter price: \");\n"
            "        double price = scanner.nextDouble();\n"
            "        System.out.print(\"Enter quantity: \");\n"
            "        int quantity = scanner.nextInt();\n"
            "        double total = price * quantity;\n"
            "        System.out.println(\"Item: \" + item);\n"
            "        System.out.println(\"Total: \" + total);\n"
            "        scanner.close();\n"
            "    }\n"
            "}",
            [
                {"line": 7, "text": "String read first with nextLine"},
                {"line": 9, "text": "Decimal price read with nextDouble"},
                {"line": 11, "text": "Whole quantity read with nextInt"},
                {"line": 12, "text": "Total is price times quantity"},
                {"line": 14, "text": "Prints the computed total"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "Reading the number first, then nextLine() for the name",
                "fixed": "Reading the name first, or consuming the leftover newline",
                "why": "nextLine() after nextInt() swallows the leftover Enter and returns empty.",
            },
            {
                "wrong": "String item = scanner.nextInt();",
                "fixed": "String item = scanner.nextLine();",
                "why": "nextInt returns an int; you cannot store it in a String.",
            },
            {
                "wrong": "Forgetting to close the scanner",
                "fixed": "Calling scanner.close() at the end",
                "why": "Closing the scanner releases the keyboard resource cleanly.",
            },
        ],
        exercise={
            "description": "Extend the cart with a discount: read a discount percentage (double), compute discounted = total x (1 - discount/100), and print both totals.",
            "starter_code": (
                "import java.util.Scanner;\n"
                "\n"
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        Scanner scanner = new Scanner(System.in);\n"
                "        System.out.print(\"Enter price: \");\n"
                "        double price = scanner.nextDouble();\n"
                "        System.out.print(\"Enter quantity: \");\n"
                "        int quantity = scanner.nextInt();\n"
                "        System.out.print(\"Enter discount percent: \");\n"
                "        double discount = scanner.nextDouble();\n"
                "        // Compute total and discounted, then print both\n"
                "        scanner.close();\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "double total = price * quantity;",
                "double discounted = total * (1 - discount / 100);",
                "Print with labels like \"Total: \" and \"After discount: \"",
            ],
            "expected_output": (
                "Total: <total>\n"
                "After discount: <discounted total>"
            ),
        },
        quiz={
            "question": "What is a good first step when building a program like the shopping cart?",
            "options": [
                "Writing random code and hoping it works",
                "Listing the variables you need and planning the flow",
                "Skipping the Scanner import",
                "Printing output without reading any input",
            ],
            "correct": 1,
            "explanation": "Planning variables and the input/output flow first makes the program easy to write correctly.",
        },
        key_takeaways=[
            "Plan variables and flow before writing code",
            "Read String values before numbers to avoid the leftover-newline trap",
            "Prompt, read, compute, print is a reusable pattern",
            "The cart pattern scales to real billing systems",
        ],
        next_steps="Level 2 done! Let us sharpen your skills with operators in Level 3!",
    ),

    # =========================================================================
    # LEVEL 3: OPERATORS
    # =========================================================================
    _lesson(
        lesson_id="java-l03-01",
        theory=(
            "Java's arithmetic operators are + (addition), - (subtraction), * (multiplication), "
            "/ (division), and % (modulo, the remainder). Division of two integers truncates "
            "the decimal, so 17 / 5 is 3. The modulo operator returns what is left over: "
            "17 % 5 is 2. The ++ and -- operators increment and decrement a variable by one."
        ),
        analogy=(
            "% is like handing out pizza slices: after giving 17 slices to 5 friends as evenly "
            "as possible, / tells you each friend gets 3 full slices and % tells you 2 slices "
            "are left in the box. Modulo is the box-check at the end of every sharing round."
        ),
        sections=[
            {
                "heading": "The five core operators",
                "body": (
                    "All five operators follow the normal precedence rules: * / and % bind "
                    "tighter than + and -. So a + b * c multiplies first, then adds. Use "
                    "parentheses to force your intended order and to make the math obvious to "
                    "every reader."
                ),
                "pro_tip": (
                    "Modulo is the secret weapon for checking evenness: number % 2 == 0 means "
                    "even."
                ),
            },
            {
                "heading": "Increment and decrement",
                "body": (
                    "counter++ adds 1 to counter, and counter-- subtracts 1. Standing alone, "
                    "they are simple and clear. The prefix form ++counter returns the new value "
                    "while the postfix form counter++ returns the old value, which only matters "
                    "when the value is used inside a larger expression."
                ),
                "pro_tip": (
                    "Incrementing inside complex expressions confuses readers; use it as a "
                    "standalone statement whenever you can."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        int a = 17;\n"
            "        int b = 5;\n"
            "        System.out.println(\"Sum: \" + (a + b));\n"
            "        System.out.println(\"Difference: \" + (a - b));\n"
            "        System.out.println(\"Product: \" + (a * b));\n"
            "        System.out.println(\"Quotient: \" + (a / b));\n"
            "        System.out.println(\"Remainder: \" + (a % b));\n"
            "        int counter = 10;\n"
            "        counter++;\n"
            "        System.out.println(\"After ++: \" + counter);\n"
            "    }\n"
            "}",
            [
                {"line": 8, "text": "Integer division: 17 / 5 is 3"},
                {"line": 9, "text": "Modulo: 17 % 5 is 2"},
                {"line": 11, "text": "Increments counter from 10 to 11"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "double result = 17 / 5;",
                "fixed": "double result = 17.0 / 5;",
                "why": "Both operands are ints, so integer division runs first and gives 3.",
            },
            {
                "wrong": "int r = -7 % 3; expecting 2",
                "fixed": "Understanding -7 % 3 is -1 in Java",
                "why": "The sign of the remainder follows the dividend in Java.",
            },
            {
                "wrong": "int result = a + b * c; assuming left-to-right",
                "fixed": "Writing a + (b * c) to make precedence explicit",
                "why": "* and / bind tighter than + and -, so multiplication happens first.",
            },
        ],
        exercise={
            "description": "Split 125 rupees among 7 people: print how much each person gets (the quotient) and how much is left over (the remainder).",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        int total = 125;\n"
                "        int people = 7;\n"
                "        // Print the quotient and remainder\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "Each person gets total / people",
                "The remainder is total % people",
                "125 / 7 is 17 and 125 % 7 is 6",
            ],
            "expected_output": (
                "Share: 17\n"
                "Remainder: 6"
            ),
        },
        quiz={
            "question": "What is 23 % 5?",
            "options": ["4", "4.6", "5", "3"],
            "correct": 0,
            "explanation": "5 goes into 23 four times (20) with 3 remaining, so 23 % 5 is 3.",
        },
        key_takeaways=[
            "Arithmetic operators are + - * / and %",
            "Integer division truncates the decimal part",
            "% returns the remainder of a division",
            "Use ++ and -- to increment and decrement by one",
        ],
        next_steps="Now let us compare values with relational operators!",
    ),

    _lesson(
        lesson_id="java-l03-02",
        theory=(
            "Relational operators compare two values and produce a boolean: == (equal), != (not "
            "equal), < (less than), > (greater than), <= (less than or equal), and >= (greater "
            "than or equal). Use == to compare primitives like numbers, but never strings: "
            "String content is compared with the equals() method."
        ),
        analogy=(
            "Relational operators are the judges in a game show: they compare two contestants "
            "and declare true or false. But beware, == compares the name tags on the "
            "contestants (references), so for Strings you must ask them to compare their actual "
            "answers (content) with equals()."
        ),
        sections=[
            {
                "heading": "Comparing numbers",
                "body": (
                    "Every relational expression evaluates to either true or false. 10 < 20 is "
                    "true, 10 > 20 is false, and 10 == 10 is true. The <= and >= operators "
                    "include the boundary, so 10 <= 10 is true while 10 < 10 is false. These "
                    "booleans become the conditions inside if statements and loops."
                ),
                "pro_tip": (
                    "Read >= as at least and <= as at most, which matches everyday English and "
                    "reminds you the boundary is included."
                ),
            },
            {
                "heading": "Strings need equals()",
                "body": (
                    "Two String variables may hold the same text but live at different memory "
                    "addresses, so name == \"Rahul\" can be false even when the text matches. "
                    "Always compare string content with name.equals(\"Rahul\"). Putting the "
                    "literal first, \"Rahul\".equals(name), is a handy trick that survives a "
                    "null name."
                ),
                "pro_tip": (
                    "\"Rahul\".equals(name) returns false when name is null instead of throwing "
                    "an exception, which is why the literal-first form is safer."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        int x = 10;\n"
            "        int y = 20;\n"
            "        System.out.println(\"x < y: \" + (x < y));\n"
            "        System.out.println(\"x == y: \" + (x == y));\n"
            "        System.out.println(\"x != y: \" + (x != y));\n"
            "        System.out.println(\"y >= x: \" + (y >= x));\n"
            "    }\n"
            "}",
            [
                {"line": 5, "text": "10 < 20 is true"},
                {"line": 6, "text": "== compares primitive values"},
                {"line": 7, "text": "!= is true when values differ"},
                {"line": 8, "text": ">= includes equality: 20 >= 10 is true"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "if (name == \"Rahul\")",
                "fixed": "if (name.equals(\"Rahul\"))",
                "why": "== compares references for objects; equals compares content.",
            },
            {
                "wrong": "if (score = 90)",
                "fixed": "if (score == 90)",
                "why": "= assigns, == compares; an assignment compiles and is always true when non-zero.",
            },
            {
                "wrong": "String s = \"5\"; if (s == 5)",
                "fixed": "if (Integer.parseInt(s) == 5)",
                "why": "Comparing a String with a number needs a conversion first.",
            },
        ],
        exercise={
            "description": "Declare int marks = 73 and print three booleans: passed (marks >= 40), distinction (marks >= 75), and failed (marks < 40).",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        int marks = 73;\n"
                "        // Compute and print the three booleans\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "boolean passed = marks >= 40; gives true",
                "boolean distinction = marks >= 75; gives false",
                "boolean failed = marks < 40; gives false",
            ],
            "expected_output": (
                "Passed: true\n"
                "Distinction: false\n"
                "Failed: false"
            ),
        },
        quiz={
            "question": "How do you correctly compare two Strings for equal content?",
            "options": ["With ==", "With equals()", "With compare()", "With a single ="],
            "correct": 1,
            "explanation": "equals() compares the text inside the strings, while == compares object references.",
        },
        key_takeaways=[
            "Relational operators return a boolean",
            "< > <= >= compare numbers, including the boundary",
            "== compares primitives, not String content",
            "Use equals() for strings, literal-first to be null-safe",
        ],
        next_steps="Let us combine conditions with logical operators!",
    ),

    _lesson(
        lesson_id="java-l03-03",
        theory=(
            "Logical operators combine booleans: && (AND) is true only when both sides are "
            "true, || (OR) is true when at least one side is true, and ! (NOT) flips a boolean. "
            "Both && and || short-circuit: Java stops evaluating the right side as soon as the "
            "result is already decided, which makes expressions both faster and safer."
        ),
        analogy=(
            "&& is a two-key launch: both keys must turn for liftoff. || is a VIP gate: any one "
            "badge gets you in. ! is a light switch. Short-circuiting is a smart doorman who "
            "checks your first badge and waves you in before you even dig the second one out of "
            "your pocket."
        ),
        sections=[
            {
                "heading": "AND, OR, NOT",
                "body": (
                    "true && true is true, everything else is false. true || false is true, and "
                    "false || false is false. The NOT operator turns true into false and vice "
                    "versa. Combined, they describe real rules: a student passes the drive if "
                    "cgpa >= 7.0 && attendance >= 75%."
                ),
                "pro_tip": (
                    "Booleans compose like English: (marks >= 60 && marks <= 90) reads as "
                    "marks between 60 and 90."
                ),
            },
            {
                "heading": "Short-circuiting",
                "body": (
                    "With &&, if the left side is false, the right side never runs. With ||, if "
                    "the left side is true, the right side never runs. This is a safety feature: "
                    "guard a risky call on the right side with a cheap check on the left, like "
                    "name != null && name.length() > 0."
                ),
                "pro_tip": (
                    "Order your checks from cheapest to most expensive, and put null checks "
                    "first so later code never blows up."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        boolean hasDegree = true;\n"
            "        boolean hasExperience = false;\n"
            "        System.out.println(\"Eligible (AND): \" + (hasDegree && hasExperience));\n"
            "        System.out.println(\"Eligible (OR): \" + (hasDegree || hasExperience));\n"
            "        System.out.println(\"Not qualified: \" + (!hasExperience));\n"
            "    }\n"
            "}",
            [
                {"line": 5, "text": "AND is true only when both sides are true"},
                {"line": 6, "text": "OR is true because one side is true"},
                {"line": 7, "text": "NOT flips false into true"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "if (a & b) when you want logical AND",
                "fixed": "if (a && b)",
                "why": "& always evaluates both sides; && short-circuits and reads as logic.",
            },
            {
                "wrong": "if (!age >= 18)",
                "fixed": "if (!(age >= 18))",
                "why": "! works on booleans; wrap the whole comparison in parentheses first.",
            },
            {
                "wrong": "if (s.length() > 0 && s != null)",
                "fixed": "if (s != null && s.length() > 0)",
                "why": "With &&, the left side runs first; null checks belong on the left.",
            },
        ],
        exercise={
            "description": "Check drive eligibility: a candidate qualifies if age >= 18 AND (cgpa >= 7.0 AND hasCleanRecord). Test with age 21, cgpa 7.5, clean record true, and print the result.",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        int age = 21;\n"
                "        double cgpa = 7.5;\n"
                "        boolean hasCleanRecord = true;\n"
                "        // Compute and print the eligibility\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "Use && to require age >= 18 and cgpa >= 7.0",
                "Combine with hasCleanRecord using another &&",
                "All three conditions hold here, so the result is true",
            ],
            "expected_output": "Qualifies: true",
        },
        quiz={
            "question": "What does true || false && false evaluate to?",
            "options": ["false", "true", "A compiler error", "0"],
            "correct": 1,
            "explanation": "&& binds tighter than ||, so it is true || (false && false) which is true || false = true.",
        },
        key_takeaways=[
            "&& is true only when both sides are true",
            "|| is true when at least one side is true",
            "! flips a boolean",
            "&& and || short-circuit; put cheap null checks on the left",
        ],
        next_steps="Now let us go down to the hardware level with bitwise operators!",
    ),

    _lesson(
        lesson_id="java-l03-04",
        theory=(
            "Bitwise operators work directly on the bits of integers: & (AND), | (OR), ^ (XOR), "
            "~ (NOT), << (left shift), and >> (right shift). They are the fastest way to pack "
            "multiple on/off switches into one int and are used in graphics, networking, and "
            "game engines. On booleans, & and | also work, but && and || are preferred for "
            "logic."
        ),
        analogy=(
            "Think of bits as light switches on a panel. & keeps a switch on only if both "
            "panels have it on. | turns it on if either panel does. ^ turns it on if exactly "
            "one does. Shifting is like sliding every switch one position left or right along "
            "the panel."
        ),
        sections=[
            {
                "heading": "The bitwise tools",
                "body": (
                    "Take a = 12 (1100) and b = 10 (1010). a & b is 1000 (8), a | b is 1110 "
                    "(14), and a ^ b is 0110 (6). The NOT operator ~ flips every bit, so ~12 is "
                    "-13 in Java's two's complement. Shift operators move bits: 12 << 1 is 24 "
                    "(doubling), 12 >> 1 is 6 (halving)."
                ),
                "pro_tip": (
                    "Memorize two facts: left shift by 1 doubles, right shift by 1 halves. "
                    "Watch for overflow when shifting into the sign bit."
                ),
            },
            {
                "heading": "Bitwise on booleans vs ints",
                "body": (
                    "The same & and | symbols work on booleans too, but with a crucial "
                    "difference: they always evaluate both sides, with no short-circuiting. For "
                    "readable logic, always prefer && and ||. Reserve the single-character "
                    "operators for actual bit manipulation."
                ),
                "pro_tip": (
                    "The right shift >> preserves the sign bit (arithmetic shift); use >>> for "
                    "an unsigned shift that always fills with zeros."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        int a = 12;  // 1100 in binary\n"
            "        int b = 10;  // 1010 in binary\n"
            "        System.out.println(\"a & b = \" + (a & b));  // 1000 = 8\n"
            "        System.out.println(\"a | b = \" + (a | b));  // 1110 = 14\n"
            "        System.out.println(\"a ^ b = \" + (a ^ b));  // 0110 = 6\n"
            "        System.out.println(\"~a = \" + (~a));\n"
            "        System.out.println(\"a << 1 = \" + (a << 1));\n"
            "    }\n"
            "}",
            [
                {"line": 5, "text": "AND of 1100 and 1010 is 1000 = 8"},
                {"line": 6, "text": "OR is 1110 = 14"},
                {"line": 7, "text": "XOR is 0110 = 6"},
                {"line": 8, "text": "NOT flips all bits: ~12 is -13"},
                {"line": 9, "text": "Left shift doubles: 12 becomes 24"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "int result = 12 >> 1; expecting the sign to be lost",
                "fixed": "Using >>> for a logical shift that fills with zeros",
                "why": ">> preserves the sign bit; >>> always shifts in zeros.",
            },
            {
                "wrong": "if (a & b) in conditions instead of a && b",
                "fixed": "if (a && b)",
                "why": "& evaluates both sides and reads as bit logic; && short-circuits.",
            },
            {
                "wrong": "int r = ~5; expecting -5",
                "fixed": "Understanding ~5 is -6 in two's complement",
                "why": "NOT flips all 32 bits including the sign bit.",
            },
        ],
        exercise={
            "description": "Compute and print 12 & 5, 12 | 5, 12 ^ 5, and 12 << 1.",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        int a = 12;\n"
                "        int b = 5;\n"
                "        // Print a & b, a | b, a ^ b, and a << 1\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "12 (1100) & 5 (0101) = 0100 = 4",
                "a | b is 13 and a ^ b is 9",
                "a << 1 doubles 12 to 24",
            ],
            "expected_output": (
                "a & b = 4\n"
                "a | b = 13\n"
                "a ^ b = 9\n"
                "a << 1 = 24"
            ),
        },
        quiz={
            "question": "What is 6 & 3?",
            "options": ["7", "6", "2", "3"],
            "correct": 2,
            "explanation": "6 is 110 and 3 is 011; AND gives 010, which is 2.",
        },
        key_takeaways=[
            "Bitwise operators: & | ^ ~ << >> work on integer bits",
            "& keeps a bit only if both have it; | if either has it; ^ if exactly one",
            "x << 1 doubles and x >> 1 halves an int",
            "Use && and || for logic; reserve & and | for bit manipulation",
        ],
        next_steps="Let us check object types with the instanceof operator!",
    ),

    _lesson(
        lesson_id="java-l03-05",
        theory=(
            "The instanceof operator checks whether an object is of a particular type and "
            "returns a boolean. It shines with inheritance: an object of a subclass is also an "
            "instance of its superclass. Because null is not an object, null instanceof "
            "anything is always false. This operator lets you safely inspect and handle objects "
            "of unknown types."
        ),
        analogy=(
            "instanceof is like a badge scanner at an office building: it checks whether a card "
            "holder belongs to a certain department. A manager's badge passes the Employee "
            "scanner too, just like a Dog passes both the Dog and Animal checks. A blank card "
            "(null) never passes any scanner."
        ),
        sections=[
            {
                "heading": "Checking types",
                "body": (
                    "Animal pet = new Dog(); creates a Dog but stores it in an Animal variable. "
                    "pet instanceof Dog is true because the real object is a Dog, and pet "
                    "instanceof Animal is also true because Dog inherits from Animal. Every "
                    "object is an instanceof Object, the root of all classes."
                ),
                "pro_tip": (
                    "Every class you write extends Object automatically, so every object passes "
                    "the instanceof Object check."
                ),
            },
            {
                "heading": "instanceof with inheritance and null",
                "body": (
                    "The classic safe pattern guards a downcast: if (pet instanceof Dog) { Dog d "
                    "= (Dog) pet; ... }. The check guarantees the cast cannot fail. And remember "
                    "the quirk: a null reference returns false, not an error, so you never crash "
                    "checking a null value."
                ),
                "pro_tip": (
                    "Modern Java (16+) even lets you write if (pet instanceof Dog d) to declare "
                    "the variable directly in the condition."
                ),
            },
        ],
        code_example=_code(
            "class Animal {}\n"
            "class Dog extends Animal {}\n"
            "\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Animal pet = new Dog();\n"
            "        System.out.println(\"pet is Dog: \" + (pet instanceof Dog));\n"
            "        System.out.println(\"pet is Animal: \" + (pet instanceof Animal));\n"
            "        System.out.println(\"pet is Object: \" + (pet instanceof Object));\n"
            "    }\n"
            "}",
            [
                {"line": 1, "text": "A simple parent class"},
                {"line": 2, "text": "Dog extends Animal, inheriting its type"},
                {"line": 6, "text": "A Dog object stored in an Animal variable"},
                {"line": 7, "text": "The real object is a Dog, so this is true"},
                {"line": 8, "text": "Dog is also an Animal, so this is true"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "if (5 instanceof Integer)",
                "fixed": "if (Integer.valueOf(5) instanceof Integer)",
                "why": "instanceof works on objects, not primitives; wrap the value first.",
            },
            {
                "wrong": "null instanceof Dog expecting an error",
                "fixed": "Understanding it quietly returns false",
                "why": "null is not an object, so instanceof safely returns false.",
            },
            {
                "wrong": "Believing pet instanceof Animal is false for a Dog",
                "fixed": "Understanding a subclass is also an instance of its superclass",
                "why": "Dog extends Animal, so every Dog is also an Animal.",
            },
        ],
        exercise={
            "description": "Given Animal pet = new Dog();, print three checks: pet instanceof Dog, pet instanceof Animal, and pet instanceof String.",
            "starter_code": (
                "class Animal {}\n"
                "class Dog extends Animal {}\n"
                "\n"
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        Animal pet = new Dog();\n"
                "        // Print the three instanceof checks\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "pet instanceof Dog is true, the object really is a Dog",
                "pet instanceof Animal is true, Dog inherits from Animal",
                "pet instanceof String is false, the object is not a String",
            ],
            "expected_output": (
                "pet is Dog: true\n"
                "pet is Animal: true\n"
                "pet is String: false"
            ),
        },
        quiz={
            "question": "What does null instanceof String return?",
            "options": ["true", "false", "A compile error", "NullPointerException"],
            "correct": 1,
            "explanation": "null is not an object, so instanceof always returns false for it.",
        },
        key_takeaways=[
            "instanceof checks whether an object is of a given type",
            "A subclass object is also an instance of its superclass",
            "null instanceof anything is false",
            "Use instanceof to guard downcasts safely",
        ],
        next_steps="Let us compress if/else into one elegant line with the ternary!",
    ),

    _lesson(
        lesson_id="java-l03-06",
        theory=(
            "The ternary operator is a compact if/else that returns a value: condition ? "
            "valueIfTrue : valueIfFalse. It replaces a multi-line if/else with a single "
            "expression, and the two branches must produce compatible types. Use it for simple "
            "choices; for complex logic, a full if/else is clearer."
        ),
        analogy=(
            "The ternary is a fork in the road with a signpost: 'raining ? take umbrella : take "
            "sunglasses'. You read it in one glance and pick a branch instantly, instead of "
            "stopping, unfolding a map (the if/else), and studying it. It is one smooth "
            "gesture."
        ),
        sections=[
            {
                "heading": "Anatomy of the ternary",
                "body": (
                    "String result = (score >= 60) ? \"Pass\" : \"Fail\"; reads as: if score is "
                    "at least 60, result becomes Pass, otherwise Fail. The condition goes before "
                    "the ?, the true-branch between ? and :, and the false-branch after :. The "
                    "whole thing evaluates to exactly one value."
                ),
                "pro_tip": (
                    "The two branches must be compatible types; if one is int and the other "
                    "double, the result is promoted to double."
                ),
            },
            {
                "heading": "When to use it",
                "body": (
                    "Use the ternary for one small decision that fits on one line. It shines for "
                    "assignments like sign, grade letters, and default values. Once you stack "
                    "ternaries inside ternaries, readability collapses; refactor into if/else "
                    "or a method for anything multi-step."
                ),
                "pro_tip": (
                    "If you need to indent a ternary onto three lines, the choice is probably "
                    "too complex and deserves an if/else."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        int score = 82;\n"
            "        String result = (score >= 60) ? \"Pass\" : \"Fail\";\n"
            "        System.out.println(\"Result: \" + result);\n"
            "        int number = 7;\n"
            "        String type = (number % 2 == 0) ? \"Even\" : \"Odd\";\n"
            "        System.out.println(number + \" is \" + type);\n"
            "    }\n"
            "}",
            [
                {"line": 4, "text": "Ternary: true branch Pass, false branch Fail"},
                {"line": 7, "text": "A ternary built from a modulo check"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "int r = (a > b) ? 1.5 : 2;",
                "fixed": "double r = (a > b) ? 1.5 : 2;",
                "why": "The branches promote to double, so the variable must be a double.",
            },
            {
                "wrong": "String t = (a > b) ? \"a\" : (a < b) ? \"b\" : \"eq\";",
                "fixed": "Splitting nested ternaries into an if/else if/else chain",
                "why": "Nested ternaries are hard to read and easy to misplace.",
            },
            {
                "wrong": "String r = (x > 0) ? \"pos\" ; \"nonpos\";",
                "fixed": "String r = (x > 0) ? \"pos\" : \"nonpos\";",
                "why": "The ternary always needs both the ? and the :.",
            },
        ],
        exercise={
            "description": "Use a ternary to assign the grade: score >= 60 gives Pass, otherwise Fail. Print the result for score 85 and for score 41.",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        int score = 85;\n"
                "        // Assign grade with a ternary and print it\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "String grade = (score >= 60) ? \"Pass\" : \"Fail\";",
                "Print with a label like \"Grade: \" + grade",
                "For score 41 the ternary gives Fail",
            ],
            "expected_output": (
                "Grade: Pass\n"
                "Grade: Fail"
            ),
        },
        quiz={
            "question": "What does (10 > 5) ? \"big\" : \"small\" return?",
            "options": ["\"big\"", "\"small\"", "true", "10"],
            "correct": 0,
            "explanation": "The condition 10 > 5 is true, so the ternary returns the true-branch \"big\".",
        },
        key_takeaways=[
            "The ternary is a one-line if/else that returns a value",
            "Format: condition ? valueIfTrue : valueIfFalse",
            "Both branches must be compatible types",
            "Avoid nesting ternaries; prefer if/else for complex logic",
        ],
        next_steps="Time to practise building boolean expressions like a pro!",
    ),

    _lesson(
        lesson_id="java-l03-07",
        theory=(
            "Real interview questions and system logic are built from boolean expressions. A "
            "good boolean expression reads like a clear English rule: a student is eligible if "
            "cgpa >= 7.0 AND there is no active backlog. Combine relational and logical "
            "operators, and use parentheses to make the grouping obvious."
        ),
        analogy=(
            "Boolean expressions are the checklists a security guard follows: 'Is the badge "
            "valid? AND is the visitor on the list?' Each check returns yes or no, and the "
            "guard combines them to open the gate. Your if-statements are the same guard, "
            "making a single yes/no decision."
        ),
        sections=[
            {
                "heading": "Building readable rules",
                "body": (
                    "Name your boolean variables like questions: isEligible, hasPassed, "
                    "isTopper. Then an expression like marks >= 60 && marks <= 90 reads almost "
                    "exactly like the sentence it models. Small named booleans also let you "
                    "reuse a check instead of recomputing it."
                ),
                "pro_tip": (
                    "When a boolean expression grows past one line, break it into named "
                    "variables and combine those."
                ),
            },
            {
                "heading": "Parentheses for clarity",
                "body": (
                    "Operator precedence already orders things: arithmetic, then relational, "
                    "then logical. But humans read best when grouping is explicit, so wrap each "
                    "comparison in parentheses. Two rules to remember: NOT binds tighter than "
                    "AND, which binds tighter than OR, and De Morgan's laws flip "
                    "!(a && b) into !a || !b."
                ),
                "pro_tip": (
                    "When negating a compound condition, apply De Morgan: NOT (A AND B) is "
                    "NOT A OR NOT B. It turns confusing expressions into readable ones."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        int marks = 75;\n"
            "        boolean passed = marks >= 40;\n"
            "        boolean topper = marks >= 90;\n"
            "        System.out.println(\"Passed: \" + passed);\n"
            "        System.out.println(\"Topper: \" + topper);\n"
            "        System.out.println(\"Between 60 and 80: \" + (marks >= 60 && marks <= 80));\n"
            "    }\n"
            "}",
            [
                {"line": 4, "text": "A named boolean from a relational check"},
                {"line": 5, "text": "Another named boolean for a different rule"},
                {"line": 8, "text": "Two comparisons joined with && inside parentheses"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "if (a < b > c)",
                "fixed": "if (a < b && b > c)",
                "why": "Java does not chain comparisons; join them with logical operators.",
            },
            {
                "wrong": "if (name == \"Riya\" && age >= 18)",
                "fixed": "if (name.equals(\"Riya\") && age >= 18)",
                "why": "String content must be compared with equals, not ==.",
            },
            {
                "wrong": "if (marks >= 60 || attendance >= 75 && cleanRecord)",
                "fixed": "if ((marks >= 60 || attendance >= 75) && cleanRecord)",
                "why": "AND binds tighter than OR; parentheses force the intended grouping.",
            },
        ],
        exercise={
            "description": "Write the rule: a candidate qualifies if age >= 21 AND (experience >= 2 OR cgpa >= 7.5). Test with age 23, experience 1, cgpa 8.0, and print the result.",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        int age = 23;\n"
                "        int experience = 1;\n"
                "        double cgpa = 8.0;\n"
                "        // Compute and print the qualification\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "age >= 21 is true, and cgpa >= 7.5 is true",
                "So (experience >= 2 || cgpa >= 7.5) is true",
                "Combine with && and print the boolean",
            ],
            "expected_output": "Qualifies: true",
        },
        quiz={
            "question": "Which expression checks that n is between 5 and 10 inclusive?",
            "options": [
                "5 <= n <= 10",
                "n >= 5 && n <= 10",
                "n > 5 && n < 10",
                "5 < n < 10",
            ],
            "correct": 1,
            "explanation": "Inclusive means both boundaries count, so n >= 5 AND n <= 10 is correct.",
        },
        key_takeaways=[
            "Boolean expressions model real-world rules",
            "Name boolean variables like questions: isEligible",
            "Use parentheses to make grouping obvious",
            "De Morgan's laws: !(A && B) equals !A || !B",
        ],
        next_steps="Ready for a low-level puzzle? Let us build Bit Flags!",
    ),

    _lesson(
        lesson_id="java-l03-08",
        theory=(
            "A bit flag packs several true/false settings into one integer by giving each a "
            "distinct bit. Set a flag with |, clear it with & ~, and test it with &. This is "
            "how operating systems pass permission sets and how game engines track player "
            "states efficiently in a single int."
        ),
        analogy=(
            "Bit flags are like a tray of toggle switches in a control room. You flip switch 1 "
            "for READ and switch 2 for WRITE. Flipping switches on is |, flipping one back off "
            "is & ~, and checking whether a switch is on is &. One panel holds every state "
            "with no extra memory."
        ),
        sections=[
            {
                "heading": "The flag pattern",
                "body": (
                    "Give each permission its own bit: READ = 1 (001), WRITE = 2 (010), "
                    "EXECUTE = 4 (100). To set a flag, OR it in: flags = flags | READ. To test, "
                    "AND it: (flags & READ) != 0 means READ is set. To clear, AND with the "
                    "inverted flag: flags = flags & ~WRITE. The entire state lives in one int."
                ),
                "pro_tip": (
                    "Write the flags as shifts so the pattern is obvious: READ = 1 << 0, WRITE "
                    "= 1 << 1, EXECUTE = 1 << 2."
                ),
            },
            {
                "heading": "Why flags matter",
                "body": (
                    "A single int holds 32 independent booleans, making flag checks blindingly "
                    "fast. File permissions on Unix, network packet headers, and game input "
                    "masks all use this technique. It also forces you to think about data "
                    "efficiently, which interviewers notice."
                ),
                "pro_tip": (
                    "Precedence gotcha: (flags & READ) != 0 needs its parentheses, because "
                    "relational operators bind tighter than &."
                ),
            },
        ],
        code_example=_code(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        int flags = 0;\n"
            "        final int READ = 1;    // 001\n"
            "        final int WRITE = 2;   // 010\n"
            "        final int EXECUTE = 4; // 100\n"
            "        flags = flags | READ;\n"
            "        flags = flags | WRITE;\n"
            "        System.out.println(\"Has READ: \" + ((flags & READ) != 0));\n"
            "        System.out.println(\"Has EXECUTE: \" + ((flags & EXECUTE) != 0));\n"
            "        flags = flags & ~WRITE;\n"
            "        System.out.println(\"Has WRITE after clear: \" + ((flags & WRITE) != 0));\n"
            "    }\n"
            "}",
            [
                {"line": 4, "text": "Each flag owns its own bit"},
                {"line": 7, "text": "OR sets the READ bit"},
                {"line": 9, "text": "AND tests whether READ is set"},
                {"line": 11, "text": "AND with ~WRITE clears the WRITE bit"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "flags = flags & WRITE; intending to clear WRITE",
                "fixed": "flags = flags & ~WRITE;",
                "why": "& WRITE keeps only that bit and wipes everything else; invert first with ~.",
            },
            {
                "wrong": "READ = 1; WRITE = 2; EXECUTE = 3;",
                "fixed": "EXECUTE = 4, giving each flag its own bit",
                "why": "Overlapping values collide; each flag needs a unique bit.",
            },
            {
                "wrong": "(flags & READ != 0) without parentheses",
                "fixed": "((flags & READ) != 0)",
                "why": "!= binds tighter than &, so the comparison happens first without parens.",
            },
        ],
        exercise={
            "description": "Add a DELETE flag with value 8 to the program, set it, print whether it is set, then clear it and print whether it is still set.",
            "starter_code": (
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        int flags = 0;\n"
                "        final int DELETE = 8; // 1000\n"
                "        // Set DELETE, print the test, clear it, print again\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "flags = flags | DELETE; sets the bit",
                "(flags & DELETE) != 0 tests it: first true, then false",
                "flags = flags & ~DELETE; clears the bit",
            ],
            "expected_output": (
                "Has DELETE: true\n"
                "Has DELETE after clear: false"
            ),
        },
        quiz={
            "question": "How do you set a flag bit in Java?",
            "options": ["flags & READ", "flags | READ", "flags ^ READ", "flags >> READ"],
            "correct": 1,
            "explanation": "OR (|) turns the bit on: flags | READ sets the READ bit.",
        },
        key_takeaways=[
            "Bit flags pack many booleans into one int",
            "Set with |, test with &, clear with & ~",
            "Each flag needs its own unique bit",
            "Parenthesize flag tests: (flags & READ) != 0",
        ],
        next_steps="Final boss: build the Math Expression Evaluator project!",
    ),

    _lesson(
        lesson_id="java-l03-09",
        theory=(
            "The Math Expression Evaluator is a mini interpreter: it reads two numbers and an "
            "operator, applies the matching arithmetic, and prints the result. It brings "
            "together Scanner input, char comparison, if/else selection, and arithmetic, the "
            "core skills behind real calculators and even compilers and parsers."
        ),
        analogy=(
            "You are building the cash register for a math shop: a customer says 3 + 4, your "
            "register checks which drawer (operator) to open, does the math, and prints the "
            "receipt. Change the operator and the whole flow repeats, exactly like a real "
            "calculator."
        ),
        sections=[
            {
                "heading": "Parsing the input",
                "body": (
                    "Read the first number with nextDouble(), then read the operator as a char "
                    "using scanner.next().charAt(0), then the second number. A single char "
                    "cleanly holds all four symbols: +, -, *, and /. Storing the operator as a "
                    "char is the key trick that keeps the program small."
                ),
                "pro_tip": (
                    "Prompt clearly for each input so the user knows the expected format, like "
                    "Enter operator (+, -, *, /):."
                ),
            },
            {
                "heading": "Choosing the operation",
                "body": (
                    "An if/else-if chain compares the operator against each symbol and runs the "
                    "matching branch. Use a separate else for invalid input so the program "
                    "never crashes on a typo. Also guard division: only divide when the second "
                    "number is not zero, otherwise an int division by zero throws an "
                    "ArithmeticException."
                ),
                "pro_tip": (
                    "The if/else-if chain here is the same pattern a switch statement uses; "
                    "either works, and if/else reads well for beginners."
                ),
            },
            {
                "heading": "From calculator to parser",
                "body": (
                    "This evaluator is a tiny taste of parsing: splitting input, deciding what "
                    "it means, and computing a result. Real compilers do the same steps at a "
                    "much larger scale with tokenizers and expression trees. Understanding this "
                    "project means you already grasp the skeleton of every interpreter."
                ),
                "pro_tip": (
                    "Extend it later: add a power operator, support more than two operands, or "
                    "wrap the logic in a method called evaluate(a, op, b)."
                ),
            },
        ],
        code_example=_code(
            "import java.util.Scanner;\n"
            "\n"
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        Scanner scanner = new Scanner(System.in);\n"
            "        System.out.print(\"Enter first number: \");\n"
            "        double a = scanner.nextDouble();\n"
            "        System.out.print(\"Enter operator (+, -, *, /): \");\n"
            "        char op = scanner.next().charAt(0);\n"
            "        System.out.print(\"Enter second number: \");\n"
            "        double b = scanner.nextDouble();\n"
            "        double result = 0;\n"
            "        if (op == '+') {\n"
            "            result = a + b;\n"
            "        } else if (op == '-') {\n"
            "            result = a - b;\n"
            "        } else if (op == '*') {\n"
            "            result = a * b;\n"
            "        } else if (op == '/') {\n"
            "            result = a / b;\n"
            "        } else {\n"
            "            System.out.println(\"Invalid operator!\");\n"
            "        }\n"
            "        System.out.println(a + \" \" + op + \" \" + b + \" = \" + result);\n"
            "        scanner.close();\n"
            "    }\n"
            "}",
            [
                {"line": 7, "text": "Reads the first number"},
                {"line": 9, "text": "Reads one character as the operator"},
                {"line": 13, "text": "If/else-if chain selects the operation"},
                {"line": 21, "text": "Handles any unexpected operator"},
                {"line": 24, "text": "Prints the full expression and result"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "result = a / b; without a zero check",
                "fixed": "Checking b != 0 before dividing",
                "why": "Division by zero throws ArithmeticException and crashes the program.",
            },
            {
                "wrong": "char op = scanner.next();",
                "fixed": "char op = scanner.next().charAt(0);",
                "why": "next() returns a String; charAt(0) extracts its first character.",
            },
            {
                "wrong": "Forgetting to close the scanner",
                "fixed": "Calling scanner.close() at the end",
                "why": "An unclosed scanner leaks the keyboard resource.",
            },
        ],
        exercise={
            "description": "Extend the evaluator to support the % (modulo) operator: add an else if branch for % and print the remainder.",
            "starter_code": (
                "import java.util.Scanner;\n"
                "\n"
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        Scanner scanner = new Scanner(System.in);\n"
                "        System.out.print(\"Enter first number: \");\n"
                "        double a = scanner.nextDouble();\n"
                "        System.out.print(\"Enter operator (+, -, *, /, %): \");\n"
                "        char op = scanner.next().charAt(0);\n"
                "        System.out.print(\"Enter second number: \");\n"
                "        double b = scanner.nextDouble();\n"
                "        double result = 0;\n"
                "        // Add an else-if branch for op == '%'\n"
                "        System.out.println(a + \" \" + op + \" \" + b + \" = \" + result);\n"
                "        scanner.close();\n"
                "    }\n"
                "}"
            ),
            "hints": [
                "Add: } else if (op == '%') { result = a % b; }",
                "Modulo on doubles works: 17 % 5 is 2.0",
                "Update the prompt to include % so users know it is supported",
            ],
            "expected_output": "17 % 5 = 2.0",
        },
        quiz={
            "question": "Which condition safely guards a division?",
            "options": ["if (b != 0)", "if (b == 0)", "Always dividing anyway", "if (a > 0)"],
            "correct": 0,
            "explanation": "Checking b != 0 before dividing prevents the ArithmeticException on division by zero.",
        },
        key_takeaways=[
            "An evaluator reads input, parses an operator, and computes",
            "Store operators as char and select with if/else-if",
            "Guard division by zero before dividing",
            "This project is the skeleton of real calculators and parsers",
        ],
        next_steps="Level 3 complete! You have mastered Java fundamentals, so keep building!",
    ),
]))
