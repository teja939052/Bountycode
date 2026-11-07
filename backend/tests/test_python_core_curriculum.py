from app.data.lesson_content import get_lesson_content
from app.services.curriculum_quality import score_lesson_content


def test_python_conditionals_use_authored_lesson_content():
    lesson = get_lesson_content(
        "python",
        "python-l04-01",
        "if Statement",
        "theory",
    )

    assert "truthy" in lesson["theory"].lower()
    assert len(lesson["sections"]) == 3
    assert len(lesson["quizzes"]) == 3
    assert len(lesson["exercises"]) == 2
    assert "temperature" in lesson["code_example"]["code"]
    assert score_lesson_content(lesson)["status"] == "ready"


def test_python_loop_and_function_lessons_are_authored_not_generic_shells():
    cases = [
        ("python-l05-01", "for Loop with range()", "range(1, 6)"),
        ("python-l05-02", "while Loop", "attempts < 3"),
        ("python-l06-01", "def & return", "def calculate_total"),
    ]

    for lesson_id, title, expected_code in cases:
        lesson = get_lesson_content("python", lesson_id, title, "theory")
        assert expected_code in lesson["code_example"]["code"]
        assert len(lesson["quizzes"]) == 3
        assert len(lesson["exercises"]) == 2
        assert score_lesson_content(lesson)["status"] == "ready"



def test_python_decision_and_collection_lessons_use_authored_content():
    cases = [
        ("python-l04-04", "Nested Conditionals", "logged_in = True"),
        ("python-l04-05", "Ternary Expression", "status = 'Adult'"),
        ("python-l04-06", "Match-Case (3.10)", "match command:"),
        ("python-l05-03", "for...in with Lists", "for price in prices:"),
        ("python-l05-06", "List Comprehensions Deep", "squares_of_evens"),
    ]

    for lesson_id, title, expected_code in cases:
        lesson = get_lesson_content("python", lesson_id, title, "theory")
        assert expected_code in lesson["code_example"]["code"]
        assert len(lesson["quizzes"]) == 3
        assert len(lesson["exercises"]) == 2
        assert score_lesson_content(lesson)["status"] == "ready"



def test_python_lists_dictionaries_and_strings_use_authored_content():
    cases = [
        ("python-l07-01", "Lists Basics", "marks = [78, 91, 64]"),
        ("python-l07-02", "List Methods", "tasks.append('revise')"),
        ("python-l07-03", "Slicing", "values[::-1]"),
        ("python-l08-01", "String Methods Deep", "raw.strip().lower()"),
        ("python-l08-02", "f-strings & Formatting", "score:.2f"),
        ("python-l08-05", "dict Basics", "student.get('grade'"),
        ("python-l08-06", "dict Methods", "scores.items()"),
    ]

    for lesson_id, title, expected_code in cases:
        lesson = get_lesson_content("python", lesson_id, title, "theory")
        assert expected_code in lesson["code_example"]["code"]
        assert len(lesson["quizzes"]) == 3
        assert len(lesson["exercises"]) == 2
        assert score_lesson_content(lesson)["status"] == "ready"



def test_python_exception_and_oop_lessons_use_authored_content():
    cases = [
        ("python-l09-05", "try / except / finally", "except ValueError"),
        ("python-l09-06", "Custom Exceptions", "class InsufficientFundsError"),
        ("python-l10-01", "Classes & Objects", "class Student:"),
        ("python-l10-02", "__init__ & self", "def __init__(self, owner"),
        ("python-l10-05", "Inheritance", "class Dog(Animal):"),
        ("python-l10-08", "Polymorphism", "for animal in [Dog(), Cat()]"),
    ]

    for lesson_id, title, expected_code in cases:
        lesson = get_lesson_content("python", lesson_id, title, "theory")
        assert expected_code in lesson["code_example"]["code"]
        assert len(lesson["quizzes"]) == 3
        assert len(lesson["exercises"]) == 2
        assert score_lesson_content(lesson)["status"] == "ready"



def test_string_slicing_uses_the_specific_string_lesson_not_list_slicing():
    lesson = get_lesson_content(
        "python",
        "python-l08-03",
        "String Slicing",
        "theory",
    )

    assert "string slicing" in lesson["theory"].lower()
    assert "code = 'BOUNTYCODE'" in lesson["code_example"]["code"]
    assert "code[::2]" in lesson["code_example"]["code"]
    assert score_lesson_content(lesson)["status"] == "ready"



def test_python_functions_tuples_files_and_json_lessons_are_authored():
    cases = [
        ("python-l06-02", "Parameters & Arguments", "def calculate_total(price, quantity)"),
        ("python-l06-03", "Default Parameters", "greeting='Hello'"),
        ("python-l06-05", "Lambda Functions", "lambda student: student[1]"),
        ("python-l06-06", "Recursion", "return number * factorial(number - 1)"),
        ("python-l07-05", "Tuples", "single = (5,)"),
        ("python-l11-06", "Sets & Frozensets", "required & known"),
        ("python-l09-01", "Reading Files", "for line in file:"),
        ("python-l09-02", "Writing Files", "path.open('a'"),
        ("python-l09-03", "with Statement (Context Manager)", "with open("),
        ("python-l09-04", "CSV Files", "csv.DictReader(file)"),
        ("python-l08-08", "JSON Parsing", "json.loads(raw)"),
    ]

    for lesson_id, title, expected_code in cases:
        lesson = get_lesson_content("python", lesson_id, title, "theory")
        assert expected_code in lesson["code_example"]["code"], title
        assert len(lesson["quizzes"]) == 3, title
        assert len(lesson["exercises"]) == 2, title
        assert score_lesson_content(lesson)["status"] == "ready", title



def test_python_algorithms_regex_and_advanced_iteration_lessons_are_authored():
    cases = [
        ("python-l07-04", "Nested Lists", "grid[row][column]"),
        ("python-l07-07", "Sorting & Searching", "sorted(scores, reverse=True)"),
        ("python-l08-04", "Regular Expressions", "re.findall"),
        ("python-l09-07", "Raising Exceptions", "raise ValueError"),
        ("python-l11-01", "Generators & yield", "yield number"),
        ("python-l11-02", "Iterators", "iterator = iter(names)"),
        ("python-l11-03", "Decorators with Parameters", "@wraps(function)"),
    ]

    for lesson_id, title, expected_code in cases:
        lesson = get_lesson_content("python", lesson_id, title, "theory")
        assert expected_code in lesson["code_example"]["code"], title
        assert len(lesson["quizzes"]) == 3, title
        assert len(lesson["exercises"]) == 2, title
        assert score_lesson_content(lesson)["status"] == "ready", title



def test_python_beginner_setup_input_and_data_type_lessons_are_authored():
    cases = [
        ("python-l01-01", "What is Python?", "language = 'Python'"),
        ("python-l01-02", "Hello World in Python", "Hello, world!"),
        ("python-l01-03", "print() Function", "sep=' | '"),
        ("python-l01-04", "Comments in Python", "# Calculate the final price"),
        ("python-l01-06", "Indentation Matters", "if score >= 40:"),
        ("python-l02-01", "Numbers: int & float", "type(items).__name__"),
        ("python-l02-02", "Strings in Python", "name.lower()"),
        ("python-l02-07", "Input with input()", "int(input('Marks: '))"),
    ]

    for lesson_id, title, expected_code in cases:
        lesson = get_lesson_content("python", lesson_id, title, "theory")
        assert expected_code in lesson["code_example"]["code"], title
        assert len(lesson["quizzes"]) == 3, title
        assert len(lesson["exercises"]) == 2, title
        assert score_lesson_content(lesson)["status"] == "ready", title
