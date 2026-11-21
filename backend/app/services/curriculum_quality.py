"""Deterministic quality checks for authored and generated curriculum content.

The audit understands the repository's real lesson schema (singular exercise/
quiz fields, language-specific authored lesson banks, and code embedded in
sections). It is an authoring gate, not an AI grader.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List


_PLACEHOLDER_MARKERS = (
    "todo:",
    "placeholder",
    "learning about ",
    "implement the concept",
    "your program should",
    "a working program demonstrating",
    "your code here",
    "implement ",
    "add the actual implementation",
    "demonstrate the concept",
)


def _as_items(content: Dict[str, Any], plural: str, singular: str) -> List[Dict[str, Any]]:
    """Accept both the singular hand-authored and plural generated schemas."""
    values = content.get(plural)
    if isinstance(values, list) and values:
        return [item for item in values if isinstance(item, dict)]
    value = content.get(singular)
    if isinstance(value, dict):
        return [value]
    return []


def _contains_placeholder(value: Any) -> bool:
    return any(marker in str(value or "").lower() for marker in _PLACEHOLDER_MARKERS)


def _mistake_is_complete(item: Dict[str, Any]) -> bool:
    mistake = item.get("mistake") or item.get("wrong")
    fix = item.get("fix") or item.get("fixed") or item.get("why")
    return bool(str(mistake or "").strip() and str(fix or "").strip())


def score_lesson_content(content: Dict[str, Any]) -> Dict[str, Any]:
    """Return a transparent 0–100 authoring score and actionable warnings."""
    warnings: List[str] = []
    theory = str(content.get("theory") or "").strip()
    sections = [s for s in (content.get("sections") or []) if isinstance(s, dict)]
    section_bodies = [str(s.get("body") or "").strip() for s in sections]
    code_example = content.get("code_example") or {}
    code = str(code_example.get("code") or "") if isinstance(code_example, dict) else str(code_example)
    section_code = "\n".join(str(s.get("code") or "") for s in sections)
    all_code = "\n".join(part for part in (code, section_code) if part.strip())
    exercises = _as_items(content, "exercises", "exercise")
    quizzes = _as_items(content, "quizzes", "quiz")
    mistakes = [m for m in (content.get("common_mistakes") or []) if isinstance(m, dict)]

    if len(theory) < 240:
        warnings.append("thin_theory")
    if len(sections) < 2 or sum(len(body) >= 100 for body in section_bodies) < 2:
        warnings.append("thin_explanatory_sections")
    if not all_code.strip() or _contains_placeholder(all_code):
        warnings.append("placeholder_or_missing_code")
    if not exercises:
        warnings.append("missing_exercise")
    elif any(
        _contains_placeholder(ex.get("description")) or
        _contains_placeholder(ex.get("expected_output")) or
        not str(ex.get("description") or "").strip()
        for ex in exercises
    ):
        warnings.append("generic_exercise_expectations")
    if not quizzes or any(
        not str(q.get("question") or "").strip()
        or len(q.get("options") or []) < 2
        or q.get("correct") is None
        or len(str(q.get("explanation") or "").strip()) < 35
        for q in quizzes
    ):
        warnings.append("insufficient_assessment_depth")
    if len(mistakes) < 2 or any(not _mistake_is_complete(m) for m in mistakes):
        warnings.append("missing_misconception_guidance")

    penalties = {
        "thin_theory": 15,
        "thin_explanatory_sections": 15,
        "placeholder_or_missing_code": 20,
        "missing_exercise": 15,
        "generic_exercise_expectations": 10,
        "insufficient_assessment_depth": 15,
        "missing_misconception_guidance": 10,
    }
    score = max(0, 100 - sum(penalties[warning] for warning in warnings))
    return {
        "score": score,
        "status": "ready" if not warnings else "needs_authoring",
        "warnings": warnings,
        "counts": {
            "sections": len(sections),
            "exercises": len(exercises),
            "quiz_questions": len(quizzes),
            "common_mistakes": len(mistakes),
            "code_examples": int(bool(all_code.strip())),
        },
    }


def audit_curriculum(language_ids: Iterable[str] | None = None) -> Dict[str, Any]:
    """Audit every configured lesson against the actual language lesson banks."""
    from app.data.curriculum import get_all_languages
    from app.data.lesson_content import get_lesson_content

    selected = set(language_ids or [])
    report: Dict[str, Any] = {
        "total_lessons": 0,
        "ready_lessons": 0,
        "by_language": {},
        "flagged": [],
    }
    for language in get_all_languages():
        language_id = language.get("id")
        if selected and language_id not in selected:
            continue
        summary = {"total": 0, "ready": 0, "average_score": 0.0}
        scores: List[int] = []
        for level in (language.get("levels") or {}).values():
            for lesson in level.get("lessons") or []:
                content = get_lesson_content(
                    language_id,
                    lesson.get("id", ""),
                    lesson.get("title", ""),
                    lesson.get("type", "theory"),
                )
                quality = score_lesson_content(content)
                summary["total"] += 1
                report["total_lessons"] += 1
                scores.append(quality["score"])
                if quality["status"] == "ready":
                    summary["ready"] += 1
                    report["ready_lessons"] += 1
                elif len(report["flagged"]) < 500:
                    report["flagged"].append({
                        "language": language_id,
                        "level_id": level.get("id"),
                        "lesson_id": lesson.get("id"),
                        "title": lesson.get("title"),
                        **quality,
                    })
        summary["average_score"] = round(sum(scores) / len(scores), 1) if scores else 0.0
        report["by_language"][language_id] = summary
    report["ready_pct"] = round(
        report["ready_lessons"] / report["total_lessons"] * 100, 1
    ) if report["total_lessons"] else 0.0
    report["flagged_truncated"] = (
        report["total_lessons"] - report["ready_lessons"] > len(report["flagged"])
    )
    return report
