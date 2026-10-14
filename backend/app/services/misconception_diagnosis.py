"""
Misconception Diagnosis - canonical entrypoint for misconception detection.

Consumes:
  - app.services.domain_misconceptions  (domain-specific misconception libraries)

Exports:
  - diagnose_misconception(...)
  - get_reteach_plan(...)
  - get_domain_library(...)
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.services.domain_misconceptions import (
    BEHAVIORAL_MISCONCEPTIONS,
    APTITUDE_MISCONCEPTIONS,
    REASONING_MISCONCEPTIONS,
    VERBAL_MISCONCEPTIONS,
    CODING_MISCONCEPTIONS,
    SQL_MISCONCEPTIONS,
    CS_CORE_MISCONCEPTIONS,
    SYSTEM_DESIGN_MISCONCEPTIONS,
    RETEACH_ROUTE_MAP,
    get_domain_library,
    get_reteach_plan,
)


def _concept_to_domain(concept: str) -> str:
    text = (concept or "").lower()
    if text.startswith("behavioral") or text.startswith("behavior"):
        return "behavioral"
    if text.startswith("system_design") or text.startswith("system"):
        return "system_design"
    if text.startswith("aptitude"):
        return "aptitude"
    if text.startswith("reasoning"):
        return "reasoning"
    if text.startswith("verbal"):
        return "verbal"
    if text.startswith("sql"):
        return "sql"
    if text.startswith("cs_core"):
        return "cs_core"
    return "coding"


def _codes_for_concept(concept: str, domain: str) -> List[str]:
    library = get_domain_library(domain)
    by_concept = library.get("by_concept", {})
    return by_concept.get(concept, [])


def _match_action_trace(
    action_trace: List[Dict[str, Any]],
    misconception_codes: List[str],
) -> Optional[str]:
    for entry in action_trace:
        action_type = str(entry.get("type", "")).lower()
        data = entry.get("data", {}) or {}
        text = " ".join(str(v) for v in data.values() if v is not None).lower()
        for code in misconception_codes:
            lib = _get_lib_for_code(code)
            if not lib:
                continue
            sig = lib.get(code, {})
            keywords = [str(k).lower() for k in sig.get("keywords", [])]
            patterns = [str(p).lower() for p in sig.get("interaction_patterns", [])]
            if any(kw in text for kw in keywords) or any(p in action_type for p in patterns):
                return code
    return None


def _get_lib_for_code(code: str) -> Optional[Dict[str, Dict[str, Any]]]:
    for lib in (
        CODING_MISCONCEPTIONS,
        BEHAVIORAL_MISCONCEPTIONS,
        SYSTEM_DESIGN_MISCONCEPTIONS,
        APTITUDE_MISCONCEPTIONS,
        REASONING_MISCONCEPTIONS,
        VERBAL_MISCONCEPTIONS,
        SQL_MISCONCEPTIONS,
        CS_CORE_MISCONCEPTIONS,
    ):
        if code in lib:
            return lib
    return None


def diagnose_misconception(
    action_trace: List[Dict[str, Any]],
    concept: str,
    misconception_codes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Diagnose likely misconception from action trace.

    Confidence is evidence-based:
      - 1 matching occurrence  → low confidence (0.3)
      - 2 matching occurrences → medium confidence (0.6)
      - 3+ matching occurrences → high confidence (0.85)

    Returns:
      {
        "misconception_code": Optional[str],
        "confidence": float,
        "evidence_count": int,
        "reteach_route": Optional[str],
        "reteach_action": Optional[str],
      }
    """
    domain = _concept_to_domain(concept)
    codes = misconception_codes or _codes_for_concept(concept, domain)
    matched = _match_action_trace(action_trace, codes)

    result: Dict[str, Any] = {
        "misconception_code": matched,
        "confidence": 0.0,
        "evidence_count": 0,
        "reteach_route": None,
        "reteach_action": None,
    }

    if matched:
        evidence_count = sum(
            1 for entry in action_trace
            for code in [matched]
            if _entry_matches_code(entry, code)
        )
        confidence = min(0.85, 0.35 * evidence_count)
        lib = _get_lib_for_code(matched) or {}
        sig = lib.get(matched, {})
        route = sig.get("reteach_route")
        plan = get_reteach_plan(matched) if route else None
        result["confidence"] = confidence
        result["evidence_count"] = evidence_count
        result["reteach_route"] = route
        result["reteach_action"] = (plan or {}).get("teacher_focus") or sig.get("reteach_action")

    return result


def _entry_matches_code(entry: Dict[str, Any], code: str) -> bool:
    """Check if a single action trace entry matches a misconception code."""
    lib = _get_lib_for_code(code)
    if not lib:
        return False
    sig = lib.get(code, {})
    keywords = [str(k).lower() for k in sig.get("keywords", [])]
    patterns = [str(p).lower() for p in sig.get("interaction_patterns", [])]
    action_type = str(entry.get("type", "")).lower()
    data = entry.get("data", {}) or {}
    text = " ".join(str(v) for v in data.values() if v is not None).lower()
    return any(kw in text for kw in keywords) or any(p in action_type for p in patterns)
