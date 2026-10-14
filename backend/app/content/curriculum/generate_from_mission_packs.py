"""Generate curriculum lesson modules from existing mission packs.

Reads mission_packs/*.json and emits curriculum/*.py modules that
register the pack content as canonical lesson dicts consumable by
DomainAdapter._authored_content() / registry.get_lesson_dict().
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

MISSION_PACKS_DIR = Path(__file__).resolve().parents[1] / "mission_packs"
CURRICULUM_DIR = Path(__file__).resolve().parent


def _slugify(text: str) -> str:
    return text.lower().replace(" ", "_").replace("/", "_").replace("-", "_")


def _python_value(value: Any) -> str:
    if value is None:
        return "None"
    if isinstance(value, str):
        return repr(value)
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        items = ", ".join(_python_value(v) for v in value)
        return f"[{items}]"
    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            lines.append(f"            {repr(k)}: {_python_value(v)}")
        inner = ",\n".join(lines)
        return f"{{\n{inner}\n        }}"
    return repr(value)


def _pack_to_lesson(pack: Dict[str, Any]) -> Dict[str, Any]:
    lesson_id = pack.get("id", _slugify(pack.get("title", "lesson")))
    module_id = pack.get("skill_id") or pack.get("id", lesson_id)
    domain = pack.get("domain", "coding")
    concept = pack.get("concept") or pack.get("title", lesson_id)

    steps: Dict[str, Any] = {}
    for step_name in [
        "discover",
        "understand",
        "manipulate",
        "predict",
        "build",
        "break_step",
        "debug",
        "retrieval",
        "transfer",
    ]:
        step_data = pack.get(step_name, {})
        if step_data:
            steps[step_name] = step_data

    srs_key_points = pack.get("srs_key_points", [])
    if not srs_key_points:
        srs_key_points = [concept]

    practice = pack.get("practice", [])
    proof = pack.get("proof", [])
    if not proof and practice:
        proof = [
            {
                "id": f"{lesson_id}-p1",
                "prompt": practice[0].get("prompt", f"Prove your {concept} skill."),
                "answer_format": "text",
                "correct": practice[0].get("answer", ""),
                "explanation": practice[0].get("explanation", ""),
                "time_limit_seconds": 60,
                "company_tags": [],
            }
        ]

    return {
        "lesson_id": lesson_id,
        "module_id": module_id,
        "title": pack.get("title", concept),
        "description": pack.get("why_it_matters", f"Master {concept}."),
        "difficulty": pack.get("difficulty", "medium"),
        "est_minutes": pack.get("estimated_minutes", 20),
        "xp_reward": 100,
        "skills_taught": [concept],
        "srs_concept_tag": module_id,
        "domain": domain,
        "captain_byte": pack.get("captain_byte", {}),
        "story_context": {
            "title": pack.get("title", concept),
            "narration": pack.get("why_it_matters", f"Master {concept}."),
            "setting": concept.lower().replace(" ", "_"),
            "character": "Captain Byte",
            "intro_text": pack.get("why_it_matters", f"Master {concept}."),
        },
        "steps": steps,
        "practice": practice,
        "proof": proof,
        "company_variants": pack.get("company_variants", []),
        "misconceptions": pack.get("misconceptions", []),
        "srs_key_points": srs_key_points,
        "srs_review_intervals": pack.get("srs_review_intervals", [1, 3, 7, 14, 30]),
        "world_progression": {
            "world_id": domain,
            "competency_id": concept.lower().replace(" ", "_"),
            "unlocks_next": [],
            "tower_badge": f"{domain}_{_slugify(concept)}",
        },
    }


def _emit_module(lesson: Dict[str, Any], filename: str) -> str:
    title = lesson.get("title", "Lesson")
    slug = filename.replace(".py", "")
    lines = [
        f'"""Lesson module — {title}"""',
        "from typing import Dict, Any",
        "",
        f"LESSON: Dict[str, Any] = {_python_value(lesson)}",
        "",
        f"SLUG = {repr(slug)}",
        "",
    ]
    return "\n".join(lines)


def generate_all(force: bool = False) -> Dict[str, str]:
    generated: Dict[str, str] = {}
    for path in MISSION_PACKS_DIR.glob("*.json"):
        slug = path.stem
        filename = f"{slug}.py"
        out_path = CURRICULUM_DIR / filename
        if out_path.exists() and not force:
            continue

        with open(path, "r", encoding="utf-8") as f:
            pack = json.load(f)
        lesson = _pack_to_lesson(pack)
        module_text = _emit_module(lesson, filename)
        out_path.write_text(module_text, encoding="utf-8")
        generated[slug] = str(out_path)
    return generated


if __name__ == "__main__":
    generated = generate_all(force=True)
    print(f"Generated {len(generated)} curriculum modules")
    for slug, path in sorted(generated.items()):
        print(f"  {slug} -> {path}")
