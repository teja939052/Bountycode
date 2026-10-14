"""
Flagship Lesson — Blood Relations
=====================================

Gold-standard interactive lesson for logical blood-relation reasoning.

Full teaching loop with Captain Byte authored mentor moments.
"""
from typing import Dict, Any

SLUG = "blood_relations"

LESSON: Dict[str, Any] = {
    "lesson_id": "blood_relations_family_tree",
    "module_id": "aptitude:logical:blood_relations",
    "title": "The Family Tree",
    "description": "Map family relations from coded statements and answer who-is-related-to-whom questions.",
    "difficulty": "beginner",
    "est_minutes": 15,
    "xp_reward": 120,
    "skills_taught": ["blood_relations", "logical_reasoning", "aptitude"],
    "srs_concept_tag": "aptitude:blood_relations",
    "captain_byte": {
        "intro": (
            "🧭 **Captain Byte**\n"
            "“The village recorder keeps the family tree as a puzzle of statements. "
            "‘A is B’s father,’ ‘C is B’s mother,’ and so on. "
            "Solve the puzzle by drawing the tree in your mind. "
            "Spouse first, then parent/child, then sibling. Once the tree is right, "
            "the answer is obvious.”"
        ),
        "correct": [
            "🧭 **Captain Byte**\n“Nice. You read the tree, not the words.”",
            "🧭 **Captain Byte**\n“That’s the right path. Count the hops.”",
            "🧭 **Captain Byte**\n“Clean. The shortest path gives the direct relation.”",
        ],
        "wrong": [
            "🧭 **Captain Byte**\n“Stop. Don’t guess from the words. Draw the tree.”",
            "🧭 **Captain Byte**\n“You’re missing a link. Add one edge at a time.”",
            "🧭 **Captain Byte**\n“Close, but you skipped a generation. Count the hops again.”",
        ],
        "after_break": "🧭 **Captain Byte**\n“You found the broken assumption. Now rebuild the tree correctly.”",
        "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any family tree, any relation.”",
        "retry_prompt": "🧭 **Captain Byte**\n“Try again. Spouse first, then parent/child, then sibling. What’s the shortest path?”",
    },
    "story_context": {
        "title": "The Family Tree",
        "narration": (
            "The village recorder keeps the family tree as a puzzle of statements: "
            "'A is B's father,' 'C is B's mother,' and so on. Solve the puzzle by "
            "drawing the tree in your mind."
        ),
        "setting": "family_tree",
        "character": "Captain Byte",
        "intro_text": (
            "Blood-relation questions are solved by one method: draw the tree. "
            "Spouse first, then parent/child, then sibling. Once the tree is right, "
            "the answer is obvious."
        ),
    },
    "discovery": {
        "title": "Sketch the Tree",
        "visual_primitives": ["trace", "compare", "reveal"],
        "steps": [
            {
                "action": "spouse_first",
                "narration": "A is B's husband. B is C's mother. Who is C to A?",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "A is B's husband. B is C's mother. Who is C to A?",
                    "options": [
                        {"id": "a", "text": "Daughter", "correct": False},
                        {"id": "b", "text": "Son", "correct": False},
                        {"id": "c", "text": "Child", "correct": True},
                        {"id": "d", "text": "Niece", "correct": False},
                    ],
                    "explanation": "A is married to B, and B is C's mother. So A is C's father. C is A's child.",
                },
            },
            {
                "action": "parent_child",
                "narration": "P is Q's father. R is Q's mother. How is P related to R?",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "P is Q's father. R is Q's mother. How is P related to R?",
                    "options": [
                        {"id": "a", "text": "Brother", "correct": False},
                        {"id": "b", "text": "Husband", "correct": True},
                        {"id": "c", "text": "Uncle", "correct": False},
                        {"id": "d", "text": "Father-in-law", "correct": False},
                    ],
                    "explanation": "Both are Q's parents, so they are spouses.",
                },
            },
            {
                "action": "sibling_link",
                "narration": "A and B share the same father. What is the simplest relation?",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "A and B have the same father. What relation connects them?",
                    "options": [
                        {"id": "a", "text": "Cousins", "correct": False},
                        {"id": "b", "text": "Siblings", "correct": True},
                        {"id": "c", "text": "Parent/child", "correct": False},
                        {"id": "d", "text": "No relation", "correct": False},
                    ],
                    "explanation": "Same father → siblings.",
                },
            },
            {
                "action": "chain_relation",
                "narration": "Chain: A is B's father. B is C's father. How is A to C?",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "A is B's father. B is C's father. How is A related to C?",
                    "options": [
                        {"id": "a", "text": "Father", "correct": False},
                        {"id": "b", "text": "Grandfather", "correct": True},
                        {"id": "c", "text": "Uncle", "correct": False},
                        {"id": "d", "text": "Brother", "correct": False},
                    ],
                    "explanation": "Two father links in a row make A the grandfather of C.",
                },
            },
        ],
        "conclusion": (
            "Blood relations are solved by tree order: spouse, then parent/child, "
            "then sibling. Each statement adds one edge. Read the tree, not the words."
        ),
    },
    "prediction": {
        "title": "Before You Draw",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Before you draw, predict. What’s the shortest path?”",
        "question": "A is B's brother. B is C's father. How is A related to C?",
        "options": [
            {"id": "a", "text": "Uncle", "correct": True, "explanation": "A is B's brother, and B is C's father, so A is C's uncle."},
            {"id": "b", "text": "Father", "correct": False, "explanation": "B is the father; A is B's brother."},
            {"id": "c", "text": "Cousin", "correct": False, "explanation": "Cousin needs a sibling-of-parent link."},
            {"id": "d", "text": "No relation", "correct": False, "explanation": "There is a clear chain here."},
        ],
        "explanation": "Brother of father = uncle.",
    },
    "explain": {
        "title": "Explain the Tree",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Why does drawing the tree make coded relation questions easier?”",
        "prompt": "Why does drawing the tree make coded relation questions easier?",
        "answer_format": "short_answer",
        "keywords": ["tree", "edge", "node", "visual", "chain", "parent", "child", "spouse", "draw"],
        "min_words": 10,
        "model_answer": (
            "A tree makes every relation an explicit edge. Once you draw spouse and "
            "parent edges, the path from one person to another is just counting hops. "
            "The words become a picture, and the answer is the shortest path."
        ),
        "intention": "The explanation must show that tree structure replaces memorization.",
    },
    "guided_build": {
        "title": "Map the Relations",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Now you write the logic. Chain the links.”",
        "steps": [
            {
                "step_order": 1,
                "title": "Short Chain",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Chain the links: A -> B -> C. Two father links = grandfather. Brother + father = uncle.”",
                "description": "Return the relation from A to C given two statements.",
                "starter_code": "def relation_a_to_c(link1, link2):\n    # link1: A->B, link2: B->C\n    # return simple relation label\n    pass",
                "function_name": "relation_a_to_c",
                "signature": "def relation_a_to_c(link1: str, link2: str) -> str:",
                "test_cases": [
                    {"input": ["father", "father"], "expected": "grandfather"},
                    {"input": ["brother", "father"], "expected": "uncle"},
                ],
                "hidden_test_cases": [
                    {"input": ["mother", "mother"], "expected": "grandmother"},
                    {"input": ["sister", "mother"], "expected": "aunt"},
                    {"input": ["father", "son"], "expected": "brother"},
                ],
                "diamonds": 35,
                "scaffolded_hints": [
                    {"level": 1, "text": "Chain the links: A -> B -> C."},
                    {"level": 2, "text": "Two father links = grandfather. Brother + father = uncle."},
                    {"level": 3, "text": "Use simple English relation labels."},
                ],
            },
            {
                "step_order": 2,
                "title": "Gender Check",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Gender is in the word. Map it.”",
                "description": "Return the gender implied by a relation word.",
                "starter_code": "def gender_of(relation):\n    # father/mother/brother/sister/uncle/aunt\n    pass",
                "function_name": "gender_of",
                "signature": "def gender_of(relation: str) -> str:",
                "test_cases": [
                    {"input": ["father"], "expected": "male"},
                    {"input": ["aunt"], "expected": "female"},
                ],
                "hidden_test_cases": [
                    {"input": ["brother"], "expected": "male"},
                    {"input": ["sister"], "expected": "female"},
                    {"input": ["uncle"], "expected": "male"},
                ],
                "diamonds": 30,
                "scaffolded_hints": [
                    {"level": 1, "text": "Map the known relation words to gender."},
                    {"level": 2, "text": "father/brother/uncle -> male; mother/sister/aunt -> female"},
                    {"level": 3, "text": "Default to unknown rather than guessing."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Recorder's Puzzle",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Deeper chain. Build the tree, then walk it.”",
        "description": (
            "A is B's father. B is C's mother. D is C's father. E is D's father. "
            "How is A related to E?"
        ),
        "function_name": "deep_relation",
        "signature": "def deep_relation() -> str:",
        "description_full": (
            "Return the relation from A to E.\n\n"
            "Example:\n"
            "  deep_relation() -> 'daughter-in-law'\n\n"
            "Write code that builds the tree and walks it."
        ),
        "test_cases": [
            {"input": [], "expected": "daughter-in-law"},
        ],
        "hidden_test_cases": [
            {"input": [], "expected": "daughter-in-law"},
        ],
        "time_limit_minutes": 8,
        "diamonds": 70,
        "scaffolded_hints": [
            {"level": 1, "text": "A is female? No — A is B's father."},
            {"level": 2, "text": "B is C's mother. D is C's father. So D and B are spouses."},
            {"level": 3, "text": "E is D's father. A is B's father. B is married to D. So A is D's father-in-law? No — A is B's father, so A and D are in-laws. A is male. D is male. E is D's father. So A is E's son-in-law."},
        ],
    },
    "assessment": {
        "title": "Family Tree Final Test",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Prove you can map any chain. Timed.”",
        "description": "Solve three blood-relation puzzles and explain the tree method.",
        "questions": [
            {
                "type": "concept",
                "question": "Pointing to a man: 'He is my father's only son's father.' Who is he?",
                "answer_format": "short_answer",
                "keywords": ["father", "grandfather", "himself", "self"],
                "explanation": "My father's only son is me. My father is the man pointing. So the man is my grandfather.",
            },
            {
                "type": "concept",
                "question": "A is B's brother. B is C's father. How is A related to C?",
                "answer_format": "short_answer",
                "keywords": ["uncle", "aunt", "sibling", "parent"],
                "explanation": "Brother of father = uncle.",
            },
            {
                "type": "debug",
                "code": "def relation(x):\n    return x + 's'\n# should return relation label",
                "error": "relation('father') must return 'father', not 'fathers'.",
                "question": "Fix the relation handler.",
                "fix": "return x",
                "explanation": "The relation is already the correct label; no suffix is needed.",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 100,
    },
    "break": {
        "title": "The Wrong Link",
        "captain_byte_intro": "🧭 **Captain Byte**\n“I gave you a broken logic shortcut. Find the unsafe assumption.”",
        "story": (
            "A puzzle says: A is B's mother. B is C's father. The solver says A is C's "
            "grandmother. What assumption is wrong?"
        ),
        "buggy_code": "def relation(a_to_b, b_to_c):\n    if a_to_b == 'mother':\n        return 'grandmother'\n    return 'unknown'\n\nprint(relation('mother', 'father'))",
        "expected_output": "grandmother",
        "actual_output": "grandmother (this case is accidentally correct)",
        "diagnosis": {
            "question": "Which assumption makes this logic unsafe?",
            "options": [
                {"id": "a", "text": "It assumes gender from one link only", "correct": True, "why": "Mother + father does not always mean grandmother; gender and direction matter."},
                {"id": "b", "text": "The function should use elif", "correct": False, "why": "elif does not fix the logical assumption."},
                {"id": "c", "text": "The return type should be int", "correct": False, "why": "Relation is text."},
                {"id": "d", "text": "print should be removed", "correct": False, "why": "print is fine."},
            ],
        },
        "fix": "return 'grandmother' if a_to_b == 'mother' and b_to_c == 'father' else 'unknown'",
        "fixed_code": "def relation(a_to_b, b_to_c):\n    return 'grandmother' if a_to_b == 'mother' and b_to_c == 'father' else 'unknown'\n\nprint(relation('mother', 'father'))",
        "explanation": (
            "The unsafe shortcut assumed every mother link leads to grandmother. "
            "The safer rule checks both links together."
        ),
    },
    "srs_enrollment": {
        "concept_id": "aptitude:blood_relations",
        "concept_name": "Blood Relations",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "draw the tree: spouse, parent, child, sibling",
            "chain links by reading statements in order",
            "gender is determined by the relation word",
            "shortest path gives the direct relation",
        ],
        "spaced_fields": [
            "tree_order",
            "chain_links",
            "gender_from_relation",
            "shortest_path",
        ],
    },
    "world_progression": {
        "world_id": "aptitude_world",
        "competency_id": "blood_relations",
        "unlocks_next": ["coding_decoding"],
        "tower_badge": "family_tree",
        "world_node": {
            "level": 2,
            "title": "The Family Tree",
            "color": "emerald",
            "icon": "🌳",
            "description": "Map coded family statements into a relation answer",
        },
    },
}
