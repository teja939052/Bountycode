from app.data.worlds_data import WORLD_REGISTRY
order = sorted(WORLD_REGISTRY.values(), key=lambda w: w.order)
for w in order:
    prereq = list(getattr(w, "prerequisites", []) or [])
    levels = sum(len(t.levels) for t in w.towns)
    print(f'{w.id}: order={w.order}, prerequisites={prereq}, levels={levels}')