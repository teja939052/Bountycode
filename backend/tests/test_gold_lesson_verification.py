"""Gold lesson runtime/content verification.

Verifies the 11 flagship DSA lessons implement the full 9-step
pedagogical structure and that each step has the required fields
for runtime execution.

Does NOT perform browser rendering tests.
"""
from __future__ import annotations

import sys
import os
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data.worlds_data import WORLD_REGISTRY
from app.content.lesson_definitions import LessonDefinition, LessonStep

GOLD_LESSONS = [
    ("problem_solver", "arrays-1", "Two Pointers"),
    ("problem_solver", "arrays-2", "Sliding Window"),
    ("problem_solver", "arrays-3", "Hash Map Lookup"),
    ("problem_solver", "arrays-4", "Binary Search"),
    ("problem_solver", "arrays-5", "Prefix Sum"),
    ("problem_solver", "trees-1", "DFS"),
    ("problem_solver", "trees-2", "BFS"),
    ("problem_solver", "graphs-1", "Graph Traversal"),
    ("problem_solver", "graphs-2", "Topological Sort"),
    ("problem_solver", "dp-1", "Memoization"),
    ("problem_solver", "dp-2", "Tabulation"),
]

REQUIRED_STEP_FIELDS = {
    "discover": ["step_type", "title", "content"],
    "predict": ["step_type", "title", "question", "options", "explanation"],
    "manipulate": ["step_type", "title", "template", "answer"],
    "build": ["step_type", "title", "function_name", "signature", "description",
              "test_cases", "passing_score", "max_attempts"],
    "break": ["step_type", "title", "content", "question", "options", "explanation"],
    "debug": ["step_type", "title", "content", "buggy_code", "fix_steps",
              "function_name", "signature", "description", "test_cases",
              "passing_score", "max_attempts"],
    "retrieve": ["step_type", "title", "content", "prompt", "answer"],
    "transfer": ["step_type", "title", "function_name", "signature", "description",
                 "test_cases", "passing_score", "max_attempts"],
    "mastery": ["step_type", "title", "function_name", "signature", "description",
                "test_cases", "passing_score", "max_attempts"],
}

EXPECTED_STEP_TYPES = ["discover", "predict", "manipulate", "build", "break",
                       "debug", "retrieve", "transfer", "mastery"]


def validate_step(step: LessonStep, expected_type: str) -> list[str]:
    """Validate a single step has required fields for runtime."""
    errors = []
    step_type = step.step_type

    if step_type != expected_type:
        errors.append(f"Wrong step_type: expected {expected_type}, got {step_type}")
        return errors

    required = REQUIRED_STEP_FIELDS.get(step_type, [])
    for field in required:
        value = getattr(step, field, None)
        if value is None or (isinstance(value, (str, list, dict)) and not value):
            errors.append(f"Missing/empty required field: {field}")

    # Type-specific checks
    if step_type == "predict":
        options = step.options or []
        if not any(opt.get("correct") for opt in options):
            errors.append("Predict step has no correct answer in options")

    if step_type == "build":
        if not step.test_cases:
            errors.append("Build step has no test_cases")
        if step.hidden_tests < 1:
            errors.append(f"Build step has hidden_tests={step.hidden_tests}, expected >= 1")

    if step_type == "debug":
        if not step.buggy_code:
            errors.append("Debug step has no buggy_code")
        if not step.fix_steps:
            errors.append("Debug step has no fix_steps")

    if step_type == "mastery":
        if step.hidden_tests < 3:
            errors.append(f"Mastery step has hidden_tests={step.hidden_tests}, expected >= 3")

    return errors


def validate_lesson(world_id: str, lesson_id: str) -> dict[str, Any]:
    """Validate a single Gold lesson."""
    lesson = None
    world = WORLD_REGISTRY.get(world_id)
    if world is not None:
        for town in world.towns:
            for lvl in town.levels:
                if lvl.id == lesson_id:
                    lesson = lvl.model_dump()
                    break
            if lesson is not None:
                break
    if lesson is None:
        return {
            "lesson_id": lesson_id,
            "found": False,
            "error": "Lesson not found in registry",
            "steps": {},
            "overall": "FAIL",
        }

    step_types_found = {s.step_type for s in lesson.steps}
    missing_steps = [t for t in EXPECTED_STEP_TYPES if t not in step_types_found]

    step_results = {}
    overall_pass = True

    # Map steps by type (some lessons may have multiple of same type)
    steps_by_type = {}
    for step in lesson.steps:
        steps_by_type.setdefault(step.step_type, []).append(step)

    for expected_type in EXPECTED_STEP_TYPES:
        if expected_type not in steps_by_type:
            step_results[expected_type] = {
                "present": False,
                "error": f"Missing step type: {expected_type}",
                "pass": False,
            }
            overall_pass = False
            continue

        step = steps_by_type[expected_type][0]
        errors = validate_step(step, expected_type)
        step_results[expected_type] = {
            "present": True,
            "title": step.title,
            "errors": errors,
            "pass": len(errors) == 0,
        }
        if errors:
            overall_pass = False

    return {
        "lesson_id": lesson_id,
        "title": lesson.title,
        "found": True,
        "missing_steps": missing_steps,
        "steps": step_results,
        "overall": "PASS" if overall_pass else "FAIL",
    }


def main() -> None:
    print("=" * 70)
    print("GOLD LESSON RUNTIME VERIFICATION")
    print("=" * 70)

    results = []
    for world_id, lesson_id, name in GOLD_LESSONS:
        result = validate_lesson(world_id, lesson_id)
        results.append((name, lesson_id, result))

    # Summary
    passed = sum(1 for _, _, r in results if r["overall"] == "PASS")
    failed = sum(1 for _, _, r in results if r["overall"] == "FAIL")

    print(f"\nTotal: {len(results)} lessons")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    # Detailed report
    print("\n" + "=" * 70)
    print("DETAILED REPORT")
    print("=" * 70)

    for name, lesson_id, result in results:
        print(f"\n{'='*70}")
        print(f"Lesson: {name} ({lesson_id})")
        print(f"Overall: {result['overall']}")

        if not result["found"]:
            print(f"  ERROR: {result['error']}")
            continue

        if result["missing_steps"]:
            print(f"  Missing steps: {result['missing_steps']}")

        for step_type, step_data in result["steps"].items():
            status = "[PASS]" if step_data["pass"] else "[FAIL]"
            print(f"  {status} {step_type}: {step_data.get('title', 'N/A')}")
            if step_data["errors"]:
                for err in step_data["errors"]:
                    print(f"      - {err}")

    # Save report
    import json
    report_path = os.path.join(os.path.dirname(__file__), "gold_lesson_verification_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nReport saved to: {report_path}")

    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
