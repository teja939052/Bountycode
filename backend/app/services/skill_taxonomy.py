"""Canonical skill ID normalization layer.

The codebase has multiple, incompatible skill naming schemes:
- adaptive_learning.SKILL_DOMAINS      (arrays_hashing, trees, dp, ...)
- skill_assessment.SKILL_CATEGORIES    (dsa→arrays, aptitude→quantitative, ...)
- readiness_engine.CATEGORY_WEIGHTS    (dsa, aptitude, cs_fundamentals, ...)
- oa.py section names                  (aptitude, logical, verbal, coding, ...)
- interview.py dimension names         (technical, communication, problem_solving, depth)
- spaced_repetition.DSA_CONCEPTS      (arrays, linked-lists, dynamic-programming, ...)

This module establishes a SINGLE canonical ID namespace (domain.subskill)
and provides deterministic mapping functions so every subsystem speaks the
same language. Historical evidence is preserved — sources are mapped TO
canonical IDs, not rewritten in place.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

# ─── Canonical skill ID registry ──────────────────────────────────────────
#
# Format:  domain.subskill
#
# Domains mirror the broad capability areas used across the platform.
# Every ID in this registry is the single source of truth for what
# skill_id values may appear in LearningEvent, skill_graph, repair_mission,
# and readiness records.

CANONICAL_SKILL_DOMAINS: Dict[str, Dict[str, str]] = {
    # ── DSA (coding problem patterns) ──
    "dsa": {
        "arrays": "Arrays",
        "hashing": "Hashing",
        "two_pointers": "Two Pointers",
        "sliding_window": "Sliding Window",
        "stack": "Stack / Monotonic Stack",
        "binary_search": "Binary Search",
        "linked_list": "Linked List",
        "strings": "Strings",
        "trees": "Trees",
        "bst": "Binary Search Trees",
        "tries": "Tries",
        "heap": "Heaps / Priority Queue",
        "graph": "Graphs",
        "bfs": "Breadth-First Search",
        "dfs": "Depth-First Search",
        "dp": "Dynamic Programming",
        "greedy": "Greedy",
        "backtracking": "Backtracking",
        "math_geometry": "Math & Geometry",
        "bit_manipulation": "Bit Manipulation",
        "sorting": "Sorting",
        "searching": "Searching",
        "recursion": "Recursion",
    },
    # ── Programming foundations ──
    "coding": {
        "variables": "Variables & Assignment",
        "types": "Type System",
        "memory_model": "Memory Model",
        "type_checking": "Type Checking",
        "conditions": "Conditions",
        "booleans": "Booleans",
        "loops": "Loops & Iteration",
        "functions": "Functions & Scope",
        "parameters": "Parameters",
        "return": "Return Values",
        "strings": "String Methods",
        "lists": "Lists / Arrays (lang)",
        "dicts": "Dictionaries / Hash Maps",
        "sets": "Sets",
        "data_structures": "Data Structures (lang)",
        "input_output": "Input/Output",
        "error_handling": "Error Handling",
        "exceptions": "Exceptions",
        "json": "JSON Parsing",
        "modules": "Modules & Imports",
        "files": "File I/O",
        "git": "Version Control",
        "debugging": "Debugging",
        "testing": "Testing",
        "http": "HTTP",
        "apis": "API Consumption",
    },
    # ── Aptitude (Indian placement pattern) ──
    "aptitude": {
        "quantitative": "Quantitative Ability",
        "logical": "Logical Reasoning",
        "verbal": "Verbal Ability",
        "data_interpretation": "Data Interpretation",
        "puzzles": "Puzzle Solving",
        "mental_ability": "Mental Ability",
    },
    # ── System design ──
    "system_design": {
        "scalability": "Scalability",
        "requirements_gathering": "Requirements Gathering",
        "high_level_design": "High-Level Design",
        "detailed_design": "Detailed Design",
        "caching": "Caching",
        "databases": "Database Design",
        "load_balancing": "Load Balancing",
        "message_queues": "Message Queues",
        "microservices": "Microservices",
        "trade_offs": "Trade-off Analysis",
        "sql": "SQL Design",
        "nosql": "NoSQL Design",
    },
    # ── Behavioral / soft skills ──
    "behavioral": {
        "leadership": "Leadership",
        "conflict_resolution": "Conflict Resolution",
        "teamwork": "Teamwork",
        "problem_solving": "Problem Solving (behavioral)",
        "communication": "Communication",
        "adaptability": "Adaptability",
        "time_management": "Time Management",
        "customer_focus": "Customer Focus",
        "innovation": "Innovation",
        "ownership": "Ownership",
        "bias_for_action": "Bias for Action",
    },
    # ── Interview-specific competencies ──
    "interview": {
        "technical": "Technical Accuracy",
        "communication": "Communication & Delivery",
        "problem_solving": "Problem Solving Approach",
        "depth": "Answer Depth",
        "explanation": "Explanation Clarity",
        "tradeoff_reasoning": "Trade-off Reasoning",
        "system_design": "System Design Reasoning",
    },
    # ── Resume & career materials ──
    "resume": {
        "content_quality": "Content Quality",
        "ats_optimization": "ATS Optimization",
        "keyword_usage": "Keyword Usage",
        "formatting": "Formatting",
        "impact_statements": "Impact Statements",
        "tailoring": "Role Tailoring",
    },
    # ── Projects ──
    "projects": {
        "architecture": "Architecture",
        "design": "System Design",
        "deployment": "Deployment",
        "testing": "Testing",
        "documentation": "Documentation",
    },
    # ── CS fundamentals ──
    "cs_fundamentals": {
        "operating_systems": "Operating Systems",
        "networking": "Networking",
        "databases": "Databases",
        "oops": "Object-Oriented Programming",
        "sql": "SQL",
        "complexity": "Complexity Analysis",
    },
}


def _build_reverse_index() -> Dict[str, str]:
    """Build {any_name: canonical_id} for all known synonyms."""
    idx: Dict[str, str] = {}
    for domain, skills in CANONICAL_SKILL_DOMAINS.items():
        for sub, label in skills.items():
            canon = f"{domain}.{sub}"
            # The canonical ID itself
            idx[canon] = canon
            # The subskill alone (for backward compat with adaptive_learning)
            idx[sub] = canon
            # The domain alone is NOT mapped (ambiguous) — use explicit mappings below
            # Label variants
            idx[label.lower()] = canon
            idx[label] = canon
            # Common hyphen/underscore aliases
            idx[sub.replace("_", "-")] = canon
            idx[sub.replace("_", "")] = canon
    return idx


_CANONICAL_INDEX: Dict[str, str] = _build_reverse_index()


# ─── Explicit synonym maps for non-canonical source names ──────────────────
#
# These cover inputs from subsystems whose naming doesn't match the
# canonical subskill keys above.

# OA section names → canonical skill IDs (and subskill for OA sub-categories)
OA_SECTION_MAP: Dict[str, str] = {
    "coding": "dsa.arrays",
    "dsa": "dsa.arrays",
    "cs_fundamentals": "cs_fundamentals",
    "aptitude": "aptitude.quantitative",
    "logical": "aptitude.logical",
    "verbal": "aptitude.verbal",
    "behavioral": "behavioral.communication",
    "situational": "behavioral.adaptability",
    # Legacy / alternate names
    "arrays": "dsa.arrays",
    "hashing": "dsa.hashing",
    "two_pointers": "dsa.two_pointers",
    "sliding_window": "dsa.sliding_window",
    "stack": "dsa.stack",
    "binary_search": "dsa.binary_search",
    "linked_list": "dsa.linked_list",
    "trees": "dsa.trees",
    "tries": "dsa.tries",
    "heap": "dsa.heap",
    "graph": "dsa.graph",
    "dp": "dsa.dp",
    "greedy": "dsa.greedy",
    "backtracking": "dsa.backtracking",
    "math_geometry": "dsa.math_geometry",
    "bit_manipulation": "dsa.bit_manipulation",
    "strings": "dsa.strings",
    "sorting": "dsa.sorting",
    "searching": "dsa.searching",
    "recursion": "dsa.recursion",
    "system_design": "system_design.scalability",
    "sql": "cs_fundamentals.sql",
}

# Interview dimension names → canonical skill IDs
INTERVIEW_DIMENSION_MAP: Dict[str, str] = {
    "technical": "interview.technical",
    "communication": "interview.communication",
    "problem_solving": "interview.problem_solving",
    "depth": "interview.depth",
    "explanation": "interview.explanation",
    "tradeoff": "interview.tradeoff_reasoning",
    "system_design": "interview.system_design",
}

# adaptive_learning.SKILL_DOMAINS keys → canonical domain
ADAPTIVE_DOMAIN_MAP: Dict[str, str] = {
    "arrays_hashing": "dsa.arrays",
    "two_pointers": "dsa.two_pointers",
    "sliding_window": "dsa.sliding_window",
    "stack": "dsa.stack",
    "binary_search": "dsa.binary_search",
    "linked_list": "dsa.linked_list",
    "trees": "dsa.trees",
    "tries": "dsa.tries",
    "heap": "dsa.heap",
    "graph": "dsa.graph",
    "dp": "dsa.dp",
    "greedy": "dsa.greedy",
    "backtracking": "dsa.backtracking",
    "math_geometry": "dsa.math_geometry",
    "bit_manipulation": "dsa.bit_manipulation",
    "system_design": "system_design.scalability",
    "behavioral": "behavioral.communication",
    "aptitude": "aptitude.quantitative",
    "sql": "cs_fundamentals.sql",
    "language_c": "coding.variables",
    "language_cpp": "coding.variables",
    "language_java": "coding.variables",
    "language_python": "coding.variables",
}

# readiness_engine.CATEGORY_WEIGHTS → canonical domain
READINESS_CATEGORY_MAP: Dict[str, str] = {
    "dsa": "dsa.arrays",
    "aptitude": "aptitude.quantitative",
    "cs_fundamentals": "cs_fundamentals",
    "coding": "coding.variables",
    "interview": "interview.technical",
    "resume": "resume.content_quality",
    "projects": "projects.architecture",
}

# spaced_repetition.DSA_CONCEPTS → canonical
SPACED_REP_MAP: Dict[str, str] = {
    "arrays": "dsa.arrays",
    "linked-lists": "dsa.linked_list",
    "stacks-queues": "dsa.stack",
    "trees": "dsa.trees",
    "graphs": "dsa.graph",
    "dynamic-programming": "dsa.dp",
    "heaps": "dsa.heap",
    "tries": "dsa.tries",
    "backtracking": "dsa.backtracking",
    "bit-manipulation": "dsa.bit_manipulation",
    "math-geometry": "dsa.math_geometry",
    "sorting": "dsa.sorting",
    "searching": "dsa.searching",
}


# ─── Public API ────────────────────────────────────────────────────────────

def canonical_skill_id(name: Optional[str]) -> Optional[str]:
    """Map any skill name from any subsystem to its canonical ID.

    Returns None if the name cannot be mapped.

    Examples:
        >>> canonical_skill_id("arrays_hashing")
        'dsa.arrays'
        >>> canonical_skill_id("technical")
        'interview.technical'
        >>> canonical_skill_id("aptitude")
        'aptitude.quantitative'
    """
    if not name:
        return None
    key = name.strip()
    # Try exact match in reverse index
    if key in _CANONICAL_INDEX:
        return _CANONICAL_INDEX[key]
    # Try OA section map
    if key in OA_SECTION_MAP:
        return OA_SECTION_MAP[key]
    # Try interview dimension map
    if key in INTERVIEW_DIMENSION_MAP:
        return INTERVIEW_DIMENSION_MAP[key]
    # Try ADAPTIVE_DOMAIN_MAP (handles keys like "arrays_hashing")
    if key in ADAPTIVE_DOMAIN_MAP:
        return ADAPTIVE_DOMAIN_MAP[key]
    # Case-insensitive fallback
    lower = key.lower()
    for canon_name, canon_id in _CANONICAL_INDEX.items():
        if canon_name.lower() == lower:
            return canon_id
    # Try without prefix: "coding.trees" should also work if "trees" maps
    parts = key.split(".", 1)
    if len(parts) == 2 and parts[1] in _CANONICAL_INDEX:
        return _CANONICAL_INDEX[parts[1]]
    # Already canonical-looking?
    if "." in key:
        domain, sub = key.split(".", 1)
        if domain in CANONICAL_SKILL_DOMAINS and sub in CANONICAL_SKILL_DOMAINS[domain]:
            return key
    return None


def normalize_skill_id(name: Optional[str]) -> Optional[str]:
    """Alias for canonical_skill_id — maps any skill name to canonical ID."""
    return canonical_skill_id(name)


def parse_oa_section(section: str) -> str:
    """Map an OA section name to canonical skill ID."""
    return OA_SECTION_MAP.get(section, canonical_skill_id(section) or f"oa.{section}")


def parse_interview_dimension(dimension: str) -> str:
    """Map an interview dimension name to canonical skill ID."""
    return INTERVIEW_DIMENSION_MAP.get(dimension, canonical_skill_id(dimension) or f"interview.{dimension}")


def is_canonical(skill_id: str) -> bool:
    """Check if a skill ID is already in canonical form."""
    if not skill_id or "." not in skill_id:
        return False
    domain, sub = skill_id.split(".", 1)
    return domain in CANONICAL_SKILL_DOMAINS and sub in CANONICAL_SKILL_DOMAINS[domain]


def canonical_domain(skill_id: str) -> Optional[str]:
    """Extract the domain from a canonical skill ID."""
    if not skill_id or "." not in skill_id:
        return None
    return skill_id.split(".", 1)[0]


def canonical_subskill(skill_id: str) -> Optional[str]:
    """Extract the subskill from a canonical skill ID."""
    if not skill_id or "." not in skill_id:
        return None
    return skill_id.split(".", 1)[1]


def all_canonical_ids() -> List[str]:
    """Return all canonical skill IDs."""
    ids = []
    for domain, skills in CANONICAL_SKILL_DOMAINS.items():
        for sub in skills:
            ids.append(f"{domain}.{sub}")
    return ids


def resolve_skill_to_category(skill_id: str) -> str:
    """Map a canonical skill ID to its skill_assessment category.

    Used by record_activity / update_skill_score which store evidence
    under categories like 'dsa', 'aptitude', 'coding'.
    """
    canon = canonical_skill_id(skill_id) or skill_id
    domain = canonical_domain(canon)
    if domain is None:
        return "coding"
    # skill_assessment uses these category names:
    #   dsa, system_design, behavioral, aptitude, resume, coding
    if domain in ("dsa",):
        return "dsa"
    if domain == "system_design":
        return "system_design"
    if domain == "behavioral":
        return "behavioral"
    if domain == "aptitude":
        return "aptitude"
    if domain == "resume":
        return "resume"
    if domain == "coding":
        return "coding"
    if domain == "cs_fundamentals":
        return "cs_fundamentals"
    if domain == "interview":
        return "behavioral"  # interview competencies fold into behavioral category
    if domain == "projects":
        return "coding"
    return "coding"


def resolve_skill_to_competency(skill_id: str) -> str:
    """Map a canonical skill ID to the subskill name used by skill_assessment.

    skill_assessment stores evidence as update_skill_score(user_id, category, sub, score, passed)
    where sub is the key inside the category.
    """
    canon = canonical_skill_id(skill_id) or skill_id
    domain = canonical_domain(canon)
    sub = canonical_subskill(canon) or "general"

    if domain == "dsa":
        # skill_assessment uses: arrays, strings, linked_lists, stacks_queues,
        # trees, graphs, hashing, sorting, searching, dynamic_programming,
        # recursion, greedy, binary_search
        sub_map = {
            "arrays": "arrays",
            "hashing": "hashing",
            "two_pointers": "arrays",
            "sliding_window": "arrays",
            "stack": "stacks_queues",
            "binary_search": "binary_search",
            "linked_list": "linked_lists",
            "strings": "strings",
            "trees": "trees",
            "tries": "tries",
            "heap": "graphs",
            "graph": "graphs",
            "bfs": "graphs",
            "dfs": "graphs",
            "dp": "dynamic_programming",
            "greedy": "greedy",
            "backtracking": "backtracking",
            "math_geometry": "arrays",
            "bit_manipulation": "arrays",
            "sorting": "sorting",
            "searching": "searching",
            "recursion": "recursion",
        }
        return sub_map.get(sub, sub)

    if domain == "aptitude":
        sub_map = {
            "quantitative": "quantitative",
            "logical": "logical_reasoning",
            "verbal": "verbal_ability",
            "data_interpretation": "data_interpretation",
            "puzzles": "puzzles",
            "mental_ability": "mental_ability",
        }
        return sub_map.get(sub, sub)

    if domain == "behavioral":
        return sub if sub in (
            "leadership", "conflict_resolution", "teamwork",
            "problem_solving", "communication", "adaptability",
            "time_management", "customer_focus", "innovation",
            "ownership", "bias_for_action",
        ) else "communication"

    if domain == "coding":
        return sub

    if domain == "cs_fundamentals":
        return sub

    if domain == "system_design":
        return sub if sub in (
            "requirements_gathering", "high_level_design", "detailed_design",
            "scaling", "caching", "databases", "load_balancing",
            "message_queues", "microservices", "trade_offs",
            "sql", "nosql",
        ) else sub

    return sub
