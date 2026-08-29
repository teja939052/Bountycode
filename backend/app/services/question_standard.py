"""Placement Question Standard (PQS).

The "hard product decision" for the question bank: stop advertising 6,000+
mediocre filler questions and instead certify a small, brutally high-quality
role-mapped set. This module defines the standard every *paid* question must
meet, grades any question against it, classifies its purpose, and maps it to
target roles + curriculum skills so the same problem feeds the learning
engine, DSA practice, OA and interview flows (instead of being an isolated
record).

Standard fields (see ``STANDARD_FIELDS``): every certified question should
carry all of them. A question that passes only a few is "bronze" territory
and must not be marketed as premium.
"""

from typing import Dict, Any, List, Optional

# Existence of a question across the four practice purposes.
QUESTION_TYPES = ("learning", "placement", "oa", "interview", "company")

# The 15-field Placement Question Standard checklist.
STANDARD_FIELDS: List[Dict[str, Any]] = [
    {"field": "question", "label": "Clear problem statement", "weight": 10},
    {"field": "constraints", "label": "Explicit constraints", "weight": 8},
    {"field": "input_output", "label": "Input/output specification", "weight": 8},
    {"field": "examples", "label": "Examples", "weight": 8},
    {"field": "edge_cases", "label": "Edge cases", "weight": 6},
    {"field": "difficulty", "label": "Difficulty", "weight": 5},
    {"field": "pattern", "label": "Pattern", "weight": 6},
    {"field": "skill", "label": "Skill being tested", "weight": 6},
    {"field": "placement_relevance", "label": "Placement relevance", "weight": 6},
    {"field": "expected_thinking", "label": "Expected thinking", "weight": 8},
    {"field": "hints", "label": "Hints", "weight": 6},
    {"field": "solution", "label": "Reference solution", "weight": 9},
    {"field": "complexity", "label": "Complexity", "weight": 6},
    {"field": "follow_up", "label": "Follow-up question", "weight": 4},
    {"field": "interview_explanation", "label": "Interview explanation", "weight": 4},
]

FIELD_TOTAL = sum(f["weight"] for f in STANDARD_FIELDS)


# Heuristic field detection on a real question dict. Field names intentionally
# mirror the existing question_store / leetcode_meta conventions so the grader
# works on the live question bank without migration.
def _field_present(q: Dict[str, Any], field: str) -> bool:
    if field == "question":
        return bool(str(q.get("question") or q.get("question_title") or q.get("statement") or "").strip())
    if field == "constraints":
        return bool(q.get("constraints"))
    if field == "input_output":
        return bool(q.get("input_output") or q.get("input_format") or q.get("output_format"))
    if field == "examples":
        return bool(q.get("examples"))
    if field == "edge_cases":
        return bool(q.get("edge_cases"))
    if field == "difficulty":
        return bool(q.get("difficulty"))
    if field == "pattern":
        return bool(q.get("pattern"))
    if field == "skill":
        return bool(q.get("skill") or q.get("skills") or q.get("topic") or q.get("sub_topic"))
    if field == "placement_relevance":
        return bool(q.get("placement_relevance") or q.get("role") or q.get("roles") or q.get("company"))
    if field == "expected_thinking":
        return bool(q.get("expected_thinking") or q.get("thinking"))
    if field == "hints":
        h = q.get("hints")
        return bool(h and (isinstance(h, (list, tuple)) and len(h) > 0))
    if field == "solution":
        s = q.get("solution")
        if isinstance(s, dict):
            return bool(s.get("code") or s.get("explanation"))
        return bool(s)
    if field == "complexity":
        return bool(q.get("complexity") or q.get("expected_time_complexity") or q.get("expected_space_complexity"))
    if field == "follow_up":
        return bool(q.get("follow_up"))
    if field == "interview_explanation":
        return bool(q.get("interview_explanation") or q.get("explanation"))
    return False


def score_against_standard(q: Dict[str, Any]) -> Dict[str, Any]:
    """Grade a question 0-100 against the Placement Question Standard.

    Returns the numeric score plus a per-field breakdown so callers can surface
    exactly what is missing (driving the 'what am I missing?' journey stance).
    """
    present = {f["field"]: _field_present(q, f["field"]) for f in STANDARD_FIELDS}
    earned = sum(f["weight"] for f in STANDARD_FIELDS if present.get(f["field"]))
    score = round((earned / FIELD_TOTAL) * 100)

    return {
        "score": score,
        "total_fields": len(STANDARD_FIELDS),
        "present_fields": sum(1 for v in present.values() if v),
        "missing": [f["label"] for f in STANDARD_FIELDS if not present.get(f["field"])],
        "fields": [
            {"label": f["label"], "weight": f["weight"], "present": present.get(f["field"])}
            for f in STANDARD_FIELDS
        ],
    }


def tier_for_score(score: int) -> str:
    """Classify a question's quality tier.

    - premium : 90+  → certified role-mapped placement question (paid bank)
    - solid   : 60-89 → good, needs a pass to close remaining gaps
    - bronze  : < 60  → filler; must not be marketed as high quality
    """
    if score >= 90:
        return "premium"
    if score >= 60:
        return "solid"
    return "bronze"


def classify_type(q: Dict[str, Any]) -> str:
    """Classify the question's purpose.

    A. learning    → teach the concept
    B. placement   → test the concept
    C. oa          → test speed + correctness (timed, test-cased)
    D. interview   → test reasoning + communication (follow-ups)
    E. company     → test skills relevant to a company's process
    """
    tags = set(q.get("tags") or [])
    qtype = q.get("type") or q.get("question_type") or ""
    if qtype in QUESTION_TYPES:
        return qtype

    if "oa" in tags or ("testcases" in q and "time_limit" in q):
        return "oa"
    if q.get("follow_up") or q.get("interview_explanation") or "interview" in tags:
        return "interview"
    if q.get("company") or q.get("companies") or "company" in tags:
        return "company"
    if q.get("learning"):
        return "learning"
    return "placement"


_ROLE_TOPIC_MAP = {
    "sde": {"dsa", "programming", "algorithms", "algorithm", "system_design", "dbms", "os",
            "operating systems", "networks", "oop", "backend", "arrays", "hashing", "hash",
            "strings", "linked_lists", "linked list", "trees", "tree", "graphs", "graph",
            "dynamic_programming", "dp", "recursion", "stack", "queue", "sorting", "search",
            "binary search", "greedy", "sliding window", "two pointers", "heaps", "bit manipulation"},
    "ai_software_developer": {"llm", "ai", "machine_learning", "ml", "prompt", "rag", "backend",
            "python", "transformers", "embedding", "vector", "agents", "model"},
    "data_analyst": {"sql", "statistics", "data", "visualization", "excel", "pandas", "aptitude",
            "probability", "cleaning", "aggregation", "join", "query"},
    "qa": {"testing", "automation", "qa", "api", "sql", "selenium", "pytest", "bug", "test cases"},
    "frontend": {"frontend", "javascript", "typescript", "react", "html", "css", "dom",
            "web api", "browser", "state"},
    "backend": {"backend", "api", "sql", "nosql", "cache", "redis", "queue", "system_design",
            "os", "operating systems", "networks", "arrays", "database", "auth",
            "rate limiting", "distributed"},
}

# Topics that are hard to misattribute and should always count for SDE/backend.
_GENERIC_DSA_TOPICS = {
    "dsa", "algorithms", "algorithm", "data structures", "programming", "arrays",
    "hashing", "strings", "linked_lists", "trees", "graphs", "dynamic_programming",
    "stack", "queue", "sorting", "search", "greedy", "recursion", "problem solving",
}


def map_roles(q: Dict[str, Any]) -> Dict[str, Any]:
    """Map a question to candidate target roles (from role_engine profiles)
    plus the curriculum skill names the question exercises.

    Uses the question's topic/tags to score affinity to each registered role.
    """
    topic = str(q.get("topic") or "").lower()
    sub = str(q.get("sub_topic") or "").lower()
    tags = {str(t).lower() for t in (q.get("tags") or [])}
    target = str(q.get("role") or "").lower()

    haystack = " ".join([topic, sub, *tags])

    scores: List[Dict[str, Any]] = []
    for role_id, keywords in _ROLE_TOPIC_MAP.items():
        matches = sum(1 for kw in keywords if kw in haystack)
        if matches:
            scores.append({"role": role_id, "affinity": matches})

    # A pure DSA/data-structures topic always implies SDE (and often backend);
    # only add it if nothing already matched to avoid spurious blur.
    if not any(s["role"] == "sde" for s in scores) and topic in _GENERIC_DSA_TOPICS:
        scores.append({"role": "sde", "affinity": 1})

    scores.sort(key=lambda r: r["affinity"], reverse=True)

    from app.services.role_engine.profiles import get_profile

    if target and get_profile(target):
        if not any(s["role"] == target for s in scores):
            scores.insert(0, {"role": target, "affinity": 99})
        else:
            for s in scores:
                if s["role"] == target:
                    s["affinity"] = max(s["affinity"], 99)

    return {
        "roles": scores,
        "skills_tested": _skills_tested(topic, sub, tags),
        "type": classify_type(q),
    }


def _skills_tested(topic: str, sub: str, tags: set) -> List[str]:
    picked: List[str] = []
    if topic:
        picked.append(topic)
    if sub:
        picked.append(sub)
    for t in ("arrays", "hashing", "complexity", "recursion", "linked_lists",
              "trees", "graphs", "dynamic_programming", "sql", "api"):
        if t in tags:
            picked.append(t)
    return picked
