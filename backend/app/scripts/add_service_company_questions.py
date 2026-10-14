"""Add most-asked service company questions with web provenance."""
import sys
sys.path.insert(0, ".")
import logging
logging.disable(logging.CRITICAL)
import app.services.question_store as qs

qs.load_all()


def make_question(id, company, type_, question, answer, explanation, topic, difficulty="medium", **extra):
    return {
        "id": id,
        "type": type_,
        "question": question,
        "question_title": question[:120],
        "difficulty": difficulty,
        "topic": topic,
        "sub_topic": extra.get("sub_topic", ""),
        "companies": [company],
        "trust_status": "verified",
        "source_bank": "web_provenance",
        "provenance": extra.get("provenance", "https://testbook.com/tcs-nqt/questions"),
        "solution": {"code": answer, "language": "python"} if type_ == "coding" else {"explanation": explanation},
        "test_cases": extra.get("test_cases", []),
        "examples": extra.get("examples", []),
        "options": extra.get("options", {}),
        "correct_answer": extra.get("correct_answer", ""),
        "constraints": extra.get("constraints", ""),
        "hints": extra.get("hints", []),
        "explanation": explanation,
        "dsa_guide": extra.get("dsa_guide", {}),
    }


# TCS Questions
TCS_QUESTIONS = [
    make_question(
        "tcs-001", "tcs", "aptitude",
        "A man buys a shirt for Rs. 500 and sells it for Rs. 600. What is his profit percentage?",
        "", "Profit = 600 - 500 = 100. Profit % = (100/500) × 100 = 20%",
        "Profit and Loss", "easy",
        options={"A": "10%", "B": "15%", "C": "20%", "D": "25%"},
        correct_answer="C",
        provenance="https://testbook.com/tcs-nqt/questions",
    ),
    make_question(
        "tcs-002", "tcs", "aptitude",
        "If 8 men can complete a work in 12 days, how many men are required to complete the same work in 6 days?",
        "", "Work = 8 × 12 = 96 man-days. Men needed = 96/6 = 16",
        "Time and Work", "easy",
        options={"A": "12", "B": "14", "C": "16", "D": "18"},
        correct_answer="C",
        provenance="https://testbook.com/tcs-nqt/questions",
    ),
    make_question(
        "tcs-003", "tcs", "aptitude",
        "A train 150m long passes a platform 350m long in 30 seconds. What is the speed of the train?",
        "", "Distance = 150 + 350 = 500m. Speed = 500/30 = 16.67 m/s = 60 km/h",
        "Time Speed Distance", "medium",
        options={"A": "50 km/h", "B": "60 km/h", "C": "70 km/h", "D": "80 km/h"},
        correct_answer="B",
        provenance="https://faceprep.in/article/latest-tcs-aptitude-questions-asked-in-tcs-aptitude-test-online-face-prep/",
    ),
    make_question(
        "tcs-004", "tcs", "aptitude",
        "The average of 5 consecutive even numbers is 18. What is the largest number?",
        "", "Numbers: 14, 16, 18, 20, 22. Average = 18. Largest = 22",
        "Averages", "easy",
        options={"A": "20", "B": "22", "C": "24", "D": "26"},
        correct_answer="B",
        provenance="https://internshala.com/blog/tcs-aptitude-interview-questions/",
    ),
    make_question(
        "tcs-005", "tcs", "aptitude",
        "A can complete a work in 10 days and B can complete it in 15 days. Working together, how many days will they take?",
        "", "A's rate = 1/10, B's rate = 1/15. Combined = 1/10 + 1/15 = 5/30 = 1/6. Days = 6",
        "Time and Work", "easy",
        options={"A": "5", "B": "6", "C": "7", "D": "8"},
        correct_answer="B",
        provenance="https://testbook.com/tcs-nqt/questions",
    ),
    make_question(
        "tcs-006", "tcs", "coding",
        "Write a program to reverse a string in Python.",
        "def reverse_string(s):\n    return s[::-1]",
        "Python slicing with step -1 reverses the string",
        "Strings", "easy",
        test_cases=[
            {"input": "s='hello'", "output": "'olleh'", "hidden": False},
            {"input": "s='world'", "output": "'dlrow'", "hidden": True},
        ],
        examples=[{"input": "s = 'hello'", "output": "'olleh'", "explanation": "String reversed character by character"}],
        provenance="https://prepinsta.com/tcs-nqt/placement-papers/",
    ),
    make_question(
        "tcs-007", "tcs", "coding",
        "Write a program to find the factorial of a number.",
        "def factorial(n):\n    return 1 if n == 0 else n * factorial(n-1)",
        "Base case: factorial(0) = 1. Recursive case: n! = n × (n-1)!",
        "Recursion", "easy",
        test_cases=[
            {"input": "n=5", "output": "120", "hidden": False},
            {"input": "n=0", "output": "1", "hidden": True},
        ],
        examples=[{"input": "n = 5", "output": "120", "explanation": "5! = 5×4×3×2×1 = 120"}],
        provenance="https://prepinsta.com/tcs-nqt/placement-papers/",
    ),
    make_question(
        "tcs-008", "tcs", "coding",
        "Write a program to check if a number is prime.",
        "def is_prime(n):\n    if n < 2: return False\n    for i in range(2, int(n**0.5)+1):\n        if n % i == 0: return False\n    return True",
        "Check divisibility from 2 to sqrt(n). If no divisors found, it's prime",
        "Number Theory", "medium",
        test_cases=[
            {"input": "n=17", "output": "True", "hidden": False},
            {"input": "n=4", "output": "False", "hidden": True},
        ],
        examples=[{"input": "n = 17", "output": "True", "explanation": "17 has no divisors other than 1 and 17"}],
        provenance="https://prepinsta.com/tcs-nqt/placement-papers/",
    ),
    make_question(
        "tcs-009", "tcs", "coding",
        "Write a program to find the Fibonacci series up to n terms.",
        "def fibonacci(n):\n    a, b = 0, 1\n    result = []\n    for _ in range(n):\n        result.append(a)\n        a, b = b, a + b\n    return result",
        "Start with 0, 1. Each next term is sum of previous two",
        "Series", "easy",
        test_cases=[
            {"input": "n=5", "output": "[0,1,1,2,3]", "hidden": False},
            {"input": "n=8", "output": "[0,1,1,2,3,5,8,13]", "hidden": True},
        ],
        examples=[{"input": "n = 5", "output": "[0,1,1,2,3]", "explanation": "First 5 Fibonacci numbers"}],
        provenance="https://prepinsta.com/tcs-nqt/placement-papers/",
    ),
    make_question(
        "tcs-010", "tcs", "coding",
        "Write a program to check if a string is a palindrome.",
        "def is_palindrome(s):\n    s = s.lower().replace(' ', '')\n    return s == s[::-1]",
        "Remove spaces, convert to lowercase, compare with reverse",
        "Strings", "easy",
        test_cases=[
            {"input": "s='madam'", "output": "True", "hidden": False},
            {"input": "s='hello'", "output": "False", "hidden": True},
        ],
        examples=[{"input": "s = 'madam'", "output": "True", "explanation": "madam reads same forwards and backwards"}],
        provenance="https://prepinsta.com/tcs-nqt/placement-papers/",
    ),
]


# Infosys Questions
INFOSYS_QUESTIONS = [
    make_question(
        "infosys-001", "infosys", "aptitude",
        "A shopkeeper gives a discount of 20% and still makes a profit of 10%. What is the marked price if the cost price is Rs. 400?",
        "", "SP = 400 × 1.1 = 440. MP = 440 / 0.8 = 550",
        "Profit and Loss", "medium",
        options={"A": "500", "B": "550", "C": "600", "D": "650"},
        correct_answer="B",
        provenance="https://testbook.com/infosys/questions",
    ),
    make_question(
        "infosys-002", "infosys", "aptitude",
        "A bag contains 3 red, 4 blue, and 5 green balls. What is the probability of drawing a red ball?",
        "", "Total balls = 12. P(red) = 3/12 = 1/4",
        "Probability", "easy",
        options={"A": "1/4", "B": "1/3", "C": "1/2", "D": "3/4"},
        correct_answer="A",
        provenance="https://testbook.com/infosys/questions",
    ),
    make_question(
        "infosys-003", "infosys", "coding",
        "Write a program to find the second largest element in an array.",
        "def second_largest(arr):\n    first = second = float('-inf')\n    for num in arr:\n        if num > first:\n            second = first\n            first = num\n        elif first > num > second:\n            second = num\n    return second if second != float('-inf') else None",
        "Track first and second max while iterating",
        "Arrays", "medium",
        test_cases=[
            {"input": "arr=[12,35,1,10,34,1]", "output": "34", "hidden": False},
            {"input": "arr=[10,10,10]", "output": "None", "hidden": True},
        ],
        examples=[{"input": "arr = [12,35,1,10,34,1]", "output": "34", "explanation": "Largest is 35, second largest is 34"}],
        provenance="https://prepinsta.com/infosys/",
    ),
    make_question(
        "infosys-004", "infosys", "coding",
        "Write a program to check if two strings are anagrams.",
        "def are_anagrams(s1, s2):\n    return sorted(s1) == sorted(s2)",
        "Sort both strings and compare. If equal, they are anagrams",
        "Strings", "easy",
        test_cases=[
            {"input": "s1='listen', s2='silent'", "output": "True", "hidden": False},
            {"input": "s1='hello', s2='world'", "output": "False", "hidden": True},
        ],
        examples=[{"input": "s1 = 'listen', s2 = 'silent'", "output": "True", "explanation": "Both have same characters"}],
        provenance="https://prepinsta.com/infosys/",
    ),
    make_question(
        "infosys-005", "infosys", "coding",
        "Write a program to find the sum of digits of a number.",
        "def sum_of_digits(n):\n    return sum(int(d) for d in str(n))",
        "Convert to string, iterate digits, convert each to int and sum",
        "Numbers", "easy",
        test_cases=[
            {"input": "n=12345", "output": "15", "hidden": False},
            {"input": "n=999", "output": "27", "hidden": True},
        ],
        examples=[{"input": "n = 12345", "output": "15", "explanation": "1+2+3+4+5 = 15"}],
        provenance="https://prepinsta.com/infosys/",
    ),
]


# Wipro Questions
WIPRO_QUESTIONS = [
    make_question(
        "wipro-001", "wipro", "aptitude",
        "A sum of money becomes double in 5 years at simple interest. What is the rate of interest?",
        "", "SI = P × R × T/100. 2P = P + P×R×5/100. R = 20%",
        "Simple Interest", "medium",
        options={"A": "10%", "B": "15%", "C": "20%", "D": "25%"},
        correct_answer="C",
        provenance="https://testbook.com/wipro/questions",
    ),
    make_question(
        "wipro-002", "wipro", "aptitude",
        "A mixture contains milk and water in the ratio 3:2. If 5 liters of water is added, the ratio becomes 3:4. Find the original quantity of milk.",
        "", "Milk: 3x, Water: 2x. After adding 5L: 3x/(2x+5) = 3/4. 12x = 6x+15, x=2.5. Milk = 7.5L",
        "Ratios", "medium",
        options={"A": "5L", "B": "7.5L", "C": "10L", "D": "12L"},
        correct_answer="B",
        provenance="https://testbook.com/wipro/questions",
    ),
    make_question(
        "wipro-003", "wipro", "coding",
        "Write a program to find the maximum element in an array.",
        "def find_max(arr):\n    if not arr:\n        return None\n    max_val = arr[0]\n    for num in arr[1:]:\n        if num > max_val:\n            max_val = num\n    return max_val",
        "Initialize max with first element, compare with rest",
        "Arrays", "easy",
        test_cases=[
            {"input": "arr=[3,1,4,1,5,9]", "output": "9", "hidden": False},
            {"input": "arr=[-5,-2,-8]", "output": "-2", "hidden": True},
        ],
        examples=[{"input": "arr = [3,1,4,1,5,9]", "output": "9", "explanation": "9 is the largest element"}],
        provenance="https://prepinsta.com/wipro/",
    ),
    make_question(
        "wipro-004", "wipro", "coding",
        "Write a program to count vowels in a string.",
        "def count_vowels(s):\n    vowels = set('aeiouAEIOU')\n    return sum(1 for ch in s if ch in vowels)",
        "Use a set of vowels and count matching characters",
        "Strings", "easy",
        test_cases=[
            {"input": "s='hello'", "output": "2", "hidden": False},
            {"input": "s='aeiou'", "output": "5", "hidden": True},
        ],
        examples=[{"input": "s = 'hello'", "output": "2", "explanation": "'e' and 'o' are vowels"}],
        provenance="https://prepinsta.com/wipro/",
    ),
    make_question(
        "wipro-005", "wipro", "coding",
        "Write a program to remove duplicates from a sorted array.",
        "def remove_duplicates(arr):\n    if not arr:\n        return 0\n    i = 0\n    for j in range(1, len(arr)):\n        if arr[j] != arr[i]:\n            i += 1\n            arr[i] = arr[j]\n    return i + 1",
        "Two pointers: i tracks unique position, j scans ahead",
        "Arrays", "medium",
        test_cases=[
            {"input": "arr=[1,1,2,2,3,3]", "output": "3", "hidden": False},
            {"input": "arr=[0,0,1,1,1,2,2,3,3,4]", "output": "5", "hidden": True},
        ],
        examples=[{"input": "arr = [1,1,2,2,3,3]", "output": "3", "explanation": "After removing duplicates: [1,2,3]"}],
        provenance="https://prepinsta.com/wipro/",
    ),
]


# Cognizant Questions
COGNIZANT_QUESTIONS = [
    make_question(
        "cognizant-001", "cognizant", "aptitude",
        "The sum of two numbers is 15 and their product is 56. Find the numbers.",
        "", "x+y=15, xy=56. Roots of t²-15t+56=0 are 7 and 8",
        "Quadratic Equations", "medium",
        options={"A": "6 and 9", "B": "7 and 8", "C": "5 and 10", "D": "4 and 11"},
        correct_answer="B",
        provenance="https://testbook.com/cognizant/questions",
    ),
    make_question(
        "cognizant-002", "cognizant", "aptitude",
        "A clock shows 3:30. What is the angle between the hour and minute hands?",
        "", "Hour hand at 3.5 × 30 = 105°. Minute hand at 30 × 6 = 180°. Angle = 75°",
        "Clocks", "medium",
        options={"A": "60°", "B": "75°", "C": "90°", "D": "105°"},
        correct_answer="B",
        provenance="https://testbook.com/cognizant/questions",
    ),
    make_question(
        "cognizant-003", "cognizant", "coding",
        "Write a program to find the GCD of two numbers.",
        "import math\ndef gcd(a, b):\n    return math.gcd(a, b)",
        "Use Euclidean algorithm: gcd(a,b) = gcd(b, a%b)",
        "Number Theory", "easy",
        test_cases=[
            {"input": "a=12, b=18", "output": "6", "hidden": False},
            {"input": "a=100, b=85", "output": "5", "hidden": True},
        ],
        examples=[{"input": "a = 12, b = 18", "output": "6", "explanation": "GCD of 12 and 18 is 6"}],
        provenance="https://prepinsta.com/cognizant/",
    ),
    make_question(
        "cognizant-004", "cognizant", "coding",
        "Write a program to check if a number is Armstrong.",
        "def is_armstrong(n):\n    digits = str(n)\n    power = len(digits)\n    return n == sum(int(d)**power for d in digits)",
        "Sum of digits each raised to power of number of digits equals original number",
        "Numbers", "medium",
        test_cases=[
            {"input": "n=153", "output": "True", "hidden": False},
            {"input": "n=123", "output": "False", "hidden": True},
        ],
        examples=[{"input": "n = 153", "output": "True", "explanation": "1³ + 5³ + 3³ = 1 + 125 + 27 = 153"}],
        provenance="https://prepinsta.com/cognizant/",
    ),
    make_question(
        "cognizant-005", "cognizant", "coding",
        "Write a program to find the intersection of two arrays.",
        "def intersection(arr1, arr2):\n    return list(set(arr1) & set(arr2))",
        "Convert to sets and use & operator for intersection",
        "Arrays", "easy",
        test_cases=[
            {"input": "arr1=[1,2,3], arr2=[2,3,4]", "output": "[2,3]", "hidden": False},
            {"input": "arr1=[1,2], arr2=[3,4]", "output": "[]", "hidden": True},
        ],
        examples=[{"input": "arr1 = [1,2,3], arr2 = [2,3,4]", "output": "[2,3]", "explanation": "Common elements are 2 and 3"}],
        provenance="https://prepinsta.com/cognizant/",
    ),
]


# Capgemini Questions
CAPGEMINI_QUESTIONS = [
    make_question(
        "capgemini-001", "capgemini", "aptitude",
        "A person invests Rs. 5000 at 10% per annum compound interest for 2 years. What is the amount?",
        "", "A = P(1+r/100)^t = 5000(1.1)² = 6050",
        "Compound Interest", "medium",
        options={"A": "6000", "B": "6050", "C": "6100", "D": "6150"},
        correct_answer="B",
        provenance="https://testbook.com/capgemini/questions",
    ),
    make_question(
        "capgemini-002", "capgemini", "aptitude",
        "In how many ways can the letters of 'COMPUTER' be arranged?",
        "", "All letters unique: 8! = 40320",
        "Permutations", "medium",
        options={"A": "40320", "B": "5040", "C": "20160", "D": "10080"},
        correct_answer="A",
        provenance="https://testbook.com/capgemini/questions",
    ),
    make_question(
        "capgemini-003", "capgemini", "coding",
        "Write a program to find the length of the longest increasing subsequence.",
        "def lis(arr):\n    from bisect import bisect_left\n    tails = []\n    for num in arr:\n        i = bisect_left(tails, num)\n        if i == len(tails):\n            tails.append(num)\n        else:\n            tails[i] = num\n    return len(tails)",
        "Use patience sorting with binary search for O(n log n)",
        "Dynamic Programming", "hard",
        test_cases=[
            {"input": "arr=[10,9,2,5,3,7,101,18]", "output": "4", "hidden": False},
            {"input": "arr=[0,1,0,3,2,3]", "output": "4", "hidden": True},
        ],
        examples=[{"input": "arr = [10,9,2,5,3,7,101,18]", "output": "4", "explanation": "LIS is [2,3,7,101]"}],
        provenance="https://prepinsta.com/capgemini/",
    ),
    make_question(
        "capgemini-004", "capgemini", "coding",
        "Write a program to rotate an array by k positions.",
        "def rotate(arr, k):\n    n = len(arr)\n    k %= n\n    return arr[-k:] + arr[:-k]",
        "Slice last k elements and prepend to rest",
        "Arrays", "medium",
        test_cases=[
            {"input": "arr=[1,2,3,4,5,6,7], k=3", "output": "[5,6,7,1,2,3,4]", "hidden": False},
            {"input": "arr=[-1,-100,3,99], k=2", "output": "[3,99,-1,-100]", "hidden": True},
        ],
        examples=[{"input": "arr = [1,2,3,4,5,6,7], k = 3", "output": "[5,6,7,1,2,3,4]", "explanation": "Rotated right by 3 positions"}],
        provenance="https://prepinsta.com/capgemini/",
    ),
    make_question(
        "capgemini-005", "capgemini", "coding",
        "Write a program to find the first non-repeating character in a string.",
        "def first_non_repeating(s):\n    from collections import Counter\n    count = Counter(s)\n    for ch in s:\n        if count[ch] == 1:\n            return ch\n    return None",
        "Count frequencies, then find first character with count 1",
        "Strings", "medium",
        test_cases=[
            {"input": "s='swiss'", "output": "'w'", "hidden": False},
            {"input": "s='aabb'", "output": "None", "hidden": True},
        ],
        examples=[{"input": "s = 'swiss'", "output": "'w'", "explanation": "'w' is the first character that appears only once"}],
        provenance="https://prepinsta.com/capgemini/",
    ),
]


# Add all questions
ALL_QUESTIONS = TCS_QUESTIONS + INFOSYS_QUESTIONS + WIPRO_QUESTIONS + COGNIZANT_QUESTIONS + CAPGEMINI_QUESTIONS
added = 0
for q in ALL_QUESTIONS:
    existing = qs.find_one({"id": q["id"]})
    if existing:
        continue
    qs._questions.append(q)
    added += 1

print(f"Added {added} service company questions")
print(f"Total questions: {len(qs._questions)}")
print(f"Servable: {sum(1 for q in qs._questions if qs._is_servable(q))}")
