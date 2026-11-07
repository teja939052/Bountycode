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
    },
    "Lists Basics": {
        "concept": "Python lists",
        "purpose": "store an ordered, mutable collection of values",
        "how": "A list is created with square brackets and keeps elements in insertion order. Indexing starts at zero, negative indexes count from the end, and len() returns the number of elements. Lists can contain repeated values and can be changed after creation.",
        "why": "Lists are useful when a program must keep a sequence such as marks, names, prices or tasks. You can access one element by index, loop over every value, and build a result collection as input is processed.",
        "pitfall": "The last valid index is len(items) - 1, not len(items). Indexing an empty list or beyond its bounds raises IndexError. Assignment to one list element changes the existing list rather than creating a new list.",
        "code": "marks = [78, 91, 64]\nprint(marks[0])\nprint(marks[-1])\nprint(len(marks))\nmarks[1] = 95\nprint(marks)",
        "output": "78\n64\n3\n[78, 95, 64]",
        "exercise": "Create a list of five subject marks. Print the first and last marks, update the second mark, and print the updated list.",
        "expected": "For [70, 80, 90, 60, 85], the first mark is 70, last is 85, and after updating index 1 to 88 the list is [70, 88, 90, 60, 85].",
        "quiz": [
            ("What is the index of the first list element?", ["0", "1", "-1", "len(list)"], 0, "Python uses zero-based indexing, so the first element is at index zero."),
            ("What does marks[-1] access?", ["The first element", "The last element", "The list length", "An invalid index always"], 1, "A negative index counts from the end; -1 refers to the final element."),
            ("What happens when marks[1] = 95 executes?", ["A new list is always created", "The second element is replaced", "The list is sorted", "The list becomes a string"], 1, "Lists are mutable, so assigning to a valid index replaces that element in the existing list."),
        ],
    },
    "List Methods": {
        "concept": "list methods",
        "purpose": "add, remove, locate and reorder elements in a list",
        "how": "append(value) adds one item to the end, extend(iterable) adds each item from another iterable, insert(index, value) adds at a position, remove(value) removes the first matching value, and pop(index) removes and returns an item. sort() changes the list in place.",
        "why": "List methods provide the standard operations needed for dynamic collections: collecting input, processing queues, removing completed tasks and ordering results. Choose pop when you need the removed value; choose remove when you know the value to delete.",
        "pitfall": "append([1, 2]) adds one nested list, while extend([1, 2]) adds two elements. remove raises ValueError when the value is absent. Methods such as sort() mutate the list and return None, so do not assign their return value back to the list.",
        "code": "tasks = ['study', 'code']\ntasks.append('revise')\ntasks.insert(1, 'class')\nremoved = tasks.pop()\nprint(tasks)\nprint(removed)",
        "output": "['study', 'class', 'code']\nrevise",
        "exercise": "Start with a list of three tasks. Append a fourth, insert one at index 1, remove one completed task with pop(), and display both the remaining list and removed task.",
        "expected": "The remaining list contains the three unremoved tasks in their updated order, and the popped task is printed separately.",
        "quiz": [
            ("Which method adds one item to the end?", ["insert", "append", "remove", "sort"], 1, "append(value) adds its argument as one new element at the end of the list."),
            ("What is the key difference between append([3, 4]) and extend([3, 4])?", ["There is no difference", "append adds one list; extend adds its elements", "extend sorts the list", "append removes elements"], 1, "append stores the supplied list as a nested element, while extend iterates and adds each value."),
            ("What does pop() return?", ["The list length", "The removed element", "None always", "A sorted copy"], 1, "pop removes and returns the element at the selected index, or the last element by default."),
        ],
    },
    "Slicing": {
        "concept": "sequence slicing",
        "purpose": "extract a subsequence using start, stop and step positions",
        "how": "A slice uses sequence[start:stop:step]. The start index is included and stop is excluded. Omitting start or stop uses the relevant boundary, and a negative step can traverse the sequence backwards. Slicing creates a new list for list inputs.",
        "why": "Slicing is useful for selecting a page of results, taking the first few values, splitting a sequence into sections, or reversing a sequence. It often replaces manual index loops with a concise expression.",
        "pitfall": "The stop index is exclusive, which is the main source of off-by-one mistakes. A slice that extends beyond the sequence boundary is allowed and is clipped; direct indexing beyond the boundary raises IndexError.",
        "code": "values = [10, 20, 30, 40, 50]\nprint(values[1:4])\nprint(values[:3])\nprint(values[::2])\nprint(values[::-1])",
        "output": "[20, 30, 40]\n[10, 20, 30]\n[10, 30, 50]\n[50, 40, 30, 20, 10]",
        "exercise": "Given a list of ten values, create a list of the first five, a list of the last three, and a reversed copy without changing the original.",
        "expected": "For [1,2,3,4,5,6,7,8,9,10], the slices are [1,2,3,4,5], [8,9,10], and [10,9,8,7,6,5,4,3,2,1].",
        "quiz": [
            ("Is the stop index included in a slice?", ["Yes", "No", "Only for strings", "Only when step is 1"], 1, "Slice stop positions are exclusive, so the element at the stop index is not included."),
            ("What does values[::-1] do?", ["Sorts values", "Creates a reversed slice", "Removes the first item", "Returns the length"], 1, "A step of -1 traverses the sequence from the end toward the beginning."),
            ("What happens with values[2:100] when the list is shorter than 100 elements?", ["It always raises IndexError", "The slice ends at the available boundary", "It pads the list", "It deletes elements"], 1, "Slicing clips out-of-range boundaries rather than raising the indexing error used by direct access."),
        ],
    },
    "String Slicing": {
        "concept": "string slicing",
        "purpose": "extract parts of text using character positions",
        "how": "Strings support the same start:stop:step slicing syntax as lists. The start position is included and stop is excluded. Negative indexes count from the end, and a negative step can reverse the characters. Because strings are immutable, slicing returns a new string.",
        "why": "String slicing is useful for extracting prefixes, suffixes, file extensions, identifiers and fixed-width fields. It is common in coding exercises involving palindromes, parsing and text transformations.",
        "pitfall": "The stop index is exclusive. Slicing beyond the end is safe and returns the available characters, but direct indexing beyond the end raises IndexError. Remember that slicing does not alter the original string.",
        "code": "code = 'BOUNTYCODE'\nprint(code[:6])\nprint(code[-4:])\nprint(code[::2])\nprint(code[::-1])",
        "output": "BOUNTY\nCODE\nBUTCD\nEDOCYTNUOB",
        "exercise": "Read a word and print its first three characters, last two characters, and reversed form. Handle words shorter than three characters without crashing.",
        "expected": "For Python, the outputs are Pyt, on and nohtyP; short words return the available slice without an indexing error.",
        "quiz": [
            ("What does text[:3] select?", ["Characters at indexes 0, 1 and 2", "Indexes 1, 2 and 3", "The final three characters", "The entire string"], 0, "The start defaults to zero and the stop is exclusive, so indexes zero through two are selected."),
            ("What does text[::-1] return?", ["The original text", "The reversed text", "The first character", "An empty string"], 1, "A step of negative one traverses the string from the last character to the first."),
            ("Does slicing change the original string?", ["Yes, strings are mutable", "No, strings are immutable and slicing returns a new string", "Only for uppercase text", "Only when the step is one"], 1, "Python strings are immutable, so slicing creates a new string value rather than modifying the original."),
        ],
    },
    "dict Basics": {
        "concept": "Python dictionaries",
        "purpose": "map unique keys to associated values for fast lookup",
        "how": "A dictionary stores key-value pairs inside braces. Access a value with data[key], add or update it with data[key] = value, and use get(key, default) when a missing key should return a fallback instead of raising KeyError. Keys must be hashable.",
        "why": "Dictionaries model records and lookups such as a student's name and marks, product prices, configuration settings, or counts by category. A meaningful key makes data easier to retrieve than searching through parallel lists.",
        "pitfall": "Accessing a missing key with square brackets raises KeyError; use get when absence is expected. Keys must be hashable, so lists cannot be dictionary keys. Assigning an existing key replaces its value rather than creating a duplicate key.",
        "code": "student = {'name': 'Asha', 'marks': 88}\nstudent['branch'] = 'CSE'\nprint(student['name'])\nprint(student.get('grade', 'Not assigned'))\nprint(student)",
        "output": "Asha\nNot assigned\n{'name': 'Asha', 'marks': 88, 'branch': 'CSE'}",
        "exercise": "Create a dictionary for a student with name, roll number and marks. Add a branch key, update marks, and safely read a missing email key with a default.",
        "expected": "The dictionary contains the updated marks and branch; the missing email lookup displays Not provided.",
        "quiz": [
            ("What does a dictionary store?", ["Only ordered indexes", "Key-value pairs", "Only unique values without keys", "A fixed-size array"], 1, "A dictionary maps each unique key to a value so the value can be retrieved by its key."),
            ("What happens when data['missing'] is read for an absent key?", ["Returns None", "Raises KeyError", "Adds the key automatically", "Returns an empty list"], 1, "Square-bracket lookup raises KeyError if the requested key does not exist."),
            ("Which method safely supplies a default for a missing key?", ["append", "get", "popitem only", "sort"], 1, "get(key, default) returns the stored value or the supplied default without raising KeyError."),
        ],
    },
    "dict Methods": {
        "concept": "dictionary methods",
        "purpose": "inspect, update, merge and safely remove key-value pairs",
        "how": "keys() exposes keys, values() exposes values, and items() exposes key-value pairs for iteration. update(other) merges entries, setdefault(key, default) inserts a default only when absent, and pop(key) removes and returns a value.",
        "why": "These methods make dictionaries practical for counting, aggregation, configuration updates and transforming structured records. items() is especially useful when both a key and its value are needed in the same loop.",
        "pitfall": "Do not assume a missing key can be removed with pop() without handling the error; pass a default when absence is normal. Avoid changing dictionary size while iterating over its live views; iterate over a list copy if mutation is required.",
        "code": "scores = {'Asha': 80, 'Ravi': 75}\nscores.update({'Ravi': 82, 'Mina': 91})\nfor name, score in scores.items():\n    print(name, score)\nremoved = scores.pop('Asha')\nprint('Removed', removed)",
        "output": "Asha 80\nRavi 82\nMina 91\nRemoved 80",
        "exercise": "Build a dictionary of three product prices. Update one price, add a fourth product, print every product and price using items(), then remove one product safely.",
        "expected": "The output shows the updated four-entry dictionary before removal and confirms the removed product's price.",
        "quiz": [
            ("Which method yields key-value pairs?", ["keys()", "values()", "items()", "clear()"], 2, "items() provides pairs that can be unpacked into a key variable and a value variable."),
            ("What does update() do when a key already exists?", ["Raises an error", "Replaces its value", "Creates a duplicate key", "Deletes the dictionary"], 1, "update merges mappings and overwrites values for keys that are already present."),
            ("Why might pop(key, default) be useful?", ["It sorts the keys", "It avoids an error when the key is absent", "It copies the dictionary", "It freezes the mapping"], 1, "Providing a default lets the program handle a missing key without an exception."),
        ],
    },
    "String Methods Deep": {
        "concept": "Python string methods",
        "purpose": "inspect, clean, search and transform text",
        "how": "Strings are immutable sequences of Unicode characters. Methods such as lower(), upper(), strip(), replace(), split() and join() return new strings or lists rather than changing the original string. find() returns an index or -1 when a substring is absent.",
        "why": "Text processing appears in input validation, log analysis, CSV cleanup, search and placement coding questions. Normalising case and removing surrounding whitespace before comparing input makes programs more robust.",
        "pitfall": "Calling strip() or lower() without storing the returned value does not modify the original string. split() returns a list, while join() is called on the separator string. Do not confuse find() returning -1 with an exception.",
        "code": "raw = '  Python,SQL,Java  '\nclean = raw.strip().lower()\nskills = clean.split(',')\nprint(skills)\nprint(' | '.join(skills))",
        "output": "['python', 'sql', 'java']\npython | sql | java",
        "exercise": "Read a comma-separated line of skills, remove surrounding spaces, normalise each skill to lowercase, and print the cleaned skills separated by ' | '.",
        "expected": "Input ' Python, SQL, Java ' prints python | sql | java.",
        "quiz": [
            ("Are Python strings mutable?", ["Yes, characters can be changed in place", "No, string methods return new values", "Only when they contain numbers", "Only inside functions"], 1, "Strings are immutable; operations such as replace and lower return new string values."),
            ("What does strip() remove by default?", ["Every space in the string", "Whitespace at both ends", "All commas", "The first character only"], 1, "strip removes leading and trailing whitespace while preserving spaces inside the text."),
            ("What type does split(',') return?", ["A dictionary", "A list of strings", "An integer", "A tuple of numbers"], 1, "split divides the string around the separator and returns a list containing the resulting pieces."),
        ],
    },
    "f-strings & Formatting": {
        "concept": "f-strings and formatted output",
        "purpose": "embed expressions and format values clearly inside strings",
        "how": "An f-string begins with f or F before its quote. Expressions inside curly braces are evaluated and converted to text. A format specifier after a colon controls presentation, such as :.2f for two decimal places or :>10 for right alignment in a field of width ten.",
        "why": "Formatted strings make reports, receipts, tables and debugging output easier to read. They are often clearer than concatenating strings and converting each value manually.",
        "pitfall": "The f prefix is required for expressions inside braces to be evaluated. Literal braces must be doubled as {{ and }}. Formatting changes how a value is displayed; it does not change the underlying numeric value.",
        "code": "name = 'Asha'\nscore = 87.456\nprint(f'{name} scored {score:.2f}%')\nprint(f'|{name:>10}|')",
        "output": "Asha scored 87.46%\n|      Asha|",
        "exercise": "Read a student's name and marks as a decimal number. Print a sentence with the name and marks rounded to exactly two decimal places.",
        "expected": "Input Asha and 91.5 prints Asha scored 91.50 marks.",
        "quiz": [
            ("Which prefix enables expression interpolation?", ["r", "b", "f", "u"], 2, "The f prefix marks a formatted string so expressions inside braces are evaluated."),
            ("What does :.2f specify?", ["Two integer digits", "Two digits after the decimal point", "Two spaces before the value", "A hexadecimal value"], 1, "The .2f format specifier displays a floating-point value with two digits after the decimal point."),
            ("How do you display a literal brace inside an f-string?", ["Use a backslash", "Double it as {{ or }}", "Use square brackets", "It is impossible"], 1, "Doubled braces escape interpolation and render as a single literal brace."),
        ],
    },
    "try / except / finally": {
        "concept": "exception handling with try, except and finally",
        "purpose": "handle expected runtime failures without crashing the entire program",
        "how": "Python executes the try suite first. If an exception occurs, control moves to the first matching except suite. The optional else suite runs only when no exception occurred, and finally runs whether an exception happened or not. Catch specific exception types before broader ones.",
        "why": "Input conversion, file access and network operations can fail for reasons outside the program's control. Handling a known failure lets the program explain the problem, retry, or recover safely while keeping normal logic separate from error handling.",
        "pitfall": "A bare except catches almost everything and can hide programming bugs. Catch ValueError for invalid numeric text or FileNotFoundError for a missing file. Do not put the whole program inside one broad try block.",
        "code": "raw = '42'\ntry:\n    number = int(raw)\nexcept ValueError:\n    print('Enter a whole number')\nelse:\n    print(number * 2)\nfinally:\n    print('Conversion finished')",
        "output": "84\nConversion finished",
        "exercise": "Read text from the user and convert it to an integer. Catch ValueError and print Invalid number; use finally to print Input check complete.",
        "expected": "Input 12 prints 12 and Input check complete; input abc prints Invalid number and Input check complete.",
        "quiz": [
            ("Which block handles a matching exception?", ["try", "except", "else", "finally"], 1, "An except clause handles an exception whose type matches the exception raised in the try suite."),
            ("When does finally execute?", ["Only after an error", "Only when there is no error", "Whether or not an exception occurred", "Only when return is used"], 2, "finally is designed for cleanup and runs whether the try suite succeeds or raises an exception."),
            ("Why should code catch ValueError instead of using bare except?", ["It makes the program faster always", "It handles the expected failure without hiding unrelated bugs", "It prevents all exceptions", "It changes input into an integer"], 1, "Specific exception handling makes recovery intentional and allows unexpected programming errors to remain visible."),
        ],
    },
    "Custom Exceptions": {
        "concept": "custom exception classes",
        "purpose": "represent domain-specific errors with meaningful exception types",
        "how": "A custom exception is normally a class that inherits from Exception. Raise an instance when a domain rule is violated, then catch that specific type where the program can respond. Exception names conventionally end with Error.",
        "why": "Built-in exceptions describe general technical failures, while custom exceptions can express business rules such as insufficient funds, invalid booking state or an unavailable inventory item. Callers can handle these cases without parsing message strings.",
        "pitfall": "Do not inherit directly from BaseException for ordinary application errors; inherit from Exception. Keep exception classes small and raise them only when a real error condition occurs.",
        "code": "class InsufficientFundsError(Exception):\n    pass\n\ndef withdraw(balance, amount):\n    if amount > balance:\n        raise InsufficientFundsError('Balance too low')\n    return balance - amount\n\ntry:\n    print(withdraw(100, 150))\nexcept InsufficientFundsError as error:\n    print(error)",
        "output": "Balance too low",
        "exercise": "Create an InvalidAgeError and a function that rejects ages below zero. Raise your custom exception and catch it at the call site.",
        "expected": "A valid age returns normally; age -2 raises InvalidAgeError and the handler prints a clear validation message.",
        "quiz": [
            ("Which class should a normal custom application exception inherit from?", ["object only", "Exception", "BaseException directly", "str"], 1, "Application-specific exceptions should normally inherit from Exception so standard exception handling works as expected."),
            ("What does raise do?", ["Silently ignores an error", "Raises an exception and transfers control to a handler or caller", "Creates a loop", "Returns None"], 1, "raise signals an exceptional condition and stops normal execution of the current path."),
            ("Why use a custom exception type?", ["To avoid writing tests", "To let callers handle a domain error specifically", "To make every error identical", "To replace all built-in exceptions"], 1, "A distinct type lets callers catch a meaningful business condition without inspecting error-message text."),
        ],
    },
    "Classes & Objects": {
        "concept": "classes and objects",
        "purpose": "model related state and behaviour together in reusable types",
        "how": "A class defines a new type with attributes and methods. Calling the class creates an object, also called an instance. Each instance can hold its own state, while methods define the operations that work with that state. Use PascalCase for class names by convention.",
        "why": "Classes are useful when several values and operations belong together, such as a bank account with an owner and balance or a student with marks and grade calculation. They help organise larger programs around clear responsibilities.",
        "pitfall": "A class definition does not create an instance until it is called. Instance methods receive the instance as their first parameter, conventionally named self. Avoid placing unrelated global state inside a class just to use object-oriented syntax.",
        "code": "class Student:\n    def describe(self):\n        return f'{self.name}: {self.marks}'\n\nstudent = Student()\nstudent.name = 'Asha'\nstudent.marks = 88\nprint(student.describe())",
        "output": "Asha: 88",
        "exercise": "Create a Book class and two objects. Give each object a title and author, then write a method that returns a formatted description.",
        "expected": "The two objects retain their own title and author values and print different descriptions.",
        "quiz": [
            ("What does a class define?", ["Only one fixed object", "A blueprint for creating instances", "A loop", "A database connection always"], 1, "A class defines the attributes and behaviour that its instances can have."),
            ("What is an object created from a class called?", ["A module", "An instance", "A decorator", "An exception"], 1, "An instance is a concrete object created by calling a class."),
            ("What is self conventionally used for?", ["The class name", "The current instance inside an instance method", "A global variable", "The return value"], 1, "self refers to the current instance so a method can read or update that object's attributes."),
        ],
    },
    "__init__ & self": {
        "concept": "the __init__ constructor method and self",
        "purpose": "initialise each new object with valid starting state",
        "how": "When a class is called, Python creates an instance and then calls its __init__ method to initialise it. The first parameter is conventionally self, followed by values supplied by the caller. Assign instance attributes with self.attribute = value.",
        "why": "Initialisation ensures every object begins in a predictable state. A BankAccount can require an owner and opening balance, while a Student can require a name and roll number. This avoids creating partially configured objects and repeating setup code.",
        "pitfall": "__init__ is not the same as the object's creation method __new__, and it should normally return None. Do not omit self from an instance method. Use instance attributes for per-object values rather than accidentally sharing mutable class attributes.",
        "code": "class BankAccount:\n    def __init__(self, owner, balance=0):\n        self.owner = owner\n        self.balance = balance\n\naccount = BankAccount('Asha', 500)\nprint(account.owner, account.balance)",
        "output": "Asha 500",
        "exercise": "Create a Student class whose __init__ accepts name, roll_number and marks. Instantiate two students and print their independent details.",
        "expected": "Each student object stores the values passed to its own constructor and displays its own details.",
        "quiz": [
            ("When is __init__ called?", ["When a class file is imported only", "During instance initialisation after object creation", "Only when an object is deleted", "Before the class exists"], 1, "Python calls __init__ to initialise a newly created instance when the class is instantiated."),
            ("What does self refer to inside an instance method?", ["The current object", "The parent class only", "The module", "The next object"], 0, "self is the conventional reference to the instance whose method is currently running."),
            ("Should __init__ explicitly return the new object?", ["Yes, with return self", "No, it should return None", "Only for strings", "Only for subclasses"], 1, "__init__ initialises an already-created object and should not return a non-None value."),
        ],
    },
    "Inheritance": {
        "concept": "class inheritance",
        "purpose": "create a specialised class that reuses and extends another class",
        "how": "A child class names its parent in parentheses, such as class SavingsAccount(BankAccount). The child inherits accessible attributes and methods, can add new methods, and can override inherited behaviour. super() provides access to the parent implementation.",
        "why": "Inheritance models a genuine is-a relationship and can reduce duplication when specialised types share stable behaviour. For example, SavingsAccount is a kind of BankAccount and may add interest calculation while retaining deposit and withdrawal operations.",
        "pitfall": "Do not use inheritance only to share a few unrelated helper functions; composition may be clearer. If a child defines __init__, call super().__init__(...) when the parent needs to initialise its state.",
        "code": "class Animal:\n    def __init__(self, name):\n        self.name = name\n\n    def speak(self):\n        return 'Some sound'\n\nclass Dog(Animal):\n    def speak(self):\n        return 'Woof'\n\ndog = Dog('Milo')\nprint(dog.name, dog.speak())",
        "output": "Milo Woof",
        "exercise": "Create a Vehicle parent class with a brand attribute and a describe method. Create a Car child class that adds a model and reuses the parent initialisation.",
        "expected": "A Car instance should expose both brand and model and return a description containing both.",
        "quiz": [
            ("How does a child class declare its parent?", ["class Child extends Parent", "class Child(Parent)", "def Child: Parent", "import Parent as Child"], 1, "Python lists one or more base classes in parentheses after the child class name."),
            ("What does super() commonly provide?", ["A random object", "Access to the next class implementation in the method resolution order", "A global variable", "A new module"], 1, "super() delegates to the next implementation in the method resolution order, commonly the parent method."),
            ("When is inheritance a good fit?", ["Whenever two classes have any shared text", "When the child is genuinely a specialised kind of the parent", "For every helper function", "To avoid all composition"], 1, "Inheritance is most appropriate when the child can be understood as a specialised form of the parent type."),
        ],
    },
    "Polymorphism": {
        "concept": "polymorphism through shared interfaces",
        "purpose": "call the same operation on different object types and let each type provide its own behaviour",
        "how": "Polymorphism means code can work with different objects through a common operation such as speak() or calculate_area(). Python supports this through method overriding and duck typing: an object is usable when it provides the behaviour the caller needs.",
        "why": "Polymorphism reduces branching in code that handles related objects. A report generator can call render() on HTML, PDF and text report objects without checking each concrete class before every call.",
        "pitfall": "Objects used polymorphically must honour the expected method contract. If one implementation returns a different kind of value or raises surprising errors, callers become fragile. Prefer clear method names and consistent return types.",
        "code": "class Dog:\n    def speak(self):\n        return 'Woof'\n\nclass Cat:\n    def speak(self):\n        return 'Meow'\n\nfor animal in [Dog(), Cat()]:\n    print(animal.speak())",
        "output": "Woof\nMeow",
        "exercise": "Create EmailNotification and SMSNotification classes with a send(message) method. Store both objects in a list and call send on each without checking its class.",
        "expected": "The same loop sends the message through both implementations, each producing its own channel-specific output.",
        "quiz": [
            ("What is the central idea of polymorphism?", ["One operation can work with different object types", "Every class must have identical data", "Objects cannot have methods", "Only one object can exist"], 0, "Polymorphism lets callers use a common operation while each object supplies the appropriate implementation."),
            ("What is duck typing?", ["Checking an object's exact class every time", "Using an object based on the behaviour it provides", "Converting all objects to strings", "A type of loop"], 1, "Duck typing focuses on whether an object supports the required operations rather than its declared class."),
            ("Why should polymorphic implementations share a consistent contract?", ["To make code longer", "So callers can rely on predictable behaviour and return values", "To prevent overriding", "To avoid methods"], 1, "A consistent contract allows the calling code to use different implementations safely."),
        ],
    }
}


def get_python_core_lesson(lesson_title: str) -> Dict[str, Any] | None:
    """Return authored content for selected high-frequency Python concepts."""
    title = str(lesson_title or "").strip().lower()
    matching_profiles = [
        (len(key), value)
        for key, value in _PYTHON_CORE.items()
        if key.lower() in title
    ]
    profile = max(matching_profiles, key=lambda item: item[0])[1] if matching_profiles else None
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
