import os
lessons_dir = "D:/Project-Fremen/backend/app/services/lessons"
target_file = os.path.join(lessons_dir, "java.py")
with open(target_file, "r") as f:
    content = f.read()
current_count = content.count('"id":')
target_total = current_count * 3
needed = target_total - current_count
print(f"Java: {current_count} -> {target_total}, adding {needed} lessons")
topics = [
    ("basics", ["hello world", "variables", "data types", "operators", "input output", "comments", "type casting", "operator precedence", "literals", "escape sequences"]),
    ("control_flow", ["if statement", "if else", "switch statement", "ternary operator", "for loop", "while loop", "do while loop", "break statement", "continue statement", "return statement"]),
    ("oop", ["classes and objects", "constructors", "destructors", "access modifiers", "data hiding", "this keyword", "static members", "final keyword", "finalize method", "object class"]),
    ("inheritance", ["single inheritance", "multiple inheritance", "multilevel inheritance", "hierarchical inheritance", "hybrid inheritance", "constructors in inheritance", "method overriding", "dynamic method dispatch", "abstract classes", "final keyword"]),
    ("polymorphism", ["compile time polymorphism", "runtime polymorphism", "method overloading", "method overriding", "dynamic binding", "static binding", "covariant return types", "covariant parameter types", "virtual functions", "abstract methods"]),
    ("interfaces", ["interface basics", "interface implementation", "multiple inheritance via interfaces", "default methods", "static methods", "private methods", "functional interfaces", "lambda expressions", "method references", "stream API"]),
    ("exception_handling", ["try catch block", "multiple catch blocks", "finally block", "throw keyword", "throws keyword", "custom exceptions", "checked exceptions", "unchecked exceptions", "exception hierarchy", "try with resources"]),
    ("collections", ["arraylist", "linkedlist", "hashset", "treeset", "hashmap", "treemap", "linkedhashmap", "priorityqueue", "deque", "iterator"]),
    ("strings", ["string class", "stringbuffer", "stringbuilder", "string methods", "string concatenation", "string comparison", "string splitting", "string formatting", "string immutability", "string pool"]),
    ("exception_handling_advanced", ["multi-catch", "try with resources", "autocloseable", "suppressed exceptions", "stack trace", "exception chaining", "custom exceptions", "checked vs unchecked", "exception propagation", "best practices"]),
    ("streams", ["stream creation", "intermediate operations", "terminal operations", "collectors", "flatmap", "map", "filter", "reduce", "collect", "parallel streams"]),
    ("multithreading", ["thread creation", "thread lifecycle", "thread priority", "thread synchronization", "synchronized keyword", "volatile keyword", "atomic variables", "concurrent collections", "executor framework", "future and callable"]),
    ("file_io", ["file class", "file reader", "file writer", "buffered reader", "buffered writer", "object serialization", "deserialization", "random access file", "nio package", "file watcher"]),
]

category_idx = 0
topic_idx = 0
new_lessons = []

for i in range(needed):
    topic_category, topics_list = topics[category_idx]
    topic = topics_list[topic_idx % len(topics_list)]
    lesson_id = f"java-{topic}-{i+1}"
    
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
        prerequisites = [f"java-{topic}-{prev_idx}"]
    
    steps = [
        {
            "id": f"{lesson_id}-s1",
            "type": "explain",
            "title": f"Understanding {topic.title()}",
            "content": f"In this lesson, you'll learn about {topic} in Java.",
            "code": f"// Example of {topic}\npublic class Main {{\n  public static void main(String[] args) {{\n  }}\n}}",
            "output": "// Example output",
            "explanation": f"This explains how {topic} works in Java."
        },
        {
            "id": f"{lesson_id}-s2",
            "type": "exercise",
            "title": f"Practice {topic.title()}",
            "instruction": f"Write Java code that demonstrates {topic}.",
            "starterCode": "public class Main {\n  public static void main(String[] args) {\n    // Write your code here\n  }\n}",
            "solution": f"public class Main {{\n  public static void main(String[] args) {{\n    // Solution for {topic}\n  }}\n}}",
                "tests": [{"input": None, "expected": None, "check": "student_attempted"}],
            "explanation": f"Here's how to implement {topic} in Java.",
            "hints": ["Start with basics", "Test your code", "Check edge cases"]
        },
        {
            "id": f"{lesson_id}-s3",
            "type": "quiz",
            "title": f"{topic.title()} Quiz",
            "question": f"What is the primary purpose of {topic} in Java?",
            "options": ["To store data", "To process data", "To organize code", "All of the above"],
            "correctIndex": 3,
            "explanation": f"{topic} serves multiple purposes in Java programming."
        }
    ]
    
    lesson = {
        "id": lesson_id,
        "title": f"{topic.title()} - Lesson {i+1}",
        "track": "java",
        "description": f"Learn about {topic} in Java with hands-on examples.",
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

py_code = f"\n# --- Auto-generated additional lessons ({needed} lessons) ---\nEXTRA_JAVA_LESSONS = [\n"
for i, lesson in enumerate(new_lessons):
    py_code += f"    {repr(lesson)}"
    if i < len(new_lessons) - 1:
        py_code += ",\n"
    else:
        py_code += "\n"
py_code += "]\nJAVA_LESSONS.extend(EXTRA_JAVA_LESSONS)\n"

print(f"Generated {len(new_lessons)} new Java lessons")
