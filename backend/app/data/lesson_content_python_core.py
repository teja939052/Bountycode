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
