"""World governance: enforce the canonical 12-world structure and dependent surfaces.

This module is the single source of truth for:
- Total world count (12)
- Total level count (50)
- Prerequisite chain integrity (11 edges)
- Landing page copy consistency
- In-code documentation requirements

Any change to world count or structure MUST update:
1. backend/app/data/worlds_data.py WORLD_REGISTRY
2. frontend/src/pages/Landing.tsx headline copy
3. Any tests referencing world count (test_rank_badge.py, etc.)
4. This file's canonical manifest below
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════
# CANONICAL 12-WORLD MANIFEST
# ═══════════════════════════════════════════════════════════════════
# Order matters: this is the expected progression path.
# Each world's prerequisite must be the previous world, except foundations which has none.

CANONICAL_WORLDS = [
    ("foundations", "Beginner Valley", 1, []),
    ("searchlands", "Searchlands", 2, ["foundations"]),
    ("sorting", "Sorting Forge", 3, ["searchlands"]),
    ("recursion", "Recursive Mountains", 4, ["sorting"]),
    ("linked", "Linked List Caves", 5, ["recursion"]),
    ("stack", "Stack Peaks", 6, ["linked"]),
    ("queue", "Queue Plains", 7, ["stack"]),
    ("hashing", "Hashing Marshes", 8, ["queue"]),
    ("trees", "Binary Tree Forest", 9, ["hashing"]),
    ("graphs", "Graph Canyons", 10, ["trees"]),
    ("dynamic", "DP Dungeon", 11, ["graphs"]),
    ("alpine", "Alpine Summit", 12, ["dynamic"]),
]

EXPECTED_TOTAL_WORLDS = 12
EXPECTED_TOTAL_LEVELS = 50
EXPECTED_LANDING_COPY = "12 worlds. 50 levels. One voyage."
EXPECTED_PREREQ_EDGES = 11


def _check_world_registry() -> list[str]:
    """Verify WORLD_REGISTRY matches canonical manifest."""
    errors: list[str] = []
    try:
        from app.data.worlds_data import WORLD_REGISTRY
    except Exception as exc:
        return [f"Cannot import WORLD_REGISTRY: {exc}"]

    if len(WORLD_REGISTRY) != EXPECTED_TOTAL_WORLDS:
        errors.append(
            f"WORLD_REGISTRY has {len(WORLD_REGISTRY)} worlds, expected {EXPECTED_TOTAL_WORLDS}"
        )

    for wid, name, order, prereqs in CANONICAL_WORLDS:
        if wid not in WORLD_REGISTRY:
            errors.append(f"Missing world: {wid}")
            continue
        world = WORLD_REGISTRY[wid]
        if world.order != order:
            errors.append(f"World {wid} has order {world.order}, expected {order}")
        actual_prereqs = list(getattr(world, "prerequisites", []) or [])
        if actual_prereqs != prereqs:
            errors.append(
                f"World {wid} has prereqs {actual_prereqs}, expected {prereqs}"
            )

    # Check for unexpected worlds
    expected_ids = {wid for wid, *_ in CANONICAL_WORLDS}
    for wid in WORLD_REGISTRY:
        if wid not in expected_ids:
            errors.append(f"Unexpected world in registry: {wid}")

    return errors


def _check_level_count() -> list[str]:
    """Verify total level count matches expected 72."""
    errors: list[str] = []
    try:
        from app.data.worlds_data import WORLD_REGISTRY
    except Exception as exc:
        return [f"Cannot import WORLD_REGISTRY: {exc}"]

    total = 0
    for wid, world in WORLD_REGISTRY.items():
        towns = getattr(world, "towns", []) or []
        for town in towns:
            levels = getattr(town, "levels", []) or []
            total += len(levels)

    if total != EXPECTED_TOTAL_LEVELS:
        errors.append(
            f"Total levels = {total}, expected {EXPECTED_TOTAL_LEVELS}"
        )

    return errors


def _check_prereq_chain() -> list[str]:
    """Verify every prerequisite resolves to an existing world."""
    errors: list[str] = []
    try:
        from app.data.worlds_data import WORLD_REGISTRY
    except Exception as exc:
        return [f"Cannot import WORLD_REGISTRY: {exc}"]

    edge_count = 0
    for wid, world in WORLD_REGISTRY.items():
        for pid in list(getattr(world, "prerequisites", []) or []):
            edge_count += 1
            if pid not in WORLD_REGISTRY:
                errors.append(
                    f"World {wid} has unresolved prerequisite: {pid}"
                )

    if edge_count != EXPECTED_PREREQ_EDGES:
        errors.append(
            f"Prerequisite edge count = {edge_count}, expected {EXPECTED_PREREQ_EDGES}"
        )

    return errors


def _check_landing_copy() -> list[str]:
    """Verify landing page copy matches expected 12-world identity."""
    errors: list[str] = []
    landing_path = Path(__file__).resolve().parents[2] / "frontend" / "src" / "pages" / "Landing.tsx"
    if not landing_path.exists():
        return [f"Landing page not found at {landing_path}"]

    text = landing_path.read_text(encoding="utf-8")
    if EXPECTED_LANDING_COPY not in text:
        errors.append(
            f"Landing page missing expected copy: '{EXPECTED_LANDING_COPY}'"
        )
    return errors


def _check_world_documentation() -> list[str]:
    """Verify each world file documents the canonical 12-world constraint."""
    errors: list[str] = []
    worlds_dir = Path(__file__).resolve().parents[2] / "backend" / "app" / "content"
    expected_marker = "CANONICAL_WORLDS in backend/scripts/verify_world_governance.py"
    for py_file in worlds_dir.glob("worlds_*.py"):
        text = py_file.read_text(encoding="utf-8")
        if expected_marker not in text:
            errors.append(
                f"{py_file.name} does not document the 12-world constraint"
            )
    return errors


def run_all_checks() -> bool:
    """Run all governance checks. Returns True if all pass."""
    all_errors: list[str] = []
    all_errors.extend(_check_world_registry())
    all_errors.extend(_check_level_count())
    all_errors.extend(_check_prereq_chain())
    all_errors.extend(_check_landing_copy())
    all_errors.extend(_check_world_documentation())

    if all_errors:
        print("WORLD GOVERNANCE CHECK: FAIL")
        for err in all_errors:
            print(f"  - {err}")
        return False

    print("WORLD GOVERNANCE CHECK: PASS")
    print(f"  Worlds: {EXPECTED_TOTAL_WORLDS}")
    print(f"  Levels: {EXPECTED_TOTAL_LEVELS}")
    print(f"  Prereq edges: {EXPECTED_PREREQ_EDGES}")
    print(f"  Landing copy: '{EXPECTED_LANDING_COPY}'")
    return True


if __name__ == "__main__":
    # Ensure backend root is importable
    backend_root = Path(__file__).resolve().parents[1]
    if str(backend_root) not in sys.path:
        sys.path.insert(0, str(backend_root))

    ok = run_all_checks()
    sys.exit(0 if ok else 1)
