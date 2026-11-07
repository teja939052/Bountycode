"""
Curriculum Generator — generate_curriculum.py

Transforms the 158 raw learning objects into a structured, LeetCode-style,
end-to-end SDE curriculum. For each of the 18 skill areas:

1. Maps questions to LeetCode-style **pattern tags** (e.g., "two-sum", "binary-search")
2. Organizes them into **difficulty buckets** (Easy → Medium → Hard)
3. Creates a **scaffolded learning path**: Concept → Guided Practice → Placement Practice → Mastery
4. Adds **company-specific OA patterns** (Amazon OA, Google Phone Screen, etc.)
5. Generates stubs for missing questions so the 325-question target is complete

This script does NOT require AI. It derives patterns from question titles/topics
and generates synthetic question stubs for gaps based on the curriculum architecture.

Output:  app/content/curriculum/learning_paths.json
"""
import json
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict

BACKEND_ROOT = Path(__file__).resolve().parents[2]
LOS_PATH = BACKEND_ROOT / "app" / "content" / "questions" / "curated" / "learning_objects.json"
OUTPUT_PATH = BACKEND_ROOT / "app" / "content" / "curriculum" / "learning_paths.json"

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

import sys
sys.path.insert(0, str(BACKEND_ROOT / "app"))
from content.curriculum.sde_placement_pack import SDE_SKILL_TREE, COMPANY_BLUEPRINTS, TOTAL_SDE_QUESTIONS_TARGET

# LeetCode-style canonical patterns mapped by keyword
PATTERN_KEYWORDS = {
    "two-sum": ["two sum", "pair sum", "complement"],
    "binary-search": ["binary search", "find first", "find last", "search insert", "rotated"],
    "sliding-window": ["sliding window", "subarray", "substring", "min size", "longest"],
    "two-pointers": ["two pointers", "reverse", "pair", "sort colors", "remove duplicates"],
    "prefix-sum": ["prefix sum", "running sum", "range sum", "subarray sum"],
    "hash-table": ["hash", "map", "count", "frequency", "anagram", "group anagram"],
    "stack": ["stack", "monotonic", "daily temperature", "min stack", "balanced bracket", "queue"],
    "heap": ["heap", "priority queue", "kth largest", "merge interval", "task schedule"],
    "greedy": ["greedy", "interval", "meeting", "jump game", "gas station", "assign-cookie"],
    "tree-dfs": ["tree", "dfs", "traversal", "inorder", "preorder", "postorder", "lca", "path"],
    "tree-bfs": ["bfs", "level order", "serialize", "deserialize", "zigzag", "right side view"],
    "bst": ["bst", "binary search tree", "validate", "insert", "delete", "successor"],
    "graph-dfs": ["graph", "dfs", "connected component", "clone", "course schedule", "topological"],
    "graph-bfs": ["bfs", "shortest path", "word ladder", "rotting orange"],
    "dp-1d": ["dp", "dynamic programming", "fibonacci", "climb", "coin change", "house"],
    "dp-2d": ["2d", "grid", "dp", "unique path", "edit distance", "longest"],
    "backtracking": ["backtracking", "n-queens", "subset", "permutation", "word search", "sudoku"],
    "union-find": ["union find", "disjoint set", "connected", "number of islands"],
    "bit-manipulation": ["bit", "xor", "and", "or", "shift", "single number"],
    "math": ["math", "prime", "gcd", "lcm", "power", "modulo"],
    "misc": [],
}

# Company-specific OA patterns
COMPANY_OA_PATTERNS = {
    "amazon": {
        "oa": ["Debugging (4 MCQ)", "Coding (2 problems, 90 min)", "Work Simulation"],
        "interview": ["Two Coding Problems", "System Design (SDE2+)", "LP Behavioral"],
        "common_patterns": ["two-sum", "sliding-window", "tree-dfs", "hash-table", "greedy"],
    },
    "google": {
        "oa": ["Hard Coding Problem (120 min)", "Googliness Survey"],
        "interview": ["LeetCode Medium-Hard (2-3 rounds)", "System Design"],
        "common_patterns": ["dp-2d", "graph-bfs", "sliding-window", "bit-manipulation"],
    },
    "microsoft": {
        "oa": ["2-3 Problems (60-90 min)", "Probability/QnA"],
        "interview": ["Live Coding", "Design (SDE2+)", "Behavioral"],
        "common_patterns": ["two-pointers", "tree-dfs", "dp-1d", "binary-search"],
    },
    "tcs": {
        "oa": ["NQT: Aptitude (40) + Coding (1) + MCQ"],
        "interview": ["TR: Project + CS Fundamentals + Coding"],
        "common_patterns": ["sliding-window", "two-sum", "hash-table", "binary-search"],
    },
    "meta": {
        "oa": ["2 Coding Problems"],
        "interview": ["2-3 Coding Rounds", "System Design", "Behavioral"],
        "common_patterns": ["graph-dfs", "dp-1d", "two-pointers", "sliding-window"],
    },
}


def _canonicalize_pattern(question_title: str, topic: str, description: str) -> str:
    """Map a question's text to a LeetCode-style canonical pattern name."""
    combined = (question_title + " " + topic + " " + description).lower()
    for pattern, keywords in PATTERN_KEYWORDS.items():
        for kw in keywords:
            if kw in combined:
                return pattern
    return "misc"


def _difficulty_bucket(difficulty: str) -> str:
    """Map difficulty to a stage in the learning path."""
    d = (difficulty or "").lower().strip()
    if d in ("easy", "simple"):
        return "easy"
    if d in ("hard", "difficult", "expert"):
        return "hard"
    return "medium"


def _stage_for_difficulty(diff_bucket: str, skill_area: str) -> str:
    """Map difficulty to curriculum stage."""
    if diff_bucket == "easy":
        return "learn"
    if diff_bucket == "medium":
        return "practice"
    return "interview"


def _generate_stub(skill_id: str, skill_name: str, diff_bucket: str, index: int) -> dict:
    """Generate a scaffolded stub question for a missing slot."""
    topics = SDE_SKILL_TREE.get(skill_id, {}).get("topics", [])
    pattern = topics[index % len(topics)] if topics else f"{skill_id}-{diff_bucket}"
    examples = {
        "easy": (f"Example: input [1,2,3] → output ...", "Starter problem for {name}."),
        "medium": (f"Example: input with edge case → output ...", "Medium-complexity {name} problem."),
        "hard": (f"Example: large input requiring optimization → output ...", "Hard {name} problem requiring advanced techniques."),
    }
    ex_text, ex_desc = examples.get(diff_bucket, examples["medium"])

    return {
        "type": "coding",
        "company": ["Amazon", "Google"],
        "role": "SDE",
        "difficulty": diff_bucket,
        "topic": skill_name,
        "sub_topic": pattern,
        "question": f"[{diff_bucket.upper()} | {skill_name} | {pattern}] {ex_desc}",
        "options": [],
        "correct_answer": "",
        "explanation": f"This is a scaffolded {diff_bucket} problem for the {skill_name} skill area. It targets the {pattern} pattern.",
        "hints": [
            {"level": 1, "type": "conceptual", "text": f"Start by understanding the constraints of the {pattern.replace('-', ' ')} pattern."},
            {"level": 2, "type": "structural", "text": f"Think about time complexity: what is the naive O(n^2) approach and how can you optimize it?"},
            {"level": 3, "type": "optimization", "text": f"Consider edge cases: empty input, single element, all same values."},
        ],
        "solution": {
            "code": f"# TODO: Implement {pattern.replace('-', ' ')} solution\n# This scaffolds the {diff_bucket} variant of the {skill_name} module.",
            "language": "pseudocode",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
        },
        "frequency": 1,
        "source": f"SDE Pack Scaffold {skill_id}_{diff_bucket}_{index}",
        "submitted_by": "sde-curriculum",
        "upvotes": 0,
        "downvotes": 0,
        "reported": False,
        "id": f"scaffold_{skill_id}_{diff_bucket}_{index:03d}",
        "review_status": "pending_learning_object_review",
        "learning_objective": f"Master {pattern.replace('-', ' ')} within {skill_name}.",
        "source_type": "bountycourse_original",
        "placement_stage": ["learning", "oa", "technical-interview"],
        "skills": [skill_id],
        "roles": ["sde"],
        "learning_object": {
            "id": f"lo_scaffold_{skill_id}_{diff_bucket}_{index:03d}",
            "title": f"{skill_name} — {diff_bucket.title()} [{pattern.replace('-', ' ').title()}]",
            "concept": f"Master {pattern.replace('-', ' ')} within {skill_name}.",
            "predict": f"For this {diff_bucket} problem, identify the core data structure and the naive approach before optimizing.",
            "explanation_steps": [f"This is a scaffolded problem for {skill_name} at {diff_bucket} difficulty."],
            "follow_up": f"What if the constraints doubled? How would you adapt your approach?",
            "interview_question": f"Explain the {pattern.replace('-', ' ')} technique and its complexity.",
            "test_cases": [
                {"input": "edge_case_input()", "expected_output": "expected_output"},
                {"input": "normal_input()", "expected_output": "expected_output"},
            ],
            "srs_interval_days": 1 if diff_bucket == "easy" else 3 if diff_bucket == "medium" else 7,
            "curriculum_skill": skill_id,
            "stages": ["concept", "predict", "guided", "code", "test", "explain", "follow-up", "interview", "mastery", "srs"],
            "difficulty_bucket": diff_bucket,
            "enriched_at": "2026-08-26T00:00:00+00:00",
        },
        "hints": [
            {"level": 1, "type": "conceptual", "text": f"Start by understanding the constraints of the {pattern.replace('-', ' ')} pattern."},
            {"level": 2, "type": "structural", "text": "Think about time complexity: what is the naive O(n^2) approach and how can you optimize it?"},
            {"level": 3, "type": "optimization", "text": "Consider edge cases: empty input, single element, all same values."},
        ],
        "hint_reveal": {
            "mechanism": "bulb",
            "max_level": 3,
            "current_revealed_level": 0,
            "cost_per_reveal": 1,
            "description": "Click the bulb icon to reveal progressive hints.",
        },
    }


def _enrich_existing_lo(lo: dict) -> dict:
    """Enrich an existing learning object with pattern + curriculum metadata."""
    q = dict(lo)
    topic = q.get("topic", "")
    title = q.get("question", "") or q.get("title", "")
    description = q.get("explanation", "") or ""

    canonical_pattern = _canonicalize_pattern(title, topic, description)
    skill_id = q.get("learning_object", {}).get("curriculum_skill", "uncategorized")
    skill_map = {
        "Arrays & Hashing": "arrays-hashing",
        "Binary Search": "binary-search",
        "Linked List": "linked-lists",
        "Trees": "trees",
        "Graphs": "graphs",
        "Dynamic Programming": "dynamic-programming",
        "Two Pointers": "two-pointers-sliding-window",
        "Sliding Window": "two-pointers-sliding-window",
        "Stack": "stacks-queues",
        "Heap / Priority Queue": "heap-greedy",
        "Strings": "strings",
    }
    if skill_id == "uncategorized" and topic in skill_map:
        skill_id = skill_map[topic]

    diff_bucket = _difficulty_bucket(q.get("difficulty", ""))

    # Add canonical pattern to learning object
    q["pattern"] = canonical_pattern
    q["learning_object"]["pattern"] = canonical_pattern
    q["learning_object"]["difficulty_bucket"] = diff_bucket
    q["learning_object"]["curriculum_stage"] = _stage_for_difficulty(diff_bucket, skill_id)

    # Add company OA patterns
    company_pats = {}
    for comp in (q.get("company") or [])[:3]:
        comp_lower = comp.lower()
        if comp_lower in COMPANY_OA_PATTERNS:
            company_pats[comp_lower] = COMPANY_OA_PATTERNS[comp_lower]

    q["learning_object"]["company_oa_patterns"] = company_pats

    # Ensure scaffolded hints exist
    if "hints" in q and q["hints"] and isinstance(q["hints"][0], dict):
        pass  # Already scaffolded
    elif "hints" in q and q["hints"] and isinstance(q["hints"][0], str):
        # Convert string hints to scaffolded format
        scaffolded = []
        for i, hint_text in enumerate(q["hints"]):
            type_map = {0: "conceptual", 1: "structural", 2: "optimization"}
            scaffolded.append({
                "level": i + 1,
                "type": type_map.get(i, "edge_case"),
                "text": hint_text,
            })
        q["hints"] = scaffolded
    else:
        q["hints"] = [
            {"level": 1, "type": "conceptual", "text": "Identify the core constraint in this problem."},
            {"level": 2, "type": "structural", "text": "Consider how you can decompose this into sub-problems."},
            {"level": 3, "type": "optimization", "text": "Think about edge cases and optimization opportunities."},
        ]

    if "hint_reveal" not in q:
        q["hint_reveal"] = {
            "mechanism": "bulb",
            "max_level": max(h["level"] for h in q["hints"]) if q["hints"] else 0,
            "current_revealed_level": 0,
            "cost_per_reveal": 1,
            "description": "Click the bulb icon to reveal progressive hints.",
        }

    return q


def build_curriculum():
    """Build the complete end-to-end curriculum from existing LOs + scaffolds."""
    if not LOS_PATH.exists():
        print(f"[generate_curriculum] Learning objects not found at {LOS_PATH}")
        return

    with open(LOS_PATH, "r", encoding="utf-8") as f:
        raw_los = json.load(f)

    # Enrich existing LOs
    enriched_los = [_enrich_existing_lo(lo) for lo in raw_los]

    # Write enriched LOs back so stubs and downstream scripts see the patterns
    with open(LOS_PATH, "w", encoding="utf-8") as f:
        json.dump(enriched_los, f, indent=2, ensure_ascii=False)

    # Group by skill area
    by_skill = defaultdict(list)
    for lo in enriched_los:
        skill = lo["learning_object"]["curriculum_skill"]
        by_skill[skill].append(lo)

    # For each skill area, ensure the right distribution of difficulties
    # Target: 30% easy, 50% medium, 20% hard (per LeetCode-style progression)
    curriculum = {}

    for skill_id, skill_info in SDE_SKILL_TREE.items():
        existing = by_skill.get(skill_id, [])
        existing_diffs = Counter = {"easy": 0, "medium": 0, "hard": 0}
        for lo in existing:
            db = lo["learning_object"]["difficulty_bucket"]
            if db in existing_diffs:
                existing_diffs[db] += 1

        target = skill_info["question_target"]
        # Distribute new stubs to fill gaps: 30% easy, 50% medium, 20% hard
        easy_target = max(0, round(target * 0.30))
        medium_target = max(0, round(target * 0.50))
        hard_target = max(0, round(target * 0.20))

        stubs = []
        stub_idx = 0
        for diff_bucket, tgt in [("easy", easy_target), ("medium", medium_target), ("hard", hard_target)]:
            have = existing_diffs.get(diff_bucket, 0)
            need = max(0, tgt - have)
            for _ in range(need):
                stubs.append(_generate_stub(skill_id, skill_info["name"], diff_bucket, stub_idx))
                stub_idx += 1

        all_questions = sorted(existing + stubs, key=lambda x: (
            x["learning_object"]["difficulty_bucket"] != "easy",
            x["learning_object"]["difficulty_bucket"] != "medium",
            x.get("id", ""),
        ))

        # Build learning path with stages
        stages = {
            "learn": [q for q in all_questions if q["learning_object"]["difficulty_bucket"] == "easy"],
            "practice": [q for q in all_questions if q["learning_object"]["difficulty_bucket"] == "medium"],
            "interview": [q["learning_object"]["difficulty_bucket"] == "hard" and q or None for q in all_questions if q["learning_object"]["difficulty_bucket"] == "hard"],
            "interview"  : [q for q in all_questions if q["learning_object"]["difficulty_bucket"] == "hard"],
        }

        curriculum[skill_id] = {
            "skill_id": skill_id,
            "name": skill_info["name"],
            "description": skill_info["description"],
            "question_target": target,
            "current_total": len(all_questions),
            "coverage_percent": round(len(all_questions) / target * 100, 1) if target > 0 else 0,
            "difficulty_distribution": {
                "easy": len(stages["learn"]),
                "medium": len(stages["practice"]),
                "hard": len(stages["interview"]),
            },
            "learning_path": {
                "learn": [
                    {
                        "id": q["id"],
                        "title": q["learning_object"]["title"],
                        "pattern": q.get("pattern", "misc"),
                        "hint_count": len(q.get("hints", [])),
                        "test_case_count": len(q["learning_object"].get("test_cases", [])),
                    }
                    for q in stages["learn"]
                ],
                "guided_practice": [
                    {
                        "id": q["id"],
                        "title": q["learning_object"]["title"],
                        "pattern": q.get("pattern", "misc"),
                        "hint_count": len(q.get("hints", [])),
                        "test_case_count": len(q["learning_object"].get("test_cases", [])),
                    }
                    for q in stages["practice"]
                ],
                "placement_practice": [
                    {
                        "id": q["id"],
                        "title": q["learning_object"]["title"],
                        "pattern": q.get("pattern", "misc"),
                        "hint_count": len(q.get("hints", [])),
                        "test_case_count": len(q["learning_object"].get("test_cases", [])),
                    }
                    for q in stages["interview"]
                ],
            },
        }

    # Build company interview blueprints
    company_curricula = {}
    for comp_id, blueprint in COMPANY_BLUEPRINTS.items():
        comp_patterns = COMPANY_OA_PATTERNS.get(comp_id, {})
        # Find existing LOs that match this company's patterns
        matching = []
        for lo in enriched_los:
            lo_patterns = [lo.get("pattern", "misc")]
            if any(p in comp_patterns.get("common_patterns", []) for p in lo_patterns):
                matching.append({
                    "id": lo["id"],
                    "title": lo["learning_object"]["title"],
                    "pattern": lo.get("pattern", "misc"),
                    "difficulty": lo.get("difficulty", ""),
                    "hint_count": len(lo.get("hints", [])),
                })

        company_curricula[comp_id] = {
            "company_id": comp_id,
            "display_name": blueprint["display_name"],
            "oa_pattern": comp_patterns.get("oa", []),
            "interview_pattern": comp_patterns.get("interview_pattern", comp_patterns.get("interview", [])),
            "common_oa_patterns": comp_patterns.get("common_patterns", []),
            "matching_questions": matching[:20],
            "coverage": f"{len(matching)} questions available",
        }

    output = {
        "generated_at": "2026-08-26T00:00:00+00:00",
        "total_questions": len(enriched_los),
        "total_with_stubs": len(enriched_los) + sum(
            max(0, SDE_SKILL_TREE[sid]["question_target"] - len(by_skill.get(sid, [])))
            for sid in SDE_SKILL_TREE
        ),
        "skill_areas": len(SDE_SKILL_TREE),
        "curriculum": curriculum,
        "company_blueprints": company_curricula,
        "sde_pack_target": TOTAL_SDE_QUESTIONS_TARGET,
        "progress_percent": 0,  # Updated below
    }

    total_count = sum(c["current_total"] for c in curriculum.values())
    output["total_questions"] = total_count
    output["progress_percent"] = round(total_count / TOTAL_SDE_QUESTIONS_TARGET * 100, 1)
    print(f"  current_total: {total_count}")
    print(f"  progress_percent: {output['progress_percent']}%")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(
        f"[generate_curriculum] Complete — "
        f"existing enriched: {len(enriched_los)} | "
        f"total with stubs: {total_count} | "
        f"target: {TOTAL_SDE_QUESTIONS_TARGET} | "
        f"progress: {output['progress_percent']}% | "
        f"output: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    build_curriculum()