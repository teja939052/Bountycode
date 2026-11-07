"""Shared builder for authored lessons in compiled-language tracks."""
from __future__ import annotations

from typing import Any, Dict


def build_authored_lesson(profile: Dict[str, Any], language_name: str) -> Dict[str, Any]:
    """Convert a reviewed concept profile into the lesson renderer's schema."""
    concept = profile["concept"]
    code = profile["code"]
    theory = (
        f"{concept.capitalize()} is an important {language_name} concept used to "
        f"{profile['purpose']}. {profile['how']} {profile['why']} "
        f"Understand the rule behind the syntax, trace the example, and verify it "
        f"with normal and boundary inputs. {profile['pitfall']}"
    )
    return {
        "theory": theory,
        "analogy": (
            f"Think of {concept} as a tool in a developer's toolkit: it helps you "
            f"{profile['purpose']}. The example demonstrates the idea with concrete data."
        ),
        "sections": [
            {
                "heading": f"How {concept} works",
                "body": profile["how"],
                "code": code,
                "pro_tip": "Predict the result before running the example, then explain why each important line behaves that way.",
            },
            {
                "heading": "When and why to use it",
                "body": profile["why"],
                "code": code,
                "pro_tip": "Prefer the simplest approach that communicates the requirement clearly and is easy to test.",
            },
            {
                "heading": "Common mistakes and edge cases",
                "body": profile["pitfall"],
                "code": code,
                "pro_tip": "Test a normal input, a boundary input, and an invalid or unexpected input.",
            },
        ],
        "code_example": {
            "code": code,
            "annotations": [
                {
                    "line": index + 1,
                    "text": "Explain what this line contributes to the example and how it changes or uses the current data.",
                }
                for index, _line in enumerate(code.splitlines())
            ],
        },
        "common_mistakes": [
            {
                "mistake": profile["pitfall"],
                "fix": "Reproduce the issue with the smallest useful input, compare expected and actual behaviour, then rerun normal and boundary tests.",
            },
            {
                "mistake": "Assuming one happy-path example proves the solution handles every input.",
                "fix": "Add a normal case, a boundary case, and an invalid or unexpected input; verify each result against an explicit expectation.",
            },
        ],
        "exercises": [
            {
                "description": profile["exercise"],
                "starter_code": profile.get("starter_code", "// Write your solution here"),
                "hints": profile.get("hints", [
                    "Identify the input and expected result before writing code.",
                    "Apply the concept's rule to a small example.",
                    "Test a boundary or alternate case before submitting.",
                ]),
                "expected_output": profile["expected"],
            },
            {
                "description": profile.get("exercise2", f"Extend the example for {concept} to handle one additional real-world case and explain your design choice."),
                "starter_code": profile.get("starter_code2", "// Extend the example here"),
                "hints": profile.get("hints2", [
                    "Start from the worked example and identify the new requirement.",
                    "Keep the change focused on one responsibility.",
                    "Run both the original and new test cases.",
                ]),
                "expected_output": profile.get("expected2", "The extended solution handles both the original case and the additional case correctly."),
            },
        ],
        "quizzes": [
            {
                "question": question,
                "options": options,
                "correct": correct,
                "explanation": explanation,
            }
            for question, options, correct, explanation in profile["quiz"]
        ],
        "key_takeaways": [
            profile["purpose"].capitalize(),
            profile["how"],
            profile["pitfall"],
            "Test normal, boundary, and invalid inputs before considering the concept reliable.",
        ],
        "next_steps": "Complete both exercises, answer the quiz, explain when this concept is useful, and solve a fresh variation without copying the example.",
    }
