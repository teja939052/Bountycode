"""Tutor Move Selector — deterministic rules for choosing teaching moves.

This is the crown jewel: a pure-code rule engine that maps
`answer/misconception_code -> move`. No LLM, no network, fully testable.

Move ladder (ordered by intensity):
1. calibrated_question — initial diagnostic MCQ
2. hint_ladder        — progressive hints
3. re_analogy         — re-explain with metaphor registry
4. decompose          — break into smaller steps
5. pick_the_truth     — MCQ with authored explanations
6. teach_back         — student arranges shuffled cards
7. advance            — move to next node/topic
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from app.services.atom_engine import get_metaphor, load_metaphors

logger = logging.getLogger(__name__)

_MOVE_ORDER = [
    "calibrated_question",
    "hint_ladder",
    "re_analogy",
    "decompose",
    "pick_the_truth",
    "teach_back",
    "advance",
]


def get_next_move(
    misconception_code: str,
    history: List[Dict[str, Any]],
    profile: Dict[str, Any],
    atom_concept: str,
) -> Dict[str, Any]:
    """Return the next teaching move for a given misconception code.

    Args:
        misconception_code: The detected misconception code from student's answer.
        history: List of past moves in this session.
        profile: Student profile for personalization.
        atom_concept: The concept being taught.

    Returns:
        A move dict with `move`, `say`, and optional `opts`/`hints`/`cards`.
    """
    load_metaphors()

    if misconception_code == "resolved":
        return _move_teach_back_or_advance(history, atom_concept)

    move_index = _misconception_to_move_index(misconception_code)
    used_moves = {entry.get("move") for entry in history if isinstance(entry, dict)}

    # If we already used this move level, escalate
    while move_index < len(_MOVE_ORDER) and _MOVE_ORDER[move_index] in used_moves:
        move_index += 1

    if move_index >= len(_MOVE_ORDER):
        return _move_teach_back_or_advance(history, atom_concept)

    move_type = _MOVE_ORDER[move_index]
    return _build_move(move_type, misconception_code, profile, atom_concept)


def get_analogy_for_concept(concept: str, profile: Dict[str, Any]) -> Dict[str, Any]:
    """Pick a metaphor from the registry for a concept, personalized by profile."""
    metaphor = get_metaphor(concept)
    if not metaphor:
        return {"physical_metaphor": "A simple example", "primitive": "Speaker"}

    companies = profile.get("company_focus", [])
    if companies:
        for company in companies:
            company_data = metaphor.get("companies", {}).get(company, {})
            if company_data:
                return {
                    "physical_metaphor": metaphor.get("physical_metaphor", ""),
                    "primitive": metaphor.get("primitive", "Speaker"),
                    "company": company,
                    "intuition_hint": company_data.get("intuition_hint", ""),
                }

    return {
        "physical_metaphor": metaphor.get("physical_metaphor", ""),
        "primitive": metaphor.get("primitive", "Speaker"),
    }


def get_move_template(move_type: str) -> Dict[str, Any]:
    """Return the base template for a move type."""
    templates = {
        "calibrated_question": {
            "move": "calibrated_question",
            "say": "Diagnostic question here.",
            "opts": [],
        },
        "hint_ladder": {
            "move": "hint_ladder",
            "say": "Hint:",
            "hints": [],
            "next": "advance",
        },
        "re_analogy": {
            "move": "re_analogy",
            "say": "Let me explain it differently.",
            "opts": [
                {"t": "I understand now", "to": "advance", "code": "resolved"},
                {"t": "Still confused", "to": "decompose", "code": "needs_decompose"},
            ],
        },
        "decompose": {
            "move": "decompose",
            "say": "Let's break this into smaller steps.",
            "steps": [],
            "next": "pick_the_truth",
        },
        "pick_the_truth": {
            "move": "pick_the_truth",
            "say": "Which is actually true?",
            "opts": [],
        },
        "teach_back": {
            "move": "teach_back",
            "say": "Arrange these ideas in order:",
            "cards": [],
            "correct_order": [],
            "next": "advance",
        },
        "advance": {
            "move": "advance",
            "say": "Ready to continue.",
            "opts": [{"t": "Continue", "to": "done"}],
        },
    }
    return templates.get(move_type, templates["advance"])


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _misconception_to_move_index(code: str) -> int:
    """Map misconception code to a starting move index."""
    mapping = {
        "program_is_magic": 1,
        "computer_guesses": 1,
        "source_is_result": 2,
        "comments_run": 2,
        "print_returns_value": 2,
        "print_changes_variable": 1,
        "missing_parentheses": 1,
        "parallel_execution": 2,
        "later_line_first": 2,
        "variables_exist_immediately": 1,
        "order_doesnt_matter": 1,
        "output_without_input": 2,
        "process_skipped": 2,
        "input_is_output": 2,
    }
    return mapping.get(code, 0)


def _move_teach_back_or_advance(history: List[Dict[str, Any]], concept: str) -> Dict[str, Any]:
    used_moves = {entry.get("move") for entry in history if isinstance(entry, dict)}
    if "teach_back" not in used_moves:
        return get_move_template("teach_back")
    return get_move_template("advance")


def _build_move(move_type: str, misconception_code: str, profile: Dict[str, Any], concept: str) -> Dict[str, Any]:
    template = get_move_template(move_type)

    if move_type == "re_analogy":
        analogy = get_analogy_for_concept(concept, profile)
        template["say"] = f"Let me explain with a different picture: {analogy.get('physical_metaphor', '')}."

    elif move_type == "decompose":
        steps = _get_decompose_steps(concept, misconception_code)
        template["say"] = "Let's break this into smaller steps."
        template["steps"] = steps
        template["next"] = "pick_the_truth"

    elif move_type == "pick_the_truth":
        options = _get_truth_options(misconception_code)
        template["opts"] = options

    elif move_type == "hint_ladder":
        hints = _get_hints_for_code(misconception_code)
        template["hints"] = hints

    elif move_type == "teach_back":
        cards = _get_teach_back_cards(concept)
        template["cards"] = cards
        template["say"] = "Arrange these ideas in the correct order:"

    return template


def _get_decompose_steps(concept: str, code: str) -> List[str]:
    steps_by_code = {
        "program_is_magic": [
            "A program is text stored in a file",
            "The computer reads that text line by line",
            "It follows the instructions exactly",
            "It does not guess or invent steps"
        ],
        "source_is_result": [
            "Source code is the input text",
            "The computer executes or interprets it",
            "Output is produced after execution",
            "Source code and output are different"
        ],
        "parallel_execution": [
            "Programs run top to bottom",
            "Each line runs after the previous one",
            "Later lines cannot affect earlier lines instantly",
            "Execution is sequential"
        ],
        "print_returns_value": [
            "print() displays a value",
            "It does not change variables",
            "Use assignment to change variables",
            "x stays the same after print(x)"
        ],
    }
    return steps_by_code.get(code, ["Step 1", "Step 2", "Step 3", "Step 4"])


def _get_hints_for_code(code: str) -> List[str]:
    hints_by_code = {
        "program_is_magic": [
            "Think about what a recipe does",
            "A computer needs exact steps",
            "It cannot guess what you meant"
        ],
        "missing_parentheses": [
            "Check function call syntax",
            "Python uses parentheses for calls",
            "Try adding ()"
        ],
        "variables_exist_immediately": [
            "A name exists only after assignment",
            "Check the order of lines",
            "Define before use"
        ],
    }
    return hints_by_code.get(code, ["Check your assumption", "Try a smaller example", "Review the basics"])


def _get_truth_options(code: str) -> List[Dict[str, Any]]:
    options_by_code = {
        "program_is_magic": [
            {"t": "Programs are magic the computer already knows", "to": "calibrated_question", "code": "program_is_magic"},
            {"t": "Programs are exact instructions executed in order", "to": "teach_back", "code": "resolved"},
            {"t": "Computers fill in missing steps automatically", "to": "calibrated_question", "code": "computer_guesses"},
        ],
        "source_is_result": [
            {"t": "Source code and output are the same", "to": "calibrated_question", "code": "source_is_result"},
            {"t": "Output is produced after execution", "to": "teach_back", "code": "resolved"},
            {"t": "Comments are executed as code", "to": "calibrated_question", "code": "comments_run"},
        ],
        "parallel_execution": [
            {"t": "Python reads all lines before running any", "to": "calibrated_question", "code": "parallel_execution"},
            {"t": "Python runs one line at a time, top to bottom", "to": "teach_back", "code": "resolved"},
            {"t": "Later lines can affect earlier lines instantly", "to": "calibrated_question", "code": "later_line_first"},
        ],
        "print_returns_value": [
            {"t": "print() changes the variable", "to": "calibrated_question", "code": "print_changes_variable"},
            {"t": "print() only shows the current value", "to": "teach_back", "code": "resolved"},
            {"t": "print() returns a new variable", "to": "calibrated_question", "code": "print_returns_value"},
        ],
    }
    return options_by_code.get(code, [
        {"t": "Option A", "to": "calibrated_question", "code": code},
        {"t": "Option B", "to": "teach_back", "code": "resolved"},
        {"t": "Option C", "to": "calibrated_question", "code": code},
    ])


def _get_teach_back_cards(concept: str) -> List[str]:
    cards_by_concept = {
        "programs_are_instructions": [
            "Program is a list of instructions",
            "Computer reads top to bottom",
            "Wrong order gives wrong result",
            "Instructions must be exact"
        ],
        "instructions_vs_output": [
            "Computer reads source text",
            "It computes or executes",
            "It may print or return output",
            "Source code stays in the file"
        ],
        "ipo_model": [
            "Input: receive data",
            "Process: compute or transform",
            "Output: show or store result"
        ],
        "print_statement": [
            "print(x) displays x",
            "print does not assign",
            "x remains unchanged",
            "Use x = print(x) only if function returns"
        ],
        "execution_order": [
            "Run line 1",
            "Run line 2",
            "Run line 3",
            "Only defined names exist"
        ],
    }
    return cards_by_concept.get(concept, ["Concept A", "Concept B", "Concept C", "Concept D"])
