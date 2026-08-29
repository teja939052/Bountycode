"""Curriculum Connector — connects the Role Curriculum spine to the
Capability World learning experiences via ONE canonical skill identity.

SPINE (user-facing journey):  Role Curriculum (roles -> phases -> modules)
ENGINE (learning experience): Capability Worlds (worlds -> competencies -> missions)

Connection rule (Curriculum 2.0):
  - One skill has ONE canonical ID:  "<category>.<skill>", where <category> and
    <skill> exactly match the SKILL_CATEGORIES vocabulary used by Mastery, SRS,
    Readiness, and the skill_graph collection.
  - The role curriculum references that canonical skill.
  - The capability world teaches that canonical skill.
  - Mastery / SRS / Readiness all read/write that same canonical skill.

This module contains NO new curriculum abstraction. It only maps the existing
two systems onto a shared identity and exposes the connected journey.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from app.data.capability_curriculum import ALL_WORLDS, get_world, get_competency


# ──────────────────────────────────────────────────────────────────
# 1. CANONICAL SKILL IDENTITIES
#    Map every flat capability skill AND every role skill_tree key to a
#    canonical "<category>.<skill>" id that matches SKILL_CATEGORIES.
# ──────────────────────────────────────────────────────────────────

# Capability curriculum skills_taught (flat) -> canonical skill inside category.
# NOTE: every target must be a REAL skill in SKILL_CATEGORIES so Mastery/SRS/
# Readiness actually track it (dsa.*, system_design.*, behavioral.*, coding.*).
CAPABILITY_SKILL_TO_CANONICAL: Dict[str, str] = {
    # --- code_foundations -> coding (Programming Foundations) ---
    "variables": "coding.variables",
    "types": "coding.types",
    "conditions": "coding.conditions",
    "type_conversion": "coding.types",
    "loops": "coding.loops",
    "functions": "coding.functions",
    "strings": "coding.strings",
    "string_methods": "coding.string_methods",
    "data_structures": "coding.data_structures",
    "exceptions": "coding.exceptions",
    "json": "coding.json",
    "modules": "coding.modules",
    "files": "coding.files",
    "input_output": "coding.input_output",
    "error_handling": "coding.error_handling",
    "debugging": "coding.debugging",
    "testing": "coding.testing",
    "git": "coding.git",
    "http": "coding.http",
    "apis": "coding.apis",
    "logging": "coding.debugging",
    "error_analysis": "coding.debugging",
    # --- problem_solver -> dsa ---
    "arrays": "dsa.arrays",
    "searching": "dsa.searching",
    "sorting": "dsa.sorting",
    "linear_search": "dsa.searching",
    "queues": "dsa.stacks_queues",
    "priority_queues": "dsa.stacks_queues",
    "heap": "dsa.greedy",
    "hashing": "dsa.hashing",
    "sets": "dsa.hashing",
    "dictionaries": "dsa.hashing",
    "fuzzy_matching": "dsa.hashing",
    "graphs": "dsa.graphs",
    "bfs": "dsa.graphs",
    "dfs": "dsa.graphs",
    "shortest_path": "dsa.graphs",
    # --- build_systems / work_with_data -> system_design ---
    "caching": "system_design.caching",
    "databases": "system_design.databases",
    "indexes": "system_design.databases",
    "scalability": "system_design.scaling",
    "performance": "system_design.scaling",
    "sql": "system_design.databases",
    "schema_design": "system_design.databases",
    "normalization": "system_design.databases",
    "aggregation": "system_design.databases",
    "joins": "system_design.databases",
    "grouping": "system_design.databases",
    "time_series": "system_design.trade_offs",
    "optimization": "system_design.trade_offs",
    # --- under_pressure / software_engineering -> behavioral + system ---
    "time_management": "behavioral.time_management",
    "problem_solving": "behavioral.problem_solving",
    "requirements_analysis": "system_design.requirements_gathering",
    "assumption_making": "behavioral.problem_solving",
    "communication": "behavioral.communication",
    "branching": "coding.git",
    "merging": "coding.git",
    "conflict_resolution": "behavioral.conflict_resolution",
    # --- hiring_arena -> behavioral ---
    "oa_timing": "behavioral.time_management",
    "problem_selection": "behavioral.problem_solving",
    "stress_management": "behavioral.adaptability",
    "approach_explanation": "behavioral.communication",
    "follow_ups": "behavioral.communication",
}

# Role curriculum skill_tree keys -> canonical "<category>.<skill>".
ROLE_SKILL_TO_CANONICAL: Dict[str, str] = {
    # SDE
    "arrays-hashing": "dsa.hashing",
    "two-pointers-sliding-window": "dsa.sorting",
    "binary-search": "dsa.binary_search",
    "strings": "coding.strings",
    "linked-lists": "dsa.linked_lists",
    "stacks-queues": "dsa.stacks_queues",
    "trees": "dsa.trees",
    "graphs": "dsa.graphs",
    "dynamic-programming": "dsa.dynamic_programming",
    "recursion-backtracking": "dsa.recursion",
    "heap-greedy": "dsa.greedy",
    "system-design": "system_design.high_level_design",
    "dbms": "system_design.databases",
    "oop": "coding.data_structures",
    "networks": "coding.http",
    # Java / SDE domain
    "microservices": "system_design.microservices",
    "api-design": "coding.apis",
    "database": "system_design.databases",
    "design-patterns": "system_design.microservices",
    # DevOps
    "docker": "system_design.scaling",
    "kubernetes": "system_design.scaling",
    "ci-cd": "system_design.scaling",
    "cloud-aws": "system_design.scaling",
    "monitoring": "system_design.trade_offs",
}


def canonical_id(*parts: str) -> str:
    """Return a canonical '<category>.<skill>' string for a given dot-path."""
    return ".".join(p for p in parts if p)


def resolve_capability_skill(skill: str) -> Optional[str]:
    """Resolve a flat capability skill name to its canonical '<cat>.<skill>' id."""
    return CAPABILITY_SKILL_TO_CANONICAL.get(skill)


def resolve_role_skill(skill: str) -> Optional[str]:
    """Resolve a role skill_tree key to its canonical '<cat>.<skill>' id."""
    return ROLE_SKILL_TO_CANONICAL.get(skill)


def canonical_skill_for_competency(competency_id: str) -> List[str]:
    """Return the set of canonical skill ids a capability competency teaches."""
    result = get_competency_with_fallback(competency_id)
    if not result:
        return []
    canon: set[str] = set()
    world_id = result["world_id"]
    for skill in result["skills_taught"]:
        cid = resolve_capability_skill(skill)
        if cid:
            canon.add(cid)
    return sorted(canon)


def get_competency_with_fallback(competency_id: str) -> Optional[Dict]:
    """Get a competency by its short id or '<world>/<id>' form, across all worlds."""
    # Try each world's competencies for a matching id / world-qualified id.
    for wid, world in ALL_WORLDS.items():
        for comp in world.get("competencies", []):
            if comp.get("id") == competency_id or f"{wid}/{comp.get('id')}" == competency_id:
                return {
                    "world_id": wid,
                    "world_title": world.get("title"),
                    "competency_id": comp.get("id"),
                    "competency": comp,
                    "skills_taught": comp.get("skills_taught", []),
                }
    return None


# ──────────────────────────────────────────────────────────────────
# 2. ROLE CURRICULUM SPINE → CAPABILITY WORLD LINKAGE
#    Ordered modules for each role. Each module lists the capability
#    competencies (world/competency) that teach it, in completion order.
# ──────────────────────────────────────────────────────────────────

ROLE_SPINE: Dict[str, List[Dict]] = {
    "sde": [
        {
            "phase": "foundation",
            "module": "Programming Foundations",
            "capability_world": "code_foundations",
            "competencies": [
                "code_foundations/validator",
                "code_foundations/command_processor",
                "code_foundations/api_parser",
                "code_foundations/small_cli",
            ],
        },
        {
            "phase": "core",
            "module": "Problem Solving & DSA",
            "capability_world": "problem_solver",
            "competencies": [
                "problem_solver/delivery_route",
                "problem_solver/support_queue",
                "problem_solver/dedup",
                "problem_solver/social_network",
            ],
        },
        {
            "phase": "core",
            "module": "Software Engineering",
            "capability_world": "software_engineering",
            "competencies": [
                "software_engineering/git_workflow",
                "software_engineering/debugging_mastery",
            ],
        },
        {
            "phase": "advanced",
            "module": "Backend & Data",
            "capability_world": "build_systems",
            "competencies": [
                "build_systems/url_shortener",
                "build_systems/scale_api",
                "work_with_data/payroll_fix",
                "work_with_data/analytics_builder",
            ],
        },
        {
            "phase": "advanced",
            "module": "Under Pressure",
            "capability_world": "under_pressure",
            "competencies": [
                "under_pressure/timed_coding",
                "under_pressure/ambiguous_reqs",
            ],
        },
        {
            "phase": "job-ready",
            "module": "Hiring Arena",
            "capability_world": "hiring_arena",
            "competencies": [
                "hiring_arena/oa_simulation",
                "hiring_arena/interview_prep",
            ],
        },
    ],
}


def get_role_spine(role_id: str = "sde") -> List[Dict]:
    """Return the connected role journey (modules -> capability competencies)."""
    return ROLE_SPINE.get(role_id, ROLE_SPINE["sde"])


def build_role_journey(role_id: str = "sde") -> Dict:
    """Build the full, connected 'Your Path' payload for a role.

    Each input module is expanded with:
      - the capability competencies it teaches (with world id + title)
      - the canonical skill ids those competencies map to
    """
    modules_out = []
    for mod in get_role_spine(role_id):
        competencies = []
        canon_skills: set[str] = set()
        for comp_key in mod["competencies"]:
            comp = get_competency_with_fallback(comp_key)
            if not comp:
                continue
            skills = canonical_skill_for_competency(comp_key)
            canon_skills.update(skills)
            competencies.append({
                "competency_id": comp["competency_id"],
                "title": comp["competency"].get("title"),
                "world_id": comp["world_id"],
                "world_title": comp["world_title"],
                "icon": ALL_WORLDS.get(comp["world_id"], {}).get("icon"),
                "scenario": comp["competency"].get("scenario"),
                "skills_taught": comp["skills_taught"],
                "canonical_skills": sorted(skills),
                "step_count": len(comp["competency"].get("steps", [])),
            })
        modules_out.append({
            "phase": mod["phase"],
            "module": mod["module"],
            "world_id": mod["capability_world"],
            "competencies": competencies,
            "canonical_skills": sorted(canon_skills),
        })
    return {
        "role_id": role_id,
        "modules": modules_out,
        "total_competencies": sum(len(m["competencies"]) for m in modules_out),
        "total_modules": len(modules_out),
    }


# ──────────────────────────────────────────────────────────────────
# 3. MASTERY WRITE-THROUGH
#    When a capability competency step/mission is completed, resolve its
#    canonical skills so the caller can call update_skill_score with the
#    exact (<category>, <skill>) the mastery/SRS/readiness systems key on.
# ──────────────────────────────────────────────────────────────────
def competency_canonical_updates(competency_id: str) -> List[Dict]:
    """Return [{'category': ..., 'skill': ...}] for a competency's canonical skills."""
    result = get_competency_with_fallback(competency_id)
    if not result:
        return []
    seen = set()
    updates = []
    for skill in result["skills_taught"]:
        cid = resolve_capability_skill(skill)
        if not cid or cid in seen:
            continue
        seen.add(cid)
        cat, skill_name = cid.split(".", 1)
        updates.append({"category": cat, "skill": skill_name})
    return updates
