"""Question verification utilities for Class B aptitude/reasoning/verbal pipeline."""
from __future__ import annotations

import re
import random
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def quick_structural_check(question: Dict[str, Any]) -> List[str]:
    """Return a list of structural issues. Empty list means structurally sound."""
    issues: List[str] = []
    if not question.get("question"):
        issues.append("missing question text")
    if len(question.get("question", "")) < 20:
        issues.append("question text too short")
    opts = question.get("options", {})
    if not isinstance(opts, dict) or len(opts) != 4:
        issues.append("options must have exactly 4 entries A/B/C/D")
    else:
        for key in ("A", "B", "C", "D"):
            if key not in opts or not str(opts[key]).strip():
                issues.append(f"missing/empty option {key}")
    correct = question.get("correct_answer", "").strip().upper()
    if correct not in ("A", "B", "C", "D"):
        issues.append(f"invalid correct_answer: {correct}")
    if not question.get("worked_solution"):
        issues.append("missing worked_solution")
    if not question.get("trick"):
        issues.append("missing trick")
    if not question.get("trap"):
        issues.append("missing trap")
    if not question.get("explanation"):
        issues.append("missing explanation")
    return issues


def estimate_difficulty(question: Dict[str, Any]) -> int:
    """Estimate difficulty 1-10 from structural signals."""
    text = question.get("question", "") + " " + question.get("worked_solution", "")
    steps = len(re.findall(r"\b(step|first|then|next|therefore|thus|hence)\b", text, re.I))
    length = len(text)
    numeric_complexity = len(re.findall(r"\d+", text))
    difficulty = 1
    if length > 200:
        difficulty += 1
    if length > 400:
        difficulty += 1
    if steps >= 3:
        difficulty += 1
    if steps >= 5:
        difficulty += 1
    if numeric_complexity >= 5:
        difficulty += 1
    if numeric_complexity >= 10:
        difficulty += 1
    return min(max(difficulty, 1), 10)


def spot_check(questions: List[Dict[str, Any]], fraction: float = 0.10) -> Dict[str, Any]:
    """Simulate 10% human spot-check. Returns pass/fail for the batch."""
    sample_size = max(1, int(len(questions) * fraction))
    sample = random.sample(questions, min(sample_size, len(questions)))
    passed = 0
    failures: List[Dict[str, Any]] = []
    for q in sample:
        issues = quick_structural_check(q)
        if issues:
            failures.append({"question_id": q.get("question_id"), "issues": issues})
        else:
            passed += 1
    return {
        "sampled": len(sample),
        "passed": passed,
        "failed": len(failures),
        "failures": failures,
        "batch_passed": len(failures) == 0,
    }
