"""Add pedagogy_profile to Gold 10 atoms."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_DATA_DIR = Path(__file__).parent.parent / "backend" / "app" / "data"
_ATOMS_FILE = _DATA_DIR / "python_50_atoms.json"

_GOLD_10 = [
    "python.001", "python.006", "python.008", "python.017",
    "python.022", "python.023", "python.027", "python.032",
    "python.043", "python.050"
]


def _profile_for(atom: dict) -> dict:
    concept = atom.get("concept", "")
    title = atom.get("title", "")
    misconception_codes = atom.get("misconception_codes", [])

    base = {
        "mental_model": atom.get("mental_model", ""),
        "core_insight": atom.get("why_this_matters", ""),
        "common_misconceptions": misconception_codes,
        "preferred_representation": atom.get("metaphor_key", concept),
        "interaction_purpose": {
            "state_manipulation": "Make the invisible memory state tangible",
            "freeze_predict": "Force prediction before seeing execution",
            "memory_board": "Show variables as named locations with values",
            "code_blocks": "Assemble logical order without syntax friction",
            "bug_surgery": "See consequences of a single structural mistake",
            "explain_to_unlock": "Require conceptual explanation, not pattern matching",
        },
        "reteach_routes": {
            misconception_codes[0] if len(misconception_codes) > 0 else "generic": "visual_state",
            misconception_codes[1] if len(misconception_codes) > 1 else "generic": "worked_example",
        },
        "transfer_targets": [
            f"Apply {concept} to a business problem",
            f"Apply {concept} to a data-processing problem",
            f"Apply {concept} to a user-interface problem",
        ],
    }
    return base


def main() -> int:
    with open(_ATOMS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    atoms = data.get("atoms", {})
    updated = 0
    for atom_id in _GOLD_10:
        atom = atoms.get(atom_id)
        if not atom:
            continue
        if "pedagogy_profile" not in atom:
            atom["pedagogy_profile"] = _profile_for(atom)
            updated += 1

    with open(_ATOMS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Updated {updated} Gold 10 atoms with pedagogy_profile")
    return 0


if __name__ == "__main__":
    sys.exit(main())
