"""Pattern Pack schema and type definitions.

A Pattern Pack is the canonical unit of learning content for one
placement pattern. It is data-only; rendering is done by the frontend.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Canonical pattern-pack shape
# ---------------------------------------------------------------------------

#: Top-level keys a pattern pack must expose.
PATTERN_PACK_KEYS = {
    "pattern_id",
    "name",
    "emoji",
    "round_id",
    "purpose",
    "prerequisites",
    "misconceptions",
    "teaching",
    "practice",
    "assessment",
    "retention",
    "company_variants",
    "interview_transfer",
}


def empty_pack(pattern_id: str) -> Dict[str, Any]:
    """Return an empty-but-valid pattern pack skeleton."""
    return {
        "pattern_id": pattern_id,
        "name": pattern_id.replace("-", " ").title(),
        "emoji": "📌",
        "round_id": "",
        "purpose": "",
        "prerequisites": [],
        "misconceptions": [],
        "teaching": [],
        "practice": [],
        "assessment": [],
        "retention": [],
        "company_variants": [],
        "interview_transfer": None,
    }
