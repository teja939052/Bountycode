import json

with open("app/data/india_placement_depth.json", "r", encoding="utf-8") as f:
    data = json.load(f)

broken_count = 0
for q in data:
    t = str(q.get("type", "")).lower()
    if t not in ("aptitude", "logical", "verbal"):
        continue
    opts = q.get("options", [])
    if len(opts) < 4:
        broken_count += 1
        if broken_count <= 3:
            print(f"{q.get('id')}: options={opts}, correct_index={q.get('correct_index')}")

print(f"Total with <4 options: {broken_count}")
