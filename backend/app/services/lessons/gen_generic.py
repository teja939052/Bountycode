"""Generic generator to add lessons to any track file."""
import os
import sys

lessons_dir = "D:/Project-Fremen/backend/app/services/lessons"
target_file = os.path.join(lessons_dir, sys.argv[1])
track_name = os.path.splitext(sys.argv[1])[0]

with open(target_file, "r") as f:
    content = f.read()

current_count = content.count('"id":')
target_total = current_count * 3
needed = target_total - current_count
print(f"{track_name}: {current_count} -> {target_total}, adding {needed} lessons")

topics = {
    "aptitude": ["percentages", "profit_loss", "ratios", "time_work", "time_speed_distance", "averages", "probability", "simple_interest", "compound_interest", "number_systems", "permutations_combinations", "data_interpretation"],
    "company_prep": ["tcs_prep", "infosys_prep", "wipro_prep", "company_coding", "common_questions", "mock_interview", "behavioral_questions", "resume_tips", "interview_etiquette", "final_checklist"],
    "cpp": ["basics", "control_flow", "functions", "arrays", "pointers", "oop", "inheritance", "polymorphism", "templates", "stl", "file_io", "memory"],
    "dsa": ["arrays", "strings", "linked_lists", "stacks", "queues", "binary_search_tree", "graphs", "hashing", "recursion", "dynamic_programming"],
    "java": ["basics", "control_flow", "oop", "inheritance", "polymorphism", "interfaces", "exception_handling", "collections", "strings", "exception_handling_advanced", "streams", "multithreading", "file_io"],
    "logical": ["series_completion", "analogy", "syllogism", "coding_decoding", "blood_relations", "direction", "seating_arrangement", "puzzle", "logical_reasoning", "critical_reasoning"],
    "networks": ["basics", "osi_model", "tcp_ip", "protocols", "ip_addressing", "routing", "security", "socket", "wireless", "cloud", "cdn"],
    "oop": ["basics", "classes_objects", "inheritance", "polymorphism", "encapsulation", "abstraction", "design_patterns", "solid_principles", "uml", "refactoring"],
    "os": ["intro", "process", "deadlock", "memory", "scheduling", "file_systems", "deadlock_prevention", "file_systems_advanced", "virtual_memory", "disk_scheduling", "file_allocation", "security"],
    "verbal": ["synonyms", "antonyms", "sentence_correction", "reading_comprehension", "sentence_arrangement", "error_spotting", "fill_in_blanks", "cloze_test", "para_jumbles", "reading_passage", "inference", "assumption", "conclusion", "argument", "critical_reasoning"],
}

topics_list = topics.get(track_name, ["concept_1", "concept_2", "concept_3", "concept_4", "concept_5", "concept_6", "concept_7", "concept_8", "concept_9", "concept_10"])

category_idx = 0
topic_idx = 0
new_lessons = []

for i in range(needed):
    topics_list_inner = topics_list
    topic = topics_list_inner[topic_idx % len(topics_list_inner)]
    lesson_id = f"{track_name}-{topic}-{i+1}"

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
        prerequisites = [f"{track_name}-{topic}-{prev_idx}"]

    steps = [
        {
            "id": f"{lesson_id}-s1",
            "type": "explain",
            "title": f"Understanding {topic.title()}",
            "content": f"In this lesson, you'll learn about {topic} in {track_name}.",
            "code": f"# Example of {topic}\n# Example code here",
            "output": "// Example output",
            "explanation": f"This explains how {topic} works in {track_name}."
        },
        {
            "id": f"{lesson_id}-s2",
            "type": "exercise",
            "title": f"Practice {topic.title()}",
            "instruction": f"Write code that demonstrates {topic}.",
            "starterCode": "# Write your code here\n",
            "solution": f"# Solution for {topic}\n# Example implementation",
            "tests": [{"input": None, "expected": None, "check": "student_attempted"}],
            "explanation": f"Here's how to implement {topic}.",
            "hints": ["Start with basics", "Test your code", "Check edge cases"]
        },
        {
            "id": f"{lesson_id}-s3",
            "type": "quiz",
            "title": f"{topic.title()} Quiz",
            "question": f"What is the primary purpose of {topic} in {track_name}?",
            "options": ["To store data", "To process data", "To organize code", "All of the above"],
            "correctIndex": 3,
            "explanation": f"{topic} serves multiple purposes in {track_name} programming."
        }
    ]

    lesson = {
        "id": lesson_id,
        "title": f"{topic.title()} - Lesson {i+1}",
        "track": track_name,
        "description": f"Learn about {topic} in {track_name} with hands-on examples.",
        "difficulty": difficulty,
        "prerequisites": prerequisites,
        "xpReward": xp,
        "steps": steps
    }
    new_lessons.append(lesson)

    topic_idx += 1
    if topic_idx >= len(topics_list_inner):
        topic_idx = 0
        category_idx += 1
        if category_idx >= len(topics):
            category_idx = 0

variable_name = f"{track_name.upper()}_LESSONS"
py_code = f"\n# --- Auto-generated additional lessons ({needed} lessons) ---\nEXTRA_{track_name.upper()}_LESSONS = [\n"
for i, lesson in enumerate(new_lessons):
    py_code += f"    {repr(lesson)}"
    if i < len(new_lessons) - 1:
        py_code += ",\n"
    else:
        py_code += "\n"
py_code += f"]\n{variable_name}.extend(EXTRA_{track_name.upper()}_LESSONS)\n"

print(f"Generated {len(new_lessons)} new {track_name} lessons")

with open(target_file, "a") as f:
    f.write(py_code)

print(f"Appended {len(new_lessons)} lessons to {target_file}")
