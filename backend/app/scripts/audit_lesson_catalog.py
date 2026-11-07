"""Audit the interactive lesson catalog for coverage and authoring quality.

Run from the backend directory:
    python app/scripts/audit_lesson_catalog.py
Use --strict to return a non-zero exit code when blocking issues are found.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

BACKEND_ROOT = Path(__file__).resolve().parents[2]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.services.lessons import _DROPPED_DUPLICATES, _LESSONS  # noqa: E402

PLACEHOLDER_MARKERS = (
    "lorem ipsum",
    "example code here",
    "coming soon",
    "todo: add",
    "to be added",
    "placeholder",
)


def audit_catalog(lessons: dict[str, dict]) -> dict[str, Any]:
    """Return deterministic catalog counts and actionable quality findings."""
    issues: list[dict[str, str]] = []
    track_counts: Counter[str] = Counter()
    known_ids = set(lessons)

    for lesson_id, lesson in lessons.items():
        track = str(lesson.get("track") or "unassigned")
        track_counts[track] += 1

        for field in ("title", "description", "difficulty"):
            if not str(lesson.get(field) or "").strip():
                issues.append({
                    "severity": "blocking",
                    "lesson_id": lesson_id,
                    "step_id": "",
                    "code": f"missing_{field}",
                    "message": f"Lesson is missing {field}.",
                })

        steps = lesson.get("steps") or []
        if not steps:
            issues.append({
                "severity": "blocking",
                "lesson_id": lesson_id,
                "step_id": "",
                "code": "missing_steps",
                "message": "Lesson has no learning steps.",
            })

        for prerequisite in lesson.get("prerequisites") or []:
            if prerequisite not in known_ids:
                issues.append({
                    "severity": "blocking",
                    "lesson_id": lesson_id,
                    "step_id": "",
                    "code": "broken_prerequisite",
                    "message": f"Unknown prerequisite: {prerequisite}.",
                })

        for step in steps:
            step_id = str(step.get("id") or "")
            step_type = step.get("type")

            if step_type == "explain":
                if not str(step.get("content") or "").strip():
                    issues.append({
                        "severity": "blocking",
                        "lesson_id": lesson_id,
                        "step_id": step_id,
                        "code": "explain_without_content",
                        "message": "Explanation step has no concept content.",
                    })
                if not str(step.get("explanation") or "").strip():
                    issues.append({
                        "severity": "warning",
                        "lesson_id": lesson_id,
                        "step_id": step_id,
                        "code": "explain_without_explanation",
                        "message": "Explanation step has no teaching explanation.",
                    })
                if not str(step.get("code") or "").strip():
                    issues.append({
                        "severity": "warning",
                        "lesson_id": lesson_id,
                        "step_id": step_id,
                        "code": "explain_without_example",
                        "message": "Explanation step has no code or worked example.",
                    })

            elif step_type == "exercise":
                for field in ("instruction", "solution", "tests"):
                    value = step.get(field)
                    if not value:
                        issues.append({
                            "severity": "blocking",
                            "lesson_id": lesson_id,
                            "step_id": step_id,
                            "code": f"exercise_without_{field}",
                            "message": f"Exercise is missing {field}.",
                        })

            elif step_type == "quiz":
                options = step.get("options") or []
                correct_index = step.get("correctIndex")
                valid_key = (
                    isinstance(correct_index, int)
                    and not isinstance(correct_index, bool)
                    and 0 <= correct_index < len(options)
                )
                if not step.get("question") or len(options) < 2 or not valid_key:
                    issues.append({
                        "severity": "blocking",
                        "lesson_id": lesson_id,
                        "step_id": step_id,
                        "code": "invalid_quiz",
                        "message": "Quiz needs a question, at least two options, and a valid answer key.",
                    })
                if not str(step.get("explanation") or "").strip():
                    issues.append({
                        "severity": "warning",
                        "lesson_id": lesson_id,
                        "step_id": step_id,
                        "code": "quiz_without_explanation",
                        "message": "Quiz has no answer explanation.",
                    })
            else:
                issues.append({
                    "severity": "blocking",
                    "lesson_id": lesson_id,
                    "step_id": step_id,
                    "code": "unknown_step_type",
                    "message": f"Unsupported step type: {step_type!r}.",
                })

            serialized = json.dumps(step, ensure_ascii=False).lower()
            for marker in PLACEHOLDER_MARKERS:
                if marker in serialized:
                    issues.append({
                        "severity": "blocking",
                        "lesson_id": lesson_id,
                        "step_id": step_id,
                        "code": "placeholder_content",
                        "message": f"Possible placeholder marker: {marker}.",
                    })

    issue_counts = Counter(issue["severity"] for issue in issues)
    return {
        "lesson_count": len(lessons),
        "track_counts": dict(sorted(track_counts.items())),
        "issue_count": len(issues),
        "issue_counts": dict(sorted(issue_counts.items())),
        "duplicate_ids_dropped": len(_DROPPED_DUPLICATES),
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="exit 1 when blocking issues exist")
    args = parser.parse_args()

    report = audit_catalog(_LESSONS)
    print(json.dumps(report, indent=2, ensure_ascii=False))

    if report["duplicate_ids_dropped"]:
        return 1
    if args.strict and report["issue_counts"].get("blocking", 0):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
