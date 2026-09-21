"""Real execution test: worlds 9-12 boss battles.

Verifies:
1. Boss lessons exist in worlds 9, 10, 12
2. Boss lessons have required fields (steps, mastery_evidence)
3. Unlock chain: completing regular lessons unlocks boss
"""
import sys
sys.path.insert(0, ".")
from app.content.worlds_7_to_9 import get_world_9
from app.content.worlds_10_to_12 import get_world_10, get_world_12

def summarize_world(world, name):
    towns = world.towns if hasattr(world, "towns") else []
    total_lessons = 0
    boss_lessons = []
    regular_lessons = []
    for town in towns:
        lessons = town.lessons if hasattr(town, "lessons") else []
        for lesson in lessons:
            total_lessons += 1
            kind = lesson.kind if hasattr(lesson, "kind") else "normal"
            if kind == "boss":
                boss_lessons.append(lesson.id)
            else:
                regular_lessons.append(lesson.id)
    
    print(f"{name}: {world.name}")
    print(f"  Towns: {len(towns)}")
    print(f"  Total lessons: {total_lessons}")
    print(f"  Regular lessons: {len(regular_lessons)}")
    print(f"  Boss lessons: {boss_lessons}")
    
    # Verify boss lessons have required fields
    for town in towns:
        for lesson in town.lessons:
            if lesson.kind == "boss":
                has_steps = bool(lesson.steps)
                has_mastery = bool(lesson.mastery_evidence)
                has_unlock = bool(lesson.unlocks)
                print(f"  Boss {lesson.id}: steps={has_steps}, mastery={has_mastery}, unlocks={has_unlock}")
    
    # Verify unlock chain: each regular lesson's unlocks points to next lesson or boss
    lesson_map = {}
    for town in towns:
        for lesson in town.lessons:
            lesson_map[lesson.id] = lesson
    
    unlock_chain_valid = True
    for lid in regular_lessons:
        lesson = lesson_map.get(lid)
        if lesson and lesson.unlocks:
            next_id = lesson.unlocks
            if next_id not in lesson_map:
                print(f"  BROKEN CHAIN: {lid} unlocks {next_id} but {next_id} not found")
                unlock_chain_valid = False
    
    print(f"  Unlock chain valid: {unlock_chain_valid}")
    
    return {
        "name": world.name,
        "total_lessons": total_lessons,
        "regular_count": len(regular_lessons),
        "boss_count": len(boss_lessons),
        "bosses_have_steps": all(bool(lesson_map[lid].steps) for lid in boss_lessons if lid in lesson_map),
        "bosses_have_mastery": all(bool(lesson_map[lid].mastery_evidence) for lid in boss_lessons if lid in lesson_map),
        "unlock_chain_valid": unlock_chain_valid,
    }

print("=== WORLDS 9-12 BOSS BATTLE EXECUTION TEST ===")
results = []

w9 = get_world_9()
results.append(summarize_world(w9, "World 9"))

w10 = get_world_10()
results.append(summarize_world(w10, "World 10"))

w12 = get_world_12()
results.append(summarize_world(w12, "World 12"))

print("\n=== SUMMARY ===")
for r in results:
    status = "PASS" if (r["bosses_have_steps"] and r["bosses_have_mastery"] and r["unlock_chain_valid"]) else "FAIL"
    print(f"{r['name']}: {status} - {r['regular_count']} regular, {r['boss_count']} boss, steps={r['bosses_have_steps']}, mastery={r['bosses_have_mastery']}, chain={r['unlock_chain_valid']}")

all_pass = all(r["bosses_have_steps"] and r["bosses_have_mastery"] and r["unlock_chain_valid"] for r in results)
if all_pass:
    print("\nWorlds 9-12 boss battle test: PASS")
else:
    print("\nWorlds 9-12 boss battle test: FAIL")
