"""Verification pipeline shim — delegates to canonical systems.

CANONICAL SYSTEMS (do not duplicate):
- app.services.question_governance (trust states + bank ownership)
- app.services.question_verification (quick_structural_check for Class B)
- app.services.content_promotion (reviewed -> verified promotion)
- backend/scripts/independent_verify.py (independent oracle verification)
- backend/scripts/repair_queue.py (UNVERIFIED triage)

This module exists only as a compatibility import. It performs structural
pre-checks and ALWAYS quarantines LLM-drafted content as UNVERIFIED candidates
in app/content/questions/raw/. It NEVER promotes to TRUSTED/AUTOMATED_CHECKED.
Promotion requires the canonical trust pipeline + human review per AGENTS.md.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def validate_question_structure(q: Dict[str, Any]) -> bool:
    """Lenient pre-check only. Not a trust promotion gate."""
    required = ["title", "description", "difficulty", "hints", "editorial", "test_cases"]
    for f in required:
        if f not in q or not q[f]:
            return False
    hints = q.get("hints")
    if not isinstance(hints, list) or len(hints) < 3:
        return False
    cases = q.get("test_cases")
    if not isinstance(cases, list) or len(cases) < 2:
        return False
    return True


def quarantine_as_candidate(q: Dict[str, Any], candidate_id: str) -> Dict[str, Any]:
    """Wrap an LLM draft as an UNVERIFIED candidate. Never served."""
    return {
        "candidate_id": candidate_id,
        "trust_status": "UNVERIFIED",
        "provenance": "llm_candidate",
        "never_serve": True,
        "title": q.get("title"),
        "description": q.get("description"),
        "difficulty": q.get("difficulty"),
        "hints": q.get("hints"),
        "editorial": q.get("editorial"),
        "test_cases": q.get("test_cases"),
    }


def promote_question(new_q: Dict[str, Any], verified_pool: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Refuse auto-promotion. LLM drafts must go through canonical pipeline.

    Returns None always — callers must route through repair_queue /
    independent_verify / human review. Kept for backward-compat imports.
    """
    return None


def run_pipeline(questions: List[Dict[str, Any]], verified_pool_path: str) -> Dict[str, Any]:
    """No-op guard: never write TRUSTED pools from LLM drafts."""
    raise RuntimeError(
        "verification_pipeline.run_pipeline is disabled. "
        "Use canonical flow: scripts/repair_queue.py -> "
        "scripts/independent_verify.py -> human review -> TRUSTED. "
        f"Refused to write {verified_pool_path}."
    )
