"""Deterministic prerequisite-aware learning plans.

The graph is deliberately explicit and conservative: missing evidence is
"not_assessed", never silently treated as mastery. Evidence must be supplied
by a trusted server-side assessment aggregator.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Set


MASTERY_THRESHOLD = 70.0
MIN_INDEPENDENT_ATTEMPTS = 3

SKILL_PREREQUISITES: Dict[str, Dict[str, Any]] = {
    # Foundational nodes are explicit leaves so graph validation can detect
    # misspelled references instead of treating every unknown node as a root.
    "coding.variables": {"title": "Variables and assignment", "prerequisites": []},
    "coding.types": {"title": "Data types", "prerequisites": []},
    "coding.conditions": {"title": "Conditions and Boolean logic", "prerequisites": []},
    "cs_fundamentals.databases": {"title": "Database fundamentals", "prerequisites": []},
    "system_design.caching": {"title": "Caching fundamentals", "prerequisites": []},
    "coding.functions": {
        "title": "Functions and scope",
        "prerequisites": ["coding.variables", "coding.types", "coding.conditions"],
    },
    "coding.parameters": {
        "title": "Function parameters",
        "prerequisites": ["coding.variables", "coding.types"],
    },
    "coding.return": {
        "title": "Return values",
        "prerequisites": ["coding.functions", "coding.conditions"],
    },
    "coding.loops": {
        "title": "Loops and iteration",
        "prerequisites": ["coding.variables", "coding.conditions"],
    },
    "coding.lists": {
        "title": "Lists and arrays",
        "prerequisites": ["coding.loops", "coding.variables"],
    },
    "dsa.recursion": {
        "title": "Recursion",
        "prerequisites": [
            "coding.functions",
            "coding.parameters",
            "coding.return",
            "coding.conditions",
        ],
    },
    "dsa.backtracking": {
        "title": "Backtracking",
        "prerequisites": ["dsa.recursion", "coding.conditions"],
    },
    "dsa.arrays": {
        "title": "Arrays",
        "prerequisites": ["coding.loops", "coding.variables"],
    },
    "dsa.trees": {
        "title": "Trees",
        "prerequisites": ["dsa.recursion", "dsa.arrays"],
    },
    "dsa.graph": {
        "title": "Graph fundamentals",
        "prerequisites": ["dsa.trees", "dsa.arrays"],
    },
    "dsa.bfs": {
        "title": "Breadth-first search",
        "prerequisites": ["dsa.graph"],
    },
    "dsa.dfs": {
        "title": "Depth-first search",
        "prerequisites": ["dsa.graph", "dsa.recursion"],
    },
    "dsa.dp": {
        "title": "Dynamic programming",
        "prerequisites": ["dsa.recursion", "dsa.arrays"],
    },
    "cs_fundamentals.complexity": {
        "title": "Complexity analysis",
        "prerequisites": ["coding.loops", "dsa.arrays"],
    },
    "system_design.scalability": {
        "title": "Scalability",
        "prerequisites": ["cs_fundamentals.databases", "system_design.caching"],
    },
}


def validate_prerequisite_graph(
    graph: Mapping[str, Mapping[str, Any]] = SKILL_PREREQUISITES,
) -> List[str]:
    """Return graph integrity errors (unknown references and dependency cycles)."""
    errors: List[str] = []
    for skill, definition in graph.items():
        for prerequisite in definition.get("prerequisites", []):
            if prerequisite not in graph:
                errors.append(f"{skill} references unknown prerequisite {prerequisite}")

    visiting: Set[str] = set()
    visited: Set[str] = set()

    def visit(skill: str, trail: List[str]) -> None:
        if skill in visiting:
            errors.append("dependency cycle: " + " -> ".join(trail + [skill]))
            return
        if skill in visited:
            return
        visiting.add(skill)
        for prerequisite in graph.get(skill, {}).get("prerequisites", []):
            if prerequisite in graph:
                visit(prerequisite, trail + [skill])
        visiting.remove(skill)
        visited.add(skill)

    for skill in graph:
        visit(skill, [])
    return errors


def _ordered_prerequisites(target_skill_id: str) -> List[str]:
    ordered: List[str] = []
    visited: Set[str] = set()

    def visit(skill: str) -> None:
        for prerequisite in SKILL_PREREQUISITES.get(skill, {}).get("prerequisites", []):
            if prerequisite in visited:
                continue
            visit(prerequisite)
            visited.add(prerequisite)
            ordered.append(prerequisite)

    visit(target_skill_id)
    return ordered


def build_prerequisite_plan(
    target_skill_id: str,
    evidence: Mapping[str, Mapping[str, Any]] | None = None,
    *,
    mastery_threshold: float = MASTERY_THRESHOLD,
    min_attempts: int = MIN_INDEPENDENT_ATTEMPTS,
) -> Dict[str, Any]:
    """Explain whether a target can be taught and what to assess or repair first.

    Evidence shape: {canonical_skill_id: {score, total_attempts}}.
    Unassessed prerequisites are surfaced for diagnostics; they are not
    represented as known weaknesses.
    """
    definition = SKILL_PREREQUISITES.get(target_skill_id)
    if not definition:
        return {
            "target_skill_id": target_skill_id,
            "target_title": target_skill_id,
            "status": "unknown_skill",
            "prerequisites": [],
            "next_action": "map_curriculum_skill",
        }

    evidence = evidence or {}
    items: List[Dict[str, Any]] = []
    for skill_id in _ordered_prerequisites(target_skill_id):
        item = evidence.get(skill_id) or {}
        attempts = max(0, int(item.get("total_attempts", 0) or 0))
        score = float(item.get("score", 0) or 0)
        if attempts < min_attempts:
            status = "not_assessed"
        elif score < mastery_threshold:
            status = "needs_review"
        else:
            status = "ready"
        items.append({
            "skill_id": skill_id,
            "title": SKILL_PREREQUISITES[skill_id]["title"],
            "status": status,
            "score": round(score, 1) if attempts else None,
            "attempts": attempts,
        })

    blockers = [item for item in items if item["status"] != "ready"]
    if any(item["status"] == "needs_review" for item in blockers):
        next_action = "teach_and_reassess"
        status = "prerequisite_gap"
    elif blockers:
        next_action = "diagnostic_assessment"
        status = "prerequisites_unassessed"
    else:
        next_action = "teach_target"
        status = "ready"

    return {
        "target_skill_id": target_skill_id,
        "target_title": definition["title"],
        "status": status,
        "next_action": next_action,
        "mastery_threshold": mastery_threshold,
        "minimum_independent_attempts": min_attempts,
        "prerequisites": items,
        "blockers": [item["skill_id"] for item in blockers],
    }
