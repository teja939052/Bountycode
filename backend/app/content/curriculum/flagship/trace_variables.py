"""
Flagship Lesson — Trace Variables
=====================================

Gold-standard interactive lesson for code tracing.

Full teaching loop with Captain Byte authored mentor moments.
"""
from typing import Dict, Any

SLUG = "trace_variables"

LESSON: Dict[str, Any] = {
    "lesson_id": "trace_variables_harvest_ledger",
    "module_id": "programming_fundamentals:tracing",
    "title": "The Harvest Ledger",
    "description": "Read a whole program line by line and predict the final printed values without running it.",
    "difficulty": "beginner",
    "est_minutes": 14,
    "xp_reward": 120,
    "skills_taught": ["tracing", "variables", "expressions", "state"],
    "srs_concept_tag": "programming_fundamentals:tracing",
    "captain_byte": {
        "intro": (
            "🧭 **Captain Byte**\n"
            "“The Harvest Ledger records the season in one long column. "
            "Numbers change, text joins, and at the end the final values are read aloud. "
            "Your job is to read the ledger like a story — line by line, box by box — "
            "and say exactly what is printed. Don’t run it. Trace it.”"
        ),
        "correct": [
            "🧭 **Captain Byte**\n“Nice. You tracked every box without running the code.”",
            "🧭 **Captain Byte**\n“That trace was clean. You’re reading state, not guessing.”",
            "🧭 **Captain Byte**\n“Exactly. The newest assignment wins, every time.”",
        ],
        "wrong": [
            "🧭 **Captain Byte**\n“Stop. Don’t guess the final value. Trace one box at a time.”",
            "🧭 **Captain Byte**\n“You’re mixing up the old and new values. Read top to bottom.”",
            "🧭 **Captain Byte**\n“Close, but you missed a reassignment. Go line by line.”",
        ],
        "after_break": "🧭 **Captain Byte**\n“You spotted the broken assumption. Now repair the trace.”",
        "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Trace anything now.”",
        "retry_prompt": "🧭 **Captain Byte**\n“Try again. Follow each box from top to bottom. What does the LAST assignment say?”",
    },
    "story_context": {
        "title": "The Harvest Ledger",
        "narration": (
            "The Harvest Ledger records the season in one long column: numbers change, "
            "text joins, and at the end the final values are read aloud. "
            "Your job is to read the ledger like a story — line by line, box by box — "
            "and say exactly what is printed."
        ),
        "setting": "harvest_ledger",
        "character": "Captain Byte",
        "intro_text": (
            "You have learned input, state, output; named boxes; types; and the order "
            "of operations. Now read complete programs the way you read a story — "
            "line by line, box by box — and state exactly what is printed."
        ),
    },
    "discovery": {
        "title": "Read the Ledger",
        "visual_primitives": ["trace", "highlight", "reveal"],
        "steps": [
            {
                "action": "recap_concat",
                "narration": "Text joins. name becomes Li, then grows a '!' and prints it.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "name = \"Li\"\nname = name + \"!\"\nprint(name)",
                    "expected_output": "Li!",
                    "hint": "name = name + \"!\" keeps the old text and adds the exclamation.",
                },
            },
            {
                "action": "recap_mixed",
                "narration": "Two boxes and one expression: a is 2, b is 2 * 3, then both print.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "a = 2\nb = a * 3\nprint(a + b)",
                    "expected_output": "8",
                    "hint": "b = 6, then 2 + 6 = 8.",
                },
            },
            {
                "action": "recap_len",
                "narration": "len counts the characters in the text; then one more is added.",
                "interaction": {
                    "type": "inspect_code",
                    "code": "word = \"hi\"\nprint(len(word) + 1)",
                    "expected_output": "3",
                    "hint": "len(\"hi\") = 2, plus 1 = 3.",
                },
            },
            {
                "action": "recap_final",
                "narration": "Which value does the box hold when the program reaches print?",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "After n = 3, then n = n + 1, then n = n + 2, what is n?",
                    "options": [
                        {"id": "a", "text": "6", "correct": True},
                        {"id": "b", "text": "3", "correct": False},
                        {"id": "c", "text": "4", "correct": False},
                        {"id": "d", "text": "Stay 3 from start to finish", "correct": False},
                    ],
                    "explanation": "3 + 1 = 4, then 4 + 2 = 6. The box ends at 6.",
                },
            },
        ],
        "conclusion": (
            "Reading a whole program is one skill: follow the boxes down, join text "
            "when you see + on strings, apply the scale to each expression, and read "
            "the final values aloud."
        ),
    },
    "prediction": {
        "title": "Before You Trace",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Before you run it, predict. What does this program print?”",
        "question": "What does this program print?",
        "code": "a = 5\nb = a + 1\na = b * 2\nprint(a + b)",
        "options": [
            {"id": "a", "text": "18", "correct": True, "explanation": "a = 5, b = 6, then a = 12; 12 + 6 = 18."},
            {"id": "b", "text": "21", "correct": False, "explanation": "21 would reuse the old a (5) after it already became 12."},
            {"id": "c", "text": "12", "correct": False, "explanation": "12 is only a, and the print adds b."},
            {"id": "d", "text": "An error", "correct": False, "explanation": "Every line is valid."},
        ],
        "explanation": (
            "Trace the boxes: a = 5, b = 6, a = 12. print(a + b) uses the NEW a: 18."
        ),
    },
    "explain": {
        "title": "Explain the Trace",
        "captain_byte_intro": "🧭 **Captain Byte**\n“In the three lines a = 5, b = a + 1, a = b * 2, explain what the line a = b * 2 does.”",
        "prompt": "In the three lines a = 5, b = a + 1, a = b * 2, explain what the line a = b * 2 does.",
        "answer_format": "short_answer",
        "keywords": ["box", "b", "assign", "new", "doubles", "twice", "value", "6", "12"],
        "min_words": 8,
        "model_answer": (
            "It reads the current value of b, which is 6, doubles it, and stores the "
            "new value 12 into the box labelled a, replacing its old value."
        ),
        "intention": "The explanation must show assignment reads the CURRENT value, computes, and replaces the box.",
    },
    "guided_build": {
        "title": "Write the Ledger, Then Read It",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Now you write the code, then read your own ledger.”",
        "steps": [
            {
                "step_order": 1,
                "title": "Moved Total",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Two steps: advance, then recede. The total can go below zero.”",
                "description": "Return the total after moving `up` then moving back `down`.",
                "starter_code": "def moved_total(start, up, down):\n    # start + up, then - down\n    pass",
                "function_name": "moved_total",
                "signature": "def moved_total(start: int, up: int, down: int) -> int:",
                "test_cases": [
                    {"input": [5, 3, 1], "expected": 7},
                    {"input": [0, 0, 0], "expected": 0},
                ],
                "hidden_test_cases": [
                    {"input": [1, 2, 5], "expected": -2},
                    {"input": [9, 1, 4], "expected": 6},
                    {"input": [3, 3, 3], "expected": 3},
                ],
                "diamonds": 35,
                "scaffolded_hints": [
                    {"level": 1, "text": "Two steps: advance, then recede."},
                    {"level": 2, "text": "return start + up - down"},
                    {"level": 3, "text": "Moving back further than the starting point is allowed — the total can go below zero."},
                ],
            },
            {
                "step_order": 2,
                "title": "Shout Twice",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Join four pieces: word, bang, word, bang.”",
                "description": "Return the word, an exclamation, the same word, and one more exclamation.",
                "starter_code": "def shout_twice(word):\n    # word + \"!\" + word + \"!\"\n    pass",
                "function_name": "shout_twice",
                "signature": "def shout_twice(word: str) -> str:",
                "test_cases": [
                    {"input": ["go"], "expected": "go!go!"},
                    {"input": ["hi"], "expected": "hi!hi!"},
                ],
                "hidden_test_cases": [
                    {"input": ["x"], "expected": "x!x!"},
                    {"input": ["hey"], "expected": "hey!hey!"},
                    {"input": [""], "expected": "!!"},
                ],
                "diamonds": 35,
                "scaffolded_hints": [
                    {"level": 1, "text": "Four pieces joined end to end."},
                    {"level": 2, "text": "return word + \"!\" + word + \"!\""},
                    {"level": 3, "text": "An empty word still leaves two exclamation points."},
                ],
            },
            {
                "step_order": 3,
                "title": "Shelved Tax",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Rate is a percent. Divide by 100 once, then multiply.”",
                "description": "Return the tax on a total: total * rate / 100.",
                "starter_code": "def taxed(total, rate):\n    # total * rate / 100\n    pass",
                "function_name": "taxed",
                "signature": "def taxed(total: int, rate: int) -> float:",
                "test_cases": [
                    {"input": [200, 10], "expected": 20.0},
                    {"input": [100, 25], "expected": 25.0},
                ],
                "hidden_test_cases": [
                    {"input": [0, 10], "expected": 0.0},
                    {"input": [500, 5], "expected": 25.0},
                    {"input": [90, 50], "expected": 45.0},
                ],
                "diamonds": 35,
                "scaffolded_hints": [
                    {"level": 1, "text": "rate is a percent; divide by 100 once."},
                    {"level": 2, "text": "return total * rate / 100"},
                    {"level": 3, "text": "Left to right: multiply first, then divide."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Window's Word",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Same skills, new shape. Three facts about a word.”",
        "description": (
            "The Librarian labels every ledger with three facts about its word: its "
            "length, its first letter, and its full-text shouting form."
        ),
        "function_name": "describe_word",
        "signature": "def describe_word(word: str) -> list:",
        "description_full": (
            "Return a list of three facts about word:\n"
            "  [len(word), the first character, word.upper()]\n\n"
            "For an empty word, the first character should be the empty string (there "
            "is no first character).\n\n"
            "Examples:\n"
            "  describe_word(\"door\") -> [4, \"d\", \"DOOR\"]\n"
            "  describe_word(\"a\")    -> [1, \"a\", \"A\"]\n"
            "  describe_word(\"\")     -> [0, \"\", \"\"]"
        ),
        "test_cases": [
            {"input": ["door"], "expected": [4, "d", "DOOR"]},
            {"input": ["a"], "expected": [1, "a", "A"]},
            {"input": ["Milo"], "expected": [4, "M", "MILO"]},
        ],
        "hidden_test_cases": [
            {"input": [""], "expected": [0, "", ""]},
            {"input": ["tea"], "expected": [3, "t", "TEA"]},
            {"input": ["Q"], "expected": [1, "Q", "Q"]},
            {"input": ["exam"], "expected": [4, "e", "EXAM"]},
        ],
        "time_limit_minutes": 7,
        "diamonds": 80,
        "scaffolded_hints": [
            {"level": 1, "text": "word[0] is the first character — but only when word is not empty."},
            {"level": 2, "text": "Build it as a list: return [len(word), word[0] if word else \"\", word.upper()]"},
            {"level": 3, "text": "The empty string is the safe first-character answer when there is no character."},
        ],
    },
    "assessment": {
        "title": "Harvest Ledger Final Test",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Prove you can trace without running. Timed.”",
        "description": "The whole chapter in three moves: trace once, explain the box, and fix a line.",
        "questions": [
            {
                "type": "code_tracing",
                "code": "name = \"Li\"\nname = name + \"!\"\nprint(len(name) + 2)",
                "answer_format": "single_number",
                "expected_answer": "5",
                "explanation": "name becomes \"Li!\", len(\"Li!\") = 3, then 3 + 2 = 5.",
            },
            {
                "type": "concept",
                "question": "A variable keeps which of its values after several assignments?",
                "answer_format": "short_answer",
                "keywords": ["last", "newest", "replaced", "latest", "overwrite"],
                "explanation": "Each assignment replaces the box, so the box keeps the NEWEST value at the end.",
            },
            {
                "type": "debug",
                "code": "def welcome(name):\n    return name\n# forgot the greeting mark",
                "error": "welcome('Ana') must return 'Ana!', but returns 'Ana'.",
                "question": "One line is wrong. What is the correct line?",
                "fix": "return name + \"!\"",
                "explanation": "return name hands back the text untouched. Joining \"!\" completes the greeting.",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 120,
    },
    "break": {
        "title": "The Double Triple",
        "captain_byte_intro": "🧭 **Captain Byte**\n“I broke the counter on purpose. Find the wrong assumption.”",
        "story": (
            "A triple counter was supposed to multiply by three, but it only doubles. "
            "Inspect the line that multiplies and find the wrong factor."
        ),
        "buggy_code": "def triple(x):\n    x = x * 2\n    return x\n\nprint(triple(3))",
        "expected_output": "9",
        "actual_output": "6 (the box is doubled, not tripled)",
        "diagnosis": {
            "question": "Which of these is the true cause?",
            "options": [
                {"id": "a", "text": "The box is multiplied by 2 instead of 3", "correct": True, "why": "tripling 3 means 3 * 3 = 9; a factor of 2 gives 6."},
                {"id": "b", "text": "The box starts at the wrong value", "correct": False, "why": "It receives 3, which is the intended input."},
                {"id": "c", "text": "The wrong box is returned", "correct": False, "why": "Returning x after the change is correct."},
                {"id": "d", "text": "print is missing a value", "correct": False, "why": "The print call passes the function's result."},
            ],
        },
        "fix": "x = x * 3",
        "fixed_code": "def triple(x):\n    x = x * 3\n    return x\n\nprint(triple(3))",
        "explanation": (
            "Doubling gives 6 where tripling must give 9. Changing the factor from 2 "
            "to 3 repairs the counter."
        ),
    },
    "srs_enrollment": {
        "concept_id": "programming_fundamentals:tracing",
        "concept_name": "Code Tracing",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "read lines top to bottom, box by box",
            "+ joins strings and adds numbers",
            "apply the order of operations to each expression",
            "the newest assignment wins",
            "print reveals the final values",
        ],
        "spaced_fields": [
            "read_whole_program",
            "string_plus_joins",
            "newest_assignment",
        ],
    },
    "world_progression": {
        "world_id": "code_foundations",
        "competency_id": "trace_variables",
        "unlocks_next": ["control_flow"],
        "tower_badge": "first_trace",
        "world_node": {
            "level": 6,
            "title": "The Harvest Ledger",
            "color": "teal",
            "icon": "📜",
            "description": "Read a whole program without running it",
        },
    },
}
