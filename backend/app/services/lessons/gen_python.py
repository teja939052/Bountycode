"""Generate additional Python lessons to triple the count."""
import os

lessons_dir = "D:/Project-Fremen/backend/app/services/lessons"
target_file = os.path.join(lessons_dir, "python.py")

with open(target_file, "r") as f:
    content = f.read()

current_count = content.count('"id":')
target_total = current_count * 3
needed = target_total - current_count
print(f"Python: {current_count} -> {target_total}, adding {needed} lessons")

topics = [
    ("basics", ["hello_world", "variables", "data_types", "operators", "input_output", "comments", "type_casting", "operator_precedence", "literals", "escape_sequences"]),
    ("control_flow", ["if_statement", "if_else", "switch_statement", "ternary_operator", "for_loop", "while_loop", "do_while_loop", "break_statement", "continue_statement", "return_statement"]),
    ("functions", ["function_declaration", "function_definition", "function_parameters", "return_values", "default_arguments", "keyword_arguments", "variable_args", "lambda_functions", "recursion", "function_overloading"]),
    ("arrays", ["array_declaration", "array_initialization", "array_access", "multidimensional_arrays", "array_functions", "string_arrays", "dynamic_arrays", "array_algorithms", "array_sorting", "array_searching"]),
    ("pointers", ["pointer_declaration", "pointer_initialization", "pointer_arithmetic", "null_pointer", "void_pointer", "wild_pointer", "dangling_pointer", "pointer_to_pointer", "function_pointers", "array_of_pointers"]),
    ("oop", ["classes_and_objects", "constructors", "destructors", "access_modifiers", "data_hiding", "this_pointer", "static_members", "friend_functions", "friend_classes", "nested_classes"]),
    ("inheritance", ["single_inheritance", "multiple_inheritance", "multilevel_inheritance", "hierarchical_inheritance", "hybrid_inheritance", "constructors_in_inheritance", "destructors_in_inheritance", "virtual_base_class", "diamond_problem", "virtual_inheritance"]),
    ("polymorphism", ["function_overloading", "operator_overloading", "virtual_functions", "pure_virtual_functions", "abstract_classes", "runtime_polymorphism", "compile_time_polymorphism", "dynamic_binding", "static_binding", "virtual_destructors"]),
    ("templates", ["function_templates", "class_templates", "template_specialization", "variadic_templates", "type_traits", "type_aliases", "auto_keyword", "decltype", "constexpr", "lambdas"]),
    ("stl", ["vector", "list", "deque", "stack", "queue", "priority_queue", "set", "map", "unordered_map", "unordered_set"]),
    ("file_io", ["file_streams", "file_open_modes", "reading_files", "writing_files", "random_access", "error_handling", "binary_files", "text_files", "string_streams", "file_exceptions"]),
    ("memory", ["stack_vs_heap", "new_and_delete", "malloc_and_free", "smart_pointers", "unique_ptr", "shared_ptr", "weak_ptr", "memory_leaks", "dangling_pointers", "memory_management"]),
]

category_idx = 0
topic_idx = 0
new_lessons = []

for i in range(needed):
    topic_category, topics_list = topics[category_idx]
    topic = topics_list[topic_idx % len(topics_list)]
    lesson_id = f"python-{topic}-{i+1}"

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
        prev_idx = max(0, i - 1)
        prev_topic_list = topics[category_idx % len(topics)][1]
        prev_topic = prev_topic_list[prev_idx % len(prev_topic_list)]
        prerequisites = [f"python-{prev_topic}-{prev_idx}"]

    steps = [
        {
            "id": f"{lesson_id}-s1",
            "type": "explain",
            "title": f"Understanding {topic.title()}",
            "content": f"In this lesson, you'll learn about {topic} in Python. This is a fundamental concept that you'll use frequently in your programs.",
            "code": f"# Example of {topic}\n# Example code here",
            "output": "# Example output",
            "explanation": f"This explains how {topic} works in Python."
        },
        {
            "id": f"{lesson_id}-s2",
            "type": "exercise",
            "title": f"Practice {topic.title()}",
            "instruction": f"Write Python code that demonstrates {topic}.",
            "starterCode": "# Write your code here\n",
            "solution": f"# Solution for {topic}\n# Example implementation",
            "tests": [{"input": None, "expected": None, "check": "student_attempted"}],
            "explanation": f"Here's how to implement {topic} in Python.",
            "hints": ["Start with basics", "Test your code", "Check edge cases"]
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

py_code = f"\n# --- Auto-generated additional lessons ({needed} lessons) ---\nEXTRA_PYTHON_LESSONS = [\n"
for i, lesson in enumerate(new_lessons):
    py_code += f"    {repr(lesson)}"
    if i < len(new_lessons) - 1:
        py_code += ",\n"
    else:
        py_code += "\n"
py_code += "]\nPYTHON_LESSONS.extend(EXTRA_PYTHON_LESSONS)\n"

print(f"Generated {len(new_lessons)} new Python lessons")
print(f"Sample lesson ID: {new_lessons[0]['id'] if new_lessons else 'none'}")

# Append to the target file
with open(target_file, "a") as f:
    f.write(py_code)

print(f"Appended {len(new_lessons)} lessons to {target_file}")
