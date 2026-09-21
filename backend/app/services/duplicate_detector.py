"""Duplicate detection for question bank."""
from __future__ import annotations

import hashlib
import logging
import re
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


def normalize(text: str) -> str:
    """Normalize question text for comparison."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fingerprint(question: Dict[str, Any]) -> str:
    """Create a deterministic fingerprint for duplicate detection."""
    q = question.get("question") or question.get("question_text") or ""
    opts = question.get("options", {})
    opt_text = " ".join(str(v) for v in (opts or {}).values())
    blob = normalize(q + " " + opt_text)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


def similarity(a: str, b: str) -> float:
    """Jaccard similarity between two normalized texts."""
    set_a = set(a.split())
    set_b = set(b.split())
    if not set_a and not set_b:
        return 1.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / max(len(union), 1)


def find_duplicates(
    new_questions: List[Dict[str, Any]],
    existing_questions: List[Dict[str, Any]],
    threshold: float = 0.85,
) -> List[Tuple[int, int, float]]:
    """Find duplicates between new and existing questions.

    Returns list of (new_index, existing_index, similarity_score).
    """
    duplicates: List[Tuple[int, int, float]] = []
    for i, nq in enumerate(new_questions):
        nq_norm = normalize(nq.get("question", ""))
        for j, eq in enumerate(existing_questions):
            eq_norm = normalize(eq.get("question", ""))
            sim = similarity(nq_norm, eq_norm)
            if sim >= threshold:
                duplicates.append((i, j, sim))
    return sorted(duplicates, key=lambda x: -x[2])


def dedupe(
    questions: List[Dict[str, Any]], threshold: float = 0.85
) -> List[Dict[str, Any]]:
    """Remove duplicates within a list, keeping the highest-quality variant."""
    seen_fingerprints: Dict[str, Dict[str, Any]] = {}
    result: List[Dict[str, Any]] = []
    for q in questions:
        fp = fingerprint(q)
        if fp in seen_fingerprints:
            continue
        seen_fingerprints[fp] = q
        result.append(q)
    return result
