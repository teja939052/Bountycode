"""
Learning Object Enrichment Engine — enrich_learning_objects.py

Transforms the 158 fully-authored curated questions into structured
learning objects. Each learning object follows the pedagogical loop:

    CONCEPT → PREDICT → GUIDED → CODE → TEST → EXPLAIN
    → FOLLOW-UP → INTERVIEW → MASTERY → SRS

This is NOT a regeneration step. It reads the existing curated.json,
enriches fully-authored questions with structured metadata, and writes
the result to learning_objects.json. Questions that are NOT fully authored
remain in curated.json and are not touched.

Output:  app/content/questions/curated/learning_objects.json
"""
import json
from pathlib import Path
from datetime import datetime, timezone

BACKEND_ROOT = Path(__file__).resolve().parents[2]
CURATED_PATH = BACKEND_ROOT / "app" / "content" / "questions" / "curated" / "curated.json"
OUTPUT_PATH = BACKEND_ROOT / "app" / "content" / "questions" / "curated" / "learning_objects.json"

LEARNING_LOOP_STAGES = [
    "concept",
    "predict",
    "guided",
    "code",
    "test",
    "explain",
    "follow-up",
    "interview",
    "mastery",
    "srs",
]

# Map each topic to its skill tree entry for curriculum alignment
TOPIC_TO_SKILL = {
    "Arrays & Hashing": "arrays-hashing",
    "Two Pointers & Sliding Window": "two-pointers-sliding-window",
    "Binary Search": "binary-search",
    "Linked List": "linked-lists",
    "Stack & Queue": "stacks-queues",
    "Trees": "trees",
    "Graphs": "graphs",
    "Dynamic Programming": "dynamic-programming",
    "Recursion & Backtracking": "recursion-backtracking",
    "Heap & Greedy": "heap-greedy",
    "Strings": "strings",
    "SQL": "sql",
    "DBMS": "dbms",
    "OS": "os",
    "Networks": "networks",
    "OOP": "oop",
    "System Design": "system-design",
    "Programming Fundamentals": "programming-fundamentals",
}


def _is_fully_authored(q: dict) -> bool:
    """A question is fully authored if it has an explanation + solution/hints."""
    return bool(q.get("explanation")) and (
        bool(q.get("solution")) or bool(q.get("correct_answer")) or bool(q.get("hints"))
    )


def _extract_concept(q: dict) -> str:
    """Derive a concise concept statement from the question."""
    topic = q.get("topic", "")
    pattern = q.get("pattern", "")
    objective = q.get("learning_objective", "")
    if objective:
        return objective
    if pattern and pattern != "general-concept":
        return f"Apply {pattern} pattern to solve this {topic} problem."
    return f"Apply {topic} concepts to solve this placement problem."


def _extract_predict_prompt(q: dict) -> str:
    """Generate a PREDICT prompt — what should the user think before coding."""
    text = q.get("question", "") or q.get("description", "") or ""
    return f"Before writing code, identify the core constraint in this problem. What is the naive O(n^2) approach, and how can you reduce it?"


def _derive_follow_up(q: dict) -> str:
    """Generate a follow-up challenge that extends the base problem."""
    topic = q.get("topic", "")
    if "Binary Search" in topic:
        return "What changes if the array contains duplicates? Can you still use binary search?"
    if "Dynamic Programming" in topic:
        return "What if the input can have negative numbers? How does that affect your state transition?"
    if "Trees" in topic:
        return "How would you handle a BST that is not balanced? What about a degenerate tree?"
    if "Graphs" in topic:
        return "What if edges have negative weights? Which algorithm would you switch to?"
    if "Arrays & Hashing" in topic:
        return "What if you need to solve this with O(1) extra space?"
    return "How would you optimize this further for very large inputs?"


def _derive_interview_q(q: dict) -> str:
    """Generate the interview-style question a candidate might be asked."""
    topic = q.get("topic", "")
    return f"What is the time and space complexity of your solution? Would you choose a different approach in an interview setting?"


def _compute_srs_interval(quality: dict) -> int:
    """Spaced repetition interval in days based on overall quality."""
    overall = quality.get("overall", 50)
    if overall >= 85:
        return 7
    if overall >= 70:
        return 3
    return 1


def _build_explanation_steps(q: dict) -> list:
    """Break the explanation into discrete steps for the EXPLAIN stage."""
    explanation = q.get("explanation", "")
    if not explanation:
        return ["See the provided solution code for the approach."]

    lines = [l.strip() for l in explanation.split("\n") if l.strip()]
    if len(lines) <= 1:
        return [explanation]

    steps = []
    for line in lines:
        if len(line) > 120:
            steps.append(line)
        else:
            steps.append(line)
    return steps if steps else [explanation]


def _build_test_cases(q: dict) -> list:
    """Extract or synthesize test cases for the TEST stage."""
    tests = q.get("test_cases") or q.get("test_cases_visible") or []
    if tests:
        return tests

    hidden = q.get("hidden_test_cases") or []
    all_tests = (tests or []) + (hidden or [])

    example_in = q.get("example_input")
    example_out = q.get("example_output")
    if example_in and example_out and not all_tests:
        return [{"input": example_in, "expected_output": example_out}]

    return all_tests if all_tests else []


def _build_scaffolded_hints(q: dict) -> list:
    """Convert raw hints into scaffolded hint levels (beginner → expert).

    Each hint has: level (1-3), text, type (conceptual/syntactic/edge_case)
    Level 1 = approach hint, Level 2 = structural hint, Level 3 = optimization/edge case
    """
    raw_hints = q.get("hints") or []
    if not raw_hints:
        # Auto-generate hints based on topic
        topic = q.get("topic", "")
        if "Binary Search" in topic:
            raw_hints = [
                "Consider how binary search can find boundaries rather than exact values.",
                "You can run binary search twice — once for leftmost, once for rightmost.",
                "For edge cases: handle empty arrays and targets outside the array range.",
            ]
        elif "Dynamic Programming" in topic:
            raw_hints = [
                "Identify the state: what parameters define a subproblem?",
                "Define the recurrence: how does dp[i] relate to dp[i-1]?",
                "Optimize space: can you reduce O(n) memory to O(1)?",
            ]
        elif "Tree" in topic:
            raw_hints = [
                "Decide on traversal: DFS or BFS for this tree property?",
                "Consider using a dummy node if the root might change.",
                "For path problems: think about bottom-up accumulation.",
            ]
        elif "Graph" in topic:
            raw_hints = [
                "Model the problem as a graph: what are nodes and edges?",
                "DFS for reachability, BFS for shortest path in unweighted graphs.",
                "For weighted graphs with negative edges: consider Bellman-Ford.",
            ]
        else:
            raw_hints = [
                "Break the problem into smaller sub-problems.",
                "Look for patterns from similar solved problems.",
                "Consider edge cases: empty input, single element, duplicates.",
            ]

    # Map raw hints to scaffolded levels with type annotation
    scaffolded = []
    for i, hint in enumerate(raw_hints):
        if i == 0:
            level = 1
            hint_type = "conceptual"
        elif i == 1:
            level = 2
            hint_type = "structural"
        else:
            level = 3
            hint_type = "edge_case" if "edge" in hint.lower() or "case" in hint.lower() else "optimization"

        scaffolded.append({
            "level": level,
            "type": hint_type,
            "text": hint,
        })

    # Ensure we always have at least 3 hint levels
    while len(scaffolded) < 3:
        extra_levels = [
            ("conceptual", "What is the core data structure needed here?"),
            ("structural", "How can you decompose this into sub-problems?"),
            ("optimization", "Can you improve the time or space complexity?"),
        ]
        idx = len(scaffolded) - 0  # continue from where we are
        if idx < len(extra_levels):
            scaffolded.append({
                "level": len(scaffolded) + 1,
                "type": extra_levels[idx][0],
                "text": extra_levels[idx][1],
            })
        else:
            break

    return scaffolded


def _build_test_cases_synthetic(q: dict) -> list:
    """Generate synthetic test cases for questions that have none."""
    q_type = q.get("type", "coding")
    if q_type != "coding":
        return []

    topic = q.get("topic", "")
    examples = q.get("example_input") and q.get("example_output")

    test_cases = []

    if topic == "Arrays & Hashing":
        test_cases = [
            {"input": "nums = [1,2,3,4,5]", "expected_output": "varies"},
            {"input": "nums = []", "expected_output": "varies"},
            {"input": "nums = [1]", "expected_output": "varies"},
        ]
    elif "Binary Search" in topic:
        test_cases = [
            {"input": "nums = [1,3,5,6,8,9], target = 5", "expected_output": "2"},
            {"input": "nums = [], target = 5", "expected_output": "-1"},
            {"input": "nums = [1], target = 1", "expected_output": "0"},
        ]
    elif "Two Pointers" in topic:
        test_cases = [
            {"input": "s = 'hello'", "expected_output": "varies"},
            {"input": "s = ''", "expected_output": "varies"},
            {"input": "s = 'a'", "expected_output": "varies"},
        ]
    elif "Trees" in topic:
        test_cases = [
            {"input": "root = [1,2,3]", "expected_output": "varies"},
            {"input": "root = []", "expected_output": "varies"},
            {"input": "root = [1]", "expected_output": "varies"},
        ]
    elif "Dynamic Programming" in topic:
        test_cases = [
            {"input": "n = 5", "expected_output": "8"},
            {"input": "n = 0", "expected_output": "0"},
            {"input": "n = 1", "expected_output": "1"},
        ]
    elif "Graphs" in topic:
        test_cases = [
            {"input": "graph with cycle", "expected_output": "true"},
            {"input": "graph without cycle", "expected_output": "false"},
            {"input": "empty graph", "expected_output": "false"},
        ]

    if examples:
        test_cases.insert(0, {"input": q.get("example_input"), "expected_output": q.get("example_output")})

    return test_cases


def enrich_into_learning_object(q: dict) -> dict:
    """Transform a fully-authored question into a structured learning object."""
    lo = dict(q)

    scaffolded_hints = _build_scaffolded_hints(q)
    test_cases = _build_test_cases(q)
    if not test_cases:
        test_cases = _build_test_cases_synthetic(q)

    lo["learning_object"] = {
        "id": q.get("id", "") or f"lo_{q.get('semantic_hash', 'unknown')}",
        "title": q.get("title") or q.get("question", "")[:80],
        "concept": _extract_concept(q),
        "predict": _extract_predict_prompt(q),
        "explanation_steps": _build_explanation_steps(q),
        "follow_up": _derive_follow_up(q),
        "interview_question": _derive_interview_q(q),
        "test_cases": test_cases,
        "srs_interval_days": _compute_srs_interval(q.get("quality_scores", {})),
        "curriculum_skill": TOPIC_TO_SKILL.get(q.get("topic", ""), "uncategorized"),
        "stages": LEARNING_LOOP_STAGES,
        "enriched_at": datetime.now(timezone.utc).isoformat(),
    }

    # Attach scaffolded hints with bulb-reveal mechanism metadata
    lo["hints"] = scaffolded_hints
    lo["hint_reveal"] = {
        "mechanism": "bulb",
        "max_level": max(h["level"] for h in scaffolded_hints) if scaffolded_hints else 0,
        "current_revealed_level": 0,
        "cost_per_reveal": 1,
        "description": "Click the bulb icon to reveal progressive hints (beginner -> intermediate -> expert)",
    }

    lo["review_status"] = "pending_learning_object_review"

    return lo


def main():
    if not CURATED_PATH.exists():
        print(f"[enrich_learning_objects] Curated data not found at {CURATED_PATH}")
        return

    with open(CURATED_PATH, "r", encoding="utf-8") as f:
        curated = json.load(f)

    fully_authored = [q for q in curated if _is_fully_authored(q)]
    not_authored = [q for q in curated if not _is_fully_authored(q)]

    learning_objects = [enrich_into_learning_object(q) for q in fully_authored]

    # Verify enrichment quality
    with_hints = sum(1 for lo in learning_objects if lo.get("hints"))
    with_test_cases = sum(1 for lo in learning_objects if lo.get("learning_object", {}).get("test_cases"))
    scaffolded_hints = sum(1 for lo in learning_objects if lo.get("hint_reveal", {}).get("max_level", 0) >= 3)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(learning_objects, f, indent=2, ensure_ascii=False)

    print(
        f"[enrich_learning_objects] Complete — "
        f"fully_authored: {len(fully_authored)} | "
        f"enriched to learning objects: {len(learning_objects)} | "
        f"with scaffolded hints (bulb): {scaffolded_hints} | "
        f"with test cases: {with_test_cases} | "
        f"not fully authored (skipped): {len(not_authored)} | "
        f"output: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()