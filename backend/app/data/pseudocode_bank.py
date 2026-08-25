"""
Pseudocode Dry-Run Bank — Infosys-style tracing drills.

Static curated questions where the candidate must predict output WITHOUT a
compiler: operator precedence, pre/post increments, bitwise shifts, nested
loop tracing, recursion trees, string slicing. Zero AI cost, zero DB writes.

Schema mirrors the aptitude banks so grading stays `answer.strip().lower() ==
correct_answer.strip().lower()`. All answers hand-verified assuming strict
left-to-right evaluation and integer division where declared.
"""

PSEUDOCODE_QUESTIONS = [
    # ---------- Operators & Increments ----------
    {
        "id": "pc001",
        "sub_category": "Operators",
        "question": (
            "int a = 5;\nint b = a++ + ++a;\nprint(b);\n\n"
            "What is printed? Dry run without a compiler."
        ),
        "options": ["12", "11", "10", "13"],
        "correct_answer": "12",
        "explanation": (
            "a++ yields 5 then a becomes 6. ++a makes a 7 and yields 7. "
            "So b = 5 + 7 = 12."
        ),
    },
    {
        "id": "pc002",
        "sub_category": "Operators",
        "question": (
            "int x = 3;\nint y = ++x * 2 + x--;\nprint(y);"
        ),
        "options": ["12", "13", "11", "10"],
        "correct_answer": "12",
        "explanation": (
            "++x -> x becomes 4, term is 4*2 = 8. x-- yields 4, then x becomes 3. "
            "y = 8 + 4 = 12."
        ),
    },
    {
        "id": "pc003",
        "sub_category": "Operators",
        "question": (
            "int a = 10;\nprint(a++ + a++ + ++a);"
        ),
        "options": ["34", "33", "35", "36"],
        "correct_answer": "34",
        "explanation": (
            "First a++ yields 10 (a=11). Second a++ yields 11 (a=12). "
            "++a yields 13. Sum = 10 + 11 + 13 = 34."
        ),
    },
    {
        "id": "pc004",
        "sub_category": "Operators",
        "question": (
            "int v = 9;\nprint(v / 2 + v % 2);   // integer division"
        ),
        "options": ["5", "4", "4.5", "6"],
        "correct_answer": "5",
        "explanation": "v/2 = 4 (integer division). v%2 = 1. Total = 5.",
    },
    {
        "id": "pc005",
        "sub_category": "Operators",
        "question": (
            "int a = 4;\nint b = 5;\nprint((a > b) ? a * b : a + b);"
        ),
        "options": ["9", "20", "true", "error"],
        "correct_answer": "9",
        "explanation": "a > b is false (4 > 5 fails), so the ternary yields a + b = 9.",
    },
    {
        "id": "pc006",
        "sub_category": "Operators",
        "question": (
            "print(5 == 5 == 5)"
        ),
        "options": ["false", "true", "error", "5"],
        "correct_answer": "false",
        "explanation": (
            "Chained comparison runs left to right: (5 == 5) -> true, "
            "then true == 5 is false."
        ),
    },
    {
        "id": "pc007",
        "sub_category": "Operators",
        "question": (
            "int c = 3;\nint d = c-- - --c;\nprint(d); print(c);"
        ),
        "options": ["d=2, c=1", "d=1, c=2", "d=3, c=1", "d=2, c=2"],
        "correct_answer": "d=2, c=1",
        "explanation": (
            "c-- yields 3, then c becomes 2. --c makes c 1 and yields 1. "
            "d = 3 - 1 = 2, and c ends at 1."
        ),
    },

    # ---------- Bitwise ----------
    {
        "id": "pc010",
        "sub_category": "Bitwise",
        "question": "int x = 8;\nprint(x << 2);",
        "options": ["32", "16", "24", "4"],
        "correct_answer": "32",
        "explanation": "Left-shifting by 2 multiplies by 4: 8 * 4 = 32.",
    },
    {
        "id": "pc011",
        "sub_category": "Bitwise",
        "question": "int x = 20;\nprint(x >> 2);",
        "options": ["5", "10", "4", "2"],
        "correct_answer": "5",
        "explanation": "Right-shifting by 2 divides by 4: 20 / 4 = 5.",
    },
    {
        "id": "pc012",
        "sub_category": "Bitwise",
        "question": "print(6 & 3)",
        "options": ["2", "1", "0", "3"],
        "correct_answer": "2",
        "explanation": "110 & 011 = 010 -> 2.",
    },
    {
        "id": "pc013",
        "sub_category": "Bitwise",
        "question": "print(6 | 3)",
        "options": ["7", "2", "9", "1"],
        "correct_answer": "7",
        "explanation": "110 | 011 = 111 -> 7.",
    },
    {
        "id": "pc014",
        "sub_category": "Bitwise",
        "question": "print(5 ^ 3)",
        "options": ["6", "1", "8", "2"],
        "correct_answer": "6",
        "explanation": "101 XOR 011 = 110 -> 6.",
    },
    {
        "id": "pc015",
        "sub_category": "Bitwise",
        "question": (
            "int n = 16;\ncount = 0;\nwhile (n > 1) {\n  n = n >> 1;\n  count++;\n}\nprint(count);"
        ),
        "options": ["4", "5", "3", "16"],
        "correct_answer": "4",
        "explanation": "Halving until 1: 16->8->4->2->1 takes 4 shifts (log2 of 16).",
    },
    {
        "id": "pc016",
        "sub_category": "Bitwise",
        "question": "print(1 << 3 | 1 << 1)",
        "options": ["10", "8", "16", "6"],
        "correct_answer": "10",
        "explanation": "<< binds tighter than |: (1<<3)=8, (1<<1)=2, 8 | 2 = 1010 -> 10.",
    },

    # ---------- Loops ----------
    {
        "id": "pc020",
        "sub_category": "Loops",
        "question": (
            "s = 0;\nfor (i = 1; i <= 5; i++) {\n  if (i % 2 == 0) continue;\n  s += i;\n}\nprint(s);"
        ),
        "options": ["9", "15", "6", "25"],
        "correct_answer": "9",
        "explanation": "continue skips evens: 1 + 3 + 5 = 9.",
    },
    {
        "id": "pc021",
        "sub_category": "Loops",
        "question": (
            "i = 1;\nwhile (i < 10) {\n  i = i * 2;\n}\nprint(i);"
        ),
        "options": ["16", "8", "10", "32"],
        "correct_answer": "16",
        "explanation": "1->2->4->8->16. The loop exits once i >= 10, so it prints 16.",
    },
    {
        "id": "pc022",
        "sub_category": "Loops",
        "question": (
            "count = 0;\nfor (i = 0; i < 3; i++) {\n  for (j = 0; j <= i; j++) {\n    count++;\n  }\n}\nprint(count);"
        ),
        "options": ["6", "9", "5", "3"],
        "correct_answer": "6",
        "explanation": "The inner loop runs 1 + 2 + 3 times = 6.",
    },
    {
        "id": "pc023",
        "sub_category": "Loops",
        "question": (
            "for (i = 0; i < 5; i++) {\n  if (i == 3) break;\n}\nprint(i);"
        ),
        "options": ["3", "5", "4", "0"],
        "correct_answer": "3",
        "explanation": "break fires when i == 3, so i stays 3.",
    },
    {
        "id": "pc024",
        "sub_category": "Loops",
        "question": (
            "n = 100;\nc = 0;\nwhile (n > 0) {\n  n = n / 10;   // integer division\n  c++;\n}\nprint(c);"
        ),
        "options": ["3", "2", "1", "infinite"],
        "correct_answer": "3",
        "explanation": "Integer division: 100->10->1->0, three iterations.",
    },
    {
        "id": "pc025",
        "sub_category": "Loops",
        "question": (
            "x = 5;\ny = 0;\ndo {\n  y += x;\n  x--;\n} while (x > 0);\nprint(y);"
        ),
        "options": ["15", "10", "20", "5"],
        "correct_answer": "15",
        "explanation": "Runs for x = 5,4,3,2,1: 5+4+3+2+1 = 15.",
    },
    {
        "id": "pc026",
        "sub_category": "Loops",
        "question": (
            "total = 0;\nfor (i = 10; i > 0; i -= 3) {\n  total++;\n}\nprint(total);"
        ),
        "options": ["4", "3", "5", "10"],
        "correct_answer": "4",
        "explanation": "i takes 10, 7, 4, 1, then -2 exits the loop. Four iterations.",
    },

    # ---------- Recursion ----------
    {
        "id": "pc030",
        "sub_category": "Recursion",
        "question": (
            "function f(n):\n  if n <= 1: return 1\n  return n * f(n - 2)\n\nprint(f(7));"
        ),
        "options": ["105", "5040", "48", "21"],
        "correct_answer": "105",
        "explanation": "f(7) = 7 * f(5) = 7*5 * f(3) = 7*5*3 * f(1) = 105. Odd factorial.",
    },
    {
        "id": "pc031",
        "sub_category": "Recursion",
        "question": (
            "function g(n):\n  if n == 0: return 0\n  return n + g(n / 2)\n  // integer division\n\nprint(g(8));"
        ),
        "options": ["15", "12", "16", "8"],
        "correct_answer": "15",
        "explanation": "g(8)=8+g(4)=8+4+g(2)=8+4+2+g(1)=8+4+2+1+g(0)=15.",
    },
    {
        "id": "pc032",
        "sub_category": "Recursion",
        "question": (
            "function mystery(a, b):\n  if b == 0: return a\n  return mystery(b, a % b)\n\nprint(mystery(12, 18));"
        ),
        "options": ["6", "3", "2", "9"],
        "correct_answer": "6",
        "explanation": (
            "Euclid's algorithm (GCD): mystery(12,18)->mystery(18,12)"
            "->mystery(12,6)->mystery(6,0)=6."
        ),
    },
    {
        "id": "pc033",
        "sub_category": "Recursion",
        "question": (
            "function p(n):\n  if n > 1:\n    p(n / 2)\n  print(n)\n  // integer division\n\np(8);"
        ),
        "options": ["1 2 4 8", "8 4 2 1", "8 4 2", "1 2 8"],
        "correct_answer": "1 2 4 8",
        "explanation": "Recursive calls happen before printing, so output unwinds 1, 2, 4, 8.",
    },
    {
        "id": "pc034",
        "sub_category": "Recursion",
        "question": (
            "function h(n):\n  if n <= 0: return 0\n  return h(n - 1) + 2\n\nprint(h(5) - h(3));"
        ),
        "options": ["4", "2", "6", "10"],
        "correct_answer": "4",
        "explanation": "h(n) returns 2*n: h(5)=10, h(3)=6, difference 4.",
    },

    # ---------- Conditionals ----------
    {
        "id": "pc040",
        "sub_category": "Conditionals",
        "question": (
            "x = 10;\nif (x > 5)\n  if (x > 20)\n    print(\"A\")\n  else\n    print(\"B\")\nelse\n  print(\"C\")"
        ),
        "options": ["B", "A", "C", "nothing"],
        "correct_answer": "B",
        "explanation": "The else binds to the nearest if: inner condition false -> B.",
    },
    {
        "id": "pc041",
        "sub_category": "Conditionals",
        "question": (
            "a = 0, b = 5;\nif (a && b / a > 1)\n  print(\"X\")\nelse\n  print(\"Y\")"
        ),
        "options": ["Y", "X", "crash", "depends on language"],
        "correct_answer": "Y",
        "explanation": "&& short-circuits: the left operand is false, so b/a never evaluates.",
    },
    {
        "id": "pc042",
        "sub_category": "Conditionals",
        "question": (
            'score = 72;\ngrade = score >= 90 ? "A" : score >= 75 ? "B" : "C";\nprint(grade);'
        ),
        "options": ["C", "B", "A", "error"],
        "correct_answer": "C",
        "explanation": "Right-associative ternary: 72 fails >=90 and >=75, landing on C.",
    },

    # ---------- Strings & Arrays ----------
    {
        "id": "pc050",
        "sub_category": "Strings",
        "question": 's = "placement";\nprint(s[2] + s[-3]);',
        "options": ["ae", "an", "am", "at"],
        "correct_answer": "ae",
        "explanation": (
            '"placement": indexes 0..8 are p,l,a,c,e,m,e,n,t. '
            "s[2]='a', s[-3] = third from end = s[6]='e'. Concatenated: \"ae\"."
        ),
    },
    {
        "id": "pc051",
        "sub_category": "Strings",
        "question": (
            's = "dryrun";\nc = 0;\nfor ch in s:\n  if ch in "aeiou":\n    c++\nprint(c);'
        ),
        "options": ["1", "2", "3", "0"],
        "correct_answer": "1",
        "explanation": 'Only \'u\' in "dryrun" is a vowel.',
    },
    {
        "id": "pc052",
        "sub_category": "Arrays",
        "question": (
            "// 0-based indexing\narr = [4, 1, 3, 2];\narr[1] = arr[arr[2]];\nprint(arr[0] + arr[1] + arr[2] + arr[3]);"
        ),
        "options": ["11", "10", "9", "12"],
        "correct_answer": "11",
        "explanation": "arr[2]=3, so arr[1] becomes arr[3]=2. Array is [4,2,3,2], sum 11.",
    },
    {
        "id": "pc053",
        "sub_category": "Arrays",
        "question": (
            "a = [2, 4, 6, 8];\nb = a[1:];\nprint(len(b) + b[0]);"
        ),
        "options": ["7", "9", "6", "8"],
        "correct_answer": "7",
        "explanation": "Slice from index 1: b = [4,6,8]. len(b)=3, b[0]=4, total 7.",
    },
    {
        "id": "pc054",
        "sub_category": "Arrays",
        "question": (
            "v = [5, 2, 9, 1];\nm = v[0];\nfor x in v:\n  if x > m:\n    m = x\nprint(m);"
        ),
        "options": ["9", "5", "17", "1"],
        "correct_answer": "9",
        "explanation": "Classic max-scan: m updates to 9.",
    },
    {
        "id": "pc055",
        "sub_category": "Mixed",
        "question": (
            "a = [1, 2, 3, 4, 5];\ns = 0;\nfor i in range(len(a)):\n  if i % 2 == 0:\n    s += a[i]\nprint(s);"
        ),
        "options": ["9", "15", "6", "12"],
        "correct_answer": "9",
        "explanation": "Even indices 0, 2, 4 -> values 1 + 3 + 5 = 9.",
    },
    {
        "id": "pc056",
        "sub_category": "Mixed",
        "question": (
            "def twist(x):\n  return (x << 1) - (x >> 1)\n\nprint(twist(5));"
        ),
        "options": ["8", "9", "7", "10"],
        "correct_answer": "8",
        "explanation": "(5<<1)=10, (5>>1)=2, so 10 - 2 = 8.",
    },
    {
        "id": "pc057",
        "sub_category": "Mixed",
        "question": (
            "n = 5;\nf = 1;\nfor (i = 1; i <= n; i++) {\n  f = f * i;\n  if (f > 20) break;\n}\nprint(f);"
        ),
        "options": ["24", "120", "6", "20"],
        "correct_answer": "24",
        "explanation": "f grows 1, 2, 6, 24 -> break fires at 24, printing 24.",
    },
]


def get_pseudocode_questions():
    """All bank questions (with answers) — server-side use only."""
    return PSEUDOCODE_QUESTIONS
