"""Deterministic quality checks for authored and generated curriculum content.

This is an authoring gate, not an AI grader: it flags generic placeholders and
missing learning artifacts so generated lesson shells are never mistaken for
finished instruction.
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
)


def _items(content: Dict[str, Any], plural: str, singular: str) -> List[Dict[str, Any]]:
    values = content.get(plural)
    if isinstance(values, list):
        return [item for item in values if isinstance(item, dict)]
    value = content.get(singular)
    return [value] if isinstance(value, dict) else []


def score_lesson_content(content: Dict[str, Any]) -> Dict[str, Any]:
    """Return a transparent 0–100 authoring score and actionable warnings."""
    warnings: List[str] = []
    theory = str(content.get("theory") or "").strip()
    sections = [s for s in (content.get("sections") or []) if isinstance(s, dict)]
    section_bodies = [str(s.get("body") or "").strip() for s in sections]
    code_example = content.get("code_example") or {}
    code = str(code_example.get("code") or "") if isinstance(code_example, dict) else str(code_example)
    exercises = _items(content, "exercises", "exercise")
    quizzes = _items(content, "quizzes", "quiz")
    mistakes = [m for m in (content.get("common_mistakes") or []) if isinstance(m, dict)]

    if len(theory) < 160:
        warnings.append("thin_theory")
    if len(sections) < 3 or sum(len(body) >= 100 for body in section_bodies) < 3:
        warnings.append("thin_explanatory_sections")
    if not code.strip() or any(marker in code.lower() for marker in _PLACEHOLDER_MARKERS):
        warnings.append("placeholder_or_missing_code")
    if len(exercises) < 2:
        warnings.append("insufficient_exercises")
    exercise_text = " ".join(
        str(ex.get("description") or "") + " " + str(ex.get("expected_output") or "")
        for ex in exercises
    ).lower()
    if any(marker in exercise_text for marker in _PLACEHOLDER_MARKERS):
        warnings.append("generic_exercise_expectations")
    if len(quizzes) < 3 or any(
        len(q.get("options") or []) < 2 or len(str(q.get("explanation") or "").strip()) < 35
        for q in quizzes
    ):
        warnings.append("insufficient_assessment_depth")
    if len(mistakes) < 2 or any(
        not str(m.get("mistake") or "").strip()
        or not str(m.get("fix") or "").strip()
        for m in mistakes
    ):
        warnings.append("missing_misconception_guidance")

    score = 100
    penalties = {
        "thin_theory": 15,
        "thin_explanatory_sections": 15,
        "placeholder_or_missing_code": 20,
        "insufficient_exercises": 15,
        "generic_exercise_expectations": 10,
        "insufficient_assessment_depth": 15,
        "missing_misconception_guidance": 10,
    }
    score -= sum(penalties[warning] for warning in warnings)
    score = max(0, score)
    return {
        "score": score,
        "status": "ready" if score >= 85 and not warnings else "needs_authoring",
        "warnings": warnings,
        "counts": {
            "sections": len(sections),
            "exercises": len(exercises),
            "quiz_questions": len(quizzes),
            "common_mistakes": len(mistakes),
        },
    }


def audit_curriculum(language_ids: Iterable[str] | None = None) -> Dict[str, Any]:
    """Audit all lessons in the selected language tracks."""
    from app.data.curriculum import get_all_languages
    from app.data.lesson_content import get_lesson_content

    selected = set(language_ids or [])
    report: Dict[str, Any] = {"total_lessons": 0, "ready_lessons": 0, "by_language": {}, "flagged": []}
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
                elif len(report["flagged"]) < 200:
                    report["flagged"].append({
                        "language": language_id,
                        "lesson_id": lesson.get("id"),
                        "title": lesson.get("title"),
                        **quality,
                    })
        summary["average_score"] = round(sum(scores) / len(scores), 1) if scores else 0.0
        report["by_language"][language_id] = summary
    report["ready_pct"] = round(
        report["ready_lessons"] / report["total_lessons"] * 100, 1
    ) if report["total_lessons"] else 0.0
    return report
