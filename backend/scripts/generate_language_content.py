"""Generate C++, Java, Python hand-crafted lessons and append to lesson_content.py.

Usage:
    python generate_language_content.py

This script reads lesson_content.py, generates high-quality hand-crafted
lesson content for C++, Java, and Python (levels 1-3, ~25 lessons each),
and inserts them before the template generator section.
"""

import re
from typing import Any


# ── helpers to format Python source code ──────────────────────────────


def _q(val: str) -> str:
    """Quote a string for Python source output (uses double quotes)."""
    escaped = (
        val
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
    )
    return f'"{escaped}"'


def _fmt(val: Any, indent: int = 0) -> str:
    """Format a Python value as minimal source code."""
    pad = "    " * indent
    pad1 = "    " * (indent + 1)

    if val is None:
        return "None"
    if isinstance(val, bool):
        return "True" if val else "False"
    if isinstance(val, int):
        return str(val)

    if isinstance(val, str):
        if "\n" in val:
            lines = val.split("\n")
            inner = "\n".join(
                f"{pad1}{_q(line)}"
                for line in lines
            )
            return f"(\n{inner}\n{pad})"
        return _q(val)

    if isinstance(val, list):
        if not val:
            return "[]"
        items = ",\n".join(
            f"{pad1}{_fmt(item, indent + 1)}"
            for item in val
        )
        return f"[\n{items},\n{pad}]"

    if isinstance(val, dict):
        if not val:
            return "{}"
        items = ",\n".join(
            f'{pad1}{_q(k)}: {_fmt(v, indent + 1)}'
            for k, v in val.items()
        )
        return f"{{\n{items},\n{pad}}}"

    return repr(val)


def _lesson_call(
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
) -> str:
    """Generate the Python source for a _lesson() call."""
    indent = 1
    pad = "    " * indent
    out = [f"{pad}_lesson("]
    out.append(f'{pad}    lesson_id={_q(lesson_id)},')
    out.append(f"{pad}    theory={_fmt(theory, indent + 1)},")
    out.append(f"{pad}    analogy={_fmt(analogy, indent + 1)},")
    out.append(f"{pad}    sections={_fmt(sections, indent + 1)},")

    if code_example is not None:
        out.append(f"{pad}    code_example={_fmt(code_example, indent + 1)},")
    if common_mistakes is not None:
        out.append(f"{pad}    common_mistakes={_fmt(common_mistakes, indent + 1)},")
    if exercise is not None:
        out.append(f"{pad}    exercise={_fmt(exercise, indent + 1)},")
    if quiz is not None:
        out.append(f"{pad}    quiz={_fmt(quiz, indent + 1)},")
    if key_takeaways is not None:
        out.append(f"{pad}    key_takeaways={_fmt(key_takeaways, indent + 1)},")
    if next_steps:
        out.append(f"{pad}    next_steps={_q(next_steps)},")

    out.append(f"{pad}),")
    return "\n".join(out)


def _section(heading: str, body: str, code: str | None = None, pro_tip: str | None = None) -> dict:
    d: dict[str, Any] = {"heading": heading, "body": body}
    if code is not None:
        d["code"] = code
    if pro_tip is not None:
        d["pro_tip"] = pro_tip
    return d


def _code_example(code: str, annotations: list[dict[str, Any]]) -> dict:
    return {"code": code, "annotations": annotations}


def _anno(line: int, text: str) -> dict[str, Any]:
    return {"line": line, "text": text}


def _mistake(mistake: str, fix: str, code: str, fixed_code: str) -> dict:
    return {"mistake": mistake, "fix": fix, "code": code, "fixed_code": fixed_code}


def _exercise(description: str, starter_code: str, hints: list[str], expected_output: str) -> dict:
    return {"description": description, "starter_code": starter_code, "hints": hints, "expected_output": expected_output}


def _quiz(question: str, options: list[str], correct: int, explanation: str) -> dict:
    return {"question": question, "options": options, "correct": correct, "explanation": explanation}


def _add(lesson_id: str, **kw) -> str:
    return _lesson_call(lesson_id, **kw)


# ═══════════════════════════════════════════════════════════════════════
# LESSON CONTENT GENERATORS
# ═══════════════════════════════════════════════════════════════════════


def _build_cpp_lesson_source() -> str:
    """Build all C++ lesson content and return it as Python source code."""
    lines: list[str] = []
    _L = lines.append

    _L("")
    _L("")
    _L("# ============================================================================")
    _L("# C++ LEVEL 1: FIRST STEPS")
    _L("# ============================================================================")
    _L("")
    _L("HAND_CRAFTED_LESSONS.update(dict([")

    # ── C++ Level 1: Lesson 1 ────────────────────────────────────────
    _L(_add(
        lesson_id="cpp-l01-01",
        theory=(
            "C++ was created in 1985 by Bjarne Stroustrup as an extension of the C language. "
            "The name C++ comes from the C increment operator ++ which means add one to C. "
            "C++ adds object-oriented programming, classes, templates, and a massive standard "
            "library (STL) to the power of C."
            "\n\n"
            "C++ is used everywhere: game engines (Unreal Engine), web browsers (Chrome, Firefox), "
            "operating systems (Windows, macOS parts), financial trading systems, machine learning "
            "frameworks (TensorFlow, PyTorch), and even Photoshop. "
            "It combines high performance with high-level abstractions."
            "\n\n"
            "Unlike C which is purely procedural, C++ supports multiple programming paradigms: "
            "procedural (like C), object-oriented (classes and objects), generic (templates), "
            "and functional (lambdas). This makes it incredibly flexible."
        ),
        analogy=(
            "If C is a manual transmission car, C++ is an automatic with sport mode. "
            "You get the same raw power and speed, but with features that make driving easier. "
            "The engine is the same under the hood, but C++ adds power steering, cruise control, "
            "and a turbo boost (the STL). You can still pop the hood and tweak everything, "
            "but you do not have to."
        ),
        sections=[
            _section(
                heading="What makes C++ special?",
                body=(
                    "Three things: zero-cost abstractions, the STL, and backward compatibility. "
                    "Zero-cost abstractions mean you can use high-level features like classes and "
                    "templates without any performance penalty. The Standard Template Library (STL) "
                    "gives you ready-to-use data structures like vectors, maps, and sorting algorithms. "
                    "And C++ is mostly backward-compatible with C, so you can use C libraries directly."
                ),
                pro_tip=(
                    "C++ is one of the most sought-after languages for high-frequency trading "
                    "because every microsecond counts, and C++ gives you full control over performance."
                ),
            ),
            _section(
                heading="C++ vs C: what is different?",
                body=(
                    "C++ adds classes and objects, which let you bundle data with the functions "
                    "that operate on it. It adds references (safer than pointers), function overloading "
                    "(same function name, different parameters), and the cout/cin streams that are "
                    "type-safe (unlike printf/scanf). C++ also has exceptions for error handling "
                    "and namespaces to organize code."
                ),
                pro_tip=(
                    "The biggest upgrade from C to C++ is the STL. Writing vector<int> v; gives you "
                    "a dynamic array that can grow and shrink. In C you would need to manage "
                    "malloc/realloc/free yourself."
                ),
            ),
        ],
        key_takeaways=[
            "C++ is C with added features: classes, templates, STL, exceptions",
            "C++ gives you high performance with high-level abstractions (zero-cost principle)",
            "The STL provides ready-to-use containers and algorithms",
            "C++ is used in games, browsers, operating systems, and finance",
            "C++ is backwards-compatible with most C code",
        ],
        next_steps="Ready to write your first C++ program? Let us go to the next lesson!",
    ))

    _L(_add(
        lesson_id="cpp-l01-02",
        theory=(
            "Let us write your first C++ program! The classic Hello World looks similar to C "
            "but with a few important differences. Instead of printf, C++ uses cout (pronounced "
            "see-out) for output. Instead of #include <stdio.h>, we use #include <iostream>."
            "\n\n"
            "Every C++ program still needs a main function in C++, int main() is the entry point. "
            "You will also see using namespace std; which tells the compiler to look for names "
            "like cout in the std (standard) namespace. Without it, you would have to write "
            "std::cout every time."
            "\n\n"
            "The << operator (stream insertion operator) sends data to cout. Think of it like "
            "an arrow pointing the data into the output stream. You can chain multiple << "
            "operators to print multiple things."
        ),
        analogy=(
            "A C++ program is like a factory assembly line. #include <iostream> brings in the "
            "machinery. using namespace std; sets up the tools where you can reach them. "
            "int main() is the start button. cout is the conveyor belt, and << pushes items "
            "onto the belt. Each item gets printed in order."
        ),
        sections=[
            _section(
                heading="Your first C++ program",
                body=(
                    "Here is the complete Hello World program in C++. Notice there are no "
                    "format specifiers like %d or %s. C++ automatically figures out the type "
                    "of each value you send to cout."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    std::cout << "Hello, World!" << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "std::endl adds a newline and flushes the output buffer. You can also "
                    "just use \\n inside the string, which does not flush. For most programs, "
                    "\\n is faster."
                ),
            ),
            _section(
                heading="Using 'using namespace std;'",
                body=(
                    "Many tutorials use using namespace std; at the top so you can write "
                    "cout instead of std::cout. It is convenient, but for larger projects "
                    "it can cause naming conflicts. For now either style is fine."
                ),
                code=(
                    '#include <iostream>\n'
                    'using namespace std;\n'
                    '\n'
                    'int main() {\n'
                    '    cout << "Hello, World!" << endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Professional C++ code typically uses std:: prefix instead of "
                    "using namespace std; to avoid name clashes. Get used to it early."
                ),
            ),
        ],
        code_example=_code_example(
            code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    std::cout << "Hello, World!" << std::endl;\n'
                '    return 0;\n'
                '}'
            ),
            annotations=[
                _anno(1, "Includes the iostream header for input/output streams"),
                _anno(3, "Every C++ program starts with int main()"),
                _anno(4, "cout prints text; << sends data into cout; endl adds a newline"),
                _anno(5, "return 0 tells the OS the program finished successfully"),
            ],
        ),
        common_mistakes=[
            _mistake(
                mistake="Writing cout without std:: or using namespace std;",
                fix="Either write std::cout or add using namespace std; at the top",
                code='cout << "Hello";',
                fixed_code='std::cout << "Hello";',
            ),
            _mistake(
                mistake="Forgetting the #include <iostream> line",
                fix="Always include <iostream> before using cout or cin",
                code='int main() { cout << "Hi"; }',
                fixed_code='#include <iostream>\nint main() { std::cout << "Hi"; }',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that prints your name, age, and favorite color "
                "on three separate lines using cout."
            ),
            starter_code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    // Write your code here\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Use std::cout << ... << std::endl; for each line",
                "You can use multiple cout statements or chain << operators",
                "Put each piece of info on its own line",
            ],
            expected_output=(
                "Name: Alex\n"
                "Age: 18\n"
                "Favorite Color: Blue"
            ),
        ),
        key_takeaways=[
            "#include <iostream> is needed for input/output",
            "cout << value prints value to the terminal",
            "std::endl or \\n adds a newline",
            "int main() is the entry point of every C++ program",
            "Every statement ends with a semicolon",
        ],
        next_steps="Great! Now let us learn more about output formatting with cout.",
    ))

    _L(_add(
        lesson_id="cpp-l01-03",
        theory=(
            "cout is much smarter than printf. It automatically detects the type of the data "
            "you send it. You do not need %d for integers or %f for floats. Just send the "
            "value and cout handles the formatting."
            "\n\n"
            "You can chain multiple values with the << operator: "
            'cout << "Value: " << x << " and " << y << endl;'
            "\n\n"
            "You can also format numbers. To print a float with 2 decimal places, you use "
            "#include <iomanip> and then setprecision(2) or fixed << setprecision(2)."
        ),
        analogy=(
            "cout with << is like a train track. Each << is a connector between train cars. "
            "The first car is cout itself. You attach a string car, then a number car, "
            "then another string car. The whole train moves to the terminal screen."
        ),
        sections=[
            _section(
                heading="Chaining output",
                body=(
                    "You can mix text, numbers, and variables in one chain. "
                    "Each << adds another piece to the output."
                ),
                code=(
                    '#include <iostream>\n'
                    '#include <string>\n'
                    '\n'
                    'int main() {\n'
                    '    std::string name = "Alex";\n'
                    '    int age = 18;\n'
                    '    double height = 5.9;\n'
                    '    std::cout << "Name: " << name\n'
                    '              << ", Age: " << age\n'
                    '              << ", Height: " << height << "ft"\n'
                    '              << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "You can split a long cout chain across multiple lines by ending "
                    "each line with << and continuing on the next line."
                ),
            ),
            _section(
                heading="Formatting numbers",
                body=(
                    "Use #include <iomanip> and setprecision() to control decimal places."
                ),
                code=(
                    '#include <iostream>\n'
                    '#include <iomanip>\n'
                    '\n'
                    'int main() {\n'
                    '    double pi = 3.1415926535;\n'
                    '    std::cout << "Default: " << pi << std::endl;\n'
                    '    std::cout << "2 decimals: " << std::fixed\n'
                    '              << std::setprecision(2) << pi << std::endl;\n'
                    '    std::cout << "4 decimals: " << std::fixed\n'
                    '              << std::setprecision(4) << pi << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "std::fixed makes setprecision control digits after the decimal point. "
                    "Without fixed, setprecision controls total significant digits."
                ),
            ),
        ],
        code_example=_code_example(
            code=(
                '#include <iostream>\n'
                '#include <iomanip>\n'
                '#include <string>\n'
                '\n'
                'int main() {\n'
                '    int score = 95;\n'
                '    double average = 87.3333;\n'
                '    char grade = \'A\';\n'
                '    std::cout << "Score: " << score << std::endl;\n'
                '    std::cout << "Average: " << std::fixed\n'
                '              << std::setprecision(1) << average << std::endl;\n'
                '    std::cout << "Grade: " << grade << std::endl;\n'
                '    return 0;\n'
                '}'
            ),
            annotations=[
                _anno(1, "Include iostream for cout"),
                _anno(2, "Include iomanip for setprecision"),
                _anno(6, "int variable holding an integer"),
                _anno(7, "double variable holding a decimal number"),
                _anno(10, "Chaining cout with text and variable"),
                _anno(11, "setprecision(1) limits to 1 decimal place"),
            ],
        ),
        common_mistakes=[
            _mistake(
                mistake="Forgetting #include <iomanip> when using setprecision",
                fix="Always include <iomanip> when you need formatted output",
                code='cout << setprecision(2) << pi;',
                fixed_code='#include <iomanip>\ncout << setprecision(2) << pi;',
            ),
            _mistake(
                mistake="Forgetting std:: before setprecision or fixed",
                fix="Use std::setprecision and std::fixed, or add using namespace std;",
                code='cout << fixed << setprecision(2) << x;',
                fixed_code='std::cout << std::fixed << std::setprecision(2) << x;',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that declares three variables (int, double, string), "
                "assigns them values, and prints them in a formatted sentence."
            ),
            starter_code=(
                '#include <iostream>\n'
                '#include <string>\n'
                '#include <iomanip>\n'
                '\n'
                'int main() {\n'
                '    // Declare variables here\n'
                '    // Print formatted output here\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Use std::string for text, int for whole numbers, double for decimals",
                "Chain multiple << operators to print everything in one cout",
                "Use std::fixed << std::setprecision(2) for decimals",
            ],
            expected_output=(
                "Product: Laptop, Price: $899.99, Quantity: 3"
            ),
        ),
        key_takeaways=[
            "cout automatically detects the type of data you print",
            "Chain values with the << operator",
            "Use #include <iomanip> and setprecision for number formatting",
            "std::fixed ensures consistent decimal places",
            "Split long cout chains across lines for readability",
        ],
        next_steps="Now let us learn about comments in C++.",
    ))

    _L(_add(
        lesson_id="cpp-l01-04",
        theory=(
            "Comments are notes you leave in your code for yourself and other programmers. "
            "The compiler completely ignores them they are for humans, not machines. "
            "Good comments explain WHY you did something, not WHAT the code does "
            "(the code itself shows what it does)."
            "\n\n"
            "C++ supports three comment styles. Single-line comments start with // and go "
            "to the end of the line. Multi-line comments use /* and */. C++ also has "
            "documentation comments starting with /// that tools like Doxygen can turn "
            "into documentation web pages."
        ),
        analogy=(
            "Comments are like sticky notes on a recipe. The recipe itself tells you what to do "
            "(add 2 cups of flour). A sticky note might say why: use cake flour not all-purpose "
            "because it makes the cake fluffier. The sticky notes do not change the cooking, "
            "but they help the next person understand the reasoning."
        ),
        sections=[
            _section(
                heading="Single-line comments",
                body=(
                    "Use // for quick notes. Everything from // to the end of the line "
                    "is ignored. These are great for short explanations or marking TODOs."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    // This is a single-line comment\n'
                    '    std::cout << "Hello!" << std::endl;  // Inline comment\n'
                    '    // TODO: Add error handling later\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Use TODO comments to mark unfinished work. Many IDEs highlight "
                    "these and show a task list."
                ),
            ),
            _section(
                heading="Multi-line and documentation comments",
                body=(
                    "Use /* */ for longer explanations that span multiple lines. "
                    "Be careful: C-style comments do not nest. Documentation comments "
                    "with /// can describe functions and classes for auto-generated docs."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    '/*\n'
                    ' * This program calculates the area of a circle.\n'
                    ' * Formula: A = pi * r * r\n'
                    ' * Author: Alex\n'
                    ' */\n'
                    'int main() {\n'
                    '    double radius = 5.0;\n'
                    '    double area = 3.14159 * radius * radius;\n'
                    '    std::cout << "Area: " << area << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Many programmers use /* */ to temporarily disable code during debugging. "
                    "Just be careful not to nest them!"
                ),
            ),
        ],
        code_example=_code_example(
            code=(
                '#include <iostream>\n'
                '\n'
                '// Calculate factorial recursively\n'
                'int factorial(int n) {\n'
                '    // Base case: 0! = 1\n'
                '    if (n <= 1) return 1;\n'
                '    /* Recursive case:\n'
                '     * n! = n * (n-1)!\n'
                '     */\n'
                '    return n * factorial(n - 1);\n'
                '}\n'
                '\n'
                'int main() {\n'
                '    int num = 5;\n'
                '    std::cout << num << "! = " << factorial(num) << std::endl;\n'
                '    return 0;\n'
                '}'
            ),
            annotations=[
                _anno(3, "Single-line comment explaining the function"),
                _anno(5, "Inline comment explaining the base case"),
                _anno(7, "Multi-line comment for the recursive logic"),
            ],
        ),
        common_mistakes=[
            _mistake(
                mistake="Nesting /* */ comments (they do not nest in C++)",
                fix="Use // for inner comments or restructure the comment",
                code='/* Outer /* inner */ more outer */',
                fixed_code='/* Outer */\n// inner\n/* more outer */',
            ),
            _mistake(
                mistake="Writing comments that just repeat the code",
                fix="Explain WHY, not WHAT. The code already shows what it does.",
                code='int x = 5;  // declare x as 5',
                fixed_code='int x = 5;  // number of retries before timeout',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that prints a short bio about yourself. "
                "Use at least one single-line comment, one multi-line comment, "
                "and one inline comment explaining what each part does."
            ),
            starter_code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    // Add your comments and code here\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Start with a multi-line comment block describing the program",
                "Use // before each section to explain what you are printing",
                "Add inline comments after cout statements",
            ],
            expected_output=(
                "Name: Alex\n"
                "Age: 18\n"
                "Hobby: Coding"
            ),
        ),
        key_takeaways=[
            "Comments are ignored by the compiler they are for humans",
            "Use // for single-line comments, /* */ for multi-line",
            "Good comments explain WHY, not WHAT",
            "C-style comments (/* */) do not nest",
            "Use TODO comments to mark unfinished sections",
        ],
        next_steps="Now let us understand how C++ programs actually run.",
    ))

    _L(_add(
        lesson_id="cpp-l01-05",
        theory=(
            "C++ is a compiled language. This means your source code is translated into machine "
            "code (binary instructions the CPU understands) before you run it. The translation "
            "is done by a program called a compiler. The most common C++ compiler is g++ "
            "(part of the GCC collection)."
            "\n\n"
            "The compilation process has four stages. First, the preprocessor handles #include "
            "and #define directives. Second, the compiler translates C++ to assembly code. "
            "Third, the assembler converts assembly to machine code (object files). Fourth, "
            "the linker combines object files and libraries into one executable."
            "\n\n"
            "When you run g++ program.cpp -o program, the compiler does all four stages "
            "automatically. The -o flag specifies the output filename."
        ),
        analogy=(
            "Compiling C++ is like building furniture from IKEA instructions. Your C++ source "
            "code is the instruction manual. The compiler is you reading and following the "
            "instructions. Preprocessing is like finding all the tools you need. Compiling is "
            "building each piece separately. Linking is putting all the pieces together into "
            "a finished bookshelf (the executable)."
        ),
        sections=[
            _section(
                heading="Compilation vs interpretation",
                body=(
                    "Unlike Python or JavaScript which are interpreted (translated line-by-line "
                    "as they run), C++ is compiled all at once. This means: "
                    "1) Compilation takes time upfront, but execution is very fast. "
                    "2) Errors are caught at compile time before the program ever runs. "
                    "3) The output is a standalone executable that does not need anything else."
                ),
                pro_tip=(
                    "The compiled executable is specific to your operating system and CPU. "
                    "A Windows .exe will not run on a Mac. You must recompile for each platform."
                ),
            ),
            _section(
                heading="Common compiler flags",
                body=(
                    "g++ has many useful flags. -Wall enables all common warnings. "
                    "-std=c++17 sets the C++ standard version. -O2 enables optimizations. "
                    "-g adds debug information for use with a debugger like GDB."
                ),
                code=(
                    '# Compile with warnings and C++17\n'
                    'g++ -Wall -std=c++17 program.cpp -o program\n'
                    '\n'
                    '# Compile with optimizations for release\n'
                    'g++ -O2 -std=c++17 program.cpp -o program\n'
                    '\n'
                    '# Compile with debug info\n'
                    'g++ -g program.cpp -o program'
                ),
                pro_tip=(
                    "Always use -Wall when learning. Warnings catch mistakes that would "
                    "otherwise cause subtle bugs that are hard to find."
                ),
            ),
        ],
        code_example=_code_example(
            code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    std::cout << "Compilation successful!" << std::endl;\n'
                '    return 0;\n'
                '}'
            ),
            annotations=[
                _anno(1, "Preprocessor includes the iostream header"),
                _anno(3, "Compiler checks that main returns int and has correct signature"),
                _anno(4, "Compiler verifies cout and endl exist in the std namespace"),
                _anno(5, "Linker ensures the return statement connects to the OS exit mechanism"),
            ],
        ),
        common_mistakes=[
            _mistake(
                mistake="Forgetting to link required libraries",
                fix="Add -l flags for external libraries (e.g., -lm for math library)",
                code='g++ program.cpp -o program  // uses sqrt() but no -lm',
                fixed_code='g++ program.cpp -o program -lm',
            ),
            _mistake(
                mistake="Typing gcc instead of g++ for C++ programs",
                fix="Use g++ to compile C++ files; gcc is for C",
                code='gcc program.cpp -o program',
                fixed_code='g++ program.cpp -o program',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a small C++ program, then compile it using g++ with -Wall -std=c++17. "
                "Fix any warnings you see. Then run the executable."
            ),
            starter_code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    std::cout << "My first compiled program!" << std::endl;\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Save the file as test.cpp",
                "Run: g++ -Wall -std=c++17 test.cpp -o test",
                "If there are no errors, run ./test (or test.exe on Windows)",
            ],
            expected_output=(
                "My first compiled program!"
            ),
        ),
        key_takeaways=[
            "C++ is compiled, not interpreted",
            "Compilation: preprocessor, compiler, assembler, linker",
            "g++ -Wall -std=c++17 program.cpp -o program is the standard compile command",
            "Compiled executables are platform-specific",
            "Compiler warnings help catch bugs early",
        ],
        next_steps="Now let us practice writing and running a complete C++ program.",
    ))

    _L(_add(
        lesson_id="cpp-l01-06",
        theory=(
            "Now you know the basics of C++. This practice session will help you reinforce "
            "everything by writing a complete program from scratch. You will use cout, "
            "comments, and multiple lines of output."
            "\n\n"
            "Remember the structure: #include <iostream>, int main() { ... return 0; }. "
            "Practice this structure until it becomes automatic. Every C++ program you write "
            "will start the same way."
        ),
        analogy=(
            "Practicing the basic C++ program structure is like a musician practicing scales. "
            "Scales are not exciting, but every great musician practices them daily. "
            "The main function structure is your scale practice for programming."
        ),
        sections=[
            _section(
                heading="What to build",
                body=(
                    "Write a program that prints a simple ASCII art figure (like a smiley face "
                    "or a house) using multiple cout statements. This teaches you how to "
                    "control the exact placement of text on the screen."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    std::cout << "  *****  " << std::endl;\n'
                    '    std::cout << " *     * " << std::endl;\n'
                    '    std::cout << "*  O O  *" << std::endl;\n'
                    '    std::cout << "*   ^   *" << std::endl;\n'
                    '    std::cout << "*  ---  *" << std::endl;\n'
                    '    std::cout << " *     * " << std::endl;\n'
                    '    std::cout << "  *****  " << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Count the characters in each line to make your art symmetric. "
                    "Use spaces to align things properly."
                ),
            ),
        ],
        code_example=_code_example(
            code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    std::cout << "Hello, C++!" << std::endl;\n'
                '    std::cout << "This is my practice program." << std::endl;\n'
                '    std::cout << "I am learning output." << std::endl;\n'
                '    return 0;\n'
                '}'
            ),
            annotations=[
                _anno(1, "Include iostream for input/output"),
                _anno(3, "The starting point of every C++ program"),
                _anno(4, "cout prints a string; endl adds a newline"),
                _anno(7, "return 0 signals successful completion"),
            ],
        ),
        common_mistakes=[
            _mistake(
                mistake="Forgetting to close a string with a double quote",
                fix="Always match opening and closing quotes around strings",
                code='cout << "Hello << endl;',
                fixed_code='cout << "Hello" << endl;',
            ),
            _mistake(
                mistake="Putting a semicolon after main() like int main();",
                fix="Do not put a semicolon after the function header",
                code='int main(); {\n    cout << "Hi";\n}',
                fixed_code='int main() {\n    cout << "Hi";\n}',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that prints a simple house shape using ASCII art. "
                "Use at least 6 cout statements. Add comments explaining each part."
            ),
            starter_code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    // Draw the roof\n'
                '    std::cout << "   /\\\\   " << std::endl;\n'
                '    // Add more lines\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Start with the roof (triangular top)",
                "Add walls below the roof",
                "Add a door and windows inside the walls",
                "Use std::endl at the end of each line of art",
            ],
            expected_output=(
                "   /\\\n"
                "  /  \\\n"
                " /____\\\n"
                " |    |\n"
                " | [] |\n"
                " |____|"
            ),
        ),
        key_takeaways=[
            "Every C++ program needs #include <iostream> and int main()",
            "cout statements print text line by line",
            "std::endl moves to the next line",
            "Comments help organize your code",
            "Practice the basic structure until it is automatic",
        ],
        next_steps="Ready for a challenge? Let us try printing patterns!",
    ))

    _L(_add(
        lesson_id="cpp-l01-07",
        theory=(
            "This challenge tests your understanding of cout and output formatting. "
            "You will print various patterns using only cout statements. Pay attention to "
            "spacing, alignment, and how characters are placed on each line."
            "\n\n"
            "The key to printing patterns is understanding that each cout statement prints "
            "exactly one line. You control the horizontal position by adding spaces inside "
            "your strings. The pattern might be symmetric, so count your characters carefully."
        ),
        analogy=(
            "Printing patterns with cout is like creating a mosaic with tiles. Each tile "
            "is a character, and you place them row by row. You need to plan the whole "
            "picture before placing the first tile."
        ),
        sections=[
            _section(
                heading="Pattern ideas",
                body=(
                    "Try printing a checkerboard pattern, a right triangle of asterisks, "
                    "or a diamond shape. For the checkerboard, alternate spaces and asterisks "
                    "in each row. For the triangle, each row has one more asterisk than the last."
                ),
                code=(
                    '# Right triangle pattern\n'
                    '*\n'
                    '**\n'
                    '***\n'
                    '****\n'
                    '*****'
                ),
                pro_tip=(
                    "For symmetric patterns like diamonds, find the center line and work "
                    "outward. The top and bottom halves are usually mirror images."
                ),
            ),
        ],
        common_mistakes=[
            _mistake(
                mistake="Not accounting for spaces when trying to center text",
                fix="Draw your pattern on paper first, counting characters per line",
                code='cout << " *** " << endl;',
                fixed_code='cout << "  ***  " << endl;',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that prints a diamond pattern of asterisks. "
                "The diamond should be 5 rows tall at its center. "
                "Hint: the top half has 3 rows, the bottom half has 2 rows."
            ),
            starter_code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    // Top half\n'
                '    std::cout << "  *  " << std::endl;\n'
                '    std::cout << " *** " << std::endl;\n'
                '    // Continue the pattern\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "The diamond should be symmetric: widest at the middle (5 stars)",
                "Each line has: spaces + stars + spaces",
                "The number of stars increases by 2 each row in the top half",
                "The bottom half is the reverse of the top half",
            ],
            expected_output=(
                "  *\n"
                " ***\n"
                "*****\n"
                " ***\n"
                "  *"
            ),
        ),
        key_takeaways=[
            "Each cout statement prints one line of output",
            "Spaces control horizontal positioning",
            "Patterns often have symmetry you can exploit",
            "Plan on paper before coding",
            "Count characters carefully for alignment",
        ],
        next_steps="Great work! Now let us build something bigger: a terminal banner project.",
    ))

    _L(_add(
        lesson_id="cpp-l01-08",
        theory=(
            "In this project, you will combine everything you have learned to create a "
            "terminal banner program. A terminal banner is a large text display that appears "
            "when your program starts it might show the program name, version, and author."
            "\n\n"
            "You will use multiple cout statements, escape sequences for formatting, "
            "and ASCII art to create a professional-looking banner. This is your first "
            "real C++ program that does something useful!"
        ),
        analogy=(
            "A terminal banner is like the sign above a store. It is the first thing people "
            "see when they walk in. A good banner is welcoming, informative, and well-designed. "
            "Your program deserves a great entrance too."
        ),
        sections=[
            _section(
                heading="Design your banner",
                body=(
                    "A good banner includes: the program name in large letters, a tagline or "
                    "description, version number, author name, and a decorative border. "
                    "Use characters like =, *, -, | to create borders."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    std::cout << "================================" << std::endl;\n'
                    '    std::cout << "   WELCOME TO MY PROGRAM" << std::endl;\n'
                    '    std::cout << "   Version 1.0" << std::endl;\n'
                    '    std::cout << "   By: Alex" << std::endl;\n'
                    '    std::cout << "================================" << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Use \\t (tab) to align text in columns inside your banner. "
                    "You can also use std::setw from <iomanip> for precise alignment."
                ),
            ),
        ],
        common_mistakes=[
            _mistake(
                mistake="Having unmatched border lengths (top border longer than bottom)",
                fix="Count the characters in your border line and make them match exactly",
                code='cout << "========" << endl;\ncout << "Text" << endl;\ncout << "=====" << endl;',
                fixed_code='cout << "========" << endl;\ncout << "Text" << endl;\ncout << "========" << endl;',
            ),
        ],
        exercise=_exercise(
            description=(
                "Create a C++ program that displays a professional terminal banner. "
                "The banner must include: "
                "1) A top and bottom border using = characters, "
                "2) The program name centered with spaces, "
                "3) A short tagline, "
                "4) Version and author info, "
                "5) At least 8 lines total."
            ),
            starter_code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    // Top border\n'
                '    std::cout << "========================================" << std::endl;\n'
                '    // Name\n'
                '    std::cout << "   C++ ADVENTURES" << std::endl;\n'
                '    // Add more banner content\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Start with the top border, then content, then bottom border",
                "Use spaces to center text within the border width",
                "Add decorative elements like asterisks or dashes",
                "Use std::endl after each line",
            ],
            expected_output=(
                "========================================\n"
                "          C++ ADVENTURES\n"
                "     Learn Programming the Fun Way\n"
                "            Version 1.0\n"
                "           By: Your Name\n"
                "========================================"
            ),
        ),
        key_takeaways=[
            "Banners make programs look professional",
            "Borders and spacing create structure",
            "cout can be used for more than just printing text",
            "Planning the layout on paper helps",
            "Small projects build confidence for bigger ones",
        ],
        next_steps="Level 1 complete! You now know the basics of C++. Next: Level 2 Variables!",
    ))

    # ── C++ Level 2 ──────────────────────────────────────────────────
    _L("")
    _L("")
    _L("# ============================================================================")
    _L("# C++ LEVEL 2: VARIABLES")
    _L("# ============================================================================")
    _L("")

    _L(_add(
        lesson_id="cpp-l02-01",
        theory=(
            "C++ has a rich type system. In addition to the basic C types (int, float, double, char), "
            "C++ adds bool (true/false), std::string for text, and wchar_t for wide characters. "
            "C++ also has references (&) which are like safer pointers."
            "\n\n"
            "Every variable in C++ has a type that is fixed at compile time. Once you declare "
            "int x = 5;, x can only store integers. If you try to assign 3.14 to it, "
            "the decimal part gets truncated."
            "\n\n"
            "C++11 introduced auto, which lets the compiler deduce the type automatically. "
            "auto x = 5; makes x an int. auto y = 3.14; makes y a double. This is useful "
            "for complex types like iterators."
        ),
        analogy=(
            "Types in C++ are like different kinds of containers in a kitchen. "
            "int is like a measuring cup for whole cups. double is like a measuring spoon "
            "for precise amounts. string is like a labeled jar for storing names. "
            "bool is like a light switch: only on or off."
        ),
        sections=[
            _section(
                heading="Basic types",
                body=(
                    "Here are the most common types in C++. int for whole numbers (-2 billion to +2 billion). "
                    "double for decimal numbers (about 15 decimal digits of precision). "
                    "char for a single character (stored as a number 0-255). "
                    "bool for true/false values. std::string for text (from #include <string>)."
                ),
                code=(
                    '#include <iostream>\n'
                    '#include <string>\n'
                    '\n'
                    'int main() {\n'
                    '    int score = 95;\n'
                    '    double pi = 3.14159;\n'
                    '    char grade = \'A\';\n'
                    '    bool passed = true;\n'
                    '    std::string name = "Alex";\n'
                    '    std::cout << name << " scored " << score << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "You can use auto to let C++ figure out the type: auto x = 5; "
                    "This is especially useful for long, complex type names."
                ),
            ),
            _section(
                heading="Type sizes and ranges",
                body=(
                    "Different types use different amounts of memory. int is typically 4 bytes. "
                    "double is 8 bytes. char is 1 byte. You can check the size with sizeof(int). "
                    "Use #include <climits> for limits like INT_MAX (2,147,483,647)."
                ),
                code=(
                    '#include <iostream>\n'
                    '#include <climits>\n'
                    '\n'
                    'int main() {\n'
                    '    std::cout << "int size: " << sizeof(int) << " bytes" << std::endl;\n'
                    '    std::cout << "double size: " << sizeof(double) << " bytes" << std::endl;\n'
                    '    std::cout << "int max: " << INT_MAX << std::endl;\n'
                    '    std::cout << "int min: " << INT_MIN << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Always check your type ranges. If you exceed INT_MAX, you get integer "
                    "overflow and the value wraps around to negative! Use long long for bigger numbers."
                ),
            ),
        ],
        code_example=_code_example(
            code=(
                '#include <iostream>\n'
                '#include <string>\n'
                '\n'
                'int main() {\n'
                '    int age = 18;\n'
                '    double price = 19.99;\n'
                '    char initial = \'A\';\n'
                '    bool isStudent = true;\n'
                '    std::string city = "New York";\n'
                '    std::cout << "Age: " << age << std::endl;\n'
                '    std::cout << "Price: $" << price << std::endl;\n'
                '    std::cout << "Initial: " << initial << std::endl;\n'
                '    std::cout << "Student: " << isStudent << std::endl;\n'
                '    std::cout << "City: " << city << std::endl;\n'
                '    return 0;\n'
                '}'
            ),
            annotations=[
                _anno(1, "Include iostream for input/output"),
                _anno(2, "Include string for std::string type"),
                _anno(5, "int stores whole numbers"),
                _anno(6, "double stores decimal numbers"),
                _anno(7, "char stores a single character (note single quotes!)"),
                _anno(8, "bool stores true or false"),
                _anno(9, "std::string stores text (from <string> header)"),
            ],
        ),
        common_mistakes=[
            _mistake(
                mistake="Forgetting #include <string> before using std::string",
                fix="Always #include <string> when using std::string",
                code='std::string name = "Alex";  // missing #include <string>',
                fixed_code='#include <string>\nstd::string name = "Alex";',
            ),
            _mistake(
                mistake="Using single quotes for strings or double quotes for chars",
                fix="Double quotes for strings (multiple chars), single quotes for chars (one char)",
                code='char c = "A";\nstd::string s = \'Hello\';',
                fixed_code='char c = \'A\';\nstd::string s = "Hello";',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that declares variables of each basic type (int, double, "
                "char, bool, string), assigns them values representing a student profile, "
                "and prints them in a formatted card."
            ),
            starter_code=(
                '#include <iostream>\n'
                '#include <string>\n'
                '\n'
                'int main() {\n'
                '    // Declare variables\n'
                '    // Print them\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Use int for age, double for GPA, char for grade, bool for enrolled, string for name",
                "Print each variable with a label",
                "Try using auto for at least one variable",
            ],
            expected_output=(
                "Student Profile\n"
                "Name: Sarah\n"
                "Age: 20\n"
                "GPA: 3.75\n"
                "Grade: A\n"
                "Enrolled: 1"
            ),
        ),
        key_takeaways=[
            "C++ has basic types: int, double, char, bool, string",
            "Each type has a fixed size and range",
            "Use #include <string> for std::string",
            "auto lets the compiler deduce the type",
            "Use sizeof() to check how much memory a type uses",
        ],
        next_steps="Now let us dive deeper into declaring and using variables.",
    ))

    _L(_add(
        lesson_id="cpp-l02-02",
        theory=(
            "Variables are the heart of any program. In C++, you must declare a variable "
            "before using it. Declaration means specifying the type and a name: int score;. "
            "You can optionally initialize it at the same time: int score = 0;."
            "\n\n"
            "Variable names must start with a letter or underscore, followed by letters, "
            "digits, or underscores. They are case-sensitive (score and Score are different). "
            "Choose descriptive names like studentCount instead of sc."
            "\n\n"
            "C++11 introduced uniform initialization with curly braces: int x{5};. "
            "This is safer because it does not allow narrowing conversions "
            "(e.g., double to int without explicit cast)."
        ),
        analogy=(
            "Declaring a variable is like labeling a storage box. int score; is like taking "
            "a box and writing score on it. The box can only hold the type of items you "
            "labeled it for. int boxes hold whole numbers. string boxes hold text. "
            "int score = 95; is like putting 95 into the score box."
        ),
        sections=[
            _section(
                heading="Declaring and initializing",
                body=(
                    "You can declare and initialize in one step, or declare first and initialize "
                    "later. Uninitialized variables contain garbage values random data that was "
                    "left in memory. Always initialize your variables!"
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    int a;        // declared but NOT initialized (contains garbage)\n'
                    '    int b = 10;   // declared and initialized with =\n'
                    '    int c{20};    // declared and initialized with {} (C++11 style)\n'
                    '    int d(30);    // declared and initialized with () (old style)\n'
                    '    std::cout << b << " " << c << " " << d << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Always prefer {} initialization. It prevents narrowing: "
                    "int x{3.14}; gives a compiler error instead of silently truncating."
                ),
            ),
            _section(
                heading="Variable naming conventions",
                body=(
                    "C++ programmers typically use camelCase for variables: studentCount, "
                    "firstName, totalScore. Constants are often UPPER_CASE or start with k. "
                    "Choose names that clearly describe what the variable holds."
                ),
                code=(
                    '#include <iostream>\n'
                    '#include <string>\n'
                    '\n'
                    'int main() {\n'
                    '    int studentCount = 30;    // clear and descriptive\n'
                    '    double averageGPA = 3.5;  // camelCase is standard\n'
                    '    const int MAX_SCORE = 100; // constants in UPPER_CASE\n'
                    '    std::string firstName = "Alex";\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Avoid names like x, y, temp, data. They do not explain what the "
                    "variable represents. Code is read more often than it is written."
                ),
            ),
        ],
        code_example=_code_example(
            code=(
                '#include <iostream>\n'
                '#include <string>\n'
                '\n'
                'int main() {\n'
                '    int totalScore = 0;        // initialize to zero\n'
                '    totalScore = 95;            // assign a new value\n'
                '    totalScore = totalScore + 5; // update: now 100\n'
                '\n'
                '    std::string playerName{"Hero"}; // C++11 uniform init\n'
                '    double health{100.0};\n'
                '\n'
                '    std::cout << playerName << " has " << health << " HP" << std::endl;\n'
                '    std::cout << "Score: " << totalScore << std::endl;\n'
                '    return 0;\n'
                '}'
            ),
            annotations=[
                _anno(1, "Include iostream for input/output"),
                _anno(5, "Declaration with initialization to 0"),
                _anno(6, "Assignment: overwrites the previous value"),
                _anno(7, "Read current value, add 5, store result back"),
                _anno(9, "Uniform initialization with curly braces"),
                _anno(13, "Variables are used in expressions"),
            ],
        ),
        common_mistakes=[
            _mistake(
                mistake="Using an uninitialized variable (contains garbage data)",
                fix="Always initialize variables when you declare them",
                code='int x;\nstd::cout << x;  // prints garbage!',
                fixed_code='int x = 0;\nstd::cout << x;',
            ),
            _mistake(
                mistake="Using reserved keywords as variable names",
                fix="Avoid words like int, return, class, if, else as names",
                code='int return = 5;  // return is a keyword',
                fixed_code='int result = 5;',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that declares variables for a simple game character. "
                "Include: player name (string), health (double), level (int), isAlive (bool). "
                "Initialize them with values and print a character status report."
            ),
            starter_code=(
                '#include <iostream>\n'
                '#include <string>\n'
                '\n'
                'int main() {\n'
                '    // Declare and initialize character variables\n'
                '    // Print character stats\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Use uniform initialization {} for at least one variable",
                "Print each stat with a label",
                "Use boolalpha to print true/false instead of 1/0",
            ],
            expected_output=(
                "Character: Warrior\n"
                "Health: 100\n"
                "Level: 1\n"
                "Alive: true"
            ),
        ),
        key_takeaways=[
            "Declare variables before using them: type name;",
            "Always initialize variables to avoid garbage values",
            "Use {} initialization for safety (prevents narrowing)",
            "Choose descriptive, meaningful variable names",
            "Variables can be reassigned after declaration",
        ],
        next_steps="Now let us learn about constants values that never change.",
    ))

    _L(_add(
        lesson_id="cpp-l02-03",
        theory=(
            "Constants are variables whose value cannot change after initialization. "
            "Use the const keyword to make a variable constant. Once set, any attempt to "
            "modify it causes a compiler error."
            "\n\n"
            "C++ also has constexpr (C++11) which guarantees the value is computed at compile "
            "time, not runtime. This can make your program faster because the compiler "
            "replaces the constant with its literal value everywhere it is used."
            "\n\n"
            "Use constants for values that should never change: pi, tax rates, maximum sizes, "
            "configuration values. This makes your code safer and easier to maintain."
        ),
        analogy=(
            "A variable is like a whiteboard you can write and erase. "
            "A constant is like an engraving in stone once carved, it stays forever. "
            "If you try to change it, the compiler (like a museum guard) stops you. "
            "constexpr is like a stamp that is pressed at the factory before the stone "
            "even arrives at the museum."
        ),
        sections=[
            _section(
                heading="const vs constexpr",
                body=(
                    "const means the value cannot change after initialization. It can be "
                    "initialized with a runtime value. constexpr means the value must be "
                    "known at compile time, which allows for more optimizations."
                    "\n\nUse const for runtime values that should not change. "
                    "Use constexpr when the value can be computed during compilation."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    const double PI = 3.14159;  // runtime constant\n'
                    '    constexpr int DAYS_IN_WEEK = 7;  // compile-time constant\n'
                    '    \n'
                    '    int radius = 5;\n'
                    '    double area = PI * radius * radius;\n'
                    '    \n'
                    '    // PI = 3.0;  // ERROR! cannot modify const\n'
                    '    std::cout << "Area: " << area << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Use const by default for any variable that should not change. "
                    "It makes your intentions clear and prevents accidental modification."
                ),
            ),
            _section(
                heading="#define vs const",
                body=(
                    "C and old C++ used #define for constants: #define PI 3.14. "
                    "This is a preprocessor macro it just replaces text before compilation. "
                    "Modern C++ prefers const because it has proper type checking and scope."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    '#define OLD_PI 3.14  // old C-style, no type, just text replacement\n'
                    'const double MODERN_PI = 3.14159;  // modern C++, has a type\n'
                    '\n'
                    'int main() {\n'
                    '    std::cout << "Old: " << OLD_PI * 2 << std::endl;\n'
                    '    std::cout << "Modern: " << MODERN_PI * 2 << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Avoid #define for constants in C++. Use const or constexpr. "
                    "#define does not respect scoping or types, which can cause subtle bugs."
                ),
            ),
        ],
        code_example=_code_example(
            code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    constexpr double TAX_RATE = 0.08;  // 8% sales tax\n'
                '    constexpr int MAX_ITEMS = 10;\n'
                '    \n'
                '    double total = 0;\n'
                '    total += 9.99 + 19.99 + 4.99;\n'
                '    double tax = total * TAX_RATE;\n'
                '    \n'
                '    std::cout << "Subtotal: $" << total << std::endl;\n'
                '    std::cout << "Tax: $" << tax << std::endl;\n'
                '    std::cout << "Total: $" << total + tax << std::endl;\n'
                '    return 0;\n'
                '}'
            ),
            annotations=[
                _anno(4, "constexpr: value computed at compile time"),
                _anno(5, "MAX_ITEMS used as array size (must be compile-time constant)"),
                _anno(9, "Using const value in calculation"),
            ],
        ),
        common_mistakes=[
            _mistake(
                mistake="Trying to modify a const variable",
                fix="Use a non-const variable if the value needs to change",
                code='const int x = 5;\nx = 10;  // ERROR',
                fixed_code='int x = 5;\nx = 10;  // OK',
            ),
            _mistake(
                mistake="Using #define when const or constexpr would be better",
                fix="Use const or constexpr for type safety and scoping",
                code='#define MAX 100\n// MAX has no type, no scope',
                fixed_code='constexpr int MAX = 100;',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that calculates the area and circumference of a circle. "
                "Use a const or constexpr for PI. Read the radius as a variable. "
                "Area = PI * r * r, Circumference = 2 * PI * r."
            ),
            starter_code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    constexpr double PI = 3.14159;\n'
                '    double radius = 7.5;\n'
                '    // Calculate and print area and circumference\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "PI should be const or constexpr",
                "Area = PI * radius * radius",
                "Circumference = 2 * PI * radius",
                "Use std::fixed and std::setprecision(2) for clean output",
            ],
            expected_output=(
                "Radius: 7.5\n"
                "Area: 176.71\n"
                "Circumference: 47.12"
            ),
        ),
        key_takeaways=[
            "const prevents a variable from being modified",
            "constexpr guarantees compile-time evaluation",
            "Constants make code safer and self-documenting",
            "Prefer const over #define for constants in C++",
            "Use const by default, only use non-const when necessary",
        ],
        next_steps="Now let us explore type sizes and memory in C++.",
    ))

    _L(_add(
        lesson_id="cpp-l02-04",
        theory=(
            "Every type in C++ takes up a certain amount of memory. The sizeof operator "
            "tells you how many bytes a type or variable uses. The actual sizes can vary "
            "by platform, but here are the typical values."
            "\n\n"
            "On most modern systems: int is 4 bytes (32 bits), double is 8 bytes (64 bits), "
            "char is 1 byte (8 bits), bool is 1 byte, float is 4 bytes. "
            "A byte is 8 bits, and a bit stores a single 0 or 1."
            "\n\n"
            "The <climits> and <cfloat> headers define the minimum and maximum values "
            "for each type, like INT_MAX, INT_MIN, DBL_MAX, etc."
        ),
        analogy=(
            "Memory in a computer is like a giant apartment building. Each byte is one "
            "apartment. A char lives in a studio apartment (1 byte). An int lives in a "
            "one-bedroom (4 bytes). A double lives in a penthouse (8 bytes). "
            "The sizeof operator is like asking the building manager: how big is the apartment?"
        ),
        sections=[
            _section(
                heading="sizeof in action",
                body=(
                    "Use sizeof(type) or sizeof(variable) to check sizes. "
                    "The result is of type size_t, which is an unsigned integer."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    std::cout << "char: " << sizeof(char) << " byte" << std::endl;\n'
                    '    std::cout << "int: " << sizeof(int) << " bytes" << std::endl;\n'
                    '    std::cout << "float: " << sizeof(float) << " bytes" << std::endl;\n'
                    '    std::cout << "double: " << sizeof(double) << " bytes" << std::endl;\n'
                    '    std::cout << "bool: " << sizeof(bool) << " byte" << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "sizeof is evaluated at compile time, so it has zero runtime cost. "
                    "Use it to write portable code that adapts to different platforms."
                ),
            ),
            _section(
                heading="Fixed-width types (C++11)",
                body=(
                    "If you need exact sizes, use fixed-width types from <cstdint>: "
                    "int32_t (exactly 4 bytes), int64_t (exactly 8 bytes), "
                    "uint32_t (unsigned 4 bytes). These are guaranteed to be the same "
                    "size on every platform."
                ),
                code=(
                    '#include <iostream>\n'
                    '#include <cstdint>\n'
                    '\n'
                    'int main() {\n'
                    '    int32_t exact32 = 100;  // exactly 32 bits (4 bytes)\n'
                    '    int64_t exact64 = 100;  // exactly 64 bits (8 bytes)\n'
                    '    uint32_t positive = 100; // unsigned, only positive\n'
                    '    std::cout << "int32_t: " << sizeof(exact32) << " bytes" << std::endl;\n'
                    '    std::cout << "int64_t: " << sizeof(exact64) << " bytes" << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Use fixed-width types when working with binary data, network protocols, "
                    "or when memory layout must be predictable across platforms."
                ),
            ),
        ],
        code_example=_code_example(
            code=(
                '#include <iostream>\n'
                '#include <climits>\n'
                '#include <cfloat>\n'
                '\n'
                'int main() {\n'
                '    std::cout << "int range: " << INT_MIN << " to " << INT_MAX << std::endl;\n'
                '    std::cout << "double range: " << DBL_MIN << " to " << DBL_MAX << std::endl;\n'
                '    std::cout << "int size: " << sizeof(int) << " bytes" << std::endl;\n'
                '    \n'
                '    long long big = 9223372036854775807LL;\n'
                '    std::cout << "long long: " << sizeof(long long) << " bytes" << std::endl;\n'
                '    std::cout << "Max long long: " << LLONG_MAX << std::endl;\n'
                '    return 0;\n'
                '}'
            ),
            annotations=[
                _anno(6, "INT_MIN and INT_MAX from <climits>"),
                _anno(7, "DBL_MIN and DBL_MAX from <cfloat>"),
                _anno(8, "sizeof returns the size in bytes at compile time"),
                _anno(10, "long long can hold very large integers"),
                _anno(11, "long long is typically 8 bytes (64 bits)"),
            ],
        ),
        common_mistakes=[
            _mistake(
                mistake="Assuming type sizes are the same on all platforms",
                fix="Use sizeof() to check, or use fixed-width types from <cstdint>",
                code='// assumes int is 4 bytes, might not be on all platforms',
                fixed_code='int32_t x = 100;  // guaranteed 4 bytes everywhere',
            ),
            _mistake(
                mistake="Overflowing an integer (exceeding its maximum value)",
                fix="Use a larger type or check for overflow before operations",
                code='int x = 2147483647;\nx = x + 1;  // overflow! becomes -2147483648',
                fixed_code='int64_t x = 2147483647;\nx = x + 1;  // safe',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that uses sizeof to print the sizes of char, int, "
                "float, double, bool, and long long. Then calculate how many of each type "
                "would fit in 1 kilobyte (1024 bytes)."
            ),
            starter_code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    // Print sizes\n'
                '    // Calculate how many fit in 1 KB\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "sizeof returns bytes; 1 KB = 1024 bytes",
                "Use 1024 / sizeof(type) to calculate how many fit",
                "Print the result as an integer",
            ],
            expected_output=(
                "char: 1 byte, 1024 fit in 1KB\n"
                "int: 4 bytes, 256 fit in 1KB\n"
                "double: 8 bytes, 128 fit in 1KB"
            ),
        ),
        key_takeaways=[
            "Use sizeof() to check how many bytes a type uses",
            "Type sizes can vary by platform",
            "Fixed-width types (int32_t) guarantee exact sizes",
            "Integer overflow happens silently, be careful!",
            "<climits> and <cfloat> provide min/max values for types",
        ],
        next_steps="Now let us learn how to get input from the user.",
    ))

    _L(_add(
        lesson_id="cpp-l02-05",
        theory=(
            "Getting user input in C++ is done with cin (pronounced see-in). "
            "It works like the opposite of cout: instead of <<, you use >> (extraction operator). "
            "cin >> variable reads a value from the keyboard and stores it in the variable."
            "\n\n"
            "cin automatically handles different types. If you read into an int, "
            "it expects digits. If you read into a string, it reads a word "
            "(stopping at the first space)."
            "\n\n"
            "cin leaves the newline character in the input buffer after reading, "
            "which can cause issues when mixing >> with getline(). "
            "Use cin.ignore() to clear the buffer between them."
        ),
        analogy=(
            "cin is like a receiving dock at a warehouse. The >> operator is a forklift "
            "that takes items from the dock and puts them into labeled storage bins. "
            "If you tell the forklift to put items into an int bin, it only accepts numbers. "
            "If you give it text, it leaves them on the dock."
        ),
        sections=[
            _section(
                heading="Reading different types",
                body=(
                    "cin >> intVariable reads an integer. cin >> doubleVariable reads a decimal. "
                    "cin >> stringVariable reads one word. For reading a whole line including "
                    "spaces, use getline(cin, stringVariable)."
                ),
                code=(
                    '#include <iostream>\n'
                    '#include <string>\n'
                    '\n'
                    'int main() {\n'
                    '    int age;\n'
                    '    double height;\n'
                    '    std::string name;\n'
                    '    \n'
                    '    std::cout << "Enter your name: ";\n'
                    '    std::getline(std::cin, name);\n'
                    '    \n'
                    '    std::cout << "Enter your age: ";\n'
                    '    std::cin >> age;\n'
                    '    \n'
                    '    std::cout << "Enter your height: ";\n'
                    '    std::cin >> height;\n'
                    '    \n'
                    '    std::cout << "Hello " << name << "!" << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "After cin >> age, there is still a newline in the buffer. "
                    "If you use getline after >>, you need cin.ignore() first."
                ),
            ),
        ],
        code_example=_code_example(
            code=(
                '#include <iostream>\n'
                '#include <string>\n'
                '\n'
                'int main() {\n'
                '    int a, b;\n'
                '    std::cout << "Enter two numbers: ";\n'
                '    std::cin >> a >> b;  // read two ints separated by space\n'
                '    std::cout << "Sum: " << a + b << std::endl;\n'
                '    \n'
                '    std::cin.ignore();  // clear newline from buffer\n'
                '    \n'
                '    std::string line;\n'
                '    std::cout << "Enter a sentence: ";\n'
                '    std::getline(std::cin, line);\n'
                '    std::cout << "You wrote: " << line << std::endl;\n'
                '    return 0;\n'
                '}'
            ),
            annotations=[
                _anno(5, "Two int variables declared together (comma-separated)"),
                _anno(7, "Read two integers in one line, separated by space"),
                _anno(10, "Clear the leftover newline before getline"),
                _anno(14, "getline reads the entire line including spaces"),
            ],
        ),
        common_mistakes=[
            _mistake(
                mistake="Using cin >> after getline without cin.ignore()",
                fix="Use cin.ignore() between >> and getline, or vice versa",
                code='cin >> age;\ngetline(cin, name);  // name will be empty!',
                fixed_code='cin >> age;\ncin.ignore();\ngetline(cin, name);',
            ),
            _mistake(
                mistake="Reading a string with >> and losing text after spaces",
                fix="Use getline(cin, string) to read text with spaces",
                code='std::cin >> fullName;  // only reads "John" from "John Doe"',
                fixed_code='std::getline(std::cin, fullName);  // reads "John Doe"',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that asks the user for their name (full name with spaces), "
                "age, and favorite number. Then print a summary. Use getline for the name "
                "and cin >> for the numbers."
            ),
            starter_code=(
                '#include <iostream>\n'
                '#include <string>\n'
                '\n'
                'int main() {\n'
                '    // Declare variables\n'
                '    // Get user input\n'
                '    // Print summary\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Use getline for name, cin >> for age and favorite number",
                "Remember cin.ignore() after >> if mixing with getline",
                "Print all the information in a formatted summary",
            ],
            expected_output=(
                "Enter your name: John Doe\n"
                "Enter your age: 20\n"
                "Enter your favorite number: 7\n"
                "\n"
                "--- Profile ---\n"
                "Name: John Doe\n"
                "Age: 20\n"
                "Favorite Number: 7"
            ),
        ),
        key_takeaways=[
            "cin >> reads input into variables, >> is the extraction operator",
            "cin >> reads one word for strings (stops at space)",
            "getline(cin, str) reads a whole line including spaces",
            "Mix >> and getline carefully: use cin.ignore() between them",
            "cin automatically converts input to the target variable type",
        ],
        next_steps="Now let us learn about type conversion between different types.",
    ))

    _L(_add(
        lesson_id="cpp-l02-06",
        theory=(
            "Sometimes you need to convert a value from one type to another. C++ has two "
            "kinds of type conversion: implicit (automatic) and explicit (you ask for it)."
            "\n\n"
            "Implicit conversion happens when you assign a value to a variable of a "
            "different type. For example, double d = 5; converts the int 5 to 5.0. "
            "This is called promotion (smaller type to larger)."
            "\n\n"
            "The reverse (double to int) is called demotion or narrowing. "
            "C++ will warn you because you lose the decimal part. "
            "int i = 3.14; gives i = 3, dropping the .14. "
            "Use static_cast<double>(x) or static_cast<int>(y) for explicit conversion."
        ),
        analogy=(
            "Type conversion is like moving between differently sized measuring cups. "
            "Pouring from a cup into a larger cup (int to double) always works, "
            "you just have more room. Pouring from a larger cup into a smaller one "
            "(double to int) spills the extra liquid (the decimal part is lost). "
            "static_cast is like using a funnel you control exactly what gets transferred."
        ),
        sections=[
            _section(
                heading="Implicit vs explicit conversion",
                body=(
                    "Implicit conversion is automatic but can lose data. "
                    "Explicit conversion with static_cast tells the compiler you know "
                    "what you are doing and the loss of data is intentional."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    double d = 5;  // implicit: int 5 becomes double 5.0\n'
                    '    int i = 3.99;  // implicit: double 3.99 becomes int 3 (truncated!)\n'
                    '    \n'
                    '    double pi = 3.14159;\n'
                    '    int truncated = static_cast<int>(pi);  // explicit: 3\n'
                    '    \n'
                    '    std::cout << "d: " << d << std::endl;\n'
                    '    std::cout << "i: " << i << std::endl;\n'
                    '    std::cout << "truncated: " << truncated << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Always use static_cast for explicit conversions. "
                    "Avoid the C-style (int)x cast it is harder to find in code searches."
                ),
            ),
            _section(
                heading="Common conversions",
                body=(
                    "int to double: automatic promotion, safe. "
                    "double to int: truncates decimals, loses data. "
                    "int to char: takes the character with that ASCII code. "
                    "string to int: use std::stoi(str) from <string>. "
                    "int to string: use std::to_string(num) from <string>."
                ),
                code=(
                    '#include <iostream>\n'
                    '#include <string>\n'
                    '\n'
                    'int main() {\n'
                    '    std::string numStr = "42";\n'
                    '    int num = std::stoi(numStr);  // string to int\n'
                    '    \n'
                    '    std::string text = std::to_string(123);  // int to string\n'
                    '    \n'
                    '    std::cout << "Parsed: " << num << std::endl;\n'
                    '    std::cout << "String: " << text << std::endl;\n'
                    '    \n'
                    '    char c = static_cast<char>(65);  // int to char: 65 = \'A\'\n'
                    '    std::cout << "Char 65: " << c << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Use std::stoi, std::stod, std::stoll for string-to-number conversions. "
                    "They throw exceptions if the string is not a valid number."
                ),
            ),
        ],
        code_example=_code_example(
            code=(
                '#include <iostream>\n'
                '#include <string>\n'
                '\n'
                'int main() {\n'
                '    int apples = 10;\n'
                '    double pricePerApple = 0.75;\n'
                '    \n'
                '    // Implicit: int promoted to double for multiplication\n'
                '    double total = apples * pricePerApple;\n'
                '    \n'
                '    // Explicit: double to int (truncates)\n'
                '    int rounded = static_cast<int>(total);\n'
                '    \n'
                '    // Convert number to string for display\n'
                '    std::string message = "Total: $" + std::to_string(total);\n'
                '    \n'
                '    std::cout << message << std::endl;\n'
                '    std::cout << "Rounded: " << rounded << std::endl;\n'
                '    return 0;\n'
                '}'
            ),
            annotations=[
                _anno(8, "int * double: C++ promotes int to double automatically"),
                _anno(11, "static_cast<int>(double) truncates, does not round"),
                _anno(14, "std::to_string converts any number to a string"),
            ],
        ),
        common_mistakes=[
            _mistake(
                mistake="Assuming static_cast rounds instead of truncating",
                fix="static_cast<int>(3.99) gives 3, not 4. Add 0.5 first if you want rounding",
                code='int x = static_cast<int>(3.99);  // x = 3',
                fixed_code='int x = static_cast<int>(3.99 + 0.5);  // x = 4 (rounding)',
            ),
            _mistake(
                mistake="Passing invalid string to stoi (crashes the program)",
                fix="Use try-catch around stoi, or check the string first",
                code='int x = std::stoi("abc");  // throws std::invalid_argument',
                fixed_code='try { int x = std::stoi("abc"); } catch (...) { /* handle error */ }',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that asks the user for a decimal number, converts it to "
                "an integer (truncating), and also converts an integer the user enters to a "
                "string. Print all the results."
            ),
            starter_code=(
                '#include <iostream>\n'
                '#include <string>\n'
                '\n'
                'int main() {\n'
                '    // Get a decimal from the user\n'
                '    // Convert to int and print both\n'
                '    // Get an int and convert to string\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Use static_cast<int>(decimalValue) for truncation",
                "Use std::to_string(intValue) for int-to-string",
                "Print the original and converted values so the user can compare",
            ],
            expected_output=(
                "Enter a decimal number: 7.89\n"
                "Original: 7.89\n"
                "Truncated to int: 7\n"
                "\n"
                "Enter an integer: 42\n"
                'As string: "42"'
            ),
        ),
        key_takeaways=[
            "Implicit conversion happens automatically (int to double is safe)",
            "Narrowing conversion (double to int) loses data truncates decimals",
            "Use static_cast<Type>(value) for explicit conversion",
            "std::stoi and std::to_string convert between strings and numbers",
            "static_cast truncates toward zero, it does not round",
        ],
        next_steps="Now let us practice with a real project: Temperature Converter!",
    ))

    _L(_add(
        lesson_id="cpp-l02-07",
        theory=(
            "In this practice session, you will combine variables, user input, and type "
            "conversion to build a temperature converter. Your program will ask the user "
            "for a temperature in Celsius and convert it to Fahrenheit."
            "\n\n"
            "The formula is: F = (C * 9/5) + 32. Notice that 9/5 in C++ is 1 (integer "
            "division), so use 9.0/5.0 or static_cast<double>() to get the correct result."
        ),
        analogy=(
            "A temperature converter is like a currency exchange booth. "
            "You give it Celsius and it gives you Fahrenheit, applying a conversion rate. "
            "Just like exchange rates, the formula never changes, but the input determines "
            "the output."
        ),
        sections=[
            _section(
                heading="The conversion formula",
                body=(
                    "The formula F = (C * 9/5) + 32 is straightforward, but in C++ you must "
                    "be careful about integer division. 9/5 in C++ is 1 (both are ints). "
                    "Use 9.0/5.0 to get 1.8, or multiply C by 9 first then divide by 5."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    double celsius, fahrenheit;\n'
                    '    \n'
                    '    std::cout << "Enter temperature in Celsius: ";\n'
                    '    std::cin >> celsius;\n'
                    '    \n'
                    '    fahrenheit = (celsius * 9.0 / 5.0) + 32.0;\n'
                    '    \n'
                    '    std::cout << celsius << "C = " << fahrenheit << "F" << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Write the formula as (celsius * 9.0 / 5.0) + 32.0. "
                    "The .0 forces floating-point division so you do not lose precision."
                ),
            ),
        ],
        common_mistakes=[
            _mistake(
                mistake="Using 9/5 instead of 9.0/5.0 (integer division truncates to 1)",
                fix="Make at least one operand a double: 9.0/5, 9/5.0, or 9.0/5.0",
                code='double f = (c * 9/5) + 32;  // 9/5 = 1, wrong!',
                fixed_code='double f = (c * 9.0 / 5.0) + 32.0;',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that converts temperature from Celsius to Fahrenheit "
                "AND from Fahrenheit to Celsius. Ask the user which conversion they want. "
                "Formula for F to C: C = (F - 32) * 5/9."
            ),
            starter_code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    int choice;\n'
                '    double temp, result;\n'
                '    \n'
                '    std::cout << "1. Celsius to Fahrenheit" << std::endl;\n'
                '    std::cout << "2. Fahrenheit to Celsius" << std::endl;\n'
                '    std::cout << "Choose (1 or 2): ";\n'
                '    std::cin >> choice;\n'
                '    \n'
                '    // Implement conversions\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Use if/else to handle choice 1 vs choice 2",
                "Use 9.0/5.0 and 5.0/9.0 to avoid integer division",
                "Format output to 1 decimal place with setprecision",
            ],
            expected_output=(
                "1. Celsius to Fahrenheit\n"
                "2. Fahrenheit to Celsius\n"
                "Choose (1 or 2): 1\n"
                "Enter temperature: 100\n"
                "100.0C = 212.0F"
            ),
        ),
        key_takeaways=[
            "Use 9.0/5.0 for floating-point division, not 9/5",
            "Variables store user input for processing",
            "Formulas combine multiple operators",
            "Always test your conversion with known values (0C = 32F, 100C = 212F)",
            "Format output for readability",
        ],
        next_steps="Now let us try a challenge: swapping variable values.",
    ))

    _L(_add(
        lesson_id="cpp-l02-08",
        theory=(
            "Swapping two values is a classic programming challenge. The goal is to exchange "
            "the values of two variables. If a = 5 and b = 10, after swapping a = 10 and b = 5."
            "\n\n"
            "The standard approach uses a temporary variable. But C++ also has std::swap() "
            "from the <utility> header that does it for you. Try solving it both ways!"
        ),
        analogy=(
            "Swapping variables is like switching two drinks between cups. "
            "You pour the first drink into a third temporary cup (temp = a), "
            "pour the second drink into the first cup (a = b), "
            "then pour from the temporary cup into the second cup (b = temp)."
        ),
        sections=[
            _section(
                heading="Swap with a temporary variable",
                body=(
                    "The classic three-step swap: temp = a; a = b; b = temp; "
                    "It is simple, clear, and works for any type."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    int a = 5, b = 10;\n'
                    '    \n'
                    '    std::cout << "Before: a = " << a << ", b = " << b << std::endl;\n'
                    '    \n'
                    '    int temp = a;\n'
                    '    a = b;\n'
                    '    b = temp;\n'
                    '    \n'
                    '    std::cout << "After: a = " << a << ", b = " << b << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "C++ has std::swap(a, b) in <utility> that does this for you. "
                    "It is optimized and works with any type."
                ),
            ),
        ],
        common_mistakes=[
            _mistake(
                mistake="Trying to swap without a temp variable by doing a = b; b = a;",
                fix="After a = b, the original value of a is lost. Always use a temp variable.",
                code='a = b;\nb = a;  // both end up with b\'s original value',
                fixed_code='temp = a;\na = b;\nb = temp;',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that swaps two numbers entered by the user. "
                "First, swap using a temporary variable. Then, try the same with std::swap. "
                "Print the values before and after swapping."
            ),
            starter_code=(
                '#include <iostream>\n'
                '#include <utility>  // for std::swap\n'
                '\n'
                'int main() {\n'
                '    int x, y;\n'
                '    std::cout << "Enter two numbers: ";\n'
                '    std::cin >> x >> y;\n'
                '    // Swap and print\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Store the original values before swapping to print both before and after",
                "Use std::swap(x, y) for the second approach",
                "Print x and y after swapping to verify it worked",
            ],
            expected_output=(
                "Enter two numbers: 7 42\n"
                "Before swap: x = 7, y = 42\n"
                "After swap: x = 42, y = 7"
            ),
        ),
        key_takeaways=[
            "Swapping needs a temporary variable to hold one value",
            "temp = a; a = b; b = temp; is the standard three-step swap",
            "C++ provides std::swap() in <utility>",
            "Without temp, you lose the original value",
            "Swapping works for any variable type, not just integers",
        ],
        next_steps="Now let us build a calculator project!",
    ))

    _L(_add(
        lesson_id="cpp-l02-09",
        theory=(
            "This project will bring together everything from Level 2: variables, types, "
            "user input, constants, and type conversion. You will build a simple calculator "
            "that can add, subtract, multiply, and divide two numbers."
            "\n\n"
            "The calculator will: ask the user for two numbers, ask which operation to perform, "
            "compute the result, and display it. This is a real program that does something "
            "useful it is your first tool-building project!"
        ),
        analogy=(
            "Building a calculator is like being a toolmaker. You are not just using "
            "a calculator you are creating one. Every time someone uses your program, "
            "they are using something you built from scratch."
        ),
        sections=[
            _section(
                heading="Calculator structure",
                body=(
                    "Your calculator will have three parts: input (get two numbers and operation), "
                    "processing (perform the calculation), and output (display the result). "
                    "Use different variables for each number and the result. Handle division "
                    "by zero as a special case."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    double a, b, result;\n'
                    '    char op;\n'
                    '    \n'
                    '    std::cout << "Enter first number: ";\n'
                    '    std::cin >> a;\n'
                    '    std::cout << "Enter operator (+, -, *, /): ";\n'
                    '    std::cin >> op;\n'
                    '    std::cout << "Enter second number: ";\n'
                    '    std::cin >> b;\n'
                    '    \n'
                    '    // Calculate based on op\n'
                    '    if (op == \'+\') result = a + b;\n'
                    '    else if (op == \'-\') result = a - b;\n'
                    '    else if (op == \'*\') result = a * b;\n'
                    '    else if (op == \'/\') result = a / b;\n'
                    '    \n'
                    '    std::cout << a << " " << op << " " << b << " = " << result;\n'
                    '    std::cout << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Always check for division by zero. In C++, dividing by zero "
                    "crashes your program. Add an if check before dividing."
                ),
            ),
        ],
        common_mistakes=[
            _mistake(
                mistake="Not handling division by zero (program crashes)",
                fix="Check if b == 0 before dividing and show an error message",
                code='result = a / b;  // crashes if b is 0',
                fixed_code='if (b != 0) result = a / b;\nelse std::cout << "Cannot divide by zero!";',
            ),
        ],
        exercise=_exercise(
            description=(
                "Build a complete calculator program in C++ that: "
                "1) Asks for two numbers (double), "
                "2) Asks for an operation (+, -, *, /), "
                "3) Computes and displays the result, "
                "4) Handles division by zero gracefully."
            ),
            starter_code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    double num1, num2, result;\n'
                '    char op;\n'
                '    \n'
                '    std::cout << "=== Simple Calculator ===" << std::endl;\n'
                '    // Get inputs\n'
                '    // Perform calculation\n'
                '    // Display result\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Use if/else if to check which operation was chosen",
                "Use double for all numbers so division works correctly",
                "Check for division by zero before performing division",
                "Format output neatly with the equation shown",
            ],
            expected_output=(
                "=== Simple Calculator ===\n"
                "Enter first number: 10\n"
                "Enter operator (+, -, *, /): /\n"
                "Enter second number: 3\n"
                "10 / 3 = 3.33333"
            ),
        ),
        key_takeaways=[
            "A program has three phases: input, processing, output",
            "Use different variables for different pieces of data",
            "Always validate input (like division by zero checks)",
            "Characters can be read with cin >> charVariable",
            "Level 2 complete you understand variables!",
        ],
        next_steps="Level 2 complete! You now understand C++ variables. Next: Level 3 Operators!",
    ))

    # ── C++ Level 3 ──────────────────────────────────────────────────
    _L("")
    _L("")
    _L("# ============================================================================")
    _L("# C++ LEVEL 3: OPERATORS")
    _L("# ============================================================================")
    _L("")

    _L(_add(
        lesson_id="cpp-l03-01",
        theory=(
            "Operators are symbols that perform operations on values. The most familiar "
            "are arithmetic operators: +, -, *, /, and %. They work mostly like math "
            "class, with some C++-specific behavior."
            "\n\n"
            "The modulo operator % gives the remainder of division. 10 % 3 = 1 "
            "(10 divided by 3 is 3 remainder 1). It only works with integers. "
            "For double, use std::fmod() from <cmath>."
            "\n\n"
            "C++ also has increment (++) and decrement (--) operators that add or "
            "subtract 1. They come in prefix (++x) and postfix (x++) forms."
        ),
        analogy=(
            "Operators are like kitchen appliances. + is like combining two bowls of ingredients. "
            "- is like removing some. * is like scaling a recipe up. / is like splitting evenly. "
            "% is like figuring out what is left after sharing cookies among friends. "
            "++ is like adding one more chocolate chip."
        ),
        sections=[
            _section(
                heading="Basic arithmetic",
                body=(
                    "Addition (+), subtraction (-), multiplication (*), division (/), "
                    "and modulo (%). Remember: integer division truncates. 7/2 = 3, not 3.5. "
                    "Use doubles if you need decimal results."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    int a = 17, b = 5;\n'
                    '    std::cout << "a + b = " << (a + b) << std::endl;\n'
                    '    std::cout << "a - b = " << (a - b) << std::endl;\n'
                    '    std::cout << "a * b = " << (a * b) << std::endl;\n'
                    '    std::cout << "a / b = " << (a / b) << std::endl;  // 3, not 3.4\n'
                    '    std::cout << "a % b = " << (a % b) << std::endl;  // 2\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Watch out for integer overflow. Adding two large ints can exceed INT_MAX. "
                    "Use long long for large numbers."
                ),
            ),
            _section(
                heading="Increment and decrement",
                body=(
                    "++x increments x then returns the new value (prefix). "
                    "x++ returns the original value then increments (postfix). "
                    "Use prefix form when possible it is slightly faster for complex types."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    int x = 5, y = 5;\n'
                    '    std::cout << "Prefix ++x: " << ++x << std::endl;  // 6\n'
                    '    std::cout << "x after: " << x << std::endl;        // 6\n'
                    '    std::cout << "Postfix y++: " << y++ << std::endl;  // 5\n'
                    '    std::cout << "y after: " << y << std::endl;        // 6\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "The difference between ++x and x++ matters in complex expressions. "
                    "When in doubt, use the standalone form: x++; or ++x; by itself."
                ),
            ),
        ],
        code_example=_code_example(
            code=(
                '#include <iostream>\n'
                '#include <cmath>\n'
                '\n'
                'int main() {\n'
                '    double a = 10.0, b = 3.0;\n'
                '    std::cout << "10 / 3 = " << a / b << std::endl;\n'
                '    std::cout << "Remainder: " << std::fmod(a, b) << std::endl;\n'
                '    \n'
                '    int count = 0;\n'
                '    count = count + 1;  // long form\n'
                '    count += 1;          // compound assignment\n'
                '    count++;             // increment operator\n'
                '    std::cout << "Count: " << count << std::endl;\n'
                '    return 0;\n'
                '}'
            ),
            annotations=[
                _anno(2, "Include cmath for std::fmod (floating-point modulo)"),
                _anno(6, "Floating-point division gives the expected 3.333..."),
                _anno(7, "std::fmod gives remainder for doubles"),
                _anno(10, "Long form addition"),
                _anno(11, "Compound assignment (add and assign)"),
                _anno(12, "Increment operator (add 1)"),
            ],
        ),
        common_mistakes=[
            _mistake(
                mistake="Confusing = (assignment) with == (comparison)",
                fix="Use = to set a value, == to check equality",
                code='if (x = 5)  // always true! assigns 5 to x',
                fixed_code='if (x == 5)  // checks if x equals 5',
            ),
            _mistake(
                mistake="Using % with double values (it only works with ints)",
                fix="Use std::fmod() from <cmath> for floating-point remainder",
                code='double r = 10.5 % 3.0;  // ERROR!',
                fixed_code='double r = std::fmod(10.5, 3.0);',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that asks the user for two integers and prints: "
                "sum, difference, product, quotient, and remainder. Also demonstrate "
                "the difference between prefix and postfix increment."
            ),
            starter_code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    int x, y;\n'
                '    std::cout << "Enter two integers: ";\n'
                '    std::cin >> x >> y;\n'
                '    // Calculate and print results\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Store results in variables or compute inline in cout",
                "For quotient, remember integer division truncates",
                "Use (x++) vs (++x) in separate cout statements to show the difference",
            ],
            expected_output=(
                "Enter two integers: 17 5\n"
                "17 + 5 = 22\n"
                "17 - 5 = 12\n"
                "17 * 5 = 85\n"
                "17 / 5 = 3\n"
                "17 % 5 = 2"
            ),
        ),
        key_takeaways=[
            "Arithmetic operators: +, -, *, /, %",
            "% (modulo) gives remainder, works only with integers",
            "Integer division truncates; use double for decimal results",
            "++x (prefix) and x++ (postfix) differ in return value",
            "Compound assignment: x += 5 is short for x = x + 5",
        ],
        next_steps="Now let us learn about comparison operators.",
    ))

    _L(_add(
        lesson_id="cpp-l03-02",
        theory=(
            "Comparison operators compare two values and return a bool (true or false). "
            "They are essential for making decisions in your programs with if statements."
            "\n\n"
            "C++ has: == (equal to), != (not equal to), < (less than), > (greater than), "
            "<= (less than or equal to), >= (greater than or equal to)."
            "\n\n"
            "A common pitfall: = is assignment, == is comparison. if (x = 5) assigns 5 to x "
            "and then checks if x is truthy (nonzero), which is always true. This is one of "
            "the most common bugs in C and C++."
        ),
        analogy=(
            "Comparison operators are like a referee at a sports match. "
            "== checks if the scores are exactly equal. != checks if they are different. "
            "< and > check which team is ahead. The referee always gives a yes/no answer "
            "(true/false). No maybes."
        ),
        sections=[
            _section(
                heading="Comparing values",
                body=(
                    "Each comparison returns a bool. You can store the result in a bool variable "
                    "or use it directly in an if statement."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    int a = 10, b = 20;\n'
                    '    \n'
                    '    std::cout << "a == b: " << (a == b) << std::endl;  // 0 (false)\n'
                    '    std::cout << "a != b: " << (a != b) << std::endl;  // 1 (true)\n'
                    '    std::cout << "a < b:  " << (a < b)  << std::endl;  // 1 (true)\n'
                    '    std::cout << "a > b:  " << (a > b)  << std::endl;  // 0 (false)\n'
                    '    \n'
                    '    bool result = (a + 10 == b);  // true, because 20 == 20\n'
                    '    std::cout << "a + 10 == b: " << result << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "cout prints bool values as 0 or 1 by default. Use "
                    "std::boolalpha to print true/false instead."
                ),
            ),
        ],
        common_mistakes=[
            _mistake(
                mistake="Using = instead of == in conditions",
                fix="Use == for comparison, = for assignment. Write constant on left: 5 == x",
                code='if (x = 5) { }  // always true, and modifies x!',
                fixed_code='if (x == 5) { }',
            ),
            _mistake(
                mistake="Comparing floating-point numbers with == (precision issues)",
                fix="Check if the difference is very small: abs(a - b) < 0.0001",
                code='if (0.1 + 0.2 == 0.3)  // might be false due to rounding!',
                fixed_code='if (abs((0.1 + 0.2) - 0.3) < 0.0001)',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that asks the user for two numbers and uses all six "
                "comparison operators to compare them. Print each comparison and its result "
                "using std::boolalpha for nice true/false output."
            ),
            starter_code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    double x, y;\n'
                '    std::cout << "Enter two numbers: ";\n'
                '    std::cin >> x >> y;\n'
                '    \n'
                '    std::cout << std::boolalpha;\n'
                '    // Compare x and y with all 6 operators\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Enable std::boolalpha once at the top for nice output",
                "Use if/else or just print the expression directly",
                "Test with equal numbers, different numbers, and edge cases",
            ],
            expected_output=(
                "Enter two numbers: 10 20\n"
                "10 == 20: false\n"
                "10 != 20: true\n"
                "10 < 20: true\n"
                "10 > 20: false\n"
                "10 <= 20: true\n"
                "10 >= 20: false"
            ),
        ),
        key_takeaways=[
            "Comparison operators return bool: true or false",
            "== checks equality, = assigns a value (do not mix them up!)",
            "<, >, <=, >= work with any numeric type",
            "Use std::boolalpha to print bool as true/false",
            "Avoid == with floating-point numbers due to precision issues",
        ],
        next_steps="Now let us learn about logical operators: and, or, not.",
    ))

    _L(_add(
        lesson_id="cpp-l03-03",
        theory=(
            "Logical operators combine multiple conditions into one. C++ has: "
            "&& (AND both must be true), || (OR at least one must be true), "
            "and ! (NOT reverses true/false)."
            "\n\n"
            "C++ also supports writing them as words: and, or, not (C++98 and later). "
            "These are especially useful when you want your code to be more readable."
            "\n\n"
            "Short-circuit evaluation: in expr1 && expr2, if expr1 is false, expr2 is "
            "never evaluated. Similarly, in expr1 || expr2, if expr1 is true, expr2 is "
            "never evaluated. This can prevent errors when the second expression depends "
            "on the first being true (like checking pointer != nullptr before using it)."
        ),
        analogy=(
            "Logical operators are like bouncers at a club. "
            "&& (AND) checks both conditions: are you on the list AND over 21? "
            "|| (OR) checks: do you have a VIP pass OR know the owner? "
            "! (NOT) reverses: if you are NOT on the list, you do not get in. "
            "Short-circuit evaluation is like the bouncer checking the easiest condition first."
        ),
        sections=[
            _section(
                heading="AND, OR, NOT",
                body=(
                    "&& requires both sides to be true. || requires at least one side to be true. "
                    "! flips true to false and vice versa."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    bool hasKey = true;\n'
                    '    bool knowsCode = false;\n'
                    '    \n'
                    '    std::cout << std::boolalpha;\n'
                    '    std::cout << "AND: " << (hasKey && knowsCode) << std::endl;  // false\n'
                    '    std::cout << "OR:  " << (hasKey || knowsCode) << std::endl;  // true\n'
                    '    std::cout << "NOT: " << (!hasKey) << std::endl;              // false\n'
                    '    \n'
                    '    int age = 20;\n'
                    '    bool canDrive = (age >= 16) && (age <= 75);\n'
                    '    std::cout << "Can drive: " << canDrive << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Use parentheses to make the order of operations clear. "
                    "Even if you know precedence, other readers might not."
                ),
            ),
        ],
        code_example=_code_example(
            code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    int score = 85;\n'
                '    bool hasBonus = true;\n'
                '    \n'
                '    // Both conditions must be true\n'
                '    if (score >= 50 && hasBonus) {\n'
                '        std::cout << "You passed with bonus!" << std::endl;\n'
                '    }\n'
                '    \n'
                '    int divisor = 0;\n'
                '    // Short-circuit saves: divisor != 0 is false, so division is skipped\n'
                '    if (divisor != 0 && 100 / divisor > 5) {\n'
                '        std::cout << "Result > 5" << std::endl;\n'
                '    } else {\n'
                '        std::cout << "Cannot divide by zero" << std::endl;\n'
                '    }\n'
                '    return 0;\n'
                '}'
            ),
            annotations=[
                _anno(8, "Both conditions must be true for the if to execute"),
                _anno(13, "Short-circuit prevents division by zero!"),
                _anno(14, "divisor != 0 is false, so 100/divisor is never computed"),
            ],
        ),
        common_mistakes=[
            _mistake(
                mistake="Using & or | instead of && or || (bitwise vs logical)",
                fix="Use && for logical AND, || for logical OR",
                code='if (x > 5 & x < 10)  // bitwise AND, not logical!',
                fixed_code='if (x > 5 && x < 10)  // logical AND',
            ),
            _mistake(
                mistake="Not using parentheses and getting wrong operator precedence",
                fix="Use parentheses to make your logic clear",
                code='if (x > 5 && y > 10 || z > 15)  // confusing',
                fixed_code='if ((x > 5 && y > 10) || z > 15)  // clear',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that asks the user for their age and whether they have "
                "a valid ID (y/n). Use logical operators to determine if they can enter "
                "a club: must be 18 or older AND have a valid ID."
            ),
            starter_code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    int age;\n'
                '    char hasID;\n'
                '    \n'
                '    std::cout << "Enter your age: ";\n'
                '    std::cin >> age;\n'
                '    std::cout << "Have a valid ID? (y/n): ";\n'
                '    std::cin >> hasID;\n'
                '    \n'
                '    // Check conditions with logical operators\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Check age >= 18 AND hasID == 'y'",
                "Use std::boolalpha for nice output",
                "Add extra conditions for practice, like VIP or guest list",
            ],
            expected_output=(
                "Enter your age: 20\n"
                "Have a valid ID? (y/n): y\n"
                "Can enter: true"
            ),
        ),
        key_takeaways=[
            "&& (AND) both must be true, || (OR) at least one must be true",
            "! (NOT) reverses a boolean value",
            "Short-circuit evaluation can prevent errors like division by zero",
            "Use parentheses to clarify complex conditions",
            "C++ also supports keywords: and, or, not",
        ],
        next_steps="Now let us learn about assignment operators that combine operation with assignment.",
    ))

    _L(_add(
        lesson_id="cpp-l03-04",
        theory=(
            "Assignment operators let you perform an operation and assign the result in one "
            "step. Instead of writing x = x + 5, you can write x += 5. "
            "This works for all arithmetic operators: +=, -=, *=, /=, %=."
            "\n\n"
            "Compound assignment operators are not just shorter they can be more efficient "
            "because the left side (the variable being assigned to) is only evaluated once."
        ),
        analogy=(
            "Compound assignment operators are like taking your dirty dishes to the sink "
            "and washing them in one trip. Without +=, you would walk to the sink, drop "
            "a dish, walk back, grab another, walk to the sink that is two trips. "
            "With +=, each dish goes to the sink immediately."
        ),
        sections=[
            _section(
                heading="All compound assignment operators",
                body=(
                    "x += 5 is x = x + 5. x -= 3 is x = x - 3. x *= 2 is x = x * 2. "
                    "x /= 4 is x = x / 4. x %= 3 is x = x % 3. "
                    "They all follow the same pattern: operator=."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    int x = 10;\n'
                    '    \n'
                    '    x += 5;   // x = 15\n'
                    '    std::cout << "After += 5: " << x << std::endl;\n'
                    '    \n'
                    '    x -= 3;   // x = 12\n'
                    '    std::cout << "After -= 3: " << x << std::endl;\n'
                    '    \n'
                    '    x *= 2;   // x = 24\n'
                    '    std::cout << "After *= 2: " << x << std::endl;\n'
                    '    \n'
                    '    x /= 4;   // x = 6\n'
                    '    std::cout << "After /= 4: " << x << std::endl;\n'
                    '    \n'
                    '    x %= 5;   // x = 1\n'
                    '    std::cout << "After %= 5: " << x << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Compound assignments work with any type that supports the operation. "
                    'For std::string, += appends text: string s = "Hello"; s += " World";'
                ),
            ),
        ],
        common_mistakes=[
            _mistake(
                mistake="Confusing =+ with += (they are very different!)",
                fix="=+ does not exist; use += for add-and-assign",
                code='x =+ 5;  // this is x = (+5), just assigns 5!',
                fixed_code='x += 5;  // adds 5 to x',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that starts with a variable int score = 0; and applies "
                "a series of operations: add 10, subtract 3, multiply by 2, divide by 3, "
                "and take modulo 5. Print the score after each operation."
            ),
            starter_code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    int score = 0;\n'
                '    // Apply operations using compound assignment\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Start with score = 0, then use += 10 first",
                "Print after each step to track the changes",
                "Use /= 3 for division",
            ],
            expected_output=(
                "Start: 0\n"
                "After += 10: 10\n"
                "After -= 3: 7\n"
                "After *= 2: 14\n"
                "After /= 3: 4\n"
                "After %= 5: 4"
            ),
        ),
        key_takeaways=[
            "Compound assignment: operator= (e.g., +=, -=, *=, /=, %=)",
            "x += 5 is short for x = x + 5",
            "The left side is only evaluated once (can be more efficient)",
            'Works with strings too: s += "text" appends',
            "Be careful not to write =+ instead of +=",
        ],
        next_steps="Now let us learn how C++ decides which operator runs first.",
    ))

    _L(_add(
        lesson_id="cpp-l03-05",
        theory=(
            "Operator precedence determines which operator runs first when multiple operators "
            "appear in an expression. Just like in math, multiplication happens before addition. "
            "C++ has 18 levels of precedence."
            "\n\n"
            "The order (highest to lowest) for common operators: "
            "1) () parentheses, 2) ++ -- (postfix), 3) ++ -- (prefix) and !, "
            "4) * / %, 5) + -, 6) << >>, 7) < <= > >=, 8) == !=, "
            "9) &&, 10) ||, 11) = += etc."
            "\n\n"
            "Associativity determines the order when operators have the same precedence. "
            "Most operators are left-to-right, but assignment is right-to-left."
        ),
        analogy=(
            "Operator precedence is like the hierarchy in a restaurant. "
            "The chef (parentheses) has the highest authority. "
            "The sous chef (multiplication/division) comes next. "
            "Then the line cook (addition/subtraction). "
            "Then the waiter (comparison). The dishwasher (assignment) goes last. "
            "You do not wash dishes before cooking!"
        ),
        sections=[
            _section(
                heading="Why precedence matters",
                body=(
                    "Without understanding precedence, you might write code that does something "
                    "different from what you intended. When in doubt, use parentheses. "
                    "They have the highest precedence and make your intent crystal clear."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    int x = 5 + 3 * 2;     // 11 (not 16!)\n'
                    '    int y = (5 + 3) * 2;   // 16 (parentheses override)\n'
                    '    \n'
                    '    bool a = 5 > 3 && 2 < 4;  // true (comparison before &&)\n'
                    '    \n'
                    '    std::cout << "x: " << x << std::endl;\n'
                    '    std::cout << "y: " << y << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "A good rule: use parentheses whenever the precedence is not obvious. "
                    "Your future self (and others reading your code) will thank you."
                ),
            ),
        ],
        common_mistakes=[
            _mistake(
                mistake="Assuming left-to-right evaluation for all operators",
                fix="Learn the precedence table or just use parentheses",
                code='int x = 5 + 3 * 2;  // might expect 16, gets 11',
                fixed_code='int x = (5 + 3) * 2;  // clear: 16',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that computes these expressions and prints each result: "
                "a) 10 + 5 * 2, b) (10 + 5) * 2, c) 10 * 2 + 5 * 3, "
                "d) 10 * (2 + 5) * 3"
            ),
            starter_code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    // Compute and print each expression\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Print the expression as a string and then the result",
                "Observe how parentheses change the outcome",
            ],
            expected_output=(
                "10 + 5 * 2 = 20\n"
                "(10 + 5) * 2 = 30\n"
                "10 * 2 + 5 * 3 = 35\n"
                "10 * (2 + 5) * 3 = 210"
            ),
        ),
        key_takeaways=[
            "Precedence determines operator execution order",
            "* / % before + -, comparison before logical, assignment is last",
            "Use () parentheses to override default precedence",
            "When in doubt, add parentheses for clarity",
            "Assignment (=) is right-to-left associative",
        ],
        next_steps="Now let us practice with a Score Calculator project.",
    ))

    _L(_add(
        lesson_id="cpp-l03-06",
        theory=(
            "In this practice session, you will build a score calculator that computes a "
            "student's final grade based on multiple components. This combines arithmetic, "
            "comparison, and assignment operators in a real-world scenario."
            "\n\n"
            "The grade will be based on: homework (30%), midterm (30%), and final exam (40%). "
            "The program will compute the weighted average and assign a letter grade "
            "(A >= 90, B >= 80, C >= 70, D >= 60, F < 60)."
        ),
        analogy=(
            "A score calculator is like a recipe that combines ingredients in specific "
            "proportions. Homework is 30% of the recipe, midterm is 30%, final is 40%. "
            "You mix them in those proportions and the result is the final dish (grade)."
        ),
        sections=[
            _section(
                heading="Weighted average calculation",
                body=(
                    "A weighted average multiplies each component by its weight (as a decimal), "
                    "then sums them up. For example: finalScore = homework * 0.30 + midterm * 0.30 "
                    "+ finalExam * 0.40. Use compound operators to build the total step by step."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    double homework, midterm, finalExam;\n'
                    '    \n'
                    '    std::cout << "Enter homework score (0-100): ";\n'
                    '    std::cin >> homework;\n'
                    '    std::cout << "Enter midterm score (0-100): ";\n'
                    '    std::cin >> midterm;\n'
                    '    std::cout << "Enter final exam score (0-100): ";\n'
                    '    std::cin >> finalExam;\n'
                    '    \n'
                    '    double total = homework * 0.30;\n'
                    '    total += midterm * 0.30;\n'
                    '    total += finalExam * 0.40;\n'
                    '    \n'
                    '    std::cout << "Final score: " << total << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Use += to accumulate values. It is cleaner than "
                    "total = total + value and less error-prone."
                ),
            ),
        ],
        common_mistakes=[
            _mistake(
                mistake="Weights not adding up to 1.0 (100%)",
                fix="Always verify: 0.30 + 0.30 + 0.40 = 1.0",
                code='total = hw*0.3 + mid*0.3 + final*0.3;  // missing 10%!',
                fixed_code='total = hw*0.3 + mid*0.3 + final*0.4;',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that calculates a final grade. Ask for homework, "
                "midterm, and final exam scores (0-100). Weights: homework 20%, "
                "midterm 30%, final 50%. Assign letter grades: A >= 90, B >= 80, "
                "C >= 70, D >= 60, F < 60."
            ),
            starter_code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    double hw, mid, fin;\n'
                '    // Get scores\n'
                '    // Calculate weighted total\n'
                '    // Determine letter grade\n'
                '    // Print result\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Use compound assignment (+=) to accumulate the weighted score",
                "Use if/else if for letter grade determination",
                "Check that each input is between 0 and 100",
            ],
            expected_output=(
                "Enter homework score: 85\n"
                "Enter midterm score: 90\n"
                "Enter final exam score: 78\n"
                "Final score: 82.0\n"
                "Letter grade: B"
            ),
        ),
        key_takeaways=[
            "Compound operators simplify accumulation: total += value",
            "Weighted averages multiply each component by its weight",
            "Weights must sum to 1.0 (100%)",
            "Comparison operators determine letter grade boundaries",
            "Real-world programs combine multiple operator types",
        ],
        next_steps="Now for a challenge: bit manipulation puzzle!",
    ))

    _L(_add(
        lesson_id="cpp-l03-07",
        theory=(
            "Bitwise operators work directly on the binary representation of integers. "
            "They are the closest you get to the metal without writing assembly."
            "\n\n"
            "C++ has: & (AND), | (OR), ^ (XOR), ~ (NOT), << (left shift), >> (right shift). "
            "Each bit of the result is computed from the corresponding bits of the inputs."
            "\n\n"
            "Bitwise AND (&): 1 & 1 = 1, otherwise 0. "
            "Bitwise OR (|): 0 | 0 = 0, otherwise 1. "
            "XOR (^): 1 ^ 0 = 1, 0 ^ 1 = 1, same bits = 0. "
            "NOT (~): flips all bits (0 to 1, 1 to 0). "
            "Left shift (x << n): moves bits left n places, fills with 0s (multiply by 2^n). "
            "Right shift (x >> n): moves bits right n places (divide by 2^n)."
        ),
        analogy=(
            "Bitwise operators are like flipping individual switches on a control panel. "
            "& is like: both switches must be ON for the light to turn on. "
            "| is like: at least one switch ON turns the light on. "
            "^ (XOR) is like: this switch controls the light only if that other switch is OFF. "
            "~ is like flipping every switch at once. "
            "<< is like pushing all sliders one position to the left."
        ),
        sections=[
            _section(
                heading="Bitwise in action",
                body=(
                    "Bitwise operators are used in flags, permissions, encryption, "
                    "graphics (color channels), and low-level hardware control. "
                    "In game programming, a single int might store player status flags: "
                    "bit 0 = isVisible, bit 1 = isInvincible, bit 2 = hasKey, etc."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    unsigned int a = 5;   // binary: 0101\n'
                    '    unsigned int b = 3;   // binary: 0011\n'
                    '    \n'
                    '    std::cout << "a & b = " << (a & b) << std::endl;  // 0001 = 1\n'
                    '    std::cout << "a | b = " << (a | b) << std::endl;  // 0111 = 7\n'
                    '    std::cout << "a ^ b = " << (a ^ b) << std::endl;  // 0110 = 6\n'
                    '    std::cout << "a << 1 = " << (a << 1) << std::endl;  // 1010 = 10\n'
                    '    std::cout << "a >> 1 = " << (a >> 1) << std::endl;  // 0010 = 2\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Left shift by 1 multiplies by 2. Right shift by 1 divides by 2. "
                    "This is faster than * and /, but compilers optimize both the same way."
                ),
            ),
        ],
        common_mistakes=[
            _mistake(
                mistake="Confusing & (bitwise AND) with && (logical AND)",
                fix="Use & for bitwise operations on integers, && for logical conditions",
                code='if (x & y)  // bitwise AND, probably not what you meant',
                fixed_code='if (x && y)  // logical AND',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a C++ program that asks the user for an integer and uses bitwise "
                "operators to check whether it is odd or even. Hint: x & 1 is 1 if x is odd "
                "(because the least significant bit is 1 for odd numbers). "
                "Also print the number multiplied by 4 using left shift."
            ),
            starter_code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    int num;\n'
                '    std::cout << "Enter an integer: ";\n'
                '    std::cin >> num;\n'
                '    // Check odd/even with &\n'
                '    // Multiply by 4 with <<\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "x & 1 gives 1 if odd, 0 if even",
                "x << 2 is x * 4 (shift left by 2 positions)",
                "Use unsigned int for predictable bitwise behavior",
            ],
            expected_output=(
                "Enter an integer: 7\n"
                "7 is odd\n"
                "7 * 4 = 28"
            ),
        ),
        key_takeaways=[
            "Bitwise operators: & | ^ ~ << >>",
            "& is bitwise AND, && is logical AND (they are different!)",
            "<< shifts bits left (multiply by 2^n), >> shifts right (divide by 2^n)",
            "Bitwise ops are used in flags, permissions, graphics, hardware",
        ],
        next_steps="Now for the final Level 3 project: Unit Converter!",
    ))

    _L(_add(
        lesson_id="cpp-l03-08",
        theory=(
            "Your Level 3 project is a Unit Converter. This brings together arithmetic operators, "
            "comparison operators, assignment operators, and everything from Levels 1 and 2."
            "\n\n"
            "The program will: show a menu of conversion types (length, weight, temperature), "
            "ask the user to choose, then perform the conversion. You will use a menu system "
            "with if/else if or switch, and handle multiple conversion formulas."
        ),
        analogy=(
            "A multi-unit converter is like a Swiss Army knife. It has a tool for every job. "
            "The user picks which blade (conversion type) they need, and the tool does the rest. "
            "Building one program that does many things is the essence of software engineering."
        ),
        sections=[
            _section(
                heading="Program structure",
                body=(
                    "Start by showing a menu with options. Read the user's choice. "
                    "Use if/else if or switch to handle each choice. "
                    "Each conversion type needs its own formula and variables."
                ),
                code=(
                    '#include <iostream>\n'
                    '\n'
                    'int main() {\n'
                    '    int choice;\n'
                    '    double value, result;\n'
                    '    \n'
                    '    std::cout << "=== Unit Converter ===" << std::endl;\n'
                    '    std::cout << "1. Meters to Feet" << std::endl;\n'
                    '    std::cout << "2. Feet to Meters" << std::endl;\n'
                    '    std::cout << "3. KG to Pounds" << std::endl;\n'
                    '    std::cout << "4. Pounds to KG" << std::endl;\n'
                    '    std::cout << "Choose: ";\n'
                    '    std::cin >> choice;\n'
                    '    \n'
                    '    std::cout << "Enter value: ";\n'
                    '    std::cin >> value;\n'
                    '    \n'
                    '    if (choice == 1) result = value * 3.28084;\n'
                    '    else if (choice == 2) result = value * 0.3048;\n'
                    '    else if (choice == 3) result = value * 2.20462;\n'
                    '    else if (choice == 4) result = value * 0.453592;\n'
                    '    \n'
                    '    std::cout << "Result: " << result << std::endl;\n'
                    '    return 0;\n'
                    '}'
                ),
                pro_tip=(
                    "Use constexpr for conversion factors. They never change "
                    "and naming them makes the code self-documenting."
                ),
            ),
        ],
        common_mistakes=[
            _mistake(
                mistake="Using wrong conversion factor (gives incorrect results)",
                fix="Double-check your conversion factors from reliable sources",
                code='result = value * 3.28;  // imprecise factor',
                fixed_code='result = value * 3.28084;  // precise factor',
            ),
        ],
        exercise=_exercise(
            description=(
                "Build a Unit Converter in C++ that supports at least 4 conversions "
                "across 2 categories (e.g., length and weight). Show a menu, get user "
                "choice, read the value, perform the conversion, and display the result. "
                "Use constexpr for all conversion factors."
            ),
            starter_code=(
                '#include <iostream>\n'
                '\n'
                'int main() {\n'
                '    constexpr double METER_TO_FEET = 3.28084;\n'
                '    constexpr double KG_TO_LBS = 2.20462;\n'
                '    // Add more conversion factors\n'
                '    // Show menu\n'
                '    // Perform conversion\n'
                '    return 0;\n'
                '}'
            ),
            hints=[
                "Use constexpr double for all conversion factors",
                "Show a numbered menu with clear descriptions",
                "Use if/else if or switch to handle choices",
                "Format output with setprecision for clean results",
            ],
            expected_output=(
                "=== Unit Converter ===\n"
                "1. Meters to Feet\n"
                "2. Feet to Meters\n"
                "3. KG to Pounds\n"
                "4. Pounds to KG\n"
                "Choose: 1\n"
                "Enter value: 10\n"
                "10 meters = 32.8084 feet"
            ),
        ),
        key_takeaways=[
            "constexpr makes conversion factors self-documenting",
            "Menu-driven programs organize multiple features",
            "Arithmetic operators perform the actual conversions",
            "Always verify conversion factors before using them",
            "Congratulations on completing C++ Level 3!",
        ],
        next_steps="Level 3 complete! You now understand C++ operators. Next: Conditionals (if, else, switch).",
    ))

    # ── End of C++ section ────────────────────────────────────────────
    _L("]));")

    _L("")
    _L("")
    _L("# ============================================================================")
    _L("# JAVA LEVEL 1: FIRST STEPS")
    _L("# ============================================================================")
    _L("")
    _L("HAND_CRAFTED_LESSONS.update(dict([")

    _L(_add(
        lesson_id="java-l01-01",
        theory=(
            "Java was created by James Gosling at Sun Microsystems in 1995. Its original "
            "name was Oak (named after a tree outside Gosling's office). The main idea behind "
            "Java was write once, run anywhere (WORA) you compile Java once and it runs on "
            "Windows, Mac, Linux, or any device with a Java Virtual Machine (JVM)."
            "\n\n"
            "Java is statically typed (like C++), garbage-collected (memory is managed "
            "automatically), and object-oriented (everything is wrapped in classes). "
            "It is one of the most popular languages for enterprise software, Android apps, "
            "and large-scale backend systems."
            "\n\n"
            "Java's slogan is WORA because Java code is compiled to bytecode which runs on "
            "the JVM. The JVM translates bytecode to the machine code of whatever platform "
            "you are on. This abstraction layer is what gives Java its portability."
        ),
        analogy=(
            "Java is like a universal power adapter. You write your code once (like a "
            "device with a standard plug), and the JVM (like the adapter) converts it "
            "to work on any electrical outlet (operating system). You do not need a "
            "separate device for every country you visit."
        ),
        sections=[
            _section(
                heading="What makes Java special?",
                body=(
                    "Three things: the JVM, garbage collection, and the massive ecosystem. "
                    "The JVM handles memory management and security. Garbage collection means "
                    "you never have to manually free memory Java does it automatically. "
                    "And Java has one of the largest libraries and community support of any language."
                ),
                pro_tip=(
                    "Java is the #1 language for enterprise backend systems. Banks, "
                    "e-commerce sites, and government systems run on Java."
                ),
            ),
            _section(
                heading="Java vs C++", 
                body=(
                    "Java is simpler than C++ in many ways. No pointers (references instead), "
                    "no multiple inheritance (interfaces instead), no operator overloading, "
                    "and automatic garbage collection. Java code is more verbose but also "
                    "more predictable and harder to crash."
                ),
                pro_tip=(
                    "Java sacrificed some performance for safety and portability. "
                    "Modern JVMs are incredibly fast, often approaching C++ speeds."
                ),
            ),
        ],
        key_takeaways=[
            "Java was created for write once, run anywhere portability",
            "Java runs on the JVM (Java Virtual Machine) which abstracts the hardware",
            "Java has automatic garbage collection no manual memory management",
            "Java is statically typed and object-oriented",
            "Java is widely used in enterprise, Android, and backend systems",
        ],
        next_steps="Ready to write your first Java program? Let us go!",
    ))

    _L(_add(
        lesson_id="java-l01-02",
        theory=(
            "Time to write your first Java program! In Java, everything is inside a class. "
            "The classic Hello World looks like this: a class called Main with a main method. "
            "The main method is the entry point just like in C++, but the syntax is more verbose."
            "\n\n"
            "The main method signature is always: public static void main(String[] args). "
            "This looks intimidating but each keyword has a purpose. public means anyone can "
            "access it. static means it belongs to the class, not an object. void means "
            "it returns nothing. String[] args is for command-line arguments."
            "\n\n"
            "System.out.println() is Java's version of printf or cout. System is a class, "
            "out is a static field (like an object), and println is a method that prints "
            "a line. Java is verbose but very explicit."
        ),
        analogy=(
            "A Java program is like a play. The class is the theater building. "
            "The main method is the stage where the performance starts. "
            "System.out.println() is like an actor speaking lines to the audience. "
            "Every part of the Java syntax serves a purpose, like lighting and stage directions."
        ),
        sections=[
            _section(
                heading="Your first Java program",
                body=(
                    "Here is the complete Hello World. Notice the class name (Main) must match "
                    "the filename (Main.java). Java is case-sensitive and filename-sensitive."
                ),
                code=(
                    'public class Main {\n'
                    '    public static void main(String[] args) {\n'
                    '        System.out.println("Hello, World!");\n'
                    '    }\n'
                    '}'
                ),
                pro_tip=(
                    "In Java, the filename must match the class name exactly. "
                    "If your class is Main, the file must be Main.java."
                ),
            ),
            _section(
                heading="How to compile and run",
                body=(
                    "Unlike C++, compile with javac and run with java. "
                    "javac Main.java creates Main.class (bytecode). "
                    "java Main runs the bytecode on the JVM."
                ),
                code=(
                    'javac Main.java\n'
                    'java Main'
                ),
                pro_tip=(
                    "When running java Main, do NOT include .class extension. "
                    "The java command expects the class name, not the filename."
                ),
            ),
        ],
        code_example=_code_example(
            code=(
                'public class Main {\n'
                '    public static void main(String[] args) {\n'
                '        System.out.println("Hello, World!");\n'
                '    }\n'
                '}'
            ),
            annotations=[
                _anno(1, "Declare a class named Main (must match filename)"),
                _anno(2, "Main method: public, static, void, String[] args"),
                _anno(3, "println prints a line of text to the console"),
            ],
        ),
        common_mistakes=[
            _mistake(
                mistake="Filename does not match class name",
                fix="The class name and filename must be identical (including capitalization)",
                code='// File: test.java\npublic class Main { }',
                fixed_code='// File: Main.java\npublic class Main { }',
            ),
            _mistake(
                mistake="Forgetting String[] args in main method signature",
                fix="The exact signature is: public static void main(String[] args)",
                code='public static void main() { }',
                fixed_code='public static void main(String[] args) { }',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a Java program that prints your name and your favorite hobby "
                "on two separate lines using System.out.println()."
            ),
            starter_code=(
                'public class Main {\n'
                '    public static void main(String[] args) {\n'
                '        // Write your code here\n'
                '    }\n'
                '}'
            ),
            hints=[
                "Use System.out.println() for each line",
                "Each println() call automatically adds a newline",
                "Remember the semicolon at the end of each statement",
            ],
            expected_output=(
                "My name is Alex\n"
                "I love programming"
            ),
        ),
        key_takeaways=[
            "Java code is inside a class",
            "public static void main(String[] args) is the entry point",
            "System.out.println() prints a line",
            "Compile with javac, run with java",
            "Filename must match class name exactly",
        ],
        next_steps="Great! Now let us explore more about output in Java.",
    ))

    _L(_add(
        lesson_id="java-l01-03",
        theory=(
            "System.out.println() is just one way to print. Java also has System.out.print() "
            "(no newline at the end) and System.out.printf() (formatted output like C's printf)."
            "\n\n"
            "println adds a newline after printing. print does not add a newline. "
            "printf uses format specifiers like %d, %s, %f, just like C. "
            "You can also concatenate strings with + to build complex output."
        ),
        analogy=(
            "println is like hitting Enter after typing. print is like typing without "
            "pressing Enter. printf is like a typewriter with formatting wheels you "
            "set exactly how things should appear."
        ),
        sections=[
            _section(
                heading="print vs println vs printf",
                body=(
                    "Choose the right tool: println for most lines, print when you want "
                    "multiple things on the same line, printf when you need precise formatting."
                ),
                code=(
                    'public class Main {\n'
                    '    public static void main(String[] args) {\n'
                    '        System.out.print("This ");\n'
                    '        System.out.print("is ");\n'
                    '        System.out.println("all on one line");\n'
                    '        \n'
                    '        String name = "Alex";\n'
                    '        int age = 18;\n'
                    '        System.out.printf("Name: %s, Age: %d%n", name, age);\n'
                    '    }\n'
                    '}'
                ),
                pro_tip=(
                    "Use %n instead of \\n in printf format strings. "
                    "%n is platform-independent (works on Windows, Mac, Linux)."
                ),
            ),
        ],
        code_example=_code_example(
            code=(
                'public class Main {\n'
                '    public static void main(String[] args) {\n'
                '        int score = 95;\n'
                '        double avg = 87.3333;\n'
                '        char grade = \'A\';\n'
                '        System.out.println("Score: " + score);\n'
                '        System.out.printf("Average: %.1f%n", avg);\n'
                '        System.out.println("Grade: " + grade);\n'
                '    }\n'
                '}'
            ),
            annotations=[
                _anno(6, "String concatenation with + combines text and variables"),
                _anno(7, "printf with %.1f formats to 1 decimal place"),
                _anno(8, "println automatically converts grade to string"),
            ],
        ),
        common_mistakes=[
            _mistake(
                mistake="Using \\n in printf instead of %n",
                fix="Use %n for platform-independent newlines in printf",
                code='System.out.printf("Line1\\nLine2");',
                fixed_code='System.out.printf("Line1%nLine2");',
            ),
            _mistake(
                mistake="Mismatching format specifiers and arguments in printf",
                fix="Each %... must have a matching argument of the correct type",
                code='System.out.printf("%d %s", "hello", 42);  // reversed!',
                fixed_code='System.out.printf("%d %s", 42, "hello");',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a Java program that uses all three output methods: print, println, "
                "and printf. Print a sentence using print() across multiple calls, "
                "a formatted table row using printf(), and a summary using println()."
            ),
            starter_code=(
                'public class Main {\n'
                '    public static void main(String[] args) {\n'
                '        // Use print()\n'
                '        // Use println()\n'
                '        // Use printf()\n'
                '    }\n'
                '}'
            ),
            hints=[
                "Use print() to build a line piece by piece",
                "Use println() to end a line",
                "Use printf() with %s, %d, %.2f for formatted output",
            ],
            expected_output=(
                "Building a line with print... done!\n"
                "Name: Alex, Age: 18, GPA: 3.75"
            ),
        ),
        key_takeaways=[
            "println() adds newline, print() does not",
            "printf() supports formatted output with % specifiers",
            "Use + for string concatenation",
            "Use %n for platform-independent newlines in printf",
            "Match format specifiers to argument types in printf",
        ],
        next_steps="Now let us learn about comments in Java.",
    ))

    _L(_add(
        lesson_id="java-l01-04",
        theory=(
            "Java supports the same comment styles as C++: // for single-line, "
            "/* */ for multi-line. But Java also has a special documentation comment "
            "/** */ (called Javadoc) that can be turned into HTML documentation "
            "using the javadoc tool."
            "\n\n"
            "Javadoc comments start with /** and use @tags like @param, @return, "
            "@author, @version to describe what methods and classes do. "
            "This is a standard practice in professional Java development."
        ),
        analogy=(
            "Comments are like the labels on a file folder. The folder name (code) tells you "
            "what is inside. The label (comment) tells you why it matters, when it was created, "
            "and what to be careful about. Javadoc is like the official catalog entry."
        ),
        sections=[
            _section(
                heading="Javadoc comments",
                body=(
                    "Javadoc comments start with /** and end with */. They describe classes, "
                    "methods, and fields. The javadoc tool generates HTML documentation from them."
                ),
                code=(
                    '/**\n'
                    ' * Calculates the area of a circle.\n'
                    ' * @param radius The radius of the circle\n'
                    ' * @return The area (pi * r * r)\n'
                    ' * @author Alex\n'
                    ' */\n'
                    'public static double area(double radius) {\n'
                    '    return Math.PI * radius * radius;\n'
                    '}'
                ),
                pro_tip=(
                    "Good Javadoc explains what the method does and what the parameters mean. "
                    "Run javadoc on your code to see professional-looking API docs."
                ),
            ),
        ],
        common_mistakes=[
            _mistake(
                mistake="Writing comments that describe the obvious",
                fix="Explain why, not what. The code shows what it does.",
                code='int x = 5;  // set x to 5',
                fixed_code='int x = 5;  // number of retry attempts',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a Java program that prints a short bio. Use single-line, multi-line, "
                "and Javadoc-style comments explaining your code."
            ),
            starter_code=(
                '/**\n'
                ' * My bio program.\n'
                ' * @author Your Name\n'
                ' */\n'
                'public class Main {\n'
                '    public static void main(String[] args) {\n'
                '        // Add your code\n'
                '    }\n'
                '}'
            ),
            hints=[
                "Start with a Javadoc comment for the class",
                "Use single-line // comments for inline explanations",
                "Use /* */ for blocking out sections"
            ],
            expected_output=(
                "Name: Alex\n"
                "Age: 18\n"
                "Goal: Become a Java developer"
            ),
        ),
        key_takeaways=[
            "// for single-line comments, /* */ for multi-line",
            "/** */ for Javadoc documentation comments",
            "Good comments explain WHY, not WHAT",
            "Javadoc can generate HTML documentation",
            "Use @param, @return, @author tags in Javadoc",
        ],
        next_steps="Now let us understand how Java programs actually run.",
    ))

    _L(_add(
        lesson_id="java-l01-05",
        theory=(
            "Java uses a hybrid approach: compilation AND interpretation. "
            "Your source code (.java) is compiled by javac into bytecode (.class). "
            "Bytecode is platform-independent. Then the JVM interprets (or JIT-compiles) "
            "the bytecode into machine code for your specific platform."
            "\n\n"
            "JIT stands for Just-In-Time compilation. The JVM identifies hot paths "
            "(code that runs frequently) and compiles them to native machine code on the fly. "
            "This gives Java near-native performance while keeping portability."
            "\n\n"
            "The JVM also handles memory management through garbage collection. "
            "Objects that are no longer referenced are automatically cleaned up. "
            "You never need to call free() or delete() in Java."
        ),
        analogy=(
            "Java is like a universal translator. You speak in Java (source code). "
            "The translator (javac) writes it down in a universal language (bytecode). "
            "Another translator (JVM) reads the universal language and speaks it in the "
            "local language (machine code). JIT compilation is like the translator getting "
            "faster at translating the phrases you use most often."
        ),
        sections=[
            _section(
                heading="The Java toolchain",
                body=(
                    "JDK (Java Development Kit) contains javac (compiler), java (launcher), "
                    "and other tools. JRE (Java Runtime Environment) contains just the JVM "
                    "for running already-compiled code. To develop Java, install the JDK."
                ),
                code=(
                    '# Step 1: Write code in Main.java\n'
                    '# Step 2: Compile to bytecode\n'
                    'javac Main.java   # creates Main.class\n'
                    '# Step 3: Run on JVM\n'
                    'java Main          # runs the bytecode'
                ),
                pro_tip=(
                    "Check your Java version: java -version and javac -version. "
                    "Make sure both are the same version to avoid compatibility issues."
                ),
            ),
        ],
        common_mistakes=[
            _mistake(
                mistake="Running java Main.class instead of java Main",
                fix="Do not include .class when running. java expects the class name.",
                code='java Main.class  // ERROR!',
                fixed_code='java Main',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a simple Java program, compile it with javac, and run it with java. "
                "Print the Java version you are using by adding System.getProperty(\"java.version\") "
                "to your output."
            ),
            starter_code=(
                'public class Main {\n'
                '    public static void main(String[] args) {\n'
                '        System.out.println("Java version: " + System.getProperty("java.version"));\n'
                '    }\n'
                '}'
            ),
            hints=[
                "Save as Main.java",
                "Compile: javac Main.java",
                "Run: java Main",
            ],
            expected_output=(
                "Java version: 17.0.1\n"
                "My first Java program runs!"
            ),
        ),
        key_takeaways=[
            "Java compiles to bytecode, which runs on the JVM",
            "JIT compilation makes frequently-used code run fast",
            "Garbage collection manages memory automatically",
            "javac compiles, java runs",
            "The JVM provides platform independence",
        ],
        next_steps="Now let us practice with a complete Java program.",
    ))

    _L(_add(
        lesson_id="java-l01-06",
        theory=(
            "Let us put everything together and write a complete Java program from scratch. "
            "You will use System.out.println(), comments, and multiple statements to create "
            "a simple program that prints information about yourself."
            "\n\n"
            "Remember the structure: public class Main, public static void main(String[] args), "
            "code inside the main method. Practice this until it becomes second nature."
        ),
        analogy=(
            "Practicing the basic Java structure is like learning to tie your shoes. "
            "At first you have to think about every loop and pull. But soon it becomes "
            "automatic, and you can do it without thinking."
        ),
        sections=[
            _section(
                heading="What to build",
                body=(
                    "Write a program that prints a simple profile card. Include your name, "
                    "age, city, and a fun fact. Use comments to label each section."
                ),
                code=(
                    'public class Main {\n'
                    '    public static void main(String[] args) {\n'
                    '        // Personal info card\n'
                    '        System.out.println("=== Profile Card ===");\n'
                    '        System.out.println("Name: Alex");\n'
                    '        System.out.println("Age: 18");\n'
                    '        System.out.println("City: New York");\n'
                    '        System.out.println("Fun Fact: I love Java!");\n'
                    '    }\n'
                    '}'
                ),
                pro_tip=(
                    "Use println() to add blank lines: System.out.println(); "
                    "with no arguments prints just a newline."
                ),
            ),
        ],
        common_mistakes=[
            _mistake(
                mistake="Missing the main method signature braces",
                fix="Check that your parentheses and curly braces all match",
                code='public static void main String[] args) { }',
                fixed_code='public static void main(String[] args) { }',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a Java program that prints an ASCII art animal (like a cat or dog) "
                "using multiple println statements. Add comments describing your art."
            ),
            starter_code=(
                'public class Main {\n'
                '    public static void main(String[] args) {\n'
                '        // Draw your animal here\n'
                '    }\n'
                '}'
            ),
            hints=[
                "Plan your art on paper first",
                "Each println() is one line of the drawing",
                "Use spaces for alignment",
            ],
            expected_output=(
                "  /\\\\_/\\\\\n"
                " ( o.o )\n"
                "  > ^ <\n"
                " /|   |\\\\\n"
                "  |   |"
            ),
        ),
        key_takeaways=[
            "Every Java program has a class and a main method",
            "println() is the primary output tool",
            "Comments help organize and explain code",
            "Practice the class + main structure until it is automatic",
        ],
        next_steps="Ready for a challenge? Let us try printing patterns in Java!",
    ))

    _L(_add(
        lesson_id="java-l01-07",
        theory=(
            "This challenge tests your understanding of output in Java by printing patterns. "
            "You will create symmetric shapes using only println() statements. "
            "Pattern printing builds your attention to detail and understanding of spacing."
        ),
        analogy=(
            "Pattern printing is like weaving. Each row (weft thread) crosses the columns "
            "(warp threads) at specific positions. Your println statements lay down each row, "
            "and spaces determine where the pattern characters sit."
        ),
        sections=[
            _section(
                heading="Challenge: a checkerboard",
                body=(
                    "Print a 5x5 checkerboard pattern where spaces and asterisks alternate. "
                    "Each row should be offset to create the checkerboard effect."
                ),
                code=(
                    '* * * * *\n'
                    ' * * * * *\n'
                    '* * * * *\n'
                    ' * * * * *\n'
                    '* * * * *'
                ),
                pro_tip=(
                    "Notice odd rows start with *, even rows start with a space. "
                    "This alternating pattern creates the checkerboard."
                ),
            ),
        ],
        common_mistakes=[
            _mistake(
                mistake="Not aligning rows properly",
                fix="Draw the pattern on grid paper first, counting every character",
                code='System.out.println(" *** ");',
                fixed_code='System.out.println("  ***  ");',
            ),
        ],
        exercise=_exercise(
            description=(
                "Write a Java program that prints a right triangle of asterisks. "
                "Row 1 has 1 star, row 2 has 2 stars, up to row 5 with 5 stars."
            ),
            starter_code=(
                'public class Main {\n'
                '    public static void main(String[] args) {\n'
                '        // Print a triangle\n'
                '    }\n'
                '}'
            ),
            hints=[
                "Row 1: 1 star, Row 2: 2 stars, etc.",
                "Use multiple println() calls",
                "No loops needed yet just hardcode each row",
            ],
            expected_output=(
                "*\n"
                "**\n"
                "***\n"
                "****\n"
                "*****"
            ),
        ),
        key_takeaways=[
            "Each println() is one row of the pattern",
            "Spaces control horizontal alignment",
            "Plan on paper before coding",
            "Pattern recognition is a key programming skill",
        ],
        next_steps="Now for a project: build a terminal banner in Java!",
    ))

    _L(_add(
        lesson_id="java-l01-08",
        theory=(
            "For your Level 1 project, you will create a terminal banner program. "
            "A terminal banner displays program information in a fancy box when the "
            "program starts. It is the first impression users get of your program."
            "\n\n"
            "You will use println(), print(), and escape sequences to create a "
            "professional-looking title screen with borders and aligned text."
        ),
        analogy=(
            "A terminal banner is like the title screen of a video game. "
            "Before the game starts, you see the logo, version, and options. "
            "Your Java banner will create that same feeling for your programs."
        ),
        sections=[
            _section(
                heading="Banner design",
                body=(
                    "Create a banner with a top border of = signs, a title line, "
                    "a tagline, version info, author credit, and a bottom border. "
                    "Make sure the borders are the same length on top and bottom."
                ),
                code=(
                    'public class Main {\n'
                    '    public static void main(String[] args) {\n'
                    '        System.out.println("================================");\n'
                    '        System.out.println("   WELCOME TO JAVA ADVENTURES");\n'
                    '        System.out.println("   Learn Coding the Fun Way");\n'
                    '        System.out.println("   Version 1.0");\n'
                    '        System.out.println("   By: Your Name");\n'
                    '        System.out.println("================================");\n'
                    '    }\n'
                    '}'
                ),
                pro_tip=(
                    "Make the border width an even number so centered text "
                    "looks symmetrical. Count the characters in your longest line."
                ),
            ),
        ],
        exercise=_exercise(
            description=(
                "Create a Java program that displays a professional terminal banner. "
                "Include: top/bottom border, program name, tagline, version, author, "
                "and at least 8 lines total. Use consistent border widths."
            ),
            starter_code=(
                'public class Main {\n'
                '    public static void main(String[] args) {\n'
                '        System.out.println("========================================");\n'
                '        // Add your banner content\n'
                '    }\n'
                '}'
            ),
            hints=[
                "Use spaces to center text within the borders",
                "Match top and bottom border lengths exactly",
                "Use println() with empty string for blank lines",
            ],
            expected_output=(
                "========================================\n"
                "          JAVA ADVENTURES\n"
                "     Learn Programming the Fun Way\n"
                "            Version 1.0\n"
                "           By: Your Name\n"
                "========================================"
            ),
        ),
        key_takeaways=[
            "Banners make terminal programs look professional",
            "Consistent border widths require careful counting",
            "println() and print() work together for layout",
            "Level 1 complete you know Java output!",
        ],
        next_steps="Level 1 complete! Next: Level 2 Variables in Java.",
    ))
