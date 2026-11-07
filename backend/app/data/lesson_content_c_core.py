"""Authored C placement-fundamentals lesson profiles."""
from __future__ import annotations

from typing import Any, Dict

from app.data.lesson_content_authored_builder import build_authored_lesson


_C_CORE: Dict[str, Dict[str, Any]] = {
    "if Statement": {
        "concept": "if selection",
        "purpose": "execute a statement block only when a condition is true",
        "how": "C evaluates the expression inside parentheses; zero is false and non-zero is true. If the condition is true, the controlled statement runs. Braces group multiple statements into one block and are recommended even when the block contains one statement.",
        "why": "Conditions express validation and decision rules such as checking eligibility, comparing marks and deciding whether a value is positive.",
        "pitfall": "Use == for comparison and = for assignment. A semicolon immediately after if(condition) creates an empty controlled statement. Use braces consistently and initialise variables before reading them.",
        "code": "#include <stdio.h>\nint main(void) {\n    int temperature = 32;\n    if (temperature > 30) {\n        printf(\"Hot\\n\");\n    }\n    printf(\"Check complete\\n\");\n    return 0;\n}",
        "expected": "Hot followed by Check complete.",
        "exercise": "Read an integer and print Positive only when it is greater than zero. Always print Check complete after the condition.",
        "expected2": "Input 5 prints Positive and Check complete; input 0 prints only Check complete.",
        "quiz": [
            ("In C, which value is treated as false in a condition?", ["Any non-zero value", "Zero", "Only -1", "Only NULL"], 1, "C treats zero as false and any non-zero scalar value as true in a condition."),
            ("Which operator compares two values for equality?", ["=", "==", "!=", "&&"], 1, "The == operator compares values; a single equals sign assigns a value."),
            ("What does a semicolon after if(condition) do?", ["Starts the block", "Creates an empty controlled statement", "Adds an else", "Declares a variable"], 1, "The semicolon is a complete empty statement, so a following block is not controlled by the if."),
        ],
    },
    "if-else Statement": {
        "concept": "if-else selection",
        "purpose": "choose between two alternative execution paths",
        "how": "C evaluates the if condition once. A true condition executes the if statement; otherwise the else statement executes. Both branches may be compound statements enclosed in braces. Exactly one branch is selected.",
        "why": "Use if-else when every input should receive one of two outcomes, such as even/odd, pass/fail or accepted/rejected.",
        "pitfall": "The else binds to the nearest unmatched if. Use braces and indentation to make nesting clear. Do not put a condition after else; use else if for additional alternatives.",
        "code": "#include <stdio.h>\nint main(void) {\n    int marks = 72;\n    if (marks >= 40) {\n        printf(\"Pass\\n\");\n    } else {\n        printf(\"Fail\\n\");\n    }\n    return 0;\n}",
        "expected": "Pass",
        "exercise": "Read an integer and print Even if it is divisible by two, otherwise print Odd.",
        "expected2": "Input 14 prints Even; input 9 prints Odd.",
        "quiz": [
            ("Which branch executes when the if condition is false?", ["if", "else", "Both", "Neither always"], 1, "The else branch is the alternative path selected when the if condition evaluates to false."),
            ("How do you add a third condition in C?", ["else if", "else(condition)", "elseif()", "case if"], 0, "C supports else if as a nested if in the else branch."),
            ("What does n % 2 == 0 check?", ["n is odd", "n is even", "n is negative", "n is zero only"], 1, "An even integer has remainder zero when divided by two."),
        ],
    },
    "for Loop": {
        "concept": "counted for loops",
        "purpose": "repeat a block using initialisation, a condition and an update",
        "how": "A for loop has three parts: initialisation runs once, the condition is checked before each iteration, and the update runs after the body. The loop ends when the condition becomes false. The body may be a single statement or a braced block.",
        "why": "Use for loops when the repetition count is known, such as processing an array, generating a table or accumulating a total.",
        "pitfall": "Check whether the upper bound is inclusive. An off-by-one condition can skip an element or access outside an array. Ensure the update moves the loop toward termination.",
        "code": "#include <stdio.h>\nint main(void) {\n    int total = 0;\n    for (int i = 1; i <= 5; ++i) {\n        total += i;\n    }\n    printf(\"%d\\n\", total);\n    return 0;\n}",
        "expected": "15",
        "exercise": "Read n and print its multiplication table from 1 through 10 using a for loop.",
        "expected2": "For n=4, the first result is 4 and the final result is 40.",
        "quiz": [
            ("How many times does for(int i=0; i<5; i++) execute?", ["4", "5", "6", "Infinite"], 1, "The loop visits indexes 0 through 4, so it executes five times."),
            ("When does the update expression run?", ["Before initialisation", "After the loop body", "Only at program exit", "Before the first condition"], 1, "The update executes after the body and before the next condition check."),
            ("What is a common result of a wrong loop boundary?", ["Automatic resizing", "Off-by-one or out-of-bounds errors", "A new function", "A type conversion"], 1, "Incorrect boundaries can skip required work or access memory outside the intended range."),
        ],
    },
    "while Loop": {
        "concept": "while loops",
        "purpose": "repeat a block while a condition remains true",
        "how": "A while loop checks its condition before each iteration. If true, the body runs and control returns to the condition. If false initially, the body does not run. The body should update state so the loop can eventually terminate.",
        "why": "Use while when the number of repetitions is not known in advance, such as reading values until a sentinel or retrying input until it is valid.",
        "pitfall": "A missing update can create an infinite loop. Check the initial condition and termination condition carefully. Use do-while only when the body must execute at least once.",
        "code": "#include <stdio.h>\nint main(void) {\n    int attempts = 0;\n    while (attempts < 3) {\n        printf(\"Attempt %d\\n\", attempts + 1);\n        ++attempts;\n    }\n    return 0;\n}",
        "expected": "Attempt 1, Attempt 2 and Attempt 3 on separate lines.",
        "exercise": "Read integers until the user enters zero. Calculate and print the sum of all non-zero values.",
        "expected2": "For inputs 4, 5, -2, 0 the sum is 7.",
        "quiz": [
            ("When is a while condition checked?", ["After every body only", "Before each iteration", "Only once", "At program exit"], 1, "The condition is evaluated before the first iteration and before every later iteration."),
            ("What happens if the loop condition never becomes false?", ["It stops after one iteration", "The loop may run indefinitely", "The compiler changes it", "It returns zero"], 1, "A while loop continues until its condition becomes false or control exits another way."),
            ("Which loop guarantees at least one body execution?", ["for", "while", "do-while", "switch"], 2, "A do-while loop checks its condition after executing the body."),
        ],
    },
    "Function Basics": {
        "concept": "C function declarations, definitions and calls",
        "purpose": "organise reusable operations with typed parameters and return values",
        "how": "A function declaration or prototype tells the compiler the function name, return type and parameter types. The definition provides the body. A function call passes arguments, executes the body and returns a value when the return type is not void.",
        "why": "Functions divide a program into small responsibilities, reduce repeated code and make logic easier to test. A clear function name communicates the operation to its caller.",
        "pitfall": "A prototype and definition must agree. A non-void function must return a value on every reachable path. In C, use void in a parameter list when a function accepts no arguments.",
        "code": "#include <stdio.h>\nint calculate_total(int price, int quantity);\nint main(void) {\n    printf(\"%d\\n\", calculate_total(25, 3));\n    return 0;\n}\nint calculate_total(int price, int quantity) {\n    return price * quantity;\n}",
        "expected": "75",
        "exercise": "Write an is_even function that accepts an int and returns 1 for even values and 0 for odd values. Call it for 8 and 7.",
        "expected2": "The function returns 1 for 8 and 0 for 7.",
        "quiz": [
            ("What is a function prototype?", ["A function call", "A declaration of the function signature", "A loop", "A variable"], 1, "A prototype declares the return type, name and parameter types before the function is used."),
            ("What does return do?", ["Only prints a value", "Ends the function and sends a value to the caller", "Starts another function", "Allocates memory"], 1, "return transfers control to the caller and optionally provides a result."),
            ("What is the correct no-argument prototype in C?", ["int run(); always means no args", "int run(void);", "void run(int);", "run(void) int;"], 1, "A void parameter list explicitly states that the function accepts no arguments in C."),
        ],
    },
    "1D Array Basics": {
        "concept": "one-dimensional arrays",
        "purpose": "store a fixed number of same-typed elements in contiguous memory",
        "how": "An array declaration such as int marks[5] reserves five integer elements. Indexes start at zero and the last valid index is length minus one. Array elements can be initialised at declaration and processed with loops.",
        "why": "Arrays are fundamental for storing marks, prices and measurements and for implementing searching, sorting and frequency-count algorithms.",
        "pitfall": "C does not automatically check array bounds. Reading an uninitialised local array element gives an indeterminate value. Access outside the array is undefined behaviour, so track the valid length explicitly.",
        "code": "#include <stdio.h>\nint main(void) {\n    int marks[5] = {70, 80, 90, 60, 85};\n    int total = 0;\n    for (int i = 0; i < 5; ++i) total += marks[i];\n    printf(\"%d %d\\n\", marks[0], total);\n    return 0;\n}",
        "expected": "70 385",
        "exercise": "Read five integers into an array and calculate the minimum, maximum and average.",
        "expected2": "For 4, 8, 2, 10, 6 the minimum is 2, maximum is 10 and average is 6.",
        "quiz": [
            ("What is the first valid index of an array in C?", ["1", "0", "-1", "Array length"], 1, "C arrays use zero-based indexing."),
            ("What is the last valid index of int values[5]?", ["5", "4", "6", "0"], 1, "Five elements are indexed from zero through four."),
            ("Does C check array bounds automatically?", ["Yes", "No", "Only for char arrays", "Only in functions"], 1, "C array indexing does not provide automatic bounds checking."),
        ],
    },
    "What are Pointers?": {
        "concept": "pointers and memory addresses",
        "purpose": "store an address so a program can indirectly access an object",
        "how": "A pointer variable stores the address of an object. The address-of operator & obtains an object's address, and the dereference operator * accesses the object through a valid pointer. A pointer's type determines how the pointed-to memory is interpreted.",
        "why": "Pointers are central to arrays, dynamic memory, linked data structures and passing data efficiently to functions. They are also a key distinction between C and many higher-level languages.",
        "pitfall": "Never dereference an uninitialised, dangling or null pointer. Initialise pointers to NULL when they do not yet point to an object, and check before dereferencing. Pointer arithmetic must remain within the same array object or one past its end.",
        "code": "#include <stdio.h>\nint main(void) {\n    int score = 88;\n    int *pointer = &score;\n    printf(\"%d\\n\", *pointer);\n    *pointer = 95;\n    printf(\"%d\\n\", score);\n    return 0;\n}",
        "expected": "88 followed by 95.",
        "exercise": "Write a function that accepts an int pointer and doubles the pointed-to value. Call it with the address of a local integer.",
        "expected2": "An initial value of 12 becomes 24 after the function call.",
        "quiz": [
            ("What does &score produce?", ["The value of score", "The address of score", "The size of score", "A null pointer"], 1, "The address-of operator produces a pointer to the named object."),
            ("What does *pointer do for a valid int pointer?", ["Gets the pointed-to integer", "Gets the pointer address", "Deletes the integer", "Changes the pointer type"], 0, "The dereference operator accesses the object stored at the address."),
            ("What should be checked before dereferencing a pointer that may be absent?", ["Whether it is NULL", "Whether it is negative", "Whether it is a float", "Whether it is global"], 0, "A null pointer does not point to a valid object and must not be dereferenced."),
        ],
    },
    "Structs": {
        "concept": "structures in C",
        "purpose": "group related fields of different types into one record",
        "how": "A struct defines a user-created record type with named members. Declare an object with struct Type or a typedef alias, access members with the dot operator, and access members through a pointer with the arrow operator. Struct values can be passed to and returned from functions.",
        "why": "Structures model records such as students, products and transactions. Grouping related data makes function interfaces clearer than passing many unrelated variables.",
        "pitfall": "A struct variable stores its members directly, while a pointer to a struct stores an address. Use -> only with a pointer. Be aware that padding may be inserted between members for alignment, so sizeof(struct) can exceed the sum of member sizes.",
        "code": "#include <stdio.h>\ntypedef struct { char name[20]; int marks; } Student;\nint main(void) {\n    Student student = {\"Asha\", 88};\n    Student *pointer = &student;\n    printf(\"%s %d\\n\", pointer->name, pointer->marks);\n    return 0;\n}",
        "expected": "Asha 88",
        "exercise": "Define a Product structure with name, quantity and price. Read or initialise two products and calculate their total inventory value.",
        "expected2": "For 3 units at 10.5 and 2 units at 20, the total inventory value is 71.5.",
        "quiz": [
            ("Which operator accesses a member through a struct object?", ["->", ".", "&", "*"], 1, "The dot operator accesses a member of a structure object."),
            ("Which operator accesses a member through a struct pointer?", [".", "->", "::", "=>"], 1, "The arrow operator is shorthand for dereferencing a struct pointer and selecting a member."),
            ("Can a struct contain fields of different types?", ["No", "Yes", "Only integers", "Only pointers"], 1, "A struct groups named members that may have different declared types."),
        ],
    },
    "Singly Linked List": {
        "concept": "singly linked lists",
        "purpose": "represent a sequence of nodes connected by pointers",
        "how": "Each node stores data and a pointer to the next node. The head pointer identifies the first node, and the final node points to NULL. Traversal follows next pointers until NULL. Insertion at the head is O(1), while searching for a value is O(n).",
        "why": "Linked lists teach pointer-based data structures and dynamic memory management. They are useful when insertions and deletions near a known node are frequent and random indexed access is not required.",
        "pitfall": "Allocate each node with enough memory, check allocation success and free every node when finished. Updating links in the wrong order can lose the rest of the list. Always handle an empty list where head is NULL.",
        "code": "#include <stdio.h>\n#include <stdlib.h>\ntypedef struct Node { int data; struct Node *next; } Node;\nint main(void) {\n    Node *head = malloc(sizeof(Node));\n    if (head == NULL) return 1;\n    head->data = 10; head->next = NULL;\n    printf(\"%d\\n\", head->data);\n    free(head);\n    return 0;\n}",
        "expected": "10",
        "exercise": "Build a three-node singly linked list, traverse it to print every value, then free all nodes.",
        "expected2": "The values print in insertion order and all allocated nodes are released.",
        "quiz": [
            ("What does the final node's next pointer contain?", ["The head always", "NULL", "Its own data", "The array length"], 1, "NULL marks the end of a singly linked list."),
            ("What is the time complexity of searching an unsorted linked list?", ["O(1)", "O(n)", "O(log n)", "O(n squared)"], 1, "In the worst case, every node must be visited."),
            ("What can happen if a node is unlinked but not freed?", ["A memory leak", "Automatic sorting", "A syntax error", "A compile-time conversion"], 0, "Allocated memory remains unavailable for reuse until it is freed."),
        ],
    },
    "Binary Search Tree": {
        "concept": "binary search trees",
        "purpose": "organise values so ordered lookup and traversal can be performed through a tree",
        "how": "Each node in a binary search tree has at most two children. Under the usual unique-key rule, values smaller than a node go left and larger values go right. Search follows one child at each comparison. In-order traversal visits keys in sorted order.",
        "why": "Binary search trees demonstrate recursive structures and ordered data. A balanced tree supports O(log n) search, insertion and deletion, while an unbalanced tree can degrade to O(n).",
        "pitfall": "The performance guarantee depends on tree height; a plain BST does not automatically balance itself. Define how duplicate keys are handled and free every node. Recursive functions must handle NULL child pointers as base cases.",
        "code": "#include <stdio.h>\ntypedef struct Node { int value; struct Node *left, *right; } Node;\nvoid inorder(Node *root) {\n    if (root == NULL) return;\n    inorder(root->left);\n    printf(\"%d \", root->value);\n    inorder(root->right);\n}\nint main(void) { inorder(NULL); return 0; }",
        "expected": "The empty-tree traversal prints no values.",
        "exercise": "Implement a recursive search function for a BST. Return a pointer to the matching node or NULL when the value is absent.",
        "expected2": "Searching for an inserted value returns its node; searching for a missing value returns NULL.",
        "quiz": [
            ("What order does in-order traversal produce for a BST with unique keys?", ["Random order", "Sorted ascending order", "Reverse insertion order", "Level order"], 1, "In-order traversal visits left subtree, node and right subtree, producing sorted order under the BST invariant."),
            ("What is the average search complexity in a balanced BST?", ["O(n)", "O(log n)", "O(n squared)", "O(1) always"], 1, "A balanced tree has logarithmic height, so each comparison removes about half of the remaining levels."),
            ("Can an unbalanced BST have O(n) search time?", ["No", "Yes", "Only with strings", "Only for empty trees"], 1, "A degenerate tree can become a chain, requiring a linear number of comparisons."),
        ],
    },
}


def get_c_core_lesson(lesson_title: str) -> Dict[str, Any] | None:
    title = str(lesson_title or "").strip().lower()
    matches = [
        (len(key), profile)
        for key, profile in _C_CORE.items()
        if key.lower() in title
    ]
    if not matches:
        return None
    profile = max(matches, key=lambda item: item[0])[1]
    return build_authored_lesson(profile, "C")
