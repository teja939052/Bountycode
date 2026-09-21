"""Real execution test: judge submission + boss trigger for worlds 9, 11, 12."""
import sys
sys.path.insert(0, ".")
from app.content.worlds_7_to_9 import get_world_9
from app.content.worlds_10_to_12 import get_world_10, get_world_12
from app.routes.worlds import judge_level, _level_by_id, _all_level_ids, _is_unlocked
from app.services.gamification import check_boss_eligibility

def test_world_boss(world, world_name):
    print(f"\n=== {world_name} ===")
    
    towns = world.towns if hasattr(world, "towns") else []
    all_lessons = []
    for town in towns:
        for lesson in town.lessons:
            all_lessons.append(lesson)
    
    # Find a regular level to complete
    regular = [l for l in all_lessons if l.kind != "boss"]
    bosses = [l for l in all_lessons if l.kind == "boss"]
    
    if not regular:
        print(f"No regular lessons found")
        return False
    
    # Pick first regular level
    test_level = regular[0]
    print(f"Testing level: {test_level.id} - {test_level.title}")
    print(f"  Concept: {test_level.concept}")
    print(f"  Required patterns: {test_level.checks.required_patterns if test_level.checks else 'None'}")
    
    # Get the test cases
    test_cases = []
    if test_level.steps:
        for step in test_level.steps:
            if hasattr(step, 'test_cases') and step.test_cases:
                test_cases.extend(step.test_cases)
    
    print(f"  Test cases: {len(test_cases)}")
    
    # Submit a solution that matches the required patterns
    code = ""
    if test_level.steps:
        for step in test_level.steps:
            if hasattr(step, 'signature') and step.signature:
                # Generate a simple solution based on the function name
                func_name = step.function_name or "solution"
                if "email" in func_name.lower():
                    code = f"def {func_name}(email: str) -> bool:\n    return '@' in email and '.' in email"
                elif "endpoint" in func_name.lower():
                    code = f"def {func_name}() -> dict:\n    return {{'validate': True, 'auth': True}}"
                elif "design" in func_name.lower() or "define" in func_name.lower():
                    code = f"def {func_name}() -> dict:\n    return {{'endpoints': [], 'schema': {{}}}}"
                elif "prompt" in func_name.lower():
                    code = f"def {func_name}() -> str:\n    return 'prompt'"
                elif "rag" in func_name.lower():
                    code = f"def {func_name}() -> dict:\n    return {{'rag': True}}"
                elif "eval" in func_name.lower():
                    code = f"def {func_name}() -> dict:\n    return {{'test_cases': [], 'metrics': []}}"
                elif "agent" in func_name.lower() or "design_ai" in func_name.lower():
                    code = f"def {func_name}() -> dict:\n    return {{'prompt': '', 'rag': {{}}, 'eval': {{}}}}"
                else:
                    code = f"def {func_name}() -> dict:\n    return {{'result': True}}"
                break
    
    if not code:
        code = "def solution() -> dict:\n    return {'result': True}"
    
    print(f"  Submitted code:\n{code}")
    
    # Judge the level
    passed, message, hint_idx = judge_level(test_level, code)
    print(f"  Judge result: {'PASS' if passed else 'FAIL'}")
    print(f"  Message: {message}")
    
    if not passed:
        print(f"  Hint index: {hint_idx}")
        return False
    
    # If passed, check if boss unlocks
    all_ids = _all_level_ids(world)
    completed = {f"{world.id}:{test_level.id}": {"completed": True, "score": 100}}
    
    boss_unlocked = False
    for boss in bosses:
        unlocked = _is_unlocked(boss.id, all_ids, completed, world.id)
        print(f"  Boss {boss.id} unlocked: {unlocked}")
        if unlocked:
            boss_unlocked = True
    
    # Simulate boss eligibility check
    boss_result = check_boss_eligibility("test-user", 100.0, "boss_battle")
    if boss_result:
        print(f"  Boss eligibility: {boss_result}")
    else:
        print(f"  Boss eligibility: None (level not a boss level or already defeated)")
    
    return passed

print("=== WORLDS 9-12 REAL JUDGE EXECUTION TEST ===")

w9 = get_world_9()
w12 = get_world_12()

# World 11 needs direct import
try:
    from app.content.worlds_10_to_12 import get_world_11
    w11 = get_world_11()
except (ImportError, AttributeError):
    print("World 11 getter not found")
    w11 = None

results = {}

if w9:
    results["world9"] = test_world_boss(w9, "World 9 (AI Engineering)")
if w11:
    results["world11"] = test_world_boss(w11, "World 11 (Projects)")
if w12:
    results["world12"] = test_world_boss(w12, "World 12 (Creative)")

print("\n=== EXECUTION SUMMARY ===")
for key, result in results.items():
    print(f"{key}: {'PASS' if result else 'FAIL'}")

all_pass = all(results.values())
if all_pass:
    print("\nAll worlds judge+boss test: PASS")
else:
    print("\nSome worlds failed judge+boss test")
