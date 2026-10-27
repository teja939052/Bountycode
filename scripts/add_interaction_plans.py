"""Add interaction_plan to all atoms.

Each atom gets a choreographed sequence of interactions from the 15 core types.
The plan is derived from the atom's concept and existing teaching data.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_DATA_DIR = Path(__file__).parent.parent / "backend" / "app" / "data"
_ATOMS_FILE = _DATA_DIR / "python_50_atoms.json"

_INTERACTION_TYPES = [
    "state_manipulation",
    "slider",
    "toggle",
    "freeze_predict",
    "time_travel",
    "memory_board",
    "code_blocks",
    "fill_missing",
    "bug_surgery",
    "first_wrong_moment",
    "compare_worlds",
    "counterexample_builder",
    "reverse_engineer",
    "explain_to_unlock",
    "same_concept_new_world",
]


def _build_interaction_plan(atom: dict) -> list[dict]:
    concept = atom.get("concept", "")
    title = atom.get("title", "").lower()

    plan = []

    if "variable" in concept or "state" in concept or "assignment" in concept:
        plan.extend([
            {"type": "state_manipulation", "params": {"variable": "balance", "initial": 500}},
            {"type": "slider", "params": {"variable": "balance", "min": 0, "max": 1000, "step": 50}},
            {"type": "freeze_predict", "params": {"after_line": 2, "question": "What is the value now?"}},
            {"type": "memory_board", "params": {"variables": ["balance"]}},
        ])
    elif "loop" in concept or "iteration" in concept or "repeat" in title:
        plan.extend([
            {"type": "slider", "params": {"variable": "count", "min": 1, "max": 10, "step": 1}},
            {"type": "time_travel", "params": {"steps": 5, "question": "What is the loop variable at each step?"}},
            {"type": "freeze_predict", "params": {"after_line": 3, "question": "What prints next?"}},
            {"type": "bug_surgery", "params": {"bug": "off_by_one", "fix": "one change"}},
        ])
    elif "condition" in concept or "if" in concept or "branch" in title:
        plan.extend([
            {"type": "toggle", "params": {"condition": "age >= 18", "values": [16, 18, 21]}},
            {"type": "compare_worlds", "params": {"left": "age >= 18", "right": "age > 18"}},
            {"type": "counterexample_builder", "params": {"claim": "The condition always passes"}},
            {"type": "freeze_predict", "params": {"after_line": 2, "question": "Which branch runs?"}},
        ])
    elif "function" in concept:
        plan.extend([
            {"type": "fill_missing", "params": {"missing": "return statement"}},
            {"type": "reverse_engineer", "params": {"input": 5, "output": 25, "rule": "square"}},
            {"type": "explain_to_unlock", "params": {"questions": ["What does x represent?", "Why return?"]}},
            {"type": "same_concept_new_world", "params": {"context": "calculator"}},
        ])
    elif "list" in concept or "array" in concept:
        plan.extend([
            {"type": "state_manipulation", "params": {"variable": "items", "initial": [1, 2, 3]}},
            {"type": "code_blocks", "params": {"blocks": ["for item in items:", "print(item)", "total += item"]}},
            {"type": "bug_surgery", "params": {"bug": "index_error", "fix": "one change"}},
            {"type": "time_travel", "params": {"steps": 4, "question": "What is the index at each step?"}},
        ])
    else:
        plan.extend([
            {"type": "state_manipulation", "params": {"variable": "x", "initial": 0}},
            {"type": "freeze_predict", "params": {"after_line": 2, "question": "What is the value?"}},
            {"type": "code_blocks", "params": {"blocks": ["line1", "line2", "line3"]}},
            {"type": "same_concept_new_world", "params": {"context": "real_world"}},
        ])

    return plan[:6]


def main() -> int:
    if not _ATOMS_FILE.exists():
        print(f"Atoms file not found: {_ATOMS_FILE}")
        return 1

    with open(_ATOMS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    atoms = data.get("atoms", {})
    updated = 0
    for atom_id, atom in atoms.items():
        if "interaction_plan" not in atom:
            atom["interaction_plan"] = _build_interaction_plan(atom)
            updated += 1

    with open(_ATOMS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Updated {updated} atoms with interaction_plan")
    print(f"Total atoms: {len(atoms)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
