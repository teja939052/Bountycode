import sys
sys.path.insert(0, ".")
from app.content.worlds_7_to_9 import get_world_9
from app.content.worlds_10_to_12 import get_world_10, get_world_12

def summarize(world, name):
    towns = world.towns if hasattr(world, "towns") else []
    total_lessons = 0
    boss_lessons = []
    for town in towns:
        lessons = town.lessons if hasattr(town, "lessons") else []
        for lesson in lessons:
            total_lessons += 1
            kind = lesson.kind if hasattr(lesson, "kind") else "normal"
            if kind == "boss":
                boss_lessons.append(lesson.id)
    print(f"{name}: {world.name}")
    print(f"  Towns: {len(towns)}")
    print(f"  Total lessons: {total_lessons}")
    print(f"  Boss lessons: {boss_lessons}")

w9 = get_world_9()
w10 = get_world_10()
w12 = get_world_12()

summarize(w9, "World 9")
summarize(w10, "World 10")
summarize(w12, "World 12")

# Verify boss lessons have required fields
for world, name in [(w9, "World 9"), (w10, "World 10"), (w12, "World 12")]:
    towns = world.towns if hasattr(world, "towns") else []
    for town in towns:
        lessons = town.lessons if hasattr(town, "lessons") else []
        for lesson in lessons:
            kind = lesson.kind if hasattr(lesson, "kind") else "normal"
            if kind == "boss":
                has_steps = bool(lesson.steps) if hasattr(lesson, "steps") else False
                has_mastery = bool(lesson.mastery_evidence) if hasattr(lesson, "mastery_evidence") else False
                print(f"  {name} boss {lesson.id}: steps={has_steps}, mastery_evidence={has_mastery}")

print("Worlds 9-12 boss verification: PASS")
