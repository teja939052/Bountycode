"""Hand-crafted lesson content for C++ levels 1-3.

Lesson ID format: cpp-l{level:02d}-{lesson:02d}
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


HAND_CRAFTED_CPP_LESSONS: dict[str, dict[str, Any]] = {}

HAND_CRAFTED_CPP_LESSONS.update(dict([
    # =========================================================================
    # LEVEL 1: FIRST STEPS
    # =========================================================================
    _lesson(
        lesson_id="cpp-l01-01",
        theory=(
            "C++ is a powerful programming language created by Bjarne Stroustrup in the 1980s. "
            "It was designed as an extension of C that adds object-oriented features while keeping "
            "C's speed and control. Today it powers game engines, operating systems, browsers, "
            "and trading systems that need maximum performance."
        ),
        analogy=(
            "Learning C++ is like upgrading from a bicycle (C) to a motorcycle. "
            "A motorcycle has everything the bicycle has, plus an engine (classes), "
            "gears (templates), and safety features (smart pointers). "
            "Once you learn to ride it, you can go much further and faster."
        ),
        sections=[
            {
                "heading": "What makes C++ special?",
                "body": (
                    "Three things: performance, control, and richness. C++ compiles directly to "
                    "machine code so it runs extremely fast. You control memory exactly when to "
                    "allocate and free it. And it gives you modern tools like classes, templates, "
                    "the Standard Template Library (STL), and smart pointers all in one language."
                ),
                "pro_tip": (
                    "C++ is the backbone of the video game industry. Games like Fortnite and "
                    "AAA titles are built with Unreal Engine, which is written in C++."
                ),
            },
            {
                "heading": "Who uses C++ today?",
                "body": (
                    "C++ programmers work on game engines, high-frequency trading systems, browsers "
                    "(Chrome, Firefox), databases, robotics, and self-driving cars. Companies like "
                    "Google, Microsoft, Meta, and Adobe rely on C++ for performance-critical software."
                ),
                "pro_tip": (
                    "Knowing C++ gives you a huge placement advantage because it proves you can "
                    "handle performance-critical and complex systems."
                ),
            },
        ],
        key_takeaways=[
            "C++ is a fast, compiled language that extends C with modern features",
            "C++ powers game engines, browsers, and financial systems",
            "C++ gives you both low-level control and high-level abstractions",
            "C++ is one of the most in-demand languages for core engineering roles",
        ],
        next_steps="Ready to write your first C++ program? Let us move to the next lesson!",
    ),

    _lesson(
        lesson_id="cpp-l01-02",
        theory=(
            "Time to write your first C++ program! Every C++ program starts with a function called "
            "main. When you run your program, the computer looks for main and starts executing "
            "the code inside its curly braces {}."
            "\n\n"
            "At the top you will see #include <iostream>. This line brings in the iostream "
            "library, which gives you tools to read input and print output. You will use it in "
            "almost every program you write."
            "\n\n"
            "The line using namespace std; lets you write cout instead of std::cout. "
            "cout (pronounced see-out) is how you print text to the screen in C++. "
            "The << symbol pushes the text into cout, and endl adds a new line."
            "\n\n"
            "Finally, return 0; tells the operating system that the program finished successfully."
        ),
        analogy=(
            "A C++ program is like a relay race. #include <iostream> is the coach gathering your "
            "gear. using namespace std; is knowing the shortcuts on the track. int main() is the "
            "starting gun. cout << is the baton that carries your message across the finish line. "
            "And return 0; is the team celebrating a clean win."
        ),
        sections=[
            {
                "heading": "The hello world program",
                "body": (
                    "Here is the complete program. Type it exactly as shown, then click Run. "
                    "Every character matters, especially the semicolons at the end of each statement."
                ),
                "pro_tip": (
                    "In C++, every statement ends with a semicolon ;. Forgetting one is the most "
                    "common beginner error, and your compiler will tell you exactly where."
                ),
            },
            {
                "heading": "Reading the output",
                "body": (
                    "When you run the program, you will see Hello World! printed on the screen. "
                    "The endl at the end moves the cursor to a new line, so the next output "
                    "starts fresh."
                ),
                "pro_tip": (
                    "Try changing the text inside the double quotes and running again. "
                    "You are already editing code!"
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    cout << \"Hello World!\" << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 1, "text": "Includes the iostream library for input/output"},
                {"line": 2, "text": "Lets us write cout instead of std::cout"},
                {"line": 4, "text": "The main function, where every program starts"},
                {"line": 5, "text": "Prints Hello World! to the screen"},
                {"line": 6, "text": "Signals the program ended successfully"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "cout << \"Hello World!\"\n",
                "fixed": "cout << \"Hello World!\" << endl;\n",
                "why": "Every statement must end with a semicolon in C++.",
            },
            {
                "wrong": "using namespace std; cout << ...",
                "fixed": "#include <iostream>\nusing namespace std;\n",
                "why": "You must include <iostream> before you can use cout.",
            },
            {
                "wrong": 'cout >> "Hello";',
                "fixed": 'cout << "Hello";',
                "why": "cout uses << to send data out. The >> symbol is for reading input with cin.",
            },
        ],
        exercise={
            "description": "Modify the hello world program to print your name, like: My name is Priya. Then add a second line that prints your favourite subject.",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "Use cout << \"Your text\" << endl; to print each line",
                "Add a second cout line to print the second message",
                "End every statement with a semicolon",
            ],
            "expected_output": (
                "My name is <your name>\n"
                "My favourite subject is <your subject>"
            ),
        },
        quiz={
            "question": "Which function does every C++ program start executing from?",
            "options": ["start()", "main()", "run()", "begin()"],
            "correct": 1,
            "explanation": "The C++ compiler always looks for the main function as the entry point of the program.",
        },
        key_takeaways=[
            "Every C++ program needs a main function",
            "#include <iostream> gives you input/output tools",
            "cout << prints text to the screen",
            "Every statement ends with a semicolon",
        ],
        next_steps="Now that you can print, let us explore iostream and cout in detail!",
    ),

    _lesson(
        lesson_id="cpp-l01-03",
        theory=(
            "iostream is the standard header that powers all console input and output in C++. "
            "It defines cout, which represents the standard output stream that prints text to "
            "your terminal. The insertion operator << pushes whatever is on its right into the "
            "stream, so cout << \"text\" sends text to the screen."
            "\n\n"
            "You can chain many values in one statement: cout << \"The answer is \" << 42 << endl. "
            "Each << sends the next piece out in order. endl finishes the line and moves to a "
            "fresh one, which keeps your output tidy and readable."
        ),
        analogy=(
            "Think of cout as a message conveyor belt. Every << places one item on the belt, and "
            "the items travel in order to the screen. endl is the button that releases the belt "
            "and drops a fresh, empty one for your next message."
        ),
        sections=[
            {
                "heading": "The output stream",
                "body": (
                    "cout is an object that represents the standard output, normally your terminal. "
                    "The << operator sends data into it, and C++ figures out how to display whatever "
                    "you give it, text, numbers, or the result of an expression."
                ),
                "pro_tip": (
                    "When printing a calculation, wrap it in parentheses: cout << (5 + 3). "
                    "Without them, operator precedence can surprise you."
                ),
            },
            {
                "heading": "Chaining values",
                "body": (
                    "One cout statement can print several values in a row. Each << adds the next "
                    "item, so a label, the number 8, and a newline can all go out in a single line "
                    "of code."
                ),
                "pro_tip": (
                    "endl flushes the output buffer, which is great for interactive prompts. "
                    "For pure text output, a plain newline is slightly faster."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    cout << \"Welcome to C++!\";\n"
            "    cout << endl;\n"
            "    cout << \"Sum of 5 and 3 is \" << (5 + 3) << endl;\n"
            "    cout << \"Tab\" << \"\\t\" << \"here\" << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 1, "text": "Includes the iostream library"},
                {"line": 2, "text": "Brings std names into scope"},
                {"line": 4, "text": "Program entry point"},
                {"line": 5, "text": "Prints text without a trailing newline"},
                {"line": 6, "text": "endl moves to a new line"},
                {"line": 7, "text": "Chaining << prints several values in order"},
                {"line": 9, "text": "Successful exit"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "cout >> \"hi\";",
                "fixed": "cout << \"hi\";",
                "why": "cout uses the insertion operator << to send data out. >> is for reading input.",
            },
            {
                "wrong": "cout << \"hi\" endl;",
                "fixed": "cout << \"hi\" << endl;",
                "why": "Every value sent to cout needs its own <<, including endl.",
            },
            {
                "wrong": "Cout << \"hi\";",
                "fixed": "cout << \"hi\";",
                "why": "C++ is case-sensitive, so Cout is a different, unknown name.",
            },
        ],
        exercise={
            "description": "Print a short introduction using chained cout statements on three lines: your name, your city, and your favourite food.",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "Start each line with cout <<",
                "Put your text inside double quotes",
                "Finish each line with << endl;",
            ],
            "expected_output": (
                "My name is <your name>\n"
                "My city is <your city>\n"
                "My favourite food is <your food>"
            ),
        },
        quiz={
            "question": "Which symbol does cout use to send text to the screen?",
            "options": [">>", "<<", "||", "&&"],
            "correct": 1,
            "explanation": "cout uses the insertion operator <<, which pushes values into the output stream.",
        },
        key_takeaways=[
            "#include <iostream> provides cout for output",
            "The << operator sends values to the screen",
            "You can chain multiple values in one cout statement",
            "endl ends the line and flushes the output",
        ],
        next_steps="You can print anything now. Next, let us learn how to read input from the user!",
    ),

    _lesson(
        lesson_id="cpp-l01-04",
        theory=(
            "cin is the counterpart to cout: it reads typed input from the keyboard into your "
            "program. You use the extraction operator >> in the opposite direction: cin >> variable. "
            "The variable must be declared first, and its type tells cin how to interpret the "
            "characters you type."
            "\n\n"
            "A single cin statement can read multiple values separated by spaces, like "
            "cin >> x >> y. But cin stops at whitespace, so it is great for numbers and single "
            "words, while reading a whole line needs getline."
        ),
        analogy=(
            "cin is like a ticket scanner at a metro gate. Each value walks through one at a time, "
            "and the scanner knows exactly what kind of ticket to expect from the variable's type. "
            "If you feed it a train of passengers with spaces between them, it lets them through "
            "one by one."
        ),
        sections=[
            {
                "heading": "Reading a number",
                "body": (
                    "Declare an int first, then prompt the user, then read: cin >> age. The prompt "
                    "is important, without it the program seems frozen while waiting for input."
                ),
                "pro_tip": (
                    "Always print a prompt before cin so the user knows what to type. "
                    "A program that silently waits feels broken."
                ),
            },
            {
                "heading": "Reading multiple values",
                "body": (
                    "cin >> a >> b reads two numbers in one statement, separated by a space or a "
                    "newline. It works because >> evaluates left to right, filling each variable "
                    "in turn."
                ),
                "pro_tip": (
                    "cin >> stops at whitespace, so it cannot read a full sentence. "
                    "Use getline(cin, text) when you want the entire line."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    int age;\n"
            "    cout << \"Enter your age: \";\n"
            "    cin >> age;\n"
            "    cout << \"You are \" << age << \" years old.\" << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 5, "text": "Declares an int variable to hold the input"},
                {"line": 6, "text": "Prompts the user before reading"},
                {"line": 7, "text": "cin >> reads the typed value into age"},
                {"line": 8, "text": "Echoes the stored value back"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "cin << age;",
                "fixed": "cin >> age;",
                "why": "cin uses the extraction operator >>. << would try to send data into cin.",
            },
            {
                "wrong": "cin >> \"age\";",
                "fixed": "cin >> age;",
                "why": "cin stores into a variable, not into a quoted string literal.",
            },
            {
                "wrong": "cin >> age; // but int age; was never declared",
                "fixed": "int age;\ncin >> age;",
                "why": "The variable must exist before cin can store into it.",
            },
        ],
        exercise={
            "description": "Read two whole numbers from the user and print their sum, like: 7 and 8 should print Sum is 15.",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    int first, second;\n"
                "    cout << \"Enter first number: \";\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "Read the second number with cin >> second;",
                "Add them and print with cout << \"Sum is \" << (first + second) << endl;",
                "Test with 7 and 8",
            ],
            "expected_output": "Sum is 15",
        },
        quiz={
            "question": "Which operator reads a value into a variable using cin?",
            "options": [">>", "<<", "&", "="],
            "correct": 0,
            "explanation": "cin uses the extraction operator >>, which pulls typed input into the variable.",
        },
        key_takeaways=[
            "cin reads keyboard input into variables",
            "Declare the variable before reading into it",
            "cin >> stops at whitespace",
            "Always prompt before reading input",
        ],
        next_steps="Input unlocks interactive programs. Next up, namespaces and the std prefix!",
    ),

    _lesson(
        lesson_id="cpp-l01-05",
        theory=(
            "Namespaces are containers that group related names so they never collide. All the "
            "standard C++ features live in the std namespace. You can either write std::cout each "
            "time, or add using namespace std; once after your includes to use cout, cin, and endl "
            "without the prefix."
            "\n\n"
            "Qualified names like std::cout are explicit and always safe. The using directive is "
            "convenient for small programs, but in large projects it can cause name clashes, which "
            "is why production code usually prefers the explicit prefix."
        ),
        analogy=(
            "A namespace is like a department in a large office. Several teams may each have a "
            "Manager, but 'HR.Manager' and 'Sales.Manager' are unambiguous. using namespace std; is "
            "like pinning a sign on the wall that says 'when in doubt, we mean the standard "
            "department'."
        ),
        sections=[
            {
                "heading": "What lives in std?",
                "body": (
                    "cout, cin, endl, string, and the entire Standard Template Library all live in "
                    "the std namespace. The :: symbol is the scope resolution operator, it says "
                    "'look up cout inside std'."
                ),
                "pro_tip": (
                    "Reading std::cout aloud as 'standard cout' helps you remember what the "
                    "prefix means."
                ),
            },
            {
                "heading": "Using namespace std",
                "body": (
                    "This directive brings all the std names into the current scope, so you can "
                    "type cout directly. It is safe in small teaching programs, but writing "
                    "std:: explicitly scales better."
                ),
                "pro_tip": (
                    "Never put using namespace std; inside a header file, it leaks the directive "
                    "into every file that includes it."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "\n"
            "int main() {\n"
            "    std::cout << \"Hello from std!\" << std::endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 1, "text": "Includes iostream without importing its names"},
                {"line": 4, "text": "std::cout and std::endl are fully qualified"},
                {"line": 5, "text": "Returns success"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "cout << \"hi\"; // with no using namespace std;",
                "fixed": "std::cout << \"hi\";",
                "why": "Without the using directive, cout must be written as std::cout.",
            },
            {
                "wrong": "using namespace std; // placed inside a header file",
                "fixed": "std::cout << \"hi\"; // keep the directive out of headers",
                "why": "A using directive in a header leaks into every file that includes it.",
            },
            {
                "wrong": "Using namespace std;",
                "fixed": "using namespace std;",
                "why": "C++ keywords are lowercase, so Using is an unknown identifier.",
            },
        ],
        exercise={
            "description": "Print 'Welcome to the C++ course!' WITHOUT using using namespace std. Use the fully qualified std::cout and std::endl instead.",
            "starter_code": (
                "#include <iostream>\n"
                "\n"
                "int main() {\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "Use std::cout with the << operator",
                "Use std::endl to end the line",
                "Every statement ends with a semicolon",
            ],
            "expected_output": "Welcome to the C++ course!",
        },
        quiz={
            "question": "What does the std:: prefix refer to?",
            "options": ["A data type", "A namespace", "A variable", "A function"],
            "correct": 1,
            "explanation": "std is the namespace that holds C++'s standard features like cout and string.",
        },
        key_takeaways=[
            "Namespaces prevent name collisions",
            "Standard C++ features live in the std namespace",
            "std::cout explicitly names the output stream",
            "using namespace std; is convenient but can cause clashes",
        ],
        next_steps="Now let us make your code easier to read with comments!",
    ),

    _lesson(
        lesson_id="cpp-l01-06",
        theory=(
            "Comments are notes you leave in your code for humans. The compiler ignores them "
            "completely, so they never affect your program. C++ gives you two ways to write them: "
            "// starts a comment that lasts until the end of the line, and /* ... */ marks a block "
            "that can span multiple lines."
            "\n\n"
            "Good comments explain why the code exists, not what each obvious line does. Write "
            "them while the idea is fresh, because future-you will thank present-you."
        ),
        analogy=(
            "Comments are like sticky notes stuck onto a recipe page. They never end up in the "
            "dish, but they remind you why you chose a particular step and help anyone else who "
            "opens your recipe book understand it at a glance."
        ),
        sections=[
            {
                "heading": "Single-line comments",
                "body": (
                    "Anything after // on a line is ignored by the compiler. This is perfect for a "
                    "short note next to a tricky line or a header describing a function's purpose."
                ),
                "pro_tip": (
                    "Comment the 'why', not the 'what'. The code already shows what it does; "
                    "your note should explain the reasoning behind it."
                ),
            },
            {
                "heading": "Block comments",
                "body": (
                    "/* ... */ can wrap several lines. Use them for longer explanations, "
                    "disclaimers, or temporarily disabling a chunk of code while you debug."
                ),
                "pro_tip": (
                    "Block comments cannot be nested safely. A second /* inside a block comment "
                    "does not open a new block, the first */ still ends everything."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    // This is a single-line comment\n"
            "    cout << \"Comments help you remember\" << endl;\n"
            "    /* This block spans\n"
            "       multiple lines */\n"
            "    return 0;\n"
            "}",
            [
                {"line": 5, "text": "// comments out the rest of the line"},
                {"line": 6, "text": "Executable code follows the comment"},
                {"line": 7, "text": "/* starts a multi-line block comment"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "/* outer /* inner */ still continues here */",
                "fixed": "/* outer block */ // inner as a separate // comment",
                "why": "Block comments do not nest, the first */ ends the whole block.",
            },
            {
                "wrong": "/* second comment (never closed)",
                "fixed": "/* second comment */",
                "why": "An unclosed /* swallows everything until the next */, if one exists at all.",
            },
            {
                "wrong": "// cout << \"old code\";  (left disabled forever)",
                "fixed": "// delete the line, or fix it properly",
                "why": "Commented-out code rots and confuses readers. Version control remembers it.",
            },
        ],
        exercise={
            "description": "Write a program that prints 'Hello C++!' and use comments to label the main function and the print statement, just like a professional code review.",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "Add a // comment describing int main()",
                "Add a // comment before the cout line",
                "Comments must come before or beside the code they explain",
            ],
            "expected_output": "Hello C++!",
        },
        quiz={
            "question": "Which of these is a valid single-line comment in C++?",
            "options": ["/* comment */", "<!-- comment -->", "// comment", "# comment"],
            "correct": 2,
            "explanation": "// starts a single-line comment in C++. /* */ is a block comment.",
        },
        key_takeaways=[
            "Comments are ignored by the compiler",
            "// marks a single-line comment",
            "/* ... */ marks a multi-line block comment",
            "Comment the why, not the obvious what",
        ],
        next_steps="Now let us combine everything into a real interactive greeting program!",
    ),

    _lesson(
        lesson_id="cpp-l01-07",
        theory=(
            "A greeting program is the classic first real program: it asks for your name, "
            "remembers it, and greets you. It combines everything so far, the #include <iostream> "
            "header, cout for prompts, cin for input, and string for storing text."
            "\n\n"
            "Notice the rhythm: prompt, read, then respond. That prompt-then-read pattern is the "
            "backbone of almost every interactive program you will ever write."
        ),
        analogy=(
            "A greeting program is like a friendly receptionist. They ask your name (prompt), "
            "listen while you say it (cin), then use it in their welcome message (cout). The whole "
            "exchange follows one simple script."
        ),
        sections=[
            {
                "heading": "The prompt-read-response rhythm",
                "body": (
                    "Each input needs a prompt first so the user knows what to type. Then cin "
                    "captures the value, and finally cout uses it in the response. Keep the order "
                    "and your programs will always feel responsive."
                ),
                "pro_tip": (
                    "Use string for names and int for ages. Mixing up types is the most common "
                    "way to break a simple program."
                ),
            },
            {
                "heading": "Working with strings and numbers together",
                "body": (
                    "cout happily mixes text and numbers, as long as each piece goes through its "
                    "own <<. To print an expression like age + 10, wrap it in parentheses so it "
                    "is computed before being printed."
                ),
                "pro_tip": (
                    "cin >> name only reads one word. For a full name, use "
                    "getline(cin, name); instead."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "#include <string>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    string name;\n"
            "    int age;\n"
            "    cout << \"Enter your name: \";\n"
            "    cin >> name;\n"
            "    cout << \"Enter your age: \";\n"
            "    cin >> age;\n"
            "    cout << \"Hello \" << name << \"! In 10 years you will be \"\n"
            "         << (age + 10) << \" years old.\" << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 2, "text": "string needs the <string> header"},
                {"line": 6, "text": "Declares a text variable for the name"},
                {"line": 9, "text": "Reads the typed name"},
                {"line": 12, "text": "Mixes text, a string, and a computed number"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "cin >> name;  // user types Ada Lovelace",
                "fixed": "getline(cin, name); // reads the whole line",
                "why": "cin >> stops at the first space, capturing only 'Ada'.",
            },
            {
                "wrong": "cout << \"In 10 years you will be \" << age + 10 << \" old.\" << endl;",
                "fixed": "cout << \"In 10 years you will be \" << (age + 10) << \" old.\" << endl;",
                "why": "Without parentheses, << and + can interact badly with precedence.",
            },
            {
                "wrong": "string name;  // but #include <string> is missing",
                "fixed": "#include <string>\nstring name;",
                "why": "std::string is declared in the <string> header, which must be included.",
            },
        ],
        exercise={
            "description": "Extend the greeting program: also ask for the user's city and print 'Hello <name>! You live in <city>'.",
            "starter_code": (
                "#include <iostream>\n"
                "#include <string>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    string name;\n"
                "    cout << \"Enter your name: \";\n"
                "    cin >> name;\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "Declare a string variable for the city",
                "Prompt, then read the city with cin >>",
                "Print the final greeting with both name and city",
            ],
            "expected_output": "Hello Priya! You live in Mumbai",
        },
        quiz={
            "question": "If the user types 'Ada Lovelace', what does cin >> name; store?",
            "options": ["Ada", "Ada Lovelace", "Lovelace", "An error"],
            "correct": 0,
            "explanation": "cin >> stops at whitespace, so it captures only the first word, 'Ada'.",
        },
        key_takeaways=[
            "Interactive programs follow a prompt-read-respond rhythm",
            "string stores text and needs #include <string>",
            "cin >> reads a single word, getline reads a whole line",
            "Wrap expressions in parentheses before printing",
        ],
        next_steps="You have the basics. Now let us build a mini calculator and put input to work!",
    ),

    _lesson(
        lesson_id="cpp-l01-08",
        theory=(
            "Now we build something useful: a mini calculator. It reads two numbers and an "
            "operator character, then decides which arithmetic to perform. To compare the "
            "operator, we use if, else if, and else, which run different blocks of code based on "
            "a condition."
            "\n\n"
            "The equality check uses ==, two equals signs, because a single = assigns a value. "
            "Confusing the two is one of the most famous bugs in C++ history."
        ),
        analogy=(
            "A calculator is like a vending machine. You insert the first number, press a button "
            "(the operator), insert the second number, and the machine runs the matching "
            "mechanism. If you press a button it does not have, it politely tells you."
        ),
        sections=[
            {
                "heading": "Making decisions with if",
                "body": (
                    "if (condition) runs the block only when the condition is true. else if "
                    "checks the next condition, and else catches everything left over. This "
                    "chain lets the program choose exactly one path."
                ),
                "pro_tip": (
                    "Use double for the numbers so the calculator can handle decimals, "
                    "not just whole numbers."
                ),
            },
            {
                "heading": "Choosing the operator",
                "body": (
                    "We read the operator into a char and compare it with == against literals "
                    "like '+'. Char literals use single quotes, double quotes would make them "
                    "strings and the comparison would fail."
                ),
                "pro_tip": (
                    "Structure the else chain so the last branch handles unexpected input. "
                    "That way bad operators get a friendly message instead of a crash."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    double a, b;\n"
            "    char op;\n"
            "    cout << \"Enter first number: \";\n"
            "    cin >> a;\n"
            "    cout << \"Enter operator (+, -, *, /): \";\n"
            "    cin >> op;\n"
            "    cout << \"Enter second number: \";\n"
            "    cin >> b;\n"
            "    if (op == '+') {\n"
            "        cout << \"Result: \" << (a + b) << endl;\n"
            "    } else if (op == '-') {\n"
            "        cout << \"Result: \" << (a - b) << endl;\n"
            "    } else {\n"
            "        cout << \"Operator not supported yet!\" << endl;\n"
            "    }\n"
            "    return 0;\n"
            "}",
            [
                {"line": 13, "text": "if runs this block when op is a plus sign"},
                {"line": 15, "text": "else if checks the next operator"},
                {"line": 17, "text": "else handles every other operator"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "if (op = '+')",
                "fixed": "if (op == '+')",
                "why": "A single = assigns, it does not compare. The condition would always be truthy.",
            },
            {
                "wrong": "if (op == \"+\")",
                "fixed": "if (op == '+')",
                "why": "A char variable must be compared with a single-quoted character, not a string.",
            },
            {
                "wrong": "int a, b;  // 6 / 7 gives 0",
                "fixed": "double a, b; // 6 / 7 gives 0.857",
                "why": "Integer division truncates the decimal part, silently losing precision.",
            },
        ],
        exercise={
            "description": "Extend the mini calculator with * and / cases so that 6 * 7 prints Result: 42 and 21 / 7 prints Result: 3.",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    double a, b;\n"
                "    char op;\n"
                "    cout << \"Enter first number: \";\n"
                "    cin >> a;\n"
                "    cout << \"Enter operator: \";\n"
                "    cin >> op;\n"
                "    cout << \"Enter second number: \";\n"
                "    cin >> b;\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "Add else if branches for '*' and '/'",
                "Compare with op == '*' and op == '/'",
                "Print the result in the same 'Result: ...' format",
            ],
            "expected_output": (
                "Result: 42\n"
                "Result: 3"
            ),
        },
        quiz={
            "question": "Which operator checks whether two values are equal in C++?",
            "options": ["=", "==", "===", "!="],
            "correct": 1,
            "explanation": "== compares for equality. A single = assigns, and === does not exist in C++.",
        },
        key_takeaways=[
            "if / else if / else chooses one path of execution",
            "== compares values, = assigns them",
            "char literals use single quotes",
            "double avoids integer truncation in division",
        ],
        next_steps="Time for a project! Let us design a rich terminal profile card.",
    ),

    _lesson(
        lesson_id="cpp-l01-09",
        theory=(
            "Time to combine everything into a small project: a rich terminal profile card. It "
            "stores your name, role, and experience in variables, then prints them in a neat, "
            "boxed layout. Simple formatting like a row of = signs turns scattered output into "
            "something that looks professional."
            "\n\n"
            "This is exactly how real terminal tools present data, and the same pattern will show "
            "up again and again in your future projects."
        ),
        analogy=(
            "A profile card is like an ID badge. The badge has a fixed layout, a photo spot, a "
            "name line, and a role line, and the same shell is reused for every employee. Your "
            "program does the same with a few cout statements."
        ),
        sections=[
            {
                "heading": "Designing the card",
                "body": (
                    "First choose what to show: name, role, and experience. Store each in a "
                    "well-named variable, then print them between decorative lines. Keeping data "
                    "in variables makes the card easy to change later."
                ),
                "pro_tip": (
                    "Indent the content lines with two spaces so the card looks balanced "
                    "inside its border."
                ),
            },
            {
                "heading": "Formatting the output",
                "body": (
                    "A border of '=' characters reads as a divider even without special terminal "
                    "features. Every content row mixes text and a variable with its own <<."
                ),
                "pro_tip": (
                    "Keep the border length consistent on both rows, it is the first thing "
                    "the eye checks."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "#include <string>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    string name = \"Priya\";\n"
            "    string role = \"Software Engineer\";\n"
            "    int years = 3;\n"
            "    cout << \"=====================\" << endl;\n"
            "    cout << \"  \" << name << endl;\n"
            "    cout << \"  \" << role << endl;\n"
            "    cout << \"  Experience: \" << years << \" years\" << endl;\n"
            "    cout << \"=====================\" << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 6, "text": "Stores the name in a string variable"},
                {"line": 9, "text": "Prints the top border"},
                {"line": 12, "text": "Mixes text with the int variable years"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "cout << name role;",
                "fixed": "cout << name << \" \" << role << endl;",
                "why": "Each value needs its own <<, and you must add separators yourself.",
            },
            {
                "wrong": "cout << \"=========\" endl;",
                "fixed": "cout << \"=========\" << endl;",
                "why": "endl must also be sent with <<, it cannot follow a string directly.",
            },
            {
                "wrong": "string name = \"Priya\";  // but <string> is not included",
                "fixed": "#include <string>\nstring name = \"Priya\";",
                "why": "Without the <string> header the compiler does not know what string is.",
            },
        ],
        exercise={
            "description": "Upgrade the profile card to ask the user for name, role, and years of experience with cin, then print the same boxed card using their answers.",
            "starter_code": (
                "#include <iostream>\n"
                "#include <string>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    string name, role;\n"
                "    int years;\n"
                "    cout << \"Enter your name: \";\n"
                "    cin >> name;\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "Prompt and read role and years",
                "Print the top border first",
                "Print each field between two spaces",
            ],
            "expected_output": (
                "=====================\n"
                "  Priya\n"
                "  Software Engineer\n"
                "  Experience: 3 years\n"
                "====================="
            ),
        },
        quiz={
            "question": "What is the row of '=====' characters doing in the profile card program?",
            "options": [
                "It is a visual divider made of printed text",
                "It is a comment",
                "It starts a loop",
                "It declares a variable",
            ],
            "correct": 0,
            "explanation": "It is ordinary text printed with cout, used purely as a visual divider.",
        },
        key_takeaways=[
            "Store display data in well-named variables",
            "Boxed formatting improves readability in the terminal",
            "Each value printed needs its own <<",
            "Interactive projects follow prompt-read-print patterns",
        ],
        next_steps="Level 1 complete! Next up, Level 2: variables, types, and the auto keyword.",
    ),

    # =========================================================================
    # LEVEL 2: VARIABLES
    # =========================================================================
    _lesson(
        lesson_id="cpp-l02-01",
        theory=(
            "Every piece of data in C++ has a type, and the primitive types are the language's "
            "basic building blocks. int stores whole numbers, double stores numbers with decimals, "
            "char stores a single character, and bool stores true or false."
            "\n\n"
            "Choosing the right type matters. A double can hold 19.99 while an int would silently "
            "drop the cents. And bool prints as 1 or 0, not the words true or false."
        ),
        analogy=(
            "Types are like containers in a kitchen. int is a measuring cup that only takes whole "
            "spoons, double is a fine scale that measures fractions, char is a tiny spice jar for "
            "one letter, and bool is a simple light switch, on or off. You pick the container "
            "that fits the ingredient."
        ),
        sections=[
            {
                "heading": "The four primitives",
                "body": (
                    "int for whole numbers, double for decimals, char for one character, and bool "
                    "for truth values. Each uses a different amount of memory, and each has its "
                    "own range of values it can represent."
                ),
                "pro_tip": (
                    "Ask yourself what the data really is: whole count, precise measure, single "
                    "letter, or yes/no. The answer tells you the type."
                ),
            },
            {
                "heading": "How values behave",
                "body": (
                    "A char literal uses single quotes: 'A'. A double keeps its decimals: 19.99. "
                    "And bool prints as 1 or 0 because that is how C++ represents truth on the "
                    "screen."
                ),
                "pro_tip": (
                    "If you need to display true/false text, compare the bool in an if and print "
                    "the words yourself."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    int score = 95;\n"
            "    double price = 19.99;\n"
            "    char grade = 'A';\n"
            "    bool passed = true;\n"
            "    cout << score << endl;\n"
            "    cout << price << endl;\n"
            "    cout << grade << endl;\n"
            "    cout << passed << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 5, "text": "int stores a whole number"},
                {"line": 6, "text": "double stores a decimal"},
                {"line": 7, "text": "char stores one character in single quotes"},
                {"line": 8, "text": "bool stores true or false"},
                {"line": 12, "text": "bool prints as 1, not 'true'"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "char grade = \"A\";",
                "fixed": "char grade = 'A';",
                "why": "Double quotes make a string; char needs a single-quoted character.",
            },
            {
                "wrong": "int score = 95.5;",
                "fixed": "double score = 95.5;",
                "why": "int truncates the fractional part, silently storing 95.",
            },
            {
                "wrong": "bool passed = \"true\";",
                "fixed": "bool passed = true;",
                "why": "bool values are the keywords true and false, not quoted strings.",
            },
        ],
        exercise={
            "description": "Declare one variable of each primitive type: a char for your initial, an int for age, a double for height, and a bool for whether you have a passport. Print each one.",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "char initial = 'A'; uses single quotes",
                "double height = 5.6; keeps its decimals",
                "bool hasPassport = true; prints as 1",
            ],
            "expected_output": (
                "Initial: A\n"
                "Age: 25\n"
                "Height: 5.6\n"
                "Passport: 1"
            ),
        },
        quiz={
            "question": "Which of these is a valid char literal in C++?",
            "options": ["\"A\"", "'A'", "A", "`A`"],
            "correct": 1,
            "explanation": "A char literal is a single character inside single quotes, like 'A'.",
        },
        key_takeaways=[
            "int holds whole numbers, double holds decimals",
            "char holds one character in single quotes",
            "bool holds true or false and prints as 1 or 0",
            "Pick the type that matches your data",
        ],
        next_steps="Now let the compiler do the typing work for you with the auto keyword!",
    ),

    _lesson(
        lesson_id="cpp-l02-02",
        theory=(
            "The auto keyword lets the compiler deduce a variable's type for you. Instead of "
            "guessing, you write auto and the compiler figures out the exact type from the "
            "initializer on the right side. This keeps your code short and avoids repeating long "
            "type names."
            "\n\n"
            "auto is not magic and it is not dynamic. The type is fixed at compile time, exactly "
            "as if you had written it by hand, so a value's type never changes while the program "
            "runs."
        ),
        analogy=(
            "auto is like handing your luggage to a porter and saying 'make sure it fits a bag'. "
            "The porter looks at the shape and size and picks the right bag for you. It is not "
            "shape-shifting luggage, the bag is chosen once and stays chosen."
        ),
        sections=[
            {
                "heading": "How auto works",
                "body": (
                    "auto needs an initializer. The compiler examines the expression on the right "
                    "and deduces the type: 42 becomes int, 3.14 becomes double, and true becomes "
                    "bool. The result is exactly like writing the type yourself."
                ),
                "pro_tip": (
                    "Hover over an auto variable in your editor and it will show the deduced "
                    "type, a great way to learn what is really happening."
                ),
            },
            {
                "heading": "What auto is not",
                "body": (
                    "auto does not give you dynamic typing like Python or JavaScript. A variable "
                    "deduced as int stays an int forever. Attempting to store text in it later is "
                    "a compile-time error."
                ),
                "pro_tip": (
                    "auto shines with huge library type names. When you see types with long "
                    "template names, auto keeps your code readable."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    auto number = 42;\n"
            "    auto ratio = 3.14;\n"
            "    auto letter = 'c';\n"
            "    auto flag = true;\n"
            "    cout << number << \" \" << ratio << \" \";\n"
            "    cout << letter << \" \" << flag << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 5, "text": "Deduced as int"},
                {"line": 6, "text": "Deduced as double"},
                {"line": 8, "text": "Deduced as bool"},
                {"line": 10, "text": "All deduced types print normally"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "auto x;",
                "fixed": "auto x = 0;",
                "why": "auto needs an initializer to deduce a type from.",
            },
            {
                "wrong": "auto value = 5;\nvalue = \"hello\";",
                "fixed": "string value = \"hello\";",
                "why": "auto is compile-time, not dynamic. Once int, always int.",
            },
            {
                "wrong": "auto pi = 3.14159; // expecting float",
                "fixed": "auto pi = 3.14159f; // a float literal needs the f suffix",
                "why": "A plain decimal literal is double, so auto deduces double.",
            },
        ],
        exercise={
            "description": "Use auto for a body temperature reading (36.6) and print it with the unit C, like: Temperature: 36.6 C.",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "auto temp = 36.6;",
                "Print with cout << \"Temperature: \" << temp << \" C\" << endl;",
                "auto deduces double here",
            ],
            "expected_output": "Temperature: 36.6 C",
        },
        quiz={
            "question": "After auto number = 42;, what is the type of number?",
            "options": ["string", "double", "int", "bool"],
            "correct": 2,
            "explanation": "The literal 42 is an int, so auto deduces number as an int.",
        },
        key_takeaways=[
            "auto deduces the type from the initializer",
            "auto is fixed at compile time, not dynamic",
            "auto needs an initializer to work",
            "auto keeps code short and readable",
        ],
        next_steps="Text deserves its own type. Let us explore the string type!",
    ),

    _lesson(
        lesson_id="cpp-l02-03",
        theory=(
            "std::string is the modern way to store text in C++. It supports concatenation with "
            "+ , indexing with [] , and a length() method that returns how many characters it "
            "holds. Because string is a class, it manages its own memory."
            "\n\n"
            "When reading whole sentences, cin >> stops at the first space, so only the first "
            "word is captured. getline(cin, line) reads an entire line, spaces and all."
        ),
        analogy=(
            "A string is like a bead necklace. You can add beads to the end with +, pick out the "
            "bead at a position with [], and count the beads with length(). The necklace grows "
            "and shrinks by itself, no string and needle required."
        ),
        sections=[
            {
                "heading": "Building and inspecting strings",
                "body": (
                    "Concatenation joins strings: first + \" \" + last gives a full name. "
                    "full[0] grabs the character at index 0, and full.length() reports how many "
                    "characters the string holds."
                ),
                "pro_tip": (
                    "Indexing starts at 0, so full[0] is the first character and "
                    "full[full.length() - 1] is the last one."
                ),
            },
            {
                "heading": "Reading whole lines",
                "body": (
                    "cin >> stops at the first space, which is useless for full names or "
                    "sentences. getline(cin, text) reads everything until the Enter key, spaces "
                    "included."
                ),
                "pro_tip": (
                    "Do not mix cin >> and getline in the same program carelessly. After cin >>, "
                    "a leftover newline can make getline return an empty line. Clear the input "
                    "with cin.ignore() when needed."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "#include <string>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    string first = \"Ada\";\n"
            "    string last = \"Lovelace\";\n"
            "    string full = first + \" \" + last;\n"
            "    cout << full << endl;\n"
            "    cout << \"Length: \" << full.length() << endl;\n"
            "    cout << full[0] << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 8, "text": "+ concatenates strings with a space between"},
                {"line": 10, "text": "length() returns the number of characters"},
                {"line": 11, "text": "Indexing starts at 0"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "string line;\ncin >> line; // user types New York",
                "fixed": "string line;\ngetline(cin, line); // reads the whole line",
                "why": "cin >> stops at whitespace, so only 'New' would be stored.",
            },
            {
                "wrong": "cout << full.length << endl;",
                "fixed": "cout << full.length() << endl;",
                "why": "length is a function, so it must be called with parentheses.",
            },
            {
                "wrong": "full[0] = \"A\";",
                "fixed": "full[0] = 'A';",
                "why": "Indexing yields a char, so it must be assigned a single-quoted character.",
            },
        ],
        exercise={
            "description": "Concatenate a city and country with a comma and space, print them, then print the length of the result.",
            "starter_code": (
                "#include <iostream>\n"
                "#include <string>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    string city = \"Mumbai\";\n"
                "    string country = \"India\";\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "Build location = city + \", \" + country;",
                "Print the location with a label",
                "Print location.length() for the character count",
            ],
            "expected_output": (
                "Location: Mumbai, India\n"
                "Length: 13"
            ),
        },
        quiz={
            "question": "What does \"Mumbai\".length() return?",
            "options": ["5", "6", "7", "8"],
            "correct": 1,
            "explanation": "Mumbai has 6 letters, so length() returns 6.",
        },
        key_takeaways=[
            "string stores text and manages its own memory",
            "+ concatenates strings, [] indexes characters",
            "length() returns the character count",
            "getline reads whole lines, cin >> stops at spaces",
        ],
        next_steps="Values that must never change need constants. Let us learn const and constexpr!",
    ),

    _lesson(
        lesson_id="cpp-l02-04",
        theory=(
            "Constants lock a value so it cannot be changed after creation. const creates a "
            "constant that is fixed at runtime, while constexpr demands the value be computable "
            "at compile time. Compilers love constexpr because it lets them optimize aggressively."
            "\n\n"
            "Naming convention: constants are usually written in ALL_CAPS with underscores. "
            "Trying to modify a const is a compile-time error, which is exactly what we want, it "
            "protects your logic from accidental changes."
        ),
        analogy=(
            "A constant is like a value stamped on a metal plate. The law of gravity, the number "
            "of days in a week, and the speed limit are fixed facts. constexpr is like a fact "
            "carved in stone before you even start driving, while const is a rule taped to your "
            "dashboard that the car enforces."
        ),
        sections=[
            {
                "heading": "const: the runtime constant",
                "body": (
                    "const double PI = 3.14159; creates a value that cannot be reassigned. The "
                    "compiler checks every assignment and refuses any attempt to modify it, "
                    "catching bugs before your program ever runs."
                ),
                "pro_tip": (
                    "Mark any variable you never intend to change as const. It documents your "
                    "intent and lets the compiler catch accidental writes."
                ),
            },
            {
                "heading": "constexpr: the compile-time constant",
                "body": (
                    "constexpr int DAYS = 7; must be computable at compile time, so the compiler "
                    "bakes the value directly into your program. This is ideal for things like "
                    "array sizes and mathematical constants."
                ),
                "pro_tip": (
                    "A constexpr value cannot depend on user input, that would only be known at "
                    "runtime. Use const for values that are fixed after the program starts."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    const double PI = 3.14159;\n"
            "    constexpr int DAYS = 7;\n"
            "    double radius = 5.0;\n"
            "    cout << \"Circumference: \" << 2 * PI * radius << endl;\n"
            "    cout << \"Days: \" << DAYS << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 5, "text": "const fixes PI for the whole program"},
                {"line": 6, "text": "constexpr is known at compile time"},
                {"line": 8, "text": "PI and radius are multiplied together"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "const int MAX = 10;\nMAX = 20;",
                "fixed": "int maxVal = 10;\nmaxVal = 20;",
                "why": "You cannot reassign a const variable; the compiler rejects it.",
            },
            {
                "wrong": "const double PI; // no initializer",
                "fixed": "const double PI = 3.14159;",
                "why": "A const must be initialized at declaration because it can never be set later.",
            },
            {
                "wrong": "const int LIMIT = input; // user input at runtime",
                "fixed": "const int LIMIT = input; // valid as const, not as constexpr",
                "why": "Input is only known at runtime, so it can be const but never constexpr.",
            },
        ],
        exercise={
            "description": "Compute the area of a circle. Ask the user for the radius, use the given const PI, and print the area using the formula PI * radius * radius.",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    const double PI = 3.14159;\n"
                "    double radius;\n"
                "    cout << \"Enter radius: \";\n"
                "    cin >> radius;\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "Area equals PI * radius * radius",
                "Wrap the calculation in parentheses before printing",
                "For radius 5, the area is about 78.54",
            ],
            "expected_output": "Area: 78.5397",
        },
        quiz={
            "question": "What happens if you try to reassign a const variable?",
            "options": [
                "It silently changes value",
                "The compiler reports an error",
                "The program crashes at runtime",
                "The program prints a warning",
            ],
            "correct": 1,
            "explanation": "Modifying a const is a compile-time error, which protects your data.",
        },
        key_takeaways=[
            "const creates a value that cannot be changed",
            "constexpr demands a compile-time constant",
            "Constants are written in ALL_CAPS by convention",
            "Constants catch accidental modifications at compile time",
        ],
        next_steps="Now let us see how C++ infers types and how numbers convert between them.",
    ),

    _lesson(
        lesson_id="cpp-l02-05",
        theory=(
            "Type inference is C++'s ability to figure out types for you, powered by auto. It "
            "becomes essential with complex library types whose names are huge, and it guarantees "
            "the variable matches the expression's true type, avoiding mismatches."
            "\n\n"
            "But inference never changes how operators behave. Dividing two ints still gives "
            "integer division: 7 / 3 is 2, not 2.33. You must convert at least one operand to "
            "double if you want a fractional result."
        ),
        analogy=(
            "Type inference is like a warehouse worker reading the label on a box and grabbing "
            "the right shelf automatically. The worker does not change what is inside the box, "
            "they just place it where it fits. If two boxes need to merge, the contents still "
            "behave exactly as they always did."
        ),
        sections=[
            {
                "heading": "Conversions happen silently",
                "body": (
                    "Assigning an int to a double converts it automatically: int a = 7; double b "
                    "= a; makes b equal 7.0. This widening conversion loses nothing. The reverse, "
                    "double to int, truncates and loses data."
                ),
                "pro_tip": (
                    "Prefer converting to the more precise type. Going from double to int drops "
                    "the decimals, so never rely on the compiler to 'round' for you."
                ),
            },
            {
                "heading": "Integer division is the trap",
                "body": (
                    "auto third = a / 3; with int a gives an int result, so 7 / 3 is 2. To get "
                    "2.333, at least one operand must be double: a / 3.0 or double(a) / 3."
                ),
                "pro_tip": (
                    "Writing 3.0 instead of 3 is a tiny change that completely changes the "
                    "result. Spotting this is a classic interview debugging question."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    int a = 7;\n"
            "    double b = a;\n"
            "    auto half = b / 2;\n"
            "    auto third = a / 3;\n"
            "    cout << b << endl;\n"
            "    cout << half << endl;\n"
            "    cout << third << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 6, "text": "int converts to double automatically"},
                {"line": 7, "text": "double divided by int gives a double"},
                {"line": 8, "text": "int divided by int stays int: 7 / 3 is 2"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "int a = 7;\ndouble half = a / 2;",
                "fixed": "double half = a / 2.0;",
                "why": "a / 2 is integer division (3). One operand must be double for 3.5.",
            },
            {
                "wrong": "auto third = a / 3; // expecting 2.333",
                "fixed": "auto third = a / 3.0; // 2.333",
                "why": "auto infers int from an int/int expression, so decimals are lost.",
            },
            {
                "wrong": "double d = 9.7;\nint n = d; // expecting rounding to 10",
                "fixed": "int n = (int)(d + 0.5); // round first, then convert",
                "why": "double to int truncates toward zero, so 9.7 becomes 9.",
            },
        ],
        exercise={
            "description": "100 rupees are shared equally among 8 students. Print how much each student pays, with the cents preserved.",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    int total = 100;\n"
                "    int students = 8;\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "Divide total by students as doubles to keep the cents",
                "total / students gives 12, total / double(students) gives 12.5",
                "Print with a label like 'Each student pays:'",
            ],
            "expected_output": "Each student pays: 12.5",
        },
        quiz={
            "question": "int a = 7; int b = 2; What does cout << a / b print?",
            "options": ["3.5", "3", "2", "4"],
            "correct": 1,
            "explanation": "Both operands are int, so integer division applies: 7 / 2 is 3.",
        },
        key_takeaways=[
            "auto infers types from expressions",
            "int to double widens safely, double to int truncates",
            "int / int is integer division",
            "Use a double operand to get a fractional result",
        ],
        next_steps="Now for something truly C++-ish: references, your first real pointer-adjacent tool!",
    ),

    _lesson(
        lesson_id="cpp-l02-06",
        theory=(
            "A reference is an alias, a second name for an existing variable. When you write "
            "int& ref = power;, ref and power are two names for the same memory. Changing one "
            "changes the other, and no copy is made."
            "\n\n"
            "References must be initialized when declared, and they cannot be rebound to a "
            "different variable later. They are the foundation of efficient code, since you can "
            "pass data around without copying it."
        ),
        analogy=(
            "A reference is like two doors leading into the same room. Whether you enter through "
            "the front door (power) or the garden door (ref), you end up in the exact same room, "
            "and any furniture you move is visible from both. You cannot re-point the garden door "
            "at a different house later."
        ),
        sections=[
            {
                "heading": "Declaring a reference",
                "body": (
                    "The & symbol in int& ref = power; means 'a reference to'. It is declared "
                    "once and glued to power forever. Assigning ref = 150 writes 150 straight "
                    "into power's memory."
                ),
                "pro_tip": (
                    "Do not confuse the reference & in a declaration with the address-of & in "
                    "expressions. Same symbol, two completely different meanings."
                ),
            },
            {
                "heading": "Assignment copies, not rebinds",
                "body": (
                    "After ref = health;, people often expect ref to now point at health. It does "
                    "not. The value of health is copied into power. References cannot be moved "
                    "onto another variable."
                ),
                "pro_tip": (
                    "If you need to point at different variables over time, you need a pointer, "
                    "not a reference. References are for permanent aliases."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    int power = 100;\n"
            "    int& ref = power;\n"
            "    ref = 150;\n"
            "    cout << power << endl;\n"
            "    int health = 50;\n"
            "    ref = health;\n"
            "    cout << power << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 6, "text": "ref is an alias for power"},
                {"line": 7, "text": "Writing through ref changes power"},
                {"line": 10, "text": "Copies health's value into power, ref still aliases power"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "int& ref; // no initializer",
                "fixed": "int value = 0;\nint& ref = value;",
                "why": "References must be bound to a variable at declaration, they cannot exist alone.",
            },
            {
                "wrong": "int& ref = power;\nref = health; // hoping ref points at health now",
                "fixed": "ref = health; // ref still aliases power, only the value is copied",
                "why": "References never rebind. Assignment through a reference writes to its original target.",
            },
            {
                "wrong": "int& ref = &power;",
                "fixed": "int& ref = power;",
                "why": "&power is an address (a pointer), but a reference binds to the variable itself.",
            },
        ],
        exercise={
            "description": "Create a reference to the fuel variable, double the fuel through the reference, and print the doubled amount.",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    int fuel = 40;\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "Declare with int& ref = fuel;",
                "Multiply through the reference: ref = ref * 2;",
                "Print fuel, it reflects the change",
            ],
            "expected_output": "Fuel doubled: 80",
        },
        quiz={
            "question": "A reference in C++ is best described as...",
            "options": [
                "A copy of a value",
                "A pointer that must be dereferenced",
                "An alias to an existing variable",
                "A constant value",
            ],
            "correct": 2,
            "explanation": "A reference is an alias; two names for the same memory with no copy made.",
        },
        key_takeaways=[
            "A reference is an alias for an existing variable",
            "References must be initialized and never rebind",
            "Writing through a reference changes the original",
            "References enable passing data without copying",
        ],
        next_steps="Let us put types, auto, and references together in a Type Explorer practice!",
    ),

    _lesson(
        lesson_id="cpp-l02-07",
        theory=(
            "This practice lesson puts the primitive types, auto, strings, and sizeof together. "
            "sizeof tells you how many bytes a type occupies, which is the first thing to "
            "understand when you worry about memory or portability."
            "\n\n"
            "The exact sizes of int and long depend on the platform, but char is always exactly "
            "1 byte by the C++ standard."
        ),
        analogy=(
            "sizeof is like checking the size label on a suitcase. Different suitcases (types) "
            "hold different amounts of luggage (bytes). Knowing the size limits helps you choose "
            "which suitcase to pack, and explains why some suitcases go missing when you try to "
            "stuff too much in."
        ),
        sections=[
            {
                "heading": "Exploring your variables",
                "body": (
                    "Declare one variable of each primitive type, then print them. Watch how a "
                    "bool prints as 1 and a double keeps its decimals. Every type behaves a "
                    "little differently on screen."
                ),
                "pro_tip": (
                    "Print each value on its own labeled line. Labels turn raw output into a "
                    "readable table."
                ),
            },
            {
                "heading": "Measuring with sizeof",
                "body": (
                    "sizeof(int) returns the number of bytes an int occupies, and it is evaluated "
                    "at compile time. It accepts either a type name like sizeof(double) or a "
                    "variable like sizeof(age)."
                ),
                "pro_tip": (
                    "sizeof is not a function, it is an operator. The parentheses are optional "
                    "but conventional, and you will almost always see them."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    int age = 25;\n"
            "    double gpa = 8.7;\n"
            "    char section = 'B';\n"
            "    bool isStudent = true;\n"
            "    cout << \"Age: \" << age << endl;\n"
            "    cout << \"GPA: \" << gpa << endl;\n"
            "    cout << \"Section: \" << section << endl;\n"
            "    cout << \"Student: \" << isStudent << endl;\n"
            "    cout << \"int size: \" << sizeof(int) << \" bytes\" << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 5, "text": "One variable of each primitive type"},
                {"line": 12, "text": "bool prints as 1, not 'true'"},
                {"line": 13, "text": "sizeof(int) reports bytes at compile time"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "bool isStudent = true;\ncout << isStudent; // expecting 'true'",
                "fixed": "cout << (isStudent ? \"true\" : \"false\");",
                "why": "cout prints bool as 1 or 0. Print text yourself if you need words.",
            },
            {
                "wrong": "cout << sizeof int << endl;",
                "fixed": "cout << sizeof(int) << endl;",
                "why": "sizeof is an operator, but for a type name the parentheses are required.",
            },
            {
                "wrong": "float gpa = 8.7; // unnecessary precision loss",
                "fixed": "double gpa = 8.7;",
                "why": "double is the default and more precise floating-point type in C++.",
            },
        ],
        exercise={
            "description": "Print the sizes of char, int, double, and bool using sizeof, each labeled on its own line.",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "Use sizeof(char), sizeof(int), and so on",
                "Print with a label like \"char: \" before each size",
                "Append \" bytes\" after each size",
            ],
            "expected_output": (
                "char: 1 bytes\n"
                "int: 4 bytes\n"
                "double: 8 bytes\n"
                "bool: 1 bytes"
            ),
        },
        quiz={
            "question": "What does cout print for a bool variable set to true?",
            "options": ["true", "1", "True", "0"],
            "correct": 1,
            "explanation": "C++ streams print bools as 1 for true and 0 for false.",
        },
        key_takeaways=[
            "Each primitive type has its own size in bytes",
            "bool prints as 1 or 0 on screen",
            "sizeof is a compile-time operator",
            "char is always exactly 1 byte",
        ],
        next_steps="Now the size puzzle challenge: let us measure every type and watch an overflow!",
    ),

    _lesson(
        lesson_id="cpp-l02-08",
        theory=(
            "Here is your challenge: explore how types really behave. Print the sizes of every "
            "primitive type and watch an integer overflow happen live when a huge int is doubled "
            "past its maximum. The wrap-around that results is why choosing the right type is not "
            "just academic."
            "\n\n"
            "sizeof is a compile-time operator: the answer is baked into your program before it "
            "even runs."
        ),
        analogy=(
            "An integer overflow is like an odometer rolling over. A car that has driven "
            "999,999 km rolls back to 000,000 on the next kilometer. A 32-bit int behaves the "
            "same way when you push it past 2,147,483,647, it wraps around into negative "
            "territory."
        ),
        sections=[
            {
                "heading": "Measuring every primitive",
                "body": (
                    "Run the program on your own machine and note each size. Sizes can vary "
                    "between platforms, so measuring instead of memorizing is the professional "
                    "approach."
                ),
                "pro_tip": (
                    "sizeof(long) is 4 bytes on Windows and 8 on many Linux systems. "
                    "Code that assumes a fixed size breaks when it moves."
                ),
            },
            {
                "heading": "The overflow trap",
                "body": (
                    "2000000000 * 2 exceeds the 32-bit int limit. C++ does not stop and report "
                    "an error, it wraps around to a negative number. This silent wrap-around has "
                    "caused real-world disasters like the Ariane 5 rocket failure."
                ),
                "pro_tip": (
                    "When a calculation can grow large, think about the type before you code. "
                    "A long long can hold far bigger values than an int."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    cout << \"char: \" << sizeof(char) << endl;\n"
            "    cout << \"short: \" << sizeof(short) << endl;\n"
            "    cout << \"int: \" << sizeof(int) << endl;\n"
            "    cout << \"long: \" << sizeof(long) << endl;\n"
            "    cout << \"long long: \" << sizeof(long long) << endl;\n"
            "    cout << \"float: \" << sizeof(float) << endl;\n"
            "    cout << \"double: \" << sizeof(double) << endl;\n"
            "    cout << \"bool: \" << sizeof(bool) << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 5, "text": "sizeof(char) is always 1"},
                {"line": 7, "text": "sizeof(int) is usually 4"},
                {"line": 8, "text": "long varies between platforms"},
                {"line": 11, "text": "double is usually 8 bytes"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "cout << \"int is always 4 bytes\";",
                "fixed": "cout << sizeof(int); // measure it yourself",
                "why": "Sizes are platform-dependent. char is the only guaranteed size in the standard.",
            },
            {
                "wrong": "int b = 2000000000 * 2; // expecting 4000000000",
                "fixed": "long long b = 2000000000LL * 2; // 4000000000",
                "why": "The result exceeds the int range and silently wraps around.",
            },
            {
                "wrong": "sizeof(char) // assuming 4",
                "fixed": "sizeof(char) // guaranteed 1 byte",
                "why": "char is defined to be exactly 1 byte, unlike every other primitive.",
            },
        ],
        exercise={
            "description": "Declare int a = 2000000000. Print a * 2 and observe the overflow wrap-around, then print the size of an int alongside it.",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    int a = 2000000000;\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "Multiply: int b = a * 2;",
                "Print b to see the negative wrap-around",
                "Also print sizeof(int) to show the 4-byte limit",
            ],
            "expected_output": (
                "a * 2 overflowed to -294967296\n"
                "int is 4 bytes"
            ),
        },
        quiz={
            "question": "Which type is guaranteed to be exactly 1 byte by the C++ standard?",
            "options": ["int", "bool", "char", "short"],
            "correct": 2,
            "explanation": "Only char has a guaranteed size of 1 byte; all other types are platform-dependent.",
        },
        key_takeaways=[
            "Type sizes vary across platforms",
            "char is always exactly 1 byte",
            "sizeof is computed at compile time",
            "Overflow wraps around silently, so choose types carefully",
        ],
        next_steps="Now the Level 2 project: a shopping cart with a discount engine!",
    ),

    _lesson(
        lesson_id="cpp-l02-09",
        theory=(
            "This project builds a shopping cart with a discount engine. You multiply a constant "
            "price by a quantity to get the subtotal, apply a percentage discount, and produce "
            "the final total. It is the same pipeline every e-commerce checkout follows."
            "\n\n"
            "Money is stored as double here, but real payment systems use integer cents to avoid "
            "floating-point rounding surprises. Notice how constants protect the price and "
            "discount from accidental changes."
        ),
        analogy=(
            "A checkout flow is like a cashier's receipt. First the line items are added up "
            "(subtotal), then the coupon is applied (discount), then the final amount is shown. "
            "You would not apply the coupon to a single item, it applies to the subtotal of "
            "everything."
        ),
        sections=[
            {
                "heading": "Subtotal, discount, total",
                "body": (
                    "The subtotal is price times quantity: PRICE * quantity. The discount is a "
                    "fraction of the subtotal, subtotal * DISCOUNT. Finally the total subtracts "
                    "the discount from the subtotal. Three steps, three well-named variables."
                ),
                "pro_tip": (
                    "A 15% discount is stored as 0.15, not 15. Percentages always become their "
                    "decimal fraction before you multiply."
                ),
            },
            {
                "heading": "Protecting the business rules",
                "body": (
                    "PRICE and DISCOUNT are const because a checkout must never mutate its own "
                    "pricing. Making them constants means the compiler enforces that rule for "
                    "you, and any accidental write becomes an error."
                ),
                "pro_tip": (
                    "Label the output lines with dollar signs and clear names so the report "
                    "reads like a real receipt."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    const double PRICE = 199.0;\n"
            "    const double DISCOUNT = 0.15;\n"
            "    int quantity = 3;\n"
            "    double subtotal = PRICE * quantity;\n"
            "    double discountAmount = subtotal * DISCOUNT;\n"
            "    double total = subtotal - discountAmount;\n"
            "    cout << \"Subtotal: $\" << subtotal << endl;\n"
            "    cout << \"Discount: $\" << discountAmount << endl;\n"
            "    cout << \"Total: $\" << total << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 5, "text": "Price is locked with const"},
                {"line": 8, "text": "Subtotal = price x quantity"},
                {"line": 9, "text": "Discount applies to the subtotal"},
                {"line": 10, "text": "Total subtracts the discount"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "double total = PRICE * quantity - DISCOUNT;",
                "fixed": "double subtotal = PRICE * quantity;\ndouble total = subtotal - subtotal * DISCOUNT;",
                "why": "Subtracting 0.15 from 597 is not a 15% discount. The discount must be a fraction of the subtotal.",
            },
            {
                "wrong": "const double DISCOUNT = 15; // then multiply",
                "fixed": "const double DISCOUNT = 0.15;",
                "why": "15% is 0.15 in decimal form. Using 15 would multiply by 1500%.",
            },
            {
                "wrong": "int subtotal = PRICE * quantity;",
                "fixed": "double subtotal = PRICE * quantity;",
                "why": "Money needs decimals, so an int would truncate the cents.",
            },
        ],
        exercise={
            "description": "Extend the checkout to also charge 5% tax on the discounted total, and print a final line with the tax applied.",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    const double PRICE = 199.0;\n"
                "    const double DISCOUNT = 0.15;\n"
                "    int quantity = 3;\n"
                "    double subtotal = PRICE * quantity;\n"
                "    double discountAmount = subtotal * DISCOUNT;\n"
                "    double total = subtotal - discountAmount;\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "Declare const double TAX = 0.05;",
                "Tax applies to the discounted total, not the subtotal",
                "Final total = total + total * TAX, around 532.82",
            ],
            "expected_output": "Final total with tax: $532.82",
        },
        quiz={
            "question": "With PRICE = 199.0, quantity = 3, and DISCOUNT = 0.15, what is the discounted total?",
            "options": ["$507.45", "$597.00", "$89.55", "$506.85"],
            "correct": 0,
            "explanation": "Subtotal is 597, discount is 89.55, so total is 597 - 89.55 = 507.45.",
        },
        key_takeaways=[
            "Compute subtotal, then discount, then total in order",
            "Percentages are stored as decimal fractions",
            "Use double for money to keep the cents",
            "const protects prices and business rules",
        ],
        next_steps="Level 2 complete! Next up, Level 3: operators, conditions, and expressions.",
    ),

    # =========================================================================
    # LEVEL 3: OPERATORS
    # =========================================================================
    _lesson(
        lesson_id="cpp-l03-01",
        theory=(
            "Arithmetic operators do the math: +, -, *, /, and %. Division of two integers "
            "always truncates, so 17 / 5 is 3, and % gives you the remainder, so 17 % 5 is 2. "
            "Assignment operators like += apply the operation and store the result back in one "
            "step."
            "\n\n"
            "The remainder operator only works on integer types. Watch out for a += 3 versus "
            "a =+ 3, they are completely different: one adds, the other assigns a positive "
            "number."
        ),
        analogy=(
            "Think of % as sharing cookies. If you have 17 cookies and 5 friends, each friend "
            "gets 3 whole cookies (the quotient) and 2 cookies are left over (the remainder). "
            "The modulus operator % reports those 2 leftovers."
        ),
        sections=[
            {
                "heading": "The five operators",
                "body": (
                    "+, -, *, and / are straightforward, but / deserves care with integers. "
                    "The % operator is unique: it only accepts integers and answers the question "
                    "'what is left over after division?'."
                ),
                "pro_tip": (
                    "x % 2 is 0 when x is even and 1 when x is odd. "
                    "This one-liner is a favorite interview trick."
                ),
            },
            {
                "heading": "Compound assignment",
                "body": (
                    "a += 3; is short for a = a + 3;. The compound operators +=, -=, *=, /=, "
                    "and %= read the variable, apply the operation, and write back, all in one "
                    "statement."
                ),
                "pro_tip": (
                    "The order is critical: a += 3 adds, but a =+ 3 just assigns positive 3. "
                    "Those two lines look alike and behave completely differently."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    int a = 17;\n"
            "    int b = 5;\n"
            "    cout << a << \" + \" << b << \" = \" << (a + b) << endl;\n"
            "    cout << a << \" / \" << b << \" = \" << (a / b) << endl;\n"
            "    cout << a << \" % \" << b << \" = \" << (a % b) << endl;\n"
            "    a += 3;\n"
            "    cout << \"After a += 3, a = \" << a << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 7, "text": "+ adds the two integers"},
                {"line": 8, "text": "/ of two ints truncates: 17 / 5 is 3"},
                {"line": 9, "text": "% reports the remainder: 17 % 5 is 2"},
                {"line": 10, "text": "a += 3 adds 3 and stores it back"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "double r = 17 % 5.0;",
                "fixed": "int r = 17 % 5;",
                "why": "The remainder operator % only works with integer types.",
            },
            {
                "wrong": "a =+ 3; // thinking it adds 3",
                "fixed": "a += 3;",
                "why": "a =+ 3 means 'assign positive 3'. The += operator must come together.",
            },
            {
                "wrong": "int result = 7 / 2; // expecting 3.5",
                "fixed": "double result = 7.0 / 2;",
                "why": "int / int is integer division, which truncates to 3.",
            },
        ],
        exercise={
            "description": "Given a = 13, b = 8, c = 4, print their sum, the average as a double, and whether c is even (use c % 2).",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    int a = 13, b = 8, c = 4;\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "Sum is (a + b + c)",
                "Average needs a double operand: (a + b + c) / 3.0",
                "Even check: (c % 2 == 0)",
            ],
            "expected_output": (
                "Sum: 25\n"
                "Average: 8.33333\n"
                "c is even: 1"
            ),
        },
        quiz={
            "question": "What is 17 % 5?",
            "options": ["3", "2", "5", "4"],
            "correct": 1,
            "explanation": "17 divided by 5 gives 3 with a remainder of 2, and % returns the 2.",
        },
        key_takeaways=[
            "+ - * / % are the arithmetic operators",
            "int / int truncates the quotient",
            "% returns the remainder and needs integers",
            "+=, -=, *= modify a variable in place",
        ],
        next_steps="Now let us compare values with relational operators and make decisions!",
    ),

    _lesson(
        lesson_id="cpp-l03-02",
        theory=(
            "Comparison operators inspect two values and produce a bool: == equal, != not equal, "
            "< less than, > greater than, <= and >= their inclusive twins. They are how programs "
            "make decisions like 'is the score above passing?'."
            "\n\n"
            "Remember that == compares while = assigns, and that comparisons of doubles can be "
            "tricky due to tiny rounding errors, so use a small tolerance instead of exact "
            "equality."
        ),
        analogy=(
            "Comparison operators are like a referee at a sports match. The referee compares "
            "scores and answers yes/no questions: is the score equal, is it greater, did the "
            "team pass the qualifying line? Each answer is a simple true or false."
        ),
        sections=[
            {
                "heading": "The six comparisons",
                "body": (
                    "Each operator returns a bool: true when the relation holds, false otherwise. "
                    "The inclusive variants <= and >= accept equality, while < and > strictly "
                    "exclude it."
                ),
                "pro_tip": (
                    "Store a comparison in a bool to give it a name: bool passed = score >= "
                    "passing;. Named booleans make code read like English."
                ),
            },
            {
                "heading": "Comparing doubles carefully",
                "body": (
                    "Floating-point math produces tiny rounding errors, so 0.1 + 0.2 may not "
                    "equal 0.3 exactly. Instead of x == y for doubles, check that the difference "
                    "is tiny: abs(x - y) < 0.0001."
                ),
                "pro_tip": (
                    "Exact == on doubles is a famous bug source. When in doubt, compare within a "
                    "small tolerance."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    int score = 85;\n"
            "    int passing = 40;\n"
            "    cout << (score == passing) << endl;\n"
            "    cout << (score > passing) << endl;\n"
            "    cout << (score <= 100) << endl;\n"
            "    cout << (score != 85) << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 7, "text": "== compares: 85 equals 40? false"},
                {"line": 8, "text": "> checks if score is above passing"},
                {"line": 9, "text": "<= includes equality with 100"},
                {"line": 10, "text": "!= is true when values differ"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "if (score = 100)",
                "fixed": "if (score == 100)",
                "why": "A single = assigns 100 to score; the condition is always truthy.",
            },
            {
                "wrong": "cout << score == 85;",
                "fixed": "cout << (score == 85);",
                "why": "Without parentheses, << has higher precedence and the comparison is misparsed.",
            },
            {
                "wrong": "double x = 0.1 + 0.2;\nif (x == 0.3)",
                "fixed": "if (x - 0.3 < 0.0001 && 0.3 - x < 0.0001)",
                "why": "Floating-point rounding can make x differ slightly from 0.3.",
            },
        ],
        exercise={
            "description": "A player scored 92 out of a possible 100. Print whether this is a new high score (score > highScore), whether it equals the high score, and whether it is below 100.",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    int score = 92;\n"
                "    int highScore = 100;\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "New high score: score > highScore",
                "Equal: score == highScore",
                "Below 100: score < 100",
            ],
            "expected_output": (
                "New high score: 0\n"
                "Equal to high score: 0\n"
                "Below 100: 1"
            ),
        },
        quiz={
            "question": "If score is 85, what does (score == 85) evaluate to?",
            "options": ["85", "true", "0", "false"],
            "correct": 1,
            "explanation": "A comparison always produces a bool, and 85 equals 85, so it is true.",
        },
        key_takeaways=[
            "== != < > <= >= all return a bool",
            "== compares, = assigns",
            "Wrap comparisons in parentheses when printing",
            "Avoid exact == on doubles; use a tolerance",
        ],
        next_steps="Now let us combine comparisons into real logic with &&, ||, and !",
    ),

    _lesson(
        lesson_id="cpp-l03-03",
        theory=(
            "Logical operators combine true/false values: && means AND, || means OR, and ! flips "
            "a value. They are the glue that turns simple comparisons into real decisions like "
            "'adult AND has a ticket'."
            "\n\n"
            "They short-circuit: && stops as soon as one side is false, and || stops as soon as "
            "one side is true. This can even prevent errors by skipping risky work on the right "
            "side."
        ),
        analogy=(
            "Logical operators are like a bouncer checking two conditions. && means 'both must "
            "hold': the guest must be 18 or older AND show an ID. || means 'at least one must "
            "hold': VIP access OR a paid ticket both let you in. ! is a 'not' stamp that flips "
            "the answer."
        ),
        sections=[
            {
                "heading": "AND, OR, NOT",
                "body": (
                    "a && b is true only when both a and b are true. a || b is true when at least "
                    "one is true. !a flips true to false and false to true. Combine them with "
                    "parentheses to build precise rules."
                ),
                "pro_tip": (
                    "Speak your condition out loud: 'can enter is age >= 18 AND has ID'. The "
                    "sentence maps directly onto the code."
                ),
            },
            {
                "heading": "Short-circuit behavior",
                "body": (
                    "In a && b, if a is false, b is never evaluated because the result cannot "
                    "change. In a || b, if a is true, b is skipped. This is useful and fast, and "
                    "it also means the right side may never run."
                ),
                "pro_tip": (
                    "Use short-circuiting to guard risky operations: if (ptr && ptr->size > 0) "
                    "safely checks ptr before touching it."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    int age = 22;\n"
            "    bool hasID = true;\n"
            "    bool canEnter = (age >= 18) && hasID;\n"
            "    bool isSenior = age >= 60;\n"
            "    bool isMinor = !(age >= 18);\n"
            "    cout << \"Can enter: \" << canEnter << endl;\n"
            "    cout << \"Is senior: \" << isSenior << endl;\n"
            "    cout << \"Is minor: \" << isMinor << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 7, "text": "&& requires both conditions to be true"},
                {"line": 8, "text": "A single comparison is still a bool"},
                {"line": 9, "text": "! flips the result of a comparison"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "if (age >= 18 & hasID)",
                "fixed": "if (age >= 18 && hasID)",
                "why": "& is the bitwise AND operator. Logical AND uses &&.",
            },
            {
                "wrong": "if (!age >= 18)",
                "fixed": "if (!(age >= 18))",
                "why": "! binds tighter than >=, so !age is evaluated first. Wrap the comparison.",
            },
            {
                "wrong": "if (age < 10 || age > 18) // want the middle range",
                "fixed": "if (age >= 10 && age <= 18)",
                "why": "A range needs && to include both bounds; || would select the outside.",
            },
        ],
        exercise={
            "description": "A theme park admits people who are 18 or older OR have a ticket. Also print whether someone aged 15 with a ticket needs a parent (under 18 AND has a ticket).",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    int age = 15;\n"
                "    bool hasTicket = true;\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "Admitted = (age >= 18) || hasTicket",
                "Needs parent = (age < 18) && hasTicket",
                "Print each as a labeled bool",
            ],
            "expected_output": (
                "Admitted: 1\n"
                "Needs parent: 1"
            ),
        },
        quiz={
            "question": "What does true && false evaluate to?",
            "options": ["true", "false", "1", "Compile error"],
            "correct": 1,
            "explanation": "&& requires both sides true, so true && false is false.",
        },
        key_takeaways=[
            "&& is AND, || is OR, ! is NOT",
            "&& and || short-circuit their right side",
            "Wrap comparisons in parentheses",
            "Read the rule aloud to translate it into operators",
        ],
        next_steps="Now let us go below the surface and manipulate individual bits!",
    ),

    _lesson(
        lesson_id="cpp-l03-04",
        theory=(
            "Bitwise operators work on the individual binary bits of an integer. & AND, | OR, ^ "
            "XOR, ~ NOT, << shift left, and >> shift right. Left-shifting by n multiplies by "
            "2^n, and right-shifting divides, which makes them blazing fast for flags and "
            "low-level math."
            "\n\n"
            "Never confuse & with &&. One is bit-level arithmetic, the other is logical logic, "
            "and mixing them is a classic bug."
        ),
        analogy=(
            "Think of bits as switches on a control panel. & keeps a switch on only if BOTH "
            "panels have it on, | turns it on if EITHER panel has it, ^ flips it if exactly one "
            "is on, and << shifts every switch one position left, doubling each value it "
            "represents."
        ),
        sections=[
            {
                "heading": "The bitwise family",
                "body": (
                    "With a = 6 (binary 110) and b = 3 (binary 011): a & b is 010 (2), a | b is "
                    "111 (7), and a ^ b is 101 (5). Shifting: 6 << 1 doubles to 12, and 6 >> 1 "
                    "halves to 3."
                ),
                "pro_tip": (
                    "A left shift by 1 is the fastest way to double an integer, and >> 1 to "
                    "halve it. Bit twiddling is used in graphics, compression, and games."
                ),
            },
            {
                "heading": "Precedence is your enemy",
                "body": (
                    "Bitwise operators have lower precedence than == and <, and much lower than "
                    "arithmetic. cout << a & b does not do what you expect, wrap every bitwise "
                    "expression in parentheses."
                ),
                "pro_tip": (
                    "When in doubt, parenthesize. It costs one character and saves a night of "
                    "debugging."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    int a = 6;   // 110\n"
            "    int b = 3;   // 011\n"
            "    cout << \"a & b = \" << (a & b) << endl;\n"
            "    cout << \"a | b = \" << (a | b) << endl;\n"
            "    cout << \"a ^ b = \" << (a ^ b) << endl;\n"
            "    cout << \"a << 1 = \" << (a << 1) << endl;\n"
            "    cout << \"a >> 1 = \" << (a >> 1) << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 5, "text": "6 in binary is 110"},
                {"line": 6, "text": "3 in binary is 011"},
                {"line": 7, "text": "& is bitwise AND, not &&"},
                {"line": 10, "text": "Shifting left by 1 doubles the value"},
                {"line": 11, "text": "Shifting right by 1 halves it"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "if (a & b == 0)",
                "fixed": "if ((a & b) == 0)",
                "why": "== has higher precedence than &, so the comparison runs first.",
            },
            {
                "wrong": "cout << a & b;",
                "fixed": "cout << (a & b);",
                "why": "Without parentheses, << grabs a and the bitwise operation is misparsed.",
            },
            {
                "wrong": "if (flags && MASK)",
                "fixed": "if (flags & MASK)",
                "why": "&& is logical AND for true/false. Checking bits needs the bitwise &.",
            },
        ],
        exercise={
            "description": "Combine FLAG_A (1) and FLAG_B (2) into a single flags value with |, then print whether FLAG_A is set and whether FLAG_C (4) is set.",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    int FLAG_A = 1;\n"
                "    int FLAG_B = 2;\n"
                "    int FLAG_C = 4;\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "flags = FLAG_A | FLAG_B",
                "Has A: (flags & FLAG_A) != 0",
                "Has C: (flags & FLAG_C) != 0",
            ],
            "expected_output": (
                "Flags: 3\n"
                "Has A: 1\n"
                "Has C: 0"
            ),
        },
        quiz={
            "question": "What does 6 << 1 evaluate to?",
            "options": ["3", "12", "6", "24"],
            "correct": 1,
            "explanation": "Shifting left by one bit doubles the value, so 6 << 1 is 12.",
        },
        key_takeaways=[
            "Bitwise operators work on individual bits",
            "&, |, ^, ~, <<, >> each have a distinct role",
            "<< by 1 doubles, >> by 1 halves",
            "Always parenthesize bitwise expressions",
        ],
        next_steps="Time for a compact decision maker: the ternary operator!",
    ),

    _lesson(
        lesson_id="cpp-l03-05",
        theory=(
            "The ternary operator cond ? a : b is a compact if-else. If cond is true the "
            "expression evaluates to a, otherwise to b. You can assign its result directly, "
            "which is perfect for choosing a value in one line."
            "\n\n"
            "Keep ternaries short. Once you nest them or make the branches long, a plain if-else "
            "is far easier to read."
        ),
        analogy=(
            "The ternary operator is like a coin flip that picks between two vending machines. "
            "Heads gives you the snack in slot a, tails gives you the one in slot b. It is one "
            "quick action that selects exactly one result."
        ),
        sections=[
            {
                "heading": "Anatomy of a ternary",
                "body": (
                    "cond ? a : b reads 'if cond, then a, otherwise b'. The whole thing is an "
                    "expression, so it produces a value you can assign, print, or pass to a "
                    "function."
                ),
                "pro_tip": (
                    "Both branches must be the same (or convertible) type. Mixing a string with "
                    "a number in the two branches will not compile."
                ),
            },
            {
                "heading": "Ternary vs if-else",
                "body": (
                    "Use a ternary when you are choosing a value. Use if-else when a branch does "
                    "several statements. Clarity beats cleverness, and a ternary with nested "
                    "ternaries is never clear."
                ),
                "pro_tip": (
                    "A good test: if your ternary does not fit comfortably on one line, "
                    "switch to if-else."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    int score = 72;\n"
            "    string result = (score >= 50) ? \"Pass\" : \"Fail\";\n"
            "    cout << \"Result: \" << result << endl;\n"
            "    int maxVal = (score > 60) ? score : 60;\n"
            "    cout << \"Max: \" << maxVal << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 6, "text": "Selects one of two strings based on the score"},
                {"line": 8, "text": "Chooses the larger of score and 60"},
                {"line": 9, "text": "The chosen value is printed like any variable"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "string r = (score >= 50) ? \"Pass\" : 0;",
                "fixed": "string r = (score >= 50) ? \"Pass\" : \"Fail\";",
                "why": "Both branches must have compatible types; a string and an int do not mix.",
            },
            {
                "wrong": "string r = a > b ? \"a\" : b > c ? \"b\" : \"c\";",
                "fixed": "if/else with clear named branches",
                "why": "Nested ternaries become unreadable. Use if-else for layered decisions.",
            },
            {
                "wrong": "int x = (score > 60) ? score + 1;",
                "fixed": "int x = (score > 60) ? score + 1 : score;",
                "why": "A ternary always needs both branches separated by the colon.",
            },
        ],
        exercise={
            "description": "A student scored 45 in one test and 78 in another. Print whether the first mark is a Pass or Fail (50 is the threshold) and print the higher of the two marks.",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    int marks1 = 45;\n"
                "    int marks2 = 78;\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "string verdict = (marks1 >= 50) ? \"Pass\" : \"Fail\";",
                "int higher = (marks1 > marks2) ? marks1 : marks2;",
                "Print both with labels",
            ],
            "expected_output": (
                "Marks 1 is Fail\n"
                "Higher: 78"
            ),
        },
        quiz={
            "question": "What does (5 > 3) ? \"yes\" : \"no\" evaluate to?",
            "options": ["no", "yes", "1", "0"],
            "correct": 1,
            "explanation": "5 > 3 is true, so the ternary evaluates to the first branch, \"yes\".",
        },
        key_takeaways=[
            "cond ? a : b selects one of two values",
            "The whole ternary is an expression producing a value",
            "Both branches must have compatible types",
            "Prefer if-else when the logic gets long",
        ],
        next_steps="Now for the showstopper: teaching your own classes to use operators!",
    ),

    _lesson(
        lesson_id="cpp-l03-06",
        theory=(
            "Operator overloading lets custom types use the same operators as built-ins. With "
            "the keyword operator you can define what a + b means for your own class, so "
            "Money(5, 75) + Money(2, 50) feels natural instead of a verbose helper function."
            "\n\n"
            "The overloaded operator is really a function, and it must keep its natural meaning. "
            "Overloading + to subtract would confuse every future reader of your code."
        ),
        analogy=(
            "Operator overloading is like teaching a dog a new command word. 'Sit' already means "
            "something for people, and you teach your dog the same word to mean its own version "
            "of sitting. The word stays intuitive, the behavior is tailored to the audience."
        ),
        sections=[
            {
                "heading": "Writing an operator",
                "body": (
                    "Inside the class, Money operator+(const Money& other) declares a function "
                    "that + will call. It receives the other Money by reference, combines the "
                    "values, and returns a brand new Money."
                ),
                "pro_tip": (
                    "Take the parameter as const& so no copy is made and the original is "
                    "protected. This is the idiomatic signature for binary operators."
                ),
            },
            {
                "heading": "Designing good overloads",
                "body": (
                    "An operator should mean exactly what it means for built-in types. + should "
                    "add, == should compare, << should output. Keep the semantics obvious and "
                    "your classes will read like the language itself."
                ),
                "pro_tip": (
                    "The compiler picks the overload by looking at the operand types. a + b with "
                    "two Money objects calls your operator+ automatically."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "class Money {\n"
            "public:\n"
            "    int dollars;\n"
            "    int cents;\n"
            "    Money(int d, int c) : dollars(d), cents(c) {}\n"
            "    Money operator+(const Money& other) {\n"
            "        int totalCents = (dollars + other.dollars) * 100\n"
            "                       + cents + other.cents;\n"
            "        return Money(totalCents / 100, totalCents % 100);\n"
            "    }\n"
            "};\n"
            "\n"
            "int main() {\n"
            "    Money a(5, 75);\n"
            "    Money b(2, 50);\n"
            "    Money total = a + b;\n"
            "    cout << total.dollars << \".\" << total.cents << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 8, "text": "A constructor sets up dollars and cents"},
                {"line": 9, "text": "operator+ defines what a + b means for Money"},
                {"line": 12, "text": "Carries cents into dollars to return a fresh Money"},
                {"line": 19, "text": "+ now works on Money objects naturally"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "Money operator+(Money other)",
                "fixed": "Money operator+(const Money& other)",
                "why": "Passing by value copies the object; const& avoids the copy and protects it.",
            },
            {
                "wrong": "Money operator+(const Money& other) { // modifies this instead of returning new }",
                "fixed": "Return a new Money and leave both operands untouched",
                "why": "a + b should not change a. Arithmetic operators conventionally return new values.",
            },
            {
                "wrong": "int operator+(const Money& other) { return dollars; } // for addition",
                "fixed": "Money operator+(const Money& other) { ... }",
                "why": "The return type should match the meaning. Adding money returns money, not an int.",
            },
        ],
        exercise={
            "description": "Add an operator== to the Money class that returns true only when both dollars AND cents are equal, then test it with the given objects.",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "class Money {\n"
                "public:\n"
                "    int dollars;\n"
                "    int cents;\n"
                "    Money(int d, int c) : dollars(d), cents(c) {}\n"
                "    // Your code here\n"
                "};\n"
                "\n"
                "int main() {\n"
                "    Money a(5, 75);\n"
                "    Money b(5, 75);\n"
                "    Money c(2, 50);\n"
                "    cout << (a == b) << endl;\n"
                "    cout << (a == c) << endl;\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "bool operator==(const Money& other) const",
                "Return dollars == other.dollars && cents == other.cents",
                "The calls in main already use ==, you only add the overload",
            ],
            "expected_output": (
                "1\n"
                "0"
            ),
        },
        quiz={
            "question": "Which keyword declares an overloaded operator in C++?",
            "options": ["overload", "operator", "function", "def"],
            "correct": 1,
            "explanation": "The operator keyword, as in Money operator+(const Money& other).",
        },
        key_takeaways=[
            "operator + customizes operators for your classes",
            "Pass operands by const& to avoid copies",
            "Arithmetic operators should return new values",
            "Keep the operator's meaning natural",
        ],
        next_steps="Let us practice building real boolean expressions like a pro!",
    ),

    _lesson(
        lesson_id="cpp-l03-07",
        theory=(
            "This practice lesson builds boolean expressions that combine comparisons with &&, "
            "||, and !. Real rules like 'allowed if adult OR with a guardian' map directly onto "
            "these operators, so building these expressions trains exactly the thinking you need "
            "for real logic."
            "\n\n"
            "The number one enemy is precedence. Comparisons run before logical operators, so "
            "parentheses around each comparison make your intent obvious and keep you safe."
        ),
        analogy=(
            "Building a boolean expression is like setting up an obstacle course. Each "
            "comparison is one obstacle with a pass/fail gate, the && gates require you to clear "
            "both obstacles, || lets you pick either path, and ! inverts the course. "
            "Parentheses mark which obstacles belong to which gate."
        ),
        sections=[
            {
                "heading": "Composing real rules",
                "body": (
                    "Take the rule 'allowed if 18 or older, or accompanied by a guardian'. That "
                    "translates to (age >= 18) || withGuardian. Each English condition becomes "
                    "one comparison, and the logical words become && and ||."
                ),
                "pro_tip": (
                    "Write the English rule as a comment above your expression. If the comment "
                    "and the code disagree, one of them is wrong."
                ),
            },
            {
                "heading": "Precedence in practice",
                "body": (
                    "C++ evaluates ! first, then comparisons, then &&, then ||. That means "
                    "age >= 12 && !(age >= 65) groups as intended, but adding || without "
                    "parentheses can silently change the meaning."
                ),
                "pro_tip": (
                    "Parenthesize every comparison. Even if it is not required, it makes the "
                    "expression self-documenting."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    int age = 17;\n"
            "    bool withGuardian = true;\n"
            "    bool allowed = (age >= 18) || withGuardian;\n"
            "    bool needsTicket = (age >= 12) && !(age >= 65);\n"
            "    cout << \"Allowed: \" << allowed << endl;\n"
            "    cout << \"Needs ticket: \" << needsTicket << endl;\n"
            "    bool senior = age >= 65;\n"
            "    cout << \"Senior: \" << senior << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 7, "text": "|| is true when either side holds"},
                {"line": 8, "text": "&& with ! builds a range: 12 to 64"},
                {"line": 11, "text": "A comparison result stored in a named bool"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "bool ok = age >= 18 || hasID && !banned;",
                "fixed": "bool ok = (age >= 18) || (hasID && !banned);",
                "why": "Without parentheses the grouping is done by precedence rules, not by your intent.",
            },
            {
                "wrong": "if (!age >= 18)",
                "fixed": "if (!(age >= 18))",
                "why": "! applies to age first, not to the whole comparison.",
            },
            {
                "wrong": "bool needsTicket = (age >= 12) || (age < 65);",
                "fixed": "bool needsTicket = (age >= 12) && !(age >= 65);",
                "why": "A range requires &&; || would accept nearly everyone.",
            },
        ],
        exercise={
            "description": "A 21-year-old with a license and a clean record wants to drive, vote, and rent a car. Print: canDrive (licensed AND clean record), canVote (21 or older), and rentalEligible (canDrive AND canVote).",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    int age = 21;\n"
                "    bool hasLicense = true;\n"
                "    bool cleanRecord = true;\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "canDrive = hasLicense && cleanRecord",
                "canVote = (age >= 18)",
                "rentalEligible = canDrive && canVote",
            ],
            "expected_output": (
                "Can drive: 1\n"
                "Can vote: 1\n"
                "Rental eligible: 1"
            ),
        },
        quiz={
            "question": "What does (false || true) && false evaluate to?",
            "options": ["true", "false", "Compile error", "1"],
            "correct": 1,
            "explanation": "false || true is true, but true && false is false.",
        },
        key_takeaways=[
            "English rules map directly onto boolean operators",
            "Parenthesize every comparison",
            "! applies to the value right next to it",
            "Ranges need &&, alternatives need ||",
        ],
        next_steps="Now a classic systems challenge: packing flags into a single int!",
    ),

    _lesson(
        lesson_id="cpp-l03-08",
        theory=(
            "Bit flags pack several true/false settings into a single integer. Each bit is one "
            "flag, you switch bits on with |, check them with &, and toggle them with ^. This "
            "is exactly how permission systems and game settings work under the hood."
            "\n\n"
            "A single int can hold 32 independent flags, making it an incredibly compact way to "
            "store state."
        ),
        analogy=(
            "Bit flags are like the setting toggles on a physical mixer board. Each fader has "
            "an ON or OFF state, and the whole board is one panel. | flicks a switch on, & "
            "checks whether a switch is on, and ^ flips it. One panel (one int) holds all the "
            "controls."
        ),
        sections=[
            {
                "heading": "Setting, checking, toggling",
                "body": (
                    "Set bits with |: perms = READ | WRITE. Check with &: (perms & READ) != 0 is "
                    "true when READ is on. Toggle with ^=: perms ^= EXECUTE flips that bit. "
                    "Turn off with &= ~MASK."
                ),
                "pro_tip": (
                    "Use powers of two for flag values: 1, 2, 4, 8. Each one occupies its own "
                    "unique bit, so flags never collide."
                ),
            },
            {
                "heading": "Why not 32 booleans?",
                "body": (
                    "Thirty-two separate bool variables would do the same job, but bit flags "
                    "store everything in one int, copy in one assignment, and combine with a "
                    "single operation. File permissions in Linux use exactly this trick."
                ),
                "pro_tip": (
                    "Read permissions as octal in Linux (like 755). Those digits are three sets "
                    "of bit flags for owner, group, and others."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    int READ = 4;\n"
            "    int WRITE = 2;\n"
            "    int EXECUTE = 1;\n"
            "    int perms = READ | WRITE;\n"
            "    cout << \"Can read: \" << ((perms & READ) != 0) << endl;\n"
            "    cout << \"Can write: \" << ((perms & WRITE) != 0) << endl;\n"
            "    cout << \"Can exec: \" << ((perms & EXECUTE) != 0) << endl;\n"
            "    perms |= EXECUTE;\n"
            "    cout << \"After grant, can exec: \" << ((perms & EXECUTE) != 0) << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 8, "text": "| combines READ and WRITE into one int"},
                {"line": 9, "text": "& tests a single flag; != 0 means it is on"},
                {"line": 12, "text": "|= switches a bit on permanently"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "if ((perms & READ) == 1)",
                "fixed": "if ((perms & READ) != 0)",
                "why": "READ is 4, so perms & READ is 4 or 0, never 1. Test against zero instead.",
            },
            {
                "wrong": "perms = READ | WRITE; // then perms = READ; // accidentally losing WRITE",
                "fixed": "perms |= READ; // add one flag without clearing others",
                "why": "Plain assignment replaces everything. Use |= to modify just one bit.",
            },
            {
                "wrong": "if (perms & READ != 0)",
                "fixed": "if ((perms & READ) != 0)",
                "why": "!= binds tighter than &, so the comparison would run first.",
            },
        ],
        exercise={
            "description": "A settings int starts as 6 (binary 110: DARK_MODE and SOUND are on, NOTIFICATIONS off). Toggle DARK_MODE with ^= and print its state before and after.",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    int DARK_MODE = 4;\n"
                "    int settings = 6;\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "Before: (settings & DARK_MODE) != 0",
                "Toggle with settings ^= DARK_MODE;",
                "Print the state again after toggling",
            ],
            "expected_output": (
                "Dark mode on: 1\n"
                "After toggle: 0"
            ),
        },
        quiz={
            "question": "If perms = 4 | 2, what does (perms & 1) equal?",
            "options": ["1", "6", "0", "4"],
            "correct": 2,
            "explanation": "perms is 6 (110). Bit 1 (001) is not set, so perms & 1 is 0.",
        },
        key_takeaways=[
            "Each bit is an independent flag",
            "| sets bits, & checks bits, ^ toggles bits",
            "Use powers of two for flag values",
            "Always parenthesize bitwise expressions",
        ],
        next_steps="Grand finale: build a tiny math expression parser using every operator you learned!",
    ),

    _lesson(
        lesson_id="cpp-l03-09",
        theory=(
            "This project ties the whole level together: a tiny expression parser. It evaluates "
            "an expression like 10 + 4 * 2 while respecting operator precedence, the rule that "
            "* and / bind tighter than + and -. Implementing this yourself demystifies what "
            "every calculator does."
            "\n\n"
            "The key insight is to evaluate the tighter-bound sub-expression first, then combine "
            "with the outer operator, exactly the order a real parser would use."
        ),
        analogy=(
            "A parser is like a court judge ruling on a disputed order of operations. The "
            "multiplication case gets heard first because * and / have seniority, and only after "
            "that ruling does the judge handle the + case. Each operator has a rank, and the "
            "higher rank always speaks first."
        ),
        sections=[
            {
                "heading": "The precedence problem",
                "body": (
                    "Evaluating 10 + 4 * 2 left to right gives 28, which is wrong. Because * "
                    "binds tighter, the parser must compute 4 * 2 first to get 8, then add 10 "
                    "for the correct answer, 18."
                ),
                "pro_tip": (
                    "The heart of any parser is deciding which sub-expression to evaluate "
                    "first. Real parsers turn this into a tree; ours uses if/else on operator "
                    "priority."
                ),
            },
            {
                "heading": "How the parser decides",
                "body": (
                    "We check both operators with bools: highFirst and highSecond. If the second "
                    "operator is * or /, we evaluate b and c first. Otherwise, if the first "
                    "operator is high priority, we evaluate a and b first. Otherwise everything "
                    "is + or -, so left to right is fine."
                ),
                "pro_tip": (
                    "Ternary operators keep the branches short and readable. Notice how the "
                    "parser's if-chain mirrors the way your brain thinks about math."
                ),
            },
        ],
        code_example=_code(
            "#include <iostream>\n"
            "using namespace std;\n"
            "\n"
            "int main() {\n"
            "    double a = 10, b = 4, c = 2;\n"
            "    char op1 = '+';\n"
            "    char op2 = '*';\n"
            "    double first, second, result;\n"
            "    bool highFirst = (op1 == '*' || op1 == '/');\n"
            "    bool highSecond = (op2 == '*' || op2 == '/');\n"
            "    if (highSecond) {\n"
            "        first = a;\n"
            "        second = (op2 == '*') ? b * c : b / c;\n"
            "        result = (op1 == '+') ? first + second : first - second;\n"
            "    } else if (highFirst) {\n"
            "        first = (op1 == '*') ? a * b : a / b;\n"
            "        second = c;\n"
            "        result = (op2 == '+') ? first + second : first - second;\n"
            "    } else {\n"
            "        first = (op1 == '+') ? a + b : a - b;\n"
            "        second = c;\n"
            "        result = (op2 == '+') ? first + second : first - second;\n"
            "    }\n"
            "    cout << a << \" \" << op1 << \" \" << b << \" \"\n"
            "         << op2 << \" \" << c << \" = \" << result << endl;\n"
            "    return 0;\n"
            "}",
            [
                {"line": 9, "text": "Detects whether the first operator binds tightly"},
                {"line": 11, "text": "When op2 is * or /, b and c combine first"},
                {"line": 15, "text": "Otherwise a and b combine first"},
                {"line": 24, "text": "Prints the full expression and its value"},
            ],
        ),
        common_mistakes=[
            {
                "wrong": "result = a + b * c; // assuming left-to-right evaluation",
                "fixed": "Compute b * c first, then add a",
                "why": "C++ follows precedence rules, not left-to-right order, for mixed operators.",
            },
            {
                "wrong": "second = b / c; // when c is 0",
                "fixed": "Guard against division by zero before evaluating",
                "why": "Dividing by zero crashes the program or yields undefined behavior.",
            },
            {
                "wrong": "if (op2 == \"*\")",
                "fixed": "if (op2 == '*')",
                "why": "op2 is a char, so it must be compared with a single-quoted character.",
            },
        ],
        exercise={
            "description": "Change the parser's inputs to op1 = '-' and op2 = '/' and confirm it prints the correct result for 10 - 4 / 2. The b / c sub-expression should be evaluated first.",
            "starter_code": (
                "#include <iostream>\n"
                "using namespace std;\n"
                "\n"
                "int main() {\n"
                "    double a = 10, b = 4, c = 2;\n"
                "    char op1 = '-';\n"
                "    char op2 = '/';\n"
                "    double first, second, result;\n"
                "    // Your code here\n"
                "    return 0;\n"
                "}"
            ),
            "hints": [
                "The highSecond branch evaluates b / c first",
                "Then the outer operator subtracts: a - second",
                "4 / 2 is 2, so the result is 10 - 2 = 8",
            ],
            "expected_output": "10 - 4 / 2 = 8",
        },
        quiz={
            "question": "In the expression 10 + 4 * 2, which operation is performed first?",
            "options": [
                "10 + 4",
                "4 * 2",
                "They happen at the same time",
                "It depends on the compiler",
            ],
            "correct": 1,
            "explanation": "* and / have higher precedence than + and -, so 4 * 2 is computed first.",
        },
        key_takeaways=[
            "Precedence decides the order of operations",
            "* and / bind tighter than + and -",
            "A parser evaluates the tighter sub-expression first",
            "Ternary operators keep branch logic compact",
        ],
        next_steps="Congratulations, you built your own expression engine! Level 3 is complete.",
    ),
]))
