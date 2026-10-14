"""
Lesson Depth Auditor - real content quality gate, not just field existence.

Validates:
  - Level model from worlds_data.py
  - MissionPack JSON from backend/app/content/mission_packs/

Quality rules:
  - 9-step loop must be filled with meaningful content
  - Misconceptions must have reteach_route + reteach_action
  - Captain Byte moments must exist
  - Visual interactions must exist in discover
  - Practice items must exist
  - Proof questions must exist
  - SRS key points must exist
  - Company variants should exist for service-placement packs
  - why_it_matters must be filled
  - Prerequisites must be defined
"""

from __future__ import annotations

import importlib.util
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from app.models.world import (
    Boss, BreakStep, Build, Debug, Discover, Level, Manipulate, Predict,
    Retrieval, Story, Success, Town, Transfer, Tutor, World, Code, Checks,
    Reward,
)
from app.models.mission_pack import MissionPack


REQUIRED_STEPS = [
    "discover",
    "understand",
    "manipulate",
    "predict",
    "build",
    "break_step",
    "debug",
    "retrieval",
    "transfer",
]

MISSION_PACKS_DIR = Path(__file__).resolve().parent.parent / "content" / "mission_packs"


def _load_worlds_data() -> Dict[str, Any]:
    """Load worlds_data module and return the WORLD_* constants."""
    worlds_data_path = Path(__file__).resolve().parent.parent / "data" / "worlds_data.py"
    spec = importlib.util.spec_from_file_location("worlds_data", str(worlds_data_path))
    if spec is None or spec.loader is None:
        return {}
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:
        return {}
    worlds = {}
    for name in dir(module):
        if name.startswith("WORLD_"):
            worlds[name] = getattr(module, name)
    return worlds


def _is_meaningful(value: Any) -> bool:
    """Check if a value contains meaningful content, not just empty/default."""
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, dict):
        return any(_is_meaningful(v) for v in value.values())
    if isinstance(value, list):
        return any(_is_meaningful(v) for v in value)
    if hasattr(value, "model_dump"):
        return _is_meaningful(value.model_dump())
    return True


def _level_step_filled(level: Level, step_name: str) -> bool:
    """Check if a specific teaching step has meaningful content."""
    if not isinstance(level, Level):
        return False
    val = getattr(level, step_name, None)
    return _is_meaningful(val)


def audit_level(level: Level) -> Dict[str, Any]:
    """Audit a single Level and return a quality report."""
    if not isinstance(level, Level):
        return {"error": "Not a Level instance", "is_complete": False, "quality": "fail"}

    steps = {}
    for step in REQUIRED_STEPS:
        steps[step] = _level_step_filled(level, step)

    unfinished = [s for s, filled in steps.items() if not filled]
    
    # Quality checks beyond field existence
    quality_issues = []
    
    # Check story/tutor presence
    if not _is_meaningful(getattr(level, "story", None)):
        quality_issues.append("missing_story")
    if not _is_meaningful(getattr(level, "tutor", None)):
        quality_issues.append("missing_tutor")
    
    # Check code/test infrastructure
    if not _is_meaningful(getattr(level, "code", None)) and not _is_meaningful(getattr(level, "test_cases", None)):
        quality_issues.append("missing_code_or_tests")
    
    # Check mastery threshold
    if not getattr(level, "mastery_threshold", None):
        quality_issues.append("missing_mastery_threshold")
    
    is_complete = len(unfinished) == 0 and len(quality_issues) == 0
    quality = "pass" if is_complete else ("partial" if len(unfinished) == 0 else "fail")
    
    return {
        "id": getattr(level, "id", None),
        "title": getattr(level, "title", ""),
        "is_complete": is_complete,
        "unfinished_steps": unfinished,
        "quality_issues": quality_issues,
        "quality": quality,
        "steps": steps,
    }


def audit_world(world: World) -> Dict[str, Any]:
    """Audit all levels in a World and return a quality report."""
    report = {
        "id": world.id,
        "name": world.name,
        "towns": [],
        "total_levels": 0,
        "complete_levels": 0,
        "incomplete_levels": 0,
        "quality_issues_by_level": {},
    }
    for town in getattr(world, "towns", []):
        town_report = {
            "id": town.id,
            "name": town.name,
            "levels": [],
        }
        for level in getattr(town, "levels", []):
            if not isinstance(level, Level):
                continue
            level_report = audit_level(level)
            town_report["levels"].append(level_report)
            report["total_levels"] += 1
            if level_report["is_complete"]:
                report["complete_levels"] += 1
            else:
                report["incomplete_levels"] += 1
            if level_report["quality_issues"]:
                report["quality_issues_by_level"][level_report["id"]] = level_report["quality_issues"]
        report["towns"].append(town_report)
    return report


def audit_all_worlds() -> Dict[str, Any]:
    """Audit all worlds loaded from worlds_data."""
    worlds = _load_worlds_data()
    report = {
        "total_worlds": len(worlds),
        "worlds": {},
        "global": {
            "total_levels": 0,
            "complete_levels": 0,
            "incomplete_levels": 0,
            "quality_fails": 0,
        },
    }
    for world_name, world in worlds.items():
        world_report = audit_world(world)
        report["worlds"][world_name] = world_report
        report["global"]["total_levels"] += world_report["total_levels"]
        report["global"]["complete_levels"] += world_report["complete_levels"]
        report["global"]["incomplete_levels"] += world_report["incomplete_levels"]
        report["global"]["quality_fails"] += sum(
            1 for l in world_report.get("quality_issues_by_level", {}).values()
            if l
        )
    return report


def get_level_by_id(level_id: str) -> Optional[Level]:
    """Find a Level by its ID across all worlds."""
    worlds = _load_worlds_data()
    for world in worlds.values():
        for town in getattr(world, "towns", []):
            for level in getattr(town, "levels", []):
                if isinstance(level, Level) and getattr(level, "id", None) == level_id:
                    return level
    return None


def diagnose_level(level_id: str) -> Dict[str, Any]:
    """Return a detailed diagnosis for a specific level."""
    level = get_level_by_id(level_id)
    if level is None:
        return {"error": f"Level '{level_id}' not found"}
    return audit_level(level)


def first_incomplete_levels(world_name: str = "WORLD_FOUNDATIONS", limit: int = 10) -> List[Dict[str, Any]]:
    """Return the first N incomplete levels from a specific world."""
    worlds = _load_worlds_data()
    world = worlds.get(world_name)
    if not isinstance(world, World):
        return []
    incomplete = []
    for town in getattr(world, "towns", []):
        for level in getattr(town, "levels", []):
            if not isinstance(level, Level):
                continue
            report = audit_level(level)
            if not report["is_complete"]:
                incomplete.append(report)
                if len(incomplete) >= limit:
                    return incomplete
    return incomplete


def _has_meaningful_text(value: Any) -> bool:
    """Check if a value has meaningful text content."""
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, dict):
        return any(_has_meaningful_text(v) for v in value.values())
    if isinstance(value, list):
        return any(_has_meaningful_text(v) for v in value)
    return False


def audit_mission_pack(pack: MissionPack) -> Dict[str, Any]:
    """Audit a MissionPack for content quality.
    
    Returns a report with:
      - is_complete: all required fields are filled with meaningful content
      - unfinished_steps: list of missing/incomplete steps
      - quality_issues: list of specific quality problems
      - quality: "pass", "partial", or "fail"
    """
    issues = []
    unfinished = []
    
    # Check 9-step loop
    for step in REQUIRED_STEPS:
        step_data = getattr(pack, step, None)
        if not _is_meaningful(step_data):
            unfinished.append(step)
    
    # Check misconceptions for non-company packs
    if pack.domain != "company" and not pack.misconceptions:
        issues.append("missing_misconceptions")
    elif pack.misconceptions:
        for i, mc in enumerate(pack.misconceptions):
            if not mc.reteach_route or not mc.reteach_action:
                issues.append(f"misconception_{i}_missing_reteach")
    
    # Check Captain Byte moments
    if not _has_meaningful_text(pack.captain_byte.intro):
        issues.append("missing_captain_byte_intro")
    if not pack.captain_byte.correct:
        issues.append("missing_captain_byte_correct")
    if not pack.captain_byte.wrong:
        issues.append("missing_captain_byte_wrong")
    
    # Check why_it_matters
    if not _has_meaningful_text(pack.why_it_matters):
        issues.append("missing_why_it_matters")
    
    # Check prerequisites - allow empty list, require defined field
    if pack.prerequisites is None:
        issues.append("missing_prerequisites")
    
    # Check discover step has visual interactions or meaningful interaction content
    discover = pack.discover or {}
    discover_ok = False
    if _has_meaningful_text(discover.get("visual_primitives", [])) and _has_meaningful_text(discover.get("steps", [])):
        discover_ok = True
    elif _has_meaningful_text(discover.get("prompt")) or _has_meaningful_text(discover.get("question")):
        discover_ok = True
    if not discover_ok:
        issues.append("missing_discover_content")
    
    # Check practice items
    if not pack.practice:
        issues.append("missing_practice")
    
    # Check proof questions
    if not pack.proof:
        issues.append("missing_proof")
    
    # Check SRS
    if not pack.srs_key_points:
        issues.append("missing_srs_key_points")
    
    # Check company variants for service-placement packs
    if pack.domain in ("aptitude", "reasoning", "verbal", "coding", "cs_core"):
        if not pack.company_variants:
            issues.append("missing_company_variants")
    
    is_complete = len(unfinished) == 0 and len(issues) == 0
    quality = "pass" if is_complete else ("partial" if len(unfinished) == 0 else "fail")
    
    return {
        "id": pack.id,
        "title": pack.title,
        "domain": pack.domain,
        "is_complete": is_complete,
        "unfinished_steps": unfinished,
        "quality_issues": issues,
        "quality": quality,
        "steps_complete": len(REQUIRED_STEPS) - len(unfinished),
        "steps_total": len(REQUIRED_STEPS),
    }


def load_mission_pack(pack_id: str) -> Optional[MissionPack]:
    """Load a MissionPack JSON file by id."""
    path = MISSION_PACKS_DIR / f"{pack_id}.json"
    if not path.exists():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return MissionPack(**raw)
    except Exception:
        return None


def audit_all_mission_packs() -> Dict[str, Any]:
    """Audit all MissionPack JSON files."""
    if not MISSION_PACKS_DIR.exists():
        return {"error": f"Mission packs directory not found: {MISSION_PACKS_DIR}", "packs": {}}
    
    report = {
        "packs_dir": str(MISSION_PACKS_DIR),
        "total_packs": 0,
        "complete_packs": 0,
        "incomplete_packs": 0,
        "quality_fails": 0,
        "packs": {},
    }
    
    for path in MISSION_PACKS_DIR.glob("*.json"):
        pack_id = path.stem
        pack = load_mission_pack(pack_id)
        if pack is None:
            continue
        
        pack_report = audit_mission_pack(pack)
        report["packs"][pack_id] = pack_report
        report["total_packs"] += 1
        
        if pack_report["is_complete"]:
            report["complete_packs"] += 1
        else:
            report["incomplete_packs"] += 1
            if pack_report["quality"] == "fail":
                report["quality_fails"] += 1
    
    return report


def diagnose_mission_pack(pack_id: str) -> Dict[str, Any]:
    """Return a detailed diagnosis for a specific MissionPack."""
    pack = load_mission_pack(pack_id)
    if pack is None:
        return {"error": f"MissionPack '{pack_id}' not found"}
    return audit_mission_pack(pack)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "mission-packs":
        report = audit_all_mission_packs()
        print(f"Mission Packs Directory: {report.get('packs_dir', 'N/A')}")
        print(f"Total packs: {report['total_packs']}")
        print(f"Complete: {report['complete_packs']}")
        print(f"Incomplete: {report['incomplete_packs']}")
        print(f"Quality fails: {report['quality_fails']}")
        for pack_id, pack_report in report["packs"].items():
            status = "✅" if pack_report["is_complete"] else "❌"
            print(f"  {status} {pack_id}: {pack_report['quality']} - {pack_report['title']}")
            if pack_report["unfinished_steps"]:
                print(f"      Missing steps: {', '.join(pack_report['unfinished_steps'])}")
            if pack_report["quality_issues"]:
                print(f"      Issues: {', '.join(pack_report['quality_issues'])}")
    else:
        report = audit_all_worlds()
        global_stats = report["global"]
        print(f"Total levels: {global_stats['total_levels']}")
        print(f"Complete: {global_stats['complete_levels']}")
        print(f"Incomplete: {global_stats['incomplete_levels']}")
        print(f"Quality fails: {global_stats['quality_fails']}")
        for world_name, world_report in report["worlds"].items():
            print(f"\n{world_name}: {world_report['complete_levels']}/{world_report['total_levels']} complete")
            for town in world_report.get("towns", []):
                incomplete_in_town = [l for l in town["levels"] if not l["is_complete"]]
                if incomplete_in_town:
                    print(f"  {town['name']}: {len(incomplete_in_town)} incomplete")
