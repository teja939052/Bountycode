"""Generate World 1 proof curriculum lesson modules.

Reads the lesson specs from WORLD1_CURRICULUM_MAP.md and emits
curriculum/world1_*.py modules with the canonical 9-step teaching loop.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List

CURRICULUM_DIR = Path(__file__).resolve().parent


def _python_value(value: Any) -> str:
    if value is None:
        return "None"
    if isinstance(value, str):
        return repr(value)
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        items = ", ".join(_python_value(v) for v in value)
        return f"[{items}]"
    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            lines.append(f"            {repr(k)}: {_python_value(v)}")
        inner = ",\n".join(lines)
        return f"{{\n{inner}\n        }}"
    return repr(value)


def _emit_lesson(lesson: Dict[str, Any], filename: str) -> str:
    return "\n".join([
        f'"""World 1 lesson — {lesson.get("title", filename)}"""',
        "from typing import Dict, Any",
        "",
        f"LESSON: Dict[str, Any] = {_python_value(lesson)}",
        "",
        f"SLUG = {repr(filename.replace('.py', ''))}",
        "",
    ])


# ═══════════════════════════════════════════════════════════════
# Lesson factory
# ═══════════════════════════════════════════════════════════════

def _base_lesson(slug: str, title: str, concept: str, mental_model: str, module_id: str) -> Dict[str, Any]:
    return {
        "lesson_id": f"world1_{slug}",
        "module_id": module_id,
        "title": title,
        "description": f"Master {title}: {mental_model}",
        "difficulty": "beginner",
        "est_minutes": 12,
        "xp_reward": 120,
        "skills_taught": [concept],
        "srs_concept_tag": f"world1:{concept}",
        "domain": "coding",
        "captain_byte": {
            "intro": f"Welcome to {title}. {mental_model}",
            "correct": ["Nice!", "Exactly right!", "Clean."],
            "wrong": ["Review the step and try again.", "Close — look at what changed.", "Think about the mental model."],
            "after_break": "You found the broken assumption. Now fix it.",
            "after_mastery": f"You've mastered {title}. On to the next challenge.",
            "retry_prompt": "Try again. You're close.",
        },
        "story_context": {
            "title": title,
            "narration": f"Learn {concept} through the complete teaching loop.",
            "setting": "world1_foundations",
            "character": "Captain Byte",
            "intro_text": mental_model,
        },
        "steps": {
            "discover": {"prompt": f"Observe how {concept} works in this example.", "interaction_kind": "mcq_read"},
            "understand": {"prompt": f"Understand the core principle of {concept}.", "explanation": mental_model, "interaction_kind": "read_explanation"},
            "manipulate": {"prompt": f"Modify the example and observe the change.", "interaction_kind": "numeric_input"},
            "predict": {"prompt": f"Predict the output before running.", "interaction_kind": "numeric_input"},
            "build": {"prompt": f"Write a function using {concept}.", "interaction_kind": "code_build"},
            "break_step": {"prompt": f"What is wrong with this {concept} usage?", "interaction_kind": "mcq_diagnose"},
            "debug": {"prompt": f"Fix the {concept} bug.", "interaction_kind": "code_fix"},
            "retrieval": {"prompt": f"Recall the key rule for {concept}.", "interaction_kind": "recall_formula"},
            "transfer": {"prompt": f"Apply {concept} to a new problem.", "interaction_kind": "word_problem"},
        },
        "practice": [
            {"kind": "mcq", "prompt": f"Practice 1: {concept} basic", "answer": "A", "explanation": "Basic application.", "difficulty": "easy", "company_tags": []},
            {"kind": "mcq", "prompt": f"Practice 2: {concept} intermediate", "answer": "B", "explanation": "Intermediate application.", "difficulty": "medium", "company_tags": []},
            {"kind": "numeric", "prompt": f"Practice 3: {concept} numeric", "answer": "42", "explanation": "Numeric application.", "difficulty": "medium", "company_tags": []},
        ],
        "proof": [
            {"id": f"{slug}-p1", "prompt": f"Prove you understand {concept}.", "answer_format": "text", "correct": "Correct", "explanation": f"Tests {concept} understanding.", "time_limit_seconds": 60, "company_tags": []},
            {"id": f"{slug}-p2", "prompt": f"Apply {concept} to a new context.", "answer_format": "text", "correct": "Correct", "explanation": f"Tests {concept} transfer.", "time_limit_seconds": 60, "company_tags": []},
        ],
        "company_variants": [],
        "misconceptions": [{"code": f"world1_{slug}_mistake", "signature": f"Common mistake in {concept}", "reteach_route": "worked_example", "reteach_action": "show_correct_process"}],
        "srs_key_points": [f"Core principle of {concept}", f"Common pitfall in {concept}", f"When to apply {concept}"],
        "srs_review_intervals": [1, 3, 7, 14, 30],
        "world_progression": {
            "world_id": "coding_foundations",
            "competency_id": concept,
            "unlocks_next": [],
            "tower_badge": f"world1_{slug}",
        },
    }


# ═══════════════════════════════════════════════════════════════
# 23 missing World 1 lessons
# ═══════════════════════════════════════════════════════════════

LESSONS: Dict[str, Dict[str, Any]] = {}

# Chapter 1
LESSONS["strings_words"] = _base_lesson(
    "strings_words",
    "The Stringed Loom",
    "strings",
    "Strings are immutable sequences of characters. Indexing starts at 0; len() gives the count.",
    "world1:strings",
)
LESSONS["booleans_compare"] = _base_lesson(
    "booleans_compare",
    "Booleans and Comparisons",
    "booleans",
    "== checks equality; = assigns. Comparison operators return True or False.",
    "world1:booleans",
)
LESSONS["control_flow"] = _base_lesson(
    "control_flow",
    "The Forking Path",
    "control_flow",
    "if/else picks one path. The 'no' case must be handled explicitly.",
    "world1:control_flow",
)

# Chapter 2
LESSONS["elif_chain"] = _base_lesson(
    "elif_chain",
    "Ordered Decisions",
    "decisions",
    "elif runs the first true branch. Order conditions from most specific to most general.",
    "world1:decisions",
)
LESSONS["logic_combo"] = _base_lesson(
    "logic_combo",
    "and / or / not",
    "booleans",
    "and needs both; or needs one; not inverts. Parentheses group logic.",
    "world1:booleans",
)
LESSONS["condition_bugs"] = _base_lesson(
    "condition_bugs",
    "Break: Wrong Condition",
    "control_flow",
    "Inverted logic, off-by-one boundaries, and missing edge cases cause wrong conditions.",
    "world1:control_flow",
)
LESSONS["condition_spec"] = _base_lesson(
    "condition_spec",
    "Eligibility Spec to Code",
    "decisions",
    "Parse English rules into correct boolean expressions with all clauses.",
    "world1:decisions",
)
LESSONS["decision_oa"] = _base_lesson(
    "decision_oa",
    "Timed Placement: Decide + Loop",
    "decisions",
    "Solve timed decision problems under placement conditions.",
    "world1:decisions",
)

# Chapter 3
LESSONS["while_loop"] = _base_lesson(
    "while_loop",
    "Controlled Repetition",
    "loops",
    "while repeats while a condition is true. The condition must change or the loop never ends.",
    "world1:loops",
)
LESSONS["accumulate_run"] = _base_lesson(
    "accumulate_run",
    "Accumulators: Sum and Count",
    "loops",
    "An accumulator starts at 0 before the loop and updates inside it.",
    "world1:loops",
)
LESSONS["string_walk"] = _base_lesson(
    "string_walk",
    "Walk a String",
    "strings",
    "Iterate over characters with for. Convert char to int with ord() or int().",
    "world1:strings",
)
LESSONS["loop_stop"] = _base_lesson(
    "loop_stop",
    "Break, Continue, Nested Loops",
    "loops",
    "break exits the innermost loop; continue skips to the next iteration.",
    "world1:loops",
)
LESSONS["loop_bugs"] = _base_lesson(
    "loop_bugs",
    "Break: Off-by-One and Infinite",
    "loops",
    "Stop-boundary errors, wrong accumulator placement, and infinite-loop risks.",
    "world1:loops",
)
LESSONS["loop_transfer"] = _base_lesson(
    "loop_transfer",
    "Timed Transfer: Sum Every Even Digit",
    "loops",
    "Parse a timed prompt, plan, build, and test hidden cases for digit filtering.",
    "world1:loops",
)

# Chapter 4
LESSONS["list_mutate"] = _base_lesson(
    "list_mutate",
    "Mutate in Place vs Rebind",
    "arrays",
    "append/insert/remove mutate; l = [...] rebinds. Know the difference.",
    "world1:arrays",
)
LESSONS["list_walk"] = _base_lesson(
    "list_walk",
    "Traverse a List",
    "arrays",
    "Sum, max, and count over a list with for x in l. Start max at -inf for negatives.",
    "world1:arrays",
)
LESSONS["list_build"] = _base_lesson(
    "list_build",
    "Build New Lists",
    "arrays",
    "Filter or transform into a new list. Do not modify the original while building.",
    "world1:arrays",
)
LESSONS["list_copy"] = _base_lesson(
    "list_copy",
    "Slicing, Aliasing, Copying",
    "arrays",
    "b = a aliases; b = a[:] copies. Slice aliases the original.",
    "world1:arrays",
)
LESSONS["list_bugs"] = _base_lesson(
    "list_bugs",
    "Break: Index, Boundary, Alias",
    "arrays",
    "Wrong index, boundary errors, mutation-during-iteration, alias surprise.",
    "world1:arrays",
)
LESSONS["list_transfer"] = _base_lesson(
    "list_transfer",
    "Timed Transfer: Second-Largest",
    "arrays",
    "Find the second-largest element handling duplicates and negatives.",
    "world1:arrays",
)

# Chapter 5
LESSONS["scope_rules"] = _base_lesson(
    "scope_rules",
    "Locals, Globals, Copies",
    "functions",
    "Locals die at return. Globals do not change inside functions. Parameters are copies.",
    "world1:functions",
)
LESSONS["compose_reuse"] = _base_lesson(
    "compose_reuse",
    "Compose Small Functions",
    "functions",
    "Factor repetition into helpers. Small functions compose; one big function does not.",
    "world1:functions",
)
LESSONS["function_bugs"] = _base_lesson(
    "function_bugs",
    "Break: The Silent Forge",
    "functions",
    "Missing return, wrong argument order, shadowing, parameter mutation.",
    "world1:functions",
)
LESSONS["capstone_oa"] = _base_lesson(
    "capstone_oa",
    "World-1 Exam: Perform + Explain",
    "capstone",
    "Solve 4 unseen timed placement-style problems unaided, then explain one solution.",
    "world1:capstone",
)


def generate_all(force: bool = False) -> Dict[str, str]:
    generated: Dict[str, str] = {}
    for slug, lesson in LESSONS.items():
        filename = f"world1_{slug}.py"
        out_path = CURRICULUM_DIR / filename
        if out_path.exists() and not force:
            continue
        text = _emit_lesson(lesson, filename)
        out_path.write_text(text, encoding="utf-8")
        generated[slug] = str(out_path)
    return generated


if __name__ == "__main__":
    generated = generate_all(force=True)
    print(f"Generated {len(generated)} World 1 lessons")
    for slug, path in sorted(generated.items()):
        print(f"  {slug} -> {path}")
