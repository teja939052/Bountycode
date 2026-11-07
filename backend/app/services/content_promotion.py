"""Content promotion: verified-only promotion from review queue."""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from app.services.class_b_generator import ClassBQuestion
from app.services.question_verification import quick_structural_check, estimate_difficulty

logger = logging.getLogger(__name__)

# Reviewer identities that can never satisfy the human-review gate (A4).
_PIPELINE_REVIEWER_TOKENS = {"", "class_b_pipeline", "pipeline", "system", "auto", "mock", "none"}


def _human_review_evidence(q: ClassBQuestion) -> Optional[Dict[str, Any]]:
    """Return the recorded human-review evidence, or None.

    Human review is recorded in metadata.human_review as
    {reviewer, reviewed_at, notes?} by an actual review step. Machine
    verification output (verification dict, mock flags, quality scores) is
    NEVER accepted as review evidence.
    """
    try:
        meta = q.metadata or {}
    except Exception:
        return None
    hr = meta.get("human_review")
    if not isinstance(hr, dict):
        return None
    if not hr.get("reviewer") or not hr.get("reviewed_at"):
        return None
    return hr


def promote_questions(
    questions: List[ClassBQuestion],
    reviewer_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Promote human-reviewed questions to the verified pool.

    Hard gates (A4, 2026-09-10) — ALL must hold, else the item is rejected:
      1. q.trust_status == "reviewed" (set only by a human review step;
         machine verify paths now emit automated_checked at best).
      2. reviewer_id present, not a pipeline/system token.
      3. metadata.human_review evidence {reviewer, reviewed_at} present and
         its reviewer matches reviewer_id.

    Returns promotion report. Nothing is auto-promoted.
    """
    promoted: List[Dict[str, Any]] = []
    rejected: List[Dict[str, Any]] = []

    reviewer = (reviewer_id or "").strip()
    reviewer_ok = reviewer.lower() not in _PIPELINE_REVIEWER_TOKENS

    for q in questions:
        if q.trust_status != "reviewed":
            rejected.append({
                "question_id": q.question_id,
                "reason": f"not human-reviewed (status={q.trust_status})",
            })
            continue

        if not reviewer_ok:
            rejected.append({
                "question_id": q.question_id,
                "reason": "human reviewer identity required (pipeline/system identities rejected)",
            })
            continue

        hr = _human_review_evidence(q)
        if hr is None or str(hr.get("reviewer", "")).strip() != reviewer:
            rejected.append({
                "question_id": q.question_id,
                "reason": "missing or mismatched human-review evidence (metadata.human_review {reviewer, reviewed_at})",
            })
            continue

        issues = quick_structural_check(q.to_dict())
        if issues:
            rejected.append({
                "question_id": q.question_id,
                "reason": f"structural issues: {issues}",
            })
            continue

        entry = q.to_dict()
        entry["trust_status"] = "verified"
        entry["verified_at"] = datetime.now(timezone.utc).isoformat()
        entry["verified_by"] = reviewer
        entry["content_version"] = 1
        entry.setdefault("difficulty", estimate_difficulty(q.to_dict()))
        promoted.append(entry)

    report = {
        "promoted": len(promoted),
        "rejected": len(rejected),
        "promoted_ids": [e["question_id"] for e in promoted],
        "rejected_ids": [e["question_id"] for e in rejected],
        "rejection_reasons": rejected,
    }
    return report
