"""LeetCode metadata overlay for curated questions.

Merges metadata (full statement, constraints, expected complexity, follow-up,
per-example explanations, LeetCode problem numbers) from ``part_*.py`` modules
into a single ``LEETCODE_META`` dict keyed by question slug id.

Consumer: ``backend/app/services/question_store.py`` enriches curated questions
with this overlay after loading.
"""

import importlib
import os

LEETCODE_META = {}

_parts_dir = os.path.dirname(__file__)
for _name in sorted(os.listdir(_parts_dir)):
    if _name.startswith("part_") and _name.endswith(".py"):
        _mod = importlib.import_module(f"{__name__}.{_name[:-3]}")
        LEETCODE_META.update(getattr(_mod, "LEETCODE_META", {}))

__all__ = ["LEETCODE_META"]
