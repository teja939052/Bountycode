"""Assessment blueprint + weighted sampling with largest-remainder allocation."""
import random
from typing import Any, Dict, List, Optional

from app.services.question_store import find


def allocate_counts(total: int, weights: Dict[str, float]) -> Dict[str, int]:
    if total <= 0 or not weights:
        return {k: 0 for k in weights}
    s = sum(weights.values()) or 1.0
    raw = {k: (w / s) * total for k, w in weights.items()}
    floors = {k: int(v) for k, v in raw.items()}
    remainder = total - sum(floors.values())
    order = sorted(raw.keys(), key=lambda k: (raw[k] - floors[k]), reverse=True)
    for i in range(remainder):
        floors[order[i % len(order)]] += 1
    return floors


def select_questions(
    topic: Optional[str] = None,
    category: Optional[str] = None,
    difficulty_mix: Optional[Dict[str, int]] = None,
    total: int = 10,
    seed: Optional[int] = None,
) -> List[dict]:
    query: Dict[str, Any] = {}
    if topic:
        query["topic"] = topic
    if category:
        query["category"] = category
    rng = random.Random(seed) if seed is not None else random.Random()
    if difficulty_mix:
        weights = {k: float(v) for k, v in difficulty_mix.items()}
        counts = allocate_counts(total, weights)
        chosen: List[dict] = []
        for diff, n in counts.items():
            q = dict(query)
            q["difficulty"] = diff
            cursor = find(q)
            if hasattr(cursor, "prefer_verified"):
                cursor = cursor.prefer_verified()
            pool = cursor.to_list() if hasattr(cursor, "to_list") else list(cursor)
            rng.shuffle(pool)
            chosen.extend(pool[:n])
        if len(chosen) < total:
            cursor = find(query)
            if hasattr(cursor, "prefer_verified"):
                cursor = cursor.prefer_verified()
            pool = cursor.to_list() if hasattr(cursor, "to_list") else list(cursor)
            ids = {q.get("id") for q in chosen}
            extra = [q for q in pool if q.get("id") not in ids]
            rng.shuffle(extra)
            chosen.extend(extra[: total - len(chosen)])
        rng.shuffle(chosen)
        return chosen[:total]
    cursor = find(query)
    if hasattr(cursor, "prefer_verified"):
        cursor = cursor.prefer_verified()
    pool = cursor.to_list() if hasattr(cursor, "to_list") else list(cursor)
    rng.shuffle(pool)
    return pool[:total]
