"""Authored Python fundamentals lessons for the placement-preparation core.

These lessons deliberately replace title-only template filler for high-frequency
control-flow and function concepts. Content is structured for the existing
lesson renderer and includes examples, misconceptions, exercises and checks.
"""
from __future__ import annotations

from typing import Any, Dict


_PYTHON_CORE: Dict[str, Dict[str, Any]] = {
    "if Statement": {
        "concept": "the if statement",
        "purpose": "run a block only when a Boolean condition is true",
        "how": "Python evaluates the expression after if. If its value is truthy, the indented suite runs; otherwise Python skips to the next statement after that suite. A colon ends the header, and indentation defines the block.",
        "why": "Programs use conditions whenever the next action depends on data: validating an age, checking whether a balance is sufficient, or deciding whether a user is allowed to continue. The condition should express the rule directly rather than hide it inside a complicated expression.",
        "pitfall": "A common error is writing an assignment-like expression or forgetting the colon. Another is using = instead of == when comparing values. Python also treats 0, empty strings, empty collections and None as false in conditions.",
        "code": "temperature = 32\nif temperature > 30:\n    print('It is hot')\nprint('Check complete')",
        "output": "It is hot\nCheck complete",
        "exercise": "Read an integer temperature and print 'Hot' only when it is greater than 30. Print 'Done' after the condition in every case.",
        "expected": "Input 35 prints Hot followed by Done; input 20 prints only Done.",
        "quiz": [
            ("When does the body of an if statement execute?", ["When its condition is truthy", "Every time the program starts", "Only when the condition is zero", "Only after a loop"], 0, "Python executes the indented if suite only when the condition evaluates to a truthy value."),
            ("What punctuation ends an if header?", ["Semicolon", "Colon", "Comma", "Curly brace"], 1, "A colon introduces the indented suite that belongs to the if statement."),
            ("What does if count == 0: check?", ["Assigns zero to count", "Checks whether count equals zero", "Increments count", "Checks whether count is positive"], 1, "The double equals operator compares values; a single equals sign assigns a value."),
        ],
    },
    "if-else Statement": {
        "concept": "the if-else statement",
        "purpose": "choose exactly one of two alternative paths",
        "how": "Python tests the if condition first. A true condition runs the if suite and skips else; a false condition skips the if suite and runs the else suite. Both suites use indentation and the else header also ends with a colon.",
        "why": "Use if-else when every input should receive one of two outcomes, such as pass/fail, even/odd, eligible/not eligible, or accepted/rejected. This makes the two cases explicit and prevents a program from silently doing nothing for the false case.",
        "pitfall": "The else keyword has no condition of its own and must align with its matching if. Do not write else if in Python; use elif when there are more than two alternatives. Keep the two branches mutually exclusive.",
        "code": "marks = 72\nif marks >= 40:\n    print('Pass')\nelse:\n    print('Fail')",
        "output": "Pass",
        "exercise": "Read an integer and print 'Even' when it is divisible by 2; otherwise print 'Odd'.",
        "expected": "Input 14 prints Even; input 9 prints Odd.",
        "quiz": [
            ("Which branch runs when an if condition is false?", ["The if suite", "The else suite", "Both suites", "Neither suite always"], 1, "The else suite is the alternative path taken when the associated if condition is false."),
            ("Can an else header contain a condition?", ["Yes, always", "No, it is the unconditional fallback", "Only inside loops", "Only with strings"], 1, "Else has no condition; use elif when another condition must be tested."),
            ("Which operator checks divisibility by two?", ["//", "%", "**", "="], 1, "The modulo operator returns the remainder; an even number has remainder zero when divided by two."),
        ],
    },
    "elif Chain": {
        "concept": "an elif chain",
        "purpose": "select one outcome from three or more ordered conditions",
        "how": "Python checks the if condition, then each elif condition from top to bottom. The first true branch runs and the rest are skipped. The optional final else runs only when every preceding condition is false.",
        "why": "An elif chain is useful for grading bands, shipping tiers, menu choices and classification rules. Order matters: put more specific or higher-threshold conditions first so a broad condition does not capture values that belong in a later category.",
        "pitfall": "Independent if statements are not equivalent to one if/elif chain: several independent branches may all run. Check boundary values carefully and make ranges non-overlapping, for example 90 and above, 75–89, 60–74, then below 60.",
        "code": "score = 82\nif score >= 90:\n    grade = 'A'\nelif score >= 75:\n    grade = 'B'\nelif score >= 60:\n    grade = 'C'\nelse:\n    grade = 'Needs practice'\nprint(grade)",
        "output": "B",
        "exercise": "Read a score from 0 to 100. Print A for 90+, B for 75–89, C for 60–74, and Needs practice below 60.",
        "expected": "Scores 95, 82, 68 and 40 produce A, B, C and Needs practice respectively.",
        "quiz": [
            ("How many branches run in one if/elif/else chain?", ["Every true branch", "At most one branch", "Exactly two branches", "No branch can run"], 1, "Python stops checking the chain after the first true condition, so at most one suite executes."),
            ("Why should a 90+ grade check come before a 75+ check?", ["Python requires alphabetical order", "The broader 75+ check would also match 95", "The 90+ check is slower", "It changes the data type"], 1, "A score of 95 also satisfies 75+, so the higher threshold must be checked first."),
            ("Is the final else required?", ["Yes, every chain needs it", "No, it is optional", "Only in functions", "Only for numeric conditions"], 1, "A chain may omit else when no fallback action is needed for unmatched values."),
        ],
    },
    "for Loop with range()": {
        "concept": "for loops with range",
        "purpose": "repeat a block once for each value in a sequence of numbers",
        "how": "range(stop) produces integers starting at zero and ending before stop. range(start, stop, step) lets you choose the first value and increment. A for loop assigns each produced value to its loop variable and executes the indented body once.",
        "why": "Counted loops are ideal when the number of repetitions is known: processing positions, generating tables, accumulating totals, or repeating an operation a fixed number of times. The stop value is exclusive, which makes range(1, 6) produce five values.",
        "pitfall": "A frequent off-by-one error is expecting the stop value to appear. Also avoid changing the loop variable to control iteration; range supplies the next value on each pass. Use a positive or negative step that moves toward the stop boundary.",
        "code": "total = 0\nfor number in range(1, 6):\n    total += number\nprint(total)",
        "output": "15",
        "exercise": "Use a for loop and range() to print the multiplication table for a number from 1 through 10.",
        "expected": "For input 4, the first line is 4 x 1 = 4 and the last line is 4 x 10 = 40.",
        "quiz": [
            ("What values does range(1, 5) produce?", ["1, 2, 3, 4", "1, 2, 3, 4, 5", "0, 1, 2, 3, 4", "5 only"], 0, "The start is included and the stop is excluded, so range(1, 5) produces four values."),
            ("How many iterations does range(10) produce?", ["9", "10", "11", "1"], 1, "range(10) produces the ten integers from 0 through 9."),
            ("What does range(2, 11, 2) produce?", ["2, 4, 6, 8, 10", "2, 4, 6, 8, 10, 12", "1, 3, 5, 7, 9", "11, 9, 7"], 0, "The sequence starts at 2, increases by 2, and stops before reaching 11."),
        ],
    },
    "while Loop": {
        "concept": "the while loop",
        "purpose": "repeat a block while a condition remains true",
        "how": "Python checks the while condition before every iteration. If it is true, the indented body runs; then the condition is checked again. When it becomes false, execution continues after the loop. The body must update the state that eventually makes the condition false.",
        "why": "Use while when the number of repetitions is not known in advance, such as retrying input until it is valid, waiting for a game to finish, or processing data until a sentinel value arrives. A for loop is usually clearer for a fixed number of iterations.",
        "pitfall": "If the condition never becomes false, the loop runs forever. Make sure the loop body changes a variable used by the condition, and test the boundary case where the condition is false before the first iteration.",
        "code": "attempts = 0\nwhile attempts < 3:\n    print('Attempt', attempts + 1)\n    attempts += 1\nprint('Finished')",
        "output": "Attempt 1\nAttempt 2\nAttempt 3\nFinished",
        "exercise": "Keep asking the user for a password until they enter 'python123'. Then print 'Access granted'.",
        "expected": "Wrong passwords cause another prompt; entering python123 ends the loop and prints Access granted.",
        "quiz": [
            ("When is a while condition checked?", ["Only after the body", "Before every iteration", "Only once at program start", "After the program exits"], 1, "A while loop checks its condition before each iteration, including before the first one."),
            ("What causes an infinite while loop?", ["A condition that never becomes false", "Using print()", "Using an integer", "A loop with three iterations"], 0, "If the state never changes so the condition stays true, the loop cannot terminate naturally."),
            ("Which loop is usually clearer for exactly 10 repetitions?", ["while with a manual counter", "for with range(10)", "A recursive function only", "An if statement"], 1, "for number in range(10) expresses a known repetition count directly and avoids manual counter mistakes."),
        ],
    },
    "def & return": {
        "concept": "functions defined with def and return",
        "purpose": "package reusable logic behind a named operation and send a result back to the caller",
        "how": "The def statement creates a function and its indented body runs only when the function is called. Parameters receive input values. return immediately ends that call and passes a value back; print displays text but does not provide a reusable result to the caller.",
        "why": "Functions break a large problem into small testable pieces, remove duplicated code, and give each operation a clear name. A function that calculates a value should normally return it so another part of the program can store it, compare it, or pass it to another function.",
        "pitfall": "Forgetting return makes a function return None. Printing a result is not the same as returning it. Also remember that code after a return in the same function call is unreachable.",
        "code": "def calculate_total(price, quantity):\n    total = price * quantity\n    return total\n\namount = calculate_total(25, 3)\nprint(amount)",
        "output": "75",
        "exercise": "Write a function called is_even(number) that returns True for even integers and False for odd integers. Call it with 8 and 7.",
        "expected": "The calls return True and False; print(is_even(8)) and print(is_even(7)) display True then False.",
        "quiz": [
            ("Which keyword sends a value back from a function?", ["print", "return", "def", "yield only"], 1, "return ends the current function call and provides its value to the caller."),
            ("What does a function return if execution reaches the end without return?", ["0", "False", "None", "An empty string"], 2, "Python functions implicitly return None when no return statement supplies a value."),
            ("What is the difference between print(result) and return result?", ["They are identical", "print displays; return passes a value to the caller", "return only works with strings", "print ends the function"], 1, "Printing is a side effect for display, while returning makes the value available to the calling code."),
        ],
    },
    "Nested Conditionals": {
        "concept": "nested conditionals",
        "purpose": "evaluate a second decision only after an outer condition has been satisfied",
        "how": "A nested if is an if statement inside another if or else suite. Python evaluates the outer condition first; only when that branch runs does it evaluate the inner condition. Indentation shows which decision owns each block.",
        "why": "Nested decisions model dependent rules, such as checking account status before checking a withdrawal limit. Use them when the second question makes sense only after the first is true. If nesting becomes deep, combine conditions or extract a helper function to keep the logic readable.",
        "pitfall": "Incorrect indentation can attach an else to the wrong if. Deep nesting is also difficult to reason about. Trace the outer decision first, then evaluate the inner one only on paths where it is reached.",
        "code": "logged_in = True\nbalance = 500\nif logged_in:\n    if balance >= 100:\n        print('Withdrawal allowed')\n    else:\n        print('Insufficient funds')\nelse:\n    print('Please log in')",
        "output": "Withdrawal allowed",
        "exercise": "Check whether a user is logged in first. If so, check whether their score is at least 40 and print Pass or Fail. Otherwise print Login required.",
        "expected": "A logged-in user with score 55 gets Pass; a logged-out user gets Login required.",
        "quiz": [
            ("When does an inner if statement execute?", ["Whenever the file is imported", "Only when its containing outer branch executes", "Before the outer condition", "Only after else"], 1, "The inner statement is part of the outer suite, so it is reached only when that suite runs."),
            ("What most directly defines a nested block in Python?", ["Curly braces", "Indentation", "Semicolons", "Parentheses"], 1, "Python uses consistent indentation to group statements into suites and nested suites."),
            ("What is a good way to simplify deeply nested conditions?", ["Add more indentation levels", "Combine clear conditions or extract a function", "Remove all conditions", "Replace every if with while"], 1, "Combining related checks or extracting a named function can make decision logic easier to read and test."),
        ],
    },
    "Ternary Expression": {
        "concept": "the conditional expression, often called the ternary expression",
        "purpose": "choose one of two values inside an expression",
        "how": "The expression has the form value_if_true if condition else value_if_false. Python evaluates the condition and then evaluates only the selected value expression. Unlike a statement block, the result can be assigned, returned, or passed to another function.",
        "why": "Use a conditional expression for a short, simple choice such as a label or a default value. It can make assignments concise, but a normal if/else block is clearer when either branch needs multiple statements or complex logic.",
        "pitfall": "The order is different from many other languages: the true value comes before if and the false value comes after else. Do not nest several conditional expressions; readability is more important than saving lines.",
        "code": "age = 20\nstatus = 'Adult' if age >= 18 else 'Minor'\nprint(status)",
        "output": "Adult",
        "exercise": "Read an integer and assign 'Positive' when it is greater than zero, otherwise assign 'Zero or negative'. Print the label.",
        "expected": "Input 5 prints Positive; input 0 prints Zero or negative.",
        "quiz": [
            ("Which is valid Python conditional-expression syntax?", ["if condition then a else b", "a if condition else b", "a ? condition : b", "if a else b"], 1, "Python places the true expression first, followed by if condition else and the false expression."),
            ("What does a conditional expression produce?", ["A reusable function", "One selected value", "A loop", "A new variable automatically"], 1, "It evaluates to either the true-side or false-side expression, which the caller can then use."),
            ("When is a regular if/else block preferable?", ["For a short label choice", "When branches contain several statements or complex logic", "For every assignment", "Never"], 1, "A statement block is easier to read when the alternatives involve multiple steps or complicated decisions."),
        ],
    },
    "Match-Case": {
        "concept": "structural pattern matching with match and case",
        "purpose": "dispatch to a branch based on the shape or value of an object",
        "how": "A match statement evaluates its subject once and checks case patterns from top to bottom. The first matching case runs. A wildcard case written as case _ is the fallback. Python 3.10 and later support this syntax.",
        "why": "Match-case is useful for command handlers, menu choices and structured data where several distinct patterns are possible. It can match literal values, sequences and mappings, making it more expressive than a long chain of equality checks.",
        "pitfall": "Match-case is not available in Python versions earlier than 3.10. A case pattern is not a general Boolean expression; use a guard with if when an additional condition is required. Put specific patterns before broad patterns.",
        "code": "command = 'start'\nmatch command:\n    case 'start':\n        print('Starting')\n    case 'stop':\n        print('Stopping')\n    case _: \n        print('Unknown command')",
        "output": "Starting",
        "exercise": "Use match-case to handle the commands add, remove and list. Print a useful message for each and use a wildcard case for unknown commands.",
        "expected": "The command add prints Add item; remove prints Remove item; an unknown command prints Unknown command.",
        "quiz": [
            ("Which Python version introduced match-case?", ["3.7", "3.8", "3.10", "2.7"], 2, "Structural pattern matching became part of Python in version 3.10."),
            ("What does case _ represent?", ["A syntax error", "A wildcard fallback pattern", "A loop variable", "A string literal"], 1, "The underscore wildcard matches any subject that was not matched by an earlier case."),
            ("How can a case add an extra Boolean condition?", ["Use a guard with if", "Use while", "Add a second match keyword", "Use elif inside the pattern"], 0, "A guard such as case value if value > 0 adds a Boolean condition to a matching pattern."),
        ],
    },
    "for...in with Lists": {
        "concept": "iterating over lists with a for loop",
        "purpose": "process each list element directly without manually managing indexes",
        "how": "A for item in items loop obtains each element from the iterable and assigns it to item for one iteration. The loop ends when the iterable is exhausted. If an index is also needed, enumerate(items) yields index-value pairs.",
        "why": "Direct iteration is the clearest way to total values, validate entries, transform data or print each item. It avoids off-by-one errors and is easier to read than range(len(items)) when the position is not needed.",
        "pitfall": "Do not modify the list's size while iterating over it unless you deliberately manage the consequences. If you need both a position and a value, use enumerate rather than maintaining a separate counter.",
        "code": "prices = [10, 20, 15]\ntotal = 0\nfor price in prices:\n    total += price\nprint(total)\nfor index, price in enumerate(prices):\n    print(index, price)",
        "output": "45\n0 10\n1 20\n2 15",
        "exercise": "Iterate over a list of five marks, calculate the total and count how many marks are at least 40.",
        "expected": "For [35, 60, 40, 25, 80], the total is 240 and the passing count is 3.",
        "quiz": [
            ("What does for item in values assign to item?", ["The list index only", "Each element in turn", "The whole list every time", "The list length"], 1, "A for loop iterates over an iterable and binds each yielded element to the loop variable."),
            ("Which built-in gives both index and value?", ["range", "enumerate", "len", "sum"], 1, "enumerate produces pairs containing the current index and corresponding element."),
            ("Why is direct list iteration often preferred to range(len(items))?", ["It is always faster", "It avoids unnecessary index management", "It sorts the list", "It copies every element"], 1, "When the index is not needed, iterating over values communicates intent and avoids manual indexing."),
        ],
    },
    "List Comprehensions": {
        "concept": "list comprehensions",
        "purpose": "build a new list by transforming or filtering an iterable in one expression",
        "how": "A list comprehension has the form [expression for item in iterable if condition]. Python visits each item, optionally filters it with the condition, evaluates the expression for accepted items, and stores the results in a new list.",
        "why": "Comprehensions are concise for simple transformations such as squaring numbers, extracting names, or filtering positive values. They replace a short loop that appends to a new list. Use a normal loop when the logic has several steps or side effects.",
        "pitfall": "The expression comes before the for clause, which can feel backwards at first. Avoid deeply nested comprehensions and do not use them just to call functions for side effects; a normal for loop is clearer for that job.",
        "code": "numbers = [1, 2, 3, 4, 5, 6]\nsquares_of_evens = [n * n for n in numbers if n % 2 == 0]\nprint(squares_of_evens)",
        "output": "[4, 16, 36]",
        "exercise": "Given a list of words, build a new list containing the lowercase versions of words longer than four characters.",
        "expected": "For ['Tree', 'Python', 'SQL', 'Backend'], the result is ['python', 'backend'].",
        "quiz": [
            ("In [n * n for n in numbers], what is n * n?", ["The filter", "The output expression", "The iterable", "The list name"], 1, "The expression before the for clause determines the value added to the resulting list."),
            ("Where does a filter condition appear?", ["Before the opening bracket", "After the iterable with if", "After a semicolon", "Inside print"], 1, "A comprehension filter is written after the for clause, such as for n in numbers if n > 0."),
            ("When should a normal for loop be preferred?", ["For a simple one-step mapping", "When logic has multiple steps or side effects", "For every list", "When creating any list"], 1, "A regular loop is easier to follow when the operation is complex or performs side effects."),
        ],
    }
}


def get_python_core_lesson(lesson_title: str) -> Dict[str, Any] | None:
    """Return authored content for selected high-frequency Python concepts."""
    title = str(lesson_title or "").strip().lower()
    profile = next(
        (value for key, value in _PYTHON_CORE.items() if key.lower() in title),
        None,
    )
    if profile is None:
        return None

    concept = profile["concept"]
    theory = (
        f"{concept.capitalize()} is a core Python control-flow building block. "
        f"It is used to {profile['purpose']}. {profile['how']} {profile['why']} "
        f"Understanding the execution rule matters more than memorising a syntax shape: "
        f"trace the values, predict the branch or iteration, then verify the result by running "
        f"a small example. {profile['pitfall']}"
    )
    sections = [
        {
            "heading": f"What {concept} does",
            "body": f"{profile['how']} This is the execution model to keep in mind when tracing a program line by line.",
            "code": profile["code"],
            "pro_tip": "Before running the code, write down the values and predict which lines execute. Then compare your prediction with the actual output.",
        },
        {
            "heading": "When and why to use it",
            "body": f"{profile['why']} Choose the construct that best communicates the problem: conditions select a path, loops repeat work, and functions package reusable operations.",
            "code": profile["code"],
            "pro_tip": "Prefer the simplest control structure that expresses the requirement. Clear code is easier to debug in interviews and in production.",
        },
        {
            "heading": "Common edge cases",
            "body": f"{profile['pitfall']} Test the normal case, the boundary case, and an unexpected input. These checks expose off-by-one errors, incorrect comparisons, and missing termination conditions.",
            "pro_tip": "Use small inputs first. A three-item example is often enough to reveal a faulty condition or loop update.",
        },
    ]
    quizzes = [
        {
            "question": question,
            "options": options,
            "correct": correct,
            "explanation": explanation,
        }
        for question, options, correct, explanation in profile["quiz"]
    ]
    return {
        "theory": theory,
        "analogy": (
            f"Think of {concept} as a clearly labelled instruction in a recipe: it tells the "
            "computer when to take a path, repeat a step, or perform a reusable operation."
        ),
        "sections": sections,
        "code_example": {
            "code": profile["code"],
            "annotations": [
                {"line": index + 1, "text": "Read this line and connect it to the execution rule described above."}
                for index, _line in enumerate(profile["code"].splitlines())
            ],
        },
        "common_mistakes": [
            {
                "mistake": profile["pitfall"],
                "fix": "Trace the condition and state changes with a small input, then test the boundary case.",
            },
            {
                "mistake": "Memorising syntax without checking what values are evaluated at runtime.",
                "fix": "Dry-run the example line by line and explain why each branch or iteration executes.",
            },
        ],
        "exercises": [
            {
                "description": profile["exercise"],
                "starter_code": "# Write your solution here",
                "hints": [
                    "Identify the input and the expected result before writing code.",
                    "Use the execution rule from the lesson and test one normal case.",
                    "Test a boundary or alternate case before submitting.",
                ],
                "expected_output": profile["expected"],
            },
            {
                "description": f"Create a second small program that uses {concept} to solve a different everyday problem. Explain why this construct is appropriate.",
                "starter_code": "# Define your own example and test it",
                "hints": [
                    "Choose a small, concrete input.",
                    "Keep the logic focused on one responsibility.",
                    "Explain the result in a comment or short note.",
                ],
                "expected_output": "A working program with a clearly explained result for at least two test inputs.",
            },
        ],
        "quizzes": quizzes,
        "key_takeaways": [
            profile["purpose"].capitalize(),
            profile["how"],
            profile["pitfall"],
            "Trace execution and test normal, boundary, and alternate inputs.",
        ],
        "next_steps": "Complete both exercises, answer the quiz, and explain the execution rule without looking at the lesson.",
    }
