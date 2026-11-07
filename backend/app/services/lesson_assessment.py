"""Server-side lesson assessment grading.

LAW
---
* The client may submit *answers*.
* The client must never submit a trusted *score*.
* Mastery and XP are awarded only when this module says so.
* Hints never grant mastery.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple


def _norm_text(value: Any) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def _grade_mcq(question: dict, answer: Any) -> Tuple[bool, str]:
    """Grade a multiple-choice question by correct_index."""
    try:
        selected = int(answer)
    except (TypeError, ValueError):
        return False, "No option selected."
    correct = question.get("correct_index")
    if correct is None:
        return False, "Question has no answer key on the server."
    ok = selected == int(correct)
    explanation = question.get("explanation") or ("Correct." if ok else "Incorrect.")
    return ok, explanation


def _grade_fill_blank(question: dict, answer: Any) -> Tuple[bool, str]:
    expected = question.get("expected_answer")
    if expected is None:
        return False, "Question has no answer key on the server."
    ok = _norm_text(answer) == _norm_text(expected)
    explanation = question.get("explanation") or ("Correct." if ok else f"Expected: {expected}")
    return ok, explanation


def _grade_order_steps(question: dict, answer: Any) -> Tuple[bool, str]:
    correct_order = question.get("correct_order")
    if not isinstance(correct_order, list):
        return False, "Question has no order key on the server."
    try:
        submitted = [int(x) for x in (answer or [])]
    except (TypeError, ValueError):
        return False, "Invalid order submission."
    ok = submitted == [int(x) for x in correct_order]
    explanation = question.get("explanation") or ("Correct order." if ok else "Order is not correct.")
    return ok, explanation


def grade_question(question: dict, answer: Any) -> Dict[str, Any]:
    """Grade one assessment question. Never trusts client score."""
    qtype = (question.get("type") or question.get("step_type") or "mcq").lower()
    if "correct_index" in question or qtype in {"mcq", "interactive", "practice", "debug_choice"}:
        ok, explanation = _grade_mcq(question, answer)
    elif "expected_answer" in question or qtype in {"fill_blank", "predict_output"}:
        ok, explanation = _grade_fill_blank(question, answer)
    elif "correct_order" in question or qtype == "order_steps":
        ok, explanation = _grade_order_steps(question, answer)
    else:
        ok, explanation = False, "Unsupported question type for server grading."
    return {
        "correct": ok,
        "explanation": explanation,
        "prompt": question.get("prompt") or question.get("title") or "",
    }


def grade_lesson_assessment(
    lesson: dict,
    answers: List[Any],
    *,
    client_claimed_score: Optional[float] = None,
) -> Dict[str, Any]:
    """Grade a full lesson assessment from the lesson JSON definition.

    ``client_claimed_score`` is intentionally ignored for mastery decisions.
    """
    assessment = lesson.get("assessment") or {}
    questions: List[dict] = list(assessment.get("questions") or [])
    if not questions:
        return {
            "ok": False,
            "error": "lesson_has_no_assessment",
            "score": 0.0,
            "mastered": False,
            "details": [],
        }

    details: List[dict] = []
    correct_count = 0
    for index, question in enumerate(questions):
        answer = answers[index] if index < len(answers) else None
        result = grade_question(question, answer)
        if result["correct"]:
            correct_count += 1
        details.append({"index": index, **result})

    total = len(questions)
    score = round(correct_count / total, 4) if total else 0.0
    threshold = float(
        assessment.get("mastery_threshold")
        or lesson.get("mastery_threshold")
        or 0.7
    )
    mastered = score >= threshold

    return {
        "ok": True,
        "score": score,
        "percent": round(score * 100, 1),
        "correct": correct_count,
        "total": total,
        "mastery_threshold": threshold,
        "mastered": mastered,
        "details": details,
        # Explicitly document that client score was not used.
        "client_claimed_score_ignored": client_claimed_score,
        "policy": "server_keys_only",
    }


def progressive_hints(step: dict, hints_used: int) -> Dict[str, Any]:
    """Return the next progressive hint without revealing the full answer."""
    hints = list(step.get("hints") or [])
    if not hints:
        return {"hint": None, "hints_remaining": 0, "exhausted": True}
    idx = max(0, min(int(hints_used), len(hints) - 1))
    remaining = max(0, len(hints) - (hints_used + 1))
    return {
        "hint": hints[idx],
        "hint_index": idx,
        "hints_remaining": remaining,
        "exhausted": remaining == 0,
        "awards_mastery": False,
    }
