"""Validate tutor trees for structural integrity.

Checks:
- Required nodes exist
- All option targets exist or are terminal ("done")
- All interpolated variables are declared in tree["vars"]
- Every path from start has at least one terminating route
- No unreachable nodes
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

_TUTOR_DIR = Path(__file__).resolve().parent.parent / "backend" / "app" / "data" / "tutor_trees"

_NODE_MOVE_TYPES = {
    "calibrated_question",
    "hint_ladder",
    "re_analogy",
    "decompose",
    "pick_the_truth",
    "teach_back",
    "advance",
}

_TERMINAL_TARGETS = {"done", "advance"}


def _load_json(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _extract_vars(text: Any) -> Set[str]:
    if not isinstance(text, str):
        return set()
    return set(re.findall(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", text))


def _collect_node_vars(node: Dict[str, Any]) -> Set[str]:
    vars_found: Set[str] = set()
    for key in ("say", "title", "description"):
        if key in node:
            vars_found.update(_extract_vars(node[key]))
    for opt in node.get("opts", []):
        if isinstance(opt, dict):
            vars_found.update(_extract_vars(opt.get("t", "")))
    for hint in node.get("hints", []):
        vars_found.update(_extract_vars(hint))
    for card in node.get("cards", []):
        vars_found.update(_extract_vars(card))
    for step in node.get("steps", []):
        vars_found.update(_extract_vars(step))
    return vars_found


def _is_node(key: str, value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    if key in ("id", "atom_id", "concept", "misconception_codes", "vars"):
        return False
    move = value.get("move")
    return move in _NODE_MOVE_TYPES


def _get_nodes(tree: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {k: v for k, v in tree.items() if _is_node(k, v)}


def _get_targets(node: Dict[str, Any]) -> List[str]:
    targets: List[str] = []
    for opt in node.get("opts", []):
        if isinstance(opt, dict):
            to = opt.get("to")
            if to:
                targets.append(to)
    next_node = node.get("next")
    if next_node:
        targets.append(next_node)
    return targets


def _reachable_from(nodes: Dict[str, Dict[str, Any]], start_id: str) -> Set[str]:
    reachable: Set[str] = set()
    stack = [start_id]
    while stack:
        current = stack.pop()
        if current in reachable or current not in nodes:
            continue
        reachable.add(current)
        for target in _get_targets(nodes[current]):
            if target not in _TERMINAL_TARGETS:
                stack.append(target)
    return reachable


def _has_terminating_path(nodes: Dict[str, Dict[str, Any]], node_id: str, visited: Set[str]) -> bool:
    if node_id in _TERMINAL_TARGETS:
        return True
    if node_id not in nodes or node_id in visited:
        return False
    visited.add(node_id)
    node = nodes[node_id]
    targets = _get_targets(node)
    if not targets:
        return node.get("move") in _TERMINAL_MOVES
    return any(_has_terminating_path(nodes, t, visited) for t in targets)


def validate_tree(tree: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    tree_id = tree.get("id", "<unknown>")
    nodes = _get_nodes(tree)

    if not nodes:
        return [f"{tree_id}: no nodes found"]

    if "start" not in nodes:
        errors.append(f"{tree_id}: missing start node")
        return errors

    declared_vars = set(tree.get("vars", []))

    for node_id, node in nodes.items():
        if not isinstance(node, dict):
            errors.append(f"{tree_id}:{node_id} is not a dict")
            continue

        for opt in node.get("opts", []):
            if not isinstance(opt, dict):
                errors.append(f"{tree_id}:{node_id} option is not a dict")
                continue
            to = opt.get("to")
            if to and to not in _TERMINAL_TARGETS and to not in nodes:
                errors.append(f"{tree_id}:{node_id} -> {to} missing target node")

        node_vars = _collect_node_vars(node)
        unknown = node_vars - declared_vars
        for var in unknown:
            errors.append(f"{tree_id}:{node_id} unknown variable {{{var}}} (not in tree vars)")

    reachable = _reachable_from(nodes, "start")
    unreachable = set(nodes.keys()) - reachable
    for node_id in sorted(unreachable):
        errors.append(f"{tree_id}:{node_id} unreachable from start")

    for node_id in nodes:
        if not _has_terminating_path(nodes, node_id, set()):
            errors.append(f"{tree_id}:{node_id} has no terminating path to done/advance")

    return errors


def main() -> int:
    if not _TUTOR_DIR.exists():
        print(f"Tutor trees directory not found: {_TUTOR_DIR}")
        return 1

    all_errors: List[str] = []
    tree_files = sorted(_TUTOR_DIR.glob("*.json"))

    for path in tree_files:
        try:
            tree = _load_json(path)
        except Exception as exc:
            print(f"FAIL {path.name}: load error: {exc}")
            all_errors.append(f"{path.name}: load error")
            continue

        errors = validate_tree(tree)
        if errors:
            print(f"FAIL {path.name}:")
            for err in errors:
                print(f"  - {err}")
            all_errors.extend(errors)
        else:
            print(f"OK   {path.name}")

    if all_errors:
        print(f"\n{len(all_errors)} error(s) found")
        return 1

    print(f"\nAll {len(tree_files)} tutor trees valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
