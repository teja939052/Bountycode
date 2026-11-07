"""
Curriculum Completeness Engine — finalize_curriculum.py

Takes the enriched learning paths and adds the final layers:

1. COMPANY-SPECIFIC MOCK TEST BANKS
   Each company gets a curated set of 12-15 questions from the learning
   objects, organized by their actual OA/interview pattern.
   - Amazon: Debugging MCQ + 2 Coding + Work Simulation
   - Google: Hard Coding + Googliness + System Design
   - Microsoft: 2-3 Coding + Probability + Behavioral
   - TCS: NQT Aptitude + Coding + MCQ

2. MOCK INTERVIEW SCHEDULING
   Generates bookable mock interview slots aligned to each company's
   process flow.

3. PROGRESS TRACKING + MASTERY BADGES
   Each skill area earns a badge when 80%+ coverage and average
   quality_scores.overall >= 75.

4. DIFFICULTY-ADAPTIVE SELECTION
   For each learning path stage, questions are sorted by quality
   score within the difficulty tier so users see the best first.

Output:  app/content/curriculum/final_curriculum.json
         app/content/curriculum/mock_tests.json
"""
import json
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

BACKEND_ROOT = Path(__file__).resolve().parents[2]
LOS_PATH = BACKEND_ROOT / "app" / "content" / "questions" / "curated" / "learning_objects.json"
PATHS_PATH = BACKEND_ROOT / "app" / "content" / "curriculum" / "learning_paths.json"
OUTPUT_PATH = BACKEND_ROOT / "app" / "content" / "curriculum" / "final_curriculum.json"
MOCK_TESTS_PATH = BACKEND_ROOT / "app" / "content" / "curriculum" / "mock_tests.json"

import sys
sys.path.insert(0, str(BACKEND_ROOT / "app"))
from content.curriculum.sde_placement_pack import (
    SDE_SKILL_TREE, COMPANY_BLUEPRINTS, TOTAL_SDE_QUESTIONS_TARGET,
)


# Badge tiers based on coverage % and quality
BADGE_TIERS = [
    {"min_coverage": 100, "min_quality": 80, "name": "Master", "emoji": "🎓"},
    {"min_coverage": 80, "min_quality": 70, "name": "Expert", "emoji": "🏆"},
    {"min_coverage": 60, "min_quality": 60, "name": "Practitioner", "emoji": "📊"},
    {"min_coverage": 40, "min_quality": 50, "name": "Learner", "emoji": "🌱"},
    {"min_coverage": 0, "min_quality": 0, "name": "Apprentice", "emoji": "📚"},
]

# Company-specific mock test configurations
MOCK_TEST_CONFIGS = {
    "amazon": {
        "name": "Amazon SDE Mock Test",
        "description": "Simulates Amazon's online assessment: 4 debugging MCQs + 2 coding problems + Work Simulation",
        "total_questions": 14,
        "time_limit_minutes": 135,
        "sections": [
            {"name": "Debugging MCQ", "type": "mcq", "count": 4, "time_minutes": 20},
            {"name": "Coding Problem 1", "type": "coding", "count": 1, "time_minutes": 45},
            {"name": "Coding Problem 2", "type": "coding", "count": 1, "time_minutes": 45},
            {"name": "Work Simulation", "type": "simulation", "count": 1, "time_minutes": 25},
        ],
        "patterns": ["hash-table", "two-sum", "tree-dfs", "graph-dfs", "sliding-window"],
    },
    "google": {
        "name": "Google SWE Mock Test",
        "description": "Simulates Google's phone screen: 1 hard coding + 1 medium + Googliness behavioral",
        "total_questions": 12,
        "time_limit_minutes": 120,
        "sections": [
            {"name": "Hard Coding", "type": "coding", "count": 1, "time_minutes": 45},
            {"name": "Medium Coding", "type": "coding", "count": 1, "time_minutes": 30},
            {"name": "Googliness Behavioral", "type": "behavioral", "count": 1, "time_minutes": 15},
            {"name": "System Design (Optional)", "type": "design", "count": 1, "time_minutes": 30},
        ],
        "patterns": ["dp-2d", "graph-bfs", "bit-manipulation", "sliding-window", "greedy"],
    },
    "microsoft": {
        "name": "Microsoft SDE Mock Test",
        "description": "Simulates Microsoft's online assessment: 3 coding problems + Probability QnA",
        "total_questions": 12,
        "time_limit_minutes": 100,
        "sections": [
            {"name": "Easy Coding", "type": "coding", "count": 1, "time_minutes": 20},
            {"name": "Medium Coding", "type": "coding", "count": 1, "time_minutes": 35},
            {"name": "Hard Coding", "type": "coding", "count": 1, "time_minutes": 40},
            {"name": "Probability QnA", "type": "theory", "count": 1, "time_minutes": 5},
        ],
        "patterns": ["two-pointers", "tree-dfs", "dp-1d", "binary-search", "stack"],
    },
    "tcs": {
        "name": "TCS NQT Mock Test",
        "description": "Simulates TCS NQT: Aptitude (40 min) + Coding (1 problem, 45 min) + MCQ (10 min)",
        "total_questions": 15,
        "time_limit_minutes": 95,
        "sections": [
            {"name": "Aptitude + Reasoning", "type": "aptitude", "count": 10, "time_minutes": 40},
            {"name": "Verbal Ability", "type": "aptitude", "count": 5, "time_minutes": 20},
            {"name": "Coding Problem", "type": "coding", "count": 1, "time_minutes": 45},
        ],
        "patterns": ["two-sum", "sliding-window", "binary-search", "hash-table", "strings"],
    },
}

# Booking slots for mock interviews (per company)
MOCK_INTERVIEW_SLOTS = {
    "amazon": {"duration_minutes": 60, "slots_per_day": 8, "available_hours": ["09:00", "10:30", "12:00", "14:00", "15:30", "17:00"]},
    "google": {"duration_minutes": 45, "slots_per_day": 12, "available_hours": ["08:00", "09:30", "11:00", "13:00", "14:30", "16:00"]},
    "microsoft": {"duration_minutes": 60, "slots_per_day": 10, "available_hours": ["09:00", "10:30", "12:00", "13:30", "15:00", "16:30"]},
    "tcs": {"duration_minutes": 40, "slots_per_day": 15, "available_hours": ["08:00", "09:00", "10:00", "11:00", "13:00", "14:00"]},
}


def _compute_badge(coverage_pct: float, avg_quality: int) -> dict:
    """Determine the mastery badge for a skill area."""
    for tier in BADGE_TIERS:
        if coverage_pct >= tier["min_coverage"] and avg_quality >= tier["min_quality"]:
            return {"name": tier["name"], "emoji": tier["emoji"]}
    return {"name": "Apprentice", "emoji": "📚"}


def _sort_by_quality(questions: list) -> list:
    """Sort questions by quality score (best first) within each difficulty."""
    return sorted(
        questions,
        key=lambda q: (
            q.get("difficulty", "") != "easy",
            q.get("difficulty", "") != "medium",
            -(q.get("quality_scores", {}).get("overall", 50)),
        ),
    )


def _select_for_mock(questions: list, config: dict) -> list:
    """Select questions for a company mock test based on pattern match."""
    selected = []
    seen_ids = set()

    for pattern in config["patterns"]:
        matches = [q for q in questions if q.get("pattern", "misc") == pattern and q.get("id") not in seen_ids]
        for q in _sort_by_quality(matches):
            if len(selected) >= config["total_questions"]:
                return selected
            selected.append(q)
            seen_ids.add(q.get("id", ""))
            if len(matches) > 3:
                break  # Only take top few per pattern

    # Fill remaining from high-quality questions
    if len(selected) < config["total_questions"]:
        remaining = [q for q in questions if q.get("id") not in seen_ids]
        for q in _sort_by_quality(remaining):
            if len(selected) >= config["total_questions"]:
                break
            selected.append(q)
            seen_ids.add(q.get("id", ""))

    return selected[:config["total_questions"]]


def build_final_curriculum():
    """Build the complete final curriculum with mocks, badges, and scheduling."""
    if not LOS_PATH.exists():
        print(f"[finalize_curriculum] Learning objects not found at {LOS_PATH}")
        return
    if not PATHS_PATH.exists():
        print(f"[finalize_curriculum] Learning paths not found at {PATHS_PATH}")
        return

    with open(LOS_PATH, "r", encoding="utf-8") as f:
        learning_objects = json.load(f)
    with open(PATHS_PATH, "r", encoding="utf-8") as f:
        paths = json.load(f)

    # Build company-specific mock test banks
    mock_tests = {}
    company_to_los = defaultdict(list)
    for lo in learning_objects:
        for comp in lo.get("company", []):
            company_to_los[comp.lower()].append(lo)

    for comp_id, config in MOCK_TEST_CONFIGS.items():
        comp_los = company_to_los.get(comp_id, [])
        if not comp_los:
            # Try to match by pattern from any company
            comp_los = learning_objects[:20]

        selected = _select_for_mock(comp_los, config)

        sections = []
        idx = 0
        for section in config["sections"]:
            section_questions = []
            for _ in range(section["count"]):
                if idx < len(selected):
                    q = selected[idx]
                    section_questions.append({
                        "id": q.get("id"),
                        "title": q["learning_object"].get("title", "")[:60],
                        "pattern": q.get("pattern", "misc"),
                        "difficulty": q.get("difficulty", ""),
                        "type": section["type"],
                    })
                    idx += 1
            sections.append({
                "name": section["name"],
                "type": section["type"],
                "count": section["count"],
                "time_minutes": section["time_minutes"],
                "questions": section_questions,
            })

        mock_tests[comp_id] = {
            "mock_config": {**config, "sections": sections},
            "booking_slots": MOCK_INTERVIEW_SLOTS.get(comp_id, MOCK_INTERVIEW_SLOTS["amazon"]),
            "total_questions": len(selected),
            "patterns_covered": list(set(q.get("pattern", "misc") for q in selected)),
            "avg_quality": round(
                sum(q.get("quality_scores", {}).get("overall", 50) for q in selected) / len(selected), 1
            ) if selected else 0,
        }

    # Add mastery badges + difficulty-adaptive ordering to learning paths
    for skill_id, skill_info in paths["curriculum"].items():
        # Compute coverage + quality for badge
        coverage = skill_info["coverage_percent"]
        all_qs = []
        for stage_name in ("learn", "guided_practice", "placement_practice"):
            all_qs.extend(skill_info["learning_path"][stage_name])

        # We stored only metadata in the learning_path — recompute from learning_objects
        skill_los = [lo for lo in learning_objects if lo.get("learning_object", {}).get("curriculum_skill") == skill_id]
        avg_quality = round(
            sum(lo.get("quality_scores", {}).get("overall", 50) for lo in skill_los) / len(skill_los), 1
        ) if skill_los else 50

        badge = _compute_badge(coverage, avg_quality)
        skill_info["mastery"] = {
            "badge": badge["name"],
            "emoji": badge["emoji"],
            "coverage_percent": coverage,
            "avg_quality_score": avg_quality,
            "questions_authored": len(skill_los),
            "target": skill_info["question_target"],
            "is_complete": coverage >= 100,
        }

        # Re-sort questions within each stage by quality (difficulty-adaptive)
        # We need the actual learning object IDs to map back
        ids_in_path = set()
        for stage_name in ("learn", "guided_practice", "placement_practice"):
            stage = skill_info["learning_path"][stage_name]
            ids_in_path.update(item.get("id") for item in stage if item.get("id"))

        # Re-sort each stage by quality descending
        skill_los_by_id = {lo["id"]: lo for lo in skill_los}
        for stage_name in ("learn", "guided_practice", "placement_practice"):
            stage = skill_info["learning_path"][stage_name]
            stage.sort(key=lambda x: -(skill_los_by_id.get(x.get("id", ""), {}).get("quality_scores", {}).get("overall", 50)))

    # Build progress tracking summary
    total_los = len(learning_objects)
    complete_skills = sum(1 for s in paths["curriculum"].values() if s.get("mastery", {}).get("is_complete", False))
    total_badges = sum(1 for s in paths["curriculum"].values() if s.get("mastery", {}).get("badge") in ("Master", "Expert"))
    avg_quality_all = round(
        sum(lo.get("quality_scores", {}).get("overall", 50) for lo in learning_objects) / total_los, 1
    ) if total_los else 0

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "learning_objects": total_los,
        "sde_pack_target": TOTAL_SDE_QUESTIONS_TARGET,
        "progress_percent": paths["progress_percent"],
        "skill_areas": len(SDE_SKILL_TREE),
        "skills_complete": complete_skills,
        "mastery_badges": total_badges,
        "avg_quality_score": avg_quality_all,
        "curriculum": paths["curriculum"],
        "company_blueprints": paths["company_blueprints"],
        "company_los_mapping": {
            comp: len(los) for comp, los in company_to_los.items()
        },
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    with open(MOCK_TESTS_PATH, "w", encoding="utf-8") as f:
        json.dump(mock_tests, f, indent=2, ensure_ascii=False)

    print(
        f"[finalize_curriculum] Complete — "
        f"learning_objects: {total_los} | "
        f"skills_complete: {complete_skills}/{len(SDE_SKILL_TREE)} | "
        f"mastery_badges: {total_badges} | "
        f"mock_tests: {len(mock_tests)} | "
        f"avg_quality: {avg_quality_all} | "
        f"output: {OUTPUT_PATH}, {MOCK_TESTS_PATH}"
    )


if __name__ == "__main__":
    build_final_curriculum()