"""Generate 8-mode teaching data for all atoms.

Reads python_50_atoms.json and adds connect/explain/show/experience/guide/fade/transfer/prove
to every atom that does not already have them.

Strategy:
- Use the atom's concept, title, and existing metadata to build mode-specific content.
- Reuse existing transfer/prove when present.
- For language-awareness, reference concept skins from languages_registry.json.
- For company-awareness, reference service_company_relevance.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_DATA_DIR = Path(__file__).parent.parent / "backend" / "app" / "data"
_ATOMS_FILE = _DATA_DIR / "python_50_atoms.json"
_LANG_FILE = _DATA_DIR / "languages_registry.json"
_METAPHOR_FILE = _DATA_DIR / "metaphor_registry.json"

_MODES = [
    "connect",
    "explain",
    "show",
    "experience",
    "guide",
    "fade",
    "transfer",
    "prove",
]


def _load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _ensure(data: dict, key: str, factory):
    if key not in data:
        data[key] = factory()


def _concept_examples(concept: str, lang: str = "python") -> dict:
    """Return language-aware examples for a concept from the registry."""
    try:
        reg = _load_json(_LANG_FILE)
        skin = reg.get("languages", {}).get(lang, {}).get("concept_skins", {}).get(concept, {})
        if skin:
            return skin
    except Exception:
        pass
    return {}


def _build_connect(atom: dict) -> dict:
    concept = atom.get("concept", "")
    title = atom.get("title", "")
    return {
        "mode": "story",
        "title": f"Why {title.lower()} matters",
        "teacher_say": f"Imagine you are managing something important: money, a list of names, a scoreboard. You need the computer to remember and update it correctly. That is what '{title.lower()}' solves.",
        "problem": f"Think of a real situation where you would need to: {title.lower()}.",
        "interaction_type": "reflection",
        "success_feedback": "Good. That everyday situation is exactly why this concept exists.",
        "failure_feedback": "Try once more with a simpler example.",
    }


def _build_explain(atom: dict) -> dict:
    concept = atom.get("concept", "")
    mental = atom.get("mental_model", "")
    return {
        "mode": "direct-teach",
        "title": f"Understanding {concept}",
        "steps": [
            {
                "say": mental or f"Let's understand {concept} clearly.",
                "visual": "text",
                "content": mental or concept,
            },
            {
                "say": "This is not just syntax. It is a mental model you will use in every program.",
                "visual": "text",
                "content": "Reusable mental model",
            },
        ],
        "teacher_summary": mental or f"Understand {concept} as a reusable mental model.",
    }


def _build_show(atom: dict) -> dict:
    see = atom.get("see", {})
    frames = see.get("steps", [])
    if not frames:
        frames = [{"scene": atom.get("title", ""), "duration_ms": 1500}]
    return {
        "mode": "animation",
        "title": f"Watch: {atom.get('title', '')}",
        "animation_key": see.get("animation", atom.get("concept", "")),
        "frames": frames,
    }


def _build_experience(atom: dict) -> dict:
    concept = atom.get("concept", "")
    return {
        "mode": "interactive",
        "title": f"Try {concept}",
        "instruction": f"Change values and see how {concept} behaves.",
        "manipulatives": [
            {
                "type": concept,
                "initial": {"value": "example"},
                "actions": ["change", "observe"],
            }
        ],
    }


def _build_guide(atom: dict) -> dict:
    build = atom.get("build", {})
    concept = atom.get("concept", "")
    skin = _concept_examples(concept)
    starter = build.get("starter_code") or next(iter(skin.values()), "# Write your code here\n")
    solution = build.get("solution") or starter
    blanks = []
    if "_" in starter:
        blanks = [part.strip() for part in starter.split("_") if part.strip()]
    return {
        "mode": "scaffold",
        "title": f"Write {concept}",
        "prompt": f"Complete the code for {concept}.",
        "starter_code": starter,
        "solution": solution,
        "blanks": blanks,
        "hints": [
            "Think about the syntax for this concept.",
            "Check the example shown earlier.",
        ],
    }


def _build_fade(atom: dict) -> dict:
    build = atom.get("build", {})
    starter = build.get("starter_code", "# Write code here\n")
    return {
        "mode": "gradual-release",
        "title": "Write it independently",
        "stages": [
            {
                "stage": "full-example",
                "show_code": True,
                "prompt": "Read the complete example carefully.",
            },
            {
                "stage": "partial",
                "show_code": False,
                "starter_code": starter,
                "blanks": [],
            },
            {
                "stage": "no-help",
                "show_code": False,
                "starter_code": "# Write the full solution\n",
                "blanks": [],
            },
        ],
    }


def _build_transfer(atom: dict) -> dict:
    existing = atom.get("transfer", {})
    if existing:
        return existing
    concept = atom.get("concept", "")
    return {
        "mode": "new-context",
        "title": f"Transfer: {concept}",
        "context": "real_world",
        "story": f"Use {concept} in a new situation.",
        "task": "Apply what you learned.",
        "options": ["Option A", "Option B", "Option C"],
        "correct_order": [0, 1, 2],
    }


def _build_prove(atom: dict) -> dict:
    existing = atom.get("prove", {})
    if existing:
        return existing
    concept = atom.get("concept", "")
    return {
        "mode": "assessment",
        "title": f"Prove: {concept}",
        "tasks": [
            {
                "type": "predict",
                "prompt": f"What happens when you apply {concept}?",
                "answer": "It works as expected.",
            },
            {
                "type": "code",
                "prompt": f"Write code using {concept}.",
                "starter_code": "# Write here\n",
                "solution": "# Solution\npass",
            },
        ],
        "passing_score": 80,
    }


def _apply_8modes(atom: dict) -> dict:
    _ensure(atom, "connect", lambda: _build_connect(atom))
    _ensure(atom, "explain", lambda: _build_explain(atom))
    _ensure(atom, "show", lambda: _build_show(atom))
    _ensure(atom, "experience", lambda: _build_experience(atom))
    _ensure(atom, "guide", lambda: _build_guide(atom))
    _ensure(atom, "fade", lambda: _build_fade(atom))
    _ensure(atom, "transfer", lambda: _build_transfer(atom))
    _ensure(atom, "prove", lambda: _build_prove(atom))
    return atom


def main() -> int:
    if not _ATOMS_FILE.exists():
        print(f"Atoms file not found: {_ATOMS_FILE}")
        return 1

    data = _load_json(_ATOMS_FILE)
    atoms = data.get("atoms", {})
    updated = 0
    for atom_id, atom in atoms.items():
        before = [k for k in atom.keys() if k in _MODES]
        _apply_8modes(atom)
        after = [k for k in atom.keys() if k in _MODES]
        if len(before) < len(after):
            updated += 1

    with open(_ATOMS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Updated {updated} atoms with 8-mode teaching data")
    print(f"Total atoms: {len(atoms)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
