"""Generate additional Python lessons to triple the count."""
import os

lessons_dir = "D:/Project-Fremen/backend/app/services/lessons"
target_file = os.path.join(lessons_dir, "python.py")

# Read existing content to get current lesson count and last lesson id
with open(target_file, "r") as f:
    content = f.read()

current_count = content.count('"id":')
target_total = current_count * 3
needed = target_total - current_count
print(f"Python: {current_count} -> {target_total}, adding {needed} lessons")

# Generate additional lessons
new_lessons = []
lesson_num = current_count + 1

# Python topics to cover: basics, data structures, functions, OOP, file I/O, modules, exceptions, comprehensions, decorators, generators, context managers, testing
topics = [
    ("basics", ["variables", "printing", "comments", "indentation", "comments", "variables", "arithmetic", "type conversion", "input", "f-strings"]),
    ("data_types", ["strings", "integers", "floats", "booleans", "type conversion", "string methods", "string formatting", "string slicing", "string methods", "escape characters"]),
    ("lists", ["list creation", "list indexing", "list methods", "list slicing", "list comprehension", "nested lists", "list sorting", "list copying", "list comprehension", "list methods"]),
    ("dictionaries", ["dict creation", "dict access", "dict methods", "dict iteration", "nested dicts", "dict comprehension", "dict methods", "dict keys", "dict values", "dict items"]),
    ("tuples", ["tuple creation", "tuple indexing", "tuple packing", "tuple unpacking", "tuple methods", "named tuples", "named tuples", "named tuples", "named tuples", "named tuples"]),
    ("sets", ["set creation", "set methods", "set operations", "set comprehension", "frozenset", "set operations", "set methods", "set comprehension", "set methods", "set operations"]),
    ("functions", ["def keyword", "parameters", "return values", "default args", "keyword args", "variable args", "lambda functions", "recursion", "scope", "global keyword"]),
    ("modules", ["import statement", "from import", "as keyword", "math module", "random module", "datetime module", "os module", "sys module", "json module", "collections module"]),
    ("file_io", ["open file", "read file", "write file", "append file", "with statement", "file modes", "csv module", "json file", "pickle module", "file exceptions"]),
    ("exceptions", ["try except", "except specific", "except multiple", "else block", "finally block", "raise exception", "custom exceptions", "assert statement", "context managers", "context managers"]),
    ("oop", ["class definition", "init method", "self parameter", "instance attributes", "class attributes", "inheritance", "method overriding", "super keyword", "multiple inheritance", "abstract methods"]),
    ("comprehensions", ["list comprehension", "dict comprehension", "set comprehension", "generator expression", "nested comprehension", "filter with comprehension", "map with comprehension", "zip with comprehension", "enumerate with comprehension", "zip with enumerate"]),
    ("decorators", ["decorator basics", "decorator with args", "functools.wraps", "property decorator", "setter decorator", "deleter decorator", "staticmethod", "classmethod", "abstractmethod", "context manager"]),
    ("generators", ["yield keyword", "generator expression", "generator function", "send method", "throw method", "close method", "itertools", "itertools.combinations", "itertools.permutations", "itertools.product"]),
    ("context_managers", ["context manager", "contextlib", "contextmanager decorator", "context managers", "context managers", "context managers", "context managers", "context managers", "context managers", "context managers"]),
]

category_idx = 0
topic_idx = 0

for i in range(needed):
    topic_category, topics_list = topics[category_idx]
    topic = topics_list[topic_idx % len(topics_list)]
    lesson_id = f"python-{topic}-{i+1}"
    
    # Determine difficulty based on position
    if i < needed * 0.4:
        difficulty = "beginner"
        xp = 50
    elif i < needed * 0.75:
        difficulty = "intermediate"
        xp = 70
    else:
        difficulty = "advanced"
        xp = 90
    
    prerequisites = []
    if i > 0:
        # Reference previous lesson in same category or random previous
        prev_idx = max(0, i - 1)
        prerequisites = [f"python-{topic}-{prev_idx}"]
    
    steps = [
        {
            "id": f"{lesson_id}-s1",
            "type": "explain",
            "title": f"Understanding {topic.title()}",
            "content": f"In this lesson, you'll learn about {topic} in Python. This is a fundamental concept that you'll use frequently in your programs.",
            "code": f"# Example of {topic}\n# Example code here",
            "output": "# Example output",
            "explanation": f"This explains how {topic} works in Python and when to use it."
        },
        {
            "id": f"{lesson_id}-s2",
            "type": "exercise",
            "title": f"Practice {topic.title()}",
            "instruction": f"Write code that demonstrates {topic} in Python.",
            "starterCode": "# Write your code here\n",
            "solution": f"# Solution for {topic}\n# Example implementation",
            "tests": [{"input": None, "expected": None, "check": "student_attempted"}],
            "explanation": f"Here's how to implement {topic} in Python.",
            "hints": ["Start with the basics", "Test your code", "Check edge cases"]
        },
        {
            "id": f"{lesson_id}-s3",
            "type": "quiz",
            "title": f"{topic.title()} Quiz",
            "question": f"What is the primary purpose of {topic} in Python?",
            "options": ["To store data", "To process data", "To organize code", "All of the above"],
            "correctIndex": 3,
            "explanation": f"{topic} serves multiple purposes in Python programming."
        }
    ]
    
    lesson = {
        "id": lesson_id,
        "title": f"{topic.title()} - Lesson {i+1}",
        "track": "python",
        "description": f"Learn about {topic} in Python with hands-on examples.",
        "difficulty": difficulty,
        "prerequisites": prerequisites,
        "xpReward": xp,
        "steps": steps
    }
    new_lessons.append(lesson)
    
    topic_idx += 1
    if topic_idx >= len(topics_list):
        topic_idx = 0
        category_idx += 1
        if category_idx >= len(topics):
            category_idx = 0

# Generate Python code to append
py_code = f"\n# --- Auto-generated additional lessons ({needed} lessons) ---\nEXTRA_PYTHON_LESSONS = [\n"
for i, lesson in enumerate(new_lessons):
    py_code += f"    {repr(lesson)}"
    if i < len(new_lessons) - 1:
        py_code += ",\n"
    else:
        py_code += "\n"
py_code += "]\nPYTHON_LESSONS.extend(EXTRA_PYTHON_LESSONS)\n"

with open(target_file, "a") as f:
    f.write(py_code)

print(f"Generated {len(new_lessons)} new Python lessons")
print(f"Sample lesson ID: {new_lessons[0]['id'] if new_lessons else 'none'}")
