import importlib.util
spec = importlib.util.spec_from_file_location("python", "D:/Project-Fremen/backend/app/services/lessons/python.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
lessons = mod.PYTHON_LESSONS
print("Total Python lessons:", len(lessons))
print("First 5:")
for l in lessons[:5]:
    print("  -", l["id"], ":", l["title"], "(", l["difficulty"], ")")
print("Middle 5:")
mid = len(lessons) // 2
for l in lessons[mid:mid+5]:
    print("  -", l["id"], ":", l["title"], "(", l["difficulty"], ")")
print("Last 3:")
for l in lessons[-3:]:
    print("  -", l["id"], ":", l["title"], "(", l["difficulty"], ")")
topics = set()
for l in lessons:
    topics.add(l["id"].split("-")[1])
print("\nUnique topics:", len(topics))
print("Topics:", sorted(list(topics))[:30])
step_types = set()
for l in lessons:
    for s in l["steps"]:
        step_types.add(s["type"])
print("Step types:", step_types)
# Check content diversity
contents = set()
for l in lessons:
    for s in l["steps"]:
        if s["type"] == "explain":
            contents.add(s["content"])
print("Unique explain contents:", len(contents))
# Check XP distribution
xp_values = set(l["xpReward"] for l in lessons)
print("XP values:", xp_values)
# Check difficulty distribution
from collections import Counter
diffs = Counter(l["difficulty"] for l in lessons)
print("Difficulty distribution:", dict(diffs))