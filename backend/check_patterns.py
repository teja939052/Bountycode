from app.data.worlds_data import WORLD_REGISTRY

for wid, w in sorted(WORLD_REGISTRY.items(), key=lambda x: x[1].order):
    has_patterns = False
    for town in w.towns:
        for lvl in town.lessons:
            patterns = lvl.checks.required_patterns if lvl.checks else []
            if patterns:
                has_patterns = True
                print(f"  {wid}/{lvl.id}: patterns={patterns}")
    if not has_patterns:
        print(f"{wid}: all patterns empty")
    else:
        print(f"{wid}: HAS PATTERNS")
