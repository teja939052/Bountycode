"""Lesson Depth Audit — scores lessons on teaching-loop completeness.

The full teaching loop is:
    discover -> manipulate -> predict -> build -> break -> debug -> retrieve -> transfer -> mastery

Each step has quality criteria. This service audits all lessons and reports
which steps are missing or shallow, enabling targeted content improvement.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from app.data.worlds_data import WORLD_REGISTRY

logger = logging.getLogger(__name__)

# The canonical teaching loop order
FULL_LOOP = [
    "discover",
    "manipulate",
    "predict",
    "build",
    "break",
    "debug",
    "retrieve",
    "transfer",
    "mastery",
]

# Steps that require code execution capability
CODE_STEPS = {"build", "debug", "transfer"}


class LessonDepthAuditor:
    """Audit lessons for teaching-loop depth."""

    def audit_lesson(self, lesson: Dict[str, Any]) -> Dict[str, Any]:
        """Audit a single lesson and return a depth report."""
        steps = lesson.get("steps", [])
        step_types = [s.get("step_type") for s in steps]
        present_steps = set(step_types)

        # Check each step's quality
        step_quality: Dict[str, Any] = {}
        for step in steps:
            stype = step.get("step_type")
            step_quality[stype] = self._assess_step_quality(step)

        # Missing steps
        missing = [s for s in FULL_LOOP if s not in present_steps]

        # Depth score (0-100)
        score = self._compute_depth_score(steps, present_steps, step_quality)

        return {
            "lesson_id": lesson.get("id", "unknown"),
            "title": lesson.get("title", ""),
            "world": lesson.get("_world_id", ""),
            "present_steps": list(present_steps),
            "missing_steps": missing,
            "step_quality": step_quality,
            "depth_score": score,
            "grade": self._grade(score),
        }

    def audit_all(self) -> Dict[str, Any]:
        """Audit all lessons across all worlds."""
        lessons = [
            lvl
            for world in WORLD_REGISTRY.values()
            for town in world.towns
            for lvl in town.levels
        ]
        reports: List[Dict[str, Any]] = []
        for lesson in lessons:
            try:
                lesson_dict = lesson.model_dump() if hasattr(lesson, "model_dump") else dict(lesson)
                lesson_dict["_world_id"] = self._find_world_for_lesson(lesson)
                reports.append(self.audit_lesson(lesson_dict))
            except Exception as exc:
                logger.warning("Audit failed for lesson %s: %s", getattr(lesson, "id", "?"), exc)

        # Summary
        if not reports:
            return {"total": 0, "reports": [], "summary": {}}

        scores = [r["depth_score"] for r in reports]
        avg_score = sum(scores) / len(scores)
        full_loop_count = sum(1 for r in reports if len(r["missing_steps"]) == 0)

        return {
            "total": len(reports),
            "average_depth_score": round(avg_score, 1),
            "lessons_with_full_loop": full_loop_count,
            "lessons_needing_work": sum(1 for s in scores if s < 60),
            "reports": sorted(reports, key=lambda r: r["depth_score"]),
        }

    def _assess_step_quality(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the quality of a single step."""
        stype = step.get("step_type", "")
        issues: List[str] = []
        score = 100

        # Common: every step should have content
        if not step.get("content") and not step.get("title"):
            issues.append("Missing content/title")
            score -= 30

        if stype == "discover":
            if not step.get("visual"):
                issues.append("No visual element")
                score -= 10
            if not step.get("interaction"):
                issues.append("No interaction specified")
                score -= 10

        elif stype == "manipulate":
            if not step.get("template"):
                issues.append("No template for manipulation")
                score -= 20

        elif stype == "predict":
            if not step.get("options") or len(step.get("options", [])) < 2:
                issues.append("Predict step needs >= 2 options")
                score -= 20
            if not step.get("explanation"):
                issues.append("No explanation for prediction")
                score -= 10

        elif stype == "build":
            if not step.get("test_cases") or len(step.get("test_cases", [])) < 1:
                issues.append("Build step needs test_cases")
                score -= 30
            if not step.get("function_name") and not step.get("signature"):
                issues.append("No function_name or signature")
                score -= 10

        elif stype == "break":
            if not step.get("question"):
                issues.append("Break step needs a question")
                score -= 20

        elif stype == "debug":
            if not step.get("buggy_code"):
                issues.append("Debug step needs buggy_code")
                score -= 30
            if not step.get("fix_steps"):
                issues.append("No fix_steps provided")
                score -= 10

        elif stype == "retrieve":
            if not step.get("prompt"):
                issues.append("Retrieve step needs a prompt")
                score -= 20

        elif stype == "transfer":
            if not step.get("test_cases") or len(step.get("test_cases", [])) < 1:
                issues.append("Transfer step needs test_cases")
                score -= 20
            if not step.get("context"):
                issues.append("No transfer context provided")
                score -= 10

        elif stype == "mastery":
            if not step.get("test_cases") or len(step.get("test_cases", [])) < 1:
                issues.append("Mastery step needs test_cases")
                score -= 20

        return {
            "score": max(0, score),
            "issues": issues,
            "pass": score >= 60,
        }

    def _compute_depth_score(
        self,
        steps: List[Dict[str, Any]],
        present_steps: set,
        quality: Dict[str, Any],
    ) -> int:
        """Compute overall depth score (0-100)."""
        if not steps:
            return 0

        # Coverage: what fraction of the full loop is present
        coverage = len(present_steps) / len(FULL_LOOP)

        # Quality: average step quality
        if quality:
            avg_quality = sum(q["score"] for q in quality.values()) / len(quality)
        else:
            avg_quality = 0

        # Weighted: 60% coverage, 40% quality
        score = int((coverage * 60) + (avg_quality * 0.4))
        return min(100, max(0, score))

    def _grade(self, score: int) -> str:
        if score >= 85:
            return "A"
        if score >= 70:
            return "B"
        if score >= 55:
            return "C"
        if score >= 40:
            return "D"
        return "F"

    def _find_world_for_lesson(self, lesson: Any) -> str:
        """Find which world a lesson belongs to."""
        lesson_id = getattr(lesson, "id", None)
        if not lesson_id:
            return "unknown"
        for world in WORLD_REGISTRY.values():
            for town in world.towns:
                for l in town.levels:
                    if l.id == lesson_id:
                        return world.id
        return "unknown"
