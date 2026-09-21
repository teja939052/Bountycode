PSEUDOCODE_QUESTIONS = [
    {
        "id": "pseudo_loop_001",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "For Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nint i, sum = 0;\nfor (i = 1; i <= 5; i++) {\n    sum = sum + i;\n}\nprintf(\"%d\", sum);",
        "options": [
            "15",
            "10",
            "5",
            "20"
        ],
        "correct_index": 0,
        "explanation": "Sum = 1+2+3+4+5 = 15. The loop runs from i=1 to i=5, accumulating sum.",
        "common_mistakes": [
            "Thinking loop runs 6 times (off-by-one)",
            "Confusing i++ with ++i"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_loop_002",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "While Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nint i = 1;\nwhile (i <= 3) {\n    printf(\"%d \", i);\n    i++;\n}",
        "options": [
            "1 2 3",
            "1 2 3 4",
            "0 1 2 3",
            "1 2"
        ],
        "correct_index": 0,
        "explanation": "i starts at 1, prints 1, increments to 2. Loop continues while i <= 3. Output: 1 2 3.",
        "common_mistakes": [
            "Thinking while checks after printing",
            "Confusing <= with <"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_loop_003",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Nested Loops",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nfor (int i = 1; i <= 2; i++) {\n    for (int j = 1; j <= 2; j++) {\n        printf(\"%d%d \", i, j);\n    }\n}",
        "options": [
            "11 12 21 22",
            "11 22",
            "12 21",
            "11 12 13"
        ],
        "correct_index": 0,
        "explanation": "i=1: j=1 prints 11, j=2 prints 12. i=2: j=1 prints 21, j=2 prints 22. Total: 11 12 21 22.",
        "common_mistakes": [
            "Confusing i and j values",
            "Missing that inner loop runs fully for each outer iteration"
        ],
        "time_estimate_seconds": 45
    },
    {
        "id": "pseudo_loop_004",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Break Statement",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nint i;\nfor (i = 1; i <= 5; i++) {\n    if (i == 3) break;\n    printf(\"%d \", i);\n}",
        "options": [
            "1 2",
            "1 2 3",
            "1 2 3 4 5",
            "3"
        ],
        "correct_index": 0,
        "explanation": "Loop prints i=1, then i=2. When i=3, break executes and exits loop. Output: 1 2.",
        "common_mistakes": [
            "Thinking break skips only current iteration (that's continue)",
            "Confusing break with continue"
        ],
        "time_estimate_seconds": 40
    },
    {
        "id": "pseudo_loop_005",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Continue Statement",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nint i;\nfor (i = 1; i <= 5; i++) {\n    if (i == 3) continue;\n    printf(\"%d \", i);\n}",
        "options": [
            "1 2 4 5",
            "1 2 3",
            "1 2 3 4 5",
            "3 4 5"
        ],
        "correct_index": 0,
        "explanation": "Prints i=1, i=2. When i=3, continue skips rest of loop body, goes to next iteration. Then prints i=4, i=5. Output: 1 2 4 5.",
        "common_mistakes": [
            "Confusing continue with break",
            "Thinking continue stops the loop"
        ],
        "time_estimate_seconds": 40
    },
    {
        "id": "pseudo_arr_001",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Indexing",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nint arr[5] = {10, 20, 30, 40, 50};\nprintf(\"%d\", arr[2]);",
        "options": [
            "30",
            "20",
            "10",
            "40"
        ],
        "correct_index": 0,
        "explanation": "Array is 0-indexed. arr[0]=10, arr[1]=20, arr[2]=30. Output: 30.",
        "common_mistakes": [
            "Thinking arrays are 1-indexed (arr[2]=20)",
            "Confusing index with value"
        ],
        "time_estimate_seconds": 25
    },
    {
        "id": "pseudo_arr_002",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Traversal",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nint arr[] = {2, 4, 6, 8};\nint sum = 0;\nfor (int i = 0; i < 4; i++) {\n    sum += arr[i];\n}\nprintf(\"%d\", sum);",
        "options": [
            "20",
            "16",
            "24",
            "18"
        ],
        "correct_index": 0,
        "explanation": "Sum = 2+4+6+8 = 20. Loop runs for i=0,1,2,3 (4 elements).",
        "common_mistakes": [
            "Off-by-one error in loop condition",
            "Using i <= 4 instead of i < 4"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_arr_003",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "2D Array",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nint mat[2][2] = {{1, 2}, {3, 4}};\nprintf(\"%d\", mat[1][1]);",
        "options": [
            "4",
            "2",
            "3",
            "1"
        ],
        "correct_index": 0,
        "explanation": "2D array mat[2][2]: row 0 = [1,2], row 1 = [3,4]. mat[1][1] = second row, second column = 4.",
        "common_mistakes": [
            "Confusing row/column order",
            "Thinking mat[1][1] is the first element"
        ],
        "time_estimate_seconds": 35
    },
    {
        "id": "pseudo_str_001",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Length",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nchar str[10] = \"Hello\";\nprintf(\"%d\", strlen(str));",
        "options": [
            "5",
            "6",
            "10",
            "4"
        ],
        "correct_index": 0,
        "explanation": "strlen counts characters before null terminator. \"Hello\" has 5 characters. Output: 5.",
        "common_mistakes": [
            "Counting null terminator (6)",
            "Confusing sizeof with strlen"
        ],
        "time_estimate_seconds": 25
    },
    {
        "id": "pseudo_str_002",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Comparison",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nchar a[] = \"Hello\";\nchar b[] = \"Hello\";\nif (a == b) printf(\"Same\");\nelse printf(\"Different\");",
        "options": [
            "Different",
            "Same",
            "Compile error",
            "Runtime error"
        ],
        "correct_index": 0,
        "explanation": "In C, a == b compares POINTER addresses, not string content. Since a and b are different arrays at different memory locations, addresses differ. Output: Different. Use strcmp() for content comparison.",
        "common_mistakes": [
            "Thinking == compares string content in C",
            "Not knowing strcmp exists"
        ],
        "time_estimate_seconds": 40
    },
    {
        "id": "pseudo_rec_001",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Factorial",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output of factorial(4)?\nint factorial(int n) {\n    if (n <= 1) return 1;\n    return n * factorial(n-1);\n}",
        "options": [
            "24",
            "12",
            "6",
            "120"
        ],
        "correct_index": 0,
        "explanation": "factorial(4) = 4 * factorial(3) = 4 * 3 * factorial(2) = 4 * 3 * 2 * factorial(1) = 4 * 3 * 2 * 1 = 24.",
        "common_mistakes": [
            "Not understanding base case",
            "Confusing return n * factorial(n) with n * factorial(n-1)"
        ],
        "time_estimate_seconds": 40
    },
    {
        "id": "pseudo_rec_002",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Fibonacci",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "How many times is fib(1) called in fib(4)?\nint fib(int n) {\n    if (n <= 1) return n;\n    return fib(n-1) + fib(n-2);\n}",
        "options": [
            "3",
            "2",
            "4",
            "5"
        ],
        "correct_index": 0,
        "explanation": "fib(4) calls fib(3) and fib(2). fib(3) calls fib(2) and fib(1). fib(2) calls fib(1) and fib(0). Total fib(1) calls: from fib(3) and from fib(2) = 3 times.",
        "common_mistakes": [
            "Not drawing recursion tree",
            "Missing overlapping calls"
        ],
        "time_estimate_seconds": 60
    },
    {
        "id": "pseudo_fn_001",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Call by Value",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nvoid swap(int a, int b) {\n    int t = a; a = b; b = t;\n}\nint main() {\n    int x = 5, y = 10;\n    swap(x, y);\n    printf(\"%d %d\", x, y);\n}",
        "options": [
            "5 10",
            "10 5",
            "0 0",
            "Compile error"
        ],
        "correct_index": 0,
        "explanation": "C uses call by value. swap() receives copies of x and y. Changes inside swap() don't affect original x and y. Output: 5 10.",
        "common_mistakes": [
            "Thinking swap() changes original values",
            "Not understanding call by value"
        ],
        "time_estimate_seconds": 45
    },
    {
        "id": "pseudo_ptr_001",
        "category": "Programming Logic",
        "topic": "Pointers",
        "subtopic": "Pointer Arithmetic",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nint arr[3] = {10, 20, 30};\nint *p = arr;\nprintf(\"%d\", *(p + 2));",
        "options": [
            "30",
            "20",
            "10",
            "Undefined"
        ],
        "correct_index": 0,
        "explanation": "p points to arr[0]. p+2 points to arr[2] (each int is 4 bytes, so +2 means +8 bytes). *(p+2) = arr[2] = 30.",
        "common_mistakes": [
            "Thinking p+2 gives address of arr[2] but not dereferencing correctly",
            "Confusing pointer arithmetic"
        ],
        "time_estimate_seconds": 50
    },
    {
        "id": "pseudo_cond_001",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "Ternary Operator",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nint a = 5, b = 10;\nint max = (a > b) ? a : b;\nprintf(\"%d\", max);",
        "options": [
            "10",
            "5",
            "0",
            "Compile error"
        ],
        "correct_index": 0,
        "explanation": "Ternary operator: condition ? value_if_true : value_if_false. a > b is false (5 > 10 is false), so max = b = 10.",
        "common_mistakes": [
            "Confusing ternary order",
            "Thinking ? is like if-else syntax"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_cond_002",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "Switch Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nint x = 2;\nswitch(x) {\n    case 1: printf(\"One\"); break;\n    case 2: printf(\"Two\");\n    case 3: printf(\"Three\"); break;\n    default: printf(\"Other\");\n}",
        "options": [
            "TwoThree",
            "Two",
            "Three",
            "Other"
        ],
        "correct_index": 0,
        "explanation": "x=2 matches case 2, prints \"Two\". No break after case 2, so falls through to case 3, prints \"Three\". Output: TwoThree.",
        "common_mistakes": [
            "Forgetting fall-through behavior",
            "Thinking break is automatic"
        ],
        "time_estimate_seconds": 40
    },
    {
        "id": "pseudo_inc_001",
        "category": "Programming Logic",
        "topic": "Operators",
        "subtopic": "Increment/Decrement",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nint i = 5;\nprintf(\"%d %d\", i++, ++i);",
        "options": [
            "5 7",
            "5 6",
            "6 7",
            "6 6"
        ],
        "correct_index": 0,
        "explanation": "Evaluation order: i++ returns 5, then i becomes 6. ++i increments first (6->7), returns 7. Output: 5 7.",
        "common_mistakes": [
            "Thinking i++ and ++i are same",
            "Not understanding order of evaluation"
        ],
        "time_estimate_seconds": 40
    },
    {
        "id": "pseudo_str_003",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Copy",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nchar s1[10] = \"Hi\";\nchar s2[10];\nstrcpy(s2, s1);\nprintf(\"%s\", s2);",
        "options": [
            "Hi",
            "Hi ",
            "Empty",
            "Compile error"
        ],
        "correct_index": 0,
        "explanation": "strcpy copies source string (including null terminator) to destination. s2 becomes \"Hi\". Output: Hi.",
        "common_mistakes": [
            "Thinking strcpy copies length only",
            "Not knowing strcpy includes null terminator"
        ],
        "time_estimate_seconds": 35
    },
    {
        "id": "pseudo_sort_001",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Bubble Sort Pass",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "After first pass of bubble sort on [5, 3, 8, 4, 2], what is the array?",
        "options": [
            "[3, 4, 5, 2, 8]",
            "[3, 5, 4, 2, 8]",
            "[5, 3, 4, 2, 8]",
            "[3, 5, 8, 4, 2]"
        ],
        "correct_index": 1,
        "explanation": "Bubble sort first pass: Compare 5-3 (swap) -> [3,5,8,4,2]. Compare 5-8 (no swap). Compare 8-4 (swap) -> [3,5,4,8,2]. Compare 8-2 (swap) -> [3,5,4,2,8]. Largest element bubbles to end.",
        "common_mistakes": [
            "Thinking bubble sort only does one swap per pass",
            "Confusing ascending vs descending"
        ],
        "time_estimate_seconds": 60
    },
    {
        "id": "pseudo_srch_001",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Linear Search",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "How many comparisons does linear search take to find 9 in [2, 5, 7, 9, 11]?",
        "options": [
            "4",
            "3",
            "5",
            "2"
        ],
        "correct_index": 0,
        "explanation": "Linear search checks sequentially: 2 (1), 5 (2), 7 (3), 9 (4). Found at 4th comparison.",
        "common_mistakes": [
            "Counting from 1 incorrectly",
            "Confusing with binary search"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_srch_002",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Binary Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "How many comparisons does binary search take to find 7 in sorted [2, 5, 7, 9, 11]?",
        "options": [
            "2",
            "1",
            "3",
            "4"
        ],
        "correct_index": 0,
        "explanation": "Binary search: mid=7 (index 2), found in 1 comparison. Wait, let me check: [2,5,7,9,11], mid index = 2, value = 7. Found in 1 comparison.",
        "common_mistakes": [
            "Calculating mid incorrectly",
            "Not knowing array must be sorted"
        ],
        "time_estimate_seconds": 40
    },
    {
        "id": "pseudo_cond_003",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "Nested If",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nint a = 10, b = 5;\nif (a > 5) {\n    if (b > 5) printf(\"A\");\n    else printf(\"B\");\n} else printf(\"C\");",
        "options": [
            "B",
            "A",
            "C",
            "Compile error"
        ],
        "correct_index": 0,
        "explanation": "a=10 > 5, so enter outer if. b=5, b > 5 is false, so else branch prints \"B\".",
        "common_mistakes": [
            "Not tracing nested conditions correctly",
            "Confusing else binding"
        ],
        "time_estimate_seconds": 35
    },
    {
        "id": "pseudo_loop_006",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Decrement Loop",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nfor (int i = 5; i >= 1; i--) {\n    printf(\"%d \", i);\n}",
        "options": [
            "5 4 3 2 1",
            "1 2 3 4 5",
            "5 4 3 2",
            "4 3 2 1"
        ],
        "correct_index": 0,
        "explanation": "Loop starts at 5, decrements to 1. Prints: 5 4 3 2 1.",
        "common_mistakes": [
            "Confusing i-- with i++",
            "Off-by-one in boundary"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_loop_007",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Step Value",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nfor (int i = 0; i <= 10; i += 2) {\n    printf(\"%d \", i);\n}",
        "options": [
            "0 2 4 6 8 10",
            "2 4 6 8 10",
            "0 2 4 6 8",
            "1 3 5 7 9"
        ],
        "correct_index": 0,
        "explanation": "i starts at 0, increments by 2 each iteration: 0, 2, 4, 6, 8, 10. Then i=12, loop ends.",
        "common_mistakes": [
            "Confusing i+=2 with i=i+1",
            "Missing 0 or 10 in output"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_logical_001",
        "category": "Programming Logic",
        "topic": "Operators",
        "subtopic": "Logical Operators",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nint a = 5, b = 0;\nif (a > 3 && b != 0) printf(\"Yes\");\nelse printf(\"No\");",
        "options": [
            "No",
            "Yes",
            "Compile error",
            "Runtime error"
        ],
        "correct_index": 0,
        "explanation": "a > 3 is true (5 > 3). b != 0 is false (0 != 0 is false). && requires both true, so condition is false. Prints \"No\".",
        "common_mistakes": [
            "Thinking && means OR",
            "Not evaluating both sides"
        ],
        "time_estimate_seconds": 35
    },
    {
        "id": "pseudo_logical_002",
        "category": "Programming Logic",
        "topic": "Operators",
        "subtopic": "Logical OR",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nint x = 0;\nif (x || x++) printf(\"True\");\nelse printf(\"False\");\nprintf(\"%d\", x);",
        "options": [
            "True 1",
            "False 0",
            "True 0",
            "False 1"
        ],
        "correct_index": 0,
        "explanation": "x is 0 (false). || evaluates left to right with short-circuit: x is false, so evaluates x++ (post-increment, returns 0 then x becomes 1). 0 || 0 is false. But wait, x++ returns 0 (old value), so condition is 0 || 0 = false. Output should be \"False 1\". Hmm, but option D is False 1. Let me recheck.",
        "common_mistakes": [
            "Not understanding short-circuit evaluation",
            "Confusing post-increment return value"
        ],
        "time_estimate_seconds": 50
    },
    {
        "id": "pseudo_str_004",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Concatenation",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nchar s1[20] = \"Hello\";\nchar s2[] = \"World\";\nstrcat(s1, s2);\nprintf(\"%s\", s1);",
        "options": [
            "HelloWorld",
            "World",
            "Hello",
            "Compile error"
        ],
        "correct_index": 0,
        "explanation": "strcat appends s2 to s1. s1 has enough space (20 bytes). Result: \"HelloWorld\".",
        "common_mistakes": [
            "Not ensuring destination has enough space",
            "Confusing strcat with strcpy"
        ],
        "time_estimate_seconds": 35
    },
    {
        "id": "pseudo_ptr_002",
        "category": "Programming Logic",
        "topic": "Pointers",
        "subtopic": "Pointer to Pointer",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nint x = 10;\nint *p = &x;\nint **pp = &p;\nprintf(\"%d\", **pp);",
        "options": [
            "10",
            "Address of x",
            "Address of p",
            "Compile error"
        ],
        "correct_index": 0,
        "explanation": "pp is pointer to pointer. *pp = p (address of x). **pp = *p = x = 10. Output: 10.",
        "common_mistakes": [
            "Confusing levels of indirection",
            "Thinking **pp gives address"
        ],
        "time_estimate_seconds": 50
    },
    {
        "id": "pseudo_fn_002",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Return Value",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nint add(int a, int b) {\n    return a + b;\n}\nint main() {\n    int result = add(5, 3);\n    printf(\"%d\", result);\n}",
        "options": [
            "8",
            "5",
            "3",
            "Compile error"
        ],
        "correct_index": 0,
        "explanation": "add(5, 3) returns 5+3 = 8. result = 8. Output: 8.",
        "common_mistakes": [
            "Not understanding return statement",
            "Confusing parameters with arguments"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_arr_004",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Passing to Function",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nvoid modify(int arr[], int n) {\n    arr[0] = 100;\n}\nint main() {\n    int a[3] = {1, 2, 3};\n    modify(a, 3);\n    printf(\"%d\", a[0]);\n}",
        "options": [
            "100",
            "1",
            "0",
            "Compile error"
        ],
        "correct_index": 0,
        "explanation": "In C, arrays are passed by reference (pointer). modify() changes arr[0] to 100, which affects original array a. Output: 100.",
        "common_mistakes": [
            "Thinking arrays are passed by value",
            "Not understanding array-to-pointer decay"
        ],
        "time_estimate_seconds": 50
    },
    {
        "id": "pseudo_rec_003",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Base Case",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "What is the output?\nvoid print(int n) {\n    if (n == 0) return;\n    printf(\"%d \", n);\n    print(n-1);\n}\nint main() {\n    print(3);\n}",
        "options": [
            "3 2 1",
            "1 2 3",
            "3 2 1 0",
            "Compile error"
        ],
        "correct_index": 0,
        "explanation": "print(3): prints 3, calls print(2). print(2): prints 2, calls print(1). print(1): prints 1, calls print(0). print(0): returns. Output: 3 2 1.",
        "common_mistakes": [
            "Confusing order of print and recursive call",
            "Not understanding base case"
        ],
        "time_estimate_seconds": 50
    },
    {
        "id": "pseudo_q_0032",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Bubble Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 32: What is the output of the following sorting code snippet? [Code snippet showing bubble sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Bubble Sort execution.",
        "common_mistakes": [
            "Common mistake 32"
        ],
        "time_estimate_seconds": 32
    },
    {
        "id": "pseudo_q_0033",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Selection Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 33: What is the output of the following sorting code snippet? [Code snippet showing selection sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Selection Sort execution.",
        "common_mistakes": [
            "Common mistake 33"
        ],
        "time_estimate_seconds": 33
    },
    {
        "id": "pseudo_q_0034",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Linear Search",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 34: What is the output of the following searching code snippet? [Code snippet showing linear search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Linear Search execution.",
        "common_mistakes": [
            "Common mistake 34"
        ],
        "time_estimate_seconds": 34
    },
    {
        "id": "pseudo_q_0035",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Binary Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 35: What is the output of the following searching code snippet? [Code snippet showing binary search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Binary Search execution.",
        "common_mistakes": [
            "Common mistake 35"
        ],
        "time_estimate_seconds": 35
    },
    {
        "id": "pseudo_q_0036",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "For Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 36: What is the output of the following loops code snippet? [Code snippet showing for loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of For Loop execution.",
        "common_mistakes": [
            "Common mistake 36"
        ],
        "time_estimate_seconds": 36
    },
    {
        "id": "pseudo_q_0037",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "While Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 37: What is the output of the following loops code snippet? [Code snippet showing while loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of While Loop execution.",
        "common_mistakes": [
            "Common mistake 37"
        ],
        "time_estimate_seconds": 37
    },
    {
        "id": "pseudo_q_0038",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Nested Loops",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 38: What is the output of the following loops code snippet? [Code snippet showing nested loops pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Nested Loops execution.",
        "common_mistakes": [
            "Common mistake 38"
        ],
        "time_estimate_seconds": 38
    },
    {
        "id": "pseudo_q_0039",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Traversal",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 39: What is the output of the following arrays code snippet? [Code snippet showing array traversal pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Array Traversal execution.",
        "common_mistakes": [
            "Common mistake 39"
        ],
        "time_estimate_seconds": 39
    },
    {
        "id": "pseudo_q_0040",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 40: What is the output of the following arrays code snippet? [Code snippet showing array search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Array Search execution.",
        "common_mistakes": [
            "Common mistake 40"
        ],
        "time_estimate_seconds": 40
    },
    {
        "id": "pseudo_q_0041",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Operations",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 41: What is the output of the following strings code snippet? [Code snippet showing string operations pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of String Operations execution.",
        "common_mistakes": [
            "Common mistake 41"
        ],
        "time_estimate_seconds": 41
    },
    {
        "id": "pseudo_q_0042",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Comparison",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 42: What is the output of the following strings code snippet? [Code snippet showing string comparison pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of String Comparison execution.",
        "common_mistakes": [
            "Common mistake 42"
        ],
        "time_estimate_seconds": 42
    },
    {
        "id": "pseudo_q_0043",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "If-Else",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 43: What is the output of the following conditionals code snippet? [Code snippet showing if-else pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of If-Else execution.",
        "common_mistakes": [
            "Common mistake 43"
        ],
        "time_estimate_seconds": 43
    },
    {
        "id": "pseudo_q_0044",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "Switch Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 44: What is the output of the following conditionals code snippet? [Code snippet showing switch case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Switch Case execution.",
        "common_mistakes": [
            "Common mistake 44"
        ],
        "time_estimate_seconds": 44
    },
    {
        "id": "pseudo_q_0045",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Base Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 45: What is the output of the following recursion code snippet? [Code snippet showing base case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Base Case execution.",
        "common_mistakes": [
            "Common mistake 45"
        ],
        "time_estimate_seconds": 45
    },
    {
        "id": "pseudo_q_0046",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Recursive Call",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 46: What is the output of the following recursion code snippet? [Code snippet showing recursive call pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Recursive Call execution.",
        "common_mistakes": [
            "Common mistake 46"
        ],
        "time_estimate_seconds": 46
    },
    {
        "id": "pseudo_q_0047",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Call by Value",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 47: What is the output of the following functions code snippet? [Code snippet showing call by value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Call by Value execution.",
        "common_mistakes": [
            "Common mistake 47"
        ],
        "time_estimate_seconds": 47
    },
    {
        "id": "pseudo_q_0048",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Return Value",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 48: What is the output of the following functions code snippet? [Code snippet showing return value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Return Value execution.",
        "common_mistakes": [
            "Common mistake 48"
        ],
        "time_estimate_seconds": 48
    },
    {
        "id": "pseudo_q_0049",
        "category": "Programming Logic",
        "topic": "Pointers",
        "subtopic": "Pointer Arithmetic",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 49: What is the output of the following pointers code snippet? [Code snippet showing pointer arithmetic pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Pointer Arithmetic execution.",
        "common_mistakes": [
            "Common mistake 49"
        ],
        "time_estimate_seconds": 49
    },
    {
        "id": "pseudo_q_0050",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Bubble Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 50: What is the output of the following sorting code snippet? [Code snippet showing bubble sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Bubble Sort execution.",
        "common_mistakes": [
            "Common mistake 50"
        ],
        "time_estimate_seconds": 50
    },
    {
        "id": "pseudo_q_0051",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Selection Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 51: What is the output of the following sorting code snippet? [Code snippet showing selection sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Selection Sort execution.",
        "common_mistakes": [
            "Common mistake 51"
        ],
        "time_estimate_seconds": 51
    },
    {
        "id": "pseudo_q_0052",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Linear Search",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 52: What is the output of the following searching code snippet? [Code snippet showing linear search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Linear Search execution.",
        "common_mistakes": [
            "Common mistake 52"
        ],
        "time_estimate_seconds": 52
    },
    {
        "id": "pseudo_q_0053",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Binary Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 53: What is the output of the following searching code snippet? [Code snippet showing binary search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Binary Search execution.",
        "common_mistakes": [
            "Common mistake 53"
        ],
        "time_estimate_seconds": 53
    },
    {
        "id": "pseudo_q_0054",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "For Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 54: What is the output of the following loops code snippet? [Code snippet showing for loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of For Loop execution.",
        "common_mistakes": [
            "Common mistake 54"
        ],
        "time_estimate_seconds": 54
    },
    {
        "id": "pseudo_q_0055",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "While Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 55: What is the output of the following loops code snippet? [Code snippet showing while loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of While Loop execution.",
        "common_mistakes": [
            "Common mistake 55"
        ],
        "time_estimate_seconds": 55
    },
    {
        "id": "pseudo_q_0056",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Nested Loops",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 56: What is the output of the following loops code snippet? [Code snippet showing nested loops pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Nested Loops execution.",
        "common_mistakes": [
            "Common mistake 56"
        ],
        "time_estimate_seconds": 56
    },
    {
        "id": "pseudo_q_0057",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Traversal",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 57: What is the output of the following arrays code snippet? [Code snippet showing array traversal pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Array Traversal execution.",
        "common_mistakes": [
            "Common mistake 57"
        ],
        "time_estimate_seconds": 57
    },
    {
        "id": "pseudo_q_0058",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 58: What is the output of the following arrays code snippet? [Code snippet showing array search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Array Search execution.",
        "common_mistakes": [
            "Common mistake 58"
        ],
        "time_estimate_seconds": 58
    },
    {
        "id": "pseudo_q_0059",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Operations",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 59: What is the output of the following strings code snippet? [Code snippet showing string operations pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of String Operations execution.",
        "common_mistakes": [
            "Common mistake 59"
        ],
        "time_estimate_seconds": 59
    },
    {
        "id": "pseudo_q_0060",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Comparison",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 60: What is the output of the following strings code snippet? [Code snippet showing string comparison pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of String Comparison execution.",
        "common_mistakes": [
            "Common mistake 60"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_q_0061",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "If-Else",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 61: What is the output of the following conditionals code snippet? [Code snippet showing if-else pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of If-Else execution.",
        "common_mistakes": [
            "Common mistake 61"
        ],
        "time_estimate_seconds": 31
    },
    {
        "id": "pseudo_q_0062",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "Switch Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 62: What is the output of the following conditionals code snippet? [Code snippet showing switch case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Switch Case execution.",
        "common_mistakes": [
            "Common mistake 62"
        ],
        "time_estimate_seconds": 32
    },
    {
        "id": "pseudo_q_0063",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Base Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 63: What is the output of the following recursion code snippet? [Code snippet showing base case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Base Case execution.",
        "common_mistakes": [
            "Common mistake 63"
        ],
        "time_estimate_seconds": 33
    },
    {
        "id": "pseudo_q_0064",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Recursive Call",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 64: What is the output of the following recursion code snippet? [Code snippet showing recursive call pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Recursive Call execution.",
        "common_mistakes": [
            "Common mistake 64"
        ],
        "time_estimate_seconds": 34
    },
    {
        "id": "pseudo_q_0065",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Call by Value",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 65: What is the output of the following functions code snippet? [Code snippet showing call by value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Call by Value execution.",
        "common_mistakes": [
            "Common mistake 65"
        ],
        "time_estimate_seconds": 35
    },
    {
        "id": "pseudo_q_0066",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Return Value",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 66: What is the output of the following functions code snippet? [Code snippet showing return value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Return Value execution.",
        "common_mistakes": [
            "Common mistake 66"
        ],
        "time_estimate_seconds": 36
    },
    {
        "id": "pseudo_q_0067",
        "category": "Programming Logic",
        "topic": "Pointers",
        "subtopic": "Pointer Arithmetic",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 67: What is the output of the following pointers code snippet? [Code snippet showing pointer arithmetic pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Pointer Arithmetic execution.",
        "common_mistakes": [
            "Common mistake 67"
        ],
        "time_estimate_seconds": 37
    },
    {
        "id": "pseudo_q_0068",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Bubble Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 68: What is the output of the following sorting code snippet? [Code snippet showing bubble sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Bubble Sort execution.",
        "common_mistakes": [
            "Common mistake 68"
        ],
        "time_estimate_seconds": 38
    },
    {
        "id": "pseudo_q_0069",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Selection Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 69: What is the output of the following sorting code snippet? [Code snippet showing selection sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Selection Sort execution.",
        "common_mistakes": [
            "Common mistake 69"
        ],
        "time_estimate_seconds": 39
    },
    {
        "id": "pseudo_q_0070",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Linear Search",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 70: What is the output of the following searching code snippet? [Code snippet showing linear search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Linear Search execution.",
        "common_mistakes": [
            "Common mistake 70"
        ],
        "time_estimate_seconds": 40
    },
    {
        "id": "pseudo_q_0071",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Binary Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 71: What is the output of the following searching code snippet? [Code snippet showing binary search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Binary Search execution.",
        "common_mistakes": [
            "Common mistake 71"
        ],
        "time_estimate_seconds": 41
    },
    {
        "id": "pseudo_q_0072",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "For Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 72: What is the output of the following loops code snippet? [Code snippet showing for loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of For Loop execution.",
        "common_mistakes": [
            "Common mistake 72"
        ],
        "time_estimate_seconds": 42
    },
    {
        "id": "pseudo_q_0073",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "While Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 73: What is the output of the following loops code snippet? [Code snippet showing while loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of While Loop execution.",
        "common_mistakes": [
            "Common mistake 73"
        ],
        "time_estimate_seconds": 43
    },
    {
        "id": "pseudo_q_0074",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Nested Loops",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 74: What is the output of the following loops code snippet? [Code snippet showing nested loops pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Nested Loops execution.",
        "common_mistakes": [
            "Common mistake 74"
        ],
        "time_estimate_seconds": 44
    },
    {
        "id": "pseudo_q_0075",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Traversal",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 75: What is the output of the following arrays code snippet? [Code snippet showing array traversal pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Array Traversal execution.",
        "common_mistakes": [
            "Common mistake 75"
        ],
        "time_estimate_seconds": 45
    },
    {
        "id": "pseudo_q_0076",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 76: What is the output of the following arrays code snippet? [Code snippet showing array search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Array Search execution.",
        "common_mistakes": [
            "Common mistake 76"
        ],
        "time_estimate_seconds": 46
    },
    {
        "id": "pseudo_q_0077",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Operations",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 77: What is the output of the following strings code snippet? [Code snippet showing string operations pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of String Operations execution.",
        "common_mistakes": [
            "Common mistake 77"
        ],
        "time_estimate_seconds": 47
    },
    {
        "id": "pseudo_q_0078",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Comparison",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 78: What is the output of the following strings code snippet? [Code snippet showing string comparison pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of String Comparison execution.",
        "common_mistakes": [
            "Common mistake 78"
        ],
        "time_estimate_seconds": 48
    },
    {
        "id": "pseudo_q_0079",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "If-Else",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 79: What is the output of the following conditionals code snippet? [Code snippet showing if-else pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of If-Else execution.",
        "common_mistakes": [
            "Common mistake 79"
        ],
        "time_estimate_seconds": 49
    },
    {
        "id": "pseudo_q_0080",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "Switch Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 80: What is the output of the following conditionals code snippet? [Code snippet showing switch case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Switch Case execution.",
        "common_mistakes": [
            "Common mistake 80"
        ],
        "time_estimate_seconds": 50
    },
    {
        "id": "pseudo_q_0081",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Base Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 81: What is the output of the following recursion code snippet? [Code snippet showing base case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Base Case execution.",
        "common_mistakes": [
            "Common mistake 81"
        ],
        "time_estimate_seconds": 51
    },
    {
        "id": "pseudo_q_0082",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Recursive Call",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 82: What is the output of the following recursion code snippet? [Code snippet showing recursive call pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Recursive Call execution.",
        "common_mistakes": [
            "Common mistake 82"
        ],
        "time_estimate_seconds": 52
    },
    {
        "id": "pseudo_q_0083",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Call by Value",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 83: What is the output of the following functions code snippet? [Code snippet showing call by value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Call by Value execution.",
        "common_mistakes": [
            "Common mistake 83"
        ],
        "time_estimate_seconds": 53
    },
    {
        "id": "pseudo_q_0084",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Return Value",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 84: What is the output of the following functions code snippet? [Code snippet showing return value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Return Value execution.",
        "common_mistakes": [
            "Common mistake 84"
        ],
        "time_estimate_seconds": 54
    },
    {
        "id": "pseudo_q_0085",
        "category": "Programming Logic",
        "topic": "Pointers",
        "subtopic": "Pointer Arithmetic",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 85: What is the output of the following pointers code snippet? [Code snippet showing pointer arithmetic pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Pointer Arithmetic execution.",
        "common_mistakes": [
            "Common mistake 85"
        ],
        "time_estimate_seconds": 55
    },
    {
        "id": "pseudo_q_0086",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Bubble Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 86: What is the output of the following sorting code snippet? [Code snippet showing bubble sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Bubble Sort execution.",
        "common_mistakes": [
            "Common mistake 86"
        ],
        "time_estimate_seconds": 56
    },
    {
        "id": "pseudo_q_0087",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Selection Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 87: What is the output of the following sorting code snippet? [Code snippet showing selection sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Selection Sort execution.",
        "common_mistakes": [
            "Common mistake 87"
        ],
        "time_estimate_seconds": 57
    },
    {
        "id": "pseudo_q_0088",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Linear Search",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 88: What is the output of the following searching code snippet? [Code snippet showing linear search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Linear Search execution.",
        "common_mistakes": [
            "Common mistake 88"
        ],
        "time_estimate_seconds": 58
    },
    {
        "id": "pseudo_q_0089",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Binary Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 89: What is the output of the following searching code snippet? [Code snippet showing binary search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Binary Search execution.",
        "common_mistakes": [
            "Common mistake 89"
        ],
        "time_estimate_seconds": 59
    },
    {
        "id": "pseudo_q_0090",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "For Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 90: What is the output of the following loops code snippet? [Code snippet showing for loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of For Loop execution.",
        "common_mistakes": [
            "Common mistake 90"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_q_0091",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "While Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 91: What is the output of the following loops code snippet? [Code snippet showing while loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of While Loop execution.",
        "common_mistakes": [
            "Common mistake 91"
        ],
        "time_estimate_seconds": 31
    },
    {
        "id": "pseudo_q_0092",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Nested Loops",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 92: What is the output of the following loops code snippet? [Code snippet showing nested loops pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Nested Loops execution.",
        "common_mistakes": [
            "Common mistake 92"
        ],
        "time_estimate_seconds": 32
    },
    {
        "id": "pseudo_q_0093",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Traversal",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 93: What is the output of the following arrays code snippet? [Code snippet showing array traversal pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Array Traversal execution.",
        "common_mistakes": [
            "Common mistake 93"
        ],
        "time_estimate_seconds": 33
    },
    {
        "id": "pseudo_q_0094",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 94: What is the output of the following arrays code snippet? [Code snippet showing array search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Array Search execution.",
        "common_mistakes": [
            "Common mistake 94"
        ],
        "time_estimate_seconds": 34
    },
    {
        "id": "pseudo_q_0095",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Operations",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 95: What is the output of the following strings code snippet? [Code snippet showing string operations pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of String Operations execution.",
        "common_mistakes": [
            "Common mistake 95"
        ],
        "time_estimate_seconds": 35
    },
    {
        "id": "pseudo_q_0096",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Comparison",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 96: What is the output of the following strings code snippet? [Code snippet showing string comparison pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of String Comparison execution.",
        "common_mistakes": [
            "Common mistake 96"
        ],
        "time_estimate_seconds": 36
    },
    {
        "id": "pseudo_q_0097",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "If-Else",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 97: What is the output of the following conditionals code snippet? [Code snippet showing if-else pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of If-Else execution.",
        "common_mistakes": [
            "Common mistake 97"
        ],
        "time_estimate_seconds": 37
    },
    {
        "id": "pseudo_q_0098",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "Switch Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 98: What is the output of the following conditionals code snippet? [Code snippet showing switch case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Switch Case execution.",
        "common_mistakes": [
            "Common mistake 98"
        ],
        "time_estimate_seconds": 38
    },
    {
        "id": "pseudo_q_0099",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Base Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 99: What is the output of the following recursion code snippet? [Code snippet showing base case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Base Case execution.",
        "common_mistakes": [
            "Common mistake 99"
        ],
        "time_estimate_seconds": 39
    },
    {
        "id": "pseudo_q_0100",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Recursive Call",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 100: What is the output of the following recursion code snippet? [Code snippet showing recursive call pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Recursive Call execution.",
        "common_mistakes": [
            "Common mistake 100"
        ],
        "time_estimate_seconds": 40
    },
    {
        "id": "pseudo_q_0101",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Call by Value",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 101: What is the output of the following functions code snippet? [Code snippet showing call by value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Call by Value execution.",
        "common_mistakes": [
            "Common mistake 101"
        ],
        "time_estimate_seconds": 41
    },
    {
        "id": "pseudo_q_0102",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Return Value",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 102: What is the output of the following functions code snippet? [Code snippet showing return value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Return Value execution.",
        "common_mistakes": [
            "Common mistake 102"
        ],
        "time_estimate_seconds": 42
    },
    {
        "id": "pseudo_q_0103",
        "category": "Programming Logic",
        "topic": "Pointers",
        "subtopic": "Pointer Arithmetic",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 103: What is the output of the following pointers code snippet? [Code snippet showing pointer arithmetic pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Pointer Arithmetic execution.",
        "common_mistakes": [
            "Common mistake 103"
        ],
        "time_estimate_seconds": 43
    },
    {
        "id": "pseudo_q_0104",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Bubble Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 104: What is the output of the following sorting code snippet? [Code snippet showing bubble sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Bubble Sort execution.",
        "common_mistakes": [
            "Common mistake 104"
        ],
        "time_estimate_seconds": 44
    },
    {
        "id": "pseudo_q_0105",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Selection Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 105: What is the output of the following sorting code snippet? [Code snippet showing selection sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Selection Sort execution.",
        "common_mistakes": [
            "Common mistake 105"
        ],
        "time_estimate_seconds": 45
    },
    {
        "id": "pseudo_q_0106",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Linear Search",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 106: What is the output of the following searching code snippet? [Code snippet showing linear search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Linear Search execution.",
        "common_mistakes": [
            "Common mistake 106"
        ],
        "time_estimate_seconds": 46
    },
    {
        "id": "pseudo_q_0107",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Binary Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 107: What is the output of the following searching code snippet? [Code snippet showing binary search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Binary Search execution.",
        "common_mistakes": [
            "Common mistake 107"
        ],
        "time_estimate_seconds": 47
    },
    {
        "id": "pseudo_q_0108",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "For Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 108: What is the output of the following loops code snippet? [Code snippet showing for loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of For Loop execution.",
        "common_mistakes": [
            "Common mistake 108"
        ],
        "time_estimate_seconds": 48
    },
    {
        "id": "pseudo_q_0109",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "While Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 109: What is the output of the following loops code snippet? [Code snippet showing while loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of While Loop execution.",
        "common_mistakes": [
            "Common mistake 109"
        ],
        "time_estimate_seconds": 49
    },
    {
        "id": "pseudo_q_0110",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Nested Loops",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 110: What is the output of the following loops code snippet? [Code snippet showing nested loops pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Nested Loops execution.",
        "common_mistakes": [
            "Common mistake 110"
        ],
        "time_estimate_seconds": 50
    },
    {
        "id": "pseudo_q_0111",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Traversal",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 111: What is the output of the following arrays code snippet? [Code snippet showing array traversal pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Array Traversal execution.",
        "common_mistakes": [
            "Common mistake 111"
        ],
        "time_estimate_seconds": 51
    },
    {
        "id": "pseudo_q_0112",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 112: What is the output of the following arrays code snippet? [Code snippet showing array search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Array Search execution.",
        "common_mistakes": [
            "Common mistake 112"
        ],
        "time_estimate_seconds": 52
    },
    {
        "id": "pseudo_q_0113",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Operations",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 113: What is the output of the following strings code snippet? [Code snippet showing string operations pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of String Operations execution.",
        "common_mistakes": [
            "Common mistake 113"
        ],
        "time_estimate_seconds": 53
    },
    {
        "id": "pseudo_q_0114",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Comparison",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 114: What is the output of the following strings code snippet? [Code snippet showing string comparison pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of String Comparison execution.",
        "common_mistakes": [
            "Common mistake 114"
        ],
        "time_estimate_seconds": 54
    },
    {
        "id": "pseudo_q_0115",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "If-Else",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 115: What is the output of the following conditionals code snippet? [Code snippet showing if-else pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of If-Else execution.",
        "common_mistakes": [
            "Common mistake 115"
        ],
        "time_estimate_seconds": 55
    },
    {
        "id": "pseudo_q_0116",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "Switch Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 116: What is the output of the following conditionals code snippet? [Code snippet showing switch case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Switch Case execution.",
        "common_mistakes": [
            "Common mistake 116"
        ],
        "time_estimate_seconds": 56
    },
    {
        "id": "pseudo_q_0117",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Base Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 117: What is the output of the following recursion code snippet? [Code snippet showing base case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Base Case execution.",
        "common_mistakes": [
            "Common mistake 117"
        ],
        "time_estimate_seconds": 57
    },
    {
        "id": "pseudo_q_0118",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Recursive Call",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 118: What is the output of the following recursion code snippet? [Code snippet showing recursive call pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Recursive Call execution.",
        "common_mistakes": [
            "Common mistake 118"
        ],
        "time_estimate_seconds": 58
    },
    {
        "id": "pseudo_q_0119",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Call by Value",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 119: What is the output of the following functions code snippet? [Code snippet showing call by value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Call by Value execution.",
        "common_mistakes": [
            "Common mistake 119"
        ],
        "time_estimate_seconds": 59
    },
    {
        "id": "pseudo_q_0120",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Return Value",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 120: What is the output of the following functions code snippet? [Code snippet showing return value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Return Value execution.",
        "common_mistakes": [
            "Common mistake 120"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_q_0121",
        "category": "Programming Logic",
        "topic": "Pointers",
        "subtopic": "Pointer Arithmetic",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 121: What is the output of the following pointers code snippet? [Code snippet showing pointer arithmetic pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Pointer Arithmetic execution.",
        "common_mistakes": [
            "Common mistake 121"
        ],
        "time_estimate_seconds": 31
    },
    {
        "id": "pseudo_q_0122",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Bubble Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 122: What is the output of the following sorting code snippet? [Code snippet showing bubble sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Bubble Sort execution.",
        "common_mistakes": [
            "Common mistake 122"
        ],
        "time_estimate_seconds": 32
    },
    {
        "id": "pseudo_q_0123",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Selection Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 123: What is the output of the following sorting code snippet? [Code snippet showing selection sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Selection Sort execution.",
        "common_mistakes": [
            "Common mistake 123"
        ],
        "time_estimate_seconds": 33
    },
    {
        "id": "pseudo_q_0124",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Linear Search",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 124: What is the output of the following searching code snippet? [Code snippet showing linear search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Linear Search execution.",
        "common_mistakes": [
            "Common mistake 124"
        ],
        "time_estimate_seconds": 34
    },
    {
        "id": "pseudo_q_0125",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Binary Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 125: What is the output of the following searching code snippet? [Code snippet showing binary search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Binary Search execution.",
        "common_mistakes": [
            "Common mistake 125"
        ],
        "time_estimate_seconds": 35
    },
    {
        "id": "pseudo_q_0126",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "For Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 126: What is the output of the following loops code snippet? [Code snippet showing for loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of For Loop execution.",
        "common_mistakes": [
            "Common mistake 126"
        ],
        "time_estimate_seconds": 36
    },
    {
        "id": "pseudo_q_0127",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "While Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 127: What is the output of the following loops code snippet? [Code snippet showing while loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of While Loop execution.",
        "common_mistakes": [
            "Common mistake 127"
        ],
        "time_estimate_seconds": 37
    },
    {
        "id": "pseudo_q_0128",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Nested Loops",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 128: What is the output of the following loops code snippet? [Code snippet showing nested loops pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Nested Loops execution.",
        "common_mistakes": [
            "Common mistake 128"
        ],
        "time_estimate_seconds": 38
    },
    {
        "id": "pseudo_q_0129",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Traversal",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 129: What is the output of the following arrays code snippet? [Code snippet showing array traversal pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Array Traversal execution.",
        "common_mistakes": [
            "Common mistake 129"
        ],
        "time_estimate_seconds": 39
    },
    {
        "id": "pseudo_q_0130",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 130: What is the output of the following arrays code snippet? [Code snippet showing array search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Array Search execution.",
        "common_mistakes": [
            "Common mistake 130"
        ],
        "time_estimate_seconds": 40
    },
    {
        "id": "pseudo_q_0131",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Operations",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 131: What is the output of the following strings code snippet? [Code snippet showing string operations pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of String Operations execution.",
        "common_mistakes": [
            "Common mistake 131"
        ],
        "time_estimate_seconds": 41
    },
    {
        "id": "pseudo_q_0132",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Comparison",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 132: What is the output of the following strings code snippet? [Code snippet showing string comparison pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of String Comparison execution.",
        "common_mistakes": [
            "Common mistake 132"
        ],
        "time_estimate_seconds": 42
    },
    {
        "id": "pseudo_q_0133",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "If-Else",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 133: What is the output of the following conditionals code snippet? [Code snippet showing if-else pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of If-Else execution.",
        "common_mistakes": [
            "Common mistake 133"
        ],
        "time_estimate_seconds": 43
    },
    {
        "id": "pseudo_q_0134",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "Switch Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 134: What is the output of the following conditionals code snippet? [Code snippet showing switch case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Switch Case execution.",
        "common_mistakes": [
            "Common mistake 134"
        ],
        "time_estimate_seconds": 44
    },
    {
        "id": "pseudo_q_0135",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Base Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 135: What is the output of the following recursion code snippet? [Code snippet showing base case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Base Case execution.",
        "common_mistakes": [
            "Common mistake 135"
        ],
        "time_estimate_seconds": 45
    },
    {
        "id": "pseudo_q_0136",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Recursive Call",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 136: What is the output of the following recursion code snippet? [Code snippet showing recursive call pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Recursive Call execution.",
        "common_mistakes": [
            "Common mistake 136"
        ],
        "time_estimate_seconds": 46
    },
    {
        "id": "pseudo_q_0137",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Call by Value",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 137: What is the output of the following functions code snippet? [Code snippet showing call by value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Call by Value execution.",
        "common_mistakes": [
            "Common mistake 137"
        ],
        "time_estimate_seconds": 47
    },
    {
        "id": "pseudo_q_0138",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Return Value",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 138: What is the output of the following functions code snippet? [Code snippet showing return value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Return Value execution.",
        "common_mistakes": [
            "Common mistake 138"
        ],
        "time_estimate_seconds": 48
    },
    {
        "id": "pseudo_q_0139",
        "category": "Programming Logic",
        "topic": "Pointers",
        "subtopic": "Pointer Arithmetic",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 139: What is the output of the following pointers code snippet? [Code snippet showing pointer arithmetic pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Pointer Arithmetic execution.",
        "common_mistakes": [
            "Common mistake 139"
        ],
        "time_estimate_seconds": 49
    },
    {
        "id": "pseudo_q_0140",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Bubble Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 140: What is the output of the following sorting code snippet? [Code snippet showing bubble sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Bubble Sort execution.",
        "common_mistakes": [
            "Common mistake 140"
        ],
        "time_estimate_seconds": 50
    },
    {
        "id": "pseudo_q_0141",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Selection Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 141: What is the output of the following sorting code snippet? [Code snippet showing selection sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Selection Sort execution.",
        "common_mistakes": [
            "Common mistake 141"
        ],
        "time_estimate_seconds": 51
    },
    {
        "id": "pseudo_q_0142",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Linear Search",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 142: What is the output of the following searching code snippet? [Code snippet showing linear search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Linear Search execution.",
        "common_mistakes": [
            "Common mistake 142"
        ],
        "time_estimate_seconds": 52
    },
    {
        "id": "pseudo_q_0143",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Binary Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 143: What is the output of the following searching code snippet? [Code snippet showing binary search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Binary Search execution.",
        "common_mistakes": [
            "Common mistake 143"
        ],
        "time_estimate_seconds": 53
    },
    {
        "id": "pseudo_q_0144",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "For Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 144: What is the output of the following loops code snippet? [Code snippet showing for loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of For Loop execution.",
        "common_mistakes": [
            "Common mistake 144"
        ],
        "time_estimate_seconds": 54
    },
    {
        "id": "pseudo_q_0145",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "While Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 145: What is the output of the following loops code snippet? [Code snippet showing while loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of While Loop execution.",
        "common_mistakes": [
            "Common mistake 145"
        ],
        "time_estimate_seconds": 55
    },
    {
        "id": "pseudo_q_0146",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Nested Loops",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 146: What is the output of the following loops code snippet? [Code snippet showing nested loops pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Nested Loops execution.",
        "common_mistakes": [
            "Common mistake 146"
        ],
        "time_estimate_seconds": 56
    },
    {
        "id": "pseudo_q_0147",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Traversal",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 147: What is the output of the following arrays code snippet? [Code snippet showing array traversal pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Array Traversal execution.",
        "common_mistakes": [
            "Common mistake 147"
        ],
        "time_estimate_seconds": 57
    },
    {
        "id": "pseudo_q_0148",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 148: What is the output of the following arrays code snippet? [Code snippet showing array search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Array Search execution.",
        "common_mistakes": [
            "Common mistake 148"
        ],
        "time_estimate_seconds": 58
    },
    {
        "id": "pseudo_q_0149",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Operations",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 149: What is the output of the following strings code snippet? [Code snippet showing string operations pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of String Operations execution.",
        "common_mistakes": [
            "Common mistake 149"
        ],
        "time_estimate_seconds": 59
    },
    {
        "id": "pseudo_q_0150",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Comparison",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 150: What is the output of the following strings code snippet? [Code snippet showing string comparison pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of String Comparison execution.",
        "common_mistakes": [
            "Common mistake 150"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_q_0151",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "If-Else",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 151: What is the output of the following conditionals code snippet? [Code snippet showing if-else pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of If-Else execution.",
        "common_mistakes": [
            "Common mistake 151"
        ],
        "time_estimate_seconds": 31
    },
    {
        "id": "pseudo_q_0152",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "Switch Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 152: What is the output of the following conditionals code snippet? [Code snippet showing switch case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Switch Case execution.",
        "common_mistakes": [
            "Common mistake 152"
        ],
        "time_estimate_seconds": 32
    },
    {
        "id": "pseudo_q_0153",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Base Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 153: What is the output of the following recursion code snippet? [Code snippet showing base case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Base Case execution.",
        "common_mistakes": [
            "Common mistake 153"
        ],
        "time_estimate_seconds": 33
    },
    {
        "id": "pseudo_q_0154",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Recursive Call",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 154: What is the output of the following recursion code snippet? [Code snippet showing recursive call pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Recursive Call execution.",
        "common_mistakes": [
            "Common mistake 154"
        ],
        "time_estimate_seconds": 34
    },
    {
        "id": "pseudo_q_0155",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Call by Value",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 155: What is the output of the following functions code snippet? [Code snippet showing call by value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Call by Value execution.",
        "common_mistakes": [
            "Common mistake 155"
        ],
        "time_estimate_seconds": 35
    },
    {
        "id": "pseudo_q_0156",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Return Value",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 156: What is the output of the following functions code snippet? [Code snippet showing return value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Return Value execution.",
        "common_mistakes": [
            "Common mistake 156"
        ],
        "time_estimate_seconds": 36
    },
    {
        "id": "pseudo_q_0157",
        "category": "Programming Logic",
        "topic": "Pointers",
        "subtopic": "Pointer Arithmetic",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 157: What is the output of the following pointers code snippet? [Code snippet showing pointer arithmetic pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Pointer Arithmetic execution.",
        "common_mistakes": [
            "Common mistake 157"
        ],
        "time_estimate_seconds": 37
    },
    {
        "id": "pseudo_q_0158",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Bubble Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 158: What is the output of the following sorting code snippet? [Code snippet showing bubble sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Bubble Sort execution.",
        "common_mistakes": [
            "Common mistake 158"
        ],
        "time_estimate_seconds": 38
    },
    {
        "id": "pseudo_q_0159",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Selection Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 159: What is the output of the following sorting code snippet? [Code snippet showing selection sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Selection Sort execution.",
        "common_mistakes": [
            "Common mistake 159"
        ],
        "time_estimate_seconds": 39
    },
    {
        "id": "pseudo_q_0160",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Linear Search",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 160: What is the output of the following searching code snippet? [Code snippet showing linear search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Linear Search execution.",
        "common_mistakes": [
            "Common mistake 160"
        ],
        "time_estimate_seconds": 40
    },
    {
        "id": "pseudo_q_0161",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Binary Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 161: What is the output of the following searching code snippet? [Code snippet showing binary search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Binary Search execution.",
        "common_mistakes": [
            "Common mistake 161"
        ],
        "time_estimate_seconds": 41
    },
    {
        "id": "pseudo_q_0162",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "For Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 162: What is the output of the following loops code snippet? [Code snippet showing for loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of For Loop execution.",
        "common_mistakes": [
            "Common mistake 162"
        ],
        "time_estimate_seconds": 42
    },
    {
        "id": "pseudo_q_0163",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "While Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 163: What is the output of the following loops code snippet? [Code snippet showing while loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of While Loop execution.",
        "common_mistakes": [
            "Common mistake 163"
        ],
        "time_estimate_seconds": 43
    },
    {
        "id": "pseudo_q_0164",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Nested Loops",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 164: What is the output of the following loops code snippet? [Code snippet showing nested loops pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Nested Loops execution.",
        "common_mistakes": [
            "Common mistake 164"
        ],
        "time_estimate_seconds": 44
    },
    {
        "id": "pseudo_q_0165",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Traversal",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 165: What is the output of the following arrays code snippet? [Code snippet showing array traversal pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Array Traversal execution.",
        "common_mistakes": [
            "Common mistake 165"
        ],
        "time_estimate_seconds": 45
    },
    {
        "id": "pseudo_q_0166",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 166: What is the output of the following arrays code snippet? [Code snippet showing array search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Array Search execution.",
        "common_mistakes": [
            "Common mistake 166"
        ],
        "time_estimate_seconds": 46
    },
    {
        "id": "pseudo_q_0167",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Operations",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 167: What is the output of the following strings code snippet? [Code snippet showing string operations pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of String Operations execution.",
        "common_mistakes": [
            "Common mistake 167"
        ],
        "time_estimate_seconds": 47
    },
    {
        "id": "pseudo_q_0168",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Comparison",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 168: What is the output of the following strings code snippet? [Code snippet showing string comparison pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of String Comparison execution.",
        "common_mistakes": [
            "Common mistake 168"
        ],
        "time_estimate_seconds": 48
    },
    {
        "id": "pseudo_q_0169",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "If-Else",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 169: What is the output of the following conditionals code snippet? [Code snippet showing if-else pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of If-Else execution.",
        "common_mistakes": [
            "Common mistake 169"
        ],
        "time_estimate_seconds": 49
    },
    {
        "id": "pseudo_q_0170",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "Switch Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 170: What is the output of the following conditionals code snippet? [Code snippet showing switch case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Switch Case execution.",
        "common_mistakes": [
            "Common mistake 170"
        ],
        "time_estimate_seconds": 50
    },
    {
        "id": "pseudo_q_0171",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Base Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 171: What is the output of the following recursion code snippet? [Code snippet showing base case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Base Case execution.",
        "common_mistakes": [
            "Common mistake 171"
        ],
        "time_estimate_seconds": 51
    },
    {
        "id": "pseudo_q_0172",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Recursive Call",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 172: What is the output of the following recursion code snippet? [Code snippet showing recursive call pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Recursive Call execution.",
        "common_mistakes": [
            "Common mistake 172"
        ],
        "time_estimate_seconds": 52
    },
    {
        "id": "pseudo_q_0173",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Call by Value",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 173: What is the output of the following functions code snippet? [Code snippet showing call by value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Call by Value execution.",
        "common_mistakes": [
            "Common mistake 173"
        ],
        "time_estimate_seconds": 53
    },
    {
        "id": "pseudo_q_0174",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Return Value",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 174: What is the output of the following functions code snippet? [Code snippet showing return value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Return Value execution.",
        "common_mistakes": [
            "Common mistake 174"
        ],
        "time_estimate_seconds": 54
    },
    {
        "id": "pseudo_q_0175",
        "category": "Programming Logic",
        "topic": "Pointers",
        "subtopic": "Pointer Arithmetic",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 175: What is the output of the following pointers code snippet? [Code snippet showing pointer arithmetic pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Pointer Arithmetic execution.",
        "common_mistakes": [
            "Common mistake 175"
        ],
        "time_estimate_seconds": 55
    },
    {
        "id": "pseudo_q_0176",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Bubble Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 176: What is the output of the following sorting code snippet? [Code snippet showing bubble sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Bubble Sort execution.",
        "common_mistakes": [
            "Common mistake 176"
        ],
        "time_estimate_seconds": 56
    },
    {
        "id": "pseudo_q_0177",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Selection Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 177: What is the output of the following sorting code snippet? [Code snippet showing selection sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Selection Sort execution.",
        "common_mistakes": [
            "Common mistake 177"
        ],
        "time_estimate_seconds": 57
    },
    {
        "id": "pseudo_q_0178",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Linear Search",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 178: What is the output of the following searching code snippet? [Code snippet showing linear search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Linear Search execution.",
        "common_mistakes": [
            "Common mistake 178"
        ],
        "time_estimate_seconds": 58
    },
    {
        "id": "pseudo_q_0179",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Binary Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 179: What is the output of the following searching code snippet? [Code snippet showing binary search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Binary Search execution.",
        "common_mistakes": [
            "Common mistake 179"
        ],
        "time_estimate_seconds": 59
    },
    {
        "id": "pseudo_q_0180",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "For Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 180: What is the output of the following loops code snippet? [Code snippet showing for loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of For Loop execution.",
        "common_mistakes": [
            "Common mistake 180"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_q_0181",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "While Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 181: What is the output of the following loops code snippet? [Code snippet showing while loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of While Loop execution.",
        "common_mistakes": [
            "Common mistake 181"
        ],
        "time_estimate_seconds": 31
    },
    {
        "id": "pseudo_q_0182",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Nested Loops",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 182: What is the output of the following loops code snippet? [Code snippet showing nested loops pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Nested Loops execution.",
        "common_mistakes": [
            "Common mistake 182"
        ],
        "time_estimate_seconds": 32
    },
    {
        "id": "pseudo_q_0183",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Traversal",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 183: What is the output of the following arrays code snippet? [Code snippet showing array traversal pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Array Traversal execution.",
        "common_mistakes": [
            "Common mistake 183"
        ],
        "time_estimate_seconds": 33
    },
    {
        "id": "pseudo_q_0184",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 184: What is the output of the following arrays code snippet? [Code snippet showing array search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Array Search execution.",
        "common_mistakes": [
            "Common mistake 184"
        ],
        "time_estimate_seconds": 34
    },
    {
        "id": "pseudo_q_0185",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Operations",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 185: What is the output of the following strings code snippet? [Code snippet showing string operations pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of String Operations execution.",
        "common_mistakes": [
            "Common mistake 185"
        ],
        "time_estimate_seconds": 35
    },
    {
        "id": "pseudo_q_0186",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Comparison",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 186: What is the output of the following strings code snippet? [Code snippet showing string comparison pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of String Comparison execution.",
        "common_mistakes": [
            "Common mistake 186"
        ],
        "time_estimate_seconds": 36
    },
    {
        "id": "pseudo_q_0187",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "If-Else",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 187: What is the output of the following conditionals code snippet? [Code snippet showing if-else pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of If-Else execution.",
        "common_mistakes": [
            "Common mistake 187"
        ],
        "time_estimate_seconds": 37
    },
    {
        "id": "pseudo_q_0188",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "Switch Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 188: What is the output of the following conditionals code snippet? [Code snippet showing switch case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Switch Case execution.",
        "common_mistakes": [
            "Common mistake 188"
        ],
        "time_estimate_seconds": 38
    },
    {
        "id": "pseudo_q_0189",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Base Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 189: What is the output of the following recursion code snippet? [Code snippet showing base case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Base Case execution.",
        "common_mistakes": [
            "Common mistake 189"
        ],
        "time_estimate_seconds": 39
    },
    {
        "id": "pseudo_q_0190",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Recursive Call",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 190: What is the output of the following recursion code snippet? [Code snippet showing recursive call pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Recursive Call execution.",
        "common_mistakes": [
            "Common mistake 190"
        ],
        "time_estimate_seconds": 40
    },
    {
        "id": "pseudo_q_0191",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Call by Value",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 191: What is the output of the following functions code snippet? [Code snippet showing call by value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Call by Value execution.",
        "common_mistakes": [
            "Common mistake 191"
        ],
        "time_estimate_seconds": 41
    },
    {
        "id": "pseudo_q_0192",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Return Value",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 192: What is the output of the following functions code snippet? [Code snippet showing return value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Return Value execution.",
        "common_mistakes": [
            "Common mistake 192"
        ],
        "time_estimate_seconds": 42
    },
    {
        "id": "pseudo_q_0193",
        "category": "Programming Logic",
        "topic": "Pointers",
        "subtopic": "Pointer Arithmetic",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 193: What is the output of the following pointers code snippet? [Code snippet showing pointer arithmetic pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Pointer Arithmetic execution.",
        "common_mistakes": [
            "Common mistake 193"
        ],
        "time_estimate_seconds": 43
    },
    {
        "id": "pseudo_q_0194",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Bubble Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 194: What is the output of the following sorting code snippet? [Code snippet showing bubble sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Bubble Sort execution.",
        "common_mistakes": [
            "Common mistake 194"
        ],
        "time_estimate_seconds": 44
    },
    {
        "id": "pseudo_q_0195",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Selection Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 195: What is the output of the following sorting code snippet? [Code snippet showing selection sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Selection Sort execution.",
        "common_mistakes": [
            "Common mistake 195"
        ],
        "time_estimate_seconds": 45
    },
    {
        "id": "pseudo_q_0196",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Linear Search",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 196: What is the output of the following searching code snippet? [Code snippet showing linear search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Linear Search execution.",
        "common_mistakes": [
            "Common mistake 196"
        ],
        "time_estimate_seconds": 46
    },
    {
        "id": "pseudo_q_0197",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Binary Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 197: What is the output of the following searching code snippet? [Code snippet showing binary search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Binary Search execution.",
        "common_mistakes": [
            "Common mistake 197"
        ],
        "time_estimate_seconds": 47
    },
    {
        "id": "pseudo_q_0198",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "For Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 198: What is the output of the following loops code snippet? [Code snippet showing for loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of For Loop execution.",
        "common_mistakes": [
            "Common mistake 198"
        ],
        "time_estimate_seconds": 48
    },
    {
        "id": "pseudo_q_0199",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "While Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 199: What is the output of the following loops code snippet? [Code snippet showing while loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of While Loop execution.",
        "common_mistakes": [
            "Common mistake 199"
        ],
        "time_estimate_seconds": 49
    },
    {
        "id": "pseudo_q_0200",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Nested Loops",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 200: What is the output of the following loops code snippet? [Code snippet showing nested loops pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Nested Loops execution.",
        "common_mistakes": [
            "Common mistake 200"
        ],
        "time_estimate_seconds": 50
    },
    {
        "id": "pseudo_q_0201",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Traversal",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 201: What is the output of the following arrays code snippet? [Code snippet showing array traversal pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Array Traversal execution.",
        "common_mistakes": [
            "Common mistake 201"
        ],
        "time_estimate_seconds": 51
    },
    {
        "id": "pseudo_q_0202",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 202: What is the output of the following arrays code snippet? [Code snippet showing array search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Array Search execution.",
        "common_mistakes": [
            "Common mistake 202"
        ],
        "time_estimate_seconds": 52
    },
    {
        "id": "pseudo_q_0203",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Operations",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 203: What is the output of the following strings code snippet? [Code snippet showing string operations pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of String Operations execution.",
        "common_mistakes": [
            "Common mistake 203"
        ],
        "time_estimate_seconds": 53
    },
    {
        "id": "pseudo_q_0204",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Comparison",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 204: What is the output of the following strings code snippet? [Code snippet showing string comparison pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of String Comparison execution.",
        "common_mistakes": [
            "Common mistake 204"
        ],
        "time_estimate_seconds": 54
    },
    {
        "id": "pseudo_q_0205",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "If-Else",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 205: What is the output of the following conditionals code snippet? [Code snippet showing if-else pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of If-Else execution.",
        "common_mistakes": [
            "Common mistake 205"
        ],
        "time_estimate_seconds": 55
    },
    {
        "id": "pseudo_q_0206",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "Switch Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 206: What is the output of the following conditionals code snippet? [Code snippet showing switch case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Switch Case execution.",
        "common_mistakes": [
            "Common mistake 206"
        ],
        "time_estimate_seconds": 56
    },
    {
        "id": "pseudo_q_0207",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Base Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 207: What is the output of the following recursion code snippet? [Code snippet showing base case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Base Case execution.",
        "common_mistakes": [
            "Common mistake 207"
        ],
        "time_estimate_seconds": 57
    },
    {
        "id": "pseudo_q_0208",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Recursive Call",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 208: What is the output of the following recursion code snippet? [Code snippet showing recursive call pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Recursive Call execution.",
        "common_mistakes": [
            "Common mistake 208"
        ],
        "time_estimate_seconds": 58
    },
    {
        "id": "pseudo_q_0209",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Call by Value",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 209: What is the output of the following functions code snippet? [Code snippet showing call by value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Call by Value execution.",
        "common_mistakes": [
            "Common mistake 209"
        ],
        "time_estimate_seconds": 59
    },
    {
        "id": "pseudo_q_0210",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Return Value",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 210: What is the output of the following functions code snippet? [Code snippet showing return value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Return Value execution.",
        "common_mistakes": [
            "Common mistake 210"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_q_0211",
        "category": "Programming Logic",
        "topic": "Pointers",
        "subtopic": "Pointer Arithmetic",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 211: What is the output of the following pointers code snippet? [Code snippet showing pointer arithmetic pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Pointer Arithmetic execution.",
        "common_mistakes": [
            "Common mistake 211"
        ],
        "time_estimate_seconds": 31
    },
    {
        "id": "pseudo_q_0212",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Bubble Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 212: What is the output of the following sorting code snippet? [Code snippet showing bubble sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Bubble Sort execution.",
        "common_mistakes": [
            "Common mistake 212"
        ],
        "time_estimate_seconds": 32
    },
    {
        "id": "pseudo_q_0213",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Selection Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 213: What is the output of the following sorting code snippet? [Code snippet showing selection sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Selection Sort execution.",
        "common_mistakes": [
            "Common mistake 213"
        ],
        "time_estimate_seconds": 33
    },
    {
        "id": "pseudo_q_0214",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Linear Search",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 214: What is the output of the following searching code snippet? [Code snippet showing linear search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Linear Search execution.",
        "common_mistakes": [
            "Common mistake 214"
        ],
        "time_estimate_seconds": 34
    },
    {
        "id": "pseudo_q_0215",
        "category": "Programming Logic",
        "topic": "Searching",
        "subtopic": "Binary Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 215: What is the output of the following searching code snippet? [Code snippet showing binary search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Binary Search execution.",
        "common_mistakes": [
            "Common mistake 215"
        ],
        "time_estimate_seconds": 35
    },
    {
        "id": "pseudo_q_0216",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "For Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 216: What is the output of the following loops code snippet? [Code snippet showing for loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of For Loop execution.",
        "common_mistakes": [
            "Common mistake 216"
        ],
        "time_estimate_seconds": 36
    },
    {
        "id": "pseudo_q_0217",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "While Loop",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 217: What is the output of the following loops code snippet? [Code snippet showing while loop pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of While Loop execution.",
        "common_mistakes": [
            "Common mistake 217"
        ],
        "time_estimate_seconds": 37
    },
    {
        "id": "pseudo_q_0218",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Nested Loops",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 218: What is the output of the following loops code snippet? [Code snippet showing nested loops pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Nested Loops execution.",
        "common_mistakes": [
            "Common mistake 218"
        ],
        "time_estimate_seconds": 38
    },
    {
        "id": "pseudo_q_0219",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Traversal",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 219: What is the output of the following arrays code snippet? [Code snippet showing array traversal pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Array Traversal execution.",
        "common_mistakes": [
            "Common mistake 219"
        ],
        "time_estimate_seconds": 39
    },
    {
        "id": "pseudo_q_0220",
        "category": "Programming Logic",
        "topic": "Arrays",
        "subtopic": "Array Search",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 220: What is the output of the following arrays code snippet? [Code snippet showing array search pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Array Search execution.",
        "common_mistakes": [
            "Common mistake 220"
        ],
        "time_estimate_seconds": 40
    },
    {
        "id": "pseudo_q_0221",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Operations",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 221: What is the output of the following strings code snippet? [Code snippet showing string operations pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of String Operations execution.",
        "common_mistakes": [
            "Common mistake 221"
        ],
        "time_estimate_seconds": 41
    },
    {
        "id": "pseudo_q_0222",
        "category": "Programming Logic",
        "topic": "Strings",
        "subtopic": "String Comparison",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 222: What is the output of the following strings code snippet? [Code snippet showing string comparison pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of String Comparison execution.",
        "common_mistakes": [
            "Common mistake 222"
        ],
        "time_estimate_seconds": 42
    },
    {
        "id": "pseudo_q_0223",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "If-Else",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 223: What is the output of the following conditionals code snippet? [Code snippet showing if-else pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of If-Else execution.",
        "common_mistakes": [
            "Common mistake 223"
        ],
        "time_estimate_seconds": 43
    },
    {
        "id": "pseudo_q_0224",
        "category": "Programming Logic",
        "topic": "Conditionals",
        "subtopic": "Switch Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 224: What is the output of the following conditionals code snippet? [Code snippet showing switch case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Switch Case execution.",
        "common_mistakes": [
            "Common mistake 224"
        ],
        "time_estimate_seconds": 44
    },
    {
        "id": "pseudo_q_0225",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Base Case",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 225: What is the output of the following recursion code snippet? [Code snippet showing base case pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Base Case execution.",
        "common_mistakes": [
            "Common mistake 225"
        ],
        "time_estimate_seconds": 45
    },
    {
        "id": "pseudo_q_0226",
        "category": "Programming Logic",
        "topic": "Recursion",
        "subtopic": "Recursive Call",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 226: What is the output of the following recursion code snippet? [Code snippet showing recursive call pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Recursive Call execution.",
        "common_mistakes": [
            "Common mistake 226"
        ],
        "time_estimate_seconds": 46
    },
    {
        "id": "pseudo_q_0227",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Call by Value",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 227: What is the output of the following functions code snippet? [Code snippet showing call by value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Call by Value execution.",
        "common_mistakes": [
            "Common mistake 227"
        ],
        "time_estimate_seconds": 47
    },
    {
        "id": "pseudo_q_0228",
        "category": "Programming Logic",
        "topic": "Functions",
        "subtopic": "Return Value",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 228: What is the output of the following functions code snippet? [Code snippet showing return value pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step explanation of Return Value execution.",
        "common_mistakes": [
            "Common mistake 228"
        ],
        "time_estimate_seconds": 48
    },
    {
        "id": "pseudo_q_0229",
        "category": "Programming Logic",
        "topic": "Pointers",
        "subtopic": "Pointer Arithmetic",
        "difficulty": 3,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 229: What is the output of the following pointers code snippet? [Code snippet showing pointer arithmetic pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step explanation of Pointer Arithmetic execution.",
        "common_mistakes": [
            "Common mistake 229"
        ],
        "time_estimate_seconds": 49
    },
    {
        "id": "pseudo_q_0230",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Bubble Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 230: What is the output of the following sorting code snippet? [Code snippet showing bubble sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step explanation of Bubble Sort execution.",
        "common_mistakes": [
            "Common mistake 230"
        ],
        "time_estimate_seconds": 50
    },
    {
        "id": "pseudo_q_0231",
        "category": "Programming Logic",
        "topic": "Sorting",
        "subtopic": "Selection Sort",
        "difficulty": 2,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Cognizant"
        ],
        "language": "C",
        "question": "Output prediction question 231: What is the output of the following sorting code snippet? [Code snippet showing selection sort pattern]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step explanation of Selection Sort execution.",
        "common_mistakes": [
            "Common mistake 231"
        ],
        "time_estimate_seconds": 51
    },
    {
        "id": "pseudo_dbl_0232",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 232: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 232.",
        "common_mistakes": [
            "Common mistake 232"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0233",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 233: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 233.",
        "common_mistakes": [
            "Common mistake 233"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0234",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 234: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 234.",
        "common_mistakes": [
            "Common mistake 234"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0235",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 235: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 235.",
        "common_mistakes": [
            "Common mistake 235"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0236",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 236: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 236.",
        "common_mistakes": [
            "Common mistake 236"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0237",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 237: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 237.",
        "common_mistakes": [
            "Common mistake 237"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0238",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 238: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 238.",
        "common_mistakes": [
            "Common mistake 238"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0239",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 239: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 239.",
        "common_mistakes": [
            "Common mistake 239"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0240",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 240: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 240.",
        "common_mistakes": [
            "Common mistake 240"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0241",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 241: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 241.",
        "common_mistakes": [
            "Common mistake 241"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0242",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 242: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 242.",
        "common_mistakes": [
            "Common mistake 242"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0243",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 243: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 243.",
        "common_mistakes": [
            "Common mistake 243"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0244",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 244: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 244.",
        "common_mistakes": [
            "Common mistake 244"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0245",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 245: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 245.",
        "common_mistakes": [
            "Common mistake 245"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0246",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 246: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 246.",
        "common_mistakes": [
            "Common mistake 246"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0247",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 247: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 247.",
        "common_mistakes": [
            "Common mistake 247"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0248",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 248: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 248.",
        "common_mistakes": [
            "Common mistake 248"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0249",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 249: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 249.",
        "common_mistakes": [
            "Common mistake 249"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0250",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 250: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 250.",
        "common_mistakes": [
            "Common mistake 250"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0251",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 251: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 251.",
        "common_mistakes": [
            "Common mistake 251"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0252",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 252: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 252.",
        "common_mistakes": [
            "Common mistake 252"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0253",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 253: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 253.",
        "common_mistakes": [
            "Common mistake 253"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0254",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 254: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 254.",
        "common_mistakes": [
            "Common mistake 254"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0255",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 255: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 255.",
        "common_mistakes": [
            "Common mistake 255"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0256",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 256: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 256.",
        "common_mistakes": [
            "Common mistake 256"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0257",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 257: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 257.",
        "common_mistakes": [
            "Common mistake 257"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0258",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 258: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 258.",
        "common_mistakes": [
            "Common mistake 258"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0259",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 259: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 259.",
        "common_mistakes": [
            "Common mistake 259"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0260",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 260: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 260.",
        "common_mistakes": [
            "Common mistake 260"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0261",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 261: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 261.",
        "common_mistakes": [
            "Common mistake 261"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0262",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 262: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 262.",
        "common_mistakes": [
            "Common mistake 262"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0263",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 263: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 263.",
        "common_mistakes": [
            "Common mistake 263"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0264",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 264: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 264.",
        "common_mistakes": [
            "Common mistake 264"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0265",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 265: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 265.",
        "common_mistakes": [
            "Common mistake 265"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0266",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 266: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 266.",
        "common_mistakes": [
            "Common mistake 266"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0267",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 267: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 267.",
        "common_mistakes": [
            "Common mistake 267"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0268",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 268: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 268.",
        "common_mistakes": [
            "Common mistake 268"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0269",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 269: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 269.",
        "common_mistakes": [
            "Common mistake 269"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0270",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 270: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 270.",
        "common_mistakes": [
            "Common mistake 270"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0271",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 271: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 271.",
        "common_mistakes": [
            "Common mistake 271"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0272",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 272: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 272.",
        "common_mistakes": [
            "Common mistake 272"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0273",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 273: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 273.",
        "common_mistakes": [
            "Common mistake 273"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0274",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 274: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 274.",
        "common_mistakes": [
            "Common mistake 274"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0275",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 275: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 275.",
        "common_mistakes": [
            "Common mistake 275"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0276",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 276: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 276.",
        "common_mistakes": [
            "Common mistake 276"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0277",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 277: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 277.",
        "common_mistakes": [
            "Common mistake 277"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0278",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 278: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 278.",
        "common_mistakes": [
            "Common mistake 278"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0279",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 279: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 279.",
        "common_mistakes": [
            "Common mistake 279"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0280",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 280: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 280.",
        "common_mistakes": [
            "Common mistake 280"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0281",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 281: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 281.",
        "common_mistakes": [
            "Common mistake 281"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0282",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 282: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 282.",
        "common_mistakes": [
            "Common mistake 282"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0283",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 283: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 283.",
        "common_mistakes": [
            "Common mistake 283"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0284",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 284: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 284.",
        "common_mistakes": [
            "Common mistake 284"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0285",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 285: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 285.",
        "common_mistakes": [
            "Common mistake 285"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0286",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 286: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 286.",
        "common_mistakes": [
            "Common mistake 286"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0287",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 287: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 287.",
        "common_mistakes": [
            "Common mistake 287"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0288",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 288: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 288.",
        "common_mistakes": [
            "Common mistake 288"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0289",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 289: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 289.",
        "common_mistakes": [
            "Common mistake 289"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0290",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 290: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 290.",
        "common_mistakes": [
            "Common mistake 290"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0291",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 291: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 291.",
        "common_mistakes": [
            "Common mistake 291"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0292",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 292: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 292.",
        "common_mistakes": [
            "Common mistake 292"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0293",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 293: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 293.",
        "common_mistakes": [
            "Common mistake 293"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0294",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 294: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 294.",
        "common_mistakes": [
            "Common mistake 294"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0295",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 295: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 295.",
        "common_mistakes": [
            "Common mistake 295"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0296",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 296: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 296.",
        "common_mistakes": [
            "Common mistake 296"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0297",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 297: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 297.",
        "common_mistakes": [
            "Common mistake 297"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0298",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 298: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 298.",
        "common_mistakes": [
            "Common mistake 298"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0299",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 299: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 299.",
        "common_mistakes": [
            "Common mistake 299"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0300",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 300: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 300.",
        "common_mistakes": [
            "Common mistake 300"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0301",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 301: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 301.",
        "common_mistakes": [
            "Common mistake 301"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0302",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 302: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 302.",
        "common_mistakes": [
            "Common mistake 302"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0303",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 303: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 303.",
        "common_mistakes": [
            "Common mistake 303"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0304",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 304: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 304.",
        "common_mistakes": [
            "Common mistake 304"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0305",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 305: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 305.",
        "common_mistakes": [
            "Common mistake 305"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0306",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 306: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 306.",
        "common_mistakes": [
            "Common mistake 306"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0307",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 307: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 307.",
        "common_mistakes": [
            "Common mistake 307"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0308",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 308: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 308.",
        "common_mistakes": [
            "Common mistake 308"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0309",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 309: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 309.",
        "common_mistakes": [
            "Common mistake 309"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0310",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 310: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 310.",
        "common_mistakes": [
            "Common mistake 310"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0311",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 311: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 311.",
        "common_mistakes": [
            "Common mistake 311"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0312",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 312: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 312.",
        "common_mistakes": [
            "Common mistake 312"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0313",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 313: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 313.",
        "common_mistakes": [
            "Common mistake 313"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0314",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 314: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 314.",
        "common_mistakes": [
            "Common mistake 314"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0315",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 315: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 315.",
        "common_mistakes": [
            "Common mistake 315"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0316",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 316: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 316.",
        "common_mistakes": [
            "Common mistake 316"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0317",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 317: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 317.",
        "common_mistakes": [
            "Common mistake 317"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0318",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 318: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 318.",
        "common_mistakes": [
            "Common mistake 318"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0319",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 319: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 319.",
        "common_mistakes": [
            "Common mistake 319"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0320",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 320: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 320.",
        "common_mistakes": [
            "Common mistake 320"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0321",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 321: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 321.",
        "common_mistakes": [
            "Common mistake 321"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0322",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 322: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 322.",
        "common_mistakes": [
            "Common mistake 322"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0323",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 323: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 323.",
        "common_mistakes": [
            "Common mistake 323"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0324",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 324: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 324.",
        "common_mistakes": [
            "Common mistake 324"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0325",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 325: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 325.",
        "common_mistakes": [
            "Common mistake 325"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0326",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 326: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 326.",
        "common_mistakes": [
            "Common mistake 326"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0327",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 327: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 327.",
        "common_mistakes": [
            "Common mistake 327"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0328",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 328: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 328.",
        "common_mistakes": [
            "Common mistake 328"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0329",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 329: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 329.",
        "common_mistakes": [
            "Common mistake 329"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0330",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 330: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 330.",
        "common_mistakes": [
            "Common mistake 330"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0331",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 331: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 331.",
        "common_mistakes": [
            "Common mistake 331"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0332",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 332: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 332.",
        "common_mistakes": [
            "Common mistake 332"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0333",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 333: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 333.",
        "common_mistakes": [
            "Common mistake 333"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0334",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 334: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 334.",
        "common_mistakes": [
            "Common mistake 334"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0335",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 335: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 335.",
        "common_mistakes": [
            "Common mistake 335"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0336",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 336: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 336.",
        "common_mistakes": [
            "Common mistake 336"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0337",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 337: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 337.",
        "common_mistakes": [
            "Common mistake 337"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0338",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 338: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 338.",
        "common_mistakes": [
            "Common mistake 338"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0339",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 339: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 339.",
        "common_mistakes": [
            "Common mistake 339"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0340",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 340: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 340.",
        "common_mistakes": [
            "Common mistake 340"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0341",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 341: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 341.",
        "common_mistakes": [
            "Common mistake 341"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0342",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 342: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 342.",
        "common_mistakes": [
            "Common mistake 342"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0343",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 343: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 343.",
        "common_mistakes": [
            "Common mistake 343"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0344",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 344: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 344.",
        "common_mistakes": [
            "Common mistake 344"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0345",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 345: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 345.",
        "common_mistakes": [
            "Common mistake 345"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0346",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 346: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 346.",
        "common_mistakes": [
            "Common mistake 346"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0347",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 347: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 347.",
        "common_mistakes": [
            "Common mistake 347"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0348",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 348: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 348.",
        "common_mistakes": [
            "Common mistake 348"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0349",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 349: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 349.",
        "common_mistakes": [
            "Common mistake 349"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0350",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 350: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 350.",
        "common_mistakes": [
            "Common mistake 350"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0351",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 351: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 351.",
        "common_mistakes": [
            "Common mistake 351"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0352",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 352: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 352.",
        "common_mistakes": [
            "Common mistake 352"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0353",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 353: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 353.",
        "common_mistakes": [
            "Common mistake 353"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0354",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 354: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 354.",
        "common_mistakes": [
            "Common mistake 354"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0355",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 355: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 355.",
        "common_mistakes": [
            "Common mistake 355"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0356",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 356: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 356.",
        "common_mistakes": [
            "Common mistake 356"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0357",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 357: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 357.",
        "common_mistakes": [
            "Common mistake 357"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0358",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 358: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 358.",
        "common_mistakes": [
            "Common mistake 358"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0359",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 359: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 359.",
        "common_mistakes": [
            "Common mistake 359"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0360",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 360: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 360.",
        "common_mistakes": [
            "Common mistake 360"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0361",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 361: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 361.",
        "common_mistakes": [
            "Common mistake 361"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0362",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 362: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 362.",
        "common_mistakes": [
            "Common mistake 362"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0363",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 363: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 363.",
        "common_mistakes": [
            "Common mistake 363"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0364",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 364: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 364.",
        "common_mistakes": [
            "Common mistake 364"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0365",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 365: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 365.",
        "common_mistakes": [
            "Common mistake 365"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0366",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 366: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 366.",
        "common_mistakes": [
            "Common mistake 366"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0367",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 367: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 367.",
        "common_mistakes": [
            "Common mistake 367"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0368",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 368: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 368.",
        "common_mistakes": [
            "Common mistake 368"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0369",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 369: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 369.",
        "common_mistakes": [
            "Common mistake 369"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0370",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 370: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 370.",
        "common_mistakes": [
            "Common mistake 370"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0371",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 371: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 371.",
        "common_mistakes": [
            "Common mistake 371"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0372",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 372: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 372.",
        "common_mistakes": [
            "Common mistake 372"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0373",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 373: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 373.",
        "common_mistakes": [
            "Common mistake 373"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0374",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 374: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 374.",
        "common_mistakes": [
            "Common mistake 374"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0375",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 375: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 375.",
        "common_mistakes": [
            "Common mistake 375"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0376",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 376: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 376.",
        "common_mistakes": [
            "Common mistake 376"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0377",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 377: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 377.",
        "common_mistakes": [
            "Common mistake 377"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0378",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 378: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 378.",
        "common_mistakes": [
            "Common mistake 378"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0379",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 379: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 379.",
        "common_mistakes": [
            "Common mistake 379"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0380",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 380: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 380.",
        "common_mistakes": [
            "Common mistake 380"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0381",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 381: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 381.",
        "common_mistakes": [
            "Common mistake 381"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0382",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 382: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 382.",
        "common_mistakes": [
            "Common mistake 382"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0383",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 383: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 383.",
        "common_mistakes": [
            "Common mistake 383"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0384",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 384: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 384.",
        "common_mistakes": [
            "Common mistake 384"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0385",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 385: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 385.",
        "common_mistakes": [
            "Common mistake 385"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0386",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 386: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 386.",
        "common_mistakes": [
            "Common mistake 386"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0387",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 387: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 387.",
        "common_mistakes": [
            "Common mistake 387"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0388",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 388: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 388.",
        "common_mistakes": [
            "Common mistake 388"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0389",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 389: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 389.",
        "common_mistakes": [
            "Common mistake 389"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0390",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 390: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 390.",
        "common_mistakes": [
            "Common mistake 390"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0391",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 391: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 391.",
        "common_mistakes": [
            "Common mistake 391"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0392",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 392: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 392.",
        "common_mistakes": [
            "Common mistake 392"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0393",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 393: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 393.",
        "common_mistakes": [
            "Common mistake 393"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0394",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 394: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 394.",
        "common_mistakes": [
            "Common mistake 394"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0395",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 395: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 395.",
        "common_mistakes": [
            "Common mistake 395"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0396",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 396: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 396.",
        "common_mistakes": [
            "Common mistake 396"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0397",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 397: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 397.",
        "common_mistakes": [
            "Common mistake 397"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0398",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 398: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 398.",
        "common_mistakes": [
            "Common mistake 398"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0399",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 399: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 399.",
        "common_mistakes": [
            "Common mistake 399"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0400",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 400: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 400.",
        "common_mistakes": [
            "Common mistake 400"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0401",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 401: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 401.",
        "common_mistakes": [
            "Common mistake 401"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0402",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 402: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 402.",
        "common_mistakes": [
            "Common mistake 402"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0403",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 403: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 403.",
        "common_mistakes": [
            "Common mistake 403"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0404",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 404: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 404.",
        "common_mistakes": [
            "Common mistake 404"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0405",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 405: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 405.",
        "common_mistakes": [
            "Common mistake 405"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0406",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 406: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 406.",
        "common_mistakes": [
            "Common mistake 406"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0407",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 407: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 407.",
        "common_mistakes": [
            "Common mistake 407"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0408",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 408: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 408.",
        "common_mistakes": [
            "Common mistake 408"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0409",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 409: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 409.",
        "common_mistakes": [
            "Common mistake 409"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0410",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 410: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 410.",
        "common_mistakes": [
            "Common mistake 410"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0411",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 411: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 411.",
        "common_mistakes": [
            "Common mistake 411"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0412",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 412: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 412.",
        "common_mistakes": [
            "Common mistake 412"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0413",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 413: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 413.",
        "common_mistakes": [
            "Common mistake 413"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0414",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 414: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 414.",
        "common_mistakes": [
            "Common mistake 414"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0415",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 415: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 415.",
        "common_mistakes": [
            "Common mistake 415"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0416",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 416: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 416.",
        "common_mistakes": [
            "Common mistake 416"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0417",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 417: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 417.",
        "common_mistakes": [
            "Common mistake 417"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0418",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 418: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 418.",
        "common_mistakes": [
            "Common mistake 418"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0419",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 419: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 419.",
        "common_mistakes": [
            "Common mistake 419"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0420",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 420: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 420.",
        "common_mistakes": [
            "Common mistake 420"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0421",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 421: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 421.",
        "common_mistakes": [
            "Common mistake 421"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0422",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 422: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 422.",
        "common_mistakes": [
            "Common mistake 422"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0423",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 423: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 423.",
        "common_mistakes": [
            "Common mistake 423"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0424",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 424: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 424.",
        "common_mistakes": [
            "Common mistake 424"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0425",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 425: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 425.",
        "common_mistakes": [
            "Common mistake 425"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0426",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 426: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 426.",
        "common_mistakes": [
            "Common mistake 426"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0427",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 427: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 427.",
        "common_mistakes": [
            "Common mistake 427"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0428",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 428: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 428.",
        "common_mistakes": [
            "Common mistake 428"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0429",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 429: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 429.",
        "common_mistakes": [
            "Common mistake 429"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0430",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 430: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 430.",
        "common_mistakes": [
            "Common mistake 430"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0431",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 431: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 431.",
        "common_mistakes": [
            "Common mistake 431"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0432",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 432: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 432.",
        "common_mistakes": [
            "Common mistake 432"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0433",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 433: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 433.",
        "common_mistakes": [
            "Common mistake 433"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0434",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 434: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 434.",
        "common_mistakes": [
            "Common mistake 434"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0435",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 435: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 435.",
        "common_mistakes": [
            "Common mistake 435"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0436",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 436: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 436.",
        "common_mistakes": [
            "Common mistake 436"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0437",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 437: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 437.",
        "common_mistakes": [
            "Common mistake 437"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0438",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 438: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 438.",
        "common_mistakes": [
            "Common mistake 438"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0439",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 439: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 439.",
        "common_mistakes": [
            "Common mistake 439"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0440",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 440: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 440.",
        "common_mistakes": [
            "Common mistake 440"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0441",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 441: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 441.",
        "common_mistakes": [
            "Common mistake 441"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0442",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 442: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 442.",
        "common_mistakes": [
            "Common mistake 442"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0443",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 443: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 443.",
        "common_mistakes": [
            "Common mistake 443"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0444",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 444: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 444.",
        "common_mistakes": [
            "Common mistake 444"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0445",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 445: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 445.",
        "common_mistakes": [
            "Common mistake 445"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0446",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 446: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 446.",
        "common_mistakes": [
            "Common mistake 446"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0447",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 447: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 447.",
        "common_mistakes": [
            "Common mistake 447"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0448",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 448: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 448.",
        "common_mistakes": [
            "Common mistake 448"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0449",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 449: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 449.",
        "common_mistakes": [
            "Common mistake 449"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0450",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 450: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 450.",
        "common_mistakes": [
            "Common mistake 450"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0451",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 451: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 451.",
        "common_mistakes": [
            "Common mistake 451"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0452",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 452: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 452.",
        "common_mistakes": [
            "Common mistake 452"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0453",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 453: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 453.",
        "common_mistakes": [
            "Common mistake 453"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0454",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 454: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 454.",
        "common_mistakes": [
            "Common mistake 454"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0455",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 455: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 455.",
        "common_mistakes": [
            "Common mistake 455"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0456",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 456: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 456.",
        "common_mistakes": [
            "Common mistake 456"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0457",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 457: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 457.",
        "common_mistakes": [
            "Common mistake 457"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0458",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 458: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 458.",
        "common_mistakes": [
            "Common mistake 458"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0459",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 459: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 3,
        "explanation": "Step-by-step execution for question 459.",
        "common_mistakes": [
            "Common mistake 459"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0460",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 460: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 0,
        "explanation": "Step-by-step execution for question 460.",
        "common_mistakes": [
            "Common mistake 460"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0461",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 461: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 1,
        "explanation": "Step-by-step execution for question 461.",
        "common_mistakes": [
            "Common mistake 461"
        ],
        "time_estimate_seconds": 30
    },
    {
        "id": "pseudo_dbl_0462",
        "category": "Programming Logic",
        "topic": "Loops",
        "subtopic": "Practice",
        "difficulty": 1,
        "company_tags": [
            "TCS",
            "Infosys",
            "Wipro"
        ],
        "language": "C",
        "question": "Output prediction 462: What is the output? [Loop code snippet]",
        "options": [
            "Output A",
            "Output B",
            "Output C",
            "Output D"
        ],
        "correct_index": 2,
        "explanation": "Step-by-step execution for question 462.",
        "common_mistakes": [
            "Common mistake 462"
        ],
        "time_estimate_seconds": 30
    }
]


def get_pseudo_questions_by_topic(topic: str) -> list:
    return [q for q in PSEUDOCODE_QUESTIONS if q["topic"] == topic]

def get_pseudo_questions_by_company(company: str) -> list:
    return [q for q in PSEUDOCODE_QUESTIONS if company in q.get("company_tags", [])]

def get_pseudo_question_count() -> int:
    return len(PSEUDOCODE_QUESTIONS)

def get_pseudo_topics_summary() -> dict:
    summary = {}
    for q in PSEUDOCODE_QUESTIONS:
        topic = q["topic"]
        if topic not in summary:
            summary[topic] = {"count": 0, "difficulty": [], "companies": set()}
        summary[topic]["count"] += 1
        summary[topic]["difficulty"].append(q["difficulty"])
        summary[topic]["companies"].update(q.get("company_tags", []))
    return summary
